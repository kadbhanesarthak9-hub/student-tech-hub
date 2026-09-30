# ============================================================
# main.py  –  Student Tech Hub Backend
# Powered by FastAPI + SQLite Database
#
# Run with:  uvicorn main:app --reload
# ============================================================

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
import os

# ------------------------------------------------------------------
# 1. Create the FastAPI app
# ------------------------------------------------------------------
app = FastAPI(title="Student Tech Hub API", version="2.0.0")

# ------------------------------------------------------------------
# 2. Enable CORS
# ------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------------------
# 3. Database Setup (SQLite)
#    SQLite is a simple file-based database — perfect for beginners!
#    No extra installation needed — it comes built into Python.
# ------------------------------------------------------------------

# The database file will be created in the same folder as main.py
DATABASE_FILE = "students.db"


def get_db_connection():
    """Create and return a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row  # Lets us access columns by name (like a dict)
    return conn


def init_db():
    """
    Create the database tables if they don't already exist.
    This runs automatically when the server starts.
    """
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            name      TEXT    NOT NULL,
            email     TEXT    NOT NULL UNIQUE,
            joined_at TEXT    DEFAULT (datetime('now', 'localtime'))
        )
    """)
    conn.commit()
    conn.close()
    print("✅ Database ready: students.db")


# Run DB initialisation when the app starts
@app.on_event("startup")
def startup():
    init_db()


# ------------------------------------------------------------------
# 4. Sample event data (stored in memory – no table needed)
# ------------------------------------------------------------------
EVENTS = [
    { "id": 1, "title": "Python for Beginners Workshop",  "date": "2026-10-10", "time": "10:00 AM", "location": "Room 201, CS Block",  "category": "Workshop",   "description": "An introductory workshop on Python programming for absolute beginners." },
    { "id": 2, "title": "Web Dev Hackathon 2026",          "date": "2026-10-18", "time": "9:00 AM",  "location": "Main Auditorium",    "category": "Hackathon",  "description": "Build a web app in 24 hours and compete with fellow students!" },
    { "id": 3, "title": "AI & Machine Learning Talk",      "date": "2026-10-25", "time": "2:00 PM",  "location": "Seminar Hall B",     "category": "Talk",       "description": "Industry experts share how AI is reshaping the tech landscape." },
    { "id": 4, "title": "Open Source Contribution Day",    "date": "2026-11-02", "time": "11:00 AM", "location": "Lab 3, IT Block",    "category": "Workshop",   "description": "Learn how to contribute to real open source projects on GitHub." },
    { "id": 5, "title": "Tech Career Fair",                "date": "2026-11-15", "time": "10:00 AM", "location": "College Ground",     "category": "Networking", "description": "Connect with top tech companies and explore internship opportunities." },
]

# ------------------------------------------------------------------
# 5. Pydantic model for registration
# ------------------------------------------------------------------
class Student(BaseModel):
    name: str
    email: str

# ------------------------------------------------------------------
# 6. API Endpoints
# ------------------------------------------------------------------

@app.get("/")
def home():
    return {"message": "Welcome to the Student Tech Hub API! 🚀", "version": "2.0.0"}


@app.get("/api/events")
def get_events():
    """
    GET /api/events
    Returns all upcoming tech events as JSON.
    """
    return {
        "success": True,
        "count": len(EVENTS),
        "events": EVENTS,
    }


@app.post("/api/register")
def register_student(student: Student):
    """
    POST /api/register
    Saves student name & email to the SQLite database.

    Request body:
    {
        "name": "Priya Sharma",
        "email": "priya@example.com"
    }
    """
    conn = get_db_connection()
    try:
        conn.execute(
            "INSERT INTO students (name, email) VALUES (?, ?)",
            (student.name, student.email)
        )
        conn.commit()

        # Count total registered students
        total = conn.execute("SELECT COUNT(*) FROM students").fetchone()[0]

        return {
            "success": True,
            "message": f"🎉 Welcome, {student.name}! You have been registered successfully.",
            "total_registered": total,
        }

    except sqlite3.IntegrityError:
        # This error is raised when the email already exists (UNIQUE constraint)
        return {
            "success": False,
            "message": f"'{student.email}' is already registered!",
        }
    finally:
        conn.close()


@app.get("/api/students")
def get_all_students():
    """
    GET /api/students
    Returns a list of all registered students from the database.
    Useful for checking who has registered.
    """
    conn = get_db_connection()
    rows = conn.execute(
        "SELECT id, name, email, joined_at FROM students ORDER BY id DESC"
    ).fetchall()
    conn.close()

    students = [dict(row) for row in rows]
    return {
        "success": True,
        "count": len(students),
        "students": students,
    }


@app.delete("/api/students/{student_id}")
def delete_student(student_id: int):
    """
    DELETE /api/students/{id}
    Removes a student from the database by their ID.
    Example: DELETE /api/students/1
    """
    conn = get_db_connection()
    result = conn.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()
    conn.close()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Student not found.")

    return {"success": True, "message": f"Student #{student_id} removed successfully."}
