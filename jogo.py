import numpy as np
import pandas as pd
import random

map_input = {'x': 2, 'o': 1, 'b': 0}
map_output_reverse = {2: 'positive', 1: 'negative', 3: 'tie', 0: 'continue'}


def inicializar_tabuleiro():
    return [[' ' for _ in range(3)] for _ in range(3)]


def mostrar_tabuleiro(tabuleiro):
    for linha in tabuleiro:
        print('|'.join(linha))
        print('-' * 5)
    print('\n')


def atualizar_tabuleiro(tabuleiro, linha, coluna, jogador):
    if tabuleiro[linha][coluna] == ' ':
        tabuleiro[linha][coluna] = jogador
        return True
    return False


def verificar_estado(tabuleiro):
    for i in range(3):
        if tabuleiro[i][0] == tabuleiro[i][1] == tabuleiro[i][2] and tabuleiro[i][0] != ' ':
            return True
    for i in range(3):
        if tabuleiro[0][i] == tabuleiro[1][i] == tabuleiro[2][i] and tabuleiro[0][i] != ' ':
            return True
    if tabuleiro[0][0] == tabuleiro[1][1] == tabuleiro[2][2] and tabuleiro[0][0] != ' ':
        return True
    if tabuleiro[0][2] == tabuleiro[1][1] == tabuleiro[2][0] and tabuleiro[0][2] != ' ':
        return True
    return False



def verificar_estado_ia(model, tabuleiro):
    tabuleiro_flat = np.array(tabuleiro).flatten()

    tabuleiro_flat = [map_input[x.lower()] if x != ' ' else map_input['b'] for x in tabuleiro_flat]

    colunas = [str(i) for i in range(1, 10)]
    tabuleiro_df = pd.DataFrame([tabuleiro_flat], columns=colunas)

    predicao = model.predict(tabuleiro_df)[0]

    return map_output_reverse[predicao]


def jogada_maquina(tabuleiro):
    jogadas_possiveis = [(i, j) for i in range(3) for j in range(3) if tabuleiro[i][j] == ' ']
    if jogadas_possiveis:
        linha, coluna = random.choice(jogadas_possiveis)
        tabuleiro[linha][coluna] = 'O'


def jogar_jogo(model, n_jogadas):
    tabuleiro = inicializar_tabuleiro()
    mostrar_tabuleiro(tabuleiro)
    while True:
        linha = int(input("Escolha a linha (0, 1, 2): "))
        coluna = int(input("Escolha a coluna (0, 1, 2): "))

        if not atualizar_tabuleiro(tabuleiro, linha, coluna, 'X'):
            print("Posição já ocupada, tente novamente.")
            continue

        n_jogadas += 1
        estado_ia = verificar_estado_ia(model, tabuleiro)
        estado = verificar_estado(tabuleiro)
        mostrar_tabuleiro(tabuleiro)
        if estado_ia == "positive":
            print("Previsão do modelo: ")
            print("X venceu")
        elif estado_ia == "tie":
            print("Previsão do modelo: ")
            print("empate")

        if estado:
            print("Estado real do jogo: ")
            print("Jogador X venceu!")
            break
        elif n_jogadas == 5:
            print("Estado real do jogo: ")
            print("O jogo terminou em empate!")
            break

        jogada_maquina(tabuleiro)
        estado_ia = verificar_estado_ia(model, tabuleiro)
        estado = verificar_estado(tabuleiro)
        mostrar_tabuleiro(tabuleiro)
        if estado_ia == "negative":
            print("Previsão do modelo: ")
            print("O venceu")
        elif estado_ia == "tie":
            print("Previsão do modelo: ")
            print("empate")

        if estado:
            print("Estado real do jogo: ")
            print("Jogador O (máquina) venceu!")
            break
