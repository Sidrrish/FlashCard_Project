BACKGROUND_COLOR = "#B1DDC6"
from tkinter import *
import pandas
import random
current_choice = {}
words_format = {}

try:
    file = pandas.read_csv("./data/words_to_learn.csv")
except FileNotFoundError:
    original_file = pandas.read_csv("./data/french_words.csv")
    words_format = original_file.to_dict(orient='records')
else:
    words_format = file.to_dict(orient='records')


def next_card():
    global current_choice, flip_timer
    window.after_cancel(flip_timer)
    current_choice = random.choice(words_format)
    canvas.itemconfig(text1, text='French', fill='black')
    canvas.itemconfig(text2, text=current_choice['French'], fill='black')
    canvas.itemconfig(card_background, image=card_front)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(card_background, image=card_back)
    canvas.itemconfig(text1, text='English', fill='white')
    canvas.itemconfig(text2, text=current_choice['English'], fill='white')


def is_known():
    next_card()
    words_format.remove(current_choice)
    data = pandas.DataFrame(words_format)
    data.to_csv("./data/words_to_learn")

window = Tk()
window.title("Flash Card")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

card_back = PhotoImage(file="./images/card_back.png")
card_front = PhotoImage(file="./images/card_front.png")
right = PhotoImage(file="./images/right.png")
wrong = PhotoImage(file="./images/wrong.png")

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_background = canvas.create_image(400, 263, image= card_front)
text1 = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
text2 = canvas.create_text(400, 283, text='', font=('Ariel', 60, 'bold'))
canvas.grid(column=1, row=1, columnspan=2)

known_button = Button(image=right, command=flip_card)
known_button.grid(column=2, row=2)

unknown_button = Button(image=wrong, command=is_known)
unknown_button.grid(column=1, row=2)
next_card()


window.mainloop()