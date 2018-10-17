import pygame

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
hp_bar = display('images/hp_bar.png')
enemy_bar = display('images/enemy_bar.png')
needle = display('images/needle.png')

# set up window display, window text, and in-game clock
gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption('Passion Fruit')
clock = pygame.time.Clock()


def game_loop():
    game_exit = False
    cowboy_init_x, cowboy_init_y = DISPLAY_WIDTH * 0.2, DISPLAY_HEIGHT * 0.2
    cowboy_x, cowboy_y = cowboy_init_x, cowboy_init_y
    cactus_init_x, cactus_init_y = DISPLAY_WIDTH * 0.8, DISPLAY_HEIGHT * 0.3
    cactus_x, cactus_y = cactus_init_x, cactus_init_y

    cowboy_speed = 8

    cowboy_x_change, cowboy_y_change = 0, 0
    box_width, box_height = cowboy_width * 4, cowboy_height * 4
    box_x, box_y = cowboy_init_x - cowboy_width * 2, cowboy_init_y - cowboy_height*1.3

    bar_x, bar_y = 5, DISPLAY_HEIGHT - 100
    enemy_bar_x, enemy_bar_y = bar_x, bar_y - 70
    bar_width = 30
    player_hp, player_atk = 23, 3
    cactus_hp, cactus_atk = 50, 2

    while not game_exit:
        gameDisplay.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    cowboy_x_change += -cowboy_speed
                if event.key == pygame.K_RIGHT:
                    cowboy_x_change += cowboy_speed
                if event.key == pygame.K_UP:
                    cowboy_y_change += -cowboy_speed
                if event.key == pygame.K_DOWN:
                    cowboy_y_change += cowboy_speed

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    cowboy_x_change += cowboy_speed
                if event.key == pygame.K_RIGHT:
                    cowboy_x_change += -cowboy_speed
                if event.key == pygame.K_UP:
                    cowboy_y_change += cowboy_speed
                if event.key == pygame.K_DOWN:
                    cowboy_y_change += -cowboy_speed

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
            if player_hp > 25:
                hp_bar(((DISPLAY_WIDTH - bar_width * 2)/player_hp)*num + bar_x, bar_y)
            else:
                hp_bar(bar_x + 30 * num, bar_y)
        for num in range(cactus_hp):
            if cactus_hp > 25:
                enemy_bar(((DISPLAY_WIDTH - bar_width * 2)/cactus_hp)*num + enemy_bar_x, enemy_bar_y)
            else:
                enemy_bar(enemy_bar_x + 30 * num, enemy_bar_y)

        # maintain a cross-hair sprite on the player's cursor that fires when mouse1 is pressed
        center_bal = 96/2
        if pygame.mouse.get_pressed()[0]:
            crosshair_fired(pygame.mouse.get_pos()[0] - center_bal, pygame.mouse.get_pos()[1] - center_bal)
        else:
            crosshair(pygame.mouse.get_pos()[0] - center_bal, pygame.mouse.get_pos()[1] - center_bal)

        # update entire display at a tick rate (FPS)
        pygame.display.update()
        clock.tick(30)


game_loop()
pygame.quit()
quit()
