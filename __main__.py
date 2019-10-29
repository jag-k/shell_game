from scense import *

# import threading
# print(os.get_terminal_size())


def main():
    try:
        size = y, x = get_size()
        if x < 39 and not Settings.get_check_size():
            print("Ширина консоли уж слишком мала, сделайте её пошире "
                  "(или поставьте флаг -S или --no-check-size для снятия проверки на размер консоли)",  file=sys.stderr)
            return
        if system == WINDOWS:
            try:
                import colorama
                colorama.init()
            except ImportError:
                print("Установите библиотеку colorama (pip install colorama)", file=sys.stderr)
        while True:
            clear()
            start(size)
            rd = render_doc(size)
            if rd == "back":
                continue
            else:
                clear()
                while game(size):
                    clear()
                return
    except KeyboardInterrupt:
        print("\nДо встречи)")

    except OSError:
        print("Хмм, кажется, здесь нельзя запустить эту игру...", file=sys.stderr)


if __name__ == '__main__':
    main()
