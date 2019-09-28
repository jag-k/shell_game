import platform
from sys import argv
import time
from color_class import Color
import os
import re


def clear():
    os.system("clr" if system == WINDOWS else "clear")


def args(*flags: str):
    arg = argv[1:]
    if any(i in arg for i in flags):
        return True
    for f in flags:
        if len(f) == 2 and f[0] == '-':
            return f[1] in ''.join(filter(lambda x: len(x) >= 2 and x[0] == '-' and x[1:].isalpha(), arg))
    return False


if args('-s', '--simple'):
    from simple_symbols import *
else:
    from symbols import *

if args("-c", "--no-color"):
    Color.DE_COLOR = True

SIZE_TYPE = (int, int)
WINDOWS = "Windows"
system = platform.system()

DOC = """Добро пожаловать в "НАПЁРСТКИ")
Правила игры очень просты:
    • Показваются 2 стакана (%s) и звёздочка (%s)
    • После этого звёздочка прячется под стакан, и стаканы меняются местами
    • В итоге, Вам нужно будет "найти" звёздочку под стаканом

P.S.: После запусука программы лучше не изменять размер терминала
P.P.S.: ЕСЛИ СТАКАН И ЗВЁЗДОЧКА ОТОБРАЖАЕТСЯ НЕ КОРРЕКТНО, 
        ТО ПРОЧИТАЙТЕ В ФАЙЛЕ "readme.txt" КАК ЭТО ИСПРАВИТЬ

Начнём играть?) (Д/н): """

START_POSITION = [
    [STAR_SYMBOL, " ", " ", " ", " ", " ", CUP_SYMBOL, " ", " ", " ", " ", " ", CUP_SYMBOL],
    [CUP_SYMBOL, " ", " ", " ", " ", " ", STAR_SYMBOL, " ", " ", " ", " ", " ", CUP_SYMBOL],
    [CUP_SYMBOL, " ", " ", " ", " ", " ", CUP_SYMBOL, " ", " ", " ", " ", " ", STAR_SYMBOL],
    [CUP_SYMBOL, " ", " ", " ", " ", " ", CUP_SYMBOL, " ", " ", " ", " ", " ", CUP_SYMBOL]
]

SWAP_RIGHT = [  # 0
    [CUP_SYMBOL, " ", " ", " ", " ", " ", CUP_SYMBOL, " ", " ", " ", " ", " ", CUP_SYMBOL],
    [CUP_SYMBOL, " ", " ", " ", " ", " ", " ", CUP_SYMBOL, " ", " ", " ", CUP_SYMBOL, " "],
    [CUP_SYMBOL, " ", " ", " ", " ", " ", " ", " ", CUP_SYMBOL, " ", CUP_SYMBOL, " ", " "],
    [CUP_SYMBOL, " ", " ", " ", " ", " ", " ", " ", " ", CUP_SYMBOL, " ", " ", " "],
    [CUP_SYMBOL, " ", " ", " ", " ", " ", " ", " ", CUP_SYMBOL, " ", CUP_SYMBOL, " ", " "],
    [CUP_SYMBOL, " ", " ", " ", " ", " ", " ", CUP_SYMBOL, " ", " ", " ", CUP_SYMBOL, " "],
    [CUP_SYMBOL, " ", " ", " ", " ", " ", CUP_SYMBOL, " ", " ", " ", " ", " ", CUP_SYMBOL]
]

SWAP_LEFT = [  # 1
    [CUP_SYMBOL, " ", " ", " ", " ", " ", CUP_SYMBOL, " ", " ", " ", " ", " ", CUP_SYMBOL],
    [" ", CUP_SYMBOL, " ", " ", " ", CUP_SYMBOL, " ", " ", " ", " ", " ", " ", CUP_SYMBOL],
    [" ", " ", CUP_SYMBOL, " ", CUP_SYMBOL, " ", " ", " ", " ", " ", " ", " ", CUP_SYMBOL],
    [" ", " ", " ", CUP_SYMBOL, " ", " ", " ", " ", " ", " ", " ", " ", CUP_SYMBOL],
    [" ", " ", CUP_SYMBOL, " ", CUP_SYMBOL, " ", " ", " ", " ", " ", " ", " ", CUP_SYMBOL],
    [" ", CUP_SYMBOL, " ", " ", " ", CUP_SYMBOL, " ", " ", " ", " ", " ", " ", CUP_SYMBOL],
    [CUP_SYMBOL, " ", " ", " ", " ", " ", CUP_SYMBOL, " ", " ", " ", " ", " ", CUP_SYMBOL]
]

SWAP_EDGE = [  # 2
    [CUP_SYMBOL, " ", " ", " ", " ", " ", CUP_SYMBOL, " ", " ", " ", " ", " ", CUP_SYMBOL],
    [" ", " ", CUP_SYMBOL, " ", " ", " ", CUP_SYMBOL, " ", " ", " ", CUP_SYMBOL, " ", " "],
    [" ", " ", " ", " ", CUP_SYMBOL, " ", CUP_SYMBOL, " ", CUP_SYMBOL, " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", CUP_SYMBOL, " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", CUP_SYMBOL, " ", CUP_SYMBOL, " ", CUP_SYMBOL, " ", " ", " ", " "],
    [" ", " ", CUP_SYMBOL, " ", " ", " ", CUP_SYMBOL, " ", " ", " ", CUP_SYMBOL, " ", " "],
    [CUP_SYMBOL, " ", " ", " ", " ", " ", CUP_SYMBOL, " ", " ", " ", " ", " ", CUP_SYMBOL]
]

SWAPS = [SWAP_RIGHT, SWAP_LEFT, SWAP_EDGE]


def get_size():
    s = os.get_terminal_size()
    return s.lines, s.columns


def center_text(size: SIZE_TYPE, text: str, add_right=True):
    y, x = size
    de_colored_text = Color.de_color(text)
    space_l = " " * (x // 2 - len(de_colored_text) // 2)
    space_r = " " * (x - len(space_l) - len(de_colored_text))
    return space_l + text + (space_r if add_right else '')


def slow_print(string: str, delay: float = 0.025):
    y, x = get_size()
    r = ''
    if args("-f", "--fast"):
        print(string, end='', flush=True)
        return

    for s in string:
        r += s
        if len(r) == x-1:
            print('\r' + r, end='', flush=True)
            r = ""
            time.sleep(delay)
            print(flush=True)
        elif s == "\n":
            print(flush=True)
            r = ""
        else:
            print('\r' + r, end='', flush=True)
            if s != ' ':
                time.sleep(delay)


def if_yes(answer: str):
    return answer.lower() in ("", "да", "д", "y", "yes")
