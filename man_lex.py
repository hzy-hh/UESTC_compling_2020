keywords = ['auto', 'short', 'int',
            'long', 'float', 'double',
            'char', 'struct', 'union',
            'enum', 'typedef', 'const',
            'unsigned', 'signed', 'extern',
            'register', 'static', 'volatile',
            'void', 'if', 'else', 'switch',
            'for', 'do', 'while', 'goto', 'continue',
            'break', 'default', 'sizeof', 'return']
operators = ['<', '>', '=', '+', '-', '*', '/', '%', '*=', '>=', '<=', '==', '-=', '%=', '++', '--', '!=']
integers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
others = [",", ".", ":", ";", "'", '"', "?", "@", "$", "#", '(', ')', '[', ']', '{','}',"\\", "&"]


class Lexier():
    def __init__(self, in_file, out_file):
        self.in_file = in_file
        self.out_file = out_file
        self.pos = 0
        self.block = None
        self.count_line = 0

    def recognize_id_and_keywords(self):
        token = ''
        token += self.block[self.pos]
        self.pos += 1
        if self.pos == len(self.block):
            with open(self.out_file, 'a') as f:
                f.writelines(['id', '\t', token, '\t', str(self.count_line), '\n'])
        while self.pos < len(self.block):
            if self.block[self.pos] == '_' or self.block[self.pos].isdigit() or self.block[self.pos].isalpha():
                token += self.block[self.pos]
                self.pos += 1
            else:
                break
        if token in keywords:
            with open(self.out_file, 'a') as f:
                f.writelines(['keyword', '\t', token, '\t', str(self.count_line), '\n'])
        else:
            with open(self.out_file, 'a') as f:
                f.writelines(['id', '\t', token, '\t', str(self.count_line), '\n'])
        if self.pos > len(self.block) - 1:
            return 'nextblock_state', self.pos
        else:
            return 'continue_state', self.pos

    def recognize_operators(self):
        token = ''
        token += self.block[self.pos]
        self.pos += 1
        if self.pos == len(self.block):
            with open(self.out_file, 'a') as f:
                f.writelines(["operators", '\t', token, '\t', str(self.count_line), '\n'])
        elif self.pos < len(self.block):
            if self.block[self.pos] == '+' and token == '+' or self.block[self.pos] == '-' and token == '-' or self.block[self.pos] == '=':
                token += self.block[self.pos]
                self.pos += 1
            else:
                pass
        if self.pos > len(self.block) - 1:
            return 'nextblock_state', self.pos
        else:
            return 'continue_state', self.pos

    def recognize_intergers(self):
        num = 0
        while self.pos < len(self.block):
            if self.block[self.pos].isdigit():
                num = num * 10 + int(self.block[self.pos])
                self.pos += 1
                if self.pos == len(self.block):
                    break
            else:
                break
        with open(self.out_file, 'a') as f:
            f.writelines(['integer', '\t', str(num), '\t', str(self.count_line), '\n'])
        if self.pos > len(self.block) - 1:
            return 'nextblock_state', self.pos
        else:
            return 'continue_state', self.pos

    def recognize_others(self):
        with open(self.out_file, 'a') as f:
            f.writelines(["others", '\t', self.block[self.pos], '\t', str(self.count_line), '\n'])
        self.pos += 1
        if self.pos > len(self.block) - 1:
            return 'nextblock_state', self.pos
        else:
            return 'continue_state', self.pos

    def __call__(self, *args, **kwargs):
        with open(self.in_file) as f:
            lines = f.readlines()

        self.count_line = 1
        for line in lines:
            line = line.strip()
            splited_line = line.split()
            for block in splited_line:
                self.block = block
                self.pos = 0
                state = 'continue_state'
                while state == 'continue_state':
                    if self.block[self.pos] == '_' or self.block[self.pos].isalpha():
                        state, self.pos = self.recognize_id_and_keywords()
                        if state == 'nextblock_state':
                            break
                    elif self.block[self.pos] in operators:
                        state, self.pos = self.recognize_operators()
                        if state == 'nextblock_state':
                            break
                    elif self.block[self.pos].isdigit():
                        state, self.pos = self.recognize_intergers()
                        if state == 'nextblock_state':
                            break
                    elif self.block[self.pos] in others:
                        state, self.pos = self.recognize_others()
                        if state == 'nextblock_state':
                            break
                    else:
                        print("lexical error in line:" + str(self.count_line))
                        state = 'nextblock_state'
            self.count_line += 1

if __name__ =="__main__":
    in_file = "/Users/hzy/PycharmProjects/Compile/rubik.txt"
    out_file = "out.txt"
    myLexier = Lexier(in_file, out_file)
    myLexier()





