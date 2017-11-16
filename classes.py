from random import *
from math import *
from tkinter import *
from time import *

class P:
    def __init__(this, x, y, name=""):
        this.x = x
        this.y = y
        this.speed = 0.5
        this.see = 70
        this.gen_way()
        this.name = name
        this.life = 5
        this.energy = 100
        this.alive = True
        this.color = "Blue"
    def gen_way(this):
        this.way = 0
    def step(this):
        this.x += this.speed * cos(this.way)
        this.y += this.speed * sin(this.way)
    def rotate(this, alpha):
        this.way += alpha
    def event(this, event):
        pass
    def death(this):
        this.alive = False
    def draw(this, canv):
        if this.alive:
            canv.create_oval(this.x - this.r, this.y - this.r, this.x + this.r, this.y + this.r, fill=this.color)
    def other(this):
        if this.life<=0:
            this.death()
    def __str__(this):
        return this.name + " " + str(this.x) + " " + str(this.y)

class Cow(P):
    def __init__(this, x, y, name=""):
        P.__init__(this, x, y, name)
        this.color = "chocolate"
        this.r = 5
        this.esc = False
    def draw(this, canv):
        P.draw(this, canv)
        if this.alive:
            canv.create_rectangle(this.x-this.life*2,this.y-this.r-10,this.x+this.life*2,this.y-this.r-5,fill="red")
    def gen_way(this):
        this.way = uniform(0.0, 2*pi)
        this.speed = uniform(0.25,0.75)
    def step(this):
        P.step(this)
        if this.x+this.speed*cos(this.way)>=1580 or this.x-this.speed*cos(this.way)<=0 or this.y+this.speed*sin(this.way)>=860 or this.y-this.speed*sin(this.way)<=0:
            this.way+=pi
            P.step(this)
            P.step(this)
    def other(this):
        P.other(this)
        if this.esc==False:
            if randint(0, 200) == 0:
                this.gen_way()
            if this.speed * cos(this.way)<=0.1 and this.speed * sin(this.way)<=0.1:
                this.r+=0.008
        if randint(0, 10) == 0 and this.r>=5 and this.life<5:
            this.life+=0.01
            this.r-=0.02
    def intersect(this, obj):
        if obj.x+obj.r>this.x-this.r and obj.x-obj.r<this.x+this.r and obj.y-obj.r<this.y+this.r and obj.y+obj.r>this.y-this.r and this.alive==True:
            this.life-=0.15
        if this.life<=0:
            if obj.life<20-5 and this.alive==True:
                obj.life+=3
            elif obj.life<20 and this.alive==True:
                obj.life=20
            if obj.energy<100-30 and this.alive==True:
                obj.energy+=30
            elif obj.energy<20 and this.alive==True:
                obj.energy=100
            this.death()
    def escape(this, obj):
        if obj.x+obj.r+this.see>this.x and obj.x-obj.r-this.see<this.x and obj.y+obj.r+this.see>this.y and obj.y-obj.r-this.see<this.y:
            this.way = atan((obj.y - this.y) / (obj.x - this.x))
            if obj.x>this.x:
                this.way+=pi
            if this.esc==False:
                this.speed=0.7
            this.esc=True
        elif obj.x+obj.r+this.see>this.x or obj.x-obj.r-this.see<this.x or obj.y+obj.r+this.see>this.y or obj.y-obj.r-this.see<this.y:
            if this.esc==True:
                this.gen_way()
                this.esc=False

class Zombie(P):
    def __init__(this, x, y, speed=0.25, name="ZOMBIE"):
        P.__init__(this, x, y, name)
        this.r = 10
        this.speed = speed
        this.color = "darkolivegreen"
        this.chs = False
        this.life = 7.5
        this.see = 100
    def gen_way(this):
        this.way = uniform(0.0, 2*pi)
        this.speed = 0.25
    def step(this):
        P.step(this)
        if this.x+this.speed*cos(this.way)>=1580 or this.x-this.speed*cos(this.way)<=0 or this.y+this.speed*sin(this.way)>=860 or this.y-this.speed*sin(this.way)<=0:
            this.way+=pi
            P.step(this)
            P.step(this)
    def other(this):
        P.other(this)
        if this.chs==False and randint(0, 200) == 0:
            this.gen_way()
    def intersect(this, obj):
        if obj.x+obj.r>this.x-this.r and obj.x-obj.r<this.x+this.r and obj.y-obj.r<this.y+this.r and obj.y+obj.r>this.y-this.r and this.alive==True:
            obj.life-=0.15
            if obj.life<=0:
                obj.death()
    def chase(this, obj):
        if obj.x+obj.r+this.see>this.x and obj.x-obj.r-this.see<this.x and obj.y+obj.r+this.see>this.y and obj.y-obj.r-this.see<this.y:
            this.way = atan((this.y - obj.y) / (this.x - obj.x))
            if this.x>obj.x:
                this.way+=pi
            if this.chs==False:
                this.speed=0.6
            this.chs=True
        elif obj.x+obj.r+this.see>this.x or obj.x-obj.r-this.see<this.x or obj.y+obj.r+this.see>this.y or obj.y-obj.r-this.see<this.y:
            if this.chs==True:
                this.gen_way()
                this.chs=False    

class Person(P):
    def __init__(this, x, y, speed=1, name="PLAYER"):
        P.__init__(this, x, y, name)
        this.life = 20
        this.energy = 100
        this.r = 10
        this.speed = speed
        this.porttime = 0
        this.portx = 0
        this.porty = 0
        this.color = "gray"
    def step(this):
        if moveP==True:
            P.step(this)
    def draw(this, canv):
        P.draw(this, canv)
        #canv.create_arc(this.x-this.r+2, this.y-this.r+2, this.x+this.r-2, this.y+this.r-2, start=-this.way*57.3-30, extent=-this.way*57.3+30, style=ARC,)
        canv.create_oval((this.x+cos(this.way)*5)-2, (this.y+sin(this.way)*5)-2, (this.x+cos(this.way))+2, (this.y+sin(this.way))+2, fill='red')
    def event(this, event):
        this.way = atan((event.y - this.y) / (event.x - this.x))
        if event.x < this.x:
            this.way += pi
    def death(this):
        global gameloop
        #s.clear()
        #gameloop=False
        root.destroy()
    def other(this):
        global moveP
        P.other(this)
        if this.porttime>0:
            canv.create_oval(this.x-this.r-this.porttime*0.5, this.y-this.r-this.porttime*0.5, this.x+this.r+this.porttime*0.5, this.y+this.r+this.porttime*0.5, outline='white')
            this.porttime-=0.5
            if this.porttime<=0:
                this.x=this.portx
                this.y=this.porty
                this.speed=1
                moveP=False

class Bullet(P):
    def __init__(this):
        P.__init__(this, 0, 0, '')
        this.speed = 6
        this.r = 3
        this.life = 8
        this.color = 'gold'
        this.alive = False
    def step(this):
        if this.alive == True:
            P.step(this)
            this.life-=0.2
            if this.life<=0:
                this.death()
    def death(this):
        this.alive = False
    def shot(this, obj, x, y):
        this.x = obj.x
        this.y = obj.y
        this.way = atan((y - this.y) / (x - this.x))
        if x<obj.x:
            this.way+=pi
        this.life = 5
        this.alive = True
    def intersect(this, obj):
        if obj.x+obj.r>this.x-this.r and obj.x-obj.r<this.x+this.r and obj.y-obj.r<this.y+this.r and obj.y+obj.r>this.y-this.r and this.alive==True:
            this.life=0
            obj.life-=2.6
            this.death()
    def other(this):
        P.other(this)


def gamerhp(this):
    canv.create_rectangle(10, 10, 10 + this.life*5, 30, fill='red', outline='')
    canv.create_rectangle(10, 10, 110, 30)
    canv.create_text(95, 20, text = str(ceil(this.life*5))+'/100', font='Verdana 12', anchor='e')
    canv.create_rectangle(10, 40, 10 + this.energy, 60, fill='blue', outline='')
    canv.create_rectangle(10, 40, 110, 60)
    canv.create_text(95, 50, text = str(this.energy)+'/100', font='Verdana 12', anchor='e')


def tick():
    global s, canv
    canv.delete("all")
    for obj in s:
        obj.step()
        obj.draw(canv)
        obj.other()
    for obj in s[0:15]:
        obj.intersect(s[15])
        obj.escape(s[15])
        for i in b:
            i.intersect(obj)
    for obj in s[16:21]:
        obj.intersect(s[15])
        for i in b:
            i.intersect(obj)
        obj.chase(s[15])
    for obj in b:
        obj.step()
        obj.draw(canv)
        obj.other()
    gamerhp(s[15])

def mouseMove(event):
    for obj in s:
        obj.event(event)

def click(event):
    if s[15].energy>5:
        if b[0].alive==False:
            b[0].shot(s[15], event.x, event.y)
            s[15].energy-=5
        elif b[1].alive==False:
            b[1].shot(s[15], event.x, event.y)
            s[15].energy-=5
        elif b[2].alive==False:
            b[2].shot(s[15], event.x, event.y)
            s[15].energy-=5
        elif b[3].alive==False:
            b[4].shot(s[15], event.x, event.y)
            s[15].energy-=5

def click2(event):
    if s[15].energy>20:
        s[15].speed = 0
        s[15].portx = event.x
        s[15].porty = event.y
        s[15].porttime = 40
        s[15].energy-=20 

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
#m.add_cascade(label="Р Р°Р·СЂРµС€РµРЅРёРµ",menu=fm)
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
    s.append(Cow(randint(0,1580), randint(0,860)))
s.append(Person(250, 250))
for i in range(5):
    s.append(Zombie(randint(0,1580), randint(0,860)))
for i in range(4):
    b.append(Bullet())
gameloop = False
moveP = False
ticktime = 0.01
gameinit()
next = time() + ticktime
while gameloop:
    while time() < next:
        pass
    next = time() + ticktime
    tick()
    canv.update()

canv.create_text(0,0,text='GAME OVER', font='Verdana 72')
