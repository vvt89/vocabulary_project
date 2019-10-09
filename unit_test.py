import sqlite3
import unittest
from create_database import *

class TestStringMethods(unittest.TestCase):

    def setUp(self):
        pass

    def test_add_new_word(self):
        conn_t = sqlite3.connect('test_database.sqlite')
        cur_t = conn_t.cursor()
        cur_t.execute('DROP TABLE IF EXISTS Words')
        cur_t.execute('CREATE TABLE Words (id INTEGER, word TEXT)')
        res = add_new_word('test_database.sqlite', " caT")
        res = add_new_word('test_database.sqlite', "to  Go ")
        res = add_new_word('test_database.sqlite', " to Go")
        res = add_new_word('test_database.sqlite', "   Self-driving")
        res = add_new_word('test_database.sqlite', "")
        res = add_new_word('test_database.sqlite', "Rock'n'roll")
        res = add_new_word('test_database.sqlite', " ")
        res = add_new_word('test_database.sqlite', "T-Shirt")
        res = add_new_word('test_database.sqlite', "1caT ")
        res = add_new_word('test_database.sqlite', "  Cat1")
        res = add_new_word('test_database.sqlite', "Ca%t ")
        res = add_new_word('test_database.sqlite', "    to    Go  ")
        res = add_new_word('test_database.sqlite', "!at1")
        res = add_new_word('test_database.sqlite', "`a%t~")
        res = add_new_word('test_database.sqlite', "1")
        res = add_new_word('test_database.sqlite', "      ")
        res = add_new_word('test_database.sqlite', "   1  2   ")
        res = add_new_word('test_database.sqlite', "Cat ")
        print(res[0], res[1], res[3])
        for i in res[2]:
            print(i)
        self.assertEqual(res[0], True)
        self.assertEqual(res[1], True)
        self.assertEqual(res[3], 5)
        self.assertEqual(res[2][0][0], 1)
        self.assertEqual(res[2][1][0], 2)
        self.assertEqual(res[2][2][0], 3)
        self.assertEqual(res[2][3][0], 4)
        self.assertEqual(res[2][4][0], 5)
        self.assertEqual(res[2][0][1], 'cat')
        self.assertEqual(res[2][1][1], 'to go')
        self.assertEqual(res[2][2][1], 'self-driving')
        self.assertEqual(res[2][3][1], "rock'n'roll")
        self.assertEqual(res[2][4][1], 't-shirt')
        # Drop the base:
        cur_t.execute('DROP TABLE IF EXISTS Words')

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()