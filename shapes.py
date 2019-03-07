import pygame


class Rect:
	def __init__(self, screen, x, y, width, height, color):
		self.screen = screen
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.color = color

	def get_middle(self):
		return self.x + self.width // 2, self.y + self.height // 2

	def get_dimensions(self):
		return self.x, self.y, self.width, self.height

	def draw(self):
		pygame.draw.rect(self.screen, self.color, self.get_dimensions(), 1)


class Progressbar(Rect):
	def get_progress(self, progress):
		return self.x, self.y, self.width * progress, self.height

	def draw(self, progress=0):
		pygame.draw.rect(self.screen, self.color, self.get_dimensions(), 1)
		pygame.draw.rect(self.screen, self.color, self.get_progress(progress))
