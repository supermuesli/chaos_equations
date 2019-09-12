import sys, pygame, math, color, random
from copy import copy

pygame.init()

size = width, height = 1280, 768

screen = pygame.display.set_mode(size)

framebuffer = [[[0, 0, 0, 255] for y in range(height)] for x in range(width)]

def cord(x):
	return abs(int(math.sin(x[0])*width))-1, abs(int(math.sin(x[1])*height))-1

# def particle motion functions
def fuck(x, y, t):
	return math.sin(2*x + 3*x**2 - 2*y - 2*y**2) + math.sin(t*x) - math.cos(t*y), \
	       math.cos(2*x + 3*x**2 - 2*y - 2*y**2 + math.sin(t*x) - math.cos(t*y))

def guck(x, y, t):
	return math.sin(x+y*t), math.cos(y+x*t)

def nuck(x, y, t):
	return -x**2 + x*t + y, x**2 - y**2 - t**2 - x*y + y*t - x + y

# initial time & time step size
tss = 10**(-4)
t = 0.024561

# amount of particles
n = 10000

# colors of particles
#colors = [[255, 255, 255, 255] for i in range(n)]

colors = [[random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)] \
          for i in range(n)]

# initial positions for single particles
x0s = [200 + i  for i in range(n)]
y0s = [200 for i in range(n)]

# decay rate in range [0, 1] where 1 means never decay and 0 means decay immediately
decay_rate = 0.9

# optimization. do not iterate over coordinates that have decayed
painted = []

# video information
frame_no = 0
total_frames = 60*60
zround = len(str(total_frames))

while 1:
	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()

	for i in painted:
		framebuffer[i[0]][i[1]][0] = int(framebuffer[i[0]][i[1]][0]*decay_rate)
		framebuffer[i[0]][i[1]][1] = int(framebuffer[i[0]][i[1]][1]*decay_rate)
		framebuffer[i[0]][i[1]][2] = int(framebuffer[i[0]][i[1]][2]*decay_rate)

		screen.set_at((i[0], i[1]), framebuffer[i[0]][i[1]])

	for j in range(len(x0s)):
		fuck_x0, fuck_y0 = cord(fuck(x0s[j], y0s[j], t))
		framebuffer[fuck_x0][fuck_y0] = copy(colors[j])
		painted += [(fuck_x0, fuck_y0)]
		screen.set_at((fuck_x0, fuck_y0), colors[j])


	pc = copy(painted)
	deleted = 0
	for i in range(len(pc)):
		if framebuffer[pc[i][0]][pc[i][1]] == [0, 0, 0, 255]:
			del(painted[i - deleted])
			deleted += 1

	pygame.display.flip()
	pygame.image.save(screen, 'video/' + str(frame_no).zfill(zround) + '.png')
	print(frame_no, '/', total_frames)
	
	frame_no += 1
	t += tss