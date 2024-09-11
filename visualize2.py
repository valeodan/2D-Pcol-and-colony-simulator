import pygame
import sys
import numpy as np

class Visualizer:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    def __init__(self, width, height, grid_size):
        self.width = width
        self.height = height
        self.grid_size = grid_size
        self.rows = height // grid_size
        self.cols = width // grid_size
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Agent Movement Visualization")
        self.clock = pygame.time.Clock()
        self.animation_delay = 0.915
        self.running = False
        self.pop_data = None

    def initVizualiser(self, numSteps, rowsEnv, colsEnv, aCoords):
        # Example usage
        self.numSteps = numSteps
        self.rowsEnv = rowsEnv
        self.colsEnv = colsEnv
        self.aCoords = aCoords

        pygame.init()
        self.screen = pygame.display.set_mode((self.colsEnv * 20, self.rowsEnv * 20))  # Directly use grid size here

        # Example initialization
        self.pop_data = np.zeros((self.rowsEnv, self.colsEnv))

    def initPopulation(self, rows, cols, agentCoords):
        pop_data = np.zeros((rows, cols))
        for coordinates in agentCoords:
            coord_j = coordinates.get("j") - 1
            coord_i = coordinates.get("i") - 1
            if 0 <= coord_i < self.rows and 0 <= coord_j < self.cols:
                pop_data[coord_i][coord_j] = 1.0
        return pop_data

    def updatePlot(self, step, initplot, pop_data, envMatrix, animation_delay, colors):
        # Update the display with the latest data
        self.screen.fill(self.WHITE)
        for i in range(min(self.rows, len(pop_data))):
            for j in range(min(self.cols, len(pop_data[0]))):
                color = self.GREEN if pop_data[i][j] == 1.0 else self.WHITE
                pygame.draw.rect(self.screen, color, (j * self.grid_size, i * self.grid_size, self.grid_size, self.grid_size))
        pygame.display.flip()
        pygame.time.delay(int(animation_delay * 1000))  # Convert seconds to milliseconds
        # Pygame events handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def endOfVisualization(self, initplot, pop_data):
        pygame.quit()
        sys.exit()

# Allow direct execution of the script
if __name__ == "__main__":
    # Example usage
    numSteps = 100
    rowsEnv = 30
    colsEnv = 20
    aCoords = [{"i": 5, "j": 5}]
    
    visualizer = Visualizer(colsEnv * 20, rowsEnv * 20, 20)  # Directly use grid size here
    visualizer.initVizualiser(numSteps, rowsEnv, colsEnv, aCoords)

    # Main control loop providing data to visualization
    for step in range(numSteps):
        # Update pop_data with new data for each step
        # Example: pop_data = get_new_data()
        pop_data = visualizer.initPopulation(rowsEnv, colsEnv, aCoords)
        visualizer.updatePlot(step, None, pop_data, None, 0.915, {})
        
    visualizer.endOfVisualization(None, pop_data)