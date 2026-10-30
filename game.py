import pygame
import random
import sys

# ============================================================================
# INITIALIZATION & CONSTANTS
# ============================================================================
# Initialize Pygame and font system
pygame.init()
pygame.font.init()

# Screen and FPS constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Color constants (RGB tuples)
BLACK  = (0, 0, 0)
WHITE  = (255, 255, 255)
RED    = (255, 0, 0)
BLUE   = (0, 102, 255)
YELLOW = (255, 255, 0)

# Game object dimensions
PLAYER_WIDTH  = 60
PLAYER_HEIGHT = 30
PLAYER_SPEED  = 7

ENEMY_WIDTH   = 50
ENEMY_HEIGHT  = 40
ENEMY_SPEED   = 4
ENEMY_SPAWN_FRAMES = 40   # Frames between each enemy spawn

# Font objects for text rendering
FONT_LARGE  = pygame.font.Font(None, 72)
FONT_MEDIUM = pygame.font.Font(None, 36)
FONT_SMALL  = pygame.font.Font(None, 24)

# ============================================================================
# MAIN GAME LOOP FUNCTION
# ============================================================================
def game_loop():
    """
    Main game loop that handles all gameplay logic.
    Returns: "restart" to restart, "quit" to quit the program.
    """
    
    # -------------------- GAME SETUP & INITIALIZATION --------------------
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Dodge the Blocks")
    clock = pygame.time.Clock()

    # Player position (starts at bottom center of screen)
    player_x = SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2
    player_y = SCREEN_HEIGHT - PLAYER_HEIGHT - 10

    # Enemy list - each enemy is [x, y] position
    enemies = []

    # Game state variables
    spawn_timer = 0      # Counter for enemy spawning
    score = 0            # Current player score
    game_over = False    # Has the player been hit?
    start_ticks = pygame.time.get_ticks()  # Time tracking for score

    # ================== MAIN GAME LOOP ==================
    running = True
    while running:
        clock.tick(FPS)
        screen.fill(BLACK)

        # ================================================================
        # INPUT HANDLING & GAME OVER LOGIC
        # ================================================================
        # Process all events (quit, keypresses)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Handle Game Over state: R to restart, Q to quit
            if game_over and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "restart"
                if event.key == pygame.K_q:
                    return "quit"

        # Read continuous key presses for player movement (LEFT/RIGHT arrows only)
        keys = pygame.key.get_pressed()
        if not game_over:
            if keys[pygame.K_LEFT]:
                player_x -= PLAYER_SPEED
            if keys[pygame.K_RIGHT]:
                player_x += PLAYER_SPEED
            # Clamp player position to keep within screen bounds
            player_x = max(0, min(player_x, SCREEN_WIDTH - PLAYER_WIDTH))

        # ================================================================
        # UPDATE LOGIC: ENEMY SPAWNING & MOVEMENT
        # ================================================================
        if not game_over:
            # Increment spawn timer and create new enemy at intervals
            spawn_timer += 1
            if spawn_timer >= ENEMY_SPAWN_FRAMES:
                # Spawn enemy at random X position at top of screen
                enemy_x = random.randint(0, SCREEN_WIDTH - ENEMY_WIDTH)
                enemies.append([enemy_x, -ENEMY_HEIGHT])
                spawn_timer = 0

            # Update all enemies: move down and remove if off-screen
            for enemy in enemies[:]:
                enemy[1] += ENEMY_SPEED
                if enemy[1] > SCREEN_HEIGHT:
                    enemies.remove(enemy)

        # ================================================================
        # COLLISION DETECTION (Player hit by enemy = Game Over)
        # ================================================================
        player_rect = pygame.Rect(player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT)
        if not game_over:
            for enemy in enemies:
                enemy_rect = pygame.Rect(enemy[0], enemy[1], ENEMY_WIDTH, ENEMY_HEIGHT)
                if player_rect.colliderect(enemy_rect):
                    game_over = True

        # ================================================================
        # SCORING SYSTEM (Score increases by 1 each second survived)
        # ================================================================
        if not game_over:
            score = (pygame.time.get_ticks() - start_ticks) // 1000

        # ================================================================
        # DRAWING ROUTINE (Render all game objects and UI)
        # ================================================================
        
        # Draw player as blue rectangle at bottom
        pygame.draw.rect(screen, BLUE, (player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT))

        # Draw all falling enemies as red rectangles
        for enemy in enemies:
            pygame.draw.rect(screen, RED, (enemy[0], enemy[1], ENEMY_WIDTH, ENEMY_HEIGHT))

        # Draw current score in top-left corner
        score_surf = FONT_MEDIUM.render(f"Score: {score}", True, WHITE)
        screen.blit(score_surf, (10, 10))

        # Draw on-screen instructions at bottom during gameplay
        if not game_over:
            inst_surf = FONT_SMALL.render("Use LEFT/RIGHT arrows to move. Avoid the red blocks!", True, YELLOW)
            screen.blit(inst_surf, (SCREEN_WIDTH//2 - inst_surf.get_width()//2, SCREEN_HEIGHT - 32))

        # ================================================================
        # GAME OVER STATE (Display final score and restart/quit options)
        # ================================================================
        if game_over:
            # Draw "GAME OVER" title
            over_text = FONT_LARGE.render("GAME OVER", True, RED)
            screen.blit(over_text, (SCREEN_WIDTH//2 - over_text.get_width()//2, 140))

            # Draw reason for game over
            msg_text = FONT_MEDIUM.render("You were hit by a block!", True, WHITE)
            screen.blit(msg_text, (SCREEN_WIDTH//2 - msg_text.get_width()//2, 230))

            # Draw final score
            final_score_surf = FONT_MEDIUM.render(f"Final Score: {score}", True, YELLOW)
            screen.blit(final_score_surf, (SCREEN_WIDTH//2 - final_score_surf.get_width()//2, 320))

            # Draw restart/quit instructions
            restart_surf = FONT_MEDIUM.render("Press R to Restart or Q to Quit.", True, BLUE)
            screen.blit(restart_surf, (SCREEN_WIDTH//2 - restart_surf.get_width()//2, 430))

        # Update display with all drawn objects
        pygame.display.flip()
    # End of game loop

# ============================================================================
# MAIN FUNCTION
# ============================================================================
def main():
    """
    Entry point for the game.
    Sets up and runs the game loop.
    Handles restart logic and quits Pygame cleanly.
    """
    while True:
        result = game_loop()
        if result == "quit":
            break
        # If result is "restart", loop continues and runs game_loop() again
    
    # Clean up and exit
    pygame.quit()
    sys.exit()

# ============================================================================
# PROGRAM ENTRY POINT
# ============================================================================
if __name__ == "__main__":
    main()