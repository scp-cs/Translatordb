from glob import glob
import json
from colorama import init, Fore, Back
from os import system
from prettytable import PrettyTable

filename_default = "translations.json"
db = {}
selected_user = ""

def print_kv(key, value, color):
    print(f"{key}: {color}{value}{Fore.RESET}{Back.RESET}")

def print_menu():
    print(Fore.YELLOW + "\nMENU" + Fore.RESET + "\n1. Vybrat uživatele\n2. Zobrazit seznam uživatelů\n3. Přidat nového uživatele\n5. Odejít\n")

def select_user():
    global selected_user
    name = input("Zadejte alias, DID nebo WID uživatele: ")
    if name in db.keys():
        selected_user = name
        system("cls")
        print(Fore.GREEN + f"\nVybrán uživatel {name}." + Fore.RESET)
        return True
    else:
        for user in db:
            if name == db[user]['discord_id'] or name == db[user]['wikidot']:
                system("cls")
                print(Fore.GREEN + f"\nVybrán uživatel {user}." + Fore.RESET)
                selected_user = user
                return True
    print(Fore.RED + f'\nUživatel "{name}" nenalezen' + Fore.RESET)
    return False

def user_menu():
    global selected_user
    user = db[selected_user]

    def print_user_menu():
        system("cls")
        print(Fore.CYAN + "INFO O UŽIVATELI" + Fore.RESET)
        print_kv("Alias", selected_user, Fore.CYAN)
        print_kv("Discord ID", user['discord_id'], Fore.CYAN)
        print_kv("Wikidot účet", user['wikidot'], Fore.CYAN)
        print_kv("Celkem bodů", "Ano" if user['exception'] else user['total_points'], Fore.CYAN)
        print(Fore.YELLOW + "\nMENU" + Fore.RESET + "\n1. Zobrazit seznam přeložených článků\n2. Přidat přeložený článek\n3. Odebrat uživatele\n4. Zpět\n")
    
    while True: 
        print_user_menu()
        inp = input("Zvolte možnost: ")
        try:
            a = int(inp)
            if 0 < a < 6:
                match a:
                    case 1:
                        pass
                    case 2:
                        pass
                    case 3:
                        pass
                    case 4:
                        system("cls")
                        return
            else:
                system("cls")
                continue
        except ValueError:
            system("cls")
            continue

if __name__ == "__main__":
    system("cls")
    init()
    print(Fore.GREEN + "Vítá vás HR databáze SCiPNETu!" + Fore.RESET)
    print(Fore.YELLOW + f"Otevírám soubor {filename_default}..." + Fore.RESET)
    with open(filename_default, "r+", encoding="utf-8") as dbfile:
        db = json.load(dbfile)
        while True: 
            print_menu()
            inp = input("Zvolte možnost: ")
            try:
                a = int(inp)
                if 0 < a < 6:
                    match a:
                        case 1:
                            if(select_user()):
                                user_menu()
                            else:
                                input("Pro pokračování stiskněte cokoliv")
                                system("cls")
                                continue;
                            pass
                        case 2:
                            pass
                        case 3:
                            pass
                        case 4:
                            pass
                        case 5:
                            print(Fore.RED + "Sbohem, Administrátore." + Fore.RESET)
                            exit(0)
                            pass
                else:
                    system("cls")
                    continue
            except ValueError:
                system("cls")
                continue
    
