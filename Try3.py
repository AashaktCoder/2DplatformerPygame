import pygame

pygame.init()

HEIGHT, WIDTH = 500, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer")

# Player Class
class Player:
	def __init__(self, x, y, width, height, CollideList):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.rect = [self.x, self.y, self.width, self.height]
		self.direction = pygame.math.Vector2()
		self.speed = 4
		self.gravity = 0.8
		self.CollideList = CollideList
		self.OnGround = False

	def Draw(self):
		self.image = pygame.draw.rect(WIN, (28, 111, 166), self.rect)	

	def Movement(self):
		keys = pygame.key.get_pressed()	
		if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
			self.direction.x = 1
		elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
			self.direction.x = -1	
		else:
			self.direction.x = 0	

		if keys[pygame.K_SPACE] and self.OnGround:
			self.direction.y = -16

	def HorizontalCollison(self):
		for Tiles in self.CollideList:
			if Tiles.colliderect(self.rect):
				if self.direction.x > 0:
					self.rect[0] = Tiles.left - 50
				if self.direction.x < 0:
					self.rect[0] = Tiles.right

	def VerticalCollison(self):
		for Tiles in self.CollideList:
			if Tiles.colliderect(self.rect):
				if self.direction.y > 0:
					self.rect[1] = Tiles.top - 50
					self.direction.y = 0
					self.OnGround = True
				if self.direction.y < 0:
					self.rect[1] = Tiles.bottom	
					self.direction.y = 0
		if self.OnGround and self.direction.y != 0:
			self.OnGround = False			

	def Update(self):		
		self.Movement()
		self.rect[0] += (self.direction.x * self.speed)
		self.HorizontalCollison()
		self.direction.y += self.gravity
		self.rect[1] += self.direction.y
		self.VerticalCollison()
		self.Draw()

def Main():
	# Main Game Variables
	run = True
	clock = pygame.time.Clock()
	FPS = 60

	# Lists
	LEVEL = [[0,0,0,0,0,0,0,0,0,0],
			 [0,0,0,0,0,0,0,0,0,0],
			 [0,0,0,0,0,0,0,0,0,0],
			 [0,0,1,0,0,0,0,0,0,0],
			 [0,0,1,1,1,0,0,0,0,0],
			 [0,0,1,1,1,1,1,0,0,0],
			 [0,0,0,0,0,0,0,0,1,1],
			 [1,2,0,0,0,0,1,1,1,1],
			 [1,1,1,1,1,1,1,1,1,1],
			 [1,1,1,1,1,1,1,1,1,1]]

	# Variables related to sprites
	TileSize = 50
	TileGroup = []

	# Making the Level
	y_pos = 0		 
	for row in LEVEL:
		x_pos = 0
		for col in row:
			x = TileSize * x_pos
			y = TileSize * y_pos
			if col == 1:
				Tile = pygame.draw.rect(WIN, (44, 47, 48), [x,y,TileSize,TileSize])
				TileGroup.append(Tile)
			if col == 2:
				player = Player(x,y,TileSize,TileSize,TileGroup)		
			x_pos += 1
		y_pos += 1		
 
	while run:
		WIN.fill((255,255,255))
		y_pos = 0		 
		for row in LEVEL:
			x_pos = 0
			for col in row:
				x = TileSize * x_pos
				y = TileSize * y_pos
				if col == 1:
					Tile = pygame.draw.rect(WIN, (44, 47, 48), [x,y,TileSize,TileSize])

				x_pos += 1
			y_pos += 1	
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()
				quit()
		player.Update()		
		pygame.display.update()
		clock.tick(FPS)		

Main()				