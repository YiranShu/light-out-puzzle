import random

class Puzzle(object):
    def __init__(self, row, column):
        self.create_puzzle(row, column)

    def create_puzzle(self, row, column):
        self.row = row
        self.column = column
        self.lights = [[0] * column for i in range(row)] 
        self.moves = 0 #the number of moves already selected
        self.evaluation = 0.0 #the evaluation of how many moves it will make
        self.selection = set() # to record the selection

    def __lt__(self, other):
        return self.moves + self.evaluation < other.moves + other.evaluation

    def perform_move(self, row, column):
        if row >= 0 and row <= self.row - 1 and column >= 0 and column <= self.column - 1:
            # pick the rows and columns adjecent
            rows = [row - 1, row + 1]
            columns = [column - 1, column + 1]
            
            # leave the valid items
            r = [item for item in rows if item >= 0 and item <= self.row - 1]
            c = [item for item in columns if item  >= 0 and item <= self.column - 1]
            
            for item in c:
                self.lights[row][item] = ~self.lights[row][item]

            for item in r:
                self.lights[item][column] = ~self.lights[item][column]

            self.lights[row][column] = ~self.lights[row][column]
            self.moves += 1
            self.evaluation = self.number_of_light_on() / 5.0
            if (row, column) not in self.selection:
                self.selection.add((row, column))
            else:
                self.selection.discard((row, column))
        else:
            print "Invalid option!"


    def scramble(self):
        for i in range(self.row):
            for j in range(self.column):
                rand = random.randint(0, 1)
                if rand == 1:
                    self.perform_move(i, j)
        self.moves = 0
        self.evaluation = self.number_of_light_on() / 5.0
        self.selection = set()


    def is_solved(self):
        """judge whether the puzzle is solved"""
        for item in self.lights:
            if -1 in item:
                # there are lights on in the puzzle. Not solved.
                return False

        return True


    def number_of_light_on(self):
        """compute the number of lights which are on"""
        count = 0
        for item in self.lights:
            count -= sum(item)

        return count
