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
        draw_rectangle(0, 0, 800, 600, "Green")
        draw_text("Get ready for the next game",50,200,)


class SimonSays:
    def __init__(self):
        self.player_1_score = 0
        self.player_2_score = 0
        self.random_direction =  random.randint(0,3)

    def on_key(self, key:str):
        if key in ["w","a","s","d"]:
            #print("Player 1")
            if ["w","d","s","a"][self.random_direction] == key:
                self.player_1_score += 1
                self.random_direction = random.randint(0, 3)
        elif key in ["i", "j", "k", "l"]:
            if ["i","l","k","j"][self.random_direction] == key:
                self.player_2_score += 1
                self.random_direction = random.randint(0, 3)
            #print("Player 2")



    def draw(self):
        draw_text("Press the arrow that simon says",100,400)
        draw_text("Player1 [W,A,S,D] ", 0, 300)
        draw_text("Player2 [I,J,K,L] ", 300, 300)
        if self.random_direction == 0:
            draw_image("/Users/jessk/Desktop/PythonProject/PythonProject/AC04_CodeMyArcadeResources/images/simon_up.png",336,100)
        elif self.random_direction == 1:
            draw_image("/Users/jessk/Desktop/PythonProject/PythonProject/AC04_CodeMyArcadeResources/images/simon_right.png", 336, 100)
        elif self.random_direction == 2:
            draw_image("/Users/jessk/Desktop/PythonProject/PythonProject/AC04_CodeMyArcadeResources/images/simon_down.png", 336, 100)
        elif self.random_direction == 3:
            draw_image("/Users/jessk/Desktop/PythonProject/PythonProject/AC04_CodeMyArcadeResources/images/simon_left.png",336,100)

    def run(self):
        if self.player_1_score >= 5:
            player_1_won()
        elif self.player_2_score>= 5:
            player_2_won()

class ResultScreen:
    def draw_player_1_won(self):
        draw_text("Player 1 Wins !", 100,250)
    def draw_player_2_won(self):
        draw_text("Player 2 Wins !", 100,250)


class SpeedCollector:
    
    
    def __init__(self):
        self.player_1_score = 0
        self.player_2_score = 0
        self.player_1_sprite = create_sprite_image("/Users/jessk/Desktop/PythonProject/PythonProject/AC04_CodeMyArcadeResources/images/car_red.png",
                                                   200,200,speed=300,up_key="w",down_key="s",left_key="a",right_key="d")
        self.player_2_sprite =create_sprite_image("/Users/jessk/Desktop/PythonProject/PythonProject/AC04_CodeMyArcadeResources/images/car_blue.png",300,200,
                                                  speed=300,up_key="i",down_key="k",left_key="j",right_key="l")
        self.collectable_sprite =create_sprite_image("/Users/jessk/Desktop/PythonProject/PythonProject/AC04_CodeMyArcadeResources/images/car_collectable.png",400,300)
    def draw(self):
        draw_image("/Users/jessk/Desktop/PythonProject/PythonProject/AC04_CodeMyArcadeResources/images/car_background.png",0,0)
        draw_sprite(self.player_1_sprite)
        draw_sprite(self.player_2_sprite)
        draw_sprite(self.collectable_sprite)

    def run(self):
        if self.player_1_sprite.overlaps(self.collectable_sprite):
            self.player_1_score += 1
            self.collectable_sprite.set_x(random.randint(50,750))
            self.collectable_sprite.set_y(random.randint(50,750))
        elif self.player_2_sprite.overlaps(self.collectable_sprite):
            self.player_2_score += 1
            self.collectable_sprite.set_x(random.randint(50, 750))
            self.collectable_sprite.set_y(random.randint(50, 750))


class Sumo :
    def __init__(self):
        self.sprite1 = create_sprite_image("/Users/jessk/Desktop/PythonProject/PythonProject/AC04_CodeMyArcadeResources/images/sumo_face.png", 320,300,
                                           speed=100,up_key="w",down_key="s",left_key="a",right_key="d")
        self.sprite2 = create_sprite_image("/Users/jessk/Desktop/PythonProject/PythonProject/AC04_CodeMyArcadeResources/images/sumo_face.png", 320,300,
                                           speed=100,up_key="i",down_key="k",left_key="j",right_key="l")

    def draw(self):
        draw_image("/Users/jessk/Desktop/PythonProject/PythonProject/AC04_CodeMyArcadeResources/images/sumo_background.png",0,0)
        draw_sprite(self.sprite1)
        draw_sprite(self.sprite2)

    def on_key(self, key:str):
        if key == "f":
            self.sprite1.dash()
        elif key == "h":
            self.sprite2.dah()

    def run(self):
        if self.sprite1.overlaps(self.sprite2):
            if self.sprite1.get_speed() > self.sprite2.get_speed():
                self.sprite1.push(self.sprite2)
            elif self.sprite1.get_speed() < self.sprite2.get_speed():
                self.sprite2.push(self.sprite1)

        if self.sprite1.get_distance_to(400,300) >= 250:
            player_2_won()
        elif self.sprite2.get_distance_to(400,300) >= 250:
            player_1_won()



setup_window()
load_menu(MainMenu)
# load_game(ButtonMasher)
# load_game(SimonSays)
#load_game(SpeedCollector)
load_game(Sumo)
load_transition(GameTransition)
load_results(ResultScreen)
start_arcade(max_lives=3)
