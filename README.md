# smart_dots
Key Changes:
Very dumb dots. I dont know why they does not go on a straight line even i removed the barrier. I will try again later. 





Reduced Population Size: Changed from 1000 to 500 in the main function to improve performance.
Optimized Movement Directions: Directly store the angles and use them to calculate the directions during movement, which avoids the overhead of creating vectors repeatedly.
Optimized Drawing: Reduced the complexity of the drawing loop.
Optimized Random Vector Generation: Used NumPy's vectorized operations for random direction generation

🌟SmartDots is a Python-based simulation demonstrating genetic Algorithm for Pathfinding
It evolves a population of pink hearts to find the most efficient path to a specified goal. The pink hearts are influenced by a series of random movement vectors, and their performance is evaluated based on their proximity to the goal and how quickly they reach it. Over successive generations, the population evolves, becoming better at navigating to the goal.

Features
Genetic Algorithm: Utilizes genetic algorithms to evolve pink hearts movements over generations.
Pygame Integration: Uses Pygame for visual representation and animation of the  pink hearts' movements.
Fitness Calculation:  pink hearts are evaluated based on their distance to the goal and the steps taken to reach it.
Natural Selection: The best-performing  pink hearts are selected to produce offspring for the next generation.
Mutation: Introduces variability in the offspring to explore new paths and improve overall performance.

Installation
Clone the repository: git clone 
cd smartdots

Create a virtual environment and activate it:
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install the required dependencies:

Simulation Details
Screen Size: Our dot playground is 800x800 pixels.
Goal: The goal is at the top center of the screen. Get there, little hearts !
Population Size: We start with 500 adorable little hearts.
Obstacle: There's a little rectangular obstacle to make the game more fun and challenging.

Future Enhancements
🎨 Custom Settings: Change parameters like population size, mutation rate, and obstacles.
🏞 More Obstacles: Add more obstacles to make the dot journey even more exciting!
🚀 Performance Boosts: Make everything run faster and smoother.
📊 Data Visualization: Add graphs and stats to see how our dots are improving over time.

Working on:
To add the feature where offspring change color from red to dark red to black to rainbow colors in each generation, you can modify the Dot class to include a generation attribute and update the show method to change colors based on the generation. Additionally, you will need to adjust the natural_selection method in the Population class to increment the generation count.

Acknowledgments
Big hugs to the Pygame community for their amazing library and support. 💖
