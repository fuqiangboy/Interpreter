INTEGER, MUL, DIV, EOF = "INTEGER", "MUL", "DIV", "EOF"

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self) -> str:
        return "Token({type}, {value})".format(type=self.type, value=repr(self.value))
    
    def __repr__(self) -> str:
        return self.__str__()

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]
    
    def error(self):
        raise Exception("Invalid character")
    
    def advance(self):
        """移动pos,更新current_char
        """
        self.pos += 1
        if self.pos > len(self.text)-1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]
    
    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        result = ""
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)
    
    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                token = Token(INTEGER, self.integer())
                return token
            
            if self.current_char == "*":
                self.advance()
                return Token(MUL, "*")
            
            if self.current_char == "/":
                self.advance()
                return Token(DIV, "/")

            self.error()
        return Token(EOF, None)

class Interpreter:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception("Invalid syntax")    

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()
    
    def factor(self):
        """判断token的类型是否满足句法,返回token的值
        tips:先用一个变量保存上一个token
        """
        token = self.current_token
        self.eat(INTEGER)
        return token.value

    def expr(self):
        result = self.factor()

        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            if token.type is MUL:
                self.eat(MUL)
                result = result * self.factor()
            elif token.type is DIV:
                self.eat(DIV)
                result = result / self.factor()

        return result

def main():
    while True:
        try:
            text = input("calc>")
        except EOFError:
            break
        if not text:
            continue
        lexer = Lexer(text)
        interpreter = Interpreter(lexer)
        result = interpreter.expr()
        print(result)

if __name__ == "__main__":
    main()