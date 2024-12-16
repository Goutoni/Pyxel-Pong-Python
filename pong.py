import pyxel

pyxel.init(160, 120, title="Pong",fps=60)
pyxel.load("assets.pyxres")

def init():
    global pos_y, pos_y_2, ball_x, ball_y, orientation, speedright, speedleft, pointer, right, left, game_over, score, old_score, ball_speed, end_left, end_right, high, down, mode_solo, mode_duo, start, high_score
    pos_y = 40
    pos_y_2 = 40
    ball_x = 20
    ball_y = 21
    high = -0.5
    down = 0.5
    orientation = 0.5
    speedleft = -1
    speedright = 1
    pointer = 1
    left = False
    right = False
    game_over = False
    score = 0
    old_score = 0
    ball_speed = 5
    mode_solo = False
    mode_duo = False
    end_left = False
    end_right = False
    start = True
    pyxel.play(0,0,loop=True)
    try:
        with open("score.txt", "r") as f:
            high_score = int(f.read())
    except:
        with open("score.txt","w") as f:
            high_score = 0
            f.write(f"{high_score}")
    
init()

def solo():
    global pos_y, ball_x, ball_y, orientation, speedright, speedleft, pointer, game_over, score, old_score
    if not game_over:
        ball_x += pointer
        ball_y += orientation
        if ball_x >= 160:
            pointer = speedleft
        if ball_x <= 8:
            if pos_y - 5 <= ball_y <= pos_y + 11:
                pointer = speedright
                score += 1
                if pos_y - 5 <= ball_y <= pos_y + 3:
                    orientation = high
                if pos_y + 3 < ball_y <= pos_y + 11:
                    orientation = down
        if ball_y >= 117:
            orientation = high
        if ball_y <= 0:
            orientation = down       
        if pyxel.btn(pyxel.KEY_UP) and pos_y > 5:
            pos_y -= 2
        if pyxel.btn(pyxel.KEY_DOWN) and pos_y < 108:
            pos_y += 2
        if old_score == score - 5:
            speedleft -= 0.5
            speedright += 0.5
            old_score = score
    if ball_x < -2:
        game_over=True 

def duo():
    global pos_y, pos_y_2, ball_x, ball_y, orientation, speedright, speedleft, pointer, right, left, game_over, score, old_score, ball_speed, end_left, end_right
    if not game_over:
        ball_x += pointer
        ball_y += orientation
        if ball_x <= 8:
            if pos_y - 5 <= ball_y <= pos_y + 11:
                pointer = speedright
                score += 1
                ball_speed -= 1
                left = True
                if pos_y - 5 <= ball_y <= pos_y + 3:
                    orientation = high
                if pos_y + 3 < ball_y <= pos_y + 11:
                    orientation = down
        if ball_x >= 152:
            if pos_y_2 - 5 <= ball_y <= pos_y_2 + 11:
                pointer = speedleft
                score += 1
                ball_speed -= 1
                right = True
                if pos_y_2 - 5 <= ball_y <= pos_y_2 + 3:
                    orientation = high
                if pos_y_2 + 3 < ball_y <= pos_y_2 + 11:
                    orientation = down
        if left == True:
            if ball_x >= 80:
                left = False
        if right == True:
            if ball_x <= 80:
                right = False
        if ball_y >= 117:
            orientation = high
        if ball_y <= 0:
            orientation = down       
        if pyxel.btn(pyxel.KEY_Z) and pos_y > 5:
            pos_y -= 2
        if pyxel.btn(pyxel.KEY_S) and pos_y < 108:
            pos_y += 2
        if pyxel.btn(pyxel.KEY_UP) and pos_y_2 > 5:
            pos_y_2 -= 2
        if pyxel.btn(pyxel.KEY_DOWN) and pos_y_2 < 108:
            pos_y_2 += 2
        if old_score == score - 5:
            speedleft -= 0.5
            speedright += 0.5
            if left == True:
                pointer = speedright
            if right == True:
                pointer = speedleft
            old_score = score
            ball_speed = 5
    if ball_x < -2:
        game_over=True
        end_left = True
    if ball_x > 164:
        game_over = True
        end_right = True

def update():
    global mode_solo, mode_duo, start
    if start:
        if pyxel.btn(pyxel.KEY_2):
            mode_duo = True
            start = False  
        if pyxel.btn(pyxel.KEY_1):
            mode_solo = True
            start = False  
    else:
        if mode_solo:
            solo()
        if mode_duo:
            duo()

def draw():
    global mode_solo, mode_duo, start
    if start:
        pyxel.cls(0)
        pyxel.rect(0,0,160,120,12)
        pyxel.blt(70,20,1,0,0,16,4,scale=8)
        pyxel.text(50, 50, "Mode Solo : 1", 5)
        pyxel.text(50, 60, "Mode Duo : 2", 5)
    else:
        if mode_solo or mode_duo and not game_over:
            pyxel.cls(0)
            pyxel.bltm(0, 0, 0, 0, 0, 160, 120)
            for i in range(2, 120, 10):  
                pyxel.rect(79, i, 1, 5, 7)
            for i in range(2,160,10):
                pyxel.rect(i,0,5,1,7)
            for i in range(2,160,10):
                pyxel.rect(i,119,5,1,7)

        if mode_solo:
            pyxel.blt(-5, pos_y, 0, 0, 0, 16, 8, rotate=90)
            pyxel.rect(ball_x, ball_y, 3, 3, 7)
            pyxel.text(90, 15, f"Score: {score}", 7)
            pyxel.text(90, 5, f"Meilleur : {high_score}", 7)

        if mode_duo:
            pyxel.blt(-5, pos_y, 0, 0, 0, 16, 8, rotate=90)
            pyxel.blt(149, pos_y_2, 0, 0, 0, 16, 8, rotate=270)
            pyxel.rect(ball_x, ball_y, 3, 3, 7)
            if not game_over:
                pyxel.text(90, 10, f"Accelere dans : {ball_speed}", 7)

        if game_over:
            pyxel.cls(0)
            pyxel.stop()
            if not end_left and not end_right:
                pyxel.text(10, 10, "Perdu", 5)
                if high_score < score:
                    with open("score.txt","w") as f:
                        f.write(f"{score}")
            elif end_right:
                pyxel.text(10, 10, "Perdu pour le joueur de droite", 5)
            elif end_left:
                pyxel.text(10, 10, "Perdu pour le joueur de gauche", 5)
            pyxel.text(10, 30, "Espace pour revenir au menu", 5)
            pyxel.text(10, 40, "Echap pour quitter", 5)
            if pyxel.btn(pyxel.KEY_SPACE):
                init()
            if pyxel.btn(pyxel.KEY_ESCAPE):
                pyxel.quit()

pyxel.run(update, draw)