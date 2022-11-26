# Built-ins
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
rewrite_urls = {"https://scp-wiki": "http://scp-cs", "https://wanderers-library": "http://wanderers-library-cs"}    # Imagine making people pay extra for HTTPS in 2022, what the fuck
rgx_scp = re.compile(r"^SCP-\d{3,4}((-J)?|(-ARC)?|(-D)?)$")

# Global vars
db = {}
selected_user = ""

# Couldn't find a fancy "pythonic" way to do this, at least you can do one-line ifs
def get_role_color(user):
    if user['exception']: return Fore.MAGENTA
    points = user['total_points']
    if points < 5: return Fore.WHITE
    elif points < 10: return Fore.CYAN
    elif points < 25: return Fore.GREEN
    elif points < 50: return Fore.YELLOW
    elif points < 100: return Fore.RED
    else: return Fore.MAGENTA
        
def write_db():
    try:
        with open(filename_default, "w", encoding="utf-8") as dbfile:
            json.dump(db, dbfile)
    except IOError as e:
        print(Fore.RED + "Chyba při zápisu: " + str(e))

def print_kv(key, value, color): print(f"{key}: {color}{value}{Fore.RESET}{Back.RESET}")

def url_rewrite(url):
    new_url = url
    for rule in rewrite_urls.items():
        new_url = new_url.replace(rule[0], rule[1])
    return new_url

def select_user():
    global selected_user
    name = input("Zadejte alias, DID nebo WID uživatele: ")
    if name in db.keys():
        selected_user = name
        system("cls")
        print(Fore.GREEN + f"\nVybrán uživatel {name}.")
        user_menu()
        return
    else:
        for user in db:
            if name == db[user]['discord_id'] or name == db[user]['wikidot']:
                system("cls")
                print(Fore.GREEN + f"\nVybrán uživatel {user}.")
                selected_user = user
                user_menu()
                return
    print(Fore.RED + f'\nUživatel "{name}" nenalezen')
    readkey()
    system('cls')

def display_translation_table(user):
    item_count = len(user['articles'])
    def show_tab(start_row, row_count):
        tab = PrettyTable()
        tab.field_names = ['č.', 'Název', 'Počet bodů', 'Potřebný překlad?', "Odkaz"]

        for idx, article in enumerate(list(user['articles'].items())[start_row:start_row+row_count]):
            tab.add_row([
            idx+start_row+1, 
            article[0], 
            format(int(article[1]['word_count'])/1000, ".2f"), 
            (Fore.GREEN + "ANO" if article[1]['bonus_points'] == 1 else Fore.RED + "NE") + Fore.RESET, 
            article[1]['wd_link']])

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
    sort_abc = False  # False = by points, True = alphabetical

    def show_tab(start_row, row_count):
        tab = PrettyTable()
        tab.field_names = ['č.', 'Přezdívka', 'Wikidot', 'Počet bodů', "Články", "Discord ID"]

        if sort_abc:
            values = list(sorted(db.items(), key=lambda item: item[0]))
        else:
            values = list(sorted(db.items(), key=lambda item: item[1]['total_points'], reverse=True))

        for idx, user in enumerate(values[start_row:start_row+row_count]):
            points = user[1]['total_points']

            tab.add_row([
            idx+start_row+1, 
            user[0], 
            user[1]['wikidot'], 
            get_role_color(user[1]) + ("ano." if user[1]['exception'] else format(points, ".2f")) + Fore.RESET, 
            len(user[1]['articles']), 
            user[1]['discord_id']])

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
                system('cls')
                return
            case 's': sort_abc = not sort_abc

def add_user():
    global db
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
    db[nick] = {'discord_id': did, 'wikidot': wid, 'total_points': 0 if not exc else 9999, 'role_level': 0, 'exception': exc, 'articles': {}}
    write_db()
    print(Fore.GREEN + "Uživatel přidán. Stiskněte cokoliv pro pokračování")
    readkey()
    system('cls')

def user_menu():
    global selected_user
    user = db[selected_user]

    def print_user_menu():
        last_article = list(user['articles'].keys())[-1] if len(user['articles']) > 0 else "ne."

        system("cls")
        print(Fore.CYAN + "INFO O UŽIVATELI\n")
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
                        if rgx_scp.match(article_name):
                            wdlink = "https://scp-cs.wikidot.com/" + article_name.lower()
                        else:
                            # Automatically rewrite EN wiki links to CS
                            article_link = input("Odkaz na článek: ")
                            wdlink = "NULL" if article_link.isspace() else url_rewrite(article_link)

                        db[selected_user]['articles'][article_name] = {'word_count': int(article_words), 'bonus_points': int(article_bonus), 'wd_link': wdlink}

                        # Recalculate points every time an entry is added, just in case the JSON was edited manually
                        db[selected_user]['total_points'] = sum(map(lambda x: int(x['word_count']) + 1000*int(x['bonus_points']), db[selected_user]['articles'].values())) / 1000

                        write_db()
                    case 3:
                        confirmation = input(Fore.RED + "Skutečně chcete tohoto uživatele odebrat? Pro potvrzení napište jeho Discord ID: ")
                        if confirmation == db[selected_user]['discord_id']:
                            del db[selected_user]
                            write_db()
                        else:
                            print(Fore.RED + "Nesprávné Discord ID.")
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
    system("title SCiPNET v1.4")
    init(autoreset=True)
    print(Fore.GREEN + "Vítá vás HR databáze SCiPNETu!")
    print(Fore.YELLOW + f"Otevírám soubor {filename_default}...")

    try:
        with open(filename_default, "r", encoding="utf-8") as dbfile:
            db = json.load(dbfile)
    except json.JSONDecodeError:
        print(Fore.RED + "Chyba dekódování JSON, soubor je pravděpodobně poškozen.")
        exit(-1)
    except IOError:
        print(Fore.RED + "Chyba při čtení souboru, zkontrolujte umístění a přístupová práva.")
        exit(-1)

    while True: 
        print(Fore.YELLOW + "\nMENU" + Fore.RESET + "\n1. Vybrat uživatele\n2. Zobrazit seznam uživatelů\n3. Přidat nového uživatele\n4. Odejít\n")
        inp = input("Zvolte možnost: ")
        try:
            a = int(inp)
            if a < 0 or a > 6: raise ValueError
            match a:
                case 1: select_user()
                case 2: display_user_table()
                case 3: add_user()
                case 4:
                    print(Fore.RED + "Sbohem, Administrátore.")
                    exit(0)
        except ValueError:
            system("cls")
            continue