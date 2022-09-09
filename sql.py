from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Integer, Sequence
from sqlalchemy.orm import sessionmaker



engine = create_engine('sqlite:///database.sqlite', echo=True)
base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()
class books(base):
	__tablename__ = 'book'

	id = Column(Integer,Sequence('book_id_seq'), primary_key=True)
	book = Column(String)

	def __repr__(self):
		return f"{self.book}"


class user(base):
	__tablename__ = 'user'

	id = Column(Integer,Sequence('user_id_seq'), primary_key=True)
	name = Column(String(60))
	username = Column(String(20))
	gender = Column(String(60))
	age = Column(Integer)
	password = Column(String(12))

	def __repr__(self):
		return f"{self.name}"


class borrowed(base):
	__tablename__ = 'borrowed'

	id = Column(Integer, Sequence("borrowed_books_id_seq"), primary_key=True)
	book = Column(String)
	user = Column(String)

	def __repr__(self):
		return f"{self.id} = {self.book} by {self.user}"


base.metadata.create_all(engine)