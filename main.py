from fastapi import FastAPI, Request, Form, UploadFile, File, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os, shutil, json

app = FastAPI(title="FastAPI Chat with File Sharing")
templates = Jinja2Templates(directory="templates")

DEFAULT_USERNAME = "admin"
DEFAULT_PASSWORD = "12345"

rooms = {}
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

@app.get("/", response_class=HTMLResponse)
async def show_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    if username == DEFAULT_USERNAME and password == DEFAULT_PASSWORD:
        return RedirectResponse(url=f"/chat?username={username}", status_code=303)
    else:
        return RedirectResponse(url="/?error=invalid_credentials", status_code=303)

@app.get("/chat", response_class=HTMLResponse)
async def chat_page(request: Request, username: str = "Guest"):
    return templates.TemplateResponse("chat.html", {"request": request, "username": username})

@app.post("/upload")
async def upload_file(username: str = Form(...), room: str = Form(...), file: UploadFile = File(...)):
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    file_url = f"/uploads/{file.filename}"

    if room in rooms:
        message = json.dumps({
            "type": "file",
            "username": username,
            "filename": file.filename,
            "url": file_url
        })
        for conn in rooms[room]:
            await conn.send_text(message)

    return {"message": "File uploaded successfully", "url": file_url}

@app.websocket("/ws/{room}")
async def websocket_endpoint(ws: WebSocket, room: str):
    await ws.accept()
    username = ws.query_params.get("username", "Guest")

    if room not in rooms:
        rooms[room] = set()
    rooms[room].add(ws)

    join_msg = json.dumps({"system": f"👋 {username} joined the chat."})
    for conn in rooms[room]:
        await conn.send_text(join_msg)

    try:
        while True:
            data = await ws.receive_text()
            msg_data = json.loads(data)
            message = msg_data.get("message", "")
            if message:
                payload = json.dumps({"username": username, "message": message})
                for conn in rooms[room]:
                    await conn.send_text(payload)
    except WebSocketDisconnect:
        rooms[room].remove(ws)
        leave_msg = json.dumps({"system": f"❌ {username} left the chat."})
        for conn in rooms.get(room, []):
            await conn.send_text(leave_msg)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
