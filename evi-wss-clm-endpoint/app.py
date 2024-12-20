import json

import uvicorn
from agent import eliza_response

from fastapi import FastAPI, WebSocket

eliza_app = FastAPI()


@eliza_app.get("/")
async def root():
    return {"message": "Hello World"}


@eliza_app.websocket("/ws")
async def websocket_handler(websocket: WebSocket) -> None:
    await websocket.accept()
    while True:
        data = await websocket.receive_text()

        hume_payload = json.loads(data)

        print(hume_payload)

        last_message = hume_payload["messages"][-1]["message"]["content"]

        user_text = last_message.split("{")[0] or ""

        await websocket.send_text(
            json.dumps({"type": "assistant_input", "text": eliza_response(user_text)})
        )
        await websocket.send_text(json.dumps({"type": "assistant_end"}))


if __name__ == "__main__":
    uvicorn.run(eliza_app, host="0.0.0.0", port=8000)
