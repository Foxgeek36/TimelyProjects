#-*-coding:utf-8-*-
import sysdeloy
import pygame
import time
import picture_attribute as pa
import player_and_enemy1 as pyem
from pygame.locals import *
from imp import *
import os

#重新加载模块
reload(pyem)  
reload(sysdeloy)

if_first_pause = False  #是否第一次暂停

def updateback(guanqia,isplay):
	#根据关卡播放背景音乐
	if guanqia == 1:
		if isplay == 0:
			pygame.mixer.music.load("./sound/bgmusic/bgm_zhandou1.mp3")
			isplay = -1 
			pygame.mixer.music.play(10)

	if guanqia == 2:
		if isplay == 0:
			pygame.mixer.music.load("./sound/bgmusic/bgm_zhandou2.mp3")
			isplay = -2 
			pygame.mixer.music.play(10)

	if guanqia == 3:
		if isplay == -2:
			pygame.mixer.music.load("./sound/bgmusic/bgm_zhandou3.mp3")
			isplay = -3 
			pygame.mixer.music.play(10)
			
	return isplay


def save_game(hero_temp):
	#背景图开始归零时，系统自动保存进度
	f = open("save_progress.txt","w")
	content = [] 
	for enemy in sysdeloy.enemy_list:  #保存游戏敌方
		content.append([enemy.x,enemy.y,enemy.ini_hp,str(enemy.__class__)])
	content.append({"hero.hp":hero_temp.hp})  #保存玩家血量
	content.append({"hero.score":hero_temp.score})  #保存玩家分数
	content.append({"hero.bullet_box": hero_temp.bullet_box})  #保存玩家子弹
	content.append([hero_temp.x,hero.y])  #保存玩家坐标
	content.append({"if_boss_over":sysdeloy.if_boss_over})
	#存档子弹
	bullet_list = []
	if len(pyem.enemy_bullet_list) > 0:
		for bullet in pyem.enemy_bullet_list:
			bullet_list.append([bullet.x,bullet.y])
	content.append({"enmey_bullet":bullet_list})
	f.write(str(content))
	f.close()

'''鼠标控制'''
mouse_x = 0
mouse_y = 0
'''结束'''
def key_control(screen,hero_temp,num):
	global if_first_pause
	for event in pygame.event.get():
		if event.type == QUIT:
			save_game(hero_temp)
			exit()
		pressed_keys = pygame.key.get_pressed()
		if pressed_keys[K_q] or pressed_keys[K_ESCAPE]:
			save_game(hero_temp)
			exit()
		if pressed_keys[K_LEFT]:
			pyem.player_move_left(hero_temp)
		elif pressed_keys[K_RIGHT]:
			pyem.player_move_right(hero_temp)
		elif pressed_keys[K_DOWN]:
			pyem.player_move_down(hero_temp)
		elif pressed_keys[K_UP]:
			pyem.player_move_up(hero_temp)
		elif pressed_keys[K_SPACE]:
			pyem.player_fire_bullet(hero_temp)
			
		if pressed_keys[K_z]:   #暂停游戏
			hero_temp.move_flag = 0
			num = 1
		elif pressed_keys[K_j]:   #继续游戏
			if if_first_pause:
				hero_temp.move_flag = 1
				num = 2
			else:
				sysdeloy.read_progress(screen,hero_temp)
				if_first_pause = True

		elif pressed_keys[K_r]:  #重新开始
			if if_first_pause:
				hero_temp.move_flag = 1
				num = 3
			else:
				f = open("save_progress.txt","w")
				f.write("")
				f.close()
				hero_temp.move_flag = 1
				num = 3
		'''鼠标控制开始'''
		if event.type == MOUSEMOTION:
			#return the X and Y position of the mouse cursor
			pos = pygame.mouse.get_pos()
			global mouse_x
			global mouse_y
			mouse_x = pos[0]   #获取鼠标的x坐标
			mouse_y = pos[1]   #获取鼠标的y坐标
			#print(mouse_x)
			#print(mouse_y)
			#pygame.mouse.set_visible(False)   #鼠标指针不可见
		if event.type == MOUSEBUTTONDOWN:
			pressed_array = pygame.mouse.get_pressed()
			for index in range(len(pressed_array)):
				if pressed_array[index]:
					if index == 0:
						print('Pressed LEFT Button!')
						if (96 < mouse_x < 144) and (245 < mouse_y < 258):   #鼠标的x和y在'继续游戏'的方框里
							print("游戏继续")
							num = 2
						elif (96 < mouse_x < 144) and (270 < mouse_y < 283):   #鼠标的x和y在'重新开始'的方框里
							print("重新开始")
							num = 3
						elif (96 < mouse_x < 144) and (295 < mouse_y < 308) :   #鼠标的x和y在'退出游戏'的方框里
							print("退出游戏")
							exit()
			hero_temp.move_flag = 1
	
	'''结束'''
	return num




if __name__ == '__main__':
	

	pygame.init()
	#设置键盘重复键
	pygame.key.set_repeat(True)
	#初始化游戏窗口
	screen = pygame.display.set_mode((240,550),0,32)
	#初始化第一关背景图片
	background = pygame.image.load(pa.get_backscreen1_image())
	#初始化第二关背景图片
	background2 = pygame.image.load(pa.get_backscreen2_image())
	#初始化第三关背景图片
	background3 = pygame.image.load(pa.get_backscreen3_image())
	#初始化背景音乐
	pygame.mixer.init() 
	pygame.mixer.music.set_volume(100)

	#初始化玩家
	hero = pyem.HeroPlane(screen)
	

	i = 0 
	prop_time = 0 #初始化道具时间
	#初始化玩家分数
	score = 0
	#声明子弹道具对象
	prop = pyem.get_a_property(screen)

	isplay = 0	#默认背景音乐没有播放

	__gamestate = 0 #游戏状态:0正常状态,1:暂停游戏，２：重新开始
	guanqia = 1 #初始化关卡

	__ispause = False #判断系统是否暂停

	sysdeloy.read_progress(screen,hero)
	__gamestate = 1

	while True:	
		if __gamestate == 0:  #游戏正常
			
			__ispause = False
			#根据关卡设置敌机数量
			guanqia,isplay,enemy_list = sysdeloy.choice_tollgate(hero.score,screen,isplay)
			isplay = updateback(guanqia,isplay)
			if guanqia == 1:
				#将背景图片贴到游戏窗口中
				screen.blit(background,(0,i))
			elif guanqia == 2:
				#将背景图片贴到游戏窗口中
				screen.blit(background2,(0,i))
			elif guanqia == 3:
				#将背景图片贴到游戏窗口中
				screen.blit(background3,(0,i))
			#显示玩家血量和分数
			sysdeloy.view_hp_score(screen,hero)

			
			if guanqia == 4:
				print("你已经通关了")
				screen.blit(background3,(0,i))
		
			#获取敌机数量
			for enemy in sysdeloy.enemy_list:

				#移除越界敌方飞机
				if not pyem.enemy_item_judge(enemy):
					sysdeloy.enemy_list.remove(enemy)
			
				pyem.enemy_item_display(enemy,hero)
				pyem.hero_bullet_judge_hit(enemy)
				pyem.judge_pengzhuang(hero,enemy)
			__gamestate = key_control(screen,hero,__gamestate)

			pyem.hero_item_display(hero)
			pyem.hero_bullet_display()
			pyem.enemy_bullet_display()
			pyem.enemy_bullet_judge_hit(hero)

		
			if prop_time == 200:
				prop =  pyem.get_a_property(screen)
			if prop_time > 200 :
				pyem.property_display(prop,hero)
			if prop_time == 500:
				prop =  pyem.get_hp_property(screen)
			if prop_time > 500 :
				pyem.property_display(prop,hero)
			if prop_time == 800:
				prop_time = 0
			#重新绘制游戏窗口
			pygame.display.update()
			if pyem.bomb_flag == 1:
				__gamestate = 4
			time.sleep(0.02)
			while i < -1450: #判断背景图片是否超出，如果超出从０开始
				i = 0
			i -= 1
			prop_time += 1

		elif __gamestate == 1: #暂停游戏
			background4 = pygame.image.load(pa.get_pause_image())
			screen.blit(background4,(0,200))
			__gamestate = key_control(screen,hero,__gamestate)
			#重新绘制游戏窗口
			pygame.display.update()
			__ispause = True
			

		elif __gamestate == 2:  #继续游戏
			__gamestate = 0

		elif __gamestate == 3 and __ispause: #重新开始
			if __ispause:
				#初始化系统
				i = 0
				__gamestate = 0
				guanqia = 1
				prop_time = 0
				sysdeloy.enemy_list = []
				sysdeloy.is_view = False
				sysdeloy.if_boss_over = False
				hero.hp = hero.init_hp
				hero.bullet_box = 100
				hero.score = 0
				hero.x = 100
				hero.y = 550 - hero.height
				pyem.enemy_bullet_list = []
				pyem.hero_bullet_list = []
				#初始化第一关背景图片
				background = pygame.image.load(pa.get_backscreen1_image())
				screen.blit(background,(0,0))
				pygame.display.update()
		elif __gamestate == 3 and (not __ispause):
			__gamestate = 0

		elif __gamestate == 4: #游戏结束
			background4 = pygame.image.load("./image/gameover.png")
			screen.blit(background4,(-5,195))
			__gamestate = key_control(screen,hero,__gamestate)
			#重新绘制游戏窗口
			pygame.display.update()
			pyem.bomb_flag = 0
			__ispause = True



