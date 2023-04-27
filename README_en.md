# Society-4

Lisez ce document en [français](README.md)

**A game similar to "chess" with some modifications made with pyxel ! **

![Screenshot_7](https://user-images.githubusercontent.com/131471941/234773177-534e65c6-808a-42e8-9e9d-eaa4292bccef.png)

## Demo 

https://user-images.githubusercontent.com/131470894/234392432-969cdbd2-0002-4b1d-9394-54a8b300baf0.mp4



## Features


### Chess but in our way...

We have been inspired by the modern society of our days to modify and change the pieces presented in chess.
However, we have made various modifications to the original game such as :
  - Society^4 is played with 4 players 
  - All pieces have abilities except the citizen, these abilities are different depending on the pieces
  - Pieces can morph to the next level in the hierarchy
  - The board is a chess-like board, but with half chess boards added on each side, which forms a kind of cross
  
  
### Menu
  - Some secrets hidden in the menu, you have to find them !

### Python and Pyxel

The pyxel module has been used to display all the pieces and icons. So the code is divided in two big parts, the part with all the calculations and the graphical part with all the display. The use of dictionaries is also omnipresent throughout the code to be able to assign parameters to each object. 
Pyxel being a module used during all the year of NSI to train us to the night of the code. So this project also allowed us to prepare for the Night of Code. 

### Display and Drawings on Pyxel

The sprites drawn on Pyxel were done by hand without any reference object or specific idea in mind. We had to imagine and draw a little from what we imagined when we thought about the parts we drew. The display of the abilities was quite long and difficult, as we wanted to give an animated effect for the abilities of each piece. We had to draw the same image several times but change its appearance and display them repeatedly one after another to give this animation effect. The number of images and sprites drawn far exceeds what was originally thought.

### Menu and Easter Egg

  - Interactive menu to allow the user to understand how the game works.
  - Easter Eggs can be accessed to play mini-games.
  - Catch a star that is wandering in one of the menus? Click on anything that moves? Lots of things to discover!


### Installation
![Screenshot_7](https://user-images.githubusercontent.com/131470894/234654262-fad628ea-0ebc-4b06-b267-bbd3fad3b15a.png)



As for the installation of the random module, you just have to replace in the above command : "pyxel" by "random".

### Usage
We have made the user interface quite simple to navigate in order to facilitate the accessibility of our game. So there are no additional commands to enter when the game is running. However, if it happens that our game stops working, please refresh the page you are on, or restart the code depending on how you started the code.

### The link to pyxel.net
https://www.pyxelstudio.net/ps/r9t5vw7d

# 1 - The Rules

Society^4 is a game similar to chess with 4 players in local. Each player has 16 pieces, including 8 Citizens, 2 Workers, 2 Soldiers, 2 Pirates, 1 Minister, 1 President. To win the game, you must be the only one to have your president alive, taking into consideration that a player can be eliminated if he doesn't play within the time limit of each turn. 



Players can choose the mode they want: easy mode - 1 min per turn; medium mode - 30 sec per turn; 
extreme mode - 9 sec per turn. Unlike traditional chess, all pieces have special abilities.




## How to play?

When you start the game, a menu will be displayed with several options: "Play", "Settings", "Help", "Credits" and the "Quit" option to close the game. Then in the Help section you will find a brief description of each piece and the rules of the game.  The movement mode is with the mouse, and for this you have to select the piece you want to move by clicking on it, then choose one of the available boxes according to the movement of this piece that will be displayed. 

And it turns! 


Be careful... Using the ability of any piece consumes your turn.
## The pawn hierarchy

When a piece captures any minister, it evolves to the next level. You can see the order of evolution in the image below:
![Hierarchie pieces](https://user-images.githubusercontent.com/131470894/233690765-9510fd53-e26f-488a-9058-b12a23243817.png)



# 2 - The pieces


## Each piece is different 
  - The "Citizen" is the chess piece which can move two squares in one direction at the first turn then move one square, can capture another piece diagonally 


  - The "Worker" is the chess knight who moves in an L-shape (two squares in one direction, then one square to the left or right) and can capture pieces in this way 


  - The "Soldier" is the chess rook that moves horizontally and vertically only and can capture pieces in this way. When this piece is captured, it will leave a grave on this square, blocking the square and can be reanimated by one of the Ministers. Be careful, the grave can be eaten by a citizen who will then become a zombie.

  - The "Hacker" is the chess bishop that moves diagonally only and can capture pieces in this way. When this piece is captured, it will leave a grave on that square, blocking the square, and can be reanimated by one of the Ministers. 


  - The "Minister" is the chess queen who can move diagonally, horizontally and vertically and can capture pieces in this way 


  - The "President" is the chess king who can move one square in any direction and can capture pieces in this way, when the king of a team dies it is eliminated 




  - The tomb appears on the square when a Soldier or Pirate dies. This tomb blocks the square it is on indefinitely, however one of the 4 ministers that can be chosen at the beginning of the game can revive the piece lost in battle.


### Abilities
  - The Citizen : has no abilities, transforms into a Worker after the capture of a Minister


  - The Worker : can block a square for 4 turns, transforms into a Soldier following the capture of a Minister (4 turns of reloading, in a circle of radius of 2 squares)



![image_ouvrier](https://user-images.githubusercontent.com/131470894/234656664-091257e7-96d7-45d5-bcf8-1b0dfc23407d.png)
![image_ouvrier_capa](https://user-images.githubusercontent.com/131470894/234656675-fe9c176d-779f-4870-9316-8dc6852a5e88.png)



  - The Soldier: can lay a mine nearby which lasts 9 turns, eliminates a counter that lands on it, turns into a Hacker after capturing a Minister (7 turns of reloading, in a radius of 2 squares around him)


![image_soldat_capa](https://user-images.githubusercontent.com/131470894/234657525-1c7a633e-33f8-42eb-8111-054889eac218.png)


  - The Hacker : can move an allied piece within a radius of 2 squares around it, regardless of its category, in a predefined way, transforms into a Minister following the capture of a Minister (12 reloading turns). It can also move tombs which can then capture other pieces. Be careful if the tomb kills a minister, the piece will be reanimated but will also receive its evolution.

  - The Minister : When a Minister is captured by another Minister, he improves the capacity of the latter (Lasts longer and less time to reload).
      - Minister 1 : set fire to a chosen square for 3 turns 
      
    
       ![image_ministre_feu](https://user-images.githubusercontent.com/131470894/234657011-23e013f3-17b7-48f6-8b9c-491e3e359134.png)


      - Minister 2 : puts a prison on a chosen piece which lasts 2 turns, kills the taken piece if it moves


       ![image_ministre_prison](https://user-images.githubusercontent.com/131470894/234657215-620a2b33-8493-4dc7-b2ca-4a793beec197.png)


      - Minister 3 : has the ability to reanimate a corpse left by a Pirate or a Soldier as a Worker 


      - Minister 4 : gives a shield that protects the piece chosen only ally and not the President who disappears when the piece moves 1 time 


       ![image_ministre_bouclier](https://user-images.githubusercontent.com/131470894/234657200-9d33cd7e-4443-4dfa-b823-e0ba2503a94d.png)



## License of Pacman


BANDAI NAMCO Entertainment owns famous franchises and offers a variety of video games licences, targeting a wide range of customers: we have games for everyone!

2010 - 2023 Bandai Namco Europe S.A.S
