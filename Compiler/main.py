##################### BOILERPLATE BEGINS ############################

# Token types enumeration
##################### YOU CAN CHANGE THE ENUMERATION IF YOU WANT #######################
class TokenType:
    IDENTIFIER = "IDENTIFIER"
    KEYWORD = "KEYWORD"
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    SYMBOL = "SYMBOL"

# Token hierarchy dictionary
token_hierarchy = {
    "if": TokenType.KEYWORD,
    "else": TokenType.KEYWORD,
    "print": TokenType.KEYWORD
}


# helper function to check if it is a valid identifier
def is_valid_identifier(lexeme):
    if not lexeme:
        return False

    # Check if the first character is an underscore or a letter
    if not (lexeme[0].isalpha() or lexeme[0] == '_'):
        return False

    # Check the rest of the characters (can be letters, digits, or underscores)
    for char in lexeme[1:]:
        if not (char.isalnum() or char == '_'):
            return False

    return True


# Tokenizer function
def tokenize(source_code):
    tokens = []
    position = 0

    while position < len(source_code):
        # Helper function to check if a character is alphanumeric
        def is_alphanumeric(char):
            return char.isalpha() or char.isdigit() or (char=='_')

        char = source_code[position]

        # Check for whitespace and skip it
        if char.isspace():
            position += 1
            continue

        # Identifier recognition
        if char.isalpha():
            lexeme = char
            position += 1
            while position < len(source_code) and is_alphanumeric(source_code[position]):
                lexeme += source_code[position]
                position += 1

            if lexeme in token_hierarchy:
                token_type = token_hierarchy[lexeme]
            else:
                # check if it is a valid identifier
                if is_valid_identifier(lexeme):
                    token_type = TokenType.IDENTIFIER
                else:
                    raise ValueError(f"Invalid identifier: {lexeme}")

        # Integer or Float recognition
        elif char.isdigit():
            lexeme = char
            position += 1

            is_float = False
            while position < len(source_code):
                next_char = source_code[position]
                # checking if it is a float, or a full-stop
                if next_char == '.':
                    if (position + 1 < len(source_code)):
                        next_next_char = source_code[position+1]
                        if next_next_char.isdigit():
                            is_float = True

                # checking for illegal identifier
                elif is_alphanumeric(next_char) and not next_char.isdigit():
                    while position < len(source_code) and is_alphanumeric(source_code[position]):
                        lexeme += source_code[position]
                        position += 1
                    if not is_valid_identifier(lexeme):
                        raise ValueError(f"Invalid identifier: {str(lexeme)}\nIdentifier can't start with digits")

                elif not next_char.isdigit():
                    break

                lexeme += next_char
                position += 1

            token_type = TokenType.FLOAT if is_float else TokenType.INTEGER

        # Symbol recognition
        else:
            lexeme = char
            position += 1
            token_type = TokenType.SYMBOL

        tokens.append((token_type, lexeme))

    return tokens

########################## BOILERPLATE ENDS ###########################
dictionary= {
    'S': 0,
    'A': 1,
    'I': 2,
    'T': 3,
    'C': 4,
    'P': 5,
    'Q': 6,
    'E': 7,
    'X': 8,
    'O': 9,
    'Y': 10
}

def CYK(G, w):
    V, R, S = G
    n = len(w)
    r = len(V)

    # Initialize the 3D array B to False
    B = [[[False for _ in range(r)] for _ in range(n)] for _ in range(n)]

    # Fill in B for substrings of length 1
    for i in range(n):
        for k, production in enumerate(R): 
            
            Xj,x = production
            j= dictionary[Xj]

            # print(j,production)

            if x == 'y' and (w[i][1]=='print' or w[i][0]=='INTEGER' or w[i][0]=='FLOAT' or w[i][0]=='IDENTIFIER'):
                # print(i,j,r,n)
                B[i][i][j] = True
            
            elif x == 'r' and (w[i][0]=='INTEGER' or w[i][0]=='FLOAT'):
                B[i][i][j] = True
            
            elif x == w[i][1]:
                B[i][i][j] = True

            # if B[i][i][j]:
            #     print("hello",i,j)
 
    # Calculate B for substrings of length > 1
    for i in range(1, n):        # length of substring
        for Left in range(n - i):   # start of substring
            Right = Left + i
            for M in range(Left +1 , Right + 1):
                for production in R:
                    # print(production)
                    X_1, X_2 = production
                    # check only those X_2 that are not terminals, i.e. they are in V
                    if X_2[0] not in V or X_2[1] not in V:
                        continue
                    X_alpha = dictionary[X_1]
                    X_beta, X_gamma = dictionary[X_2[0]], dictionary[X_2[1]]
                    # print(X_alpha,X_beta,X_gamma)
                    if B[Left][M - 1][X_beta] and B[M][Right][X_gamma]:
                        B[Left][Right][X_alpha] = True

    # Check if the start symbol S can generate the input string
    for i in range(r):
        if B[0][n - 1][i] and i == dictionary['S']:
            return True

    return False

def checkGrammar(tokens):
    # write the code the syntactical analysis in this function
    # You CAN use other helper functions and create your own helper functions if needed
    # reference: https://courses.engr.illinois.edu/cs373/sp2009/lectures/lect_15.pdf + ChatGPT
    variables = ['S','A', 'I','T','C','P','Q','E','X','O','Y']
    production_rules = [('S','IA'),('S','TT'),('S','y'),\
                        ('T','IA'),('T','TT'),('T','y'),\
                        ('I','if'),\
                        ('A','CT'),('A','PT'),\
                        ('P','QE'),\
                        ('Q','CT'),\
                        ('E','else'),\
                        ('C','YX'),('C','y'),('C','r'),\
                        ('X','YX'),('X','y'),('X','r'),\
                        ('Y','XO'),\
                        ('O','+'),('O','-'),('O','*'),('O','/'),('O','^'),('O','>'),('O','<'),('O','=')]  

    G = (variables, production_rules, 'S')
    result = CYK(G, tokens)
    return result
    # pass

def checkSyntax(tokens):
    
    check_error = False
    error_string = ""

    # for the list get the second tuple
    tokens_list = [i[1] for i in tokens]

    # if else's are more than if's
    if tokens_list.count('else') > tokens_list.count('if'):
        # print("reached here")
        check_error = True
        error_string = "Syntax Error: else and if are not equal in number"

    # check if the first else comes before the first if
    if tokens.count('else') != 0 and tokens.count('else') != 0 and tokens.index('else') < tokens.index('if'):
        check_error = True
        error_string = "Syntax Error: else comes before if"

    # Can't start with an operator or an else
    if tokens[0][0] == 'SYMBOL' or tokens[0][1] == 'else':
        check_error = True
        error_string = "Syntax Error: Can't start with an operator or an else"

    # Two operators can't be adjacent to each other
    for i in range(len(tokens)-1):
        if tokens[i][0] == 'SYMBOL' and tokens[i+1][0] == 'SYMBOL':
            check_error = True
            error_string = "Syntax Error: Two symbols can't be adjacent to each other"

    # A statement cannot end with an "else" (or) an operator
    if tokens[-1][0] == 'SYMBOL' or tokens[-1][1] == 'else' or tokens[-1][1] == 'if':
        check_error = True
        error_string = "Syntax Error: A statement cannot end with an else,if or an operator"

    # There must be atleast 2 arguments after if: second last position can also not be if
    if tokens[-2][1] == 'if':
        check_error = True
        error_string = "Syntax Error: There must be atleast 2 arguments after if"

    # Only an if or an operator can come 2 positions before an operator
    for i in range(len(tokens)-1):
        if tokens[i][0]=='SYMBOL' and (i-2)>=0:
            if tokens[i-2][0]!='SYMBOL' and tokens[i-2][1]!='if':
                check_error = True
                error_string = "Syntax Error: Only an if or an operator can come 2 positions before an operator"

    # The minimum distance between an else and an operator must be greater than equal to 2
    for i in range(len(tokens)-1):
        if tokens[i][1] == 'else' and tokens[i+1][0]== 'SYMBOL':
            if i == 0 or tokens[i-1][0] != 'SYMBOL' or tokens[i-1][1] == 'if':
                check_error = True
                error_string = "Syntax Error: The minimum distance between an 'else' and an operator must be >= 2"

    # check the stack order of if and else
    stack = []
    for i in range(len(tokens)):
        if tokens[i][1] == 'if':
            stack.append('if')
        elif tokens[i][1] == 'else':
            if len(stack) == 0:
                check_error = True
                error_string = "Syntax Error: Wrong nesting of if and else"
            else:
                stack.pop()

    return check_error, error_string

# Test the tokenizer
if __name__ == "__main__":
    # source_code = "if 2+xi > 0 print 2.0 else print -1;"
    source_code = "if 1-2 print hi else print else hello if 2-3 print wow"
    tokens = tokenize(source_code)

    check_error, error_string = checkSyntax(tokens)
    logs = checkGrammar(tokens)  # You are tasked with implementing the function checkGrammar
    # print(logs)
    
    if logs:
        for token in tokens:
            print(f"Token Type: {token[0]}, Token Value: {token[1]}")
        
    if check_error:
        print(error_string)
    
        




        
    
        
    
    


