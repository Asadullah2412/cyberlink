from fastapi import FastAPI,WebSocket,WebSocketDisconnect
from fastapi.responses import HTMLResponse

from connection import ConnectionManager

app = FastAPI()




manager = ConnectionManager()

@app.get('/')
async def get():
    with open("index.html", "r", encoding="utf-8") as file:
        return HTMLResponse(content=file.read())
    

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")
