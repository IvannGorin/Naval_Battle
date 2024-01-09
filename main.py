import pygame

class MyBoard:
    def __init__(self):
        self.board = [[0] * 10 for i in range(10)] ## 0 - пусто, 1 - мимо, 2 - попал
        self.width, self.height = 10, 10
        self.cell_size = 40
        self.top, self.left = 30, 30

    def render(self, screen):
        for i in range(self.width):
            for g in range(self.width):
                if self.board[i][g] == 0:  # обычная клетка - квадрат с синими сторонами
                    pygame.draw.rect(screen, (109, 104, 255), (self.top + g * self.cell_size,
                                                               self.left + i * self.cell_size,
                                                               self.cell_size, self.cell_size), 1)
                elif self.board[i][g] == 1:  # пустая простреленная клетка, с серым фоном и с более светлыми сторонами
                    pygame.draw.rect(screen, (209, 209, 209), (self.top + g * self.cell_size,
                                                               self.left + i * self.cell_size,
                                                               self.cell_size, self.cell_size))
                    pygame.draw.rect(screen, (123, 171, 255), (self.top + g * self.cell_size,
                                                               self.left + i * self.cell_size,
                                                               self.cell_size, self.cell_size), 1)
                    pygame.draw.circle(screen, 'black', ((g + 0.5) * self.cell_size + self.top,
                                                         (i + 0.5) * self.cell_size + self.left), self.cell_size / 15)
                elif self.board[i][g] == 2:  # попадание, с красным крестом и красными сторонами
                    pygame.draw.rect(screen, 'red',
                                     (self.top + g * self.cell_size, self.left + i * self.cell_size, self.cell_size,
                                      self.cell_size), 1)
                    pygame.draw.line(screen, 'red',
                                     (self.top + g * self.cell_size, self.left + i * self.cell_size),
                                     (self.top + g * self.cell_size + self.cell_size,
                                      self.left + i * self.cell_size + self.cell_size), 2)
                    pygame.draw.line(screen, 'red',
                                     (self.top + (g + 1) * self.cell_size, self.left + i * self.cell_size),
                                     (self.top + g * self.cell_size, self.left + (i + 1) * self.cell_size), 2)

    def get_cell(self, mouse_pos):
        if self.top <= int(mouse_pos[0]) <= self.height * self.cell_size + self.top and \
                self.left <= int(mouse_pos[-1]) <= self.width * self.cell_size + self.left:
            cell_coords = [int(mouse_pos[0]) - self.top, int(mouse_pos[-1]) - self.left]
            if cell_coords:
                return [int(cell_coords[0] // self.cell_size), int(cell_coords[1] // self.cell_size)]
            else:
                return None
        else:
            return None

    def getfired(self):
        from random import randint
        while True:
            x, y = randint(0, 9), randint(0, 9)
            if self.board[x][y] == 0:
                self.board[x][y] = 1
                break

class EnemyBoard:
    def __init__(self):
        self.board = [[0] * 10 for i in range(10)]
        self.width, self.height = 10, 10
        self.cell_size = 40
        self.top, self.left = 500, 30

    def render(self, screen):
        for i in range(self.width):
            for g in range(self.width):
                if self.board[i][g] == 0:
                    pygame.draw.rect(screen, (109, 104, 255), (self.top + g * self.cell_size,
                                                               self.left + i * self.cell_size,
                                                               self.cell_size, self.cell_size), 1)
                elif self.board[i][g] == 1:
                    pygame.draw.rect(screen, (209, 209, 209), (self.top + g * self.cell_size,
                                                               self.left + i * self.cell_size,
                                                               self.cell_size, self.cell_size))
                    pygame.draw.rect(screen, (123, 171, 255), (self.top + g * self.cell_size,
                                                               self.left + i * self.cell_size,
                                                               self.cell_size, self.cell_size), 1)
                    pygame.draw.circle(screen, 'black', ((g + 0.5) * self.cell_size + self.top,
                                                         (i + 0.5) * self.cell_size + self.left), self.cell_size / 15)
                elif self.board[i][g] == 2:
                    pygame.draw.rect(screen, 'red',
                                     (self.top + g * self.cell_size, self.left + i * self.cell_size, self.cell_size,
                                      self.cell_size), 1)
                    pygame.draw.line(screen, 'red',
                                     (self.top + g * self.cell_size, self.left + i * self.cell_size),
                                     (self.top + g * self.cell_size + self.cell_size,
                                      self.left + i * self.cell_size + self.cell_size), 2)
                    pygame.draw.line(screen, 'red',
                                     (self.top + (g + 1) * self.cell_size, self.left + i * self.cell_size),
                                     (self.top + g * self.cell_size, self.left + (i + 1) * self.cell_size), 2)

    def get_cell(self, mouse_pos):
        if self.top <= int(mouse_pos[0]) <= self.height * self.cell_size + self.top and \
                self.left <= int(mouse_pos[-1]) <= self.width * self.cell_size + self.left:
            cell_coords = [int(mouse_pos[0]) - self.top, int(mouse_pos[-1]) - self.left]
            if cell_coords:
                return [int(cell_coords[0] // self.cell_size), int(cell_coords[1] // self.cell_size)]
            else:
                return None
        else:
            return None

    def fired(self, pos):
        the_cell = self.get_cell(pos)
        if the_cell == None:
            return False
        elif self.board[the_cell[-1]][the_cell[0]] != 0:
            return False
        else:
            try:  # решение проблем с краями, которые выдают ошибку через IndexError
                self.board[the_cell[-1]][the_cell[0]] = 1
                return True
            except IndexError:
                return False


class MainScene():
    def __init__(self):
        self.stop, self.cont, self.rules = False, False, False
        pygame.init()
        FPS = 60
        pygame.display.set_caption('Naval Battle')
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
        screen.fill('white')
        intro_text = ["Морской Бой",
                      "Начать",
                      "Правила",
                      "Выйти"]
        text_coord = 200
        clickable = []
        for line in intro_text:
            string_rendered = pygame.font.Font('ComicoroRu_0.ttf', 80).render(line, 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            if line == 'Морской Бой':
                intro_rect.top = 100
                intro_rect.x = 540
            else:
                text_coord += 10
                intro_rect.top = text_coord
                intro_rect.x = 600
                clickable.append(intro_rect)
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        while not self.stop and not self.cont and not self.rules:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pass
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    for i in clickable:
                        if i.left <= int(mouse_pos[0]) <= i.left + i.width and \
                                i.top <= int(mouse_pos[-1]) <= i.top + i.height:
                            if i == (600, 455, 160, 75):
                                self.stop = True
                            elif i == (600, 285, 180, 75):
                                self.cont = True
                            elif i == (600, 370, 215, 75):
                                self.rules = True
            pygame.display.flip()
            clock.tick(FPS)
        pygame.quit()

class RulesScene():
    def __init__(self):
        pygame.init()
        self.back = False
        FPS = 60
        pygame.display.set_caption('Naval Battle')
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((1400, 600))
        screen.fill('white')
        intro_text = ["Принцип «Морского боя» очень прост.",
                      "Вы расставляете свои корабли на поле 10х10 оппонент расставляет свои.",
                      "Далее вы по очереди делаете «выстрелы», кликая те или иные координаты поля.",
                      "Оппонент же запускает ответный огонь по вашим кораблям.",
                      "Побеждает тот, у кого к концу игры хотя бы один корабль устоял."]
        text_coord = 60
        for line in intro_text:
            string_rendered = pygame.font.Font('ComicoroRu_0.ttf', 50).render(line, 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord += 20
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        while not self.back:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.back = True
                if event.type == pygame.QUIT:
                    self.back = True
                pygame.display.flip()
                clock.tick(FPS)
        pygame.quit()

class BattleScene():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Naval Battle')
        screen = pygame.display.set_mode((1000, 500))
        board1 = MyBoard()
        board2 = EnemyBoard()
        self.running = True
        while self.running:
            screen.fill('white')
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if board2.fired(event.pos): board1.getfired()
            board1.render(screen)
            board2.render(screen)
            pygame.display.flip()
        pygame.quit()

main = MainScene()
while True:
    if main.stop:
        break
    elif main.cont:
        battle = BattleScene()
        if not battle.running:
            break
    elif main.rules:
        rules = RulesScene()
        if rules.back:
            main = MainScene()
