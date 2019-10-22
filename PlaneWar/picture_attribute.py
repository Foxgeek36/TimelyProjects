#-*-coding:utf-8-*-
#----------------飞机---------------------
def get_hero_image(arg):
	arg.file_address = "./image/hero.png"
	arg.width = 27
	arg.height = 32
def get_enemy1_image(arg):
	arg.file_address = "./image/enemy1.png"
	arg.width = 42
	arg.height = 28
def get_enemy2_image(arg):
	arg.file_address = "./image/enemy2.png"
	arg.width = 32
	arg.height = 27
def get_enemy3_image(arg):
	arg.file_address = "./image/enemy3.png"
	arg.width = 56
	arg.height = 31
def get_enemyboss1_image(arg):
	arg.file_address = "./image/EnemyBoss1.png"
	arg.width = 128
	arg.height = 64
def get_enemyboss2_image(arg):
	arg.file_address = "./image/EnemyBoss2.png"
	arg.width = 113
	arg.height = 80
def get_enemyboss3_image(arg):
	arg.file_address = "./image/EnemyBoss3.png"
	arg.width = 206
	arg.height = 60


#----------------子弹-------------------------
def get_herobullet1_image(arg):
	arg.file_address = "./image/HeroBullet1.png"
	arg.width = 8
	arg.height = 25
def get_herobullet2_image(arg):
	arg.file_address = "./image/HeroBullet2.png"
	arg.width = 8
	arg.height = 25
def get_enemybullet1_image(arg):
	arg.file_address = "./image/EnemyBullet1.png"
	arg.width = 10
	arg.height = 8


#-----------补给-------------------
def get_goods1_image(arg):
	arg.file_address = "./image/Goods01.png"
	arg.width = 16
	arg.height = 17
def get_goods2_image(arg):
	arg.file_address = "./image/Goods02.png"
	arg.width = 16
	arg.height = 17


#------------爆炸效果----------------
def get_planeboom1_image(arg):
	arg.file_address = "./image/planeboom/Plane_Boom_01.png"
	# arg.width = 42
	# arg.height = 32
def get_planeboom2_image(arg):
	arg.file_address = "./image/planeboom/Plane_Boom_02.png"
	# arg.width = 42
	# arg.height = 32
def get_planeboom3_image(arg):
	arg.file_address = "./image/planeboom/Plane_Boom_03.png"
	# arg.width = 42
	# arg.height = 32
def get_planeboom4_image(arg):
	arg.file_address = "./image/planeboom/Plane_Boom_04.png"
	# arg.width = 42
	# arg.height = 32
def get_planeboom5_image(arg):
	arg.file_address = "./image/planeboom/Plane_Boom_05.png"
	# arg.width = 42
	# arg.height = 32
def get_planeboom6_image(arg):
	arg.file_address = "./image/planeboom/Plane_Boom_06.png"
	# arg.width = 42
	# arg.height = 32
#--------------开始菜单和暂停菜单--------------------
def get_pause_image():
	file_address = "./image/pause.png"
	width = 42
	height = 32
	return file_address

def get_gameover_image():
	file_address = "./image/gameover.png"
	width = 42
	height = 32
	return file_address


def get_bossboom1_image(arg):
	arg.file_address = "./image/bossboom/Boss_Boom_01.png"
	# arg.width = 42
	# arg.height = 42
def get_bossboom2_image(arg):
	arg.file_address = "./image/bossboom/Boss_Boom_02.png"
	# arg.width = 42
	# arg.height = 42
def get_bossboom3_image(arg):
	arg.file_address = "./image/bossboom/Boss_Boom_03.png"
	# arg.width = 42
	# arg.height = 42
def get_bossboom4_image(arg):
	arg.file_address = "./image/bossboom/Boss_Boom_04.png"
	# arg.width = 42
	# arg.height = 42
def get_bossboom5_image(arg):
	arg.file_address = "./image/bossboom/Boss_Boom_05.png"
	# arg.width = 42
	# arg.height = 42
def get_bossboom6_image(arg):
	arg.file_address = "./image/bossboom/Boss_Boom_06.png"
	# arg.width = 42
	# arg.height = 42


#-----------------背景图---------------------
def get_backscreen1_image():
	file_address = "./image/BackScr1.png"
	width = 240
	height = 2000
	return file_address

def get_backscreen2_image():
	file_address = "./image/BackScr2.png"
	wdith = 240
	height = 2100
	return file_address
	
def get_backscreen3_image():
	file_address = "./image/BackScr3.png"
	width = 240
	height = 2100
	return file_address
