import pygame as pg
from random import randint


def is_happy(a, pers, x, y, percent):
    area = [(x - 1, y - 1), (x - 1, y), (x - 1, y + 1), (x, y - 1),
            (x, y + 1), (x + 1, y - 1), (x + 1, y), (x + 1, y + 1)]
    people = []
    for k in area:
        if 0 <= k[0] < n and 0 <= k[1] < m and a[k[0]][k[1]]:
            people.append(a[k[0]][k[1]])
    other = people.count(1 if pers == 2 else 2)
    if other == 0 or other / len(people) <= percent / 100:
        return True
    return False


h, w = 600, 1200
n, m = 30, 60

num_free_cells = 100
percent = 30
error = 10

pg.init()
window = pg.display.set_mode((w, h))
clock = pg.time.Clock()

a = [[0] * m for _ in range(n)]
for i in range(n):
    for j in range(m):
        if num_free_cells > 0:
            a[i][j] = 0
            num_free_cells -= 1
        else:
            a[i][j] = randint(1, 2)


simulation, radius, pause = True, min(h // n, w // m) // 2 - 2, False
while simulation:
    clock.tick(60)
    pg.display.set_caption('Модель сегрегации' + ' '*100 + 'Процент толерантности: ' + str(percent))

    window.fill((250, 250, 250))
    for i in range(n):
        pg.draw.line(window, (0, 0, 0), (0, h // n * i), (w, h // n * i))
    for i in range(m):
        pg.draw.line(window, (0, 0, 0), (w // m * i, 0), (w // m * i, h))

    for _ in range(1000):
        i, j = randint(0, n-1), randint(0, m-1)
        if not pause and a[i][j] and not is_happy(a, a[i][j], i, j, percent):
            variants = []
            for i1 in range(n):
                for j1 in range(m):
                    if not a[i1][j1]:
                        err = randint(0, 100) <= error
                        will_happy = is_happy(a, a[i][j], i1, j1, percent)
                        if (will_happy and not err) or (not will_happy and err):
                            variants.append((i1, j1))
            if len(variants) > 0:
                i1, j1 = variants[randint(0, len(variants)-1)]
                a[i][j], a[i1][j1] = a[i1][j1], a[i][j]

    for i in range(n):
        for j in range(m):
            if a[i][j]:
                color = (250, 0, 0) if a[i][j] == 1 else (0, 0, 250)
                # pg.draw.circle(window, color, (w // m * j + radius + 2, h // n * i + radius + 2), radius)
                pg.draw.rect(window, color, (w // m * j + 2, h // n * i + 2, radius * 2+1, radius * 2+1),
                             border_radius=5)
                pg.draw.line(window, (250, 250, 250), (w // m * j + 5, h // n * i + radius + 1),
                             (w // m * (j + 1) - 5, h // n * i + radius + 1), 2)
                if is_happy(a, a[i][j], i, j, percent):
                    pg.draw.line(window, (250, 250, 250), (w // m * j + radius + 1, h // n * i + 5),
                                 (w // m * j + radius + 1, h // n * (i + 1) - 5), 2)
    pg.display.flip()

    for e in pg.event.get():
        if e.type == pg.QUIT:
            simulation = False

        if e.type == pg.KEYUP and e.key == pg.K_SPACE:
            pause = not pause

    if pg.key.get_pressed()[pg.K_UP] and percent < 100:
        percent += 1
    if pg.key.get_pressed()[pg.K_DOWN] and percent > 0:
        percent -= 1
