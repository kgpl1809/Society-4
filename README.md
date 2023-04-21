# Society-4

Read this document in .[english]

**Un jeu similaire au "echecs" avec quelques modifications fait avec pyxel !**

(un screen de notre jeu)

## Caracteristiques

### Les echecs mais un peu different...

On s'est inspire de la hierarchie de la societe moderne de nos jours pour modifier et changer les pieces presentes aux echecs.
Cependant, on a apporte divers modifications au jeu originale telles que :
  - Society^4 est jouee avec 4 joueurs au lieu de 2
  - Tout les pions possedent des capacites sauf le citoyen etant l'equivalent du pion, ces capacites sont uniques a la categorie du pion
  - Les pions peuventse moprher au niveau superieure dans la hierarchie si et seulement si ce dernier effectue une capture du Ministre etant la Reine

#####
On a utiliser le module Pyxel sur le language Python pour faire imiter le jeu des echecs. Les modifications apportes sont les suivantes :
    - Chaque piece est differente :
          - Le "Citoyen" est le pion des echecs qui peut se deplacer de deux cases dans une direction au premier tour puis se deplace d'une case, peut "manger" ou capturer une autre piece en diagonale. Se transforme en 
          - L' "Ouvrier" est le chevalier des echecs qui se deplace en L (deux cases dans une direction, puis une case dans une autre) et peut capturer des pieces de cette facon
          - Le "Soldat" est la tour des echecs qui se deplace d'autant de cases qu'il ne veut horizontalement et verticalement uniquement et peut capturer des pieces de cette facon. Quand cette piece est capturee, elle laissera un "cadavre" sur cette case, bloquant la case et pourra se faire reanimer par un des Ministres, disparaitra apres (jsp cb de tours, on peut pas faire ca etre infinie) 
          - Le "Pirate" est le fou des echecs qui se deplace d'autant de cases qu'il ne veut diagonalement uniquement et peut capturer des pieces de cette facon. Quand cette piece est capturee, elle laissera un "cadavre" sur cette case, bloquant la case et pourra se faire reanimer par un des Ministres, disparaitra apres (jsp cb de tours, on peut pas faire ca etre infinie) 
          - Le "Ministre" est la reine des echecs qui peut se deplacer d'autant de case qu'il ne veut en diagonale, horizontale, verticale et peut capturer des pieces de cette facon
          - Le "President" est le roi des echecs qui peut se deplacer d'une case dans n'importe quelle direction et peut capturer des pieces de cette facon, lorsque le Roi d'une equipe meurt celle-ci est elimine

####**Les capacites**
  - Le Citoyen : ne possede pas de capacites, se transforme en Ouvrier suite a la capture d'un Ministre
  - L'Ouvrier : peut bloquer une case pour 1 tour, se transforme en Soldat suite a la capture d'un Ministre
  - Le Soldat : peut poser une mine a proximite qui elimine un pion qui atterit dessus, se transforme en Pirate suite a la capture d'un Ministre
  - Le Pirate : peut deplacer un pion allie peut importe de facons predefinies, se transforme en Ministre suite a la capture d'un Ministre
  - Le Ministre : Quand un Ministre est capture par un autre Ministre il transmet ca capacite a ce dernier, ou ameliore une des capacite si ils possedent la meme
      - Ministre 1 : met le feu a une case choisi sur une duree de 3 tours --> (amelioration de la capacite) le feu dure 5 tours au lieu de 3 tours
      - Ministre 2 : pose une prison sur une piece choisi qui dire 2 tours, tue la piece prise si elle bouge --> (amelioration de la capacite) la prison dure 3 tours au lieu de 2 tours
      - Ministre 3 : a la possibilite de reanimer un cadavre laisse par un Pirate ou un Soldat en Ouvrier --> (amelioration de la capacite) reanime les Soldats en Soldats et les Pirates en Pirates
      - Ministre 4 : pose une bouclier qui protege la piece choisi (allie, pas le President) qui disparait quand la piece bouge 1 fois--> (amelioration de la capacite) le bouclier disparaitra apres que la piece bouge 2 fois
    
