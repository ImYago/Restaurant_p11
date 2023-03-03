import os
import json
from colorama import Fore
import datetime


cu = 0


class Restaurant:
    # create json files
    @staticmethod
    def create_json():
        if not os.path.exists('products.json'):
            with open('products.json', 'w') as f:
                f.write('[]')

        if not os.path.exists('users.json'):
            with open('users.json', 'w') as f:
                f.write('[]')

    create_json()

    # order history
    @staticmethod
    def order_history():
        with open("users.json", "r") as f:
            e = json.load(f)

            for i in e:
                if i["id"] == str(cu):
                    print(f'history: {i["order history"]}')

    # check user
    @staticmethod
    def check_user(username, password):
        with open('users.json', 'r') as f:
            file = json.load(f)

            for i in file:
                if i["username"].lower() == username.lower() and i["password"].lower() == password.lower():
                    cu = i["username"]
                    return True
                else:
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

    def add_food(self):
        print(Fore.RED + '[default product type: "food"]')
        p_id = self.make_p_id()
        name = input(Fore.CYAN + 'Product name: ')
        price = input(Fore.MAGENTA + 'Product price: ')
        quantity = int(input(Fore.LIGHTRED_EX + 'Product quantity: '))

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

    def add_drink(self):
        print(Fore.RED + '[default product type: "drink"]')
        p_id = self.make_p_id()
        name = input(Fore.CYAN + 'Product name: ')
        price = input(Fore.MAGENTA + 'Product price: ')
        quantity = int(input(Fore.LIGHTRED_EX + 'Product quantity: '))

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

    @staticmethod
    def report():
        print(Fore.RED + 'This page not finished')
        pass

    # enterance
    def enterance(self):
        print(cu, type(cu))
        enterance_text = '''
            1. Login
            2. add food
            3. add drink
            4. report
            5. exit
            : '''
        selection = input(Fore.BLUE + enterance_text)
        if selection == '1':
            self.login()
        elif selection == '2':
            self.add_food()
        elif selection == '3':
            self.add_drink()
        elif selection == '4':
            self.report()
        elif selection == '5':
            print(Fore.CYAN + "https://www.pdp.uz")
            exit()
        else:
            print(Fore.YELLOW + 'selection not exist')
        self.enterance()

    # sign up
    def signup(self, username, password):
        with open("users.json", "r") as f:
            file = json.load(f)

        u_id = self.make_u_id()
        new_user = {
            "id": u_id,
            "username": username,
            "password": password,
            "order history": []
        }
        file.append(new_user)
        with open("users.json", "w") as f:
            json.dump(file, f, indent=2)

    # login
    def login(self):
        username = input(Fore.GREEN + 'Enter username: ')
        password = input(Fore.GREEN + 'Enter password: ')

        if self.check_user(username, password):
            print(Fore.GREEN + 'Successfully logged in!')
            self.dining_menu()
        else:
            sign_up = input(Fore.YELLOW + 'User not found !\nWould you sign up?\n[y/n]: ')
            if sign_up.lower() in ['yes', 'y', 'yep']:
                self.signup(username, password)
                print(Fore.GREEN + 'Sign up successfully')
            else:
                self.enterance()

    # add information to the history
    @staticmethod
    def add_to_history(p_name, p_price, p_quantity):
        with open("users.json", "r") as d:
            users_file = json.load(d)
            print(type(users_file))

            res = f" product: {p_name} , price: {p_price} - {p_quantity}x, time: {datetime.datetime.now()}"

            for i in users_file:
                if i["id"] == cu:
                    i["order history"].append(res)

        with open("users.json", "w") as f:
            json.dump(users_file, f, indent=2)

    @staticmethod
    def get_food():
        with open("products.json", "r") as f:
            t = json.load(f)
            for i in t:
                if i["product type"] == "food":
                    print(Fore.LIGHTGREEN_EX + f'{i["product id"]} {i["product name"]} ~~ {i["product price"]}')

            sf = input(Fore.LIGHTCYAN_EX + '$ ')
            for i in t:
                if i["product id"] == sf:
                    if i["product type"] == "food":
                        print(Fore.LIGHTGREEN_EX + f'{i["product name"]} |=> {i["product price"]}')
            ays = int(input(Fore.RESET + 'how much do you want?\n$ '))
            if ays == int(ays):

                for i in t:
                    if ays >= i["quantity"]:
                        if i["product id"] == sf:
                            i["quantity"] -= ays

            with open("products.json", "w") as z:
                json.dump(t, z, indent=2)
        print(Fore.GREEN + "successfully ordered products")

    @staticmethod
    def get_drink():
        with open("products.json", "r") as f:
            t = json.load(f)
            for i in t:
                if i["product type"] == "drink":
                    print(Fore.LIGHTGREEN_EX + f'{i["product id"]} {i["product name"]} ~~ {i["product price"]}')

            sf = input(Fore.LIGHTCYAN_EX + '$ ')
            for i in t:
                if i["product id"] == sf:
                    if i["product type"] == "drink":
                        print(Fore.LIGHTGREEN_EX + f'{i["product name"]} |=> {i["product price"]}')
            ays = int(input(Fore.RESET + 'how much do you want?\n$ '))
            if ays == int(ays):

                for i in t:
                    if ays >= int(i["quantity"]):
                        if i["product id"] == sf:
                            print(type(i["quantity"]))
                            i["quantity"] -= ays

            with open("products.json", "w") as z:
                json.dump(t, z, indent=2)
        print(Fore.GREEN + "successfully ordered products")

    # order food and quantity - x
    def order_food(self):
        print(Fore.CYAN + "1. Order food\n2. Order drink")
        st = int(input(Fore.BLUE + '$ '))
        if st == int(st):
            if st == 1:
                self.get_food()
            elif st == 2:
                self.get_drink()

    # dining menu
    def dining_menu(self):
        menu = '''
        1. order food
        2. history
        3. exit\n$ 
        '''
        s = input(Fore.MAGENTA + menu)
        if s == '1':
            self.order_food()
            self.dining_menu()
        elif s == '2':
            self.order_history()
            self.dining_menu()
        elif s == '3':
            self.enterance()


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
#~1  If json file is empty, return empty warnings
"""
# ---------------------------------------------------------->
