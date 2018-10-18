import pygame
import random

pygame.init()

# basic game constants
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# dimensions for hit boxes
cowboy_width, cowboy_height = 60, 83
cactus_width, cactus_height = 86, 94
needle_width, needle_height = 96, 42
side_needle_width, side_needle_height = 96, 96
heal_width, heal_height = 96, 48
fire_width, fire_height = heal_width, heal_height


# set up display, each sprite capable of movement
def display(filename):
    def display_func(x, y):
        gameDisplay.blit(pygame.image.load(filename), (x, y))
    return display_func


# define appropriate png files for sprites
cowboy = display('images/cowboy.png')
cactus = display('images/cactus.png')
crosshair = display('images/crosshair.png')
crosshair_fired = display('images/crosshair_fired.png')
heal_cursor = display('images/heal_cursor.png')
heal_fired = display('images/heal_fired.png')
hp_bar = display('images/hp_bar.png')
enemy_bar = display('images/enemy_bar.png')
needle = display('images/needle.png')
side_needle = display('images/side_needle.png')
heal = display('images/heal.png')
fire = display('images/fire.png')


# function for displaying text on screen
def message_display(text, x_pos, y_pos, font_size):
    font = pygame.font.SysFont('Georgia', font_size)
    gameDisplay.blit(font.render(text, True, WHITE), (x_pos, y_pos))


# set up window display, window text, and in-game clock
gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption('Passion Fruit')
clock = pygame.time.Clock()


def game_loop():
    game_exit = False
    game_won = False
    game_over = False
    debug = False

    cowboy_init_x, cowboy_init_y = DISPLAY_WIDTH * 0.2, DISPLAY_HEIGHT * 0.2
    cowboy_x, cowboy_y = cowboy_init_x, cowboy_init_y
    cactus_init_x, cactus_init_y = DISPLAY_WIDTH * 0.8, DISPLAY_HEIGHT * 0.3
    cactus_x, cactus_y = cactus_init_x, cactus_init_y
    needle_x, needle_y = cactus_init_x, cactus_init_y
    heal_x, heal_y = DISPLAY_WIDTH * 0.4, DISPLAY_HEIGHT * 0.63
    fire_x, fire_y = heal_x + heal_width + 30, heal_y

    cowboy_speed = 8
    needle_speed = 12
    side_needle_speed = 10

    cowboy_x_change, cowboy_y_change = 0, 0
    box_width, box_height = cowboy_width * 4, cowboy_height * 4
    box_x, box_y = cowboy_init_x - cowboy_width * 2, cowboy_init_y - cowboy_height*1.3
    side_needle_x, side_needle_y = box_x, box_y + box_height

    bar_x, bar_y = 5, DISPLAY_HEIGHT - 100
    enemy_bar_x, enemy_bar_y = bar_x, bar_y - 70
    bar_width = 30
    message1_x, message1_y = DISPLAY_WIDTH * 0.6, DISPLAY_HEIGHT * 0.6
    message2_x, message2_y = DISPLAY_WIDTH * 0.8, DISPLAY_HEIGHT * 0.6 + 30
    message3_x, message3_y = DISPLAY_WIDTH * 0.65, DISPLAY_HEIGHT * 0.6 + 67

    player_max_hp, player_atk = 12, 1
    cactus_max_hp, cactus_atk = 50, 2
    player_hp = player_max_hp
    cactus_hp = cactus_max_hp

    fps = 30
    # cooldown is 1/2 a second
    cooldown = fps * 0.5
    invuln_time = cooldown
    damaged = False
    heal_mode = False
    cactus_healed = False

    while not game_exit:
        gameDisplay.fill(BLACK)

        player_hitbox = pygame.Rect(cowboy_x, cowboy_y, cowboy_width - 15, cowboy_height)
        cactus_hitbox = pygame.Rect(cactus_x, cactus_y, cactus_width, cactus_height)
        needle_hitbox = pygame.Rect(needle_x, needle_y, needle_width, needle_height)
        side_needle_hitbox = pygame.Rect(side_needle_x, side_needle_y, side_needle_width, side_needle_height)
        heal_hitbox = pygame.Rect(heal_x, heal_y, heal_width, heal_height)
        fire_hitbox = pygame.Rect(fire_x, fire_y, fire_width, fire_height)
        if debug:
            pygame.draw.rect(gameDisplay, WHITE, player_hitbox, 2)
            pygame.draw.rect(gameDisplay, WHITE, cactus_hitbox, 2)
            pygame.draw.rect(gameDisplay, WHITE, needle_hitbox, 2)
            pygame.draw.rect(gameDisplay, WHITE, side_needle_hitbox, 2)

        # define conditions for having game won or lost
        if player_hp <= 0 and not game_won:
            # there is obviously a better way to make this irreversible, will fix later
            player_hp = -9999999
            game_over = True
            message_display("GAME OVER!", DISPLAY_WIDTH / 2, 50, 70)
        if cactus_hp <= 0 and not game_over:
            cactus_hp = -9999999
            game_won = True
            message_display("YOU WIN!", DISPLAY_WIDTH / 2, 50, 70)
        if game_won or game_over:
            message1_x, message2_x, message3_x = 1000, 1000, 1000

        # flavor text for healing the enemy
        if cactus_healed:
            message_display("What are you doing!? Don't heal your opponent!",
                            message1_x, message1_y, 20)

        if cactus_hp > cactus_max_hp * 1.2:
            message_display("STOP!!!!!!!!!!", message2_x, message2_y, 20)

        if cactus_hp > cactus_max_hp * 1.5:
            message_display("OH MY GOD... WE'RE ALL GOING TO DIE", message3_x, message3_y, 20)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True

            # movement based on keys being pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    cowboy_x_change += -cowboy_speed
                if event.key == pygame.K_RIGHT:
                    cowboy_x_change += cowboy_speed
                if event.key == pygame.K_UP:
                    cowboy_y_change += -cowboy_speed
                if event.key == pygame.K_DOWN:
                    cowboy_y_change += cowboy_speed

            # movement negated when keys are lifted
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    cowboy_x_change += cowboy_speed
                if event.key == pygame.K_RIGHT:
                    cowboy_x_change += -cowboy_speed
                if event.key == pygame.K_UP:
                    cowboy_y_change += cowboy_speed
                if event.key == pygame.K_DOWN:
                    cowboy_y_change += -cowboy_speed

            # event for firing at cactus: deals damage equal to player_atk
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if not heal_mode:
                    crosshair_fired(mouse_x - fire_bal, mouse_y - fire_bal)
                else:
                    heal_fired(mouse_x - heal_bal_x, mouse_y - heal_bal_y)
                if not heal_mode:
                    if cactus_hitbox.collidepoint(mouse_x, mouse_y):
                        cactus_hp -= player_atk
                    if needle_hitbox.collidepoint(mouse_x, mouse_y):
                        # ideally the needle object would be temporarily disabled, for now it just moves out of bounds
                        needle_y = -100
                        needle_x = cactus_init_x
                    if side_needle_hitbox.collidepoint(mouse_x, mouse_y):
                        side_needle_x = -200
                if heal_hitbox.collidepoint(mouse_x, mouse_y):
                    heal_mode = True
                if fire_hitbox.collidepoint(mouse_x, mouse_y):
                    heal_mode = False
                if player_hitbox.collidepoint(mouse_x, mouse_y) and heal_mode:
                    if player_hp < player_max_hp:
                        player_hp += 1
                if cactus_hitbox.collidepoint(mouse_x, mouse_y) and heal_mode:
                    cactus_hp += 1
                    cactus_healed = True
                    message_x, message_y = DISPLAY_WIDTH * 0.6, DISPLAY_HEIGHT * 0.6

        # set up cowboy and movement
        cowboy(cowboy_x, cowboy_y)
        cowboy_x += cowboy_x_change
        cowboy_y += cowboy_y_change
        
        # set up cactus
        cactus(cactus_x, cactus_y)

        # set up box and keep player confined within
        pygame.draw.rect(gameDisplay, WHITE, [box_x, box_y, box_width, box_height], 2)
        if cowboy_x > box_x + box_width - cowboy_width:
            cowboy_x = box_x + box_width - cowboy_width
        elif cowboy_x < box_x:
            cowboy_x = box_x
        if cowboy_y > box_y + box_height - cowboy_height:
            cowboy_y = box_y + box_height - cowboy_height
        elif cowboy_y < box_y:
            cowboy_y = box_y

        # purely visual graphics
        pygame.draw.line(gameDisplay, WHITE, (0, DISPLAY_HEIGHT * 0.60), (DISPLAY_WIDTH, DISPLAY_HEIGHT * 0.60))

        # display player HP and cactus HP bars
        for num in range(player_hp):
            hp_bar(bar_x + bar_width * num, bar_y)
        for num in range(cactus_hp):
            enemy_bar(enemy_bar_x + 7 * num, enemy_bar_y)

        # generate horizontal needle fire attack
        needle(needle_x, needle_y)
        needle_x -= needle_speed
        if needle_x <= 0:
            needle_x = cactus_init_x
            needle_y = cactus_init_y + random.randint(-125, 75)
        if player_hitbox.colliderect(needle_hitbox) and not damaged:
            player_hp -= cactus_atk
            damaged = True

        # generate vertical needle attack
        side_needle(side_needle_x, side_needle_y)
        side_needle_y -= side_needle_speed
        if side_needle_y <= -200:
            side_needle_y = box_height + box_y + 20
            side_needle_x = box_x + random.randint(0, 150)
        if player_hitbox.colliderect(side_needle_hitbox) and not damaged:
            player_hp -= cactus_atk
            damaged = True

        # set up invulnerability period after taking damage
        if damaged:
            if invuln_time > 0:
                invuln_time -= 1
            if invuln_time <= 0:
                damaged = False
                invuln_time = cooldown

        # set up heal button and healing mechanic
        heal(heal_x, heal_y)

        # set up fire button and firing mechanic
        fire(fire_x, fire_y)

        # maintain a cross-hair sprite on the player's cursor
        fire_bal = 96 / 2
        heal_bal_x = 40
        heal_bal_y = 20
        if not heal_mode:
            crosshair(pygame.mouse.get_pos()[0] - fire_bal, pygame.mouse.get_pos()[1] - fire_bal)
        else:
            heal_cursor(pygame.mouse.get_pos()[0] - heal_bal_x, pygame.mouse.get_pos()[1] - heal_bal_y)
        # update entire display at a tick rate (FPS)
        pygame.display.update()
        clock.tick(fps)


game_loop()
pygame.quit()
quit()
