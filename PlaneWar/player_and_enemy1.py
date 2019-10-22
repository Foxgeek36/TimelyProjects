#-*-coding:utf-8-*-
from picture_attribute import *#引入图片属性模块，包含图片地址和宽高
from pygame.locals import *
import pygame
import random
import time
hero_bullet_list = []	
enemy_bullet_list = []	
hero_score = 0
bomb_flag = 0
#定义玩家飞机类
class Base(object):
	def __init__(self, screen):
		super(Base, self).__init__()
		self.screen = screen
		self.image = pygame.image.load(self.file_address)

class Plane(Base):
	def __init__(self, screen):
		self.bomb_image_list = []
		self.image_index = 0
		super(Plane, self).__init__(screen)

	def get_image(self):
		get_planeboom1_image(self)
		self.bomb_image_list.append(pygame.image.load(self.file_address))		
		get_planeboom2_image(self)
		self.bomb_image_list.append(pygame.image.load(self.file_address))		
		get_planeboom3_image(self)
		self.bomb_image_list.append(pygame.image.load(self.file_address))		
		get_planeboom4_image(self)
		self.bomb_image_list.append(pygame.image.load(self.file_address))		
		get_planeboom5_image(self) 
		self.bomb_image_list.append(pygame.image.load(self.file_address))		
		get_planeboom6_image(self)
		self.bomb_image_list.append(pygame.image.load(self.file_address))

	def bomb(self):
		if self.hp <= 0:
			return True
		else:
			return False

	def lose_hp(self):#一次掉血掉10hp
		self.hp -= 10							

class HeroPlane(Plane):
	def __init__(self,screen):
		get_hero_image(self)
		super(HeroPlane, self).__init__(screen)
		self.init_hp = 100
		self.get_image()
		self.x = 100
		self.y = 550 - self.height#此处窗口高度未知，小组讨论直接定下来,设置一个窗口高度全局变量
		self.hp = self.init_hp
		self.bullet_box = 100
		self.image_num = 0
		self.score = 0
		self.move_flag = 1
		

	def move_left(self):
		if self.x < 0 or self.move_flag == 0:
			pass
		else:
			self.x -= 4

	def move_right(self):
		if self.x > 240 - self.width or self.move_flag == 0:#需要窗口宽度全局变量
				pass
		else:
			self.x += 4

	def move_up(self) :
		if self.y < 0 or self.move_flag == 0:
			pass
		else:
			self.y -= 4	

	def move_down(self):
		if self.y > 550 - self.height or self.move_flag == 0:#需要窗口高度全局变量
			pass
		else:
			self.y += 4

	def fire(self):
		if self.bullet_box > 0:
			bullet_item = HeroBullet(self.screen, self.width, self.x, self.y)
			hero_bullet_list.append(bullet_item)
			self.bullet_box -= 1	
		else:
			pass

	def display(self):
		if self.bomb():
			self.move_flag = 0
			self.screen.blit(self.bomb_image_list[self.image_index], (self.x, self.y))
			self.image_num+=1
			if self.image_num == 7:
				self.image_num=0			
				self.image_index += 1
				if self.image_index > 5:
					global bomb_flag

					self.image_index = 5
					# exit()#炸完了咋样？待讨论
					bomb_flag = 1
		else:
			self.screen.blit(self.image, (self.x, self.y))

	def judge_pengzhuang(self, enemy_item):
		#if (self.x > enemy_item.x) and (self.x < enemy_item.x + enemy_item.width - self.width) and (self.y > enemy_item.y) and (self.y < enemy_item.y - self.height + enemy_item.height):
		if (enemy_item.x in range(self.x-20 , self.x + self.width - enemy_item.width + 20) and enemy_item.y in range(self.y - 20,self.y + self.height - enemy_item.height +20)) or (self.x in range(enemy_item.x-20 , enemy_item.x + enemy_item.width - self.width + 20) and self.y in range(enemy_item.y-20,enemy_item.y + enemy_item.height - self.height + 20)):
			self.hp -= 100
			if self.hp < 0:
				self.hp = 0
			#一打中子弹就挪到屏幕外
			return True
		else:
			return False	
					



class EnemyPlane(Plane):
	def __init__(self,screen):
		super(EnemyPlane, self).__init__(screen)
		self.get_image()
		self.y = 0
		self.x = random.randint(0, 240-self.width)


	#判断敌机是否在屏幕内，在返回true
	def judge(self):
		if self.y <= 550:
			return True
		else :
			return False
	def move(self):
		self.y += 2

	def display(self, hero_item):
		if self.judge():#在屏幕内的才显示
			if self.bomb():
				self.screen.blit(self.bomb_image_list[self.image_index], (self.x, self.y))
				self.image_index += 1
				if self.image_index > 5:
					hero_item.score += self.ini_hp
					self.image_index = 0
					self.y = 551#炸完了挪出屏幕
			else:
				self.screen.blit(self.image, (self.x, self.y))
				self.move()
				if random.randint(0,50) == 1 :
					bullet_item = EnemyBullet(self.screen, self.width, self.height, self.x, self.y)
					enemy_bullet_list.append(bullet_item)				



class EnemyPlane1(EnemyPlane):#定义第一类敌机
	def __init__(self,screen):
		self.hp = 20
		self.ini_hp = 20
		get_enemy1_image(self)
		super(EnemyPlane1, self).__init__(screen)


class EnemyPlane2(EnemyPlane):#定义第二类敌机
	def __init__(self,screen):
		self.hp = 10
		self.ini_hp = 10
		get_enemy2_image(self)
		super(EnemyPlane2, self).__init__(screen)

class EnemyPlane3(EnemyPlane):#定义第三类敌机
	def __init__(self,screen):
		self.hp = 30
		self.ini_hp = 30
		get_enemy3_image(self)
		super(EnemyPlane3, self).__init__(screen)

class EnemyBoss(EnemyPlane):#定义敌机boss
	def __init__(self, screen):
		super(EnemyBoss, self).__init__(screen)
		self.direction = "right"
		self.image_num=0				

	def get_image(self):
		get_bossboom1_image(self)
		self.bomb_image_list.append(pygame.image.load(self.file_address))		
		get_bossboom2_image(self)
		self.bomb_image_list.append(pygame.image.load(self.file_address))		
		get_bossboom3_image(self)
		self.bomb_image_list.append(pygame.image.load(self.file_address))		
		get_bossboom4_image(self)
		self.bomb_image_list.append(pygame.image.load(self.file_address))		
		get_bossboom5_image(self) 
		self.bomb_image_list.append(pygame.image.load(self.file_address))		
		get_bossboom6_image(self)
		self.bomb_image_list.append(pygame.image.load(self.file_address))
				
	def move(self):
		if self.direction == "right" :
			self.x += 2
		elif self.direction == "left":
			self.x -= 2
		if self.x > 240 - self.width :
			self.direction = "left"
		elif self.x < 0 :
			self.direction = "right"			

	def display(self, hero_item):
		if self.judge():#在屏幕内的才显示
			if self.bomb():
				self.screen.blit(self.bomb_image_list[self.image_index], (self.x, self.y))
				self.image_num+=1
				if self.image_num == 7:
					self.image_num=0				
					self.image_index += 1
					if self.image_index > 5:
						hero_item.score += self.ini_hp
						self.image_index = 0
						self.y = 551#炸完了挪出屏幕
						#exit()
			else:
				self.screen.blit(self.image, (self.x, self.y))
				self.move()
				if random.randint(0,50) == 1 :
					bullet_item1 = BossBulletLeft(self.screen, self.width, self.height, self.x, self.y)
					enemy_bullet_list.append(bullet_item1)				
					bullet_item2 = BossBulletRight(self.screen, self.width, self.height, self.x, self.y)
					enemy_bullet_list.append(bullet_item2)	

class EnemyBoss1(EnemyBoss):#定义第一类boss
	def __init__(self,screen):
		self.hp = 300
		self.ini_hp = 300
		get_enemyboss1_image(self)
		super(EnemyBoss1, self).__init__(screen)
		print(self.width)

class EnemyBoss2(EnemyBoss):#定义第er类boss
	def __init__(self,screen):
		self.hp = 600
		self.ini_hp = 600
		get_enemyboss2_image(self)
		super(EnemyBoss2, self).__init__(screen)

class EnemyBoss3(EnemyBoss):#定义第san类boss
	def __init__(self,screen):
		self.hp = 900
		self.ini_hp = 900
		get_enemyboss3_image(self)
		super(EnemyBoss3, self).__init__(screen)

								

class HeroBullet(Base):
	def __init__(self, screen, plane_width, plane_x, plane_y):
		get_herobullet1_image(self)
		super(HeroBullet, self).__init__(screen)
		self.x = plane_x+plane_width/2 - self.width/2
		self.y = plane_y - self.height
	#子弹移动
	def move(self):
		self.y -= 5

	#判断子弹是否越界
	def judge(self):
		if self.y < 0:
			return True
		else :
			return False
	#判断是否打中敌机
	def judge_hit(self, enemy_item):
		#if (self.x > enemy_item.x) and (self.x < enemy_item.x + enemy_item.width - self.width) and (self.y > enemy_item.y) and (self.y < enemy_item.y - self.height + enemy_item.height):
		if self.x in range(enemy_item.x - self.width, enemy_item.x + enemy_item.width) and self.y in range(enemy_item.y,enemy_item.y + enemy_item.height):
			self.x = -self.width
			#一打中子弹就挪到屏幕外
			enemy_item.lose_hp()#打中直接敌机掉血
			return True
		else:
			return False	

	

class EnemyBullet(Base):#定义敌机子弹

	def __init__(self, screen, plane_width, plane_height, plane_x, plane_y):
		get_enemybullet1_image(self)
		super(EnemyBullet, self).__init__(screen)
		self.x = plane_x+plane_width/2 - self.width/2
		self.y = plane_y + plane_height
	#子弹移动
	def move(self):
		self.y += 5

	#判断子弹是否越界
	def judge(self):
		if self.y >= 550:
			return True
		else :
			return False	
	#判断是否打中英雄机
	def judge_hit(self, hero_item):
		if (self.x > hero_item.x) and (self.x < hero_item.x + hero_item.width - self.width) and (self.y > hero_item.y) and (self.y < hero_item.y - self.height + hero_item.height):
			self.y = 550 #一打中子弹就挪到屏幕外
			hero_item.lose_hp()#打中直接敌机掉血
			return True
		else:
			return False	

class BossBulletLeft(EnemyBullet):
	def __init__(self, screen, plane_width, plane_height, plane_x, plane_y):
		super(BossBulletLeft, self).__init__(screen, plane_width, plane_height, plane_x, plane_y)
		self.x = plane_x + 35
		self.y = plane_y + plane_height + 20
class BossBulletRight(EnemyBullet):
	def __init__(self, screen, plane_width, plane_height, plane_x, plane_y):
		super(BossBulletRight, self).__init__(screen, plane_width, plane_height, plane_x, plane_y)
		self.x = plane_x+plane_width - self.width - 35
		self.y = plane_y + plane_height + 20

			
class Property(Base):
	def __init__(self, screen):
		super(Property, self).__init__(screen)
		self.x = random.randint(0,200)
		self.y = 0	
	#掉落道具
	def drop_prop(self):
		'''
		函数说明：每隔一分钟掉落一个道具
		screen：游戏窗口
		'''
		self.x += random.randint(-3,3)
		self.y += 2		

	#展示道具
	def display(self, hero_item):
		if self.judge():
			pass
		else:
			self.screen.blit(self.image,(self.x,self.y))
			self.drop_prop()
			self.judge_property(hero_item)

	def judge(self):#越界返回真
		if (self.x >= 240) or (self.x <= -self.width) or (self.y >= 560):
			return True
		else:
			return False

class BulletProperty(Property):#补子弹道具
	def __init__(self, screen):
		get_goods1_image(self)
		super(BulletProperty, self).__init__(screen)

	def judge_property(self, hero_item):#判断玩家飞机是否吃到道具
		if (self.x > hero_item.x - self.width) and (self.x < hero_item.x + hero_item.width) and (self.y > hero_item.y - self.height) and (self.y < hero_item.y +hero_item.height):
			self.x = -self.width  #吃到就删除
			hero_item.bullet_box = 100
			return True
		else:
			return False


class HpProperty(Property):#补hp道具
	def __init__(self, screen):
		get_goods2_image(self)
		super(HpProperty, self).__init__(screen)

	def judge_property(self, hero_item):#判断玩家飞机是否吃到道具
		if (self.x > hero_item.x - self.width) and (self.x < hero_item.x + hero_item.width) and (self.y > hero_item.y - self.height) and (self.y < hero_item.y +hero_item.height):
			self.x = -self.width  #吃到就删除
			hero_item.hp += 30
			if hero_item.hp > hero_item.init_hp:
				hero_item.hp = hero_item.init_hp
			return True
		else:
			return False





#玩家操作
def player_move_left(arg):#这里要传一个玩家实例对象
	arg.move_left()

def player_move_right(arg):#这里要传一个玩家实例对象
	arg.move_right()

def player_move_up(arg):#这里要传一个玩家实例对象
	arg.move_up()

def player_move_down(arg):#这里要传一个玩家实例对象
	arg.move_down()

def player_fire_bullet(arg):#这里要传一个玩家实例对象
	arg.fire()

#敌机出现（敌机显示规则：设置多种敌机样式，每种敌机Hp不一样）我这里先设置两种敌机，最终种数待定，敌机每出现一次，种类随机，



def get_player_hp(arg):
	if arg.hp < 0:
		return 0
	else:
		return arg.hp

def get_player_score(hero):
	return hero.score


def get_bullet_num(arg,hero_item):#弹仓剩余子弹数
	if arg.judge_property(hero_item):#这里要写两个实例化了的实例对象
		hero_item.bullet_box = 100
	return hero_item.bullet_box

def get_a_enemy(screen):
	n = random.randint(0,2)
	if n == 0:
		return EnemyPlane1(screen)
	elif n == 1:
		return EnemyPlane2(screen)
	else:
		return EnemyPlane3(screen)

def get_a_hero(screen):
	return HeroPlane(screen)

def get_a_boss1(screen):
	return EnemyBoss1(screen)
def get_a_boss2(screen):
	return EnemyBoss2(screen)
def get_a_boss3(screen):
	return EnemyBoss3(screen)

def hero_item_display(arg):#第一个参数是你要展示的对象
	arg.display()

def enemy_item_display(arg, hero):
	arg.display(hero)

def get_a_property(screen):#得到一个子弹道具对象，参数是窗口
	return BulletProperty(screen)

def get_hp_property(screen):#得到一个补血道具对象，参数是窗口
	return HpProperty(screen)

def property_display(arg, hero_item):#展示补血道具或子弹道具，第一个参数是你要展示的对象
	arg.display(hero_item)

#传入实例对象
def enemy_item_judge(arg):
	return arg.judge()

def hero_bullet_display():#这是玩家子弹显示的方法，需传敌机对象
	hero_del_bullet_list = []
	for bullet in hero_bullet_list:
		bullet.screen.blit(bullet.image, (bullet.x, bullet.y))
		if bullet.judge():
			hero_del_bullet_list.append(bullet)
		bullet.move()
	for bullet in hero_del_bullet_list:
		hero_bullet_list.remove(bullet)	

def hero_bullet_judge_hit(enemy):
	for bullet in hero_bullet_list:
		bullet.judge_hit(enemy)

def enemy_bullet_display():#这是敌机子弹显示的方法，需传玩家对象
	enemy_del_bullet_list = []
	for bullet in enemy_bullet_list:
		bullet.screen.blit(bullet.image, (bullet.x, bullet.y))
		if bullet.judge():
			enemy_del_bullet_list.append(bullet)
		bullet.move()
	for bullet in enemy_del_bullet_list:
		enemy_bullet_list.remove(bullet)

def enemy_bullet_judge_hit(hero):
	for bullet in enemy_bullet_list:
		bullet.judge_hit(hero)					
def	judge_pengzhuang(arg, enemy):
	arg.judge_pengzhuang(enemy)