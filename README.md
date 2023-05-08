# About this Program
## Background on Small World
Small World is one of the more interesting card in the game of Yu-Gi-Oh!. Using it, you can search for almost any monster in the game based upon your deck composition and a monster in your hand that you are willing to give up.
Every Yu-Gi-Oh monster has 5 characteristics that are vital to using Small World:
- Type
- Attribute
- Level
- ATK (Attack)
- DEF (Defense)
Small World uses exactly 1 characteristic to bridge from a Starting Card to a Bridge Card to the Target Card. To explain in detail:
1. Using the Starting Card, you would then find a card(s) in your deck that share exactly 1 characteristic with the Starting Card. This will be our Bridge Card.
2. Then using the Bridge Card, you would then find a card(s) in your deck that share exactly 1 characteristic with the Bridge Card. This will be our Target Card.

DIAGRAM: Starting Card ---bridges to---> Bridge Card ---bridges to---> Target Card
e.g. Blue-Eyes White Dragon -> Effect Vieler -> Dark Magician 

Note: Monsters with undefined ATK or DEF indicated by ‘?’ cannot use that characteristic for bridging with Small World. The reason why is that currently ‘?’ ATK/DEF does not compare to anything (see related rulings).
## What this Program accomplishes
Requirements: A YDK file of your Yu-Gi-Oh! deck
This program is used to accomplish 3 things:
- Given a Starting Card and a Target Card, returns a list of possible Bridge Cards to complete Small World. 
- Return a list of cards that share exactly 1 characteristic.
- Tells how well Small World would work in your deck.

## Credits
Credit to YGOPRODECK for their API to get all the monsters within the game and credit to Gabrial Netz of the Disciples on Youtube for his code as a starter.

