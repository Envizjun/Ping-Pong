import pygame
import sys
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import random

# Initialize Pygame
pygame.init()

# Initialize the mixer for music playback
pygame.mixer.init()

# Screen dimensions
screen_width = 800
screen_height = 600

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)

# Paddle dimensions
paddle_width = 10
paddle_height = 100

# Ball dimensions
ball_radius = 7

# Paddle positions
paddle1_x = 50
paddle1_y = (screen_height - paddle_height) // 2
paddle2_x = screen_width - 50 - paddle_width
paddle2_y = (screen_height - paddle_height) // 2

# Ball position and speed
ball_x = screen_width // 2
ball_y = screen_height // 2
ball_speed_x = 3
ball_speed_y = 3
collision_counter = 0

# Paddle speed
paddle_speed = 5

# AI Paddle speed
ai_speed = 4
ai_difficulty_increase_counter = 0

# Score
score1 = 0
score2 = 0

# Volume control
volume = 0.5  # Initial volume
slider_rect = pygame.Rect(screen_width // 2 - 50, 20, 100, 10)
slider_handle_rect = pygame.Rect(screen_width // 2 - 5, 15, 10, 20)

# Screen setup
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Ping Pong Game")

# Font setup
font = pygame.font.Font(None, 36)

# Clock
clock = pygame.time.Clock()

# Game mode
mode = None

def draw_paddles_and_ball(background):
    screen.blit(background, (0, 0))
    pygame.draw.rect(screen, white, (paddle1_x, paddle1_y, paddle_width, paddle_height))
    pygame.draw.rect(screen, white, (paddle2_x, paddle2_y, paddle_width, paddle_height))
    pygame.draw.circle(screen, white, (ball_x, ball_y), ball_radius)

    # Draw volume slider
    pygame.draw.rect(screen, white, slider_rect)
    pygame.draw.rect(screen, red, slider_handle_rect)

    # Draw scores
    score_text = font.render(f"{score1} - {score2}", True, white)
    screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, 50))

    pygame.display.flip()

def move_paddles():
    keys = pygame.key.get_pressed()
    global paddle1_y, paddle2_y

    if keys[pygame.K_w] and paddle1_y > 0:
        paddle1_y -= paddle_speed
    if keys[pygame.K_s] and paddle1_y < screen_height - paddle_height:
        paddle1_y += paddle_speed
    if mode == "PvP":
        if keys[pygame.K_UP] and paddle2_y > 0:
            paddle2_y -= paddle_speed
        if keys[pygame.K_DOWN] and paddle2_y < screen_height - paddle_height:
            paddle2_y += paddle_speed
    elif mode == "PvAI":
        move_ai()

def move_ball():
    global ball_x, ball_y, ball_speed_x, ball_speed_y, score1, score2, collision_counter, ai_speed, ai_difficulty_increase_counter

    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Ball collision with top and bottom
    if ball_y - ball_radius <= 0 or ball_y + ball_radius >= screen_height:
        ball_speed_y *= -1

    # Ball collision with paddles
    if (paddle1_x < ball_x - ball_radius < paddle1_x + paddle_width and
            paddle1_y < ball_y < paddle1_y + paddle_height) or \
            (paddle2_x < ball_x + ball_radius < paddle2_x + paddle_width and
             paddle2_y < ball_y < paddle2_y + paddle_height):
        ball_speed_x *= -1
        collision_counter += 1
        if collision_counter % 4 == 0:
            ball_speed_x *= 1.1
            ball_speed_y *= 1.1
            ai_difficulty_increase_counter += 1
            if ai_difficulty_increase_counter % 2 == 0:
                ai_speed += 0.5

    # Ball out of bounds
    if ball_x - ball_radius <= 0:
        score2 += 1
        reset_ball()
    if ball_x + ball_radius >= screen_width:
        score1 += 1
        reset_ball()

def reset_ball():
    global ball_x, ball_y, ball_speed_x, ball_speed_y, collision_counter
    ball_x, ball_y = screen_width // 2, screen_height // 2
    ball_speed_x = 3 * random.choice([-1, 1])
    ball_speed_y = 3 * random.choice([-1, 1])
    collision_counter = 0

def move_ai():
    global paddle2_y
    if random.randint(0, 10) > 2:  # Add randomness to AI movement
        if paddle2_y + paddle_height / 2 < ball_y:
            paddle2_y += ai_speed
        if paddle2_y + paddle_height / 2 > ball_y:
            paddle2_y -= ai_speed
    if paddle2_y < 0:
        paddle2_y = 0
    if paddle2_y > screen_height - paddle_height:
        paddle2_y = screen_height - paddle_height

def load_music():
    # Tkinter root window for file dialog
    root = Tk()
    root.withdraw()  # Hide the root window

    # File dialog to choose music file
    music_file = askopenfilename(filetypes=[("Music Files", "*.mp3;*.wav")])

    if music_file:
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1)  # Play the music indefinitely

def load_background():
    # Tkinter root window for file dialog
    root = Tk()
    root.withdraw()  # Hide the root window

    # File dialog to choose background file
    background_file = askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])

    if background_file:
        background = pygame.image.load(background_file)
        background = pygame.transform.scale(background, (screen_width, screen_height))
        return background
    else:
        return pygame.Surface((screen_width, screen_height))

def handle_volume_slider(event):
    global volume
    if event.type == pygame.MOUSEBUTTONDOWN and slider_handle_rect.collidepoint(event.pos):
        slider_handle_rect.centerx = event.pos[0]
        volume = (slider_handle_rect.centerx - slider_rect.x) / slider_rect.width
        pygame.mixer.music.set_volume(volume)
    elif event.type == pygame.MOUSEMOTION and event.buttons[0] and slider_handle_rect.collidepoint(event.pos):
        slider_handle_rect.centerx = event.pos[0]
        volume = (slider_handle_rect.centerx - slider_rect.x) / slider_rect.width
        pygame.mixer.music.set_volume(volume)

def show_menu():
    screen.fill(black)
    title = font.render("Ping Pong Game", True, white)
    pvp_option = font.render("1. Player vs Player", True, green)
    pvai_option = font.render("2. Player vs AI", True, green)
    screen.blit(title, (screen_width // 2 - title.get_width() // 2, screen_height // 4))
    screen.blit(pvp_option, (screen_width // 2 - pvp_option.get_width() // 2, screen_height // 2))
    screen.blit(pvai_option, (screen_width // 2 - pvai_option.get_width() // 2, screen_height // 2 + 50))
    pygame.display.flip()

def handle_menu_events():
    global mode
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                mode = "PvP"
            if event.key == pygame.K_2:
                mode = "PvAI"

# Load and play music
load_music()

# Load background
background = load_background()

# Main game loop
while True:
    if mode is None:
        show_menu()
        handle_menu_events()
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            handle_volume_slider(event)

        move_paddles()
        move_ball()
        draw_paddles_and_ball(background)

        clock.tick(60)
