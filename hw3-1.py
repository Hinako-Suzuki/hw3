# coding:utf-8

def readNumber(line, index):             #数字の処理
    number = 0
    flag = 0     #０→整数、１→小数
    keta = 1
    while index < len(line) and (line[index].isdigit() or line[index] == '.'):
        if line[index] == '.':
            flag = 1
        else:
            number = number * 10 + int(line[index])
            if flag == 1:
                keta *= 0.1
        index += 1                #一つ右にずれる
    token = {'type': 'NUMBER', 'number': number * keta}
    return token, index


def readPlus(line, index):        #足し算
    token = {'type': 'PLUS'}
    return token, index + 1

def readMinus(line, index):       #引き算
    token = {'type': 'MINUS'}
    return token, index + 1

def readMul(line, index):         #掛け算
    token = {'type': 'MUL'}
    return token, index + 1

def readDiv(line, index):         #割り算
    token = {'type': 'DIV'}
    return token, index + 1

def readKakko_hajime(line, index):
    token = {'type': 'Kakko_hajime'}
    return token, index + 1

def readKakko_owari(line, index):
    token = {'type': 'Kakko_owari'}
    return token, index + 1

def tokenize(line):              #字句に分割
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = readNumber(line, index)
        elif line[index] == '+':
            (token, index) = readPlus(line, index)
        elif line[index] == '-':
            (token, index) = readMinus(line, index)
        elif line[index] == '*':
            (token, index) = readMul(line, index)
        elif line[index] == '/':
            (token, index) = readDiv(line, index)
        elif line[index] == '(':
            (token, index) = readKakko_hajime(line, index)
        elif line[index] == ')':
            (token, index) = readKakko_owari(line, index)
        else:
            print 'Invalid character found: ' + line[index]
            exit(1)
        tokens.append(token)
    return tokens

#def evaluate1(tokens):      #字句の並びを計算、()について
#   tokens.insert(0, {'type': 'PLUS'})
#    answer = 0
#    index = 1
#    while index < len(tokens):
#        if tokens[index]['type'] == 'Kakko_hajime':
#           kakko_index = index
#            index += 1
#            if tokens[index]['type'] != 'Kakko_owari':
#                tokens = evaluate2(tokens)
#                answer = evaluate3(tokens)
#            elif tokens[index]['type'] == 'Kakko_owari':
#                index = kakko_index
#                tokens[index]['number'] = answer
#            else:
#                print 'Invalid syntax1'
#   return tokens


def evaluate2(tokens):      #字句の並びを計算、＊と/について
    tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    index = 1
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'MUL':
                tokens[index - 2]['number'] = tokens[index - 2]['number'] * tokens[index]['number']   #*を挟んでる両隣を計算
                del tokens[index]
                del tokens[index - 1]
                index = index - 2                                                                     #＊と後ろの数字を削除して番号は最初の数字にする
            elif tokens[index - 1]['type'] == 'DIV':
                tokens[index - 2]['number'] = tokens[index - 2]['number'] / tokens[index]['number']   #/を挟んでる両隣を計算
                del tokens[index]
                del tokens[index - 1]
                index = index - 2
            elif tokens[index - 1]['type'] == 'PLUS':
                index += 1                                  #+は飛ばす
            elif tokens[index - 1]['type'] == 'MINUS':
                index += 1                                  #-も飛ばす
            else:
                print 'Invalid syntax1'
        index += 1
    return tokens

def evaluate3(tokens):      #字句の並びを計算、＋とーについて
    answer = 0
    tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    index = 1
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'PLUS':
                answer += tokens[index]['number']
            elif tokens[index - 1]['type'] == 'MINUS':
                answer -= tokens[index]['number']
            else:
                print 'Invalid syntax1'
        index += 1
    return answer

def test(line, expectedAnswer):
    tokens = tokenize(line)
    #tokens = evaluate1(tokens)
    tokens = evaluate2(tokens)
    actualAnswer = evaluate3(tokens)
    if abs(actualAnswer - expectedAnswer) < 1e-8:
        print "PASS! (%s = %f)" % (line, expectedAnswer)           #成功
    else:
        print "FAIL! (%s should be %f but was %f)" % (line, expectedAnswer, actualAnswer)     #失敗


# Add more tests to this function :)
def runTest():
    print "==== Test started! ===="
    test("1+2", 3)
    test("1.0+2.1-3", 0.1)
    test("2*3", 6) 
    test("1.0/5.0", 0.2)
    test("4/2-1*5", -3)
    test("2.0*4+1/2.0", 8.5)
    test("3.0*1+4*2-1/5.0", 10.8)
    test("1", 1)
    test("1+2", 3)
    test("1.0+2", 3.0)
    test("1.0+2.0", 3.0)
    test("1*2*3/6.0-4/2.0*2.0+3", 0)
    #test("(3.0+4*(2-1))/5", 1.4)
    print "==== Test finished! ====\n"

runTest()

while True:
    print '> ',
    line = raw_input()              #一行読む
    tokens = tokenize(line)
    #tokens = evaluate1(tokens)
    tokens = evaluate2(tokens)         #字句に区切る 
    answer = evaluate3(tokens)       #字句の並びを計算
    print "answer = %f\n" % answer  #答えを出力