import pygame, math
from assets import Text
from random import random, randint, choice
from assets import Meteor

class SimpleEnemy(pygame.sprite.Sprite):
	def __init__(self, groups, pos, player):
		super().__init__(groups)
		self.image = pygame.image.load('../photos/SimpleEnemy.png').convert_alpha()
		self.rect = self.image.get_rect(center = pos)
		self.player = player

		self.speed = 10
		self.pos = self.rect.center
		self.direction = pygame.math.Vector2(0, 0)

		self.flipped = False

	def move(self, dt):
		self.pos += self.speed * self.direction * dt
		self.rect.center = round(self.pos.x), round(self.pos.y)

	def checkPlayer(self):
		distance = [-self.rect.centerx + self.player.rect.centerx, -self.rect.centery + self.player.rect.centery]
		norm = round(math.sqrt(distance[0] ** 2 + distance[1] ** 2))
		
		if norm < 50 and norm != 0:
			self.direction = pygame.math.Vector2(distance[0] / norm, distance[1] / norm)
		else:
			self.direction = pygame.math.Vector2(0, 0)

		if self.direction.x > 0 and not self.flipped:
			self.flipped = True
			self.image = pygame.transform.flip(self.image, True, False)
		elif self.direction.x < 0 and self.flipped:
			self.flipped = False
			self.image = pygame.transform.flip(self.image, True, False)

	def update(self, dt, offset):
		self.move(dt)
		self.checkPlayer()

class BlackHole(pygame.sprite.Sprite):
	def __init__(self, groups, pos, start_pos, end_pos, speed):
		super().__init__(groups)
		self.image = pygame.image.load('../photos/blackhole.png').convert_alpha()
		self.rect = self.image.get_rect(center = pos)
		self.start_pos = start_pos
		self.end_pos = end_pos

		self.speed = speed
		self.pos = self.rect.center

		distance = [-start_pos[0] + end_pos[0], -start_pos[1] + end_pos[1]]
		self.direction = pygame.math.Vector2(distance[0] / 10, distance[1] / 10)

	def move(self, dt):
		self.pos += self.speed * self.direction * dt
		self.rect.center = round(self.pos.x), round(self.pos.y)

	def calculate(self):
		if self.rect.center == self.end_pos:
			self.direction *= -1
			self.start_pos, self.end_pos = self.end_pos, self.start_pos

	def update(self, dt, offset):
		self.move(dt)
		self.calculate()

class Saturn(pygame.sprite.Sprite):
	def __init__(self, groups, pos, player, meteorGroup):
		super().__init__(groups)
		self.image = pygame.image.load('../photos/saturn.png').convert_alpha()
		self.rect = self.image.get_rect(center = pos)

		self.health = 100
		self.last_shoot = 0
		self.player = player
		self.meteor_groups = meteorGroup

		self.text = Text(
			groups,
			pygame.font.Font('../photos/REDENSEK.TTF', 12),
			f'{self.health}HP',
			(self.rect.centerx, self.rect.top - 5),
			(100, 250, 100)
		)

	def attack(self):
		if self.rect.centerx - self.player.rect.centerx < 50:
			if pygame.time.get_ticks() - self.last_shoot > 2000:
				self.last_shoot = pygame.time.get_ticks()

				SimpleEnemy(self.meteor_groups, self.rect.center, self.player)

	def update(self, dt, offset):
		self.attack()

class Jupiter(pygame.sprite.Sprite):
	def __init__(self, groups, pos, player):
		super().__init__(groups)
		self.image = pygame.image.load('../photos/jupiter.png').convert_alpha()
		self.rect = self.image.get_rect(center = pos)

		self.health = 200
		self.last_shoot = 0
		self.player = player
		self.groups = groups

		self.text = Text(
			groups,
			pygame.font.Font('../photos/REDENSEK.TTF', 12),
			f'{self.health}HP',
			(self.rect.centerx, self.rect.top - 5),
			(100, 250, 100)
		)

		self.speed = 20
		self.direction = pygame.math.Vector2()
		self.pos = pygame.math.Vector2(self.rect.center)
		self.last_changed = 0

	def move(self, dt):
		self.pos += self.speed * self.direction * dt
		self.rect.center = round(self.pos.x), round(self.pos.y)

		self.text.kill()
		self.text = Text(
			self.groups,
			pygame.font.Font('../photos/REDENSEK.TTF', 12),
			f'{self.health}HP',
			(self.rect.centerx, self.rect.top - 5),
			(100, 250, 100)
		)

	def checkPlayer(self):
		if self.rect.centerx - self.player.rect.centerx < 64 and pygame.time.get_ticks() - self.last_changed > 4000:
			self.last_changed = pygame.time.get_ticks()
			self.direction.x = round(random(), 1) * randint(-1, 1)
			self.direction.y = round(random(), 1) * randint(-1, 1)

	def border(self):
		if self.pos.y - 30 < 0:
			self.pos.y = 30
		elif self.pos.y + 30 > 64:
			self.pos.y = 34
		if self.pos.x > 620:
			self.pos.x = 620

	def update(self, dt, offset):
		self.move(dt)
		self.checkPlayer()
		self.border()

class Mars(pygame.sprite.Sprite):
	def __init__(self, groups, pos, player, meteor_groups):
		super().__init__(groups)
		self.image = pygame.image.load('../photos/mars.png').convert_alpha()
		self.rect = self.image.get_rect(center = pos)

		self.health = 100
		self.last_shoot = 0
		self.player = player
		self.groups = groups
		self.meteor_groups = meteor_groups

		self.text = Text(
			groups,
			pygame.font.Font('../photos/REDENSEK.TTF', 12),
			f'{self.health}HP',
			(self.rect.centerx, self.rect.top - 5),
			(100, 250, 100)
		)

		self.speed = 20
		self.direction = pygame.math.Vector2()
		self.pos = pygame.math.Vector2(self.rect.center)
		self.last_changed = 0

		self.directions = [-1, 1]

	def move(self, dt):
		self.pos += self.speed * self.direction * dt
		self.rect.center = round(self.pos.x), round(self.pos.y)

		self.text.kill()
		self.text = Text(
			self.groups,
			pygame.font.Font('../photos/REDENSEK.TTF', 12),
			f'{self.health}HP',
			(self.rect.centerx, self.rect.top - 5),
			(100, 250, 100)
		)

	def border(self):
		if self.pos.y - 6 < 0:
			self.pos.y = 6
		elif self.pos.y + 6 > 64:
			self.pos.y = 58

	def checkPlayer(self):
		if self.rect.centerx - self.player.rect.centerx < 60 and pygame.time.get_ticks() - self.last_changed > 2000:
			self.last_changed = pygame.time.get_ticks()
			self.direction.y = round(random(), 1) * choice(self.directions)

			meteor = Meteor(self.rect.center, self.player, 0, self.meteor_groups)
			distance = [-meteor.rect.centerx + self.player.rect.centerx, -meteor.rect.centery + self.player.rect.centery]
			norm = round(math.sqrt(distance[0] ** 2 + distance[1] ** 2))
			meteor.direction = pygame.math.Vector2(distance[0] / norm, distance[1] / norm)

	def update(self, dt, offset):
		self.move(dt)
		self.border()
		self.checkPlayer()

class Laser(pygame.sprite.Sprite):
	def __init__(self, groups, pos, changeTime, width):
		super().__init__(groups)
		self.images = [
			pygame.transform.scale(pygame.image.load('../photos/laser_normal.png').convert_alpha(), (width, 64)),
			pygame.transform.scale(pygame.image.load('../photos/laser_active.png').convert_alpha(), (width, 64)),
		]
		self.image = self.images[0]
		self.rect = self.image.get_rect(topleft = pos)

		self.last_changed = pygame.time.get_ticks()
		self.change_time = changeTime
		self.active = False

	def change(self):
		if pygame.time.get_ticks() - self.last_changed > self.change_time:
			self.last_changed = pygame.time.get_ticks()
			self.active = not self.active
			self.image = self.images[int(self.active)]

	def update(self, dt, offset):
		self.change()

class Sun(pygame.sprite.Sprite):
	def __init__(self, groups, pos, player, meteorGroups):
		super().__init__(groups)
		self.image = pygame.image.load('../photos/sun.png').convert_alpha()
		self.rect = self.image.get_rect(center = pos)

		self.health = 300
		self.player = player

		self.text = Text(
			groups,
			pygame.font.Font('../photos/REDENSEK.TTF', 12),
			f'{self.health}HP',
			(self.rect.centerx, self.rect.top - 5),
			(100, 250, 100)
		)

		self.speed = 10
		self.direction = pygame.math.Vector2()
		self.pos = pygame.math.Vector2(self.rect.center)
		self.meteor_groups = meteorGroups
		self.group = groups

		self.last_changed = 0
		self.last_shoot = 0
		self.laser = None

	def move(self, dt):
		self.pos += self.speed * self.direction * dt
		self.rect.center = round(self.pos.x), round(self.pos.y)

		self.text.kill()
		self.text = Text(
			self.group,
			pygame.font.Font('../photos/REDENSEK.TTF', 12),
			f'{self.health}HP',
			(self.rect.centerx, self.rect.top - 5),
			(100, 250, 100)
		)

	def checkPlayer(self):
		if self.rect.centerx - self.player.rect.centerx < 70 and pygame.time.get_ticks() - self.last_changed > 5000:
			self.last_changed = pygame.time.get_ticks()
			self.direction.x = round(random(), 1) * randint(-1, 1)
			self.direction.y = round(random(), 1) * randint(-1, 1)

			self.last_shoot = pygame.time.get_ticks()
			SimpleEnemy(self.meteor_groups, self.rect.center, self.player)

			if self.laser: self.laser.kill()
			self.laser = Laser(self.group, (self.player.rect.x, 0), 2500, randint(5, 15))
			self.laser.active = False

	def border(self):
		if self.pos.y - 30 < 0:
			self.pos.y = 30
		elif self.pos.y + 30 > 64:
			self.pos.y = 34
		if self.pos.x > 620:
			self.pos.x = 620

	def update(self, dt, offset):
		self.move(dt)
		self.checkPlayer()
		self.border()