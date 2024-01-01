from csv import DictReader, DictWriter
from os.path import exists


class LenNumberError(Exception):
    def __init__(self, txt):
        self.txt = txt


def work_with_user(text, user_len=2):
    is_valid = False
    user_data = ''
    while not is_valid:
        try:
            user_data = input(f"{text}: ")
            if len(user_data) < user_len:
                raise LenNumberError("Невалидная длинна!")
            is_valid = True
        except LenNumberError as err:
            print(err)
            continue

    return user_data


def get_info():
    phone_number = 0
    firstname = work_with_user('Введите имя')
    lastname = work_with_user('Введите фамилию')
    is_valid_number = False
    while not is_valid_number:
        try:
            phone_number = int(input("Введите номер: "))
            if len(str(phone_number)) != 11:
                raise LenNumberError("Невалидная длинна!")
            is_valid_number = True
        except ValueError:
            print("Невалидный номер!")
        except LenNumberError as err:
            print(err)
            continue

    return [firstname, lastname, phone_number]


def create_file(file_name):
    with open(file_name, 'w', encoding='utf-8') as data:
        f_writer = DictWriter(data, fieldnames=['Имя', 'Фамилия', 'Телефон'])
        f_writer.writeheader()


def read_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as data:
        f_reader = DictReader(data)

        return list(f_reader)


def write_file(file_name):
    res = read_file(file_name)
    user_data = get_info()
    for el in res:
        if el['Телефон'] == str(user_data[2]):
            print("Указанный номер уже cуществует!")
            return
    obj = {'Имя': user_data[0], 'Фамилия': user_data[1], 'Телефон': user_data[2]}
    res.append(obj)

    with open(file_name, 'w', encoding='utf-8', newline='') as data:
        f_writer = DictWriter(data, fieldnames=['Имя', 'Фамилия', 'Телефон'])
        f_writer.writeheader()
        f_writer.writerows(res)


def copy_row(file_name, new_file_name, row):
    res = read_file(file_name)
    if len(res) < row:
        print("Указанной строки не существует!")
    else:
        if not exists(new_file_name):
            create_file(new_file_name)
        with open(new_file_name, 'w', encoding='utf-8', newline='') as data:
            f_writer = DictWriter(data, fieldnames=['Имя', 'Фамилия', 'Телефон'])
            f_writer.writeheader()
            f_writer.writerow(res[row-1])


file_name = 'phone.csv'
new_file_name = 'phone_copy.csv'


def main():
    while True:
        command = input("Введиет комманду: ")
        if command in ('q', 'й'):
            break
        elif command in ('w', 'ц'):
            if not exists(file_name):
                create_file(file_name)
            write_file(file_name)
        elif command in ('r', 'к'):
            if not exists(file_name):
                print('Файл для чтения не существует! Создайте файл.')
                continue
            print(*read_file(file_name))
        elif command in ('c', 'с'):
            if not exists(file_name):
                print('Файл для чтения не существует! Создайте исходный файл.')
                continue
            row_copy = int(work_with_user("Укажите номер строки для копирования", 1))
            copy_row(file_name, new_file_name, row_copy)


main()
