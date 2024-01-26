import pygame


class MyBoard:
    def __init__(self):
        self.board = [[0] * 12 for _ in range(12)]
        # создается поле 12 на 12, где мы будем рассматривать только поле 10 * 10, ведь края нужны только для
        # сокращения действий после попадания
        self.width, self.height = 11, 11
        self.hit = []
        self.cell_size = 40
        self.top, self.left = 5, 0
        self.theships = []
        self.recomendation = []
        self.ships = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]  # все корабли
        for ship in range(len(self.ships)):
            while True:
                no = 0
                from random import randint
                rotate = randint(0, 1)
                if rotate == 0:  # если корабль ставится горизонтально
                    first = randint(1, 10)
                    second_start = randint(1, 10 - self.ships[ship])
                    for i in range(-1, self.ships[ship] + 1):
                        for g in range(-1, 2):
                            if self.board[first + g][second_start + i] != 0:
                                no = 1
                    if no == 0:  # если ближайщие клетки пустые
                        add = []
                        for i in range(self.ships[ship]):
                            self.board[first][second_start + i] = 1
                            add.append([[first, second_start + i], False])  # второе значение - уничтожено - ли
                        self.theships.append(add)  # добавляем корабль в список кораблей с их координатами
                        break
                elif rotate == 1:  # если корабль ставится вертикально
                    second = randint(1, 10)
                    first_start = randint(1, 10 - self.ships[ship])
                    for i in range(-1, self.ships[ship] + 1):
                        for g in range(-1, 2):
                            if self.board[first_start + i][second + g] != 0:
                                no = 1
                    if no == 0:  # если ближайщие клетки пустые
                        add = []
                        for i in range(self.ships[ship]):
                            self.board[first_start + i][second] = 1
                            add.append([[first_start + i, second], False])  # второе значение - уничтожено - ли
                        self.theships.append(add)  # добавляем корабль в список кораблей с их координатами
                        break

    def render(self, screen):
        letters = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'К']  # буквы для рендера
        numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']  # цифры для рендера
        text_coord1 = 17
        text_coord2 = 17
        for line in range(10):
            letter_rendered = pygame.font.Font('ComicoroRu_0.ttf', 50).render(letters[line], 1, pygame.Color('black'))
            number_rendered = pygame.font.Font('ComicoroRu_0.ttf', 50).render(numbers[line], 1, pygame.Color('black'))
            letter_rect = letter_rendered.get_rect()
            number_rect = number_rendered.get_rect()
            text_coord1 += 15
            text_coord2 += 15
            letter_rect.top = text_coord1
            number_rect.top = 2
            number_rect.x = text_coord2 + 21
            letter_rect.x = 9
            text_coord1 += letter_rect.height - 21
            text_coord2 += letter_rect.height - 22
            screen.blit(letter_rendered, letter_rect)
            screen.blit(number_rendered, number_rect)
        player = pygame.font.Font('ComicoroRu_0.ttf', 50).render('Ваше поле', 1, pygame.Color('black'))
        pl_rect = player.get_rect()
        pl_rect.top = 440
        pl_rect.x = 60
        screen.blit(player, pl_rect)
        for i in range(1, 11):
            for g in range(1, 11):
                if self.board[i][g] == 0:  # если клетка непроверенна
                    pygame.draw.rect(screen, (109, 104, 255), (self.top + g * self.cell_size,
                                                               self.left + i * self.cell_size,
                                                               self.cell_size, self.cell_size), 1)
                elif self.board[i][g] == 1:  # отображение вашего корабля
                    pygame.draw.rect(screen, (0, 7, 195), (self.top + g * self.cell_size,
                                                           self.left + i * self.cell_size,
                                                           self.cell_size, self.cell_size))

                elif self.board[i][g] == 2:  # пустая простреленная клетка, с серым фоном и с более светлыми сторонами
                    pygame.draw.rect(screen, (209, 209, 209), (self.top + g * self.cell_size,
                                                               self.left + i * self.cell_size,
                                                               self.cell_size, self.cell_size))
                    pygame.draw.rect(screen, (123, 171, 255), (self.top + g * self.cell_size,
                                                               self.left + i * self.cell_size,
                                                               self.cell_size, self.cell_size), 1)
                    pygame.draw.circle(screen, 'black', ((g + 0.5) * self.cell_size + self.top,
                                                         (i + 0.5) * self.cell_size + self.left), self.cell_size / 15)
                elif self.board[i][g] == 3:  # попадание, с красным крестом и красными сторонами
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

    def get_cell(self, mouse_pos):  # определяет квадрат
        if self.top <= int(mouse_pos[0]) <= self.height * self.cell_size + self.top and \
                self.left <= int(mouse_pos[-1]) <= self.width * self.cell_size + self.left:
            cell_coords = [int(mouse_pos[0]) - self.top, int(mouse_pos[-1]) - self.left]
            if cell_coords:
                return [int(cell_coords[0] // self.cell_size), int(cell_coords[1] // self.cell_size)]
            else:
                return None
        else:
            return None

    def getfired(self, screen, board1, board2):
        from random import randint
        stop = False
        while True:
            if is_game_over(board1, board2) != '':  # если все корабли уже уничтожены
                break
            if len(self.recomendation) > 0:  # если было попадание без уничтожения
                coord = self.recomendation[randint(0, len(self.recomendation) - 1)]  # координаты - одна из рекомендаций
                if not (1 <= coord[0] <= 10 and 1 <= coord[1] <= 10):  # если вне поля, то убираем
                    self.recomendation.remove(coord)
                if self.board[coord[0]][coord[1]] == 1 and (1 <= coord[0] <= 10 and 1 <= coord[1] <= 10):
                    # если на поле находится корабль - попадаем в него
                    self.board[coord[0]][coord[1]] = 3
                    if not self.check(coord[0], coord[1]):  # если весь корабль уничтожен (конкретней в той функции)
                        self.recomendation.clear()
                        stop = True
                    screen.fill('white')
                    board2.render(screen)
                    board1.render(screen)
                    pygame.display.flip()
                    pygame.time.wait(1000)
                    if stop:
                        continue
                    elif len(self.hit) == 2:  # если уже попали 2 раза
                        removelist = []
                        if self.hit[0][0] == coord[0]:  # если совпадает по горизонтале
                            first = self.hit[0][0]
                            for i in self.recomendation:
                                if i[0] != first:  # если не на той же горизонтале - убрать
                                    removelist.append(i)
                            for i in removelist:
                                self.recomendation.remove(i)
                            self.recomendation.remove(coord)
                            if self.hit[0][1] < coord[1]:  # добавить в рекомендацию новую соседнюю клетку
                                self.recomendation.append([first, coord[1] + 1])
                            else:
                                self.recomendation.append([first, coord[1] - 1])
                        elif self.hit[0][1] == coord[1]:  # если совпадает по вертикале
                            second = self.hit[0][1]
                            for i in self.recomendation:
                                if i[1] != second:  # если не сопадает по вертикале - убрать
                                    removelist.append(i)
                            for i in removelist:
                                self.recomendation.remove(i)
                            self.recomendation.remove(coord)
                            if self.hit[0][0] < coord[0]:  # добавить новую соседнюю клетку
                                self.recomendation.append([coord[0] + 1, second])
                            else:
                                self.recomendation.append([coord[0] - 1, second])
                    elif len(self.hit) == 3:  # если попали в 3 раз и не убили
                        if self.hit[0][0] == coord[0]:  # если общая прямая - горизонтальная
                            self.recomendation.clear()
                            first = self.hit[0][0]  # добавили к каждой клетке по бокам проверку
                            self.recomendation.append([first, self.hit[0][1] - 1])
                            self.recomendation.append([first, self.hit[0][1] + 1])
                            self.recomendation.append([first, self.hit[1][1] - 1])
                            self.recomendation.append([first, self.hit[1][1] + 1])
                            self.recomendation.append([first, self.hit[2][1] - 1])
                            self.recomendation.append([first, self.hit[2][1] + 1])
                        elif self.hit[0][1] == coord[1]:  # если общая прямая - вертикальная
                            second = self.hit[0][1]
                            self.recomendation.append([self.hit[0][0] - 1, second])
                            self.recomendation.append([self.hit[0][0] + 1, second])
                            self.recomendation.append([self.hit[1][0] - 1, second])
                            self.recomendation.append([self.hit[1][0] + 1, second])
                            self.recomendation.append([self.hit[2][0] - 1, second])
                            self.recomendation.append([self.hit[2][0] + 1, second])
                        self.recomendation.remove(coord)
                elif self.board[coord[0]][coord[1]] == 3 and (1 <= coord[0] <= 10 and 1 <= coord[1] <= 10):
                    # если клетка уже уничтожена - убрать из рекомендации
                    self.recomendation.remove(coord)
                elif self.board[coord[0]][coord[1]] == 0 and (1 <= coord[0] <= 10 and 1 <= coord[1] <= 10):
                    # если клетка пустая - изменить на клетку с промахом
                    self.board[coord[0]][coord[1]] = 2
                    screen.fill('white')
                    board2.render(screen)
                    board1.render(screen)
                    pygame.display.flip()
                    pygame.time.wait(1000)
                    self.recomendation.remove(coord)
                    break
                elif self.board[coord[0]][coord[1]] == 2 and (1 <= coord[0] <= 10 and 1 <= coord[1] <= 10):
                    # если клетка уже проверенна и там пусто - убрать из рекомендации
                    self.recomendation.remove(coord)
            else:  # если не рекомендаций
                x, y = randint(1, 10), randint(1, 10)  # выбирается рандомная клетка
                if self.board[x][y] == 0:  # если там пусто - заменить на промах
                    self.board[x][y] = 2
                    screen.fill('white')
                    board2.render(screen)
                    board1.render(screen)
                    pygame.display.flip()
                    pygame.time.wait(1000)
                    break
                elif self.board[x][y] == 1:  # если там часть корабля - уничтожить его
                    self.board[x][y] = 3
                    if self.check(x, y):  # если у корабля есть ещё части
                        if len(self.hit) == 1:  # если попали в первый раз - в рекомендации добавить все соседние клетки
                            self.recomendation.append([x + 1, y])
                            self.recomendation.append([x - 1, y])
                            self.recomendation.append([x, y + 1])
                            self.recomendation.append([x, y - 1])
                            self.check(x, y)
                    screen.fill('white')
                    board2.render(screen)
                    board1.render(screen)
                    pygame.display.flip()
                    pygame.time.wait(1000)
            if is_game_over(board1, board2) != '':  # ещё раз проверка на наличие кораблей
                break

    def check(self, x, y):  # функция на проверку кораблей на полное уничтожение
        for I in range(len(self.theships)):  # во всех кораблях
            for q in range(len(self.theships[I])):  # по каждой клетке кораблей
                if self.theships[I][q] == [[x, y], False]:  # если клетка совпадает с той, что даны в x, y
                    self.theships[I][q][1] = True  # изменяем конкретно этой клетки на то, что в неё попали
                    if all(self.theships[I][r][1] for r in range(len(self.theships[I]))):
                        # если в данном корабле все клетки уничтожены
                        if len(self.theships[I]) == 1:  # если корабль - единичка
                            # уничтожаем все: пример
                            # 000   111     0 - пусто, непроверенно
                            # 0x0 > 1x1     1 - проверенно, мимо
                            # 000   111     x - сам корабль
                            first = self.theships[I][0][0][0]
                            second = self.theships[I][0][0][1]
                            for i in range(-1, len(self.theships[I]) + 1):
                                for g in range(-1, 2):
                                    if not (i == 0 and g == 0):
                                        self.board[first + g][second + i] = 2
                        elif self.theships[I][1][0][0] == self.theships[I][0][0][0]:  # если корабль располог. по гориз.
                            first = self.theships[I][0][0][0]  # первая координата для всех едина
                            second_start = min(x[0][1] for x in self.theships[I])  # вторая считается с минимальной
                            # зачищается как в примере выше
                            for i in range(-1, len(self.theships[I]) + 1):
                                for g in range(-1, 2):
                                    self.board[first + g][second_start + i] = 2
                            for i in range(len(self.theships[I])):
                                self.board[first][second_start + i] = 3
                        elif self.theships[I][1][0][1] == self.theships[I][0][0][1]:  # если корабль располог. по верт.
                            second = self.theships[I][0][0][1]  # второе - общее
                            first_start = min(x[0][0] for x in self.theships[I])  # первая - считаем с минимума
                            # также зачищаем
                            for i in range(-1, len(self.theships[I]) + 1):
                                for g in range(-1, 2):
                                    self.board[first_start + i][second + g] = 2
                            for i in range(len(self.theships[I])):
                                self.board[first_start + i][second] = 3
                        self.hit.clear()  # обнуляем последние попадания
                        return False  # корабль уничтожен
                    else:
                        self.hit.append([x, y])
                        return True  # стандартное попадение


class EnemyBoard:
    def __init__(self):
        self.board = []
        for i in range(12):
            add = []
            for g in range(12):  # отличается от MyBoard доп. индексом
                add.append([0, 0])  # первое число - стреляли \ не стреляли, 2ое - есть корабль, нет
                # по итогу всё работает также, только когда опираемя на координаты надо к индексу по другом обращаться
            self.board.append(add)
        self.theships = []
        self.width, self.height = 11, 11
        self.cell_size = 40
        self.top, self.left = 505, 0
        self.ships = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
        for ship in range(len(self.ships)):
            while True:
                no = 0
                from random import randint
                rotate = randint(0, 1)
                if rotate == 0:  # gorizontalno
                    first = randint(1, 10)
                    second_start = randint(1, 10 - self.ships[ship])
                    for i in range(-1, self.ships[ship] + 1):
                        for g in range(-1, 2):
                            if self.board[first + g][second_start + i][1] != 0:
                                no = 1
                    if no == 0:
                        add = []
                        for i in range(self.ships[ship]):
                            self.board[first][second_start + i][1] = 1
                            add.append([[first, second_start + i], False])
                        self.theships.append(add)
                        break
                elif rotate == 1:  # verticalno
                    second = randint(1, 10)
                    first_start = randint(1, 10 - self.ships[ship])
                    for i in range(-1, self.ships[ship] + 1):
                        for g in range(-1, 2):
                            if self.board[first_start + i][second + g][1] != 0:
                                no = 1
                    if no == 0:
                        add = []
                        for i in range(self.ships[ship]):
                            self.board[first_start + i][second][1] = 1
                            add.append([[first_start + i, second], False])
                        self.theships.append(add)
                        break

    def render(self, screen):
        letters = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'К']
        numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        text_coord1 = 17
        text_coord2 = 519
        for line in range(10):
            letter_rendered = pygame.font.Font('ComicoroRu_0.ttf', 50).render(letters[line], 1, pygame.Color('black'))
            number_rendered = pygame.font.Font('ComicoroRu_0.ttf', 50).render(numbers[line], 1, pygame.Color('black'))
            letter_rect = letter_rendered.get_rect()
            number_rect = number_rendered.get_rect()
            text_coord1 += 15
            text_coord2 += 15
            letter_rect.top = text_coord1
            number_rect.top = 2
            number_rect.x = text_coord2 + 21
            letter_rect.x = 519
            text_coord1 += letter_rect.height - 21
            text_coord2 += letter_rect.height - 22
            screen.blit(letter_rendered, letter_rect)
            screen.blit(number_rendered, number_rect)
        enemy = pygame.font.Font('ComicoroRu_0.ttf', 50).render('Поле противника', 1, pygame.Color('black'))
        en_rect = enemy.get_rect()
        en_rect.top = 440
        en_rect.x = 565
        screen.blit(enemy, en_rect)
        for i in range(1, 11):
            for g in range(1, 11):
                if self.board[i][g][0] == 0:
                    pygame.draw.rect(screen, (109, 104, 255), (self.top + g * self.cell_size,
                                                               self.left + i * self.cell_size,
                                                               self.cell_size, self.cell_size), 1)
                elif self.board[i][g][0] == 1 and self.board[i][g][1] == 0:
                    pygame.draw.rect(screen, (209, 209, 209), (self.top + g * self.cell_size,
                                                               self.left + i * self.cell_size,
                                                               self.cell_size, self.cell_size))
                    pygame.draw.rect(screen, (123, 171, 255), (self.top + g * self.cell_size,
                                                               self.left + i * self.cell_size,
                                                               self.cell_size, self.cell_size), 1)
                    pygame.draw.circle(screen, 'black', ((g + 0.5) * self.cell_size + self.top,
                                                         (i + 0.5) * self.cell_size + self.left), self.cell_size / 15)
                elif self.board[i][g][0] == 1 and self.board[i][g][1] == 1:
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

    def fired(self, pos, screen, board1, board2):
        if is_game_over(board1, board2) != '':
            return True
        the_cell = self.get_cell(pos)
        if not the_cell or not (1 <= the_cell[-1] <= 11 and 1 <= the_cell[0] <= 11):
            return False
        else:
            try:  # решение проблем с краями, которые выдают ошибку через IndexError
                if self.board[the_cell[-1]][the_cell[0]][0] != 0:
                    return False
                self.board[the_cell[-1]][the_cell[0]][0] = 1
                if self.board[the_cell[-1]][the_cell[0]][1] == 0:
                    screen.fill('white')
                    board2.render(screen)
                    board1.render(screen)
                    pygame.display.flip()
                    pygame.time.wait(1000)
                    return True
                for i in range(len(self.theships)):
                    if any(self.theships[i][q][0] == [the_cell[-1], the_cell[0]] for q in range(len(self.theships[i]))):
                        self.theships[i][self.theships[i].index([[the_cell[-1], the_cell[0]], False])][1] = True
                        if all(self.theships[i][q][1] for q in range(len(self.theships[i]))):
                            if len(self.theships[i]) == 1:
                                first = self.theships[i][0][0][0]
                                second = self.theships[i][0][0][1]
                                for i in range(-1, len(self.theships[i]) + 1):
                                    for g in range(-1, 2):
                                        self.board[first + g][second + i][0] = 1
                            elif self.theships[i][1][0][0] == self.theships[i][0][0][0]:
                                first = self.theships[i][0][0][0]
                                second_start = min(x[0][1] for x in self.theships[i])
                                for i in range(-1, len(self.theships[i]) + 1):
                                    for g in range(-1, 2):
                                        self.board[first + g][second_start + i][0] = 1
                            elif self.theships[i][1][0][1] == self.theships[i][0][0][1]:
                                second = self.theships[i][0][0][1]
                                first_start = min(x[0][0] for x in self.theships[i])
                                for i in range(-1, len(self.theships[i]) + 1):
                                    for g in range(-1, 2):
                                        self.board[first_start + i][second + g][0] = 1
                pygame.time.wait(1000)
                screen.fill('white')
                board2.render(screen)
                board1.render(screen)
                pygame.display.flip()
            except IndexError:
                return False
        if is_game_over(board1, board2) != '':
            return True


class MainScene():  # основная сцена, главный экран
    def __init__(self):
        self.stop, self.cont, self.rules = False, False, False
        pygame.init()
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
                clickable.append(intro_rect)  # добавляем координаты квадрата в кликабельное
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        while not self.stop and not self.cont and not self.rules:  # если у нас есть нажатие на 'кнопки' - прерывается
            for event in pygame.event.get():
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
            clock.tick(60)
        pygame.quit()


class RulesScene():  # сцена с правилами
    def __init__(self):
        pygame.init()
        self.back = False
        pygame.display.set_caption('Naval Battle')
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((1400, 600))
        screen.fill('white')
        intro_text = ["Принцип «Морского боя» очень прост.",
                      "Корабли расставляются на поле боя, размером 10 на 10.",
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
                clock.tick(60)
        pygame.quit()


class BattleScene():  # сцена бойни
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
                    pygame.quit()
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if board2.fired(event.pos, screen, board1, board2):
                        board2.render(screen)
                        board1.render(screen)
                        pygame.display.flip()
                        is_game_over(board1, board2)  # куча проверок на победу, до выстрелов и после
                        if is_game_over(board1, board2) == '':
                            board1.getfired(screen, board1, board2)
                            if is_game_over(board1, board2) != '':
                                pygame.quit()
                                WinnerScene(is_game_over(board1, board2))
                                self.running = False
                        else:
                            pygame.quit()
                            WinnerScene(is_game_over(board1, board2))
                            self.running = False
            if self.running:
                board1.render(screen)
                board2.render(screen)
                pygame.display.flip()


class WinnerScene():  # сцена победителя
    def __init__(self, winner):
        clickable = []
        pygame.init()
        pygame.display.set_caption('Конец.')
        screen = pygame.display.set_mode((500, 250))
        repeat_rendered = pygame.font.Font('ComicoroRu_0.ttf', 50).render('Повторить', 1, pygame.Color('black'))
        exit_rendered = pygame.font.Font('ComicoroRu_0.ttf', 50).render('Выйти', 1, pygame.Color('black'))
        string_rendered = pygame.font.Font('ComicoroRu_0.ttf', 50).render(winner, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        repeat_rect = repeat_rendered.get_rect()
        exit_rect = exit_rendered.get_rect()
        repeat_rect.top = 160
        repeat_rect.x = 70
        exit_rect.top = 160
        exit_rect.x = 290
        intro_rect.top = 70
        intro_rect.x = 110
        clickable.append(repeat_rect)
        clickable.append(exit_rect)
        running = True
        while running:
            screen.fill('white')
            screen.blit(string_rendered, intro_rect)
            screen.blit(repeat_rendered, repeat_rect)
            screen.blit(exit_rendered, exit_rect)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    for i in clickable:
                        if i.left <= int(mouse_pos[0]) <= i.left + i.width and \
                                i.top <= int(mouse_pos[-1]) <= i.top + i.height:
                            if i == (70, 160, 171, 47):
                                running = False
                                pygame.quit()
                                start()
                            elif i == (290, 160, 101, 47):
                                running = False
        pygame.quit()


def is_game_over(board1, board2):  # определение победителя
    winner = ''
    NOT = False
    for i in board1.board:
        if any(g == 1 for g in i):  # если хотя бы один корабль цел
            NOT = True  # оппонент не победил
            break
    if not NOT:
        winner = 'Оппонент победил :-('
    else:
        NOT = False
        for i in board2.board:
            if any(g[1] == 1 and g[0] == 0 for g in i):  # если хотя бы один корабль цел
                NOT = True  # вы не победили
                break
        if not NOT:
            winner = 'Вы победили :-)'
    return winner


def start():  # главная 'шина' морского боя.
    main = MainScene()
    while True:
        if main.stop:  # если выход - выход из цикла, конец
            break
        elif main.cont:  # если начать игру
            battle = BattleScene()  # создаём сцену бойни
            if not battle.running:  # если выход - выход из боя ВООБЩЕ
                break
        elif main.rules:  # если посмотреть правила
            rules = RulesScene()  # сцена правил
            if rules.back:  # если выход - выход из правил
                main = MainScene()  # новое главное меню


start()
