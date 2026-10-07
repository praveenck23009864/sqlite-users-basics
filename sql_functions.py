import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "users.db"
connection = sqlite3.connect(DB_PATH)

try:
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM users")
    print("Total users:", cursor.fetchone()[0])

    cursor.execute("SELECT MIN(id), MAX(id) FROM users")
    smallest_id, largest_id = cursor.fetchone()
    print("Smallest ID:", smallest_id)
    print("Largest ID:", largest_id)

    # Use sample numbers to understand AVG.
    cursor.execute("""
        SELECT AVG(score)
        FROM (
            SELECT 60 AS score
            UNION ALL SELECT 80
            UNION ALL SELECT 100
        )
    """)
    print("Average sample score:", cursor.fetchone()[0])

    cursor.execute("SELECT UPPER(name), LOWER(email) FROM users")
    print("\nFormatted users:")
    for name, email in cursor.fetchall():
        print(f"{name} | {email}")

finally:
    connection.close()