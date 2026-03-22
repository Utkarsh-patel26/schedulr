# Asynchronous Task Scheduler

A lightweight distributed backend system for scheduling and executing periodic background tasks. Built using FastAPI, MongoDB, Redis, and Celery, this application allows you to define tasks with cron-based schedules, start/end windows, and automatic execution via worker processes.

---

## 🚀 Tech Stack

* **API & Scheduler:** FastAPI (Python)
* **Database:** MongoDB (Motor - Async)
* **Message Broker:** Redis
* **Task Queue / Worker:** Celery
* **Frontend:** React (Vite)

---

## 📦 Prerequisites

Ensure the following are installed:

* Python 3.8+
* Node.js (for frontend)
* Redis (local on port 6379 or cloud instance)
* MongoDB (local or Atlas)

---

## ⚙️ Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/Utkarsh-patel26/schedulr.git
cd backend
```

---

### 2. Create virtual environment

#### Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3. Install backend dependencies

```bash
pip install fastapi uvicorn motor pydantic redis celery eventlet python-dotenv croniter
```

---

### 4. Configure environment variables

Create a `.env` file in root:

```env
MONGO_DETAILS=mongodb+srv://<username>:<password>@<cluster-url>/task_scheduler_db?retryWrites=true&w=majority
REDIS_URL=redis://localhost:6379
```

---

## ▶️ Running the Application

⚠️ This system requires **3 terminals**

---

### 🔹 Terminal 1 — Start FastAPI Server

```bash
uvicorn main:app --reload
```

API:

```
http://127.0.0.1:8000
```

---

### 🔹 Terminal 2 — Start Celery Worker

#### Windows:

```bash
celery -A worker.celery_app worker --loglevel=info -P eventlet
```

#### macOS/Linux:

```bash
celery -A worker.celery_app worker --loglevel=info
```

---

### 🔹 Terminal 3 — Start Frontend (React)

Navigate to frontend folder:

```bash
cd ../frontend
npm install
npm run dev
```

Frontend:

```
http://localhost:5173
```

---

## 📌 Usage

Send a POST request to:

```
/api/tasks
```

### Example Request:

```json
{
  "name": "My Scheduled Task",
  "cron": "*/5 * * * *",
  "nextRun": "2026-03-22T10:00:00Z",
  "startDate": "2026-03-22T09:00:00Z",
  "endDate": "2026-03-23T09:00:00Z"
}
```

---

## 🔄 How It Works

1. Tasks are stored in MongoDB
2. Scheduler (FastAPI) checks every 60 seconds
3. Matching tasks are sent to Celery
4. Celery workers execute tasks
5. `nextRun` is updated using cron expression

---

## ⚠️ Notes

* Use UTC time (`Z` format) for all timestamps
* Ensure Redis is running before starting worker
* MongoDB Atlas IP whitelist must allow your IP (`0.0.0.0/0` for dev)

---

## 📁 Project Structure (Simplified)

```
backend/
│── main.py
│── worker.py
│── .env
│── requirements.txt

frontend/
│── src/
│── package.json
```

---

## ✅ Status

* MongoDB Integration ✔️
* Redis Queue ✔️
* Scheduler Logic ✔️
* Celery Worker ✔️
* React Frontend ✔️

---

## 📬 Future Improvements

* Add retry logic
* Add logging system
* UI dashboard for task monitoring
* Authentication

---
