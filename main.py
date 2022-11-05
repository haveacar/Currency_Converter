
from utilits import *



def main():
    """
    Main function menu

    """
    while True:
        match menu_main():
        # exit case
            case 0:
                sys.exit()
        # converter
            case 1:
                menu_curency()
                pass
        # get rates
            case 2:
                reload_rates()
                pass
        # add/delete favorite rates
            case 3:
                favorite_edit()
                pass


main()
