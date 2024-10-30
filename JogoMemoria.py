import pygame
import random
import sys

# Inicialização do Pygame
pygame.init()

# Configurações iniciais de tela
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

# Cores padrão
BACKGROUND_COLOR = (50, 168, 82)
CARD_BACK_COLOR = (100, 149, 237)
CARD_FRONT_COLOR = (224, 255, 255)
TEXT_COLOR = (0, 0, 0)
BUTTON_COLOR = (173, 216, 230)
BUTTON_HOVER_COLOR = (135, 206, 235)
BORDER_COLOR = (255, 0, 0)  # Vermelho para a borda das cartas

# Configurações do Jogo
GRID_SIZE = 4  # 4x4 grid
PADDING = 10

# Carregar Cartas
cards = list(range(1, (GRID_SIZE ** 2) // 2 + 1)) * 2
random.shuffle(cards)

# Estado do Jogo
flipped = [False] * len(cards)
first_card_index = None
matches_found = 0
attempts = 0
score = 0

# Temporização
start_time = None
elapsed_time = 0

# Fontes
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 72)

def draw_header(screen):
    # Exibe o tempo e o score no topo da tela
    time_text = f"Tempo: {elapsed_time}s"
    score_text = f"Score: {score}"
    draw_text_top_left(screen, time_text, 10, 10)
    draw_text_top_right(screen, score_text, SCREEN_WIDTH - 150, 10)

def calculate_score():
    # Calcula o score com base no tempo e nas tentativas
    return max(1000 - (elapsed_time * 5 + (attempts - matches_found) * 10), 0)

def draw_board(screen):
    screen.fill(BACKGROUND_COLOR)
    draw_header(screen)
    
    # Tamanho da carta, ajustado para caber sem cortar
    card_width = (SCREEN_WIDTH - (GRID_SIZE + 1) * PADDING) // GRID_SIZE
    card_height = (SCREEN_HEIGHT - (GRID_SIZE + 2) * PADDING - 50) // GRID_SIZE
    board_x = (SCREEN_WIDTH - (card_width * GRID_SIZE + (GRID_SIZE + 1) * PADDING)) // 2
    board_y = 50 + PADDING  # Ajuste para o cabeçalho

    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            index = i * GRID_SIZE + j
            x = board_x + j * (card_width + PADDING) + PADDING
            y = board_y + i * (card_height + PADDING) + PADDING
            if flipped[index]:
                pygame.draw.rect(screen, CARD_FRONT_COLOR, (x, y, card_width, card_height))
                pygame.draw.rect(screen, BORDER_COLOR, (x, y, card_width, card_height), 3)  # Borda vermelha
                draw_text_center(screen, str(cards[index]), x + card_width // 2, y + card_height // 2)
            else:
                pygame.draw.rect(screen, CARD_BACK_COLOR, (x, y, card_width, card_height))
                pygame.draw.rect(screen, BORDER_COLOR, (x, y, card_width, card_height), 3)  # Borda vermelha

def draw_text_center(screen, text, x, y):
    text_surf = font.render(text, True, TEXT_COLOR)
    text_rect = text_surf.get_rect(center=(x, y))
    screen.blit(text_surf, text_rect)

def draw_text_top_left(screen, text, x, y):
    text_surf = font.render(text, True, TEXT_COLOR)
    text_rect = text_surf.get_rect(topleft=(x, y))
    screen.blit(text_surf, text_rect)

def draw_text_top_right(screen, text, x, y):
    text_surf = font.render(text, True, TEXT_COLOR)
    text_rect = text_surf.get_rect(topright=(x, y))
    screen.blit(text_surf, text_rect)

def draw_end_screen(screen):
    screen.fill(BACKGROUND_COLOR)
    congrats_text = "Parabéns!"
    congrats_surf = large_font.render(congrats_text, True, TEXT_COLOR)
    congrats_rect = congrats_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
    screen.blit(congrats_surf, congrats_rect)

    final_score = calculate_score()
    info_text = f"Tempo: {elapsed_time}s   Pontuação: {final_score}"
    info_surf = font.render(info_text, True, TEXT_COLOR)
    info_rect = info_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(info_surf, info_rect)

    play_again_button = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 50, 130, 50)
    quit_button = pygame.Rect(SCREEN_WIDTH // 2 + 20, SCREEN_HEIGHT // 2 + 50, 130, 50)

    mouse_pos = pygame.mouse.get_pos()
    for button, text in [(play_again_button, "Jogar de Novo"), (quit_button, "Fechar")]:
        color = BUTTON_HOVER_COLOR if button.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(screen, color, button)
        button_text = font.render(text, True, TEXT_COLOR)
        button_rect = button_text.get_rect(center=button.center)
        screen.blit(button_text, button_rect)

    return play_again_button, quit_button

def main():
    global SCREEN_WIDTH, SCREEN_HEIGHT, first_card_index, matches_found, attempts, start_time, elapsed_time, flipped, cards, score

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Jogo da Memória")

    clock = pygame.time.Clock()
    running = True
    waiting = False
    timer_start = 0
    game_over = False
    start_time = pygame.time.get_ticks()

    while running:
        screen.fill(BACKGROUND_COLOR)

        # Atualizar o tempo decorrido
        if not game_over:
            elapsed_time = (pygame.time.get_ticks() - start_time) // 1000

        if not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.VIDEORESIZE:
                    SCREEN_WIDTH, SCREEN_HEIGHT = event.size
                    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
                elif event.type == pygame.MOUSEBUTTONDOWN and not waiting:
                    x, y = pygame.mouse.get_pos()
                    card_width = (SCREEN_WIDTH - (GRID_SIZE + 1) * PADDING) // GRID_SIZE
                    card_height = (SCREEN_HEIGHT - (GRID_SIZE + 2) * PADDING - 50) // GRID_SIZE
                    board_x = (SCREEN_WIDTH - (card_width * GRID_SIZE + (GRID_SIZE + 1) * PADDING)) // 2
                    board_y = 50 + PADDING

                    column = (x - board_x) // (card_width + PADDING)
                    row = (y - board_y) // (card_height + PADDING)
                    index = row * GRID_SIZE + column

                    if 0 <= column < GRID_SIZE and 0 <= row < GRID_SIZE and not flipped[index]:
                        if first_card_index is None:
                            first_card_index = index
                            flipped[index] = True
                        else:
                            flipped[index] = True
                            attempts += 1
                            waiting = True
                            timer_start = pygame.time.get_ticks()
            if waiting:
                current_time = pygame.time.get_ticks()
                if current_time - timer_start > 300:
                    if cards[first_card_index] == cards[index]:
                        matches_found += 1
                        score += 50  # Incremento no score para acertos
                    else:
                        flipped[first_card_index] = False
                        flipped[index] = False
                        score -= 5  # Penalidade para erros
                    first_card_index = None
                    waiting = False
            if matches_found == (GRID_SIZE ** 2) // 2:
                game_over = True
        else:
            # Desenhar tela de fim de jogo
            play_again_button, quit_button = draw_end_screen(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if play_again_button.collidepoint(mouse_pos):
                        # Reiniciar o jogo
                        cards = list(range(1, (GRID_SIZE ** 2) // 2 + 1)) * 2
                        random.shuffle(cards)
                        flipped = [False] * len(cards)
                        first_card_index = None
                        matches_found = 0
                        attempts = 0
                        score = 0
                        start_time = pygame.time.get_ticks()
                        game_over = False
                    elif quit_button.collidepoint(mouse_pos):
                        running = False

        if not game_over:
            draw_board(screen)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
