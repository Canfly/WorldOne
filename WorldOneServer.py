# server.py (FastAPI + WebSockets)

from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import random
import json
import uuid

app = FastAPI()

# Load game map from json file
with open("map.json", "r", encoding="utf-8") as f:
    map_data = json.load(f)

game_map = {
    "map_size": map_data["map_size"],
    "tile_size": map_data["tile_size"],
    "tiles": map_data["tiles"],
    "houses": [],
    "players": {}
}

# Locate houses on map
for y, row in enumerate(game_map["tiles"]):
    for x, tile in enumerate(row):
        if tile == "house":
            game_map["houses"].append({"x": x * game_map["tile_size"], "y": y * game_map["tile_size"], "owner": None})

app.websocket_connections = set() # Store all active websocket connection

@app.get("/")
async def get():
    return HTMLResponse(content="<p>Hello, world!</p>")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    client_id = str(uuid.uuid4())  # Generate a unique UUID

    app.websocket_connections.add(websocket) # Add to list of open websocket connections

    # Assign a house
    available_houses = [house for house in game_map["houses"] if house["owner"] is None]
    if available_houses:
        chosen_house = random.choice(available_houses)
        chosen_house["owner"] = client_id
        game_map["players"][client_id] = {"x": chosen_house["x"], "y": chosen_house["y"]}

        initial_data = {
            "map": game_map,
            "your_house": chosen_house,
            "your_id": client_id,
        }
        await websocket.send_text(json.dumps(initial_data))
        await broadcast(websocket, {"message_type": "player_joined", "player_id": client_id, "position": game_map["players"][client_id]})


        try:
            while True:
                data = await websocket.receive_text()
                client_data = json.loads(data)
                action = client_data.get("action")

                if action == "move":
                    new_x = client_data.get("x")
                    new_y = client_data.get("y")
                    if new_x is not None and new_y is not None:
                       game_map["players"][client_id]["x"] = new_x
                       game_map["players"][client_id]["y"] = new_y
                       await broadcast(websocket, {"message_type": "player_moved", "player_id": client_id, "position": game_map["players"][client_id]})


                elif action == "chat":
                    message = client_data.get("message")
                    if message:
                       await broadcast(websocket, {"message_type": "chat", "player_id": client_id, "message": message})



        except Exception as e:
            print(f"Error: {e}")
            del game_map["players"][client_id]
            await broadcast(websocket, {"message_type": "player_left", "player_id": client_id})

        finally:
            app.websocket_connections.remove(websocket)
    else:
        await websocket.send_text(json.dumps({"error": "No available houses"}))

async def broadcast(current_websocket: WebSocket, message: dict):
    """Broadcasts a message to all connected clients."""
    for ws in app.websocket_connections:
         await ws.send_text(json.dumps(message))