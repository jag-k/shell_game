class Color:
    # ATTRIBUTES
    NORMAL = 0
    THUMBNAIL = 1
    UNDERLINE = 4
    FLASHING = 5
    INVERTED = 7
    INVISIBLE = 8

    # TEXT COLOR
    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    PURPLE = 35
    LIGHT_BLUE = 36
    WHITE = 37

    # BACKGROUND COLOR
    ON_BLACK = 40
    ON_RED = 41
    ON_GREEN = 42
    ON_YELLOW = 43
    ON_BLUE = 44
    ON_PURPLE = 45
    ON_LIGHT_BLUE = 46
    ON_WHITE = 47

    DE_COLOR = False

    def __init__(self, text='', *attributes, to_normal_end=True):

        if not all(map(lambda x: type(x) is int, attributes)):
            raise TypeError("attribute takes only 'int' arguments")
        elif not all(map(lambda x: x in [0, 1, 4, 5, 7, 8]+list(range(30, 38))+list(range(40, 48)), attributes)):
            raise ValueError("the values ​​of 'attribute' are not in the values ​​of the table")
        self.atr = '\x1b['+';'.join(sorted(map(str, attributes)))+'m'
        self.attributes = attributes
        self.text = str(text)
        self.end = bool(to_normal_end)

    def __str__(self):
        if self.DE_COLOR:
            return Color.de_color(self.text)
        return self.atr+self.text+('\x1b[0m' if self.end else '')

    def no_end(self):
        if self.DE_COLOR:
            return Color.de_color(self.text)
        return self.atr+str(self.text)

    def __add__(self, other):
        if type(other) is Color:
            return Color(self.no_end() + other.no_end + self.atr, *self.attributes, to_normal_end=self.end)
        return str(self) + other

    def __radd__(self, other):
        if type(other) is Color:
            return Color(other.no_end + self.no_end(), *self.attributes, to_normal_end=self.end)
        return other + str(self)

    @staticmethod
    def de_color(text: str):
        res = ''
        add = True
        for i in text:
            if i == "\x1b":
                add = False
                continue
            if not add and i == 'm':
                add = True
                continue
            if add:
                res += i
        return res
