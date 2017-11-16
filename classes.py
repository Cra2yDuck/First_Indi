from tkinter import *
import random
import math
import time


class P:
    def __init__(self, x, y, name=""):
        self.x = x
        self.y = y
        self.speed = 0.5
        self.see = 70
        self.gen_way()
        self.name = name
        self.life = 5
        self.energy = 100
        self.alive = True
        self.color = "Blue"

    def gen_way(self):
        self.way = 0

    def step(self):
        self.x += self.speed * math.cos(self.way)
        self.y += self.speed * math.sin(self.way)

    def rotate(self, alpha):
        self.way += alpha

    def event(self, event):
        pass

    def death(self):
        self.alive = False

    def draw(self, canv):
        if self.alive:
            canv.create_oval(self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r, fill=self.color)

    def other(self):
        if self.life <= 0:
            self.death()

    def __str__(self):
        return self.name + " " + str(self.x) + " " + str(self.y)


class Cow(P):
    def __init__(self, x, y, name=""):
        P.__init__(self, x, y, name)
        self.color = "chocolate"
        self.r = 5
        self.esc = False

    def draw(self, canv):
        P.draw(self, canv)
        if self.alive:
            canv.create_rectangle(self.x-self.life*2,self.y-self.r-10,self.x+self.life*2,self.y-self.r-5,fill="red")

    def gen_way(self):
        self.way = random.uniform(0.0, 2 * math.pi)
        self.speed = random.uniform(0.25, 0.75)

    def step(self):
        P.step(self)
        if self.x + self.speed * math.cos(self.way) >= 1580 or self.x - self.speed * math.cos(self.way) <= 0 or \
           self.y + self.speed * math.sin(self.way) >= 860 or self.y - self.speed * math.sin(self.way) <= 0:
            self.way += math.pi
            P.step(self)
            P.step(self)

    def other(self):
        P.other(self)
        if not self.esc:
            if random.randint(0, 200) == 0:
                self.gen_way()
            if self.speed * math.cos(self.way) <= 0.1 and self.speed * math.sin(self.way) <= 0.1:
                self.r += 0.008
        if random.randint(0, 10) == 0 and self.r >= 5 and self.life < 5:
            self.life += 0.01
            self.r -= 0.02

    def intersect(self, obj):
        if obj.x+obj.r>self.x-self.r and obj.x-obj.r<self.x+self.r and obj.y-obj.r<self.y+self.r and obj.y+obj.r>self.y-self.r and self.alive==True:
            self.life-=0.15
        if self.life<=0:
            if obj.life<20-5 and self.alive==True:
                obj.life+=3
            elif obj.life<20 and self.alive==True:
                obj.life=20
            if obj.energy<100-30 and self.alive==True:
                obj.energy+=30
            elif obj.energy<20 and self.alive==True:
                obj.energy=100
            self.death()

    def escape(self, obj):
        if obj.x + obj.r + self.see > self.x and obj.x -obj.r -self.see < self.x and \
           obj.y + obj.r + self.see > self.y and obj.y -obj.r -self.see < self.y:
            self.way = math.atan((obj.y - self.y) / (obj.x - self.x))
            if obj.x > self.x:
                self.way += math.pi
            if not self.esc:
                self.speed = 0.7
            self.esc=True
        elif obj.x+obj.r+self.see>self.x or obj.x-obj.r-self.see<self.x or obj.y+obj.r+self.see>self.y or obj.y-obj.r-self.see<self.y:
            if self.esc:
                self.gen_way()
                self.esc = False


class Zombie(P):
    def __init__(self, x, y, speed=0.25, name="ZOMBIE"):
        P.__init__(self, x, y, name)
        self.r = 10
        self.speed = speed
        self.color = "darkolivegreen"
        self.chs = False
        self.life = 7.5
        self.see = 100

    def gen_way(self):
        self.way = random.uniform(0.0, 2 * math.pi)
        self.speed = 0.25

    def step(self):
        P.step(self)
        if self.x + self.speed * math.cos(self.way) >= 1580 or self.x - self.speed * math.cos(self.way) <= 0 or \
           self.y + self.speed * math.sin(self.way) >= 860 or self.y - self.speed * math.sin(self.way) <= 0:
            self.way += math.pi
            P.step(self)
            P.step(self)

    def other(self):
        P.other(self)
        if not self.chs and random.randint(0, 200) == 0:
            self.gen_way()

    def intersect(self, obj):
        if obj.x+obj.r>self.x-self.r and obj.x-obj.r<self.x+self.r and obj.y-obj.r<self.y+self.r and obj.y+obj.r>self.y-self.r and self.alive==True:
            obj.life-=0.15
            if obj.life<=0:
                obj.death()

    def chase(self, obj):
        if obj.x+obj.r+self.see>self.x and obj.x-obj.r-self.see<self.x and obj.y+obj.r+self.see>self.y and obj.y-obj.r-self.see<self.y:
            self.way = math.atan((self.y - obj.y) / (self.x - obj.x))
            if self.x > obj.x:
                self.way += math.pi
            if not self.chs:
                self.speed = 0.6
            self.chs=True
        elif obj.x+obj.r+self.see>self.x or obj.x-obj.r-self.see<self.x or obj.y+obj.r+self.see>self.y or obj.y-obj.r-self.see<self.y:
            if self.chs:
                self.gen_way()
                self.chs = False


class Person(P):
    def __init__(self, x, y, speed=1, name="PLAYER"):
        P.__init__(self, x, y, name)
        self.life = 20
        self.energy = 100
        self.r = 10
        self.speed = speed
        self.porttime = 0
        self.portx = 0
        self.porty = 0
        self.color = "gray"

    def step(self):
        if moveP==True:
            P.step(self)

    def draw(self, canv):
        P.draw(self, canv)
        #canv.create_arc(self.x-self.r+2, self.y-self.r+2, self.x+self.r-2, self.y+self.r-2, start=-self.way*57.3-30, extent=-self.way*57.3+30, style=ARC,)
        canv.create_oval((self.x + math.cos(self.way)*5) - 2,
                         (self.y + math.sin(self.way)*5) - 2,
                         (self.x + math.cos(self.way))+2,
                         (self.y + math.sin(self.way))+2, fill='red')

    def event(self, event):
        self.way = math.atan((event.y - self.y) / (event.x - self.x))
        if event.x < self.x:
            self.way += math.pi

    def death(self):
        global gameloop
        #s.clear()
        #gameloop=False
        root.destroy()

    def other(self):
        global moveP
        P.other(self)
        if self.porttime>0:
            canv.create_oval(self.x-self.r-self.porttime*0.5, self.y-self.r-self.porttime*0.5, self.x+self.r+self.porttime*0.5, self.y+self.r+self.porttime*0.5, outline='white')
            self.porttime-=0.5
            if self.porttime<=0:
                self.x=self.portx
                self.y=self.porty
                self.speed=1
                moveP=False


class Bullet(P):
    def __init__(self):
        P.__init__(self, 0, 0, '')
        self.speed = 6
        self.r = 3
        self.life = 8
        self.color = 'gold'
        self.alive = False

    def step(self):
        if self.alive == True:
            P.step(self)
            self.life-=0.2
            if self.life<=0:
                self.death()

    def death(self):
        self.alive = False

    def shot(self, obj, x, y):
        self.x = obj.x
        self.y = obj.y
        self.way = math.atan((y - self.y) / (x - self.x))
        if x<obj.x:
            self.way += math.pi
        self.life = 5
        self.alive = True

    def intersect(self, obj):
        if obj.x+obj.r>self.x-self.r and obj.x-obj.r<self.x+self.r and obj.y-obj.r<self.y+self.r and obj.y+obj.r>self.y-self.r and self.alive==True:
            self.life = 0
            obj.life -= 2.6
            self.death()

    def other(self):
        P.other(self)


def gamerhp(self):
    canv.create_rectangle(10, 10, 10 + self.life*5, 30, fill='red', outline='')
    canv.create_rectangle(10, 10, 110, 30)
    canv.create_text(95, 20, text=str(math.ceil(self.life*5))+'/100', font='Verdana 12', anchor='e')
    canv.create_rectangle(10, 40, 10 + self.energy, 60, fill='blue', outline='')
    canv.create_rectangle(10, 40, 110, 60)
    canv.create_text(95, 50, text=str(self.energy)+'/100', font='Verdana 12', anchor='e')


def tick():
    global s, canv
    canv.delete("all")
    for obj in s:
        obj.step()
        obj.draw(canv)
        obj.other()
    for obj in s:
        if Cow == type(obj):
            obj.intersect(global_person)
            obj.escape(global_person)
            for i in b:
                i.intersect(obj)
        elif Zombie == type(obj):
            obj.intersect(global_person)
            for i in b:
                i.intersect(obj)
            obj.chase(global_person)
    for obj in b:
        obj.step()
        obj.draw(canv)
        obj.other()
    gamerhp(global_person)


def mouseMove(event):
    for obj in s:
        obj.event(event)


def click(event):
    if global_person.energy>=5:
        if b[0].alive==False:
            b[0].shot(global_person, event.x, event.y)
            global_person.energy-=5
        elif b[1].alive==False:
            b[1].shot(global_person, event.x, event.y)
            global_person.energy-=5
        elif b[2].alive==False:
            b[2].shot(global_person, event.x, event.y)
            global_person.energy-=5
        elif b[3].alive==False:
            b[4].shot(global_person, event.x, event.y)
            global_person.energy-=5


def click2(event):
    if global_person.energy>20:
        global_person.speed = 0
        global_person.portx = event.x
        global_person.porty = event.y
        global_person.porttime = 40
        global_person.energy-=20 


def click3(event):
    global moveP
    moveP=True


def release3(event):
    global moveP
    moveP=False


def Key(event):
    global gameloop
    if event.keysym=='Escape':
        gameloop=False


def gameinit():
    global gameloop
    gameloop=True


root=Tk()
canv=Canvas(root,width=1580,height=860,bg='darkgreen')
canv.pack()
#m = Menu(root)
#root.config(menu=m)
#fm = Menu(m)
#m.add_cascade(label="Р Р°Р·СЂРµС€РµРЅРёРµ",menu=fm)
#fm.add_command(label="320 x 200",command=display1)
#fm.add_command(label="320 x 240",command=display2)
#fm.add_command(label="640 x 480",command=display3)
#fm.add_command(label="720 x 480",command=display4)
#fm.add_command(label="768 x 576",command=display5)
#fm.add_command(label="800 x 480",command=display6)
#fm.add_command(label="800 x 600",command=display7)
#fm.add_command(label="1024 x 600",command=display8)
#fm.add_command(label="1024 x 768",command=display9)
#fm.add_command(label="1152 x 864",command=display10)
#fm.add_command(label="1280 x 720",command=display11)
#fm.add_command(label="1280 x 768",command=display12)
#fm.add_command(label="1280 x 800",command=display13)
#fm.add_command(label="1280 x 960",command=display14)
#fm.add_command(label="1280 x 1024",command=display15)
#fm.add_command(label="1400 x 1050",command=display16)
#fm.add_command(label="1440 x 900",command=display17)
#fm.add_command(label="1440 x 960",command=display18)
#fm.add_command(label="1600 x 900",command=displaypre19)
#fm.add_command(label="1600 x 1200",command=display19)
#fm.add_command(label="1680 x 1050",command=display20)
#fm.add_command(label="1920 x 1080",command=display21)
#fm.add_command(label="1920 x 1200",command=display22)
#fm.add_command(label="2048 x 1536",command=display23)
#fm.add_command(label="2560 x 1600",command=display24)
#fm.add_command(label="2560 x 2048",command=display25)
root.bind("<B3-Motion>", mouseMove)
root.bind('<Button-1>', click)
root.bind('<Button-2>', click2)
root.bind('<Button-3>', click3)
root.bind('<ButtonRelease-3>', release3)

s = []
b = []
for i in range(15):
    s.append(Cow(random.randint(0,1580), random.randint(0,860)))
s.append(Person(250, 250))
global_person = s[-1]
for i in range(5):
    s.append(Zombie(random.randint(0,1580), random.randint(0,860)))
for i in range(4):
    b.append(Bullet())
gameloop = False
moveP = False
ticktime = 0.01
gameinit()
next = time.time() + ticktime
while gameloop:
    while time.time() < next:
        pass
    next = time.time() + ticktime
    tick()
    canv.update()

canv.create_text(0, 0, text='GAME OVER', font='Verdana 72')
