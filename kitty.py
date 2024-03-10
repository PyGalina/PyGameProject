import pygame, sys, os, random

WIDTH = 650
HEIGHT = 550
FPS = 20

pygame.init()
size = WIDTH, HEIGHT
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Поймай мышек")
score = 0 # очки
n = 0 # количество мышей
# загрузка изображений
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image

# остановка приложения
def terminate():
    pygame.quit()
    sys.exit()

def start_screen():
    intro_text = ["Правила игры:",
                  "- управление котиком с помощью стелок;",
                  "- необходимо собрать всех мышат с поля за определенное время.",
                  "Сколько? Решит программа)"]
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 50)
    string_rendered = font.render("Поймай мышат", 1, pygame.Color((255, 0, 0)))
    intro_rect = string_rendered.get_rect()
    intro_rect.midtop = (WIDTH // 2, HEIGHT // 2 - 20)
    screen.blit(string_rendered, intro_rect)
    font = pygame.font.Font(None, 30)
    text_coord = 300
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color((127, 15, 70)))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return True# начинаем игру
        pygame.display.flip()
        clock.tick(FPS)

def end_screen(result="Конец игры"):
    intro_text = [result,
                  "Было поймано мышек: " + str(score)]
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 50)
    string_rendered = font.render(result, 1, pygame.Color((255, 0, 0)))
    intro_rect = string_rendered.get_rect()
    intro_rect.midtop = (WIDTH // 2, HEIGHT // 2)
    screen.blit(string_rendered, intro_rect)
    font = pygame.font.Font(None, 30)
    string_rendered = font.render(intro_text[1], 1, pygame.Color((127, 15, 70)))
    intro_rect = string_rendered.get_rect()
    intro_rect.midleft = (20, HEIGHT * 2 // 3)
    screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.MOUSEBUTTONDOWN:
                terminate()# выход из игры
        pygame.display.flip()
        clock.tick(FPS)

def output_score(score):
    intro_text = "Score: " + str(score)
    font = pygame.font.Font(None, 30)
    text_surface = font.render(intro_text, True, "white")
    text_rect = text_surface.get_rect()
    text_rect.bottomleft = (30, 530)
    screen.blit(text_surface, text_rect)

def draw_timer(time_left):
    font = pygame.font.Font(None, 30)
    text = font.render("Time left: " + str(time_left), True, (255, 255, 255))
    screen.blit(text, (250, 510))

def load_level(filename):
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))

tile_images = {
    'fence': load_image('fence.png'),
    'empty': load_image('grass.png')
}
player_image = {
    'cat': load_image('cat2.png'),
    'mouse': load_image('mouse.png')
}

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        #self.image = player_image["cat"]
        self.frames_r = [load_image("cat_r1.png"), load_image("cat_r2.png"), load_image("cat_r3.png"),
                      load_image("cat_r4.png"), load_image("cat_r5.png"), load_image("cat_r6.png")]
        self.frames_l = [load_image("cat_l1.png"), load_image("cat_l2.png"), load_image("cat_l3.png"),
                         load_image("cat_l4.png"), load_image("cat_l5.png"), load_image("cat_l6.png")]
        self.image = self.frames_r[0]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.pos = (pos_x, pos_y)
        self.numb_frames = 0

    def update_r(self):
        self.numb_frames = (self.numb_frames + 1) % 6
        self.image = self.frames_r[self.numb_frames]

    def update_l(self):
        self.numb_frames = (self.numb_frames + 1) % 6
        self.image = self.frames_l[self.numb_frames]

    def move(self, x=0, y=0):
        global score
        x_pos, y_pos = self.rect.x, self.rect.y
        if x and 0 <= x_pos + x < WIDTH:
            if x < 0 and level[self.pos[1]][(self.pos[0] - 1) % len(level[0])] != "#":
                self.pos =((self.pos[0] - 1) % len(level[0]), self.pos[1])
                self.rect = self.rect.move(x, y)
            elif x > 0 and level[self.pos[1]][(self.pos[0] + 1) % len(level[0])] != "#":
                self.pos = ((self.pos[0] + 1) % len(level[0]), self.pos[1])
                self.rect = self.rect.move(x, y)
        if y and 0 <= y_pos + y < HEIGHT:
            if y < 0 and level[(self.pos[1] - 1) % len(level)][self.pos[0]] != "#":
                self.pos = (self.pos[0], (self.pos[1] - 1) % len(level))
                self.rect = self.rect.move(x, y)
            elif y > 0 and level[(self.pos[1] + 1) % len(level)][self.pos[0]] != "#":
                self.pos = (self.pos[0], (self.pos[1] + 1) % len(level))
                self.rect = self.rect.move(x, y)

        if pygame.sprite.spritecollide(self, mouse_group, True):
            score += 1

class Mouse(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(mouse_group, all_sprites)
        self.image = player_image["mouse"]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self, field_size):
        self.dx = 0
        self.dy = 0
        self.field_size = field_size

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        if obj.rect.x < -obj.rect.width:
            obj.rect.x += (self.field_size[0] + 1) * obj.rect.width
        if obj.rect.x >= self.field_size[0] * obj.rect.width:
            obj.rect.x += -obj.rect.width * (1 + self.field_size[0])
        obj.rect.y += self.dy
        if obj.rect.y < -obj.rect.height:
            obj.rect.y += (self.field_size[1] + 1) * obj.rect.height
        if obj.rect.y >= self.field_size[1] * obj.rect.height:
            obj.rect.y += -obj.rect.height * (1 + self.field_size[1])

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)

def generate_level(level):
    global n
    new_player, x, y = None, None, None
    for y1 in range(len(level)):
        n += level[y1].count('.')
    n = random.randint(5, n // 4)
    i = 0
    while i != n:
        y1 = random.randint(0, len(level) - 1)
        x1 = random.randint(0, len(level[0]) - 1)
        if level[y1][x1] == '.':
            level[y1] = level[y1][:x1] + '&' + level[y1][x1 + 1:]
            i += 1
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('fence', x, y)
               # Fence('fence', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
            elif level[y][x] == '&':
                Tile('empty', x, y)
                Mouse(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y, level

def draw_sprites():
    # изменяем ракурс камеры
    camera.update(player)
    # обновляем положение всех спрайтов
    for sprite in all_sprites:
        camera.apply(sprite)
    screen.fill((53, 145, 4))
    tiles_group.draw(screen)
    player_group.draw(screen)
    mouse_group.draw(screen)
    if right:
        player.update_r()
    if left:
        player.update_l()
    output_score(score)
    draw_timer(time_left)
    pygame.display.flip()


if __name__ == '__main__':
    file_level = random.choice(["level.txt", "level1.txt", "level2.txt"])
    fullname = 'data/' + file_level
    if not os.path.isfile(fullname):
        print(f"Такого уровня не существует")
        sys.exit()
    # основной персонаж
    player = None
    # группы спрайтов
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    fence_group = pygame.sprite.Group()
    mouse_group =pygame.sprite.Group()
    clock = pygame.time.Clock()
    start = start_screen()
    running = True
    right = True
    left = False
    player, level_x, level_y, level = generate_level(load_level(fullname))
    camera = Camera((level_x, level_y))
    time_left = FPS * n
    while running:
        for event in pygame.event.get():
            # при закрытии окна
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    player.move(x=50)
                    right = True
                    left = False
                elif event.key == pygame.K_LEFT:
                    player.move(x=-50)
                    right = False
                    left = True
                elif event.key == pygame.K_UP:
                    player.move(y=-50)
                elif event.key == pygame.K_DOWN:
                    player.move(y=50)
        time_left -= 1
        draw_sprites()
        clock.tick(FPS)
        #print(score, n)
        if score == n:
            end_screen("Победа")
        elif time_left < 0:
            end_screen("Время истекло")
        # завершение работы:
    end_screen()
    pygame.quit()