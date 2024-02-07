import pygame
import random
import sys

# Initialize Pygame and set up the game window
pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Define colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

# Set up FPS controller and font
clock = pygame.time.Clock()
fps = 30
font = pygame.font.SysFont("arial", 28)

lives = 5  # Initial number of lives for the player

# Basket class to catch falling objects
class Basket:
    def __init__(self):
        self.width = 100
        self.height = 100
        self.x = screen_width / 2 - self.width / 2
        self.y = screen_height - self.height - 20
        self.move_speed = 10

    def draw(self):
        # Draw the basket as a rectangle
        pygame.draw.rect(screen, black, [self.x, self.y, self.width, self.height])

    def move(self, direction):
        # Move the basket within the window boundaries
        if direction == "LEFT" and self.x > 0:
            self.x -= self.move_speed
        if direction == "RIGHT" and self.x < screen_width - self.width:
            self.x += self.move_speed

# FallingObject class for objects that the basket needs to catch
class FallingObject:
    def __init__(self):
        self.x = random.randint(0, screen_width - 20)
        self.y = 0
        # Start with a slower speed
        self.speed = random.randint(1, 4)

    def draw(self):
        # Draw the object as a circle
        pygame.draw.circle(screen, red, (self.x, self.y), 20)

    def fall(self):
        # Update the position of the falling object
        self.y += self.speed

# Main game loop
def game_loop():
    basket = Basket()
    objects = []
    score = 0
    global lives
    start_time = pygame.time.get_ticks()
    object_spawn_rate = 60  # Start with a higher spawn rate for an easier start

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        # Control the basket with arrow keys
        if keys[pygame.K_LEFT]:
            basket.move("LEFT")
        if keys[pygame.K_RIGHT]:
            basket.move("RIGHT")

        # Gradually increase difficulty by spawning objects more frequently and increasing their speed
        if random.randint(1, object_spawn_rate) == 1:
            obj = FallingObject()
            objects.append(obj)
            # Decrease spawn rate and increase speed over time to make the game harder
            object_spawn_rate = max(20, object_spawn_rate - 1)
            obj.speed += score // 10

        screen.fill(white)

        # Check for collisions and update the score
        for obj in objects[:]:
            obj.fall()
            obj.draw()
            if obj.y > screen_height:
                objects.remove(obj)
                lives -= 1
                if lives <= 0:
                    end_time = (pygame.time.get_ticks() - start_time) / 1000
                    print(f"Game Over! Your score: {score}, Time survived: {end_time:.2f} seconds")
                    pygame.quit()
                    sys.exit()
            elif basket.x < obj.x < basket.x + basket.width and basket.y < obj.y + 20 < basket.y + basket.height:
                score += 1
                objects.remove(obj)

        basket.draw()

        # Display score and lives
        current_time = (pygame.time.get_ticks() - start_time) / 1000
        score_text = font.render(f"Score: {score}", True, black)
        lives_text = font.render(f"Lives: {lives}", True, black)
        time_text = font.render(f"Time: {current_time:.2f}", True, black)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 40))
        screen.blit(time_text, (10, 70))

        pygame.display.flip()
        clock.tick(fps)

game_loop()
