# GridMark Kanban

A modern, lightweight Kanban board built with FastAPI, HTMX, and SQLite. It features a professional Markdown Editor (EasyMDE) with live side-by-side preview and persistent storage.

## Features

- Full Kanban Workflow: Add, move, and delete tasks across columns.
- Pro Markdown Support: Integrated EasyMDE editor with support for tables, code blocks, and bold text.
- Live Preview: Edit your tasks with a real-time side-by-side Markdown preview.
- Drag & Drop: Smooth task reordering powered by SortableJS.
- No Page Reloads: Built with HTMX for a seamless, Single Page Application (SPA) feel.
- Persistent Storage: All data is saved in a local SQLite database (kanban.db).
- Beautiful UI: Styled with Tailwind CSS and Typography plugin.

## Tech Stack

- Backend: FastAPI (Python)
- Frontend: HTMX, Tailwind CSS, SortableJS
- Editor: EasyMDE
- Database: SQLite

---

## Getting Started

### 1. Clone the repository
```bash
git clone [https://github.com/your-username/gridmark-kanban.git](https://github.com/your-username/gridmark-kanban.git)
cd gridmark-kanban
```
2 How to onstall dependencies
pip install -r requirements.txt

3. How to run the application

1 Run server
```Bash
python main.py```

2 Open the app :
http://127.0.0.1:8000 

in your web browser.