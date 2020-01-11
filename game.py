import pygame
import random
pygame.init()

# first it reads the variables from the file

file = open("settings.txt", "r")
file_lines = file.readlines()
for i in range(len(file_lines)):
	try:
		file_lines[i] = int("".join(file_lines[i][:-1]).lower())
	except:
		pass

square_size = file_lines[1] - 1

grid_width = file_lines[4]
grid_height = file_lines[7]

screen_width = (square_size + 1) * grid_width
screen_height = (square_size + 1) * grid_height

fps = file_lines[10]
start_length = file_lines[13]
growth = file_lines[16]
pink_apple_growth = file_lines[19]
pink_apple = False
pink_apple_chance = file_lines[22]

# pygame stuff

win = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

# class for each square

class Square(object):
	def __init__(self, x, y, color):
		self.x = x
		self.y = y
		self.color = color

	# to draw the certain box
	def draw(self):
		pygame.draw.rect(win, self.color, (self.x, self.y, square_size, square_size))

# class for the apple, i put this in a class to make it more organised
class Apple(object):
	def __init__(self):
		self.x = random.randint(0, grid_width-1)
		self.y = random.randint(0, grid_height-1)

	# to put the apple in a random not taken spot
	def find(self):
		global pink_apple
		while True:
			self.x = random.randint(0, grid_width-1)
			self.y = random.randint(0, grid_height-1)
			if not((self.x, self.y) in snake.tail):
				break

		if random.random() < pink_apple_chance / 100:
			pink_apple = True
		else:
			pink_apple = False
		self.draw()

	# draws the apple
	def draw(self):
		global pink_apple
		if pink_apple:
			grid[self.x][self.y].color = (255, 0, 128)
		else:
			grid[self.x][self.y].color = (255, 0, 0)

# class for the snake
class Snake(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.tail = []
		self.x_vel = 1
		self.y_vel = 0
		# the snake.dept variable if for when it is growing
		self.dept = start_length

	# doaws up the snake
	def draw(self):
		def colorround(color):
			if color > 255:
				color = 255
			elif color < 0:
				color = 0
			return round(color)

		self.move()

		# draw the head
		grid[self.x][self.y].color = (0, 255, 0)

		# graws the tail with a gradient
		grad_step = 127 / len(self.tail)
		grad_count = 0
		for place in self.tail:
			grad_count += 1
			grid[place[0]][place[1]].color = (colorround(grad_step * grad_count), 255, colorround(grad_step * grad_count))

	def move(self):
		# adds to the tail
		self.tail.insert(0, (self.x, self.y))
		# moves the head
		self.x += self.x_vel
		self.y += self.y_vel

		# detecting if it hits the edge
		if self.x < 0 or self.x > grid_width - 1:
			print("Dead")
			pygame.quit()
			quit()
		if self.y < 0 or self.y > grid_width - 1:
			print("Dead")
			run = False
			pygame.quit()
			quit()
		# or if it hits the tail
		if (self.x, self.y) in self.tail:
			print("Dead")
			run = False
			pygame.quit()
			quit()
		# deletes the last part off the tail
		if self.dept == 0:
			self.tail = self.tail[:-1]
		else:
			self.dept -= 1

		# if it hits an apple
		if self.x == apple.x and self.y == apple.y:
			if pink_apple:
				self.dept += pink_apple_growth
			else:
				self.dept += growth
			apple.find()


# code for the text
def text_objects(text, font):
	textSurface = font.render(text, True, (200, 200, 200))
	return textSurface, textSurface.get_rect()

def display_score(text):
	largeText = pygame.font.Font('freesansbold.ttf', 30)
	TextSurf, TextRect = text_objects(text, largeText)
	TextRect.center = (round(screen_width * 0.95), round(screen_height * 0.95))
	win.blit(TextSurf, TextRect)

# draws up the window
def redrawGameWindow():
	win.fill((0, 0, 0))
	# makes the grid grey
	for x in grid:
		for y in x:
			y.color = (60, 60, 60)
	# changes grid colors for the snake and apple
	snake.draw()
	apple.draw()
	# draws up the grid
	for x in grid:
		for y in x:
			y.draw()
	# then draws the score
	display_score(str(len(snake.tail)))
	pygame.display.update()

# makes the grid variable with classes in it
grid = []
for i in range(screen_width // (square_size + 1)):
	grid.append([])
	for j in range(screen_height // (square_size + 1)):
		grid[i].append(Square(i * (square_size + 1), j * (square_size + 1), (60, 60, 60)))

snake = Snake(grid_width//2, grid_height//2)
apple = Apple()

run = True
while run:
	clock.tick(fps)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

		# movement
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_a or event.key == pygame.K_LEFT:
				moveLEFT = True
				snake.x_vel = -1
				snake.y_vel = 0
			elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
				moveRIGHT = True
				snake.x_vel = 1
				snake.y_vel = 0
			elif event.key == pygame.K_w or event.key == pygame.K_UP:
				moveUP = True
				snake.x_vel = 0
				snake.y_vel = -1
			elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
				moveDOWN = True
				snake.x_vel = 0
				snake.y_vel = 1

	keys = pygame.key.get_pressed()

	redrawGameWindow()

pygame.quit()
quit()
