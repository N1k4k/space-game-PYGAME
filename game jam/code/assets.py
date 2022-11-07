import pygame, math
from setting import *
from random import randint

class AllSprites(pygame.sprite.Group):
	def __init__(self, display_surface):
		super().__init__()
		self.offset = pygame.math.Vector2()
		self.display_surface = display_surface
		self.bg = pygame.image.load('../photos/background.png').convert()

	def customize_draw(self, player):
		# change the offset vector
		self.offset.x = player.rect.centerx - REZOLUTION / 2 + round(player.offset)

		# blit the surfaces 
		self.display_surface.blit(self.bg,-self.offset)

		for sprite in self.sprites():
			offset_rect = sprite.image.get_rect(center = (sprite.rect.centerx - 13, sprite.rect.centery))
			offset_rect.center -= self.offset
			self.display_surface.blit(sprite.image,offset_rect)


class Meteor(pygame.sprite.Sprite):
	def __init__(self, pos, player, offset, groups):
		super().__init__(groups)
		self.rotation = randint(0, 4) * 90

		self.image = pygame.image.load('../photos/meteor.png').convert_alpha()
		self.image = pygame.transform.rotate(self.image, self.rotation)
		self.rect = self.image.get_rect(center = pos)

		self.speed = 25
		self.pos = self.rect.center

		mousex = round((pygame.mouse.get_pos()[0] * 64) / 900) + offset + 13
		mousey = round((pygame.mouse.get_pos()[1] * 64) / 900)
		distance = [mousex - player.rect.centerx, mousey - player.rect.centery]
		norm = math.sqrt(distance[0] ** 2 + distance[1] ** 2)
		if norm:
			self.direction = pygame.math.Vector2(distance[0] / norm, distance[1] / norm)
		else:
			self.direction = pygame.math.Vector2(0, 0)

		self.spawn_time = pygame.time.get_ticks()

	def move(self, dt):
		self.pos += self.speed * self.direction * dt
		self.rect.center = round(self.pos.x), round(self.pos.y)

	def detect(self):
		if self.rect.bottom < 0 or self.rect.top > REZOLUTION or pygame.time.get_ticks() - self.spawn_time > 10000:
			self.kill()

	def update(self, dt, offset):
		self.move(dt)
		self.detect()

		if self.speed > 1:
			self.speed -= 6 * dt
		else:
			self.speed = 0


# Menu
class Button(pygame.sprite.Sprite):
	def __init__(self, pos, text, groups):
		super().__init__(groups)
		self.image = pygame.image.load('../photos/button.png').convert_alpha()
		self.rect = self.image.get_rect(center = pos)
		self.i = text

		self.font = pygame.font.Font('../photos/REDENSEK.TTF', 12)
		self.text = self.font.render(text, False, (200, 200, 200))
		self.text_rect = self.text.get_rect(center = (pos[0] +1, pos[1] -1))

	def update(self, surface):
		surface.blit(self.image, self.rect)
		surface.blit(self.text, self.text_rect)

class Menu:
	def __init__(self):
		self.image = pygame.image.load('../photos/menu.png').convert()
		self.rect = self.image.get_rect(topleft = (0, 0))

		self.btn_pos = [10, 28]
		self.btn_margin = 3
		self.button_group = pygame.sprite.Group()

		# display
		for i in range(1, 5):
			Button(self.btn_pos, str(i), self.button_group)

			self.btn_pos[0] += 8 + self.btn_margin

			if i % 5 == 0:
				self.btn_pos[0] = 10
				self.btn_pos[1] += 8 + self.btn_margin

	def draw(self, surface):
		surface.blit(self.image, self.rect)
		self.button_group.update(surface)

class Text(pygame.sprite.Sprite):
	def __init__(self, groups, font, text, pos, color):
		super().__init__(groups)
		self.image = font.render(text, False, color)
		self.rect = self.image.get_rect(center = pos)