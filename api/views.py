from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from django.core.cache import cache
import copy


class Sudoko(GenericAPIView):

    def get(self, request):
        ss = SolveSudoku()
        puzzle = [
            [0, 5, 0, 9, 0, 0, 0, 0, 0],
            [8, 0, 0, 0, 4, 0, 3, 0, 7],
            [0, 0, 0, 2, 8, 0, 1, 9, 0],
            [5, 3, 8, 6, 0, 7, 9, 4, 0],
            [0, 2, 0, 3, 0, 1, 0, 0, 0],
            [1, 0, 9, 8, 0, 4, 6, 2, 3],
            [9, 0, 7, 4, 0, 0, 0, 0, 0],
            [0, 4, 5, 0, 0, 0, 2, 0, 9],
            [0, 0, 0, 0, 3, 0, 0, 7, 0]
        ]
 
        unsolved_puzzle = copy.deepcopy(puzzle)
        ss.solve_sudoku(puzzle)
        cache.set('solved_puzzle', puzzle, 86400)
        return Response(unsolved_puzzle)
    
    def post(self, request):
        ss = SolveSudoku()
        player_solution = request.data.get('playerSolution')
        solved_puzzle = cache.get('solved_puzzle')
        response = ss.compare_solutions(player_solution, solved_puzzle)
        return Response(response)
    

class GetSudokoSolution(GenericAPIView):

    def get(self, request):
        solved_puzzle = cache.get('solved_puzzle')
        return Response(solved_puzzle)


class SolveSudoku():
    def check_column_valid(self, board, col, num):
        for rows in board:
            if rows[col] == num:
                return False
        return True

    def check_row_valid(self, board, row, num):
        for val in board[row]:
            if val == num:
                return False
        return True

    def check_box_valid(self, board, row, col, num):
        box_values = []
        row_start = row - (row % 3)
        col_start = col - (col % 3)

        for i in range(3):
            for j in range(3):
                box_values.append(board[row_start + i][col_start + j])
        
        for val in box_values:
            if val == num:
                return False
        return True

    def check_if_valid(self, new_board, row, column, value):
        if (self.check_column_valid(new_board, column, value) and 
            self.check_row_valid(new_board, row, value) and 
            self.check_box_valid(new_board, row, column, value)) == True:
            return True
        return False
    
    def solve_sudoku(self, board, row = 0, column = 0):
        if (row == 8 and column == 9):
            return True
        if column == 9:
            row += 1
            column = 0
        if board[row][column] > 0:
            column += 1
            return self.solve_sudoku(board, row, column)
        
        for num in range(1, 10): 
            if self.check_if_valid(board, row, column, num):
                board[row][column] = num
                if self.solve_sudoku(board, row, column + 1):
                    return True
            board[row][column] = 0
        return False
    
    def compare_solutions(self, player_solution, solved_puzzle):
        message = {}
        for i in range(9):
            for j in range(9):
                if player_solution[i][j] == 0:
                    message['message'] = "No issues, values missing" 
                elif player_solution[i][j] != solved_puzzle[i][j]:
                    message['message'] = "Solution is incorrect"
                    print(message)
                    return message
                else:
                    message['message'] = "Solution is correct"
        return message

