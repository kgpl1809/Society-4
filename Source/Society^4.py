
import pyxel
import random


pyxel.init(384, 256,  title="Society ^ 4", fps=30)



pyxel.load("assets/res_3.pyxres")




###################################################################################
selected_option = 0
menu = ["Jouer", "Credits", "Aide", "Quitter"]
pyxel.mouse(True)
game = False # variable pour commencer le jeu
credit = False
frame_click = pyxel.frame_count
about = False
pieces = False
r1 = False
pacman = " "
ability = False
mecanique = False


#jeu : OX
OX = False
board = [[' '] * 3 for i in range(3)]
current_player = 'X'
winner = None
game_over = False
winning_coords = None
player_X_wins = 0
player_O_wins = 0

#jeu : snake
apple_x = random.randint(0, 368)
apple_y = random.randint(0, 240)
show_apple = False
frame_apple = pyxel.frame_count
snake_game = False
snake = [(384 // 2, 256 // 2)]
direction = (0, 0)
score = 0
game_over = False
fruit = (random.randint(0, 23) * 16, random.randint(0, 15) * 16)

#jeu : breakout
breakout = False
score1 = 0
lives = 3
ball_x = 60
ball_y = 80
ball_dx = 1
ball_dy = 1
paddle_x = 144
paddle_y = 210
paddle_dx = 0
bricks = []
extra_balls = []
all_bricks_destroyed = False
ball_speed = 1

# position initiale du pacman
pacman_x = 100
pacman_y = 100

#############################################################################3
def generate_bricks():
    global bricks

    bricks = []
    for row in range(5):
        brick_row = []
        for col in range(14):
            if random.randint(0, 4) == 0:
                brick_row.append(2)
            else:
                brick_row.append(1)
        bricks.append(brick_row)

def restart_breakout():
    global score1, lives, ball_x, ball_y, ball_dx, ball_dy, paddle_x, paddle_y, extra_balls, all_bricks_destroyed, ball_speed

    score1 = 0
    lives = 3
    ball_x = 60
    ball_y = 80
    ball_dx = 1
    ball_dy = 1
    paddle_x = 144
    paddle_y = 210
    extra_balls = []
    all_bricks_destroyed = False
    ball_speed = 1
    generate_bricks()

def update_ball_position():
    global ball_x, ball_y, ball_dx, ball_dy, paddle_x, paddle_y, score1, lives, extra_balls, ball_speed

    ball_x += ball_dx * ball_speed
    ball_y += ball_dy * ball_speed

    if ball_x <= 0 or ball_x + 4 >= 384:
        ball_dx *= -1
    if ball_y <= 0:
        ball_dy *= -1

    if ball_y + 4 >= paddle_y and ball_x >= paddle_x and ball_x <= paddle_x + 60:
        ball_dy *= -1

    for row in range(5):
        for col in range(14):
            if bricks[row][col] != 0:
                brick_x = col * (26 + 1)
                brick_y = row * (12 + 1)
                if ball_y <= brick_y + 12 and ball_x + 4 >= brick_x and ball_x <= brick_x + 26:
                    if bricks[row][col] == 2:
                        add_extra_ball(ball_x, ball_y)
                    ball_dy *= -1
                    bricks[row][col] = 0
                    score1 += 10

    if ball_y + 4 >= 256:
        lives -= 1
        ball_x = 60
        ball_y = 80
        ball_dx = 1
        ball_dy = 1

    for extra_ball in extra_balls:
        extra_ball[0] += extra_ball[2] * ball_speed
        extra_ball[1] += extra_ball[3] * ball_speed
        if extra_ball[0] <= 0 or extra_ball[0] + 4 >= 384:
            extra_ball[2] *= -1
        if extra_ball[1] <= 0:
            extra_ball[3] *= -1
        if extra_ball[1] + 4 >= 256:
            extra_balls.remove(extra_ball)
            lives -= 1
        elif extra_ball[1] + 4 >= paddle_y and extra_ball[0] >= paddle_x and extra_ball[0] <= paddle_x + 60:
            extra_ball[3] *= -1
        for row in range(5):
            for col in range(14):
                if bricks[row][col] != 0:
                    brick_x = col * (26 + 1)
                    brick_y = row * (12 + 1)
                    if extra_ball[1] <= brick_y + 12 and extra_ball[0] + 4 >= brick_x and extra_ball[0] <= brick_x + 26:
                        if bricks[row][col] == 2:
                            add_extra_ball(extra_ball[0], extra_ball[1])
                        extra_ball[3] *= -1
                        bricks[row][col] = 0
                        score1 += 10

def add_extra_ball(ball_x, ball_y):
    global extra_balls

    new_ball_dx = ball_dx
    new_ball_dy = ball_dy

    extra_balls.append([ball_x, ball_y, new_ball_dx, new_ball_dy])

def update_paddle_position():
    global paddle_x, paddle_dx

    if pyxel.btn(pyxel.KEY_LEFT):
        paddle_dx = -4
    elif pyxel.btn(pyxel.KEY_RIGHT):
        paddle_dx = 4
    else:
        paddle_dx = 0

    paddle_x += paddle_dx

    if paddle_x <= 0:
        paddle_x = 0
    if paddle_x + 60 >= 384:
        paddle_x = 384 - 60

def draw_breakout():
    pyxel.cls(0)

    all_bricks_destroyed = True
    for row in range(5):
        for col in range(14):
            if bricks[row][col] == 1:
                all_bricks_destroyed = False
                brick_x = col * (26 + 1)
                brick_y = row * (12 + 1)
                pyxel.rect(brick_x, brick_y, 26, 12, 8)
            elif bricks[row][col] == 2:
                all_bricks_destroyed = False
                brick_x = col * (26 + 1)
                brick_y = row * (12 + 1)
                pyxel.rect(brick_x, brick_y, 26, 12, 9)

    if lives > 0 and not all_bricks_destroyed:
        pyxel.circ(ball_x, ball_y, 4, 7)

    if lives > 0 and not all_bricks_destroyed:
        for extra_ball in extra_balls:
            pyxel.circ(extra_ball[0], extra_ball[1], 4, 7)

    pyxel.rect(paddle_x, paddle_y, 60, 10, 7)

    pyxel.text(5, 5, "Score: {}".format(score1), pyxel.frame_count % 16)
    if lives > 0:
        pyxel.text(384 - 40, 5, "Lives: {}".format(lives), pyxel.frame_count % 16)
    elif lives < 0:
        pyxel.text(384 - 40, 5, "Lives: 0", pyxel.frame_count % 16)

    if lives <= 0 or all_bricks_destroyed:
        pyxel.text(384 // 2 - 55, 256 // 2, "Press R to restart", 8)

def update_breakout():
    global lives, all_bricks_destroyed, ball_speed

    update_ball_position()
    update_paddle_position()

    if len(extra_balls) > 0:
        ball_speed = 1 + len(extra_balls) * 0.2

    if all_bricks_destroyed and pyxel.btn(pyxel.KEY_R):
        restart_breakout()

    if lives <= 0 and pyxel.btn(pyxel.KEY_R):
        restart_breakout()

def draw_snake():
    for x, y in snake:
        pyxel.rect(x, y, 16, 16, 5)

def move_snake():
    global snake, direction, game_over, fruit, score

    x, y = snake[0]
    dx, dy = direction
    head = ((x + dx * 16) % 384, (y + dy * 16) % 256)

    if collision(head[0], head[1], fruit[0], fruit[1], 16, 16, 16, 16):
        score += 1
        fruit = (random.randint(0, 23) * 16, random.randint(0, 15) * 16)
        snake.append(head)
    else:
        snake.pop()
        snake.insert(0, head)

    if head[0] < 0 or head[0] > 384 - 12 or head[1] < 0 or head[1] > 256 - 16:
        game_over = True

def update_direction():
    global direction

    if pyxel.btnp(pyxel.KEY_UP):
        direction = (0, -0.1)
    elif pyxel.btnp(pyxel.KEY_DOWN):
        direction = (0, 0.1)
    elif pyxel.btnp(pyxel.KEY_LEFT):
        direction = (-0.1, 0)
    elif pyxel.btnp(pyxel.KEY_RIGHT):
        direction = (0.1, 0)

def update_snake():
    global score

    if not game_over:
        move_snake()
        update_direction()

    if pyxel.btnp(pyxel.KEY_R) and game_over:
        restart_game()

def draw_snake_game():
    global score, snake_game, credit
    pyxel.cls(0)
    pyxel.bltm(0, 0, 0, 576, 0, 384, 256)
    text_len = len("Pieces") * pyxel.FONT_WIDTH
    if pyxel.mouse_x >= pyxel.width - text_len and pyxel.mouse_x <= pyxel.width and pyxel.mouse_y >= pyxel.height - pyxel.FONT_HEIGHT and pyxel.mouse_y <= pyxel.height:

        # dessine rectangle qui clignote
        if pyxel.frame_count % 20 < 10:
            pyxel.rect(pyxel.width - text_len - 2, pyxel.height - pyxel.FONT_HEIGHT - 1, text_len + 4,
                       pyxel.FONT_HEIGHT + 2, 7)
        pyxel.text(pyxel.width - text_len, pyxel.height - pyxel.FONT_HEIGHT, "Retour", 0)
        if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
            snake_game = False
            credit = True
    else:
        pyxel.text(pyxel.width - text_len, pyxel.height - pyxel.FONT_HEIGHT, "Retour", 7)
    if not game_over:
        draw_snake()
        pyxel.blt(fruit[0], fruit[1], 0, 80, 64, 16, 16, 0)
        pyxel.blt(0, 0, 0, 80, 64, 16, 16, 0)
        pyxel.text(20, 5, str(score), 7)


    if game_over:
        pyxel.text(100, 100, "GAME OVER", 8)
        pyxel.text(100, 110, "Press R to restart", 8)
        pyxel.blt(0, 0, 0, 80, 64, 16, 16, 0)
        pyxel.text(20, 5, str(score), 7)

def restart_game():
    global snake, direction, score, game_over, fruit

    snake = [(384 // 2, 256 // 2)]
    direction = (0, 0)
    score = 0
    game_over = False
    fruit = (random.randint(0, 23) * 16, random.randint(0, 15) * 16)

def collision(x, y, x_1, y_1, boundrie_height, boundrie_width, boundrie_width_1, boundrie_height_1):
    if (x - boundrie_width_1 + 1 <= x_1 <= x + boundrie_width) and (y - boundrie_height_1 + 1 <= y_1 <= y + boundrie_height):
        return True
    else:
        return False

def update_apple():
    global show_apple, apple_x, apple_y, frame_apple, snake_game

    if pyxel.frame_count % 300 == 0:
        a = random.randint(0, 1)
        if a == 0:
            show_apple = True
            apple_x = random.randint(0, 368)
            apple_y = random.randint(0, 240)
            frame_apple = pyxel.frame_count

    if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x >= apple_x and pyxel.mouse_x <= apple_x + 16 and pyxel.mouse_y >= apple_y and pyxel.mouse_y <= apple_y + 16:
        snake_game = True
        show_apple = False

    elif show_apple and pyxel.frame_count >= frame_apple + 60:
        show_apple = False

def play(row, col):
    global current_player, winner, game_over, winning_coords, player_O_wins, player_X_wins
    if row >= 0 and row < 3 and col >= 0 and col < 3 and board[row][col] == ' ':
        board[row][col] = current_player
        if check_win():
            winner = current_player
            game_over = True
            winning_coords = get_winning_coords()
            if winner == 'X':
                player_X_wins += 1
            else:
                player_O_wins += 1
        elif check_tie():
            game_over = True
        else:
            current_player = 'O' if current_player == 'X' else 'X'

def check_win():
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != ' ':
            return True
        elif board[0][i] == board[1][i] == board[2][i] != ' ':
            return True
    if board[0][0] == board[1][1] == board[2][2] != ' ':
        return True
    elif board[0][2] == board[1][1] == board[2][0] != ' ':
        return True
    else:
        return False

def check_tie():
    for row in board:
        for col in row:
            if col == ' ':
                return False
    return True

def reset():
    global board, current_player, winner, game_over, winning_coords
    board = [[' '] * 3 for i in range(3)]
    current_player = 'X'
    winner = None
    game_over = False
    winning_coords = None

def get_winning_coords():
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != ' ':
            return [(i, 0), (i, 1), (i, 2)]
        elif board[0][i] == board[1][i] == board[2][i] != ' ':
            return [(0, i), (1, i), (2, i)]
    if board[0][0] == board[1][1] == board[2][2] != ' ':
        return [(0, 0), (1, 1), (2, 2)]
    elif board[0][2] == board[1][1] == board[2][0] != ' ':
        return [(0, 2), (1, 1), (2, 0)]
    else:
        return None

def update_OX():
    global game_over
    if not game_over:
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            row = pyxel.mouse_y // (256 // 3)
            col = pyxel.mouse_x // (256 // 3)
            play(row, col)
    else:
        if pyxel.btnp(pyxel.KEY_R):
            reset()

def draw_OX():
    for i in range(1, 3):
        pyxel.line(0, i * (256 // 3), 256, i * (256 // 3), 7)
        pyxel.line(i * (256 // 3), 0, i * (256 // 3), 256, 7)
    for row in range(3):
        for col in range(3):
            if board[row][col] == 'X':
                pyxel.rect(col * (256 // 3) + 16, row * (256 // 3) + 16, 256 // 3 - 32, 256 // 3 - 32, 8)
            elif board[row][col] == 'O':
                pyxel.circ(col * (256 // 3) + 256 // 6, row * (256 // 3) + 256 // 6, 256 // 6 - 8, 9)
    if winner:
        if winning_coords:
            start_x = winning_coords[0][1] * (256 // 3) + 256 // 6
            start_y = winning_coords[0][0] * (256 // 3) + 256 // 6
            end_x = winning_coords[-1][1] * (256 // 3) + 256 // 6
            end_y = winning_coords[-1][0] * (256 // 3) + 256 // 6
            pyxel.line(start_x, start_y, end_x, end_y, 12)
        pyxel.text(310, 48, f"{winner} WON!", 7)
        pyxel.text(282, 58, "Press R to restart", 7)
    elif game_over:
        pyxel.text(300, 48, "TIE GAME!", 7)
        pyxel.text(282, 58, "Press R to restart", 7)
    pyxel.text(282, 200, f"Player X wins: {player_X_wins}", 7)
    pyxel.text(282, 220, f"Player O wins: {player_O_wins}", 7)

def start_game_draw():
    global selected_option, credit, game, frame_click, about, pieces, r1, OX, player_X_wins, player_O_wins, apple_x, apple_y, snake_game, breakout, ability, mecanique

    star_x = (pyxel.frame_count * 3) % (pyxel.width)
    star_y = (pyxel.frame_count * 3) % (pyxel.height)

    if credit:

        pyxel.cls(0)
        hearts = [(1, 1), (1, 1), (2, 1), (5, 1), (1, 5), (1, 5), (5, 5), (1, 2), (1, 1), (2, -1),
                  (-1, -5), (-1, -8), (-5, 1), (-1, 5)]
        for heart in hearts:
            x = (pyxel.frame_count * heart[0]) % pyxel.width
            y = (pyxel.frame_count * heart[1]) % pyxel.height
            pyxel.blt(x, y, 0, 216, 80, 16, 16, 0)

        if show_apple and not snake_game:
            pyxel.blt(apple_x, apple_y, 0, 80, 64, 16, 16, 0)
        pyxel.rect(172, 28, 34, 6, 0)
        pyxel.rectb(172, 28, 34, 10, 7)
        pyxel.text(175, 30, "CREDITS", 7)

        pyxel.text(100, 70, "Assim - le meilleur developeur (note : il a prit la decision de tout\nfaire tout seul et a eu un burnout son ego l'a sans doute rattrapee)", 7)
        pyxel.text(100, 100, "Raees - le developeur un peu moins bon \n(surnomme l'usine a gaz que des variables globales pas de return)", 7)
        pyxel.text(100, 120, "Sania - elle dessine bien ", 7)
        pyxel.text(100, 140, "Krish - maitrise la langue de Shakespear,\nmoins celle de Moliere", 7)
        pyxel.text(100, 160, "Josh - il etait en retard", 7)
        pyxel.text(100, 180, "Note : Il est important de savoir que ce projet\na ete realise en l'espace de 3semaines\navec au millieu bac blanc, examen, ect...\nPS : Josh etait une des difficultes rencontre pendant\nce projet mais utile quand il le fallait.", 7)
        pyxel.text(100, 200, "\n\nAttend la pomme !!!", 7)

        
        
        

        text_len = len("Menu") * pyxel.FONT_WIDTH
        if pyxel.mouse_x >= pyxel.width - text_len and pyxel.mouse_x <= pyxel.width and pyxel.mouse_y >= pyxel.height - pyxel.FONT_HEIGHT and pyxel.mouse_y <= pyxel.height:
            # dessine rectangle qui clignote
            if pyxel.frame_count % 20 < 10:
                pyxel.rect(pyxel.width - text_len - 2, pyxel.height - pyxel.FONT_HEIGHT - 1, text_len + 4,
                           pyxel.FONT_HEIGHT + 2, 7)
            pyxel.text(pyxel.width - text_len, pyxel.height - pyxel.FONT_HEIGHT, "Menu", 0)
            if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
                credit = False
        else:
            pyxel.text(pyxel.width - text_len, pyxel.height - pyxel.FONT_HEIGHT, "Menu", 7)

    elif about:
        pyxel.cls(5)
        if not pieces and not r1 and not ability and not mecanique:
            pyxel.text(175, 30, "A PROPOS", pyxel.frame_count % 16)
            text1_len = len("Pieces") * pyxel.FONT_WIDTH
            if pyxel.mouse_x >= 199 - text1_len and pyxel.mouse_x <= 199 and pyxel.mouse_y >= 90 - pyxel.FONT_HEIGHT and pyxel.mouse_y <= 90 and not pieces:
                # dessine rectangle qui clignote
                if pyxel.frame_count % 20 < 10 and not pieces and not r1 and not ability and not mecanique:
                    pyxel.rect(199 - text1_len - 2, 90 - pyxel.FONT_HEIGHT - 1, text1_len + 4, pyxel.FONT_HEIGHT + 2, 7)
                pyxel.text(199 - text1_len, 90 - pyxel.FONT_HEIGHT, "Pieces", 0)
                if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
                    pieces = True
            elif not pieces and not r1 and not ability and not mecanique:
                pyxel.text(199 - text1_len, 90 - pyxel.FONT_HEIGHT, "Pieces", 7)

            text_len = len("Menu") * pyxel.FONT_WIDTH
            if not pieces and not r1 and not ability:
                pyxel.text(pyxel.width - text_len, pyxel.height - pyxel.FONT_HEIGHT, "Menu", 7)
            if not pieces and not r1 and not ability and not mecanique and pyxel.mouse_x >= pyxel.width - text_len and pyxel.mouse_x <= pyxel.width and pyxel.mouse_y >= pyxel.height - pyxel.FONT_HEIGHT and pyxel.mouse_y <= pyxel.height:
                # dessine rectangle qui clignote
                if pyxel.frame_count % 20 < 10:
                    pyxel.rect(pyxel.width - text_len - 2, pyxel.height - pyxel.FONT_HEIGHT - 1, text_len + 4, pyxel.FONT_HEIGHT + 2, 7)
                    pyxel.text(pyxel.width - text_len, pyxel.height - pyxel.FONT_HEIGHT, "Menu", 0)
                if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
                    about = False

            text2_len = len("Regles") * pyxel.FONT_WIDTH
            if pyxel.mouse_x >= 199 - text2_len and pyxel.mouse_x <= 199 and pyxel.mouse_y >= 70 - pyxel.FONT_HEIGHT and pyxel.mouse_y <= 70 and not r1:
                # dessine rectangle qui clignote
                if pyxel.frame_count % 20 < 10 and not r1:
                    pyxel.rect(199 - text2_len - 2, 70 - pyxel.FONT_HEIGHT - 1, text2_len + 4, pyxel.FONT_HEIGHT + 2, 7)
                pyxel.text(199 - text2_len, 70 - pyxel.FONT_HEIGHT, "Regles", 0)
                if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
                    r1 = True
            elif not r1 and not pieces and not ability and not mecanique:
                pyxel.text(199 - text2_len, 70 - pyxel.FONT_HEIGHT, "Regles", 7)

            text3_len = len("Abilites") * pyxel.FONT_WIDTH
            if pyxel.mouse_x >= 209 - text3_len and pyxel.mouse_x <= 209 and pyxel.mouse_y >= 110 - pyxel.FONT_HEIGHT and pyxel.mouse_y <= 110 and not ability:
                # dessine rectangle qui clignote
                if pyxel.frame_count % 20 < 10 and not ability and not mecanique:
                    pyxel.rect(209 - text3_len - 2, 110 - pyxel.FONT_HEIGHT - 1, text3_len + 4, pyxel.FONT_HEIGHT + 2, 7)
                pyxel.text(209 - text3_len, 110 - pyxel.FONT_HEIGHT, "Abilites", 0)
                if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
                    ability = True
            elif not r1 and not pieces and not ability and not mecanique:
                pyxel.text(209 - text3_len - 2, 110 - pyxel.FONT_HEIGHT, "Abilites", 7)

            text4_len = len("Mecaniques") * pyxel.FONT_WIDTH
            if pyxel.mouse_x >= 217 - text4_len and pyxel.mouse_x <= 217 and pyxel.mouse_y >= 130 - pyxel.FONT_HEIGHT and pyxel.mouse_y <= 130 and not mecanique:
                # dessine rectangle qui clignote
                if pyxel.frame_count % 20 < 10 and not mecanique:
                    pyxel.rect(217 - text4_len - 2, 130 - pyxel.FONT_HEIGHT - 1, text4_len + 4, pyxel.FONT_HEIGHT + 2, 7)
                pyxel.text(217 - text4_len, 130 - pyxel.FONT_HEIGHT, "Mecaniques", 0)
                if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
                    mecanique = True
            elif not r1 and not pieces and not ability and not mecanique:
                pyxel.text(217 - text4_len - 2, 130 - pyxel.FONT_HEIGHT, "Mecaniques", 7)

        elif r1:
            pyxel.cls(0)
            if not breakout:
                pyxel.blt(star_x, star_y, 0, 96, 16 * ((pyxel.frame_count // 2) % 4), 16, 16, 0)
                pyxel.text(175, 30, "Regles", 7)

                pyxel.text(25, 80, "Chaque joueur possede 16 pieces.", 7)
                pyxel.text(25, 90, "Dont 8 citoyens, 2 ouvriers , 2 soldats , 2 pirates , 1 ministre , 1 president.", 7)
                pyxel.text(25, 100, "Il faut etre le seul à avoir son president en vie", 7)
                pyxel.text(25, 110, "N'oubliez pas de jouer dans le temps impartie choisie", 7)
            
                pyxel.bltm(0, 0, 0, 0, 96*8, 384, 256,0)

            if pyxel.mouse_x >= star_x and pyxel.mouse_x <= star_x + 16 and pyxel.mouse_y >= star_y and pyxel.mouse_y <= star_y + 16 and pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
                breakout = True

            elif breakout:
            
                draw_breakout()

                text_len = len("Pieces") * pyxel.FONT_WIDTH
                if pyxel.mouse_x >= pyxel.width - text_len and pyxel.mouse_x <= pyxel.width and pyxel.mouse_y >= pyxel.height - pyxel.FONT_HEIGHT and pyxel.mouse_y <= pyxel.height:
                    # dessine rectangle qui clignote
                    if pyxel.frame_count % 20 < 10:
                        pyxel.rect(pyxel.width - text_len - 2, pyxel.height - pyxel.FONT_HEIGHT - 1, text_len + 4, pyxel.FONT_HEIGHT + 2, 7)
                    pyxel.text(pyxel.width - text_len, pyxel.height - pyxel.FONT_HEIGHT, "Retour", 0)
                    if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
                        breakout = False
                else:
                    pyxel.text(pyxel.width - text_len, pyxel.height - pyxel.FONT_HEIGHT, "Retour", 7)

            text_len = len("Pieces") * pyxel.FONT_WIDTH
            if pyxel.mouse_x >= pyxel.width - text_len and pyxel.mouse_x <= pyxel.width and pyxel.mouse_y >= pyxel.height - pyxel.FONT_HEIGHT and pyxel.mouse_y <= pyxel.height:
                # dessine rectangle qui clignote
                if pyxel.frame_count % 20 < 10:
                    pyxel.rect(pyxel.width - text_len - 2, pyxel.height - pyxel.FONT_HEIGHT - 1, text_len + 4, pyxel.FONT_HEIGHT + 2, 7)
                pyxel.text(pyxel.width - text_len, pyxel.height - pyxel.FONT_HEIGHT, "Retour", 0)
                if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
                    r1 = False
            else:
                pyxel.text(pyxel.width - text_len, pyxel.height - pyxel.FONT_HEIGHT, "Retour", 7)


        elif pieces:
            pyxel.text(175, 30, "Pieces", 7)
            image_index = (pyxel.frame_count // 20) % 4
            # desciption de chaque piece
            if pyxel.mouse_x >= 130 and pyxel.mouse_x <= 146 and pyxel.mouse_y >= 60 and pyxel.mouse_y <= 76:
                pyxel.blt(130, 60, 0, 0, 16 * image_index, 16, 16)
                pyxel.text(20, 110, "Le president se déplace comme le roi.", 7)
                pyxel.text(20, 120, "Il peut echanger de position avec un soldat dans un rayon de 2 cases autour de lui.", 7)
                pyxel.text(20, 130, "Il peut lancer une bombe et tuer une piece de son choix sauf les presidents adverses.", 7)
            elif pyxel.mouse_x >= 150 and pyxel.mouse_x <= 166 and pyxel.mouse_y >= 60 and pyxel.mouse_y <= 76:
                pyxel.blt(150, 60, 0, 48, 16 * image_index, 16, 16)
                pyxel.text(12, 110, "Le ministre se deplace comme la reine.", 7)
                pyxel.text(12, 120, "Il peut choisir entre 4 capacites avant le debut de la partie :", 7)
                pyxel.text(12, 130, "- Le feu ", 7)
                pyxel.text(12, 140, "- La prison ", 7)
                pyxel.text(12, 150, "- Le soin ", 7)
                pyxel.text(12, 160, "- Le bouclier ",7)
                pyxel.text(12, 190, "Si un ministre tue un ministre avec sa capacite, va être amélioree.", 7)
            elif pyxel.mouse_x >= 170 and pyxel.mouse_x <= 186 and pyxel.mouse_y >= 60 and pyxel.mouse_y <= 76:
                pyxel.blt(170, 60, 0, 16, 16 * image_index, 16, 16)
                pyxel.text(60, 110, "Le pirate se deplace comme le fou.", 7)
                pyxel.text(60, 120, "Il peut controler une piece de son equipe et lui donner un deplacement special.", 7)
                pyxel.text(60, 130, "Il se transforme en ministre lorsqu'il tue un ministre.", 7)
                pyxel.text(60, 140, "Lorsqu'il meurt, il laisse une tombe bloquant la case.", 7)
            elif pyxel.mouse_x >= 190 and pyxel.mouse_x <= 206 and pyxel.mouse_y >= 60 and pyxel.mouse_y <= 76:
                pyxel.blt(190, 60, 0, 32, 16 * image_index, 16, 16)
                pyxel.text(80, 110, "Le soldat se deplace comme une tour.", 7)
                pyxel.text(80, 120, "Il peut poser des mines et se transformer en hacker si il tue un ministre.", 7)
                pyxel.text(80, 130, "Lorsqu'il meurt, il laisse une tombe bloquant la case.", 7)
            elif pyxel.mouse_x >= 210 and pyxel.mouse_x <= 226 and pyxel.mouse_y >= 60 and pyxel.mouse_y <= 76:
                pyxel.blt(210, 60, 0, 80, 16 * image_index, 16, 16)
                pyxel.text(100, 110, "L'ouvrier se déplace comme le cavalier.", 7)
                pyxel.text(100, 120, "Il peut bloquer une case pendant 5 tour.", 7)
                pyxel.text(100, 130, "Il se transforme en soldat.", 7)
            elif pyxel.mouse_x >= 230 and pyxel.mouse_x <= 246 and pyxel.mouse_y >= 60 and pyxel.mouse_y <= 76:
                pyxel.blt(230, 60, 0, 64, 16 * image_index, 16, 16)
                pyxel.text(100, 110, "Le citoyen se deplace comme un pion et attaque comme ce dernier. \nIl n'a pas de capacite particuliere.", 7)
                pyxel.text(100, 120, "\nIl se transforme en ouvrier si il tue un minstre ou atteint la zone \ndu plateau oppose a lui.", 7)

            else:
                # dessine les images des pieces
                pyxel.blt(130, 60, 0, 0, 16 * image_index, 16, 16, 4)
                pyxel.blt(150, 60, 0, 48, 16 * image_index, 16, 16, 4)
                pyxel.blt(170, 60, 0, 16, 16 * image_index, 16, 16, 4)
                pyxel.blt(190, 60, 0, 32, 16 * image_index, 16, 16, 4)
                pyxel.blt(210, 60, 0, 80, 16 * image_index, 16, 16, 4)
                pyxel.blt(230, 60, 0, 64, 16 * image_index, 16, 16, 4)

            text_len = len("Pieces") * pyxel.FONT_WIDTH
            if pyxel.mouse_x >= pyxel.width - text_len and pyxel.mouse_x <= pyxel.width and pyxel.mouse_y >= pyxel.height - pyxel.FONT_HEIGHT and pyxel.mouse_y <= pyxel.height:
                # dessine rectangle qui clignote
                if pyxel.frame_count % 20 < 10:
                    pyxel.rect(pyxel.width - text_len - 2, pyxel.height - pyxel.FONT_HEIGHT - 1, text_len + 4, pyxel.FONT_HEIGHT + 2, 7)
                pyxel.text(pyxel.width - text_len, pyxel.height - pyxel.FONT_HEIGHT, "Retour", 0)
                if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
                    pieces = False
            else:
                pyxel.text(pyxel.width - text_len, pyxel.height - pyxel.FONT_HEIGHT, "Retour", 7)

        elif ability:
            pyxel.text(175, 30, "Abilites", 7)

            image_index = (pyxel.frame_count // 20) % 4
            # desciption des abilites
            if pyxel.mouse_x >= 110 and pyxel.mouse_x < 126 and pyxel.mouse_y >= 60 and pyxel.mouse_y < 76:
                pyxel.blt(110, 60, 0, 112, 16 * image_index, 16, 16, 0)
                pyxel.text(110, 80, "peut mettre le feu a une case pendant 15 tours", 7)
            elif pyxel.mouse_x >= 130 and pyxel.mouse_x < 146 and pyxel.mouse_y >= 60 and pyxel.mouse_y < 76:
                pyxel.blt(130, 60, 0, 128, 16 * image_index, 16, 16, 0)
                pyxel.text(130, 80, "peut reanimer un soldat ou pirate", 7)
            elif pyxel.mouse_x >= 150 and pyxel.mouse_x < 166 and pyxel.mouse_y >= 60 and pyxel.mouse_y < 76:
                pyxel.blt(150, 60, 0, 160, 16 * image_index, 16, 16, 4)
                pyxel.text(150, 80, "peut poser des mines", 7)
            elif pyxel.mouse_x >= 170 and pyxel.mouse_x < 186 and pyxel.mouse_y >= 60 and pyxel.mouse_y < 76:
                pyxel.blt(170, 60, 0, 176, 16 * image_index, 16, 16, 0)
                pyxel.text(170, 80, "peut bloquer une case pendant 5 tour", 7)
            elif pyxel.mouse_x >= 190 and pyxel.mouse_x < 206 and pyxel.mouse_y >= 60 and pyxel.mouse_y < 76:
                pyxel.blt(190, 60, 0, 144 + (image_index * 16), 64, 16, 16, 0)
                pyxel.text(170, 80, "peut mettre un bouclier sur une piece,", 7)
                pyxel.text(170, 90, "le bouclier disparait quand la piece bouge une fois \nou apres 5 tours", 7)
            elif pyxel.mouse_x >= 210 and pyxel.mouse_x < 226 and pyxel.mouse_y >= 60 and pyxel.mouse_y < 76:
                pyxel.blt(210, 60, 0, 144 + (image_index * 16), 80, 16, 16, 0)
                pyxel.text(210, 80, "bloque une piece pendant 10 tours,", 7)
                pyxel.text(210, 90, "si la piece bouge elle meurt", 7)
            elif pyxel.mouse_x >= 230 and pyxel.mouse_x < 246 and pyxel.mouse_y >= 60 and pyxel.mouse_y < 76:
                pyxel.blt(230, 60, 0, 144 + (image_index * 16), 96, 16, 16, 0)
                pyxel.text(230, 80, "peut controler une piece de son equipe", 7)
                pyxel.text(230, 90, "et lui donner un deplacement special", 7)
            elif pyxel.mouse_x >= 250 and pyxel.mouse_x < 266 and pyxel.mouse_y >= 60 and pyxel.mouse_y < 76:
                pyxel.blt(250, 60, 0, 144 + (image_index * 16), 112, 16, 16, 4)
                pyxel.text(220, 80, "peut echanger de position avec un soldat", 7)
                pyxel.text(220, 90, "dans un rayon de 2 cases autour de lui", 7)
            elif pyxel.mouse_x >= 270 and pyxel.mouse_x < 286 and pyxel.mouse_y >= 60 and pyxel.mouse_y < 76:
                pyxel.blt(270, 60, 0, 192, 16 * image_index, 16, 16, 4)
                pyxel.text(250, 80, "peut lancer une bombe", 7)
                pyxel.text(250, 90, "et tue une piece de son choix ", 7)
                pyxel.text(250, 100, "sauf les presidents adverses", 7)

            else:
                # dessine les images des abilites
                pyxel.blt(110, 60, 0, 112, 16 * image_index, 16, 16, 0)
                pyxel.blt(130, 60, 0, 128, 16 * image_index, 16, 16, 0)
                pyxel.blt(150, 60, 0, 160, 16 * image_index, 16, 16, 4)
                pyxel.blt(170, 60, 0, 176, 16 * image_index, 16, 16, 0)
                pyxel.blt(190, 60, 0, 144 + (image_index * 16), 64, 16, 16, 0)
                pyxel.blt(210, 60, 0, 144 + (image_index * 16), 80, 16, 16, 0)
                pyxel.blt(230, 60, 0, 144 + (image_index * 16), 96, 16, 16, 0)
                pyxel.blt(250, 60, 0, 144 + (image_index * 16), 112, 16, 16, 4)
                pyxel.blt(270, 60, 0, 192, 16 * image_index, 16, 16, 4)



            text_len = len("Pieces") * pyxel.FONT_WIDTH
            if pyxel.mouse_x >= pyxel.width - text_len and pyxel.mouse_x <= pyxel.width and pyxel.mouse_y >= pyxel.height - pyxel.FONT_HEIGHT and pyxel.mouse_y <= pyxel.height:
                # dessine rectangle qui clignote
                if pyxel.frame_count % 20 < 10:
                    pyxel.rect(pyxel.width - text_len - 2, pyxel.height - pyxel.FONT_HEIGHT - 1, text_len + 4, pyxel.FONT_HEIGHT + 2, 7)
                pyxel.text(pyxel.width - text_len, pyxel.height - pyxel.FONT_HEIGHT, "Retour", 0)
                if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
                    ability = False
            else:
                pyxel.text(pyxel.width - text_len, pyxel.height - pyxel.FONT_HEIGHT, "Retour", 7)

        elif mecanique:
            pyxel.text(175, 30, "Mecaniques", 7)

            pyxel.text(30, 150, "Les amelioration : Les pieces peuvent debloquer leurs ameliorations en tuant un ministre.", 7)
            pyxel.text(30, 160, "Les capacites : L’utilisation d’une capacite consomme le tour du joueur.", 7)

            pyxel.text(30, 130, "Le citoyen se transforme en Ouvrier lorsqu'il touche un des bords du plateau", 7)

            image_index = (pyxel.frame_count // 20) % 4

            if pyxel.mouse_x >= 110 and pyxel.mouse_x < 126 and pyxel.mouse_y >= 60 and pyxel.mouse_y < 76:
                pyxel.blt(110, 60, 0, 144, 16 * image_index, 16, 16, 4)
                pyxel.text(110, 80, "Un citoyen a la possibilite de manger un cadavre", 7)
                pyxel.text(130, 90, "si c'est le cas, il devient un zombie", 7)
            elif pyxel.mouse_x >= 130 and pyxel.mouse_x < 166 and pyxel.mouse_y >= 60 and pyxel.mouse_y < 76:
                pyxel.blt(130, 60, 0, 208, 16 * image_index, 16, 16, 4)
                pyxel.blt(150, 60, 0, 224, 16 * image_index, 16, 16, 4)
                pyxel.text(130, 80, "Les tombes apparaissent quand un soldat ou un hacker meurt", 7)

            else :
                pyxel.blt(110, 60, 0, 144, 16 * image_index, 16, 16, 4)
                pyxel.blt(130, 60, 0, 208, 16 * image_index, 16, 16, 0)
                pyxel.blt(150, 60, 0, 224, 16 * image_index, 16, 16, 4)





            text_len = len("Pieces") * pyxel.FONT_WIDTH
            if pyxel.mouse_x >= pyxel.width - text_len and pyxel.mouse_x <= pyxel.width and pyxel.mouse_y >= pyxel.height - pyxel.FONT_HEIGHT and pyxel.mouse_y <= pyxel.height:
                # dessine rectangle qui clignote
                if pyxel.frame_count % 20 < 10:
                    pyxel.rect(pyxel.width - text_len - 2, pyxel.height - pyxel.FONT_HEIGHT - 1, text_len + 4,
                               pyxel.FONT_HEIGHT + 2, 7)
                pyxel.text(pyxel.width - text_len, pyxel.height - pyxel.FONT_HEIGHT, "Retour", 0)
                if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
                    mecanique = False
            else:
                pyxel.text(pyxel.width - text_len, pyxel.height - pyxel.FONT_HEIGHT, "Retour", 7)


    elif OX:

        text_len = len("Menu") * pyxel.FONT_WIDTH
        pyxel.text(pyxel.width - text_len, pyxel.height - pyxel.FONT_HEIGHT, "Menu", 7)
        if pyxel.mouse_x >= pyxel.width - text_len and pyxel.mouse_x <= pyxel.width and pyxel.mouse_y >= pyxel.height - pyxel.FONT_HEIGHT and pyxel.mouse_y <= pyxel.height:
            # dessine rectangle qui clignote
            if pyxel.frame_count % 20 < 10:
                pyxel.rect(pyxel.width - text_len - 2, pyxel.height - pyxel.FONT_HEIGHT - 1, text_len + 4, pyxel.FONT_HEIGHT + 2, 7)
                pyxel.text(pyxel.width - text_len, pyxel.height - pyxel.FONT_HEIGHT, "Menu", 0)
            if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
                OX = False
                reset()
                player_X_wins = 0
                player_O_wins = 0


    else:
        pyxel.rect(150, 65, 84, 120, 0)
        pyxel.text(pyxel.width // 3 + 34, pyxel.height // 3, ">>> SOCIETY <<< ", pyxel.frame_count % 16)

        for i, option in enumerate(menu):
            text_len = len(option) * pyxel.FONT_WIDTH
            if i == selected_option:
                # dessine rectangle qui clignote
                if pyxel.frame_count % 20 < 10:
                    pyxel.rect((pyxel.width - text_len) // 2 - 2, pyxel.height // 2 + i * 8 - 1, text_len + 4,pyxel.FONT_HEIGHT + 2, 7)
                pyxel.text((pyxel.width - text_len) // 2, pyxel.height // 2 + i * 8, option, 0)
            else:
                pyxel.text((pyxel.width - text_len) // 2, pyxel.height // 2 + i * 8, option, 7)

            if pyxel.mouse_x >= (pyxel.width - text_len) // 2 and pyxel.mouse_x <= (pyxel.width - text_len) // 2 + text_len and pyxel.mouse_y >= pyxel.height // 2 + i * 8 and pyxel.mouse_y <= pyxel.height // 2 + i * 8 + pyxel.FONT_HEIGHT:
                selected_option = i
                if pyxel.btnr(pyxel.KEY_SPACE) or pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT) and frame_click != pyxel.frame_count:
                    frame_click = pyxel.frame_count
                    if selected_option == 0:
                        game = True
                    elif selected_option == 1:
                        credit = True
                    elif selected_option == 2:
                        about = True
                    elif selected_option == 3:
                        pyxel.quit()

def start_game_update(selected_option, game, credit, frame_click):
    pass

#########################


choix = True
winner_1 = None
game_start = True
jouer = False
choix_1 = False
choix_2 = False
choix_3 = False
choix_4 = False
couleur = 8 


jou = ['rose', 'bleu', 'jaune', 'vert']
turn = random.randint(0 , 3)
frame_piece = pyxel.frame_count
frame_abilite = pyxel.frame_count
temps = None
frame_tour = pyxel.frame_count
frame_choix = pyxel.frame_count

turn_1 = jou[turn]
end = False

tour = 0
tour_1 = tour

pyxel.mouse(True)



position_jouable = [(x , y) for x in range(0, 256, 16) for y in range(64, 192, 16)] + \
                [(x , y) for x in range(64, 192, 16) for y in range(192, 256, 16)] + \
                [(x , y) for x in range(64, 192, 16) for y in range(0, 64, 16)]



position_a_jouer = []
position_valide = {position : True for position in position_jouable}

equipe_bleu =   [{'tag': 'piece', 'type' : 'citoyen', 'zombie' : False,'equipe' : 'bleu', 'en_vie' : True, 'en_mouvement' : False, 'x' : x , 'y' : 224 , '1er_tour' : True, 'barriere' : False, 'controle' : False, 'en_prison' : False } for x in range(64, 177, 16)]  +\
                [{'tag': 'piece', 'type' : 'ouvrier','equipe' : 'rose', 'en_vie' : True, 'en_mouvement' : False, 'x' : 160, 'y' : 240 , '1er_tour' : True, 'barriere' : False, 'controle' : False, 'en_prison' : False },\
                 {'tag': 'piece', 'type' : 'ouvrier','equipe' : 'rose', 'en_vie' : True, 'en_mouvement' : False, 'x' : 80, 'y' : 240 , '1er_tour' : True, 'barriere' : False, 'controle' : False, 'en_prison' : False }] +\
                [{'tag': 'piece', 'type' : 'soldat','equipe' : 'rose', 'en_vie' : True, 'en_mouvement' : False, 'x' : 176, 'y' : 240 , '1er_tour' : True, 'barriere' : False, 'controle' : False, 'en_prison' : False },\
                 {'tag': 'piece', 'type' : 'soldat','equipe' : 'rose', 'en_vie' : True, 'en_mouvement' : False, 'x' : 64, 'y' : 240 , '1er_tour' : True, 'barriere' : False, 'controle' : False, 'en_prison' : False }] + \
                [{'tag': 'piece', 'type' : 'president', 'equipe' : 'bleu', 'en_vie' : True, 'en_mouvement' : False, 'x' : 112, 'y' : 240 , '1er_tour' : True, 'barriere' : False, 'controle' : False, 'en_prison' : False }]+\
                [{'tag': 'piece', 'type' : 'ministre', 'equipe' : 'bleu', 'en_vie' : True, 'en_mouvement' : False, 'x' : 128, 'y' : 240 , '1er_tour' : True, 'barriere' : False, 'controle' : False, 'en_prison' : False }] +\
                [{'tag': 'piece', 'type' : 'pirate', 'equipe' : 'bleu', 'en_vie' : True, 'en_mouvement' : False, 'x' : 144, 'y' : 240 , '1er_tour' : True, 'barriere' : False, 'controle' : False, 'en_prison' : False }] +\
                [{'tag': 'piece', 'type' : 'pirate', 'equipe' : 'bleu', 'en_vie' : True, 'en_mouvement' : False, 'x' : 96, 'y' : 240 , '1er_tour' : True, 'barriere' : False, 'controle' : False, 'en_prison' : False }]

equipe_jaune =  [{'tag': 'piece', 'type' : 'citoyen', 'zombie' : False,'equipe' : 'jaune', 'en_vie' : True, 'en_mouvement' : False, 'x' : 16 , 'y' : y , '1er_tour' : True, 'barriere' : False, 'controle' : False, 'en_prison' : False } for y in range(64, 177, 16)] + \
                [{'tag': 'piece', 'type' : 'ouvrier','equipe' : 'rose', 'en_vie' : True, 'en_mouvement' : False, 'x' : 0, 'y' : 80 , '1er_tour' : True, 'barriere' : False, 'controle' : False, 'en_prison' : False }, \
                {'tag': 'piece', 'type' : 'ouvrier','equipe' : 'rose', 'en_vie' : True, 'en_mouvement' : False, 'x' : 0, 'y' : 160 , '1er_tour' : True, 'barriere' : False, 'controle' : False, 'en_prison' : False }] + \
                [{'tag': 'piece', 'type' : 'soldat','equipe' : 'rose', 'en_vie' : True, 'en_mouvement' : False, 'x' : 0, 'y' : 176 , '1er_tour' : True, 'barriere' : False, 'controle' : False, 'en_prison' : False }, \
                 {'tag': 'piece', 'type' : 'soldat', 'equipe' : 'rose', 'en_vie' : True, 'en_mouvement' : False, 'x' : 0, 'y' : 64 , '1er_tour' : True, 'barriere' : False, 'controle' : False, 'en_prison' : False }] + \
                [{'tag': 'piece', 'type' : 'president', 'equipe' : 'jaune', 'en_vie' : True, 'en_mouvement' : False, 'x' : 0, 'y' : 128 , '1er_tour' : True, 'barriere' : False, 'controle' : False, 'en_prison' : False }] +\
                [{'tag': 'piece', 'type' : 'ministre', 'equipe' : 'jaune', 'en_vie' : True, 'en_mouvement' : False, 'x' : 0, 'y' : 112 , '1er_tour' : True, 'barriere' : False, 'controle' : False, 'en_prison' : False }]+\
                [{'tag': 'piece', 'type' : 'pirate', 'equipe' : 'jaune', 'en_vie' : True, 'en_mouvement' : False, 'x' : 0, 'y' : 144 , '1er_tour' : True, 'barriere' : False, 'controle' : False, 'en_prison' : False }] +\
                [{'tag': 'piece', 'type' : 'pirate', 'equipe' : 'jaune', 'en_vie' : True, 'en_mouvement' : False, 'x' : 0, 'y' : 96 , '1er_tour' : True, 'barriere' : False, 'controle' : False, 'en_prison' : False }]

equipe_vert =   [{'tag': 'piece', 'type' : 'citoyen', 'zombie' : False,'equipe' : 'vert', 'en_vie' : True,'en_mouvement' : False, 'x' : x , 'y' : 16 , '1er_tour' : True, 'barriere' : False, 'controle' : False, 'en_prison' : False } for x in range(64, 177, 16)] + \
                [{'tag': 'piece', 'type' : 'ouvrier','equipe' : 'rose', 'en_vie' : True,'en_mouvement' : False, 'x' : 80, 'y' : 0 , '1er_tour' : True, 'barriere' : False, 'controle' : False, 'en_prison' : False },\
                {'tag': 'piece', 'type' : 'ouvrier','equipe' : 'rose', 'en_vie' : True, 'en_mouvement' : False, 'x' : 160, 'y' : 0 , '1er_tour' : True, 'barriere' : False, 'controle' : False, 'en_prison' : False }] +\
                [{'tag': 'piece', 'type' : 'soldat', 'equipe' : 'rose', 'en_vie' : True, 'en_mouvement' : False, 'x' : 64, 'y' : 0 , '1er_tour' : True, 'barriere' : False, 'controle' : False, 'en_prison' : False },\
                 {'tag': 'piece', 'type' : 'soldat', 'equipe' : 'rose', 'en_vie' : True, 'en_mouvement' : False, 'x' : 176, 'y' : 0 , '1er_tour' : True, 'barriere' : False, 'controle' : False, 'en_prison' : False }] + \
                [{'tag': 'piece', 'type' : 'president', 'equipe' : 'vert', 'en_vie' : True, 'en_mouvement' : False, 'x' : 128, 'y' : 0 , '1er_tour' : True, 'barriere' : False, 'controle' : False, 'en_prison' : False }] +\
                [{'tag': 'piece', 'type' : 'ministre', 'equipe' : 'vert', 'en_vie' : True, 'en_mouvement' : False, 'x' : 112, 'y' : 0 , '1er_tour' : True, 'barriere' : False, 'controle' : False, 'en_prison' : False }]+\
                [{'tag': 'piece', 'type' : 'pirate', 'equipe' : 'vert', 'en_vie' : True, 'en_mouvement' : False, 'x' : 144, 'y' : 0 , '1er_tour' : True, 'barriere' : False, 'controle' : False, 'en_prison' : False }] +\
                [{'tag': 'piece', 'type' : 'pirate', 'equipe' : 'vert', 'en_vie' : True, 'en_mouvement' : False, 'x' : 96, 'y' : 0 , '1er_tour' : True, 'barriere' : False, 'controle' : False, 'en_prison' : False }]

equipe_rose =   [{'tag': 'piece', 'type' : 'citoyen', 'zombie' : False,'equipe' : 'rose', 'en_vie' : True,'en_mouvement' : False, 'x' : 224, 'y' : y , '1er_tour' : True, 'barriere' : False, 'controle' : False, 'en_prison' : False } for y in range(64, 177, 16)] + \
                [{'tag': 'piece', 'type' : 'ouvrier','equipe' : 'rose', 'en_vie' : True, 'en_mouvement' : False, 'x' : 240, 'y' : 80 , '1er_tour' : True, 'barriere' : False, 'controle' : False, 'en_prison' : False },\
                 {'tag': 'piece', 'type' : 'ouvrier','equipe' : 'rose', 'en_vie' : True,'en_mouvement' : False, 'x' : 240, 'y' : 160 , '1er_tour' : True, 'barriere' : False, 'controle' : False, 'en_prison' : False }] + \
                [{'tag': 'piece', 'type' : 'soldat', 'equipe' : 'rose', 'en_vie' : True, 'en_mouvement' : False, 'x' : 240, 'y' : 176 , '1er_tour' : True, 'barriere' : False, 'controle' : False, 'en_prison' : False },\
                 {'tag': 'piece', 'type' : 'soldat','equipe' : 'rose', 'en_vie' : True, 'en_mouvement' : False, 'x' : 240, 'y' : 64 , '1er_tour' : True, 'barriere' : False, 'controle' : False, 'en_prison' : False }] + \
                [{'tag': 'piece', 'type' : 'president', 'equipe' : 'rose', 'en_vie' : True, 'en_mouvement' : False, 'x' : 240, 'y' : 112 , '1er_tour' : True, 'barriere' : False, 'controle' : False, 'en_prison' : False }] +\
                [{'tag': 'piece', 'type' : 'ministre', 'equipe' : 'rose', 'en_vie' : True, 'en_mouvement' : False, 'x' : 240, 'y' : 128 , '1er_tour' : True, 'barriere' : False, 'controle' : False, 'en_prison' : False }] +\
                [{'tag': 'piece', 'type' : 'pirate', 'equipe' : 'rose', 'en_vie' : True, 'en_mouvement' : False, 'x' : 240, 'y' : 144 , '1er_tour' : True, 'barriere' : False, 'controle' : False, 'en_prison' : False }] +\
                [{'tag': 'piece', 'type' : 'pirate', 'equipe' : 'rose', 'en_vie' : True, 'en_mouvement' : False, 'x' : 240, 'y' : 96 , '1er_tour' : True, 'barriere' : False, 'controle' : False, 'en_prison' : False }]

abilite_rose =  [{'tag' : 'abilite', 'equipe' : 'rose', 'type' : 'mur', 'x' : 192, 'y': 192, 'selection' : False, 'recharge' : 0, 'activation' : True, 'boost' : 0}] +\
                [{'tag' : 'abilite', 'equipe' : 'rose', 'type' : 'mine', 'x' : 208, 'y': 192, 'selection' : False, 'recharge' : 0, 'activation' : True, 'boost' : 0}] +\
                [{'tag' : 'abilite', 'equipe' : 'rose', 'type' : 'piratage', 'x' : 224, 'y': 192, 'selection' : False, 'recharge' : 0, 'activation' : True, 'boost' : 0}]+\
                [{'tag' : 'abilite', 'equipe' : 'rose', 'type' : 'bombe', 'x' : 240, 'y': 192, 'selection' : False, 'recharge' : 0, 'activation' : False, 'boost' : 0}]+\
                [{'tag' : 'abilite', 'equipe' : 'rose', 'type' : 'feu', 'x' : 192, 'y': 224, 'selection' : False, 'recharge' : 0, 'activation' : False, 'boost' : 0}]+\
                [{'tag' : 'abilite', 'equipe' : 'rose', 'type' : 'barriere', 'x' : 208, 'y': 224, 'selection' : False, 'recharge' : 0, 'activation' : False, 'boost' : 0}]+\
                [{'tag' : 'abilite', 'equipe' : 'rose', 'type' : 'prison', 'x' : 224, 'y': 224, 'selection' : False, 'recharge' : 0, 'activation' : False, 'boost' : 0}]+\
                [{'tag' : 'abilite', 'equipe' : 'rose', 'type' : 'soin', 'x' : 240, 'y': 224, 'selection' : False, 'recharge' : 0, 'activation' : False, 'boost' : 0}]+\
                [{'tag' : 'abilite', 'equipe' : 'rose', 'type' : 'teleportation', 'x' : 192, 'y': 208, 'selection' : False, 'recharge' : 0, 'activation' : True, 'boost' : 0}]

abilite_bleu =  [{'tag' : 'abilite', 'equipe' : 'bleu', 'type' : 'mur', 'x' : 0, 'y': 192, 'selection' : False, 'recharge' : 0, 'activation' : True, 'boost' : 0}]+\
                [{'tag' : 'abilite', 'equipe' : 'bleu', 'type' : 'mine', 'x' : 16, 'y': 192, 'selection' : False, 'recharge' : 0, 'activation' : True, 'boost' : 0}]+\
                [{'tag' : 'abilite', 'equipe' : 'bleu', 'type' : 'piratage', 'x' : 32, 'y': 192, 'selection' : False, 'recharge' : 0, 'activation' : True, 'boost' : 0}]+\
                [{'tag' : 'abilite', 'equipe' : 'bleu', 'type' : 'bombe', 'x' : 48, 'y': 192, 'selection' : False, 'recharge' : 0, 'activation' : False, 'boost' : 0}]+\
                [{'tag' : 'abilite', 'equipe' : 'bleu', 'type' : 'feu', 'x' : 0, 'y': 224, 'selection' : False, 'recharge' : 0, 'activation' : False, 'boost' : 0}]+\
                [{'tag' : 'abilite', 'equipe' : 'bleu', 'type' : 'barriere', 'x' : 16, 'y': 224, 'selection' : False, 'recharge' : 0, 'activation' : False, 'boost' : 0}]+\
                [{'tag' : 'abilite', 'equipe' : 'bleu', 'type' : 'prison', 'x' : 32, 'y': 224, 'selection' : False, 'recharge' : 0, 'activation' : False, 'boost' : 0}]+\
                [{'tag' : 'abilite', 'equipe' : 'bleu', 'type' : 'soin', 'x' : 48, 'y': 224, 'selection' : False, 'recharge' : 0, 'activation' : False, 'boost' : 0}]+\
                [{'tag' : 'abilite', 'equipe' : 'bleu', 'type' : 'teleportation', 'x' : 0, 'y': 208, 'selection' : False, 'recharge' : 0, 'activation' : True, 'boost' : 0}]

abilite_jaune = [{'tag' : 'abilite', 'equipe' : 'jaune', 'type' : 'mur', 'x' : 0, 'y': 0, 'selection' : False, 'recharge' : 0, 'activation' : True, 'boost' : 0}]+\
                [{'tag' : 'abilite', 'equipe' : 'jaune', 'type' : 'mine', 'x' : 16, 'y': 0, 'selection' : False, 'recharge' : 0, 'activation' : True, 'boost' : 0}]+\
                [{'tag' : 'abilite', 'equipe' : 'jaune', 'type' : 'piratage', 'x' : 32, 'y': 0, 'selection' : False, 'recharge' : 0, 'activation' : True, 'boost' : 0}]+\
                [{'tag' : 'abilite', 'equipe' : 'jaune', 'type' : 'bombe', 'x' : 48, 'y': 0, 'selection' : False, 'recharge' : 0, 'activation' : False, 'boost' : 0}]+\
                [{'tag' : 'abilite', 'equipe' : 'jaune', 'type' : 'feu', 'x' : 0, 'y': 32, 'selection' : False, 'recharge' : 0, 'activation' : False, 'boost' : 0}]+\
                [{'tag' : 'abilite', 'equipe' : 'jaune', 'type' : 'barriere', 'x' : 16, 'y': 32, 'selection' : False, 'recharge' : 0, 'activation' : False, 'boost' : 0}]+\
                [{'tag' : 'abilite', 'equipe' : 'jaune', 'type' : 'prison', 'x' : 32, 'y': 32, 'selection' : False, 'recharge' : 0, 'activation' : False, 'boost' : 0}]+\
                [{'tag' : 'abilite', 'equipe' : 'jaune', 'type' : 'soin', 'x' : 48, 'y': 32, 'selection' : False, 'recharge' : 0, 'activation' : False, 'boost' : 0}]+\
                [{'tag' : 'abilite', 'equipe' : 'jaune', 'type' : 'teleportation', 'x' : 0, 'y': 16, 'selection' : False, 'recharge' : 0, 'activation' : True, 'boost' : 0}]

abilite_vert =  [{'tag' : 'abilite', 'equipe' : 'vert', 'type' : 'mur', 'x' : 192, 'y': 0, 'selection' : False, 'recharge' : 0, 'activation' : True, 'boost' : 0}]+\
                [{'tag' : 'abilite', 'equipe' : 'vert', 'type' : 'mine', 'x' : 208, 'y': 0, 'selection' : False, 'recharge' : 0, 'activation' : True, 'boost' : 0}]+\
                [{'tag' : 'abilite', 'equipe' : 'vert', 'type' : 'piratage', 'x' : 224, 'y': 0, 'selection' : False, 'recharge' : 0, 'activation' : True, 'boost' : 0}]+\
                [{'tag' : 'abilite', 'equipe' : 'vert', 'type' : 'bombe', 'x' : 240, 'y': 0, 'selection' : False, 'recharge' : 0, 'activation' : False, 'boost' : 0}]+\
                [{'tag' : 'abilite', 'equipe' : 'vert', 'type' : 'feu', 'x' : 192, 'y': 32, 'selection' : False, 'recharge' : 0, 'activation' : False, 'boost' : 0}]+\
                [{'tag' : 'abilite', 'equipe' : 'vert', 'type' : 'barriere', 'x' : 208, 'y': 32, 'selection' : False, 'recharge' : 0, 'activation' : False, 'boost' : 0}]+\
                [{'tag' : 'abilite', 'equipe' : 'vert', 'type' : 'prison', 'x' : 224, 'y': 32, 'selection' : False, 'recharge' : 0, 'activation' : False, 'boost' : 0}]+\
                [{'tag' : 'abilite', 'equipe' : 'vert', 'type' : 'soin', 'x' : 240, 'y': 32, 'selection' : False, 'recharge' : 0, 'activation' : False, 'boost' : 0}]+\
                [{'tag' : 'abilite', 'equipe' : 'vert', 'type' : 'teleportation', 'x' : 192, 'y': 16, 'selection' : False, 'recharge' : 0, 'activation' : True, 'boost' : 0}]

liste_mur = []

liste_feu = []

liste_prison = []

liste_mine = []

liste_barriere = []

liste_explosion = []

def board_update(board, equipe_1, equipe_2, equipe_3, equipe_4, liste_mur, liste_mine) :
    
    for key in board : 
        board[key] = True

    for piece_1 in equipe_1 : 
        board[(piece_1['x'], piece_1['y'])] = False

    for piece_2 in equipe_2 : 
        board[(piece_2['x'], piece_2['y'])] = False
    
    for piece_3 in equipe_3 : 
        board[(piece_3['x'], piece_3['y'])] = False

    for piece_4 in equipe_4 : 
        board[(piece_4['x'], piece_4['y'])] = False
    
    for mur in liste_mur : 
        board[(mur['x'], mur['y'])] = False
    
    for mine in liste_mine : 
        board[(mine['x'], mine['y'])] = False

        
    return board

position_valide = board_update(position_valide, equipe_rose, equipe_bleu, equipe_jaune, equipe_vert, liste_mur, liste_mine)

def selection_piece(liste_equipe, choix, frame_piece, liste_abilite, position_a_jouer) : 
    if choix: 
        for piece in liste_equipe : 
            if pyxel.mouse_x//16 * 16 == piece['x'] and pyxel.mouse_y//16 * 16 == piece['y'] and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and frame_piece != pyxel.frame_count and piece['en_vie'] and (piece['x'], piece['y']) not in position_a_jouer : 
                piece['en_mouvement'] = True
                frame_piece = pyxel.frame_count                
    else : 
        for piece in liste_equipe : 

            if pyxel.mouse_x//16 * 16 == piece['x'] and pyxel.mouse_y//16 * 16 == piece['y'] and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and piece['en_mouvement'] and frame_piece != pyxel.frame_count and piece['en_vie'] and (piece['x'], piece['y']) not in position_a_jouer  : 
                piece['en_mouvement'] = False
                piece['controle'] = False
                choix = True
                frame_piece = pyxel.frame_count

            elif pyxel.mouse_x//16 * 16 == piece['x'] and pyxel.mouse_y//16 * 16 == piece['y'] and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and not piece['en_mouvement'] and frame_piece != pyxel.frame_count and piece['en_vie'] and (piece['x'], piece['y']) not in position_a_jouer : 
                for piece_1 in liste_equipe  :
                    if piece_1['en_mouvement'] and piece_1 != piece and piece_1['en_vie']: 
                        piece_1['en_mouvement'] = False
                        piece_1['controle'] = False
                        piece['en_mouvement'] = True
                        choix = True
                        frame_piece = pyxel.frame_count
                
                for abilite_1 in liste_abilite  :
                    if abilite_1['selection'] and abilite_1['type'] != 'piratage' : 
                        abilite_1['selection'] = False
                        piece['en_mouvement'] = True
                        choix = True
                        frame_piece = pyxel.frame_count
                    
                    if abilite_1['selection'] and abilite_1['type'] == 'piratage'  and (piece['x'], piece['y']) not in position_a_jouer : 
                        abilite_1['selection'] = False
                        piece['en_mouvement'] = True
                        choix = True
                        frame_piece = pyxel.frame_count

    return liste_equipe, choix, frame_piece, liste_abilite

def selection_abilite(liste_abilite, choix, frame_abilite, liste_equipe) : 
    if choix: 
        for abilite in liste_abilite : 
            if pyxel.mouse_x//16 * 16 == abilite['x'] and pyxel.mouse_y//16 * 16 == abilite['y'] and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and frame_abilite != pyxel.frame_count and abilite['recharge'] == 0 and abilite['activation']: 
                
                abilite['selection'] = True
                choix = False
                frame_abilite = pyxel.frame_count                
    else : 
        for abilite in liste_abilite : 

            if pyxel.mouse_x//16 * 16 == abilite['x'] and pyxel.mouse_y//16 * 16 == abilite['y'] and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and abilite['selection'] and frame_abilite != pyxel.frame_count and abilite['recharge'] == 0 and abilite['activation'] : 
                abilite['selection'] = False
                choix = True
                frame_abilite = pyxel.frame_count

            elif pyxel.mouse_x//16 * 16 == abilite['x'] and pyxel.mouse_y//16 * 16 == abilite['y'] and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and not abilite['selection'] and frame_abilite != pyxel.frame_count and abilite['recharge'] == 0 and abilite['activation'] : 
                for abilite_1 in liste_abilite  :
                    if abilite_1['selection'] and abilite != abilite_1: 
                        abilite_1['selection'] = False
                        abilite['selection'] = True
                        choix = True
                        frame_abilite = pyxel.frame_count
                for piece_1 in liste_equipe  :
                    if piece_1['en_mouvement'] : 
                        piece_1['en_mouvement'] = False
                        piece_1['controle'] = False
                        abilite['selection'] = True
                        choix = True
                        frame_abilite = pyxel.frame_count

    return liste_abilite, choix, frame_abilite, liste_equipe

def mouvement_citoyen(liste_equipe, liste_equipe_1, liste_equipe_2, liste_equipe_3, position_a_jouer, position_jouable, position_valide, choix, liste_mine) : 

    if choix and not len(position_a_jouer) > 0: 


        
        for piece in liste_equipe : 
            #ROSE
            if piece['type'] == 'citoyen' and piece['en_mouvement'] and piece['equipe'] == 'rose'  :

                position_a_jouer = mouvement_citoyen_1(piece, position_a_jouer, (-16), 0, liste_equipe_1, liste_equipe_2, liste_equipe_3, position_jouable, position_valide, liste_equipe, liste_mine)

                
            #VERT
            elif piece['type'] == 'citoyen' and piece['en_mouvement'] and piece['equipe'] == 'vert'  :

                position_a_jouer = mouvement_citoyen_1(piece, position_a_jouer, 0, (+16), liste_equipe_1, liste_equipe_2, liste_equipe_3, position_jouable, position_valide, liste_equipe, liste_mine)

            #JAUNE
            elif piece['type'] == 'citoyen' and piece['en_mouvement'] and piece['equipe'] == 'jaune'  :

                position_a_jouer = mouvement_citoyen_1(piece, position_a_jouer, (+16), 0, liste_equipe_1, liste_equipe_2, liste_equipe_3, position_jouable, position_valide, liste_equipe, liste_mine)

            elif piece['type'] == 'citoyen' and piece['en_mouvement'] and piece['equipe'] == 'bleu'  :

                position_a_jouer = mouvement_citoyen_1(piece, position_a_jouer, 0, (-16), liste_equipe_1, liste_equipe_2, liste_equipe_3, position_jouable, position_valide, liste_equipe, liste_mine)

    return liste_equipe, position_a_jouer

def mouvement_citoyen_1(piece, position_a_jouer, new_x, new_y, liste_equipe_1, liste_equipe_2, liste_equipe_3, position_jouable, position_valide, liste_equipe, liste_mine) : 
    new_position = (piece['x'] + new_x, piece['y'] + new_y)
    i = 0

    if piece['1er_tour'] : 
        while new_position in position_jouable and position_valide[new_position] and i < 2: 
            position_a_jouer.append(new_position)
            new_position = (new_position[0] + new_x, new_position[1]+ new_y)
            i += 1 
        
        if new_position in position_jouable and not position_valide[new_position] and i < 2 :
            for mine in liste_mine : 
                if (mine['x'], mine['y']) == new_position : 
                    position_a_jouer.append(new_position)
            

    else :
        while new_position in position_jouable and position_valide[new_position] and i < 1: 
            position_a_jouer.append(new_position)
            new_position = (new_position[0] + new_x, new_position[1] + new_y)
            i += 1 
        if new_position in position_jouable and not position_valide[new_position] and i < 1 :
            for mine in liste_mine : 
                if (mine['x'], mine['y']) == new_position : 
                    position_a_jouer.append(new_position)
    


    
    position_a_jouer = citoyen_attaque(liste_equipe_1, liste_equipe_2, liste_equipe_3, position_a_jouer, position_jouable, piece, position_valide, liste_equipe, liste_mine)

    return position_a_jouer

def citoyen_attaque(liste_equipe_1, liste_equipe_2, liste_equipe_3, position_a_jouer, position_jouable, piece, position_valide, liste_equipe, liste_mine) : 
        
    var_1 = []
    for piece_4 in liste_equipe : 
        if (piece_4['x'], piece_4['y']) in [(piece['x'] + 16, piece['y'] + 16), (piece['x'] - 16, piece['y'] + 16), (piece['x'] + 16, piece['y'] - 16), (piece['x'] - 16, piece['y'] - 16)] :
            var_1.append((piece_4['x'], piece_4['y'])) 

   
    #ROSE
    if  piece['equipe'] == 'rose' and (piece['x'] - 16, piece['y'] - 16) in  position_jouable and not(position_valide[(piece['x'] - 16, piece['y'] - 16)]) and (piece['x'] - 16, piece['y'] - 16) not in var_1:
        for piece_1 in liste_equipe_1 : 
            if (piece_1['x'], piece_1['y']) == (piece['x'] - 16, piece['y'] - 16)  and not piece_1['barriere']: 
                position_a_jouer.append((piece_1['x'], piece_1['y']))

        for piece_1 in liste_equipe_2 : 
            if (piece_1['x'], piece_1['y']) == (piece['x'] - 16, piece['y'] - 16)  and not piece_1['barriere']: 
                position_a_jouer.append((piece_1['x'], piece_1['y']))
        
        for piece_1 in liste_equipe_3 : 
            if (piece_1['x'], piece_1['y']) == (piece['x'] - 16, piece['y'] - 16)  and not piece_1['barriere']: 
                position_a_jouer.append((piece_1['x'], piece_1['y']))
        
        for mine in liste_mine :
            if (mine['x'], mine['y']) == (piece['x'] - 16, piece['y'] - 16)  and not piece_1['barriere']:
                position_a_jouer.append((mine['x'], mine['y']))
    
    if  piece['equipe'] == 'rose' and (piece['x'] - 16, piece['y'] + 16) in  position_jouable and not(position_valide[(piece['x'] - 16, piece['y'] + 16)]) and (piece['x'] - 16, piece['y'] + 16) not in var_1:
        for piece_1 in liste_equipe_1 : 
            if (piece_1['x'], piece_1['y']) == (piece['x'] - 16, piece['y'] + 16) and not piece_1['barriere'] : 
                position_a_jouer.append((piece_1['x'], piece_1['y']))

        for piece_1 in liste_equipe_2 : 
            if (piece_1['x'], piece_1['y']) == (piece['x'] - 16, piece['y'] + 16) and not piece_1['barriere'] : 
                position_a_jouer.append((piece_1['x'], piece_1['y']))
        
        for piece_1 in liste_equipe_3 : 
            if (piece_1['x'], piece_1['y']) == (piece['x'] - 16, piece['y'] + 16) and not piece_1['barriere'] : 
                position_a_jouer.append((piece_1['x'], piece_1['y']))
        for mine in liste_mine :
            if (mine['x'], mine['y']) == (piece['x'] - 16, piece['y'] + 16) and not piece_1['barriere'] :
                position_a_jouer.append((mine['x'], mine['y']))

    #VERT   
    if  piece['equipe'] == 'vert' and (piece['x'] - 16, piece['y'] + 16) in  position_jouable and not(position_valide[(piece['x'] - 16, piece['y'] + 16)]) and (piece['x'] - 16, piece['y'] + 16) not in var_1:
        for piece_1 in liste_equipe_1 : 
            if (piece_1['x'], piece_1['y']) == (piece['x'] - 16, piece['y'] + 16) and not piece_1['barriere'] : 
                position_a_jouer.append((piece_1['x'], piece_1['y']))

        for piece_1 in liste_equipe_2 : 
            if (piece_1['x'], piece_1['y']) == (piece['x'] - 16, piece['y'] + 16) and not piece_1['barriere'] : 
                position_a_jouer.append((piece_1['x'], piece_1['y']))
        
        for piece_1 in liste_equipe_3 : 
            if (piece_1['x'], piece_1['y']) == (piece['x'] - 16, piece['y'] + 16) and not piece_1['barriere'] : 
                position_a_jouer.append((piece_1['x'], piece_1['y']))

        for mine in liste_mine :
            if (mine['x'], mine['y']) == (piece['x'] - 16, piece['y'] + 16) and not piece_1['barriere'] :
                position_a_jouer.append((mine['x'], mine['y']))
    
    if  piece['equipe'] == 'vert' and (piece['x'] + 16, piece['y'] + 16) in  position_jouable and not(position_valide[(piece['x'] + 16, piece['y'] + 16)]) and (piece['x'] + 16, piece['y'] + 16) not in var_1:
        for piece_1 in liste_equipe_1 : 
            if (piece_1['x'], piece_1['y']) == (piece['x'] + 16, piece['y'] + 16) and not piece_1['barriere'] : 
                position_a_jouer.append((piece_1['x'], piece_1['y']))

        for piece_1 in liste_equipe_2 : 
            if (piece_1['x'], piece_1['y']) == (piece['x'] + 16, piece['y'] + 16) and not piece_1['barriere'] : 
                position_a_jouer.append((piece_1['x'], piece_1['y']))
        
        for piece_1 in liste_equipe_3 : 
            if (piece_1['x'], piece_1['y']) == (piece['x'] + 16, piece['y'] + 16) and not piece_1['barriere'] : 
                position_a_jouer.append((piece_1['x'], piece_1['y']))

        for mine in liste_mine :
            if (mine['x'], mine['y']) == (piece['x'] + 16, piece['y'] + 16) and not piece_1['barriere'] :
                position_a_jouer.append((mine['x'], mine['y']))

    #JAUNE
    if  piece['equipe'] == 'jaune' and (piece['x'] + 16, piece['y'] - 16) in  position_jouable and not(position_valide[(piece['x'] + 16, piece['y'] - 16)]) and (piece['x'] + 16, piece['y'] - 16) not in var_1:
        for piece_1 in liste_equipe_1 : 
            if (piece_1['x'], piece_1['y']) == (piece['x'] + 16, piece['y'] - 16) and not piece_1['barriere'] : 
                position_a_jouer.append((piece_1['x'], piece_1['y']))

        for piece_1 in liste_equipe_2 : 
            if (piece_1['x'], piece_1['y']) == (piece['x'] + 16, piece['y'] - 16) and not piece_1['barriere'] : 
                position_a_jouer.append((piece_1['x'], piece_1['y']))
        
        for piece_1 in liste_equipe_3 : 
            if (piece_1['x'], piece_1['y']) == (piece['x'] + 16, piece['y'] - 16) and not piece_1['barriere'] : 
                position_a_jouer.append((piece_1['x'], piece_1['y']))

        for mine in liste_mine :
            if (mine['x'], mine['y']) == (piece['x'] + 16, piece['y'] - 16) and not piece_1['barriere'] :
                position_a_jouer.append((mine['x'], mine['y']))
    
    if  piece['equipe'] == 'jaune' and (piece['x'] + 16, piece['y'] + 16) in  position_jouable and not(position_valide[(piece['x'] + 16, piece['y'] + 16)]) and (piece['x'] + 16, piece['y'] + 16) not in var_1:
        for piece_1 in liste_equipe_1 : 
            if (piece_1['x'], piece_1['y']) == (piece['x'] + 16, piece['y'] + 16) and not piece_1['barriere'] : 
                position_a_jouer.append((piece_1['x'], piece_1['y']))

        for piece_1 in liste_equipe_2 : 
            if (piece_1['x'], piece_1['y']) == (piece['x'] + 16, piece['y'] + 16) and not piece_1['barriere'] : 
                position_a_jouer.append((piece_1['x'], piece_1['y']))
        
        for piece_1 in liste_equipe_3 : 
            if (piece_1['x'], piece_1['y']) == (piece['x'] + 16, piece['y'] + 16) and not piece_1['barriere'] : 
                position_a_jouer.append((piece_1['x'], piece_1['y']))

        for mine in liste_mine :
            if (mine['x'], mine['y']) == (piece['x'] + 16, piece['y'] + 16) and not piece_1['barriere'] :
                position_a_jouer.append((mine['x'], mine['y']))

    #BLEU

    if  piece['equipe'] == 'bleu' and (piece['x'] - 16, piece['y'] - 16) in  position_jouable and not(position_valide[(piece['x'] - 16, piece['y'] - 16)]) and (piece['x'] - 16, piece['y'] - 16) not in var_1:
        for piece_1 in liste_equipe_1 : 
            if (piece_1['x'], piece_1['y']) == (piece['x'] - 16, piece['y'] - 16) and not piece_1['barriere'] : 
                position_a_jouer.append((piece_1['x'], piece_1['y']))

        for piece_1 in liste_equipe_2 : 
            if (piece_1['x'], piece_1['y']) == (piece['x'] - 16, piece['y'] - 16) and not piece_1['barriere'] : 
                position_a_jouer.append((piece_1['x'], piece_1['y']))
        
        for piece_1 in liste_equipe_3 : 
            if (piece_1['x'], piece_1['y']) == (piece['x'] - 16, piece['y'] - 16) and not piece_1['barriere'] : 
                position_a_jouer.append((piece_1['x'], piece_1['y']))
        
        for mine in liste_mine :
            if (mine['x'], mine['y']) == (piece['x'] - 16, piece['y'] - 16) and not piece_1['barriere'] :
                position_a_jouer.append((mine['x'], mine['y']))
    
    if  piece['equipe'] == 'bleu' and (piece['x'] + 16, piece['y'] - 16) in  position_jouable and not(position_valide[(piece['x'] + 16, piece['y'] - 16)]) and (piece['x'] + 16, piece['y'] - 16) not in var_1:
        for piece_1 in liste_equipe_1 : 
            if (piece_1['x'], piece_1['y']) == (piece['x'] + 16, piece['y'] - 16) and not piece_1['barriere'] : 
                position_a_jouer.append((piece_1['x'], piece_1['y']))

        for piece_1 in liste_equipe_2 : 
            if (piece_1['x'], piece_1['y']) == (piece['x'] + 16, piece['y'] - 16) and not piece_1['barriere'] : 
                position_a_jouer.append((piece_1['x'], piece_1['y']))
        
        for piece_1 in liste_equipe_3 : 
            if (piece_1['x'], piece_1['y']) == (piece['x'] + 16, piece['y'] - 16) and not piece_1['barriere'] : 
                position_a_jouer.append((piece_1['x'], piece_1['y']))
        
        for mine in liste_mine :
            if (mine['x'], mine['y']) == (piece['x'] + 16, piece['y'] - 16) and not piece_1['barriere'] :
                position_a_jouer.append((mine['x'], mine['y']))


    return position_a_jouer

def mouvement_ouvrier(liste_equipe, liste_equipe_1, liste_equipe_2, liste_equipe_3, position_a_jouer, position_jouable, position_valide, choix, liste_mine) : 



    if choix and len(position_a_jouer) < 1 : 
        new_position = (32, 16)
        new_position_1 = (32, -16)
        new_position_2 = (-16, 32)
        new_position_3 = (16, 32)
        new_position_4 = (-32, 16)
        new_position_5 = (-32, -16)
        new_position_6 = (-16, -32)
        new_position_7 = (16, -32)

        for piece in liste_equipe : 
            if piece['type'] == 'ouvrier' and piece['en_mouvement'] : 

                if (piece['x'] + new_position[0], piece['y'] + new_position[1]) in position_jouable and position_valide[(piece['x'] + new_position[0], piece['y'] + new_position[1])] :
                    position_a_jouer.append((piece['x'] + new_position[0], piece['y'] + new_position[1]))
                elif (piece['x'] + new_position[0], piece['y'] + new_position[1]) in position_jouable and not position_valide[(piece['x'] + new_position[0], piece['y'] + new_position[1])] : 
                    position_a_jouer = piece_attaque(piece['x'] + new_position[0], piece['y'] + new_position[1], liste_equipe_1, liste_equipe_2, liste_equipe_3, position_a_jouer, liste_mine)

                if (piece['x'] + new_position_1[0], piece['y'] + new_position_1[1]) in position_jouable and position_valide[(piece['x'] + new_position_1[0], piece['y'] + new_position_1[1])] :
                    position_a_jouer.append((piece['x'] + new_position_1[0], piece['y'] + new_position_1[1]))
                elif (piece['x'] + new_position_1[0], piece['y'] + new_position_1[1]) in position_jouable and not position_valide[(piece['x'] + new_position_1[0], piece['y'] + new_position_1[1])] : 
                    position_a_jouer = piece_attaque(piece['x'] + new_position_1[0], piece['y'] + new_position_1[1], liste_equipe_1, liste_equipe_2, liste_equipe_3, position_a_jouer, liste_mine)

                if (piece['x'] + new_position_2[0], piece['y'] + new_position_2[1]) in position_jouable and position_valide[(piece['x'] + new_position_2[0], piece['y'] + new_position_2[1])] :
                    position_a_jouer.append((piece['x'] + new_position_2[0], piece['y'] + new_position_2[1]))
                elif (piece['x'] + new_position_2[0], piece['y'] + new_position_2[1]) in position_jouable and not position_valide[(piece['x'] + new_position_2[0], piece['y'] + new_position_2[1])] : 
                    position_a_jouer = piece_attaque(piece['x'] + new_position_2[0], piece['y'] + new_position_2[1], liste_equipe_1, liste_equipe_2, liste_equipe_3, position_a_jouer, liste_mine)              
                
                if (piece['x'] + new_position_3[0], piece['y'] + new_position_3[1]) in position_jouable and position_valide[(piece['x'] + new_position_3[0], piece['y'] + new_position_3[1])] :
                    position_a_jouer.append((piece['x'] + new_position_3[0], piece['y'] + new_position_3[1]))
                elif (piece['x'] + new_position_3[0], piece['y'] + new_position_3[1]) in position_jouable and not position_valide[(piece['x'] + new_position_3[0], piece['y'] + new_position_3[1])] : 
                    position_a_jouer = piece_attaque(piece['x'] + new_position_3[0], piece['y'] + new_position_3[1], liste_equipe_1, liste_equipe_2, liste_equipe_3, position_a_jouer, liste_mine)            
                
                if (piece['x'] + new_position_4[0], piece['y'] + new_position_4[1]) in position_jouable and position_valide[(piece['x'] + new_position_4[0], piece['y'] + new_position_4[1])] :
                    position_a_jouer.append((piece['x'] + new_position_4[0], piece['y'] + new_position_4[1]))
                elif (piece['x'] + new_position_4[0], piece['y'] + new_position_4[1]) in position_jouable and not position_valide[(piece['x'] + new_position_4[0], piece['y'] + new_position_4[1])] : 
                    position_a_jouer = piece_attaque(piece['x'] + new_position_4[0], piece['y'] + new_position_4[1], liste_equipe_1, liste_equipe_2, liste_equipe_3, position_a_jouer, liste_mine)

                if (piece['x'] + new_position_5[0], piece['y'] + new_position_5[1]) in position_jouable and position_valide[(piece['x'] + new_position_5[0], piece['y'] + new_position_5[1])] :
                    position_a_jouer.append((piece['x'] + new_position_5[0], piece['y'] + new_position_5[1]))
                elif (piece['x'] + new_position_5[0], piece['y'] + new_position_5[1]) in position_jouable and not position_valide[(piece['x'] + new_position_5[0], piece['y'] + new_position_5[1])] : 
                    position_a_jouer = piece_attaque(piece['x'] + new_position_5[0], piece['y'] + new_position_5[1], liste_equipe_1, liste_equipe_2, liste_equipe_3, position_a_jouer, liste_mine)

                if (piece['x'] + new_position_6[0], piece['y'] + new_position_6[1]) in position_jouable and position_valide[(piece['x'] + new_position_6[0], piece['y'] + new_position_6[1])] :
                    position_a_jouer.append((piece['x'] + new_position_6[0], piece['y'] + new_position_6[1]))
                elif (piece['x'] + new_position_6[0], piece['y'] + new_position_6[1]) in position_jouable and not position_valide[(piece['x'] + new_position_6[0], piece['y'] + new_position_6[1])] : 
                    position_a_jouer = piece_attaque(piece['x'] + new_position_6[0], piece['y'] + new_position_6[1], liste_equipe_1, liste_equipe_2, liste_equipe_3, position_a_jouer, liste_mine)

                if (piece['x'] + new_position_7[0], piece['y'] + new_position_7[1]) in position_jouable and position_valide[(piece['x'] + new_position_7[0], piece['y'] + new_position_7[1])] :
                    position_a_jouer.append((piece['x'] + new_position_7[0], piece['y'] + new_position_7[1]))
                elif (piece['x'] + new_position_7[0], piece['y'] + new_position_7[1]) in position_jouable and not position_valide[(piece['x'] + new_position_7[0], piece['y'] + new_position_7[1])] : 
                    position_a_jouer = piece_attaque(piece['x'] + new_position_7[0], piece['y'] + new_position_7[1], liste_equipe_1, liste_equipe_2, liste_equipe_3, position_a_jouer, liste_mine)
    return position_a_jouer

def piece_attaque(x_attaque, y_attaque, liste_equipe_1, liste_equipe_2, liste_equipe_3, position_a_jouer, liste_mine) : 
    for piece in liste_equipe_1 : 
        if piece['en_vie'] and (piece['x'], piece['y']) == (x_attaque, y_attaque) and not piece['barriere'] : 
            position_a_jouer.append((x_attaque, y_attaque))
    for piece in liste_equipe_2 : 
        if piece['en_vie'] and (piece['x'], piece['y']) == (x_attaque, y_attaque) and not piece['barriere'] : 
            position_a_jouer.append((x_attaque, y_attaque))
    for piece in liste_equipe_3 : 
        if piece['en_vie'] and (piece['x'], piece['y']) == (x_attaque, y_attaque) and not piece['barriere'] : 
            position_a_jouer.append((x_attaque, y_attaque))
    for mine in liste_mine : 
        if (mine['x'], mine['y']) == (x_attaque, y_attaque) : 
            position_a_jouer.append((x_attaque, y_attaque))

    return position_a_jouer

def mouvement_soldat(liste_equipe, liste_equipe_1, liste_equipe_2, liste_equipe_3, position_a_jouer, position_jouable, position_valide, choix, liste_mine) : 

    if choix and len(position_a_jouer) < 1 : 
        for piece in liste_equipe : 
            if piece['type'] == 'soldat' and piece['en_mouvement'] : 
                
                new_position = (piece['x'] + 16, piece['y'])
                while new_position in position_jouable and position_valide[new_position]: 
                    position_a_jouer.append(new_position)
                    new_position = (new_position[0] + 16, new_position[1])
                if new_position in position_jouable and not position_valide[new_position] : 
                    position_a_jouer = piece_attaque(new_position[0] , new_position[1], liste_equipe_1, liste_equipe_2, liste_equipe_3, position_a_jouer, liste_mine)

                new_position = (piece['x'] - 16 , piece['y'])
                while new_position in position_jouable and position_valide[new_position]: 
                    position_a_jouer.append(new_position)
                    new_position = (new_position[0] - 16, new_position[1])
                if new_position in position_jouable and not position_valide[new_position] : 
                    position_a_jouer = piece_attaque(new_position[0] , new_position[1], liste_equipe_1, liste_equipe_2, liste_equipe_3, position_a_jouer, liste_mine)

                new_position = (piece['x'] , piece['y'] +16)
                while new_position in position_jouable and position_valide[new_position]: 
                    position_a_jouer.append(new_position)
                    new_position = (new_position[0], new_position[1] +16)
                if new_position in position_jouable and not position_valide[new_position] : 
                    position_a_jouer = piece_attaque(new_position[0], new_position[1] , liste_equipe_1, liste_equipe_2, liste_equipe_3, position_a_jouer, liste_mine)

                new_position = (piece['x'] , piece['y']-16)
                while new_position in position_jouable and position_valide[new_position]: 
                    position_a_jouer.append(new_position)
                    new_position = (new_position[0] , new_position[1]-16)
                if new_position in position_jouable and not position_valide[new_position] : 
                    position_a_jouer = piece_attaque(new_position[0], new_position[1] , liste_equipe_1, liste_equipe_2, liste_equipe_3, position_a_jouer, liste_mine)

    return position_a_jouer

def mouvement_president(liste_equipe, liste_equipe_1, liste_equipe_2, liste_equipe_3, position_a_jouer, position_jouable, position_valide, choix, liste_mine) :
    if choix and len(position_a_jouer) < 1 : 
        for piece in liste_equipe : 
            if piece['en_mouvement'] and piece['type'] == 'president' : 
                for j in range(-16 ,17, 16) : 
                    for i in range(-16, 17, 16) : 
                        if (piece['x'] + j, piece['y'] + i) in position_jouable and position_valide[(piece['x'] + j, piece['y'] + i)] : 
                            position_a_jouer.append((piece['x'] + j, piece['y'] + i))
                        elif (piece['x'] + j, piece['y'] + i) in position_jouable and not position_valide[(piece['x'] + j, piece['y'] + i)] :
                            position_a_jouer = piece_attaque(piece['x'] + j , piece['y'] + i, liste_equipe_1, liste_equipe_2, liste_equipe_3, position_a_jouer, liste_mine)
    return position_a_jouer

def mouvement_ministre(liste_equipe, liste_equipe_1, liste_equipe_2, liste_equipe_3, position_a_jouer, position_jouable, position_valide, choix, liste_mine) :
    if choix and len(position_a_jouer) < 1 :
         for piece in liste_equipe : 
            if piece['type'] == 'ministre' and piece['en_mouvement'] : 
                new_position = (piece['x'] + 16, piece['y'])
                while new_position in position_jouable and position_valide[new_position]: 
                    position_a_jouer.append(new_position)
                    new_position = (new_position[0] + 16, new_position[1])
                if new_position in position_jouable and not position_valide[new_position] : 
                    position_a_jouer = piece_attaque(new_position[0] , new_position[1], liste_equipe_1, liste_equipe_2, liste_equipe_3, position_a_jouer, liste_mine)

                new_position = (piece['x'] - 16 , piece['y'])
                while new_position in position_jouable and position_valide[new_position]: 
                    position_a_jouer.append(new_position)
                    new_position = (new_position[0] - 16, new_position[1])
                if new_position in position_jouable and not position_valide[new_position] : 
                    position_a_jouer = piece_attaque(new_position[0] , new_position[1], liste_equipe_1, liste_equipe_2, liste_equipe_3, position_a_jouer, liste_mine)

                new_position = (piece['x'] , piece['y'] +16)
                while new_position in position_jouable and position_valide[new_position]: 
                    position_a_jouer.append(new_position)
                    new_position = (new_position[0], new_position[1] +16)
                if new_position in position_jouable and not position_valide[new_position] : 
                    position_a_jouer = piece_attaque(new_position[0], new_position[1] , liste_equipe_1, liste_equipe_2, liste_equipe_3, position_a_jouer, liste_mine)

                new_position = (piece['x'] , piece['y']-16)
                while new_position in position_jouable and position_valide[new_position]: 
                    position_a_jouer.append(new_position)
                    new_position = (new_position[0] , new_position[1]-16)
                if new_position in position_jouable and not position_valide[new_position] : 
                    position_a_jouer = piece_attaque(new_position[0], new_position[1] , liste_equipe_1, liste_equipe_2, liste_equipe_3, position_a_jouer, liste_mine)

                

                new_position = (piece['x'] + 16, piece['y'] +16)
                while new_position in position_jouable and position_valide[new_position]: 
                    position_a_jouer.append(new_position)
                    new_position = (new_position[0] +16 , new_position[1] + 16)
                if new_position in position_jouable and not position_valide[new_position] : 
                    position_a_jouer = piece_attaque(new_position[0] , new_position[1], liste_equipe_1, liste_equipe_2, liste_equipe_3, position_a_jouer, liste_mine)

                new_position = (piece['x'] - 16 , piece['y'] -16)
                while new_position in position_jouable and position_valide[new_position]: 
                    position_a_jouer.append(new_position)
                    new_position = (new_position[0] -16 , new_position[1] - 16)
                if new_position in position_jouable and not position_valide[new_position] : 
                    position_a_jouer = piece_attaque(new_position[0] , new_position[1], liste_equipe_1, liste_equipe_2, liste_equipe_3, position_a_jouer, liste_mine)

                new_position = (piece['x'] -16 , piece['y'] +16)
                while new_position in position_jouable and position_valide[new_position]: 
                    position_a_jouer.append(new_position)
                    new_position = (new_position[0] -16 , new_position[1] + 16)
                if new_position in position_jouable and not position_valide[new_position] : 
                    position_a_jouer = piece_attaque(new_position[0], new_position[1] , liste_equipe_1, liste_equipe_2, liste_equipe_3, position_a_jouer, liste_mine)

                new_position = (piece['x'] +16, piece['y']-16)
                while new_position in position_jouable and position_valide[new_position]: 
                    position_a_jouer.append(new_position)
                    new_position = (new_position[0] +16 , new_position[1] - 16)
                if new_position in position_jouable and not position_valide[new_position] : 
                    position_a_jouer = piece_attaque(new_position[0], new_position[1] , liste_equipe_1, liste_equipe_2, liste_equipe_3, position_a_jouer, liste_mine)

    return position_a_jouer

def mouvement_pirate(liste_equipe, liste_equipe_1, liste_equipe_2, liste_equipe_3, position_a_jouer, position_jouable, position_valide, choix, liste_mine) : 
    if choix and len(position_a_jouer) < 1 :
         for piece in liste_equipe : 
            if piece['type'] == 'pirate' and piece['en_mouvement'] :            
                new_position = (piece['x'] + 16, piece['y'] +16)
                while new_position in position_jouable and position_valide[new_position]: 
                    position_a_jouer.append(new_position)
                    new_position = (new_position[0] +16 , new_position[1] + 16)
                if new_position in position_jouable and not position_valide[new_position] : 
                    position_a_jouer = piece_attaque(new_position[0] , new_position[1], liste_equipe_1, liste_equipe_2, liste_equipe_3, position_a_jouer, liste_mine)

                new_position = (piece['x'] - 16 , piece['y'] -16)
                while new_position in position_jouable and position_valide[new_position]: 
                    position_a_jouer.append(new_position)
                    new_position = (new_position[0] -16 , new_position[1] - 16)
                if new_position in position_jouable and not position_valide[new_position] : 
                    position_a_jouer = piece_attaque(new_position[0] , new_position[1], liste_equipe_1, liste_equipe_2, liste_equipe_3, position_a_jouer, liste_mine)

                new_position = (piece['x'] -16 , piece['y'] +16)
                while new_position in position_jouable and position_valide[new_position]: 
                    position_a_jouer.append(new_position)
                    new_position = (new_position[0] -16 , new_position[1] + 16)
                if new_position in position_jouable and not position_valide[new_position] : 
                    position_a_jouer = piece_attaque(new_position[0], new_position[1] , liste_equipe_1, liste_equipe_2, liste_equipe_3, position_a_jouer, liste_mine)

                new_position = (piece['x'] +16, piece['y']-16)
                while new_position in position_jouable and position_valide[new_position]: 
                    position_a_jouer.append(new_position)
                    new_position = (new_position[0] +16 , new_position[1] - 16)
                if new_position in position_jouable and not position_valide[new_position] : 
                    position_a_jouer = piece_attaque(new_position[0], new_position[1] , liste_equipe_1, liste_equipe_2, liste_equipe_3, position_a_jouer, liste_mine)

    return position_a_jouer

def piece_mouvement(liste_equipe, liste_equipe_1, liste_equipe_2, liste_equipe_3, position_a_jouer, position_jouable, position_valide, choix, liste_mine, liste_abilite) : 
    var_1 = True
    for abilite in liste_abilite : 
        if abilite['selection'] :   
            var_1 = False 
    
    for piece in  liste_equipe : 
                if piece['en_mouvement'] and piece['en_prison'] : 
                    piece['en_mouvement'] = False

    if var_1 : 
        position_a_jouer.clear()
        liste_equipe, position_a_jouer = mouvement_citoyen(liste_equipe, liste_equipe_1, liste_equipe_2, liste_equipe_3, position_a_jouer, position_jouable, position_valide, choix, liste_mine)
        position_a_jouer = mouvement_ouvrier(liste_equipe, liste_equipe_1, liste_equipe_2, liste_equipe_3, position_a_jouer, position_jouable, position_valide, choix, liste_mine)
        position_a_jouer = mouvement_soldat(liste_equipe, liste_equipe_1, liste_equipe_2, liste_equipe_3, position_a_jouer, position_jouable, position_valide, choix, liste_mine)
        position_a_jouer = mouvement_president(liste_equipe, liste_equipe_1, liste_equipe_2, liste_equipe_3, position_a_jouer, position_jouable, position_valide, choix, liste_mine)
        position_a_jouer = mouvement_ministre(liste_equipe, liste_equipe_1, liste_equipe_2, liste_equipe_3, position_a_jouer, position_jouable, position_valide, choix, liste_mine)
        position_a_jouer = mouvement_pirate(liste_equipe, liste_equipe_1, liste_equipe_2, liste_equipe_3, position_a_jouer, position_jouable, position_valide, choix, liste_mine)


        if len(position_a_jouer) > 0 : 
            choix = False
            
        else : 
            choix = True
            for piece in  liste_equipe : 
                if piece['en_mouvement'] : 
                    piece['en_mouvement'] = False
        
    return liste_equipe, position_a_jouer, choix

def piece_deplacement(liste_equipe, liste_equipe_1, liste_equipe_2, liste_equipe_3, position_a_jouer, position_valide, choix, turn, liste_abilite) : 
    for piece in liste_equipe : 
        if (piece['en_mouvement'] or piece['controle']) \
            and (pyxel.mouse_x//16 * 16, pyxel.mouse_y//16 * 16) in position_a_jouer \
            and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) :
                
                if piece['controle'] : 
                    for abilite in liste_abilite : 
                        if abilite['type'] == 'piratage' : 
                            abilite['recharge'] = 12

                piece['en_mouvement'] = False
                piece['controle'] = False
                position_valide[(piece['x'], piece['y'])] = True
                piece['x'] = pyxel.mouse_x//16 * 16
                piece['y'] = pyxel.mouse_y//16 * 16
                position_valide[(piece['x'], piece['y'])] = False
                position_a_jouer.clear()
                choix = True
                turn = (turn + 1)%4

                piece['1er_tour'] = False

                piece, liste_equipe_1, liste_abilite = piece_deplacement_1(piece, liste_equipe_1, liste_abilite)
                piece, liste_equipe_2, liste_abilite = piece_deplacement_1(piece, liste_equipe_2, liste_abilite)
                piece, liste_equipe_3, liste_abilite = piece_deplacement_1(piece, liste_equipe_3, liste_abilite)


    return liste_equipe, liste_equipe_1, liste_equipe_2, liste_equipe_3, position_a_jouer,position_valide, choix, turn, liste_abilite

def piece_deplacement_1(piece, liste_equipe_1, liste_abilite) :
    for piece_1 in liste_equipe_1 : 
                    if (piece['x'], piece['y']) == (piece_1['x'], piece_1['y']) : 
                        if piece_1['type'] != 'soldat' and piece_1['type'] != 'pirate' and piece_1['type'] != 'president' : 
                            liste_equipe_1.remove(piece_1)
                        elif piece_1['type'] in ['soldat', 'pirate'] and piece_1['en_vie']:
                            piece_1['en_vie'] = False

                        elif piece_1['type'] != 'president' : 
                            liste_equipe_1.remove(piece_1)
                            piece['zombie'] = True
                        
                        elif piece_1['type'] == 'president' : 
                            piece_1['en_vie'] = False
                        
                        if piece_1['type'] == 'ministre' : 
                            if piece['type'] == 'citoyen' : 
                                piece['type'] = 'ouvrier'
                            elif piece['type'] == 'ouvrier' : 
                                piece['type'] = 'soldat'
                            elif piece['type'] == 'soldat' : 
                                piece['type'] = 'pirate'
                                piece['en_vie'] = True
                            elif piece['type'] == 'pirate' : 
                                piece['type'] = 'ministre'
                                piece['en_vie'] = True
                            elif piece['type'] == 'president'  :
                                liste_abilite = abilite_changement(liste_abilite)
    

    return piece, liste_equipe_1, liste_abilite

def abilite_changement(liste_abilite) : 
    for abilite in liste_abilite :
        if abilite['type'] == 'bombe' and not abilite['activation'] : 
            abilite['activation'] = True
        elif abilite['type'] == 'bombe' and  abilite['activation'] :
            abilite['boost'] += 1
        elif abilite['type'] == 'teleportation' and  abilite['activation'] : 
            abilite['boost'] += 1

    return liste_abilite

def abilite_positions(liste_equipe, liste_equipe_1, liste_equipe_2, liste_equipe_3, liste_abilite, position_a_jouer, position_jouable, position_valide, choix, liste_mur, liste_mine, liste_prison) :
    var_1 = False
    for abilite in liste_abilite : 
        if abilite['selection'] : 
            var_1 = True
    if var_1 : 
        position_a_jouer.clear()
        position_a_jouer = mur_position(liste_equipe, liste_abilite, position_a_jouer, position_jouable, position_valide)
        position_a_jouer = mine_position(liste_equipe, liste_abilite, position_a_jouer, position_jouable, position_valide)
        position_a_jouer = piratage_position(liste_equipe, liste_abilite, position_a_jouer, position_jouable, position_valide)
        position_a_jouer = bombe_position(liste_equipe, liste_abilite, position_a_jouer, position_jouable, position_valide)
        position_a_jouer = teleportation_position(liste_equipe, liste_abilite, position_a_jouer)
        position_a_jouer = feu_position(liste_equipe, liste_equipe_1, liste_equipe_2, liste_equipe_3, liste_abilite, position_a_jouer, liste_mur, liste_mine, liste_prison)
        position_a_jouer = soin_position(liste_abilite, liste_equipe,liste_equipe_1, liste_equipe_2, liste_equipe_3, position_a_jouer)
        position_a_jouer = prison_position(liste_equipe,liste_equipe_1, liste_equipe_2, liste_equipe_3, liste_abilite, position_a_jouer) 
        position_a_jouer = barriere_position(liste_abilite, liste_equipe, position_a_jouer)

        if len(position_a_jouer) > 0 : 
            choix = False

        else :
            choix = True
            for abilite in liste_abilite : 
                if abilite['selection'] : 
                    abilite['selection'] = False

    return liste_abilite, position_a_jouer, choix

def barriere_position(liste_abilite, liste_equipe, position_a_jouer) :
    
    if len(position_a_jouer) < 1: 
        for abilite in liste_abilite : 
            if abilite['selection'] and abilite['type'] == 'barriere' : 
                
                for piece in liste_equipe : 
                    if piece['type'] == 'ministre' and piece['1er_tour'] == False :
                        for piece_1 in liste_equipe : 
                            if piece_1['en_vie'] and piece_1['type'] != 'president' :
                                for i in range(-32, 33, 16) : 
                                    if (piece['x'] + i, piece['y'] - 32) == (piece_1['x'], piece_1['y']) : 
                                        position_a_jouer.append((piece['x'] + i, piece['y'] - 32))
                                
                                
                                    if (piece['x'] + i, piece['y'] + 32) == (piece_1['x'], piece_1['y']) : 
                                        position_a_jouer.append((piece['x'] + i, piece['y'] + 32))

                                
                                    if (piece['x'] + 32, piece['y'] + i) == (piece_1['x'], piece_1['y']) : 
                                        position_a_jouer.append((piece['x'] + 32, piece['y'] + i))
                                
                                
                                    if (piece['x'] -32, piece['y'] + i) == (piece_1['x'], piece_1['y']) : 
                                        position_a_jouer.append((piece['x'] -32, piece['y'] + i))

                                for j in range(-16 ,17, 16) : 
                                    for i in range(-16, 17, 16) : 
                                        if (piece['x'] + j, piece['y'] + i) == (piece_1['x'], piece_1['y']) : 
                                            position_a_jouer.append((piece['x'] + j, piece['y'] + i))
        
    return position_a_jouer

def soin_position(liste_abilite, liste_equipe,liste_equipe_1, liste_equipe_2, liste_equipe_3, position_a_jouer) :

    var_1 = liste_equipe_1 + liste_equipe_2 + liste_equipe_3
    if len(position_a_jouer) < 1: 
        for abilite in liste_abilite : 
            if abilite['selection'] and abilite['type'] == 'soin' : 
                
                for piece in liste_equipe : 
                    if piece['type'] == 'ministre' and piece['1er_tour'] == False :
                        for piece_1 in liste_equipe : 
                            if piece_1['type'] in ('soldat', 'pirate') and not piece_1['en_vie']  :
                                position_a_jouer.append((piece_1['x'], piece_1['y']))
        for coord in position_a_jouer : 
            if coord in var_1 : 
                position_a_jouer.remove(coord)
    return position_a_jouer

def teleportation_position(liste_equipe, liste_abilite, position_a_jouer) : 
    if len(position_a_jouer) < 1: 
        for abilite in liste_abilite : 
            if abilite['selection'] and abilite['type'] == 'teleportation' : 
               
                for piece in liste_equipe : 
                    if piece['type'] == 'president' and piece['1er_tour'] == False :
                        for piece_1 in liste_equipe : 
                            if piece_1['type'] == 'soldat'  :

                                for i in range(-32, 33, 16) : 
                                    if (piece['x'] + i, piece['y'] - 32) == (piece_1['x'], piece_1['y']) : 
                                        position_a_jouer.append((piece['x'] + i, piece['y'] - 32))
                                
                                
                                    if (piece['x'] + i, piece['y'] + 32) == (piece_1['x'], piece_1['y']) : 
                                        position_a_jouer.append((piece['x'] + i, piece['y'] + 32))

                                
                                    if (piece['x'] + 32, piece['y'] + i) == (piece_1['x'], piece_1['y']) : 
                                        position_a_jouer.append((piece['x'] + 32, piece['y'] + i))
                                
                                
                                    if (piece['x'] -32, piece['y'] + i) == (piece_1['x'], piece_1['y']) : 
                                        position_a_jouer.append((piece['x'] -32, piece['y'] + i))

                                for j in range(-16 ,17, 16) : 
                                    for i in range(-16, 17, 16) : 
                                        if (piece['x'] + j, piece['y'] + i) == (piece_1['x'], piece_1['y']) : 
                                            position_a_jouer.append((piece['x'] + j, piece['y'] + i))
    return position_a_jouer

def feu_position(liste_equipe,liste_equipe_1, liste_equipe_2, liste_equipe_3, liste_abilite, position_a_jouer, liste_mur, liste_mine, liste_prison) : 
    somme_liste = liste_mur + liste_mine + liste_prison  + liste_equipe_1 +  liste_equipe_2+  liste_equipe_3 + liste_equipe
    
    if len(position_a_jouer) < 1 : 
        for abilite in liste_abilite : 
            if abilite['selection'] and abilite['type'] == 'feu' : 

                for piece in liste_equipe : 
                    if piece['type'] == 'ministre' and piece['1er_tour'] == False :

                        for i in range(-32, 33, 16) : 
                            if (piece['x'] + i, piece['y'] - 32) in position_jouable : 
                                position_a_jouer.append((piece['x'] + i, piece['y'] - 32))
                        
                        
                            if (piece['x'] + i, piece['y'] + 32) in position_jouable : 
                                position_a_jouer.append((piece['x'] + i, piece['y'] + 32))

                        
                            if (piece['x'] + 32, piece['y'] + i) in position_jouable : 
                                position_a_jouer.append((piece['x'] + 32, piece['y'] + i))
                        
                        
                            if (piece['x'] -32, piece['y'] + i) in position_jouable: 
                                position_a_jouer.append((piece['x'] -32, piece['y'] + i))

                        for j in range(-16 ,17, 16) : 
                            for i in range(-16, 17, 16) : 
                                if (piece['x'] + j, piece['y'] + i) in position_jouable : 
                                    position_a_jouer.append((piece['x'] + j, piece['y'] + i))

                        if (piece['x'], piece['y']) in position_a_jouer : 
                            position_a_jouer.remove((piece['x'], piece['y']))
    
        for element in somme_liste :
            if element['type'] not in ['citoyen', 'pirate', 'soldat', 'ouvrier', 'ministre'] and (element['x'], element['y']) in position_a_jouer : 
                position_a_jouer.remove((element['x'], element['y']))


    return position_a_jouer

def mur_position(liste_equipe, liste_abilite, position_a_jouer, position_jouable, position_valide) :
    if len(position_a_jouer) < 1: 
        for abilite in liste_abilite : 
            if abilite['selection'] and abilite['type'] == 'mur' : 
               
                for piece in liste_equipe : 
                    if piece['type'] == 'ouvrier' and piece['1er_tour'] == False :

                        for i in range(-32, 33, 16) : 
                            if (piece['x'] + i, piece['y'] - 32) in position_jouable and position_valide[(piece['x'] + i, piece['y'] - 32)] : 
                                position_a_jouer.append((piece['x'] + i, piece['y'] - 32))
                        
                        
                            if (piece['x'] + i, piece['y'] + 32) in position_jouable and position_valide[(piece['x'] + i, piece['y'] + 32)] : 
                                position_a_jouer.append((piece['x'] + i, piece['y'] + 32))

                        
                            if (piece['x'] + 32, piece['y'] + i) in position_jouable and position_valide[(piece['x'] + 32, piece['y'] + i)] : 
                                position_a_jouer.append((piece['x'] + 32, piece['y'] + i))
                        
                        
                            if (piece['x'] -32, piece['y'] + i) in position_jouable and position_valide[(piece['x'] -32, piece['y'] + i)] : 
                                position_a_jouer.append((piece['x'] -32, piece['y'] + i))
    

    return position_a_jouer

def mine_position(liste_equipe, liste_abilite, position_a_jouer, position_jouable, position_valide):

    if len(position_a_jouer) < 1 : 
        for abilite in liste_abilite : 
            if abilite['selection'] and abilite['type'] == 'mine' : 

                for piece in liste_equipe : 
                    if piece['type'] == 'soldat' and piece['1er_tour'] == False and piece['en_vie'] :

                        for i in range(-32, 33, 16) : 
                            if (piece['x'] + i, piece['y'] - 32) in position_jouable and position_valide[(piece['x'] + i, piece['y'] - 32)] : 
                                position_a_jouer.append((piece['x'] + i, piece['y'] - 32))
                        
                        
                            if (piece['x'] + i, piece['y'] + 32) in position_jouable and position_valide[(piece['x'] + i, piece['y'] + 32)] : 
                                position_a_jouer.append((piece['x'] + i, piece['y'] + 32))

                        
                            if (piece['x'] + 32, piece['y'] + i) in position_jouable and position_valide[(piece['x'] + 32, piece['y'] + i)] : 
                                position_a_jouer.append((piece['x'] + 32, piece['y'] + i))
                        
                        
                            if (piece['x'] -32, piece['y'] + i) in position_jouable and position_valide[(piece['x'] -32, piece['y'] + i)] : 
                                position_a_jouer.append((piece['x'] -32, piece['y'] + i))

                        for j in range(-16 ,17, 16) : 
                            for i in range(-16, 17, 16) : 
                                if (piece['x'] + j, piece['y'] + i) in position_jouable and position_valide[(piece['x'] + j, piece['y'] + i)] : 
                                    position_a_jouer.append((piece['x'] + j, piece['y'] + i))
    return position_a_jouer

def piratage_position(liste_equipe, liste_abilite, position_a_jouer, position_jouable, position_valide) : 

    if len(position_a_jouer) < 1 : 
        for abilite in liste_abilite : 
            if abilite['selection'] and abilite['type'] == 'piratage' : 

                for piece in liste_equipe : 
                    if piece['type'] == 'pirate' and piece['1er_tour'] == False and piece['en_vie'] :
                        for piece_1 in liste_equipe : 

                            for i in range(-32, 33, 16) : 
                                if (piece['x'] + i, piece['y'] - 32) == (piece_1['x'], piece_1['y']) : 
                                    position_a_jouer.append((piece['x'] + i, piece['y'] - 32))
                            
                            
                                if (piece['x'] + i, piece['y'] + 32) == (piece_1['x'], piece_1['y']) : 
                                    position_a_jouer.append((piece['x'] + i, piece['y'] + 32))

                            
                                if (piece['x'] + 32, piece['y'] + i) == (piece_1['x'], piece_1['y']) : 
                                    position_a_jouer.append((piece['x'] + 32, piece['y'] + i))
                            
                            
                                if (piece['x'] -32, piece['y'] + i) == (piece_1['x'], piece_1['y']) : 
                                    position_a_jouer.append((piece['x'] -32, piece['y'] + i))

                            for j in range(-16 ,17, 16) : 
                                for i in range(-16, 17, 16) : 
                                    if (piece['x'] + j, piece['y'] + i) == (piece_1['x'], piece_1['y']) : 
                                        position_a_jouer.append((piece['x'] + j, piece['y'] + i))
        

    return position_a_jouer

def bombe_position(liste_equipe, liste_abilite, position_a_jouer , position_jouable, position_valide) :
    if len(position_a_jouer) < 1 :
        for abilite in liste_abilite : 
            if abilite['type'] == 'bombe' and abilite['selection'] :
                for piece in liste_equipe : 
                    if piece['type'] == 'president' and piece['1er_tour'] == False : 
                            for i in range(-32, 33, 16) : 

                                if (piece['x'] + i, piece['y']- 32) in position_jouable and not position_valide[(piece['x'] + i, piece['y'] - 32)] : 
                                    position_a_jouer.append((piece['x'] + i, piece['y'] - 32))
                            
                            
                                if (piece['x'] + i, piece['y'] + 32) in position_jouable and not position_valide[(piece['x'] + i, piece['y'] + 32)] : 
                                    position_a_jouer.append((piece['x'] + i, piece['y'] + 32))

                            
                                if (piece['x'] + 32, piece['y'] + i) in position_jouable and not position_valide[(piece['x'] + 32, piece['y'] + i)] : 
                                    position_a_jouer.append((piece['x'] + 32, piece['y'] + i))
                            
                            
                                if (piece['x'] -32, piece['y'] + i) in position_jouable and not position_valide[(piece['x'] -32, piece['y'] + i)] : 
                                    position_a_jouer.append((piece['x'] -32, piece['y'] + i))

                            for j in range(-16 ,17, 16) : 
                                for i in range(-16, 17, 16) : 
                                    if (piece['x'] + j, piece['y'] + i) in position_jouable and not position_valide[(piece['x'] + j, piece['y'] + i)] : 
                                        position_a_jouer.append((piece['x'] + j, piece['y'] + i))

        for piece_1 in liste_equipe : 
            if (piece_1['x'], piece_1['y']) in position_a_jouer :   
                position_a_jouer.remove((piece_1['x'], piece_1['y']))

    return position_a_jouer

def prison_position(liste_equipe,liste_equipe_1, liste_equipe_2, liste_equipe_3, liste_abilite, position_a_jouer) : 
    if len(position_a_jouer) < 1 : 
        for abilite in liste_abilite  :
            if abilite['type'] == 'prison' and abilite['selection'] : 
                for piece in liste_equipe :
                    if piece['type'] == 'ministre' and piece['1er_tour'] == False : 
                        position_a_jouer = prison_position_1(liste_equipe_1, piece, position_a_jouer)
                        position_a_jouer = prison_position_1(liste_equipe_2, piece, position_a_jouer)
                        position_a_jouer = prison_position_1(liste_equipe_3, piece, position_a_jouer)
    return position_a_jouer

def prison_position_1(liste_equipe, piece, position_a_jouer) : 

    for piece_1 in liste_equipe : 
        if piece_1['en_vie'] and not piece_1['en_prison'] and piece_1['type'] != 'president' : 
            for i in range(-32, 33, 16) : 
                if (piece['x'] + i, piece['y'] - 32) == (piece_1['x'], piece_1['y']) : 
                    position_a_jouer.append((piece['x'] + i, piece['y'] - 32))
            
            
                if (piece['x'] + i, piece['y'] + 32) == (piece_1['x'], piece_1['y']) : 
                    position_a_jouer.append((piece['x'] + i, piece['y'] + 32))

            
                if (piece['x'] + 32, piece['y'] + i) == (piece_1['x'], piece_1['y']) : 
                    position_a_jouer.append((piece['x'] + 32, piece['y'] + i))
            
            
                if (piece['x'] -32, piece['y'] + i) == (piece_1['x'], piece_1['y']) : 
                    position_a_jouer.append((piece['x'] -32, piece['y'] + i))

            for j in range(-16 ,17, 16) : 
                for i in range(-16, 17, 16) : 
                    if (piece['x'] + j, piece['y'] + i) == (piece_1['x'], piece_1['y']) : 
                        position_a_jouer.append((piece['x'] + j, piece['y'] + i))
    return position_a_jouer

def mouvement_piratage(piece, liste_equipe_1, liste_equipe_2, liste_equipe_3, liste_mine ,position_a_jouer, position_jouable, position_valide) : 
    i = 0
    new_position = (piece['x'] + 16, piece['y'] +16)
    while new_position in position_jouable and position_valide[new_position] and i < 2: 
        position_a_jouer.append(new_position)
        new_position = (new_position[0] +16 , new_position[1] + 16)
        i += 1
    if new_position in position_jouable and not position_valide[new_position] and i < 2: 
        position_a_jouer = piece_attaque(new_position[0] , new_position[1], liste_equipe_1, liste_equipe_2, liste_equipe_3, position_a_jouer, liste_mine)

    i = 0
    new_position = (piece['x'] - 16 , piece['y'] -16)
    while new_position in position_jouable and position_valide[new_position] and i < 2: 
        position_a_jouer.append(new_position)
        new_position = (new_position[0] -16 , new_position[1] - 16)
        i += 1
    if new_position in position_jouable and not position_valide[new_position] and i < 2: 
        position_a_jouer = piece_attaque(new_position[0] , new_position[1], liste_equipe_1, liste_equipe_2, liste_equipe_3, position_a_jouer, liste_mine)

    i = 0
    new_position = (piece['x'] -16 , piece['y'] +16)
    while new_position in position_jouable and position_valide[new_position] and i < 2: 
        position_a_jouer.append(new_position)
        new_position = (new_position[0] -16 , new_position[1] + 16)
        i += 1
    if new_position in position_jouable and not position_valide[new_position] and i < 2: 
        position_a_jouer = piece_attaque(new_position[0], new_position[1] , liste_equipe_1, liste_equipe_2, liste_equipe_3, position_a_jouer, liste_mine)

    i = 0
    new_position = (piece['x'] +16, piece['y']-16)
    while new_position in position_jouable and position_valide[new_position] and i < 2: 
        position_a_jouer.append(new_position)
        new_position = (new_position[0] +16 , new_position[1] - 16)
        i += 1
    if new_position in position_jouable and not position_valide[new_position] and i < 2: 
        position_a_jouer = piece_attaque(new_position[0], new_position[1] , liste_equipe_1, liste_equipe_2, liste_equipe_3, position_a_jouer, liste_mine)

    return position_a_jouer

def bombe(liste_element, x_attaque, y_attaque) : 
    var_1 = False
    for element in liste_element : 
        if (element['x'], element['y']) == (x_attaque, y_attaque) and element['type'] != 'president' : 
            liste_element.remove(element)
            var_1 = True
    return liste_element, var_1

def abilite_action(liste_equipe, liste_equipe_1, liste_equipe_2, liste_equipe_3, liste_abilite, position_a_jouer, position_valide, liste_mur, liste_feu, liste_mine, choix, turn) :
    for abilite in liste_abilite : 
        if abilite['selection']  and (pyxel.mouse_x//16 * 16, pyxel.mouse_y//16 * 16) in position_a_jouer \
            and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and abilite['type'] in ['mur', 'mine', 'piratage', 'bombe', 'teleportation', 'feu', 'soin']:

            if abilite['type'] == 'mur'  : 
                liste_mur.append({'x' : pyxel.mouse_x//16 * 16, 'y' : pyxel.mouse_y//16 * 16, 'tour_restant' : 5, 'type' : 'obstacle' }) 
                position_valide[(pyxel.mouse_x//16 * 16, pyxel.mouse_y//16 * 16)] = False                
                abilite['recharge'] = 6
                turn = (turn + 1)%4
                position_a_jouer.clear()
                choix = True
                
            elif abilite['type'] == 'mine'  : 
                liste_mine.append({'x' : pyxel.mouse_x//16 * 16, 'y' : pyxel.mouse_y//16 * 16, 'tour_restant' : 10, 'type' : 'piege' }) 
                position_valide[(pyxel.mouse_x//16 * 16, pyxel.mouse_y//16 * 16)] = False    
                abilite['recharge'] = 7
                turn = (turn + 1)%4
                position_a_jouer.clear()
                choix = True
                                
            elif abilite['type'] == 'piratage' : 
                for piece in liste_equipe :
                    if (piece['x'], piece['y']) == (pyxel.mouse_x//16 * 16, pyxel.mouse_y//16 * 16) : 

                        position_a_jouer.clear()
                        position_a_jouer = mouvement_piratage(piece, liste_equipe_1, liste_equipe_2, liste_equipe_3, liste_mine ,position_a_jouer, position_jouable, position_valide)

                        if len(position_a_jouer) > 0 : 
                            choix = False
                            piece['controle'] = True
                            piece['en_mouvement'] = True
                            
                        else :
                            choix = True
                        
                        turn = turn
            
            elif abilite['type'] == 'bombe' : 

                liste_mur, var_1 = bombe(liste_mur, pyxel.mouse_x//16 *16, pyxel.mouse_y//16 * 16)
                if not var_1 : 
                    liste_equipe_1, var_1 = bombe(liste_equipe_1, pyxel.mouse_x//16 *16, pyxel.mouse_y//16 * 16)
                if not var_1 :
                    liste_equipe_2, var_1 = bombe(liste_equipe_2, pyxel.mouse_x//16 *16, pyxel.mouse_y//16 * 16)
                if not var_1 :
                    liste_equipe_3, var_1 = bombe(liste_equipe_3, pyxel.mouse_x//16 *16, pyxel.mouse_y//16 * 16)
                if not var_1 :
                    liste_mine, var_1 = bombe(liste_mine, pyxel.mouse_x//16 *16, pyxel.mouse_y//16 * 16)

                if var_1 :
                    position_valide[(pyxel.mouse_x//16 * 16, pyxel.mouse_y//16 * 16)] = True  
                    abilite['recharge'] = 32 - 4 * abilite['boost']
                    
                    turn = (turn + 1)%4
                
                    choix = True

                    position_a_jouer.clear()
                    position_a_jouer = ['explosion']
                    abilite['selection'] = False
            
            elif abilite['type'] == 'teleportation' : 
                new_position_1 = 0  
                new_position_2 = 0
                for piece in liste_equipe : 
                    if piece['type'] == 'president' : 
                        new_position_1 = (piece['x'], piece['y'])
                    if piece['type'] == 'soldat' and (piece['x'], piece['y']) == (pyxel.mouse_x//16 *16, pyxel.mouse_y//16 * 16) and piece['en_vie'] :
                        new_position_2 = (piece['x'], piece['y'])

                if new_position_1 != 0 and new_position_2 != 0 : 
                    for piece in liste_equipe : 
                        if piece['type'] == 'president' : 
                            piece['x'] = new_position_2[0]
                            piece['y'] = new_position_2[1]
                        if piece['type'] == 'soldat' and piece['en_vie'] and (piece['x'], piece['y']) == (pyxel.mouse_x//16 *16, pyxel.mouse_y//16 * 16) : 
                            piece['x'] = new_position_1[0]
                            piece['y'] = new_position_1[1]
                            var_1 = True
                if var_1 : 
                    position_a_jouer.clear()
                    position_a_jouer = ['explosion']

                choix = True
                turn = (turn + 1)%4
                abilite['recharge'] = 20  - 2 * abilite['boost']

            elif abilite['type'] == 'feu' : 
                liste_feu.append({'type' : 'objet', 'tour_restant' : 15 + 3 * abilite['boost'], 'x' : pyxel.mouse_x//16 * 16, 'y' : pyxel.mouse_y//16 * 16, 'frame' : 0})
                abilite['recharge'] = 12 - 2 *abilite['boost']
                turn = (turn + 1)%4            
                choix = True
                position_a_jouer.clear()

            elif abilite['type'] == 'soin' : 
                for piece in liste_equipe : 
                    if not piece['en_vie'] and (piece['x'], piece['y']) == (pyxel.mouse_x//16 * 16, pyxel.mouse_y//16 * 16) :
                        piece['en_vie'] = True
                        abilite['recharge'] = 20 - 3 *abilite['boost']
                        turn = (turn + 1)%4
                        position_a_jouer.clear()
                        choix = True


            if abilite['type'] != 'bombe' : 
                abilite['selection'] = False
                
            


    return liste_equipe, liste_abilite, position_a_jouer, position_valide, liste_mur, liste_feu, liste_mine, choix, turn, liste_equipe_1, liste_equipe_2, liste_equipe_3

def abilite_action_1(liste_equipe, liste_equipe_1, liste_equipe_2, liste_equipe_3, liste_abilite, position_a_jouer, position_valide, liste_prison, liste_barriere,  choix, turn) : 
    for abilite in liste_abilite : 
        if abilite['selection']  and (pyxel.mouse_x//16 * 16, pyxel.mouse_y//16 * 16) in position_a_jouer \
            and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and abilite['type'] in ['prison', 'barriere'] : 
            if abilite['type'] == 'prison' : 
                liste_prison.append({'x': pyxel.mouse_x//16*16, 'y' : pyxel.mouse_y//16 * 16, 'tour_restant' : 10, 'type' : 'stun'})

                position_valide[(pyxel.mouse_x//16 * 16, pyxel.mouse_y//16 * 16)] = False
                abilite['recharge'] = 12 - abilite['boost']
                abilite['selection'] = False
                choix = True
                turn = (turn + 1)%4
            
            elif abilite['type'] == 'barriere' : 
                liste_barriere.append({'x': pyxel.mouse_x//16*16, 'y' : pyxel.mouse_y//16 * 16, 'tour_restant' : 5, 'type' : 'protection'})  
                abilite['recharge'] = 10 - abilite['boost']
                abilite['selection'] = False
                choix = True
                turn = (turn + 1)%4
    


    return liste_equipe, liste_abilite, position_a_jouer, position_valide, liste_prison, liste_barriere, choix, turn, liste_equipe_1, liste_equipe_2, liste_equipe_3

def abilite_update(liste_mur, liste_feu, liste_mine, liste_prison,liste_barriere, position_valide) :


    position_interdite = [(prison['x'], prison['y']) for prison in liste_prison] + [(barriere['x'], barriere['y']) for barriere in liste_barriere]

    for mur in liste_mur : 
        mur['tour_restant'] -= 1 
        if mur['tour_restant'] < 0 : 
            position_valide[(mur['x'], mur['y'])] = True
            liste_mur.remove(mur)
    
    for mine in liste_mine : 
        mine['tour_restant'] -= 1 
        if mine['tour_restant'] < 0 : 
            position_valide[(mine['x'], mine['y'])] = True
            liste_mine.remove(mine)
    
    for feu in liste_feu : 
        feu['tour_restant'] -= 1 
        if feu['tour_restant'] < 0 or (feu['x'], feu['y']) in position_interdite : 
            liste_feu.remove(feu)
    
    for prison in liste_prison : 
        prison['tour_restant'] -= 1 
        if prison['tour_restant'] < 0 or position_valide[(prison['x'], prison['y'])] : 
            position_valide[(prison['x'], prison['y'])] = True
            liste_prison.remove(prison)
    
    for barriere in liste_barriere : 
        barriere['tour_restant'] -= 1 
        if barriere['tour_restant'] < 0 or position_valide[(barriere['x'], barriere['y'])] : 
            position_valide[(barriere['x'], barriere['y'])] = True
            liste_barriere.remove(barriere)
    

    return liste_mur,liste_feu, liste_mine, liste_prison,liste_barriere, position_valide

def abilite_refresh(liste_abilite_1, liste_abilite_2, liste_abilite_3, liste_abilite_4) : 
    liste_abilite_1 = abilite_refresh_1(liste_abilite_1)
    liste_abilite_2 = abilite_refresh_1(liste_abilite_2)
    liste_abilite_3 = abilite_refresh_1(liste_abilite_3)
    liste_abilite_4 = abilite_refresh_1(liste_abilite_4)

    return liste_abilite_1, liste_abilite_2, liste_abilite_3, liste_abilite_4

def abilite_refresh_1(liste_abilite) : 
    for abilite in liste_abilite : 
        if abilite['recharge'] > 0 : 
            abilite['recharge'] -= 1 
    
    return liste_abilite

def equipe_actualise(liste_equipe_1, liste_equipe_2, liste_equipe_3, liste_equipe_4) :
    liste_equipe_1 = equipe_actualise_1(liste_equipe_1)
    liste_equipe_2 = equipe_actualise_1(liste_equipe_2)
    liste_equipe_3 = equipe_actualise_1(liste_equipe_3)
    liste_equipe_4 = equipe_actualise_1(liste_equipe_4)

    return liste_equipe_1,liste_equipe_2,liste_equipe_3,liste_equipe_4

def equipe_actualise_1(liste_equipe) :
    for piece in liste_equipe : 
        if piece['type'] == 'president' and piece['en_vie'] == False :
            liste_equipe.clear()
    return liste_equipe

def mine_update(liste_mine, liste_explosion, liste_equipe, liste_equipe_1, liste_equipe_2, liste_equipe_3) : 
    for mine in liste_mine : 

        for piece in liste_equipe : 
            if (piece['x'], piece['y']) == (mine['x'], mine['y']) : 
                liste_mine.remove(mine)
                liste_equipe.remove(piece)
                liste_explosion.append({'x' : mine['x'], 'y' : mine['y'], 'rayon' : 8, 'couleur' : 0})
        for piece in liste_equipe_1 : 
            if (piece['x'], piece['y']) == (mine['x'], mine['y']) : 
                liste_mine.remove(mine)
                liste_equipe_1.remove(piece)
                liste_explosion.append({'x' : mine['x'], 'y' : mine['y'], 'rayon' : 8, 'couleur' : 0})

        for piece in liste_equipe_2 : 
            if (piece['x'], piece['y']) == (mine['x'], mine['y']) : 
                liste_mine.remove(mine)
                liste_equipe_2.remove(piece)
                liste_explosion.append({'x' : mine['x'], 'y' : mine['y'], 'rayon' : 8, 'couleur' : 0})

        for piece in liste_equipe_3 : 
            if (piece['x'], piece['y']) == (mine['x'], mine['y']) : 
                liste_mine.remove(mine)
                liste_equipe_3.remove(piece)
                liste_explosion.append({'x' : mine['x'], 'y' : mine['y'], 'rayon' : 8, 'couleur' : 0})
    return liste_mine, liste_explosion, liste_equipe, liste_equipe_1, liste_equipe_2, liste_equipe_3

def win(liste_equipe, liste_equipe_1, liste_equipe_2, liste_equipe_3) : 
    rose = 0
    bleu = 0
    jaune = 0
    vert = 0
    
    if len(liste_equipe) == 0 :
        bleu += 1
        jaune += 1
        vert += 1
         
    if len(liste_equipe_1) == 0 : 
        rose += 1
        jaune += 1
        vert += 1
          
    if len(liste_equipe_2) == 0 : 
        rose += 1
        bleu += 1
        vert += 1
          
    if len(liste_equipe_3) == 0 : 
        rose += 1
        bleu += 1
        jaune += 1

    var_1 = max(rose, bleu, jaune, vert)

    if var_1 > 2 :
        if rose == var_1 :
            return 'Gagnant rose'
        if bleu == var_1 : 
            return 'Gagnant bleu'
        if jaune == var_1 :
            return 'Gagnant jaune'
        if vert == var_1 : 
            return 'Gagnant vert'
    else :
        return None

def choix_ministre(liste_abilite, choix_ab) :

    for abilite in liste_abilite : 
        if abilite['type'] == 'feu' and pyxel.mouse_x < 88 and pyxel.mouse_x > 12 and pyxel.mouse_y > 64 and pyxel.mouse_y < 192 and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) : 
            abilite['activation'] = True
            
            choix_ab = True 
        
        if abilite['type'] == 'barriere' and pyxel.mouse_x < 88 + 96 * 1 and pyxel.mouse_x > 12 + 96 * 1  and pyxel.mouse_y > 64 and pyxel.mouse_y < 192 and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) : 
            abilite['activation'] = True
            
            choix_ab = True 

        if abilite['type'] == 'prison' and pyxel.mouse_x < 88 + 96 * 2 and pyxel.mouse_x > 12 + 96 * 2 and pyxel.mouse_y > 64 and pyxel.mouse_y < 192 and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) : 
            abilite['activation'] = True
            
            choix_ab = True 

        if abilite['type'] == 'soin' and pyxel.mouse_x < 88 + 96 * 3 and pyxel.mouse_x > 12 + 96 * 3 and pyxel.mouse_y > 64 and pyxel.mouse_y < 192 and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) : 
            abilite['activation'] = True
            
            choix_ab = True 

    return liste_abilite , choix_ab

def feu_animation(liste_feu) : 
    for feu in liste_feu : 
        feu['frame'] = (feu['frame'] + 1)%7
    return liste_feu

def feu_update(liste_feu, position_valide, liste_equipe) : 
    for piece in liste_equipe : 
        for feu in liste_feu : 
            if (feu['x'], feu['y']) == (piece['x'], piece['y']) : 
                if piece['type'] != 'president' and not piece['barriere']  and not piece['en_prison']: 
                    liste_equipe.remove(piece)
                elif  not piece['barriere'] and not piece['en_prison'] : 
                    piece['en_vie'] = False
                position_valide[(piece['x'], piece['y'])] = True

    return liste_equipe, position_valide

def prison_update(liste_equipe, liste_equipe_1,liste_equipe_2, liste_equipe_3, liste_prison) :
    var_1 = []
    for prison in liste_prison : 
        var_1.append((prison['x'], prison['y']))
    
    liste_equipe = prison_update_1(liste_equipe, var_1) 
    liste_equipe_1 = prison_update_1(liste_equipe_1, var_1) 
    liste_equipe_2 = prison_update_1(liste_equipe_2, var_1) 
    liste_equipe_3 = prison_update_1(liste_equipe_3, var_1)

    return liste_equipe, liste_equipe_1, liste_equipe_2, liste_equipe_3 

def barriere_update(liste_equipe, liste_equipe_1,liste_equipe_2, liste_equipe_3, liste_barriere) : 
    var_1 = []
    for barriere in liste_barriere : 
        var_1.append((barriere['x'], barriere['y']))
    
    liste_equipe = barriere_update_1(liste_equipe, var_1) 
    liste_equipe_1 = barriere_update_1(liste_equipe_1, var_1) 
    liste_equipe_2 = barriere_update_1(liste_equipe_2, var_1) 
    liste_equipe_3 = barriere_update_1(liste_equipe_3, var_1)

    return liste_equipe, liste_equipe_1, liste_equipe_2, liste_equipe_3 

def prison_update_1(liste_equipe, liste_coord) :
    for piece in liste_equipe : 
        if (piece['x'], piece['y']) in liste_coord :
            piece['en_prison'] = True 
        else : 
            piece['en_prison'] = False
    return liste_equipe

def barriere_update_1(liste_equipe, liste_coord) :
    for piece in liste_equipe : 
        if (piece['x'], piece['y']) in liste_coord :
            piece['barriere'] = True 
        else : 
            piece['barriere'] = False
    return liste_equipe

def update_brison_barriere(liste_barriere, liste_prison, position_valide) : 
    for barriere in liste_barriere : 
        if position_valide[(barriere['x'], barriere['y'])] : 
            liste_barriere.remove(barriere)
    
    for prison in liste_prison : 
        if position_valide[(prison['x'], prison['y'])] : 
            liste_prison.remove(prison)
    
    return liste_barriere, liste_prison
        


def update():
    
    global selected_option, game, credit, frame_click, pacman_x, pacman_y, about, pieces, OX, pacman
    
    global position_jouable, choix, equipe_rose, equipe_bleu, equipe_jaune, equipe_vert, \
            tour, jou, frame_click, position_valide, position_a_jouer, turn, frame_piece, frame_abilite, abilite_rose, abilite_bleu, abilite_jaune, abilite_vert, \
            liste_feu,liste_mine,liste_mur, turn_1, tour_1, end, winner_1, temps, game_start, frame_tour, jouer, liste_explosion, choix_1, choix_2, choix_3, choix_4, couleur, frame_choix, liste_barriere, liste_prison


    if not game:
        
        if pyxel.frame_count % 5 == 0:
            direction = random.choice(["up", "down", "left", "right"])
            if direction == "up" and pacman_y > 0:
                pacman_y -= 10
                pacman = "up"
            elif direction == "down" and pacman_y < pyxel.height - 32:
                pacman_y += 10
                pacman = "down"
            elif direction == "left" and pacman_x > 0:
                pacman_x -= 10
                pacman = "left"
            elif direction == "right" and pacman_x < pyxel.width - 32:
                pacman_x += 10
                pacman = "right"

        if OX:
            update_OX()

        if credit:
            update_apple()
            if snake_game:
                update_snake()
        if breakout:
            update_breakout()

        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x >= pacman_x and pyxel.mouse_x <= pacman_x + 32 and pyxel.mouse_y >= pacman_y and pyxel.mouse_y <= pacman_y + 32:
            OX = True
            about = False
            pieces = False
            settings = False



        if not game_start :
            frame_tour = frame_tour + 1

    elif not end and game:

        

        if not game_start :

            liste_feu = feu_animation(liste_feu)

            if pyxel.btnp(pyxel.KEY_M) or (pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and (pyxel.mouse_x//16 * 16, pyxel.mouse_y //16 * 16) == (304, 240)) : 
                game = False



            for explosion in liste_explosion : 
                explosion['rayon'] -= 1
                if explosion['rayon'] < 0 : 
                    liste_explosion.remove(explosion)


            if jou[turn] == 'rose' and choix : 
                equipe_rose, choix, frame_piece, abilite_rose = selection_piece(equipe_rose, choix, frame_piece, abilite_rose, position_a_jouer)
                abilite_rose, choix, frame_abilite, equipe_rose = selection_abilite(abilite_rose, choix, frame_abilite, equipe_rose)
                
                equipe_rose, position_a_jouer, choix = piece_mouvement(equipe_rose, equipe_bleu, equipe_jaune, equipe_vert, position_a_jouer, position_jouable, position_valide, choix,liste_mine, abilite_rose)
                abilite_rose, position_a_jouer, choix = abilite_positions(equipe_rose, equipe_bleu, equipe_jaune, equipe_vert, abilite_rose, position_a_jouer, position_jouable, position_valide, choix, liste_mur, liste_mine, liste_prison)

            elif jou[turn] =='vert' and choix :
                equipe_vert, choix, frame_piece,abilite_vert = selection_piece(equipe_vert, choix, frame_piece, abilite_vert, position_a_jouer)
                abilite_vert, choix, frame_abilite, equipe_vert = selection_abilite(abilite_vert, choix, frame_abilite, equipe_vert)


                equipe_vert, position_a_jouer, choix = piece_mouvement(equipe_vert, equipe_bleu, equipe_jaune, equipe_rose, position_a_jouer, position_jouable, position_valide, choix,liste_mine, abilite_vert)
                abilite_vert, position_a_jouer, choix = abilite_positions(equipe_vert, equipe_bleu, equipe_jaune, equipe_rose, abilite_vert, position_a_jouer, position_jouable, position_valide, choix, liste_mur, liste_mine, liste_prison)

            elif jou[turn] =='jaune' and choix :
                equipe_jaune, choix, frame_piece,abilite_jaune = selection_piece(equipe_jaune, choix, frame_piece, abilite_jaune, position_a_jouer)
                abilite_jaune, choix, frame_abilite,equipe_jaune = selection_abilite(abilite_jaune, choix, frame_abilite, equipe_jaune)


                equipe_jaune, position_a_jouer, choix = piece_mouvement(equipe_jaune, equipe_bleu, equipe_vert, equipe_rose, position_a_jouer, position_jouable, position_valide, choix,liste_mine, abilite_jaune)
                abilite_jaune, position_a_jouer, choix = abilite_positions(equipe_jaune, equipe_bleu, equipe_vert, equipe_rose, abilite_jaune, position_a_jouer, position_jouable, position_valide, choix, liste_mur, liste_mine, liste_prison)

            elif jou[turn] =='bleu' and choix :
                equipe_bleu,choix, frame_piece,abilite_bleu = selection_piece(equipe_bleu, choix, frame_piece, abilite_bleu, position_a_jouer)
                abilite_bleu, choix, frame_abilite,equipe_bleu = selection_abilite(abilite_bleu, choix, frame_abilite, equipe_bleu)


                equipe_bleu, position_a_jouer, choix = piece_mouvement(equipe_bleu, equipe_jaune, equipe_vert, equipe_rose, position_a_jouer, position_jouable, position_valide, choix,liste_mine, abilite_bleu)
                abilite_bleu, position_a_jouer, choix = abilite_positions(equipe_bleu, equipe_jaune, equipe_vert, equipe_rose, abilite_bleu, position_a_jouer, position_jouable, position_valide, choix, liste_mur, liste_mine, liste_prison)



            if jou[turn] =='rose' and not(choix)  :
                equipe_rose, choix, frame_piece, abilite_rose = selection_piece(equipe_rose, choix, frame_piece, abilite_rose, position_a_jouer)
                abilite_rose, choix, frame_abilite, equipe_rose = selection_abilite(abilite_rose, choix, frame_abilite, equipe_rose)

                equipe_rose, equipe_bleu, equipe_jaune, equipe_vert, position_a_jouer, position_valide, choix, turn, abilite_rose = \
                piece_deplacement(equipe_rose, equipe_bleu, equipe_jaune, equipe_vert, position_a_jouer, position_valide, choix, turn, abilite_rose)

                equipe_rose, abilite_rose, position_a_jouer, position_valide, liste_mur, liste_feu, liste_mine, choix, turn, equipe_bleu, equipe_jaune, equipe_vert = \
                    abilite_action(equipe_rose, equipe_bleu, equipe_jaune, equipe_vert, abilite_rose, position_a_jouer, position_valide, liste_mur, liste_feu, liste_mine, choix, turn)

                equipe_rose, abilite_rose, position_a_jouer, position_valide, liste_prison , liste_barriere, choix, turn, equipe_bleu, equipe_jaune, equipe_vert = \
                    abilite_action_1(equipe_rose, equipe_bleu, equipe_jaune, equipe_vert, abilite_rose, position_a_jouer, position_valide, liste_prison , liste_barriere, choix, turn)
                jouer = True

            elif jou[turn] =='vert' and not(choix)  :
                equipe_vert, choix, frame_piece,abilite_vert = selection_piece(equipe_vert, choix, frame_piece, abilite_vert, position_a_jouer)
                abilite_vert, choix, frame_abilite, equipe_vert = selection_abilite(abilite_vert, choix, frame_abilite, equipe_vert)

                equipe_vert, equipe_bleu, equipe_jaune, equipe_rose, position_a_jouer, position_valide, choix, turn, abilite_vert = \
                piece_deplacement(equipe_vert, equipe_bleu, equipe_jaune, equipe_rose, position_a_jouer, position_valide, choix, turn, abilite_vert)
                
                equipe_vert, abilite_vert, position_a_jouer, position_valide, liste_mur, liste_feu, liste_mine, choix, turn, equipe_bleu, equipe_jaune, equipe_rose = \
                    abilite_action(equipe_vert, equipe_bleu, equipe_jaune, equipe_rose, abilite_vert, position_a_jouer, position_valide, liste_mur, liste_feu, liste_mine, choix, turn)

                equipe_vert, abilite_vert, position_a_jouer, position_valide, liste_prison , liste_barriere, choix, turn, equipe_bleu, equipe_jaune, equipe_rose = \
                    abilite_action_1(equipe_vert, equipe_bleu, equipe_jaune, equipe_rose, abilite_vert, position_a_jouer, position_valide, liste_prison , liste_barriere, choix, turn)

                jouer = True

            elif jou[turn] =='jaune' and not(choix)  :
                equipe_jaune, choix, frame_piece,abilite_jaune = selection_piece(equipe_jaune, choix, frame_piece,abilite_jaune, position_a_jouer)
                abilite_jaune, choix, frame_abilite,equipe_jaune = selection_abilite(abilite_jaune, choix, frame_abilite, equipe_jaune)

                equipe_jaune, equipe_bleu, equipe_vert, equipe_rose, position_a_jouer, position_valide, choix, turn, abilite_jaune = \
                piece_deplacement(equipe_jaune, equipe_bleu, equipe_vert, equipe_rose, position_a_jouer, position_valide, choix, turn, abilite_jaune)

                equipe_jaune, abilite_jaune, position_a_jouer, position_valide, liste_mur, liste_feu, liste_mine, choix, turn, equipe_bleu, equipe_vert, equipe_rose = \
                    abilite_action(equipe_jaune, equipe_bleu, equipe_vert, equipe_rose, abilite_jaune, position_a_jouer, position_valide, liste_mur, liste_feu, liste_mine, choix, turn)

                equipe_jaune, abilite_jaune, position_a_jouer, position_valide, liste_prison , liste_barriere, choix, turn, equipe_bleu, equipe_vert, equipe_rose = \
                    abilite_action_1(equipe_jaune, equipe_bleu, equipe_vert, equipe_rose, abilite_jaune, position_a_jouer, position_valide, liste_prison , liste_barriere, choix, turn)

                jouer = True

            elif jou[turn] =='bleu' and not(choix)  :
                equipe_bleu,choix, frame_piece,abilite_bleu = selection_piece(equipe_bleu, choix, frame_piece,abilite_bleu, position_a_jouer)
                abilite_bleu, choix, frame_abilite,equipe_bleu = selection_abilite(abilite_bleu, choix, frame_abilite, equipe_bleu)

                equipe_bleu, equipe_vert, equipe_jaune, equipe_rose, position_a_jouer, position_valide, choix, turn, abilite_bleu = \
                piece_deplacement(equipe_bleu, equipe_vert, equipe_jaune, equipe_rose, position_a_jouer, position_valide, choix, turn, abilite_bleu)

                equipe_bleu, abilite_bleu, position_a_jouer, position_valide, liste_mur, liste_feu, liste_mine, choix, turn,equipe_jaune ,equipe_vert , equipe_rose = \
                    abilite_action(equipe_bleu, equipe_jaune, equipe_vert, equipe_rose, abilite_bleu, position_a_jouer, position_valide, liste_mur, liste_feu, liste_mine, choix, turn)

                equipe_bleu, abilite_bleu, position_a_jouer, position_valide, liste_prison , liste_barriere, choix, turn, equipe_jaune ,equipe_vert , equipe_rose = \
                    abilite_action_1(equipe_bleu, equipe_jaune, equipe_vert, equipe_rose, abilite_bleu, position_a_jouer, position_valide, liste_prison , liste_barriere, choix, turn)
                
                jouer = True

            
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and (pyxel.mouse_x//16 * 16, pyxel.mouse_y//16 * 16) in [(256, 240), (272, 240), (288, 240)] or pyxel.frame_count - frame_tour == temps*30 : 
                if jou[turn] == 'rose' : 
                    equipe_rose.clear()
                if jou[turn] == 'bleu' : 
                    equipe_bleu.clear()
                if jou[turn] == 'jaune' : 
                    equipe_jaune.clear()
                if jou[turn] == 'vert' :
                    equipe_vert.clear()
                
                choix = True
                position_a_jouer.clear()
                turn = (turn+1)%4
                jouer = True

            if turn_1 != jou[turn] : 

                if jouer : 
                    tour += 1 
                    jouer = False

                if tour_1 != tour : 

                    liste_mur, liste_feu, liste_mine, liste_prison,liste_barriere, position_valide  = abilite_update(liste_mur, liste_feu, liste_mine, liste_prison,liste_barriere, position_valide) 
                    abilite_rose, abilite_bleu, abilite_jaune, abilite_vert = abilite_refresh(abilite_rose, abilite_bleu, abilite_jaune, abilite_vert)
                    

                    tour_1 = tour

                if len(position_a_jouer) > 0 and position_a_jouer[-1] == 'explosion' : 
                    liste_explosion.append({'x' : pyxel.mouse_x//16 * 16, 'y' : pyxel.mouse_y//16 * 16, 'rayon' : 8, 'couleur' : 1})
                    liste_explosion.append({'x' : pyxel.mouse_x//16 * 16, 'y' : pyxel.mouse_y//16 * 16, 'rayon' : 8, 'couleur' : 1})
                    position_a_jouer.clear()
                    
                
                liste_mine, liste_explosion, equipe_rose, equipe_bleu, equipe_jaune, equipe_vert = mine_update(liste_mine, liste_explosion, equipe_rose, equipe_bleu, equipe_jaune, equipe_vert)

                equipe_rose, equipe_bleu, equipe_jaune, equipe_vert = prison_update(equipe_rose, equipe_bleu, equipe_jaune, equipe_vert, liste_prison)

                equipe_rose, equipe_bleu, equipe_jaune, equipe_vert = barriere_update(equipe_rose, equipe_bleu, equipe_jaune, equipe_vert, liste_barriere)


                if turn_1 == 'rose'  : 
                    equipe_rose, position_valide = feu_update(liste_feu, position_valide, equipe_rose) 
                    
                if turn_1 == 'bleu' : 
                    equipe_bleu, position_valide = feu_update(liste_feu, position_valide, equipe_bleu) 
                    
                if turn_1 == 'jaune'  : 
                    equipe_jaune, position_valide = feu_update(liste_feu, position_valide, equipe_jaune) 
                    
                if turn_1 == 'vert' : 
                    equipe_vert, position_valide = feu_update(liste_feu, position_valide, equipe_vert) 
                

                for piece in equipe_rose :
                    if piece['type'] == 'citoyen' and piece['x'] == 0 :
                        piece['type'] = 'ouvrier'

                for piece in equipe_bleu :
                    if piece['type'] == 'citoyen' and piece['y'] == 0 :
                        piece['type'] = 'ouvrier'

                for piece in equipe_jaune :
                    if piece['type'] == 'citoyen' and piece['x'] == 240 :
                        piece['type'] = 'ouvrier'

                for piece in equipe_vert :
                    if piece['type'] == 'citoyen' and piece['y'] == 240 :
                        piece['type'] = 'ouvrier'

                equipe_rose, equipe_bleu, equipe_jaune, equipe_vert = equipe_actualise(equipe_rose, equipe_bleu, equipe_jaune, equipe_vert)

                liste_barriere, liste_prison = update_brison_barriere(liste_barriere, liste_prison, position_valide)

                position_valide = board_update(position_valide, equipe_rose, equipe_bleu, equipe_jaune, equipe_vert, liste_mur, liste_mine)

                if jou[turn] == 'rose' and len(equipe_rose) < 1 : 
                    turn = (turn+1)%4
                    
                if jou[turn] == 'bleu' and len(equipe_bleu) < 1 : 
                    turn = (turn+1)%4
                    
                if jou[turn] == 'jaune' and len(equipe_jaune) < 1 : 
                    turn = (turn+1)%4
                    
                if jou[turn] == 'vert' and len(equipe_vert) < 1 : 
                    turn = (turn+1)%4
                    
    
                winner_1 = win(equipe_rose, equipe_bleu, equipe_jaune, equipe_vert)
                if winner_1 != None :
                    
                    end = True

                frame_tour = pyxel.frame_count
                turn_1 = jou[turn]
        
        else : 
            
            if temps == None :
                if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x >= 32 and pyxel.mouse_y >= 64 and pyxel.mouse_x <=96 and pyxel.mouse_y <= 192 :
                    temps = 120
                    frame_choix = pyxel.frame_count
                    
                    
                if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x >= 160 and pyxel.mouse_y >= 64 and pyxel.mouse_x <=224 and pyxel.mouse_y <= 192 :
                    temps = 30
                    frame_choix = pyxel.frame_count
                    

                if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x >= 288 and pyxel.mouse_y >= 64 and pyxel.mouse_x <=352 and pyxel.mouse_y <= 192 :
                    temps = 9
                    frame_choix = pyxel.frame_count
                
            
            if temps != None : 
                
                if not choix_1 and pyxel.frame_count != frame_choix : 
                    abilite_rose, choix_1 =  choix_ministre(abilite_rose, choix_1)
                    frame_choix = pyxel.frame_count
                
                elif choix_1 and not choix_2  and pyxel.frame_count != frame_choix : 
                    abilite_bleu, choix_2 =  choix_ministre(abilite_bleu, choix_2)
                    frame_choix = pyxel.frame_count

                elif choix_1 and  choix_2 and not choix_3  and pyxel.frame_count != frame_choix : 
                    abilite_jaune, choix_3 =  choix_ministre(abilite_jaune, choix_3)
                    frame_choix = pyxel.frame_count
                    
                elif choix_1 and  choix_2 and  choix_3 and not choix_4  and pyxel.frame_count != frame_choix : 
                    abilite_vert, choix_4 =  choix_ministre(abilite_vert, choix_4)
                    frame_choix = pyxel.frame_count

                elif choix_1 and choix_2 and choix_3 and choix_4 : 
                    frame_tour = pyxel.frame_count
                    game_start = False              

    else : 

       

        if pyxel.btnp(pyxel.KEY_M) or ((pyxel.mouse_x//16 * 16, pyxel.mouse_y//16 * 16) == (64, 112) and pyxel.btnp (pyxel.MOUSE_BUTTON_LEFT)) : 

            #recommencer la partie
            
            game = False
            end = False
            game_start = True
            temps = None
            equipe_rose.clear()
            equipe_bleu.clear()
            equipe_jaune.clear()
            equipe_vert.clear()
            abilite_rose.clear()
            abilite_bleu.clear()
            abilite_vert.clear()
            abilite_jaune.clear()
            abilite_vert.clear()
            position_a_jouer.clear()
            liste_explosion.clear()

            equipe_bleu =   [{'tag': 'piece', 'type' : 'citoyen', 'zombie' : False,'equipe' : 'bleu', 'en_vie' : True, 'en_mouvement' : False, 'x' : x , 'y' : 224 , '1er_tour' : True, 'barriere' : False, 'controle' : False, 'en_prison' : False } for x in range(64, 177, 16)]  +\
                            [{'tag': 'piece', 'type' : 'ouvrier','equipe' : 'rose', 'en_vie' : True, 'en_mouvement' : False, 'x' : 160, 'y' : 240 , '1er_tour' : True, 'barriere' : False, 'controle' : False, 'en_prison' : False },\
                            {'tag': 'piece', 'type' : 'ouvrier','equipe' : 'rose', 'en_vie' : True, 'en_mouvement' : False, 'x' : 80, 'y' : 240 , '1er_tour' : True, 'barriere' : False, 'controle' : False, 'en_prison' : False }] +\
                            [{'tag': 'piece', 'type' : 'soldat','equipe' : 'rose', 'en_vie' : True, 'en_mouvement' : False, 'x' : 176, 'y' : 240 , '1er_tour' : True, 'barriere' : False, 'controle' : False, 'en_prison' : False },\
                            {'tag': 'piece', 'type' : 'soldat','equipe' : 'rose', 'en_vie' : True, 'en_mouvement' : False, 'x' : 64, 'y' : 240 , '1er_tour' : True, 'barriere' : False, 'controle' : False, 'en_prison' : False }] + \
                            [{'tag': 'piece', 'type' : 'president', 'equipe' : 'bleu', 'en_vie' : True, 'en_mouvement' : False, 'x' : 112, 'y' : 240 , '1er_tour' : True, 'barriere' : False, 'controle' : False, 'en_prison' : False }]+\
                            [{'tag': 'piece', 'type' : 'ministre', 'equipe' : 'bleu', 'en_vie' : True, 'en_mouvement' : False, 'x' : 128, 'y' : 240 , '1er_tour' : True, 'barriere' : False, 'controle' : False, 'en_prison' : False }] +\
                            [{'tag': 'piece', 'type' : 'pirate', 'equipe' : 'bleu', 'en_vie' : True, 'en_mouvement' : False, 'x' : 144, 'y' : 240 , '1er_tour' : True, 'barriere' : False, 'controle' : False, 'en_prison' : False }] +\
                            [{'tag': 'piece', 'type' : 'pirate', 'equipe' : 'bleu', 'en_vie' : True, 'en_mouvement' : False, 'x' : 96, 'y' : 240 , '1er_tour' : True, 'barriere' : False, 'controle' : False, 'en_prison' : False }]

            equipe_jaune =  [{'tag': 'piece', 'type' : 'citoyen', 'zombie' : False,'equipe' : 'jaune', 'en_vie' : True, 'en_mouvement' : False, 'x' : 16 , 'y' : y , '1er_tour' : True, 'barriere' : False, 'controle' : False, 'en_prison' : False } for y in range(64, 177, 16)] + \
                            [{'tag': 'piece', 'type' : 'ouvrier','equipe' : 'rose', 'en_vie' : True, 'en_mouvement' : False, 'x' : 0, 'y' : 80 , '1er_tour' : True, 'barriere' : False, 'controle' : False, 'en_prison' : False }, \
                            {'tag': 'piece', 'type' : 'ouvrier','equipe' : 'rose', 'en_vie' : True, 'en_mouvement' : False, 'x' : 0, 'y' : 160 , '1er_tour' : True, 'barriere' : False, 'controle' : False, 'en_prison' : False }] + \
                            [{'tag': 'piece', 'type' : 'soldat','equipe' : 'rose', 'en_vie' : True, 'en_mouvement' : False, 'x' : 0, 'y' : 176 , '1er_tour' : True, 'barriere' : False, 'controle' : False, 'en_prison' : False }, \
                            {'tag': 'piece', 'type' : 'soldat', 'equipe' : 'rose', 'en_vie' : True, 'en_mouvement' : False, 'x' : 0, 'y' : 64 , '1er_tour' : True, 'barriere' : False, 'controle' : False, 'en_prison' : False }] + \
                            [{'tag': 'piece', 'type' : 'president', 'equipe' : 'jaune', 'en_vie' : True, 'en_mouvement' : False, 'x' : 0, 'y' : 128 , '1er_tour' : True, 'barriere' : False, 'controle' : False, 'en_prison' : False }] +\
                            [{'tag': 'piece', 'type' : 'ministre', 'equipe' : 'jaune', 'en_vie' : True, 'en_mouvement' : False, 'x' : 0, 'y' : 112 , '1er_tour' : True, 'barriere' : False, 'controle' : False, 'en_prison' : False }]+\
                            [{'tag': 'piece', 'type' : 'pirate', 'equipe' : 'jaune', 'en_vie' : True, 'en_mouvement' : False, 'x' : 0, 'y' : 144 , '1er_tour' : True, 'barriere' : False, 'controle' : False, 'en_prison' : False }] +\
                            [{'tag': 'piece', 'type' : 'pirate', 'equipe' : 'jaune', 'en_vie' : True, 'en_mouvement' : False, 'x' : 0, 'y' : 96 , '1er_tour' : True, 'barriere' : False, 'controle' : False, 'en_prison' : False }]

            equipe_vert =   [{'tag': 'piece', 'type' : 'citoyen', 'zombie' : False,'equipe' : 'vert', 'en_vie' : True,'en_mouvement' : False, 'x' : x , 'y' : 16 , '1er_tour' : True, 'barriere' : False, 'controle' : False, 'en_prison' : False } for x in range(64, 177, 16)] + \
                            [{'tag': 'piece', 'type' : 'ouvrier','equipe' : 'rose', 'en_vie' : True,'en_mouvement' : False, 'x' : 80, 'y' : 0 , '1er_tour' : True, 'barriere' : False, 'controle' : False, 'en_prison' : False },\
                            {'tag': 'piece', 'type' : 'ouvrier','equipe' : 'rose', 'en_vie' : True, 'en_mouvement' : False, 'x' : 160, 'y' : 0 , '1er_tour' : True, 'barriere' : False, 'controle' : False, 'en_prison' : False }] +\
                            [{'tag': 'piece', 'type' : 'soldat', 'equipe' : 'rose', 'en_vie' : True, 'en_mouvement' : False, 'x' : 64, 'y' : 0 , '1er_tour' : True, 'barriere' : False, 'controle' : False, 'en_prison' : False },\
                            {'tag': 'piece', 'type' : 'soldat', 'equipe' : 'rose', 'en_vie' : True, 'en_mouvement' : False, 'x' : 176, 'y' : 0 , '1er_tour' : True, 'barriere' : False, 'controle' : False, 'en_prison' : False }] + \
                            [{'tag': 'piece', 'type' : 'president', 'equipe' : 'vert', 'en_vie' : True, 'en_mouvement' : False, 'x' : 128, 'y' : 0 , '1er_tour' : True, 'barriere' : False, 'controle' : False, 'en_prison' : False }] +\
                            [{'tag': 'piece', 'type' : 'ministre', 'equipe' : 'vert', 'en_vie' : True, 'en_mouvement' : False, 'x' : 112, 'y' : 0 , '1er_tour' : True, 'barriere' : False, 'controle' : False, 'en_prison' : False }]+\
                            [{'tag': 'piece', 'type' : 'pirate', 'equipe' : 'vert', 'en_vie' : True, 'en_mouvement' : False, 'x' : 144, 'y' : 0 , '1er_tour' : True, 'barriere' : False, 'controle' : False, 'en_prison' : False }] +\
                            [{'tag': 'piece', 'type' : 'pirate', 'equipe' : 'vert', 'en_vie' : True, 'en_mouvement' : False, 'x' : 96, 'y' : 0 , '1er_tour' : True, 'barriere' : False, 'controle' : False, 'en_prison' : False }]

            equipe_rose =   [{'tag': 'piece', 'type' : 'citoyen', 'zombie' : False,'equipe' : 'rose', 'en_vie' : True,'en_mouvement' : False, 'x' : 224, 'y' : y , '1er_tour' : True, 'barriere' : False, 'controle' : False, 'en_prison' : False } for y in range(64, 177, 16)] + \
                            [{'tag': 'piece', 'type' : 'ouvrier','equipe' : 'rose', 'en_vie' : True, 'en_mouvement' : False, 'x' : 240, 'y' : 80 , '1er_tour' : True, 'barriere' : False, 'controle' : False, 'en_prison' : False },\
                            {'tag': 'piece', 'type' : 'ouvrier','equipe' : 'rose', 'en_vie' : True,'en_mouvement' : False, 'x' : 240, 'y' : 160 , '1er_tour' : True, 'barriere' : False, 'controle' : False, 'en_prison' : False }] + \
                            [{'tag': 'piece', 'type' : 'soldat', 'equipe' : 'rose', 'en_vie' : True, 'en_mouvement' : False, 'x' : 240, 'y' : 176 , '1er_tour' : True, 'barriere' : False, 'controle' : False, 'en_prison' : False },\
                            {'tag': 'piece', 'type' : 'soldat','equipe' : 'rose', 'en_vie' : True, 'en_mouvement' : False, 'x' : 240, 'y' : 64 , '1er_tour' : True, 'barriere' : False, 'controle' : False, 'en_prison' : False }] + \
                            [{'tag': 'piece', 'type' : 'president', 'equipe' : 'rose', 'en_vie' : True, 'en_mouvement' : False, 'x' : 240, 'y' : 112 , '1er_tour' : True, 'barriere' : False, 'controle' : False, 'en_prison' : False }] +\
                            [{'tag': 'piece', 'type' : 'ministre', 'equipe' : 'rose', 'en_vie' : True, 'en_mouvement' : False, 'x' : 240, 'y' : 128 , '1er_tour' : True, 'barriere' : False, 'controle' : False, 'en_prison' : False }] +\
                            [{'tag': 'piece', 'type' : 'pirate', 'equipe' : 'rose', 'en_vie' : True, 'en_mouvement' : False, 'x' : 240, 'y' : 144 , '1er_tour' : True, 'barriere' : False, 'controle' : False, 'en_prison' : False }] +\
                            [{'tag': 'piece', 'type' : 'pirate', 'equipe' : 'rose', 'en_vie' : True, 'en_mouvement' : False, 'x' : 240, 'y' : 96 , '1er_tour' : True, 'barriere' : False, 'controle' : False, 'en_prison' : False }]

            abilite_rose =  [{'tag' : 'abilite', 'equipe' : 'rose', 'type' : 'mur', 'x' : 192, 'y': 192, 'selection' : False, 'recharge' : 0, 'activation' : True, 'boost' : 0}] +\
                            [{'tag' : 'abilite', 'equipe' : 'rose', 'type' : 'mine', 'x' : 208, 'y': 192, 'selection' : False, 'recharge' : 0, 'activation' : True, 'boost' : 0}] +\
                            [{'tag' : 'abilite', 'equipe' : 'rose', 'type' : 'piratage', 'x' : 224, 'y': 192, 'selection' : False, 'recharge' : 0, 'activation' : True, 'boost' : 0}]+\
                            [{'tag' : 'abilite', 'equipe' : 'rose', 'type' : 'bombe', 'x' : 240, 'y': 192, 'selection' : False, 'recharge' : 0, 'activation' : False, 'boost' : 0}]+\
                            [{'tag' : 'abilite', 'equipe' : 'rose', 'type' : 'feu', 'x' : 192, 'y': 224, 'selection' : False, 'recharge' : 0, 'activation' : False, 'boost' : 0}]+\
                            [{'tag' : 'abilite', 'equipe' : 'rose', 'type' : 'barriere', 'x' : 208, 'y': 224, 'selection' : False, 'recharge' : 0, 'activation' : False, 'boost' : 0}]+\
                            [{'tag' : 'abilite', 'equipe' : 'rose', 'type' : 'prison', 'x' : 224, 'y': 224, 'selection' : False, 'recharge' : 0, 'activation' : False, 'boost' : 0}]+\
                            [{'tag' : 'abilite', 'equipe' : 'rose', 'type' : 'soin', 'x' : 240, 'y': 224, 'selection' : False, 'recharge' : 0, 'activation' : False, 'boost' : 0}]+\
                            [{'tag' : 'abilite', 'equipe' : 'rose', 'type' : 'teleportation', 'x' : 192, 'y': 208, 'selection' : False, 'recharge' : 0, 'activation' : True, 'boost' : 0}]

            abilite_bleu =  [{'tag' : 'abilite', 'equipe' : 'bleu', 'type' : 'mur', 'x' : 0, 'y': 192, 'selection' : False, 'recharge' : 0, 'activation' : True, 'boost' : 0}]+\
                            [{'tag' : 'abilite', 'equipe' : 'bleu', 'type' : 'mine', 'x' : 16, 'y': 192, 'selection' : False, 'recharge' : 0, 'activation' : True, 'boost' : 0}]+\
                            [{'tag' : 'abilite', 'equipe' : 'bleu', 'type' : 'piratage', 'x' : 32, 'y': 192, 'selection' : False, 'recharge' : 0, 'activation' : True, 'boost' : 0}]+\
                            [{'tag' : 'abilite', 'equipe' : 'bleu', 'type' : 'bombe', 'x' : 48, 'y': 192, 'selection' : False, 'recharge' : 0, 'activation' : False, 'boost' : 0}]+\
                            [{'tag' : 'abilite', 'equipe' : 'bleu', 'type' : 'feu', 'x' : 0, 'y': 224, 'selection' : False, 'recharge' : 0, 'activation' : False, 'boost' : 0}]+\
                            [{'tag' : 'abilite', 'equipe' : 'bleu', 'type' : 'barriere', 'x' : 16, 'y': 224, 'selection' : False, 'recharge' : 0, 'activation' : False, 'boost' : 0}]+\
                            [{'tag' : 'abilite', 'equipe' : 'bleu', 'type' : 'prison', 'x' : 32, 'y': 224, 'selection' : False, 'recharge' : 0, 'activation' : False, 'boost' : 0}]+\
                            [{'tag' : 'abilite', 'equipe' : 'bleu', 'type' : 'soin', 'x' : 48, 'y': 224, 'selection' : False, 'recharge' : 0, 'activation' : False, 'boost' : 0}]+\
                            [{'tag' : 'abilite', 'equipe' : 'bleu', 'type' : 'teleportation', 'x' : 0, 'y': 208, 'selection' : False, 'recharge' : 0, 'activation' : True, 'boost' : 0}]

            abilite_jaune = [{'tag' : 'abilite', 'equipe' : 'jaune', 'type' : 'mur', 'x' : 0, 'y': 0, 'selection' : False, 'recharge' : 0, 'activation' : True, 'boost' : 0}]+\
                            [{'tag' : 'abilite', 'equipe' : 'jaune', 'type' : 'mine', 'x' : 16, 'y': 0, 'selection' : False, 'recharge' : 0, 'activation' : True, 'boost' : 0}]+\
                            [{'tag' : 'abilite', 'equipe' : 'jaune', 'type' : 'piratage', 'x' : 32, 'y': 0, 'selection' : False, 'recharge' : 0, 'activation' : True, 'boost' : 0}]+\
                            [{'tag' : 'abilite', 'equipe' : 'jaune', 'type' : 'bombe', 'x' : 48, 'y': 0, 'selection' : False, 'recharge' : 0, 'activation' : False, 'boost' : 0}]+\
                            [{'tag' : 'abilite', 'equipe' : 'jaune', 'type' : 'feu', 'x' : 0, 'y': 32, 'selection' : False, 'recharge' : 0, 'activation' : False, 'boost' : 0}]+\
                            [{'tag' : 'abilite', 'equipe' : 'jaune', 'type' : 'barriere', 'x' : 16, 'y': 32, 'selection' : False, 'recharge' : 0, 'activation' : False, 'boost' : 0}]+\
                            [{'tag' : 'abilite', 'equipe' : 'jaune', 'type' : 'prison', 'x' : 32, 'y': 32, 'selection' : False, 'recharge' : 0, 'activation' : False, 'boost' : 0}]+\
                            [{'tag' : 'abilite', 'equipe' : 'jaune', 'type' : 'soin', 'x' : 48, 'y': 32, 'selection' : False, 'recharge' : 0, 'activation' : False, 'boost' : 0}]+\
                            [{'tag' : 'abilite', 'equipe' : 'jaune', 'type' : 'teleportation', 'x' : 0, 'y': 16, 'selection' : False, 'recharge' : 0, 'activation' : True, 'boost' : 0}]

            abilite_vert =  [{'tag' : 'abilite', 'equipe' : 'vert', 'type' : 'mur', 'x' : 192, 'y': 0, 'selection' : False, 'recharge' : 0, 'activation' : True, 'boost' : 0}]+\
                            [{'tag' : 'abilite', 'equipe' : 'vert', 'type' : 'mine', 'x' : 208, 'y': 0, 'selection' : False, 'recharge' : 0, 'activation' : True, 'boost' : 0}]+\
                            [{'tag' : 'abilite', 'equipe' : 'vert', 'type' : 'piratage', 'x' : 224, 'y': 0, 'selection' : False, 'recharge' : 0, 'activation' : True, 'boost' : 0}]+\
                            [{'tag' : 'abilite', 'equipe' : 'vert', 'type' : 'bombe', 'x' : 240, 'y': 0, 'selection' : False, 'recharge' : 0, 'activation' : False, 'boost' : 0}]+\
                            [{'tag' : 'abilite', 'equipe' : 'vert', 'type' : 'feu', 'x' : 192, 'y': 32, 'selection' : False, 'recharge' : 0, 'activation' : False, 'boost' : 0}]+\
                            [{'tag' : 'abilite', 'equipe' : 'vert', 'type' : 'barriere', 'x' : 208, 'y': 32, 'selection' : False, 'recharge' : 0, 'activation' : False, 'boost' : 0}]+\
                            [{'tag' : 'abilite', 'equipe' : 'vert', 'type' : 'prison', 'x' : 224, 'y': 32, 'selection' : False, 'recharge' : 0, 'activation' : False, 'boost' : 0}]+\
                            [{'tag' : 'abilite', 'equipe' : 'vert', 'type' : 'soin', 'x' : 240, 'y': 32, 'selection' : False, 'recharge' : 0, 'activation' : False, 'boost' : 0}]+\
                            [{'tag' : 'abilite', 'equipe' : 'vert', 'type' : 'teleportation', 'x' : 192, 'y': 16, 'selection' : False, 'recharge' : 0, 'activation' : True, 'boost' : 0}]

            liste_mur.clear()

            liste_feu.clear()

            liste_prison.clear()

            liste_mine.clear()

            liste_barriere.clear()

            liste_explosion.clear()


            choix = True
            winner_1 = None
            game_start = True
            jouer = False
            choix_1 = False
            choix_2 = False
            choix_3 = False
            choix_4 = False
            couleur = 8 


            jou = ['rose', 'bleu', 'jaune', 'vert']
            turn = random.randint(0 , 3)
            frame_piece = pyxel.frame_count
            frame_abilite = pyxel.frame_count
            temps = None
            frame_tour = pyxel.frame_count
            frame_choix = pyxel.frame_count

            turn_1 = jou[turn]
            end = False

            tour = 0
            tour_1 = tour
            position_valide = board_update(position_valide, equipe_rose, equipe_bleu, equipe_jaune, equipe_vert, liste_mur, liste_mine)

    
                

def draw() :
    global about, pacman_x, pacman_y
    pyxel.cls(0)

    if not game:
        

        if not credit and not about and not OX:
            pyxel.bltm(0, 0, 0, 0, 384, 384, 256)
        start_game_draw()
        if OX:
            draw_OX()
        elif snake_game:
            draw_snake_game()
        
        # dessiner le pacman
        if not OX and not credit and not snake_game and not r1 and not about and not ability and not pieces and not breakout:
            image_index = (pyxel.frame_count // 8) % 3
            if pacman == "right":
                pyxel.blt(pacman_x, pacman_y, 0, 0, 96 + image_index * 32, 32, 32, 0)
            elif pacman == "left":
                pyxel.blt(pacman_x, pacman_y, 0, 32, 96 + image_index * 32, 32, 32, 0)
            elif pacman == "down":
                pyxel.blt(pacman_x, pacman_y, 0, 64, 96 + image_index * 32, 32, 32, 0)
            elif pacman == "up":
                pyxel.blt(pacman_x, pacman_y, 0, 96, 96 + image_index * 32, 32, 32, 0)
    
    elif game and not end:
        if not game_start : 
            pyxel.bltm(0, 0, 0, 0, 0, 256, 257)

            if pyxel.mouse_x < 256 : 
                pyxel.rect(pyxel.mouse_x//16 * 16, pyxel.mouse_y//16 * 16, 16, 16, 13)
                    
            for tab in position_jouable : 
                if position_valide[tab] :
                    pyxel.rect(tab[0] , tab[1], 2, 2, 3)
                else : 
                    pyxel.rect(tab[0] , tab[1], 2, 2, 8)

            for coord in position_a_jouer : 
                pyxel.rect(coord[0] + 1, coord[1] + 1 , 14, 14, 13)

            for mine in liste_mine : 
                pyxel.blt(mine['x'], mine['y'], 0, 16 ,80 ,16, 16, 0)
                pyxel.text(mine['x'] + 8 , mine['y'] + 4, str(mine['tour_restant']) , 2)

            for tombe in equipe_rose : 
                if not tombe['en_vie']  : 
                    if tombe['type'] == 'soldat' : 
                        pyxel.blt(tombe['x'], tombe['y'], 0, 0, 32, 16, 16, 0)
                    if tombe['type'] == 'pirate' :
                        pyxel.blt(tombe['x'], tombe['y'], 0, 224, 32, 16, 16, 4)
            for tombe in equipe_vert :
                if not tombe['en_vie']  : 

                    if tombe['type'] == 'soldat' : 
                        pyxel.blt(tombe['x'], tombe['y'], 0, 208, 16, 16, 16, 0)
                    if tombe['type'] == 'pirate' :
                        pyxel.blt(tombe['x'], tombe['y'], 0, 224, 16, 16, 16, 4)           
            for tombe in equipe_jaune :
                if not tombe['en_vie']  : 
                    if tombe['type'] == 'soldat' : 
                        pyxel.blt(tombe['x'], tombe['y'], 0, 208, 0, 16, 16, 4)
                    if tombe['type'] == 'pirate' :
                        pyxel.blt(tombe['x'], tombe['y'], 0, 224, 0, 16, 16, 4)           
            for tombe in equipe_bleu :
                    if not tombe['en_vie']  :

                        if tombe['type'] == 'soldat' : 
                            pyxel.blt(tombe['x'], tombe['y'], 0, 208, 48 , 16, 16, 4)
                        if tombe['type'] == 'pirate' :
                            pyxel.blt(tombe['x'], tombe['y'], 0, 224, 48, 16, 16, 4)

                    
            for piece in equipe_rose : 

                if piece['en_vie'] and (piece['en_mouvement']) : 
                    
                    pyxel.rect(piece['x'], piece['y'], 16, 16, 13)
                    
                if piece['en_vie'] : 
                    
                    if piece['type'] == 'citoyen' : 

                        if piece['zombie'] : 
                            pyxel.blt(piece['x'], piece['y'], 0, 144, 32, 16, 16, 4 )
                        else : 
                            pyxel.blt(piece['x'], piece['y'], 0, 64, 32, 16, 16, 4 )

                    if piece['type'] == 'ouvrier' : 
                        pyxel.blt(piece['x'], piece['y'], 0, 80, 32, 16, 16, 4 )

                    if piece['type'] == 'soldat' : 
                        pyxel.blt(piece['x'], piece['y'], 0, 32, 32, 16, 16, 4 )

                    if piece['type'] == 'president' : 
                        pyxel.blt(piece['x'], piece['y'], 0, 0, 32, 16, 16, 4 )
                    
                    if piece['type'] == 'ministre' :
                        pyxel.blt(piece['x'], piece['y'], 0, 48, 32, 16, 16, 4 )
                    
                    if piece['type'] == 'pirate' :
                        pyxel.blt(piece['x'], piece['y'], 0, 16, 32, 16, 16, 4 )
                        
            for piece in equipe_vert : 

                if piece['en_vie'] and (piece['en_mouvement']) : 
                    
                    pyxel.rect(piece['x'], piece['y'], 16, 16, 13)

                if piece['en_vie'] : 
                    if piece['type'] == 'citoyen' : 
                        if piece['zombie'] : 
                            pyxel.blt(piece['x'], piece['y'], 0, 144, 16, 16, 16, 4 )
                        else : 
                            pyxel.blt(piece['x'], piece['y'], 0, 64, 16, 16, 16, 4 )

                    if piece['type'] == 'ouvrier' : 
                        pyxel.blt(piece['x'], piece['y'], 0, 80, 16, 16, 16, 4 )

                    if piece['type'] == 'soldat' : 
                        pyxel.blt(piece['x'], piece['y'], 0, 32, 16, 16, 16, 4 )
                    
                    if piece['type'] == 'president' : 
                        pyxel.blt(piece['x'], piece['y'], 0, 0, 16, 16, 16, 4 )

                    if piece['type'] == 'ministre' :
                        pyxel.blt(piece['x'], piece['y'], 0, 48, 16, 16, 16, 4 )
                    
                    if piece['type'] == 'pirate' :
                        pyxel.blt(piece['x'], piece['y'], 0, 16, 16, 16, 16, 4 )
                        
            for piece in equipe_jaune : 

                if piece['en_vie'] and (piece['en_mouvement']) : 
                    
                    pyxel.rect(piece['x'], piece['y'], 16, 16, 13)

                

                if piece['en_vie'] : 
                    if piece['type'] == 'citoyen' : 
                        if piece['zombie'] : 
                            pyxel.blt(piece['x'], piece['y'], 0, 144, 0, 16, 16, 4 )
                        else : 
                            pyxel.blt(piece['x'], piece['y'], 0, 64, 0, 16, 16, 4 )

                    if piece['type'] == 'ouvrier' : 
                        pyxel.blt(piece['x'], piece['y'], 0, 80, 0, 16, 16, 4 )

                    if piece['type'] == 'soldat' : 
                        pyxel.blt(piece['x'], piece['y'], 0, 32, 0, 16, 16, 4 )
                    
                    if piece['type'] == 'president' : 
                        pyxel.blt(piece['x'], piece['y'], 0, 0, 0, 16, 16, 4 )
                    
                    if piece['type'] == 'ministre' :
                        pyxel.blt(piece['x'], piece['y'], 0, 48, 0, 16, 16, 4 )
                    
                    if piece['type'] == 'pirate' :
                        pyxel.blt(piece['x'], piece['y'], 0, 16, 0, 16, 16, 4 )
                                         
            for piece in equipe_bleu : 

                if piece['en_vie'] and (piece['en_mouvement']) : 
                    
                    pyxel.rect(piece['x'], piece['y'], 16, 16, 13)

                

                if piece['en_vie'] :  
                    if piece['type'] == 'citoyen' : 
                        if piece['zombie'] : 
                            pyxel.blt(piece['x'], piece['y'], 0, 144, 48, 16, 16, 4 )
                        else : 
                            pyxel.blt(piece['x'], piece['y'], 0, 64, 48, 16, 16, 4 )

                    if piece['type'] == 'ouvrier' : 
                        pyxel.blt(piece['x'], piece['y'], 0, 80, 48, 16, 16, 4 )

                    if piece['type'] == 'soldat' : 
                        pyxel.blt(piece['x'], piece['y'], 0, 32, 48, 16, 16, 4 )

                    if piece['type'] == 'president' : 
                        pyxel.blt(piece['x'], piece['y'], 0, 0, 48, 16, 16, 4 )
                    
                    if piece['type'] == 'ministre' :
                        pyxel.blt(piece['x'], piece['y'], 0, 48, 48, 16, 16, 4 )
                    
                    if piece['type'] == 'pirate' :
                        pyxel.blt(piece['x'], piece['y'], 0, 16, 48, 16, 16, 4 )
                        


            for abilite in abilite_rose : 
                if abilite['selection'] : 
                    pyxel.rect(abilite['x'], abilite['y'], 16, 16, 13)
                
                if abilite['type'] == 'mur' : 
                    pyxel.blt(abilite['x'], abilite['y'],0, 176, 32, 16, 16, 0)

                if abilite['type'] == 'mine' : 
                    pyxel.blt(abilite['x'], abilite['y'],0, 160, 32, 16, 16, 4)
                
                if abilite['type'] == 'piratage' : 
                    pyxel.blt(abilite['x'], abilite['y'],0, 176, 96, 16, 16, 0)
                
                if abilite['type'] == 'feu' : 
                    pyxel.blt(abilite['x'], abilite['y'],0, 112, 32, 16, 16, 0)
                
                if abilite['type'] == 'soin' : 
                    pyxel.blt(abilite['x'], abilite['y'],0, 128, 32, 16, 16, 0)
                
                if abilite['type'] == 'prison' : 
                    pyxel.blt(abilite['x'], abilite['y'],0, 176, 80, 16, 16, 0)
                
                if abilite['type'] == 'barriere' : 
                    pyxel.blt(abilite['x'], abilite['y'],0, 176, 64, 16, 16, 0)
                
                if abilite['type'] == 'teleportation' :
                    pyxel.blt(abilite['x'], abilite['y'],0, 176, 112, 16, 16, 4)
                
                if abilite['type'] == 'bombe' :
                    pyxel.blt(abilite['x'], abilite['y'],0, 192, 32, 16, 16, 4)
                
                

                
                
                if not abilite['activation'] : 
                    pyxel.line(abilite['x'], abilite['y'], abilite['x'] + 15, abilite['y'] + 15 ,1)
                    pyxel.line(abilite['x'] + 15, abilite['y'], abilite['x'],  abilite['y'] + 15 ,1)

                if abilite['recharge'] > 0 : 
                    pyxel.text(abilite['x'] + 9 , abilite['y'] + 9, str(abilite['recharge']) , 7)
                
            for abilite in abilite_bleu : 
                if abilite['selection'] : 
                    pyxel.rect(abilite['x'], abilite['y'], 16, 16, 13)
                

                if abilite['type'] == 'mur' : 
                    pyxel.blt(abilite['x'], abilite['y'],0, 176, 48, 16, 16, 0)

                if abilite['type'] == 'mine' : 
                    pyxel.blt(abilite['x'], abilite['y'],0, 160, 48, 16, 16, 4)
                
                if abilite['type'] == 'piratage' : 
                    pyxel.blt(abilite['x'], abilite['y'],0, 192, 96, 16, 16, 0)
                
                if abilite['type'] == 'feu' : 
                    pyxel.blt(abilite['x'], abilite['y'],0, 112, 48, 16, 16, 0)
                
                if abilite['type'] == 'soin' : 
                    pyxel.blt(abilite['x'], abilite['y'],0, 128, 48, 16, 16, 0)
                
                if abilite['type'] == 'prison' : 
                    pyxel.blt(abilite['x'], abilite['y'],0, 192, 80, 16, 16, 0)
                
                if abilite['type'] == 'barriere' : 
                    pyxel.blt(abilite['x'], abilite['y'],0, 192, 64, 16, 16, 0)
                
                if abilite['type'] == 'teleportation' :
                    pyxel.blt(abilite['x'], abilite['y'],0, 192, 112, 16, 16, 4)
                
                if abilite['type'] == 'bombe' :
                    pyxel.blt(abilite['x'], abilite['y'],0, 192, 48, 16, 16, 4)
                
                if not abilite['activation'] : 
                    pyxel.line(abilite['x'], abilite['y'], abilite['x'] + 15, abilite['y'] + 15 ,1)
                    pyxel.line(abilite['x'] + 15, abilite['y'], abilite['x'],  abilite['y'] + 15 ,1)

                if abilite['recharge'] > 0 : 
                    pyxel.text(abilite['x'] + 9 , abilite['y'] + 9, str(abilite['recharge']) , 7)

            for abilite in abilite_jaune : 
                if abilite['selection'] : 
                    pyxel.rect(abilite['x'], abilite['y'], 16, 16, 13)
                

                if abilite['type'] == 'mur' : 
                    pyxel.blt(abilite['x'], abilite['y'],0, 176, 0, 16, 16, 0)
                
                if abilite['type'] == 'mine' : 
                    pyxel.blt(abilite['x'], abilite['y'],0, 160, 0, 16, 16, 4)

                if abilite['type'] == 'piratage' : 
                    pyxel.blt(abilite['x'], abilite['y'],0, 144, 96, 16, 16, 0)
                
                if abilite['type'] == 'feu' : 
                    pyxel.blt(abilite['x'], abilite['y'],0, 112, 0, 16, 16, 0)
                
                if abilite['type'] == 'soin' : 
                    pyxel.blt(abilite['x'], abilite['y'],0, 128, 0, 16, 16, 0)
                
                if abilite['type'] == 'prison' : 
                    pyxel.blt(abilite['x'], abilite['y'],0, 144, 80, 16, 16, 0)
                
                if abilite['type'] == 'barriere' : 
                    pyxel.blt(abilite['x'], abilite['y'],0, 144, 64, 16, 16, 0)
                
                if abilite['type'] == 'teleportation' :
                    pyxel.blt(abilite['x'], abilite['y'],0, 144, 112, 16, 16, 4)
                
                if abilite['type'] == 'bombe' :
                    pyxel.blt(abilite['x'], abilite['y'],0, 192, 0, 16, 16, 4)
                
                if not abilite['activation'] : 
                    pyxel.line(abilite['x'], abilite['y'], abilite['x'] + 15, abilite['y'] + 15 ,1)
                    pyxel.line(abilite['x'] + 15, abilite['y'], abilite['x'],  abilite['y'] + 15 ,1)

                if abilite['recharge'] > 0 : 
                    pyxel.text(abilite['x'] + 9 , abilite['y'] + 9, str(abilite['recharge']) , 7)

            for abilite in abilite_vert : 
                if abilite['selection'] : 
                    pyxel.rect(abilite['x'], abilite['y'], 16, 16, 13)
                

                if abilite['type'] == 'mur' : 
                    pyxel.blt(abilite['x'], abilite['y'],0, 176, 16, 16, 16, 0)
                
                if abilite['type'] == 'mine' : 
                    pyxel.blt(abilite['x'], abilite['y'],0, 160, 16, 16, 16, 4)
                
                if abilite['type'] == 'piratage' : 
                    pyxel.blt(abilite['x'], abilite['y'],0, 160, 96, 16, 16, 0)
                
                if abilite['type'] == 'feu' : 
                    pyxel.blt(abilite['x'], abilite['y'],0, 112, 16, 16, 16, 0)
                
                if abilite['type'] == 'soin' : 
                    pyxel.blt(abilite['x'], abilite['y'],0, 128, 16, 16, 16, 0)
                
                if abilite['type'] == 'prison' : 
                    pyxel.blt(abilite['x'], abilite['y'],0, 160, 80, 16, 16, 0)
                
                if abilite['type'] == 'barriere' : 
                    pyxel.blt(abilite['x'], abilite['y'],0, 160, 64, 16, 16, 0)
                
                if abilite['type'] == 'teleportation' :
                    pyxel.blt(abilite['x'], abilite['y'],0, 160, 112, 16, 16, 4)
                
                if abilite['type'] == 'bombe' :
                    pyxel.blt(abilite['x'], abilite['y'],0, 192, 16, 16, 16, 4)
                
                if not abilite['activation'] : 
                    pyxel.line(abilite['x'], abilite['y'], abilite['x'] + 15, abilite['y'] + 15 ,1)
                    pyxel.line(abilite['x'] + 15, abilite['y'], abilite['x'],  abilite['y'] + 15 ,1)

                if abilite['recharge'] > 0 : 
                    pyxel.text(abilite['x'] + 9 , abilite['y'] + 9, str(abilite['recharge']) , 7)

                    

            if jou[turn] == 'bleu' : 
                pyxel.rect(256, 0, pyxel.width-256, 25, 5)
            
            if jou[turn] == 'rose' : 
                pyxel.rect(256, 0, pyxel.width-256, 25, 8)

            if jou[turn] == 'jaune' : 
                pyxel.rect(256, 0, pyxel.width-256, 25, 10)

            if jou[turn] == 'vert' : 
                pyxel.rect(256, 0, pyxel.width-256, 25, 3)

            for mur in liste_mur : 
                pyxel.blt(mur['x'], mur['y'], 0, 64, 80, 16, 16, 0)
                pyxel.text(mur['x'] + 8 , mur['y'] + 4, str(mur['tour_restant']) ,2)

            for explosion in liste_explosion : 
                if pyxel.frame_count%3 == 0 :
                    pyxel.circb(explosion['x'] +8, explosion['y'] +8, explosion['rayon'] ,8)
                elif pyxel.frame_count%2 == 0 : 
                    pyxel.circb(explosion['x'] +8, explosion['y'] +8, explosion['rayon'] ,10 - explosion['couleur'])

            for prison in liste_prison :
                pyxel.blt(prison['x'], prison['y'], 0, 32, 80, 16, 16, 0)
                pyxel.text(prison['x'] + 8 , prison['y'] + 4, str(prison['tour_restant']) ,2)

            for barriere in liste_barriere : 
                pyxel.blt(barriere['x'], barriere['y'], 0, 48, 80, 16, 16, 0)
                pyxel.text(barriere['x'] + 8 , barriere['y'] + 4, str(barriere['tour_restant']) ,2)

            for feu in liste_feu : 
                if feu['frame'] >= 0 : 
                    pyxel.blt(feu['x'], feu['y'], 0, 32, 64, 16, 16, 0)
                if feu['frame'] >= 2 : 
                    pyxel.blt(feu['x'], feu['y'], 0, 16, 64, 16, 16, 0)
                if feu['frame'] >= 4 : 
                    pyxel.blt(feu['x'], feu['y'], 0, 0, 64, 16, 16, 0)
                pyxel.text(feu['x'] + 8 , feu['y'] + 4, str(feu['tour_restant']) ,2)
            
            pyxel.text(260, 2, str((temps*30 - int(pyxel.frame_count - frame_tour))//30+ 1) + ' seconde restante', 7)
            pyxel.rect(256, 240, 48, 16, 8)
            pyxel.text(256 + 3, 240 + 5, 'Abandonner?', 7)
            pyxel.blt(304, 240, 0, 128, 64,16, 16, 4)
            pyxel.text(260, 40, "Appuyer sur le bouton rouge \npour mettre le jeu sur pause \net sur le carre pour abandonner. \nAller dans aide si \nil y a un manque de \ncomprehension.", 7)
            pyxel.text(260, 90, "Les carres gris montrent \nles endroits ou l'on peut \nutiliser une abilite \net deplacer des pieces", 7)
            pyxel.text(260, 120, "Chaque abilite \nfait queleque chose de \ndifferent", 7)
            pyxel.text(260, 150, "Bonne chance !", 7)

        else : 
            
            if not choix_1 : 
                couleur = 8 
                equipe = 'rose'
            elif choix_1 and not choix_2 : 
                couleur = 5 
                equipe = 'bleu'
            elif choix_1 and  choix_2 and not choix_3 : 
                couleur = 10 
                equipe = 'jaune'
            elif choix_1 and  choix_2 and choix_3 and not choix_4: 
                couleur = 3 
                equipe = 'vert'
            else : 
                couleur = 7
                equipe = 'None'

            if temps == None : 
                pyxel.rectb(32, 64, 64, 128, 3)
                pyxel.text(35, 128, '120sec par tour', 3)
                pyxel.text(44, 136, 'pour jouer', 3)
                pyxel.text(31, 55, 'Difficulte Facile', 3)

                pyxel.rectb(32 +128, 64, 64, 128, 9)
                pyxel.text(37 +128, 128, '30sec par tour', 9)
                pyxel.text(40 +128, 136, 'pour jouer', 9)
                pyxel.text(29 +128, 55, 'Difficulte Moyenne', 9)
                if pyxel.frame_count%3 == 0 :
                    pyxel.rectb(32 +128 +128, 64, 64, 128, 9)
                    pyxel.text(40 +128 +128, 128, '9sec par tour', 9)
                    pyxel.text(44 +128 +128, 136, 'pour jouer', 9)
                    pyxel.text(38 +128 +128, 55, '>>>EXTREME<<<', 9)
                elif pyxel.frame_count%2 == 0 :
                    pyxel.rectb(32 +128 +128, 64, 64, 128, 8)
                    pyxel.text(40 +128 +128, 128, '9sec par tour', 8)
                    pyxel.text(44 +128 +128, 136, 'pour jouer', 8)
                    pyxel.text(38 +128 +128, 55, '>>>EXTREME<<<', 8)
                else : 
                    pyxel.rectb(32 +128 +128, 64, 64, 128, 10)
                    pyxel.text(40 +128 +128, 128, '9sec par tour', 10)
                    pyxel.text(44 +128 +128, 136, 'pour jouer', 10)
                    pyxel.text(38 +128 +128, 55, '>>>EXTREME<<<', 10)
            else : 
                pyxel.rectb(12, 64, 76, 128, couleur)
                pyxel.rectb(12 + 96*1, 64, 76, 128, couleur)
                pyxel.rectb(12 + 96*2, 64, 76, 128, couleur)
                pyxel.rectb(12 + 96*3, 64, 76, 128, couleur)

                pyxel.text(112, 16, f"choix abilite du ministre : equipe {equipe}", couleur)

                pyxel.text(20, 55, 'FEU', couleur)
                pyxel.text(20 +  96*1, 55, 'BARRIERE', couleur)
                pyxel.text(20 +  96*2, 55, 'PRISON', couleur)
                pyxel.text(20 +  96*3, 55, 'SOIN', couleur)

                pyxel.text(20, 80, "Le ministre peut \nmetttre en feu\nune case force\nla piece sur \ncette derniere\na bouger.", couleur)
                pyxel.text(20 + 96*1, 80, "Le ministre peut \nprotger une\npiece si\nelle bouge la\nbarriere\ndisparait.", couleur)
                pyxel.text(20 + 96*2, 80, "Le ministre peut \nemprisoner une \npiece \net l'empeche \nde bouger. \nAttention tuer\nun prisioner\nemprisone \nl'assaillant", couleur)
                pyxel.text(20 + 96*3, 80, "Le ministre peut \nreanimer\nun soldat\nou pirate \ntomber au\ncombat.", couleur)


    else : 
        if winner_1 == 'Gagnant rose':
            pyxel.cls(8)
        elif winner_1 == 'Gagnant vert':
            pyxel.cls(3)
        elif winner_1 == 'Gagnant bleu':
            pyxel.cls(5)
        elif winner_1 == 'Gagnant jaune':
            pyxel.cls(10)

        pyxel.text(64, 64, winner_1, 7)
        pyxel.text(64, 100, 'Appuyer sur "M" ou le bouton rouge pour recommencer la partie ', 7)
        pyxel.blt(64, 110, 0, 128, 64,16, 16, 4)
            

        


generate_bricks()
pyxel.run(update, draw)
