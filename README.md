# 🚀 Student Tech Hub

A beginner-friendly full-stack web application built with **plain HTML/CSS/JavaScript** on the frontend and **Python + FastAPI** on the backend.

---

## 📂 Project Structure

```
student-tech-hub/
├── frontend/
│   ├── index.html      ← The web page (structure)
│   ├── style.css       ← Styling (look & feel)
│   └── script.js       ← Interactivity (fetching data, form handling)
│
├── backend/
│   ├── main.py         ← FastAPI server with all API endpoints
│   └── requirements.txt ← Python packages needed
│
└── README.md           ← You are here!
```

---

## 🌟 What the Project Does

| Feature | Description |
|---|---|
| **Event Listing** | Displays upcoming tech events (workshops, hackathons, talks) loaded from the backend |
| **Load Events Button** | Fetches event data live from the FastAPI server using a `GET` request |
| **Registration Form** | Lets students enter their name & email and submit via a `POST` request |
| **CORS Support** | The backend is configured to allow the frontend (on any port) to communicate with it |

---

## ⚙️ How to Install the Backend

> Make sure you have **Python 3.8+** installed. You can check with `python --version`.

### Step 1 – Open a terminal in the `backend/` folder

```bash
cd student-tech-hub/backend
```

### Step 2 – (Recommended) Create a virtual environment

A virtual environment keeps the project's packages separate from your system Python.

```bash
# Create the virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# Activate it (Mac / Linux)
source venv/bin/activate
```

### Step 3 – Install the required packages

```bash
pip install -r requirements.txt
```

This installs:
- **FastAPI** – the web framework for building the API
- **Uvicorn** – a lightweight server to run the FastAPI app

---

## ▶️ How to Run the Backend

Make sure you are inside the `backend/` folder with the virtual environment activated, then run:

```bash
uvicorn main:app --reload
```

You should see output like:

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
```

> `--reload` makes the server restart automatically when you edit `main.py`. Great for development!

### ✅ Test the API in your browser

Once the backend is running, open these URLs:

| URL | What it does |
|---|---|
| `http://127.0.0.1:8000/` | Confirms the server is alive |
| `http://127.0.0.1:8000/api/events` | Returns all events as JSON |
| `http://127.0.0.1:8000/docs` | **Auto-generated interactive API docs** (Swagger UI) |

---

## 🌐 How to Run the Frontend Locally

The frontend is just an HTML file — no build step needed!

### Option A – Use VS Code Live Server (Recommended)

1. Install the **Live Server** extension in VS Code.
2. Open the `frontend/` folder in VS Code.
3. Right-click `index.html` → **"Open with Live Server"**.
4. Your browser will open at `http://127.0.0.1:5500`.

### Option B – Open Directly in Browser

Simply double-click `index.html` to open it in your browser.

> ⚠️ **Note:** Opening the file directly (`file://...`) may cause CORS issues in some browsers when making API requests. Using Live Server (Option A) avoids this.

---

## 🔗 How the Frontend Communicates with the Backend

Here's the flow in simple terms:

```
User clicks "Load Events"
        ↓
script.js sends a GET request to:
  http://127.0.0.1:8000/api/events
        ↓
FastAPI (main.py) receives the request
and returns a JSON response like:
  { "success": true, "events": [...] }
        ↓
script.js reads the JSON and
creates event cards on the page
```

```
User fills the form and clicks "Register"
        ↓
script.js sends a POST request to:
  http://127.0.0.1:8000/api/register
  with body: { "name": "...", "email": "..." }
        ↓
FastAPI validates the data, saves it in memory,
and returns: { "success": true, "message": "..." }
        ↓
script.js shows the success/error message to the user
```

### Why CORS?

Browsers block requests between different "origins" (different ports count as different origins).  
For example, the frontend on port `5500` talking to the backend on port `8000` would normally be blocked.

In `main.py`, we added this to allow it:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Allow requests from any origin
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Backend | Python 3, FastAPI, Uvicorn |
| Data Storage | In-memory (Python list) – no database |

---

## 💡 Want to Learn More?

- [FastAPI Official Docs](https://fastapi.tiangolo.com/)
- [MDN Web Docs – Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)
- [MDN Web Docs – HTML Forms](https://developer.mozilla.org/en-US/docs/Learn/Forms)

---

*Built with ❤️ for students learning full-stack web development.*
