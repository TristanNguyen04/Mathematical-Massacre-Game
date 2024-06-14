from random import randint, choice
import time

class ProgressBar:
    def __init__(self, cvs, xspawnpos, yspawnpos, width=10, height=20, fill= ''):
        self.xspawnpos = xspawnpos
        self.yspawnpos = yspawnpos
        self.width = width
        self.height = height
        self.fill = fill
        self.cvs = cvs

        self.rect = self.cvs.create_rectangle(xspawnpos, yspawnpos, xspawnpos+self.width, yspawnpos+self.height, fill=self.fill)

    def lengthenRectangle(self,streakCount, factor):

        self.cvs.coords(self.rect, self.xspawnpos,self.yspawnpos,self.xspawnpos+(streakCount*factor),self.yspawnpos+self.height)

    def resetRectangle(self):
        self.cvs.coords(self.rect,100,100,self.xspawnpos+10,self.yspawnpos+20)


class IMG_GIF:
    def __init__(self, x, cvs, y=0, y_vel=2, currentFrame = 0, imageObject = [], xdimension=50, ydimension=50):
        self.x = x
        self.y = y
        self.y_vel = y_vel
        self.currentFrame = currentFrame
        self.imageObject = imageObject
        self.xdimension = xdimension
        self.ydimension =ydimension
        self.cvs = cvs

        self.rect = cvs.create_image(50,50, image= self.imageObject[self.currentFrame])
        width = cvs.bbox(self.rect)[2] - cvs.bbox(self.rect)[0]
        cvs.move(self.rect, x-width, self.y)

    def getWidth(self):
        return self.cvs.bbox(self.rect)[2] - self.cvs.bbox(self.rect)[0]

    def getHeight(self):
        return self.cvs.bbox(self.rect)[3] - self.cvs.bbox(self.rect)[1]

    def animation(self, currentFrame):
        self.cvs.itemconfig(self.rect, image= self.imageObject[int(currentFrame)])

    def TrackFrames(currentFrame, totalFrames):
        if currentFrame == totalFrames:
            return True
        

class GuidingLine:
    def __init__(self, cvs):
        self.rect = cvs.create_line(0, 0, 0, 0)
        self.color = 'grey51'
        self.last_error_time = time.time()
        self.cvs = cvs

    # set last error time to now, when current_time - last error time < 1 second, set color to red.
    def show_error(self):
        self.last_error_time = time.time()

    def update(self, cannon, questions, PLAYER_SIZE):
        if time.time() - self.last_error_time < 0.5:
            self.color = 'red2'
        else:
            self.color = 'grey51'
        return self.cvs.create_line(cannon.x+PLAYER_SIZE/2, cannon.y, questions[0].x+(questions[0].get_width()/2), questions[0].y+(questions[0].get_height()/2), dash=(5, 1), fill=self.color)

class Cannon:
    def __init__(self, cvs, x, y, PLAYER_SIZE):
        self.x = x
        self.y = y
        self.rect = cvs.create_rectangle(0, 0, PLAYER_SIZE, PLAYER_SIZE, fill='grey99')
        cvs.moveto(self.rect, self.x, self.y)

class Question:
    def __init__(self, cvs, x, CURRENT_LEVEL, NUMBER_TYPE, PRIME_NUMBERS):
        self.x = x
        self.y = 0
        self.y_vel = 2
        self.cvs = cvs

        # from NUMBER_TYPE list, choose a type of number as answer
        if CURRENT_LEVEL == 1:
            self.answer = choice(NUMBER_TYPE)
        elif CURRENT_LEVEL == 2:
            self.answer = choice(NUMBER_TYPE[0:2])
        elif CURRENT_LEVEL >= 3:
            self.answer = choice(NUMBER_TYPE)

        # generate a random number from the above answer and show it in a text

        self.rect = cvs.create_text(0, 0, text=self.generate_question(self.answer, PRIME_NUMBERS), font=('Purisa', 20), fill='grey99')
        width = cvs.bbox(self.rect)[2] - cvs.bbox(self.rect)[0]
        cvs.move(self.rect, x-width, 0)

    # Generate random numbers based on chosen number type
    def generate_question(self, number_type, PRIME_NUMBERS):
        if number_type == 'positive':
            # if number is prime, skip
            random_number = randint(1, 100)
            while random_number in PRIME_NUMBERS:
                random_number = randint(1, 100)
            return random_number
        elif number_type == 'negative':
            return randint(-100, -1)
        #AK
        elif number_type == 'even':
           i = randint(-100,100)
           if i % 2 == 0:
               return i

           return i-1
        #AK
        elif number_type == 'odd':
            i = randint(-100,100)
            if i % 2 == 1:
                return i
            return i + 1

        elif number_type == 'prime':
            return choice(PRIME_NUMBERS)
        elif number_type == 'complex':
            return f'{randint(0, 100)} + {randint(0, 100)}j'


    def get_height(self):
        return self.cvs.bbox(self.rect)[3] - self.cvs.bbox(self.rect)[1]

    def get_width(self):
        return self.cvs.bbox(self.rect)[2] - self.cvs.bbox(self.rect)[0]
