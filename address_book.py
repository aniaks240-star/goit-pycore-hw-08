from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Enter a name.")
        super().__init__(value.strip())


class Phone(Field):
    def __init__(self, value):
        if not isinstance(value, str) or len(value) != 10 or not value.isascii() or not value.isdigit():
            raise ValueError("Phone must contain 10 digits.")
        super().__init__(value)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, number):
        phone = Phone(number)
        if self.find_phone(number) is None:
            self.phones.append(phone)

    def find_phone(self, number):
        for phone in self.phones:
            if phone.value == number:
                return phone
        return None

    def remove_phone(self, number):
        phone = self.find_phone(number)
        if phone is None:
            raise ValueError("Phone not found.")
        self.phones.remove(phone)

    def edit_phone(self, old_number, new_number):
        phone = self.find_phone(old_number)
        if phone is None:
            raise ValueError("Phone not found.")
        replacement = Phone(new_number)
        if old_number != new_number and self.find_phone(new_number) is not None:
            raise ValueError("Phone already exists.")
        self.phones[self.phones.index(phone)] = replacement

    def __str__(self):
        phones = "; ".join(str(phone) for phone in self.phones)
        return f"Contact name: {self.name}, phones: {phones}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        del self.data[name]
