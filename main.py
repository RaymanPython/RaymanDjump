from kivy.app import App
import kivy.app
from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty
)
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.core.window import Window
import random
import pickle
import time


class PongPaddle(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            #offset = (ball.center_y - self.center_y) / (self.height / 2)
            offset = 0
            bounced = Vector(vx, -1 * vy)
            vel = bounced * 1.0000001
            if vel.x == 0:
                s = 1
            else:
                s = vel.x / abs(vel.x)
            ball.velocity = vel.x + s * offset, vel.y


class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos



class PongBall1(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self, widthw):
        self.pos = (self.pos[0] - 2, self.pos[1])
        if self.pos[0] < 0 or self.pos[0] > widthw:
            self.pos[0] = widthw - 20
    def new(self, widthw, heightw):
        self.pos = (random.randint(5, 20) * widthw // 20, random.randint(5, 20) * heightw // 20)




class PongBallr(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self, widthw, heightw):
        self.pos = (self.pos[0] - 1, self.pos[1])
        if self.pos[0] < 0 or self.pos[0] > widthw:
            self.pos = (widthw, random.randint(5, 20) * heightw // 20)


class PongGame(Widget):
    ball = ObjectProperty(None)
    ball1 = ObjectProperty(None)
    ballr = ObjectProperty(None)
    player1 = ObjectProperty(None)
    djump = 0
    try:
        with open('data/score.dat', 'rb') as file:
            record = pickle.load(file)
            file.close()
    except:
        record = 0


    def serve_ball(self, vel=(0, 5)):
        self.ball.center = self.center
        self.ball.velocity = vel
        self.ball1.center = (random.randint(0, 20) * self.width//20, random.randint(0, 20) * self.height // 20)
        self.ballr.pos = (self.width, random.randint(0, 20) * self.height // 20)
        self.vel = vel
    def update(self, dt):
        self.ball.move()
        self.ballr.move(self.width, self.height)
        self.ball1.move(self.width)
        #print(self.ball1.y)

        # bounce of paddles
        self.player1.bounce_ball(self.ball)
        if self.djump > 0:
            self.ball.velocity = (self.vel[0], -self.vel[1])
            self.ball.velocity_y = -1
            if self.ball.y < 50:
                self.ball.y = 75
                self.ball.velocity_y *= -1
            self.djump -= 1
            if self.djump == 0:
                self.ball.velocity_y = -self.vel[1]


        # bounce ball off bottom or top
        #if (self.ball.y < self.y) or (self.ball.top > self.top):
            #self.ball.velocity_y *= -1

        # went of to a side to score point?
        if self.ball.x < self.x or  self.ball.x > self.width:
            self.ball.velocity_x *= -1
        if self.ball.y > self.height or self.ball.y <= 0:
            self.ball.velocity_y *= -1
        if abs(self.ball.x - self.ball1.x) < 50 and abs(self.ball.y - self.ball1.y) < 50:
            self.ball1.new(self.width,  self.height)
            self.player1.score += 1
        if abs(self.ball.x - self.ballr.x) < 50 and abs(self.ball.y - self.ballr.y) < 50:
            #self.player1.score += 1
            #PobApp().run()
            self.record = max(int(self.record), self.player1.score)
            with open('data/score.dat', 'wb') as file:
                pickle.dump(self.record, file)
                file.close()
            #App.get_running_app().stop()

            #global Rayman, sound
            #sound.stop()
            #Rayman.stop()
            self.player1.score = 0

    def on_touch_move(self, touch):
        if touch.y < self.height / 3:
            self.player1.center_x = touch.x
            self.ball.x = touch.x
        else:
            if self.ball.velocity_y < 0:
                self.ball.velocity_y *= -1
            #self.ball.pos = self.pos - Vector(*self.ball.velocity)
            #print(self.ball.velocity_y)
            if self.ball.y >= self.height:
                self.ball.y = self.height - 20
            self.djump = 5

class RaymanApp(App):
    def build(self):
        global sound
        sound = SoundLoader.load('sound/Rayman2.mp3')
        sound.play()
        sound.loop = True
        self.icon = r'image/icon.jpg'
        self.game = PongGame()
        self.game.serve_ball()
        Clock.schedule_interval(self.game.update, 1.0 / 60.0)
        return self.game

    def exit(self):
        App.get_running_app().stop()



class PobApp(App):
    def build(self):
        global soundo
        soundo = SoundLoader.load('sound/Overworld.mp3')
        soundo.play()
        soundo.loop = True
        self.icon = r'image/icon.jpg'
        try:
            with open('data/score.dat', 'rb') as file:
                record = pickle.load(file)
                file.close()
        except:
            record = 0
        layout = BoxLayout()
        img = Image(source='image/r.jpg',
                    size_hint=(1, 1),
                    pos_hint={'center_x': .5, 'center_y': 0.5})
        layout.add_widget(img)
        button = Button(text='record ' + str(record),
                        size_hint=(.5, .5),
                        pos_hint={'center_x': .5, 'center_y': .5})
        button.bind(on_press=self.callback)
        layout.add_widget(button)
        return layout

    def callback(self, items):
        #PobApp.stop(self)
        global Pob, soundo
        soundo.stop()
        Pob.stop()

def Ray():
    global Rayman
    Rayman = RaymanApp()
    Rayman.run()
    #Rayman.stop()
    main()
def main():
    Window.bind(on_keyboard=Android_back_click)
    #RaymanApp().run()
    global Pob, Rayman
    Pob = PobApp()
    Pob.run()
    del Pob
    Ray()

def Android_back_click(window,key,*largs):
    try:
        global sound, soundo, Pob, Rayman
        sound.stop()
        soundo.stop()
        Pob.stop()
        Rayman.stop()
    except:
        5
main()