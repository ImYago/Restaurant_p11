import os
import json
from colorama import Fore
import datetime
import bcrypt


class Restaurant:
    # simple variables
    def __init__(self):
        self.current_user = 0
        self.current_grade = ''

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
        password = input(Fore.RESET + "Enter password: ").encode()

        with open('users.json', 'r') as f:
            file = json.load(f)
            for i in file:
                if i["username"] == username:
                    hashed_password = i["password"].encode()
                    if bcrypt.checkpw(password, hashed_password):
                        self.current_user = int(i["id"])
                        self.current_grade = self.get_grade(username)
                        return True
        return False

    @staticmethod
    def make_p_id(type_):
        with open('products.json', 'r') as f:
            products = json.load(f)
            for i in products:
                if i["type"] == type_:
                    return len(i["items"]) + 1

    @staticmethod
    def make_u_id():
        with open('users.json', 'r') as f:
            e = json.load(f)
            return len(e) + 1

    # encrypt
    @staticmethod
    def encrypt(password):
        salt = bcrypt.gensalt()  # Generate a salt value
        hashed_password = bcrypt.hashpw(password.encode(), salt)  # Hash the password using bcrypt
        return hashed_password

    # add food
    def add_item(self, selection):
        if 0 < int(selection) < 3:
            food_type = 'food' if int(selection) == 1 else 'drink'
            print(Fore.LIGHTBLUE_EX + f'default product type: {food_type}')
            p_id = self.make_p_id(food_type)
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
                print(Fore.LIGHTMAGENTA_EX + "user [" + str(i["username"]) + "] : " + str(i["order history"]))

    # username checking
    @staticmethod
    def check_username(username):
        with open("users.json", "r") as f:
            file = json.load(f)

            for i in file:
                if username.lower() == i['username'].lower():
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
        username = input(Fore.LIGHTWHITE_EX + 'Enter username (0 for exit): ')
        if username == '0':
            return False
        if len(username.strip()) > 0:
            password = input(Fore.LIGHTWHITE_EX + 'Enter password: ')
            if len(password) > 0:
                grade = input('Are you guest !? [y/n]: ')
                if grade.lower() in ['yes', 'y', 'yep', 'ha', 'yeah']:
                    grade = True
                    self.current_grade = 'True'
                elif grade.lower() in ['no', 'nah', 'not', 'yoq', 'n']:
                    grade = False
                    self.current_grade = 'False'
                else:
                    print(Fore.LIGHTYELLOW_EX + 'Invalid grade!')
                    self.signup()

                if not self.check_username(username) and username not in ["", " ", "0"]:
                    with open("users.json", "r") as f:
                        file = json.load(f)

                    u_id = self.make_u_id()
                    self.current_user = int(u_id)

                    password = self.encrypt(password)

                    new_user = {
                        "id": u_id,
                        "username": username.strip(),
                        "password": password.decode(),
                        "order history": [],
                        "grade": str(grade)
                    }
                    file.append(new_user)
                    with open("users.json", "w") as f:
                        json.dump(file, f, indent=2)
                    return True
                elif self.check_username(username):
                    print(Fore.YELLOW + 'Username already taken')
                    self.signup()
                else:
                    print(Fore.YELLOW + 'minimum username characters : 1')
                    return False
            else:
                print(Fore.LIGHTYELLOW_EX + 'minimum password characters : 1')
                self.signup()
        else:
            print(Fore.LIGHTYELLOW_EX + "minimum username characters : 1")
            self.signup()

    @staticmethod
    def get_grade(username):
        with open("users.json", "r") as f:
            users = json.load(f)

        for i in users:
            if i["username"] == username:
                return i["grade"]

    # add information to the history
    def add_to_history(self, p_name, p_price, p_quantity):
        with open("users.json", "r") as d:
            users_file = json.load(d)
            time = datetime.datetime.now()
            int_price = ''
            for i in p_price:
                if i == i.isdigit():
                    int_price += i
            res = [p_name, p_quantity, str(time)]

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

            print('items not found')
            return False

    # order food and quantity - x
    def order_food(self, st):
        actions = {
            1: "food",
            2: "drink",
        }

        if st.isdigit():
            if 0 < int(st) < 3:
                return self.get_food(actions[int(st)])
            if int(st) == 3:
                return False
            print(Fore.YELLOW + "selection failed")
            self.order_food(st)
        else:
            print(Fore.YELLOW + 'select with numbers only!')
            self.order_food(st)

    # the enterance
    def enterance(self):
        self.create_json()
        enterance_text = '''
1. register
2. login
3. exit
: '''
        selection = input(Fore.LIGHTBLUE_EX + enterance_text)
        if selection.isdigit():
            if selection == '1':
                if self.signup():
                    self.main_page()
                else:
                    self.enterance()
            elif selection == '2':
                if self.login():
                    self.main_page()
                else:
                    self.enterance()
            elif selection == '3':
                print(Fore.GREEN + 'See you soon 👋\n' + Fore.MAGENTA + "YOUR ADS HERE!")
                exit()
        else:
            print(Fore.YELLOW + 'selection not exist')
            self.enterance()

    # dining menu
    def main_page(self):
        if self.current_grade == 'True':
            menu = '''
1. order food 
2. order drink
3. history
4. exit
$ '''
            s = input(Fore.LIGHTGREEN_EX + menu)
            if s == '1':
                if self.order_food(s):
                    self.main_page()
                else:
                    self.main_page()
            elif s == '2':
                self.order_food(s)
                self.main_page()
            elif s == '3':
                self.order_history()
                self.main_page()
            elif s == '4':
                self.enterance()
            else:
                print(Fore.YELLOW + 'selection not exist')
                self.main_page()
        elif self.current_grade == 'False':
            t = '''
1. add food
2. add drink 
3. report 
4. exit
$ '''
            s = input(Fore.LIGHTCYAN_EX + t)
            if s.isdigit():
                if s == '1':
                    self.add_item(s)
                    self.main_page()
                elif s == '2':
                    self.add_item(s)
                    self.main_page()
                elif s == '3':
                    self.report()
                    self.main_page()
                elif s == '4':
                    self.enterance()
        else:
            print(Fore.LIGHTRED_EX + 'Grade not exist')


# ----------------------------------------------------------------
a = Restaurant()
a.enterance()  # main function of the restaurant
# ----------------------------------------------------------------
