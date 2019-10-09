import re
import sqlite3

conn = sqlite3.connect('english_vocabulary.sqlite')
cur = conn.cursor()

# Do not uncomment if database already created:
#cur.execute('DROP TABLE IF EXISTS Words')
#cur.execute('CREATE TABLE Words (id INTEGER, word TEXT)')
# Irregular Verbs start from 1033 to 1277

word = "wound"
wordiscorrect = False
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
print(match0, match)
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
    print("Uncorrect word")

if wordiscorrect:
    cur.execute('SELECT * FROM Words')
    counter = 0
    last_number = 0
    words_match = False
    for row in cur:  # How large is our vocabulary?
        counter += 1
        last_number = row[0]  # It is used for next id calculation
        print(row)
        if new_word == row[1]:
            words_match = True
    print("length of the base: ", counter)

    if words_match is False:  # Add new word
        params = (last_number+1, new_word)
        cur.execute('INSERT INTO Words (id, word) VALUES(?,?)', params)
        conn.commit()
    else:
        print("this word is already exists in vocabulary")

    #cur.execute('DELETE FROM Words WHERE id = 617')
    #cur.execute('INSERT INTO Words (id, word) VALUES(?,?)', (181, "grandmother"))
    #conn.commit()
    cur.execute('SELECT * FROM Words')
    for row in cur:
        print(row)

cur.close()
