from functools import wraps

from birthdays import Record
from storage import load_data, save_data


def input_error(handler):
    @wraps(handler)
    def wrapped(args, book):
        try:
            return handler(args, book)
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Enter the argument for the command."
        except ValueError as error:
            return str(error)

    return wrapped


def parse_input(line):
    command, *args = line.split() or [""]
    return command.lower(), args


def require_contact(book, name):
    record = book.find(name)
    if record is None:
        raise KeyError(name)
    return record


@input_error
def add_contact(args, book):
    if len(args) != 2:
        raise ValueError("Give me name and phone please.")
    name, number = args
    record = book.find(name)
    if record is None:
        record = Record(name)
        record.add_phone(number)
        book.add_record(record)
        return "Contact added."
    record.add_phone(number)
    return "Contact updated."


@input_error
def change_contact(args, book):
    if len(args) != 3:
        raise ValueError("Give me name, old phone and new phone please.")
    name, old_number, new_number = args
    require_contact(book, name).edit_phone(old_number, new_number)
    return "Contact updated."


@input_error
def show_phone(args, book):
    if len(args) != 1:
        raise ValueError("Enter user name.")
    record = require_contact(book, args[0])
    return "; ".join(str(phone) for phone in record.phones) or "No phones."


@input_error
def show_all(args, book):
    if args:
        raise ValueError("This command does not take arguments.")
    return "\n".join(str(record) for record in book.values()) or "No contacts."


@input_error
def add_birthday(args, book):
    if len(args) != 2:
        raise ValueError("Give me name and birthday please.")
    name, birthday = args
    require_contact(book, name).add_birthday(birthday)
    return "Birthday added."


@input_error
def show_birthday(args, book):
    if len(args) != 1:
        raise ValueError("Enter user name.")
    birthday = require_contact(book, args[0]).birthday
    return str(birthday) if birthday is not None else "No birthday set."


@input_error
def birthdays(args, book):
    if args:
        raise ValueError("This command does not take arguments.")
    return "\n".join(
        f"{entry['name']}: {entry['congratulation_date']}"
        for entry in book.get_upcoming_birthdays()
    ) or "No upcoming birthdays."


def main():
    book = load_data()
    handlers = {
        "add": add_contact,
        "change": change_contact,
        "phone": show_phone,
        "all": show_all,
        "add-birthday": add_birthday,
        "show-birthday": show_birthday,
        "birthdays": birthdays,
    }
    print("Welcome to the assistant bot!")
    while True:
        try:
            line = input("Enter a command: ")
        except (EOFError, KeyboardInterrupt):
            save_data(book)
            print("\nGood bye!")
            break
        command, args = parse_input(line)
        if command in ("close", "exit"):
            save_data(book)
            print("Good bye!")
            break
        if command == "hello":
            print("How can I help you?")
        elif command in handlers:
            print(handlers[command](args, book))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
