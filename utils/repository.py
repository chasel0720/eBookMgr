from sqlmodel import Session, SQLModel, create_engine, select
from define.Book import Book
from define.Config import DBFile

class Repository:
    def __init__(self):
        self.engine = create_engine(DBFile)
        SQLModel.metadata.create_all(self.engine)

    def create(self,book):
        with Session(self.engine) as session:
            session.add(book)
            session.commit()

    def bulk_create(self,books):
        with Session(self.engine) as session:
            for book in books:
                session.add(book)
            session.commit()

    def get_all(self):
        with Session(self.engine) as session:
            statement = select(Book)
            return session.exec(statement).all()

    def get_by_name(self,name):
        with Session(self.engine) as session:
            statement = select(Book).where(Book.name.lower() == name.lower())
            return session.exec(statement).first()

    def get_by_id(self,id):
        with Session(self.engine) as session:
            statement = select(Book).where(Book.id == id)
            return session.exec(statement).first()

    def update(self,book):
        with Session(self.engine) as session:
            db_book = session.get(Book, book.id)
            if db_book:
                for key, value in book.dict().items():
                    setattr(db_book, key, value)
                session.add(db_book)
                session.commit()

    def delete(self,id):
        with Session(self.engine) as session:
            book = session.get(Book, id)
            if book:
                session.delete(book)
                session.commit()

repository = Repository()