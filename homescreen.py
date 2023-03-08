import pygame
import sys

pygame.init()

WINDOW_WIDTH = 480
WINDOW_HEIGHT = 853
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Doodle Jump")

FONT = pygame.font.Font(None, 50)

# backgroundcolor
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

#player
PLAYER_WIDTH = 20
PLAYER_HEIGHT = 20
PLAYER_X = WINDOW_WIDTH // 2 - PLAYER_WIDTH // 2
PLAYER_Y = WINDOW_HEIGHT - PLAYER_HEIGHT
PLAYER_RECT = pygame.Rect(PLAYER_X, PLAYER_Y, PLAYER_WIDTH, PLAYER_HEIGHT)
VELOCITY = 0
GRAVITY = 0.8
IS_JUMPING = False

#platform
PLATFORM_WIDTH = 100
PLATFORM_HEIGHT = 20
PLATFORM_X = WINDOW_WIDTH // 2 - PLATFORM_WIDTH // 2
PLATFORM_Y = WINDOW_HEIGHT // 2
PLATFORM_RECT = pygame.Rect(PLATFORM_X, PLATFORM_Y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


#home screen
def home_screen():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    return

        WINDOW.fill(WHITE)
        play_button = FONT.render("PLAY", True, BLACK)
        play_button_rect = play_button.get_rect(center=WINDOW.get_rect().center)
        WINDOW.blit(play_button, play_button_rect)

        pygame.display.update()



def game_loop():
    global PLAYER_RECT, VELOCITY, IS_JUMPING

    clock = pygame.time.Clock()
    is_running = True

    while is_running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                is_running = False
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and not IS_JUMPING:
            VELOCITY = -15
            IS_JUMPING = True
        elif keys[pygame.K_UP] and IS_JUMPING:
            pass
        else:
            IS_JUMPING = False

        VELOCITY += GRAVITY
        PLAYER_RECT.y += VELOCITY

        if PLAYER_RECT.colliderect(PLATFORM_RECT) and VELOCITY >= 0:
            PLAYER_RECT.bottom = PLATFORM_RECT.top
            VELOCITY = 0
            IS_JUMPING = False

        if PLAYER_RECT.y > WINDOW_HEIGHT:
            is_running = False

      
        WINDOW.fill(RED if PLAYER_RECT.y < PLATFORM_Y else WHITE)
        pygame.draw.rect(WINDOW, BLACK, PLAYER_RECT)
        pygame.draw.rect(WINDOW, BLACK, PLATFORM_RECT)
        pygame.display.update()

        clock.tick(60)

    pygame.quit()


home_screen()
game_loop()
