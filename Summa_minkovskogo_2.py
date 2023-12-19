from pygame import *
import os


# Функция для определения направления поворота
def orientation(p, q, r):
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])

    if val == 0:
        return 0  # коллинеарные точки
    elif val > 0:
        return 1  # против часовой стрелки
    else:
        return 2  # по часовой стрелке


# Функция для нахождения выпуклой оболочки
def convexhull(points):
    n = len(points)
    # Если точек меньше 3, то выпуклая оболочка не может быть образована
    if n < 3:
        return []
    # Находим самую левую точку
    leftmost = min(points, key=lambda x: x[0])
    leftmost_idx = points.index(leftmost)
    hull1 = []
    p = leftmost_idx
    q = None
    while True:
        hull1.append(points[p])
        q = (p + 1) % n
        for r in range(n):
            if orientation(points[p], points[q], points[r]) == 2:
                q = r
        p = q
        if p == leftmost_idx:
            break
    return hull1


# подсчёт суммы минковского
def minkowski_sum(v1, v2):
    return v1[0] + v2[0], v1[1] + v2[1]


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


# проверка файлов
path = 'input1.txt'
path1 = 'input2.txt'

if not os.path.exists(path) or not os.path.exists(path1): print("Файла нет"), exit()

if (os.path.splitext(path)[-1] or os.path.splitext(path1)[-1]) != ".txt":
    print("Входной файл должен иметь формат txt")
    exit()

# настройка окна вывода
display.set_caption("Minkowski_sum")
img = image.load("icons.png")
display.set_icon(img)
XPOS = 1200
YPOS = 800
X_center = (XPOS // 2)
Y_center = (YPOS // 2)

# цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GRAY = (100, 100, 100)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# необходимые переменные и хранилища
counter = -1
case = []
carton = []
hull = []

# ввод векторов
with open("input1.txt", "r") as file:
    try:
        vector1 = tuple(map(lambda x: tuple(map(int, x.split())), file.readlines()))
    except ValueError:
        print("Пустой файл или имеет некорректные значения")

with open("input2.txt", "r") as file:
    try:
        vector2 = tuple(map(lambda x: tuple(map(int, x.split())), file.readlines()))
    except ValueError:
        print("Пустой файл или имеет некорректные значения")

# перебираем все суммы
for i in vector1:
    for j in vector2:
        summ = minkowski_sum(i, j)
        case.append(summ)

# убираем лишнее
case = tuple(set(case))
hull = case
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
point = convexhull(hull)

# записываем точки выпуклой оболочки в коробку
carton = list(map(lambda x: tuple(map(lambda y: y * 50, x)), point))

# добавим первую точку для правильной отрисовки
carton.append(carton[0])

# Делаем вектора в 50 раз больше
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
