import random
import pygame

AI_level = "Débutant"

# Pygame (paramètres de la fenêtre)

Width, Height = 300, 300
Line_width = 4
Background_color = (30, 30, 30)
Line_color = (200, 200, 200)
X_color = (200, 50, 50)
O_color = (50, 50, 200)

pygame.init()
Screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Tic Tac Toe")
Font = pygame.font.SysFont(None, 80)
Info_Font = pygame.font.SysFont(None, 30)
Clock = pygame.time.Clock()


# Condition de victoire

WIN_LINES = [
    [0,1,2], [3,4,5], [6,7,8],
    [0,3,6], [1,4,7], [2,5,8],
    [0,4,8], [2,4,6]
]

# Déclaration du vainqueur

def is_winner(board, sign):
    for line in WIN_LINES:
        i, j, k = line
        if board[i] == sign and board[j] == sign and board[k] == sign:
            return True
    return False

# Vérifier si le plateau est plein

def board_full(board):
    for cell in board:
        if cell == " ":
            return False
    return True

#  Cherche la 1ère case vide

def first_empty_cell(board):
    for i in range(9):
        if board[i] == " ":
            return i
    return -1

# IA : minimax

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

# Niveaux

def computer(board, current_player):
    ai_sign = current_player
    human_sign = "O" if ai_sign == "X" else "X"
    
    empty_cells = [i for i in range(9) if board[i] == " "]
    if not empty_cells:
        return False
    
    # Niveau 1 : debutant

    if AI_level == "Débutant":
        return random.choice(empty_cells)
    
    # Niveau 2 : intermédiaire

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
    
    # Niveau 3 : expert

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
    
    # Niveau 4 : imbattable

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

# Grille 3x3

def display_board(board, message=""):
    Screen.fill(Background_color)

    pygame.draw.line(Screen, Line_color, (Width // 3, 0), (Width // 3, Height), Line_width)
    pygame.draw.line(Screen, Line_color, (2 * Width // 3, 0), (2 * Width // 3, Height), Line_width)

    pygame.draw.line(Screen, Line_color, (0, Height // 3), (Width, Height // 3), Line_width)
    pygame.draw.line(Screen, Line_color, (0, 2 * Height // 3), (Width, 2 * Height // 3), Line_width)

    cell_w = Width // 3
    cell_h = Height // 3

    for i in range(9):
        sign = board[i]
        if sign != " ":
            row = i // 3
            col = i % 3
            x = col * cell_w + cell_w // 2
            y = row * cell_h + cell_h // 2

            if sign == "X":
                text = Font.render("X", True, X_color)
            else:
                text = Font.render("O", True, O_color)

            rect = text.get_rect(center=(x, y))
            Screen.blit(text, rect)

    if message:
        info_surface = Info_Font.render(message, True, (255, 255, 255))
        Screen.blit(info_surface, (10, Height - 25))

    pygame.display.flip()

# Interaction avec la souris

def mouse_click(pos):
    x, y = pos
    cell_w = Width // 3
    cell_h = Height // 3
    col = x // cell_w
    row = y // cell_h
    if col < 0 or col > 2 or row < 0 or row > 2:
        return None
    return row * 3 + col

# Dessin d'un bouton

def draw_button(rect, text, highlighted=False):
    color = (70, 70, 70) if not highlighted else (100, 100, 100)
    pygame.draw.rect(Screen, color, rect)
    pygame.draw.rect(Screen, (200, 200, 200), rect, 2)

    label = Info_Font.render(text, True, (255, 255, 255))
    label_rect = label.get_rect(center=rect.center)
    Screen.blit(label, label_rect)

# Menu Pygame : choix du mode et de la difficulté

def menu_pygame():
    global AI_level

    mode = None
    step = "mode"  # "mode" puis éventuellement "difficulty"
    running = True

    # Rectangles des boutons
    btn_pvp = pygame.Rect(50, 100, 200, 50)
    btn_vs_ai = pygame.Rect(50, 170, 200, 50)

    btn_diff1 = pygame.Rect(50, 80, 200, 40)
    btn_diff2 = pygame.Rect(50, 130, 200, 40)
    btn_diff3 = pygame.Rect(50, 180, 200, 40)
    btn_diff4 = pygame.Rect(50, 230, 200, 40)

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
                        AI_level = "Débutant"  # pas utilisé en mode 1 mais on met une valeur par défaut
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

        # Affichage du menu
        if step == "mode":
            title = Info_Font.render("Choisissez le mode", True, (255, 255, 255))
            Screen.blit(title, (60, 40))

            draw_button(btn_pvp, "2 Joueurs")
            draw_button(btn_vs_ai, "Joueur vs IA")

        elif step == "difficulty":
            title = Info_Font.render("Difficulte IA", True, (255, 255, 255))
            Screen.blit(title, (80, 40))

            draw_button(btn_diff1, "Debutant")
            draw_button(btn_diff2, "Intermediaire")
            draw_button(btn_diff3, "Expert")
            draw_button(btn_diff4, "Imbattable")

        pygame.display.flip()

# Boucle avec pygame

def loop_pygame(board, mode):
    current_player = "X"
    game_over = False
    message = "Tour du joueur X"
    running = True

    while running:
        Clock.tick(60)

        # IA en mode joueur vs IA
        if not game_over and mode == 2 and current_player == "O":
            pygame.time.delay(400)
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

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
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

    pygame.quit()

# Fonction pour definir le jeu

def game():
    board = [" "] * 9

    # Menu graphique pour choisir le mode et la difficulté
    mode, _ = menu_pygame()

    # Boucle principale du jeu
    loop_pygame(board, mode)

    print("FIN DU JEU !!!")

if __name__ == "__main__":
    game()
