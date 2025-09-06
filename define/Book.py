from define.Status import Status
from sqlmodel import Field, SQLModel
import uuid
import datetime

class Book(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, unique=True, primary_key=True)
    name: str = Field(nullable=False,unique=True,index=True)
    author: str = Field(default="unknow")
    status: Status = Field(default=Status.NEW)
    bookMark: int = Field(default=0)
    createdAt: datetime.datetime = Field(default=datetime.datetime.now())
    latestReadAt: datetime.datetime = Field(default=datetime.datetime.now())
    tag: str = Field(default="",nullable=True)
