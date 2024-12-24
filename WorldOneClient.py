# client.py (Pygame)

import pygame
import json
import threading
import time
from websocket._app import WebSocketApp


# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Village Game")

# Global variables for game state
game_map = {}
my_house = {}
my_player_id = None

def on_message(ws, msg):
    global game_map, my_house, my_player_id
    data = json.loads(msg)
    if "map" in data:
        game_map = data["map"]
        my_house = data["your_house"]
        my_player_id = data["your_id"]

    elif "message_type" in data: # Process server updates
        if data["message_type"] == "player_moved":
            player_id = data["player_id"]
            if player_id in game_map["players"]:
              game_map["players"][player_id] = data["position"]
        elif data["message_type"] == "player_joined":
          player_id = data["player_id"]
          game_map["players"][player_id] = data["position"]
        elif data["message_type"] == "player_left":
            player_id = data["player_id"]
            if player_id in game_map["players"]:
               del game_map["players"][player_id]

def on_error(ws, error):
    print(f"WebSocket error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("WebSocket connection closed")

def on_open(ws):
    print("WebSocket connection opened")


ws_app = None
def websocket_thread(ws_url):
    global ws_app
    ws_app = WebSocketApp(ws_url,
                                      on_open=on_open,
                                      on_message=on_message,
                                      on_error=on_error,
                                      on_close=on_close)

    ws_app.run_forever()


ws_url = "ws://localhost:8000/ws"
ws_thread = threading.Thread(target=websocket_thread, args=(ws_url,))
ws_thread.daemon = True
ws_thread.start()

# Helper function to send movement to the server
def send_move(new_x, new_y):
    if ws_app:
        data = {"action": "move", "x": new_x, "y": new_y}
        ws_app.send(json.dumps(data))

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if my_player_id and my_player_id in game_map["players"]:
                  if event.key == pygame.K_LEFT:
                      game_map["players"][my_player_id]["x"] -= 10
                      send_move(game_map["players"][my_player_id]["x"], game_map["players"][my_player_id]["y"])
                  elif event.key == pygame.K_RIGHT:
                      game_map["players"][my_player_id]["x"] += 10
                      send_move(game_map["players"][my_player_id]["x"], game_map["players"][my_player_id]["y"])
                  elif event.key == pygame.K_UP:
                      game_map["players"][my_player_id]["y"] -= 10
                      send_move(game_map["players"][my_player_id]["x"], game_map["players"][my_player_id]["y"])
                  elif event.key == pygame.K_DOWN:
                       game_map["players"][my_player_id]["y"] += 10
                       send_move(game_map["players"][my_player_id]["x"], game_map["players"][my_player_id]["y"])



    screen.fill((255, 255, 255))  # Clear screen

    if game_map and my_house:
        for house in game_map["houses"]:
            pygame.draw.rect(screen, (100, 100, 100), (house["x"], house["y"], 20, 20))
        for factory in game_map.get("factories", []):
            pygame.draw.rect(screen, (150, 150, 150), (factory["x"], factory["y"], 20, 20))
        for store in game_map.get("stores", []):
            pygame.draw.rect(screen, (200, 200, 200), (store["x"], store["y"], 20, 20))

        if "players" in game_map:
            for player_id, player_data in game_map["players"].items():
               pygame.draw.circle(screen, (0, 0, 255), (player_data["x"], player_data["y"]), 10)


    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()