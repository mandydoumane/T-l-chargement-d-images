import sqlite3

DATABASE = 'app.db'
db = sqlite3.connect(DATABASE)

cursor = db.cursor()


# Creation table "pictures"
cursor.execute("DROP TABLE IF EXISTS pictures")
cursor.execute("""CREATE TABLE pictures (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                     path VARCHAR(200) NOT NULL,
                                     title VARCHAR(200) NOT NULL,
                                     category VARCHAR(200) NOT NULL,
                                     description VARCHAR(200) NOT NULL,
                                     create_date INTEGER NOT NULL)""")

cursor.execute("DROP TABLE IF EXISTS comments")
cursor.execute("""CREATE TABLE comments (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                         comment VARCHAR(200),
                                         image_id INTEGER)""")
# creation table "category"
# cursor.execute("DROP TABLE IF EXISTS category")
# cursor.execute("""CREATE TABLE category (id INTEGER PRIMARY KEY AUTOINCREMENT,
#                                      path VARCHAR(200) NOT NULL,
#                                      title VARCHAR(200) NOT NULL,
#                                      category VARCHAR(200) NOT NULL,
#                                      description VARCHAR(200) NOT NULL)""")

# Save changements
db.commit()

# Close database
db.close()
