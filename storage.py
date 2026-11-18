import os
import pickle
from pathlib import Path
from tempfile import NamedTemporaryFile

from birthdays import AddressBook


def save_data(book, filename="addressbook.pkl"):
    destination = Path(filename)
    temporary_path = None
    try:
        with NamedTemporaryFile(mode="wb", dir=destination.parent, delete=False) as file:
            temporary_path = Path(file.name)
            pickle.dump(book, file, protocol=pickle.HIGHEST_PROTOCOL)
            file.flush()
            os.fsync(file.fileno())
        temporary_path.replace(destination)
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)


def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as file:
            book = pickle.load(file)
    except FileNotFoundError:
        return AddressBook()
    if not isinstance(book, AddressBook):
        raise ValueError("The file does not contain an address book.")
    return book
