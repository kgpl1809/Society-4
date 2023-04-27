# Society-4

Read this document in [english](README_en.md)

**Un jeu similaire au "échecs" avec quelques modifications faites avec pyxel !**

![Screenshot_7](https://user-images.githubusercontent.com/131471941/234773177-534e65c6-808a-42e8-9e9d-eaa4292bccef.png)

## Demo 

https://user-images.githubusercontent.com/131470894/234392432-969cdbd2-0002-4b1d-9394-54a8b300baf0.mp4



## Caractéristiques


### les échecs mais à notre manière...

On s'est inspiré de la société moderne de nos jours pour modifier et changer les pièces présentés aux échecs.
Cependant, on a apporté divers modifications au jeu originale telles que :
  - Society^4 est jouée avec 4 joueurs 
  - Toutes les pièces possèdent des capacités sauf le citoyen, ces capacités sont différentes en fonction des pièces
  - Les pièces peuvent se morpher au niveau supérieure dans la hiérarchie
  - Le plateau est un plateau identique aux echecs, mais avec des demis plateau d'échec ajoute sur chaque côté, ce qui forme sur sorte de croix
  
  
#### Menu
  - Quelques secrets cachés dans le menu, à vous de les trouver !

### Python et Pyxel

Le module pyxel a été utilisé pour afficher toutes les pièces et icônes. Le code est donc divisé en deux grandes parties, la partie avec tous les calculs et la partie graphique avec tout l'affichage. L'utilisation des dictionnaires est aussi omniprésente à travers le code pour pouvoir attribuer à chaque objet des paramètres. 
Pyxel étant un module utilisé durant toute l'année de NSI pour nous entraîner à la nuit du code. Ainsi ce projet nous a aussi permis de nous préparer pour la Nuit Du Code. 

### Affichage et Dessins sur Pyxel

Les sprites dessinés sur Pyxel ont été faits à la main sans objet de référence, ni d'idée spécifique en tête. On a dû imaginer et s'inspirer un peu de ce qu'on imaginait quand on pensait aux pièces que l'on a dessiné. L'affichage des capacités a été assez long et difficile, comme on voulait donner un effet d'animation pour les capacités de chaque pièce. Il a fallu dessiner plusieurs fois la même image mais en modifiant son apparence et les affiches répétitivement les unes après les autres pour donner cet effet d'animation. Le nombre d'images et de sprites dessinés dépasse largement ce qu'on pensait originellement.

### Menu et Easter Egg

  - Menu interactif pour permettre à l'utilisateur de comprendre comment le jeu fonctionne.
  - Les Easter Egg peuvent être accéder afin de  jouer à des mini-jeux.
  - Attraper une étoile qui se balade dans un des menus ? Cliquer sur tout ce qui bouge ? Plein de choses à découvrir  !


### Installation
![Screenshot_7](https://user-images.githubusercontent.com/131470894/234654262-fad628ea-0ebc-4b06-b267-bbd3fad3b15a.png)



Quant à l'installation du module random, il suffit de remplacer dans la commande ci-dessus : "pyxel" par "random"

### Utilisation 

On a rendu l'interface d'utilisateur assez simple à naviguer afin de faciliter l'accessibilité à notre jeu. Il n y a donc pas de commandes additionnelles à entrer lorsque le jeu est lancé. Cependant, si il arrive à notre jeu d'arrêter de fonctionner, veuillez rafraîchir la page sur laquelle vous êtes, ou de relancer le code dépendant de comment vous avez lancé le code.

### Le lien vers le pyxel.net
https://www.pyxelstudio.net/ps/r9t5vw7d



# 1 - Les regles

Society^4 est un jeu semblable au échecs à 4 joueurs en local. Chaque joueur possède 16 pièces, dont 8 Citoyens, 2 Ouvriers , 2 Soldats , 2 Pirates , 1 Ministre , 1 Président. Pour gagner la partie il faut être le seul à avoir son président en vie, il faut prendre en considération qu'un joueur peut être éliminé s'il ne joue pas dans le temps imparti chaque tour. 



Les joueurs pourront choisir le mode qu'ils souhaitent : mode facile - 1 min par tour ; mode moyen - 30 sec par tour ; 
mode extrême - 9 sec par tour. Contrairement au jeu d'échecs traditionnel, toutes les pièces possèdent des capacités spéciales.




## Comment jouer ?

Quand vous lancez le jeu, un menu sera affiché avec plusieurs options : "Jouer", "Paramètres", "Aide", les "Crédits" et l'option "Quitter" pour fermer le jeu. Puis dans l'Aide la description brève de chaque pièce et des règles du jeu.  Le mode de déplacement est avec la souris, et pour cela vous devez sélectionner la pièce que vous souhaitez déplacer en cliquant dessus, puis choisir une des cases disponible en fonction du mouvement de cette pièce qui sera affichée. 

Et ca tourne ! 


Faites attention... L'utilisation de la capacité de n'importe quelle pièce consomme votre tour.
## La hiérarchie des pions

Lorsqu'une pièce capture un ministre quelconque, ce dernier évolue au niveau supérieur. Vous trouverez l'ordre d'évolution dans l'image ci-dessous :
![Hierarchie pieces](https://user-images.githubusercontent.com/131470894/233690765-9510fd53-e26f-488a-9058-b12a23243817.png)



# 2 - Les pieces


## Chaque pièce est différente 
  - Le "Citoyen" est le pion des échecs qui peut se déplacer de deux cases dans une direction au premier tour puis se déplace d'une case, peut capturer une autre pièce en diagonale 


  - L' "Ouvrier" est le chevalier des échecs qui se déplace en L (deux cases dans une direction, puis une case vers la gauche ou la droite) et peut capturer des pièces de cette façon 


  - Le "Soldat" est la tour des échecs qui se déplace horizontalement et verticalement uniquement et peut capturer des pièces de cette façon. Quand cette pièce est capturée, elle laissera une tombe sur cette case, bloquant la case et pourra se faire réanimer par un des Ministres. Attention la tombe peut se faire manger par un citoyen qui deviendra alors un zombie.

  - Le "Pirate" est le fou des échecs qui se déplace diagonalement uniquement et peut capturer des pièces de cette façon. Quand cette pièce est capturée, elle laissera une tombe sur cette case, bloquant la case et pourra se faire réanimer par un des Ministres. 


  - Le "Ministre" est la reine des échecs qui peut se déplacer en diagonale, horizontale, verticale et peut capturer des pièces de cette façon 


  - Le "Président" est le roi des échecs qui peut se déplacer d'une case dans n'importe quelle direction et peut capturer des pièces de cette façon, lorsque le Roi d'une équipe meurt celle-ci est éliminé 


  - La tombe apparaît sur la case lors de la mort d'un Soldat ou d'un Pirate. Cette tombe bloque la case sur laquelle elle se trouve indéfiniment, cependant un des 4 ministres que l'on peut choisir au début de la partie peut ranimer la pièce perdue au combat.


### _Les capacites_
  - Le Citoyen : ne possède pas de capacités, se transforme en Ouvrier suite à la capture d'un Ministre


  - L'Ouvrier : peut bloquer une case pour 4 tour, se transforme en Soldat suite à la capture d'un Ministre (4 tours de rechargement, dans un cercle de rayon de 2 cases)



![image_ouvrier](https://user-images.githubusercontent.com/131470894/234656664-091257e7-96d7-45d5-bcf8-1b0dfc23407d.png)
![image_ouvrier_capa](https://user-images.githubusercontent.com/131470894/234656675-fe9c176d-779f-4870-9316-8dc6852a5e88.png)



  - Le Soldat : peut poser une mine à proximité qui dure 9 tours, qui élimine un pion qui atterrit dessus, se transforme en Pirate suite à la capture d'un Ministre (7 tours de rechargement, dans un rayon de 2 cases autour de lui)


![image_soldat_capa](https://user-images.githubusercontent.com/131470894/234657525-1c7a633e-33f8-42eb-8111-054889eac218.png)


  - Le Pirate : peut déplacer une pièce allie dans un rayon de 2 cases autour peu importe sa catégorie d'une façons prédéfinie, se transforme en Ministre suite à la capture d'un Ministre (12 tours de rechargement). Il peut aussi déplacer des tombes qui pourront alors capturer d'autre pièce. Attention si la tombe tue un ministre, la pièce sera réanimée mais recevra aussi son évolution.

  - Le Ministre : Quand un Ministre est capturé par un autre Ministre il ameliore la capacite de ce dernier (Dure plus longtemps et moins de temps de rechargement).
      - Ministre 1 : met le feu a une case choisi sur une durée de 3 tours 
      
    
       ![image_ministre_feu](https://user-images.githubusercontent.com/131470894/234657011-23e013f3-17b7-48f6-8b9c-491e3e359134.png)


      - Ministre 2 : pose une prison sur une pièce choisie qui dure 2 tours, tue la pièce prise si elle bouge


       ![image_ministre_prison](https://user-images.githubusercontent.com/131470894/234657215-620a2b33-8493-4dc7-b2ca-4a793beec197.png)


      - Ministre 3 : a la possibilité de réanimer un cadavre laissé par un Pirate ou un Soldat en Ouvrier 


      - Ministre 4 : donne un bouclier qui protège la piece choisi seulement allié et pas le Président qui disparait quand la pièce bouge 1 fois 


       ![image_ministre_bouclier](https://user-images.githubusercontent.com/131470894/234657200-9d33cd7e-4443-4dfa-b823-e0ba2503a94d.png)



## License de Pacman


BANDAI NAMCO Entertainment owns famous franchises and offers a variety of video games licences, targeting a wide range of customers: we have games for everyone!

© 2010 - 2023 Bandai Namco Europe S.A.S


