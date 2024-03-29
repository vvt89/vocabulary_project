import random
import re
import sqlite3


def add_new_word(database_file, word):

    # Receives name of database file, and word that should be added to vocabulary
    # Returns :
    #   1 Is word correct (T/F)
    #   2 Is word already exists in vocabulary (T/F)
    #   3 List of rows contained in database
    #   4 The last id
    #   5 The word id if word already exists or the last number if not

    conn = sqlite3.connect(database_file)
    cur = conn.cursor()

    wordiscorrect = False
    words_match = True
    word_number = None
    list_of_rows = []
    last_number = 0

    word = word.strip()  # Delete spaces on both sides
    word = word.lower()
    match = []
    match0 = (re.match("^[ '\-abcdefghijklmnopqrstuvwxyz]*$", word))  # Check if string consists only letters
    match.append(re.search("^'\S", word))  # Check if word starts from '
    match.append(re.search("^\S+'$", word))  # Check if word ends by '
    match.append(re.search("^\S+'+'", word))  # Check if word consists ''
    match.append(re.search("^-\S", word))  # Check if word starts from -
    match.append(re.search("^\S+-$", word))  # Check if word ends by -
    match.append(re.search("^\S+-+-", word))  # Check if word consists --
    match_flag = False
    # print(match0, match)
    if match0 is None:
        match_flag = True
    for m in match:
        if m is not None:
            match_flag = True
    if match_flag is False:
        words = word.split()  # Delete redundant spaces
        new_word = ""
        for w in words:
            if len(w)>0:
                new_word += w
                new_word += " "
        new_word = new_word.strip()  # Delete spaces on both sides
        wordiscorrect = True
    else:
        wordiscorrect = False
        #print("Uncorrect word")

    if len(word) == 0:
        wordiscorrect = False

    # Check the length of a word. The longest known word is pseudopseudohypoparathyroidism, which contains 30 letters.
    if len(word) > 30:
        wordiscorrect = False

    if wordiscorrect:
        cur.execute('SELECT * FROM Words')
        counter = 0

        words_match = False
        for row in cur:  # How large is our vocabulary?
            counter += 1
            last_number = row[0]  # It is used for next id calculation
            #print(row)
            if new_word == row[1]:
                words_match = True
                word_number = last_number
        #print("length of the base: ", counter)

        if words_match is False:  # Add new word
            params = (last_number+1, new_word)
            word_number = last_number+1
            cur.execute('INSERT INTO Words (id, word) VALUES(?,?)', params)
            conn.commit()
        else:
            pass
            #print("this word is already exists in vocabulary")

        cur.execute('SELECT * FROM Words')
        list_of_rows = cur.fetchall()

    cur.close()
    return wordiscorrect, words_match, list_of_rows, last_number+1, word_number


def add_translation(database_file, trans_database_file, word, translation):
    wordiscorrect = False
    res = add_new_word(database_file, word)
    if res[0] is True:
        wordiscorrect = True
        if (res[4] is not None) and (len(translation) > 0):
            #trans_database_file = 'translations_' + database_file
            conn = sqlite3.connect(trans_database_file)
            try:
                cur = conn.cursor()
                params = (res[4], translation)
                cur.execute('INSERT INTO Translations (id, word) VALUES(?,?)', params)
                conn.commit()
            except:
                cur = conn.cursor()
                cur.execute('CREATE TABLE Translations (id INTEGER, word TEXT)')
                print('Database of translations has been created')
                params = (res[4], translation)
                cur.execute('INSERT INTO Translations (id, word) VALUES(?,?)', params)
                conn.commit()
            cur.execute('SELECT * FROM Translations')
            list_of_rows = cur.fetchall()
            #for string in list_of_rows:
            #    print(string)
            cur.close()
    return wordiscorrect


def delete_word(database_file, input_word):
    conn = sqlite3.connect(database_file)
    cur = conn.cursor()
    cur.execute('DELETE FROM Words WHERE word = "' + input_word + '"')
    conn.commit()
    cur.execute('SELECT * FROM Words')
    list_of_rows = cur.fetchall()
    cur.close()
    return list_of_rows


def delete_id(database_file, index):
    conn = sqlite3.connect(database_file)
    cur = conn.cursor()
    cur.execute('DELETE FROM Words WHERE id = ' + str(index))
    conn.commit()
    cur.execute('SELECT * FROM Words')
    list_of_rows = cur.fetchall()
    cur.close()
    return list_of_rows


def get_random_word(database_file):
    word = None
    conn = sqlite3.connect(database_file)
    cur = conn.cursor()
    cur.execute('SELECT * FROM Words')
    counter = len(cur.fetchall())
    last_number = random.randint(1, counter)
    cur.execute('SELECT * FROM Words')
    counter = 0
    for i in cur:
        counter += 1
        if counter == last_number:
            word = i[1]
    return word


def get_random_word_from_the_last(database_file, first_num):
    word = None
    number = None
    conn = sqlite3.connect(database_file)
    cur = conn.cursor()
    cur.execute('SELECT * FROM Words')
    counter = len(cur.fetchall())
    first_num = min(first_num, counter)
    last_number = random.randint(first_num, counter)
    cur.execute('SELECT * FROM Words')
    counter = 0
    for i in cur:
        counter += 1
        if counter == last_number:
            word = i[1]
            number = i[0]
    return word, number


def get_translation_by_number(trans_file_name, number):
    translations_list = []
    conn = sqlite3.connect(trans_file_name)
    try:
        cur = conn.cursor()
        cur.execute('SELECT * FROM Translations WHERE id = ?', (number,))
        list_of_rows = cur.fetchall()
        for string in list_of_rows:
            translations_list.append(string[1])
        cur.close()
    except:
        pass
    return translations_list


def return_database_as_list(database_file, trans_file_name, number):

    def make_filter(word_id):
        def find_translations(data):
            if data[0] == word_id:
                return True
            else:
                return False
        return find_translations

    conn = sqlite3.connect(database_file)
    cur = conn.cursor()
    cur.execute('SELECT * FROM Words')
    long_word_list = cur.fetchall()
    cur.close()
    required_word_list = long_word_list[max(0, len(long_word_list) - number):]
    required_word_list.reverse()
    print(required_word_list)

    conn = sqlite3.connect(trans_file_name)
    cur = conn.cursor()
    cur.execute('SELECT * FROM Translations')
    long_translations_list = cur.fetchall()
    cur.close()
    print(long_translations_list)

    words_tranlations_list = []

    for element in required_word_list:
        word_id = element[0]
        find_translations_by_number = make_filter(word_id)
        transl_list = list(filter(find_translations_by_number, long_translations_list))
        transl_string = ''
        for j in transl_list:
            transl_string += j[1]
            transl_string += ', '
        words_tranlations_list.append(element[1] + ' - ' + transl_string)

    #print("Итоговый список")
    #for i in words_tranlations_list:
    #    print(i)

    return 0


# main routine:
if __name__ == "__main__":
    file_name = 'english_vocabulary.sqlite'
    new_word = "forgery"
    '''
    res = add_new_word(file_name, new_word)
    if res[0] is False:
        print("Incorrect word")
    else:
        if res[1] is True:
            print("This word is already exists in vocabulary")
    for row in res[2]:
        print(row)
    print("The last number is: ", res[3])
    random_word = get_random_word_from_the_last(file_name, 1)
    print("random word: ", random_word)
    '''

    trans_file_name = 'translations_english_vocabulary.sqlite'
    add_translation(file_name, trans_file_name, new_word, 'подлог')
    res = get_random_word_from_the_last(file_name, 0)
    res1 = get_translation_by_number(trans_file_name, 411)
    print(res)
    print(res1)


    trans_file_name = 'translations_english_vocabulary.sqlite'
    return_database_as_list(file_name, trans_file_name, 100)

    # delete_word(file_name, "wast")
    # Irregular Verbs located from 1033 to 1277
    # Do not uncomment if database already created:
    # cur.execute('DROP TABLE IF EXISTS Words')
    # cur.execute('CREATE TABLE Words (id INTEGER, word TEXT)')
    # cur.execute('DELETE FROM Words WHERE id = 617')
    # cur.execute('INSERT INTO Words (id, word) VALUES(?,?)', (181, "grandmother"))
    # conn.commit()

    '''
    file_name = 'databases/' + 'Vladimir1989' + '_english_vocabulary.sqlite'
    conn = sqlite3.connect(file_name)
    cur = conn.cursor()
    cur.execute('CREATE TABLE Words (id INTEGER, word TEXT)')
    conn.commit()
    cur.close()
    res = add_new_word(file_name, 'cat')
    '''