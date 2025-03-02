from dataclasses import dataclass
from PIL import Image
import pygame


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


a
image = Image.new('P', (1000, 500), (0, 0, 0))
image2 = Image.fromarray(a)


end = True
while (end):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end = False
list = [4, 4, 4, 4]
print(list)
list += [5]
print(list)
del list[:1]
print(list)
print(tuptomath((67, 98)) // 10 != tuptomath((62, 98)) // 10)
