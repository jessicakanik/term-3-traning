import random

from arcade_wrapper import *

class MainMenu:
    def draw(self):
        draw_rectangle(0,0,800,600,"Blue")
        draw_text("Arcade", 100,100)
        draw_text("Instruction:", 100, 200)
        draw_text("Press 1 to start the competition", 100, 250)
        draw_text("Press 2 to exit this competition", 100, 300)

    def on_key(self, key :str):
        if key == "1":
            start_next_game()
        elif key == "2":
            close()

class ButtonMasher:
    def __init__(self):
        self.player1_score = 0
        self.player2_score = 0
    def draw(self):
        draw_text(f"Player 1 score: {self.player1_score}",0,300)
        draw_text(f"Player 2 score: {self.player2_score}",300,300)
        draw_text("press [a](player 1) and [l](player 2) to increase score ",5,10)

    def on_key(self,key :str):
        if key == "a":
            self.player1_score +=1
        elif key == "l":
            self.player2_score += 1

    def run(self):
        if self.player1_score >= 20:
            player_1_won()
        elif self.player2_score>= 20:
            player_2_won()

        
class GameTransition:

    def draw(self):
        draw_text("Get ready for the next game",50,200,)


class SimonSays:
    def __init__(self):
        self.player_1_score = 0
        self.player_2_score = 0
        self.random_direction =  random.randint(0,3)

    def draw(self):
        draw_text("Press the arrow that simon says",100,400)
        if self.random_direction == 0:
            draw_image("/Users/jessk/Desktop/PythonProject/AC04_T03/AC04_CodeMyArcadeResources/images/simon_up.png",336,100)
        elif self.random_direction == 1:
            draw_image("/Users/jessk/Desktop/PythonProject/AC04_T03/AC04_CodeMyArcadeResources/images/simon_right.png", 336, 100)
        elif self.random_direction == 2:
            draw_image("/Users/jessk/Desktop/PythonProject/AC04_T03/AC04_CodeMyArcadeResources/images/simon_down.png", 336, 100)
        elif self.random_direction == 3:
            draw_image("/Users/jessk/Desktop/PythonProject/AC04_T03/AC04_CodeMyArcadeResources/images/simon_left.png",336,100)



setup_window()
load_menu(MainMenu)
load_game(ButtonMasher)
load_game(SimonSays)
load_transition(GameTransition)
start_arcade(max_lives=3)
