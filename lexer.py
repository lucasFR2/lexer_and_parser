import re
import sys

#utilizei Python por ser mais prático para regex e parsing (LL1)

#definição dos padrões (Tabela 1) de tokens
token_specification = [
    ("NUM_DEC",   r'\d+\.\d+'),
    ("NUM_INT",   r'\d+'),
    ("STR",       r'"[^"\n]*"'),
    ("SCANF",     r'\bscanf\b'),
    ("PRINTLN",   r'\bprintln\b'),
    ("MAIN",      r'\bmain\b'),
    ("INT",       r'\bint\b'),
    ("FLOAT",     r'\bfloat\b'),
    ("CHAR",      r'\bchar\b'),
    ("BOOLEAN",   r'\bboolean\b'),
    ("VOID",      r'\bvoid\b'),
    ("IF",        r'\bif\b'),
    ("ELSE",      r'\belse\b'),
    ("FOR",       r'\bfor\b'),
    ("WHILE",     r'\bwhile\b'),
    ("RETURN",    r'\breturn\b'),
    ("ID",        r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ("COMENT",   r'//.*'),
    ("COMP",      r'==|!=|>=|<=|>|<'), #operadores relacionais
    ("ATRIB",    r'='),
    ("ADIÇAO",      r'\+'),
    ("SUBSTRA",     r'-'),
    ("MULT",      r'\*'),
    ("DIV",       r'/'),
    ("MOD",       r'%'),
    ("AND",       r'&&'),
    ("OU",        r'\|\|'),
    ("NOT",       r'!'),#!
    ("LPARENTESE",    r'\('),#(
    ("RPARENTESE",    r'\)'),#)
    ("LCOLCHETE",    r'\['), #[
    ("RCOLCHETE",    r'\]'),#]
    ("LCHAVE",    r'\{'), #{
    ("RCHAVE",    r'\}'), #}
    ("VIRGULA",     r','), #,
    ("PONTOVIRGULA",      r';'), #;
    ("SKIP",      r'[ \t\n]+'),   #espaços e quebras de linha
    ("INESPERADO",  r'.'),          #qualquer coisa inesperada
]

tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification) #combina todos os padrões em uma única expressão regular

#função principal do analisador léxico
def lexer(code):
    tokens = []
    for mo in re.finditer(tok_regex, code):#procura por todos os padrões na string de código
        kind = mo.lastgroup
        value = mo.group()

        if kind == "SKIP" or kind == "COMMENT": #ignorar espaços e comentários
            continue
        elif kind == "MISMATCH": #se for uma coisa inesperada
            raise RuntimeError(f"Token inválido: {value}")
        else:
            tokens.append((kind, value))
    return tokens

#executar via terminal
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Use no terminal: python lexer.py arquivo.minijava")
        sys.exit(1)

    with open(sys.argv[1], "r", encoding="utf-8") as f:
        code = f.read()

    tokens = lexer(code)
    for t in tokens:
        print(f"({t[0]}, \"{t[1]}\")")
