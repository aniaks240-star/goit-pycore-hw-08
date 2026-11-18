from datetime import date, datetime, timedelta

from address_book import AddressBook as BaseAddressBook
from address_book import Field, Name, Phone, Record as BaseRecord


class Birthday(Field):
    def __init__(self, value):
        try:
            parsed = datetime.strptime(value, "%d.%m.%Y").date()
            if parsed.strftime("%d.%m.%Y") != value:
                raise ValueError
        except (TypeError, ValueError):
            raise ValueError("Invalid date format. Use DD.MM.YYYY") from None
        super().__init__(parsed)

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")


class Record(BaseRecord):
    def __init__(self, name):
        super().__init__(name)
        self.birthday = None

    def add_birthday(self, value):
        self.birthday = Birthday(value)


class AddressBook(BaseAddressBook):
    def get_upcoming_birthdays(self, today=None):
        today = date.today() if today is None else today
        upcoming = []
        for record in self.data.values():
            if record.birthday is None:
                continue
            birthday = record.birthday.value
            for year in (today.year, today.year + 1):
                try:
                    celebration = birthday.replace(year=year)
                except ValueError:
                    celebration = date(year, 2, 28)
                if celebration >= today:
                    break
            if (celebration - today).days >= 7:
                continue
            if celebration.weekday() in (5, 6):
                celebration += timedelta(days=7 - celebration.weekday())
            upcoming.append((celebration, record.name.value))
        return [
            {"name": name, "congratulation_date": day.strftime("%d.%m.%Y")}
            for day, name in sorted(upcoming)
        ]
