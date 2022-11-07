import pygame
from setting import *

class Player(pygame.sprite.Sprite):
	def __init__(self, groups):
		super().__init__(groups)
		self.image = pygame.image.load('../photos/earth.png')
		self.rect = self.image.get_rect(center = (40, REZOLUTION / 2))

		self.speed = 15
		self.pos = self.rect.center
		self.direction = pygame.math.Vector2(0, 0)

		self.flipped = False
		self.offset = 0

	def input(self, dt):
		keys = pygame.key.get_pressed()

		# horizontal
		if keys[pygame.K_d] and self.rect.right < 600:
			self.direction.x = 1

			if self.offset < 12:
				self.offset += 1 * dt

		elif keys[pygame.K_a] and self.rect.left > 31:
			self.direction.x = -1

			if self.offset > -35:
				self.offset -= 5 * dt
		else:
			self.direction.x = 0
			if self.offset > 0.1:
				self.offset -= 10 * dt
			elif self.offset < -0.1:
				self.offset += 10 * dt
			else:
				self.offset = 0

		# vertical
		if keys[pygame.K_w] and self.rect.top > 0:
			self.direction.y = -1
		elif keys[pygame.K_s] and self.rect.bottom < REZOLUTION:
			self.direction.y = 1
		else:
			self.direction.y = 0

	def move(self, dt):
		self.pos += self.speed * self.direction * dt
		self.rect.center = round(self.pos.x), round(self.pos.y)

	def rotate(self, offset):
		pos = round((pygame.mouse.get_pos()[0] * 64) / 900) + offset + 13

		if pos > self.rect.centerx and self.flipped == True:
			self.image = pygame.transform.flip(self.image, True, False)
			self.flipped = False

		if pos < self.rect.centerx and self.flipped == False:
			self.image = pygame.transform.flip(self.image, True, False)
			self.flipped = True

	def update(self, dt, offset):
		self.input(dt)
		self.move(dt)
		self.rotate(offset)
