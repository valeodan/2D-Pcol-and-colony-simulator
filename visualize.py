from matplotlib import pyplot, colors
from matplotlib.widgets import Button
from matplotlib.patches import Rectangle
import matplotlib.patches as mpatches
import numpy
import sys

"""
parameters of visualizer:
1) animation_delay
2) show_default_position
3) ... colours? Like: p>green ...
"""

animation_delay = 0.915 # pause between displaying new iteration in seconds [default: 0.15]

def initPopulation(rows, cols, acoordinates, defaultPosition=False):
    popData = [[0.0 for i in range(1, cols-1)] for j in range(1, rows-1)]
    for coordinates in acoordinates:
        coord_j = coordinates.get("j")-1 #switch j and i
        coord_i = coordinates.get("i")-1
        if coord_i in range(0, rows-2) and coord_j in range (0,cols-2):
            popData[coord_i][coord_j]=1.0 #Agent is not out of the env
    showDefaultPosition(acoordinates[0].get("j")-1, acoordinates[0].get("i")-1, defaultPosition)
    return popData

def updatePlot(step, initplot, popData, envMatrix, animation_delay, colors): # function to update 2D plot
    initplot.set_data(popData)
    pyplot.title("Iteration "+str(step),
                fontsize = 24)
    print (colors)
    markInterest(envMatrix, colors)
    pyplot.pause(animation_delay)

def markInterest(envMatrix,visibleObjectsColors):
    defPos=pyplot.gca().patches.pop(0)
    [p.remove() for p in reversed(pyplot.gca().patches)]
    pyplot.gca().add_patch(defPos) 
    for i,row in enumerate(envMatrix):
        for j,col in enumerate(row):
            for object in col:
                if str(object) in visibleObjectsColors:
                    clr=visibleObjectsColors[str(object)]
                    rect=mpatches.Rectangle((int(j)-0.5, int(i)-0.5), 1, 1, fill=False, color=clr, linewidth=1)
                    pyplot.gca().add_patch(rect)
"""    
Hint: Colour settings:
                clrs = {0:"aquamarine", 1:"mediumaquamarine", 2:"lightgreen", 3:"greenyellow", 4:"yellowgreen", 5:"olivedrab", 6:"seagreen",7:"darkgreen", 8:"olive"};
                clr = "black"
                clrs = {0:"lightpink", 1:"pink", 2:"plum", 3:"violet", 4:"orchid", 5:"darkorchid"};
                clr = "purple"
                clrs = {0:"aquamarine", 1:"mediumaquamarine", 2:"lightgreen", 3:"greenyellow", 4:"yellowgreen", 5:"olivedrab", 6:"seagreen",7:"darkgreen", 8:"olive"};
                clr = "darkgreen"
                rect=mpatches.Rectangle((int(j)-0.5,int(i)-0.5),1,1, fill = False, color = clr,linewidth = 1)
                pyplot.gca().add_patch(rect)
                #[p.remove() for p in reversed(pyplot.gca().patches)]
"""

def showDefaultPosition(x,y,visible):
    lwidth=0
    if visible: lwidth=1
    rect=mpatches.Rectangle((x-0.5,y-0.5),1,1, fill = False, color = "red",linewidth = lwidth)
    pyplot.gca().add_patch(rect)

def initVizualiser(numSteps, rowsEnv, colsEnv, aCoords):
    # using colors from matplotlib, define a color map
    colormap = colors.ListedColormap(["lightgrey","green","blue"])
    # define figure size using pyplot
    fig = pyplot.figure("Model Visualization")
    # using pyplot add a title
    pyplot.title("Iteration 0",
                fontsize = 24)
    subtitle = 'Simulation is running... will run up to ' + str(numSteps) + ' iterations.'
    pyplot.suptitle(subtitle, fontsize = 16, ha='center', va='center')
    # using pyplot add x and y labels
    pyplot.xlabel("x coordinates", fontsize = 20)
    pyplot.ylabel("y coordinates", fontsize = 20)
    # adjust x and y axis ticks, using pyplot
    pyplot.xticks(fontsize = 12)
    pyplot.yticks(fontsize = 12)
    ax = fig.gca()

    ax.set_xticks(numpy.arange(0, colsEnv, 1))
    ax.set_xticks(numpy.arange(-0.5, colsEnv, 1),minor=True)
    ax.set_xticklabels(numpy.arange(1, colsEnv+1, 1))

    ax.set_yticks(numpy.arange(0, rowsEnv, 1)) # EDIT
    ax.set_yticks(numpy.arange(-0.5, rowsEnv, 1), minor=True)
    ax.set_yticklabels(numpy.arange(1, rowsEnv+1, 1))
    pyplot.grid(which='minor')
    # use .imshow() method from pyplot to visualize agent locations
    initplot = pyplot.imshow(X = initPopulation(rowsEnv,colsEnv,aCoords,defaultPosition=True), 
                cmap = colormap) 
    def keypress(keyEvent):
        character = str(keyEvent.key)
        print (character)
        if (character == "c"):
            sys.exit(0)
        if (character == "p"):
            pyplot.pause(5)

    fig.canvas.mpl_connect('key_press_event', keypress)
    pyplot.draw()
    pyplot.pause(animation_delay)
    return initplot

def endOfVisualization(initplot, popData):
    initplot.set_data(popData)
    newtitle = str(pyplot.gca().get_title()) + " [END]"
    pyplot.title(newtitle, fontsize = 24)
    pyplot.suptitle("Click anywhere to exit.", fontsize = 16, ha='center', va='center')
    pyplot.waitforbuttonpress(0)
    pyplot.draw()
    print ("[Info] End of simulation")
