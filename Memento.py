from datetime import datetime
from abc import ABC, abstractmethod

class User():
    users = list()
    index_users = 0

    _state = None

    def __init__(self, id_user, name, password):
        self._id_user = id_user
        self._name = name
        self._password = password
        self._state = [id_user, name]

    def change_name(self, new_name):
        self._name = new_name
        self._state = [self._id_user, new_name]

    def save(self):
        return ConcreteMemento(self._state)

    def restore(self, memento):
        self._state = memento.get_state()
        for user in User.users:
            if user._id_user == self._state[0]:
                user._name = self._state[1]
                break

    @staticmethod
    def list_users():
        star = '*'
        for user in User.users:
            print(f'\nName: {user._name}\nPassword: {star * len(user._password)}')


class Memento(ABC):

    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def get_date(self):
        pass


class ConcreteMemento(Memento):
    
    def __init__(self, state = None):
        self._state = state
        self._date = str(datetime.now())[:19]

    def get_state(self):
        return self._state
    
    def get_name(self):
        return f'{self._date} / {self._state[0], self._state[1]}'

    def get_date(self):
        return self._date


class Caretaker():

    def __init__(self, originator):
        self._mementos = []
        self._originator = originator

    def backup(self):
        print("\n\nCaretaker: Saving Originator's state...")
        self._mementos.append(self._originator.save())

    def undo(self):
        if not len(self._mementos):
            return
    
        memento = self._mementos.pop()
        print(f"\nCaretaker: Restoring state to: {memento.get_name()}")
        try:
            self._originator.restore(memento)
        except Exception:
            self.undo()
    
    def show_history(self):
        for memento in self._mementos:
            print(memento.get_name())


def menu():
    print('1 - Add user')
    print('2 - List users')
    print('3 - Change user name')
    print('4 - Undo')


def main():
    new_user = User(User.index_users + 1, 'Eduardo', 'Senha')
    User.index_users += 1
    User.users.append(new_user)
    caretaker = Caretaker(new_user)
    while(True):
        menu()
        option = int(input('--> '))

        if option == 1:
            name = str(input('Name: '))
            password = str(input('Password: '))
            new_user = User(User.index_users + 1, name, password)
            User.users.append(new_user)
            User.index_users += 1
            caretaker = Caretaker(new_user)
        elif option == 2:
            User.list_users()
        elif option == 3:
            caretaker.backup()
            index = int(input('User id: '))
            try:
                user = User.users[index - 1]
                print(f'Name: {user._name}')
            except IndexError:
                print('Invalid ID!')
            new_name = str(input('New name: '))
            user.change_name(new_name)
        else:
            caretaker.undo()
    
        if option != 2:
            print()
            caretaker.show_history()


if __name__ == '__main__':
    main()