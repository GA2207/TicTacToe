import random

AI_level = "Débutant"

# Fonction pour definir le jeu

def game():
    global AI_level

    board = [" "] * 9

# Affichage du menu

    print("Bienvenue dans le Jeu du TIC TAC TOE")
    print("Choisissez le mode : ")
    print("1 - 2 Joueurs")
    print("2 - Joueurs vs IA")

    mode = (input("Entrez le mode : "))
    try:
        mode = int(mode)
    except:
        mode = 1

    if mode != 1 and mode != 2:
        print("Mode invalide")

    if mode == 2:
        print("\nChoisissez la difficulté de l'IA : ")
        print("1 - Débutant")
        print("2 - Intermédiaire")
        print("3 - Expert")
        print("4 - Imbattable")
    
        diff = input("Entrer la difficulté : ")
        try:
            diff = int(diff)
        except:
            diff = 1
        
        if diff == 1:
            AI_level = "Débutant"
        elif diff == 2:
            AI_level = "Intermédiaire"
        elif diff == 3:
            AI_level = "Expert"
        elif diff == 4:
            AI_level = "Imbattable"
        else:
            AI_level = "Débutant"
        
        print(f"Difficulté choisie : {AI_level.upper()}")

    current_player = "X"
    game_over = False

# Boucle principale du jeu

    while not game_over:

        display_board(board)

        # Mode 2 joueurs

        if mode == 1:
            print(f"C'est au tour du joueur {current_player}")
            position = ask_player_move(board)

        # Mode joueur vs IA
        else:
            if current_player == "X":
                print(f"C'est votre tour {current_player}")
                position = ask_player_move(board)
            else:
                print("L'ordinateur réfléchit ...")
                position = computer(board,current_player)
                if position is False:
                    position = first_empty_cell(board)

        # Vérifiaction du coup

        if position < 0 or position > 8 or board[position] != " ":
            print("Coup invalise, recommencez")
            continue
        
        # Jouer le coup 

        board[position] = current_player

        # Vérifier la victoire

        if is_winner(board,current_player):
            display_board(board)
            print(f"JOUEUR {current_player} À GAGNÉ !!!")
            game_over = True
        
        # Vérifier le match nul

        elif board_full(board):
            display_board(board)
            print("MATCH NUL !!!")
            game_over = True

        # Changement de joueur

        else:
            current_player = "O" if current_player == "X" else "X"
    
    print("FIN DU JEU !!!")

# Condition de victoire

WIN_LINES = [
    [0,1,2], [3,4,5], [6,7,8],
    [0,3,6], [1,4,7], [2,5,8],
    [0,4,8], [2,4,6]
]

# Grille 3x3

def display_board(board):
    print("-------------")
    print(f"| {board[0]} | {board[1]} | {board[2]} |")
    print("-------------")
    print(f"| {board[3]} | {board[4]} | {board[5]} |")
    print("-------------")
    print(f"| {board[6]} | {board[7]} | {board[8]} |")
    print("-------------")

# Demande une position

def ask_player_move(board):
    while True:
        try:
            pos = int(input("Entrer une position en 0 et 8 : "))
            return pos
        except:
            print("Entrer un nombre : ")

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

def minimax(board,depth,is_maximizing,ai_sign,human_sign,max_depth=None):
    if is_winner(board,ai_sign):
        return 10 - depth
    if is_winner(board,human_sign):
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
                score = minimax(board,depth + 1,False,ai_sign,human_sign,max_depth)
                board[i] = " "
                if score > best_score:
                    best_score = score
        return best_score
    
    else:
        best_score = 999
        for i in range(9):
            if board[i] == " ":
                board[i] = human_sign
                score = minimax(board,depth + 1,True,ai_sign,human_sign,max_depth)
                board[i] = " "
                if score < best_score:
                    best_score = score
        return best_score

# Niveaux

def computer(board,current_player):
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
            if is_winner(board,ai_sign):
                board[i] = " "
                return i
            board[i] = " "
        
        for i in empty_cells:
            board[i] = human_sign
            if is_winner(board,human_sign):
                board[i] = " "
                return i
            board[i] = " "

        return random.choice(empty_cells)
    
    # Niveau 3 : expert

    if AI_level == "Expert":
        if random.random() < 0.4:
            for i in empty_cells:
                board[i] = ai_sign
                if is_winner(board,ai_sign):
                    board[i] = " "
                    return i
                board[i] = " "
            
            for i in empty_cells:
                board[i] = human_sign
                if is_winner(board,human_sign):
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
            
        if best_move == None:
            return random.choice(empty_cells)
        return best_move
    
    return random.choice(empty_cells)

game()