# Gra wąż - na podstawie tutoriala Clear Code(Learning pygame by creating Snake)


import pygame
import sys
import os
import random
import pickle
from pygame.constants import BLENDMODE_ADD
from pygame.math import Vector2
from operator import itemgetter


class MUSHROOM:
    def __init__(self):
        self.mushroom_png = pygame.image.load(
            os.path.join('Graphics', 'mushroom.png')).convert_alpha()
        self.randomize()

    def draw_mushroom(self):
        x_pos = self.pos.x * CELL_SIZE
        y_pos = self.pos.y * CELL_SIZE
        mushroom_rect = pygame.Rect(
            int(x_pos), int(y_pos), CELL_SIZE, CELL_SIZE)
        screen.blit(self.mushroom_png, mushroom_rect)

    def randomize(self):
        self.x = random.randint(0, CELL_NUMBER_H - 1)
        self.y = random.randint(1, CELL_NUMBER_V - 1)
        self.pos = Vector2(self.x, self.y)


class MUSHROOM_BAD:
    def __init__(self):
        self.mushroom_bad = pygame.image.load(os.path.join(
            'Graphics', 'bad_mushroom.png')).convert_alpha()
        self.mushroom_bad_list = []
        self.mushroom_bad_count = 0
        self.randomize()

    def draw_mushroom(self):
        for index, block in enumerate(self.mushroom_bad_list):
            x_pos = block.x * CELL_SIZE
            y_pos = block.y * CELL_SIZE
            mushroom_rect = pygame.Rect(
                int(x_pos), int(y_pos), CELL_SIZE, CELL_SIZE)
            screen.blit(self.mushroom_bad, mushroom_rect)

    # todo: usuwanie pierwszego grzyba z listy
    # def remove_mushroom(self):
    #     del self.mushroom_bad_list[0]
    #     print(self.mushroom_bad_list)

    def randomize(self):
        self.x = random.randint(0, CELL_NUMBER_H - 1)
        self.y = random.randint(1, CELL_NUMBER_V - 1)
        self.pos = Vector2(self.x, self.y)

    def generate(self):
        self.mushroom_bad_list.append(self.pos)
        self.mushroom_bad_count = len(self.mushroom_bad_list)

    # resetowanie muchomorów po grze
    def reset(self):
        self.mushroom_bad_list = []
        self.mushroom_bad_count = 0


class MUSHROOM_GOLD:
    def __init__(self):
        self.mushroom_gold = pygame.image.load(
            os.path.join('Graphics', 'gold_mushroom.png')).convert_alpha()
        self.active = False
        self.pos = []

    def draw_mushroom(self):
        if self.active == True:
            x_pos = self.pos.x * CELL_SIZE
            y_pos = self.pos.y * CELL_SIZE
            mushroom_gold_rect = pygame.Rect(
                int(x_pos), int(y_pos), CELL_SIZE, CELL_SIZE)
            screen.blit(self.mushroom_gold, mushroom_gold_rect)

    def randomize(self):
        r = random.randrange(0, 4)
        if r == 0:
            self.x = random.randint(0, CELL_NUMBER_H - 1)
            self.y = random.randint(1, CELL_NUMBER_V - 1)
            self.pos = Vector2(self.x, self.y)
            self.active = True
        else:
            self.reset()

    def reset(self):
        self.pos = []
        self.active = False


class PLAYER:
    def __init__(self):
        self.body = [Vector2(5, 7), Vector2(4, 7)]
        self.direction = Vector2(1, 0)
        self.new_block = False
        # Grafiki gracz zależnie od kierunku ruchu
        # głowa
        self.head_up = pygame.image.load(os.path.join(
            'Graphics', 'ewa_up.png')).convert_alpha()
        self.head_down = pygame.image.load(os.path.join(
            'Graphics', 'ewa_down.png')).convert_alpha()
        self.head_left = pygame.image.load(os.path.join(
            'Graphics', 'ewa_left.png')).convert_alpha()
        self.head_right = pygame.image.load(
            os.path.join('Graphics', 'ewa_right.png')).convert_alpha()
        # ciało
        self.player_mushroom_left = pygame.image.load(
            os.path.join('Graphics', 'mushroom_small_left.png')).convert_alpha()
        self.player_mushroom_right = pygame.image.load(
            os.path.join('Graphics', 'mushroom_small_right.png')).convert_alpha()
        self.player_mushroom_down = pygame.image.load(
            os.path.join('Graphics', 'mushroom_small_down.png')).convert_alpha()
        self.player_mushroom_up = pygame.image.load(
            os.path.join('Graphics', 'mushroom_small_up.png')).convert_alpha()
        # ogon
        self.tail_left = pygame.image.load(
            os.path.join('Graphics', 'mushroom_small_last_left.png')).convert_alpha()
        self.tail_right = pygame.image.load(
            os.path.join('Graphics', 'mushroom_small_last_right.png')).convert_alpha()
        self.tail_down = pygame.image.load(
            os.path.join('Graphics', 'mushroom_small_last_down.png')).convert_alpha()
        self.tail_up = pygame.image.load(
            os.path.join('Graphics', 'mushroom_small_last_up.png')).convert_alpha()

        # zakręty
        self.turn_right_top = pygame.image.load(
            os.path.join('Graphics', 'mushroom_small_turn_rt.png')).convert_alpha()
        self.turn_left_top = pygame.image.load(
            os.path.join('Graphics', 'mushroom_small_turn_lt.png')).convert_alpha()
        self.turn_top_left = pygame.image.load(
            os.path.join('Graphics', 'mushroom_small_turn_tl.png')).convert_alpha()
        self.turn_top_right = pygame.image.load(
            os.path.join('Graphics', 'mushroom_small_turn_tr.png')).convert_alpha()

    # rysowanie węża

    def draw_player(self):
        self.update_head_graphics()
        self.update_tail_graphics()
        for index, block in enumerate(self.body):
            x_pos = block.x * CELL_SIZE
            y_pos = block.y * CELL_SIZE
            block_rect = pygame.Rect(
                int(x_pos), int(y_pos), CELL_SIZE, CELL_SIZE)

            if index == 0:  # głowa
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:  # ogon
                screen.blit(self.tail, block_rect)
            # ciało
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block

                if previous_block.y == next_block.y:
                    if previous_block == Vector2(1, 0):
                        screen.blit(self.player_mushroom_left, block_rect)
                    elif previous_block == Vector2(-1, 0):
                        screen.blit(self.player_mushroom_right, block_rect)
                if previous_block.x == next_block.x:
                    if previous_block == Vector2(0, 1):
                        screen.blit(self.player_mushroom_up, block_rect)
                    elif previous_block == Vector2(0, -1):
                        screen.blit(self.player_mushroom_down, block_rect)
                # zakręty
                else:
                    if previous_block.y == -1 and next_block.x == -1 or previous_block.x == -1 and next_block.y == -1:
                        screen.blit(self.turn_right_top, block_rect)
                    elif previous_block.y == -1 and next_block.x == 1 or previous_block.x == 1 and next_block.y == -1:
                        screen.blit(self.turn_left_top, block_rect)
                    elif previous_block.y == 1 and next_block.x == -1 or previous_block.x == -1 and next_block.y == 1:
                        screen.blit(self.turn_top_left, block_rect)
                    elif previous_block.y == 1 and next_block.x == 1 or previous_block.x == 1 and next_block.y == 1:
                        screen.blit(self.turn_top_right, block_rect)

    # grafika głowy węża zgodnie z kierunkiem ruchu
    def update_head_graphics(self):
        head_position = self.body[1] - self.body[0]
        if head_position == Vector2(1, 0):
            self.head = self.head_left
        elif head_position == Vector2(-1, 0):
            self.head = self.head_right
        elif head_position == Vector2(0, 1):
            self.head = self.head_up
        elif head_position == Vector2(0, -1):
            self.head = self.head_down

    def update_tail_graphics(self):
        tail_position = self.body[-2] - self.body[-1]
        if tail_position == Vector2(-1, 0):
            self.tail = self.tail_left
        elif tail_position == Vector2(1, 0):
            self.tail = self.tail_right
        elif tail_position == Vector2(0, -1):
            self.tail = self.tail_up
        elif tail_position == Vector2(0, 1):
            self.tail = self.tail_down

    # poruszanie węża
    def move_player(self):

        if self.new_block == True:
            body_copy = self.body[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
        body_copy.insert(0, body_copy[0] + self.direction)
        self.body = body_copy[:]

        # if self.new_block == True:
        #     body_copy = self.body[:]

        #     body_copy.insert(0, body_copy[0] + self.direction)
        #     self.body = body_copy[:]
        #     self.new_block = False
        # else:
        #     body_copy = self.body[:-1]
        #     body_copy.insert(0, body_copy[0] + self.direction)
        #     self.body = body_copy[:]


    def add_block(self):
        self.new_block = True

    # resetowanie węża po grze
    def reset(self):
        self.body = [Vector2(5, 7), Vector2(4, 7)]
        self.direction = Vector2(1, 0)


class MAIN:
    def __init__(self):
        self.player = PLAYER()
        self.mushroom = MUSHROOM()
        self.mushroom_bad = MUSHROOM_BAD()
        self.mushroom_gold = MUSHROOM_GOLD()
        self.score = 1
        self.count_mushroom = 1
        self.count_mushroom_gold = 0
        self.record = 0
        self.state = 'menu'
        self.menu_position = 1
        self.name = 'Ewa'
        self.unavailable_list = []
        self.start_game = True
        self.highscore = []
        self.start_active = True
        self.name_rect_active = False

    def state_manager(self):
        if self.state == 'menu':
            self.menu()
            self.game_reset()
        elif self.state == 'game':
            if self.start_game == True:
                pygame.mixer.music.play(-1)
                self.start_game = False
            self.game()
        elif self.state == 'game_over':
            pygame.mixer.music.stop()
            self.game_over_screen()
        elif self.state == 'highscore':
            self.highscore_list()

    def menu(self):
        screen.blit(BACKGROUND_IMAGE, (0, 0))

        # tekst nazwa gry
        game_title_text_caption = game_font_title_very_big.render(
            'mikroSnake', True, GREEN_FONT_COLOR)
        game_text_caption_rect = game_title_text_caption.get_rect(
            center=(SCREEN_WIDTH/2, 70))

        # tekst start
        if self.menu_position == 1:
            start_text = game_font_big.render(
                'Start', True, GREEN_FONT_COLOR_ACTIVE)
        else:
            start_text = game_font_big.render('Start', True, GREEN_FONT_COLOR)
        start_text_rect = start_text.get_rect(center=(SCREEN_WIDTH/2, 190))

        # tekst do imienia
        if self.menu_position == 2:
            name_text_caption = game_font_big.render(
                'Gracz:', True, GREEN_FONT_COLOR_ACTIVE)
        else:
            name_text_caption = game_font_big.render(
                'Gracz:', True, GREEN_FONT_COLOR)
        name_text_caption_rect = name_text_caption.get_rect(
            center=(SCREEN_WIDTH/2-70, 270))

        # tekst imię
        input_name_rect = pygame.rect.Rect(495, 237, 100, 250)
        if self.name_rect_active == True:
            input_font_color = (255, 255, 255)
            name_text = game_font_big.render(
                self.name + '_', True, input_font_color)
        else:
            input_font_color = GREEN_FONT_COLOR_ACTIVE
            name_text = game_font_big.render(self.name, True, input_font_color)

        # tekst wyniki
        if self.menu_position == 3:
            result_text = game_font_big.render(
                'Najlepsze wyniki', True, GREEN_FONT_COLOR_ACTIVE)
        else:
            result_text = game_font_big.render(
                'Najlepsze wyniki', True, GREEN_FONT_COLOR)
        result_text_rect = result_text.get_rect(center=(SCREEN_WIDTH/2, 355))

        # tekst koniec
        if self.menu_position == 4:
            end_text = game_font_big.render(
                'Wyjście', True, GREEN_FONT_COLOR_ACTIVE)
        else:
            end_text = game_font_big.render('Wyjście', True, GREEN_FONT_COLOR)
        end_text_rect = end_text.get_rect(center=(SCREEN_WIDTH/2, 440))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if start_text_rect.collidepoint(x, y):
                    self.state = 'game'
                if result_text_rect.collidepoint(x, y):
                    self.state = 'highscore'
                if end_text_rect.collidepoint(x, y):
                    pygame.quit()
                    sys.exit()
                if input_name_rect.collidepoint(x, y) or name_text_caption_rect.collidepoint(x, y):
                    if self.name_rect_active == True:
                        self.name_rect_active = False
                    else:
                        self.name_rect_active = True
                        self.menu_position = 2

            if event.type == pygame.KEYDOWN:
                if self.name_rect_active:
                    if event.key == pygame.K_RETURN:
                        self.name_rect_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        self.name = self.name[:-1]
                    else:
                        if(len(self.name) < 10):
                            self.name += event.unicode
                else:
                    if event.key == pygame.K_DOWN and self.menu_position < 4:
                        self.menu_position += 1
                    if event.key == pygame.K_UP and self.menu_position > 1:
                        self.menu_position -= 1
                    if event.key == pygame.K_RETURN:
                        if self.menu_position == 2:
                            self.name_rect_active = True
                        elif self.menu_position == 4:
                            pygame.quit()
                            sys.exit()
                        else:
                            self.state = MENU_DICT[self.menu_position]
                    if event.key == pygame.K_s:
                        self.state = 'game'
                    if event.key == pygame.K_n:
                        self.state = 'highscore'
                        self.highscore_list()
                    if event.key == pygame.K_g:
                        if self.name_rect_active == True:
                            self.name_rect_active = False
                        else:
                            self.name_rect_active = True
                            self.menu_position = 2
                    if event.key == pygame.K_w:
                        pygame.quit()
                        sys.exit()

        screen.blit(game_title_text_caption, game_text_caption_rect)
        screen.blit(start_text, start_text_rect)
        screen.blit(name_text_caption, name_text_caption_rect)
        screen.blit(name_text, input_name_rect)
        screen.blit(result_text, result_text_rect)
        screen.blit(end_text, end_text_rect)
        # pygame.display.update()

    def game(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == SCREEN_UPDATE:
                main_game.update()
            if event.type == MUSHROOM_GEN:
                if self.score > 6:
                    self.mushroom_gold.randomize()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and main_game.player.direction.y != 1:
                    main_game.player.direction = Vector2(0, -1)
                if event.key == pygame.K_DOWN and main_game.player.direction.y != -1:
                    main_game.player.direction = Vector2(0, 1)
                if event.key == pygame.K_LEFT and main_game.player.direction.x != 1:
                    main_game.player.direction = Vector2(-1, 0)
                if event.key == pygame.K_RIGHT and main_game.player.direction.x != -1:
                    main_game.player.direction = Vector2(1, 0)
            if event.type == pygame.JOYAXISMOTION:
                if j.get_axis(1) <= -0.5 and main_game.player.direction.y != 1:
                    main_game.player.direction = Vector2(0, -1)
                if j.get_axis(1) >= 0.5 and main_game.player.direction.y != -1:
                    main_game.player.direction = Vector2(0, 1)
                if j.get_axis(0) <= -0.5 and main_game.player.direction.x != 1:
                    main_game.player.direction = Vector2(-1, 0)
                if j.get_axis(0) >= 0.5 and main_game.player.direction.x != -1:
                    main_game.player.direction = Vector2(1, 0)

        # rysuj wszystkie elementy
        #screen.fill(pygame.Color((134, 170, 74)))
        main_game.draw_elements()

    def update(self):
        self.player.move_player()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.draw_grass()
        self.draw_points()
        self.player.draw_player()
        self.mushroom_bad.draw_mushroom()
        self.mushroom.draw_mushroom()
        self.mushroom_gold.draw_mushroom()

    def check_collision(self):
        # złapanie grzyba
        if self.mushroom.pos == self.player.body[0]:
            sound_catch.play()
            self.score += 1
            self.count_mushroom += 1
            self.player.add_block()
            self.mushroom.randomize()

        # sprawdzenie czy kurka
        if self.mushroom_gold.pos == self.player.body[0]:
            sound_catch.play()
            self.score += 3
            self.count_mushroom_gold += 1
            self.player.add_block()
            self.mushroom_gold.reset()

        # algorytm dodawania muchomorów
        # dodanie muchomora na początku
        # if self.mushroom_bad.mushroom_bad_count == 0:
        #     self.mushroom_bad.randomize()
        #     self.mushroom_bad.generate()
        # # dodanie muchomora gdy ilość punktów / ilość muchomorów > 2
        # else:
        #     if self.score / self.mushroom_bad.mushroom_bad_count > 2:
        #         self.mushroom_bad.randomize()
        #         available = 0
        #         # sprawdzenie czy muchomor nie generuje się w wężu lub tuż przed nim i powtórna generacja
        #         while available == 0:
        #             for block in self.player.body:
        #                 if block == self.mushroom.pos:
        #                     self.mushroom_bad.randomize()
        #                     continue
        #             if block == self.player.body[0] + self.player.direction or block == self.player.body[0] + (self.player.direction * 2):
        #                 self.mushroom_bad.randomize()
        #                 continue
        #             available = 1
        #         self.mushroom_bad.generate()

         # dodanie muchomora na początku oraz gdy ilość punktów / ilość muchomorów > 2
        if self.mushroom_bad.mushroom_bad_count == 0 or self.score / self.mushroom_bad.mushroom_bad_count > 2:
            self.mushroom_bad.randomize()
            available = 0
            # sprawdzenie czy muchomor nie generuje się w wężu lub tuż przed nim i powtórna generacja
            while available == 0:
                for block in self.player.body:
                    if block == self.mushroom.pos:
                        self.mushroom_bad.randomize()
                        continue
                if block == self.player.body[0] + self.player.direction or block == self.player.body[0] + (self.player.direction * 2):
                    self.mushroom_bad.randomize()
                    continue
                available = 1
            self.mushroom_bad.generate()

        # sprawdzenie czy grzyb nie generuje się w wężu lub w muchomorze
        available = 0
        unavailable_list = self.player.body + self.mushroom_bad.mushroom_bad_list
        unavailable_list.append(self.mushroom_gold.pos)
        while available == 0:
            for block in unavailable_list:
                if block == self.mushroom.pos:
                    self.mushroom.randomize()
                    continue
                available = 1

    def check_fail(self):
        # ściany
        if not 0 <= self.player.body[0].x < CELL_NUMBER_H:
            self.game_over()
        if not 1 <= self.player.body[0].y < CELL_NUMBER_V:
            self.game_over()

        # ciało węża
        for block in self.player.body[1:]:
            if block == self.player.body[0]:
                self.game_over()

        for block in self.mushroom_bad.mushroom_bad_list[:]:
            if block == self.player.body[0]:
                self.game_over()

    def draw_grass(self):
        grass_color = (134, 178, 74)
        screen.fill(pygame.Color((134, 170, 74)))
        for row in range(CELL_NUMBER_V):
            if row % 2 == 0:
                for col in range(CELL_NUMBER_H):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(
                            col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range(CELL_NUMBER_H):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(
                            col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                        pygame.draw.rect(screen, grass_color, grass_rect)

    def draw_points(self):  # górna listwa z punktacją
        points_screen_rect = pygame.Rect(
            0, 0, CELL_NUMBER_H * CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, (134, 178, 74), points_screen_rect)
        pygame.draw.line(screen, (15, 60, 15), (0, CELL_SIZE),
                         (CELL_SIZE*CELL_NUMBER_H, CELL_SIZE), 2)

        # tekst z tytułem
        title_text = game_font_title.render(
            'mikroSnake', True, GREEN_FONT_COLOR)
        title_text_rect = title_text.get_rect(center=(120, CELL_SIZE/2))
        screen.blit(title_text, title_text_rect)

        # Licznik grzybów
        mushroom_points = pygame.image.load(
            os.path.join('Graphics', 'mushroom_points.png')).convert_alpha()
        points_rect = pygame.Rect(260, 6, CELL_SIZE, CELL_SIZE)
        screen.blit(mushroom_points, points_rect)

        mushroom_counter_text = game_font_very_small.render(
            str(self.count_mushroom), True, GREEN_FONT_COLOR)
        mushroom_counter_text_rect = mushroom_counter_text.get_rect(
            center=(300, CELL_SIZE/2))
        screen.blit(mushroom_counter_text, mushroom_counter_text_rect)

        # Licznik kurek
        mushroom_gold_points = pygame.image.load(
            os.path.join('Graphics', 'gold_mushroom_points.png')).convert_alpha()
        mushroom_gold_points_rect = pygame.Rect(340, 6, CELL_SIZE, CELL_SIZE)
        screen.blit(mushroom_gold_points, mushroom_gold_points_rect)

        mushroom_gold_counter_text = game_font_very_small.render(
            str(self.count_mushroom_gold), True, GREEN_FONT_COLOR)
        mushroom_gold_counter_text_rect = mushroom_gold_counter_text.get_rect(
            center=(380, CELL_SIZE/2))
        screen.blit(mushroom_gold_counter_text,
                    mushroom_gold_counter_text_rect)

        # Licznik muchomorów
        mushroom_bad_points = pygame.image.load(
            os.path.join('Graphics', 'bad_mushroom_points.png')).convert_alpha()
        mushroom_bad_points_rect = pygame.Rect(420, 6, CELL_SIZE, CELL_SIZE)
        screen.blit(mushroom_bad_points, mushroom_bad_points_rect)

        mushroom_bad_counter_text = game_font_very_small.render(
            str(self.mushroom_bad.mushroom_bad_count), True, GREEN_FONT_COLOR)
        mushroom_bad_counter_text_rect = mushroom_bad_counter_text.get_rect(
            center=(460, CELL_SIZE/2))
        screen.blit(mushroom_bad_counter_text, mushroom_bad_counter_text_rect)

        # punkty gracza
        points_counter_text = game_font_very_small.render(self.name + ': ' +
                                                          str(self.score), True, GREEN_FONT_COLOR)
        points_counter_text_rect = points_counter_text.get_rect(
            center=(600, CELL_SIZE/2))
        screen.blit(points_counter_text, points_counter_text_rect)

        if self.record > 0:
            highscore_text = game_font_very_small.render(
                'Rekord: ' + str(self.record), True, GREEN_FONT_COLOR)
            highscore_text_rect = highscore_text.get_rect(
                center=(750, CELL_SIZE/2))
            screen.blit(highscore_text, highscore_text_rect)

    def game_over(self):
        sound_end.play()
        pygame.time.wait(1000)
        if self.score > self.record:
            self.record = self.score
        self.highscore_check(self.name, self.score)
        self.game_over_screen()
        self.player.reset()
        self.mushroom_bad.reset()
        self.state = 'game_over'

    def game_over_screen(self):

        # rysuj wszystkie elementy

        screen.blit(BACKGROUND_IMAGE, (0, 0))

        # tekst Koniec gry
        end_text = game_font_very_big.render(
            'Koniec Gry!', True, GREEN_FONT_COLOR)
        end_text_rect = end_text.get_rect(center=(SCREEN_WIDTH/2, 60))
        screen.blit(end_text, end_text_rect)

        # punkty grzyby
        mushroom_points = pygame.image.load(
            os.path.join('Graphics', 'mushroom.png')).convert_alpha()
        points_rect = pygame.Rect(395, 160, CELL_SIZE, CELL_SIZE)
        screen.blit(mushroom_points, points_rect)

        if self.count_mushroom > 9:
            count_width = 340
        else:
            count_width = 360
        mushroom_counter_text_part1 = game_font_small.render(
            str(self.count_mushroom), True, GREEN_FONT_COLOR)
        mushroom_counter_text_part2 = game_font_small.render(
            'x  1  =  ' + str(self.count_mushroom), True, GREEN_FONT_COLOR)
        screen.blit(mushroom_counter_text_part1, (count_width, 150))
        screen.blit(mushroom_counter_text_part2, (450, 150))

        # punkty kurki
        mushroom_gold_points = pygame.image.load(
            os.path.join('Graphics', 'gold_mushroom.png')).convert_alpha()
        mushroom_gold_points_rect = pygame.Rect(395, 240, CELL_SIZE, CELL_SIZE)
        screen.blit(mushroom_gold_points, mushroom_gold_points_rect)

        if self.count_mushroom_gold > 9:
            count_width = 340
        else:
            count_width = 360
        mushroom_gold_counter_text_part1 = game_font_small.render(
            str(self.count_mushroom_gold), True, GREEN_FONT_COLOR)
        mushroom_gold_counter_text_part2 = game_font_small.render(
            'x  3  =  ' + str(self.count_mushroom_gold*3), True, GREEN_FONT_COLOR)
        screen.blit(mushroom_gold_counter_text_part1, (count_width, 230))
        screen.blit(mushroom_gold_counter_text_part2, (450, 230))

        pygame.draw.line(screen, (15, 60, 15), (330, 300), (630, 300), 2)

        score_counter_text = game_font_small.render(
            str(self.score), True, GREEN_FONT_COLOR)
        screen.blit(score_counter_text, (580, 308))

        # tekst - Menu
        menu_text = game_font_big.render(
            'Powrót do menu', True, GREEN_FONT_COLOR_ACTIVE)
        menu_text_rect = menu_text.get_rect(center=(SCREEN_WIDTH/2, 440))
        screen.blit(menu_text, menu_text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if menu_text_rect.collidepoint(x, y):
                    self.state = 'menu'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m or event.key == pygame.K_RETURN:
                    self.state = 'menu'

        # pygame.display.update()

    def game_reset(self):
        self.score = 1
        self.count_mushroom = 1
        self.count_mushroom_gold = 0
        self.start_game = True

    def highscore_unpickle(self):
        try:
            with open('highscore.dat', 'rb') as file:
                self.highscore = pickle.load(file)
                self.record = self.highscore[0][1]
        except:
            self.highscore = []

    def highscore_check(self, name, result):

        self.highscore.append((name, result))

        self.highscore = sorted(
            self.highscore, key=itemgetter(1), reverse=True)

        while len(self.highscore) > 10:
            del self.highscore[-1]

        with open('highscore.dat', 'wb') as file:
            pickle.dump(self.highscore, file)

    def highscore_list(self):
        screen.fill((134, 178, 74))

        # tekst nagłówek
        title_text = game_font_very_big.render(
            'Najlepsze wyniki', True, GREEN_FONT_COLOR)
        title_text_rect = title_text.get_rect(center=(SCREEN_WIDTH/2, 50))
        screen.blit(title_text, title_text_rect)
        # tekst powrót
        back_text = game_font_big.render(
            'Powrót do menu', True, GREEN_FONT_COLOR_ACTIVE)
        back_text_rect = back_text.get_rect(center=(SCREEN_WIDTH/2, 680))
        screen.blit(back_text, back_text_rect)

        result_width = 100
        for i in range(len(self.highscore)):
            if self.highscore[i][1] > 0:

                hs_place_text = game_font_small.render(
                    str(i + 1) + '.  ', True, GREEN_FONT_COLOR)
                hs_name_text = game_font_small.render(
                    str(self.highscore[i][0]), True, GREEN_FONT_COLOR)
                hs_place_result_text = game_font_small.render(
                    str(self.highscore[i][1]), True, GREEN_FONT_COLOR)
                screen.blit(hs_place_text, (220, result_width))
                screen.blit(hs_name_text, (290, result_width))
                screen.blit(hs_place_result_text, (690, result_width))
                result_width += 52

        # pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if back_text_rect.collidepoint(x, y):
                    self.state = 'menu'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p or event.key == pygame.K_RETURN:
                    self.state = 'menu'


# Stałe
CELL_SIZE = 40
CELL_NUMBER_H = 24  # poziomo
CELL_NUMBER_V = 18  # pionowo
SCREEN_WIDTH = CELL_NUMBER_H * CELL_SIZE
SCREEN_HEIGHT = CELL_NUMBER_V * CELL_SIZE
ICON = pygame.image.load(os.path.join('Graphics', 'mushroom.png'))
GREEN_FONT_COLOR = (53, 64, 35)
GREEN_FONT_COLOR_ACTIVE = (223, 243, 243)
GREEN_FONT_COLOR_NAME = (197, 225, 165)


pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
# Joystick/pad
pygame.joystick.init()
try:
    j = pygame.joystick.Joystick(0)  # create a joystick instance
    j.init()  # init instance
except pygame.error:
    pass
# monitor_size = [pygame.display.Info().current_w,
#                 pygame.display.Info().current_h]
screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

pygame.display.set_caption('mikroSnake')
pygame.display.set_icon(ICON)
clock = pygame.time.Clock()
current_time = 0

# Czcionki
game_font_very_big = pygame.font.Font(
    os.path.join('Fonts', 'NotoSerif.ttf'), 65)
game_font_big = pygame.font.Font(os.path.join('Fonts', 'NotoSerif.ttf'), 50)
game_font_small = pygame.font.Font(os.path.join('Fonts', 'NotoSerif.ttf'), 40)
game_font_very_small = pygame.font.Font(
    os.path.join('Fonts', 'NotoSerif.ttf'), 16)
game_font_title = pygame.font.Font(
    os.path.join('Fonts', 'PoorRichard.ttf'), 40)
game_font_title_very_big = pygame.font.Font(
    os.path.join('Fonts', 'PoorRichard.ttf'), 150)

# Tło
BACKGROUND_IMAGE = pygame.image.load(os.path.join(
    'Graphics', 'bg.png')).convert_alpha()
# Dżwięki
sound_catch = pygame.mixer.Sound(os.path.join('Sounds', 'catch.wav'))
sound_end = pygame.mixer.Sound(os.path.join('Sounds', 'end.wav'))
music = pygame.mixer.music.load(os.path.join('Sounds', 'music.mp3'))

# timer ruch węża(milisekundy)
SCREEN_UPDATE = pygame.USEREVENT + 1
pygame.time.set_timer(SCREEN_UPDATE, 190)
MUSHROOM_GEN = pygame.USEREVENT + 2
pygame.time.set_timer(MUSHROOM_GEN, random.randrange(4000, 6000))

MENU_DICT = {1: 'game', 2: 'name', 3: 'highscore', 4: 'exit'}

main_game = MAIN()
main_game.highscore_unpickle()


while True:
    main_game.state_manager()
    pygame.display.update()
    clock.tick(60)
