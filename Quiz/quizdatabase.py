# gets current date and time
from datetime import datetime

# creates database and manipulates data
import sqlite3

# generates random value
import random

# create a connection to the database
db = sqlite3.connect('quizdatabase.db')
print(db)

# Creating Cursor
cur = db.cursor()

# method of getting random values
random_value = (random.randint(1000000, 9999999))

# converting values to hex decimal
val = format(random_value, 'x')

# getting current date and storing in a variable
now = datetime.now()
formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')

# cur.execute("CREATE table Userdetails(Username VARCHAR(10), Emailaddress VARCHAR(100), Password VARCHAR(8))")

# cur.execute("CREATE table Questions(question VARCHAR(500), right_answer VARCHAR(100), wrong1 VARCHAR(100), wrong2 VARCHAR(100), wrong3 VARCHAR(100), wrong4 VARCHAR(100))")

# cur.execute("Create table LoginHistory(Username VARCHAR(10), Login_date DATETIME)")

db.commit()