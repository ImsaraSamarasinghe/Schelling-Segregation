import numpy as np
import random
import matplotlib.pyplot as plt

class SchellingModel:
    def __init__(self, height, width, density, similarity_threshold, max_steps):
        self.height = height
        self.width = width
        self.density = density
        self.similarity_threshold = similarity_threshold
        self.max_steps = max_steps
        self.grid = np.zeros((height, width))  # 0 represents empty cell
        self.agent_positions = []

    def initialize_agents(self):
        num_agents = int(self.height * self.width * self.density)
        agent_indices = random.sample(range(self.height * self.width), num_agents)
        for idx in agent_indices:
            x = idx // self.width
            y = idx % self.width
            self.grid[x, y] = random.choice([1, -1])
            self.agent_positions.append((x, y))

    def calculate_similarity(self, x, y):
        agent_type = self.grid[x, y]
        similar_neighbors = 0
        total_neighbors = 0
        for i in range(max(0, x - 1), min(self.height, x + 2)):
            for j in range(max(0, y - 1), min(self.width, y + 2)):
                if (i, j) != (x, y) and self.grid[i, j] != 0:
                    total_neighbors += 1
                    if self.grid[i, j] == agent_type:
                        similar_neighbors += 1
        return similar_neighbors / total_neighbors if total_neighbors > 0 else 0

    def is_happy(self, x, y):
        return self.calculate_similarity(x, y) >= self.similarity_threshold

    def move_agent(self, x, y):
        empty_cells = [(i, j) for i in range(self.height) for j in range(self.width) if self.grid[i, j] == 0]
        if empty_cells:
            new_x, new_y = random.choice(empty_cells)
            self.grid[new_x, new_y] = self.grid[x, y]
            self.grid[x, y] = 0
            self.agent_positions.remove((x, y))
            self.agent_positions.append((new_x, new_y))

    def step(self):
        for _ in range(self.max_steps):
            moved = False
            random.shuffle(self.agent_positions)
            for x, y in self.agent_positions:
                if not self.is_happy(x, y):
                    self.move_agent(x, y)
                    moved = True
            if not moved:
                break

    def visualize(self):
        plt.imshow(self.grid, cmap='bwr', interpolation='nearest')
        plt.title("Schelling Segregation Model")
        plt.colorbar(ticks=[-1, 0, 1])
        plt.show()

# Example usage
height = 70
width = 70
density = 0.9
similarity_threshold = 0.58
max_steps = 200

model = SchellingModel(height, width, density, similarity_threshold, max_steps)
model.initialize_agents()
model.step()
model.visualize()

