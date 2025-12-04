import random
import pygame

#   CONFIG THEME
# Choix du thème :
# "modern", "retro", "minimalist", "dark"
SELECTED_THEME = "modern"

STYLES = {
    "modern": {
        "name": "Moderne",
        "background": (25, 25, 35),
        "grid": (220, 220, 230),
        "x": (255, 105, 97),    # rouge pastel
        "o": (64, 156, 255),    # bleu pastel
        "line_width": 4,
        "button_bg": (50, 50, 70),
        "button_hover": (70, 70, 100),
        "button_border": (230, 230, 240),
        "message": (240, 240, 245),
        "font_main": "bahnschrift",
        "font_main_size": 80,
        "font_info": "bahnschrift",
        "font_info_size": 24,
        "grid_margin": 30
    },

    "retro": {
        "name": "Rétro",
        "background": (15, 15, 15),
        "grid": (0, 255, 0),
        "x": (255, 255, 0),
        "o": (0, 255, 255),
        "line_width": 3,
        "button_bg": (10, 40, 10),
        "button_hover": (20, 70, 20),
        "button_border": (0, 255, 0),
        "message": (0, 255, 0),
        "font_main": "consolas",
        "font_main_size": 72,
        "font_info": "consolas",
        "font_info_size": 20,
        "grid_margin": 25
    },
    
    "dark": {
        "name": "Dark Futuriste",
        "background": (8, 10, 25),
        "grid": (50, 80, 150),
        "x": (255, 64, 129),   # rose néon
        "o": (3, 218, 198),    # turquoise néon
        "line_width": 4,
        "button_bg": (15, 20, 45),
        "button_hover": (30, 40, 80),
        "button_border": (3, 218, 198),
        "message": (200, 200, 255),
        "font_main": "calibri",
        "font_main_size": 80,
        "font_info": "calibri",
        "font_info_size": 22,
        "grid_margin": 30
    }
}

#   INIT PYGAME + THEME

AI_level = "Débutant"

Width, Height = 300, 340  # un peu plus haut pour les boutons
pygame.init()
Screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Tic Tac Toe")

Clock = pygame.time.Clock()

# Style courant
style = STYLES.get(SELECTED_THEME, STYLES["modern"])

Background_color = style["background"]
Line_color = style["grid"]
X_color = style["x"]
O_color = style["o"]
Line_width = style["line_width"]
Button_bg = style["button_bg"]
Button_hover = style["button_hover"]
Button_border = style["button_border"]
Message_color = style["message"]
GRID_MARGIN = style["grid_margin"]

Font = pygame.font.SysFont(style["font_main"], style["font_main_size"])
Info_Font = pygame.font.SysFont(style["font_info"], style["font_info_size"])

# Zone de jeu (carré centré)
GRID_LEFT = GRID_MARGIN
GRID_TOP = GRID_MARGIN
GRID_SIZE = Width - 2 * GRID_MARGIN
CELL_SIZE = GRID_SIZE // 3

#   LOGIQUE JEU

WIN_LINES = [
    [0,1,2], [3,4,5], [6,7,8],
    [0,3,6], [1,4,7], [2,5,8],
    [0,4,8], [2,4,6]
]

def is_winner(board, sign):
    for line in WIN_LINES:
        i, j, k = line
        if board[i] == sign and board[j] == sign and board[k] == sign:
            return True
    return False

def board_full(board):
    for cell in board:
        if cell == " ":
            return False
    return True

def minimax(board, depth, is_maximizing, ai_sign, human_sign, max_depth = None):
    if is_winner(board, ai_sign):
        return 10 - depth
    if is_winner(board, human_sign):
        return depth - 10
    if board_full(board):
        return 0
    
    if max_depth is not None and depth >= max_depth:
        return 0
    
    if is_maximizing:
        best_score = -999
        for i in range(9):
            if board[i] == " ":
                board[i] = ai_sign
                score = minimax(board, depth + 1, False, ai_sign, human_sign, max_depth)
                board[i] = " "
                if score > best_score:
                    best_score = score
        return best_score
    else:
        best_score = 999
        for i in range(9):
            if board[i] == " ":
                board[i] = human_sign
                score = minimax(board, depth + 1, True, ai_sign, human_sign, max_depth)
                board[i] = " "
                if score < best_score:
                    best_score = score
        return best_score

def computer(board, current_player):
    ai_sign = current_player
    human_sign = "O" if ai_sign == "X" else "X"
    
    empty_cells = [i for i in range(9) if board[i] == " "]
    if not empty_cells:
        return False
    
    if AI_level == "Débutant":
        return random.choice(empty_cells)
    
    if AI_level == "Intermédiaire":
        for i in empty_cells:
            board[i] = ai_sign
            if is_winner(board, ai_sign):
                board[i] = " "
                return i
            board[i] = " "
        
        for i in empty_cells:
            board[i] = human_sign
            if is_winner(board, human_sign):
                board[i] = " "
                return i
            board[i] = " "

        return random.choice(empty_cells)
    
    if AI_level == "Expert":
        if random.random() < 0.4:
            for i in empty_cells:
                board[i] = ai_sign
                if is_winner(board, ai_sign):
                    board[i] = " "
                    return i
                board[i] = " "
            
            for i in empty_cells:
                board[i] = human_sign
                if is_winner(board, human_sign):
                    board[i] = " "
                    return i
                board[i] = " "

            return random.choice(empty_cells)

        best_score = -999
        move_scores = []

        for i in empty_cells:
            board[i] = ai_sign
            score = minimax(board, 0, False, ai_sign, human_sign, max_depth = 2)
            board[i] = " "
            move_scores.append((i, score))
            if score > best_score:
                best_score = score

        good_moves = [pos for (pos, sc) in move_scores if sc >= best_score - 2]

        return random.choice(good_moves)
    
    if AI_level == "Imbattable":
        best_score = -999
        best_move = None

        for i in empty_cells:
            board[i] = ai_sign
            score = minimax(board, 0, False, ai_sign, human_sign, max_depth = None)
            board[i] = " "
            if score > best_score:
                best_score = score
                best_move = i
            
        if best_move is None:
            return random.choice(empty_cells)
        return best_move
    
    return random.choice(empty_cells)

#   AFFICHAGE

def display_board(board, message=""):
    Screen.fill(Background_color)

    # Grille
    for i in range(1, 3):
        x = GRID_LEFT + i * CELL_SIZE
        pygame.draw.line(Screen, Line_color, (x, GRID_TOP), (x, GRID_TOP + GRID_SIZE), Line_width)
        y = GRID_TOP + i * CELL_SIZE
        pygame.draw.line(Screen, Line_color, (GRID_LEFT, y), (GRID_LEFT + GRID_SIZE, y), Line_width)

    # X / O
    for i in range(9):
        sign = board[i]
        if sign != " ":
            row = i // 3
            col = i % 3
            cx = GRID_LEFT + col * CELL_SIZE + CELL_SIZE // 2
            cy = GRID_TOP + row * CELL_SIZE + CELL_SIZE // 2

            if sign == "X":
                text = Font.render("X", True, X_color)
            else:
                text = Font.render("O", True, O_color)

            rect = text.get_rect(center=(cx, cy))
            Screen.blit(text, rect)

    # Message
    if message:
        info_surface = Info_Font.render(message, True, Message_color)
        info_rect = info_surface.get_rect(center=(Width // 2, Height - 70))
        Screen.blit(info_surface, info_rect)

def mouse_click(pos):
    x, y = pos
    if x < GRID_LEFT or x > GRID_LEFT + GRID_SIZE:
        return None
    if y < GRID_TOP or y > GRID_TOP + GRID_SIZE:
        return None

    col = (x - GRID_LEFT) // CELL_SIZE
    row = (y - GRID_TOP) // CELL_SIZE

    if col < 0 or col > 2 or row < 0 or row > 2:
        return None

    return row * 3 + col

def draw_button(rect, text, highlighted=False):
    bg = Button_hover if highlighted else Button_bg
    pygame.draw.rect(Screen, bg, rect, border_radius=10)
    pygame.draw.rect(Screen, Button_border, rect, 2, border_radius=10)

    label = Info_Font.render(text, True, Message_color)
    label_rect = label.get_rect(center=rect.center)
    Screen.blit(label, label_rect)

#   MENU

def menu_pygame():
    global AI_level

    mode = None
    step = "mode"
    running = True

    btn_pvp = pygame.Rect(50, 120, 200, 45)
    btn_vs_ai = pygame.Rect(50, 180, 200, 45)

    btn_diff1 = pygame.Rect(50, 90, 200, 35)
    btn_diff2 = pygame.Rect(50, 135, 200, 35)
    btn_diff3 = pygame.Rect(50, 180, 200, 35)
    btn_diff4 = pygame.Rect(50, 225, 200, 35)

    while running:
        Clock.tick(60)
        Screen.fill(Background_color)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos

                if step == "mode":
                    if btn_pvp.collidepoint(mx, my):
                        mode = 1
                        AI_level = "Débutant"
                        return mode, AI_level
                    if btn_vs_ai.collidepoint(mx, my):
                        mode = 2
                        step = "difficulty"

                elif step == "difficulty":
                    if btn_diff1.collidepoint(mx, my):
                        AI_level = "Débutant"
                        return mode, AI_level
                    if btn_diff2.collidepoint(mx, my):
                        AI_level = "Intermédiaire"
                        return mode, AI_level
                    if btn_diff3.collidepoint(mx, my):
                        AI_level = "Expert"
                        return mode, AI_level
                    if btn_diff4.collidepoint(mx, my):
                        AI_level = "Imbattable"
                        return mode, AI_level

        title = Info_Font.render("Tic Tac Toe - " + style["name"], True, Message_color)
        title_rect = title.get_rect(center=(Width // 2, 40))
        Screen.blit(title, title_rect)

        if step == "mode":
            draw_button(btn_pvp, "2 Joueurs")
            draw_button(btn_vs_ai, "Joueur vs IA")
        elif step == "difficulty":
            draw_button(btn_diff1, "Débutant")
            draw_button(btn_diff2, "Intermédiaire")
            draw_button(btn_diff3, "Expert")
            draw_button(btn_diff4, "Imbattable")

        pygame.display.flip()

#   BOUCLE DU JEU

def loop_pygame(board, mode):
    current_player = "X"
    game_over = False
    message = "Tour du joueur X (style : " + style["name"] + ")"
    running = True

    btn_replay = pygame.Rect(30, Height - 50, 110, 30)
    btn_menu = pygame.Rect(160, Height - 50, 110, 30)

    while running:
        Clock.tick(60)

        # IA
        if not game_over and mode == 2 and current_player == "O":
            pygame.time.delay(350)
            pos = computer(board, current_player)
            if pos is not False and board[pos] == " ":
                board[pos] = current_player
                if is_winner(board, current_player):
                    message = f"JOUEUR {current_player} A GAGNÉ !!!"
                    game_over = True
                elif board_full(board):
                    message = "MATCH NUL !!!"
                    game_over = True
                else:
                    current_player = "X"
                    message = "Tour du joueur X"

        mouse_pos = pygame.mouse.get_pos()
        hover_replay = btn_replay.collidepoint(mouse_pos)
        hover_menu = btn_menu.collidepoint(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return None

            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_over:
                    mx, my = event.pos
                    if btn_replay.collidepoint(mx, my):
                        return "REPLAY"
                    if btn_menu.collidepoint(mx, my):
                        return "MENU"

                if not game_over:
                    if mode == 1 or current_player == "X":
                        index = mouse_click(event.pos)
                        if index is not None and board[index] == " ":
                            board[index] = current_player

                            if is_winner(board, current_player):
                                message = f"JOUEUR {current_player} A GAGNÉ !!!"
                                game_over = True
                            elif board_full(board):
                                message = "MATCH NUL !!!"
                                game_over = True
                            else:
                                if mode == 1:
                                    current_player = "O" if current_player == "X" else "X"
                                    message = f"Tour du joueur {current_player}"
                                else:
                                    current_player = "O"
                                    message = "L'ordinateur réfléchit ..."

        display_board(board, message)

        if game_over:
            draw_button(btn_replay, "Rejouer", hover_replay)
            draw_button(btn_menu, "Menu", hover_menu)

        pygame.display.flip()

    return None

#   JEU

def game():
    running = True
    mode = None

    while running:
        if mode is None:
            mode, _ = menu_pygame()

        board = [" "] * 9
        result = loop_pygame(board, mode)

        if result == "REPLAY":
            continue

        if result == "MENU":
            mode = None
            continue

        running = False

    pygame.quit()
    print("FIN DU JEU !!!")

if __name__ == "__main__":
    game()
