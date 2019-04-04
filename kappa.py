import random
import curses
import math


def drawlayout(w, sh, sw, nums):
    w.clrtobot()
    w.erase()

    # w.addstr(0, 0, sh.__str__())
    if sh < 9 or sw < 17:
        return True

    center = [math.floor(sh/2), math.floor(sw/2)]
    # print(center)

    w.addstr(center[0], center[1]-8,        '+---+---+---+---+')
    w.addstr(center[0] - 1, center[1] - 8,  '|   |   |   |   |')
    w.addstr(center[0] - 2, center[1] - 8,  '+---+---+---+---+')
    w.addstr(center[0] - 3, center[1] - 8,  '|   |   |   |   |')
    w.addstr(center[0] - 4, center[1] - 8,  '+---+---+---+---+')
    w.addstr(center[0] + 1, center[1] - 8,  '|   |   |   |   |')
    w.addstr(center[0] + 2, center[1] - 8,  '+---+---+---+---+')
    w.addstr(center[0] + 3, center[1] - 8,  '|   |   |   |   |')
    w.addstr(center[0] + 4, center[1] - 8,  '+---+---+---+---+')

    pos = []

    topleft = [center[0]-4, center[1]-4*2]

    for i in range(4):
        pos.append([])
        for j in range(4):
            pos[i].append([topleft[0]+1+i*2, topleft[1]+2+j*4])

    for i in range(4):
        for j in range(4):
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

# GENERATING STARTING LETTERS
nums = []
for i in range(4):
    nums.append([])
    for j in range(4):
        nums[i].append(0)

startpos = []
while len(startpos) < 2:
    newpos = [random.randint(0, 3), random.randint(0, 3)]
    if not startpos.__contains__(newpos):
        startpos.append(newpos)

for pos in startpos:
    nums[pos[0]][pos[1]] = 1

# ACTUAL LOOP
while True:
    sh, sw = s.getmaxyx()  # refresh also window dimension
    if not drawlayout(w, sh, sw, nums):
        curses.endwin()
        break

    dir = w.getch()

    if dir != -1:

        moved = False

        if dir == curses.KEY_DOWN:
            for j in range(4):  # cols
                for i in range(3, -1, -1):  # rows
                    if nums[i][j] != 0:
                        n = nums[i][j]
                        startpos = i
                        nums[i][j] = 0
                        while True:
                            i += 1
                            if i >= 4:  # hit the wall
                                nums[i - 1][j] = n

                                if startpos != i+1:
                                    moved = True

                                break
                            else:
                                if nums[i][j] != 0:  # find another char
                                    if nums[i][j] == n:  # if same, come together
                                        nums[i][j] = n + 1
                                    else:  # otherwise stack
                                        nums[i - 1][j] = n

                                        if startpos != i + 1:
                                            moved = True

                                    break

        if dir == curses.KEY_UP:
            for j in range(4):  # cols
                for i in range(4):  # rows
                    if nums[i][j] != 0:
                        n = nums[i][j]
                        startpos = i
                        nums[i][j] = 0
                        while True:
                            i -= 1
                            if i < 0:  # hit the wall
                                nums[i + 1][j] = n

                                if startpos != i-1:
                                    moved = True
                                break
                            else:
                                if nums[i][j] != 0:  # find another char
                                    if nums[i][j] == n:  # if same, come together
                                        nums[i][j] = n + 1
                                    else:  # otherwise stack
                                        nums[i + 1][j] = n
                                        if startpos != i-1:
                                            moved = True
                                    break

        if dir == curses.KEY_LEFT:
            for i in range(4):  # rows
                for j in range(4):  # cols
                    if nums[i][j] != 0:
                        n = nums[i][j]
                        startpos = j
                        nums[i][j] = 0
                        while True:
                            j -= 1
                            if j < 0:  # hit the wall
                                nums[i][j + 1] = n

                                if startpos != j+1:
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
            for i in range(4):  # rows
                for j in range(3, -1, -1):  # cols
                    if nums[i][j] != 0:
                        n = nums[i][j]
                        startpos = j
                        nums[i][j] = 0
                        while True:
                            j += 1
                            if j >= 4:  # hit the wall
                                nums[i][j - 1] = n

                                if startpos != j-1:
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

        if moved and (dir == curses.KEY_DOWN or dir == curses.KEY_UP or dir == curses.KEY_LEFT or dir == curses.KEY_RIGHT):
            newnum = [random.randint(0, 3), random.randint(0, 3)]

            while nums[newnum[0]][newnum[1]] != 0:
                newnum = [random.randint(0, 3), random.randint(0, 3)]

            nums[newnum[0]][newnum[1]] = 1

    w.refresh()

curses.endwin()
curses.curs_set(1)
