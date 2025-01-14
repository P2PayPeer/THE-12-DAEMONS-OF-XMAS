# Astaroth Mini Game .. Food Fight
# 🏗️ Focus on joy and the contrast between gluttony and temperance.
# 🏗️ Astaroth tempts with excess and joy, testing humanity's resolve against gluttony and temperance.
# 🚧 Astaroth's temptation pertains to the enduring battle against gluttony and the importance of temperance in the face of excessive indulgence. 
# 🚧 It serves as a timeless reminder of the need for moderation.
"""
In another realm, far removed from Lily's magical adventure, lived a fearsome hunter known as Kael. 
His prowess in tracking down prey was legendary, rivaling even that of the great goddess Artemis herself. 
One day, while wandering deep into the heart of a dense forest, Kael stumbled upon an unusual sight – rams frolicking freely among the trees. 
Curiosity piqued, he decided to pursue them, unaware of the mischief brewing around him. 
Suddenly, a booming laugh echoed through the trees, followed closely by the appearance of none other than Astaroth, the Winter Huntress. 
She revealed herself as the true architect behind this grand game, offering Kael a challenge: 
if he could hunt down all the rogue rams and turn them into delicious hamburgers before sunset, he would earn a prize beyond his wildest dreams. 
Agreeing to the terms, Kael embarked on a frantic chase across treacherous terrain, dodging traps and evading obstacles along the way. 
As the hours ticked away, fatigue began to set in, testing both his physical and mental fortitude. 
But driven by the promise of ultimate glory, he pressed on relentlessly, determined to prove himself worthy of Astaroth's favor. 
With the clock counting down towards sundown and victory within reach, only time will tell whether Kael succeeds in claiming his reward or falls victim to Astaroth's deceptively playful nature."
"""
import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 1280, 720
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ramburger Hunt")

# Load images with error handling
def load_image(image_path):
    try:
        return pygame.image.load(image_path)
    except pygame.error as e:
        show_debug_message(f"Error loading image {image_path}: {e}")
        return None

# Display debug message on the screen
def show_debug_message(message):
    debug_daemon_image = load_image('../IMG/DEBUG/debug_daemon.png')
    screen.blit(debug_daemon_image, (50, 50))
    font = pygame.font.Font(None, 36)
    text = font.render(message, True, (255, 0, 0))
    screen.blit(text, (100, 150))
    pygame.display.flip()
    time.sleep(5)

# Load images
kael_image = load_image('../IMG/CHAR/kael_sprite.png')
ram_image = load_image('../IMG/NPC/ram_sprite.png')
background_image = load_image('../IMG/BACKGROUND/forest_background.png')
powerup_image = load_image('../IMG/SPRITE/powerup_sprite.png')  # Power-up sprite

# Game variables
kael_position = [width // 2, height // 2]
ram_positions = [[random.randrange(width), random.randrange(height)] for _ in range(5)]
powerup_positions = [[random.randrange(width), random.randrange(height)] for _ in range(3)]  # Power-up positions
caught_rams = 0
start_time = time.time()
game_duration = 300  # 5 minutes in seconds
kael_stamina = 100  # Kael's initial stamina

# Font for displaying text
font = pygame.font.Font(None, 36)

def draw_text(text, position):
    text_surface = font.render(text, True, (255, 255, 255))
    screen.blit(text_surface, position)

def manage_stamina():
    global kael_stamina
    # Decrease stamina as Kael moves
    kael_stamina -= 0.1  # Adjust the rate as needed
    kael_stamina = max(kael_stamina, 0)

def collect_powerup():
    global kael_stamina
    for powerup_position in powerup_positions[:]:
        if pygame.Rect(kael_position[0], kael_position[1], kael_image.get_width(), kael_image.get_height()).colliderect(
            pygame.Rect(powerup_position[0], powerup_position[1], powerup_image.get_width(), powerup_image.get_height())):
            powerup_positions.remove(powerup_position)
            kael_stamina = min(kael_stamina + 20, 100)  # Increase stamina

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        kael_position[0] -= 5
    if keys[pygame.K_RIGHT]:
        kael_position[0] += 5
    if keys[pygame.K_UP]:
        kael_position[1] -= 5
    if keys[pygame.K_DOWN]:
        kael_position[1] += 5

    manage_stamina()
    collect_powerup()

    # Ram catching logic
    for ram_position in ram_positions[:]:
        if pygame.Rect(kael_position[0], kael_position[1], kael_image.get_width(), kael_image.get_height()).colliderect(
            pygame.Rect(ram_position[0], ram_position[1], ram_image.get_width(), ram_image.get_height())):
            ram_positions.remove(ram_position)
            caught_rams += 1
            # Launch hamburger transformation mini-game

    # Draw everything
    screen.blit(background_image, (0, 0))
    for ram_position in ram_positions:
        screen.blit(ram_image, ram_position)
    for powerup_position in powerup_positions:
        screen.blit(powerup_image, powerup_position)  # Draw power-ups
    screen.blit(kael_image, kael_position)

    # Display caught rams, timer, and Kael's stamina
    elapsed_time = time.time() - start_time
    remaining_time = max(game_duration - int(elapsed_time), 0)
    draw_text(f"Rams Caught: {caught_rams}", (10, 10))
    draw_text(f"Time Left: {remaining_time}", (10, 40))
    draw_text(f"Stamina: {kael_stamina}", (10, 70))

    # Check for game end conditions
    # if remaining_time == 0 or kael_stamina //FRAG?
    if remaining_time == 0 or kael_stamina <= 0:
        show_debug_message("Game Over! Try Again.")
        running = False
    elif caught_rams == len(ram_positions):
        show_debug_message("Congratulations! You've won!")
        running = False

    pygame.display.flip()

pygame.quit()
