import re
import os
from rules import rules
import datetime as time

input_file = input("Input file to check : ")

file_path = './' + input_file
file = open(file_path, 'r')
text = file.read()
import os.path
import grammar as convert


class Node:
    def __init__(self, symbol, child1, child2=None):
        self.symbol = symbol
        self.child1 = child1
        self.child2 = child2

    def __repr__(self):
        return self.symbol


class Parser:
    def __init__(self, grammar, sentence):
        self.parse_table = None
        self.prods = {}
        self.grammar = None
        self.input = None
        self.sentence = sentence
        if os.path.isfile(grammar):
            self.grammar_from_file(grammar)
        else:
            self.grammar_from_string(grammar)
        self.__call__(sentence)

    def __call__(self, sentence, parse=False):
        if os.path.isfile(sentence):
            with open(sentence) as inp:
                self.input = inp.readline().split()
                if parse:
                    self.parse()
        else:
            self.input = sentence.split()
            self.sentence = sentence

    def __del__(self):
        print("Closing parser...")

    def grammar_from_file(self, grammar):
        self.grammar = convert.convert_grammar(convert.read_grammar(grammar))

    def grammar_from_string(self, grammar):
        self.grammar = convert.convert_grammar([x.replace("->", "").split() for x in grammar.split("\n")])

    def parse(self):
        length = len(self.input)
        self.parse_table = [[[] for x in range(length - y)] for y in range(length)]

        for i, word in enumerate(self.input):
            for rule in self.grammar:
                if f"'{word}'" == rule[1]:
                    self.parse_table[0][i].append(Node(rule[0], word))
        for words_to_consider in range(2, length + 1):
            for starting_cell in range(0, length - words_to_consider + 1):
                for left_size in range(1, words_to_consider):
                    right_size = words_to_consider - left_size
                    left_cell = []
                    right_cell = []
                    left_cell = self.parse_table[left_size - 1][starting_cell]
                    right_cell = self.parse_table[right_size - 1][starting_cell + left_size]
                    # print(len(left_cell))
                    for rule in self.grammar:
                        left_nodes = [n for n in left_cell if n.symbol == rule[1]]
                        if left_nodes:
                            right_nodes = [n for n in right_cell if n.symbol == rule[2]]
                            self.parse_table[words_to_consider - 1][starting_cell].extend(
                                [Node(rule[0], left, right) for left in left_nodes for right in right_nodes]
                            )

    def print_tree(self, output=True):
        start_symbol = self.grammar[0][0]
        final_nodes = [n for n in self.parse_table[-1][0] if n.symbol == start_symbol]
        if final_nodes:
            if output:
                return True
        else:
            
            print("The given sentence is not contained in the language produced by the given grammar!")
            print(self.sentence)
            return False

class Token(object):
    def __init__(self, type, val, pos):
        self.type = type
        self.val = val
        self.pos = pos

    def __str__(self):
        return '%s(%s) at %s' % (self.type, self.val, self.pos)


class ERROR(Exception):
    def __init__(self, pos):
        self.pos = pos


class Lexer(object):
    def __init__(self, rules, skip_whitespace=True):
        idx = 1
        regex_parts = []
        self.group_type = {}

        for regex, type in rules:
            groupname = 'GROUP%s' % idx
            regex_parts.append('(?P<%s>%s)' % (groupname, regex))
            self.group_type[groupname] = type
            idx += 1

        self.regex = re.compile('|'.join(regex_parts))
        self.skip_whitespace = skip_whitespace
        self.re_ws_skip = re.compile('\S')

    def input(self, buf):
        self.buf = buf
        self.pos = 0

    def token(self):
        if self.pos >= len(self.buf):
            return None
        else:
            if self.skip_whitespace:
                m = self.re_ws_skip.search(self.buf, self.pos)

                if m:
                    self.pos = m.start()
                else:
                    return None

            m = self.regex.match(self.buf, self.pos)
            if m:
                groupname = m.lastgroup
                tok_type = self.group_type[groupname]
                tok = tok_type
                self.pos = m.end()
                if (tok == 'WHITESPACE') :
                    return ''
                return tok
            raise ERROR(self.pos)

    def tokens(self):
        while 1:
            tok = self.token()
            if tok is None: 
                break
            yield tok

CYK = Parser('grammar.txt', " COMMENT ")

def process(sentence) :
    CYK.__call__(sentence)
    CYK.parse()
    return CYK.print_tree()

if __name__ == '__main__':

    lx = Lexer(rules, skip_whitespace=False)
    lx.input(text)
    output = ''

    try:
        for tok in lx.tokens():
            if tok == '' :
                output = output
            else :
                output += tok + ' '
    except ERROR as err:
        print('ERROR at position %s' % err.pos)
    
    string_container = output.split('NEWLINE')
    # print(string_container)
    if_toggle = 0
    multiline_toggle = False
    start_time = time.datetime.now()
    total_string = len(string_container)
    total_success = 0
    total_error = 0
    line_counter = 0
    print("Parsing {} line(s) of code...".format(total_string))
    for text in string_container :
        line_counter += 1
        if (text == ' ' or text == ''):
            print("",end='')
            total_success += 1
        elif multiline_toggle == False :
                if process(text) :
                    total_success += 1
                else :
                    print("Error at line {}.".format(line_counter))
                    total_error += 1
    
    if (total_error == 0) :
        print("ACCEPTED")
    else :
        print("{} Error(s) detected on the file.".format(total_error))
