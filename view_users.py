import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "users.db"
connection = sqlite3.connect(DB_PATH)

try:
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id, name, email, created_at FROM users ORDER BY id"
    )
    users = cursor.fetchall()

    if not users:
        print("No users found.")
    else:
        for user in users:
            print(f"ID: {user[0]}")
            print(f"Name: {user[1]}")
            print(f"Email: {user[2]}")
            print(f"Created: {user[3]}")
            print("-" * 30)

    print(f"Total users: {len(users)}")

finally:
    connection.close()