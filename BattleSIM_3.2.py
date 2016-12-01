import pygame
from time import time
from random import randint

pygame.init()

# COLORS
white = (255, 255, 255)
black = (0, 0, 0)
red = (200, 0, 0)
light_red = (255, 99, 71)
green = (34, 177, 76)
light_green = (0, 255, 0)
dark_yellow = (204, 204, 0)
yellow = (200, 200, 0)
light_yellow = (255, 255, 0)
blue = (0, 0, 200)
light_blue = (0, 191, 255)
brown = (139, 69, 19)
light_brown = (222, 184, 135)
gray = (105, 105, 105)
light_gray = (192, 192, 192)

# Different sizes
display_width = 1200
display_height = 600
button_width = 100
button_height = 50
monster_width = 200

# Different locations for hp and man bars
hum_x = 100
hum_y = 50
comp_x = 900
comp_y = 50
mana_y = 40

Screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("BattleSIM")


# Fonts
smallFont = pygame.font.SysFont("Rockwell", 25)
medFont = pygame.font.SysFont("Rockwell", 50)
largeFont = pygame.font.SysFont("Rockwell", 80)

# Game music
pygame.mixer.music.load("arcade music.mp3")

background_pics = {}
mon_pics = {}
dice_pics = {}
battle_pics = {}

# Background pictures
land_fire = pygame.image.load("Volcano.png")
background_pics["land_fire"] = pygame.transform.scale(land_fire, (display_width, display_height))
land_earth = pygame.image.load("land_forest.jpg")
background_pics["land_earth"] = pygame.transform.scale(land_earth, (display_width, display_height))
land_water = pygame.image.load("land-water.jpg")
background_pics["land_water"] = pygame.transform.scale(land_water, (display_width, display_height))
land_air = pygame.image.load("land-6hk.jpg")
background_pics["land_air"] = pygame.transform.scale(land_air, (display_width, display_height))

# Monster pictures
fire = pygame.image.load("fire.png")
mon_pics["Fire"] = pygame.transform.scale(fire, (monster_width, monster_width))
earth = pygame.image.load("Element_Earth.png")
mon_pics["Earth"] = pygame.transform.scale(earth, (monster_width, monster_width))
water = pygame.image.load("water.png")
mon_pics["Water"] = pygame.transform.scale(water, (monster_width, monster_width))
air = pygame.image.load("air.png")
mon_pics["Air"] = pygame.transform.scale(air, (monster_width, monster_width))

# Dice pictures
dice_1 = pygame.image.load("dice 1.jpg")
dice_pics["dice 1"] = pygame.transform.scale(dice_1, (monster_width, monster_width))
dice_2 = pygame.image.load("dice 2.jpg")
dice_pics["dice 2"] = pygame.transform.scale(dice_2, (monster_width, monster_width))
dice_3 = pygame.image.load("dice 3.jpg")
dice_pics["dice 3"] = pygame.transform.scale(dice_3, (monster_width, monster_width))
dice_4 = pygame.image.load("dice 4.jpg")
dice_pics["dice 4"] = pygame.transform.scale(dice_4, (monster_width, monster_width))
dice_5 = pygame.image.load("dice 5.jpg")
dice_pics["dice 5"] = pygame.transform.scale(dice_5, (monster_width, monster_width))
dice_6 = pygame.image.load("dice 6.jpg")
dice_pics["dice 6"] = pygame.transform.scale(dice_6, (monster_width, monster_width))

# Battle effects
smash = pygame.image.load("Fist.jpg")
battle_pics["smash"] = pygame.transform.scale(smash, (monster_width//2, monster_width//2))


#  Info for Monster
class Monster():

    def __init__(self, max_hp, max_mana, element, skill, exp, LVL):
        self.max_hp = max_hp
        self.hp = max_hp
        self.max_mana = max_mana
        self.mana = max_mana
        self.element = element
        self.skill = skill
        self.exp = exp
        self.LVL = LVL

    def add_exp(self, exp):  # adds LVLs
        self.exp += exp
        if self.exp >= self.LVL*100:
            self.exp -= self.LVL*100
            self.LVL += 1
            self.max_hp += 10
            self.max_mana += 5
            return True
        return False

    def refill(self):  # if you start the game, then refills hp and mana
        self.mana = self.max_mana
        self.hp = self.max_hp

    def load_info(self, LVL, exp):  # when you load a save
        self.max_mana = 50+LVL*5
        self.mana = self.max_mana
        self.max_hp = 200+(LVL-1)*10
        self.hp = self.max_hp
        self.exp = exp
        self.element = ""
        self.skill = ""
        self.LVL = LVL


# Displays hp_and mana bar
def hp_bar(hp, max_hp, hp_x, hp_y, mp, max_mp, mp_x, mp_y):
    hp_percent = hp/max_hp
    mp_percent = mp/max_mp
    pygame.draw.rect(Screen, red, [hp_x, hp_y, 2*100, 20])
    pygame.draw.rect(Screen, green, [hp_x, hp_y, 2*100*hp_percent, 20])
    pygame.draw.rect(Screen, black, [mp_x, mp_y, 4*50, 20])
    pygame.draw.rect(Screen, blue, [mp_x, mp_y, 4*50*mp_percent, 20])


# Displays hp and mana number
def hp_nr(hp, mp, hp_color, mp_color, y_displace, x_displace):
    message_to_screen(str(hp), hp_color, y_displace-40, "small", "hp_bar", x_displace)
    message_to_screen(str(mp), mp_color, y_displace, "small", "hp_bar", x_displace)


# LVL display
def LVL_display(LVL, y_displace, x_displace):
    message_to_screen("Level: "+str(LVL), black, y_displace, "small", "LVL", x_displace)


# Random landscape choice
def land_choice(fire_land, earth_land, water_land, air_land):
    choice = randint(1, 4)
    if choice == 1:
        background = fire_land
    elif choice == 2:
        background = earth_land
    elif choice == 3:
        background = water_land
    elif choice == 4:
        background = air_land
    return background


# Creating background with monsters
def landscape(background, hum_mon, com_mon):
    Screen.blit(background, (0, 0))
    Screen.blit(hum_mon, (100, 200))
    Screen.blit(com_mon, (900, 200))


# Showing dice pictures
def show_dice(nr, x, y):
    if nr == 1:
        Screen.blit(dice_pics["dice 1"], (x, y))
    elif nr == 2:
        Screen.blit(dice_pics["dice 2"], (x, y))
    elif nr == 3:
        Screen.blit(dice_pics["dice 3"], (x, y))
    elif nr == 4:
        Screen.blit(dice_pics["dice 4"], (x, y))
    elif nr == 5:
        Screen.blit(dice_pics["dice 5"], (x, y))
    elif nr == 6:
        Screen.blit(dice_pics["dice 6"], (x, y))


# combat effects
def combat_effects(skill, mon_x, enemy_x):
    skill_x = 0
    mon_y = 50
    print("hello")
    if skill == "smash":
        print("hello vol2")
        if mon_x < enemy_x:
            print("hello vol 3")
            while mon_x + monster_width + skill_x < enemy_x:
                print("hey!")
                Screen.blit(battle_pics["smash"], (mon_x + monster_width + skill_x, mon_y + 50))
                skill_x += 1


# Choosing name for enemy monster
def comp_mon(choice):
    if choice == 1:
        Computer.element = "Fire"
    elif choice == 2:
        Computer.element = "Earth"
    elif choice == 3:
        Computer.element = "Water"
    elif choice == 4:
        Computer.element = "Air"


# Choosing enemy monster
def comp_mon_choice(hum_choice):
    if hum_choice == "Fire":
        comp = randint(1, 3)
        comp += 1
        comp_mon(comp)
    elif hum_choice == "Earth":
        comp = randint(1, 3)
        if comp > 1:
            comp += 1
        comp_mon(comp)
    elif hum_choice == "Water":
        comp = randint(1, 3)
        if comp > 2:
            comp += 1
        comp_mon(comp)
    elif hum_choice == "Air":
        comp = randint(1, 3)
        comp_mon(comp)


# Giving bonus to monster if possible
def bonus(me, enemy, background):
    boonus = 0
    if me.element == "Fire" and enemy.element == "Earth":
        boonus = 3
        if background == background_pics["land_fire"]:
            boonus += 2
    elif me.element == "Earth" and enemy.element == "Water":
        boonus = 3
        if background == background_pics["land_earth"]:
            boonus += 2
    elif me.element == "Water" and enemy.element == "Fire":
        boonus = 3
        if background == background_pics["land_water"]:
            boonus += 2
    elif me.element == "Air":
        if background == background_pics["land_air"]:
            boonus += 2
    return boonus


# if enemy is higher LVL than I, then I get bonus damage
def handycap(me, enemy):
    if enemy.LVL - me.LVL > 1:
        return 5*(enemy.LVL - me.LVL)
    return 0


# Fonts
def text_objects(text, color, size):
    if size == "small":
        text_surface = smallFont.render(text, True, color)
    elif size == "medium":
        text_surface = medFont.render(text, True, color)
    elif size == "large":
        text_surface = largeFont.render(text, True, color)
    return text_surface, text_surface.get_rect()


# Text for button
def text_to_button(msg, color, button_x, button_y, but_width, but_height, size="small"):
    textsurface, textrectangle = text_objects(msg, color, size)
    textrectangle.center = ((button_x + (but_width / 2)), button_y + (but_height / 2))
    Screen.blit(textsurface, textrectangle)


# Text to screen
def message_to_screen(msg, color, y_displace=0, size="small", background=white, x_displace=0):
    textsurface, textrectangle = text_objects(msg, color, size)
    textrectangle.center= (display_width / 2) + x_displace, (display_height / 2) + y_displace
    if background is not None:
        pygame.draw.rect(Screen, white, ((display_width / 2 - textrectangle.width / 2 + x_displace),
                                         (display_height / 2 - textrectangle.height / 2 + y_displace), textrectangle.width, textrectangle.height))
    Screen.blit(textsurface, textrectangle)


# Button info
class Button():
    def __init__(self, rect, col1, col2, button_text, tulemus):
        self.rect = rect
        self.col1 = col1
        self.col2 = col2
        self.button_text = button_text
        self.tulemus = tulemus

    def draw(self):
        if collision(self.rect[0], self.rect[1], self.rect[2],self.rect[3],pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
            pygame.draw.rect(Screen, self.col2, self.rect)
        else:
            pygame.draw.rect(Screen, self.col1, self.rect)
        text_to_button(self.button_text, black, self.rect[0], self.rect[1], self.rect[2], self.rect[3])

    def mouse_collision(self, mouse_event):
        if collision(self.rect[0], self.rect[1], self.rect[2], self.rect[3], mouse_event.pos[0], mouse_event.pos[1]):
            return self.tulemus
        else:
            return

# BUTTONS
intro_But = [Button((250, 500, button_width, button_height), green, light_green, "Play", "Play"),
             Button((450, 500, button_width, button_height), blue, light_blue, "Load", "Load"),
             Button((650, 500, button_width, button_height), yellow, light_yellow, "Help", "Help"),
             Button((850, 500, button_width, button_height), red, light_red, "Quit", "Quit")]

monster_But = [Button((150, 400, button_width, button_height), red, light_red, "Fire", "Fire"),
               Button((400, 400, button_width, button_height), brown, light_brown, "Earth", "Earth"),
               Button((650, 400, button_width, button_height), blue, light_blue, "Water", "Water"),
               Button((900, 400, button_width, button_height), gray, light_gray, "Air", "Air")]

skill_But = [Button((250, 500, button_width, button_height), red, light_red, "Smash", "Smash"),
             Button((450, 500, button_width, button_height), yellow, light_yellow, "Special", "Special"),
             Button((650, 500, button_width, button_height), green, light_green, "Heal", "Heal"),
             Button((850, 500, button_width, button_height), blue, light_blue, "Restore", "Restore")]

gameOver_But = [Button((350, 500, button_width, button_height), green, light_green, "Play", "Play"),
                Button((550, 500, button_width, button_height), blue, light_blue, "Save", "Save"),
                Button((750, 500, button_width, button_height), red, light_red, "Quit", "Quit")]

help_But = [Button((250, 500, button_width, button_height), red, light_red, "Quit", "Quit"),
            Button((850, 500, button_width, button_height), green, light_green, "Play", "Play")]

save_But = [Button((display_width/2-button_width/2, display_height/2-100, button_width, button_height),
                   green, light_green, "Save 1", "Save1.txt"),
            Button((display_width/2-button_width/2, display_height/2-50, button_width, button_height),
                   green, light_green, "Save 2", "Save2.txt"),
            Button((display_width/2-button_width/2, display_height/2, button_width, button_height),
                   green, light_green, "Save 3", "Save3.txt"),
            Button((display_width/2-button_width/2, display_height/2+100, button_width, button_height),
                   blue, light_blue, "Back", "Back")]


def handle_buttons(buttons, mouse_event):
    for b in buttons:
        result = b.mouse_collision(mouse_event)
        if result is not None:
            return result


def draw_buttons(buttons):
    for b in buttons:
        b.draw()


def collision(box_x, box_y, box_w, box_h, point_x, point_y):
    if point_x < box_x or point_y < box_y or point_x > box_x+box_w or point_y > box_y + box_h:
        return False
    else:
        return True


# Opening save file
def files(file_name):
    f = open(file_name)
    info = []
    for line in f:
        info += [line.strip()]
    f.close()
    return info


# Loading info to Human and Computer
def load(file_name):
    info = files(file_name)
    Human.load_info(int(info[0]), int(info[1]))
    Computer.load_info(int(info[2]), int(info[3]))
    return Human, Computer


# Saving data to files
def save(human, computer, file):
    LVL1 = human.LVL
    LVL2 = computer.LVL
    exp1 = human.exp
    exp2 = computer.exp
    data = [LVL1, exp1, LVL2, exp2]
    new_save(data, file)


# Save file changing
def new_save(data, file):
    f = open(file, "w")
    for num in data:
        f.write(str(num))
        f.write("\n")
    f.close()


# Calculating the fight
def effect(me, enemy, choice):
    if choice == "Smash":
        # combat_effects("smash", 100, 900)
        enemy.hp -= (randint(20, 35) + bonus(me, enemy, land) + handycap(me, enemy))
        if enemy.hp <= 0:
            enemy.hp = 0
    elif choice == "Special":
        enemy.hp -= (randint(25, 50) + bonus(me, enemy, land) + handycap(me, enemy))
        me.mana -= 15
        if enemy.hp <= 0:
            enemy.hp = 0
    elif choice == "Heal":
        me.hp += randint(30, 45)
        me.mana -= 10
        if me.hp >= me.max_hp:
            me.hp = 100
    elif choice == "Restore":
        me.mana += randint(5, 15)
        if me.mana >= me.max_mana:
            me.mana = me.max_mana


# Attack color
def att_color(attack):
    if attack == "Smash":
        return red
    if attack == "Special":
        return dark_yellow
    if attack == "Heal":
        return green
    if attack == "Restore":
        return blue


# Choosing computer attack
def comp_att(computer):
    while True:
        choice = randint(1, 4)
        if choice == 1:
            computer.skill = "Smash"
            return
        if choice == 2:
            if Computer.mana >= 15:
                computer.skill = "Special"
                return
        if choice == 3:
            if computer.hp <= computer.max_hp // 2:
                if computer.mana >= 10:
                    computer.skill = "Heal"
                    return
        if choice == 4:
            if computer.mana <= computer.max_mana // 2:
                computer.skill = "Restore"
                return


# Different globals
land = ""
result = ""
hum_pic, comp_pic = "", ""
gameExit = False
gameOver = False
Human = Monster(200, 50, 0, "", 0, 1)
Computer = Monster(200, 50, 0, "", 0, 1)
combat_state = ""
state = "menu"
who = "human"
comp_chance = 0
hum_chance = 0
human_attack = False
comp_attack = False
last_time = time()
elapsed_time = 0
LVL_comp = False
LVL_hum = False

pygame.mixer.music.play(-1)
pygame.mixer.music.play(-1)
# GAMELOOP
while not gameExit:

    for event in pygame.event.get():
        pygame.mixer.music.play(-1, 0.0)
        if event.type == pygame.QUIT:
            gameExit = True
        if event.type == pygame.MOUSEBUTTONUP:

            # Different stages are chosen here
            if state == "menu":
                result = handle_buttons(intro_But, event)
                if result == "Play":
                    state = "chance"
                    comp_chance = randint(1, 6)
                    hum_chance = randint(1, 6)
                if result == "Load":
                    state = "load game"
                if result == "Help":
                    state = "help"
                if result == "Quit":
                    gameExit = True

            elif state == "load game":
                result = handle_buttons(save_But, event)
                if result == "Save1.txt":
                    load(result)
                    state = "chance"
                elif result == "Save2.txt":
                    load(result)
                    state = "chance"
                elif result == "Save3.txt":
                    load(result)
                    state = "chance"
                elif result == "Back":
                    state = "menu"
                comp_chance = randint(1, 6)
                hum_chance = randint(1, 6)

            elif state == "help":
                result = handle_buttons(help_But, event)
                if result == "Play":
                    state = "chance"
                    comp_chance = randint(1, 6)
                    hum_chance = randint(1, 6)
                if result == "Quit":
                    gameExit = True

            elif state == "chance":
                elapsed_time = 0
                state = "show chance"
                if comp_chance > hum_chance:
                    who = "computer"
                elif hum_chance > comp_chance:
                    who = "human"

            elif state == "choice":
                result = handle_buttons(monster_But, event)
                if result is not None:
                    Human.element = result
                    Human.refill()
                    Computer.refill()
                    land = land_choice(land_fire, land_earth, land_water, land_air)
                    hum_pic = mon_pics[Human.element]
                    comp_mon_choice(Human.element)
                    comp_pic = mon_pics[Computer.element]
                    state = "fight"

            elif state == "fight" or state == "missing mana":
                result = handle_buttons(skill_But, event)
                if result == "Special" and Human.mana < 15:
                    state = "missing mana"
                elif result == "Heal" and Human.mana < 10:
                    state = "missing mana"
                elif result is not None:
                    Human.skill = result
                    comp_att(Computer)
                    state = "calculate"
                    combat_state = "intro"
                    human_attack = False
                    comp_attack = False
                    elapsed_time = 0

            elif state == "game over":
                result = handle_buttons(gameOver_But, event)
                if result == "Play":
                    state = "menu"
                if result == "Save":
                    state = "save"
                if result == "Quit":
                    gameExit = True

            elif state == "save":
                result = handle_buttons(save_But, event)
                if result == "Save1.txt":
                    save(Human, Computer, "Save1.txt")
                    state = "menu"
                elif result == "Save2.txt":
                    save(Human, Computer, "Save2.txt")
                    state = "menu"
                elif result == "Save3.txt":
                    save(Human, Computer, "Save3.txt")
                    state = "menu"
                elif result == "Back":
                    state = "menu"

    # LOGICS
    if state == "calculate":
        elapsed_time += time()-last_time
        if combat_state == "intro":
            if elapsed_time > 1:
                combat_state = "full intro"
                elapsed_time = 0

        if combat_state == "full intro":
            if elapsed_time > 2:
                combat_state = "lives"
                elapsed_time = 0
                if who == "human":
                    effect(Human, Computer, Human.skill)
                if who == "computer":
                    effect(Computer, Human, Computer.skill)

        if combat_state == "lives":
            if elapsed_time > 3:
                elapsed_time = 0
                if who == "human":
                    combat_state = "intro"
                    who = "computer"
                    human_attack = True
                elif who == "computer":
                    combat_state = "intro"
                    who = "human"
                    comp_attack = True
                if comp_attack and human_attack:
                    state = "fight"
                if Human.hp <= 0 or Computer.hp <= 0:
                    state = "game over"
                    if Human.hp <= 0:
                        LVL_comp = Computer.add_exp(100)
                    if Computer.hp <= 0:
                        LVL_hum = Human.add_exp(100)

    if state == "show chance":
        if comp_chance == hum_chance:
            state = "chance"
            comp_chance = randint(1, 6)
            hum_chance = randint(1, 6)

        elapsed_time += time()-last_time
        if elapsed_time > 1:
            elapsed_time = 0
            state = "choice"

    last_time = time()

    # DISPLAY

    if state == "menu":
        Screen.fill(white)
        draw_buttons(intro_But)
        message_to_screen("Welcome to BattleSIM", green, 0, size="large")

    if state == "load game":
        Screen.fill(white)
        message_to_screen("Choose your save!", black, -150, size="medium")
        draw_buttons(save_But)

    if state == "help":
        Screen.fill(white)
        draw_buttons(help_But)
        message_to_screen("Here are instructions for stupid people", black, -150, size="medium", background=None)
        message_to_screen("You can choose between 4 monster to battle your enemy.", black, -90, background=None)
        message_to_screen("Enemy chooses a random monster.", black, -65, background=None)
        message_to_screen("Each monster is stronger against one other monster.", black, -40, background=None)
        message_to_screen("Fire wins Earth, Earth wins Water, Water wins Fire, but Air is NEUTRAL.", black, -15, background=None)
        message_to_screen("Background is chosen by random and it gives bonus too.", black, 10, background=None)
        message_to_screen("You have 4 skills to use: Smash, Special, Heal and Restore.", black, 35, background=None)
        message_to_screen("Smash does 20-35 damage, Special does 25-50 damage.", black, 60, background=None)
        message_to_screen("Heal gives 30-45 HP and Restore gives 5-15 MP.", black, 85, background=None)
        message_to_screen("When you defeat the enemy's monster, you gain EXP and Levels.", black, 110, background=None)

    if state == "chance":
        Screen.fill(white)
        message_to_screen("You and computer are rolling a die.", black, -100, size="medium", background=None)
        message_to_screen("You got: " + str(hum_chance), black, -50, size="medium", background=None)
        show_dice(hum_chance, 100, 300)
        message_to_screen("Computer got: " + str(comp_chance), black, 0, size="medium", background=None)
        show_dice(comp_chance, 900, 300)
        message_to_screen("Click to continue", black, 100, background=None)

    if state == "show chance":
        Screen.fill(white)
        if who == "computer":
            message_to_screen("Computer starts!", black, -25, background=None, size="large")
        elif who == "human":
            message_to_screen("You start!", black, -25, background=None, size="large")

    if state == "choice":
        Screen.fill(white)
        draw_buttons(monster_But)
        Screen.blit(mon_pics["Fire"], (100, 200))
        Screen.blit(mon_pics["Earth"], (350, 200))
        Screen.blit(mon_pics["Water"], (600, 200))
        Screen.blit(mon_pics["Air"], (850, 200))
        message_to_screen("Choose Your Monster", black, -200, size="medium")

    if state == "fight" or state == "calculate" or state == "missing mana":
        landscape(land, hum_pic, comp_pic)
        hp_nr(Human.hp, Human.mana, red, blue, -200, -530)
        hp_nr(Computer.hp, Computer.mana, red, blue, -200, 530)
        hp_bar(Human.hp, Human.max_hp, hum_x, hum_y, Human.mana, Human.max_mana, hum_x, hum_y + mana_y)
        hp_bar(Computer.hp, Computer.max_hp, comp_x, comp_y, Computer.mana, Computer.max_mana, comp_x, comp_y + mana_y)
        LVL_display(Human.LVL, 120, -400)
        LVL_display(Computer.LVL, 120, 400)

        if state == "missing mana":
            message_to_screen("Not enough mana!", black, -200)

        if state == "fight" or state == "missing mana":
            draw_buttons(skill_But)

        if state == "calculate":
            if combat_state == "intro" and who == "computer":
                message_to_screen("Enemy is deciding...", black, -200)

            if combat_state == "full intro" and who == "human":
                message_to_screen("Your monster used " + Human.skill, att_color(Human.skill), -200)
            if combat_state == "full intro" and who == "computer":
                message_to_screen("Enemy's monster used " + Computer.skill, att_color(Computer.skill), -200)

            if combat_state == "lives" and who == "human":
                if Human.skill == "Smash" or Human.skill == "Special" or Human.skill == "Heal":
                    message_to_screen("Enemy's monster has " + str(Computer.hp) + " HP left", black, -200)
                if Human.skill == "Special" or Human.skill == "Heal" or Human.skill == "Restore":
                    message_to_screen("Your monster has " + str(Human.mana) + " MP left", black, -170)

            if combat_state == "lives" and who == "computer":
                if Computer.skill == "Smash" or Computer.skill == "Special" or Computer.skill == "Heal":
                    message_to_screen("Your monster has " + str(Human.hp) + " HP left", black, -200)
                if Computer.skill == "Special" or Computer.skill == "Heal" or Computer.skill == "Restore":
                    message_to_screen("Enemy's monster has " + str(Computer.mana) + " MP left", black, -170)

    if state == "game over":
        Screen.fill(white)
        message_to_screen("Game Over", black, -100, size="large", background=None)

        if Human.hp <= 0:
            message_to_screen("Computer won!", black, -50, size="medium", background=None)
            if LVL_comp is True:
                message_to_screen("Computer Leveled to: " + str(Computer.LVL), black, 30, background=None)

        if Computer.hp <= 0:
            message_to_screen("You won!", black, -50, size="medium", background=None)
            if LVL_hum is True:
                message_to_screen("You Leveled to: " + str(Human.LVL), black, 30, background=None)
            else:
                message_to_screen(str(Human.exp) + " exp to next level", black, 30, background=None)
        draw_buttons(gameOver_But)

    if state == "save":
        Screen.fill(white)
        message_to_screen("Where do you wish to save your game?", black, -150, size="medium", background=None)
        draw_buttons(save_But)
    pygame.display.update()

pygame.quit()
quit()
