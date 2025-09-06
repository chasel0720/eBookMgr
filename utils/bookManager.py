import os
import shutil
from typing import List
from define import Config
from define.Book import Book
from pathlib import Path
from define.Status import Status
from utils.repository import repository as repo
from py_linq import Enumerable

def import_folder(path, tag):
    folder = Path(path)
    if not folder.is_dir() or not folder.exists():
        raise FileNotFoundError(f"{path} is not a directory or does not exist")
    folder = Path(path)
    files = ((Enumerable(folder.glob("*"))
             .where(lambda f: f.is_file())
             .where(lambda f: f.suffix.lower() == ".pdf"))
             .to_list())
    books:List[Book] = []
    for f in files:
        books.append(create_book(f,tag))
        copy_book_to_lib(f)
    repo.bulk_create(books)

def create_book(path,tag)->Book:
    book = Book()
    book.name = Path(path).name
    book.tag = tag
    return book

def import_file(path, tag):
    file = Path(path)
    if not file.is_file() or not file.exists():
        raise FileNotFoundError(f"{path} is not a file or does not exist")
    book = create_book(path,tag)
    repo.create(book)
    copy_book_to_lib(path)

def move_or_copy_book(file_path, target_folder_path, copy):
    target_folder = Path.cwd() / target_folder_path
    if target_folder and not target_folder.exists():
        os.makedirs(target_folder, exist_ok=True)
    target_file_path = target_folder / Path(file_path).name
    if copy:
        shutil.copy2(file_path, target_file_path)
    else:
        shutil.move(file_path, target_file_path)

def copy_book_to_lib(file_path):
    move_or_copy_book(file_path,Config.LibPath,True)

def move_book_to_archive(file_path):
    move_or_copy_book(file_path,Config.Lib_Archive,False)

def archive_book(book):
    book.status = Status.ARCHIVE
    repo.update(book)
    file_path = os.path.join(Path.cwd(), Config.LibPath, str(book.name))
    move_book_to_archive(file_path)


def modify_tag(self, book, tag):
    pass

def unarchive_book(book):
    pass


def list_all_unarchived_books():
    all_books = repo.get_all()
    books_archived = (Enumerable(all_books)
                      .where(lambda b: b.status == Status.ARCHIVE)
                      .select(lambda b: b.name)
                      .to_list())

    print(books_archived)


def list_books(tag):
    books = Enumerable(repo.get_all()).where(lambda b: b.tag.lower() == tag.lower()).select(lambda b: b.name).to_list()
    print(books)


def list_tags():
    all_tags = Enumerable(repo.get_all()).select(lambda b: b.tag.lower()).distinct().to_list()
    print(all_tags)


def open_book_by_name(name):
    file_path = os.path.join(Path.cwd(), Config.LibPath, name)
    open(file_path)

def open_book_by_id(id):
    book = repo.get_by_id(id)
    open_book_by_name(book.name)


def remove_book_by_id(id):
    book = repo.get_by_id(id)
    repo.delete(book)
    delete_book_from_lib(book.name)


def remove_book_by_name(name):
    book = repo.get_by_name(name)
    repo.delete(book)
    delete_book_from_lib(book.name)

def delete_book_from_lib(name):
    file_path = os.path.join(Path.cwd(), Config.LibPath, name)
    os.remove(file_path)