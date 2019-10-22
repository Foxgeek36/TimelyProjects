#-*-coding:utf-8-*-
import random
import pygame
import time
from pygame.locals import *
import player_and_enemy1 as pyem
from imp import *
import os


enemy_list = []
guanqia = 1
is_view = False
if_boss_over = False
reload(pyem)  #重新加载模块

#关卡
def choice_tollgate(score,screen,isplay):
	'''
	score：分数，player：玩家，enemy：敌机
	根据玩家分数自动进入下一关
	一个飞机50分值
	第一关：1-3000
	第二关：3001-7000
	第三关：7001-11000
	方法返回参数：关卡,敌机列表
	'''
	pass_score_one = 100  #第一关过关分数
	pass_score_two = 700  #第二关过关分数
	pass_score_three = 1600 #第三关过关分数
	global guanqia
	global if_boss_over
	global is_view
	if score < pass_score_one :   #第一关
		if random.randint(1,100) in range(1,2):
			enemy_list.append(pyem.get_a_enemy(screen))
		guanqia = 1
		if isplay == -1:
			isplay = -1

		return guanqia,isplay,enemy_list

	elif score < pass_score_two and (not if_boss_over): #第一关boss出现
		guanqia = 1
		if isplay == -1:
			isplay = -1
		  
		if not is_view:   #判断boos是否出现
			is_view = True   #更改boss出现状态
			enemy_list.append(pyem.get_a_boss1(screen))  #增加ｂｏｓｓ对象
		print(enemy_list[len(enemy_list)-1].hp)
		if enemy_list[len(enemy_list)-1].hp <= 0 : #获取敌方ｂｏｓｓ
			if_boss_over = True

		return guanqia,isplay,enemy_list

	elif score >= pass_score_one and score < pass_score_two and if_boss_over: #第二关
		is_view = False  #更改ｂｏｓｓ出现状态
		if random.randint(1,100) in range(1,4):
			enemy_list.append(pyem.get_a_enemy(screen))
		guanqia = 2

		if isplay == -1:
			isplay = 0
	
		return guanqia,isplay,enemy_list	
	elif score <= pass_score_three and if_boss_over: #第二关ｂｏｓｓ出现
		
		if isplay == -1:
			isplay = 0
		  
		if not is_view :   #判断boos是否出现
			is_view = True  #更改boss出现状态
			enemy_list.append(pyem.get_a_boss2(screen))  #增加ｂｏｓｓ对象
		print(enemy_list[len(enemy_list)-1].hp)
		if enemy_list[len(enemy_list)-1].hp <= 0 :
			
			if_boss_over = False

		return guanqia,isplay,enemy_list

	elif score >= pass_score_two and score < pass_score_three and (not if_boss_over): #第三关
		guanqia = 2
		is_view = False
		if random.randint(1,100) in range(1,6):
			enemy_list.append(pyem.get_a_enemy(screen))
		guanqia = 3
		if isplay == -1:
			isplay = 0

		return guanqia,isplay,enemy_list

	elif score >= pass_score_three and (not if_boss_over): #第三关boss出现
		guanqia = 3
		if isplay == -1:
			isplay = 0
		  
		if not is_view :   #判断boos是否出现
			is_view = True   #更改boss出现状态
			enemy_list.append(pyem.get_a_boss3(screen))  #增加ｂｏｓｓ对象
		print(enemy_list[len(enemy_list)-1].hp)
		if enemy_list[len(enemy_list)-1].hp <= 0 :
			if_boss_over = True

		return guanqia,isplay,enemy_list

	else:
		return 4,0,[]	
	
#显示玩家飞机hp和分数
def view_hp_score(screen,hero):
	#创建游戏文字对象
	my_font = pygame.font.SysFont("simsun.ttc",20)
	game_hp = my_font.render("HP: "+ str(hero.hp),True,(255,255,255))
	if hero.hp <= 30:
		if game_hp < 0:
			game_hp = my_font.render("HP: 0",True,(255,35,0))
		else:
			game_hp = my_font.render("HP: "+ str(hero.hp),True,(255,35,0))

	game_score = my_font.render("SCORE: "+ str(hero.score),True,(255,255,255))
	game_bullet = my_font.render("BULLET: "+ str(hero.bullet_box),True,(255,255,255))
	if hero.bullet_box <= 30:
		game_bullet = my_font.render("BULLET: "+ str(hero.bullet_box),True,(255,35,0))
	game_pause = my_font.render("z : Pause",True,(255,255,255))
	game_continue = my_font.render("j : Continue",True,(255,255,255))
	game_restart = my_font.render("r : Restart",True,(255,255,255))
	game_exit = my_font.render("q: Exit",True,(255,255,255))
	screen.blit(game_hp,(20,20))	
	screen.blit(game_bullet,(20,40))
	screen.blit(game_score,(20,60))
	#－－－温馨提示-------
	screen.blit(game_pause,(150,20))	
	screen.blit(game_continue,(150,40))
	screen.blit(game_restart,(150,60))
	screen.blit(game_exit,(150,80))


#子弹样式和威力
def bullet_style(prop,player_bullet,enemy):
	'''
	prop：子弹道具
	player_bullet：玩家子弹对象
	enemy：敌机对象
	根据传入的子弹道具，改变子弹样式和子弹威力
	子弹射击样式分三种，一处子弹/两处子弹/三处子弹
	一发子弹威力为：10
	'''
	if prop == 1: #一处子弹
		player_bullet.image = pygame.image.load("")  #子弹样式
		enemy.hp -= 10
	elif prop == 2: #两处子弹
		player_bullet.image = pygame.image.load("./image/HeroBullet2.png")
		enemy.hp -= 20
	elif prop == 3:  #三处子弹
		player_bullet.image = pygame.image.load("3.jpg")
		enemy.hp -= 30

class Prop(object): #道具类
	def __init__(self,screen,image_path):
		self.x = random.randint(0,200)
		self.y = 0
		self.screen = screen
		self.image = pygame.image.load(image_path)


	#掉落道具
	def drop_prop(self):
		'''
		函数说明：每隔一分钟掉落一个道具
		screen：游戏窗口
		'''
		self.x += random.randint(-3,3)
		self.y += 2

	#展示道具
	def display(self):
		self.screen.blit(self.image,(self.x,self.y))


#读取游戏进度
def read_progress(screen,hero):
	is_exist = False
	#首先判断文件是否存在
	for file in os.listdir("./"):
		if file == "save_progress.txt":
			is_exist = True
			break
	if is_exist: #文件存在
		f = open("save_progress.txt")
		content = f.read()
		if len(content) == 0:   #避免文件内容为空，程序出错
			return ""
		content = eval(content)
		for plane in content[0:len(content) - 6]:  #循环遍历文件添加敌机


			if plane[3] == "<class 'player_and_enemy1.EnemyPlane1'>":
				plane1 = pyem.EnemyPlane1(screen)
				enemy_list.append(plane1)
				plane1.x = plane[0]
				plane1.y = plane[1]
				plane1.hp = plane[2]

			if plane[3] == "<class 'player_and_enemy1.EnemyPlane2'>":
				plane2 = pyem.EnemyPlane2(screen)
				enemy_list.append(plane2)
				plane2.x = plane[0]
				plane2.y = plane[1]
				plane2.hp = plane[2]

			if plane[3] == "<class 'player_and_enemy1.EnemyPlane3'>":
				plane3 = pyem.EnemyPlane3(screen)
				enemy_list.append(plane3)
				plane3.x = plane[0]
				plane3.y = plane[1]
				plane3.hp = plane[2]


		hero.hp = content[len(content) - 6]["hero.hp"]
		hero.score = content[len(content) - 5]["hero.score"]
		hero.bullet_box = content[len(content) -4]["hero.bullet_box"]
		hero.x = content[len(content) - 3][0]
		hero.y = content[len(content) - 3][1]
		global if_boss_over
		if_boss_over = content[len(content) - 2]["if_boss_over"]
		#加载子弹,暂时不做
		enemy_bullet_list = content[len(content) - 1]["enmey_bullet"]
		for bullet in enemy_bullet_list:
			enmeybullet = pyem.EnemyBullet(screen,0,0,0,0)
			enmeybullet.x = bullet[0]
			enmeybullet.y = bullet[1]
			pyem.enemy_bullet_list.append(enmeybullet)
			
		f.close()

if __name__ == '__main__':
	pygame.init()
	#创建游戏窗口
	screen = pygame.display.set_mode((240,550),0,32)
	#加载游戏背景图片
	background = pygame.image.load("./image/BackScr1.png")
	#加载道具
	p = Prop(screen,"./image/Goods02.png")
	enemy_list.append(p)
	while True:

		#把背景图片贴在窗口中
		screen.blit(background,(0,0))
		#p.drop_prop()
		if p.y > 600:
			p.y = 0
			p.x = random.randint(100,240)
			enemy_list = []
		
		if len(enemy_list) < 5:
			if random.randint(0,100) == 40 or random.randint(0,100) == 30:
				p = Prop(screen,"./image/Goods02.png")
				enemy_list.append(p)
		for i in enemy_list:
			i.drop_prop()
			i.display()
		
		print(p.y)
		pygame.display.update()
		time.sleep(0.02)


