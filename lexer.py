import unittest
from rply import LexerGenerator
from rply import Token

class Lexer():
    __lexer_gen = None

    @classmethod
    def get_lexer(cls):
        if cls.__lexer_gen is None:
            gen = LexerGenerator()

            # reserved words
            gen.add('DATA', r'data')
            gen.add('LET', r'let')
            gen.add('IN', r'in')
            gen.add('FOR', r'for')
            gen.add('IF', r'if')
            gen.add('ELSE', r'else')
            gen.add('MATCH', r'match')
            gen.add('FUN', r'fn')

            # reserved symbols
            gen.add('EQUALS', r'\=')
            gen.add('O_BRACE', r'\{')
            gen.add('C_BRACE', r'\}')
            gen.add('O_BRACKET', r'\(')
            gen.add('C_BRACKET', r'\)')
            gen.add('O_SQ_BRACKET', r'\[')
            gen.add('C_SQ_BRACKET', r'\]')
            gen.add('COMMA', r'\,')
            gen.add('COLLON', r'\:')
            gen.add('D_COLLON', r'\:\:')
            gen.add('SEMICOLLON', r'\;')
            gen.add('REV_SLASH', r'\\')
            gen.add('S_ARROW', r'\->')
            gen.add('D_ARROW', r'\=>')
            
            # values
            gen.add('INT', r'-?(\d+(?!\.)|0[xX][\da-fA-F]+|0[bB][01]+|0[0-7]+)')
            gen.add('STRING', r'\"[^"]*\"')
            gen.add('LABEL_NAME', r'\$\w(_|\d|\w)*')
            gen.add('SYMBOLS', r'[^\w\s\d]+')
            gen.add('FLOAT', r'-?\d[_0-9]+\.\d[_0-9]+([eE][+-]?\d{1,3})?')
            gen.add('FUNC_NAME', r'[a-z](_|\d|\w)*')
            gen.add('DATA_NAME', r'[A-Z](_|\d|\w)*')

            # ignore
            gen.ignore('\s+')
            gen.ignore('\-\-\s.*\n')
            gen.ignore('\(-(.|\n)*\-\)')
            cls.__lexer_gen = gen
        
        return cls.__lexer_gen.build()

class TestLexer (unittest.TestCase):
    def setUp(self) -> None:
        self.lexer = Lexer.get_lexer()
        return super().setUp()

    def test_gen_tokens(self):
        tokens = self.lexer.lex('[Foo $x for $x in test(10)]')
        self.assertEqual(tokens.next(), Token('O_SQ_BRACKET', '['))
        self.assertEqual(tokens.next(), Token('DATA_NAME', 'Foo'))
        self.assertEqual(tokens.next(), Token('LABEL_NAME', '$x'))
        self.assertEqual(tokens.next(), Token('FOR', 'for'))
        self.assertEqual(tokens.next(), Token('LABEL_NAME', '$x'))
        self.assertEqual(tokens.next(), Token('IN', 'in'))
        self.assertEqual(tokens.next(), Token('FUNC_NAME', 'test'))
        self.assertEqual(tokens.next(), Token('O_BRACKET', '('))
        self.assertEqual(tokens.next(), Token('INT', '10'))
        self.assertEqual(tokens.next(), Token('C_BRACKET', ')'))
        self.assertEqual(tokens.next(), Token('C_SQ_BRACKET', ']'))

    def test_get_number_tokens(self):
        tokens = self.lexer.lex('3 -3 -1.5 1.5 -1.5e-1 1.5_5e1 0xFF 0d1001 09123')
        self.assertEqual(tokens.next(), Token('INT', '3'))
        self.assertEqual(tokens.next(), Token('INT', '-3'))
        self.assertEqual(tokens.next(), Token('FLOAT', '-1.5'))
        self.assertEqual(tokens.next(), Token('FLOAT', '-1.5e-1'))
        self.assertEqual(tokens.next(), Token('FLOAT', '1.5_5e1'))
        self.assertEqual(tokens.next(), Token('INT', '0xFF'))
        self.assertEqual(tokens.next(), Token('INT', '0d1001'))
        self.assertEqual(tokens.next(), Token('INT', '09123'))


if __name__ == '__main__':
    unittest.main()