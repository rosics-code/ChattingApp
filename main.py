from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

connected_clients = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            for client in connected_clients:
                if client != websocket:
                    await client.send_text(data)
    except Exception as e:
        print(f"Client disconnected: {e}")
    finally:
        connected_clients.remove(websocket)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
