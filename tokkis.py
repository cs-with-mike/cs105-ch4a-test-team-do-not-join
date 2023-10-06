import re, sys, enum


class CharClass(enum.Enum):
    EOF = -1
    LETTER = 0
    DIGIT = 1
    UNKNOWN = 99


class Token(enum.Enum):
    EOF = -1
    INT_LIT = "INT_LIT"
    IDENT = 11
    ASSIGN_OP = 20
    ADD_OP = 21
    SUB_OP = 22
    MULT_OP = 23
    DIV_OP = 24
    LEFT_PAREN = 25
    RIGHT_PAREN = 26

    def __str__(self):
        return super().__str__()[len("Token."):]


class Tokki:
    def __init__(self, sentence: iter):
        self.sentence = sentence
        self.char_class = CharClass.EOF
        self.lexeme = [''] * 100
        self.prev_char = ''
        self.next_char = ''
        self.lex_len = 0
        self.token = Token.EOF
        self.next_token = Token.EOF
        self.depth = 0

    def get_char(self):
        self.prev_char = self.next_char
        self.next_char = next(self.sentence, '')
        if self.next_char:
            if self.next_char.isalpha():
                self.char_class = CharClass.LETTER
            elif self.next_char.isdigit():
                self.char_class = CharClass.DIGIT
            else:
                self.char_class = CharClass.UNKNOWN
        else:
            self.char_class = CharClass.EOF

    def add_char(self):
        if self.lex_len <= 98:
            self.lexeme[self.lex_len] = self.next_char
            self.lex_len += 1
            self.lexeme[self.lex_len] = ''
        else:
            print("ERROR - lexeme is too long.", end="\n\n")
            exit()


def main():
    file_path = "(no file path)"
    try:
        file_path = sys.argv[1]
        with open(file_path, 'r') as file:
            sentence = iter(re.sub(r"\s", "", file.read()))

        t = Tokki(sentence)
        t.get_char()
        lex(t)
        expr(t)
        while t.next_token != Token.EOF:
            # lex(t)
            expr(t)
    except IndexError as e:
        print("ERROR - no tokki source file given.\n\n ",
              "Usage: ./tokki.sh path/to/tokki/source/file.tk",
              end="\n\n")
    except FileNotFoundError as e:
        print("ERROR - cannot open file: {}\n"
              .format(file_path), e, end="\n\n")


def lex(t: Tokki):
    t.lex_len = 0
    if t.char_class == CharClass.LETTER:
        t.add_char()
        t.get_char()
        while t.char_class in (CharClass.LETTER, CharClass.DIGIT):
            t.add_char()
            t.get_char()
        t.next_token = Token.IDENT
    elif t.char_class == CharClass.DIGIT:
        t.add_char()
        t.get_char()
        while t.char_class == CharClass.DIGIT:
            t.add_char()
            t.get_char()
        t.next_token = Token.INT_LIT
    elif t.char_class == CharClass.UNKNOWN:
        lookup(t.next_char, t)
        t.get_char()
    elif t.char_class == CharClass.EOF:
        t.next_token = Token.EOF
        t.lex_len = len("EOF")
        t.lexeme[:t.lex_len] = "EOF"

    print_at_depth(t, "{} [ {} ]".format(
        t.next_token,
        ''.join(t.lexeme[:t.lex_len])
    ), entering=False, alt_symbol='=')


def lookup(ch: str, t: Tokki):
    if ch == '(':
        t.add_char()
        t.next_token = Token.LEFT_PAREN
    elif ch == ')':
        t.add_char()
        t.next_token = Token.RIGHT_PAREN
    elif ch == '+':
        t.add_char()
        t.next_token = Token.ADD_OP
    elif ch == '-':
        t.add_char()
        t.next_token = Token.SUB_OP
    elif ch == '*':
        t.add_char()
        t.next_token = Token.MULT_OP
    elif ch == '/':
        t.add_char()
        t.next_token = Token.DIV_OP
    else:
        t.add_char()
        t.next_token = Token.EOF


def expr(t: Tokki):
    print_at_depth(t, "expr", alter_depth=1)

    term(t)
    while t.next_token == Token.ADD_OP or t.next_token == Token.SUB_OP:
        lex(t)
        term(t)

    print_at_depth(t, "expr", entering=False, alter_depth=-1)


def term(t: Tokki):
    print_at_depth(t, "term", alter_depth=1)

    factor(t)
    while t.next_token == Token.MULT_OP or t.next_token == Token.DIV_OP:
        lex(t)
        factor(t)

    print_at_depth(t, "term", entering=False, alter_depth=-1)


def factor(t: Tokki):
    print_at_depth(t, "factor", alter_depth=1)

    if t.next_token == Token.IDENT or t.next_token == Token.INT_LIT:
        lex(t)
    else:
        if t.next_token == Token.LEFT_PAREN:
            lex(t)
            expr(t)
            if t.next_token == Token.RIGHT_PAREN:
                lex(t)
            else:
                error(t)
        else:
            error(t)

    print_at_depth(t, "factor", entering=False, alter_depth=-1)


def error(t: Tokki):
    print("Error - invalid tokki syntax at: {}".format(t.prev_char))
    exit(0)


def print_at_depth(t: Tokki, msg: str, entering=True, alter_depth=0, alt_symbol=None):
    if alter_depth >= 1:
        t.depth += alter_depth

    print("{} {}".format(
        (alt_symbol if alt_symbol else '>' if entering else '<') * t.depth,
        msg
    ))

    if alter_depth < 0:
        t.depth += alter_depth


if __name__ == "__main__":
    main()