import random
import curses
import math
import sys

if len(sys.argv) > 1:
    try:
        DIM = int(sys.argv[1])
    except ValueError:
        DIM = 4
else:
    DIM = 4


def drawinfo(w, sh, sw):
    w.clrtobot()
    w.erase()

    center = [math.floor(sh / 2), math.floor(sw / 2)]

    for i in range(sw):
        w.addch(sh - 2, i, "_")
        w.addch(1, i, "_")

    w.addstr(sh - 1, 0, "q for coming back to game")
    w.addstr(0, 0, "Kappa v. 1.0.1")

    w.addstr(center[0]-5, 0, "The goal of the game is getting a K on the grid," )
    w.addstr(center[0]-4, 0, "but don't worry, once you win you'll be able to go on!" )
    w.addstr(center[0]-2, 0, "You can change the grid size by putting the desired size as argument")

    w.addstr(center[0], 0, "Thanks for playing Kappa")
    w.addstr(center[0]+1, 0, "This game is brought to you by Lorenzo De Nisi")
    w.addstr(center[0]+2, 0, "https://github.com/lorenzodenisi")
    w.addstr(center[0]+5, 0, "Version: 1.0.1")
    w.addstr(center[0]+6, 0, "Source code: https://github.com/lorenzodenisi/kappa")
    key = 0
    while key != 113:
        key = w.getch()



def drawlayout(w, sh, sw, nums, points):
    w.clrtobot()
    w.erase()

    if sh < DIM * 2 + 1 or sw < DIM * 4 + 1:
        return True

    for i in range(sw):
        w.addch(sh-2, i, "_")
        w.addch(1, i, "_")
        w.addch(sh-4, i, "_")

    w.addstr(0, 0, "Kappa v. 1.0.1")
    w.addstr(sh - 3, 0, "q : quit | r : restart")
    w.addstr(sh - 1, 0, "POINTS: "+points.__str__())
    w.addstr(sh - 1, sw-15, "DIMENSION: " + DIM.__str__())

    center = [math.floor(sh / 2), math.floor(sw / 2)]
    pos = []
    topleft = [center[0] - DIM, center[1] - DIM * 2]

    for i in range(DIM + 1):
        w.addch(topleft[0] + i * 2, topleft[1], '+')
        for j in range(DIM):
            w.addstr(topleft[0] + i * 2, topleft[1] + j * 4 + 1, '---+')

    for i in range(DIM):
        for j in range(DIM + 1):
            w.addch(topleft[0] + i * 2 + 1, topleft[1] + j * 4, '|')

    for i in range(DIM):
        pos.append([])
        for j in range(DIM):
            pos[i].append([topleft[0] + 1 + i * 2, topleft[1] + 2 + j * 4])

    for i in range(DIM):
        for j in range(DIM):
            if nums[i][j]:
                w.addch(pos[i][j][0], pos[i][j][1], 64 + nums[i][j])
            # w.addstr(j+i*4, 0, (pos[i][j].__str__() + i.__str__() + j.__str__()))

    return True


# main


s = curses.initscr()
curses.curs_set(0)
sh, sw = s.getmaxyx()
w = curses.newwin(sh, sw, 0, 0)
w.keypad(1)

newgame = True

# ACTUAL LOOP
while True:

    if newgame:
        # GENERATING STARTING LETTERS
        newgame=False
        nums = []
        for i in range(DIM):
            nums.append([])
            for j in range(DIM):
                nums[i].append(0)

        startpos = []
        while len(startpos) < 2:
            newpos = [random.randint(0, DIM - 1), random.randint(0, DIM - 1)]
            if not startpos.__contains__(newpos):
                startpos.append(newpos)

        for pos in startpos:
            nums[pos[0]][pos[1]] = 1

        points = 2


    sh, sw = s.getmaxyx()  # refresh also window dimension
    if not drawlayout(w, sh, sw, nums, points):
        curses.endwin()
        break

    dir = w.getch()

    if dir != -1:

        moved = False

        if dir == 105:          # i key
            drawinfo(w, sh, sw)

        if dir == 113:          # q key
            break

        if dir == 114:
            newgame = True


        if dir == curses.KEY_DOWN:
            for j in range(DIM):  # cols
                for i in range(DIM - 1, -1, -1):  # rows
                    if nums[i][j] != 0:
                        n = nums[i][j]
                        startpos = i
                        nums[i][j] = 0
                        while True:
                            i += 1
                            if i >= DIM:  # hit the wall
                                nums[i - 1][j] = n

                                if startpos != i - 1:
                                    moved = True

                                break
                            else:
                                if nums[i][j] != 0:  # find another char
                                    if nums[i][j] == n:  # if same, come together
                                        nums[i][j] = n + 1
                                    else:  # otherwise stack
                                        nums[i - 1][j] = n

                                        if startpos != i - 1:
                                            moved = True

                                    break

        if dir == curses.KEY_UP:
            for j in range(DIM):  # cols
                for i in range(DIM):  # rows
                    if nums[i][j] != 0:
                        n = nums[i][j]
                        startpos = i
                        nums[i][j] = 0
                        while True:
                            i -= 1
                            if i < 0:  # hit the wall
                                nums[i + 1][j] = n

                                if startpos != i + 1:
                                    moved = True
                                break
                            else:
                                if nums[i][j] != 0:  # find another char
                                    if nums[i][j] == n:  # if same, come together
                                        nums[i][j] = n + 1
                                    else:  # otherwise stack
                                        nums[i + 1][j] = n
                                        if startpos != i + 1:
                                            moved = True
                                    break

        if dir == curses.KEY_LEFT:
            for i in range(DIM):  # rows
                for j in range(DIM):  # cols
                    if nums[i][j] != 0:
                        n = nums[i][j]
                        startpos = j
                        nums[i][j] = 0
                        while True:
                            j -= 1
                            if j < 0:  # hit the wall
                                nums[i][j + 1] = n

                                if startpos != j + 1:
                                    moved = True

                                break
                            else:
                                if nums[i][j] != 0:  # find another char
                                    if nums[i][j] == n:  # if same, come together
                                        nums[i][j] = n + 1
                                    else:  # otherwise stack
                                        nums[i][j + 1] = n

                                        if startpos != j + 1:
                                            moved = True

                                    break

        if dir == curses.KEY_RIGHT:
            for i in range(DIM):  # rows
                for j in range(DIM - 1, -1, -1):  # cols
                    if nums[i][j] != 0:
                        n = nums[i][j]
                        startpos = j
                        nums[i][j] = 0
                        while True:
                            j += 1
                            if j >= DIM:  # hit the wall
                                nums[i][j - 1] = n

                                if startpos != j - 1:
                                    moved = True

                                break
                            else:
                                if nums[i][j] != 0:  # find another char
                                    if nums[i][j] == n:  # if same, come together
                                        nums[i][j] = n + 1
                                    else:  # otherwise stack
                                        nums[i][j - 1] = n

                                        if startpos != j - 1:
                                            moved = True

                                    break

        if moved and (
                dir == curses.KEY_DOWN or dir == curses.KEY_UP or dir == curses.KEY_LEFT or dir == curses.KEY_RIGHT):
            newnum = [random.randint(0, DIM - 1), random.randint(0, DIM - 1)]

            while nums[newnum[0]][newnum[1]] != 0:
                newnum = [random.randint(0, DIM - 1), random.randint(0, DIM - 1)]

            nums[newnum[0]][newnum[1]] = 1
            points += 1

    w.refresh()

curses.endwin()
