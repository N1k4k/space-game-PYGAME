WINDOW_WIDTH, WINDOW_HEIGHT = 900, 900
REZOLUTION = 64
ccenter = REZOLUTION / 2

level1 = [
	# simple enemys
	[
		(200, ccenter), (250, 10), (250, 25), (250, 40), (250, 55), (280, 10), (280, 25), (280, 40),
	 	(280, 55), (410, ccenter), (430, ccenter), (450, ccenter)
	],
	# text
	['Press Left', 'Click To Shoot', "Don't Touch", 'Black Holes', 'Defeat the', 'Boss'],
	[(150, 10), (150, 20), (320, 10), (320, 20), (500, 10), (500, 20)],
	# black hole
	[(350, 45), (370, 10)], #pos
	[((350, 45), (360, 15)), ((370, 10), (370, 50))], #move
	[4, 3], #speed
]

level2 = [
	# simple enemys
	[(150, 20), (170, 50), (150, 50), (170, 20), (200, 10), (200, 20), (200, 30), (200, 40), (200, 50), (200, 60),
	(350, 10), (350, 20), (350, 30), (350, 40), (350, 50), (350, 60),
	],
	# text
	[],
	[],
	# black hole
	[(60, ccenter), (100, 54), (100, 12), (250, 0), (270, 0), (290, 0), (410, 5), (410, 60)], #pos
	[((60, ccenter), (100, ccenter)), ((100, 54), (60, 54)), ((100, 12), (60, 12)), ((250, 0), (250, 64)), ((270, 0), (270, 64)),
	((290, 0), (290, 64)), ((410, 5), (450, 60)), ((410, 60), (450, 5)),
	], #move
	[3, 2, 1, 5, 3, 2, 2, 3], #speed
]

level3 = [
	# simple enemys
	[(150, ccenter), (170, ccenter), (280, 10), (280, 20), (280, 30), (280, 40), (280, 50), (280, 60), (300, 20), (300, 40),
	(450, 50), (470, 50), (460, 20)],
	# text
	[],
	[],
	# black hole
	[(170, 10), (170, 50), (200, 50), (230, 50), (410, ccenter)], #pos
	[((170, 10), (170, 10)), ((170, 50), (200, 10)), ((200, 50), (230, 10)), ((230, 50), (230, 50)), 
	((410, ccenter), (500, ccenter)), ], #move
	[0, 2, 2, 0, 5], #speed
	# laser
	[80, 100, 350, 390],
	[2500, 1500, 2000, 2100],
	[10, 5, 8, 8],
]

level4 = [
	# simple enemys
	[],
	# text
	[],
	[],
	# black hole
	[], #speed
	# laser
	[],
	[],
	[],
]