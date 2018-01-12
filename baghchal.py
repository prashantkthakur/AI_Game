import numpy as np

from evaluation import Evaluation


class GameBoard:

    def __init__(self,):
        self.board = ['T','','','','T','','','','','','','','','','','','','','','','T','','','','T']
        self.goat_lost = 0
        self.player = 'G'
        self.playerLookAhead = self.player
        self.movesExplored = 0

    def __repr__(self):
        return self.printState(self.board) + ("Goats Dead: " + str(self.goat_lost) + "\n" if self.goat_lost > 0 else "")

    def __str__(self):
        return self.printState(self.board) + ("Goats Dead: " + str(self.goat_lost) + "\n" if self.goat_lost > 0 else "")

    @staticmethod
    def to2D(idx):
        if type(idx) is list:
            return [(int(i / 5), i % 5) for i in idx]
        else:
            return (int(idx / 5), idx % 5)

    @staticmethod
    def to1D(coord):
        if type(coord) is list:
            return [i * 5 + j for (i, j) in coord]
        else:
            return coord[0] * 5 + coord[1]

    @staticmethod
    def printState(state):
        boardStr = ""
        for i in range(0, 25, 5):
            boardStr += '---'.join(['o' if s == '' else s for s in state[i:i + 5]]) + "\n"
            if i < 20:
                boardStr += "| \ | / | \ | / |\n"  if i % 2 == 0 else "| / | \ | / | \ |\n"
        return boardStr

    @staticmethod
    def positionOf(player, state):
        idx = [i for i, x in enumerate(state) if x == player]
        return GameBoard.to2D(idx)

    @staticmethod
    def action(position):
        moves = ['up', 'down', 'right', 'left']
        row,col = position
        if row == 0:
            moves.remove('up')
        if row == 4:
            moves.remove('down')
        if col == 0:
            moves.remove('left')
        if col == 4:
            moves.remove('right')

        return moves

    @staticmethod
    # Takes current board (5X5 matrix), position to compute side moves.
    def side_move(board,position):
        new_position = []
        idx = np.where(board == '')
        blank_position = set(list(zip(idx[0],idx[1])))
        moves = GameBoard.action(position)
        row, col = position
        # print(position)
        # Compute new position based on moves
        for move in moves:
            if move == 'up':
                new_position.append((row-1,col))
            if move == 'down':
                new_position.append((row+1,col))
            if move == 'left':
                new_position.append((row,col-1))
            if move == 'right':
                new_position.append((row,col+1))

        # Check for diagonal moves.
        if (row+col) % 2 == 0:
            if 'down' in moves:
                if 'right' in moves:
                    new_position.append((row+1,col+1))
                if 'left' in moves:
                    new_position.append((row+1, col-1))
            if 'up' in moves:
                if 'right' in moves:
                    new_position.append((row-1, col+1))
                if 'left' in moves:
                    new_position.append((row-1, col-1))
        # Return all positions which is empty (no other animal already present).
        valid_moves = list(set(new_position) & blank_position)
        # print("Valid moves:{}".format(valid_moves))
        return valid_moves

    @staticmethod
    # board is 5X5 matrix, position of tiger which needs to jump.
    def jumping_move(board, position):
        valid_moves = []
        new_position = []
        idx = np.where(board == '')
        blank_position = set(list(zip(idx[0],idx[1])))
        goat_idx = np.where(board == 'G')
        goat_position = set(list(zip(goat_idx[0],goat_idx[1])))
        moves = GameBoard.action(position)
        jump_moves = moves.copy()
        row,col = position
        for move in moves:
            if (row+2 >= 5 and move == 'down') or (row-2 <= -1 and move == 'up') or (col+2 >= 5 and move == 'right') \
                    or (col-2 <= -1 and move == 'left'):
                jump_moves.remove(move)
                continue
            else:
                if move == 'up':
                    new_position.append((row-2,col))
                if move == 'down':
                    new_position.append((row+2,col))
                if move == 'left':
                    new_position.append((row,col-2))
                if move == 'right':
                    new_position.append((row,col+2))
        # print(position, jump_moves)
        # Check for diagonal moves.
        if (row+col) % 2 == 0:
            if 'down' in jump_moves:
                if 'right' in jump_moves:
                    new_position.append((row+2,col+2))
                if 'left' in jump_moves:
                    new_position.append((row+2, col-2))
            if 'up' in jump_moves:
                if 'right' in jump_moves:
                    new_position.append((row-2, col+2))
                if 'left' in jump_moves:
                    new_position.append((row-2, col-2))

        # print("Jumpables:{}".format(jumpables))
        # Check if there is a goat in-between the jump position and current position.
        for pos in set(new_position) & blank_position:
            r, c = pos
            if ((row+r)/2, (col+c)/2) in goat_position:
                valid_moves.append(pos)
            else:
                continue
        # print("Valid moves:{}".format(valid_moves))
        return valid_moves

    @staticmethod
    def output_pair(data):
        output = []
        for key, values in data.items():
            src = GameBoard.to1D(key)
            for val in values:
                output.append((src,GameBoard.to1D(val)))
        return output


    def valid_goat_move(self):
        initial_moves = []
        current_board = np.array(self.board).reshape(5,5)
        idx = np.where(current_board == '')
        goat_data = dict()
        num_goat_in_board = len(GameBoard.positionOf('G', self.board))
        num_goats = num_goat_in_board + self.goat_lost
        if num_goats < 20:
            for val in (list(zip(idx[0],idx[1]))):
                initial_moves.append(GameBoard.to1D(val))
            return [(-1,c) for c in initial_moves]
        else:
            goat_idx = np.where(current_board == 'G')
            positions = list(zip(goat_idx[0], goat_idx[1]))
            # Compute all legal moves for a given position
            for position in positions:
                side_move = self.side_move(current_board, position)
                if side_move:
                    goat_data[position] = side_move
        # print(goat_data)
        return self.output_pair(goat_data)

    def valid_tiger_move(self):
        current_board = np.array(self.board).reshape(5,5)
        tiger_idx = np.where(current_board == 'T')
        positions = list(zip(tiger_idx[0], tiger_idx[1]))
        tiger_data = dict()
        # Check side move
        for position in positions:
            # Check slide move
            side_move = self.side_move(current_board,position)
            if side_move:
                tiger_data[position]= side_move
            # Check jump move
            jump_moves = self.jumping_move(current_board,position)
            if jump_moves:
                if tiger_data.get(position):
                    tiger_data[position].extend(jump_moves)
                else:
                    tiger_data[position]= jump_moves
        # print(tiger_data)
        return self.output_pair(tiger_data)

    def availableMoves(self, sort=False):
        if (self.playerLookAhead == 'G'):
            return self.sortGoatMoves(self.valid_goat_move()) if sort else self.valid_goat_move()
        else:
            return self.sortTigerMoves(self.valid_tiger_move()) if sort else self.valid_tiger_move()

    def sortTigerMoves(self, moves):
        scoredMoves = []
        for move in moves:
            source = self.to2D(move[0])
            dest = self.to2D(move[1])
            scoredMoves.append( ( move, max(abs(dest[0] - source[0]), abs(dest[1] - source[1])) ) )

        scoredMoves.sort(key=lambda x:x[1], reverse=True)
        return [move[0] for move in scoredMoves]

    def sortGoatMoves(self, moves):
        valuedDest = []
        tigerMoves = self.valid_tiger_move()
        for move in tigerMoves:
            source = self.to2D(move[0])
            dest = self.to2D(move[1])
            if max(abs(dest[0] - source[0]), abs(dest[1] - source[1])) > 1:
                valuedDest.append(move[1])

        if len(valuedDest) > 0:
            scoredMoves = []
            for move in moves:
                if move[1] in valuedDest:
                    scoredMoves.append((move, 1))
                else:
                    scoredMoves.append((move, 0))
            scoredMoves.sort(key=lambda x: x[1], reverse=True)
            return [move[0] for move in scoredMoves]
        else:
            return moves

    def makeMove(self, move):
        if move[0] == -1:
            self.board[move[1]] = 'G'
        else:
            piece = self.board[move[0]]
            self.board[move[0]] = ''
            self.board[move[1]] = piece
            if piece == 'T':
                source = GameBoard.to2D(move[0])
                dest = GameBoard.to2D(move[1])
                if max(abs(dest[0] - source[0]), abs(dest[1] - source[1])) > 1:
                    self.goat_lost += 1
                    mid = (int((source[0]+dest[0])/2), int((source[1]+dest[1])/2))
                    self.board[GameBoard.to1D(mid)] = ''
        self.playerLookAhead = 'G' if self.playerLookAhead=='T' else 'T'
        self.movesExplored += 1


    def unmakeMove(self, move):
        if move[0] == -1:
            self.board[move[1]] = ''
        else:
            piece = self.board[move[1]]
            self.board[move[1]] = ''
            self.board[move[0]] = piece
            if piece == 'T':
                source = GameBoard.to2D(move[0])
                dest = GameBoard.to2D(move[1])
                if max(abs(dest[0] - source[0]), abs(dest[1] - source[1])) > 1:
                    self.goat_lost -= 1
                    mid = (int((source[0]+dest[0])/2), int((source[1]+dest[1])/2))
                    self.board[GameBoard.to1D(mid)] = 'G'
        self.playerLookAhead = 'G' if self.playerLookAhead == 'T' else 'T'

    def isOver(self):
        tiger_move = self.valid_tiger_move()
        if len(tiger_move) == 0:
            return True
        if self.goat_lost >=5:
            return True
        return False

    def getWinner(self):
        tiger_move = self.valid_tiger_move()
        if len(tiger_move) == 0:
            return 'G'
        if self.goat_lost >=5:
            return 'T'
        return None


    def changePlayer(self):
        self.player = 'G' if self.player == 'T' else 'T'
        self.playerLookAhead = self.player

    def getMovesExplored(self):
        return self.movesExplored





if __name__=="__main__":
    state=['T','G','','G','T','','','','','','','','','','','','','','','','T','','','','T']
    game = GameBoard()

    state2=['T','','','G','G','T','G','G','','','','G','T','G','G','G','G','','G','G','G','G','G','G','T']
    game.board = state2
    game.changePlayer()
    print(game)
    print(Evaluation.sortTigerMoves(game, game.availableMoves()))
    print(Evaluation.ebf(189985, 200))

    """
    GameBoard.printState(state2)
    tiger_move = game.valid_tiger_move(state2)
    print("Tiger moves:{}".format(tiger_move))
    goat_move = game.valid_goat_move(state2)
    print("Goat move", goat_move)
    print("All moves", game.availableMoves(state2))

    state2 = ['T', '', '', 'G', 'G', 'T', 'G', 'G', '', '', '', 'G', 'T', 'G', 'G', 'G', 'G', '', 'G', 'G', 'G', 'G',
              'G', 'G', 'T']
    game.printState(state2)
    game.makeMove(state2, (12,10))
    game.printState(state2)
    print(game.goat_lost)
    game.unmakeMove(state2, (12,10))
    game.printState(state2)
    print(game.goat_lost)
    """
