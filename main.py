from tkinter import *
from tkinter import messagebox
import random
import pandas as pd

BACKGROUND_COLOR = "#B1DDC6"
FONT_NAME = "Ariel"
STARTED = False
MY_TIMER = None
FILE_PATH_ORIGINAL = "./data/french_words.csv"
FILE_PATH_TO_LEARN = "./data/to_learn.csv"
VOC_DICT = []
CURRENT_VOCAB = {}

# ------------------ data ---------------------- #

def get_voc():
    """Finds a random word and sets the global variable accordingly."""
    global CURRENT_VOCAB
    CURRENT_VOCAB = random.choice(VOC_DICT)


def adjust_file():
    """Updates the file with vocabulary still to learn."""
    VOC_DICT.remove(CURRENT_VOCAB)
    voc_dict_df = pd.DataFrame(VOC_DICT)
    voc_dict_df.to_csv(FILE_PATH_TO_LEARN, index=False)


# ------------------ functions ---------------------- #

def renew():
    """Sets the flashcard to a new word and calls for show_answer() to reveal the solution after three seconds."""
    global VOC_DICT
    global CURRENT_VOCAB
    global MY_TIMER
    if MY_TIMER is not None:
        window.after_cancel(MY_TIMER)
    if len(VOC_DICT) > 0:
        get_voc()
        canvas.itemconfig(vocab, text=CURRENT_VOCAB["French"])
        canvas.itemconfig(card_image, image=FRONT_IMAGE)
        canvas.itemconfig(lang, text="French")
        MY_TIMER = window.after(3000, show_answer)
    else:
        canvas.itemconfig(lang, text="You are through all words")
        voc_df_new = pd.read_csv(FILE_PATH_ORIGINAL)
        VOC_DICT = voc_df_new.to_dict(orient="records")


def show_answer():
    """Reveals the solution"""
    canvas.itemconfig(vocab, text=CURRENT_VOCAB["English"])
    canvas.itemconfig(lang, text="English")
    canvas.itemconfig(card_image, image=BACK_IMAGE)


def correct_answer():
    """Checks whether the check button is used to start or mark for correct.
     If it is used for marking correct, it calls adjust_file() and then renew()."""
    global STARTED
    if not STARTED:
        STARTED = True
    else:
        adjust_file()

    renew()


def wrong_answer():
    """Calls renew() only. The word is not deleted from the file."""
    renew()


# ------------------ UI ---------------------- #
window = Tk()
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
window.title("French")

FRONT_IMAGE = PhotoImage(file="./images/card_front.png")
BACK_IMAGE = PhotoImage(file="./images/card_back.png")

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_image = canvas.create_image(400, 263, image=FRONT_IMAGE)
canvas.grid(column=0, row=0, columnspan=2)

wrong_image = PhotoImage(file="./images/wrong.png")
button_wrong = Button(image=wrong_image, command=wrong_answer)
button_wrong.grid(column=0, row=1)

check_image = PhotoImage(file="./images/right.png")
button_correct = Button(highlightthickness=0, image=check_image, command=correct_answer, bg=BACKGROUND_COLOR)
button_correct.grid(column=1, row=1)

lang = canvas.create_text(400, 150, text="Flash Cards", fill="black", font=(FONT_NAME, 40, "italic"))

vocab = canvas.create_text(400, 263, text="Press check mark to start", fill="black", font=(FONT_NAME, 60, "bold"))

# ------------------ Running ---------------------- #


answer = messagebox.askquestion(title="Your progress", message="Would you like to take up were you left?")
if answer == "no":
    try:
        voc_df = pd.read_csv(FILE_PATH_ORIGINAL)
        VOC_DICT = voc_df.to_dict(orient="records")
    except FileNotFoundError:
        VOC_DICT = [{'French': 'no data', 'English': 'no data'}]
        messagebox.showinfo(title="No data", message="The file has been removed. Please move it back and start anew.")
else:
    try:
        voc_df = pd.read_csv(FILE_PATH_TO_LEARN)
        VOC_DICT = voc_df.to_dict(orient="records")
    except FileNotFoundError:
        VOC_DICT = [{'French': 'no data', 'English': 'no data'}]
        messagebox.showinfo(title="No data", message="You have no progress saved. Please start anew.")




window.mainloop()
