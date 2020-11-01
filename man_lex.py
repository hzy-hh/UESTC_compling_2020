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

def recognize_id_and_keywords(block, pos, count_line, f):
    token = ''
    token += block[pos]
    pos += 1
    if pos == len(block):
        f.writelines(['id', '\t', token, '\t', str(count_line), '\n'])
    while pos < len(block):
        if block[pos] == '_' or block[pos].isdigit() or block[pos].isalpha():  # 识别操作符或关键字
            token += block[pos]
            pos += 1
        else:
            break
    if token in keywords:
        f.writelines(['keyword', '\t', token, '\t', str(count_line), '\n'])
    else:
        f.writelines(['id', '\t', token, '\t', str(count_line), '\n'])
    if pos > len(block) - 1:
        return 'nextblock_state', pos
    else:
        return 'continue_state', pos


def recognize_operators(block, pos, count_line, f):
    token = ''
    token += block[pos]
    pos += 1
    if pos == len(block):
        f.writelines(["operators", '\t', token, '\t', str(count_line), '\n'])
    elif pos < len(block):
        if block[pos] == '+' and token == '+' or block[pos] == '-' and token == '-' or block[pos] == '=':
            token += block[pos]
            pos += 1
        else:
            pass
    if pos > len(block) - 1:
        return 'nextblock_state', pos
    else:
        return 'continue_state', pos


def recognize_intergers(block, pos, count_line, f):
    num = 0
    while pos < len(block):
        if block[pos].isdigit():
            num = num * 10 + int(block[pos])
            pos += 1
            if pos == len(block):
                break
        else:
            break
    f.writelines(['integer', '\t', str(num), '\t', str(count_line), '\n'])
    if pos > len(block) - 1:
        return 'nextblock_state', pos
    else:
        return 'continue_state', pos


def recognize_others(block, pos, count_line, f):
    f.writelines(["others", '\t', block[pos], '\t', str(count_line), '\n'])
    pos += 1
    if pos > len(block) - 1:
        return 'nextblock_state', pos
    else:
        return 'continue_state', pos


with open("rubik.txt") as f:
    lines = f.readlines()

with open('out.txt', 'w') as f:  #f = open('out.txt', 'w')
    count_line = 1
    for line in lines:
        line = line.strip()
        splited_line = line.split()
        for block in splited_line:
            pos = 0
            state = 'continue_state'
            while state == 'continue_state':
                if block[pos] == '_' or block[pos].isalpha():
                    state, pos = recognize_id_and_keywords(block, pos, count_line, f)
                    if state == 'nextblock_state':
                        break
                elif block[pos] in operators:
                    state, pos = recognize_operators(block, pos, count_line, f)
                    if state == 'nextblock_state':
                        break
                elif block[pos].isdigit():
                    state, pos = recognize_intergers(block, pos, count_line, f)
                    if state == 'nextblock_state':
                        break
                elif block[pos] in others:
                    state, pos = recognize_others(block, pos, count_line, f)
                    if state == 'nextblock_state':
                        break
                else:
                    print("lexical error in line:" + str(count_line))
                    state = 'nextblock_state'
        count_line += 1


