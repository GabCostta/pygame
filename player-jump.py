import pgzrun
import random
from pygame import Rect
from pgzero.builtins import keyboard, keys
import pygame
from pygame import mixer

# Inicializar o mixer do pygame para música de fundo
mixer.init()
mixer.music.load("music/background_music.mp3")
mixer.music.play(-1)
mixer.music.set_volume(0.5)

WIDTH = 800
HEIGHT = 600
TITLE = "Player Jump!"

game_state = "menu"

class Player:
    def __init__(self, x, y):
        self.image = "player"
        self.rect = Rect(x, y, 50, 50)
        self.vx = 0
        self.vy = 0
        self.on_ground = False

    def move(self):
        # Atualiza a posição do jogador e aplica gravidade
        self.vy += 0.5
        self.rect.x += self.vx
        self.rect.y += self.vy

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

        if self.rect.bottom > HEIGHT - 50:
            self.rect.bottom = HEIGHT - 50
            self.vy = 0
            self.on_ground = True

    def jump(self):
        # Permite que o jogador pule se estiver no chão
        if self.on_ground:
            self.vy = -15
            self.on_ground = False

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

class Enemy:
    def __init__(self, x, y):
        self.image_base = "meanie"
        self.type = random.randint(0, 2)
        self.image = f"{self.image_base}0{self.type}"
        self.rect = Rect(x, y, 50, 50)
        self.direction = random.choice([-1, 1])
        self.animation_frame = 0
        self.speed = random.randint(2, 4)

    def move(self):
        # Move o inimigo e alterna a direção ao atingir as bordas
        self.rect.x += self.direction * self.speed
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.direction *= -1

        self.animation_frame = (self.animation_frame + 1) % 2
        self.image = f"{self.image_base}{self.animation_frame}{self.type}"

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

player = Player(WIDTH // 2 - 25, HEIGHT - 100)
player.health = 3

initial_enemy_count = 3
enemies = [Enemy(random.randint(200, WIDTH - 200), HEIGHT - 100) for _ in range(initial_enemy_count)]

bullet = Actor("bullet")
bullet.alive = False
bullet.speed = 10

player_lives = 3
score = 0
meanie_spawn_rate = 100

def reset_game():
    # Reinicia o estado do jogo
    global score, meanie_spawn_rate, background_y, player_lives
    player.rect.x, player.rect.y = WIDTH // 2, HEIGHT - player.rect.height
    player.health = 3
    bullet.alive = False
    background_y = 0
    if player_lives > 0:
        player_lives -= 1
    else:
        score = 0
        meanie_spawn_rate = 100
        player_lives = 3

def draw():
    screen.clear()
    if game_state == "menu":
        draw_menu()
    elif game_state == "playing":
        draw_game()
        for i in range(player_lives):
            screen.blit("health", (WIDTH - (i + 1) * 30, HEIGHT - 30))
    elif game_state == "game_over":
        draw_game_over()

def draw_menu():
    # Desenha o menu inicial
    screen.clear()
    screen.draw.text("Player Jump!", center=(WIDTH // 2, HEIGHT // 4), fontsize=50, color="white")
    screen.draw.text("Press SPACE to Start", center=(WIDTH // 2, HEIGHT // 2), fontsize=30, color="white")
    screen.draw.text("Press Q to Quit", center=(WIDTH // 2, HEIGHT // 2 + 100), fontsize=30, color="white")

def draw_game():
    # Desenha o jogo em andamento
    screen.fill((135, 206, 235))
    screen.draw.filled_rect(Rect(0, HEIGHT - 50, WIDTH, 50), (34, 139, 34))
    player.draw()
    for enemy in enemies:
        enemy.draw()

def draw_game_over():
    # Desenha a tela de GAME OVER
    screen.clear()
    screen.draw.text("GAME OVER", center=(WIDTH // 2, HEIGHT // 2), fontsize=50, color="red")
    screen.draw.text("Press SPACE to Restart", center=(WIDTH // 2, HEIGHT // 2 + 50), fontsize=30, color="white")

def update():
    # Atualiza o estado do jogo
    global game_state, player_lives

    if game_state == "menu":
        if keyboard.space:
            game_state = "playing"
        elif keyboard.q:
            exit()
    elif game_state == "playing":
        player.move()
        for enemy in enemies:
            enemy.move()

        for enemy in enemies:
            if player.rect.colliderect(enemy.rect):
                player_lives -= 1  # Perde uma vida
                if player_lives <= 0:
                    game_state = "game_over"  # Vai para o estado de GAME OVER
                else:
                    reset_game()  # Reinicia o jogo com vidas restantes
    elif game_state == "game_over":
        if keyboard.space:
            reset_game()
            game_state = "menu"  # Retorna ao menu para reiniciar o jogo

def on_key_down(key):
    # Gerencia eventos de pressionamento de teclas
    if key == keys.SPACE and not bullet.alive and player.health > 0:
        bullet.alive = True
        bullet.pos = (player.rect.x, player.rect.y)
    if key == keys.UP:
        player.jump()
    if key == keys.LEFT:
        player.vx = -5
    if key == keys.RIGHT:
        player.vx = 5

def on_key_up(key):
    # Gerencia eventos de soltura de teclas
    if key == keys.LEFT or key == keys.RIGHT:
        player.vx = 0

def move_player():
    # Move o jogador e reinicia o jogo se necessário
    if player.health <= 0:
        if keyboard.RETURN:
            reset_game()
        return

    if keyboard.left:
        player.x -= EAGLE_SPEED
    elif keyboard.right:
        player.x += EAGLE_SPEED
    player.x = min(WIDTH, max(0, player.x))

pgzrun.go()
