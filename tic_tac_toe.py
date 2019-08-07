import pygame, sys
from pygame.locals import *
from threading import Timer


def init_settings():
    global draw, count, player, window, width, height, mainFont, start_coordinates_x, start_coordinates_y, final_board, box_size
    # Constants
    width = 500
    height = 500
    start_coordinates_x = width/2 - (width*0.65/2)
    start_coordinates_y = height/2 - (height*0.65/2)
    box_size = (width * 0.65)/3
    pygame.font.init()
    mainFont = pygame.font.SysFont('circe', 90)
    final_board = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
    player = 1
    count = 0
    draw = False

    # Functions
    pygame.init()
    pygame.display.set_caption('Tic Tac Toe')
    window = pygame.display.set_mode((width, height))
    window.fill((255, 255, 255))
    game_board = draw_lines(start_coordinates_x, start_coordinates_y, box_size)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                mouse_x, mouse_y = event.pos
                check_value(game_board, mouse_x, mouse_y)

        pygame.display.update()


def reset_game():
    global final_board, count
    if not draw:
        if player == 1:
            print('Player {} wins'.format(player + 1))
        elif player == 2:
            print('Player {} wins'.format(player - 1))
    else:
        print('Draw')
    final_board = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
    count = 0
    window.fill((255, 255, 255))
    draw_lines(start_coordinates_x, start_coordinates_y, box_size)
    pygame.display.update()


def win_game(win_str, point):
    global draw
    t = Timer(0.5, reset_game)
    if win_str == '1D':
        pygame.draw.line(window, (255, 0, 0), (start_coordinates_x, start_coordinates_y),
                         (start_coordinates_x + 3 * box_size, start_coordinates_y + 3 * box_size), 20)

    elif win_str == '2D':
        pygame.draw.line(window, (255, 0, 0), (start_coordinates_x + 3 * box_size, start_coordinates_y),
                         (start_coordinates_x, start_coordinates_y + 3 * box_size), 20)

    elif win_str == 'V':
        pygame.draw.line(window, (255, 0, 0), (start_coordinates_x + box_size/2 + point * box_size, start_coordinates_y),
                         (start_coordinates_x + box_size/2 + point * box_size, start_coordinates_y + 3 * box_size), 20)

    elif win_str == 'H':
        pygame.draw.line(window, (255, 0, 0), (start_coordinates_x, start_coordinates_y + box_size/2 + point * box_size),
                         (start_coordinates_x + 3 * box_size, start_coordinates_y + box_size/2 + point * box_size), 20)
    else:
        draw = True
    t.start()


def check_winner():
    first_diagonal = final_board[0][0] == final_board[1][1] == final_board[2][2]
    second_diagonal = final_board[0][2] == final_board[1][1] == final_board[2][0]
    if count < 9:
        if first_diagonal:
            win_game('1D', None)
        elif second_diagonal:
            win_game('2D', None)
        else:
            for n in range(len(final_board)):
                vertical = final_board[n][0] == final_board[n][1] == final_board[n][2]
                horizontal = final_board[0][n] == final_board[1][n] == final_board[2][n]
                if horizontal:
                    win_game('V', n)
                elif vertical:
                    win_game('H', n)
    elif count == 9:
        win_game('Draw', None)


def check_value(arr, x, y):
    click_pair = None
    for i in range(len(arr)):
        for j in range(len(arr)):
            if arr[i][j].collidepoint(x, y):
                click_pair = (i, j)
    if click_pair is not None and type(final_board[click_pair[0]][click_pair[1]]) != str:
        input_box(arr, click_pair)


def input_box(arr, pair):
    global player, count, final_board
    main_array = arr[pair[0]][pair[1]]
    mark = ''
    count += 1
    if player == 1:
        final_board[pair[0]][pair[1]] = 'X'
        mark = mainFont.render('X', True, (0, 0, 0))
        player += 1
        window.blit(mark, (main_array.left + 20, main_array.top))
    elif player == 2:
        final_board[pair[0]][pair[1]] = 'O'
        mark = mainFont.render('O', True, (0, 0, 0))
        player -= 1
        window.blit(mark, (main_array.left + 20, main_array.top))

    if count > 4:
        check_winner()


def draw_lines(x, y, box):
    array_rect = [[], [], []]
    column = 0
    x_payload = x
    y_payload = y
    for n in range(9):
        if n < 3:
            payload = pygame.draw.rect(window, (0, 0, 0), (x_payload, y_payload, box, box), 2)
            array_rect[column].append(payload)
            x_payload += box
        elif n % 3 == 0:
            x_payload = x
            y_payload += box
            column += 1
            payload = pygame.draw.rect(window, (0, 0, 0), (x_payload, y_payload, box, box), 2)
            array_rect[column].append(payload)
            x_payload += box
        elif n > 3:
            payload = pygame.draw.rect(window, (0, 0, 0), (x_payload, y_payload, box, box), 2)
            array_rect[column].append(payload)
            x_payload += box
    # Box Lines
    pygame.draw.rect(window, (255, 255, 255), (start_coordinates_x, start_coordinates_y, 3*box, 2))
    pygame.draw.rect(window, (255, 255, 255), (start_coordinates_x, start_coordinates_y, 2, 3 * box))
    pygame.draw.rect(window, (255, 255, 255), (start_coordinates_x, start_coordinates_y + 3*box - 2, 3 * box, 4))
    pygame.draw.rect(window, (255, 255, 255), (start_coordinates_x + 3*box - 2, start_coordinates_y, 4, 3 * box))
    return array_rect


if __name__ == '__main__':
    init_settings()
