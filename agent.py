from baghchal import GameBoard
from evaluation import Evaluation




class MiniMax:
    def minimax(self, game, depth, maximizingPlayer, evalF):
        if depth==0 or game.isOver():
            evaluation = evalF(game)
            #print(game, "Player", game.player, "LAD", game.playerLookAhead, "eval", evaluation)
            return evaluation, None

        bestMove = None
        if maximizingPlayer==game.playerLookAhead:
            bestValue = float("-inf")
            for move in game.availableMoves():
                game.makeMove(move)
                v, _ = self.minimax(game, depth-1, maximizingPlayer, evalF)
                if v > bestValue:
                    bestValue = v
                    bestMove = move
                game.unmakeMove(move)
        else:
            bestValue = float("+inf")
            for move in game.availableMoves():
                game.makeMove(move)
                v, _ = self.minimax(game, depth-1, maximizingPlayer, evalF)
                if v < bestValue:
                    bestValue = v
                    bestMove = move
                game.unmakeMove(move)

        return bestValue, bestMove

    def alphabeta(self, game, depth, maximizingPlayer, evalF, alpha=float("-inf"), beta=float("inf"), sorting=False):
        #print(game)
        #print("____________")
        if depth==0 or game.isOver():
            evaluation = evalF(game)
            #print("Player", game.player, "LAD", game.playerLookAhead, "eval", evaluation)
            return evaluation, None

        bestMove = None
        if maximizingPlayer==game.playerLookAhead:
            bestValue = float("-inf")
            for move in game.availableMoves(sorting):
                game.makeMove(move)
                v, _ = self.alphabeta(game, depth-1, maximizingPlayer, evalF, alpha, beta)
                if v > bestValue:
                    bestValue = v
                    bestMove = move
                game.unmakeMove(move)
                alpha = max(bestValue, alpha)
                if alpha >= beta:
                    break
        else:
            bestValue = float("+inf")
            for move in game.availableMoves(sorting):
                game.makeMove(move)
                v, _ = self.alphabeta(game, depth-1, maximizingPlayer, evalF, alpha, beta)
                if v < bestValue:
                    bestValue = v
                    bestMove = move
                game.unmakeMove(move)
                beta = min(bestValue, beta)
                if alpha >= beta:
                    break

        return bestValue, bestMove

    def gamePlay(self):
        game = GameBoard()

        moves = 0
        while not game.isOver() and moves<101:
            value, move = self.alphabeta(game, 4, game.player, Evaluation.evaluate, sorting=False)
            if move is None:
                print('move is None. Stopping')
                break
            game.makeMove(move)
            moves += 1
            print("\nPlayer", game.player, "to", move, "for value", value)
            print(game)
            game.changePlayer()
        print("Moves Explored", game.getMovesExplored(), "Moves: ", moves)
        print("EBF: ", Evaluation.ebf(game.getMovesExplored(), moves))



def main():
    minimax = MiniMax()
    minimax.gamePlay()
    # state = ['T','','','G','G','T','G','G','','','','G','T','G','G','G','G','','G','G','G','G','G','G','T']
    # # state = ['T', '', '', '', 'T', '', '', '', '', '', '', '', '', '', '', '', '', 'G', '', 'G', 'T', '', 'G', 'G', 'T']
    # GameBoard.printState(state)
    # print("tigerMovability", Evaluation.tigerMovability(state))
    # print("deadGoats", Evaluation.vulnerableGoats(state))

if __name__ == "__main__":
    main()
