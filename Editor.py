# Built-ins
from email.policy import default
import json
import re
import os
from os import system

# External
from readchar import readkey, key
from colorama import init, Fore, Back
from prettytable import PrettyTable

# Internal


# Constants
filename_default = "translations.json"
page_length = 15

# Global vars
db = {}
selected_user = ""

def write_db():
    try:
        with open(filename_default, "w", encoding="utf-8") as dbfile:
            json.dump(db, dbfile)
    except IOError as e:
        print(Fore.RED + "Chyba při zápisu: " + str(e) + Fore.RESET)


def print_kv(key, value, color):
    print(f"{key}: {color}{value}{Fore.RESET}{Back.RESET}")

def print_menu():
    print(Fore.YELLOW + "\nMENU" + Fore.RESET + "\n1. Vybrat uživatele\n2. Zobrazit seznam uživatelů\n3. Přidat nového uživatele\n4. Odejít\n")

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

def display_translation_table(user):
    item_count = len(user['articles'])
    def show_tab(start_row, row_count):
        tab = PrettyTable()
        tab.field_names = ['č.', 'Název', 'Počet bodů', 'Potřebný překlad?', "Odkaz"]
        for idx, article in enumerate(list(user['articles'].items())[start_row:start_row+row_count]):
            tab.add_row([idx+start_row+1, article[0], format(int(article[1]['word_count'])/1000, ".2f"), (Fore.GREEN + "ANO" if article[1]['bonus_points'] == 1 else Fore.RED + "NE") + Fore.RESET, article[1]['wd_link']])
        print(tab)
        print(f"Zobrazuji {start_row} - {start_row+row_count if start_row + row_count < item_count else item_count} z {item_count} položek")
    page = 0
    while True:
        os.system("cls")
        show_tab(page*page_length, page_length)
        k = readkey()
        match k:
            case key.RIGHT:
                if page < len(user['articles'])/page_length-1: page += 1
            case key.LEFT:
                if page > 0: page -= 1
            case key.ESC | key.ESC_2 | 'q':
                return

def display_user_table():
    item_count = len(db)
    def show_tab(start_row, row_count):
        tab = PrettyTable()
        tab.field_names = ['č.', 'Přezdívka', 'Wikidot', 'Počet bodů', "Články", "Discord ID"]
        for idx, user in enumerate(list(db.items())[start_row:start_row+row_count]):
            tab.add_row([idx+start_row+1, user[0], user[1]['wikidot'], (Fore.MAGENTA + "ano."if user[1]['exception'] else Fore.CYAN + format(user[1]['total_points'], ".2f")) + Fore.RESET, len(db[user[0]]['articles']), user[1]['discord_id']])
        print(tab)
        print(f"Zobrazuji {start_row} - {start_row+row_count if start_row + row_count < item_count else item_count} z {item_count} položek")
    page = 0
    while True:
        os.system("cls")
        show_tab(page*page_length, page_length)
        k = readkey()
        match k:
            case key.RIGHT:
                if page < len(db)/page_length-1: page += 1
            case key.LEFT:
                if page > 0: page -= 1
            case key.ESC | key.ESC_2 | 'q':
                return

def user_menu():
    global selected_user
    user = db[selected_user]

    def print_user_menu():
        last_article = list(user['articles'].keys())[-1] if len(user['articles']) > 0 else "ne."

        system("cls")
        print(Fore.CYAN + "INFO O UŽIVATELI\n" + Fore.RESET)
        print_kv("Alias", selected_user, Fore.CYAN)
        print_kv("Discord ID", user['discord_id'], Fore.CYAN)
        print_kv("Wikidot účet", user['wikidot'], Fore.CYAN)
        print_kv("Celkem bodů", "Ano" if user['exception'] else format(user['total_points'], '.2f'), Fore.CYAN)
        print_kv("Poslední zapsaný překlad", last_article, Fore.CYAN)
        print(Fore.YELLOW + "\nMENU" + Fore.RESET + "\n1. Zobrazit seznam přeložených článků\n2. Přidat přeložený článek\n3. Odebrat uživatele\n4. Zpět\n")
    
    while True: 
        print_user_menu()
        inp = input("Zvolte možnost: ")
        try:
            a = int(inp)
            if 0 < a < 6:
                match a:
                    case 1:
                        display_translation_table(db[selected_user])
                    case 2:
                        article_name = input("Jméno článku: ")
                        article_words = input("Počet slov: ")
                        article_bonus = input("Bonusové body: ")
                        
                        # Find link to normal SCPs
                        if re.match(r"^SCP-\d{3,4}(-J)?$", article_name):
                            wdlink = "https://scp-cs.wikidot.com/" + article_name.lower()
                        else:
                            # Automatically rewrite EN wiki links to CS
                            # TODO: Funguje to ale vypadá to hrozně
                            article_link = input("Odkaz na článek: ")
                            wdlink = "NULL" if article_link.isspace() else article_link.replace('https://scp-wiki', 'http://scp-cs', 1).replace('https://wanderers-library', 'http://wanderers-library-cs')

                        db[selected_user]['articles'][article_name] = {'word_count': int(article_words), 'bonus_points': int(article_bonus), 'wd_link': wdlink}

                        db[selected_user]['total_points'] = sum(map(lambda x: int(x['word_count']) + 1000*int(x['bonus_points']), db[selected_user]['articles'].values())) / 1000

                        write_db()
                    case 3:
                        confirmation = input(Fore.RED + "Skutečně chcete tohoto uživatele odebrat? Pro potvrzení napište jeho Discord ID: " + Fore.RESET)
                        if confirmation == db[selected_user]['discord_id']:
                            del db[selected_user]
                            write_db()
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
                            print("Pro pokračování stiskněte cokoliv")
                            readkey()
                            system("cls")
                            continue;
                        pass
                    case 2:
                        display_user_table()
                        system('cls')
                        pass
                    case 3:
                        nick = input("Zadejte přezdívku: ")
                        did = input("Zadejte Discord ID: ")
                        wid = input("Zadejte Wikidot ID: ")
                        print("Vyloučit z počítání bodů? [A/N]")
                        exc_key = readkey()
                        match exc_key:
                            case 'y' | 'Y' | 'a' | 'A':
                                exc = True
                            case _:
                                exc = False
                        db[nick] = {'discord_id': did, 'wikidot': wid, 'total_points': 0, 'role_level': 0, 'exception': exc, 'articles': {}}
                        write_db()
                        print(Fore.GREEN + "Uživatel přidán. Stiskněte cokoliv pro pokračování" + Fore.RESET)
                        readkey()
                        system('cls')
                        pass
                    case 4:
                        print(Fore.RED + "Sbohem, Administrátore." + Fore.RESET)
                        exit(0)
                        pass
            else:
                system("cls")
                continue
        except ValueError:
            system("cls")
            continue