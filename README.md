# Space-Racing-Game
#### Space Racing Game with Sprites, Source Code, and Pickle File to Store Local High Scores

## Game Overview
<img width="746" alt="Screen Shot 2022-03-23 at 9 42 25 PM" src="https://user-images.githubusercontent.com/100534404/159825354-d7f5c583-240d-44ba-bcaf-85e29fe6a4a1.png">

The space racing game is a game where the goal is to travel as far as possible. There is a limited amount of gas and ammo with enemy ships attacking your ship as you travel through space.

<img width="700" alt="Screen Shot 2022-03-23 at 9 43 20 PM" src="https://user-images.githubusercontent.com/100534404/159825381-bb80712b-f4e3-4f5a-8b7b-cbddcf7bc618.png">

While traveling, the ship gradually gains more and more speed; however, there are asteroid belts along the way that can stop your ship causing you to need to regain speed all over again. Every astroid belt passed is 1 point, but there are cows in addition that can provide a multiplier if the cows are picked up.

<img width="750" alt="Screen Shot 2022-03-23 at 9 43 38 PM" src="https://user-images.githubusercontent.com/100534404/159825395-dfc02d15-a282-4e5f-bcf0-e424ed0fdc9d.png">

There are various enemy ships such as gap ships which are small ships that float between the crack of the astroids, normal enemy ships which stay in one place in the path between the astroid belts, and greater enemy ships which move around attacking at rapid speeds. There are also 1-3 different sprites for each type of enemy, ammo boxes, gas containers, and cows. Encounters seen between asteroid belts are entirely random encounters, favoring some types of bonuses and enemy appearances over others.

<img width="752" alt="Screen Shot 2022-03-23 at 9 44 01 PM" src="https://user-images.githubusercontent.com/100534404/159825408-8e2f8573-bd1e-40ce-b37e-fc3c916df659.png">

The game, sprites, and many ideas are inspired by the anime "Cowboy Bebop."


https://user-images.githubusercontent.com/100534404/159826934-ce457644-42ed-4a8c-a6d8-b649e3207e41.mov

## How to Play
### Setup
In order to get set-up, the folder containing the sprites, scripts, and pickle file must all first be downloaded.

To play the game through Anaconda, the Anaconda navigator must first be opened and pygame must be installed using:
!pip install pygame

After installation, the script can be opened and ran. I would recommend running it on Spyder.

### Controls

The controls are simple. You can move in 8 directions using the 4 arrow keys and combonations of each to move diagonally. The space bar is how the player shoots. Note that not only can you shoot enemies, but the bonuses like ammo, gas canisters, and cows as well. So it's best to aim carefully.

## Future Improvements

Things this game will eventually add:
 * A resetting script to reset the high score
 * More enemies (bosses)
 * An option to slightly slow down when a certain speed is achieved allowing one to maintain greater speeds for longer
