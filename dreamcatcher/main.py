""" Dreamcatcher
"""
___title___        = "Dreamcatcher Puzzle"
___license___      = "MIT"
___dependencies___ = ["ugfx_helper", "sleep", "dialogs", "database", "buttons"]
___categories___   = ["Other"]
___bootstrapped___ = False
import ugfx, buttons, dialogs, sleep, app
from database import *
from tilda import Buttons

###
# Questioner
###
questions = {
    1: "Imagination",
    2: "Empathy",
    3: "Vision",
    4: "Storage",
    5: "Embodiment",
    6: "Induction",
    7: "Mutation",
    8: "Curiosity",
    9: "Deduction",
    10: "Recall"
}

hashed_answers = {
    1: 'nrflnsfynts',
    2: 'jrufymD',
    3: 'Anxnts',
    4: 'xytwflj',
    5: 'jrgtinrjsy',
    6: 'nsizhynts',
    7: 'rzyfynts',
    8: 'hzwntxnyD',
    9: 'ijizhynts',
    10: 'wjhfqq'
}


def prompt_and_check_answer(key):
    answer = prompt_answer_and_make_lowercase(key)
    if check_answer_ignoring_case(key, answer):
        return answer
    else:
        return None


def prompt_answer_and_make_lowercase(key):
    answer = dialogs.prompt_text("Enter answer for " + questions[key], init_text="")
    return answer.lower()


def check_answer_ignoring_case(key, answer):
    hashed_answer = hash_answer(answer)
    if hashed_answer == hashed_answers[key]:
        return True
    else:
        return False


printable_chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ ' \
                  '\t\n\r\x0b\x0c'

chars_double_list = list(printable_chars + printable_chars)


def hash_answer(answer):
    answer_as_list = list(answer.lower())
    caesar_encrypted = ''
    for character in answer_as_list:
        index = chars_double_list.index(character) + 5
        caesar_encrypted += chars_double_list[index]
    return caesar_encrypted


###
# Game State
###
DB_KEY_PROGRESS = "dreamcatcher::progress"
unlocked_answers = {}


def read_progress():
    global unlocked_answers

    with Database() as db:
        try:
            value = db.get(DB_KEY_PROGRESS)
            if value is None:
                unlocked_answers = {}
            else:
                unlocked_answers = value
        except ValueError:
            display_notice("Progress corrupted. Resetting.")
            db.set(DB_KEY_PROGRESS, {})


def update_progress(key, answer):
    if answer is None:
        display_notice("Sorry, that's not a correct answer :'(")
    elif unlocked_answers.get(key) == answer:
        display_notice("You've already unlocked that answer")
    else:
        old_answers = dict(unlocked_answers)
        unlocked_answers[key] = answer
        write_progress()
        display_notice("That's right, you clever clogs!")
        draw_progress_and_flicker_new_answer(key, old_answers)


def write_progress():
    with Database() as db:
        db.set(DB_KEY_PROGRESS, unlocked_answers)


###
# Display
###
EMPTY_CELL = 0x52c9
SELECTED_EMPTY_CELL = 0xbe54


class Polygon:
    def __init__(self, x, y, points, colour):
        self.x = x
        self.y = y
        self.points = points
        self.colour = colour


polygons = {
    1: Polygon(0, 0, [[0, 0], [74, 0], [100, 95], [60, 95], [44, 111], [0, 71]], ugfx.RED),
    2: Polygon(0, 0, [[74, 0], [100, 95], [151, 56], [177, 58], [233, 0]], ugfx.ORANGE),
    3: Polygon(0, 0, [[233, 0], [319, 0], [319, 72], [177, 58]], ugfx.RED),
    4: Polygon(0, 0, [[0, 71], [75, 141], [46, 239], [0, 240]], ugfx.YELLOW),
    5: Polygon(0, 0, [[44, 111], [60, 95], [100, 95], [124, 77], [190, 155], [124, 187]], ugfx.BLUE),
    6: Polygon(0, 0, [[124, 77], [151, 56], [217, 62], [251, 125], [189, 154]], ugfx.GREEN),
    7: Polygon(0, 0, [[217, 62], [319, 72], [319, 165], [283, 181]], ugfx.BLUE),
    8: Polygon(0, 0, [[75, 141], [124, 187], [190, 153], [189, 239], [46, 239]], ugfx.RED),
    9: Polygon(0, 0, [[189, 155], [251, 125], [284, 181], [248, 198], [276, 239], [189, 240]], ugfx.PURPLE),
    10: Polygon(0, 0, [[319, 165], [319, 239], [276, 239], [248, 198]], ugfx.YELLOW)
}


def draw_progress_and_display_current_answer(current_key, unlocked_answers):
    draw_progress(unlocked_answers)
    highlight_current_polygon(current_key, unlocked_answers)
    display_current_answer(current_key, unlocked_answers)


def draw_progress_and_flicker_new_answer(new_answer_key, old_answers):
    draw_progress(old_answers)
    flicker_new_answer(new_answer_key)


def draw_progress(unlocked_answers):
    for key, polygon in polygons.items():
        if unlocked_answers.get(key) is not None:
            draw_polygon(polygon, polygon.colour)
        else:
            draw_polygon(polygon, EMPTY_CELL)


def highlight_current_polygon(current_key, unlocked_answers):
    polygon = polygons[current_key]
    if unlocked_answers.get(current_key) is None:
        draw_polygon(polygon, SELECTED_EMPTY_CELL)
    else:
        draw_polygon(polygon, ugfx.WHITE)


def display_current_answer(current_key, unlocked_answers):
    text = questions[current_key] + ": " + unlocked_answers.get(current_key, "???")
    display_text(text)


def flicker_new_answer(new_answer):
    polygon = polygons[new_answer]
    sleep.sleep_ms(100)
    draw_polygon(polygon, polygon.colour)
    sleep.sleep_ms(100)
    draw_polygon(polygon, ugfx.BLACK)
    sleep.sleep_ms(100)
    draw_polygon(polygon, polygon.colour)
    sleep.sleep_ms(100)
    draw_polygon(polygon, ugfx.BLACK)
    sleep.sleep_ms(100)
    draw_polygon(polygon, polygon.colour)
    sleep.sleep_ms(500)
    draw_polygon(polygon, ugfx.BLACK)
    sleep.sleep_ms(100)
    draw_polygon(polygon, polygon.colour)
    sleep.sleep_ms(2000)


def draw_polygon(polygon, colour):
    ugfx.fill_polygon(polygon.x, polygon.y, polygon.points, colour)
    ugfx.polygon(polygon.x, polygon.y, polygon.points, ugfx.BLACK)


def display_text(text):
    ugfx.text(40, 150, text, ugfx.WHITE)


def display_notice(text):
    dialogs.notice(text, style=dialogs.default_style_badge)


def initialize():
    ugfx.area(0, 0, ugfx.width(), ugfx.height(), ugfx.BLACK)


###
# Game
###
current_key = 1


def run():
    while True:
        draw_progress_and_display_current_answer(current_key, unlocked_answers)

        execute_next_command()


def execute_next_command():
    while True:
        sleep.wfi()

        if buttons.is_pressed(Buttons.BTN_A):
            return answer_current_question()

        if buttons.is_pressed(Buttons.BTN_Menu) or buttons.is_pressed(Buttons.BTN_B):
            return quit_game()

        if buttons.is_pressed(Buttons.JOY_Up) or buttons.is_pressed(Buttons.JOY_Left):
            return next_question()

        if buttons.is_pressed(Buttons.JOY_Down) or buttons.is_pressed(Buttons.JOY_Right):
            return previous_question()


def answer_current_question():
    global unlocked_answers
    global current_key
    if unlocked_answers.get(current_key) is None:
        answer = prompt_and_check_answer(current_key)
        update_progress(current_key, answer)


def quit_game():
    app.restart_to_default()


def previous_question():
    global current_key
    if current_key == 10:
        current_key = 1
    else:
        current_key += 1


def next_question():
    global current_key
    if current_key == 1:
        current_key = 10
    else:
        current_key -= 1


def main():
    ugfx.init()

    read_progress()
    run()


if __name__ == "__main__":
    main()
