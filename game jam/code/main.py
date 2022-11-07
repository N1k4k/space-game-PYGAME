import pygame, sys
from setting import *
from player import Player
from assets import *
from enemy import *

class Game():
	def __init__(self):
		pygame.init()
		self.clock = pygame.time.Clock()

		self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
		self.display_surface = pygame.Surface((REZOLUTION, REZOLUTION))
		pygame.display.set_caption('The Sun Is Your Enemy')

		# groups
		self.all_sprites = AllSprites(self.display_surface)
		self.meteors = pygame.sprite.Group()
		self.enemy_group = pygame.sprite.Group()
		self.obsticle_group = pygame.sprite.Group()
		self.laser_group = pygame.sprite.Group()

		self.boss = None

		# events
		self.last_shoot = 0

		# menu
		self.level = 'menu'
		self.menu = Menu()
		self.font = pygame.font.Font('../photos/REDENSEK.TTF', 12)

		# music
		self.explosion_sound = pygame.mixer.Sound("../sounds/explosion.wav")
		self.enemy_kill_sound = pygame.mixer.Sound('../sounds/enemyKill.wav')
		self.black_hole_death_sound = pygame.mixer.Sound('../sounds/blackHoleDeath.wav')

		pygame.mixer.music.load('../sounds/background.wav')
		pygame.mixer.music.play(-1)

	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

			self.dt = self.clock.tick() /1000

			# ------- menu ------------
			if self.level == 'menu':
				self.menu.draw(self.display_surface)

				if pygame.mouse.get_pressed()[0]:
					for button in self.menu.button_group:
						pos = round(pygame.mouse.get_pos()[0] * 64 / 900), round(pygame.mouse.get_pos()[1] * 64 / 900)
						if button.rect.collidepoint(pos):
							self.level = 'level' + button.i

			# ---------- level generator -------------
			elif self.level[0:5] == 'level':
				for sprite in self.all_sprites: sprite.kill()
				self.player = Player(self.all_sprites)

				if self.level[-1] == '1':
					level_table = level1
					self.boss = Saturn(self.all_sprites, (600, 42), self.player, [self.all_sprites, self.enemy_group])
				elif self.level[-1] == '2':
					level_table = level2
					self.boss = Jupiter([self.all_sprites, self.obsticle_group], (600, 42), self.player)
				elif self.level[-1] == '3':
					level_table = level3
					self.boss = Mars(self.all_sprites, (600, 30), self.player, [self.all_sprites, self.enemy_group])

					for index in level_table[6]:
						i = level_table[6].index(index)
						Laser([self.all_sprites, self.laser_group], (level_table[6][i], 0), level_table[7][i], level_table[8][i])

				elif self.level[-1] == '4':
					level_table = level4
					# ------------- main boss -----------
					self.boss = Sun(
						[self.all_sprites, self.obsticle_group],
						(300, 35),
						self.player,
						[self.all_sprites, self.enemy_group],
					)

					for index in level_table[6]:
						i = level_table[6].index(index)
						Laser([self.all_sprites, self.laser_group], (level_table[6][i], 0), level_table[7][i], level_table[8][i])


				for text in level_table[1]:
					i = level_table[1].index(text)
					Text(self.all_sprites, self.font, text, level_table[2][i], (200, 200, 200))

				for pos in level_table[0]:
					SimpleEnemy([self.all_sprites, self.enemy_group], pos, self.player)

				for pos in level_table[3]:
					i = level_table[3].index(pos)

					start_pos = level_table[4][i][0]
					end_pos = level_table[4][i][1]
					speed = level_table[5][i]
					BlackHole([self.all_sprites, self.obsticle_group], pos, start_pos, end_pos, speed)

				past_level = self.level
				self.level = ''

			# ---------------- game --------------
			else:
				# update
				self.all_sprites.update(self.dt, offset=self.all_sprites.offset[0])

				# shoot
				if pygame.mouse.get_pressed()[0] and pygame.time.get_ticks() - self.last_shoot > 1000:
					self.last_shoot = pygame.time.get_ticks()
					Meteor(
						pos = self.player.rect.center,
						player = self.player,
						offset = self.all_sprites.offset[0],
						groups = [self.all_sprites, self.meteors],
					)

				if pygame.sprite.groupcollide(self.meteors, self.enemy_group, True, True):
					pygame.mixer.Sound.play(self.enemy_kill_sound)

				for sprite in pygame.sprite.spritecollide(self.player, self.laser_group, False):
					if sprite.active:
						self.level = past_level
						pygame.mixer.Sound.play(self.explosion_sound)

				if pygame.sprite.spritecollide(self.player, self.enemy_group, False, pygame.sprite.collide_mask):
					self.level = past_level
					pygame.mixer.Sound.play(self.explosion_sound)

				if pygame.sprite.spritecollide(self.player, self.obsticle_group, False, pygame.sprite.collide_mask):
					self.level = past_level
					pygame.mixer.Sound.play(self.black_hole_death_sound)

				if self.boss and pygame.sprite.spritecollide(self.boss, self.meteors, True, pygame.sprite.collide_mask):
					self.boss.health -= 10
					self.boss.text.kill()

					self.boss.text = Text(
						self.all_sprites,
						self.font,
						f'{self.boss.health}HP',
						(self.boss.rect.centerx, self.boss.rect.top - 5),
						(100, 250, 100),
					)

					if self.boss.health <= 0:
						self.boss.text.kill()
						self.boss.kill()
						self.boss = None
						self.boss_kill_time = pygame.time.get_ticks()

				if self.boss == None and pygame.time.get_ticks() - self.boss_kill_time > 2000:
					self.level = 'menu'

				# draw
				self.all_sprites.customize_draw(self.player)


			frame = pygame.transform.scale(self.display_surface, (WINDOW_WIDTH, WINDOW_HEIGHT))
			self.screen.blit(frame, frame.get_rect())
			pygame.display.update()


if __name__ == '__main__':
	game = Game()
	game.run()