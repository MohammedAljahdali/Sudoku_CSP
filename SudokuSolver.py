import numpy as np
import copy
import queue
from tkinter import *

class SetQueue(queue.Queue):
    def _init(self, maxsize):
        self.queue = set()

    def _put(self, item):
        self.queue.add(item)

    def _get(self):
        return self.queue.pop()


class Sudoku():
    board = np.zeros((9, 9), dtype=int)
    domains = np.zeros((9,9,9), dtype = int)

    def __init__(self):
        self.board = np.zeros((9, 9), dtype=int)
        for i in range(9):
            for j in range(9):
                for k in range(9):
                    self.domains[i, j, k] = k + 1



    def fill(self, filled: np.ndarray):
        for i in range(filled.shape[0]):
            if filled[i, 2] == 0:
                continue
            x = filled[i, 0]
            y = filled[i, 1]
            value = filled[i, 2]
            self.board[x, y] = value
            ### here we change the domain of added values to be only the value
            self.domains[x][y] = [value]

def allArcs():
    q = SetQueue(0)
    for i in range(9):
        for j in range(9):
            for l in range(9):
                for m in range(9):
                    if l == i or m == j:
                        q.put((i, j, l, m))
                    if i in range(0, 3) and j in range(0, 3) and l in range(0, 3) and m in range(0, 3):
                        q.put((i, j, l, m))
                    if i in range(0, 3) and j in range(3, 6) and l in range(0, 3) and m in range(3, 6):
                        q.put((i, j, l, m))
                    if i in range(0, 3) and j in range(6, 9) and l in range(0, 3) and m in range(6, 9):
                        q.put((i, j, l, m))
                    if i in range(3, 6) and j in range(0, 3) and l in range(3, 6) and m in range(0, 3):
                        q.put((i, j, l, m))
                    if i in range(3, 6) and j in range(3, 6) and l in range(3, 6) and m in range(3, 6):
                        q.put((i, j, l, m))
                    if i in range(3, 6) and j in range(6, 9) and l in range(3, 6) and m in range(6, 9):
                        q.put((i, j, l, m))
                    if i in range(6, 9) and j in range(0, 3) and l in range(6, 9) and m in range(0, 3):
                        q.put((i, j, l, m))
                    if i in range(6, 9) and j in range(3, 6) and l in range(6, 9) and m in range(3, 6):
                        q.put((i, j, l, m))
                    if i in range(6, 9) and j in range(6, 9) and l in range(6, 9) and m in range(6, 9):
                        q.put((i, j, l, m))
    return q

def assignmentComplete(assignment, game):
    for i in range(9):
        for j in range(9):
            if game.board[i][j] == 0:
                if assignment.board[i][j] == 0:
                    return False
    return True


def assignValue(assignment, game):  ## TODO: we might need to add counter to not repeat wrong assignment
    for i in range(9):
        for j in range(9):
            if game.board[i][j] == 0 and assignment.board[i][j] == 0:
                return i, j


def isConsistent(valueI, valueJ, value, assignment, game):
    for i in range(9):
        if value == assignment.board[valueI][i] or value == assignment.board[i][valueJ] or game.board[valueI][
            i] == value or value == game.board[i][valueJ]:
            return False
    index = getBlock(valueI, valueJ)
    for i in range(index[0] * 3, index[0] * 3 + 3):
        for j in range(index[1] * 3, index[1] * 3 + 3):
            if value == assignment.board[i][j] or value == game.board[i][j]:
                return False
    return True


def getBlock(valueI, valueJ):
    index = []
    index.append(valueI // 3)
    index.append(valueJ // 3)
    return index

def getNeighborsOf(i , j):
    ## get index of all of Di neighbors
    neighbors = []
    for l in range(9):
        for m in range(9):
            if l == i or m == j:
                neighbors.append(l)
                neighbors.append(m)
            if i in range(0, 3) and j in range(0, 3) and l in range(0, 3) and m in range(0, 3):
                neighbors.append(l)
                neighbors.append(m)
            if i in range(0, 3) and j in range(3, 6) and l in range(0, 3) and m in range(3, 6):
                neighbors.append(l)
                neighbors.append(m)
            if i in range(0, 3) and j in range(6, 9) and l in range(0, 3) and m in range(6, 9):
                neighbors.append(l)
                neighbors.append(m)
            if i in range(3, 6) and j in range(0, 3) and l in range(3, 6) and m in range(0, 3):
                neighbors.append(l)
                neighbors.append(m)
            if i in range(3, 6) and j in range(3, 6) and l in range(3, 6) and m in range(3, 6):
                neighbors.append(l)
                neighbors.append(m)
            if i in range(3, 6) and j in range(6, 9) and l in range(3, 6) and m in range(6, 9):
                neighbors.append(l)
                neighbors.append(m)
            if i in range(6, 9) and j in range(0, 3) and l in range(6, 9) and m in range(0, 3):
                neighbors.append(l)
                neighbors.append(m)
            if i in range(6, 9) and j in range(3, 6) and l in range(6, 9) and m in range(3, 6):
                neighbors.append(l)
                neighbors.append(m)
            if i in range(6, 9) and j in range(6, 9) and l in range(6, 9) and m in range(6, 9):
                neighbors.append(l)
                neighbors.append(m)
    return neighbors

# TODO: set and queue of all arcs perform update on each one,
# TODO: if an arc get updated then also update it's neighbours
def arcConsistency(assignment, game):
    q = allArcs()

    while not q.empty():
        indices = q.get()
        Di = assignment.domains[indices[0]][indices[1]]
        Dj = assignment.domains[indices[2]][indices[3]]
        if updateDomains(Di,Dj):
            if len(Di) == 0:
                return False
            neighbors = getNeighborsOf(indices[0], indices[1])
            for index in range(len(neighbors) // 2):
                q.put((neighbors[index * 2], neighbors[index * 2 + 1], indices[0], indices[1]))
    return True


# TODO: check the domains of two variables and remove Di if it does not work
# TODO: with all Dj
def updateDomains(Di: np.ndarray, Dj):
    updated = False
    if len(Di) == 9 and len(Dj) == 9:
        return updated
    for i in range(len(Di)):
        if Di[i] == 0:
            continue
        satisfied = False
        for j in range(len(Dj)):
            if Di[j] == 0:
                continue
            if Di[i] != Dj[j]:
                satisfied = True
        if not satisfied:
            updated = True
            Di[i] = 0
    return updated


def backTracking(assignment, game):
    # if all the variable are assigned we stop the backtracking
    if assignmentComplete(assignment, game):
        print(assignment.board)
        displayFinalBoard(assignment.board)
        return True
    # assignValue return a an index of variable that is not assigned yet.
    varI, varJ = assignValue(assignment, game)
    # here we run through all possible domain values for the an assigned variable.
    for value in assignment.domains[varI][varJ]:
        if value == 0:
            continue
        if isConsistent(varI, varJ, value, assignment, game):  ## see if value is consistent with assignment
            assignmentTemp = copyGame(assignment)
            assignmentTemp.fill(np.array([[varI, varJ, value]]))
            if arcConsistency(assignmentTemp, game):
                if backTracking(assignmentTemp, game):
                    return True
    return False

def displayFinalBoard(board: np.ndarray):
    for i in range(9):
        for j in range(9):
            index = i * 9 + j
            e[index].delete(0, END)
            e[index].insert(0, board[i,j])

def CSP(game):
    return backTracking(copy.deepcopy(game), game)

def copyGame(assignment: Sudoku):
    s = Sudoku()
    s.board = np.copy(assignment.board)
    s.domains = np.copy(assignment.domains)
    return s


#### GUI ####
root = Tk()
e = []
for i in range(9):
    for j in range(9):
        e.append(Entry(root, text = i * 9 + j + 1, width = 5, font=("Calibri",14)))
        e[i * 9 + j].grid(row = i, column = j,padx=5,pady=5,ipady=3)
        e[i * 9 + j].insert(0, 0)

def start():
    filled = np.zeros((81, 3), dtype=int)
    for i in range(9):
        for j in range(9):
            index = i * 9 + j
            filled[index, 0] = i
            filled[index, 1] = j
            filled[index, 2] = int(e[index].get())
    s = Sudoku()
    s.fill(filled)
    CSP(s)

b1 = Button(root, width = 20, text = "start", command = start).grid(row = 9, column = 0, columnspan = 5, padx=5,pady=5,ipady=3)

def reset():
    for i in range(9):
        for j in range(9):
            e[i * 9 + j].delete(0, END)
            e[i * 9 + j].insert(0, 0)

b2 = Button(root, width = 20, text = "reset", command = reset).grid(row = 9, column = 4, columnspan = 5, padx=5,pady=5,ipady=3)

print(e[1].get())
mainloop()
#### GUI ####
