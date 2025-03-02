from dataclasses import dataclass
from PIL import Image
import pygame
import numpy


pygame.init()

screen = pygame.display.set_mode((1000, 500))

pygame.draw.rect(screen, (255, 125, 42), (10, 50, 40, 10))
pygame.display.update()


@dataclass
class tuptomath:
    tupel: tuple[int, int]

    def __floordiv__(self, int):
        x = ""
        y = ""
        for num in self.tupel:
            if x == "":
                x = num // int
            else:
                y = num // int
        return (x, y)



a = []
i = 0
j = 0
while (i < 500):
    b = []
    while (j < 1000):
        b.append((255, 255, 255))
        j += 1
    a.append(b)
    j = 0
    i += 1
# for i in range(50, 100):
#     for j in range(100, 200):
#         a[j][i] = (255, 125, 42)
a = numpy.array(a)

Image.new('P', (1000, 500), (255, 125, 42)).show()
image2 = Image.fromarray(a, 'RGB').show()


list = [4, 4, 4, 4]
print(list)
list += [5]
print(list)
del list[:1]
print(list)
print(tuptomath((67, 98)) // 10 != tuptomath((62, 98)) // 10)
