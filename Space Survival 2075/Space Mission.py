import pygame
import time
import random
pygame.font.init() # pygame.font.init() | this initializes the font module in Pygame
WIDTH, HEIGHT = 800, 600 # width and height are defined
player_width, player_height = 40, 60 # player width and height are defined
player_vel = 5
asteroid_width, asteroid_height = 30, 30 # asteroid width and height are defined
asteroid_vel = 3
font = pygame.font.SysFont("Pool", 50) # pygame.font.SysFont() | this creates a font object with the specified font and size
WIN = pygame.display.set_mode((WIDTH, HEIGHT))# pygame.display.set_mode() | this creates the window with the specified width and height
pygame.display.set_caption("Space Mission") # pygame.display.set_caption() | this sets the title of the window
background = pygame.transform.scale(pygame.image.load("background.jpg"), (WIDTH, HEIGHT)) # pygame.transform.scale() | this used to scale the image to window length
# Load the asteroid image
asteroid_image = pygame.image.load("asteroid.jpg")
asteroid_image = pygame.transform.scale(asteroid_image, (asteroid_width, asteroid_height))  # Scale to match asteroid dimensions

# Load the back button image
back_button_image = pygame.image.load("Back button.jpg")
back_button_image = pygame.transform.scale(back_button_image, (300, 100))  # Scale the back button image

# Load the coin image
coin_image = pygame.image.load("coin.jpg")
coin_image = pygame.transform.scale(coin_image, (30, 30))  # Scale the coin image

# Load the coin stash image
coin_stash_image = pygame.image.load("coin stash.jpg")
coin_stash_image = pygame.transform.scale(coin_stash_image, (50, 50))  # Scale the coin stash image

# Global variable to track total coins collected
total_coins_collected = 0

def draw(player, elapsed_time, asteroids, coins, coin_count):
    WIN.blit(background, (0, 0))  # Draw the background
    score_text = font.render(f"Score: {round(elapsed_time)}", 1, "green")  # Render the score
    coin_text = font.render(f"Coins: {coin_count}", 1, "yellow")  # Render the coin count
    WIN.blit(score_text, (20, 20))  # Draw the score text
    WIN.blit(coin_text, (20, 60))  # Draw the coin count text

    for asteroid in asteroids:
        WIN.blit(asteroid_image, (asteroid.x, asteroid.y))  # Draw the asteroid image

    for coin in coins:
        round_coin = create_round_coin(coin_image, coin.width)  # Create a round coin surface
        WIN.blit(round_coin, (coin.x, coin.y))  # Draw the round coin

    spaceship_image = pygame.image.load("spaceship.jpg")
    WIN.blit(spaceship_image, (player.x, player.y))  # Draw the spaceship
    pygame.display.update()  # Update the display

def wait_for_start():
    global total_coins_collected  # Access the global variable

    # Draw the title
    title_font = pygame.font.SysFont("Pool", 100)
    title_text = title_font.render("Space Mission", 1, "white")
    WIN.blit(background, (0, 0))  # Draw the background
    WIN.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 200))  # Position the title

    # Draw the Start button
    button_font = pygame.font.SysFont("Pool", 60)
    button_text = button_font.render("START", 1, "white")
    button_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2, 300, 100)  # Button dimensions
    pygame.draw.rect(WIN, "green", button_rect)  # Draw the button
    WIN.blit(button_text, (button_rect.x + button_rect.width // 2 - button_text.get_width() // 2,
                           button_rect.y + button_rect.height // 2 - button_text.get_height() // 2))  # Center text

    # Draw the coin stash and total coins collected
    WIN.blit(coin_stash_image, (20, 20))  # Draw the coin stash image at the top-left corner
    total_coins_text = font.render(f"{total_coins_collected}", 1, "yellow")  # Render the total coins count
    WIN.blit(total_coins_text, (80, 30))  # Position the text next to the coin stash

    pygame.display.update()

    # Wait for the user to click the Start button
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:  # Check for mouse click
                if button_rect.collidepoint(event.pos):  # Check if click is inside the Start button
                    waiting = False

def main(start_game=True):
    global total_coins_collected  # Access the global variable
    while True:  # Add a loop to allow restarting the game
        if start_game:  # Only show the start button on the first run
            wait_for_start()  # Wait for the user to start the game
        run = True
        player = pygame.Rect(200, HEIGHT - player_height, player_width, player_height)
        clock = pygame.time.Clock()
        start_time = time.time()
        elapsed_time = 0
        asteroid_add_increment = 150
        asteroid_count = 0
        asteroids = []
        coins = []
        coin_count = 0
        coin_add_increment = 600  # Increased to make coins appear less frequently
        coin_timer = 0
        hit = False
        while run:
            asteroid_count += clock.tick(60) - 10
            coin_timer += clock.get_time()
            elapsed_time = time.time() - start_time

            # Add asteroids
            if asteroid_count >= asteroid_add_increment:
                asteroid_add_increment = random.randint(80, 200)
                for _ in range(2):
                    asteroid_x = random.randint(0, WIDTH - asteroid_width)
                    asteroid = pygame.Rect(asteroid_x, -asteroid_height, asteroid_width, asteroid_height)
                    asteroids.append(asteroid)
                asteroid_count = 0

            # Add coins
            if coin_timer >= coin_add_increment:
                coin_x = random.randint(0, WIDTH - 30)
                coin_y = -30  # Start the coin above the screen
                coin = pygame.Rect(coin_x, coin_y, 30, 30)
                coins.append(coin)
                coin_timer = 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # Pause the game when ESC is pressed
                        pause_game()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player.x - player_vel >= 0:
                player.x -= player_vel
            if keys[pygame.K_RIGHT] and player.x + player_vel + player.width <= WIDTH:
                player.x += player_vel

            # Move asteroids
            for asteroid in asteroids[:]:
                asteroid.y += asteroid_vel
                if asteroid.y > HEIGHT:
                    asteroids.remove(asteroid)
                elif asteroid.y + asteroid.height >= player.y and asteroid.colliderect(player):
                    asteroids.remove(asteroid)
                    hit = True
                    break

            # Move coins
            for coin in coins[:]:
                coin.y += asteroid_vel  # Move the coin down at the same speed as asteroids
                if coin.y > HEIGHT:  # Remove the coin if it goes off the screen
                    coins.remove(coin)
                elif player.colliderect(coin):  # Check for collision with the player
                    coins.remove(coin)
                    coin_count += 1
                    total_coins_collected += 1  # Increment the total coins collected

            if hit:
                draw_explosion(player)  # Show the explosion
                lost = font.render("Game Over!", 1, "white")
                WIN.blit(lost, (WIDTH // 2 - lost.get_width() // 2, HEIGHT // 2 - lost.get_height() // 2))
                pygame.display.update()
                pygame.time.delay(2000)
                action = wait_for_restart_or_home(elapsed_time, coin_count)  # Pass the score and coin count
                if action == "restart":
                    start_game = False  # Skip the start button on restart
                elif action == "home":
                    start_game = True  # Go back to the start button screen
                break  # Exit the game loop to restart or go home
            draw(player, elapsed_time, asteroids, coins, coin_count)

def wait_for_restart_or_home(previous_score, coin_count):
    restart_rect, home_rect = draw_restart_and_home_buttons(previous_score, coin_count)
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:  # Check for mouse click
                if restart_rect.collidepoint(event.pos):  # Check if click is inside the Restart button
                    return "restart"
                if home_rect.collidepoint(event.pos):  # Check if click is inside the Home button
                    return "home"

def draw_restart_and_home_buttons(previous_score, coin_count):
    WIN.blit(background, (0, 0))  # Draw the background
    button_font = pygame.font.SysFont("Pool", 60)
    
    # Display the previous score and coins collected
    score_text = button_font.render(f"Score: {round(previous_score)}", 1, "white")
    coin_text = button_font.render(f"Coins: {coin_count}", 1, "yellow")
    WIN.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 250))  # Position above the buttons
    WIN.blit(coin_text, (WIDTH // 2 - coin_text.get_width() // 2, HEIGHT // 2 - 200))  # Position above the buttons

    # Draw the Restart button
    restart_text = button_font.render("RESTART", 1, "white")
    restart_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 50, 300, 100)  # Restart button dimensions
    pygame.draw.rect(WIN, "red", restart_rect)  # Draw the Restart button
    WIN.blit(restart_text, (restart_rect.x + restart_rect.width // 2 - restart_text.get_width() // 2,
                            restart_rect.y + restart_rect.height // 2 - restart_text.get_height() // 2))  # Center text

    # Draw the Home button using the image
    home_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 100, 300, 100)  # Home button dimensions
    WIN.blit(back_button_image, (home_rect.x, home_rect.y))  # Draw the Home button image

    pygame.display.update()
    return restart_rect, home_rect

def pause_game():
    paused = True
    pause_font = pygame.font.SysFont("Pool", 80)
    pause_text = pause_font.render("PAUSED", 1, "white")
    WIN.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - pause_text.get_height() // 2))
    pygame.display.update()

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Resume the game when ESC is pressed again
                    paused = False

# Load the explosion image
explosion_image = pygame.image.load("Explosion.jpg")
explosion_image = pygame.transform.scale(explosion_image, (player_width * 2, player_height * 2))  # Scale the explosion

def draw_explosion(player):
    # Draw the explosion at the spaceship's position
    WIN.blit(explosion_image, (player.x - player_width // 2, player.y - player_height // 2))  # Center the explosion
    pygame.display.update()
    pygame.time.delay(500)  # Pause for 500ms to show the explosion

def create_round_coin(image, size):
    # Create a circular surface with transparency
    coin_surface = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.circle(coin_surface, (255, 255, 255, 0), (size // 2, size // 2), size // 2)  # Transparent circle
    coin_surface.blit(pygame.transform.scale(image, (size, size)), (0, 0))  # Blit the scaled image onto the surface
    return coin_surface

if __name__ == "__main__":
    main()