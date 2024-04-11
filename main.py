import os
import pygame
import random


pygame.init()

SCREEN_WIDTH = 750
SCREEN_HEIGHT = 750

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Sumo Game')

speed = 10
initial_size = 50
growth_rate = 0.4
max_width = SCREEN_WIDTH
max_height = SCREEN_HEIGHT

running = True
pause = False
lives = 3
player_weight = initial_size

highest_scores = []

# Load image of Sumo.
sumo = pygame.image.load('images/sumo/sumo.png')

# Load images of Enemies.
enemy_type_1 = pygame.image.load('images/enemy/enemy_type_1.png')
enemy_type_2 = pygame.image.load('images/enemy/enemy_type_2.png')
enemy_type_3 = pygame.image.load('images/enemy/enemy_type_3.png')

# Create a list of enemies.
enemy_types = [enemy_type_1, enemy_type_2, enemy_type_3]
active_enemies = []


# Load images of Food.
burger = pygame.image.load('images/bigFoods/burger.png')
fries = pygame.image.load('images/bigFoods/fries.png')
hotdog = pygame.image.load('images/bigFoods/hotdog.png')
pizza = pygame.image.load('images/bigFoods/pizza.png')
soda = pygame.image.load('images/bigFoods/soda.png')

# Create a list of foods.
food_types = [burger, fries, hotdog, pizza, soda]
active_foods = []


# Load images of Rotten Food.
pepper = pygame.image.load('images/rottenFoods/rottenPepper.png')
tomato = pygame.image.load('images/rottenFoods/rottenTomato.png')
steak = pygame.image.load('images/rottenFoods/rottenSteak.png')

# Create a list of rotten foods.
rotten_types = [pepper, tomato, steak]
active_rotten = []

# Load images of Killer Fish.
pufferfish = pygame.image.load('images/killerFoods/pufferfish.png')
pufferfish_type_2 = pygame.image.load('images/killerFoods/pufferfish_type_2.png')
pufferfish_types = [pufferfish, pufferfish_type_2]
active_pufferfish = []

# Load in Soundtrack.
main_theme = pygame.mixer.Sound('soundtrack/ost/main_theme.wav')

# Load in sound effects.
sumo_sound = pygame.mixer.Sound('soundtrack/sfx/sumo_bounce.wav')
food_sound = pygame.mixer.Sound('soundtrack/sfx/food_bounce.wav')
rotten_sound = pygame.mixer.Sound('soundtrack/sfx/rotten_bounce.wav')
pufferfish_sound = pygame.mixer.Sound('soundtrack/sfx/pufferfish_bounce.wav')


clock = pygame.time.Clock()


class Image:
    def __init__(self, x, y, image, scale_min, scale_max, speed_x, speed_y):
        width = image.get_width()
        height = image.get_height()
        scale_enemies = random.uniform(scale_min, scale_max)
        self.original_image = pygame.transform.scale(image, (int(width * scale_enemies), int(height * scale_enemies)))
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed_x = speed_x
        self.speed_y = speed_y

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))


sumo_rect = sumo.get_rect()
sumo_rect.center = (540, 540)
current_size = initial_size
sumo_image = pygame.transform.scale(sumo, (current_size, current_size))

dohyo = pygame.image.load('images/dohyo/dohyo-creative-icon-design-vector.jpg')
dohyo_resize = (750, 750)
dohyo_final_image = pygame.transform.scale(dohyo, dohyo_resize)

hearts = pygame.image.load('images/heart/heart.png')
hearts_resize = (50, 50)
hearts_final_image = pygame.transform.scale(hearts, hearts_resize)


pressed_keys = {'left': False, 'right': False, 'up': False, 'down': False}


def main_menu():
    main_theme.play()
    main_theme.set_volume(0.2)
    menu_font = pygame.font.Font(None, 50)
    title_font = pygame.font.Font(None, 100)
    title_text = title_font.render("ConSumo", True, (255, 255, 255))
    start_text = menu_font.render("Press SPACE to Start", True, (255, 255, 255))
    quit_text = menu_font.render("Press Q to Quit", True, (255, 255, 255))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return game_loop()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        screen.fill((0, 0, 0))
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))
        screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, 250))
        screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, 450))

        pygame.display.flip()
        clock.tick(30)


def pause_menu():
    pause_font = pygame.font.Font(None, 150)
    options_font = pygame.font.Font(None, 50)
    game_name_text = pause_font.render("Paused!", True, (255, 255, 255))
    restart_text = options_font.render("Press SPACE to Resume",  True, (255, 255, 255))
    quit_text = options_font.render("Press Q to Quit", True, (255, 255, 255))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return resume_game()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        screen.fill((0, 0, 0))
        screen.blit(game_name_text, (SCREEN_WIDTH // 2 - game_name_text.get_width() // 2, 50))
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 250))
        screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, 450))

        pygame.display.flip()
        clock.tick(30)


def reset_game():
    global speed, current_size, lives, active_enemies, active_foods, active_rotten, active_pufferfish
    speed = 10
    current_size = initial_size
    lives = 3
    active_enemies = []
    active_foods = []
    active_rotten = []
    active_pufferfish = []
    sumo_rect.center = (375, 375)


def game_over(score):
    global running, pause, highest_scores_updated
    if not highest_scores_updated:
        pause = True
        highest_scores_updated = True
        pause_menu()

    pause_font = pygame.font.Font(None, 150)
    options_font = pygame.font.Font(None, 50)
    game_name_text = pause_font.render("Game Over!", True, (255, 255, 255))
    restart_text = options_font.render("Press SPACE to Restart",  True, (255, 255, 255))
    quit_text = options_font.render("Press Q to Quit", True, (255, 255, 255))
    score_text = options_font.render(f"Score: {round(score, 2)}", True, (255, 255, 255))

    screen.fill((0, 0, 0))
    screen.blit(game_name_text, (SCREEN_WIDTH // 2 - game_name_text.get_width() // 2, 50))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 150))
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 550))
    screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, 650))

    active_enemies.clear()
    active_foods.clear()
    active_rotten.clear()
    active_pufferfish.clear()

    highest_scores.append(score)

    scoreboard(score)

    show_highest_scores()

    pygame.display.flip()
    clock.tick(30)


def scoreboard(score):
    score_path = os.path.dirname(os.path.abspath(__file__))
    if not os.path.exists(score_path):
        os.makedirs(score_path)

    saving_score = os.path.join(score_path, "highest_scores.txt")
    with open(saving_score, 'a+') as file:
        file.seek(0)
        scores = file.readlines()
        scores = [float(s.strip()) for s in scores]

        if score not in scores:
            scores.append(score)
        elif len(scores) < 1:
            scores.append(score)
            scores.sort(reverse=True)

        scores.sort(reverse=True)  # Sort the scores in descending order
        scores = scores[:1]  # Keep only the top 10 scores

        file.seek(0)
        for s in scores:
            rounded_score = round(s, 2)  # Round the score to two decimal places
            file.write(f"{rounded_score:.2f}\n")  # Format the score with two decimal places

    highest_scores.clear()
    highest_scores.extend(scores)


def show_highest_scores():
    font = pygame.font.Font(None, 30)
    text_y = 200
    title_text = font.render("Highest Scores:", True, (255, 255, 255))
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, text_y))
    text_y += 50
    for i, score in enumerate(highest_scores, start=1):
        score_text = font.render(f"{i}. {score}", True, (255, 255, 255))
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, text_y))
        text_y += 30

    pygame.display.flip()


def game_loop():
    global running, lives, pause, speed, current_size, highest_scores_updated
    highest_scores_updated = True
    while True:
        clock.tick(30)
        screen.blit(dohyo_final_image, (0, 0))

        if lives == 3:
            screen.blit(hearts_final_image, (700, 0))
            screen.blit(hearts_final_image, (650, 0))
            screen.blit(hearts_final_image, (600, 0))
        elif lives == 2:
            screen.blit(hearts_final_image, (700, 0))
            screen.blit(hearts_final_image, (650, 0))
        elif lives == 1:
            screen.blit(hearts_final_image, (700, 0))
        else:
            game_over(current_size)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    reset_game()
                    return
                if event.key == pygame.K_LEFT:
                    pressed_keys['left'] = True
                elif event.key == pygame.K_RIGHT:
                    pressed_keys['right'] = True
                elif event.key == pygame.K_UP:
                    pressed_keys['up'] = True
                elif event.key == pygame.K_DOWN:
                    pressed_keys['down'] = True
                if event.key == pygame.K_p and not pause:
                    pause = True
                    pause_menu()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    pressed_keys['left'] = False
                elif event.key == pygame.K_RIGHT:
                    pressed_keys['right'] = False
                elif event.key == pygame.K_UP:
                    pressed_keys['up'] = False
                elif event.key == pygame.K_DOWN:
                    pressed_keys['down'] = False

        if pause:
            continue

        # Update sumo's position based on pressed keys
        if pressed_keys['left']:
            sumo_rect.x -= speed
        if pressed_keys['right']:
            sumo_rect.x += speed
        if pressed_keys['up']:
            sumo_rect.y -= speed
        if pressed_keys['down']:
            sumo_rect.y += speed

        for enemy in active_enemies:
            collision_area = pygame.Rect(sumo_rect.x - 2, sumo_rect.y - 2, sumo_rect.width + 2, sumo_rect.height + 2)
            if collision_area.colliderect(enemy.rect):
                sumo_sound.play()
                if sumo_rect.x < enemy.rect.x:
                    sumo_rect.x -= 35
                    current_size -= growth_rate
                if sumo_rect.x > enemy.rect.x:
                    sumo_rect.x += 35
                    current_size -= growth_rate
                if sumo_rect.y < enemy.rect.y:
                    sumo_rect.y -= 35
                    current_size -= growth_rate
                if sumo_rect.y > enemy.rect.y:
                    sumo_rect.y += 35
                    current_size -= growth_rate

        if random.randint(0, 775) < 3:
            if not pause:
                enemy_image = random.choice(enemy_types)
                enemy_speed = random.randint(1, 8)
                spawn_side = random.choice(['top', 'bottom', 'left', 'right'])
                if spawn_side == 'top':
                    enemy_instance = Image(random.randint(10, SCREEN_WIDTH - 80), -250, enemy_image, 0.2, 0.24, 0,
                                           enemy_speed)
                elif spawn_side == 'bottom':
                    enemy_instance = Image(random.randint(10, SCREEN_WIDTH - 80), SCREEN_HEIGHT + 250, enemy_image, 0.2,
                                           0.24, 0, -enemy_speed)
                elif spawn_side == 'left':
                    enemy_instance = Image(-250, random.randint(10, SCREEN_HEIGHT - 80), enemy_image, 0.2, 0.24,
                                           enemy_speed, 0)
                else:
                    enemy_instance = Image(SCREEN_WIDTH + 250, random.randint(10, SCREEN_HEIGHT - 80), enemy_image, 0.2,
                                           0.24, -enemy_speed, 0)
                active_enemies.append(enemy_instance)

        for enemy in active_enemies:
            if not pause:
                enemy.rect.y += enemy.speed_y
                enemy.rect.x += enemy.speed_x
                enemy.draw()

        for food in active_foods:
            collision_area = pygame.Rect(sumo_rect.x - 1, sumo_rect.y - 1, sumo_rect.width + 1, sumo_rect.height + 1)

            if collision_area.colliderect(food.rect):
                if current_size < max_width and current_size < max_height:
                    food_sound.play()
                    current_size += growth_rate
                    speed -= 0.05
                    if speed <= 1:
                        speed = 1
                active_foods.remove(food)

        if random.randint(0, 150) < 5:
            if not pause:
                food_image = random.choice(food_types)
                food_speed = random.randint(2, 13)
                spawn_side = random.choice(['top', 'bottom', 'left', 'right'])
                if spawn_side in ['top', 'bottom']:
                    food_instance = Image(random.randint(10, SCREEN_WIDTH - 80),
                                          -50 if spawn_side == 'top' else SCREEN_HEIGHT + 50, food_image, 0.05, 0.07, 0,
                                          food_speed if spawn_side == 'top' else -food_speed)
                else:  # spawn_side in ['left', 'right']
                    food_instance = Image(-50 if spawn_side == 'left' else SCREEN_WIDTH + 50,
                                          random.randint(10, SCREEN_HEIGHT - 30), food_image, 0.05, 0.07,
                                          food_speed if spawn_side == 'left' else -food_speed, 0)
                active_foods.append(food_instance)

        for food in active_foods:
            if not pause:
                food.rect.x += food.speed_x
                food.rect.y += food.speed_y
                food.draw()

        for rotten in active_rotten:
            collision_area = pygame.Rect(sumo_rect.x - 1, sumo_rect.y - 1, sumo_rect.width + 1, sumo_rect.height + 1)

            if collision_area.colliderect(rotten.rect):
                rotten_sound.play()
                rotten_sound.set_volume(0.5)
                current_size -= growth_rate
                if current_size <= 49.6:
                    current_size = 50
                    lives -= 1
                active_rotten.remove(rotten)

        if random.randint(0, 200) < 5:
            if not pause:
                rotten_image = random.choice(rotten_types)
                rotten_speed = random.randint(2, 17)
                spawn_side = random.choice(['top', 'bottom', 'left', 'right'])
                if spawn_side in ['top', 'bottom']:
                    rotten_instance = Image(random.randint(10, SCREEN_WIDTH - 80), -50 if spawn_side == 'top' else SCREEN_HEIGHT + 50,
                                            rotten_image, 0.2, 0.3, 0, rotten_speed
                                            if spawn_side == 'top' else -rotten_speed)
                else:
                    rotten_instance = Image(-50 if spawn_side == 'left' else SCREEN_WIDTH + 50,
                                            random.randint(10, SCREEN_HEIGHT - 30), rotten_image, 0.2, 0.3,
                                            rotten_speed if spawn_side == 'left' else -rotten_speed, 0)
                active_rotten.append(rotten_instance)

        for rotten in active_rotten:
            if not pause:
                rotten.rect.x += rotten.speed_x
                rotten.rect.y += rotten.speed_y
                rotten.draw()

        for puffer in active_pufferfish:
            collision_area = pygame.Rect(sumo_rect.x - 1, sumo_rect.y - 1, sumo_rect.width + 1, sumo_rect.height + 1)

            if collision_area.colliderect(puffer.rect):
                pufferfish_sound.play()
                lives -= 1
                active_pufferfish.remove(puffer)

        if random.randint(0, 500) < 5:
            if not pause:
                puffer_image = random.choice(pufferfish_types)
                puffer_speed = random.randint(2, 17)
                spawn_side = random.choice(['top', 'bottom', 'left', 'right'])
                if spawn_side in ['top', 'bottom']:
                    puffer_instance = Image(random.randint(10, SCREEN_WIDTH - 80), -50 if spawn_side == 'top' else SCREEN_HEIGHT + 50,
                                            puffer_image, 0.02, 0.03, 0, puffer_speed
                                            if spawn_side == 'top' else -puffer_speed)
                else:
                    puffer_instance = Image(-50 if spawn_side == 'left' else SCREEN_WIDTH + 50,
                                            random.randint(10, SCREEN_HEIGHT - 30), puffer_image, 0.02, 0.03,
                                            puffer_speed if spawn_side == 'left' else -puffer_speed, 0)
                active_pufferfish.append(puffer_instance)

        for puffer in active_pufferfish:
            if not pause:
                puffer.rect.x += puffer.speed_x
                puffer.rect.y += puffer.speed_y
                puffer.draw()

        # Update the image and rect
        sumo_image = pygame.transform.scale(sumo, (current_size, current_size))
        sumo_rect.size = sumo_image.get_size()

        # Ensure the image stays within the boundaries of the window
        sumo_rect.x = max(0, min(sumo_rect.x, SCREEN_WIDTH - sumo_rect.width))
        sumo_rect.y = max(0, min(sumo_rect.y, SCREEN_HEIGHT - sumo_rect.height))

        fonts = pygame.font.Font(None, 50)
        formatted_weight = f"{current_size:.1f}"
        score_text = fonts.render(f'{formatted_weight} lb', True, (255, 255, 255))

        # Draw the updated image on the screen
        screen.blit(sumo_image, sumo_rect)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()


def resume_game():
    global pause
    pause = False


while running:
    main_menu()
    game_loop()

pygame.quit()
