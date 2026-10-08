import sqlite3
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from database import create_tables, get_connection
from schemas import UserCreate, UserUpdate


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(
    title="Users Management API",
    lifespan=lifespan,
)

@app.post("/api/v1/users", status_code=201)
def create_user(user: UserCreate):
    connection = get_connection()

    try:
        cursor = connection.execute(
            "INSERT INTO users (name, email) VALUES (?, ?)",
            (user.name, str(user.email)),
        )

        created_user = connection.execute(
            """
            SELECT id, name, email, created_at
            FROM users
            WHERE id = ?
            """,
            (cursor.lastrowid,),
        ).fetchone()

        connection.commit()

        return dict(created_user)

    except sqlite3.IntegrityError as error:
        connection.rollback()

        if error.sqlite_errorname == "SQLITE_CONSTRAINT_UNIQUE":
            raise HTTPException(
                status_code=409,
                detail="A user with this email already exists",
            ) from error

        raise

    finally:
        connection.close()
@app.get("/")
def home():
    return {"message": "Users API is running"}




@app.get("/api/v1/users")
def get_users():
    connection = get_connection()

    try:
        cursor = connection.execute(
            "SELECT id, name, email, created_at FROM users ORDER BY id"
        )
        users = cursor.fetchall()

        return [dict(user) for user in users]
    finally:
        connection.close()
@app.patch("/api/v1/users/{user_id}")
def update_user(user_id: int, user: UserUpdate):
    changes = user.model_dump(exclude_unset=True)

    if not changes:
        raise HTTPException(
            status_code=400,
            detail="Provide a name or email to update",
        )

    connection = get_connection()

    try:
        # Start a transaction before reading and updating.
        connection.execute("BEGIN IMMEDIATE")

        existing_user = connection.execute(
            "SELECT * FROM users WHERE id = ?",
            (user_id,),
        ).fetchone()

        if existing_user is None:
            raise HTTPException(
                status_code=404,
                detail="User not found",
            )

        name = changes.get("name", existing_user["name"])
        email = changes.get("email", existing_user["email"])

        connection.execute(
            "UPDATE users SET name = ?, email = ? WHERE id = ?",
            (name, str(email), user_id),
        )

        updated_user = connection.execute(
            "SELECT * FROM users WHERE id = ?",
            (user_id,),
        ).fetchone()

        connection.commit()

        return dict(updated_user)

    except sqlite3.IntegrityError as error:
        connection.rollback()

        if error.sqlite_errorname == "SQLITE_CONSTRAINT_UNIQUE":
            raise HTTPException(
                status_code=409,
                detail="A user with this email already exists",
            ) from error

        raise

    finally:
        connection.close()
@app.delete("/api/v1/users/{user_id}")
def delete_user(user_id: int):
    connection = get_connection()

    try:
        cursor = connection.execute(
            "DELETE FROM users WHERE id = ?",
            (user_id,),
        )

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="User not found",
            )

        connection.commit()

        return {
            "message": "User deleted successfully",
            "user_id": user_id,
        }

    finally:
        connection.close()
 
 
 