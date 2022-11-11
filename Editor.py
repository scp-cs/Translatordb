import json
from unicodedata import name
from colorama import init, Fore, Back
from os import system
from prettytable import PrettyTable
import re

filename_default = "translations.json"
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
        last_article = list(user['articles'].keys())[-1]

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
                        pass
                    case 2:
                        article_name = input("Jméno článku: ")
                        article_words = input("Počet slov: ")
                        article_bonus = input("Bonusové body: ")
                        
                        # U normálních SCP automaticky složit odkaz
                        if re.match(r"^SCP-\d{3,4}(-J)?$", article_name):
                            wdlink = "https://scp-cs.wikidot.com/" + article_name.lower()
                        else:
                            # Automaticky přepsat odkazy z EN na CS wiki
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
    
