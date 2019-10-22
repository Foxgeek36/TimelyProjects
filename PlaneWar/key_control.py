#-*-coding:utf-8-*-
import pygame
import time
from pygame.locals import *
import random

#初始化混音器模块
pygame.init()
pygame.mixer.init() 

#抽取一个基类
class Base(object):
	def __init__(self , screen_temp , x , y , image_path):
		self.x = x 
		self.y = y 
		self.image = pygame.image.load(image_path)
		self.screen = screen_temp

#抽取一个子弹的基类
class BaseBullet(Base):
	def __init__(self , screen_temp , x , y , image_path):
		Base.__init__(self , screen_temp , x , y , image_path)
	def display(self):
		self.screen.blit(self.image , (self.x , self.y))

#抽取飞机基类
class BasePlane(Base):
	def __init__(self , screen_temp , x , y , image_path):
		Base.__init__(self , screen_temp , x , y , image_path)
		self.bullet_list =[]  #装载子弹的列表

#定义玩家飞机的类
class HeroPlane(BasePlane):
	"""英雄飞机的类"""
	bomb_sound = pygame.mixer.Sound("explosion.mp3")
	bomb_sound.set_volume(1000)
	def __init__(self, screen_temp):
		BasePlane.__init__(self , screen_temp , 160 , 710 , "./feiji/hero1.png")
		self.hit = False 
		self.bomb_list = []
		self.__create_images()
		self.image_num = 0 
		self.image_index = 0 
	def __create_images(self):
		self.bomb_list.append(pygame.image.load("./feiji/hero_blowup_n1.png"))
		self.bomb_list.append(pygame.image.load("./feiji/hero_blowup_n2.png"))
		self.bomb_list.append(pygame.image.load("./feiji/hero_blowup_n3.png"))
		self.bomb_list.append(pygame.image.load("./feiji/hero_blowup_n4.png"))
	def she_bullet(self , enemy_temp):
		self.bullet_list.append(Bullet((self.screen) , self.x , self.y))
		self.enemy_temp = enemy_temp
	def display(self):
		#如果被击中就显示爆炸效果，如果没有就显示普通敌机效果
		if self.hit == True:
			self.screen.blit(self.bomb_list[self.image_index] , (self.x , self.y))
			self.image_num += 1
			if self.image_num == 7:
				self.image_num = 0 
				self.image_index += 1
				if self.image_index > 3:
					self.bomb_sound.play()   #音效播放
					time.sleep(1)
					exit()  #调用exit来结束游戏
		else:
			self.screen.blit(self.image , (self.x , self.y))
		#如果子弹的列表里有子弹，调用子弹的展示和移动方法
		bullet_list_remove = []  #定义一个装越界子弹的空列表
		for bullet in self.bullet_list:
			bullet.display()
			bullet.move()
			#判断有没有越界
			if bullet.judge():
				bullet_list_remove.append(bullet)
			#判断是否击中敌机
			if bullet.judge_jizhong(self.enemy_temp):
				self.enemy_temp.bomb()
		for temp in bullet_list_remove:
			self.bullet_list.remove(temp)
	def bomb(self):
		self.hit = True
	def move_left(self):  #左移
		if self.x > 0 :
			self.x -= 5
		else:
			self.x = 0
	def move_right(self):  #右移
		if self.x < 380:
			self.x += 5
		else:
			self.x = 380
	def move_up(self):   #上移
		if self.y > 0:
			self.y -= 5
		else :
			self.y = 0
	def move_down(self):   #下移
		if self.y < 710:
			self.y += 5
		else :
			self.y = 710
	def move_left_now(self):   #左闪现
		self.x = 0
	def move_right_now(self):   #右闪现
		self.x = 380
	def move_up_now(self):   #上闪现
		self.y = 0
	def move_down_now(self):   #下闪现
		self.y = 710
	
#定义一个敌机的类
class EnemyPlane(BasePlane):
	bomb_sound = pygame.mixer.Sound("explosion.mp3")
	bomb_sound.set_volume(1000)
	def __init__(self , screen_temp):
		BasePlane.__init__(self , screen_temp , random.randint(0 , 390) , random.randint(0 , 500) , "./feiji/enemy1.png")
		self.direction_x = "right"  #标识左右移动，默认向右移动
		self.direction_y = "down"
		self.hit = False 
		self.bomb_list = []
		self.__create_images()
		self.image_num = 0 
		self.image_index = 0 
	def __create_images(self):
		self.bomb_list.append(pygame.image.load("./feiji/enemy1_down1.png"))
		self.bomb_list.append(pygame.image.load("./feiji/enemy1_down2.png"))
		self.bomb_list.append(pygame.image.load("./feiji/enemy1_down3.png"))
		self.bomb_list.append(pygame.image.load("./feiji/enemy1_down4.png"))
	def she_bullet(self , hero_temp):
		self.hero_temp = hero_temp
		#加上判断，随机子弹
		random_num = random.randint(1 , 100)
		if 0 < random_num < 5:
			#添加子弹到列表中
			self.bullet_list.append(EnemyBullet(self.screen , self.x , self.y))
	def display(self):
		#如果被击中就显示爆炸效果，如果没有就显示普通敌机效果
		if self.hit == True:
			self.screen.blit(self.bomb_list[self.image_index] , (self.x , self.y))
			self.image_num += 1
			if self.image_num == 7:
				self.image_num = 0 
				self.image_index += 1
				if self.image_index > 3:
					self.bomb_sound.play()   #音效播放
					time.sleep(1)
					exit()  #调用exit来结束游戏
		else:
			self.screen.blit(self.image , (self.x , self.y))
		bullet_list_remove = []  #记录要删除的数据
		for bullet in self.bullet_list:
			bullet.display()
			bullet.move()
			#判断有没有越界
			if bullet.judge():
				bullet_list_remove.append(bullet)
			#判断是否击中敌机
			if bullet.judge_jizhong_hero(self.hero_temp):
				self.hero_temp.bomb()
		for temp in bullet_list_remove:
			self.bullet_list.remove(temp)
	def bomb(self):
		self.hit = True
	def move(self):
		#使敌机左右移动
		#对方向的判定
		if self.direction_x == "left":
			self.x -= 1
		elif self.direction_x == "right":
			self.x += 1
		if self.direction_y == "down":
			self.y += 1
		elif self.direction_y == "up":
			self.y -= 1
		#限制敌机不能出边框
		if self.x > 415 :
			self.direction_x = "left"
		elif self.x < 0 :
			self.direction_x = "right"
		if self.y > 700 :
			self.direction_y = "up"
		elif self.y < 0 :
			self.direction_y = "down"

action = "hh"   #定义全局变量，用来接收鼠标的按键功能
#控制玩具飞机
def key_control(hero_temp , enemy_temp):
	#加载音效
	shoot_sound = pygame.mixer.Sound("fazidan.mp3")
	shoot_sound.set_volume(1000)
	for event in pygame.event.get():
		#判断是否点击了退出按钮
		if event.type == QUIT:
			#退出
			print("exit")
			exit()
		#判断是否按下了键
		if event.type == KEYDOWN:
			# 获取键盘事件（上下左右按键）
			key_pressed = pygame.key.get_pressed()
			# 处理键盘事件（移动飞机的位置）
			if key_pressed[K_SPACE]:
				#上方向键
				print("space--空格")
				shoot_sound.play()  #播放音效
				hero_temp.she_bullet(enemy_temp)
			elif key_pressed[K_w] or key_pressed[K_UP]:
				print("up")
				hero_temp.move_up()
			elif key_pressed[K_s] or key_pressed[K_DOWN]:
				print("down")
				hero_temp.move_down()
			elif key_pressed[K_a] or key_pressed[K_LEFT]:
				print("left")
				hero_temp.move_left()
			elif key_pressed[K_d] or key_pressed[K_RIGHT]:
				print("right")
				hero_temp.move_right()
		elif event.type == MOUSEBUTTONDOWN:
			pressed_array = pygame.mouse.get_pressed()
			for index in range(len(pressed_array)):
				if pressed_array[index]:
					if index == 0:
						print('Pressed LEFT Button!')
						global action
						action = "LEFT"
					'''
					elif index == 1:
						print('The mouse wheel Pressed!')
						global action
						action = "WHEEL"
					elif index == 2:
						print('Pressed RIGHT Button!')
						global action
						action = "RIGHT"
					'''
		elif event.type == MOUSEMOTION:
			#return the X and Y position of the mouse cursor
			pos = pygame.mouse.get_pos()
			mouse_x = pos[0]   #获取鼠标的x坐标
			mouse_y = pos[1]   #获取鼠标的y坐标
			pygame.mouse.set_visible(False)   #鼠标指针不可见
			if action == "LEFT":
				if (0 < mouse_x < 100 ) and (0 < mouse_y < 100):   #鼠标的x和y在'继续游戏'的方框里
					break
				elif mouse_x:   #鼠标的x和y在'重新开始'的方框里
					continue
				elif mouse_x :   #鼠标的x和y在'退出游戏'的方框里
					break


			'''
			#判断是否按下了ESC键
			if event.key == K_ESCAPE:
			#退出
				print("exit")
				exit()
			#判断是否按下了a或者left键
			elif event.key == K_LEFT or event.key == K_a:
				print("left")
				hero_temp.move_left()
			#判断是否按下了d或者right键
			elif event.key == K_RIGHT or event.key == K_d:
				print("right")
				hero_temp.move_right()
			#判断是否按下了w或者up键
			elif event.key == K_UP or event.key == K_w:
				print("up")
				hero_temp.move_up()
			#判断是否按下了s或者down键
			elif event.key == K_DOWN or event.key == K_s:
				print("down")
				hero_temp.move_down()
			#判断是否按下了空格键
			elif event.key == K_SPACE:
				#上方向键
				print("space--空格")
				shoot_sound.play()  #播放音效
				hero_temp.she_bullet(enemy_temp)
			'''
	
#定义一个子弹的类
class Bullet(BaseBullet):
	'''子弹类'''
	def __init__(self , screen_temp , x , y):
		BaseBullet.__init__(self , screen_temp , x + 40 , y - 30 , "./feiji/bullet.png")
	def move(self):
		self.y -= 10
	def judge(self):
		if self.y < 0:
			return True
		else:
			return False
	def judge_jizhong(self , enemy_temp):
		#判断子弹的x坐标是否和敌机x坐标重合
		if enemy_temp.x < self.x < enemy_temp.x + 50:
			#判断子弹的y坐标是否和敌机y坐标重合
			if enemy_temp.y < self.y < enemy_temp.y + 50:
				return True		

#定义一个敌机子弹的类
class EnemyBullet(BaseBullet):
	def __init__(self , screen_temp , x , y):
		BaseBullet.__init__(self , screen_temp , x + 30 , y + 90 , "./feiji/bullet1.png")
	def move(self):
		self.y += 5
	def judge(self):
		if self.y > 840:
			return True
		else :
			return False
	def judge_jizhong_hero(self , hero_temp):
		#判断子弹的x坐标是否和敌机x坐标重合
		if hero_temp.x + 40< self.x < hero_temp.x + 60:
			#判断子弹的y坐标是否和敌机y坐标重合
			if hero_temp.y < self.y < hero_temp.y + 50:
				return True		

def main():
	#1.创建窗口
	screen = pygame.display.set_mode((480 , 840) , 0 , 32)

	#2.加载背景图片
	background = pygame.image.load("./feiji/background.png")
	
	#游戏开始图片
	start_image = pygame.image.load("./feiji/name.png")
	
	#加载玩家飞机
	hero = HeroPlane(screen)

	#创建一架敌机
	enemy = EnemyPlane(screen)
	
	#使英雄飞机可以在按键不抬起的情况下,持续移动
	pygame.key.set_repeat(True)
	#添加背景音乐
	
	pygame.mixer.music.load("赵方婧-尽头.flac")
	pygame.mixer.music.set_volume(20)
	pygame.mixer.music.play()
	
	while True:
		#把图片贴到窗口里面去
		screen.blit(background , (0 , 0))

		#把游戏开头的图片贴上来
		screen.blit(start_image , (25 , 330))

		#把玩家飞机贴到窗口去
		hero.display()

		#显示敌机
		enemy.display()
		#让敌机自由移动
		enemy.move()
		#敌机发射子弹
		enemy.she_bullet(hero)

		#根据键盘让玩家飞机移动
		key_control(hero , enemy)
		
		#更新重新绘制
		pygame.display.update()

		#时间休眠————让cpu休息
		time.sleep(0.01)

main()