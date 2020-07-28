import pygame
import random 
import os

WIDTH = 480
HEIGHT = 600
FPS = 30

#define colors

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

game_folder = os.path.dirname( __file__ )
img_foder = os.path.join(game_folder,"image")
# print(game_folder)

font_name = pygame.font.match_font('arial')
def draw_text(surf,text,size,x,y):
	font = pygame.font.Font(font_name,size)
	text_surface = font.render(text , True,WHITE)
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x,y)
	surf.blit(text_surface,text_rect)

class Player(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.scale(pygame.image.load(os.path.join(img_foder,"playerShip2_blue.png")).convert(),(50,38))
		self.image.set_colorkey(BLACK)
		# self.image = pygame.Surface((50,40))
		# self.image.fill(GREEN)
		self.rect = self.image.get_rect()
		self.radius = int(self.rect.width/2)-4
		# pygame.draw.circle(self.image,RED,self.rect.center,self.radius)
		self.rect.centerx = WIDTH/2
		self.rect.bottom = HEIGHT-10
		self.speedx = 0
		self.speedy = 0
		# self.gravity = 10

	def update(self):
		self.speedx=0
		self.speedy=0
		keystate = pygame.key.get_pressed()
		if keystate[pygame.K_LEFT]:
			self.speedx=-20
		if keystate[pygame.K_RIGHT]:
			self.speedx=20
		# if keystate[pygame.K_UP]:
		# 	self.speedy=-12
		# self.rect.y+=self.speedy
		# self.rect.y+=self.gravity	
		self.rect.x+=self.speedx
		if self.rect.bottom > HEIGHT:
			self.rect.bottom= HEIGHT
		if self.rect.right > WIDTH:
			self.rect.right= WIDTH
		if self.rect.left <0:
			self.rect.left= 0

	def shoot(self):
		bullet = Bullet(self.rect.centerx,self.rect.top)
		all_sprites.add(bullet)
		bullets.add(bullet)

		
class Mob(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image_orig = metore_img
		self.image_orig.set_colorkey(BLACK)
		self.image = self.image_orig.copy()
		# self.image = pygame.Surface((30,40))
		# self.image.fill(RED)
		self.rect = self.image.get_rect()
		self.radius = int(self.rect.width*0.85/2)
		# pygame.draw.circle(self.image,RED,self.rect.center,self.radius)
		self.rect.x = random.randrange(WIDTH-self.rect.width)
		self.rect.y = random.randrange(-100,-40)
		self.speedy = random.randrange(2,12)
		self.speedx = random.randrange(-3,3)
		self.rot = 0
		self.rotate_speed = random.randrange(-8,8)
		self.last_update = pygame.time.get_ticks()

	def rotate(self):
		now = pygame.time.get_ticks()
		if now-self.last_update > 50:
			last_update = now
			self.rot= (self.rot + self.rotate_speed)%360
			new_image = pygame.transform.rotate(self.image_orig,self.rot)
			old_center = self.rect.center
			self.image = new_image
			self.rect = self.image.get_rect()
			self.rect.center = old_center
	def update(self):
		self.rotate()
		self.rect.y+=self.speedy
		self.rect.x+=self.speedx
		if self.rect.top > HEIGHT+10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
			self.rect.x = random.randrange(WIDTH-self.rect.width)
			self.rect.y = random.randrange(-100,-40)
			self.speedy = random.randrange(2,12)

class Bullet(pygame.sprite.Sprite):
	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(os.path.join(img_foder,"laserBlue06.png")).convert()
		self.image.set_colorkey(BLACK)
		# self.image = pygame.Surface((10,20))
		# self.image.fill(WHITE)
		self.rect = self.image.get_rect()
		self.rect.bottom = y
		self.rect.centerx = x
		self.speedy = -15

	def update(self):
		self.rect.y += self.speedy
		if self.rect.top< 0 :
			self.kill()

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("My game");
clock = pygame.time.Clock()

background= pygame.image.load(os.path.join(img_foder,"bHiPMju.png")).convert()
background_rect = background.get_rect()
metore_img = pygame.image.load(os.path.join(img_foder,"meteorBrown_med1.png")).convert()

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

for i in range(8):
	m =  Mob()
	all_sprites.add(m)
	mobs.add(m)

# Game loop
running = True;
score=0
while running:
	clock.tick(FPS)
	# Process input
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running=False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				player.shoot()
	#update
	all_sprites.update()

	hits = pygame.sprite.groupcollide(mobs,bullets,True,True)
	# if hits:
	for hit in hits:
		score=score+1
		m =  Mob()
		all_sprites.add(m)
		mobs.add(m)
	hits = pygame.sprite.spritecollide(player,mobs,False,pygame.sprite.collide_circle)
	if hits:
		running = False
	#draw / render
	screen.fill(BLACK)
	screen.blit(background,background_rect)	
	all_sprites.draw(screen)
	draw_text(screen,str(score),18,WIDTH/2,10)
	pygame.display.flip()

pygame.quit()