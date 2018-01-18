import createPuzzle
import time

class Gaussian(object):
    def __init__(self):
        self.step = 0

    def is_adjecent(self, cell1, cell2):
        """This method is to figure out whether is adjecent to each other"""
        if cell1 == cell2:
            return True
        elif cell1[0] == cell2[0] and (cell1[1] - cell2[1] == 1 or cell1[1] - cell2[1] == -1):
            return True
        elif cell1[1] == cell2[1] and (cell1[0] - cell2[0] == 1 or cell1[0] - cell2[0] == -1):
            return True
        else:
            return False

    def eliminate(self, A):
        """This method is to proceed Gaussian Elimination to simplify the matrix"""
        length = len(A)
        width = len(A[0])
        for i in range(length):
            if A[i][i] != 1:
                # if current entry on the diagonal is 0 (off), proceed row interchange. 
                for k in range(i + 1, length):
                    if A[k][i] == 1:
                        A[i], A[k] = A[k], A[i]
                        self.step += 1
                        break
            for j in range(i + 1, length):
                # eliminate the entries under the diagonal
                if A[j][i] == 1:
                    A[j] = [(A[i][m] + A[j][m]) % 2 for m in range(width)]
                    self.step += width

        for i in range(length - 1, -1, -1):
            # eliminate the entries above the diagonal
            for j in range(i - 1, -1, -1):
                if A[j][i] != 0:
                    A[j] = [(A[i][k] + A[j][k]) % 2 for k in range(width)]
                    self.step += width
        # Now, only the entries on the diagonal are 1, the rest are 0.


    def solute(self, puzzle):
        """This method is the drive to solve light out puzzle"""
        """suppose that ax = c, where a is a matrix, c and x are vectors."""
        """The aim is to figure out x, which indicates the solution."""
        A, a, c = [], [], []
        for i in range(puzzle.row):
            for j in range(puzzle.column):
                # create a puzzle.row * puzzle.column by puzzle.row * puzzle.column matrix.
                # each column represents a cell in the puzzle.
                # each row represents the changed cell if column c is selected.
                if puzzle.lights[i][j] == -1:
                    c.append(1)
                else:
                    c.append(0)
                for m in range(puzzle.row):
                    for n in range(puzzle.column):
                        if self.is_adjecent([m, n], [i, j]):
                            # if [m, n] is adjecent to [i, j], then a[ij][mn] should be 1.
                            a.append(1)
                        else:
                            a.append(0)
                a.append(c[i * puzzle.column + j])
                A.append(a)
                a = []

        self.eliminate(A)
        x = [item[len(item) - 1] for item in A]
        # x is the last column of A.
        # if x[i] is 1, cell i should be selected.
        i = 0
        for m in range(puzzle.row):
            for n in range(puzzle.column):
                if x[i] == 1:
                    puzzle.selection.add((m, n))
                i += 1

        return puzzle.selection

if __name__ == '__main__':
    trials = 100
    timeGaussian = 0
    lengthGaussian = 0
    row, column = 5, 5 # the value can be changed into 4, 4 or 8, 8 or 10, 10 to see the result
    gau = Gaussian()
    for i in range(trials):
        puzzleGaussian = createPuzzle.Puzzle(row, column)
        puzzleGaussian.scramble()

        start = time.clock()
        moves = gau.solute(puzzleGaussian)
        end = time.clock()
        timeGaussian += end - start
        lengthGaussian += len(moves)

    print row, " *  ", column, ": "
    print "Time: ", timeGaussian, "secs"
    print "Length: ", lengthGaussian
    print "Steps:", gau.step

