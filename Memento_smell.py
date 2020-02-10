class User():
    users = list()
    index_users = 0

    def __init__(self, id_user, name, password):
        self._id_user = id_user
        self._name = name
        self._password = password

    def change_name(self, new_name):
        self._name = new_name

    @staticmethod
    def list_users():
        star = '*'
        for user in User.users:
            print(f'\nName: {user._name}\nPassword: {star * len(user._password)}')


class Undo():
    states = list()
    
    @staticmethod
    def save_state():
        Undo.states.append(User.users.copy())
    
    @staticmethod
    def undo():
        current_state = Undo.states.pop()
        while len(current_state) < len(User.users):
            User.users.pop()

        for index, user in enumerate(User.users):
            user._name = current_state[index]._name
            user._password = current_state[index]._password



def menu():
    print('1 - Add user')
    print('2 - List users')
    print('3 - Change user name')
    print('4 - Undo')


def main():
    new_user = User(User.index_users + 1, 'Eduardo', 'Senha')
    User.users.append(new_user)
    while(True):
        menu()
        option = int(input('--> '))

        if option == 1:
            Undo.save_state()
            name = str(input('Name: '))
            password = str(input('Password: '))
            new_user = User(User.index_users + 1, name, password)
            User.users.append(new_user)
            User.index_users += 1
        elif option == 2:
            User.list_users()
        elif option == 3:
            Undo.save_state()
            index = int(input('User id: '))
            try:
                user = User.users[index - 1]
                print(f'Name: {user._name}')
            except IndexError:
                print('Invalid ID!')
            new_name = str(input('New name: '))
            user.change_name(new_name)
        else:
            Undo.undo()


if __name__ == '__main__':
    main()