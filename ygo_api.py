import requests

ALL_MAIN_DECK_MONSTER_MONSTER_TYPES = "Effect Monster,Flip Effect Monster,Flip Tuner Effect Monster,Gemini Monster,Normal Monster,Normal Tuner Monster,Pendulum Effect Monster,Pendulum Flip Effect Monster,Pendulum Normal Monster,Pendulum Tuner Effect Monster,Ritual Effect Monster,Ritual Monster,Spirit Monster,Toon Monster,Tuner Monster,Union Effect Monster"

QM_ATK_AND_DEF = {
    "Cyber Eltanin",
    "Destiny HERO - Dreadmaster",
    "Doomsday Horror",
    "Eater of Millions",
    "Evil Dragon Ananta",
    "Exodia, the Legendary Defender",
    "Fortune Lady Dark",
    "Fortune Lady Earth",
    "Fortune Lady Fire",
    "Fortune Lady Light",
    "Fortune Lady Past",
    "Fortune Lady Water",
    "Fortune Lady Wind",
    "Gradius' Option",
    "Greed Quasar",
    "Gren Maju Da Eiza",
    "Helios - The Primordial Sun",
    "Helios Duo Megistus",
    "Helios Trice Megistus",
    "Holactie the Creator of Light",
    "Leafplace Plaice",
    "Ma'at",
    "Megarock Dragon",
    "Odd-Eyes Revolution Dragon",
    "Parasitic Ticky",
    "Scanner",
    "Slifer the Sky Dragon",
    "Starduston",
    "Ten Thousand Dragon",
    "The Wicked Avatar",
    "The Wicked Eraser",
    "The Winged Dragon of Ra",
    "The Winged Dragon of Ra - Sphere Mode",
    "Tragoedia",
    "Winged Kuriboh LV9",
    "Yosenju Oyam",
}
QM_ATK = {
    "Arcana Triumph Joker",
    "Blackwing - Aurora the Northern Lights",
    "Clear Vice Dragon",
    "D/D/D Destiny King Zero Laplace",
    "Darton the Mechanical Monstrosity",
    "Divine Serpent Geh",
    "Endless Decay",
    "Exodius the Ultimate Forbidden Lord",
    "Gogogo Golem - Golden Form",
    "Kasha",
    "King of the Skull Servants",
    "Maju Garzett",
    "Montage Dragon",
    "Orichalcos Shunoros",
    "Rai-Jin",
    "Super Anti-Kaiju War Machine Mecha-Dogoran",
    "Supreme Sovereign Serpent of Golgonda",
    "The Calculator",
    "The Legendary Exodia Incarnate",
    "Tyranno Infinity",
}
QM_DEF = {'Lost Guardian'}


def get_all_monsters_for_small_world():
    parameters = {}
    parameters['type'] = ALL_MAIN_DECK_MONSTER_MONSTER_TYPES
    parameters['misc'] = 'yes'
    response = requests.get(
        'https://db.ygoprodeck.com/api/v7/cardinfo.php', params=parameters
    )
    response_json = response.json()

    # deal with ? atk/def
    for i in range(len(response_json['data'])):
        if response_json['data'][i]['name'] in QM_ATK_AND_DEF:
            response_json['data'][i]['atk'] = -i - 1 
            response_json['data'][i]['def'] = -i - 1
        if response_json['data'][i]['name'] in QM_ATK:
            response_json['data'][i]['atk'] = -i - 1
        if response_json['data'][i]['name'] in QM_DEF:
            response_json['data'][i]['def'] = -i - 1

    return response_json
