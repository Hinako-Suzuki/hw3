# coding:utf-8

def readNumber(line, index):
    number = 0
    flag = 0
    keta = 1
    while index < len(line) and (line[index].isdigit() or line[index] == '.'):
        if line[index] == '.':
            flag = 1
        else:
            number = number * 10 + int(line[index])
            if flag == 1:
                keta *= 0.1
        index += 1
    token = {'type': 'NUMBER', 'number': number * keta}
    return token, index

def readPlus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1

def readMinus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1

def readkakeru(line, index):
    token = {'type': 'kakeru'}
    return token, index + 1

def readwaru(line, index):
    token = {'type': 'waru'}
    return token, index + 1

def readkakko_start(line, index):
    token = {'type': 'kakko_start'}
    return token, index + 1

def readkakko_fin(line, index):
    token = {'type': 'kakko_fin'}
    return token, index + 1

def tokenize(line):
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
            (token, index) = readkakeru(line, index)
        elif line[index] == '/':
            (token, index) = readwaru(line, index)
        elif line[index] == '(':
            (token, index) = readkakko_start(line, index)
        elif line[index] == ')':
            (token, index) = readkakko_fin(line, index)
        else:
            print 'Invalid character found:' + line[index]
            exit(1)
        tokens.append(token)
    return tokens

def evaluate(tokens):
    tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    index = 1
    (answer,index)=culculate(tokens,index)
    return answer

def culculate(tokens,index):
    before=index
    tokens[index-1]['type']='PLUS'
    answer=0
    while (index < len(tokens)) and (tokens[index]['type'] != 'kakko_fin'):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'kakeru':
                tokens[index - 2]['number']*=tokens[index]['number']
                del tokens[index]
                del tokens[index - 1]
                index=index-2
            elif tokens[index - 1]['type'] == 'waru':
                tokens[index - 2]['number']/=tokens[index]['number']
                del tokens[index]
                del tokens[index - 1]
                index=index-2
        elif tokens[index]['type'] == 'kakko_start':
            start=index
            (result,fin)=culculate(tokens,index+1)
            tokens[start]['type']='NUMBER'
            tokens[start]['number']=result
            for num in range(fin,start+1,-1):
                del tokens[num]
        index += 1
    index=before
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'PLUS':
                answer += tokens[index]['number']
            elif tokens[index - 1]['type'] == 'MINUS':
                answer -= tokens[index]['number']
        elif tokens[index]['type'] == 'kakko_fin':
            return answer,index
        index+=1
    return answer,index
    

def test(line, expectedAnswer):
    tokens = tokenize(line)
    actualAnswer = evaluate(tokens)
    if abs(actualAnswer - expectedAnswer) < 1e-8:
        print "PASS! (%s = %f)" % (line, expectedAnswer)
    else:
        print "FAIL! (%s should be %f but was %f)" % (line, expectedAnswer, actualAnswer)
# Add more tests to this function :)
def runTest():
    print "==== Test started! ===="
    test("1+2", 3)
    test("1.0+2.1-3", 0.1)
    test("3.0+4*2-1/5", 10.8)
    #test("(((1*2.0)*3)-(4*5))+((6*7)+(8*9))",100)
    print "==== Test finished! ====\n"
    
while True:
    print '> ',
    line = raw_input()
    tokens = tokenize(line)
    answer = evaluate(tokens)
    print ("answer = %f\n" % answer)