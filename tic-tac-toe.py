# Fonction pour definir le jeu

def game():

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

game()