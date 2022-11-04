import csv
import json

def format_name(name: str):
    if name.isnumeric():
        return f"SCP-{name.zfill(3)}"
    else:
        return name

with open("PrekladyNew.csv", "r", encoding="utf8") as csvf:
    reader = csv.reader(csvf, delimiter=",", quotechar="\"")
    jsond = {}
    for index, row in enumerate(reader):
        if index == 0:
            continue
        if row[2] == "":
            bonus = 0
        else:
            bonus = int(row[2])
        if row[3] not in jsond:
            did = input(f"Enter Discord ID for {row[3]}: ")
            wiki = input(f"Enter Wikidot username for {row[3]}: ")
            jsond[row[3]] = {'discord_id': did, 'wikidot': wiki, "total_points": 0, "role_level": 0, "exception": False, "articles": {}}
        jsond[row[3]]['articles'][format_name(row[0])] = {'word_count': int(row[1]), 'bonus_points': bonus, 'wd_link': "NULL"}
        jsond[row[3]]['total_points'] += round(float(row[1])/1000, 2)
        jsond[row[3]]['total_points'] += bonus
    with open("translations.json", "w+") as jsonfile:
        jsonfile.write(json.dumps(jsond, indent=2))
