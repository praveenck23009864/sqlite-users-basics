import sqlite3
from pathlib import Path

# Store users.db beside this Python script.
DB_PATH = Path(__file__).resolve().parent / "users.db"

connection = sqlite3.connect(DB_PATH)

try:
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()

    print("Users table is ready.")
    print(f"Database location: {DB_PATH}")

finally:
    connection.close()
