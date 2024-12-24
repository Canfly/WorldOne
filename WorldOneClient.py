# client.py (Pygame)

import pygame
import json
import threading
import time
from websocket import WebSocketApp

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Village Game")

# Global variables for game state
game_map = {}
my_house = {}
my_player_id = None

# Colors for tiles
tile_colors = {
    "grass": (0, 150, 0),
    "road": (100, 100, 100),
    "house": (0, 0, 150),
    "factory": (150, 150, 150),
    "store": (200, 100, 0),
    "farm": (200, 200, 0),
    "mine": (100, 50, 0),
    "school": (0, 100, 100),
    "hospital": (255, 0, 0),
    "police": (0, 0, 255),
    "park": (0, 100, 0),
    "power_plant": (255, 255, 0),
    "water_pump": (0, 200, 255)
}

# Emojis for tiles
tile_emojis = {
    "grass": "🍀",
    "road": "️⚫️",
    "house": "🏠",
    "factory": "🏭",
    "store": "🏪",
    "farm": "🏡",
    "mine": "⛏️",
    "school": "🚸",
    "hospital": "🏥",
    "police": "🌳",
    "park": "🚨",
    "power_plant": "⚡",
    "water_pump": "💧"
}

# Font for emojis
tile_size = 28
font = pygame.font.Font("NotoEmoji-VariableFont_wght.ttf", tile_size) # Linux/macOS

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
                new_x, new_y = game_map["players"][my_player_id]["x"], game_map["players"][my_player_id]["y"]
                if event.key == pygame.K_LEFT:
                    new_x -= tile_size
                elif event.key == pygame.K_RIGHT:
                    new_x += tile_size
                elif event.key == pygame.K_UP:
                    new_y -= tile_size
                elif event.key == pygame.K_DOWN:
                    new_y += tile_size

                # Ensure movement is only on "road"
                if 0 <= new_x < game_map["map_size"]["width"] * tile_size and 0 <= new_y < game_map["map_size"]["height"] * tile_size:
                    tile_x, tile_y = new_x // tile_size, new_y // tile_size
                    if game_map["tiles"][tile_y][tile_x] == "road":
                        game_map["players"][my_player_id]["x"] = new_x
                        game_map["players"][my_player_id]["y"] = new_y
                        send_move(new_x, new_y)

    screen.fill((255, 255, 255))  # Clear screen

    if game_map:
        for y, row in enumerate(game_map["tiles"]):
            for x, tile in enumerate(row):
                tile_color = tile_colors.get(tile, (200, 200, 200))
                pygame.draw.rect(screen, tile_color, (x * tile_size, y * tile_size, tile_size, tile_size))

                emoji = tile_emojis.get(tile, "?")
                text_surface = font.render(emoji, True, (0, 0, 0))
                text_rect = text_surface.get_rect(center=(x * tile_size + tile_size // 2, y * tile_size + tile_size // 2))
                screen.blit(text_surface, text_rect)

        if "players" in game_map:
            for player_id, player_data in game_map["players"].items():
                pygame.draw.circle(screen, (0, 0, 255), (player_data["x"], player_data["y"]), 10)

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()