"""
# Simulator and vizualizer
# This application requires Python 3.10 or newer and mathplotlib library
# Authors: Daniel Valenta, Miroslav Langer
"""

# import libraries
from turtle import position
from matplotlib import pyplot, colors
from matplotlib.widgets import Button
from matplotlib.patches import Rectangle
import matplotlib.patches as mpatches
import random
import numpy
import math
import sys

pyplot.style.use('dark_background') #Night mode

"""
App settings - here you can set up parameters of 2D P colony
"""
animation_delay = 0.000000015 # pause between displaying new iteration in seconds [default: 0.15]

# initialization - basic input parameters
n_iterations = 400 # number of iterations (max) [default value: 900]
x_dim = 100 # size of the environment on axis X [default value: 100]
y_dim = 150 # size of the environment on axis Y [default value: 150]
num_of_agents = 100 # size of population [default value: 100]

# initialization - other input parameters
x_base, y_base = int(x_dim/2), int(y_dim/2) # x,y position of nest (base point, anthill) [default value: int(x_dim/2), int(y_dim/2)]
dirchangeconst = 6 # probability of change of direction of the agent in each iteration [default value: 6]

# feromones settings
defaultFI = 40.0 # default value of feromone intensity [default: 40]
rmFI = 1 # constant defines how pheromone vanishes in each iteration [default: 1]

print ("[Info] Application started. Please wait until the end of simulation.")

"""
Structures, variables and functions
"""
#function ensuring the movement of the agent
def AgentMoving(agnt,dir,toEnv=""):
    i, j = agnt.obj3[0], agnt.obj3[1]
    ni, nj = i, j
    if (dir == "R"): #Right
        ni, nj = i,j+1
    elif (dir == "D"): #Down
        ni, nj = i+1,j
    elif (dir == "L"): #Left
        ni, nj = i,j-1
    elif (dir == "U"): #Up
        ni, nj = i-1,j
    else: 
        print ("Function AgentMoving: invalid input 'dir'")
    if not agentColision (ni, nj):
        if toEnv:
            environmentSymbols[i][j].value = toEnv
            environmentSymbols[i][j].size = defaultFI
        agnt.obj3=[ni,nj]
        agnt.ready=False
        agnt.lastDirection = dir
        lastMoveOfAgent[i][j]=0
        lastMoveOfAgent[ni][nj]=0
        return 1 #OK
    else: 
        return 0 

#Agent programs for the first quadrant (the anthill is on the bottom right)
def Q1programs(agnt): #Rules only for quartal Q1 
    i,j = agnt.obj3[0],agnt.obj3[1]
    programs = []
    """Structure of o2:
        [0][1][2]
        [3][4][5]
        [6][7][8]
    print (o2[0],o2[1],o2[2])
    print (o2[3],o2[4],o2[5])
    print (o2[6],o2[7],o2[8])
    """
    
    feromoneOrPrey = False
    for o in agnt.obj2:
        if o=="p" or o=="P":
            feromoneOrPrey = True
    if not feromoneOrPrey:
        if not agent.lastDirection: #All directions can be used
            programs.append(1)
            programs.append(2)
            programs.append(3)
            programs.append(4) 
        #opposite directions cant be used
        elif agent.lastDirection == "L": #except right
            programs.append(2)
            programs.append(3)
            programs.append(4)
        elif agent.lastDirection == "R": #except left
            programs.append(1)
            programs.append(3)
            programs.append(4)
        elif agent.lastDirection == "U": #except down
            programs.append(1)
            programs.append(2)
            programs.append(4)
        elif agent.lastDirection == "D": #except up
            programs.append(1)
            programs.append(2)
            programs.append(3)
         
    if agnt.obj1 == "e" and ((agnt.obj2[2] == "p") or (agnt.obj2[5]=="p") or (agnt.obj2[8]=="p")): #Program 5
        if not (agnt.obj2[4] == "p" or agnt.obj2[4]=="P"):
            programs.append(5) #right
    if agnt.obj1 == "e" and ((agnt.obj2[0] == "p") or (agnt.obj2[3]=="p") or (agnt.obj2[6]=="p")): #Program 6
        if not (agnt.obj2[4] == "p" or agnt.obj2[4]=="P"):
            programs.append(6) #left
    if agnt.obj1 == "e" and ((agnt.obj2[6] == "p") or (agnt.obj2[7]=="p") or (agnt.obj2[8]=="p")): #Program 7
        if not (agnt.obj2[4] == "p" or agnt.obj2[4]=="P"):
            programs.append(7) #down
    if agnt.obj1 == "e" and ((agnt.obj2[0] == "p") or (agnt.obj2[1]=="p") or (agnt.obj2[2]=="p")): #Program 8
        if not (agnt.obj2[4] == "p" or agnt.obj2[4]=="P"):
            programs.append(8) #up
    if (agnt.obj2[4] == "p"): #rule 9, prey is found, program continue with rules 11 or 12
        programs.append(9)
    if (agnt.obj1 == "P"):
        print ("o1 is P !!!")
        #program = 11 or 12 (randomly select)
        print ("both below is applicable, but it can be specified")
        if (agnt.obj2[5] == "P"):
            if not (agnt.obj2[7] == "P"):
                #print ("put P to env AND [go right] applicable - program = 11")
                programs.append(11)
                """
                * * *
                * P P
                * * *
                """
        if (agnt.obj2[7] == "P"):
            if not (agnt.obj2[5] == "P"):
                #print ("put P to env AND [go down] applicable - program = 12")
                programs.append(12)
                """
                * * *
                * P *
                * P *
                """
        if not programs:
            #print ("put P to env AND [go down or right] applicable - program = 13 and 14")
            programs.append(13)
            programs.append(14)
            """
            * * *
            * P *
            * * *
            """
    if agnt.obj1 == "e" and ((agnt.obj2[2] == "P") or (agnt.obj2[5]=="P") or (agnt.obj2[8]=="P")): #Program 19
        if not (agnt.obj2[4] == "p" or agnt.obj2[4]=="P"):
            programs.append(19) #right
            programs.append(19) #right
            programs.append(1) 
    if agnt.obj1 == "e" and ((agnt.obj2[0] == "P") or (agnt.obj2[3]=="P") or (agnt.obj2[6]=="P")): #Program 20
        if not (agnt.obj2[4] == "p" or agnt.obj2[4]=="P"):
            programs.append(20) #left
            programs.append(20) #left
            programs.append(1)
    if agnt.obj1 == "e" and ((agnt.obj2[6] == "P") or (agnt.obj2[7]=="P") or (agnt.obj2[8]=="P")): #Program 21
        if not (agnt.obj2[4] == "p" or agnt.obj2[4]=="P"):
            programs.append(21) #down
            programs.append(21) #down
            programs.append(1) 
    if agnt.obj1 == "e" and ((agnt.obj2[0] == "P") or (agnt.obj2[1]=="P") or (agnt.obj2[2]=="P")): #Program 22
        if not (agnt.obj2[4] == "p" or agnt.obj2[4]=="P"):
            programs.append(22) #up
            programs.append(22) #up
            programs.append(1)
    if (agnt.obj1 == "e" and agnt.obj2[4] == "P"):
        if (agnt.obj2[1] == "P"):
            programs.append(23)
        if (agnt.obj2[3] == "P"):
            programs.append(24)
    doAction(agnt, programs)

#Similar rules for other environmental quadrants
def Q2programs(agnt): #Rules only for quartal Q1 
    i,j = agnt.obj3[0],agnt.obj3[1]
    programs = []
    """Structure of o2:
        [0][1][2]
        [3][4][5]
        [6][7][8]
    print (o2[0],o2[1],o2[2])
    print (o2[3],o2[4],o2[5])
    print (o2[6],o2[7],o2[8])
    """
    
    feromoneOrPrey = False
    for o in agnt.obj2:
        if o=="p" or o=="P":
            feromoneOrPrey = True
    if not feromoneOrPrey:
        if not agent.lastDirection: #All directions can be used
            programs.append(1)
            programs.append(2)
            programs.append(3)
            programs.append(4) 
        #opposite directions cant be used
        elif agent.lastDirection == "L": #except right
            programs.append(2)
            programs.append(3)
            programs.append(4)
        elif agent.lastDirection == "R": #except left
            programs.append(1)
            programs.append(3)
            programs.append(4)
        elif agent.lastDirection == "U": #except down
            programs.append(1)
            programs.append(2)
            programs.append(4)
        elif agent.lastDirection == "D": #except up
            programs.append(1)
            programs.append(2)
            programs.append(3)
         
    if agnt.obj1 == "e" and ((agnt.obj2[2] == "p") or (agnt.obj2[5]=="p") or (agnt.obj2[8]=="p")): #Program 5
        if not (agnt.obj2[4] == "p" or agnt.obj2[4]=="P"):
            programs.append(5) #right
    if agnt.obj1 == "e" and ((agnt.obj2[0] == "p") or (agnt.obj2[3]=="p") or (agnt.obj2[6]=="p")): #Program 6
        if not (agnt.obj2[4] == "p" or agnt.obj2[4]=="P"):
            programs.append(6) #left
    if agnt.obj1 == "e" and ((agnt.obj2[6] == "p") or (agnt.obj2[7]=="p") or (agnt.obj2[8]=="p")): #Program 7
        if not (agnt.obj2[4] == "p" or agnt.obj2[4]=="P"):
            programs.append(7) #down
    if agnt.obj1 == "e" and ((agnt.obj2[0] == "p") or (agnt.obj2[1]=="p") or (agnt.obj2[2]=="p")): #Program 8
        if not (agnt.obj2[4] == "p" or agnt.obj2[4]=="P"):
            programs.append(8) #up
    if (agnt.obj2[4] == "p"): #rule 9, prey is found, program continue with rules 11 or 12
        programs.append(9)
    if (agnt.obj1 == "P"):
        print ("o1 is P !!!")
        #program = 11 or 12 (randomly select)
        print ("both below is applicable, but it can be specified")
        if (agnt.obj2[3] == "P"):
            if not (agnt.obj2[7] == "P"):
                #print ("put P to env AND [go left] applicable - program = 11")
                programs.append(15) #left
                """
                * * *
                * P P
                * * *
                """
        if (agnt.obj2[7] == "P"):
            if not (agnt.obj2[3] == "P"):
                #print ("put P to env AND [go down] applicable - program = 12")
                programs.append(12) #down
                """
                * * *
                * P *
                * P *
                """
        if not programs:
            #print ("put P to env AND [go down or right] applicable - program = 13 and 14")
            programs.append(17)
            programs.append(14)
            """
            * * *
            * P *
            * * *
            """
    if agnt.obj1 == "e" and ((agnt.obj2[2] == "P") or (agnt.obj2[5]=="P") or (agnt.obj2[8]=="P")): #Program 19
        if not (agnt.obj2[4] == "p" or agnt.obj2[4]=="P"):
            programs.append(19) #right
            programs.append(19) #right
            programs.append(1) 
    if agnt.obj1 == "e" and ((agnt.obj2[0] == "P") or (agnt.obj2[3]=="P") or (agnt.obj2[6]=="P")): #Program 20
        if not (agnt.obj2[4] == "p" or agnt.obj2[4]=="P"):
            programs.append(20) #left
            programs.append(20) #left
            programs.append(1)
    if agnt.obj1 == "e" and ((agnt.obj2[6] == "P") or (agnt.obj2[7]=="P") or (agnt.obj2[8]=="P")): #Program 21
        if not (agnt.obj2[4] == "p" or agnt.obj2[4]=="P"):
            programs.append(21) #down
            programs.append(21) #down
            programs.append(1) 
    if agnt.obj1 == "e" and ((agnt.obj2[0] == "P") or (agnt.obj2[1]=="P") or (agnt.obj2[2]=="P")): #Program 22
        if not (agnt.obj2[4] == "p" or agnt.obj2[4]=="P"):
            programs.append(22) #up
            programs.append(22) #up
            programs.append(1) #up
    if (agnt.obj1 == "e" and agnt.obj2[4] == "P"):
        if (agnt.obj2[1] == "P"):
            programs.append(23)
        if (agnt.obj2[5] == "P"):
            programs.append(19)
    doAction(agnt, programs)

def Q3programs(agnt): #Rules only for quartal Q3 
    i,j = agnt.obj3[0],agnt.obj3[1]
    programs = []
    """Structure of o2:
        [0][1][2]
        [3][4][5]
        [6][7][8]
    print (o2[0],o2[1],o2[2])
    print (o2[3],o2[4],o2[5])
    print (o2[6],o2[7],o2[8])
    """
    
    feromoneOrPrey = False
    for o in agnt.obj2:
        if o=="p" or o=="P":
            feromoneOrPrey = True
    if not feromoneOrPrey:
        if not agent.lastDirection: #All directions can be used
            programs.append(1)
            programs.append(2)
            programs.append(3)
            programs.append(4) 
        #opposite directions cant be used
        elif agent.lastDirection == "L": #except right
            programs.append(2)
            programs.append(3)
            programs.append(4)
        elif agent.lastDirection == "R": #except left
            programs.append(1)
            programs.append(3)
            programs.append(4)
        elif agent.lastDirection == "U": #except down
            programs.append(1)
            programs.append(2)
            programs.append(4)
        elif agent.lastDirection == "D": #except up
            programs.append(1)
            programs.append(2)
            programs.append(3)
         
    if agnt.obj1 == "e" and ((agnt.obj2[2] == "p") or (agnt.obj2[5]=="p") or (agnt.obj2[8]=="p")): #Program 5
        if not (agnt.obj2[4] == "p" or agnt.obj2[4]=="P"):
            programs.append(5) #right
    if agnt.obj1 == "e" and ((agnt.obj2[0] == "p") or (agnt.obj2[3]=="p") or (agnt.obj2[6]=="p")): #Program 6
        if not (agnt.obj2[4] == "p" or agnt.obj2[4]=="P"):
            programs.append(6) #left
    if agnt.obj1 == "e" and ((agnt.obj2[6] == "p") or (agnt.obj2[7]=="p") or (agnt.obj2[8]=="p")): #Program 7
        if not (agnt.obj2[4] == "p" or agnt.obj2[4]=="P"):
            programs.append(7) #down
    if agnt.obj1 == "e" and ((agnt.obj2[0] == "p") or (agnt.obj2[1]=="p") or (agnt.obj2[2]=="p")): #Program 8
        if not (agnt.obj2[4] == "p" or agnt.obj2[4]=="P"):
            programs.append(8) #up
    if (agnt.obj2[4] == "p"): #rule 9, prey is found, program continue with rules 11 or 12
        programs.append(9)
    if (agnt.obj1 == "P"):
        print ("o1 is P !!!")
        #program = 11 or 12 (randomly select)
        print ("both below is applicable, but it can be specified")
        if (agnt.obj2[5] == "P"):
            if not (agnt.obj2[1] == "P"):
                #print ("put P to env AND [go right] applicable - program = 11")
                programs.append(11)
                """
                * * *
                * P P
                * * *
                """
        if (agnt.obj2[1] == "P"):
            if not (agnt.obj2[5] == "P"):
                #print ("put P to env AND [go down] applicable - program = 12")
                programs.append(16)
                """
                * * *
                * P *
                * P *
                """
        if not programs:
            #print ("put P to env AND [go down or right] applicable - program = 13 and 14")
            programs.append(13)
            programs.append(18)
            """
            * * *
            * P *
            * * *
            """
    if agnt.obj1 == "e" and ((agnt.obj2[2] == "P") or (agnt.obj2[5]=="P") or (agnt.obj2[8]=="P")): #Program 19
        if not (agnt.obj2[4] == "p" or agnt.obj2[4]=="P"):
            programs.append(19) #right
            programs.append(19) #right
            programs.append(1)
    if agnt.obj1 == "e" and ((agnt.obj2[0] == "P") or (agnt.obj2[3]=="P") or (agnt.obj2[6]=="P")): #Program 20
        if not (agnt.obj2[4] == "p" or agnt.obj2[4]=="P"):
            programs.append(20) #left
            programs.append(20) #left
            programs.append(1) #
    if agnt.obj1 == "e" and ((agnt.obj2[6] == "P") or (agnt.obj2[7]=="P") or (agnt.obj2[8]=="P")): #Program 21
        if not (agnt.obj2[4] == "p" or agnt.obj2[4]=="P"):
            programs.append(21) #down
            programs.append(21) #down
            programs.append(1) #down
    if agnt.obj1 == "e" and ((agnt.obj2[0] == "P") or (agnt.obj2[1]=="P") or (agnt.obj2[2]=="P")): #Program 22
        if not (agnt.obj2[4] == "p" or agnt.obj2[4]=="P"):
            programs.append(22) #up
            programs.append(22) #up
            programs.append(1) #up
    if (agnt.obj1 == "e" and agnt.obj2[4] == "P"):
        if (agnt.obj2[7] == "P"):
            programs.append(21)
        if (agnt.obj2[3] == "P"):
            programs.append(24)
    doAction(agnt, programs)

def Q4programs(agnt): #Rules only for quartal Q1 
    i,j = agnt.obj3[0],agnt.obj3[1]
    programs = []
    """Structure of o2:
        [0][1][2]
        [3][4][5]
        [6][7][8]
    print (o2[0],o2[1],o2[2])
    print (o2[3],o2[4],o2[5])
    print (o2[6],o2[7],o2[8])
    """
    
    feromoneOrPrey = False
    for o in agnt.obj2:
        if o=="p" or o=="P":
            feromoneOrPrey = True
    if not feromoneOrPrey:
        if not agent.lastDirection: #All directions can be used
            programs.append(1)
            programs.append(2)
            programs.append(3)
            programs.append(4) 
        #opposite directions cant be used
        elif agent.lastDirection == "L": #except right
            programs.append(2)
            programs.append(3)
            programs.append(4)
        elif agent.lastDirection == "R": #except left
            programs.append(1)
            programs.append(3)
            programs.append(4)
        elif agent.lastDirection == "U": #except down
            programs.append(1)
            programs.append(2)
            programs.append(4)
        elif agent.lastDirection == "D": #except up
            programs.append(1)
            programs.append(2)
            programs.append(3)
         
    if agnt.obj1 == "e" and ((agnt.obj2[2] == "p") or (agnt.obj2[5]=="p") or (agnt.obj2[8]=="p")): #Program 5
        if not (agnt.obj2[4] == "p" or agnt.obj2[4]=="P"):
            programs.append(5) #right
    if agnt.obj1 == "e" and ((agnt.obj2[0] == "p") or (agnt.obj2[3]=="p") or (agnt.obj2[6]=="p")): #Program 6
        if not (agnt.obj2[4] == "p" or agnt.obj2[4]=="P"):
            programs.append(6) #left
    if agnt.obj1 == "e" and ((agnt.obj2[6] == "p") or (agnt.obj2[7]=="p") or (agnt.obj2[8]=="p")): #Program 7
        if not (agnt.obj2[4] == "p" or agnt.obj2[4]=="P"):
            programs.append(7) #down
    if agnt.obj1 == "e" and ((agnt.obj2[0] == "p") or (agnt.obj2[1]=="p") or (agnt.obj2[2]=="p")): #Program 8
        if not (agnt.obj2[4] == "p" or agnt.obj2[4]=="P"):
            programs.append(8) #up
    if (agnt.obj2[4] == "p"): #rule 9, prey is found, program continue with rules 11 or 12
        programs.append(9)
    if (agnt.obj1 == "P"):
        print ("o1 is P !!!")
        #program = 11 or 12 (randomly select)
        print ("both below is applicable, but it can be specified")
        if (agnt.obj2[3] == "P"):
            if not (agnt.obj2[1] == "P"):
                #print ("put P to env AND [go left] applicable - program = 11")
                programs.append(15) #left
                """
                * * *
                * P P
                * * *
                """
        if (agnt.obj2[1] == "P"):
            if not (agnt.obj2[3] == "P"):
                #print ("put P to env AND [go up] applicable - program = 16")
                programs.append(16) #up
                """
                * * *
                * P *
                * P *
                """
        if not programs:
            #print ("put P to env AND [go up or left] applicable - program = 13 and 14")
            programs.append(18)
            programs.append(17)
            """
            * * *
            * P *
            * * *
            """
    if agnt.obj1 == "e" and ((agnt.obj2[2] == "P") or (agnt.obj2[5]=="P") or (agnt.obj2[8]=="P")): #Program 19
        if not (agnt.obj2[4] == "p" or agnt.obj2[4]=="P"):
            programs.append(19) #right
            programs.append(19) #right
            programs.append(1) 
    if agnt.obj1 == "e" and ((agnt.obj2[0] == "P") or (agnt.obj2[3]=="P") or (agnt.obj2[6]=="P")): #Program 20
        if not (agnt.obj2[4] == "p" or agnt.obj2[4]=="P"):
            programs.append(20) #left
            programs.append(20) #left
            programs.append(1) #left
    if agnt.obj1 == "e" and ((agnt.obj2[6] == "P") or (agnt.obj2[7]=="P") or (agnt.obj2[8]=="P")): #Program 21
        if not (agnt.obj2[4] == "p" or agnt.obj2[4]=="P"):
            programs.append(21) #down
            programs.append(21) #down
            programs.append(1) 
    if agnt.obj1 == "e" and ((agnt.obj2[0] == "P") or (agnt.obj2[1]=="P") or (agnt.obj2[2]=="P")): #Program 22
        if not (agnt.obj2[4] == "p" or agnt.obj2[4]=="P"):
            programs.append(23) #up
            programs.append(23) #up
            programs.append(1) #up
    if (agnt.obj1 == "e" and agnt.obj2[4] == "P"): #21=D, 22=R, 23=U, 24=L
        if (agnt.obj2[7] == "P"):
            programs.append(21)
        if (agnt.obj2[5] == "P"):
            programs.append(19)
    doAction(agnt, programs)

def Q5programs(agnt): #Rules only for quartal Q1 
    i,j = agnt.obj3[0],agnt.obj3[1]
    programs = []
    
    feromoneOrPrey = False
    for o in agent.obj2:
        if o=="p" or o=="P":
            feromoneOrPrey = True
    if not feromoneOrPrey:
        if not agent.lastDirection: #All directions can be used
            programs.append(1)
            programs.append(2)
            programs.append(3)
            programs.append(4) 
        #opposite directions cant be used
        elif agent.lastDirection == "L": #except right
            programs.append(2)
            programs.append(3)
            programs.append(4)
        elif agent.lastDirection == "R": #except left
            programs.append(1)
            programs.append(3)
            programs.append(4)
        elif agent.lastDirection == "U": #except down
            programs.append(1)
            programs.append(2)
            programs.append(4)
        elif agent.lastDirection == "D": #except up
            programs.append(1)
            programs.append(2)
            programs.append(3)
    if agnt.obj1 == "e" and ((agnt.obj2[2] == "p") or (agnt.obj2[5]=="p") or (agnt.obj2[8]=="p")): #Program 5
        if not (agnt.obj2[4] == "p" or agnt.obj2[4]=="P"):
            programs.append(5) #right
    if agnt.obj1 == "e" and ((agnt.obj2[0] == "p") or (agnt.obj2[3]=="p") or (agnt.obj2[6]=="p")): #Program 6
        if not (agnt.obj2[4] == "p" or agnt.obj2[4]=="P"):
            programs.append(6) #left
    if agnt.obj1 == "e" and ((agnt.obj2[6] == "p") or (agnt.obj2[7]=="p") or (agnt.obj2[8]=="p")): #Program 7
        if not (agnt.obj2[4] == "p" or agnt.obj2[4]=="P"):
            programs.append(7) #down
    if agnt.obj1 == "e" and ((agnt.obj2[0] == "p") or (agnt.obj2[1]=="p") or (agnt.obj2[2]=="p")): #Program 8
        if not (agnt.obj2[4] == "p" or agnt.obj2[4]=="P"):
            programs.append(8) #up
    if (agnt.obj2[4] == "p"): #rule 9, prey is found, program continue with rules 11 or 12
        programs.append(9)
    if (agnt.obj1 == "P"):
        print ("o1 is P !!!")
        #program = 11 or 12 (randomly select)
        print ("both below is applicable, but it can be specified")
        if (agnt.obj2[5] == "P"): #12&14=D, 11&13=R, 15&17=L, 16&18=U
            programs.append(11)
        if not programs:
            #print ("put P to env AND [go down or right] applicable - program = 13 and 14")
            programs.append(13)
            
    if agnt.obj1 == "e" and ((agnt.obj2[2] == "P") or (agnt.obj2[5]=="P") or (agnt.obj2[8]=="P")): #Program 19
        if not (agnt.obj2[4] == "p" or agnt.obj2[4]=="P"):
            programs.append(19) #right
            programs.append(19) #right
            programs.append(1)
    if agnt.obj1 == "e" and ((agnt.obj2[0] == "P") or (agnt.obj2[3]=="P") or (agnt.obj2[6]=="P")): #Program 20
        if not (agnt.obj2[4] == "p" or agnt.obj2[4]=="P"):
            programs.append(20) #left
            programs.append(20) #left
            programs.append(1) 
    if agnt.obj1 == "e" and ((agnt.obj2[6] == "P") or (agnt.obj2[7]=="P") or (agnt.obj2[8]=="P")): #Program 21
        if not (agnt.obj2[4] == "p" or agnt.obj2[4]=="P"):
            programs.append(21) #down
            programs.append(21) #down
            programs.append(1) 
    if agnt.obj1 == "e" and ((agnt.obj2[0] == "P") or (agnt.obj2[1]=="P") or (agnt.obj2[2]=="P")): #Program 22
        if not (agnt.obj2[4] == "p" or agnt.obj2[4]=="P"):
            programs.append(22) #up
            programs.append(22) #up
            programs.append(1)
    if (agnt.obj1 == "e" and agnt.obj2[4] == "P"): #21=D, 22=R, 23=U, 24=L
        if (agnt.obj2[1] == "P"):
            programs.append(23)
        if (agnt.obj2[3] == "P"):
            programs.append(24)
        if (agnt.obj2[7] == "P"):
            programs.append(21)
    #pozor, 24 zabrani agentum na konci stopy pokracovat ... to chce symbol P0 --> n (none)
    doAction(agnt, programs)

def Q6programs(agnt): #Rules only for quartal Q6 
    i,j = agnt.obj3[0],agnt.obj3[1]
    programs = []
    
    feromoneOrPrey = False
    for o in agent.obj2:
        if o=="p" or o=="P":
            feromoneOrPrey = True
    if not feromoneOrPrey:
        if not agent.lastDirection: #All directions can be used
            programs.append(1)
            programs.append(2)
            programs.append(3)
            programs.append(4) 
        #opposite directions cant be used
        elif agent.lastDirection == "L": #except right
            programs.append(2)
            programs.append(3)
            programs.append(4)
        elif agent.lastDirection == "R": #except left
            programs.append(1)
            programs.append(3)
            programs.append(4)
        elif agent.lastDirection == "U": #except down
            programs.append(1)
            programs.append(2)
            programs.append(4)
        elif agent.lastDirection == "D": #except up
            programs.append(1)
            programs.append(2)
            programs.append(3)
    if agnt.obj1 == "e" and ((agnt.obj2[2] == "p") or (agnt.obj2[5]=="p") or (agnt.obj2[8]=="p")): #Program 5
        if not (agnt.obj2[4] == "p" or agnt.obj2[4]=="P"):
            programs.append(5) #right
    if agnt.obj1 == "e" and ((agnt.obj2[0] == "p") or (agnt.obj2[3]=="p") or (agnt.obj2[6]=="p")): #Program 6
        if not (agnt.obj2[4] == "p" or agnt.obj2[4]=="P"):
            programs.append(6) #left
    if agnt.obj1 == "e" and ((agnt.obj2[6] == "p") or (agnt.obj2[7]=="p") or (agnt.obj2[8]=="p")): #Program 7
        if not (agnt.obj2[4] == "p" or agnt.obj2[4]=="P"):
            programs.append(7) #down
    if agnt.obj1 == "e" and ((agnt.obj2[0] == "p") or (agnt.obj2[1]=="p") or (agnt.obj2[2]=="p")): #Program 8
        if not (agnt.obj2[4] == "p" or agnt.obj2[4]=="P"):
            programs.append(8) #up
    if (agnt.obj2[4] == "p"): #rule 9, prey is found, program continue with rules 11 or 12
        programs.append(9)
    if (agnt.obj1 == "P"):
        print ("o1 is P !!!")
        #program = 11 or 12 (randomly select)
        print ("both below is applicable, but it can be specified")
        if (agnt.obj2[3] == "P"): #12&14=D, 11&13=R, 15&17=L, 16&18=U
            programs.append(15)
        if not programs:
            #print ("put P to env AND [go down or right] applicable - program = 13 and 14")
            programs.append(17)
            
    if agnt.obj1 == "e" and ((agnt.obj2[2] == "P") or (agnt.obj2[5]=="P") or (agnt.obj2[8]=="P")): #Program 19
        if not (agnt.obj2[4] == "p" or agnt.obj2[4]=="P"):
            programs.append(19) #right
            programs.append(19) #right
            programs.append(1) 
    if agnt.obj1 == "e" and ((agnt.obj2[0] == "P") or (agnt.obj2[3]=="P") or (agnt.obj2[6]=="P")): #Program 20
        if not (agnt.obj2[4] == "p" or agnt.obj2[4]=="P"):
            programs.append(20) #left
            programs.append(20) #left
            programs.append(1)
    if agnt.obj1 == "e" and ((agnt.obj2[6] == "P") or (agnt.obj2[7]=="P") or (agnt.obj2[8]=="P")): #Program 21
        if not (agnt.obj2[4] == "p" or agnt.obj2[4]=="P"):
            programs.append(21) #down
            programs.append(21) #down
            programs.append(1) 
    if agnt.obj1 == "e" and ((agnt.obj2[0] == "P") or (agnt.obj2[1]=="P") or (agnt.obj2[2]=="P")): #Program 22
        if not (agnt.obj2[4] == "p" or agnt.obj2[4]=="P"):
            programs.append(22) #up
            programs.append(22) #up
            programs.append(1)
    if (agnt.obj1 == "e" and agnt.obj2[4] == "P"): #21=D, 22=R, 23=U, 24=L
        if (agnt.obj2[1] == "P"):
            programs.append(23)
        if (agnt.obj2[5] == "P"):
            programs.append(19)
        if (agnt.obj2[7] == "P"):
            programs.append(21)
    #pozor, 24 zabrani agentum na konci stopy pokracovat ... to chce symbol P0 --> n (none)
    doAction(agnt, programs)

def Q7programs(agnt): #Rules only for quartal Q1 
    i,j = agnt.obj3[0],agnt.obj3[1]
    programs = []
    
    feromoneOrPrey = False
    for o in agent.obj2:
        if o=="p" or o=="P":
            feromoneOrPrey = True
    if not feromoneOrPrey:
        if not agent.lastDirection: #All directions can be used
            programs.append(1)
            programs.append(2)
            programs.append(3)
            programs.append(4) 
        #opposite directions cant be used
        elif agent.lastDirection == "L": #except right
            programs.append(2)
            programs.append(3)
            programs.append(4)
        elif agent.lastDirection == "R": #except left
            programs.append(1)
            programs.append(3)
            programs.append(4)
        elif agent.lastDirection == "U": #except down
            programs.append(1)
            programs.append(2)
            programs.append(4)
        elif agent.lastDirection == "D": #except up
            programs.append(1)
            programs.append(2)
            programs.append(3)
    if agnt.obj1 == "e" and ((agnt.obj2[2] == "p") or (agnt.obj2[5]=="p") or (agnt.obj2[8]=="p")): #Program 5
        if not (agnt.obj2[4] == "p" or agnt.obj2[4]=="P"):
            programs.append(5) #right
    if agnt.obj1 == "e" and ((agnt.obj2[0] == "p") or (agnt.obj2[3]=="p") or (agnt.obj2[6]=="p")): #Program 6
        if not (agnt.obj2[4] == "p" or agnt.obj2[4]=="P"):
            programs.append(6) #left
    if agnt.obj1 == "e" and ((agnt.obj2[6] == "p") or (agnt.obj2[7]=="p") or (agnt.obj2[8]=="p")): #Program 7
        if not (agnt.obj2[4] == "p" or agnt.obj2[4]=="P"):
            programs.append(7) #down
    if agnt.obj1 == "e" and ((agnt.obj2[0] == "p") or (agnt.obj2[1]=="p") or (agnt.obj2[2]=="p")): #Program 8
        if not (agnt.obj2[4] == "p" or agnt.obj2[4]=="P"):
            programs.append(8) #up
    if (agnt.obj2[4] == "p"): #rule 9, prey is found, program continue with rules 11 or 12
        programs.append(9)
    if (agnt.obj1 == "P"):
        print ("o1 is P !!!")
        #program = 12 or 14 (randomly select)
        print ("both below is applicable, but it can be specified")
        if (agnt.obj2[5] == "P"): #12&14=D, 11&13=R, 15&17=L, 16&18=U
            programs.append(12)
        if not programs:
            #print ("put P to env AND [go down or right] applicable - program = 13 and 14")
            programs.append(14)
            
    if agnt.obj1 == "e" and ((agnt.obj2[2] == "P") or (agnt.obj2[5]=="P") or (agnt.obj2[8]=="P")): #Program 19
        if not (agnt.obj2[4] == "p" or agnt.obj2[4]=="P"):
            programs.append(19) #right
            programs.append(19) #right
            programs.append(1) 
    if agnt.obj1 == "e" and ((agnt.obj2[0] == "P") or (agnt.obj2[3]=="P") or (agnt.obj2[6]=="P")): #Program 20
        if not (agnt.obj2[4] == "p" or agnt.obj2[4]=="P"):
            programs.append(20) #left
            programs.append(20) #left
            programs.append(1)
    if agnt.obj1 == "e" and ((agnt.obj2[6] == "P") or (agnt.obj2[7]=="P") or (agnt.obj2[8]=="P")): #Program 21
        if not (agnt.obj2[4] == "p" or agnt.obj2[4]=="P"):
            programs.append(21) #down
            programs.append(21) #down
            programs.append(1)
    if agnt.obj1 == "e" and ((agnt.obj2[0] == "P") or (agnt.obj2[1]=="P") or (agnt.obj2[2]=="P")): #Program 22
        if not (agnt.obj2[4] == "p" or agnt.obj2[4]=="P"):
            programs.append(22) #up
            programs.append(22) #up
            programs.append(1)
    if (agnt.obj1 == "e" and agnt.obj2[4] == "P"): #21=D, 22=R, 23=U, 24=L
        if (agnt.obj2[1] == "P"):
            programs.append(23)
        if (agnt.obj2[3] == "P"):
            programs.append(24)
        if (agnt.obj2[5] == "P"):
            programs.append(19)
    #pozor, 24 zabrani agentum na konci stopy pokracovat ... to chce symbol P0 --> n (none)
    doAction(agnt, programs)

def Q8programs(agnt): #Rules only for quartal Q1 
    i,j = agnt.obj3[0],agnt.obj3[1]
    programs = []
    
    feromoneOrPrey = False
    for o in agent.obj2:
        if o=="p" or o=="P":
            feromoneOrPrey = True
    if not feromoneOrPrey:
        if not agent.lastDirection: #All directions can be used
            programs.append(1)
            programs.append(2)
            programs.append(3)
            programs.append(4) 
        #opposite directions cant be used
        elif agent.lastDirection == "L": #except right
            programs.append(2)
            programs.append(3)
            programs.append(4)
        elif agent.lastDirection == "R": #except left
            programs.append(1)
            programs.append(3)
            programs.append(4)
        elif agent.lastDirection == "U": #except down
            programs.append(1)
            programs.append(2)
            programs.append(4)
        elif agent.lastDirection == "D": #except up
            programs.append(1)
            programs.append(2)
            programs.append(3)
    if agnt.obj1 == "e" and ((agnt.obj2[2] == "p") or (agnt.obj2[5]=="p") or (agnt.obj2[8]=="p")): #Program 5
        if not (agnt.obj2[4] == "p" or agnt.obj2[4]=="P"):
            programs.append(5) #right
    if agnt.obj1 == "e" and ((agnt.obj2[0] == "p") or (agnt.obj2[3]=="p") or (agnt.obj2[6]=="p")): #Program 6
        if not (agnt.obj2[4] == "p" or agnt.obj2[4]=="P"):
            programs.append(6) #left
    if agnt.obj1 == "e" and ((agnt.obj2[6] == "p") or (agnt.obj2[7]=="p") or (agnt.obj2[8]=="p")): #Program 7
        if not (agnt.obj2[4] == "p" or agnt.obj2[4]=="P"):
            programs.append(7) #down
    if agnt.obj1 == "e" and ((agnt.obj2[0] == "p") or (agnt.obj2[1]=="p") or (agnt.obj2[2]=="p")): #Program 8
        if not (agnt.obj2[4] == "p" or agnt.obj2[4]=="P"):
            programs.append(8) #up
    if (agnt.obj2[4] == "p"): #rule 9, prey is found, program continue with rules 11 or 12
        programs.append(9)
    if (agnt.obj1 == "P"):
        print ("o1 is P !!!")
        #program = 12 or 14 (randomly select)
        print ("both below is applicable, but it can be specified")
        if (agnt.obj2[5] == "P"): #12&14=D, 11&13=R, 15&17=L, 16&18=U
            programs.append(16)
        if not programs:
            #print ("put P to env AND [go down or right] applicable - program = 13 and 14")
            programs.append(18)
            
    if agnt.obj1 == "e" and ((agnt.obj2[2] == "P") or (agnt.obj2[5]=="P") or (agnt.obj2[8]=="P")): #Program 19
        if not (agnt.obj2[4] == "p" or agnt.obj2[4]=="P"):
            programs.append(19) #right #19 R 20 L 21 D 22 U
            programs.append(19) #right #19 R 20 L 21 D 22 U
            programs.append(1) 
    if agnt.obj1 == "e" and ((agnt.obj2[0] == "P") or (agnt.obj2[3]=="P") or (agnt.obj2[6]=="P")): #Program 20
        if not (agnt.obj2[4] == "p" or agnt.obj2[4]=="P"):
            programs.append(20) #left
            programs.append(20) #left
            programs.append(1)
    if agnt.obj1 == "e" and ((agnt.obj2[6] == "P") or (agnt.obj2[7]=="P") or (agnt.obj2[8]=="P")): #Program 21
        if not (agnt.obj2[4] == "p" or agnt.obj2[4]=="P"):
            programs.append(21) #down
            programs.append(21) #down
            programs.append(1)
    if agnt.obj1 == "e" and ((agnt.obj2[0] == "P") or (agnt.obj2[1]=="P") or (agnt.obj2[2]=="P")): #Program 22
        if not (agnt.obj2[4] == "p" or agnt.obj2[4]=="P"):
            programs.append(22) #up
            programs.append(22) #up
            programs.append(1)
    if (agnt.obj1 == "e" and agnt.obj2[4] == "P"): #21=D, 22=R, 23=U, 24=L
        if (agnt.obj2[7] == "P"):
            programs.append(21)
        if (agnt.obj2[3] == "P"):
            programs.append(24)
        if (agnt.obj2[5] == "P"):
            programs.append(19)
    #pozor, 24 zabrani agentum na konci stopy pokracovat ... to chce symbol P0 --> n (none)
    doAction(agnt, programs)

def OTHERprogramsREMOVE(agnt): #Rules only for quartal Q1 
    i,j = agnt.obj3[0],agnt.obj3[1]
    programs = []
    
    feromoneOrPrey = False

    if not feromoneOrPrey:
        if not agent.lastDirection: #All directions can be used
            programs.append(1)
            programs.append(2)
            programs.append(3)
            programs.append(4) 
        #opposite directions cant be used
        elif agent.lastDirection == "L": #except right
            programs.append(2)
            programs.append(3)
            programs.append(4)
        elif agent.lastDirection == "R": #except left
            programs.append(1)
            programs.append(3)
            programs.append(4)
        elif agent.lastDirection == "U": #except down
            programs.append(1)
            programs.append(2)
            programs.append(4)
        elif agent.lastDirection == "D": #except up
            programs.append(1)
            programs.append(2)
            programs.append(3)
    doAction(agnt, programs)

def doAction(agnt, programs=[]):
    if programs:
        #select program from applicable programs
        selected = random.choice(programs)
        print ("...", programs, selected)
        #do program 
        match (selected):
            case 1:
                x = int (random.choice(range(1,11))) #probability to change direction can be adjusted in app settings
                if x < dirchangeconst and agnt.lastDirection: #do not change direction
                    AgentMoving(agnt,agnt.lastDirection) 
                else: #change direction
                    AgentMoving(agnt,"R")
            case 2:
                x = int (random.choice(range(1,11)))
                if x < dirchangeconst and agnt.lastDirection:
                    AgentMoving(agnt,agnt.lastDirection) 
                else:
                    AgentMoving(agnt,"L") #left
            case 3:
                x = int (random.choice(range(1,11)))
                if x < dirchangeconst and agnt.lastDirection:
                    AgentMoving(agnt,agnt.lastDirection) 
                else:
                    AgentMoving(agnt,"D") #down
            case 4: 
                x = int (random.choice(range(1,11)))
                if x < dirchangeconst and agnt.lastDirection:
                    AgentMoving(agnt,agnt.lastDirection) 
                else:
                    AgentMoving(agnt,"U") #up
            case 5:
                AgentMoving(agnt,"R") #right
            case 6:
                AgentMoving(agnt,"L")#left
            case 7:
                AgentMoving(agnt,"D") #down
            case 8:
                AgentMoving(agnt,"U") #up
            case 9:
                agnt.obj1="P"
                environmentSymbols[i][j].value="P"
            case 10:
                print("program 10 not defined")
            case 11: #put P to env AND [go right] 
                AgentMoving(agnt,"R",agnt.obj1) #Agent moved successfully
            case 12: #put P to env AND [go down]  #12&14=D, 11&13=R, 15&17=L, 16&18=U
                #1) communicating rule - push pheromone into environment
                AgentMoving(agnt,"D",agnt.obj1) #Agent moved successfully
            case 13: #put P to env AND [go right] 
                AgentMoving(agnt,"R",agnt.obj1) #Agent moved successfully
            case 14: #put P to env AND [go down] 
                AgentMoving(agnt,"D",agnt.obj1) #Agent moved successfully
            #15,16,17,18 for Q0 with prey
            case 15: #put P to env AND [go left]
                AgentMoving(agnt,"L",agnt.obj1) #Agent moved successfully
            case 16: #put P to env AND [go up]
                AgentMoving(agnt,"U",agnt.obj1) #Agent moved successfully
            case 17: #put P to env AND [go left]
                AgentMoving(agnt,"L",agnt.obj1) #Agent moved successfully
            case 18: #put P to env AND [go up]
                AgentMoving(agnt,"U",agnt.obj1) #Agent moved successfully
            case 19: #19 R 20 L 21 D 22 U
                AgentMoving(agnt,"R") #right
            case 20:
                AgentMoving(agnt,"L") #left
            case 21:
                AgentMoving(agnt,"D") #down 
            case 22: 
                AgentMoving(agnt,"U") #right
            case 23:
                AgentMoving(agnt,"U") #up
            case 24:
                AgentMoving(agnt,"L") #left
            case 25:
                print("do nothing")
            case _:        
                return 0 #default case if program not found

def Quartal(i,j): #"Compass" 
    if i < x_base and j < y_base:
        return 1
    elif i < x_base and j > y_base:
        return 2
    elif i > x_base and j < y_base:
        return 3
    elif i > x_base and j > y_base:
        return 4
    elif i == x_base and j < y_base:
        return 5
    elif i == x_base and j > y_base:
        return 6
    elif i < x_base and j == y_base:
        return 7
    elif i > x_base and j == y_base:
        return 8
    else:
        return 9 # anthill 


# class, defining agents as abstract data types
class agent:#ready=True, obj1=e, obj2=e, obj3=[x,y]
    # init-method, the constructor method for agents with 2 internal objects
    def __init__(self,ready,obj1,obj2,obj3):
        self.ready = ready #Agent is ready to move
        self.obj1 = obj1 #first object of the agent
        self.obj2 = obj2 #second object of the agent
        self.obj3 = obj3
        self.lastDirection = ""

preylist = []

def updatePlot(initplot): # function to update 2D plot, positions of agents are also updated
    # producing a plot of all battlefield locations, 10 iterations after
    popData = [[0.0 for j in range(0,y_dim)] for i in range(0,x_dim)]
    for agent in population:
        popData[agent.obj3[0]][agent.obj3[1]]=1.0
    initplot.set_data(popData)
    rect=mpatches.Rectangle((y_base-0.5,x_base-0.5),1,1, fill = False, color = "red",linewidth = 1)
    pyplot.gca().add_patch(rect)
    
    for i in range(1,x_dim):
        for j in range(1,y_dim):
            if environmentSymbols[i][j].value == 'P':
                clrs = {0:"aquamarine", 1:"mediumaquamarine", 2:"lightgreen", 3:"greenyellow", 4:"yellowgreen", 5:"olivedrab", 6:"seagreen",7:"darkgreen", 8:"olive"};
                clr = "black"
                sz = int(environmentSymbols[i][j].size)
                if 0 <= sz <= 5:
                    clr = clrs[sz]
                rect=mpatches.Rectangle((int(j)-0.5,int(i)-0.5),1,1, fill = False, color = clr,linewidth = 1)
                pyplot.gca().add_patch(rect)
                if environmentSymbols[i][j].size < 1:
                    environmentSymbols[i][j].value = 'e'
                else:
                    environmentSymbols[i][j].size -= rmFI
            if environmentSymbols[i][j].value == 'p':
                clrs = {0:"lightpink", 1:"pink", 2:"plum", 3:"violet", 4:"orchid", 5:"darkorchid"};
                clr = "purple"
                sz = int(environmentSymbols[i][j].size)
                if 0 <= sz <= 5:
                    clr = clrs[sz]
                rect=mpatches.Rectangle((int(j)-0.5,int(i)-0.5),1,1, fill = False, color = clr,linewidth = 1)
                pyplot.gca().add_patch(rect)
            elif (environmentSymbols[i][j].value == 'L' or environmentSymbols[i][j].value == 'R' or environmentSymbols[i][j].value == 'U' or environmentSymbols[i][j].value == 'D'):
                clrs = {0:"aquamarine", 1:"mediumaquamarine", 2:"lightgreen", 3:"greenyellow", 4:"yellowgreen", 5:"olivedrab", 6:"seagreen",7:"darkgreen", 8:"olive"};
                clr = "darkgreen"
                sz = int(environmentSymbols[i][j].size)
                if 0 <= sz <= 5:
                    clr = clrs[sz]
                rect=mpatches.Rectangle((int(j)-0.5,int(i)-0.5),1,1, fill = False, color = clr,linewidth = 1)
                pyplot.gca().add_patch(rect)
                if environmentSymbols[i][j].size < 1:
                    environmentSymbols[i][j].value = 'e'
                else:
                    environmentSymbols[i][j].size -= rmFI

    #for prey in preylist:
    #    rect=mpatches.Rectangle((int(prey[1])-0.5,int(prey[0])-0.5),1,1, fill = False, color = "purple",linewidth = 1)
    #    pyplot.gca().add_patch(rect)
    pyplot.pause(animation_delay)
    [p.remove() for p in reversed(pyplot.gca().patches)]

    #pyplot.draw()

population = []

class envSymb:
    # init-method, the constructor method for agents with 2 internal objects
    def __init__(self,sym,size=0):
        self.size = size # define size, 0=not defined, >0: for example if p=prey, size = max number of visits by agents before prey is eaten
        self.value = sym #prey

"""
Put prey source into the environment
"""

########
#Generating extremes (prey) using normal distribution
########
environmentSymbols = [[envSymb('e') for j in range(0,y_dim)] for i in range(0,x_dim)]
for i in range (0, x_dim):
    addPrey = numpy.random.normal(10, 5, size=y_dim) #10 is the mean value, 5 is the standart deviation.
    for j in range (0, y_dim):
        if int(addPrey[j]) > 21:
            environmentSymbols[int(i-1)][int(j-1)] = envSymb('p',5)#'p' #prey
            preylist.append([i-1,j-1])
preyCounter=0
for i in range(1,x_dim):
        for j in range(1,y_dim):
            if environmentSymbols[i][j].value == 'p':
                preyCounter=preyCounter+1

"""environmentSymbols[int(70)][int(50)] = envSymb('p',5)#'p' #prey
preylist.append([70,50])
environmentSymbols[int(30)][int(90)] = envSymb('p',5) #prey
preylist.append([30,90])
environmentSymbols[int(45)][int(100)] = envSymb('p',5) #prey
preylist.append([45,100])
environmentSymbols[int(50)][int(50)] = envSymb('p',5) #prey
preylist.append([50,50])
environmentSymbols[int(25)][int(25)] = envSymb('p',5) #prey
preylist.append([25,25])
environmentSymbols[int(80)][int(100)] = envSymb('p',5) #prey
preylist.append([80,100])
#environmentSymbols[int(80)][int(40)] = 'p' #prey
#environmentSymbols[int(50)][int(90)] = 'p' #prey"""
lastMoveOfAgent = [[0 for j in range(0,y_dim)] for i in range(0,x_dim)]

# -- define a function for creating agents and assigning them to environment
def agentCreator(size,Ready,Obj1, Obj2, Obj3):
    #Agent: ready=True, obj1=e, obj2=e, obj3=[x,y]
    for j in range(0,size):
        newAgent = agent(ready=Ready, obj1=Obj1, obj2=Obj2, obj3=Obj3)
        population.append(newAgent)

# create agents; 
agentCreator(size = num_of_agents, Ready= False, Obj1= "e", Obj2= "e", Obj3= [x_base-1,y_base-1])

popData = [[0.0 for j in range(0,y_dim)] for i in range(0,x_dim)]
for agent in population:
    popData[agent.obj3[0]][agent.obj3[1]] = 1.0

# using colors from matplotlib, define a color map
colormap = colors.ListedColormap(["lightgrey","green","blue"])
# define figure size using pyplot
fig = pyplot.figure("Model Visualization")
# using pyplot add a title
pyplot.title("Iteration 0",
            fontsize = 24)
pyplot.suptitle("Simulation is running...", fontsize = 16, ha='center', va='center')
# using pyplot add x and y labels
pyplot.xlabel("x coordinates", fontsize = 20)
pyplot.ylabel("y coordinates", fontsize = 20)
# adjust x and y axis ticks, using pyplot
pyplot.xticks(fontsize = 16)
pyplot.yticks(fontsize = 16)
# use .imshow() method from pyplot to visualize agent locations
initplot = pyplot.imshow(X = popData,
             cmap = colormap)
def keypress(keyEvent):
    character = str(keyEvent.key)
    print (character)
    if (character == "c"):
        sys.exit(0)
    if (character == "p"):
        pyplot.pause(5)
    """
    Other shortcuts can be defined here.
    """
fig.canvas.mpl_connect('key_press_event', keypress)
pyplot.draw()


def agentColision (ni, nj):
    if ni < x_dim-1 and ni > 0 and nj < y_dim-1 and nj > 0:
        return False
    else: 
        return True


def changeAgentDir(i,j): #Random movement of agent inside environment boundaries
    ni, nj = i, j
    x = lastMoveOfAgent[i][j] #Vychozi hodnota 0 - mozno pouzit libovolny smer
    prevDirection = 0 #zabranuje pohyb zpet na pozici v predchozim kroku
    while (x == int(lastMoveOfAgent[i][j])): #
        x = random.choice(range(1,5))
    if (x == 1):
        ni = ni-1 #U
        prevDirection = 2
    elif (x == 2):
        ni = ni+1 #D
        prevDirection = 1
    elif (x == 3):
        nj = nj-1 #L
        prevDirection = 4
    else:
        nj = nj+1 #R
        prevDirection = 3
    if (0 < ni < x_dim) and (0 < nj < y_dim): 
        if agentColision(ni, nj):
            return i,j,0
        else:
            return ni,nj, prevDirection
    else:
        return (changeAgentDir(i,j)) #new position is out of the environment => generate new position again

"""
Main cycle
"""
#pyplot.pause(20.0)
itercount = 1
for counter in range(0,n_iterations): # in this case I am conducting "n_iterations" iterations 
    for agent in population:#set each of the agent ready to do action at begining of new iteration
        agent.ready = True
    # iterating through all cells on the battlefield
    for agent in population:
        i,j = agent.obj3[0],agent.obj3[1]
        if agent.ready:
            #print ("is ready")
            if i==x_base and j==y_base: 
                ni, nj, prevdir = changeAgentDir(i,j)
                agent.obj3=[ni,nj]
                agent.obj1="e"
                agent.ready=False
            elif (Quartal(i,j) == 1):
                agent.obj2 = [environmentSymbols[i-1][j-1].value,environmentSymbols[i-1][j].value,environmentSymbols[i-1][j+1].value,environmentSymbols[i][j-1].value,environmentSymbols[i][j].value,environmentSymbols[i][j+1].value,environmentSymbols[i+1][j-1].value,environmentSymbols[i+1][j].value,environmentSymbols[i+1][j+1].value]
                Q1programs(agent)
            #DEFINE Q2,Q3,Q4
            elif (Quartal(i,j) == 2):
                agent.obj2 = [environmentSymbols[i-1][j-1].value,environmentSymbols[i-1][j].value,environmentSymbols[i-1][j+1].value,environmentSymbols[i][j-1].value,environmentSymbols[i][j].value,environmentSymbols[i][j+1].value,environmentSymbols[i+1][j-1].value,environmentSymbols[i+1][j].value,environmentSymbols[i+1][j+1].value]
                Q2programs(agent)
            elif (Quartal(i,j) == 3):
                agent.obj2 = [environmentSymbols[i-1][j-1].value,environmentSymbols[i-1][j].value,environmentSymbols[i-1][j+1].value,environmentSymbols[i][j-1].value,environmentSymbols[i][j].value,environmentSymbols[i][j+1].value,environmentSymbols[i+1][j-1].value,environmentSymbols[i+1][j].value,environmentSymbols[i+1][j+1].value]
                Q3programs(agent)
            elif (Quartal(i,j) == 4):
                agent.obj2 = [environmentSymbols[i-1][j-1].value,environmentSymbols[i-1][j].value,environmentSymbols[i-1][j+1].value,environmentSymbols[i][j-1].value,environmentSymbols[i][j].value,environmentSymbols[i][j+1].value,environmentSymbols[i+1][j-1].value,environmentSymbols[i+1][j].value,environmentSymbols[i+1][j+1].value]
                Q4programs(agent)
            elif (Quartal(i,j) == 5): #X-axis left
                agent.obj2 = [environmentSymbols[i-1][j-1].value,environmentSymbols[i-1][j].value,environmentSymbols[i-1][j+1].value,environmentSymbols[i][j-1].value,environmentSymbols[i][j].value,environmentSymbols[i][j+1].value,environmentSymbols[i+1][j-1].value,environmentSymbols[i+1][j].value,environmentSymbols[i+1][j+1].value]
                Q5programs(agent)
            elif (Quartal(i,j) == 6): #X-axis right
                agent.obj2 = [environmentSymbols[i-1][j-1].value,environmentSymbols[i-1][j].value,environmentSymbols[i-1][j+1].value,environmentSymbols[i][j-1].value,environmentSymbols[i][j].value,environmentSymbols[i][j+1].value,environmentSymbols[i+1][j-1].value,environmentSymbols[i+1][j].value,environmentSymbols[i+1][j+1].value]
                Q6programs(agent)
            elif (Quartal(i,j) == 7): #Y-axis up
                agent.obj2 = [environmentSymbols[i-1][j-1].value,environmentSymbols[i-1][j].value,environmentSymbols[i-1][j+1].value,environmentSymbols[i][j-1].value,environmentSymbols[i][j].value,environmentSymbols[i][j+1].value,environmentSymbols[i+1][j-1].value,environmentSymbols[i+1][j].value,environmentSymbols[i+1][j+1].value]
                Q7programs(agent)
            elif (Quartal(i,j) == 8): 
                agent.obj2 = [environmentSymbols[i-1][j-1].value,environmentSymbols[i-1][j].value,environmentSymbols[i-1][j+1].value,environmentSymbols[i][j-1].value,environmentSymbols[i][j].value,environmentSymbols[i][j+1].value,environmentSymbols[i+1][j-1].value,environmentSymbols[i+1][j].value,environmentSymbols[i+1][j+1].value]
                Q8programs(agent)
            else:
                print("Quartal not defined yet:", Quartal(i,j))  
                #OTHERprogramsREMOVE(agent)             
    # Display iteration number and update environment
    newtitle = "Iteration " + str(itercount) + " of " + str(n_iterations)
    pyplot.title(newtitle,
            fontsize = 24)
    updatePlot(initplot)
    itercount = itercount + 1

"""
End of simulation
"""
preyCounterFin=0
for i in range(1,x_dim):
        for j in range(1,y_dim):
            if environmentSymbols[i][j].value == 'p':
                preyCounterFin=preyCounterFin+1
print ("Prey counter at the start of the computation:", preyCounter)
print ("Prey counter at the end of the computation:", preyCounterFin)
preyFound=preyCounter-preyCounterFin
print ("The number of preys taken from the environment:", preyCounter-preyCounterFin)
file_path = "C:\\Users\\valeodan\\Desktop\\develop\\newresults.txt"
with open(file_path, "a", encoding="utf-8") as file:
    toFile = str(preyCounter)+","+str(preyCounterFin)+","+str(preyFound)+"\n"
    file.write(toFile)

newtitle = "Iteration " + str(itercount - 1) + " of " + str(n_iterations) + " [end]"
pyplot.title(newtitle, fontsize = 24)
pyplot.suptitle("Click anywhere to exit.", fontsize = 16, ha='center', va='center')
#pyplot.waitforbuttonpress(0)
pyplot.draw()
print ("[Info] End of simulation")