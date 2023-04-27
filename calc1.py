INTEGER, PLUS, MINUS, EOF = "INTEGER", "PLUS", "MINUS", "EOF"

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self) -> str:
        return "Token({type}, {value})".format(type=self.type, value=repr(self.value))
    
    def __repr__(self) -> str:
        return self.__str__()
    
class Interpreter:
    def __init__(self, text):
        self.text = text
        self.pos = 0 # 指向当前的下一个位置
        self.current_token = None # 当前token
        self.current_char = self.text[self.pos] # 指向当前的下一个字符

    def error(self):
        raise Exception("Error parsing input")
    
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
    
    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            if self.current_char.isdigit():
                token = Token(INTEGER, int(self.current_char))
                self.advance()
                return token
            
            if self.current_char == "+":
                token = Token(PLUS, "+")
                self.advance()
                return token
            
            if self.current_char == "-":
                token = Token(MINUS, "-")
                self.advance()
                return token

            self.error()
        return Token(EOF, None)

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def expr(self):
        self.current_token = self.get_next_token()

        left = self.current_token
        self.eat(INTEGER)

        op = self.current_token
        if op.type == PLUS:
            self.eat(PLUS)
        else:
            self.eat(MINUS)

        right = self.current_token
        self.eat(INTEGER)

        if op.type == PLUS:
            result = left.value + right.value
        else:
            result = left.value - right.value
        return result

def main():
    while True:
        try:
            text = input("calc>")
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)

if __name__ == "__main__":
    main()