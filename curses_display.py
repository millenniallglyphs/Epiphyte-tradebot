import curses
import random
import time
import traceback

def generateSky(y, x, req):
	sky = []

	xsky = []

	for iy in range(0, y/2):
		for ix in range(0, x):
			xsky.append(["g"])
		sky.append(xsky)
		xsky = []

	return sky

def generateMy(y, x, req):
	my = []

        xmy = []

        for iy in range(y/2, y):
                for ix in range(0, x):
                        xmy.append(["b"])
                my.append(xmy)
                xmy = []

        return my



def renderSky(screen, sky, my):
	screen.clear()
	try:
		for i in sky:
			for x in i:
				screen.addstr(x[0])
			screen.addstr("\n")
		for i in my:
			for x in i:
				screen.addstr(x[0])
			screen.addstr("\n")
	except curses.error:
		pass
	screen.refresh()

def main():
	try:
		screen = curses.initscr()
		size = screen.getmaxyx()
		sky = generateSky(size[0]-1, size[1]-1, 0.025)
		my = generateMy(size[0]-1, size[1]-1, 0.025)

		while True:
			if size[0] != screen.getmaxyx()[0] and size[1] != screen.getmaxyx()[1]:
				size = screen.getmaxyx()
				sky = generateSky(size[0]-1, size[1]-1, 0.05)
				my = generateSky(size[0]-1, size[1]-1, 0.05)
 
			renderSky(screen, sky, my)
			time.sleep(1)

		curses.endwin()

	except KeyboardInterrupt:
		curses.endwin()

	except:
		curses.endwin()
		traceback.print_exc()


main()
