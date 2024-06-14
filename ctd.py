#LATEST ITERATION
from tkinter import *
import time
from random import choice, randint
import winsound
from classes import *
from assets_object import *

# Configs
WIDTH = 600 # screen width
HEIGHT = 900 # screen height
PLAYER_SIZE = 20 # width and height of the player box
KEY_CONFIG = {'1': 'positive', '2': 'negative', '3': 'prime', '4': 'complex'} # which key to press for each number type
NUMBER_TYPE = ['positive', 'negative'] # list for types of number
START_X = [WIDTH/8, 3*WIDTH/8, 5*WIDTH/8, 7*WIDTH/8]       # x coordinates for every dropping numbers
END_HEIGHT = HEIGHT-95 # height of the red line where HP loses if number crosses the line
HP = 3
SCORE = 0
CURRENT_LEVEL = 1
THRESHOLD = 5
POINTS = {
    'positive': 1,
    'negative': 1,
    'even': 2,
    'odd': 2,
    'complex': 3,
    'prime': 5
}

# declare the window
window = Tk()
# set window title
window.title(" ")
# set window width and height
window.configure(width=WIDTH, height=HEIGHT)

# set canvas for line/box drawing in tkinter
cvs = Canvas(window, width=WIDTH, height=HEIGHT)
cvs.configure(bg='grey1')
cvs.pack()

#create A gif
Runningimage = "assets\\gif3.gif"
BloodSpatterImage = "assets\\gif4.gif"
StreakImage = "assets\\gif5.gif"

CURRENTFRAME = 0

def getFrames(framelist, frame_Index, gifFileName, currentFrame):
    while True:
        try:
            # Read a frame from GIF file
            part = 'gif -index {}'.format(frame_Index)
            currentFrame = PhotoImage(file=gifFileName, format=part)
        except:
            last_frame = frame_Index - 1    # Save index for last frame
            break               # Will break when GIF index is reached
        framelist.append(currentFrame)
        frame_Index += 1        # Next frame index

    return framelist, last_frame

FrameList = []
RunningimageObject, Runningframes = getFrames(FrameList, 0,Runningimage, CURRENTFRAME)
FrameList= []
BloodimageObject, BloodSpatterframes = getFrames(FrameList,0, BloodSpatterImage, CURRENTFRAME)
FrameList = []
StreakGIFObject, StreakGIFframes = getFrames(FrameList, 0, StreakImage, CURRENTFRAME)
FrameList = []

# draw lines for each number dropdown line
for x in START_X:
    cvs.create_line(x, 20, x, HEIGHT-120, fill='gray50')
# draw the line where HP loses
cvs.create_line(0, END_HEIGHT, WIDTH, END_HEIGHT, fill='red', width=2)

# change window background color
window.configure(bg='gray2')

# show instructions for player
text1 = cvs.create_text(80, HEIGHT - 80, text= "'1' - Positive", fill="turquoise1", font=('Purisa', 13))
text2 = cvs.create_text(80, HEIGHT - 60, text="'2' - Negative", fill="SeaGreen1", font=('Purisa', 13))
text3 = cvs.create_text(80, HEIGHT - 40, text='', fill="gray99", font=('Purisa', 13)) # 3: prime number
text4 = cvs.create_text(80, HEIGHT - 20, text='', fill="gray99", font=('Purisa', 13)) # 4: complex number
hpText = cvs.create_text(WIDTH-70, HEIGHT-62, text=f"HP: {HP}", font=('Purisa', 15), fill="red3")
scoreText = cvs.create_text(WIDTH-70, HEIGHT-39, text=f"Scores: {SCORE}", font=('Purisa', 15), fill="RoyalBlue3")
levelText = cvs.create_text(WIDTH-295, HEIGHT-20, text=f"LEVEL {CURRENT_LEVEL}", font=('Purisa', 18), fill="yellow")

bloodSpatters = []
bloodSpatterExistenceTimes = []
questions = []
gifs = []
bullets = []
proj_lines = []
streakgifs = []



# variable to keep track of time after spawning a question
current_time = time.time()
ischecked = False
offset = 25
RunningFrameCount = 0
BloodSpatterFrameCount = 0
StreakGifCount = 0
factor = 2
isStreakExistence = False

ISPLAYING = True
ISPLAYINGSTREAKPROG = False
STREAKCOUNT = 0
STREAKSTEP = 8

def handleStreakStep(currentLvl = 1):
    if currentLvl == 1:
        streakStep = 8
    if currentLvl == 2:
        streakStep = 8
    if currentLvl == 3:
        streakStep = 8  
    return streakStep

STREAKSTEP = handleStreakStep(CURRENT_LEVEL)
FACTOR = 40
#Creating Hot Streak Bar
STREAKBARX = 110
STREAKBARY = 100
STREAKBARWIDTH = 10
STREAKBARHEIGHT = 20
borderFillColour = "green"
streakBar = ProgressBar(cvs, STREAKBARX,STREAKBARY,STREAKBARWIDTH,STREAKBARHEIGHT, fill="red")
streakMaxBarTop = ProgressBar(cvs, streakBar.xspawnpos-10,streakBar.yspawnpos-10,(STREAKSTEP)*(FACTOR)+10,10, fill=borderFillColour)
streakBarBottom = ProgressBar(cvs, streakBar.xspawnpos-10,streakBar.yspawnpos+10,(STREAKSTEP)*(FACTOR)+10,10,fill=borderFillColour)
streakBarEndLimit = ProgressBar(cvs, streakBar.xspawnpos+(STREAKSTEP)*(FACTOR), streakBar.yspawnpos,-10,10,fill=borderFillColour)
streakBarStartBlock = ProgressBar(cvs, streakBar.xspawnpos-10,streakBar.yspawnpos,10,10,fill=borderFillColour)

#AK Changing of Labels from Positive and Negative and Even and Odd Respectively
def changeLabel(labelName, text):
    cvs.itemconfig(labelName, text = text)

# objects lists
cannon = Cannon(cvs, WIDTH/2-PLAYER_SIZE/2, HEIGHT-80, PLAYER_SIZE)
guiding_line_obj = GuidingLine(cvs=cvs)
guiding_line = guiding_line_obj.rect

def playSound(selectedSoundList):
    selectedSound = choice(selectedSoundList)
    winsound.PlaySound(selectedSound, winsound.SND_FILENAME | winsound.SND_ASYNC)

# function for generating prime numbers from 2 to upper_limit
def sieve_of_eratosthenes(upper_limit):
    PRIME_NUMBERS = []
    lp = [0] * (upper_limit + 1)
    it=2
    while(it<=upper_limit):
        if(lp[it]==0):
            lp[it]=it
            PRIME_NUMBERS.append(it)
        it2=0
        while(it*PRIME_NUMBERS[it2]<=upper_limit):
            lp[it*PRIME_NUMBERS[it2]]=PRIME_NUMBERS[it2]
            if(PRIME_NUMBERS[it2]==lp[it]):
                break
            it2+=1
        it+=1
    return PRIME_NUMBERS

PRIME_NUMBERS = sieve_of_eratosthenes(100) # list for pre-calculated prime numbers

def TrackStreakPlaySound(streakCount, streakLimit, isPlayingStreakProg, hasstreaked):
    if hasstreaked == False:
        if streakCount == streakLimit //2:
            isPlayingStreakProg = True

    return isPlayingStreakProg

# function for moving any objects in canvas
def move(obj, x, y):
    obj.x = x
    obj.y = y
    cvs.moveto(obj.rect, obj.x, obj.y)

# function for the cannon shooting
def shoot(user_key):
    global HP, SCORE, THRESHOLD, CURRENT_LEVEL, SCORE,STREAKCOUNT,STREAKSTEP, ISPLAYINGSTREAKPROG, isStreakExistence, HASSTREAKED
    # getting width and height of the question object
    if KEY_CONFIG.get(user_key) != questions[0].answer:
        isStreakExistence = False
        HASSTREAKED = False
        playSound(ShockedSoundsFilenames)
        STREAKCOUNT = 0
        HP = max(0, HP-1)
        guiding_line_obj.show_error()
        cvs.itemconfig(hpText, text=f"HP: {HP}")
        
        if(len(streakgifs) > 0):
            cvs.delete(streakgifs[0].rect)
            streakgifs.clear()
        return

    question_width = questions[0].get_width()
    question_height = questions[0].get_height()

    SCORE += POINTS[questions[0].answer]
    cvs.itemconfig(scoreText, text=f"Scores: {SCORE}")

    # draw bullet trajectory line
    proj_line = (cvs.create_line(cannon.x + PLAYER_SIZE/2, cannon.y, questions[0].x + question_width/2, questions[0].y + question_height, fill='orange', width=3), time.time())
    proj_lines.append(proj_line)

    #Instantiate a Blood Spatter
    bloodSpatter = IMG_GIF(x= gifs[0].x, y= gifs[0].y, currentFrame=BloodSpatterFrameCount,imageObject=BloodimageObject, cvs=cvs)
    bloodSpatters.append(bloodSpatter)

    #AK -> Get references to thje global variables of SCORE and CURRENT_LEVEL perfom manipulations on BOTH
    changeLabel(scoreText, f"Scores: {SCORE}" )

    # remove the question from screen and from questions list after shooting it
    cvs.delete(questions[0].rect)
    questions.pop(0)

    cvs.delete(gifs[0].rect)
    gifs.pop(0)

    if SCORE // THRESHOLD > 0 and CURRENT_LEVEL < 3:
        CURRENT_LEVEL += 1
        return

    if isStreakExistence == False and ISPLAYINGSTREAKPROG == False and HASSTREAKED == False:
        STREAKCOUNT += 1
        streakBar.lengthenRectangle(streakCount=STREAKCOUNT,factor=FACTOR)
        playSound(hitSoundsFileNames)

    ISPLAYINGSTREAKPROG = TrackStreakPlaySound(streakCount=STREAKCOUNT,streakLimit=STREAKSTEP,isPlayingStreakProg=ISPLAYINGSTREAKPROG, hasstreaked=HASSTREAKED)

    if ISPLAYINGSTREAKPROG == True and isStreakExistence == False:
        print("playing")
        playSound(StreakProgressionSoundsFilenames)
        ISPLAYINGSTREAKPROG = False

# handle user's key strokes
def handle_keypress1(ev):
    # if no question exists, do nothing, else shoot
    #print(ev.char, KEY_CONFIG.get(ev.char), questions[0].answer)
    if questions:
        shoot(ev.char)


# function to restart and cleanup everything after losing
def restart():
    global CURRENT_LEVEL, STREAKCOUNT, NUMBER_TYPE, KEY_CONFIG
    # reset key binding
    window.bind('<KeyPress>', handle_keypress1)

    SCORE = 0
    # reset labels
    changeLabel(scoreText, f"Scores: {SCORE}")
    changeLabel(text1, "'1' - Positive")
    changeLabel(text2, "'2' - Negative")
    changeLabel(text3, "")
    changeLabel(text4, "")
    cvs.delete(loseText)

    # clear all lists
    for question in questions:
        cvs.delete(question.rect)

    for gif in gifs:
        cvs.delete(gif.rect)
        
    for blood in bloodSpatters:
        cvs.delete(blood)

    cvs.delete(guiding_line_obj)

    NUMBER_TYPE = ['positive', 'negative']
    KEY_CONFIG = {'1': 'positive', '2': 'negative', '3': 'prime', '4': 'complex'} # which key to press for each number type

    questions.clear()
    gifs.clear()
    bullets.clear()
    proj_lines.clear()
    bloodSpatterExistenceTimes.clear()
    STREAKCOUNT = 0

    CURRENT_LEVEL = 1

    STREAKSTEP = handleStreakStep(1)
    streakBar = ProgressBar(cvs, STREAKBARX,STREAKBARY,STREAKBARWIDTH,STREAKBARHEIGHT, fill="red")
    streakMaxBarTop = ProgressBar(cvs, streakBar.xspawnpos-10,streakBar.yspawnpos-10,(STREAKSTEP)*(FACTOR)+10,10, fill=borderFillColour)
    streakBarBottom = ProgressBar(cvs, streakBar.xspawnpos-10,streakBar.yspawnpos+10,(STREAKSTEP)*(FACTOR)+10,10,fill=borderFillColour)
    streakBarEndLimit = ProgressBar(cvs, streakBar.xspawnpos+(STREAKSTEP)*(FACTOR), streakBar.yspawnpos,-10,10,fill=borderFillColour)
    streakBarStartBlock = ProgressBar(cvs, streakBar.xspawnpos-10,streakBar.yspawnpos,10,10,fill=borderFillColour)

def level_transition(next_level):
    global CURRENT_LEVEL,STREAKCOUNT, SCORE, ISPLAYINGSTREAKPROG, HASSTREAKED, isStreakExistence
    CURRENT_LEVEL = next_level

    # black rectangle to drop from the top and cover the scene for level transition
    cover_rect = cvs.create_rectangle(0, 0, WIDTH, 0, fill='grey0')
    while cvs.coords(cover_rect)[3] < HEIGHT:
        # get coordinates of the cover rectangle
        x0, y0, x1, y1 = cvs.coords(cover_rect)
        cvs.coords(cover_rect, x0, y0, x1, y1 + 2)
        cvs.update()

    nice_text = cvs.create_text(WIDTH/2, HEIGHT/3, text='NICE!!!!!', fill='orange red', font = ('Purisa', 30))
    try_best_text = cvs.create_text(WIDTH/2, 1.5*HEIGHT/3, text='Try your best next stage!', fill='green yellow', font = ('Purisa', 30))
    cvs.update()

    time.sleep(2)

    cvs.delete(nice_text)
    cvs.delete(try_best_text)
    cvs.itemconfig(levelText, text = 'LEVEL ' + str(next_level))

    countdown()

    cvs.delete(cover_rect)

    for gif in gifs:
        cvs.delete(gif.rect)

    for question in questions:
        cvs.delete(question.rect)

    gifs.clear()
    questions.clear()
    streakBar.resetRectangle()
    STREAKCOUNT = 0
    SCORE = 0
    HASSTREAKED = False
    ISPLAYINGSTREAKPROG = False
    if len(streakgifs) > 0: 
        cvs.delete(streakgifs[0].rect)
        streakgifs.clear()
    isStreakExistence = False
    cvs.itemconfig(scoreText, text="Scores: 0")

# function for buttons
buttons = []

def mouse_decorator(func):
    def inner(*args, **kwargs):
        def handle_mouseclick(ev):
            for button in buttons:
                if button.check_mouse_collide(ev):
                    button.mouse_click()

        def handle_mousemotion(ev):
            for button in buttons:
                if button.check_mouse_collide(ev):
                    cvs.itemconfig(button.rect, fill='grey55')
                else:
                    cvs.itemconfig(button.rect, fill='grey0')

        # bind left click
        window.bind('<Button-1>', handle_mouseclick)

        # bind mouse motion to keep track of mouse pos
        window.bind('<Motion>', handle_mousemotion)

        func(*args, **kwargs)

        def cleanup_scene():
            for button in buttons:
                cvs.delete(button.rect)
                cvs.delete(button.text)
            buttons.clear()
            window.unbind('<Button-1>')
            window.unbind('<Motion>')

        cleanup_scene()

    return inner

@mouse_decorator
def end(has_passed):
    global loseText
    cover_rect = cvs.create_rectangle(0,0,WIDTH,0, fill = 'grey0')

    cvs.delete(guiding_line_obj)
    for gif in gifs:
        cvs.delete(gif)

    while cvs.coords(cover_rect)[3] < HEIGHT:
        x0, y0, x1, y1 = cvs.coords(cover_rect)
        cvs.coords(cover_rect, x0, y0, x1, y1 + 2)
        cvs.update()

    if not has_passed:
        text1 = 'No lah! It\'s almost...!'
        text2 = 'Go back to your school, PLSSS!'
        text3 = ''
        text4 = 'Try again ?'
    else:
        text1 = 'Congratulations !'
        text2 = 'You are the most skillful killer !!!'
        text3 = f'"{name}"'
        text4 = 'Play again ?'

    loseText = cvs.create_text(WIDTH/2, HEIGHT/3, text=text1, fill='red3', font = ('Purisa', 30))
    backtoschool_text = cvs.create_text(WIDTH/2, 1.15*HEIGHT/3, text=text2, fill='DarkOrange1', font = ('Purisa', 30))
    tryagain_text = cvs.create_text(WIDTH/2, 1.4*HEIGHT/3, text=text3, fill='SpringGreen', font = ('Purisa', 30))
    last_text = cvs.create_text(WIDTH/2, 1.6*HEIGHT/3, text=text4, fill='orchid2', font = ('Purisa', 30))
    no_button = Button(WIDTH/6, 2*HEIGHT/3, WIDTH/6 + 100, 2*HEIGHT/3 - 50, text='No')
    yes_button = Button(4*WIDTH/6, 2*HEIGHT/3, 4*WIDTH/6 + 100, 2*HEIGHT/3 - 50, text='Yes')
    cvs.itemconfig(levelText, text = 'LEVEL 1')
    buttons.append(no_button)
    buttons.append(yes_button)

    cvs.update()

    time.sleep(1)

    while True:
        # if user press space, quit this lose function and continue game
        if yes_button.clicked:
            break

        if no_button.clicked:
            import sys
            sys.exit()

        window.update()
        time.sleep(0.001)

    streakBar.resetRectangle()
    cvs.delete(cover_rect)
    cvs.delete(backtoschool_text)
    cvs.delete(tryagain_text)
    cvs.delete(last_text)
    for button in buttons:
        cvs.delete(button.text)
        cvs.delete(button.rect)
    buttons.clear()

    restart()
    countdown()


@mouse_decorator
def menu():
    global name
    name = ''
    continue_menu = [True]
    winsound.PlaySound(MainMenuMusic, winsound.SND_FILENAME |winsound.SND_ASYNC | winsound.SND_LOOP)

    name_instruction_title = 'Greetings! Name?  '
    menu_bg_rect = cvs.create_rectangle(0, 0, WIDTH, HEIGHT, fill='gray1')
    name_instruction = cvs.create_text(WIDTH/20, 3*HEIGHT/5, text=name_instruction_title, fill = 'yellow', font = ('Purisa', 20), anchor='w')
    title = cvs.create_text(WIDTH/2, HEIGHT/5, text='The Mathematician\'s Massacre', fill='red', font=('Purisa', 30))
    sub_title = cvs.create_text(WIDTH/2, HEIGHT/4, text='- OATAD -', fill='green', font=('Purisa', 25))

    # helper function to add a character from name variable
    def input_name(ev):
        global name
        name += ev.char
        cvs.itemconfig(name_instruction, text = name_instruction_title + '             ' + name, fill="salmon1")

    # helper function to remove a character from name variable
    def delete_char(ev):
        global name
        if name:
            name = name[:-1]
        cvs.itemconfig(name_instruction, text = name_instruction_title + '             ' +  name, fill='dodger blue')

    # helper function to set the variable continue_menu to false so that the game can proceed
    def set_continue(ev):
        continue_menu[0] = False

    # bind enter key to set variable 'continue_menu' to False
    window.bind('<Return>', set_continue)

    # bind user input to change the variable 'name'
    window.bind('<KeyPress>', input_name)
    window.bind('<BackSpace>', delete_char)

    while continue_menu[0]:
        cvs.update()

    # clean up scene
    cvs.delete(title)
    cvs.delete(sub_title)
    cvs.delete(menu_bg_rect)
    cvs.delete(name_instruction)

    # black blackground rectangle
    background = cvs.create_rectangle(0, 0, WIDTH, HEIGHT, fill='grey0')

    # 'are you ready for massacre?'
    title = cvs.create_text(WIDTH/2, HEIGHT/5, text='Are you ready for the massacre?', anchor='center', fill='red', font=('Purisa', 25))

    # buttons
    yes_button = Button(WIDTH/2+50, 2*HEIGHT/3 - 30 ,WIDTH/2+170, 2*HEIGHT/3 + 20, text='Yes')
    no_button = Button(WIDTH/2-50, 2*HEIGHT/3 - 30 ,WIDTH/2-170, 2*HEIGHT/3 + 20, text='No')
    buttons.append(yes_button)
    buttons.append(no_button)


    # function for setting up 'no' button clicked
    def no_scene():
        last_time = time.time()

        background = cvs.create_rectangle(0, 0, WIDTH, HEIGHT, fill='grey0')
        too_late = cvs.create_text(WIDTH/2, HEIGHT/5, anchor='center', font=('Purisa', 45), fill='OrangeRed2', text='Too late ah boi')
        while time.time() - last_time < 1.5:
            cvs.update()
        cvs.delete(too_late)
        cvs.delete(background)

    while True:
        if yes_button.clicked:
            break

        if no_button.clicked:
            no_scene()
            break

        cvs.update()

    cvs.delete(title)
    cvs.delete(background)
    winsound.PlaySound(None,winsound.SND_PURGE)

# function for counting down from 3 to 1
def countdown():
    for cd in range(3, 0, -1):
        current_time = time.time()

        font_size = 600
        countdown_text = cvs.create_text(WIDTH/2, HEIGHT/2, text=cd, font = ('Purisa', font_size), fill = 'grey99')

        while time.time() - current_time < 1:
            font_size = max(0, font_size - 1)
            cvs.itemconfig(countdown_text, font = ('Purisa', font_size))
            cvs.update()
        cvs.delete(countdown_text)

def Intro():
    winsound.PlaySound(introsound, winsound.SND_FILENAME | winsound.SND_ASYNC)

class Button:
    def __init__(self, x0, y0, x1, y1, text):
        self.x = x0
        self.y = y0
        self.rect = cvs.create_rectangle(x0, y0, x1, y1, width=2, outline='grey99')
        self.text = cvs.create_text((x0+x1)/2, (y0+y1)/2, text=text, anchor='center', fill='gold', font=('Purisa', 20))
        self.clicked = False

    def check_mouse_collide(self, ev):
        return cvs.bbox(self.rect)[0] <= ev.x <= cvs.bbox(self.rect)[2] and cvs.bbox(self.rect)[1] <= ev.y <= cvs.bbox(self.rect)[3]

    def mouse_click(self):
        self.clicked = True


def BAnimLifetimeCounter(counterStep, counterLimit, multiplicativeFac, playing = True):
    if playing == False:
        return playing, counterStep

    counterStep += 0.001 * multiplicativeFac
    if counterStep >= counterLimit:
        playing = False

    return playing, counterStep

def AnimFrameCounter(counterStep, counterLimit, multiplicativeFac, animFrame, maxAnimFrames):
    counterStep += 0.001 * multiplicativeFac
    if counterStep >= counterLimit:
        animFrame += 1
        if animFrame == maxAnimFrames:
            animFrame = 0
        
        counterStep = 0

    return animFrame, counterStep

def counter(counterStep, counterLimit, multiplicativeFac, bplaynext):
    counterStep += 0.001 * multiplicativeFac
    if counterStep >= counterLimit:
        bplaynext = True
        counterStep = 0
   
    return bplaynext, counterStep

def handleHasStreaked(counterStep, counterLimit, multiplicativeFac, hasStreaked, previousScore, currentScore):
    if hasStreaked == True and currentScore > previousScore:
       counterStep += 0.001 * multiplicativeFac
       if counterStep >= counterLimit:
           counterStep = 0
           hasStreaked = False
    
    return hasStreaked, counterStep

def IntroSpeech(n):
    while n < 1:
        winsound.PlaySound(introsound,winsound.SND_FILENAME | winsound.SND_ASYNC)
        time.sleep(0.5)
        n+=1

menu()
countdown()
IntroSpeech(0)

#main loop for the game

window.bind('<KeyPress>', handle_keypress1)

running = True

STREAKSOUNDTIMER = 5.0
STREAKSOUNDSTEP = 0.0
SOUNDPLAYTIMESTEP = 0.0
STREAKGIFTIMESTEP = 0.0
STREAKGIFTIMETHRESHOLD = 0.1

TIMESTEP = 0.0
TIMELIMIT_RUN = 0.025
TIMESTEP_BLOOD = 0.0
TIMELIMIT_BLOOD = 0.040
TIMESTEP_BLOOD_EXISTENCE = 0.0
TIME_EXISTENCE_BLOOD = 0.25
PLAYNEXTSOUNDINTERVAL = 0.0015
STREAKCOOLDOWNTIMER = 0
previousScore = SCORE

RunningFrameCount = 0
BloodSpatterFrameCount = 0
StreakGifCount = 0

current_time = time.time()
ischecked = False
isStreakExistence = False
HASSTREAKED = False

bPLAYNEXT = False
PLAYNEXTSOUNDINTERVAL = 0.003

soundlifeLimit = 2.0
previousScore = 0

yvelocity = 1.5

STREAKCOOLDOWNDURATION = STREAKSOUNDTIMER+0.005

while running:
    


    # Changes config at different levels
    if CURRENT_LEVEL == 2 and ischecked == False:
        changeLabel(levelText, "LEVEL {a}".format(a = CURRENT_LEVEL))
        level_transition(next_level=2)

        HP = 3
        cvs.itemconfig(hpText, text=f"HP: {HP}")
        changeLabel(text1, "'1' - Even")
        cvs.itemconfig(text1, fill = 'maroon1')
        changeLabel(text2, "'2' - Odd")
        cvs.itemconfig(text2, fill = "OliveDrab1" )
        changeLabel(text3, "'3' - Complex")
        cvs.itemconfig(text3, fill = "cyan")
        NUMBER_TYPE = ['even','odd','complex','prime']
        KEY_CONFIG = {'1': 'even', '2': 'odd', '3': 'complex', '4': 'prime'}

        yvelocity = 1.0
        ischecked = True

        cvs.delete(streakBarBottom.rect)
        cvs.delete(streakBarEndLimit.rect)
        cvs.delete(streakBarStartBlock.rect)
        cvs.delete(streakMaxBarTop.rect)

        STREAKSTEP = handleStreakStep(CURRENT_LEVEL)
        streakMaxBarTop = ProgressBar(cvs, streakBar.xspawnpos-10,streakBar.yspawnpos-10,(STREAKSTEP)*(FACTOR)+10,10, fill=borderFillColour)
        streakBarBottom = ProgressBar(cvs, streakBar.xspawnpos-10,streakBar.yspawnpos+10,(STREAKSTEP)*(FACTOR)+10,10,fill=borderFillColour)
        streakBarEndLimit = ProgressBar(cvs, streakBar.xspawnpos+(STREAKSTEP)*(FACTOR), streakBar.yspawnpos,-10,10,fill=borderFillColour)
        streakBarStartBlock = ProgressBar(cvs, streakBar.xspawnpos-10,streakBar.yspawnpos,10,10,fill=borderFillColour)

    if CURRENT_LEVEL == 3 and ischecked == True:
        changeLabel(levelText, "LEVEL {a}".format(a = CURRENT_LEVEL))
        level_transition(next_level=3)
        
        if SCORE == THRESHOLD:
            end(has_passed=True)

        HP = 3
        cvs.itemconfig(hpText, text=f"HP: {HP}")
        changeLabel(text1, "'1' - Even")
        cvs.itemconfig(text1, fill = 'deep pink')
        changeLabel(text2, "'2' - Odd")
        cvs.itemconfig(text2, fill = "lawn green" )
        changeLabel(text3, "'3' - Complex")
        cvs.itemconfig(text3, fill = "turquoise1")
        changeLabel(text4, "'4' - Prime")
        cvs.itemconfig(text4, fill = "goldenrod1")

        NUMBER_TYPE = ['even','odd','complex','prime']
        KEY_CONFIG = {'1': 'even', '2': 'odd', '3': 'complex', '4': 'prime'}

        yvelocity = 0.7
        ischecked = False


        cvs.delete(streakBarBottom.rect)
        cvs.delete(streakBarEndLimit.rect)
        cvs.delete(streakBarStartBlock.rect)
        cvs.delete(streakMaxBarTop.rect)

        STREAKSTEP = handleStreakStep(CURRENT_LEVEL)
        streakMaxBarTop = ProgressBar(cvs, streakBar.xspawnpos-10,streakBar.yspawnpos-10,(STREAKSTEP)*(FACTOR)+10,10, fill=borderFillColour)
        streakBarBottom = ProgressBar(cvs, streakBar.xspawnpos-10,streakBar.yspawnpos+10,(STREAKSTEP)*(FACTOR)+10,10,fill=borderFillColour)
        streakBarEndLimit = ProgressBar(cvs, streakBar.xspawnpos+(STREAKSTEP)*(FACTOR), streakBar.yspawnpos,-10,10,fill=borderFillColour)
        streakBarStartBlock = ProgressBar(cvs, streakBar.xspawnpos-10,streakBar.yspawnpos,10,10,fill=borderFillColour)

    RunningFrameCount,TIMESTEP = AnimFrameCounter(counterStep=TIMESTEP, counterLimit=TIMELIMIT_RUN, multiplicativeFac=2, animFrame=RunningFrameCount, maxAnimFrames=Runningframes)

    BloodSpatterFrameCount, TIMESTEP_BLOOD = AnimFrameCounter(counterStep=TIMESTEP_BLOOD, counterLimit=TIMELIMIT_BLOOD, multiplicativeFac=1,animFrame=BloodSpatterFrameCount,maxAnimFrames=BloodSpatterframes)

    if len(bloodSpatters) > 0:
        TIMESTEP_BLOOD_EXISTENCE += 0.001
        if TIMESTEP_BLOOD_EXISTENCE >= TIME_EXISTENCE_BLOOD:
            cvs.delete(bloodSpatters[0].rect)
            bloodSpatters.pop(0)
            TIMESTEP_BLOOD_EXISTENCE = 0

    if len(bloodSpatters) > 0:
        for bloodSpatter in bloodSpatters:
            bloodSpatter.animation(BloodSpatterFrameCount)

    # Every n seconds, create a question to dropdown from top
    if time.time() - current_time > 2:
        # Initialize question object on random dropdown line
        index = randint(0, len(START_X)-1)
        question = Question(cvs, START_X[index], CURRENT_LEVEL, NUMBER_TYPE, PRIME_NUMBERS)
        gifSpawn = IMG_GIF(START_X[index], imageObject=RunningimageObject, cvs=cvs) #creating a paired gif for every quesiton element

        # Centering question and gifimage to the dropdown line
        question_width = question.get_width()
        question.x -= question_width / 2

        gifSpawn_width = gifSpawn.getWidth()
        gifSpawn.x -= (gifSpawn_width/2 + question_width/2 + offset)
        gifSpawn.y -= 10

        # Append new question to the questions list
        questions.append(question)

        gifs.append(gifSpawn)

        # Update time
        current_time = time.time()

    STREAKSTEP = handleStreakStep(currentLvl=CURRENT_LEVEL)


    if STREAKCOUNT >= STREAKSTEP and STREAKCOUNT % STREAKSTEP == 0 and isStreakExistence == False and HASSTREAKED == False:
        playSound(StreakOpeningSoundsFilenames)
        isplaying = False
        STREAKSOUNDSTEP = 0
        SOUNDPLAYTIMESTEP = 0
        if len(streakgifs) == 0:
            streakgifs.append(IMG_GIF(x=600, y=400, currentFrame=StreakGifCount, imageObject=StreakGIFObject,xdimension=250,ydimension=150,cvs = cvs))
        HASSTREAKED = True
        isStreakExistence = True
        bPLAYNEXT = False
        previousScore = SCORE
        STREAKCOUNT = 0
        STREAKGIFTIMESTEP = 0
        PLAYNEXTSOUNDCOUNTER = 0.0
    
    HASSTREAKED, STREAKCOOLDOWNTIMER = handleHasStreaked(STREAKCOOLDOWNTIMER,STREAKCOOLDOWNDURATION,1,hasStreaked=HASSTREAKED, previousScore=previousScore, currentScore=SCORE)
    if isStreakExistence == True:
        bPLAYNEXT, PLAYNEXTSOUNDCOUNTER = counter(counterStep=PLAYNEXTSOUNDCOUNTER,counterLimit=PLAYNEXTSOUNDINTERVAL,multiplicativeFac=2,bplaynext=bPLAYNEXT)
        if bPLAYNEXT == True:
            if isplaying == False:
                isplaying, SOUNDPLAYTIMESTEP = BAnimLifetimeCounter(counterStep=SOUNDPLAYTIMESTEP, counterLimit=soundlifeLimit,multiplicativeFac=1)
                playSound(StreakRunningSoundFilenames)
                SOUNDPLAYTIMESTEP = 0

        #Animate Streak Gif Image
        StreakGifCount, STREAKGIFTIMESTEP = AnimFrameCounter(counterStep=STREAKGIFTIMESTEP,counterLimit=STREAKGIFTIMETHRESHOLD,multiplicativeFac=1,animFrame=StreakGifCount,maxAnimFrames=StreakGIFframes)
        streakgifs[0].animation(StreakGifCount)
        isStreakExistence,STREAKSOUNDSTEP = BAnimLifetimeCounter(counterStep=STREAKSOUNDSTEP,counterLimit=STREAKSOUNDTIMER,multiplicativeFac=1, playing=ISPLAYING)
        isplaying, SOUNDPLAYTIMESTEP = BAnimLifetimeCounter(counterStep=SOUNDPLAYTIMESTEP, counterLimit=soundlifeLimit,multiplicativeFac=1, playing=ISPLAYING)
    
        if isStreakExistence == False:
            streakBar.resetRectangle()
            cvs.delete(streakgifs[0].rect)
            streakgifs.pop(0)
            STREAKCOUNT = 0
            bPLAYNEXT = False

    # If a question exists, draw dotted lines to show the current number to be shot
    cvs.delete(guiding_line)
    if questions:
        question_width = questions[0].get_width()
        question_height = questions[0].get_height()
        guiding_line = guiding_line_obj.update(cannon, questions, PLAYER_SIZE)


    # Update every question object
    for question in questions:
        move(question, question.x, question.y + yvelocity)
        question_height = question.get_height()
        # If question touches the red line, remove it and deduct HP
        if question.y + question_height > END_HEIGHT:
            cvs.delete(question.rect)
            questions.pop(0)
            HP = max(0, HP-1)
            cvs.itemconfig(hpText, text=f"HP: {HP}")

    for gif in gifs:
        gif.animation(RunningFrameCount)
        move(gif, gif.x, gif.y + yvelocity)
        gif_height = gif.getHeight()

        if gif.y + gif_height >= END_HEIGHT:
            cvs.delete(gif.rect)
            gifs.pop(0)
            break

    # Update every projection lines
    if proj_lines and time.time() - proj_lines[0][1] > 0.2:
        cvs.delete(proj_lines[0][0])
        proj_lines.pop(0)

    if HP <= 0:
        if CURRENT_LEVEL == 1:
            end(has_passed=False)
        
        if CURRENT_LEVEL == 2:
            end(has_passed=False)
        
        if CURRENT_LEVEL == 3:
            end(has_passed=True)

        # reset HP attribute
        HP = 3
        SCORE = 0
        cvs.itemconfig(hpText, text=f"HP: {HP}")

    # Update screen every n seconds
    window.update()
    time.sleep(0.001)  
