# 💬 FastAPI Real-Time Chat Application

A simple yet elegant **real-time chat application** built using **FastAPI** and **WebSockets**, featuring a clean UI and minimal setup.

---

## 🚀 Features
- Real-time communication using **WebSockets**
- Join chat rooms dynamically
- Clean and responsive chat UI
- Lightweight — no database required
- Easy to extend with authentication or Redis pub/sub for scalability

---

## 🧰 Tech Stack
- **Backend:** FastAPI (WebSockets)
- **Frontend:** HTML, CSS, Vanilla JavaScript
- **Server:** Uvicorn

---

## 📦 Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/fastapi-chat-app.git
cd fastapi-chat-app
```

### 2️⃣ Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\\Scripts\\activate
```

### 3️⃣ Install Dependencies
```bash
pip install fastapi uvicorn
```

---

## ▶️ Run the Application
```bash
python real_time_chat_fastapi.py
```

The app will start at: **http://localhost:8000/**

---

## 💻 Usage
1. Open `http://localhost:8000/` in your browser.
2. Enter your **username** and a **room name** (e.g., `main`).
3. Click **Join Room**.
4. Open multiple tabs or browsers to simulate multiple users.
5. Start chatting in real-time!

---

## 🧩 Folder Structure
```
fastapi-chat-app/
│
├── real_time_chat_fastapi.py   # Main FastAPI app
├── README.md                   # Project documentation
└── requirements.txt            # Dependencies (optional)
```

---

## ⚙️ Customization Ideas
- Add **user authentication (JWT)**
- Store **chat history** in a database (SQLite, PostgreSQL)
- Integrate **Redis Pub/Sub** for distributed chat rooms
- Add **typing indicators** and **user join/leave notifications**
- Create a **React/Vue frontend** for better UI/UX

---

## 📸 Screenshot
*(Optional — add an image of your running chat app here)*

---

## 🧑‍💻 Author
**Vivek**  
B.Tech (CSE) | Developer | Learner

---

## 🪪 License
This project is licensed under the **MIT License** — feel free to use and modify it for learning or production.

---

### ⭐ Don’t forget to star the repo if you found it helpful!