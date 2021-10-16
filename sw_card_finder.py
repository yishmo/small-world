import requests
import os

from gabesw import run_gabes_code
from ygo_api import get_all_monsters_for_small_world

# best to use a global variable
# since we want to query the API as
# little as possible
response_json = get_all_monsters_for_small_world()


def given_card_name_get_attrs(cardName):
    attr_dict = {}
    for card in response_json["data"]:
        #ignore case
        if cardName.lower() == card["name"].lower():
            attr_dict["atk"] = card["atk"]
            attr_dict["def"] = card["def"]
            attr_dict["attribute"] = card["attribute"]
            attr_dict["level"] = card["level"]
            attr_dict["race"] = card["race"]

    return attr_dict


def exactly_one_equal(card, attrs):
    similar_attrs = 0
    if attrs["atk"] == card["atk"]:
        similar_attrs += 1
    if attrs["def"] == card["def"]:
        similar_attrs += 1
    if attrs["attribute"] == card["attribute"]:
        similar_attrs += 1
    if attrs["level"] == card["level"]:
        similar_attrs += 1
    if attrs["race"] == card["race"]:
        similar_attrs += 1
    return similar_attrs == 1


def card_popularity_function(card_api_resp):
    total = card_api_resp["misc_info"][0]["views"] / 1000
    total += card_api_resp["misc_info"][0]["viewsweek"]
    total += card_api_resp["misc_info"][0]["upvotes"]
    total += card_api_resp["misc_info"][0]["downvotes"]

    return total


def find_bridge(name1, name2):
    attrs1 = given_card_name_get_attrs(name1)
    attrs2 = given_card_name_get_attrs(name2)

    card_list = []
    bridge_list = []
    for card in response_json["data"]:
        if exactly_one_equal(card, attrs1):
            card_list.append(card)
    for card in card_list:
        if exactly_one_equal(card, attrs2):
            bridge_list.append(card)

    sorted_list = sorted(bridge_list, key=card_popularity_function)
    for i in range(len(sorted_list)):
        print(f'{i + 1}. {sorted_list[i]["name"]}')

def verify_card_legality(cardName):
    attr_dict = given_card_name_get_attrs(cardName)
    if attr_dict == {}:
        print(
            cardName,
            "is not the full name of a Yu-Gi-Oh! monster card, please check your spelling and try again (name is case sensitive).",
        )
        return False
    return True


def find_small_world_compatible(name):
    attrs = given_card_name_get_attrs(name)

    card_list = []
    for card in response_json["data"]:
        if exactly_one_equal(card, attrs):
            card_list.append(card)

    sorted_list = sorted(card_list, key=card_popularity_function)
    for i in range(len(sorted_list)):
        print(f'{i + 1}. {sorted_list[i]["name"]}')


def main():
    while True:
        mode = input(
"""
Which mode would you like to use? Type in the corresponding number and press 
enter or press (q) to quit.

1. Banish card A from hand, reveal card B from deck, 
   add card C to hand ... I have cards A and C and want to find B.

2. I want to know all cards that share extacly one thing (ATK, DEF, Level, Type, Attribute) 
   with a card.

3. I want to see how well Small World works in my deck (Gabriel 
   Netz wrote most of this code).

Your Choice: """
        )

        if mode == "1":
            card1 = input("Enter the name of the monster card in your hand: ").strip()
            card2 = input("Enter the name of the monster card you want to search: ").strip()
            print('--------------')
            if verify_card_legality(card1) and verify_card_legality(card2):
                find_bridge(card1, card2)
        elif mode == "2":
            card = input(
                "Enter the name of a monster card to find all Small World compatible cards: "
            ).strip()
            print('--------------')
            if verify_card_legality(card):
                find_small_world_compatible(card)
        elif mode == "3":
            print('--------------')
            run_gabes_code()

        elif mode == "q":
            break
        else:
            print("please enter 1, 2 or q")


if __name__ == "__main__":
    main()
