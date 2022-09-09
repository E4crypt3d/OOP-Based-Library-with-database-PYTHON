from sql import session
from sql import books,user, borrowed
from passlib.hash import pbkdf2_sha256

class Student:
	def __init__(self,username, passwd):
		self.username = username
		self.password = passwd

	def login(self):
		if session.query(user).filter_by(username=self.username).first() is not None:
			current_user = session.query(user).filter_by(username = self.username).first()
			if pbkdf2_sha256.verify(self.password, current_user.password):
				print(f"Welcome the to New OOP Library, {current_user.name}")
			else:
				print("\nIncorrect Account Details")
				exit()
		else:
			print("\nIncorrect Login Details")
			exit()

	def signup(name, username, gender, age , password):
		new_pass = pbkdf2_sha256.hash(password)
		if session.query(user).filter_by(username=username).first() is not None:
			print("Username not available for now")
			exit()
		new_user = user(name=name, username=username,gender=gender,age=age,password=new_pass)
		session.add(new_user)
		session.commit()

class Books(Student):
	def __init__(self,avail,username, passwd):
		super().__init__(username, passwd)
		self.username = username
		self.password = passwd
		self.books = avail

	def ShowAvailableBooks(self):
		print("\nAvailable Books in the Library at the moment")
		for no, b in enumerate(self.books, 1):
			print(f"{no} = {b}")


	def BorrowBook(self, requestedBook):
		if requestedBook in self.books:
			borrowing = borrowed(book = requestedBook, user = self.username)
			session.query(books).filter_by(book = requestedBook).delete()
			session.commit()
			print(f'\n{requestedBook} has been issued to you, Please return the book after 5 days. Thanks for visiting us')
		else:
			print('\nThis book is not available at the moment, Thanks for visiting us')

	def returnBook(self, returnit):
		try:
			borrow = session.query(borrowed).filter_by(book = returnit).first()
			if self.username == borrow.user:
				r = books(book= returnit)
				session.add(r)
				session.query(borrowed).filter_by(book = returnit).delete()
				session.commit()
				print("Thanks for returning the Book have a Great Day")
			else:
				print("Incorrect Book")
		except Exception:
			print("Incorrect Book")

			
	#adding a add book function
	def add_book(self, book):
		if self.username == "admin":
			password = input("Please Enter your password: ")
			adminpass = session.query(user).filter_by(username = self.username).first()
			if pbkdf2_sha256.verify(password, adminpass.password):
				new_book = books(book = book)
				session.add(new_book)
				session.commit()
				print(f"Book '{book}' added to the Library")
			else:
				print("Admin password incorrect")
		else:
			print("Access not allowed")
			exit()

if __name__ == "__main__":
	print("Login or Sign Up")
	print("1 = Login\n2 = Sign up")
	new_user_or_not = input("Please Choose a option: ")
	if new_user_or_not == "1":
		username = input('Username here : ')
		passwd = input('passwd here: ')
	elif new_user_or_not == "2":
		name = input("Name: ")
		username = input("Username: ")
		gender = input("Gender: ")
		age = input("Age: ")
		email = input("Email: ")
		passwd = input("Password: ")
		Student.signup(name, username, gender, age, passwd)
	listed = []
	for i in session.query(books).all():
		listed.append(str(i))
	data = Books(listed, username, passwd)
	data.ShowAvailableBooks()
	data.login()
	while True:
		if username.lower() != 'admin':
			print('''Choose a option?\n1 = Show available books\n2 = Borrow a Book\n3 = Return a Book\nType "exit" to exit out of Library''')
		else:
			print('''Choose a option?\n1 = Show available books\n2 = Borrow a Book\n3 = Return a Book\n4 = Add a Book\nType "exit" to exit out of Library''')
		ui = input("What do you wanna do: ")
		if ui == '1':
			listed = []
			for i in session.query(books).all():
				listed.append(str(i))
				data = Books(listed, username, passwd)
			data.ShowAvailableBooks()
		elif ui == '2':
			b = input("Enter the book you wanna borrow: ")
			data.BorrowBook(b)
		elif ui == '3':
			b = input("Enter the book name you wanna return: ")
			data.returnBook(b)
		elif ui.lower() == 'exit':
			print('Thanks for Using OOP Library')
			exit()
		if username.lower() == 'admin':
			if ui == '4':
				b = input("Add a book: ")
				data.add_book(b)
		