#Создай собственный Шутер!

from pygame import *
from random import randint
win_width=700
win_height=500
window=display.set_mode((win_width,win_height))
display.set_caption("ZOMBI_GAME")
back=image.load('karta.jpg')
back=transform.scale(back,(win_width,win_height))
clock=time.Clock()
FPS=60

killed=0
skipped=0

class GameSprite(sprite.Sprite):
	def __init__(self, width,height,picture,x,y,speed):
		super().__init__()
		self.width = width
		self.height = height
		self.image= transform.scale(image.load(picture),(self.width,self.height)) 
		self.rect=self.image.get_rect() 
		self.rect.x=x
		self.rect.y=y
		self.speed=speed
	def reset(self):
		window.blit(self.image,(self.rect.x,self.rect.y))

class Hero(GameSprite):
	def __init__(self, width,height,picture,x,y,speed):
		super().__init__(width,height,picture,x,y,speed)
	def update(self):
		keys = key.get_pressed()
		if keys[K_LEFT] and self.rect.x>0:
			self.rect.x-=self.speed
		elif keys[K_RIGHT] and self.rect.x+self.width<win_width:
			self.rect.x+=self.speed
	def fire(self):
		global bullets
		bullet = Bullet(width=15,height=20,picture='bullet.png',x=self.rect.x+46,y=self.rect.y,speed=2)
		bullets.add(bullet)

class UFO(GameSprite):
	def __init__(self, width,height,picture,x,y,speed):
		super().__init__(width,height,picture,x,y,speed)
	def update(self):
		global skipped,text_skipped
		self.rect.y+=self.speed
		if self.rect.y >= win_height:
			skipped+=1
			text_skipped = font24.render("Пропущенно:{0}".format(skipped),True,(255,0,0))
			self.rect.y = 0
			self.rect.x = randint(0,win_width-self.width) 
class Bullet(GameSprite):
	def init(self, width,height,picture,x,y,speed):
		super().init(width,height,picture,x,y,speed)
	def update(self):
		self.rect.y-=self.speed
		if self.rect.y<0:
			self.kill()



rocket = Hero(width=70,height=70,picture="oxotnikk.png",x=325,y=430,speed=2)#  ширина и высота - по 50, скорость - 1, коорд:х=325 у=450
enemies=sprite.Group()#СОЗДАЛИ ГРУППУ ВРАГОВ

bullets=sprite.Group()

for i in range(5):
	ufo=UFO(width=50,height=50,picture="zombii.png",x=randint(0,win_width-50),y=0,speed=1)
	enemies.add(ufo)

font.init()#Подключаем шрифты
font24 = font.SysFont('Arial',40)#Задаем параметры шрифта
text_killed = font24.render("Убито:{0}".format(killed),True,(255,0,0)) 
text_skipped = font24.render("Пропущенно:{0}".format(skipped),True,(255,0,0))
text_win = font24.render("⚠Zombies⚠/n have/n entered the city⚠",True,(0,0,255))
game = 'in_process'

while True:
	if game == 'in_process':
		window.blit(back,(0,0))
		window.blit(text_killed,(0,0))
		window.blit(text_skipped,(0,30))
		enemies.draw(window)#отрисовка всех спрайтов группы
		enemies.update()#применяем .update() ко всем спрайтам в группе
		bullets.draw(window)
		bullets.update()
		rocket.reset()
		rocket.update()
		display.update()
		hits = sprite.groupcollide(bullets,enemies,True,True)
		for i in hits:
			killed+=1
			text_killed = font24.render("Убито:{0}".format(killed),True,(255,0,0)) 
			ufo=UFO(width=50,height=50,picture="zombii.png",x=randint(0,win_width-50),y=0,speed=1)
			enemies.add(ufo)
		if sprite.spritecollideany(rocket,enemies):
			game = 'fail'
		if killed >=10:
			game = 'win'
		if skipped >=10:
			game = 'fail'
	elif game == 'win':
		text_fail = font24.render("WINNER!",True,(255,0,0)) 
		window.blit(text_fail,(350,200))
		display.update()

	elif game == 'fail':
		text_win = font24.render("⚠Zombies⚠/n have/n entered the city⚠",True,(0,0,255))
		display.update()



	for i in event.get():
		if i.type == QUIT:
			quit()
		if i.type == KEYDOWN:
			if i.key == K_SPACE and game == "in_process":
				rocket.fire()
			



	clock.tick(FPS)



