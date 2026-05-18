from fastapi import FastAPI, HTTPException
from schemas import NoteCreate, NoteUpdate, NoteResponse
from database import get_connection, init_db
from typing import List

app = FastAPI(
    title="Notes API",
    description="A simple REST API to create, read, update, and delete notes.",
    version="1.0.0"
)

@app.on_event("startup")
def startup():
    init_db()

@app.post("/notes", response_model=NoteResponse, status_code=201)
def create_note(note: NoteCreate):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO notes (title, content) VALUES (?, ?)",
        (note.title, note.content)
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return get_note(new_id)

@app.get("/notes", response_model=List[NoteResponse])
def list_notes():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notes ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.get("/notes/{note_id}", response_model=NoteResponse)
def get_note(note_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notes WHERE id = ?", (note_id,))
    row = cursor.fetchone()
    conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return dict(row)

@app.put("/notes/{note_id}", response_model=NoteResponse)
def update_note(note_id: int, note: NoteUpdate):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notes WHERE id = ?", (note_id,))
    existing = cursor.fetchone()
    if existing is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Note not found")
    updated_title   = note.title   if note.title   is not None else existing["title"]
    updated_content = note.content if note.content is not None else existing["content"]
    cursor.execute(
        "UPDATE notes SET title = ?, content = ?, updated_at = datetime('now') WHERE id = ?",
        (updated_title, updated_content, note_id)
    )
    conn.commit()
    conn.close()
    return get_note(note_id)

@app.delete("/notes/{note_id}", status_code=204)
def delete_note(note_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM notes WHERE id = ?", (note_id,))
    if cursor.fetchone() is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Note not found")
    cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    conn.commit()
    conn.close()