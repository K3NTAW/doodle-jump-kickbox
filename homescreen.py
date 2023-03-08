import pygame
import sys

pygame.init()

window_width = 480
window_height = 853
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Doodle Jump")

font = pygame.font.Font(None, 50)

# background color
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# platform
platform_width = 100
platform_height = 20
platform_x = window_width // 2 - platform_width // 2
platform_y = window_height // 2
platform_rect = pygame.Rect(platform_x, platform_y, platform_width, platform_height)

# player
player_width = 20
player_height = 20
player_x = window_width // 2 - player_width // 2
player_y = platform_rect.top - player_height 
player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

# movement variables
move_left = False
move_right = False
player_speed = 5

velocity = 0
gravity = 0.8
is_jumping = False

# home screen
def home_screen():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    return

        window.fill(white)
        play_button = font.render("PLAY", True, black)
        play_button_rect = play_button.get_rect(center=window.get_rect().center)
        window.blit(play_button, play_button_rect)
        pygame.display.update()

# game over screen
def game_over_screen():
    global move_right, move_left, velocity, is_jumping
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if retry_button_rect.collidepoint(event.pos):
                    move_left = False
                    move_right = False
                    velocity = 0
                    is_jumping = False
                    return player_rect
                elif home_button_rect.collidepoint(event.pos):
                    move_left = False
                    move_right = False
                    velocity = 0
                    is_jumping = False
                    home_screen()
                    return player_rect
                
        window.fill(red)
        game_over_text = font.render("Game Over!", True, white)
        game_over_rect = game_over_text.get_rect(center=(window_width/2, window_height/2 - 50))
        window.blit(game_over_text, game_over_rect)
 
        retry_button = font.render("Retry?", True, black, red)
        retry_button_rect = retry_button.get_rect(center=(window_width/2, window_height/2 + 50))
        pygame.draw.rect(window, black, retry_button_rect, 3)
        window.blit(retry_button, retry_button_rect)

        home_button = font.render("Back to Home Screen", True, black, white)
        home_button_rect = home_button.get_rect(center=(window_width/2, window_height/2 + 100))
        pygame.draw.rect(window, black, home_button_rect, 3)
        window.blit(home_button, home_button_rect)
        pygame.display.update()

# game loop
def game_loop():
    global player_rect, velocity, is_jumping, platform_rect, move_left, move_right 
    clock = pygame.time.Clock()
    touch = False 
    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.FINGERDOWN:   
                touch = True     
                x_coordinate, y_coordinate = event.x, event.y 
                player_rect.bottom = y_coordinate

            elif event.type == pygame.FINGERMOTION and touch:
                x_coordinate, y_coordinate = event.x, event.y
                player_rect.bottom = y_coordinate 
    
            elif event.type == pygame.FINGERUP and touch:
                touch = False      

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    move_left = True
                elif event.key == pygame.K_RIGHT:
                    move_right = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    move_left = False
                elif event.key == pygame.K_RIGHT:
                    move_right = False

        if not touch:
            is_jumping = False
  
        if touch and not is_jumping:
            velocity = -15
            is_jumping = True
          
        elif touch and is_jumping:
            pass
        
        else:
            is_jumping = False
          
        velocity += gravity
        player_rect.y += velocity

        if player_rect.colliderect(platform_rect) and velocity >= 0:
            player_rect.bottom = platform_rect.top
            velocity = 0
            is_jumping = False

        if move_left:
            player_rect.x -= player_speed
        if move_right:
            player_rect.x += player_speed

        if player_rect.y < window_height/2:
            platform_rect.centery += abs(velocity)
            player_rect.centery += abs(velocity)

        if player_rect.y > window_height:
            player_rect = game_over_screen()
            velocity = 0
            is_jumping = False

        window.fill(red if player_rect.y < platform_rect.y else white)
        pygame.draw.rect(window, black, player_rect)
        pygame.draw.rect(window, black, platform_rect)
        pygame.display.update()

home_screen()
game_loop()
