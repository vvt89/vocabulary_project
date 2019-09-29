import re
import sqlite3

conn = sqlite3.connect('english_vocabulary.sqlite')
cur = conn.cursor()

#cur.execute('DROP TABLE IF EXISTS Words')
#cur.execute('CREATE TABLE Words (id INTEGER, word TEXT)')

word = "trillion"
wordiscorrect = False
word = word.strip()  # Delete spaces on bath sides
word = word.lower()
match = re.match("^[ abcdefghijklmnopqrstuvwxyz]*$", word)  # Check if string consists only letters
if match is not None:
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
    print("Uncorrect word")

if wordiscorrect:
    cur.execute('SELECT * FROM Words')
    #cur.execute('DELETE FROM Words WHERE word = "fourteenteen"')
    counter = 0
    words_match = False
    for row in cur:  # How large is our vocabulary?
        counter += 1
        print(row)
        if new_word == row[1]:
            words_match = True
    print("length of the base: ", counter)

    if words_match is False:  # Add new word
        params = (counter, new_word)
        cur.execute('INSERT INTO Words (id, word) VALUES(?,?)', params)
        conn.commit()
    else:
        print("this word is already exists in vocabulary")

    #cur.execute('DELETE FROM Words WHERE id = 19')
    #conn.commit()
    cur.execute('SELECT * FROM Words')
    for row in cur:
        print(row)

cur.close()
