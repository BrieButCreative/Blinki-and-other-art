import pygame
import os
import numpy
from dataclasses import dataclass, field
from typing import Optional
from PIL import Image, ImageOps

name = "main"
speed = 150

pygame.init()

# default color values
coloron = (255, 255, 255)
colorinv = (25, 50, 25)

# typical size of blinkies
screen = pygame.display.set_mode((1500, 200))
screen.fill(colorinv)
end = True
count = 0

filepath = os.path.dirname(os.path.realpath(__file__))


@dataclass
class tuptomath:
    tupel: tuple[int, int]

    def __floordiv__(self, int) -> tuple[int, int]:
        x = ""
        y = ""
        for num in self.tupel:
            if x == "":
                x = num // int
            else:
                y = num // int
        return ((x, y))                 # type: ignore

    def __mul__(self, int) -> tuple[int, int]:
        x = ""
        y = ""
        for num in self.tupel:
            if x == "":
                x = num * int
            else:
                y = num * int
        return ((x, y))                 # type: ignore

    def untupl(self) -> int:            # type: ignore
        for x in self.tupel:
            return (x)

    def untupr(self) -> int:            # type: ignore
        n = 0
        for x in self.tupel:
            if (n > 0):
                return (x)
            n += 1


@dataclass
class Screen:
    __mat: numpy.array = field(init=False, repr=False)      # type: ignore

    def __init__(self):
        self.__mat = numpy.zeros((150, 20))

    def generate(self):
        global current
        generating = True
        n = 0
        while (generating):
            if (os.path.exists(f'{filepath}/Blinki-{n}')):
                n += 1
                continue
            os.makedirs(f'{filepath}/Blinki-{n}')
            generating = False
            current = f'{filepath}/Blinki-{
                n}'

    def matout(self) -> list[list[bool]]:
        mat = []
        y = 19
        while (y >= 0):
            x = 149
            inner = []
            while (x >= 0):
                inner += [self.val(149 - x, 19 - y)]
                x -= 1
            mat += [inner]
            y -= 1
        return (mat)

    def matin(self, matrix: list[list[bool]]):
        ycord = 0
        for y in matrix:
            xcord = 0
            for x in y:
                self.__mat[xcord, ycord] = int(x)
                xcord += 1
            ycord += 1

    def val(self, x: int, y: int) -> bool:
        return (bool(self.__mat[x, y]))

    def change(self, x: int, y: int):
        if (int(self.__mat[x, y])):
            self.__mat[x, y] = False
        else:
            self.__mat[x, y] = True

    def reset(self):
        self.__mat = numpy.zeros((150, 20))

    def differ(self, matrix: list[list[bool]]) -> list[tuple[int, int]]:
        y = 0
        out = []
        for cory in matrix:
            x = 0
            for corx in cory:
                if (self.__mat[x, y] != int(corx)):
                    out += [(x * 10, y * 10)]
                x += 1
            y += 1
        return (out)

    def out(self):
        global count
        global current
        global view
        X = 0
        Y = 0
        while (X < 150):
            while (Y < 20):
                if (view.val(X, Y)):
                    pygame.draw.line(
                        screen, coloron, (X * 10, Y * 10), (X * 10 + 9, Y * 10))
                    pygame.draw.line(
                        screen, coloron, (X * 10, Y * 10), (X * 10, Y * 10 + 9))
                else:
                    pygame.draw.line(screen, colorinv,
                                     (X * 10, Y * 10), (X * 10 + 9, Y * 10))
                    pygame.draw.line(screen, colorinv,
                                     (X * 10, Y * 10), (X * 10, Y * 10 + 9))
                Y += 1
            X += 1
            Y = 0
        pygame.image.save(screen, f'{current}/frame-{count}')
        with Image.open(f'{current}/frame-{count}') as im:
            ImageOps.fit(im, (150, 20)).save(f'{current}/frame-{count}.jpg')
        os.remove(f'{current}/frame-{count}')
        X = 0
        Y = 0
        while (X < 150):
            while (Y < 20):
                if (view.val(X, Y)):
                    pygame.draw.line(screen, colorinv,
                                     (X * 10, Y * 10), (X * 10 + 9, Y * 10))
                    pygame.draw.line(screen, colorinv,
                                     (X * 10, Y * 10), (X * 10, Y * 10 + 9))
                else:
                    pygame.draw.line(
                        screen, coloron, (X * 10, Y * 10), (X * 10 + 9, Y * 10))
                    pygame.draw.line(
                        screen, coloron, (X * 10, Y * 10), (X * 10, Y * 10 + 9))
                Y += 1
            X += 1
            Y = 0
        pygame.display.update()
        count += 1


def animate():
    global current
    global count
    n = 0
    images = []
    while (n < count):
        images.append(Image.open(f'{current}/frame-{n}.jpg'))
        n += 1
    images[0].save(f'{current}/final-gif.gif', save_all=True,
                   append_images=images[1:], duration=speed, loop=0)


def fill():
    global backsteps
    global foresteps
    global view
    global end
    fill = True
    while (fill):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fill = False
                end = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                corner = pygame.mouse.get_pressed()
                n = 0
                for c in corner:
                    if n == 0 and c:
                        corn = False
                        fill = False
                    elif n == 2 and c:
                        corn = True
                        fill = False
                    n += 1
                if (fill is False):
                    x = -1
                    y = -1
                    for cord in pygame.mouse.get_pos():
                        if (x == -1):
                            x = cord // 10
                        else:
                            y = cord // 10
                    base = view.val(x, y)
                    color((x * 10, y * 10))
                    compare(base, [(x, y)], corn)
                    fill = True
                    backsteps += [view.matout()]
                    foresteps = ['Empty']
            elif event.type == pygame.KEYDOWN:
                if pygame.key.get_pressed()[pygame.K_RSHIFT] and pygame.key.get_pressed()[pygame.K_BACKSPACE] or pygame.key.get_pressed()[pygame.K_LSHIFT] and pygame.key.get_pressed()[pygame.K_BACKSPACE]:
                    fore()
                elif event.key == pygame.K_BACKSPACE:
                    back()
                elif event.key == pygame.K_f:
                    fill = False
                elif event.key == pygame.K_RETURN:
                    view.out()
                elif event.key == pygame.K_a:
                    ...
                elif event.key == pygame.K_l:
                    line()
                    fill = False
                elif event.key == pygame.K_r:
                    view.reset()
                    screen.fill(colorinv)
                    setup()
                    backsteps += [view.matout()]
                    foresteps = ['Empty']
                elif event.key == pygame.K_i:
                    invert()
                    backsteps += [view.matout()]
                    foresteps = ['Empty']
    return (view)


def compare(base: bool, cords: list[tuple[int, int]], corner: bool):
    global view
    filling = True
    while (filling):
        for cor in cords:
            x = -1
            y = -1
            for c in cor:
                if (x == -1):
                    x = c
                else:
                    y = c
            cords.remove(cor)
            if (y + 1 < 20 and view.val(x, y + 1) == base):
                color((x * 10, (y + 1) * 10))
                cords += [(x, y + 1)]
            if (y + 1 < 20 and x + 1 < 150 and corner and view.val(x + 1, y + 1) == base):
                color(((x + 1) * 10, (y + 1) * 10))
                cords += [(x + 1, y + 1)]
            if (x + 1 < 150 and view.val(x + 1, y) == base):
                color(((x + 1) * 10, y * 10))
                cords += [(x + 1, y)]
            if (y - 1 >= 0 and x + 1 < 150 and corner and view.val(x + 1, y - 1) == base):
                color(((x + 1) * 10, (y - 1) * 10))
                cords += [(x + 1, y - 1)]
            if (y - 1 >= 0 and view.val(x, y - 1) == base):
                color((x * 10, (y - 1) * 10))
                cords += [(x, y - 1)]
            if (y - 1 >= 0 and x - 1 >= 0 and corner and view.val(x - 1, y - 1) == base):
                color(((x - 1) * 10, (y - 1) * 10))
                cords += [(x - 1, y - 1)]
            if (x - 1 >= 0 and view.val(x - 1, y) == base):
                color(((x - 1) * 10, y * 10))
                cords += [(x - 1, y)]
            if (y + 1 < 20 and x - 1 >= 0 and corner and view.val(x - 1, y + 1) == base):
                color(((x - 1) * 10, (y + 1) * 10))
                cords += [(x - 1, y + 1)]
        if (cords == []):
            filling = False


def line():
    global backsteps
    global foresteps
    global screen
    global end
    global view
    global coloron
    global colorinv
    draw = True
    while (draw):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                draw = False
                end = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                thirdview = Screen()
                thirdview.matin(view.matout())
                start = pygame.mouse.get_pos()
                startx = tuptomath(start).untupl()
                starty = tuptomath(start).untupr()
                drawing = True
                aimxo = -1
                aimyo = -1
                aimlisto = []
                while (drawing):
                    aim = pygame.mouse.get_pos()
                    aimx = tuptomath(aim).untupl()
                    aimy = tuptomath(aim).untupr()
                    if (aimx // 10 != aimxo or aimy // 10 != aimyo):
                        aimlist = closest((startx, starty), (aimx, aimy))
                    for cord in aimlisto:
                        if (cord not in aimlist):
                            thirdview = color(cord, thirdview)
                    for cord in aimlist:
                        if (cord not in aimlisto):
                            thirdview = color(cord, thirdview)
                    aimxo = aimx // 10
                    aimyo = aimy // 10
                    aimlisto = aimlist
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            draw = False
                            end = False
                            drawing = False
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            for tup in aimlist:
                                color(tup)
                            drawing = False
                            backsteps += [view.matout()]
                            foresteps = ['Empty']
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_l:
                                for cord in view.differ(thirdview.matout()):
                                    color(cord, thirdview)
                                draw = False
                                drawing = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_l:
                    draw = False
                elif pygame.key.get_pressed()[pygame.K_RSHIFT] and pygame.key.get_pressed()[pygame.K_BACKSPACE] or pygame.key.get_pressed()[pygame.K_LSHIFT] and pygame.key.get_pressed()[pygame.K_BACKSPACE]:
                    fore()
                elif event.key == pygame.K_BACKSPACE:
                    back()
                elif event.key == pygame.K_RETURN:
                    view.out()
                elif event.key == pygame.K_a:
                    ...
                elif event.key == pygame.K_f:
                    draw = False
                    fill()
                elif event.key == pygame.K_r:
                    view.reset()
                    screen.fill(colorinv)
                    setup()
                    backsteps += [view.matout()]
                    foresteps = ['Empty']
                elif event.key == pygame.K_i:
                    invert()
                    backsteps += [view.matout()]
                    foresteps = ['Empty']


def closest(begin: tuple[int, int], end: tuple[int, int]) -> list[tuple[int, int]]:
    def dist(x1: int, y1: int, x2: int, y2: int) -> float:
        return (((x1 - x2) ** 2 + (y1 - y2) ** 2) ** (1 / 2))

    testcordx = tuptomath(begin).untupl() // 10
    testcordy = tuptomath(begin).untupr() // 10
    endx = tuptomath(end).untupl() // 10
    endy = tuptomath(end).untupr() // 10
    begin = tuptomath(tuptomath(begin) // 10) * 10
    ret = [begin]
    lineage = True
    if (testcordx == endx and testcordy == endy):
        lineage = False
    while (lineage):
        shortest = min(dist(testcordx + 1, testcordy, endx, endy), dist(testcordx, testcordy + 1, endx, endy),
                       dist(testcordx, testcordy - 1, endx,
                            endy), dist(testcordx - 1, testcordy, endx, endy),
                       dist(testcordx + 1, testcordy + 1, endx,
                            endy), dist(testcordx - 1, testcordy - 1, endx, endy),
                       dist(testcordx + 1, testcordy - 1, endx, endy), dist(testcordx - 1, testcordy + 1, endx, endy))
        if (dist(testcordx - 1, testcordy - 1, endx, endy) == shortest):
            testcordx -= 1
            testcordy -= 1
            ret += [(testcordx * 10, testcordy * 10)]
            if (dist(testcordx, testcordy + 1, endx, endy) < dist(testcordx + 1, testcordy, endx, endy)):
                ret += [(testcordx * 10, (testcordy + 1) * 10)]
            else:
                ret += [((testcordx + 1) * 10, testcordy * 10)]
        elif (dist(testcordx + 1, testcordy + 1, endx, endy) == shortest):
            testcordx += 1
            testcordy += 1
            ret += [(testcordx * 10, testcordy * 10)]
            if (dist(testcordx, testcordy - 1, endx, endy) < dist(testcordx - 1, testcordy, endx, endy)):
                ret += [(testcordx * 10, (testcordy - 1) * 10)]
            else:
                ret += [((testcordx - 1) * 10, testcordy * 10)]
        elif (dist(testcordx + 1, testcordy - 1, endx, endy) == shortest):
            testcordx += 1
            testcordy -= 1
            ret += [(testcordx * 10, testcordy * 10)]
            if (dist(testcordx, testcordy + 1, endx, endy) < dist(testcordx - 1, testcordy, endx, endy)):
                ret += [(testcordx * 10, (testcordy + 1) * 10)]
            else:
                ret += [((testcordx - 1) * 10, testcordy * 10)]
        elif (dist(testcordx - 1, testcordy + 1, endx, endy) == shortest):
            testcordx -= 1
            testcordy += 1
            ret += [(testcordx * 10, testcordy * 10)]
            if (dist(testcordx, testcordy - 1, endx, endy) < dist(testcordx + 1, testcordy, endx, endy)):
                ret += [(testcordx * 10, (testcordy - 1) * 10)]
            else:
                ret += [((testcordx + 1) * 10, testcordy * 10)]
        elif (dist(testcordx, testcordy + 1, endx, endy) == shortest):
            testcordy += 1
            ret += [(testcordx * 10, testcordy * 10)]
        elif (dist(testcordx, testcordy - 1, endx, endy) == shortest):
            testcordy -= 1
            ret += [(testcordx * 10, testcordy * 10)]
        elif (dist(testcordx + 1, testcordy, endx, endy) == shortest):
            testcordx += 1
            ret += [(testcordx * 10, testcordy * 10)]
        elif (dist(testcordx - 1, testcordy, endx, endy) == shortest):
            testcordx -= 1
            ret += [(testcordx * 10, testcordy * 10)]
        if (testcordx == endx and testcordy == endy):
            lineage = False
    return (ret)


def back():
    global backsteps
    global foresteps
    global view
    backsteps.reverse()
    if (backsteps[0] != 'start'):
        foresteps += [backsteps[0]]
        del backsteps[:1]
        if (backsteps[0] != 'start'):
            state = Screen()
            state.matin(backsteps[0])           # type: ignore
            colorin = state.differ(view.matout())
            for col in colorin:
                color(col)
    if (backsteps[0] == 'start'):
        view.reset()
        screen.fill(colorinv)
        setup()
    backsteps.reverse()


def fore():
    global backsteps
    global foresteps
    global view
    foresteps.reverse()
    if (foresteps[0] != 'Empty'):
        state = Screen()
        state.matin(foresteps[0])           # type: ignore
        colorin = state.differ(view.matout())
        for col in colorin:
            color(col)
        del foresteps[:1]
        backsteps += [view.matout()]
    foresteps.reverse()


def invert():
    x = 0
    y = 0
    while (x < 1500):
        while (y < 200):
            color((x, y))
            y += 10
        x += 10
        y = 0


def colorchange():
    global view
    global coloron
    global colorinv


def setup():
    screen.fill(colorinv)
    x = 0
    y = 0
    while (x < 1500):
        pygame.draw.line(screen, coloron, (x, 0), (x, 200))
        pygame.draw.line(screen, coloron, (0, y), (1500, y))
        x += 10
        y += 10
    pygame.display.update()


def color(pos: tuple[int, int], vie: Optional[Screen] = None) -> Screen:
    global view
    global screen
    global colorinv
    global coloron
    if (vie is None):
        x = -1
        y = -1
        for cord in pos:
            if (x != -1):
                y = cord
            if (y == -1):
                x = cord
        X = x // 10
        Y = y // 10
        rectX = X * 10
        rectY = Y * 10
        if (view.val(X, Y)):
            pygame.draw.rect(screen, colorinv, (rectX, rectY, 10, 10))
            pygame.draw.line(screen, coloron, (rectX, rectY),
                             (rectX + 9, rectY))
            pygame.draw.line(screen, coloron, (rectX, rectY),
                             (rectX, rectY + 9))
        else:
            pygame.draw.rect(screen, coloron, (rectX, rectY, 10, 10))
            pygame.draw.line(screen, colorinv, (rectX, rectY),
                             (rectX + 9, rectY))
            pygame.draw.line(screen, colorinv, (rectX, rectY),
                             (rectX, rectY + 9))
        view.change(X, Y)
        pygame.display.update()
        return (view)
    else:
        x = -1
        y = -1
        for cord in pos:
            if (x != -1):
                y = cord
            if (y == -1):
                x = cord
        X = x // 10
        Y = y // 10
        rectX = X * 10
        rectY = Y * 10
        if (vie.val(X, Y)):
            pygame.draw.rect(screen, colorinv, (rectX, rectY, 10, 10))
            pygame.draw.line(screen, coloron, (rectX, rectY),
                             (rectX + 9, rectY))
            pygame.draw.line(screen, coloron, (rectX, rectY),
                             (rectX, rectY + 9))
        else:
            pygame.draw.rect(screen, coloron, (rectX, rectY, 10, 10))
            pygame.draw.line(screen, colorinv, (rectX, rectY),
                             (rectX + 9, rectY))
            pygame.draw.line(screen, colorinv, (rectX, rectY),
                             (rectX, rectY + 9))
        vie.change(X, Y)
        pygame.display.update()
        return (vie)


setup()
view = Screen()
view.generate()
backsteps = ['start']
foresteps = ['Empty']
while (end):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            check = pygame.mouse.get_pressed()
            n = 0
            yes = False
            for boo in check:
                if (n == 0 and boo):
                    yes = True
                n = 1
            if (yes):
                base = view.val(tuptomath(pygame.mouse.get_pos()).untupl(
                ) // 10, tuptomath(pygame.mouse.get_pos()).untupr() // 10)
                wait = True
                pos = (-1, -1)
                while (wait):
                    if (tuptomath(pygame.mouse.get_pos()).untupl() // 10 < 150 and tuptomath(pygame.mouse.get_pos()).untupl() // 10 >= 0 and tuptomath(pygame.mouse.get_pos()).untupr() // 10 < 20 and tuptomath(pygame.mouse.get_pos()).untupr() // 10 >= 0 and tuptomath(pygame.mouse.get_pos()) // 10 != tuptomath(pos) // 10 and base == view.val(tuptomath(pygame.mouse.get_pos()).untupl() // 10, tuptomath(pygame.mouse.get_pos()).untupr() // 10)):
                        pos = pygame.mouse.get_pos()
                        color(pos)
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONUP:
                            wait = False
                backsteps += [view.matout()]
                foresteps = ['Empty']
        elif event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_RSHIFT] and pygame.key.get_pressed()[pygame.K_BACKSPACE] or pygame.key.get_pressed()[pygame.K_LSHIFT] and pygame.key.get_pressed()[pygame.K_BACKSPACE]:
                fore()
            elif event.key == pygame.K_BACKSPACE:
                back()
            elif event.key == pygame.K_RETURN:
                view.out()
            elif event.key == pygame.K_a:
                ...  # free potential add-on is a preview and 'custom frame editor
            elif event.key == pygame.K_f:
                fill()
            elif event.key == pygame.K_c:
                colorchange()
            elif event.key == pygame.K_l:
                line()
            elif event.key == pygame.K_r:
                view.reset()
                screen.fill(colorinv)
                setup()
                backsteps += [view.matout()]
                foresteps = ['Empty']
            elif event.key == pygame.K_i:
                invert()
                backsteps += [view.matout()]
                foresteps = ['Empty']


animate()
pygame.time.Clock().tick(1080)
pygame.quit()
