import extractExcel
import colony as col
import visualize2
import sys
import os

"""
Select the visualizer:
0 = Without visualizer (console output only)
1 = Tkinter-based visualizer (more detailed)
2 = PyGame-based visualizer (faster)
"""
visualizer=2

def main(args=sys.argv[1:]):
    if len(args):
        definitionFile = str(args[0])
    else:
        pyDir = os.path.dirname(os.path.realpath(__file__)) #Get directory of the current .py script
        definitionFile = pyDir + '\\colony.xlsx'
    colonieDefinition = extractExcel.getColonie(definitionFile)
    colony = col.Colony(colonieDefinition['environment'], colonieDefinition['agents'],
                        colonieDefinition['parameters']['jokerSymbols']
                        )
    step = 0
    steps = colonieDefinition['parameters']['steps']
    agentCoords = [o.coordinates for o in colony.agent]
    iniplot = ''
    ## Comment line below for "visualize" visualizer 
    if (visualizer==2): #PyGame visualizer
        import visualize2
        visualize = visualize2.Visualizer(colony.colsEnv * 20, colony.rowsEnv * 20, 20)  # Directly use grid size here
        initplot = visualize.initVizualiser(steps, colony.rowsEnv, colony.colsEnv, agentCoords)
    elif (visualizer==1):
        import visualize #Tkinter visualizer
        initplot = visualize.initVizualiser(steps, colony.rowsEnv, colony.colsEnv, agentCoords)
    
    while step != steps:
        step += 1
        print(step)
        colony.colonyStep()
        agentCoords = [o.coordinates for o in colony.agent]
        if visualizer>0:
            popData = visualize.initPopulation(colony.rowsEnv, colony.colsEnv, agentCoords)
            visualize.updatePlot(step, initplot, popData, colony.envMatrix,
                             colonieDefinition['parameters']['animationDelay'],
                             colonieDefinition['parameters']['colorSettings']
                             )
    if visualizer>0:
        visualize.endOfVisualization(initplot, popData)

    print(colony.envMatrix) 
    #for a in colony.agent: #Print the last configuration of the agent / can be commented
    #    print("Agent:")
    #    print(a.contents)
    #    print(a.coordinates.get("i"), a.coordinates.get("j"))
    
    #print(colony.agent[0].contents)
    #print(colony.agent[0].coordinates)
    #print(colony.agent[1].contents)
    #print(colony.agent[1].coordinates)
    #print(colony.agent[2].contents)
    #print(colony.agent[2].coordinates)
main()