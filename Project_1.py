# ChatGPT was used to generate basic outline of class and function structure
# All code within class and functions is my own work
import regexTokenizer as tk
from more_itertools import peekable


class RegexParser:
    def __init__(self, tokens):
        self.tokens = tokens

    def parse_re(self, level=0):
        self.print_node("RE", level)
        self.parse_simple_re(level + 1)
        while self.peek_token() and self.peek_token().type == 'VERT':
            self.consume_token()
            self.print_node("| VERT", (level + 1))
            self.parse_simple_re(level + 1)

    def parse_simple_re(self, level=0):
        self.print_node("S_RE", level)
        self.parse_basic_re(level + 1)
        while self.peek_token() and self.peek_token().type in {'CHAR', 'LPAREN', 'PERIOD', 'LPOSET', 'LNEGSET', 'BSLASH'}:
            self.parse_basic_re(level + 1)


    def parse_basic_re(self, level=0):
        self.print_node("B_RE", level)
        self.parse_elementary_re(level + 1)
        if self.peek_token() and self.peek_token().type in {'STAR', 'PLUS', 'QMARK'}:
            self.parse_char_or_meta(level)

    def parse_elementary_re(self, level=0):
        self.print_node("E_RE", level)
        if self.peek_token().type == 'LPAREN':
            self.parse_char_or_meta(level)
            self.parse_re(level + 1)
            if self.peek_token().type == 'RPAREN':
                self.parse_char_or_meta(level)
            else:
                raise RuntimeError("')' Right Parenthesis Expected. Recieved: " + self.consume_token().value)
        elif self.peek_token().type == 'PERIOD':
            self.parse_char_or_meta(level + 1)
        elif self.peek_token().type in {'BSLASH','CHAR', 'LANGLE', 'RANGLE'}:
            self.print_node("CHAR_OR_META", level + 1)
            self.parse_char_or_meta(level + 1)
        elif self.peek_token().type == 'LPOSSET':
            self.parse_char_or_meta(level + 1)
            self.parse_set_items(level + 2)
            if self.peek_token().type == 'RSET':
                self.parse_char_or_meta(level)
            else:
                raise RuntimeError("']' Right Square Bracket Expected. Recieved: " + self.consume_token().value)
        elif self.peek_token().type == 'LNEGSET':
            self.parse_char_or_meta(level + 1)
            self.parse_set_items(level + 2)
            if self.peek_token().type == 'RSET':
                self.parse_char_or_meta(level)
            else:
                raise RuntimeError("']' Right Square Bracket Expected. Recieved: " + self.consume_token().value)


    def parse_set_items(self, level=0):
        self.print_node("SITEMS", level)
        if self.peek_token().type != 'RSET':
            self.print_node("CHAR_OR_META", level + 1)
        while self.peek_token() and self.peek_token().type != 'RSET':
            self.parse_char_or_meta(level + 2)

    def parse_char_or_meta(self, level=0):
        char_or_meta = self.consume_token()
        self.print_node(char_or_meta.value + " " + char_or_meta.type, level + 1)
        if char_or_meta.type == 'BSLASH':
            self.parse_char_or_meta(level)


    def peek_token(self):
        return self.tokens.peek(None)

    def consume_token(self):
        return next(self.tokens)

    def print_node(self, content, level):
        print("  " * level + content)


# Sample usage
if __name__ == "__main__":
    sample_inputs = ['two', 't|w|o', '[two]', '[^two]', 't(oo?|wo)', "(\<(/?[^\>]+)\>)"]
    for regex in sample_inputs:
        print(f'\nProcessing expression: "{regex}"')
        tokens = peekable(tk.tokenize(regex))
        parser = RegexParser(tokens)
        parser.parse_re(0)