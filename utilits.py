import os, json, requests
import sys
from datetime import datetime

os.system("\n")

# api key and request url
API_KEY = "c66xOBOerxjgjCqRfbT3MzvIIqMoDm6e"
REQUEST_URL = "https://api.apilayer.com/fixer/latest?base=USD"

# current path directory
CURRENT_PATCH = os.path.dirname(__file__)
# current path Jason directory
CURRENT_PATCH_JASON = os.path.join(CURRENT_PATCH, "rates")

# my basic rates
basic_favorite_rates = ["USD", "UAH", "EUR", "PLN", "RON", "HUF", "ILS"]

# main menu print
MAIN_MENU = f"""\u001b[38;5;12m{11 * '*'}\n*Main menu*\n{11 * '*'}\u001b[0m
\u001b[38;5;9m0\u001b[0m - EXIT
\u001b[38;5;9m1\u001b[0m - convert
\u001b[38;5;9m2\u001b[0m - recheck online rates
\u001b[38;5;9m3\u001b[0m - ADD/DELETE favorites
PRESS: """

# menu func favorite currency
MENU_FAVORITE_CUR = """\u001b[38;5;12m1 - ADD Currency
2 - Del Currency 
3 - Convector
0 - Exit\n: \u001b[0m"""


def menu_main():
    """
    Func Menu Main print menu and check input
    :return: int(input)
    """
    favorite_rates(rates_file)
    while True:
        # check correct input
        main_input = input(MAIN_MENU)
        if not main_input.isdigit() or int(main_input) not in range(0, 4):
            print("***Wrong Input***")
            continue
        else:
            return int(main_input)


def receive_data():
    """
    Receive_data func check
    :return:  dict(collected_rates) or False
    """

    try:
        # receive data
        response_data = requests.get(REQUEST_URL, headers={"UserAgent": "XY", "apikey": API_KEY})
        collected_rates = json.loads(response_data.text)
        if collected_rates.get("success") == True:
            return collected_rates
    except:
        return False


def favorite_rates(rates):
    """
    Func favorite_rates print favorite rate and value
    :param rates: rates_file:
    :return:
    """
    print(f"Favorite Currency Rates\n{'*' * 25}\n*Last update {rates_file.get('date')}*")
    for i in range(len(basic_favorite_rates)):
        print(
            f"\u001b[38;5;9m{i + 1}\u001b[0m {basic_favorite_rates[i]} {rates.get('rates').get(basic_favorite_rates[i])}")


def reload_rates() -> dict:
    """
    Func Reload_data checks date from file
    if date!= date.now try upload
    :return: dict (rates)
    """
    rates = {}
    time_now = datetime.now().strftime("%Y-%m-%d")
    # open rates from file
    with open(os.path.join(CURRENT_PATCH_JASON, "data_rates.json")) as f:
        rates_from_file = json.load(f)
    rates = rates_from_file

    # check from file current date
    if rates_from_file.get("date") != time_now:
        print("Uploading Data")
        rates = receive_data()

        # cannot receive data
        if rates == False:
            print("Cannot update")
            rates = rates_from_file
        else:
            print("Uploading successful")
            # create file
            file_name = "data_rates.json"
            with open(os.path.join(CURRENT_PATCH_JASON, file_name), "w") as f:
                json.dump(rates, f, indent=4)
                pass
    return rates


rates_file = reload_rates()


def currency_converter(choice):
    """
    Func to convert favorite rates
    :param choice: choice_currency

    """

    while True:
        value = input(f"{basic_favorite_rates[(choice) - 1]} Amount: ")
        # check correct input
        if not value.isdigit():
            print("***Wrong input***")
            continue
        else:
            value = int(value)
            # converter if choice==USD
            if basic_favorite_rates[int(choice) - 1] == "USD":

                for i in range(len(basic_favorite_rates)):
                    print(f"{basic_favorite_rates[i]} {value * (rates_file.get('rates').get(basic_favorite_rates[i]))}")
            else:
                # converter if choice!=USD
                for j in range(len(basic_favorite_rates)):
                    print(
                        f"{basic_favorite_rates[j]} {(value * (rates_file.get('rates').get(basic_favorite_rates[j]))) / (rates_file.get('rates').get(basic_favorite_rates[int(choice) - 1]))}")
            break


def menu_curency():
    """
    Func menu_curency check input, choice favorite currency, exit
    :return:
    """
    while True:
        favorite_rates(rates_file)
        # choice currency input
        choice_currency = input("To choice favorite currency NUMBER CURRENCY\nPRESS 0 to exit\n***Choice***:")
        # check correct input
        if not choice_currency.isdigit() or int(choice_currency) not in range(0, (len(basic_favorite_rates) + 1)):
            print("***Wrong input***")
            continue
        # exit from app
        if int(choice_currency) == 0:
            sys.exit
        else:
            # start convector
            currency_converter(int(choice_currency))
        break


def favorite_edit():
    """
    Func favorite edit add/delete basic favorite list
    :return:
    """
    global basic_favorite_rates

    while True:
        favorite_menu = input(MENU_FAVORITE_CUR)
        # check correct input
        if not favorite_menu.isdigit() or int(favorite_menu) not in range(0, 4):
            print("***Wrong input***")
            continue

        else:
            favorite_menu = int(favorite_menu)
            # exit
            if favorite_menu == 0:
                sys.exit()
                pass

            # add favorites currency
            if favorite_menu == 1:
                currency_keys = list(rates_file.get("rates").keys())

                # print list all currency
                for i in range(len(currency_keys)):
                    print(f"\u001b[38;5;9m{i}\u001b[0m - {currency_keys[i]}")

                # add currency to favorite currency list
                add_choice = int(input("Write number of currency to ADD: "))
                if currency_keys[add_choice] not in basic_favorite_rates:
                    basic_favorite_rates.append(currency_keys[add_choice])
                    print(f"*****Added {currency_keys[add_choice]}*****")
                    pass

            # delete favorite currency
            if favorite_menu == 2:
                for j in range(len(basic_favorite_rates)):
                    print(f"\u001b[38;5;9m{j}\u001b[0m - {basic_favorite_rates[j]}")
                del_cur_input = int(input("choice number currency to delete: "))
                basic_favorite_rates.pop(del_cur_input)
                pass
            # return to menu currency
            if favorite_menu == 3:
                menu_curency()
