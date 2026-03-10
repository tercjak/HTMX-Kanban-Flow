from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import markdown
import sqlite3
import uuid

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Rozszerzone wsparcie dla tabel i kodu w Markdown
templates.env.filters["markdown"] = lambda text: markdown.markdown(text, extensions=['tables', 'fenced_code']) if text else ""

def get_db_connection():
    conn = sqlite3.connect('kanban.db')
    conn.row_factory = sqlite3.Row
    return conn

# Inicjalizacja bazy przy starcie
with get_db_connection() as conn:
    conn.execute('CREATE TABLE IF NOT EXISTS tasks (id TEXT PRIMARY KEY, title TEXT, content TEXT, status TEXT)')

async def get_board_response(request: Request, template_name: str = "board.html"):
    """Pomocnicza funkcja do pobierania aktualnego stanu tablicy z bazy"""
    tasks = {"todo": [], "in_progress": [], "done": []}
    with get_db_connection() as conn:
        rows = conn.execute('SELECT * FROM tasks').fetchall()
        for row in rows:
            tasks[row['status']].append(dict(row))
    return templates.TemplateResponse(template_name, {"request": request, "tasks": tasks})

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return await get_board_response(request, "index.html")

@app.post("/add", response_class=HTMLResponse)
async def add_task(request: Request, title: str = Form(...), content: str = Form(""), column: str = Form("todo")):
    with get_db_connection() as conn:
        conn.execute('INSERT INTO tasks (id, title, content, status) VALUES (?, ?, ?, ?)',
                     (str(uuid.uuid4()), title, content, column))
    return await get_board_response(request)

@app.get("/task/{task_id}/edit", response_class=HTMLResponse)
async def edit_task_modal(request: Request, task_id: str):
    with get_db_connection() as conn:
        task = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
    if not task:
        return HTMLResponse("Nie znaleziono zadania", status_code=404)
    return templates.TemplateResponse("edit_modal.html", {"request": request, "task": dict(task)})

@app.post("/task/{task_id}/edit", response_class=HTMLResponse)
async def update_task(request: Request, task_id: str, title: str = Form(...), content: str = Form("")):
    with get_db_connection() as conn:
        conn.execute('UPDATE tasks SET title = ?, content = ? WHERE id = ?', (title, content, task_id))
    return await get_board_response(request)

@app.post("/move-drag/{task_id}/{to_column}", response_class=HTMLResponse)
async def move_drag(request: Request, task_id: str, to_column: str):
    with get_db_connection() as conn:
        conn.execute('UPDATE tasks SET status = ? WHERE id = ?', (to_column, task_id))
    return await get_board_response(request)

@app.delete("/delete/{task_id}", response_class=HTMLResponse)
async def delete_task(request: Request, task_id: str):
    with get_db_connection() as conn:
        conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    return await get_board_response(request)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)