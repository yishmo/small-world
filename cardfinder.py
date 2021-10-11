import requests
import json
import time
import random

ALL_MAIN_DECK_MONSTER_MONSTER_TYPES = "Effect Monster,Flip Effect Monster,Flip Tuner Effect Monster,Gemini Monster,Normal Monster,Normal Tuner Monster,Pendulum Effect Monster,Pendulum Flip Effect Monster,Pendulum Normal Monster,Pendulum Tuner Effect Monster,Ritual Effect Monster,Ritual Monster,Spirit Monster,Toon Monster,Tuner Monster,Union Effect Monster"

QM_ATK_AND_DEF = {"Gren Maju Da Eiza", "Eater of Millions"}


def gen_other_attrs(attribute):
    allAttrs = {"WATER,", "EARTH,", "FIRE,", "WIND,", "DARK,", "LIGHT,", "DIVINE,"}
    allAttrs.remove(attribute + ",")
    attrStr = ""

    for item in allAttrs:
        attrStr += item

    return attrStr[:-1]


def gen_other_races(attribute):
    attribute = attribute.lower()
    allRaces = {
        "zombie,",
        "fiend,",
        "rock,",
        "warrior,",
        "winged beast,",
        "spellcaster,",
        "beast,",
        "fairy,",
        "fish,",
        "beast-warrior,",
        "thunder,",
        "machine,",
        "sea serpent,",
        "aqua,",
        "plant,",
        "dragon,",
        "reptile,",
        "psychic,",
        "insect,",
        "pyro,",
        "dinosaur,",
        "wyrm,",
        "cyberse,",
        "divine-beast,",
        "creator-god,",
    }

    allRaces.remove(attribute + ",")
    racesStr = ""

    for item in allRaces:
        racesStr += item

    return racesStr[:-1]


def gen_other_levels(level):
    all_levels = list(range(13))  # 0-12
    del all_levels[level]
    return all_levels


def given_attrs_search_along_atk(attr_dict):
    print("Checking all cards with same ATK.")
    parameters = {"atk": attr_dict["atk"]}
    possibleCards = []

    parameters["attribute"] = gen_other_attrs(attr_dict["attribute"])
    parameters["misc"] = "yes"
    parameters["race"] = gen_other_races(attr_dict["race"])
    parameters["type"] = ALL_MAIN_DECK_MONSTER_MONSTER_TYPES

    for level in gen_other_levels(attr_dict["level"]):
        for ltOrGt in ("lt", "gt"):
            parameters["def"] = ltOrGt + str(attr_dict["def"])
            parameters["level"] = level

            response_json = request_from_ygoprodeck(parameters)

            possibleCards = append_cards_to_list(possibleCards, response_json)

    return possibleCards


def given_attrs_search_along_def(attr_dict):
    print("Checking all cards with same DEF.")
    parameters = {"def": attr_dict["def"]}
    possibleCards = []

    parameters["misc"] = "yes"
    parameters["attribute"] = gen_other_attrs(attr_dict["attribute"])
    parameters["race"] = gen_other_races(attr_dict["race"])
    parameters["type"] = ALL_MAIN_DECK_MONSTER_MONSTER_TYPES

    for level in gen_other_levels(attr_dict["level"]):
        for ltOrGt in ("lt", "gt"):
            parameters["atk"] = ltOrGt + str(attr_dict["atk"])
            parameters["level"] = level

            response_json = request_from_ygoprodeck(parameters)

            possibleCards = append_cards_to_list(possibleCards, response_json)

    return possibleCards


def given_attrs_search_along_attribute(attr_dict):
    print("Checking all cards with same Attribute.")
    possibleCards = []

    parameters = {"attribute": attr_dict["attribute"]}
    parameters["misc"] = "yes"
    parameters["race"] = gen_other_races(attr_dict["race"])
    parameters["type"] = ALL_MAIN_DECK_MONSTER_MONSTER_TYPES

    for level in gen_other_levels(attr_dict["level"]):
        # 4 possible variations for atk/def now
        for atkLtOrGt, defLtOrGt in [
            ("lt", "lt"),
            ("gt", "gt"),
            ("lt", "gt"),
            ("gt", "lt"),
        ]:
            parameters["atk"] = atkLtOrGt + str(attr_dict["atk"])
            parameters["def"] = defLtOrGt + str(attr_dict["def"])
            parameters["level"] = level

            response_json = request_from_ygoprodeck(parameters)

            possibleCards = append_cards_to_list(possibleCards, response_json)

    return possibleCards


def given_attrs_search_along_race(attr_dict):
    print("Checking all cards with same Type.")
    possibleCards = []

    parameters = {"race": attr_dict["race"]}
    parameters["misc"] = "yes"
    parameters["attribute"] = gen_other_attrs(attr_dict["attribute"])
    parameters["type"] = ALL_MAIN_DECK_MONSTER_MONSTER_TYPES

    for level in gen_other_levels(attr_dict["level"]):
        # 4 possible variations for atk/def now
        for atkLtOrGt, defLtOrGt in [
            ("lt", "lt"),
            ("gt", "gt"),
            ("lt", "gt"),
            ("gt", "lt"),
        ]:
            parameters["atk"] = atkLtOrGt + str(attr_dict["atk"])
            parameters["def"] = defLtOrGt + str(attr_dict["def"])
            parameters["level"] = level

            response_json = request_from_ygoprodeck(parameters)

            possibleCards = append_cards_to_list(possibleCards, response_json)

    return possibleCards


def given_attrs_search_along_level(attr_dict):
    print("Checking all cards with same Level.")
    possibleCards = []

    parameters = {"level": attr_dict["level"]}
    parameters["misc"] = "yes"
    parameters["attribute"] = gen_other_attrs(attr_dict["attribute"])
    parameters["race"] = gen_other_races(attr_dict["race"])
    parameters["type"] = ALL_MAIN_DECK_MONSTER_MONSTER_TYPES

    # 4 possible variations for atk/def now
    for atkLtOrGt, defLtOrGt in [
        ("lt", "lt"),
        ("gt", "gt"),
        ("lt", "gt"),
        ("gt", "lt"),
    ]:
        parameters["atk"] = atkLtOrGt + str(attr_dict["atk"])
        parameters["def"] = defLtOrGt + str(attr_dict["def"])

        response_json = request_from_ygoprodeck(parameters)

        possibleCards = append_cards_to_list(possibleCards, response_json)

    return possibleCards


def append_cards_to_list(possibleCards, response_json):
    try:
        error_message = response_json["error"]
        assert error_message == (
            "No card matching your query was found in "
            "the database. Please see https://db.ygoprodeck."
            "com/api-guide/ for syntax usage."
        )
    except KeyError:
        for card in response_json["data"]:
            attr_dict = {}
            attr_dict["atk"] = card["atk"]
            attr_dict["def"] = card["def"]
            attr_dict["level"] = card["level"]
            attr_dict["attribute"] = card["attribute"]
            attr_dict["race"] = card["race"]
            possibleCards.append(
                (card["name"], card_popularity_function(card), attr_dict)
            )

    return possibleCards


def return_all_possibilities_given_name(cardName):
    attrs = given_card_name_get_attrs(cardName)

    all = (
        given_attrs_search_along_level(attrs)
        + given_attrs_search_along_atk(attrs)
        + given_attrs_search_along_def(attrs)
        + given_attrs_search_along_race(attrs)
        + given_attrs_search_along_attribute(attrs)
    )

    return sorted(all, key=lambda x: -x[1])


def given_card_name_get_attrs(cardName):
    parameters = {"name": cardName}
    attr_dict = {}
    response_json = request_from_ygoprodeck(parameters)
    attr_dict["atk"] = response_json["data"][0]["atk"]
    attr_dict["def"] = response_json["data"][0]["def"]
    attr_dict["attribute"] = response_json["data"][0]["attribute"]
    attr_dict["level"] = response_json["data"][0]["level"]
    attr_dict["race"] = response_json["data"][0]["race"]
    return attr_dict


def find_bridge(start, end):
    small_world_compatible = []
    allPossible = return_all_possibilities_given_name(start)
    import pdb

    pdb.set_trace()
    attrs = given_card_name_get_attrs(end)

    for card in allPossible:
        similar_attrs = 0
        if attrs["atk"] == card[2]["atk"]:
            similar_attrs += 1
        if attrs["def"] == card[2]["def"]:
            similar_attrs += 1
        if attrs["attribute"] == card[2]["attribute"]:
            similar_attrs += 1
        if attrs["level"] == card[2]["level"]:
            similar_attrs += 1
        if attrs["race"] == card[2]["race"]:
            similar_attrs += 1
        if similar_attrs == 1:
            small_world_compatible.append(card[0])

    return small_world_compatible


def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


def request_from_ygoprodeck(parameters):
    # stay under limit of 20 per second
    request_from_ygoprodeck.tracker += 1
    if request_from_ygoprodeck.tracker == 20:
        time.sleep(1)
        request_from_ygoprodeck.tracker = 0
    response = requests.get(
        "https://db.ygoprodeck.com/api/v7/cardinfo.php", params=parameters
    )
    response_json = response.json()

    try:
        for card in response_json["data"]:
            if card["name"] in QM_ATK_AND_DEF:
                card["atk"] = random_10_digit_int()
                card["def"] = random_10_digit_int()
    except KeyError:
        error_message = response_json["error"]
        assert error_message == (
            "No card matching your query was found in "
            "the database. Please see https://db.ygoprodeck."
            "com/api-guide/ for syntax usage."
        )

    return response_json


def card_popularity_function(card_api_resp):
    total = card_api_resp["misc_info"][0]["views"] / 1000
    total += card_api_resp["misc_info"][0]["viewsweek"]
    total += card_api_resp["misc_info"][0]["upvotes"]
    total += card_api_resp["misc_info"][0]["downvotes"]

    return total


def random_10_digit_int():
    return random.randint(1000000000, 9999999999)


# this function attribute keeps track of
# how many times we have called the API
request_from_ygoprodeck.tracker = 0

start = time.time()
allPossible = find_bridge("Danger! Thunderbird!", "Gren Maju Da Eiza")
print(allPossible)
print(len(allPossible))
end = time.time()
print(end - start)
