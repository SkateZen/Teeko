import random
from constante import *
import affichage
import game_rules as game
from player import *


def choix_case(grid, tour, cnv):

    max = -1000
    final_coup = None
    final_piece = None
    list_pos = []

    ordi = Player(grid, game.pion_tour(tour))
    adversaire = Player(grid, game.pion_tour(tour + 1))

    print(ordi.list_pieces)
    print(ordi.token, adversaire.token)

    if tour < 8:

        print("beginning")
        
        choice_list = list_first_cases(grid, adversaire)

        for coup in choice_list:

            (l, c) = coup
            affichage.draw_possible_case(cnv, l, c, "red")
            list_pos.append((l, c))

            grid[l][c] = ordi.token
            ordi.add_piece(coup)

            score = minimax_alpha_beta_first_coups(grid, tour + 1, 6, coup, ordi, adversaire, -1000, 1000)
            print(score)

            grid[l][c] = '_'
            ordi.remove_piece(coup)

            if score > max:
                max = score
                final_coup = coup

        grid[final_coup[0]][final_coup[1]] = ordi.token
        affichage.draw_piece(cnv, final_coup[0], final_coup[1], ordi.token)
        
        game.hide_case(list_pos, cnv)
        return final_coup

    else:

        choice_list = list_all_cases(grid, ordi)

        for coup_piece in choice_list:

            piece, list_coup = coup_piece
            # last_l, last_c = piece

            for coup in list_coup:
                (l, c) = coup
                affichage.draw_possible_case(cnv, l, c, "blue")
                list_pos.append((l, c))

                move_the_piece(coup, piece, grid, ordi)

                score = minimax_alpha_beta(grid, tour + 1, 4, coup, ordi, adversaire, -1000, 1000)
                print(score)

                move_the_piece(piece, coup, grid, ordi)

                if score > max:
                    max = score
                    final_coup = coup
                    final_piece = piece

        move_the_piece(final_coup, final_piece, grid, ordi)
        game.hide_case(list_pos, cnv)
        affichage.remove_piece(cnv, final_piece[0], final_piece[1])
        affichage.draw_piece(cnv, final_coup[0], final_coup[1], ordi.token)

        return final_coup


def minimax_alpha_beta(grid, tour, profondeur, last_case, ordi, adversaire, alpha, beta):

    max = None
    (l, c) = last_case

    if game.victory.victoire_with_case(l, c, grid):

        if game.pion_tour(tour-1) == adversaire.token:  # defaite

            return -100 - profondeur * 10

        else:
            return 100 + profondeur * 10

    elif profondeur < 0:
        return 0

    else:
        if game.pion_tour(tour) == ordi.token:
            #print("ok")

            max = -10000

            choice_list = list_all_cases(grid, ordi)
            #print(choice_list)

            for coup_piece in choice_list:

                piece, list_coup = coup_piece
                #print("ok")
                
                for coup in list_coup:

                    move_the_piece(coup, piece, grid, ordi)

                    score = minimax_alpha_beta(grid, tour + 1, profondeur - 1, coup, ordi, adversaire, alpha, beta)
                    #print("ok")

                    move_the_piece(piece, coup, grid, ordi)

                    if score > max:
                        max = score

                    if score >= beta:
                        return score

                    if score > alpha:
                        alpha = score

        elif game.pion_tour(tour) == adversaire.token:

            max = 10000

            choice_list = list_all_cases(grid, adversaire)

            for coup_piece in choice_list:

                piece, list_coup = coup_piece
                # last_l, last_c = piece

                for coup in list_coup:

                    move_the_piece(coup, piece, grid, adversaire)

                    score = minimax_alpha_beta(grid, tour + 1, profondeur - 1, coup, ordi, adversaire, alpha, beta)

                    move_the_piece(piece, coup, grid, adversaire)

                    if score < max:
                        max = score

                    if score <= alpha:
                        return score

                    if score < beta:
                        beta = score

    return max


def minimax_alpha_beta_first_coups(grid, tour, profondeur, last_case, ordi, adversaire, alpha, beta):
    max = None
    #print(tour)

    if tour >= 8:
        #print(grid)
        #ordi.actu_list_pieces(grid)
        #print(ordi.list_pieces)
        #adversaire.actu_list_pieces(grid)

        score = minimax_alpha_beta(grid, tour, 1, last_case, ordi, adversaire, -100000, 100000)

        #ordi.vide_list_pieces()
        #adversaire.vide_list_pieces()
        #print(score)
        return score
    else:

        (l, c) = last_case

        if game.victory.victoire_with_case(l, c, grid):

            if game.pion_tour(tour - 1) == adversaire.token:  # defaite

                return -100 - profondeur * 10

            else:
                return 100 + profondeur * 10

        elif profondeur < 0:
            return 0

        else:
            if game.pion_tour(tour) == ordi.token:

                max = -1001

                choice_list = list_first_cases(grid, adversaire)

                for coup in choice_list:

                    (l, c) = coup
                    grid[l][c] = ordi.token
                    ordi.add_piece(coup)

                    score = minimax_alpha_beta_first_coups(grid, tour + 1, profondeur - 1, coup, ordi, adversaire,
                                                           alpha, beta)
                    grid[l][c] = '_'
                    ordi.remove_piece(coup)

                    if score > max:
                        max = score

                    if score >= beta:
                        return score

                    if score > alpha:
                        alpha = score

            elif game.pion_tour(tour) == adversaire.token:

                max = 1000

                choice_list = list_first_cases(grid, ordi)

                for coup in choice_list:

                    l, c = coup
                    grid[l][c] = adversaire.token
                    adversaire.add_piece(coup)

                    score = minimax_alpha_beta_first_coups(grid, tour + 1, profondeur - 1, coup, ordi, adversaire,
                                                           alpha, beta)

                    grid[l][c] = '_'
                    adversaire.remove_piece(coup)
                    # print(score)

                    if score < max:
                        max = score

                    if score <= alpha:
                        return score

                    if score < beta:
                        beta = score
        return max
            
    
def move_the_piece(coup, last_case, grid, player):

    ligne, colonne = coup
    last_l, last_c = last_case

    player.list_pieces.remove((last_l, last_c))
    player.list_pieces.append((ligne, colonne))

    grid[last_l][last_c] = '_'
    grid[ligne][colonne] = player.token


def list_all_cases(grid, player):

    list = []

    for i in player.list_pieces:

        (l, c) = i

        list.append((i, list_case(l, c, grid)))

    return list


def list_case(l, c, grid):

    list_pos = []
    for i in range(l-1, l+2):
        for j in range(c-1, c+2):

            if 0 <= i < NB_LINE and 0 <= j < NB_COLUMN and grid[i][j] == '_':
                list_pos.append((i, j))
    return list_pos


def list_first_cases(grid, adversaire):

    list = []

    if adversaire.list_pieces:
        for i in adversaire.list_pieces:
            l, c = i
            tmp_list = list_case(l, c, grid)

            for j in tmp_list:

                if j not in list:
                    list.append(j)
    else:
        list.append((3, 3))

    return list




    













