# Small World Simulator

import requests
import json
import pprint

from ygo_api import get_all_monsters_for_small_world


def getScore(card, comparison):
    score = 0
    for key in card:
        if card[key] == comparison[key]:
            score = score + 1
    return score

def run_gabes_code():
    deck = []
    print("Copy and paste your .ydk file main deck card numbers", 
        "(all numbers after #main and before #side then press enter): ")
    while True:
        user_input = input()
        if user_input == '':
            break
        elif len(user_input) != 8:
            pass
        else:
            deck.append(int(user_input))
    # remove duplicates
    deck = set(list(deck))

    deckmonsters = {}
    monsterbridges = {}

    response_json = get_all_monsters_for_small_world()

    # Step 2: API Calls
    for card in deck:
        for info in response_json["data"]:
            if card == info["id"]:
                deckmonsters[info["name"]] = {
                    "ATK": info["atk"],
                    "DEF": info["def"],
                    "Attribute": info["attribute"],
                    "Type": info["race"],
                    "Level": info["level"],
                }

    monster_names = set(deckmonsters.keys())

    # Step 3: Actual Logic


    for card in deckmonsters:
        monsterbridges[card] = []
        for key in deckmonsters:
            score = getScore(deckmonsters[card], deckmonsters[key])
            if score == 1:
                monsterbridges[card].append(key)


    # Right Now, monster-bridges is a dict with all cards that connect to each other. Now, we want to output all the cards each card can search

    missing = {}
    print("---ALL POSSIBLE SMALL WORLD ADDS---")
    with open("output.txt", "w") as f:
        for card in monsterbridges:
            targets = set()
            for key in monsterbridges[card]:
                for target in monsterbridges[key]:
                    print(f"Banish {card} ---> Reveal {key} ---> Add {target}")
                    f.write(f"Banish {card} ---> Reveal {key} ---> Add {target}\n")
                    targets.add(target)
            missing[card] = monster_names - targets - {card}

    print()
    print("---ALL MISSING LINKS---")
    pprint.pprint(missing)
