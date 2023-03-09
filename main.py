import os
import json
from colorama import Fore
import datetime


class Restaurant:
    # simple variables
    def __init__(self):
        self.current_user = 0

    # create json files
    @staticmethod
    def create_json():
        # create json files for products
        if not os.path.exists('products.json'):
            with open('products.json', 'w') as f:
                t = '[\n' \
                    '   {\n' \
                    '       "type": "food",\n' \
                    '       "items": []\n' \
                    '   },\n' \
                    '   {\n' \
                    '       "type": "drink",\n' \
                    '       "items": []\n' \
                    '   }\n' \
                    ']'
                f.write(t)
        # create json files for users
        if not os.path.exists('users.json'):
            with open('users.json', 'w') as f:
                f.write('[]')

    # order history
    def order_history(self):
        with open("users.json", "r") as f:
            e = json.load(f)

            for i in e:
                if i["id"] == self.current_user:
                    all_history = i["order history"]

                    if len(all_history) > 0:
                        for order in all_history:
                            print(order)
                    else:
                        print(Fore.LIGHTYELLOW_EX + 'history not found')
                        break

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
            for i in e:
                return len(i["items"]) + 1

    @staticmethod
    def make_u_id():
        with open('users.json', 'r') as f:
            e = json.load(f)
            return len(e) + 1

    # add food
    def add_item(self, selection):
        if 1 < int(selection) < 4:
            food_type = 'food' if int(selection) == 2 else 'drink'
            print(Fore.LIGHTBLUE_EX + f'default product type: {food_type}')
            p_id = self.make_p_id()
            name = input(Fore.CYAN + 'Food name: ')
            price = input(Fore.MAGENTA + 'Food price: ')
            quantity = int(input(Fore.LIGHTRED_EX + 'Food quantity: '))

            d = {
                "type": food_type,
                "id": p_id,
                "name": name,
                "price": price,
                "quantity": quantity
            }
            with open("products.json", "r") as g:
                s = json.load(g)

            for i in s:
                if i["type"] == food_type:
                    i["items"].append(d)

            with open("products.json", "w") as f:
                json.dump(s, f, indent=2)
                print(Fore.GREEN + 'Item added successfully')

        else:
            print(Fore.YELLOW + "selection not found !")

    # report (last order)
    @staticmethod
    def report():
        # all_history = []

        with open("users.json", "r") as f:
            f = json.load(f)
            for i in f:
                # all_history.append(i["order history"])
                print("user [" + str(i["username"]) + "] : " + str(i["order history"]))

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
                                          'Would you try again? [y/N]\n'
                                          ': ')
            if sign_up.lower() in ['yes', 'y', 'yep', 'ha', 'yeah']:
                return self.login()

        return False

    # sign up
    def signup(self):
        username = input('Enter username: ')
        password = input('Enter password: ')

        if not self.check_username(username) and username != '':
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
        elif not self.check_username(username):
            print(Fore.YELLOW + 'Username already taken')
            self.signup()
        else:
            print(Fore.YELLOW + 'minimum username characters : 1')
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
            res = [p_name, int(p_price) * int(p_quantity), p_quantity, str(time)]

            for i in users_file:
                if i["id"] == self.current_user:
                    i["order history"].append(res)

        with open("users.json", "w") as f:
            json.dump(users_file, f, indent=2)

    # get food
    def get_food(self, _type):
        with open("products.json", "r") as f:
            products = json.load(f)

            for o in products:
                if o["type"] == _type:
                    if len(o["items"]) > 0:

                        # if product list is not null
                        for i, v in enumerate(products):
                            if v["type"] == _type:
                                items = products[i]["items"]
                                item_id = i
                                for product in v["items"]:
                                    a_t, b_t = f'currency: {product["quantity"]}x', 'out of stock'
                                    lines = '<------------------------------------------>\n'
                                    print(Fore.LIGHTGREEN_EX + f'{lines}'
                                                               f'| {product["id"]}. {product["name"]} - '
                                                               f'{product["price"]} - '
                                                               f'{a_t if product["quantity"] else b_t}\n'
                                                               f'{lines}')
                        order_id = int(input(Fore.LIGHTCYAN_EX + '$ '))

                        for i, v in enumerate(items):
                            if v["id"] == order_id:
                                print(Fore.LIGHTGREEN_EX + f'{v["name"]} - {v["price"]}')
                                count = int(input(Fore.RESET + 'how much do you want?\n$ '))
                                while 0 > count or count > v["quantity"]:
                                    count = int(input(
                                        Fore.RESET + f'how much do you want? base: [{v["quantity"]}]. {0} for exit\n$ '))
                                if count == 0:
                                    return False
                                self.add_to_history(v["name"], v["price"], count)
                                products[item_id]['items'][i]["quantity"] -= count
                                with open("products.json", "w") as z:
                                    json.dump(products, z, indent=2)
                                print(Fore.GREEN + "successfully ordered products")
                                return True

            print('item not found')
            return False

    # order food and quantity - x
    def order_food(self):
        actions = {
            1: "food",
            2: "drink",
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
            self.add_item(selection)
            self.enterance()
        elif selection == '3':
            self.add_item(selection)
            self.enterance()
        elif selection == '4':
            self.report()
            self.enterance()
        elif selection == '5':
            print(Fore.GREEN + 'See you soon 👋\n' + Fore.MAGENTA + "YOUR ADS HERE!")
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
            print(Fore.YELLOW + 'selection not exist')
            self.main_menu()


# ----------------------------------------------------------------
a = Restaurant()
# enterance -> main function
a.enterance()
# ----------------------------------------------------------------
