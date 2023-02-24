
from django.urls import path

from . import views

app_name = 'api'
urlpatterns = [
    path('sudoku/', views.Sudoko.as_view(), name ='getSudoku'),
    path('getSudokuSolution/', views.GetSudokoSolution.as_view(), name ='GetSudokoSolution')
]