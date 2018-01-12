import decimal
from random import randint
decimal.getcontext().prec = 100


class Evaluation:
    # def getAdjacentVertex(pos):
    #     moves = [(-1,0),(1,0),(0,-1),(0,1)]
    #     if (pos[0]+pos[1])%2==0:
    #         moves = moves + [(-1,-1),(-1,1),(1,-1),(1,1)]
    #     vertex = []
    #     for move in moves:
    #         newPos = (pos[0]+move[0], pos[1]+move[1])
    #         if newPos[0]>0 and newPos[1]>0:
    #             vertex.append(newPos)
    #     return vertex

    def ebf(nNodes, depth, precision=0.01):
        ## Lambda for computing N as in above equation.
        ### To prevent divide by zero, here's something
        func = lambda b: (1 - decimal.Decimal(b) ** decimal.Decimal(depth + 1)) / decimal.Decimal(0.00001) if b == 1 else (1 - decimal.Decimal(b) ** decimal.Decimal(depth + 1)) / decimal.Decimal(1 - b)
        bLow = 0.0
        ### setting upper limit as nNodes
        bHigh = nNodes
        counter = 0
        calcNodes = func(bLow)
        ### Using binary search to find b till we reach given precision of nNodes
        while abs(calcNodes - nNodes) > precision and counter < 10000:
            midpoint = (bLow + bHigh) / 2
            calcNodes = func(midpoint)
            if calcNodes - nNodes < 0:
                bLow = midpoint
            else:
                bHigh = midpoint
            counter += 1
        return bHigh

    def distBetweenGoat(pos1, pos2):
        diff0 = abs(pos2[0]-pos1[0])
        diff1 = abs(pos2[1]-pos1[1])
        diff = max(diff0, diff1)
        return diff + (1 if (diff !=0 and (pos1[0]+pos1[1])%2!=0 and (pos2[0]+pos2[1])%2!=0) else 0)


    def goatDistanceAmong(game):
        sum = 0
        goatPos = game.positionOf('G', game.board)
        for pos1 in goatPos:
            for pos2 in goatPos:
                sum += Evaluation.distBetweenGoat(pos1,pos2)
        return sum/(len(goatPos)+1)

    def tigerMovability(game):
        return len(game.valid_tiger_move())

    def vulnerableGoats(game):
        deadGoatsNextLevel = 0
        moves = game.valid_tiger_move()
        for move in moves:
            # print(move)
            source = game.to2D(move[0])
            dest = game.to2D(move[1])
            if max(abs(dest[0]-source[0]), abs(dest[1]-source[1])) > 1:
                deadGoatsNextLevel += 1
        return deadGoatsNextLevel

    def evaluate(game):
        metric = 1*Evaluation.vulnerableGoats(game) + 5*game.goat_lost #+ 1*Evaluation.tigerMovability(game) + 1*Evaluation.goatDistanceAmong(game)
        if (game.player == 'T'):
            return metric
        else:
            return randint(-10, 10)



if __name__ == "__main__":
    from baghchal import GameBoard
    game = GameBoard()
    game.board = ['T', '', '', 'G', 'G', 'T', 'G', 'G', '', '', '', 'G', 'T', 'G', 'G', 'G', 'G', '', 'G', 'G', 'G', 'G',
              'G', 'G', 'T']

    # game.changePlayer()
    print(game)
    moves = game.availableMoves()
    ret = Evaluation.sortGoatMoves(game, moves)
    print(ret)

