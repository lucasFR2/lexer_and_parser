import sys
from lexer import lexer

#utilizei Python por ser mais prático para regex e parsing (LL1)

#classe Parser = analisador sintático (método LL1)

class Parser:
    def __init__(self, tokens): #recebe a lista de tokens do analisador léxico
        self.tokens = tokens
        self.pos = 0

    def current(self):#pega o token atual
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]#tipo, valor
        return ("EOF", "EOF")

    def eat(self, expected_type):#consumindo o token atual caso for do tipo esperado
        token_type, tok_value = self.current()
        if token_type == expected_type:#se for do tipo esperado, consome o token
            self.pos += 1
        else:
            raise SyntaxError(f"Erro sintático: esperado {expected_type}, mas encontrado {token_type} ({tok_value})")

 
    #gramatica simplificada MiniJava
    def parse(self):
        self.program()
        if self.current()[0] != "EOF":
            raise SyntaxError("Erro sintático: tokens restantes após fim do programa")
        print("O programa é válido sintaticamente!")

    def program(self):
        # int main() { ... }
        self.eat("INT")
        self.eat("MAIN")
        self.eat("LPARENTESE")
        self.eat("RPARENTESE")
        self.eat("LCHAVE")
        while self.current()[0] in ["INT", "FLOAT", "CHAR", "BOOLEAN", "ID"]:
            self.statement()
        self.eat("RCHAVE")

    def statement(self):
        token_type, _ = self.current()
        if token_type in ["INT", "FLOAT", "CHAR", "BOOLEAN"]:
            self.declaration()
        elif token_type == "ID":
            self.assignment()
        else:
            raise SyntaxError(f"Erro sintático: declaração ou atribuição esperada, mas encontrado {token_type}")

    def declaration(self):
        # tipo ID ;
        self.eat(self.current()[0])  #pega o tipo
        self.eat("ID")
        self.eat("PONTOVIRGULA")

    def assignment(self):
        # ID = expressão ;
        self.eat("ID")
        self.eat("ATRIB")
        self.expression()
        self.eat("PONTOVIRGULA")

    def expression(self):
        # expressão simples: NUM_INT | NUM_DEC | ID | STR
        token_type, _ = self.current()
        if token_type in ["NUM_INT", "NUM_DEC", "ID", "STR"]:#se o token for um desses tipos, consome
            self.eat(token_type)#consome o token atual
        else:
            raise SyntaxError(f"Erro sintático: expressão inválida ({token_type})")#se não for um desses tipos, erro


#executar via terminal
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Use no terminal: python parser.py arquivo.minijava")
        sys.exit(1)

    with open(sys.argv[1], "r", encoding="utf-8") as f:
        code = f.read()

    tokens = lexer(code)
    parser = Parser(tokens)
    try:
        parser.parse()
    except SyntaxError as e:
        print(e)
