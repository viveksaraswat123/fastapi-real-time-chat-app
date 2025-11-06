from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import json, asyncio

app = FastAPI(title="FastAPI Chat App")

rooms = {}

@app.get("/", response_class=HTMLResponse)
async def get():
    return HTMLResponse("""
<!DOCTYPE html>
<html>
<head>
<title>Chat App</title>
<style>
  body { font-family: Arial; display: flex; flex-direction: column; align-items: center; margin-top: 40px; }
  #chat-box { width: 400px; height: 400px; border: 1px solid #ccc; overflow-y: auto; padding: 10px; border-radius: 10px; background: #f9f9f9; }
  #chat-box div { margin: 5px 0; padding: 6px 10px; border-radius: 6px; }
  .me { background: #d1f0ff; align-self: flex-end; }
  .other { background: #e8e8e8; }
  #controls { margin-top: 10px; width: 400px; display: flex; }
  input { flex: 1; padding: 8px; border-radius: 6px; border: 1px solid #ccc; }
  button { margin-left: 6px; padding: 8px 12px; border: none; border-radius: 6px; background: #0078ff; color: white; cursor: pointer; }
  button:disabled { background: gray; }
</style>
</head>
<body>
  <h2>FastAPI Chat</h2>
  <input id="username" placeholder="Enter username" style="width: 200px; margin-bottom: 10px;"/>
  <input id="room" placeholder="Enter room name" style="width: 200px; margin-bottom: 10px;"/>
  <button id="connect">Join Room</button>
  <div id="chat-box"></div>
  <div id="controls">
    <input id="msg" placeholder="Type a message..." />
    <button id="send" disabled>Send</button>
  </div>
  
<script>
let ws = null;
let username = "";
let room = "";
const box = document.getElementById('chat-box');
const msgInput = document.getElementById('msg');
const sendBtn = document.getElementById('send');
const connectBtn = document.getElementById('connect');

function addMessage(user, text, isMe=false){
  const div = document.createElement('div');
  div.textContent = `${user}: ${text}`;
  div.className = isMe ? 'me' : 'other';
  box.appendChild(div);
  box.scrollTop = box.scrollHeight;
}

connectBtn.onclick = () => {
  username = document.getElementById('username').value.trim() || 'Anon';
  room = document.getElementById('room').value.trim() || 'main';
  ws = new WebSocket(`ws://${location.host}/ws/${room}?username=${username}`);
  ws.onopen = () => { connectBtn.disabled = true; sendBtn.disabled = false; addMessage('System', `You joined room: ${room}`); };
  ws.onmessage = (e) => {
    try {
      const data = JSON.parse(e.data);
      if (data.username && data.message){
        const isMe = data.username === username;
        addMessage(isMe ? 'You' : data.username, data.message, isMe);
      }
    } catch {}
  };
  ws.onclose = () => { addMessage('System', 'Connection closed.'); connectBtn.disabled = false; sendBtn.disabled = true; };
};

sendBtn.onclick = () => {
  const text = msgInput.value.trim();
  if(!text) return;
  ws.send(JSON.stringify({ message: text }));
  msgInput.value = '';
};

msgInput.addEventListener('keyup', e => { if(e.key === 'Enter') sendBtn.click(); });
</script>
</body>
</html>
""")

@app.websocket("/ws/{room}")
async def websocket_endpoint(ws: WebSocket, room: str):
    await ws.accept()
    username = ws.query_params.get("username", "Anon")
    if room not in rooms:
        rooms[room] = set()
    rooms[room].add(ws)

    try:
        while True:
            data = await ws.receive_text()
            msg = json.loads(data).get("message", "")
            payload = json.dumps({"username": username, "message": msg})
            for conn in rooms[room]:
                await conn.send_text(payload)
    except WebSocketDisconnect:
        rooms[room].remove(ws)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('real_time_chat_fastapi:app', host='0.0.0.0', port=8000, reload=True)
