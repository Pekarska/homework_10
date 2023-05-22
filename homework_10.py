from collections import UserDict


class Field:
    value = ''


class NameField(Field):
    def __init__(self, name):
        self.value = name


class PhoneField(Field):
    def __init__(self, phone):
        self.value = phone


class Record:
    name: NameField = None

    def __init__(self, n: NameField):
        self.name = NameField(n)
        self.phones = []

    def add_phone(self, number: str):
        phone = PhoneField(number)
        self.phones.append(phone)

    def delete_phone(self, number: str):
        for s in self.phones:
            if s.value == number:
                self.phones.remove(s)
                break

    def clear_phones(self):
        self.phones.clear()


class AddressBook(UserDict):
    def add_record(self, r: Record):
        self.data[r.name.value] = r


def input_error(func):
    def inner(command, *inputs):
        if command == 'add' or command == 'change':
            if inputs and len(inputs) == 2:
                return func(*inputs)
            else:
                return 'Give me name and phone please'
        if command == 'phone':
            if inputs and len(inputs) == 1:
                return func(*inputs)
            else:
                return 'Enter user name'
        if command == 'hello':
            if len(inputs) > 0:
                return func(inputs[0])
            return func(None)
        if command == 'show':
            if inputs and len(inputs) == 1:
                return func(*inputs)
            else:
                return 'Show must be with parameter `all` or name'

        return 'Not correct validation'

    return inner


book = AddressBook()


@input_error
def hello(n):
    if n is None:
        return "How can I help you?"
    else:
        return "Hello " + n + ", how can I help you?"


@input_error
def adding(name, phone):
    person = Record(name)
    person.add_phone(phone)
    book.add_record(person)
    return 'add completed'


@input_error
def change(n, p):
    for name in book.keys():
        if name.lower() == n.lower():
            record = book[name]
            record.clear_phones()
            record.add_phone(p)
            return 'Number is changed'
    return 'Name is not found'


@input_error
def show(n):
    info_line = ''

    def print_record(r: Record):
        if len(r.phones) == 1:
            return name + '\t| ' + r.phones[0].value + '\n'
        else:
            return name + '\t| ' + ', '.join(x.value for x in r.phones) + '\n'

    if n == 'all':
        for name, record in book.items():
            info_line += print_record(record)
    else:
        for name, record in book.items():
            if n.lower() in name.lower():
                info_line += print_record(record)
    return info_line


commands = {
    'hello': hello,
    'hi': hello,
    'add': adding,
    'show': show,
    'change': change,
}

exit_commands = [
    'good bye',
    'exit',
    'close'
]


def main_example():
    while True:
        command, *data = input().strip().split(' ', 1)
        if command in exit_commands:
            print('Good Bye!')
            break
        elif (handler := commands.get(command)) is not None:
            if data:
                data = data[0].split(',')
            result = handler(command, *data)
        else:
            result = "Not correct command"
        print(result)


if __name__ == "__main__":
    main_example()
