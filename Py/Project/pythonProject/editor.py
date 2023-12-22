import pygame
import pickle
from os import path


pygame.init()

clock = pygame.time.Clock()
fps = 60

tile_size = 50
cols = 32
rows = 18
margin = 100
screen_width = tile_size * cols
screen_height = (tile_size * rows) + margin

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Level Editor')


sun_img = pygame.image.load('Assets/sun.png')
sun_img = pygame.transform.scale(sun_img, (tile_size, tile_size))
bg_img = pygame.image.load('Assets/darkmood.jpg')
bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height - margin))
stone_img = pygame.image.load('Assets/block1.png')
grass_img = pygame.image.load('Assets/grass1.png')
frame_img = pygame.image.load('Assets/frame.png')
platform_x_img = pygame.image.load('Assets/platform.png')
platform_y_img = pygame.image.load('Assets/platform.png')
lava_img = pygame.image.load('Assets/lava.png')
coin_img = pygame.image.load('Assets/coin.png')
door_img = pygame.image.load('Assets/door.png')
save_img = pygame.image.load('Assets/savebutton.png')
load_img = pygame.image.load('Assets/loadbutton.png')


clicked = False
level = 1

white = (255, 255, 255)
black = (0, 0, 0)

font = pygame.font.SysFont('Futura', 25)

world_data = []
for row in range(18):
	r = [0] * 32
	world_data.append(r)

#создаем границы
for tile1 in range(0, 18):
    world_data[tile1][0] = 1
    world_data[tile1][31] = 1
    for tile2 in range(0, 32):
        world_data[17][tile2] = 2
        world_data[0][tile2] = 1

def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

#сетка
def draw_grid():
	for _ in range(33):
		#вертикальные линии
		pygame.draw.line(screen, white, (_ * tile_size, 0), (_ * tile_size, screen_height - margin))
	for _ in range(19):
		#горизонтальные линии
		pygame.draw.line(screen, white, (0, _ * tile_size), (screen_width, _ * tile_size))


def draw_world():
	for row in range(18):
		for col in range(32):
			if world_data[row][col] == 1:
				img = pygame.transform.scale(stone_img, (tile_size, tile_size))
				screen.blit(img, (col * tile_size, row * tile_size))
			if world_data[row][col] == 2:
				img = pygame.transform.scale(grass_img, (tile_size, tile_size))
				screen.blit(img, (col * tile_size, row * tile_size))
			if world_data[row][col] == 3:
				img = pygame.transform.scale(frame_img, (tile_size, int(tile_size * 0.75)))
				screen.blit(img, (col * tile_size, row * tile_size + (tile_size * 0.25)))
			if world_data[row][col] == 4:
				img = pygame.transform.scale(platform_x_img, (tile_size, tile_size // 2))
				screen.blit(img, (col * tile_size, row * tile_size))
			if world_data[row][col] == 5:
				img = pygame.transform.scale(platform_y_img, (tile_size, tile_size // 2))
				screen.blit(img, (col * tile_size, row * tile_size))
			if world_data[row][col] == 6:
				img = pygame.transform.scale(lava_img, (tile_size, tile_size // 2))
				screen.blit(img, (col * tile_size, row * tile_size + (tile_size // 2)))
			if world_data[row][col] == 7:
				img = pygame.transform.scale(coin_img, (tile_size // 2, tile_size // 2))
				screen.blit(img, (col * tile_size + (tile_size // 4), row * tile_size + (tile_size // 4)))
			if world_data[row][col] == 8:
				img = pygame.transform.scale(door_img, (tile_size, int(tile_size * 1.5)))
				screen.blit(img, (col * tile_size, row * tile_size - (tile_size // 2)))



class Button():
	def __init__(self, x, y, image):
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self):
		action = False

		pos = pygame.mouse.get_pos()

		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				action = True
				self.clicked = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		screen.blit(self.image, (self.rect.x, self.rect.y))

		return action

save_button = Button(screen_width // 2 - 150, screen_height - 80, save_img)
load_button = Button(screen_width // 2 + 50, screen_height - 80, load_img)

run = True
while run:

	clock.tick(fps)

	screen.fill(black)
	screen.blit(bg_img, (0, 0))
	screen.blit(sun_img, (tile_size * 2, tile_size * 2))

	if save_button.draw():
		pickle_out = open(f'level{level}_data', 'wb')
		pickle.dump(world_data, pickle_out)
		pickle_out.close()
	if load_button.draw():
		if path.exists(f'level{level}_data'):
			pickle_in = open(f'level{level}_data', 'rb')
			world_data = pickle.load(pickle_in)



	draw_grid()
	draw_world()


	draw_text(f'Level: {level}', font, white, tile_size, screen_height - 60)


	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		#меняем тайлы кликом
		if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
			clicked = True
			pos = pygame.mouse.get_pos()
			x = pos[0] // tile_size
			y = pos[1] // tile_size
			#проверка координат
			if x < 32 and y < 18:
				if pygame.mouse.get_pressed()[0] == 1:
					world_data[y][x] += 1
					if world_data[y][x] > 8:
						world_data[y][x] = 0
				elif pygame.mouse.get_pressed()[2] == 1:
					world_data[y][x] -= 1
					if world_data[y][x] < 0:
						world_data[y][x] = 8
		if event.type == pygame.MOUSEBUTTONUP:
			clicked = False
		#меняем уровни стрелками
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				level += 1
			elif event.key == pygame.K_DOWN and level > 1:
				level -= 1

	pygame.display.update()

pygame.quit()