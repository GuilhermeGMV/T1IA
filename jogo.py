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


def escolher_dificuldade():
    while True:
        try:
            escolha = int(input("Escolha o nível de dificuldade (1: Fácil, 2: Médio, 3: Difícil): "))
            if escolha in [1, 2, 3]:
                return escolha
            else:
                print("Escolha inválida. Tente novamente.")
        except ValueError:
            print("Escolha inválida. Tente novamente.")


def escolher_simbolo():
    while True:
        escolha = input("Escolha seu símbolo (X/O): ").upper()
        if escolha in ['X', 'O']:
            return escolha
        else:
            print("Escolha inválida. Tente novamente.")


def atualizar_tabuleiro(tabuleiro, linha, coluna, jogador):
    if tabuleiro[linha][coluna] == ' ':
        tabuleiro[linha][coluna] = jogador
        return True
    return False


def verificar_estado(tabuleiro):
    for i in range(3):
        if tabuleiro[i][0] == tabuleiro[i][1] == tabuleiro[i][2] and tabuleiro[i][0] != ' ':
            return True
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


def minimax(tabuleiro, profundidade, is_maximizing, jogador_ia, jogador_humano):
    if verificar_estado(tabuleiro):
        return profundidade - 10 if is_maximizing else 10 - profundidade
    elif all(cell != ' ' for row in tabuleiro for cell in row):
        return 0

    if is_maximizing:
        melhor_pontuacao = float('inf')
        for i in range(3):
            for j in range(3):
                if tabuleiro[i][j] == ' ':
                    tabuleiro[i][j] = jogador_humano
                    pontuacao = minimax(tabuleiro, profundidade + 1, False, jogador_ia, jogador_humano)
                    tabuleiro[i][j] = ' '
                    melhor_pontuacao = min(melhor_pontuacao, pontuacao)
        return melhor_pontuacao
    else:
        melhor_pontuacao = -float('inf')
        for i in range(3):
            for j in range(3):
                if tabuleiro[i][j] == ' ':
                    tabuleiro[i][j] = jogador_ia
                    pontuacao = minimax(tabuleiro, profundidade + 1, True, jogador_ia, jogador_humano)
                    tabuleiro[i][j] = ' '
                    melhor_pontuacao = max(melhor_pontuacao, pontuacao)
        return melhor_pontuacao


def jogada_maquina(tabuleiro, jogador_ia, jogador_humano, dificuldade):
    usar_minimax = False

    if dificuldade == 1:
        usar_minimax = random.random() < 0.25
    elif dificuldade == 2:
        usar_minimax = random.random() < 0.50
    elif dificuldade == 3:
        usar_minimax = True

    if usar_minimax:
        melhor_pontuacao = float('inf')
        melhor_jogada = None

        for i in range(3):
            for j in range(3):
                if tabuleiro[i][j] == ' ':
                    tabuleiro[i][j] = jogador_ia
                    pontuacao = minimax(tabuleiro, 0, True, jogador_ia, jogador_humano)
                    tabuleiro[i][j] = ' '
                    if pontuacao < melhor_pontuacao:
                        melhor_pontuacao = pontuacao
                        melhor_jogada = (i, j)

        if melhor_jogada:
            linha, coluna = melhor_jogada
            tabuleiro[linha][coluna] = jogador_ia
    else:
        jogadas_possiveis = [(i, j) for i in range(3) for j in range(3) if tabuleiro[i][j] == ' ']
        if jogadas_possiveis:
            linha, coluna = random.choice(jogadas_possiveis)
            tabuleiro[linha][coluna] = jogador_ia


def jogar_jogo(model):
    tabuleiro = inicializar_tabuleiro()
    jogador_escolha = escolher_simbolo()
    dificuldade = escolher_dificuldade()
    jogador_ia = 'O' if jogador_escolha == 'X' else 'X'
    jogador_humano = jogador_escolha
    turno_jogador = jogador_humano == 'X'
    n_jogadas = 0

    mostrar_tabuleiro(tabuleiro)

    while True:
        if turno_jogador:
            linha = int(input("Escolha a linha (0, 1, 2): "))
            coluna = int(input("Escolha a coluna (0, 1, 2): "))

            if not atualizar_tabuleiro(tabuleiro, linha, coluna, jogador_humano):
                print("Posição já ocupada, tente novamente.")
                continue

            n_jogadas += 1
            estado_ia = verificar_estado_ia(model, tabuleiro)
            estado = verificar_estado(tabuleiro)
            mostrar_tabuleiro(tabuleiro)

            if estado_ia == "continue":
                print("Previsão do modelo: ")
                print("Continue")
            elif estado_ia == "positive":
                print("Previsão do modelo: ")
                print("X venceu")
            elif estado_ia == "negative":
                print("Previsão do modelo: ")
                print("O venceu")
            elif estado_ia == "tie":
                print("Previsão do modelo: ")
                print("empate")

            if estado:
                print("Estado real do jogo: ")
                print(f"Jogador {jogador_humano} venceu!")
                break
            elif n_jogadas == 9:
                print("Estado real do jogo: ")
                print("O jogo terminou em empate!")
                break
        else:
            jogada_maquina(tabuleiro, jogador_ia, jogador_humano, dificuldade)
            n_jogadas += 1
            estado_ia = verificar_estado_ia(model, tabuleiro)
            estado = verificar_estado(tabuleiro)
            mostrar_tabuleiro(tabuleiro)

            if estado_ia == "continue":
                print("Previsão do modelo: ")
                print("Continue")
            elif estado_ia == "positive":
                print("Previsão do modelo: ")
                print("X venceu")
            elif estado_ia == "negative":
                print("Previsão do modelo: ")
                print("O venceu")
            elif estado_ia == "tie":
                print("Previsão do modelo: ")
                print("empate")

            if estado:
                print("Estado real do jogo: ")
                print(f"Jogador {jogador_ia} venceu!")
                break
            elif n_jogadas == 9:
                print("Estado real do jogo: ")
                print("O jogo terminou em empate!")
                break
        turno_jogador = not turno_jogador
