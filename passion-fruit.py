import pygame

pygame.init()

# basic game constants
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 800
BLACK = (0, 0, 0)

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
    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
        gameDisplay.fill(BLACK)
        pygame.display.update()
        clock.tick(60)


game_loop()
pygame.quit()
quit()
