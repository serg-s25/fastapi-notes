# Notes API

A RESTful API for creating, reading, updating, and deleting notes. Built with FastAPI and SQLite.

![API Overview](images/Overview.png) 

## Tech Stack
- Python 3.x
- FastAPI
- SQLite (Python's built-in `sqlite3`)
- Pydantic
- Uvicorn

## Setup

```bash
git clone https://github.com/YOUR-USERNAME/fastapi-notes.git
cd fastapi-notes
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
uvicorn main:app --reload
```

Open `http://127.0.0.1:8000/docs` for the interactive API docs.

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/notes` | Create a new note |
![Create note](images/create1.png)
![Create note](images/create2.png)

| GET | `/notes` | List all notes |
![List notes](images/get3.png)

| GET | `/notes/{id}` | Get a single note |
![Get note](images/get1.png)

| PUT | `/notes/{id}` | Update a note (partial updates supported) |
![Update note](images/update1.png)
![Update note](images/update2.png)
![Update note](images/update3.png)

| DELETE | `/notes/{id}` | Delete a note |
![Delete note](images/delete1.png)
![Delete note](images/delete2.png)

## Project Structure

```
fastapi-notes/
├── main.py        # API routes and endpoint logic
├── database.py    # SQLite connection and table setup
├── schemas.py     # Pydantic models for request/response validation
├── requirements.txt
└── README.md
```