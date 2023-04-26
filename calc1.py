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
        self.pos = 0
        self.current_token = None

    def error(self):
        raise Exception("Error parsing input")
    
    def get_next_token(self):
        text = self.text

        if self.pos > len(self.text)-1:
            return Token(EOF, None)
        
        current_char = text[self.pos]
        if current_char.isdigit():
            token = Token(INTEGER, int(current_char))
            self.pos += 1
            return token
        
        if current_char == "+":
            token = Token(PLUS, "+")
            self.pos += 1
            return token
        
        if current_char == "-":
            token = Token(MINUS, "-")
            self.pos += 1
            return token

        self.error()

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