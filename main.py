from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import json

app = FastAPI(title="FastAPI Real-Time Chat")

templates = Jinja2Templates(directory="templates")

rooms = {}
usernames = {}


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})


@app.websocket("/ws/{room}")
async def websocket_endpoint(ws: WebSocket, room: str):
    await ws.accept()
    username = ws.query_params.get("username", "Anonymous")

    if room not in rooms:
        rooms[room] = set()
    rooms[room].add(ws)
    usernames[ws] = username

    join_msg = json.dumps({"system": f" {username} joined the chat."})
    for conn in rooms[room]:
        await conn.send_text(join_msg)

    try:
        while True:
            data = await ws.receive_text()
            msg_data = json.loads(data)
            if "typing" in msg_data:
                payload = json.dumps({"type": "typing", "username": username})
                for conn in rooms[room]:
                    if conn != ws:
                        await conn.send_text(payload)
            elif "message" in msg_data:
                msg = msg_data["message"]
                payload = json.dumps({"username": username, "message": msg})
                for conn in rooms[room]:
                    await conn.send_text(payload)
    except WebSocketDisconnect:
        rooms[room].remove(ws)
        del usernames[ws]
        leave_msg = json.dumps({"system": f" {username} left the chat."})
        for conn in rooms[room]:
            await conn.send_text(leave_msg)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
