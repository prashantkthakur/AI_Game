from agent import MiniMax
from baghchal import GameBoard
from evaluation import Evaluation
from random import randint


def evaluation1T(game):
    # metric = 1 * Evaluation.vulnerableGoats(game) + 5 * game.goat_lost # + 1*Evaluation.tigerMovability(game) + 1*Evaluation.goatDistanceAmong(game)
    metric = Evaluation.goatDistanceAmong(game) + 5*Evaluation.tigerMovability(game)
    return metric
    # return randint(-10, 10)

def evaluation1G(game):
    # metric =  1 * Evaluation.vulnerableGoats(game) + 5 * game.goat_lost +0.25*Evaluation.tigerMovability(game) #+ 1*Evaluation.goatDistanceAmong(game)
    # return -metric
    # return -1 *( Evaluation.vulnerableGoats(game) + 5 * game.goat_lost )
    return randint(-10, 10)


def gamePlay(evalFT, evalFG, numGames):
    winners = []
    ebfs = []
    minimax = MiniMax()
    for i in range(numGames):
        game = GameBoard()
        moves = 0
        while not game.isOver() and moves < 100:
            if game.player == 'T':
                value, move = minimax.minimax(game, 3, game.player, evalFT)
            else:
                value, move = minimax.minimax(game, 3, game.player, evalFG)
            if move is None:
                print('move is None. Stopping')
                break
            game.makeMove(move)
            moves += 1
            if moves >98:
                print("\nPlayer", game.player, "to", move, "for value", value)
                print(game)
            game.changePlayer()
        winner = game.getWinner()
        print("game", i, "winner", winner)
        winners.append(winner if winner is not None else 'D')
        ebfs.append(Evaluation.ebf(game.getMovesExplored(), moves))
    return winners, ebfs


if __name__ == "__main__":
    _, ebf = gamePlay(evaluation1T, evaluation1G, 500)
    print (ebf)

