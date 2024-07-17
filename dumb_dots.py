import numpy as np
import pygame
#Importing necessary libraries: numpy for efficient numerical operations and pygame for graphical
# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
GOAL = np.array([400, 10])
POPULATION_SIZE = 100
LIFESPAN = 400

# Initialize Pygame
pygame.init()
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

def draw_heart(surface, color, center, size):
    points = []
    for t in np.linspace(0, 2 * np.pi, 100):
        x = size * 16 * np.sin(t)**3
        y = -size * (13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t))
        points.append((center[0] + x, center[1] + y))
    pygame.draw.polygon(surface, color, points)
#mathematical parametric equation in polar coordinates, also need to translate this equation into Cartesian coordinates and scale it to fit our needs.
#The size parameter is used to scale the heart, and center shifts the heart to the desired location on the surface.
#generates 100 equally spaced values of t between 0 and 2π
#Note the subtraction in the y-coordinate calculation. This is because the y-axis in many graphical coordinate systems (including Pygame) points downwards.
#Each cosine term contributes to the vertical component of the heart, with the coefficients (13, 

class Movement:
    def __init__(self, size: int):
        self.directions = [self.random_vector() for _ in range(size)]
        self.step = 0
#A list comprehension [self.random_vector() for _ in range(size)] generates size random vectors using the random_vector method.
#This list is converted to a NumPy array and assigned to self.directions.


    def random_vector(self):
        angle = np.random.uniform(0, 2 * np.pi)
        return np.array([np.cos(angle), np.sin(angle)])

    def clone(self):
        clone = Movement(len(self.directions))
        clone.directions = self.directions.copy()
        return clone

    def mutate(self, mutation_rate: float = 0.01):
        for i in range(len(self.directions)):
            if np.random.rand() < mutation_rate:
                self.directions[i] = self.random_vector()

class Dot:
    def __init__(self, screen_width: int, screen_height: int):
        self.pos = np.array([screen_width / 2, screen_height - 10], dtype=float)
        self.vel = np.array([0, 0], dtype=float)
        self.acc = np.array([0, 0], dtype=float)
        self.movement = Movement(LIFESPAN)
        self.dead = False
        self.reached_goal = False
        self.is_best = False
        self.fitness = 0

    def show(self, win, color):
        size = 0.8 if self.is_best else 0.4
        draw_heart(win, color, self.pos.astype(int), size)

    def apply_force(self, force):
        self.acc += force

    def move(self):
        if self.movement.step < LIFESPAN:
            self.apply_force(self.movement.directions[self.movement.step])
            self.movement.step += 1
        self.vel += self.acc
        self.pos += self.vel
        self.acc *= 0
        self.check_collision()

    def check_collision(self):
        if self.pos[0] < 0 or self.pos[0] > SCREEN_WIDTH or self.pos[1] < 0 or self.pos[1] > SCREEN_HEIGHT:
            self.dead = True
        if np.linalg.norm(self.pos - GOAL) < 5:
            self.reached_goal = True

    def update(self):
        if not self.dead and not self.reached_goal:
            self.move()

    def calculate_fitness(self):
        if self.reached_goal:
            self.fitness = 1.0 / 16.0 + 10000.0 / (self.movement.step ** 2)
        else:
            distance_to_goal = np.linalg.norm(self.pos - GOAL)
            self.fitness = 1.0 / (distance_to_goal ** 2)

    def gimme_baby(self):
        baby = Dot(SCREEN_WIDTH, SCREEN_HEIGHT)
        baby.movement = self.movement.clone()
        return baby

class Population:
    def __init__(self, size: int):
        self.dots = [Dot(SCREEN_WIDTH, SCREEN_HEIGHT) for _ in range(size)]
        self.fitness_sum = 0
        self.gen = 0
        self.best_dot = None
        self.best_dot_index = 0
        self.min_step = LIFESPAN

    def update(self):
        for dot in self.dots:
            dot.update()

    def show(self, win):
        for dot in self.dots:
            color = self.get_color(dot)
            dot.show(win, color)

    def get_color(self, dot):
        if self.gen == 0:
            return (255, 105, 180)  # Pink
        elif self.gen == 1:
            return (255, 0, 0)  # Red
        elif self.gen == 2:
            return (139, 0, 0)  # Dark Red
        elif self.gen == 3:
            return (0, 0, 0)  # Black
        else:
            hue = (self.gen + dot.movement.step / LIFESPAN) % 1.0
            color = pygame.Color(0)
            color.hsva = (hue * 360, 100, 100, 100)
            return color

    def calculate_fitness(self):
        for dot in self.dots:
            dot.calculate_fitness()

    def all_dots_dead(self):
        return all(dot.dead or dot.reached_goal for dot in self.dots)

    def natural_selection(self):
        self.calculate_fitness_sum()
        new_dots = [self.select_parent().gimme_baby() for _ in range(len(self.dots))]
        self.dots = new_dots
        self.gen += 1

    def calculate_fitness_sum(self):
        self.fitness_sum = sum(dot.fitness for dot in self.dots)

    def select_parent(self):
        rand = np.random.uniform(0, self.fitness_sum)
        running_sum = 0
        for dot in self.dots:
            running_sum += dot.fitness
            if running_sum > rand:
                return dot
        return self.dots[0]

    def mutate_dem_babies(self):
        for dot in self.dots:
            dot.movement.mutate()

    def set_best_dot(self):
        max_fitness = 0
        max_index = 0
        for i, dot in enumerate(self.dots):
            if dot.fitness > max_fitness:
                max_fitness = dot.fitness
                max_index = i
        self.best_dot_index = max_index
        self.best_dot = self.dots[max_index]
        self.best_dot.is_best = True
        if self.best_dot.reached_goal:
            self.min_step = self.best_dot.movement.step
            print(f"Generation: {self.gen}, Min Step: {self.min_step}")

def main():
    pop = Population(POPULATION_SIZE)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        win.fill((255, 255, 255))
        pygame.draw.circle(win, (255, 0, 0), GOAL.astype(int), 10)

        if pop.all_dots_dead():
            pop.calculate_fitness()
            pop.set_best_dot()
            pop.natural_selection()
            pop.mutate_dem_babies()
        else:
            pop.update()
            pop.show(win)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
