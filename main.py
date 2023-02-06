import os
import random
import sys

import pygame

# Ширина окна
WIDTH = 500
# Высота окна
HEIGHT = 600
FPS = 60

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Создаем игру и окно
pygame.init()  # инициализация Pygame
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Создание холста
pygame.display.set_caption("Танки")  # Название окна
clock = pygame.time.Clock()


# Загрузка изображений
def load_image(name):
    fullname = os.path.join('Image', name)
    # Изображение обрезаем по размерам
    image = pygame.image.load(fullname)
    return image


# Загрузка изображения - фон
background = load_image('Background.png')
# Загрузка изображения - танк
tank_img = load_image('Tank.png')
# Загрузка изображения - камень
stone_img = load_image('Stone.png')
# Загрузка изображения - пуля
bullet_img = load_image('Bullet.png')


# Начальный экран
def start_screen():
    intro_text = ["ТАНКИ", "",
                  "Правила игры",
                  "Ваша задача убить",
                  "как можно больше камней,",
                  "сделать это можно нажатием",
                  "на кнопку пробел",
                  "При этом",
                  "избегайте попадания камней в танк",
                  "Ваше здоровье ограничено",
                  "Для начала игры",
                  "нажмите любую клавишу"]

    # Загрузка фона
    fon = pygame.transform.scale(load_image('Background.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 35)
    # Положение текста
    text_coord = 80
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        # Смещаем положение следующей строчки
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Проверка на нажатие кнопки
            # Или клика мышки
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                # начинаем игру
                return
        pygame.display.flip()
        clock.tick(FPS)


start_screen()


# Конечный экран
def finish_screen():
    finish_text = ["КОНЕЦ", "",
                   "Поздравляем!",
                   "Игра закончена"]

    # Загрузка фона
    fon_f = pygame.transform.scale(load_image('Background.png'), (WIDTH, HEIGHT))
    screen.blit(fon_f, (0, 0))
    font = pygame.font.Font(None, 35)
    # Положение текста
    text_coord = 100
    for line in finish_text:
        string_rendered = font.render(line, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        # Смещаем положение следующей строчки
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.flip()
        clock.tick(FPS)


def draw_health(surf, x, y, percent):  # Полоска здоровья
    if percent < 0:
        percent = 0
    # Длина полоски
    stripe_width = 100
    # Ширина полоски
    stripe_height = 10
    # Высчитывание заливки
    fill = (percent / 100) * stripe_width
    outline_rect = pygame.Rect(x, y, stripe_width, stripe_height)
    fill_rect = pygame.Rect(x, y, fill, stripe_height)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)


def draw_score(surf, text, size, x, y):  # Отображение счёта
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


class Tank(pygame.sprite.Sprite):  # Танк
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = tank_img  # Картинка
        # Граница прямоугольника
        self.rect = self.image.get_rect()
        # Начальное положение - по центру
        self.rect.centerx = WIDTH / 2
        # Начальное положение - внизу окна
        self.rect.bottom = HEIGHT
        self.speed = 0
        # Жизнь танка
        self.shield = 100

    # Движение танка
    def update(self):
        # Скорость движения танка
        self.speed = 0
        state = pygame.key.get_pressed()
        # Если состояние в списке нажатой левой клавиши
        if state[pygame.K_LEFT]:
            # Определяем смещение танка
            self.speed = -8
            # Если состояние в списке нажатой правой клавиши
        if state[pygame.K_RIGHT]:
            # Определяем смещение танка
            self.speed = 8
        # Изменяем положение танка по оси х
        self.rect.x += self.speed
        # Если правая граница танка совпадает или становится больше границы окна
        if self.rect.right > WIDTH:
            # Не выходить за правую границу окна
            self.rect.right = WIDTH
        # Если левая граница танка совпадает или становится меньше границы окна
        if self.rect.left < 0:
            # Не выходить за левую границу окна
            self.rect.left = 0

    def shoot(self):  # Стрельба
        # Передаём координаты х и у танка, чтобы знать с какой координаты должна появляться пуля:
        bullet = Bullet(self.rect.centerx, self.rect.top)
        # Добавление пули в группу спрайтов
        all_sprites.add(bullet)
        bullets.add(bullet)


class Stones(pygame.sprite.Sprite):  # Камни
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = stone_img  # Картинка
        # Граница прямоугольника
        self.rect = self.image.get_rect()
        # Задаем место появления камня по оси х и следим чтобы он не выходил за границы окна:
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        # Аналогично, по оси у, но за границами окна
        self.rect.y = random.randrange(-100, -10)
        # Определям рандомню скорость по оси у
        self.speed_y = random.randrange(1, 10)
        # Определям рандомню скорость по оси у
        self.speed_x = random.randrange(-2, 2)

    def update(self):  # Движение камня
        self.rect.x += self.speed_x  # Изменяем положение камня по оси х
        self.rect.y += self.speed_y  # Изменяем положение камня по оси у
        # Если камень выходит за нижние или левые или правые границы окна:
        if self.rect.top > HEIGHT or self.rect.left < -40 or self.rect.right > WIDTH + 40:
            # (чтобы камень полностью вышел за границы окна а не его одна сторона, так как размеры камня 40*40)
            # Как только это происходит меняем координаты камня на рандомные начальные
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -10)
            self.speed_y = random.randrange(1, 10)
            self.speed_x = random.randrange(-2, 2)


# Пули
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # убить, если он заходит за верхнюю часть экрана
        if self.rect.bottom < 0:
            self.kill()


all_sprites = pygame.sprite.Group()
# Танк - класса танк
tank = Tank()
bullets = pygame.sprite.Group()
stones = pygame.sprite.Group()
# Добавление танка в группу спрайтов
all_sprites.add(tank)
# Создаём 7 экземпляров камней
for i in range(7):
    s = Stones()
    # Добавляем их в группу спрайтов
    all_sprites.add(s)
    stones.add(s)
# Счёт
score = 0

# Цикл игры
running = True
while running:
    # Скорость смены картинок
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # проверка для закрытия окна
        if event.type == pygame.QUIT:
            running = False
        # Если нажали кнопку
        elif event.type == pygame.KEYDOWN:
            # Если это пробел
            if event.key == pygame.K_SPACE:
                # Метод стрельбы класса Tank
                tank.shoot()

    # Обновление
    all_sprites.update()

    # При столкновении пули с камнем, определять какой камень задели
    # И так как этот камень удаляется, на его место создавать новый
    conflicts = pygame.sprite.groupcollide(stones, bullets, True, True)
    for conflict in conflicts:
        # Увеличиваем счёт от попадания пули в камень
        score += 10
        s = Stones()
        all_sprites.add(s)
        stones.add(s)

    # Проверяем, не попал ли камень в танк
    conflicts = pygame.sprite.spritecollide(tank, stones, True)
    # Если это произошло, то
    if conflicts:
        # Отнимаем здоровье
        tank.shield -= 20
        s = Stones()
        all_sprites.add(s)
        stones.add(s)
        # Если здоровье <= 0
        if tank.shield <= 0:
            # Заканчиваем игру и отображаем конечный экран
            finish_screen()

    # Фон - изображение и прямоугольник, ограничивающий его
    screen.blit(background, background.get_rect())
    all_sprites.draw(screen)
    draw_score(screen, str(score), 18, WIDTH / 2, 10)
    draw_health(screen, 5, 5, tank.shield)
    pygame.display.flip()  # смена (отрисовка) кадра

pygame.quit()  # завершение работы
