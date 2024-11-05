#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Oct 12, 2024
@author: maida (adapted from example found on web)
Scanner modified for regex
"""
#! /usr/local/bin/python3
import collections
import re

# namedtype: entries in tuple can be accessed via names
Token = collections.namedtuple('Token', ['type', 'value', 'line', 'column'])

# Returns an iterable via a generator
def tokenize(code):
    keywords = {'let', 'in', 'minus', 'iszero', 'if', 'then', 'else'}
    token_specification = [
        ('VERT',    r'\|'),
        ('STAR',    r'\*'),
        ('PLUS',    r'\+'),
        ('QMARK',   r'\?'),
        ('LPAREN',  r'[(]'),          # Left parentheses
        ('RPAREN',  r'[)]'),          # Right parentheses
        ('PERIOD',  r'\.'),
        ('BSLASH',  r'\\'),
#        ('FSLASH',  r'/'),
        ('LNEGSET', r'\[\^'),
        ('LPOSSET',  r'\['),           # LPOSET must go after LNEGSET
        ('RSET',   r'\]'),
        ('LANGLE',  r'\<'),
        ('RANGLE',  r'\>'),
        ('CHAR',    r'[A-Za-z0-9_/]'),
#        ('LETTER',  r'[A-Za-z]'),
#        ('DIGIT',   r'[0-9]'),
        ('EOL',     r'\n'),           # Line endings
        ('SKIP',    r'[ \t]+'),       # Skip over spaces and tabs
        ('MISMATCH',r'.'),            # Any other character
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    #print("tok_regex:",tok_regex) # uncomment to see what join did
    line_num = 1
    line_start = 0
    # re.finditer(tok_regex, code) returns list of token matches in code string
    for mo in re.finditer(tok_regex, code): # mo: match object
        kind = mo.lastgroup
        #print("kind:", kind)
        value = mo.group(kind)
        #print("value:", value)
        if kind == 'NEWLINE':
            line_start = mo.end()
            line_num += 1
        elif kind == 'SKIP':
            pass
        elif kind == 'MISMATCH':
            raise RuntimeError('%r unexpected on line %d' % (value, line_num))
        else:
            if kind == 'IDENTIF' and value in keywords:
                kind = value
            column = mo.start() - line_start
            yield Token(kind, value, line_num, column)

regex1 = 'two'

regex2 = 't(oo?|wo)'

regex3 = '(\<(/?[^\>]+)\>)'

if __name__ == "__main__":
    print("\nregex1:")
    for token in tokenize(regex1):
        print(token)
        if token.type == 'IDENTIF':
            print("    ", token.value)
    
    print("\nregex2:")
    for token in tokenize(regex2):
        print(token)
        if token.type == 'IDENTIF':
            print("    ", token.value)

    print("\nregex3:")
    for token in tokenize(regex3):
        print(token)
        if token.type == 'IDENTIF':
            print("    ", token.value)