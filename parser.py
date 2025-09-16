import sys
from lexer import lexer

#utilizei Python por ser mais prático para regex e parsing (LL = descendente preditivo recursivo, recursividade a esquerda)
#parsing = análise sintática (sintaxe)
#classe Parser = analisador sintático (método LL)

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
            self.pos += 1#avança para o próximo token
        else:
            raise SyntaxError(f"Erro sintático: esperado {expected_type}, mas encontrado {token_type} ({tok_value})")#se não for do tipo esperado, erro

 
    #gramatica simplificada MiniJava
    def parse(self): #inicia a análise sintática
        self.program()
        if self.current()[0] != "EOF": #EOF = fim do arquivo (end of file), indicando que chegou ao fim do código
            raise SyntaxError("Erro sintático: tokens restantes após fim do programa") #se não chegou ao fim do arquivo, erro
        print("O programa é válido sintaticamente! \n\nTokens: \n")
        for t in tokens:
            print(f"({t[0]}, \"{t[1]}\")")

    def program(self): #estrutura básica do programa
        # int main() { ... }
        self.eat("INT")
        self.eat("MAIN")
        self.eat("LPARENTESE")
        self.eat("RPARENTESE")
        self.eat("LCHAVE")
        while self.current()[0] in ["INT", "FLOAT", "CHAR", "BOOLEAN", "ID"]:
            self.statement()
        self.eat("RCHAVE")

    def statement(self):#declaração ou atribuição
        token_type, _ = self.current()
        if token_type in ["INT", "FLOAT", "CHAR", "BOOLEAN"]:
            self.declaration()
        elif token_type == "ID":
            self.assignment()
        else:
            raise SyntaxError(f"Erro sintático: declaração ou atribuição esperada, mas encontrado {token_type}")

    def declaration(self):#declaração de variável
        # tipo ID ;
        self.eat(self.current()[0])  #pega o tipo
        self.eat("ID")#consome o ID, que é o nome da variável
        self.eat("PONTOVIRGULA")# PONTOVIRGULA = ;

    def assignment(self):#atribuição de variável
        # ID = expressão ;
        self.eat("ID") #consome o ID, que é o nome da variável
        self.eat("ATRIB")# ATRIB = =
        self.expression()#chama a função expressão para validar o valor atribuído
        self.eat("PONTOVIRGULA")# PONTOVIRGULA = ;

    def expression(self):
        # expressão simples para definir o tipo: NUM_INT | NUM_DEC | ID | STR
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

    with open(sys.argv[1], "r", encoding="utf-8") as f: #abre o arquivo de teste minijava
        code = f.read()#lê o conteúdo do arquivo

    tokens = lexer(code)#chama o analisador léxico para obter a lista de tokens
    parser = Parser(tokens)#cria o analisador sintático com a lista de tokens
    try:
        parser.parse() #inicia a análise sintática
    except SyntaxError as e:
        print(e)
