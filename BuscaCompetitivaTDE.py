
# In[1]:


import numpy as np
import random
import time


# Verificação de Vitória:
# 
# Se o jogador vence (ou seja, completa uma linha, coluna ou diagonal), a função pode retornar um valor heurístico alto, indicando uma vitória. Isso poderia ser, por exemplo, +10 pontos.
# 
# Se o oponente vence, a função pode retornar um valor heurístico baixo, como -10 pontos.
# 
# Se Nenhuma Vitória Ocorre:
# 
# Se nenhuma vitória foi detectada para nenhum dos jogadores, a função então analisa o tabuleiro contando as marcas nas linhas, colunas e diagonais:
# 
# Para cada linha, coluna e diagonal, a função soma +1 para cada marca do jogador e -1 para cada marca do oponente.
# 
# Isso resulta em uma pontuação que reflete a "força" do jogador em relação ao oponente, mesmo sem uma vitória imediata.
# 
# Célula Central:
# 
# Como mencionado anteriormente, se o jogador ou o oponente ocupa a célula central, a função também ajusta a pontuação para refletir o controle estratégico sobre essa posição.

# In[2]:


class Board:
    def __init__(self, size=4):
        """Inicializa o tabuleiro com o tamanho especificado (4x4 por padrão)."""
        self.size = size
        self.board = np.full((self.size, self.size), '', dtype=str)  # Cria uma matriz vazia de strings para o tabuleiro.

    def display(self):
        """Exibe o tabuleiro como uma matriz."""
        print(self.board)  # Mostra o estado atual do tabuleiro.

    def reset(self):
        """Reinicia o tabuleiro."""
        self.board = np.full((self.size, self.size), '', dtype=str)  # Redefine o tabuleiro para seu estado vazio.

    def is_full(self):
        """Verifica se o tabuleiro está cheio."""
        return '' not in self.board  # Retorna True se não houver células vazias no tabuleiro.

    def make_move(self, row, col, player):
        """Marca o tabuleiro na posição especificada com o símbolo do jogador."""
        if self.board[row, col] == '':  # Verifica se a célula está vazia.
            self.board[row, col] = player  # Preenche a célula com o símbolo do jogador.
            return True  # Movimento bem-sucedido.
        return False  # Movimento inválido, célula já ocupada.

    def check_victory(self, player):
        """Verifica se o jogador especificado venceu."""
        # Verifica se o jogador venceu em qualquer linha ou coluna.
        for i in range(self.size):
            if all(self.board[i, j] == player for j in range(self.size)) or \
               all(self.board[j, i] == player for j in range(self.size)):
                return True

        # Verifica se o jogador venceu em qualquer uma das diagonais.
        if all(self.board[i, i] == player for i in range(self.size)) or \
           all(self.board[i, self.size - 1 - i] == player for i in range(self.size)):
            return True

        return False  # Retorna False se não houver vitória.

    def evaluate(self, player):
        """
        Avalia o tabuleiro e retorna um valor heurístico para o jogador especificado.
        O valor é calculado com base nas marcas do jogador e do oponente nas linhas, colunas e diagonais.
        """
        opponent = 'O' if player == 'X' else 'X'  # Define o símbolo do oponente
        score = 0  # Inicializa o placar.

        # Avaliação das linhas e colunas
        for i in range(self.size):
            # Conta o número de marcações do jogador e do oponente em cada linha.
            row_count = np.sum(self.board[i] == player)
            opponent_row_count = np.sum(self.board[i] == opponent)
            score += row_count  # +1 para cada marcação do jogador.
            score -= opponent_row_count  # -1 para cada marcação do oponente.

            # Conta o número de marcações do jogador e do oponente em cada coluna.
            col_count = np.sum(self.board[:, i] == player)
            opponent_col_count = np.sum(self.board[:, i] == opponent)
            score += col_count  # +1 para cada marcação do jogador.
            score -= opponent_col_count  # -1 para cada marcação do oponente.

        # Avaliação das diagonais
        # Conta o número de marcações do jogador e do oponente na diagonal principal.
        main_diag_count = np.sum(self.board[i, i] == player for i in range(self.size))
        opponent_main_diag_count = np.sum(self.board[i, i] == opponent for i in range(self.size))
        score += main_diag_count  # +1 para cada marcação do jogador na diagonal principal.
        score -= opponent_main_diag_count  # -1 para cada marcação do oponente na diagonal principal.

        # Conta o número de marcações do jogador e do oponente na diagonal secundária.
        anti_diag_count = np.sum(self.board[i, self.size - 1 - i] == player for i in range(self.size))
        opponent_anti_diag_count = np.sum(self.board[i, self.size - 1 - i] == opponent for i in range(self.size))
        score += anti_diag_count  # +1 para cada marcação do jogador na diagonal secundária.
        score -= opponent_anti_diag_count  # -1 para cada marcação do oponente na diagonal secundária.

        # Contar o número de células vazias no tabuleiro.
        empty_cells = np.sum(self.board == '')
        score += empty_cells  # +1 para cada célula vazia.

        # Avaliação da célula central.
        if self.board[1, 1] == player:
            score += 5  # Bônus se o jogador marcar a célula central.
        elif self.board[1, 1] == opponent:
            score -= 5  # Penalidade se o oponente marcar a célula central.

        return score  # Retorna o valor heurístico final.


# In[3]:


class Player:
    def __init__(self, symbol):
        """Inicializa um jogador com o símbolo especificado ('X' ou 'O')."""
        self.symbol = symbol  # Atribui o símbolo do jogador, que pode ser 'X' ou 'O'.

    def make_move(self, board):
        """Interface para fazer uma jogada, a ser implementada nas subclasses."""
        pass  # Método abstrato para ser sobrescrito por classes filhas (HumanPlayer, etc.).

class HumanPlayer(Player):
    def make_move(self, board):
        """Permite que o jogador humano escolha uma célula no tabuleiro para jogar."""
        while True:  # Loop para garantir que o jogador escolha uma célula válida.
            try:
                # Solicita ao jogador a linha e a coluna para fazer a jogada.
                row = int(input(f"Escolha a linha (1-{board.size}) para o {self.symbol}: ")) - 1
                col = int(input(f"Escolha a coluna (1-{board.size}) para o {self.symbol}: ")) - 1

                # Verifica se a entrada está dentro dos limites do tabuleiro.
                if 0 <= row < board.size and 0 <= col < board.size:
                    # Tenta fazer a jogada na célula especificada.
                    if board.make_move(row, col, self.symbol):
                        break  # Sai do loop se a jogada for bem-sucedida.
                    else:
                        print("Posição já ocupada, tente novamente.")  # Mensagem de erro para célula ocupada.
                else:
                    # Mensagem de erro se a entrada estiver fora dos limites.
                    print(f"Entrada inválida. Insira números entre 1 e {board.size}.")
            except ValueError:
                # Mensagem de erro se a entrada não for um número inteiro.
                print("Entrada inválida. Insira números válidos.")


# In[4]:


class ComputerPlayer(Player):
    def __init__(self, symbol, strategy):
        """Inicializa o jogador computador com o símbolo e a estratégia especificados."""
        super().__init__(symbol)  # Chama o construtor da classe base Player.
        self.strategy = strategy  # Define a estratégia ('random', 'minimax', ou 'alpha_beta').

    def make_move(self, board):
        """O jogador computador faz um movimento baseado na estratégia escolhida."""
        if self.strategy == 'random':  # Executa uma jogada aleatória.
            self.random_move(board)
        elif self.strategy == 'minimax':  # Executa uma jogada usando o algoritmo Minimax.
            self.minimax_move(board)
        elif self.strategy == 'alpha_beta':  # Executa uma jogada usando o algoritmo Minimax com Poda Alpha-Beta.
            self.alpha_beta_move(board)

    def random_move(self, board):
        """Escolhe uma célula aleatória vazia e marca o tabuleiro com o símbolo do computador."""
        # Obtém todas as células vazias no tabuleiro.
        available_moves = [(i, j) for i in range(board.size) for j in range(board.size) if board.board[i, j] == '']
        if available_moves:
            # Escolhe uma célula aleatória.
            row, col = random.choice(available_moves)
            board.make_move(row, col, self.symbol)
            print(f"Computador {self.symbol} jogou na posição ({row + 1}, {col + 1}).")

    def minimax_move(self, board):
        """Escolhe a melhor jogada usando o algoritmo Minimax."""
        best_value = -np.inf  # Inicializa o valor da melhor jogada como menos infinito.
        best_move = None  # Inicializa a melhor jogada como None.

        # Avalia todas as células vazias no tabuleiro.
        for i in range(board.size):
            for j in range(board.size):
                if board.board[i, j] == '':
                    # Faz uma jogada provisória.
                    board.make_move(i, j, self.symbol)
                    move_value = self.minimax(board, 4, False)  # Chama o algoritmo Minimax.
                    board.board[i, j] = ''  # Desfaz a jogada.

                    # Atualiza a melhor jogada se necessário.
                    if move_value > best_value:
                        best_value = move_value
                        best_move = (i, j)

        # Faz a melhor jogada encontrada.
        if best_move:
            board.make_move(best_move[0], best_move[1], self.symbol)
            print(f"Computador {self.symbol} jogou na posição ({best_move[0] + 1}, {best_move[1] + 1}).")

    def minimax(self, board, depth, is_max):
        """Função Minimax para encontrar o valor ótimo de uma jogada."""
        # Condições de vitória ou fim do jogo.
        if board.check_victory(self.symbol):
            return 10  # Retorna valor máximo se o computador vencer.
        elif board.check_victory('X' if self.symbol == 'O' else 'O'):
            return -10  # Retorna valor mínimo se o oponente vencer.
        elif board.is_full() or depth == 0:
            return board.evaluate(self.symbol)  # Avalia o tabuleiro se empatar ou atingir profundidade.

        if is_max:  # Se é a vez do computador (maximizador).
            best_value = -np.inf
            for i in range(board.size):
                for j in range(board.size):
                    if board.board[i, j] == '':
                        board.make_move(i, j, self.symbol)
                        best_value = max(best_value, self.minimax(board, depth - 1, False))
                        board.board[i, j] = ''  # Desfaz a jogada.
            return best_value
        else:  # Se é a vez do oponente (minimizador).
            best_value = np.inf
            for i in range(board.size):
                for j in range(board.size):
                    if board.board[i, j] == '':
                        board.make_move(i, j, 'X' if self.symbol == 'O' else 'O')
                        best_value = min(best_value, self.minimax(board, depth - 1, True))
                        board.board[i, j] = ''  # Desfaz a jogada.
            return best_value

    def minimax_alpha_beta(self, board, depth, is_max, alpha, beta):
        """Função Minimax com Poda Alpha-Beta para encontrar o valor ótimo de uma jogada."""
        # Condições de vitória ou fim do jogo.
        if board.check_victory(self.symbol):
            return 10  # Retorna valor máximo se o computador vencer.
        elif board.check_victory('X' if self.symbol == 'O' else 'O'):
            return -10  # Retorna valor mínimo se o oponente vencer.
        elif board.is_full() or depth == 0:
            return board.evaluate(self.symbol)  # Avalia o tabuleiro se empatar ou atingir profundidade.

        if is_max:  # Se é a vez do computador (maximizador).
            best_value = -np.inf
            for i in range(board.size):
                for j in range(board.size):
                    if board.board[i, j] == '':
                        board.make_move(i, j, self.symbol)
                        best_value = max(best_value, self.minimax_alpha_beta(board, depth - 1, False, alpha, beta))
                        board.board[i, j] = ''  # Desfaz a jogada.
                        alpha = max(alpha, best_value)  # Atualiza o valor de alpha.
                        if beta <= alpha:  # Poda a árvore de busca se beta <= alpha.
                            break
            return best_value
        else:  # Se é a vez do oponente (minimizador).
            best_value = np.inf
            for i in range(board.size):
                for j in range(board.size):
                    if board.board[i, j] == '':
                        board.make_move(i, j, 'X' if self.symbol == 'O' else 'O')
                        best_value = min(best_value, self.minimax_alpha_beta(board, depth - 1, True, alpha, beta))
                        board.board[i, j] = ''  # Desfaz a jogada.
                        beta = min(beta, best_value)  # Atualiza o valor de beta.
                        if beta <= alpha:  # Poda a árvore de busca se beta <= alpha.
                            break
            return best_value

    def alpha_beta_move(self, board):
        """Escolhe a melhor jogada usando o algoritmo Minimax com Poda Alpha-Beta."""
        best_value = -np.inf
        best_move = None
        alpha = -np.inf
        beta = np.inf

        # Avalia todas as células vazias no tabuleiro.
        for i in range(board.size):
            for j in range(board.size):
                if board.board[i, j] == '':
                    # Faz uma jogada provisória.
                    board.make_move(i, j, self.symbol)
                    move_value = self.minimax_alpha_beta(board, 4, False, alpha, beta)
                    board.board[i, j] = ''  # Desfaz a jogada.

                    # Atualiza a melhor jogada se necessário.
                    if move_value > best_value:
                        best_value = move_value
                        best_move = (i, j)

        # Faz a melhor jogada encontrada.
        if best_move:
            board.make_move(best_move[0], best_move[1], self.symbol)
            print(f"Computador {self.symbol} jogou na posição ({best_move[0] + 1}, {best_move[1] + 1}).")


# In[5]:


class Game:
    def __init__(self):
        """
        Inicializa o jogo, configurando o tabuleiro e os jogadores.

        Atributos:
            board: Instância da classe Board que representa o tabuleiro do jogo.
            player1: Representa o primeiro jogador (Humano ou Computador).
            player2: Representa o segundo jogador (Humano ou Computador).
            move_count: Contador de jogadas realizadas durante o jogo.
            start_time: Hora em que o jogo começou, usado para calcular a duração total do jogo.
        """
        self.board = Board()  # Cria uma nova instância do tabuleiro
        self.player1 = None   # Inicializa o primeiro jogador como None
        self.player2 = None   # Inicializa o segundo jogador como None
        self.move_count = 0   # Inicializa o contador de jogadas
        self.start_time = 0   # Inicializa a hora de início do jogo

    def setup(self):
        """
        Exibe um menu para configurar o jogo, permitindo escolher entre
        Humano vs Computador ou Computador vs Computador.
        """
        print("Bem-vindo ao Jogo da Velha 4x4!")  # Mensagem de boas-vindas
        print("Escolha o modo de jogo:")
        print("1. Humano vs Computador")
        print("2. Computador vs Computador")

        while True:
            mode = input("Escolha (1/2): ")  # Solicita ao usuário a escolha do modo de jogo
            if mode == "1":
                strategy = self.choose_strategy("computador")  # Escolhe a estratégia para o computador
                self.player1 = HumanPlayer("X")  # Define o primeiro jogador como Humano
                self.player2 = ComputerPlayer("O", strategy)  # Define o segundo jogador como Computador
                break
            elif mode == "2":
                print("Escolha a estratégia para os computadores:")
                strategy = self.choose_strategy("computadores")  # Escolhe a estratégia para ambos os computadores
                self.player1 = ComputerPlayer("X", strategy)  # Define o primeiro jogador como Computador
                self.player2 = ComputerPlayer("O", strategy)  # Define o segundo jogador como Computador
                break
            else:
                print("Entrada inválida. Tente novamente.")  # Mensagem de erro para entrada inválida

    def choose_strategy(self, player_name="computadores"):
        """
        Exibe o menu para o usuário escolher a estratégia do computador.

        Parâmetros:
            player_name (str): Nome do jogador para a mensagem de escolha (padrão: "computadores").

        Retorna:
            str: A estratégia escolhida pelo usuário.
        """
        print(f"Escolha a estratégia para {player_name}:")
        print("1. Random")  # Estratégia aleatória
        print("2. Minimax")  # Estratégia Minimax
        print("3. Alpha-Beta")  # Estratégia Alpha-Beta

        while True:
            choice = input("Escolha (1/2/3): ")  # Solicita a escolha da estratégia
            if choice == "1":
                return "random"  # Retorna a estratégia aleatória
            elif choice == "2":
                return "minimax"  # Retorna a estratégia Minimax
            elif choice == "3":
                return "alpha_beta"  # Retorna a estratégia Alpha-Beta
            else:
                print("Entrada inválida. Tente novamente.")  # Mensagem de erro para entrada inválida

    def play(self):
        """
        Executa o loop principal do jogo até que um jogador vença ou o tabuleiro fique cheio.

        O método exibe o estado atual do tabuleiro, solicita jogadas dos jogadores,
        e verifica se houve um vencedor ou um empate após cada jogada.
        """
        self.start_time = time.time()  # Início do cronômetro
        current_player = self.player1  # Define o jogador atual como player1

        while True:
            print("\nEstado atual do tabuleiro:")  # Exibe o estado atual do tabuleiro
            self.board.display()  # Método para exibir o tabuleiro

            self.move_count += 1  # Incrementa o contador de jogadas
            print(f"Jogada {self.move_count}:")  # Exibe o número da jogada
            start_move_time = time.time()  # Início do tempo da jogada

            current_player.make_move(self.board)  # Solicita ao jogador atual que faça uma jogada

            move_duration = time.time() - start_move_time  # Tempo da jogada em segundos
            print(f"Tempo gasto nesta jogada: {move_duration:.2f} segundos")  # Exibe o tempo gasto

            # Verifica se o jogador atual venceu ou se o tabuleiro está cheio
            if self.board.check_victory(current_player.symbol) or self.board.is_full():
                print("\nEstado final do tabuleiro:")  # Exibe o estado final do tabuleiro
                self.board.display()  # Método para exibir o tabuleiro
                if self.board.check_victory(current_player.symbol):
                    print(f"{current_player.symbol} venceu!")  # Mensagem de vitória
                else:
                    print("Empate!")  # Mensagem de empate
                break  # Termina o loop

            # Alterna entre os jogadores
            current_player = self.player1 if current_player == self.player2 else self.player2

        total_duration = time.time() - self.start_time  # Tempo total do jogo em segundos
        print(f"Tempo total do jogo: {total_duration:.2f} segundos")  # Exibe o tempo total

    def reset(self):
        """
        Reinicia o jogo, redefinindo o tabuleiro e os contadores de jogadas e tempo.
        """
        self.board.reset()  # Método para redefinir o tabuleiro
        self.move_count = 0  # Reinicia o contador de jogadas
        self.start_time = 0  # Reinicia a hora de início do jogo


# In[7]:


if __name__ == "__main__":
    game = Game()
    game.setup()
    game.play()

