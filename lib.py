import json
import platform
from sys import argv
import sys
import time
from color_class import Color
import os


SIZE_TYPE = (int, int)
WINDOWS = "Windows"
system = platform.system()


def clear():
    os.system("cls" if system == WINDOWS else r'printf "\033c"')


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def args(*flags: str):
    arg = argv[1:]
    if any(i in arg for i in flags):
        return True
    for f in flags:
        if len(f) == 2 and f[0] == '-':
            return f[1] in ''.join(filter(lambda x: len(x) >= 2 and x[0] == '-' and x[1:].isalpha(), arg))
    return False


class Settings:
    ANIMATION = "animation"
    DIFFICULT = "difficult"
    SIMPLE_SYMBOLS = "simple_symbols"
    COLOR = "color"
    CHECK_SIZE = "check_size"

    LOCALIZED_FUNCS = {
        ANIMATION: "Анимации в разных меню",
        DIFFICULT: "Сложность и скорость игры",
        SIMPLE_SYMBOLS: "Замена Emoji на простые символы",
        COLOR: "Цветной вывод",
        CHECK_SIZE: "Проверять разрешение консоли перед запуском",
    }

    SETTINGS_PATH = resource_path("settings.json")  # type: str
    DATA = json.load(open(SETTINGS_PATH))  # type: dict

    KEYS = ["настройки", "s", "settings", "1"]

    PAGES = [
        """
%s:
        
Текущее состояние: %s
        
    1) Включить
    2) Выключить
        
0) Назад
        
Введите номер комманды (0-2): """,
        """
Сложности:
        
Текущая сложность: %s
Выберите сложность:
%s
        
0) Назад

Введите номер комманды (0-%s): """
    ]

    @classmethod
    def edit_page(cls, size: SIZE_TYPE, val, title):
        if val == cls.DIFFICULT:
            p = cls.PAGES[1] % (
                cls.get_state(cls.DIFFICULT),
                '\n'.join("    %s) %s" % i for i in enumerate(DIFFICULT.LOCALISED_SPEED.values(), 1)),
                len(DIFFICULT.LOCALISED_SPEED) + 1
            )
        elif val in cls.LOCALIZED_FUNCS:
            p = cls.PAGES[0] % (
                cls.LOCALIZED_FUNCS[val],
                cls.get_state(val)
            )
        else:
            return

        clear()
        print('\r%s' % Color(center_text(size, title), 30, 47), end='', flush=True)
        slow_print(p, 0)
        i = input()
        while True:
            if i.isnumeric():
                i = int(i)
                if i == 0:
                    return "back"
                if val == cls.DIFFICULT and i in range(1, 6):
                    cls.set_difficult(list(DIFFICULT.LOCALISED_SPEED.keys())[i - 1])
                elif i in range(1, 3):
                    cls.set_any_bool(val, bool(i - 2))
                else:
                    i = input("Вы ввели данные некорректно! Попробуйте снова: ")
                    continue
                print("Изменения сохранены!", end='', flush=True)
                time.sleep(1.5)
                return
            i = input("Вы ввели данные некорректно! Попробуйте снова: ")

    @classmethod
    def get_param(cls, key: str, *flags: str):
        return args(*flags) or cls.DATA.get(key, False)

    @classmethod
    def get_speed(cls):
        speed = DIFFICULT.get_speed(cls.get_param(cls.DIFFICULT))
        if args("-H", "--super-hard"):
            speed = 0.025
        elif args("-h", "--hard"):
            speed = 0.05
        elif args("-e", "--easy"):
            speed = 0.2
        elif args("-E", "--super-easy"):
            speed = 0.4
        return speed

    @classmethod
    def save_settings(cls):
        json.dump(cls.DATA, open(cls.SETTINGS_PATH, 'w'), indent=2, ensure_ascii=False)

    @classmethod
    def set_difficult(cls, value):
        cls.DATA[cls.DIFFICULT] = value
        cls.save_settings()

    @classmethod
    def get_animation(cls):
        return cls.get_param(cls.ANIMATION, "-f", "--fast")

    @classmethod
    def get_color(cls):
        return cls.get_param(cls.COLOR, "-c", "--no-color")

    @classmethod
    def get_simple(cls):
        return cls.get_param(cls.SIMPLE_SYMBOLS, '-s', '--simple')

    @classmethod
    def get_check_size(cls):
        return cls.get_param(cls.CHECK_SIZE, "-S", "--no-check-size")

    @classmethod
    def set_any_bool(cls, key: str, value: bool):
        cls.DATA[key] = bool(value)
        cls.save_settings()

    @classmethod
    def set_animation(cls, value: bool):
        cls.set_any_bool(cls.ANIMATION, value)

    @classmethod
    def set_color(cls, value: bool):
        cls.set_any_bool(cls.COLOR, value)
        Color.DE_COLOR = not cls.get_color()

    @classmethod
    def set_simple(cls, value: bool):
        cls.set_any_bool(cls.SIMPLE_SYMBOLS, value)
        if cls.get_simple():
            from simple_symbols import *
        else:
            from symbols import *

    @classmethod
    def set_check_size(cls, value: bool):
        cls.set_any_bool(cls.CHECK_SIZE, value)

    @classmethod
    def settings_keys(cls):
        return '"' + ('", "'.join(cls.KEYS[:-1])) + '" или "' + cls.KEYS[-1] + '"'

    @classmethod
    def get_state(cls, value):
        if value == cls.DIFFICULT:
            return DIFFICULT.LOCALISED_SPEED.get(DIFFICULT.get_speed(cls.get_speed())[0])
        return Color("ВКЛЮЧЕНО", Color.GREEN) if cls.DATA.get(value) else Color("ВЫКЛЮЧЕНО", Color.RED)


class DIFFICULT:
    SUPER_HARD = 5
    HARD = 4
    NORMAL = 3
    EASY = 2
    SUPER_EASY = 1

    STR_SUPER_HARD = "super-hard"
    STR_HARD = "hard"
    STR_NORMAL = "normal"
    STR_EASY = "easy"
    STR_SUPER_EASY = "super-easy"

    LOCALISED_SPEED = {
        STR_SUPER_HARD: Color("ОЧЕНЬ СЛОЖНО", Color.RED),
        STR_HARD: Color("Сложно", Color.RED),
        STR_NORMAL: Color("Нормально", Color.YELLOW),
        STR_EASY: Color("Просто", Color.GREEN),
        STR_SUPER_EASY: Color("ОЧЕНЬ ПРОСТО", Color.GREEN),
    }

    SPEED = {
        STR_SUPER_HARD: 0.025,
        SUPER_HARD: 0.025,
        0.025: (STR_SUPER_HARD, SUPER_HARD),

        STR_HARD: 0.05,
        HARD: 0.05,
        0.05: (STR_HARD, HARD),

        STR_NORMAL: 0.1,
        NORMAL: 0.1,
        0.1: (STR_NORMAL, NORMAL),

        STR_EASY: 0.2,
        EASY: 0.2,
        0.2: (STR_EASY, EASY),

        STR_SUPER_EASY: 0.4,
        SUPER_EASY: 0.4,
        0.4: (STR_SUPER_EASY, SUPER_EASY),
    }

    @classmethod
    def get_speed(cls, diff):
        return cls.SPEED.get(diff.lower() if type(diff) is str else diff)


if Settings.get_simple():
    from simple_symbols import *
else:
    from symbols import *

Color.DE_COLOR = not Settings.get_color()

DOC = """Добро пожаловать в "НАПЁРСТКИ")
Правила игры очень просты:
    • Показваются 2 стакана (%s) и звёздочка (%s)
    • После этого звёздочка прячется под стакан, и стаканы меняются местами
    • В итоге, Вам нужно будет "найти" звёздочку под стаканом

Для входа в настройки введите %s

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
    if not Settings.get_animation() or not delay:
        print(string, end='', flush=True)
        return

    for s in string:
        r += s
        if len(r) == x - 1:
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


if system == WINDOWS:
    Settings.set_simple(True)
