from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.exceptions import ValidationError
from api.utils import SolveSudoku
from sudoku import Sudoku
from random import randint

from django.core.cache import cache

class Sudoko(GenericAPIView):

    def get(self, request):
        difficulty = request.GET.get('difficulty')

        if not difficulty:
            raise ValidationError('difficulty must be included')

        seed = randint(100, 999)
        puzzle = Sudoku(3, seed=seed).difficulty(float(difficulty)).board

        puzzle_obj = self.generate_puzzle_obj(puzzle)

        response = {
            'sudoku': puzzle_obj,
            'seed': seed
        }

        return Response(response)
    
    def post(self, request):
        player_solution = request.data.get('playerSolution')
        seed = request.data.get('seed')

        if not player_solution:
            raise ValidationError('playerSolution must be included')
        if not seed:
            raise ValidationError('seed must be included')
        
        puzzle = Sudoku(3, seed=int(seed)).difficulty(0.1).solve(raising=True).board
        solution_obj = self.generate_puzzle_obj(puzzle)

        response = {}
        for k, v in player_solution.items():
            if v != solution_obj[int(k)]:
                answer = False
            else:
                answer = True
            response[k] = answer
        
        return Response(response)
    

    def generate_puzzle_obj(self, puzzle):
        puzzle_obj = {}
        count = 0

        for row in puzzle:
            for val in row:
                if val == None:
                    val = 0
                puzzle_obj[count] = val
                count += 1

        return puzzle_obj
