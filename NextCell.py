import createPuzzle

class nextCell(object):
    """description of class"""
    def next_cell(self, rows, columns, row, column):
        if row >= 0 and row < rows and column >= 0 and column < columns:
            if column < columns - 1:
                return [row, column + 1]
            elif column == columns - 1 and row < rows - 1:
                return [row + 1, 0]
            else:
                return [0, 0]
        else:
            print "Invalid command!"
