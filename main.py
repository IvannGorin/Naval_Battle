import pygame

class MyBoard:
    def __init__(self):
        self.board = [[0] * 8 for i in range(8)] ## 0 - пусто, 1 - мимо, 2 - попал
        self.width, self.height = 8, 8
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

class EnemyBoard:
    def __init__(self):
        self.board = [[0] * 8 for i in range(8)]
        self.width, self.height = 8, 8
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
            pass
        else:
            try:  # решение проблем с краями, которые выдают ошибку через IndexError
                self.board[the_cell[-1]][the_cell[0]] = 1
            except IndexError:
                pass

pygame.init()
pygame.display.set_caption('Naval Battle.')
size = width, height = 1000, 600
screen = pygame.display.set_mode(size)
board1 = MyBoard()
board2 = EnemyBoard()
running = True
while running:
    screen.fill('white')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            board2.fired(event.pos)
    board1.render(screen)
    board2.render(screen)
    pygame.display.flip()
pygame.quit()