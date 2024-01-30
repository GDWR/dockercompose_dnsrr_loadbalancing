import os

from fastapi.websockets import WebSocketState

import redis.asyncio as redis

from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

app = FastAPI()
r = redis.Redis(host="redis", port=6379)


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Example</title>
    </head>
    <body>
        <h1>WebSocket Messages</h1>
        <button id="reconnectButton">Reconnect</button>
        <ol id='messages'>
        </ol>
        <script>
            ws = new WebSocket("ws://localhost:8000/ws");

            ws.onmessage = function(event) {
                var messages = document.getElementById('messages');
                var message = document.createElement('li');
                var content = document.createTextNode(event.data);       
                message.appendChild(content)
                messages.appendChild(message)
            };        
            
            var reconnectButton = document.getElementById("reconnectButton");
            reconnectButton.addEventListener('click', function() {
                ws.close();

                var messages = document.getElementById('messages');
                var message = document.createElement('li');
                var content = document.createTextNode("Reconnection Requested");       
                message.appendChild(content)
                messages.appendChild(message)

                ws = new WebSocket("ws://localhost:8000/ws");
                ws.onmessage = function(event) {
                    var messages = document.getElementById('messages');
                    var message = document.createElement('li');
                    var content = document.createTextNode(event.data);       
                    message.appendChild(content)
                    messages.appendChild(message)
                };       
            }, false);
        </script>
    </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("Client connected")

    while websocket.client_state is not WebSocketState.DISCONNECTED:
        async with r.pubsub() as pubsub:
            await pubsub.subscribe("messages")

            while True:
                message = await pubsub.get_message(ignore_subscribe_messages=True)
                if message is not None:
                    content = message["data"].decode()
                    await websocket.send_text(f"app({os.uname().nodename}) {content}")
