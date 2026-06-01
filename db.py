import sqlite3

def init_db():
    conn = sqlite3.connect("notes.db")
    
    cursor = conn.cursor()

    cursor.execute("""
                   
  CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        )
                   
"""
    )

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL unique,
            password TEXT NOT NULL
        )
                   
"""
    )
    

    conn.commit()
    conn.close()