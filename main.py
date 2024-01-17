from tkinter import *
import requests
import random
import html

# (Open Trivia Database API)
api_link = "https://opentdb.com/api.php?category=15"  # Using Base URL, we will have to pass parameters ourselves
api_parameters = {
    'amount': 20,
    'type': 'boolean'
}

###############  GET QUESTIONS FROM API  ###############
# Getting 10 true/false questions
def get_questions():
    response = requests.get(url=api_link, params=api_parameters)
    response.raise_for_status()
    data = response.json()
    return data['results']

###############  GAME VARIABLES  ####################
sc = 0  # To keep track of score
q_list = []
total_questions = 0
correct_answers = 0
wrong_answers = 0
FONT1 = ("Algeria", 15, 'bold')
FONT2 = ("Kabel", 20, 'normal')
q_color = "#171717"
bg_color = "#008080"
cd_color = "#f1c40f"
ques = None
k = None  # for window.after() events

############ BUTTON FUNCTIONS  ##############
def start_quiz():

    global sc, q_list, ques, k, total_questions, correct_answers, wrong_answers
    greeting_label.grid_forget()  # Hide the greeting label
    start_btn.grid_forget()  # Remove the Start Quiz button
    q_list = get_questions()
    total_questions = len(q_list)
    correct_answers = 0
    wrong_answers = 0
    ques = random.choice(q_list)
    score.config(text=f"Score: {sc}")
    question_counter.config(text=f"Questions Remaining: {total_questions}")
    card.grid(column=1, row=3, columnspan=3)  # Show the question card
    true_btn.grid(column=1, row=5)  # Show the True button
    false_btn.grid(column=3, row=5)  # Show the False button
    update_card()

def res_true():

    global ques, sc, q_list, k, total_questions, correct_answers, wrong_answers
    if(len(q_list) == 0):  # No remaining questions
        finish_quiz()
    else:
        if(ques['correct_answer'] == "True"):
            # Player is correct
            sc += 1
            correct_answers += 1
            card.config(bg='green')
            score.config(text=f"Score: {sc}")
        else:
            # Player is incorrect
            wrong_answers += 1
            card.config(bg='red')
        # We should remove the question from q_list only after it has been attempted
        
        q_list.remove(ques)
        total_questions -= 1
        question_counter.config(text=f"Questions Remaining: {total_questions}")
        if(k != None):
            window.after_cancel(k)
        k = window.after(400, update_card)

def res_false():

    global ques, sc, q_list, k, total_questions, correct_answers, wrong_answers
    if(len(q_list) == 0):  # No remaining questions
        finish_quiz()
    else:
        if(ques['correct_answer'] == "False"):
            # Player is correct
            sc += 1
            correct_answers += 1
            card.config(bg='green')
            score.config(text=f"Score: {sc}")
        else:
            # Player is incorrect
            wrong_answers += 1
            card.config(bg='red')
        q_list.remove(ques)
        total_questions -= 1
        question_counter.config(text=f"Questions Remaining: {total_questions}")
        if(k != None):
            window.after_cancel(k)
        k = window.after(400, update_card)

def finish_quiz():

    global sc, q_list, ques, k, correct_answers, wrong_answers
    card.grid_forget()  # Hide the question card
    restart_btn.grid(column=2, row=5)  # Show the Restart Quiz button
    true_btn.grid_forget()  # Hide the True button
    false_btn.grid_forget()  # Hide the False button
    score.config(text=f"Final Score: {sc}")
    question_counter.config(text=f"Correct Answers: {correct_answers}\nWrong Answers: {wrong_answers}")

def restart_quiz():

    global sc, q_list, ques, k, total_questions, correct_answers, wrong_answers
    sc = 0
    q_list = []  # Reset the question list
    total_questions = 0
    correct_answers = 0
    wrong_answers = 0
    restart_btn.grid_forget()  # Hide the Restart Quiz button
    start_btn.grid(column=2, row=4)  # Show the Start Quiz button
    greeting_label.config(text="Welcome to Quizzy! Press 'Start Quiz' to begin.")

##############  UPDATE QUESTION CARD  ###############
def update_card():

    global ques, q_list
    card.config(bg=cd_color)
    if(len(q_list) == 0):  # No remaining questions
        finish_quiz()
    else:
        ques = random.choice(q_list)
        card.itemconfig(card_txt, text=html.unescape(ques['question']))

################  UI SETUP  ##################
# Set Up Window
window = Tk()
window.title("GamesQuizzy")
window.config(bg=bg_color, padx=50, pady=20)
window.resizable(False, False)  # Make the window non-resizable

# Greeting Label
greeting_label = Label(text="Welcome to GamesQuizzy Press 'Start Quiz' to begin.", font=FONT1, fg='white', bg=bg_color)
greeting_label.grid(column=1, row=0, columnspan=3)

# Set Up Score Label
score = Label(text=f"Score: {sc}", font=FONT1, fg='white', bg=bg_color)
score.config(pady=10)
score.grid(column=3, row=1)

# Set Up Question Counter Label

question_counter = Label(text="", font=FONT1, fg='white', bg=bg_color)
question_counter.grid(column=1, row=1)

# Blank Row to create space between buttons and card 

b_row = Label(text='', bg=bg_color, fg=bg_color)
b_row.grid(column=2, row=2)

# Set Up Canvas to display the question

card = Canvas(bg=cd_color, width=600, height=400, highlightthickness=0)
card.grid(column=1, row=3, columnspan=3)
# Unescaping HTML entities before displaying the question (Using html module)

card_txt = card.create_text(300, 200, text="", font=FONT2, fill=q_color, width=400)

# Set Up Buttons

# Start Quiz btn

start_btn = Button(text="Start Quiz", font=FONT1, fg='white', bg='green', command=start_quiz)
start_btn.grid(column=2, row=4)

# True btn

true_img = PhotoImage(file='./images/true img.png')
true_btn = Button(image=true_img, highlightthickness=0, border=0, command=res_true)
true_btn.grid(column=1, row=5)
true_btn.grid_forget()  # Hide the True button initially

# False btn

false_img = PhotoImage(file='./images/false img.png')
false_btn = Button(image=false_img, highlightthickness=0, border=0, command=res_false)
false_btn.grid(column=3, row=5)
false_btn.grid_forget()  # Hide the False button initially

# Restart btn

restart_btn = Button(text="Restart Quiz", font=FONT1, fg='white', bg='blue', command=restart_quiz)
restart_btn.grid(column=2, row=6)
restart_btn.grid_forget()  # Hide the Restart Quiz button initially

# To keep the window displayed

window.mainloop()
