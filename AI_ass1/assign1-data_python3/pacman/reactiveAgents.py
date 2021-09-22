# reactiveAgents.py
# ---------------
# Licensing Information: You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC
# Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).
from game import Directions
from game import Agent
from game import Actions
import numpy as np
import util
import time
import search


class NaiveAgent(Agent):
    "An agent that goes West until it can't."

    def getAction(self, state):
        "The agent receives a GameState (defined in pacman.py)."
        sense = state.getPacmanSensor()
        if sense[7]:
            action = Directions.STOP
        else:
            action = Directions.WEST
        return action

class PSAgent(Agent):
    "An agent that follows the boundary using production system."

    def getAction(self, state):
        sense = state.getPacmanSensor()
        x = [sense[1] or sense[2] , sense[3] or sense[4] ,
        sense[5] or sense[6] , sense[7] or sense[0]]
        if x[0] and not x[1]:
            action = Directions.EAST
        elif x[1] and not x[2]:
            action = Directions.SOUTH
        elif x[2] and not x[3]:
            action = Directions.WEST
        elif x[3] and not x[0]:
            action = Directions.NORTH
        else:
            action = Directions.NORTH
        return action

class ECAgent(Agent):
    "An agent that follows the boundary using error-correction."

    def __init__(self):
        # Define weight and threhold learned from Perceptron.py
        self.north_w = [ 0.01, -0.04, -0.04,  0.,    0.,    0.,    0.,    0.01]
        self.north_b = -0.009999999999999997

        self.south_w = [ 0.,    0.,    0.,    0.01,  0.01, -0.04, -0.04,  0.  ]
        self.south_b = -0.009999999999999997

        self.west_w = [-0.04,  0.,    0.,    0.,    0.,    0.01,  0.01, -0.04]
        self.west_b =  -0.009999999999999997

        self.east_w = [ 0.,    0.01,  0.01, -0.04, -0.04,  0.,    0.,    0.  ]
        self.east_b =  -0.009999999999999997

    def getAction(self, state):
        ''' @TODO: Your code goes here! '''
        sense = state.getPacmanSensor()
        x = np.array([sense[0], sense[1], sense[2], sense[3], sense[4] ,
        sense[5], sense[6] , sense[7] ])

        north_val = np.dot(x,np.array(self.north_w).T) + self.north_b
        go_north = north_val >= 0

        south_val = np.dot(x,np.array(self.south_w).T) + self.south_b
        go_south = south_val >= 0

        west_val = np.dot(x,np.array(self.west_w).T) + self.west_b
        go_west = west_val >= 0

        east_val = np.dot(x,np.array(self.east_w).T) + self.east_b
        go_east = east_val >= 0

        if sum([go_north,go_east,go_south,go_west]) >= 1:
            if go_north:
                return Directions.NORTH
            elif go_east:
                return Directions.EAST
            elif go_south:
                return Directions.SOUTH
            else:
                return Directions.WEST
        else:
            return Directions.NORTH

class SMAgent(Agent):
    "An sensory-impaired agent that follows the boundary using state machine."
    def registerInitialState(self,state):
        "The agent receives the initial GameState (defined in pacman.py)."
        sense = state.getPacmanImpairedSensor() 
        self.prevAction = Directions.STOP
        self.prevSense = sense

    def getAction(self, state):
        '''@TODO: Your code goes here! '''  
        sense = state.getPacmanImpairedSensor() 
        w1,w3,w5,w7 = 0,0,0,0
        if self.prevSense[0] == 1 and self.prevAction == Directions.EAST:
            w1 = 1
        if self.prevSense[1] == 1 and self.prevAction == Directions.SOUTH:
            w3 = 1  
        if self.prevSense[2] == 1 and self.prevAction == Directions.WEST:
            w5 = 1 
        if self.prevSense[3] == 1 and self.prevAction == Directions.NORTH:
            w7 = 1    
        full_sense = [w1,sense[0],w3,sense[1],w5,sense[2],w7,sense[3]]  #temperal full sense

        ##Production Function
        if full_sense[1] and not full_sense[3]:
            self.prevAction = Directions.EAST
            self.prevSense = sense
            return Directions.EAST
        elif full_sense[3] and not full_sense[5]:
            self.prevAction = Directions.SOUTH
            self.prevSense = sense
            return Directions.SOUTH
        elif full_sense[5] and not full_sense[7]:
            self.prevAction = Directions.WEST
            self.prevSense = sense
            return Directions.WEST
        elif full_sense[7] and not full_sense[1]:
            self.prevAction = Directions.NORTH
            self.prevSense = sense
            return Directions.NORTH
        elif full_sense[0]:
            self.prevAction = Directions.NORTH
            self.prevSense = sense
            return Directions.NORTH
        elif full_sense[2]:
            self.prevAction = Directions.EAST
            self.prevSense = sense
            return Directions.EAST
        elif full_sense[4]:
            self.prevAction = Directions.SOUTH
            self.prevSense = sense
            return Directions.SOUTH
        elif full_sense[6]:
            self.prevAction = Directions.WEST
            self.prevSense = sense
            return Directions.WEST
        else:
            self.prevAction = Directions.NORTH
            self.prevSense = sense
            return Directions.NORTH
