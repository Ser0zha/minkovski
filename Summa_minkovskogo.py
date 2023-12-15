from itertools import *
from pygame import *
from scipy.spatial import *


# выпуклая оболочка
def jarvis_march(points):
    result = [points[0]]
    for point in points[1:]:
        new_result1 = []
        for result_point in result:
            if result_point.y < point.y:
                new_result1.append(result_point)
            elif result_point.x < point.x:
                if result_point.y == point.y:
                    new_result1.append(point)
            else:
                new_result1.append(result_point)
                return new_result1


# подсчёт суммы минковского
def minkowski_sum(v1, v2):
    return v1[0] + v2[0], v1[1] + v2[1]


# Функция для нахождения выпуклой оболочки
def find_convex_hull(points):
    convex_hull = ConvexHull(points)
    return convex_hull.vertices


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen, font):
        xpos = XPOS
        ypos = YPOS
        n = 50
        for i in range(0, xpos // n):
            draw.line(screen, BLACK, (i * n, 0), (i * n, ypos), 1)
            text = font.render(f"{i}", True, BLACK)
            screen.blit(text, [xpos / 2 + i * n, ypos / 2])
            text = font.render(f"{-i}", True, BLACK)
            screen.blit(text, [xpos / 2 - i * n, ypos / 2])

        for i in range(0, ypos // n):
            draw.line(screen, BLACK, (0, i * n), (xpos, i * n), 1)
            text = font.render(f"{-i}", True, BLACK)
            screen.blit(text, [xpos / 2, ypos / 2 + i * n])
            text = font.render(f"{i}", True, BLACK)
            screen.blit(text, [xpos / 2, ypos / 2 - i * n])


# настройка окна вывода
display.set_caption("Minkowski_sum")
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GRAY = (100, 100, 100)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
XPOS = 1200
YPOS = 800
X_center = (XPOS // 2)
Y_center = (YPOS // 2)

# необходимые переменные и хранилища
counter = -1
case = []
carton = []
hull = []

# ввод векторов
with open("input1.txt", "r") as file:
    vector1 = tuple(map(lambda x: tuple(map(int, x.split())), file.readlines()))

with open("input2.txt", "r") as file:
    vector2 = tuple(map(lambda x: tuple(map(int, x.split())), file.readlines()))

for i in combinations(set(vector1 + vector2), 2):
    if all([i1 in vector1 for i1 in i]) or all([j1 in vector2 for j1 in i]):
        continue
    summ = minkowski_sum(*i)
    case.append(summ)

case = tuple(set(case))
hull = case

# case = sorted(case, key=lambda x: (-x[0], -x[1]))
case = tuple(map(lambda x: tuple(map(lambda y: y * 50, x)), case))

# bg окна
init()
size = width, height = XPOS, YPOS
screen = display.set_mode(size)
font = font.Font(None, 20)
screen.fill(WHITE)

# поле 5 на 7
board = Board(5, 7)
board.render(screen, font)

# используем функцию выпуклой оболочки
find_convex_hull(case)
a = find_convex_hull(hull)

# записываем точки выпуклой оболочки в коробку
for i in a:
    if counter == -1:
        counter = i
    carton.append(case[i])
# добавим первую точку для правильной отрисовки
carton.append(case[counter])

vector1 = tuple(map(lambda x: tuple(map(lambda y: y * 50, x)), vector1))
vector2 = tuple(map(lambda x: tuple(map(lambda y: y * 50, x)), vector2))

# отрисовка 1-го множества:
for pos in range(len(vector1) - 1):
    draw.line(screen, BLUE, [X_center + vector1[pos][0], Y_center - vector1[pos][1]],
              [X_center + vector1[pos + 1][0], Y_center - vector1[pos + 1][1]], 3)

# отрисовка 2-го множества:
for pos in range(len(vector2) - 1):
    draw.line(screen, GREEN, [X_center + vector2[pos][0], Y_center - vector2[pos][1]],
              [X_center + vector2[pos + 1][0], Y_center - vector2[pos + 1][1]], 3)

# отрисовка суммы Минковского:
for pos in range(len(carton) - 1):
    draw.line(screen, RED, [X_center + carton[pos][0], Y_center - carton[pos][1]],
              [X_center + carton[pos + 1][0], Y_center - carton[pos + 1][1]], 3)

# смена (отрисовка) кадра:
display.flip()

# ожидание закрытия окна:
while event.wait().type != QUIT:
    pass

# завершение работы:
quit()
