# Michael Mansfield

import LexicalAnalyzer

# Function definitions for recursive descent parsing
# Contains several 'return 1's to prevent accidental
# operations on 'NoneType' in case of error


# Begin recursive descent expression parsing
def parse_expr():
    global exprTuples
    global error
    if not error:
        term = parse_term()
        while True:
            if exprTuples and exprTuples[0][1] is 'PLUS':
                exprTuples = exprTuples[1:]
                term += parse_term()
            elif exprTuples and exprTuples[0][1] is 'MINUS':
                exprTuples = exprTuples[1:]
                term -= parse_term()
            else:
                return term
    else:
        return 1


# Recurse to term parsing
def parse_term():
    global exprTuples
    global error
    if not error:
        factor = parse_factor()
        while True:
            if exprTuples and exprTuples[0][1] is 'STAR':
                exprTuples = exprTuples[1:]
                factor *= parse_factor()
            elif exprTuples and exprTuples[0][1] is 'SLASH':
                exprTuples = exprTuples[1:]
                factor /= parse_factor()
            else:
                return factor
    else:
        return 1


# Recurse to factor parsing
def parse_factor():
    global exprTuples
    global error
    if not error:
        if exprTuples and exprTuples[0][1] is 'MINUS':
            exprTuples = exprTuples[1:]
            sign = -1
        else:
            sign = 1
        if exprTuples and exprTuples[0][1] is 'NUMBER':
            num = parse_number()
            if exprTuples and exprTuples[0][1] is 'CARRET':
                exprTuples = exprTuples[1:]
                exp = parse_factor()
            else:
                exp = 1
            return sign * (num ** exp)
        elif exprTuples and exprTuples[0][1] is 'LPAR':
            exprTuples = exprTuples[1:]
            expr = parse_expr()
            if exprTuples and exprTuples[0][1] is 'RPAR':
                exprTuples = exprTuples[1:]
                if exprTuples and exprTuples[0][1] is 'CARRET':
                    exprTuples = exprTuples[1:]
                    exp = parse_factor()
                else:
                    exp = 1
                return sign * (expr ** exp)
            else:
                error = True
                return 1
        else:
            error = True
            return 1
    error = True
    return 1


# Recurse to number parsing
def parse_number():
    global exprTuples
    global error
    if not error:
        num = int(exprTuples[0][0])
        exprTuples = exprTuples[1:]
        while exprTuples and exprTuples[0][1] is 'NUMBER':
            num *= 10
            num += int(exprTuples[0][0])
            exprTuples = exprTuples[1:]
        return num


# The main operation
expression = input()
while expression is not '':
    la = LexicalAnalyzer.LexicalAnalyzer(expression)
    exprTuples = []
    error = False
    while la.nextToken_ != 'EOF':
        exprTuples.append((la.nextLexeme_, la.nextToken_))
        la.lex()
    for (lexeme, token) in exprTuples:
        if token is 'UNKNOWN':
            print('Lexical error!')
            error = True
            break
    if not error:
        result = parse_expr()
        if not error:
            print(result)
        else:
            print('Syntactic error!')
    expression = input()