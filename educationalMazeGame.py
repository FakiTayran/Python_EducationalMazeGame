import sys
import copy
import os
import subprocess
import platform
import random

class MazeGame:
    def __init__(self):
        self.mazelevel = 1

    def show_maze(self, maze):
        for row in maze:
            print(''.join(row))

    def clear_screen(self):
        if platform.system() == "Windows":
            if platform.release() in {"10", "11"}:
                subprocess.run("", shell=True)
                print("\033c", end="")
            else:
                subprocess.run(["cls"])
        else:
            print("\033c", end="")

    def ask_continue(self):
        response = input("Do you want to continue to the next step? (y/n - yes/no): ").lower()
        return response == "y" or response == "yes"

    def play_game(self, maze, choices, correct_choice, lives):
        current_position = None
        exit_position = None
        lives = lives

        # Find the starting and exit positions
        for i in range(len(maze)):
            for j in range(len(maze[0])):
                if maze[i][j] == '1':
                    if current_position is None:
                        current_position = (i, j)
                    else:
                        exit_position = (i, j)
                        break

        # Show the maze before starting the game
        self.show_maze(mazes[self.mazelevel - 1]["maze"])


        questions = [  # Soruları ve cevaplarını içeren bir liste
            ("What is the capital of France?", "Paris"),
            ("What is the largest planet in our solar system?", "Jupiter"),
            ("Who is the founder of Turkey ?", "Ataturk")
        ]

        while lives > 0:

            print("Maze Level ", self.mazelevel)
            print(f"You have {lives} lives left.")
            print("You are \033[91mX\033[0m in the game. Choose one of the following options to find the correct path. How can you leave the maze for following numbers of 1")
            for choice in choices:
                print(f"{choice}: {choices[choice]}")

            for i in range(len(maze)):
                for j in range(len(maze[0])):
                    if maze[i][j] == '\033[91mX\033[0m':
                        maze[i][j] = '1'
                        break

            choice = input("Your choice: ").lower()
            while choice != correct_choice:
                print("Wrong choice! Try again.")
                lives -= 1
                print(lives," life left")

                if lives == 0:
                    print("You lost all your lives!")
                    print("You can earn lives to answer the following questions")
                    # General Culture Questions
                    for _ in range(3):
                        question, answer = random.choice(questions)
                        user_answer = input(question + " ").strip().capitalize()
                        if user_answer == answer:
                            print("Correct! You earned 1 extra life.")
                            lives += 1
                            x,y = current_position
                            maze[x][y-1] = '\033[91mX\033[0m'
                            self.continue_game(lives)
                        else:
                            print("Incorrect! No extra lives earned.")
                    return
                else:
                    choice = input("Your choice: ").lower()

            self.clear_screen()

            # Mark the starting position
            x, y = current_position
            maze[x][y] = '\033[91mX\033[0m'

            while (x, y) != exit_position:
                self.show_maze(maze)
                input("To move press enter")
                self.clear_screen()

                if maze[x + 1][y] == '1':
                    maze[x][y] = '1'
                    x, y = x + 1, y
                    maze[x][y] = '\033[91mX\033[0m'
                elif maze[x][y + 1] == '1':
                    maze[x][y] = '1'
                    x, y = x, y + 1
                    maze[x][y] = '\033[91mX\033[0m'
                elif maze[x][y - 1] == '1':
                    maze[x][y] = '1'
                    x, y = x, y - 1
                    maze[x][y] = '\033[91mX\033[0m'

            maze[x][y] = '\033[91mX\033[0m'

            self.show_maze(maze)

            print("Congratulations, you found the correct path!")
            if self.ask_continue() and self.mazelevel < len(mazes):
                self.clear_screen()
                print("Moving to the next maze...\n")
                self.mazelevel += 1
                return
            else:
                print("New levels are coming...For now thanks for playing!")
                quit()

    def startGame(self,lives):
        for i, maze_data in enumerate(mazes, start=self.mazelevel):
            self.play_game(maze_data["maze"], maze_data["choices"], maze_data["correct_choice"], lives)
    def continue_game(self, lives):
        if self.mazelevel <= len(mazes):
            maze_data = mazes[self.mazelevel - 1]
            self.play_game(maze_data["maze"], maze_data["choices"], maze_data["correct_choice"], lives)


# Define mazes and choices
mazes = [
    {
        "maze": [
            ['0', '0', '0', '0', '\033[91mX\033[0m', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0']
        ],
        "choices": {
            "a": "Down",
            "b": "Left",
            "c": "Right"
        },
        "correct_choice": "a"
    },
    {
        "maze": [
            ['0', '0', '0', '0', '\033[91mX\033[0m', '1', '1', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '1', '1', '1', '1', '1', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '1'],
            ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1']
        ],
        "choices": {
            "a": "Move right until block and down",
            "b": "Move down until block then turn right",
            "c": "Move right and and continue to down while block"
        },
        "correct_choice": "c"
    }
]

# Create an instance of the MazeGame class
game = MazeGame()
game.startGame(3)
