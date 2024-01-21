import pygame


class MyBoard:
    def __init__(self):
        self.board = [[0] * 12 for i in range(12)] ## 0 - пусто, 1 - корабль, 2 - мимо, 3 - попал
        self.width, self.height = 11, 11
        self.hit = []
        self.cell_size = 40
        self.top, self.left = 5, 0
        self.theships = []
        self.recomendation = []
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
                            if self.board[first + g][second_start + i] != 0:
                                no = 1
                    if no == 0:
                        add = []
                        for i in range(self.ships[ship]):
                            self.board[first][second_start + i] = 1
                            add.append([[first, second_start + i], False])
                        self.theships.append(add)
                        break
                elif rotate == 1:  # verticalno
                    second = randint(1, 10)
                    first_start = randint(1, 10 - self.ships[ship])
                    for i in range(-1, self.ships[ship] + 1):
                        for g in range(-1, 2):
                            if self.board[first_start + i][second + g] != 0:
                                no = 1
                    if no == 0:
                        add = []
                        for i in range(self.ships[ship]):
                            self.board[first_start + i][second] = 1
                            add.append([[first_start + i, second], False])
                        self.theships.append(add)
                        break


    def render(self, screen):
        letters = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'К']
        numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
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
                if self.board[i][g] == 0:  # обычная клетка - квадрат с синими сторонами
                    pygame.draw.rect(screen, (109, 104, 255), (self.top + g * self.cell_size,
                                                               self.left + i * self.cell_size,
                                                               self.cell_size, self.cell_size), 1)
                elif self.board[i][g] == 1:
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

    def getfired(self, screen, board1, board2):
        from random import randint
        stop = False
        while True:
            if is_game_over(board1, board2) != '':
                break
            if len(self.recomendation) > 0:
                coord = self.recomendation[randint(0, len(self.recomendation) - 1)]
                print('Из списка рандома:')
                print(self.recomendation)
                print('Рандом выбрал:')
                print(coord)
                if not (1 <= coord[0] <= 10 and 1 <= coord[1] <= 10):
                    self.recomendation.remove(coord)
                    print('И убрал, тк вне поля')
                if self.board[coord[0]][coord[1]] == 1 and (1 <= coord[0] <= 10 and 1 <= coord[1] <= 10):
                    self.board[coord[0]][coord[1]] = 3
                    print('И попал')
                    if not self.check(coord[0], coord[1]):
                        self.recomendation.clear()
                        print('Добив корабль')
                        stop = True
                    screen.fill('white')
                    board2.render(screen)
                    board1.render(screen)
                    pygame.display.flip()
                    pygame.time.wait(1000)
                    if stop:
                        continue
                    elif len(self.hit) == 2:
                        print('Тк попал второй раз')
                        print('Самое первое попадание и это попадание')
                        print([self.hit[0], coord])
                        removelist = []
                        if self.hit[0][0] == coord[0]:
                            print('Общая прямая горизонтальная')
                            first = self.hit[0][0]
                            print(first)
                            print('Рекомендация до сортировки')
                            print(self.recomendation)
                            for i in self.recomendation:
                                if i[0] != first:
                                    removelist.append(i)
                            for i in removelist:
                                self.recomendation.remove(i)
                            self.recomendation.remove(coord)
                            print('После')
                            print(self.recomendation)
                            print('Не помню, что делает')
                            if self.hit[0][1] < coord[1]:
                                self.recomendation.append([first, coord[1] + 1])
                            else:
                                self.recomendation.append([first, coord[1] - 1])
                            print(self.recomendation)
                        elif self.hit[0][1] == coord[1]:
                            print('Общая прямая вертикальная')
                            second = self.hit[0][1]
                            print(second)
                            print('Рекомендация до сортировки')
                            print(self.recomendation)
                            for i in self.recomendation:
                                if i[1] != second:
                                    removelist.append(i)
                            for i in removelist:
                                self.recomendation.remove(i)
                            self.recomendation.remove(coord)
                            print('После')
                            print(self.recomendation)
                            print('Не знаю что делает')
                            if self.hit[0][0] < coord[0]:
                                self.recomendation.append([coord[0] + 1, second])
                            else:
                                self.recomendation.append([coord[0] - 1, second])
                            print(self.recomendation)
                    elif len(self.hit) == 3:
                        print('Попал в 3й раз')
                        print('До сортировки')
                        print(self.recomendation)
                        print('После')
                        if self.hit[0][0] == coord[0]:
                            first = self.hit[0][0]
                            if self.hit[0][1] < coord[1]:
                                self.recomendation.append([first, coord[1] + 1])
                            else:
                                self.recomendation.append([first, coord[1] - 1])
                        elif self.hit[0][1] == coord[1]:
                            second = self.hit[0][1]
                            if self.hit[0][0] < coord[0]:
                                self.recomendation.append([coord[0] + 1, second])
                            else:
                                self.recomendation.append([coord[0] - 1, second])
                        self.recomendation.remove(coord)
                        print(self.recomendation)
                elif self.board[coord[0]][coord[1]] == 3 and (1 <= coord[0] <= 10 and 1 <= coord[1] <= 10):
                    self.recomendation.remove(coord)
                    print('Там уже корабль')
                    print(self.recomendation)
                elif self.board[coord[0]][coord[1]] == 0 and (1 <= coord[0] <= 10 and 1 <= coord[1] <= 10):
                    self.board[coord[0]][coord[1]] = 2
                    print('Там ничего нет')
                    screen.fill('white')
                    board2.render(screen)
                    board1.render(screen)
                    pygame.display.flip()
                    pygame.time.wait(1000)
                    self.recomendation.remove(coord)
                    print(self.recomendation)
                    break
                elif self.board[coord[0]][coord[1]] == 2 and (1 <= coord[0] <= 10 and 1 <= coord[1] <= 10):
                    print('Там уже пустая клетка')
                    self.recomendation.remove(coord)
                    print(self.recomendation)
            else:
                x, y = randint(1, 10), randint(1, 10)
                if self.board[x][y] == 0:
                    self.board[x][y] = 2
                    print('Промазал')
                    print(x, y)
                    screen.fill('white')
                    board2.render(screen)
                    board1.render(screen)
                    pygame.display.flip()
                    pygame.time.wait(1000)
                    break
                elif self.board[x][y] == 1:
                    self.board[x][y] = 3
                    print('Попал впервые')
                    print(x, y)
                    if self.check(x, y):
                        if len(self.hit) == 1:
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
            if is_game_over(board1, board2) != '':
                break
            print('')



    def check(self, x, y):
        for I in range(len(self.theships)):
            for q in range(len(self.theships[I])):
                if self.theships[I][q] == [[x, y], False]:
                    self.theships[I][q][1] = True
                    if all(self.theships[I][r][1] for r in range(len(self.theships[I]))):
                        if len(self.theships[I]) == 1:
                            first = self.theships[I][0][0][0]
                            second = self.theships[I][0][0][1]
                            for i in range(-1, len(self.theships[I]) + 1):
                                for g in range(-1, 2):
                                    if not (i == 0 and g == 0):
                                        self.board[first + g][second + i] = 2
                        elif self.theships[I][1][0][0] == self.theships[I][0][0][0]:
                            first = self.theships[I][0][0][0]
                            second_start = min(x[0][1] for x in self.theships[I])
                            for i in range(-1, len(self.theships[I]) + 1):
                                for g in range(-1, 2):
                                    self.board[first + g][second_start + i] = 2
                            for i in range(len(self.theships[I])):
                                self.board[first][second_start + i] = 3
                        elif self.theships[I][1][0][1] == self.theships[I][0][0][1]:
                            second = self.theships[I][0][0][1]
                            first_start = min(x[0][0] for x in self.theships[I])
                            for i in range(-1, len(self.theships[I]) + 1):
                                for g in range(-1, 2):
                                    self.board[first_start + i][second + g] = 2
                            for i in range(len(self.theships[I])):
                                self.board[first_start + i][second] = 3
                        self.hit.clear()
                        return False
                    else:
                        self.hit.append([x, y])
                        return True


class EnemyBoard:
    def __init__(self):
        self.board = []
        for i in range(12):
            add = []
            for g in range(12):
                add.append([0, 0])  # первое число - стреляли \ не стреляли, 2ое - есть корабль, нет
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


class MainScene():
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
            clock.tick(60)
        pygame.quit()


class RulesScene():
    def __init__(self):
        pygame.init()
        self.back = False
        pygame.display.set_caption('Naval Battle')
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((1400, 600))
        screen.fill('white')
        intro_text = ["Принцип «Морского боя» очень прост.",
                      "Вы расставляете свои корабли на поле 10х10, оппонент расставляет свои.",
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
                    pygame.quit()
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if board2.fired(event.pos, screen, board1, board2):
                        board2.render(screen)
                        board1.render(screen)
                        pygame.display.flip()
                        is_game_over(board1, board2)
                        if is_game_over(board1, board2) == '':
                            board1.getfired(screen, board1, board2)
                            if is_game_over(board1, board2) != '':
                                pygame.quit()
                                Winner(is_game_over(board1, board2))
                                self.running = False
                        else:
                            pygame.quit()
                            Winner(is_game_over(board1, board2))
                            self.running = False
            if self.running:
                board1.render(screen)
                board2.render(screen)
                pygame.display.flip()


class Winner():
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


def is_game_over(board1, board2):
    winner = ''
    NOT = False
    for i in board1.board:
        if any(g == 1 for g in i):
            NOT = True
            break
    if not NOT:
        winner = 'Оппонент победил :-('
    else:
        NOT = False
        for i in board2.board:
            if any(g[1] == 1 and g[0] == 0 for g in i):
                NOT = True
                break
        if not NOT:
            winner = 'Вы победили :-)'
    return winner


def start():
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

start()
