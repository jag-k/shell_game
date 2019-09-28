from typing import List
from random import randint
from lib import *

TITLE = "НАПЁРСТКИ"
title = ""
index = 0
count = [0, 0]


def start(size: SIZE_TYPE):
    global index, TITLE, title
    y, x = size
    delay = int(not args("-f", "--fast"))

    while title != TITLE:
        if index < x:
            print('\r%s' % Color(' ' * index, 30, 47), end='', flush=True)
            index += 1
            time.sleep(0.001 * delay)
        else:
            print('\r%s' % Color(center_text(size, title + (' ' * (len(TITLE) - len(title)))), 30, 47),
                  end='', flush=True)
            time.sleep(0.25 * delay)
            title = TITLE[:len(title) + 1]
    else:
        print('\r%s' % Color(center_text(size, title), 30, 47), flush=True)


def render_doc(size: SIZE_TYPE):
    print()
    slow_print(DOC % (CUP_SYMBOL, STAR_SYMBOL))

    i = input()
    if if_yes(i):
        slow_print("Тогда начинаем)")
        time.sleep(1)
    else:
        slow_print("Ну, тогда до встречи)")
    return if_yes(i)


def game(size: SIZE_TYPE):
    y, x = size

    def print_swap_position(s: List[str]):
        print("\r" + center_text(size, ''.join(s), False), end='', flush=True)

    swap_count = randint(4, 7)
    swaps = [randint(0, 2) for _ in range(swap_count)]
    start_pos = randint(0, 2)
    current_pos = [0, 0, 0]
    current_pos[start_pos] = 1
    speed = 0.1

    if args("-H", "--super-hard"):
        speed = 0.025
    elif args("-h", "--hard"):
        speed = 0.05
    elif args("-e", "--easy"):
        speed = 0.2
    elif args("-E", "--super-easy"):
        speed = 0.4

    print('\r' + Color(center_text(size, title), 30, 47), flush=True)
    print(center_text(size, "Счёт %s:%s" % (Color(count[0], Color.GREEN), Color(count[1], Color.RED))), flush=True)
    print('\n' * (y//2 - 2), end='', flush=True)
    print_swap_position(START_POSITION[start_pos])
    time.sleep(1.5)
    print_swap_position(START_POSITION[-1])
    time.sleep(0.5)
    for swap in swaps:
        if swap == 0:
            current_pos[1], current_pos[2] = current_pos[2], current_pos[1]
        elif swap == 1:
            current_pos[0], current_pos[1] = current_pos[1], current_pos[0]
        elif swap == 2:
            current_pos[0], current_pos[2] = current_pos[2], current_pos[0]

        for s in SWAPS[swap]:
            print_swap_position(s)
            time.sleep(speed)

    answer = input(('\n' * (y - y//2 - 4)) + "В каком стакане звёздочка? (1, 2, 3): ")
    while answer.strip() not in "123":
        answer = input("Вы ввели данные неверно! Повторите попытку (1, 2, 3): ")
    if int(answer) - 1 != current_pos.index(1):
        count[1] += 1
        star_index = current_pos.index(1) + 1
        print(Color(center_text(size, 'Вы проиграли( Счёт %s:%s' % tuple(count)), Color.ON_RED))
        print(center_text(size, 'Звёздочка была в%s %s стакане' % ("о" if star_index == 2 else "",
                                                                   Color(star_index, Color.GREEN))))
    else:
        count[0] += 1
        print(Color(center_text(size, 'Вы выиграли!)) Счёт %s:%s' % tuple(count)), Color.ON_GREEN))

    cont = input("Вы хотите продолжить? (Д/н): ")
    if if_yes(cont):
        slow_print("Тогда продолжим)")
        time.sleep(0.4)
    else:
        slow_print("Ну, тогда до встречи)")
    return if_yes(cont)
