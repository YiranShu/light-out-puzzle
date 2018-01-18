import createPuzzle
import Queue
import copy
import NextCell

class Solution(object):
    """description of class"""
    def __init__(self):
        self.stepDFS = 0 # number of perform_move callings in DFS
        self.stepBFS = 0 # number of perform_move callings in BFS
        self.stepAStar = 0 # number of perform_move callings in AStar

    def drive_for_DFS(self, puzzle):
        self.DFS(0, 0, puzzle)
        if puzzle.is_solved():
            return puzzle.selection

    def DFS(self, row, column, puzzle):
        nextcell = NextCell.nextCell()
        if puzzle.is_solved():
            return
        for i in range(2):
            # when i is 0, the current cell is selected.
            # when i is 1, the current cell is selected again, which is equivalent to not selecting at all.
            # In this way, the search pointer can return to parent node.
            puzzle.perform_move(row, column)
            self.stepDFS += 1
            if puzzle.is_solved():
                return
            else:
                if nextcell.next_cell(puzzle.row, puzzle.column, row, column) != [0, 0]:
                    # this is not the last cell.
                    [row1, column1] = nextcell.next_cell(puzzle.row, puzzle.column, row, column) # fetch next cell
                    self.DFS(row1, column1, puzzle) # recursive to find the solution.
                    if puzzle.is_solved():
                        return
        
    def BFS(self, puzzle):
        que = Queue.Queue()
        nextcell = NextCell.nextCell()
        p = puzzle
        p.currentRow, p.currentColumn = 0, 0 # start from cell[0, 0].
        que.put(puzzle)
        while not que.empty():
            # pop 1 item per iteration
            # when a item in the queue is popped, its child nodes are added into the queue.
            # in this way to implement BFS
            temp = que.get()
            currentRow, currentColumn = temp.currentRow, temp.currentColumn
            if temp.is_solved():
                result = temp
                break
            else:
                if nextcell.next_cell(puzzle.row, puzzle.column, currentRow, currentColumn) != [0, 0]:
                    # the current cell is not the last cell.
                    temp.currentRow, temp.currentColumn = nextcell.next_cell(puzzle.row, puzzle.column, currentRow, currentColumn)
                    que.put(temp)
                    t = copy.deepcopy(temp)
                    t.perform_move(currentRow, currentColumn)
                    self.stepBFS += 1
                    if t.is_solved():
                        result = t
                        break
                    que.put(t)
                else:
                    temp.perform_move(currentRow, currentColumn)
                    self.stepBFS += 1
                    if temp.is_solved():
                        result = temp
                        break

        return result.selection

    def AStar(self, puzzle):
        history = set() # it records the history selections.
        que = Queue.PriorityQueue()
        que.put(puzzle)
        mini = que.get()
        while not mini.is_solved():
            # the priority queue pops the item with minimum heuristic function per iteration
            for i in range(puzzle.row):
                for j in range(puzzle.column):
                    if (i, j) not in mini.selection:
                        # cell[i, j] was not selected before
                        if tuple(mini.selection | {(i, j)}) in history:
                            # if the combination of cell[i, j] and the cells selected appeared before, do not need to try it.
                            continue
                        # Otherwise, add this combination to the history set.
                        history.add(tuple(mini.selection | {(i, j)}))
                        temp = copy.deepcopy(mini)
                        temp.perform_move(i, j)
                        self.stepAStar += 1
                        if temp.is_solved():
                            return temp.selection
                        que.put(temp)
            mini = que.get()
        
        if mini.is_solved():
            return mini.selection
