import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BROWN = (139, 69, 19)

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dig Dug")

# Load images
player_image = pygame.image.load("player.png")
pooka_image = pygame.image.load("pooka.png")
fygar_image = pygame.image.load("fygar.png")
rock_image = pygame.image.load("rock.png")
bullet_image = pygame.image.load("bullet.png")
dirt_image = pygame.image.load("dirt.png")

# Load sounds
shoot_sound = pygame.mixer.Sound("shoot.wav")
hit_sound = pygame.mixer.Sound("hit.wav")
game_over_sound = pygame.mixer.Sound("game_over.wav")
rock_sound = pygame.mixer.Sound("rock.wav")

# Fonts
score_font = pygame.font.Font(None, 36)
level_font = pygame.font.Font(None, 48)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 2
        self.rect.y = SCREEN_HEIGHT // 2
        self.speed_x = 0
        self.speed_y = 0

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        # Boundary check
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def go_left(self):
        self.speed_x = -5

    def go_right(self):
        self.speed_x = 5

    def go_up(self):
        self.speed_y = -5

    def go_down(self):
        self.speed_y = 5

    def stop(self):
        self.speed_x = 0
        self.speed_y = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        shoot_sound.play()

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - self.rect.height)
        self.speed_x = random.choice([-3, 3])
        self.speed_y = random.choice([-3, 3])
        self.health = 3

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        # Bounce off walls
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.speed_x = -self.speed_x
        if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
            self.speed_y = -self.speed_y

    def hit(self):
        self.health -= 1
        if self.health <= 0:
            self.kill()
            hit_sound.play()

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_image
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self.speed_y = -10

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0:
            self.kill()

# Rock class
class Rock(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = rock_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Dirt class
class Dirt(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = dirt_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Main game loop
def main():
    running = True
    clock = pygame.time.Clock()
    score = 0
    level = 1
    lives = 3

    # Create sprite groups
    global all_sprites, enemies, rocks, bullets, dirt
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    rocks = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    dirt = pygame.sprite.Group()

    # Create player
    player = Player()
    all_sprites.add(player)

    # Create enemies
    for i in range(3):
        enemy = Enemy(pooka_image)
        all_sprites.add(enemy)
        enemies.add(enemy)
    for i in range(2):
        enemy = Enemy(fygar_image)
        all_sprites.add(enemy)
        enemies.add(enemy)

    # Create rocks
    for i in range(5):
        x = random.randint(0, SCREEN_WIDTH - 32)
        y = random.randint(0, SCREEN_HEIGHT - 32)
        rock = Rock(x, y)
        all_sprites.add(rock)
        rocks.add(rock)

    # Create dirt
    for x in range(0, SCREEN_WIDTH, 32):
        for y in range(0, SCREEN_HEIGHT, 32):
            dirt_block = Dirt(x, y)
            all_sprites.add(dirt_block)
            dirt.add(dirt_block)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                elif event.key == pygame.K_RIGHT:
                    player.go_right()
                elif event.key == pygame.K_UP:
                    player.go_up()
                elif event.key == pygame.K_DOWN:
                    player.go_down()
                elif event.key == pygame.K_SPACE:
                    player.shoot()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.speed_x < 0:
                    player.stop()
                elif event.key == pygame.K_RIGHT and player.speed_x > 0:
                    player.stop()
                elif event.key == pygame.K_UP and player.speed_y < 0:
                    player.stop()
                elif event.key == pygame.K_DOWN and player.speed_y > 0:
                    player.stop()

        # Update sprites
        all_sprites.update()

        # Check for bullet-enemy collisions
        hits = pygame.sprite.groupcollide(enemies, bullets, False, True)
        for enemy in hits:
            enemy.hit()
            score += 10

        # Check for player-enemy collisions
        if pygame.sprite.spritecollide(player, enemies, False):
            lives -= 1
            if lives <= 0:
                game_over_sound.play()
                running = False  # End game when lives run out
            else:
                # Reset player and enemy positions
                player.rect.x = SCREEN_WIDTH // 2
                player.rect.y = SCREEN_HEIGHT // 2
                for enemy in enemies:
                    enemy.rect.x = random.randint(0, SCREEN_WIDTH - enemy.rect.width)
                    enemy.rect.y = random.randint(0, SCREEN_HEIGHT - enemy.rect.height)

        # Level up
        if len(enemies) == 0:
            level += 1
            for i in range(level * 3):
                enemy = Enemy(pooka_image)
                all_sprites.add(enemy)
                enemies.add(enemy)
            for i in range(level * 2):
                enemy = Enemy(fygar_image)
                all_sprites.add(enemy)
                enemies.add(enemy)

        # Draw everything
        screen.fill(BLACK)
        dirt.draw(screen)
        all_sprites.draw(screen)

        # Draw score and level
        score_text = score_font.render(f"Score: {score}", True, WHITE)
        level_text = level_font.render(f"Level: {level}", True, WHITE)
        lives_text = score_font.render(f"Lives: {lives}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (SCREEN_WIDTH // 2 - level_text.get_width() // 2, 10))
        screen.blit(lives_text, (SCREEN_WIDTH - 10 - lives_text.get_width(), 10))

        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()