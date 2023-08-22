#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
import random
import sys

from fleet import *

testfleet = battleship_fleet()
testfleet.scatter()

def sink_algorithm(board_state, _fleet, x1, y1):
  new_targets = []

  fleet_matrix = _fleet.fleet2matrix()

  # iterate through the adjacent squares
  for [dx,dy] in [[1,0],[0,1],[0,-1],[-1,0]]:
    if _fleet._ships[_fleet._index[fleet_matrix[x1,y1]]]._sunk:
      break
    x = x1+dx
    y = y1+dy
    # continue in direction until miss or no more board or ship sunk
    go_immediately_to_opposite = False
    for n in range(10):
      if _fleet._ships[_fleet._index[fleet_matrix[x1,y1]]]._sunk:
        break
      elif(x > 9 or x < 0 or y > 9 or y < 0):
        break
      elif(board_state[x,y] == '.'):
        if(fleet_matrix[x,y] == '.'):
          board_state[x,y] = 'M'
          break
        elif(fleet_matrix[x,y] != fleet_matrix[x1,y1]):
        # accidently hit an additional target!
          board_state[x,y] = 'H'
          go_immediately_to_opposite = True
          _fleet.update_status(board_state)
          if(not _fleet._ships[_fleet._index[fleet_matrix[x,y]]]._sunk):
            new_targets.append([x,y])
        else:
        # hit the same boat, woot!
          board_state[x,y] = 'H'
          go_immediately_to_opposite = True
          _fleet.update_status(board_state)
      else:
        break

      x += dx
      y += dy

    # try other direction if we have to hits in a straight line
    if(go_immediately_to_opposite):
      x = x1-dx
      y = y1-dy
      # continue in direction until miss or no more board or ship sunk
      for n in range(10):
        go_immediately_to_opposite = False
        if _fleet._ships[_fleet._index[fleet_matrix[x1,y1]]]._sunk:
          break
        elif(x > 9 or x < 0 or y > 9 or y < 0):
          break
        elif(board_state[x,y] == '.'):
          if(fleet_matrix[x,y] == '.'):
            board_state[x,y] = 'M'
            break
          elif(fleet_matrix[x,y] != fleet_matrix[x1,y1]):
          # accidently hit an additional target!
            board_state[x,y] = 'H'
            go_immediately_to_opposite = True
            _fleet.update_status(board_state)
            if(not _fleet._ships[_fleet._index[fleet_matrix[x,y]]]._sunk):
              new_targets.append([x,y])
          else:
          # hit the same boat, woot!
            board_state[x,y] = 'H'
            go_immediately_to_opposite = True
            _fleet.update_status(board_state)
        else:
          break

        x -= dx
        y -= dy

  # sink any new targets we accidentally found
  for target in new_targets:
    [x,y] = target
    board_state = sink_algorithm(board_state, _fleet, x, y)
    _fleet.update_status(board_state)
  return board_state

def grid2sequence(grid):
  sequence = [[-1,-1]]*100

  cnt = 0;
  for j in range(10):
    for k in range(10):
      if(grid[j][k] != '.'):
        sequence[grid[j][k]-1] = [j,k];
        cnt += 1;
      
  sequence = sequence[0:cnt]
  return sequence

def group1_algorithm(_fleet):
  fleet_matrix = _fleet.fleet2matrix()

  board_state = np.array([['.']*10]*10)

  static1 = [['.',  1,'.','.',  3,'.',  8,'.','.', 15],\
             [  2,'.','.',  4,'.',  9,'.','.', 16,'.'],\
             ['.','.',  5,'.', 10,'.','.', 17,'.','.'],\
             ['.',  6,'.', 11,'.','.', 18,'.','.', 25],\
             [  7,'.', 12,'.','.', 19,'.','.', 26,'.'],\
             ['.', 13,'.','.', 20,'.','.', 27,'.', 32],\
             [ 14,'.','.', 21,'.','.', 28,'.', 33,'.'],\
             ['.','.', 22,'.','.', 29,'.', 34,'.','.'],\
             ['.', 23,'.','.', 30,'.', 35,'.','.', 37],\
             [ 24,'.','.', 31,'.', 36,'.','.', 38,'.']];

  static2 = [['.', 42,'.', 28,'.','.', 29,'.', 43,'.'],\
             [ 41,'.', 27,'.', 11, 12,'.', 30,'.', 44],\
             ['.', 26,'.', 10,'.','.', 13,'.', 31,'.'],\
             [ 25,'.',  9,'.',  1,  2,'.', 14,'.', 32],\
             ['.', 24,'.',  8,'.','.',  3,'.', 15,'.'],\
             ['.', 23,'.',  7,'.','.',  4,'.', 16,'.'],\
             [ 40,'.', 22,'.',  6,  5,'.', 17,'.', 33],\
             ['.', 39,'.', 21,'.','.', 18,'.', 34,'.'],\
             [ 48,'.', 38,'.', 20, 19,'.', 35,'.', 45],\
             ['.', 47,'.', 37,'.','.', 36,'.', 46,'.']];


  static3 = [['.','.',  3,'.','.','.','.', 11,'.','.'],\
             ['.',  2,'.','.','.','.', 10,'.','.','.'],\
             [  1,'.','.','.','.',  9,'.','.','.', 19],\
             ['.','.','.','.',  8,'.','.','.', 18,'.'],\
             ['.','.','.',  7,'.','.','.', 17,'.','.'],\
             ['.','.',  6,'.','.','.', 16,'.','.','.'],\
             ['.',  5,'.','.','.', 15,'.','.','.','.'],\
             [  4,'.','.','.', 14,'.','.','.','.', 22],\
             ['.','.','.', 13,'.','.','.','.', 21,'.'],\
             ['.','.', 12,'.','.','.','.', 20,'.','.']];

  static4 = [['.','.','.','.','.','.','.','.','.','.'],\
             ['.','.','.','.','.','.','.','.','.','.'],\
             ['.','.','.','.','.','.','.','.','.','.'],\
             ['.','.','.','.','.','.','.','.','.','.'],\
             ['.','.','.','.','.','.','.','.','.','.'],\
             ['.','.','.','.','.','.','.','.','.','.'],\
             ['.','.','.','.','.','.','.','.','.','.'],\
             ['.','.','.','.','.','.','.','.','.','.'],\
             ['.','.','.','.','.','.','.','.','.','.'],\
             ['.','.','.','.','.','.','.','.','.','.']];

  cnt = 0
  current_seq = 1
  sequence1 = grid2sequence(static1)
  sequence2 = grid2sequence(static2)
  sequence3 = grid2sequence(static3)
  sequence = sequence1
  while(not _fleet._sunk):
    [x,y] = sequence[cnt]
    if(board_state[x,y] == '.'):
      if fleet_matrix[x,y] == '.':
        board_state[x,y] = 'M'
      else:
        board_state[x,y] = 'H'
        board_state = sink_algorithm(board_state, _fleet, x, y)
        _fleet.update_status(board_state)
    cnt += 1
    if(current_seq == 1 and _fleet._ships[0]._sunk and _fleet._ships[1]._sunk and _fleet._ships[2]._sunk and _fleet._ships[3]._sunk):
      sequence = sequence2
      current_seq = 2
      cnt = 0
    if(current_seq == 1 and cnt >= len(sequence1)):
      sequence = sequence3
      current_seq = 3
      cnt = 0
    if(cnt >= len(sequence)):
      # randomly select final shots
      sequence = []
      for x in range(10):
        for y in range(10):
          if(board_state[x,y] == '.'):
            sequence.append([x,y])
          random.shuffle(sequence)
          current_seq = 4
          cnt = 0
          

  return board_state

def group2_algorithm(_fleet):
  fleet_matrix = _fleet.fleet2matrix()

  board_state = np.array([['.']*10]*10)

  static  = [[ 31,'.', 33,'.', 35,'.', 37,'.', 39,'.'],\
             ['.', 32,'.', 34,'.', 36,'.', 38,'.', 40],\
             [ 11,'.', 13,'.', 15,'.', 17,'.', 19,'.'],\
             ['.', 12,'.', 14,'.', 16,'.', 18,'.', 20],\
             [  1,'.',  3,'.',  5,'.',  7,'.',  9,'.'],\
             ['.',  2,'.',  4,'.',  6,'.',  8,'.', 10],\
             [ 21,'.', 23,'.', 25,'.', 27,'.', 29,'.'],\
             ['.', 22,'.', 24,'.', 26,'.', 28,'.', 30],\
             [ 41,'.', 43,'.', 45,'.', 47,'.', 49,'.'],\
             ['.', 42,'.', 44,'.', 46,'.', 48,'.', 50]];

  cnt = 0
  sequence = grid2sequence(static)
  while(not _fleet._sunk):
    [x,y] = sequence[cnt]
    if(board_state[x,y] == '.'):
      if fleet_matrix[x,y] == '.':
        board_state[x,y] = 'M'
      else:
        board_state[x,y] = 'H'
        board_state = sink_algorithm(board_state, _fleet, x, y)
        _fleet.update_status(board_state)
    cnt += 1

  return board_state

def group5_algorithm(_fleet):
  fleet_matrix = _fleet.fleet2matrix()

  board_state = np.array([['.']*10]*10)

  static  = [['.', 48,'.', 38,'.', 21,'.', 37,'.', 47],\
             [ 49,'.', 39,'.', 22,'.', 20,'.', 36,'.'],\
             ['.', 40,'.', 23,'.',  7,'.', 19,'.', 35],\
             [ 41,'.', 24,'.',  8,'.',  6,'.', 18,'.'],\
             ['.', 25,'.',  9,'.',  1,'.',  5,'.', 17],\
             [ 26,'.', 10,'.',  2,'.',  4,'.', 16,'.'],\
             ['.', 27,'.', 11,'.',  3,'.', 15,'.', 34],\
             [ 42,'.', 28,'.', 12,'.', 14,'.', 33,'.'],\
             ['.', 43,'.', 29,'.', 13,'.', 32,'.', 46],\
             [ 50,'.', 44,'.', 30,'.', 31,'.', 45,'.']];

  cnt = 0
  sequence = grid2sequence(static)
  while(not _fleet._sunk):
    [x,y] = sequence[cnt]
    if(board_state[x,y] == '.'):
      if fleet_matrix[x,y] == '.':
        board_state[x,y] = 'M'
      else:
        board_state[x,y] = 'H'
        board_state = sink_algorithm(board_state, _fleet, x, y)
        _fleet.update_status(board_state)
    cnt += 1

  return board_state

def group6_algorithm(_fleet):
  fleet_matrix = _fleet.fleet2matrix()

  board_state = np.array([['.']*10]*10)

  static  = [[ 37,'.', 36,'.', 35,'.', 34,'.', 33,'.'],\
             ['.', 22,'.', 21,'.', 20,'.', 19,'.', 50],\
             [ 38,'.', 11,'.', 10,'.',  9,'.', 32,'.'],\
             ['.', 23,'.',  4,'.',  3,'.', 18,'.', 49],\
             [ 39,'.', 12,'.',  1,'.',  8,'.', 31,'.'],\
             ['.', 24,'.',  5,'.',  2,'.', 17,'.', 48],\
             [ 40,'.', 13,'.',  6,'.',  7,'.', 30,'.'],\
             ['.', 25,'.', 14,'.', 15,'.', 16,'.', 47],\
             [ 41,'.', 26,'.', 27,'.', 28,'.', 29,'.'],\
             ['.', 42,'.', 43,'.', 44,'.', 45,'.', 46]];

  cnt = 0
  sequence = grid2sequence(static)
  nohit = True
  reverse = False
  while(not _fleet._sunk):
    [x,y] = sequence[cnt]
    if(board_state[x,y] == '.'):
      if fleet_matrix[x,y] == '.':
        board_state[x,y] = 'M'
      else:
        board_state[x,y] = 'H'
        board_state = sink_algorithm(board_state, _fleet, x, y)
        _fleet.update_status(board_state)
        nohit = False
    cnt += 1

    # if we aren't finding center values, go other way
    if(cnt > 7 and nohit and not reverse):
      reverse = True
      sequence.reverse()
      cnt = 0

  return board_state

def group7_algorithm(_fleet):
  fleet_matrix = _fleet.fleet2matrix()

  board_state = np.array([['.']*10]*10)

  static  = [[ 22,'.','.', 21,'.','.', 11,'.','.', 10],\
             ['.','.', 20,'.','.', 12,'.','.',  9,'.'],\
             ['.', 19,'.','.', 13,'.','.',  8,'.','.'],\
             [ 18,'.','.', 14,'.','.',  7,'.','.', 28],\
             ['.','.', 15,'.','.',  6,'.','.', 29,'.'],\
             ['.', 16,'.','.',  5,'.','.', 30,'.','.'],\
             [ 17,'.','.',  4,'.','.', 31,'.','.', 27],\
             ['.','.',  3,'.','.', 32,'.','.', 26,'.'],\
             ['.',  2,'.','.', 33,'.','.', 25,'.','.'],\
             [  1,'.','.', 34,'.','.', 24,'.','.', 23]];

  cnt = 0
  sequence = grid2sequence(static)
  nohit = True
  reverse = False
  while(not _fleet._sunk):
    [x,y] = sequence[cnt]
    if(board_state[x,y] == '.'):
      if fleet_matrix[x,y] == '.':
        board_state[x,y] = 'M'
      else:
        board_state[x,y] = 'H'
        board_state = sink_algorithm(board_state, _fleet, x, y)
        _fleet.update_status(board_state)
        nohit = False
    cnt += 1

    if (cnt >= len(sequence)):
      sequence = []
      for x in range(10):
        for y in range(10):
          if(board_state[x,y] == '.'):
            sequence.append([x,y])
      random.shuffle(sequence)
      cnt = 0


  return board_state

def group8_algorithm(_fleet):
  fleet_matrix = _fleet.fleet2matrix()

  board_state = np.array([['.']*10]*10)

  static  = [[ 13,'.', 37,'.', 21, 34,'.', 38,'.', 14],\
             ['.',  5,'.', 25,'.','.', 30,'.',  6,'.'],\
             [ 44,'.',  1,'.', 45,'.','.',  2,'.', 39],\
             ['.', 29,'.', 17,'.','.', 18,'.', 26,'.'],\
             [ 33,'.', 48,'.',  9, 10,'.', 46,'.', 22],\
             [ 24,'.','.','.', 11, 12,'.','.','.', 35],\
             ['.', 28,'.', 19,'.','.', 20,'.', 31,'.'],\
             [ 43,'.',  3,'.','.', 47,'.',  4,'.', 40],\
             ['.',  7,'.', 32,'.','.', 27,'.',  8,'.'],\
             [ 15,'.', 42,'.', 36, 23,'.', 41,'.', 16]];

  cnt = 0
  sequence = grid2sequence(static)
  nohit = True
  reverse = False
  while(not _fleet._sunk):
    [x,y] = sequence[cnt]
    if(board_state[x,y] == '.'):
      if fleet_matrix[x,y] == '.':
        board_state[x,y] = 'M'
      else:
        board_state[x,y] = 'H'
        board_state = sink_algorithm(board_state, _fleet, x, y)
        _fleet.update_status(board_state)
        nohit = False
    cnt += 1

    if (cnt >= len(sequence)):
      sequence = []
      for x in range(10):
        for y in range(10):
          if(board_state[x,y] == '.'):
            sequence.append([x,y])
      random.shuffle(sequence)
      cnt = 0


  return board_state

def group9_algorithm(_fleet):
  fleet_matrix = _fleet.fleet2matrix()

  board_state = np.array([['.']*10]*10)

  static1 = [[ 10,'.', 46,'.', 26,'.', 32,'.', 48,'.'],\
             ['.',  8,'.', 37,'.', 17,'.', 41,'.', 49],\
             [ 44,'.',  6,'.', 24,'.', 30,'.', 43,'.'],\
             ['.', 34,'.',  4,'.', 15,'.', 33,'.', 35],\
             [ 22,'.', 20,'.',  2,'.', 19,'.', 21,'.'],\
             ['.', 13,'.', 11,'.',  1,'.', 12,'.', 14],\
             [ 29,'.', 27,'.', 23,'.',  3,'.', 28,'.'],\
             ['.', 39,'.', 36,'.', 16,'.',  5,'.', 40],\
             [ 47,'.', 45,'.', 25,'.', 31,'.',  7,'.'],\
             ['.', 50,'.', 38,'.', 18,'.', 42,'.',  9]];

  static2 = [[ 10,'.','.', 27,'.','.', 23,'.','.', 34],\
             ['.',  8,'.','.', 18,'.','.', 30,'.','.'],\
             ['.','.',  6,'.','.', 13,'.','.', 31,'.'],\
             [ 25,'.','.',  4,'.','.', 22,'.','.', 26],\
             ['.', 16,'.','.',  2,'.','.', 15,'.','.'],\
             ['.','.', 11,'.','.',  1,'.','.', 12,'.'],\
             [ 20,'.','.', 19,'.','.',  3,'.','.', 21],\
             ['.', 29,'.','.', 17,'.','.',  5,'.','.'],\
             ['.','.', 32,'.','.', 14,'.','.',  7,'.'],\
             [ 33,'.','.', 28,'.','.', 24,'.','.',  9]];

  static3 = [[ 10,'.','.','.', 18,'.','.','.', 24,'.'],\
             ['.',  8,'.','.','.', 13,'.','.','.', 25],\
             ['.','.',  6,'.','.','.', 20,'.','.','.'],\
             ['.','.','.',  4,'.','.','.', 21,'.','.'],\
             [ 16,'.','.','.',  2,'.','.','.', 15,'.'],\
             ['.', 11,'.','.','.',  1,'.','.','.', 12],\
             ['.','.', 19,'.','.','.',  3,'.','.','.'],\
             ['.','.','.', 22,'.','.','.',  5,'.','.'],\
             [ 23,'.','.','.', 17,'.','.','.',  7,'.'],\
             ['.', 26,'.','.','.', 14,'.','.','.',  9]];

  static4 = [[ 10,'.','.','.','.', 12,'.','.','.','.'],\
             ['.',  8,'.','.','.','.', 16,'.','.','.'],\
             ['.','.',  6,'.','.','.','.', 20,'.','.'],\
             ['.','.','.',  4,'.','.','.','.', 17,'.'],\
             ['.','.','.','.',  2,'.','.','.','.', 13],\
             [ 11,'.','.','.','.',  1,'.','.','.','.'],\
             ['.', 15,'.','.','.','.',  3,'.','.','.'],\
             ['.','.', 19,'.','.','.','.',  5,'.','.'],\
             ['.','.','.', 18,'.','.','.','.',  7,'.'],\
             ['.','.','.','.', 14,'.','.','.','.',  9]];

  cnt = 0
  current_seq = 1
  sequence1 = grid2sequence(static1)
  sequence2 = grid2sequence(static2)
  sequence3 = grid2sequence(static3)
  sequence4 = grid2sequence(static4)
  sequence = sequence1
  while(not _fleet._sunk):
    [x,y] = sequence[cnt]
    if(board_state[x,y] == '.'):
      if fleet_matrix[x,y] == '.':
        board_state[x,y] = 'M'
      else:
        board_state[x,y] = 'H'
        board_state = sink_algorithm(board_state, _fleet, x, y)
        _fleet.update_status(board_state)
    cnt += 1
    if(current_seq == 1 and _fleet._ships[4]._sunk):
      sequence = sequence2
      current_seq = 2
      cnt = 0
    if(current_seq == 2 and _fleet._ships[3]._sunk and _fleet._ships[2]._sunk):
      sequence = sequence3
      current_seq = 3
      cnt = 0
    if(current_seq == 3 and _fleet._ships[3]._sunk and _fleet._ships[2]._sunk and _fleet._ships[1]._sunk):
      sequence = sequence4
      current_seq = 4
      cnt = 0
          
  return board_state


def group10_algorithm(_fleet):
  fleet_matrix = _fleet.fleet2matrix()

  board_state = np.array([['.']*10]*10)

  static  = [[  1,'.', 11,'.', 12,'.', 13,'.', 14,'.'],\
             ['.',  2,'.', 15,'.', 16,'.', 17,'.', 18],\
             [ 19,'.',  3,'.', 20,'.', 21,'.', 22,'.'],\
             ['.', 35,'.',  4,'.', 36,'.', 37,'.', 38],\
             [ 23,'.', 24,'.',  5,'.', 25,'.', 26,'.'],\
             ['.', 39,'.', 40,'.',  6,'.', 41,'.', 42],\
             [ 27,'.', 28,'.', 29,'.',  7,'.', 30,'.'],\
             ['.', 43,'.', 44,'.', 45,'.',  8,'.', 46],\
             [ 31,'.', 32,'.', 33,'.', 34,'.',  9,'.'],\
             ['.', 47,'.', 48,'.', 49,'.', 50,'.', 10]];

  cnt = 0
  sequence = grid2sequence(static)
  nohit = True
  reverse = False
  while(not _fleet._sunk):
    [x,y] = sequence[cnt]
    if(board_state[x,y] == '.'):
      if fleet_matrix[x,y] == '.':
        board_state[x,y] = 'M'
      else:
        board_state[x,y] = 'H'
        board_state = sink_algorithm(board_state, _fleet, x, y)
        _fleet.update_status(board_state)
        nohit = False
    cnt += 1

  return board_state

def group11_algorithm(_fleet):
  fleet_matrix = _fleet.fleet2matrix()

  board_state = np.array([['.']*10]*10)

  static  = [[  1,'.', 11,'.', 12,'.', 13,'.', 14,'.'],\
             ['.',  2,'.', 15,'.', 16,'.', 17,'.', 18],\
             [ 19,'.',  3,'.', 20,'.', 21,'.', 22,'.'],\
             ['.', 35,'.',  4,'.', 36,'.', 37,'.', 38],\
             [ 23,'.', 24,'.',  5,'.', 25,'.', 26,'.'],\
             ['.', 39,'.', 40,'.',  6,'.', 41,'.', 42],\
             [ 27,'.', 28,'.', 29,'.',  7,'.', 30,'.'],\
             ['.', 43,'.', 44,'.', 45,'.',  8,'.', 46],\
             [ 31,'.', 32,'.', 33,'.', 34,'.',  9,'.'],\
             ['.', 47,'.', 48,'.', 49,'.', 50,'.', 10]];

  cnt = 0
  sequence = grid2sequence(static)
  nohit = True
  reverse = False
  while(not _fleet._sunk):
    [x,y] = sequence[cnt]
    if(board_state[x,y] == '.'):
      if fleet_matrix[x,y] == '.':
        board_state[x,y] = 'M'
      else:
        board_state[x,y] = 'H'
        board_state = sink_algorithm(board_state, _fleet, x, y)
        _fleet.update_status(board_state)
        nohit = False
    cnt += 1

  return board_state



def extra_algorithm(_fleet):
  fleet_matrix = _fleet.fleet2matrix()

  board_state = np.array([['.']*10]*10)

  static  = [[ 49,'.', 33,'.',  5,'.', 29,'.', 46,'.'],\
             ['.', 37,'.',  9,'.',  1,'.', 25,'.', 45],\
             [ 36,'.', 40,'.', 13,'.', 21,'.', 26,'.'],\
             ['.', 12,'.', 41,'.', 17,'.', 22,'.', 30],\
             [  8,'.', 16,'.', 44,'.', 18,'.',  2,'.'],\
             ['.',  4,'.', 20,'.', 43,'.', 14,'.',  6],\
             [ 32,'.', 24,'.', 19,'.', 42,'.', 10,'.'],\
             ['.', 28,'.', 23,'.', 15,'.', 39,'.', 34],\
             [ 47,'.', 27,'.',  3,'.', 11,'.', 38,'.'],\
             ['.', 48,'.', 31,'.',  7,'.', 35,'.', 50]];

  cnt = 0
  sequence = grid2sequence(static)
  reverse = False
  while(not _fleet._sunk):
    [x,y] = sequence[cnt]
    if(board_state[x,y] == '.'):
      if fleet_matrix[x,y] == '.':
        board_state[x,y] = 'M'
      else:
        board_state[x,y] = 'H'
        board_state = sink_algorithm(board_state, _fleet, x, y)
        _fleet.update_status(board_state)
    cnt += 1

  return board_state

def random_algorithm(_fleet):
  fleet_matrix = _fleet.fleet2matrix()

  board_state = np.array([['.']*10]*10)
  while(not _fleet._sunk):
    x = random.randint(0,9)
    y = random.randint(0,9)
    if(board_state[x,y] == '.'):
      if fleet_matrix[x,y] == '.':
        board_state[x,y] = 'M'
      else:
        board_state[x,y] = 'H'
        board_state = sink_algorithm(board_state, _fleet, x, y)
        _fleet.update_status(board_state)
  return board_state


shot_avg = 0
ntrials = 10000

#algorithms = [random_algorithm, group1_algorithm, group2_algorithm, group5_algorithm, group6_algorithm]
algorithms = [random_algorithm, extra_algorithm]
#algorithm_names = ["Pure Random", "Counter-Clockwise Search", "Dark Knight", "Checkered Quadrants", "Spider Web", "Iterated Guess", "Pentagons", "X factor", "Swirl"]
for alg_idx in range(0,len(algorithms)):
  algorithm = algorithms[alg_idx]
#  algorithm_name = algorithm_names[alg_idx]
  for k in range(ntrials):
    testfleet.scatter()
    fleet_matrix = testfleet.fleet2matrix()

    board_state = algorithm(testfleet)
    nshots = 0
    for i in range(10):
      for j in range(10):
        if(board_state[i,j] != '.'):
          nshots += 1
    shot_avg += nshots
    #print("nshots=",nshots)

  shot_avg /= ntrials
#  print(algorithm_name, shot_avg)
  print(shot_avg)


