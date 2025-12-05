import random
import pygame

#   CONFIG THEMES
STYLES = {
    "modern": {
        "name": "Moderne",
        "background": (25, 25, 35),
        "grid": (220, 220, 230),
        "x": (255, 105, 97),
        "o": (64, 156, 255),
        "line_width": 4,
        "button_bg": (50, 50, 70),
        "button_hover": (70, 70, 100),
        "button_border": (230, 230, 240),
        "message": (240, 240, 245),
        "font_main": "bahnschrift",
        "font_main_size": 80,
        "font_info": "bahnschrift",
        "font_info_size": 24,
        "grid_margin": 30,
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
        "grid_margin": 25,
    },
    
    "dark": {
        "name": "Dark Futuriste",
        "background": (8, 10, 25),
        "grid": (50, 80, 150),
        "x": (255, 64, 129),
        "o": (3, 218, 198),
        "line_width": 4,
        "button_bg": (15, 20, 45),
        "button_hover": (30, 40, 80),
        "button_border": (3, 218, 198),
        "message": (200, 200, 255),
        "font_main": "calibri",
        "font_main_size": 80,
        "font_info": "calibri",
        "font_info_size": 22,
        "grid_margin": 30,
    },
}

# thème sélectionné
SELECTED_THEME = "modern"

#   INIT PYGAME
AI_level = "Débutant"

Width, Height = 300, 340
pygame.init()
Screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Tic Tac Toe")
Clock = pygame.time.Clock()

# Variables de style
style = None
Background_color = None
Line_color = None
X_color = None
O_color = None
Line_width = None
Button_bg = None
Button_hover = None
Button_border = None
Message_color = None
GRID_MARGIN = None
Font = None
Info_Font = None
GRID_LEFT = None
GRID_TOP = None
GRID_SIZE = None
CELL_SIZE = None


def apply_style(theme_key: str):
    """Applique le thème choisi."""
    global style, Background_color, Line_color, X_color, O_color, Line_width
    global Button_bg, Button_hover, Button_border, Message_color
    global GRID_MARGIN, Font, Info_Font
    global GRID_LEFT, GRID_TOP, GRID_SIZE, CELL_SIZE

    style = STYLES[theme_key]

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

    # grille décalée vers le bas pour laisser la place aux boutons
    GRID_LEFT = GRID_MARGIN
    GRID_TOP = GRID_MARGIN + 40
    GRID_SIZE = Width - 2 * GRID_MARGIN
    CELL_SIZE = GRID_SIZE // 3


# appliquer le thème par défaut
apply_style(SELECTED_THEME)

#   LOGIQUE JEU

WIN_LINES = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6],
]


def is_winner(board, sign):
    for i, j, k in WIN_LINES:
        if board[i] == sign and board[j] == sign and board[k] == sign:
            return True
    return False


def board_full(board):
    return all(cell != " " for cell in board)


def minimax(board, depth, is_maximizing, ai_sign, human_sign, max_depth=None):
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
                best_score = max(best_score, score)
        return best_score
    else:
        best_score = 999
        for i in range(9):
            if board[i] == " ":
                board[i] = human_sign
                score = minimax(board, depth + 1, True, ai_sign, human_sign, max_depth)
                board[i] = " "
                best_score = min(best_score, score)
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
        # essaie de gagner
        for i in empty_cells:
            board[i] = ai_sign
            if is_winner(board, ai_sign):
                board[i] = " "
                return i
            board[i] = " "

        # bloque l'adversaire
        for i in empty_cells:
            board[i] = human_sign
            if is_winner(board, human_sign):
                board[i] = " "
                return i
            board[i] = " "

        return random.choice(empty_cells)

    if AI_level == "Expert":
        # parfois joue "humain" (erreurs)
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
            score = minimax(board, 0, False, ai_sign, human_sign, max_depth=2)
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
            score = minimax(board, 0, False, ai_sign, human_sign, max_depth=None)
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

            text = Font.render(sign, True, X_color if sign == "X" else O_color)
            rect = text.get_rect(center=(cx, cy))
            Screen.blit(text, rect)

    # message en bas
    if message:
        info_surface = Info_Font.render(message, True, Message_color)
        info_rect = info_surface.get_rect(center=(Width // 2, Height - 20))
        Screen.blit(info_surface, info_rect)


def mouse_click(pos):
    x, y = pos
    if x < GRID_LEFT or x > GRID_LEFT + GRID_SIZE:
        return None
    if y < GRID_TOP or y > GRID_TOP + GRID_SIZE:
        return None

    col = (x - GRID_LEFT) // CELL_SIZE
    row = (y - GRID_TOP) // CELL_SIZE
    return row * 3 + col


def draw_button(rect, text, highlighted=False):
    rect_to_draw = rect.copy()
    if highlighted:
        rect_to_draw.inflate_ip(6, 4)

    bg = Button_hover if highlighted else Button_bg
    pygame.draw.rect(Screen, bg, rect_to_draw, border_radius=10)
    pygame.draw.rect(Screen, Button_border, rect_to_draw, 2, border_radius=10)

    label = Info_Font.render(text, True, Message_color)
    label_rect = label.get_rect(center=rect_to_draw.center)
    Screen.blit(label, label_rect)


#   ANIMATIONS DE FIN (traversent l'écran)

def draw_end_animation(result_type):
    """
    Animation différente selon :
    - SELECTED_THEME : modern / retro / dark
    - result_type : "win" ou "draw"
    Toutes les formes traversent la fenêtre d'un bout à l'autre.
    """
    # Thème moderne : projecteurs / faisceaux de lumière
    if SELECTED_THEME == "modern":
        if result_type == "win":
            # Gros faisceaux verticaux du haut jusqu'en bas
            for _ in range(4):
                x = random.randint(-20, Width)
                beam_width = random.randint(25, 45)
                color = random.choice([Line_color, Message_color])
                pygame.draw.rect(Screen, color, (x, 0, beam_width, Height), width=1)
        else:  # match nul
            # Faisceaux diagonaux du haut jusqu'en bas
            for _ in range(3):
                x1 = random.randint(0, Width)
                x2 = random.randint(0, Width)
                color = Line_color
                pygame.draw.line(Screen, color, (x1, 0), (x2, Height), 2)

    # Thème retro : colonnes / scanlines sur toute la hauteur/largeur
    elif SELECTED_THEME == "retro":
        if result_type == "win":
            # Colonnes verticales sur toute la hauteur de la fenêtre
            for _ in range(6):
                x = random.randint(0, Width)
                col_width = random.randint(3, 6)
                color = random.choice([X_color, O_color, Line_color])
                pygame.draw.rect(Screen, color, (x, 0, col_width, Height), width=1)
        else:  # match nul
            # Lignes horizontales qui traversent tout l'écran
            for _ in range(5):
                y = random.randint(0, Height)
                pygame.draw.line(Screen, Line_color, (0, y), (Width, y), 1)

    # Thème dark : lasers et cercles
    elif SELECTED_THEME == "dark":
        if result_type == "win":
            # Lasers partant du bas jusqu'en haut
            for _ in range(6):
                x1 = random.randint(0, Width)
                y1 = Height
                x2 = random.randint(0, Width)
                y2 = 0
                color = random.choice([X_color, O_color])
                pygame.draw.line(Screen, color, (x1, y1), (x2, y2), 2)
        else:  # match nul
            # Cercles concentriques qui atteignent les bords de la fenêtre
            center = (Width // 2, Height // 2)
            max_radius = min(Width, Height) // 2
            for r in range(10, max_radius, 20):
                color = random.choice([Line_color, O_color, X_color])
                pygame.draw.circle(Screen, color, center, r, 1)


#   MENU

def menu_pygame():
    global AI_level, SELECTED_THEME

    mode = None
    step = "theme"
    running = True

    # Boutons thème
    btn_theme1 = pygame.Rect(50, 90, 200, 40)
    btn_theme2 = pygame.Rect(50, 140, 200, 40)
    btn_theme3 = pygame.Rect(50, 190, 200, 40)

    # Bouton retour
    btn_back = pygame.Rect(50, 260, 200, 30)

    # Boutons mode
    btn_pvp = pygame.Rect(50, 120, 200, 45)
    btn_vs_ai = pygame.Rect(50, 180, 200, 45)

    # Boutons difficulté
    btn_diff1 = pygame.Rect(50, 90, 200, 35)
    btn_diff2 = pygame.Rect(50, 135, 200, 35)
    btn_diff3 = pygame.Rect(50, 180, 200, 35)
    btn_diff4 = pygame.Rect(50, 225, 200, 35)

    while running:
        Clock.tick(60)
        Screen.fill(Background_color)

        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos

                # Étape 1 : theme
                if step == "theme":
                    if btn_theme1.collidepoint(mx, my):
                        SELECTED_THEME = "modern"
                        apply_style("modern")
                        step = "mode"

                    if btn_theme2.collidepoint(mx, my):
                        SELECTED_THEME = "retro"
                        apply_style("retro")
                        step = "mode"

                    if btn_theme3.collidepoint(mx, my):
                        SELECTED_THEME = "dark"
                        apply_style("dark")
                        step = "mode"

                # Étape 2 : mode
                elif step == "mode":
                    if btn_back.collidepoint(mx, my):
                        step = "theme"

                    elif btn_pvp.collidepoint(mx, my):
                        mode = 1
                        AI_level = "Débutant"
                        return mode, AI_level

                    elif btn_vs_ai.collidepoint(mx, my):
                        mode = 2
                        step = "difficulty"

                # Étape 3 : difficulté
                elif step == "difficulty":
                    if btn_back.collidepoint(mx, my):
                        step = "theme"

                    elif btn_diff1.collidepoint(mx, my):
                        AI_level = "Débutant"
                        return mode, AI_level
                    elif btn_diff2.collidepoint(mx, my):
                        AI_level = "Intermédiaire"
                        return mode, AI_level
                    elif btn_diff3.collidepoint(mx, my):
                        AI_level = "Expert"
                        return mode, AI_level
                    elif btn_diff4.collidepoint(mx, my):
                        AI_level = "Imbattable"
                        return mode, AI_level

        # Affichage
        title = Info_Font.render(f"Tic Tac Toe - {style['name']}", True, Message_color)
        title_rect = title.get_rect(center=(Width // 2, 40))
        Screen.blit(title, title_rect)

        if step == "theme":
            h1 = btn_theme1.collidepoint(mouse_pos)
            h2 = btn_theme2.collidepoint(mouse_pos)
            h3 = btn_theme3.collidepoint(mouse_pos)

            draw_button(btn_theme1, "Thème moderne", h1)
            draw_button(btn_theme2, "Thème rétro", h2)
            draw_button(btn_theme3, "Thème dark", h3)

            notice = Info_Font.render("Choisissez un thème", True, Message_color)
            Screen.blit(notice, (50, 260))

        elif step == "mode":
            h1 = btn_pvp.collidepoint(mouse_pos)
            h2 = btn_vs_ai.collidepoint(mouse_pos)
            h_back = btn_back.collidepoint(mouse_pos)

            draw_button(btn_pvp, "2 Joueurs", h1)
            draw_button(btn_vs_ai, "Joueur vs IA", h2)
            draw_button(btn_back, "Retour", h_back)

        elif step == "difficulty":
            h1 = btn_diff1.collidepoint(mouse_pos)
            h2 = btn_diff2.collidepoint(mouse_pos)
            h3 = btn_diff3.collidepoint(mouse_pos)
            h4 = btn_diff4.collidepoint(mouse_pos)
            h_back = btn_back.collidepoint(mouse_pos)

            draw_button(btn_diff1, "Débutant", h1)
            draw_button(btn_diff2, "Intermédiaire", h2)
            draw_button(btn_diff3, "Expert", h3)
            draw_button(btn_diff4, "Imbattable", h4)
            draw_button(btn_back, "Retour", h_back)

        pygame.display.flip()


#   BOUCLE DE JEU

def loop_pygame(board, mode):
    current_player = "X"
    game_over = False
    message = f"Tour du joueur X ({style['name']})"
    running = True

    # boutons en haut
    btn_replay = pygame.Rect(30, 5, 110, 30)
    btn_menu = pygame.Rect(160, 5, 110, 30)
    btn_undo = pygame.Rect(95, 40, 110, 25)  # nouveau bouton annuler

    # historique des coups (position, joueur)
    history = []

    # état pour l'animation de fin
    result_type = None  # "win" ou "draw"
    animation_counter = 0  # pour ralentir l'animation

    while running:
        Clock.tick(60)

        # IA joue automatiquement
        if not game_over and mode == 2 and current_player == "O":
            pygame.time.delay(350)
            pos = computer(board, current_player)
            if pos is not False and board[pos] == " ":
                history.append((pos, current_player))  # on sauvegarde le coup de l'IA
                board[pos] = current_player

                if is_winner(board, current_player):
                    message = f"JOUEUR {current_player} A GAGNÉ !!!"
                    game_over = True
                    result_type = "win"
                elif board_full(board):
                    message = "MATCH NUL !!!"
                    game_over = True
                    result_type = "draw"
                else:
                    current_player = "X"
                    message = "Tour du joueur X"

        mouse_pos = pygame.mouse.get_pos()
        hover_replay = btn_replay.collidepoint(mouse_pos)
        hover_menu = btn_menu.collidepoint(mouse_pos)
        hover_undo = btn_undo.collidepoint(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos

                # Bouton MENU toujours actif
                if btn_menu.collidepoint(mx, my):
                    return "MENU"

                # Bouton REJOUER toujours actif
                if btn_replay.collidepoint(mx, my):
                    return "REPLAY"

                # Bouton ANNULER COUP
                if btn_undo.collidepoint(mx, my):
                    if history:
                        last_pos, last_player = history.pop()
                        board[last_pos] = " "
                        # en 2 joueurs : on redonne la main à celui qui vient d'être annulé
                        # en mode IA : on redonne toujours la main au joueur X (humain)
                        if mode == 2:
                            current_player = "X"
                            message = "Tour du joueur X"
                        else:
                            current_player = last_player
                            message = f"Tour du joueur {current_player}"

                        # si on annule après une victoire / match nul, on annule aussi la fin
                        game_over = False
                        result_type = None
                        animation_counter = 0
                    continue

                # Clic sur la grille (uniquement si la partie n'est pas finie)
                if not game_over:
                    if mode == 1 or current_player == "X":
                        index = mouse_click((mx, my))
                        if index is not None and board[index] == " ":
                            history.append((index, current_player))  # on enregistre le coup
                            board[index] = current_player

                            if is_winner(board, current_player):
                                message = f"JOUEUR {current_player} A GAGNÉ !!!"
                                game_over = True
                                result_type = "win"
                            elif board_full(board):
                                message = "MATCH NUL !!!"
                                game_over = True
                                result_type = "draw"
                            else:
                                if mode == 1:
                                    current_player = "O" if current_player == "X" else "X"
                                    message = f"Tour du joueur {current_player}"
                                else:
                                    current_player = "O"
                                    message = "L'ordinateur réfléchit ..."

        # affichage de la grille + message
        display_board(board, message)

        # animation de fin (en continu tant qu'on n'a pas cliqué sur menu/rejouer/annuler)
        if game_over and result_type is not None:
            animation_counter += 1
            # on ne redessine l'animation qu'une frame sur 5 pour la ralentir
            if animation_counter % 5 == 0:
                draw_end_animation(result_type)

        # boutons (toujours visibles)
        draw_button(btn_replay, "Rejouer", hover_replay)
        draw_button(btn_menu, "Menu", hover_menu)
        draw_button(btn_undo, "Annuler", hover_undo)

        pygame.display.flip()

    return None


#   LANCEMENT DU JEU

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
