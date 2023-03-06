import os
import json
from colorama import Fore
import datetime

"""
shop

magazin
restaranga oxshash + (product soni)

----------------------------------------------------------------
restaran

1 login
2 ovqat qoshish
3 ichimlik qoshish
4 hisobot

* botirjon01
* -mijoz

* 1. ovqatga buyurtma
* 2. oldingi buyurtmalari
* 3. exit
"""


class Restaurant:
    # simple variables
    def __init__(self):
        self.current_user = 0

    # create json files
    @staticmethod
    def create_json():
        if not os.path.exists('products.json'):
            with open('products.json', 'w') as f:
                f.write('[]')

        if not os.path.exists('users.json'):
            with open('users.json', 'w') as f:
                f.write('[]')

    # order history
    def order_history(self):
        with open("users.json", "r") as f:
            e = json.load(f)

            for i in e:
                if i["id"] == self.current_user:
                    print(f'history: {i["order history"]}')

                else:
                    print(Fore.YELLOW + "id not found")

    # check user
    def check_user(self):

        username = input(Fore.RESET + "Enter username: ")
        password = input(Fore.RESET + "Enter password: ")

        with open('users.json', 'r') as f:
            file = json.load(f)
            for i in file:
                if i["username"] == username and i["password"] == password:
                    self.current_user = int(i["id"])
                    return True
            return False

    @staticmethod
    def make_p_id():
        with open('products.json', 'r') as f:
            e = json.load(f)
            return len(e) + 1

    @staticmethod
    def make_u_id():
        with open('users.json', 'r') as f:
            e = json.load(f)
            return len(e) + 1

    # add food
    def add_food(self):
        print(Fore.RED + '[default product type: "food"]')
        p_id = self.make_p_id()
        name = input(Fore.CYAN + 'Food name: ')
        price = input(Fore.MAGENTA + 'Food price: ')
        quantity = int(input(Fore.LIGHTRED_EX + 'Food quantity: '))

        d = {
            "product type": "food",
            "product id": p_id,
            "product name": name,
            "product price": price,
            "quantity": quantity
        }
        with open("products.json", "r") as g:
            s = json.load(g)

        s.append(d)

        with open("products.json", "w") as f:
            json.dump(s, f, indent=2)

    # add drink
    def add_drink(self):
        print(Fore.RED + '[default product type: "drink"]')
        p_id = self.make_p_id()
        name = input(Fore.CYAN + 'Drink name: ')
        price = input(Fore.MAGENTA + 'Drink price: ')
        quantity = int(input(Fore.LIGHTRED_EX + 'Drink quantity: '))

        d = {
            "product type": "drink",
            "product id": p_id,
            "product name": name,
            "product price": price,
            "quantity": quantity
        }
        with open("products.json", "r") as g:
            s = json.load(g)

        s.append(d)

        with open("products.json", "w") as f:
            json.dump(s, f, indent=2)

    # report (last order)
    def report(self):
        with open("users.json", "r") as f:
            print(self.current_user)
            f = json.load(f)
            for i in f:
                if i["id"] == self.current_user:
                    j = i["order history"]
                    if len(j) >= 1:
                        print(f'last: {j[-1]}')
                        break
                    else:
                        print(Fore.LIGHTCYAN_EX + 'history not found')
                        break

                else:
                    print(Fore.YELLOW + "user not signed , please sign in for use report")
                    break

    # username checking
    @staticmethod
    def check_username(username):
        with open("users.json", "r") as f:
            file = json.load(f)

            for i in file:
                if username == i['username']:
                    return True
            return False

    # login
    def login(self):
        if self.check_user():
            print(Fore.GREEN + 'Success!')
            return True
        else:
            sign_up = input(Fore.YELLOW + 'Password or username incorrect!\n'
                                          'Would you try again? [y/n]\n'
                                          ': ')
            if sign_up.lower() in ['yes', 'y', 'yep', 'ha', 'yeah']:
                return self.login()

        return False

    # sign up
    def signup(self):
        username = input('Enter username: ')
        password = input('Enter password: ')

        if not self.check_username(username):
            with open("users.json", "r") as f:
                file = json.load(f)

            u_id = self.make_u_id()
            self.current_user = int(u_id)

            new_user = {
                "id": u_id,
                "username": username,
                "password": password,
                "order history": []
            }
            file.append(new_user)
            with open("users.json", "w") as f:
                json.dump(file, f, indent=2)
            return True
        else:
            print(Fore.YELLOW + 'Username already taken')
            self.signup()

    def sign(self):
        print(Fore.GREEN + '1. Sign In \n'
                           '2. Sign Up \n'
                           '3. exit')
        s = input(Fore.LIGHTGREEN_EX + '$ ')

        if not s.isalpha():
            # Log in
            if int(s) == 1:
                return self.login()

            # Sign up
            elif int(s) == 2:
                if self.signup():
                    print(Fore.LIGHTGREEN_EX + 'Success !')
                    return True
        return False

    # add information to the history
    def add_to_history(self, p_name, p_price, p_quantity):
        with open("users.json", "r") as d:
            users_file = json.load(d)
            time = datetime.datetime.now()
            res = [p_name, p_price, p_quantity, str(time)]

            for i in users_file:
                print(self.current_user)
                if i["id"] == self.current_user:
                    i["order history"].append(res)
                    print(i["order history"])

        with open("users.json", "w") as f:
            json.dump(users_file, f, indent=2)

    # get food
    def get_food(self, _type):
        with open("products.json", "r") as f:
            products = json.load(f)
            if len(products) >= 1:
                for i, v in enumerate(products):
                    if v["type"] == _type:
                        items = products[i]["items"]
                        item_id = i
                        for product in v["items"]:
                            print(Fore.LIGHTGREEN_EX + f'+------------------------------+\n'
                                                       f'{product["id"]}. {product["name"]} ~~ {product["price"]} ~~ '
                                                       f'{"in stock" if product["quantity"] else "out of stock"} '
                                                       f'\n'
                                                       f'+------------------------------+\n')
                order_id = int(input(Fore.LIGHTCYAN_EX + '$ '))

                for i, v in enumerate(items):
                    if v["id"] == order_id:
                        print(Fore.LIGHTGREEN_EX + f'{v["name"]} |=> {v["price"]}')
                        count = int(input(Fore.RESET + 'how much do you want?\n$ '))
                        while count > v["quantity"]:
                            count = int(input(Fore.RESET + f'how much do you want? {0} for exit\n$ '))
                        if count < 1:
                            return False
                        self.add_to_history(v["name"], v["price"], count)
                        products[item_id]['items'][i]["quantity"] -= count
                        with open("products.json", "w") as z:
                            json.dump(products, z, indent=2)
                        print(Fore.GREEN + "successfully ordered products")
                        return True

        print('foods  not found')
        return False

    # order food and quantity - x
    def order_food(self):
        actions = {
            1: 'food',
            2: 'drink',
        }
        print(Fore.CYAN + "1. Order food \n"
                          "2. Order drink \n"
                          "3. exit")
        st = int(input(Fore.BLUE + '$ '))
        if 0 < st < 3:
            return self.get_food(actions[st])
        if st == 3:
            return False
        print(Fore.YELLOW + "selection failed")
        self.order_food()

    # the enterance
    def enterance(self):
        self.create_json()
        enterance_text = '''
                        1. Sign
                        2. add food
                        3. add drink
                        4. report
                        5. exit
                        : '''
        selection = input(Fore.BLUE + enterance_text)
        if selection == '1':
            if self.sign():
                self.main_menu()
            else:
                self.enterance()
        elif selection == '2':
            self.add_food()
            self.enterance()
        elif selection == '3':
            self.add_drink()
            self.enterance()
        elif selection == '4':
            self.report()
            self.enterance()
        elif selection == '5':
            print(Fore.CYAN + "YOUR ADS HERE!")
            exit()
        else:
            print(Fore.YELLOW + 'selection not exist')
            self.enterance()

    # dining menu
    def main_menu(self):
        menu = '''
                        1. order food
                        2. history
                        3. exit\n$ '''
        s = input(Fore.MAGENTA + menu)
        if s == '1':
            if self.order_food():
                self.main_menu()
            else:
                self.main_menu()
        elif s == '2':
            self.order_history()
            self.main_menu()
        elif s == '3':
            self.enterance()
        else:
            print(Fore.YELLOW + 'selection not exist | Project/Dining_menu/else')


# ----------------------------------------------------------------
a = Restaurant()
a.enterance()
# ----------------------------------------------------------------

# if you finish project test all functions, don't forget testing
# create_json() --> X
# order_history() --> X
# check_user() --> X
# enterance() --> X
# signup() --> X
# login() --> X
# add_to_history() --> X
# order_food() --> X
# dining_menu() --> X

# check generating id --> X

# ---------------------( PROBLEMS / BUGS )------------------>
"""
errors: in home page
"""
# ---------------------------------------------------------->
