import math
import random as _random
import pygame as _pg

class _Window:
    def __init__(self, width: int = 800, height: int = 600, title: str = "Arcade Cabinet", clear_colour: tuple[int, int, int] = (255, 255, 255)):
        _pg.init()
        self.window_width = width
        self.window_height = height
        self.title = title
        self.pg_window = _pg.display.set_mode((width, height))
        self._drawn_window = _pg.Surface((width, height), _pg.SRCALPHA)
        self._clear_colour = clear_colour
        self._loaded_images = {}
        _pg.display.set_caption(title)

    def load_image(self, image_path: str):
        if image_path in self._loaded_images:
            return self._loaded_images[image_path]
        image = _pg.image.load(image_path).convert_alpha()
        self._loaded_images[image_path] = image
        return image

    def clear(self):
        self._drawn_window.fill(self._clear_colour)

    def draw(self, other_surface: _pg.Surface, position: tuple[int, int]):
        self._drawn_window.blit(other_surface, position)

    def show_frame(self):
        scaled_frame = _pg.transform.scale(self._drawn_window, (self.window_width, self.window_height))
        self.pg_window.blit(scaled_frame, (0, 0))
        _pg.display.flip()


_current_window = None
_current_program = None
_recent_dt = 0

TRANSITION_NONE = 0
TRANSITION_SWIPE_RIGHT = 1
TRANSITION_SWIPE_LEFT = 1
TRANSITION_SWIPE_UP = 2
TRANSITION_SWIPE_DOWN = 3


class _Program:
    def __init__(self, fps: int = 60):
        self._running = True
        self._fps = fps
        self._current_screen = None
        self._game_screens = []
        self._menu_screens = []
        self._transition_screens = []
        self._transition_effects = []
        self._current_effect = 0
        self._current_effect_blanker = None
        self._results_screens = []
        self._game_state = 0
        self._recent_games = []
        self._recent_transitions = []
        self._recent_results_screens = []
        self._total_sprites = []
        self._player_1_lives = 0
        self._player_2_lives = 0
        self.max_lives = 3
        self._transition_timer = 2
        self._results_timer = 4
        self._playing_music = None
        self._previous_winner = 0
        self._num_games = 0

    def play_music(self, music_object: _pg.mixer.Sound):
        if isinstance(self._playing_music, _pg.mixer.Sound):
            self._playing_music.stop()
        self._playing_music = music_object
        self._playing_music.play(loops=-1)

    def add_menu_screen(self, menu_class):
        self._menu_screens.append(menu_class)

    def add_game_screen(self, game_class):
        self._game_screens.append(game_class)

    def add_transition_screen(self, transition_class, transition_type: int):
        self._transition_screens.append(transition_class)
        self._transition_effects.append(transition_type)

    def add_results_screen(self, results_class):
        self._results_screens.append(results_class)

    def reset_game(self):
        self._game_state = 0
        self._num_games = 0
        self._player_1_lives = self.max_lives
        self._player_2_lives = self.max_lives
        self._current_screen = self._menu_screens[0]()

    def get_previous_winner(self):
        return self._previous_winner

    def stop(self):
        self._running = False

    def load_next_game(self):
        self._current_effect = 0
        self._current_effect_blanker = None
        if len(self._game_screens) == 0:
            print("There are no games in the arcade system to play")
            return
        if len(self._recent_games) == len(self._game_screens):
            self._recent_games.clear()
        while True:
            random_game_index = _random.randint(0, len(self._game_screens) - 1)
            if self._game_screens[random_game_index] not in self._recent_games:
                self._recent_games.append(self._game_screens[random_game_index])
                self._total_sprites.clear()
                self._current_screen = self._game_screens[random_game_index]()
                if self._game_state == 0:
                    self._player_1_lives = self.max_lives
                    self._player_2_lives = self.max_lives
                self._game_state = 1
                self._num_games += 1
                break

    def get_number_games(self):
        return self._num_games

    def _finish_game(self):
        if self._player_1_lives == 0 or self._player_2_lives == 0:
            self._game_state = 3
            if len(self._results_screens) == 0:
                self._game_state = 0
                self._player_1_lives = self.max_lives
                self._player_2_lives = self.max_lives
                self._current_screen = self._menu_screens[0]()
                return
            if len(self._recent_results_screens) == len(self._results_screens):
                self._recent_results_screens.clear()
            while True:
                random_results_index = _random.randint(0, len(self._results_screens) - 1)
                if self._results_screens[random_results_index] not in self._recent_results_screens:
                    self._recent_results_screens.append(self._results_screens[random_results_index])
                    self._current_screen = self._results_screens[random_results_index]()
                    self._results_timer = 4
                    return
        if len(self._transition_screens) == 0:
            self.load_next_game()
            return
        if len(self._recent_transitions) == len(self._transition_screens):
            self._recent_transitions.clear()
        while True:
            random_transition_index = _random.randint(0, len(self._transition_screens) - 1)
            if self._transition_screens[random_transition_index] not in self._recent_transitions:
                self._recent_transitions.append(self._transition_screens[random_transition_index])
                self._current_screen = self._transition_screens[random_transition_index]()
                self._current_effect = self._transition_effects[random_transition_index]
                if self._current_effect > 0 and isinstance(_current_window, _Window):
                    self._current_effect_blanker = create_sprite_rectangle(0, 0, _current_window.window_width, _current_window.window_height, (0, 0, 0), 800, face_movement_direction=False)
                    self._current_effect_blanker.surface.fill((0, 0, 0, 255))
                    if self._current_effect == TRANSITION_SWIPE_UP:
                        self._current_effect_blanker.direction.y = -1
                    elif self._current_effect == TRANSITION_SWIPE_DOWN:
                        self._current_effect_blanker.direction.y = 1
                    elif self._current_effect == TRANSITION_SWIPE_RIGHT:
                        self._current_effect_blanker.direction.x = 1
                    elif self._current_effect == TRANSITION_SWIPE_LEFT:
                        self._current_effect_blanker.direction.x -= 1
                break
        self._transition_timer = 2
        self._game_state = 2

    def register_sprite(self, sprite: "Sprite"):
        self._total_sprites.append({"instance": sprite, "up": sprite.up_key, "right": sprite.right_key, "down": sprite.down_key, "left": sprite.left_key})

    def player_1_won(self):
        self._previous_winner = 1
        self._player_2_lives -= 1
        self._finish_game()

    def player_2_won(self):
        self._previous_winner = 2
        self._player_1_lives -= 1
        self._finish_game()

    def get_lives_left(self):
        return self._player_1_lives, self._player_2_lives

    def set_volume(self, volume: float):
        if isinstance(self._playing_music, _pg.mixer.Sound):
            self._playing_music.set_volume(volume)

    def start(self):
        global _recent_dt
        if len(self._menu_screens) > 0:
            self._current_screen = self._menu_screens[0]()
        clock = _pg.time.Clock()
        self._player_1_lives = self.max_lives
        self._player_2_lives = self.max_lives
        while self._running:
            for event in _pg.event.get():
                if event.type == _pg.QUIT:
                    self._running = False
                elif event.type == _pg.KEYDOWN:
                    key = _pg.key.name(event.key)
                    for sprite_dict in self._total_sprites:
                        if sprite_dict["up"] == key:
                            sprite_dict["instance"].direction.y -= 1
                        elif sprite_dict["right"] == key:
                            sprite_dict["instance"].direction.x += 1
                        elif sprite_dict["down"] == key:
                            sprite_dict["instance"].direction.y += 1
                        elif sprite_dict["left"] == key:
                            sprite_dict["instance"].direction.x -= 1
                    try:
                        self._current_screen.on_key(key)
                    except AttributeError:
                        pass
                elif event.type == _pg.KEYUP:
                    key = _pg.key.name(event.key)
                    for sprite_dict in self._total_sprites:
                        if sprite_dict["up"] == key:
                            sprite_dict["instance"].direction.y += 1
                        elif sprite_dict["right"] == key:
                            sprite_dict["instance"].direction.x -= 1
                        elif sprite_dict["down"] == key:
                            sprite_dict["instance"].direction.y -= 1
                        elif sprite_dict["left"] == key:
                            sprite_dict["instance"].direction.x += 1
            _recent_dt = clock.tick(self._fps) / 1000.0
            if self._game_state == 2:
                self._transition_timer -= _recent_dt
                if isinstance(self._current_effect_blanker, Sprite):
                    self._current_effect_blanker.update()
                if self._transition_timer <= 0:
                    self.load_next_game()
            if self._game_state == 3:
                self._results_timer -= _recent_dt
                if self._results_timer <= 0:
                    self.reset_game()
            if self._current_screen is not None:
                for sprite_dict in self._total_sprites:
                    sprite_dict["instance"].update()
                try:
                    self._current_screen.run()
                except AttributeError:
                    pass
                if isinstance(_current_window, _Window):
                    _current_window.clear()
                    try:
                        if self._game_state == 3 and self._player_1_lives == 0:
                            self._current_screen.draw_player_2_won()
                        elif self._game_state == 3 and self._player_2_lives == 0:
                            self._current_screen.draw_player_1_won()
                        else:
                            self._current_screen.draw()
                        if isinstance(self._current_effect_blanker, Sprite):
                            _current_window.draw(self._current_effect_blanker.surface, (int(self._current_effect_blanker.position.x), int(self._current_effect_blanker.position.y)))
                            _pg.image.save(self._current_effect_blanker.surface, "test.png")
                    except AttributeError:
                        pass
                    _current_window.show_frame()


class Sprite:
    def __init__(self, position: tuple[int, int], size: tuple[int, int], speed: float = 0.0, up_key: str = "", down_key: str = "", right_key: str = "", left_key: str = "", face_movement_direction: bool = True):
        self._original_surface = _pg.Surface(size, _pg.SRCALPHA)
        self.surface = _pg.Surface(size, _pg.SRCALPHA)
        self.position = _pg.Vector2(*position)
        self._previous_position = _pg.Vector2(*position)
        self.direction = _pg.Vector2()
        self._dash_multiplier = 1
        self._dash_timer = 0
        self._dash_cooldown = 0
        self._push_duration = 0
        self._push_direction = _pg.Vector2()
        self.speed = speed
        self.up_key = up_key
        self.down_key = down_key
        self.right_key = right_key
        self.left_key = left_key
        self.face_movement_direction = face_movement_direction

    def change_rectangle(self, new_colour: tuple[int, int, int]):
        self.surface.fill(new_colour)

    def change_image(self, new_image_path: str):
        new_surface = _pg.image.load(new_image_path).convert_alpha()
        new_surface = _pg.transform.scale(new_surface, (self.surface.get_width(), self.surface.get_height()))
        self.surface = new_surface

    def change_circle(self, new_colour: tuple[int, int, int]):
        new_surface = _pg.Surface((self.surface.get_width(), self.surface.get_height()), _pg.SRCALPHA)
        _pg.draw.circle(new_surface, new_colour, (self.surface.get_width() // 2, self.surface.get_height() // 2), (self.surface.get_width() // 2))
        self.surface = new_surface

    def update_appearance(self, new_surface: _pg.Surface):
        self._original_surface = new_surface

    def update(self):
        if self._dash_timer > 0:
            self._dash_timer -= _recent_dt
            if self._dash_timer <= 0:
                self._dash_multiplier = 1
        if self._dash_cooldown > 0:
            self._dash_cooldown -= _recent_dt
        if self._push_duration > 0:
            self._push_duration -= _recent_dt
            new_position = self.position + (self._push_direction * _recent_dt)
            self._previous_position = self.position
            self.position = new_position
        elif self.direction.x != 0 or self.direction.y != 0:
            normalised_direction = self.direction.normalize()
            velocity = normalised_direction * self.speed * self._dash_multiplier
            new_position = self.position + (velocity * _recent_dt)
            self._previous_position = self.position
            self.position = new_position
        if self.face_movement_direction:
            angle = math.degrees(math.atan2(-(self.position.y - self._previous_position.y), self.position.x - self._previous_position.x))
            self.surface = _pg.transform.rotate(self._original_surface, angle)

    def dash(self, multiplier: float = 3, duration: float = 0.2, cooldown: float = 1.0):
        if self._dash_cooldown > 0:
            return
        self._dash_multiplier = multiplier
        self._dash_timer = duration
        self._dash_cooldown = duration + cooldown

    def overlaps(self, other_sprite: "Sprite") -> bool:
        a_rect = self.surface.get_rect().move(self.position.x, self.position.y).move(-(self.surface.get_width()//2), -(self.surface.get_height()//2))
        b_rect = other_sprite.surface.get_rect().move(other_sprite.position.x, other_sprite.position.y).move(-(other_sprite.surface.get_width()//2), -(other_sprite.surface.get_height()//2))
        return a_rect.colliderect(b_rect)

    def set_x(self, x: int):
        self.position.x = x
        self._previous_position.x = x

    def set_y(self, y: int):
        self.position.y = y
        self._previous_position.y = y

    def reflect_x(self):
        self.direction.x *= -1

    def reflect_y(self):
        self.direction.y *= -1

    def get_distance_to(self, x: int, y: int) -> float:
        return _pg.Vector2(self.position.x, self.position.y).distance_to(_pg.Vector2(x, y))

    def get_speed(self):
        return self.speed * self._dash_multiplier

    def push(self, other_sprite: "Sprite", push_force: float = 200, push_duration: float = 0.2):
        direction = (other_sprite.position - self.position).normalize()
        self.position += -direction
        other_sprite.position += direction
        if self._push_duration <= 0 and other_sprite._push_duration <= 0:
            push_speed = direction * push_force
            other_sprite._push_direction = push_speed
            other_sprite._push_duration = push_duration
            self._push_direction = _pg.Vector2()
            self._push_duration = push_duration / 2



def setup_window(width: int = 800, height: int = 600, title: str = "Arcade Cabinet"):
    global _current_window, _current_program
    _current_window = _Window(width, height, title)
    _current_program = _Program()

def load_menu(menu_class):
    if isinstance(_current_program, _Program):
        _current_program.add_menu_screen(menu_class)

def load_game(game_class):
    if isinstance(_current_program, _Program):
        _current_program.add_game_screen(game_class)

def load_transition(transition_class, transition_type: int = TRANSITION_NONE):
    if isinstance(_current_program, _Program):
        _current_program.add_transition_screen(transition_class, transition_type)

def load_results(results_class):
    if isinstance(_current_program, _Program):
        _current_program.add_results_screen(results_class)

def start_arcade(max_lives: int = 3):
    if isinstance(_current_program, _Program):
        _current_program.max_lives = max_lives
        _current_program.start()

def draw_rectangle(x: int, y: int, width: int, height: int, colour: tuple[int, int, int, int], edge_radius: int = 0, outline_only: bool = False):
    if isinstance(_current_window, _Window):
        rect_surface = _pg.Surface((width, height), _pg.SRCALPHA)
        _pg.draw.rect(rect_surface, colour, (0, 0, width, height), border_radius=edge_radius, width=5 if outline_only else 0)
        _current_window.draw(rect_surface, (x, y))

def draw_oval(x: int, y: int, width: int, height: int, colour: tuple[int, int, int, int], outline_only: bool = False):
    if isinstance(_current_window, _Window):
        oval_surface = _pg.Surface((width, height), _pg.SRCALPHA)
        _pg.draw.ellipse(oval_surface, colour, (0, 0, width, height), width=5 if outline_only else 0)
        _current_window.draw(oval_surface, (x, y))

def draw_circle(x: int, y: int, radius: int, colour: tuple[int, int, int, int]):
    if isinstance(_current_window, _Window):
        circle_surface = _pg.Surface((radius * 2, radius * 2), _pg.SRCALPHA)
        _pg.draw.circle(circle_surface, colour, (radius, radius), radius)
        _current_window.draw(circle_surface, (x, y))

def draw_text(text: str, x: int, y: int, font_name: str = "Calibri", font_size: int = 32, font_colour: tuple[int, int, int, int] = (255, 255, 255, 255), background_colour: tuple[int, int, int, int] = (0, 0, 0, 0), bold: bool = False, italic: bool = False, antialias: bool = True):
    if isinstance(_current_window, _Window):
        font = _pg.font.SysFont(font_name, font_size, bold=bold, italic=italic)
        text_surface = font.render(text, antialias, font_colour, background_colour)
        _current_window.draw(text_surface, (x, y))

def start_next_game():
    if isinstance(_current_program, _Program):
        _current_program.load_next_game()

def player_1_won():
    if isinstance(_current_program, _Program):
        _current_program.player_1_won()

def player_2_won():
    if isinstance(_current_program, _Program):
        _current_program.player_2_won()

def create_sprite_rectangle(x: int, y: int, width: int, height: int, colour: tuple[int, int, int], speed: float = 0.0, up_key: str = "", down_key: str = "", right_key: str = "", left_key: str = "", should_turn: bool = False, starting_direction: tuple[float, float] = (0.0, 0.0)):
    new_sprite = Sprite((x, y), (width, height), speed=speed, up_key=up_key, down_key=down_key, right_key=right_key, left_key=left_key, face_movement_direction=should_turn)
    sprite_surface = _pg.Surface((width, height), _pg.SRCALPHA)
    sprite_surface.fill(colour)
    new_sprite.update_appearance(sprite_surface)
    new_sprite.direction = _pg.Vector2(*starting_direction)
    if isinstance(_current_program, _Program):
        _current_program.register_sprite(new_sprite)
    return new_sprite

def create_sprite_image(image_path: str, x: int, y: int, speed: float = 0.0, up_key: str = "", down_key: str = "", right_key: str = "", left_key: str = "", should_turn: bool = False, starting_direction: tuple[float, float] = (0.0, 0.0)):
    if isinstance(_current_window, _Window):
        image_surface = _current_window.load_image(image_path)
        new_sprite = Sprite((x, y), image_surface.get_size(), speed, up_key, down_key, right_key, left_key, face_movement_direction=should_turn)
        new_sprite.update_appearance(image_surface)
        new_sprite.direction = _pg.Vector2(*starting_direction)
        if isinstance(_current_program, _Program):
            _current_program.register_sprite(new_sprite)
        return new_sprite
    return None


def create_sprite_circle(x: int, y: int, radius: int, colour: tuple[int, int, int], speed: float = 0.0, up_key: str = "", down_key: str = "", right_key: str = "", left_key: str = "", should_turn: bool = False, starting_direction: tuple[float, float] = (0.0, 0.0)):
    new_sprite = Sprite((x, y), (radius * 2, radius * 2), speed=speed, up_key=up_key, down_key=down_key, right_key=right_key, left_key=left_key, face_movement_direction=should_turn)
    sprite_surface = _pg.Surface((radius * 2, radius * 2), _pg.SRCALPHA)
    _pg.draw.circle(sprite_surface, colour, (radius, radius), radius)
    new_sprite.update_appearance(sprite_surface)
    new_sprite.direction = _pg.Vector2(*starting_direction)
    if isinstance(_current_program, _Program):
        _current_program.register_sprite(new_sprite)
    return new_sprite


def draw_image(image_path: str, x: int, y: int):
    if isinstance(_current_window, _Window):
        image_surface = _current_window.load_image(image_path)
        _current_window.draw(image_surface, (x, y))


def draw_sprite(sprite):
    if isinstance(_current_window, _Window):
        _current_window.draw(sprite.surface, (sprite.position.x - (sprite.surface.get_width() // 2), sprite.position.y - (sprite.surface.get_height() // 2)))


def close():
    if isinstance(_current_program, _Program):
        _current_program.stop()


def get_time():
    return _recent_dt


def play_music(music_file_path: str, volume: float = 0.5):
    if isinstance(_current_program, _Program):
        music_object = _pg.mixer.Sound(music_file_path)
        music_object.set_volume(volume)
        _current_program.play_music(music_object)


def play_sound_effect(sound_file_path: str, volume: float = 0.5):
    if isinstance(_current_program, _Program):
        sound_object = _pg.mixer.Sound(sound_file_path)
        sound_object.set_volume(volume)
        sound_object.play()


def get_previous_winner():
    if isinstance(_current_program, _Program):
        return _current_program.get_previous_winner()
    return 0


def get_lives_left():
    if isinstance(_current_program, _Program):
        return _current_program.get_lives_left()
    return 0, 0


def change_music_volume(volume: float):
    if isinstance(_current_program, _Program):
        _current_program.set_volume(volume)


def get_number_games():
    if isinstance(_current_program, _Program):
        return _current_program.get_number_games()
    return 0


def get_window_width():
    if isinstance(_current_window, _Window):
        return _current_window.window_width
    return -1


def get_window_height():
    if isinstance(_current_window, _Window):
        return _current_window.window_height
    return -1