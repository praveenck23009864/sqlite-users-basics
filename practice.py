import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "users.db"
connection = sqlite3.connect(DB_PATH)

try:
    cursor = connection.cursor()

    # CREATE: insert a user using placeholders.
    cursor.execute(
        "INSERT INTO users (name, email) VALUES (?, ?)",
        ("Praveen", "praveen2@example.com"),
    )
    user_id = cursor.lastrowid
    connection.commit()
    print("Created user ID:", user_id)

    # READ: retrieve all users.
    cursor.execute("SELECT * FROM users ORDER BY id")
    print("\nAll users:")
    for user in cursor.fetchall():
        print(user)

    # FILTER: retrieve Gmail users.
    cursor.execute(
        "SELECT * FROM users WHERE email LIKE ?",
        ("%@gmail.com",),
    )
    print("\nGmail users:", cursor.fetchall())

    # FUNCTION: count records.
    cursor.execute("SELECT COUNT(*) FROM users")
    print("\nTotal users:", cursor.fetchone()[0])

    # FUNCTION: uppercase names in the result.
    cursor.execute("SELECT id, UPPER(name) FROM users")
    print("\nUppercase names:", cursor.fetchall())

    # UPDATE: change the user created above.
    cursor.execute(
        "UPDATE users SET name = ? WHERE id = ?",
        ("Praveen C K", user_id),
    )
    connection.commit()

    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    print("\nUpdated user:", cursor.fetchone())

    cursor.execute(
        "DELETE FROM users WHERE id = ?",
        (user_id,),
    )
    connection.commit()

    print("\nDeleted rows:", cursor.rowcount)

except sqlite3.IntegrityError as error:
    connection.rollback()
    print("Constraint error:", error)

finally:
    connection.close()