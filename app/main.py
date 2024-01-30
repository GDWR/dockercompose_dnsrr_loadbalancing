import asyncio
import os

from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

app = FastAPI()


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
    print("Client connected")
    await websocket.accept()
    while True:
        print("Sending message to client")
        await websocket.send_text(f"Hello from {os.uname().nodename}")
        await asyncio.sleep(1)
