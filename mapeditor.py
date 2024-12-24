import pygame
import json

# Инициализация Pygame
pygame.init()

# Загрузка карты из JSON
with open("map.json", "r", encoding="utf-8") as f:
    map_data = json.load(f)

map_width = map_data["map_size"]["width"]
map_height = map_data["map_size"]["height"]
tile_size = map_data["tile_size"]
tiles = map_data["tiles"]

# Создание окна
screen_width = map_width * tile_size
screen_height = map_height * tile_size
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Редактор карты")

# Шрифты для эмодзи
font = pygame.font.Font("NotoEmoji-VariableFont_wght.ttf", tile_size) # Linux/macOS

# Цвета тайлов
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

# Эмодзи тайлов
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
current_tile_type = "grass" # Текущий выбранный тип тайла

# ... (создание окна - увеличена высота)
screen_height = (map_height + 2) * tile_size
screen = pygame.display.set_mode((screen_width, screen_height))

def fill_map_with_grass(map_data):
    width = map_data["map_size"]["width"]
    height = map_data["map_size"]["height"]
    for y in range(height):
        if y >= len(map_data["tiles"]):
            map_data["tiles"].append(["grass"] * width)
        else:
            for x in range(width):
                if x >= len(map_data["tiles"][y]):
                    map_data["tiles"][y].append("grass")

# ... (основной цикл)
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if mouse_y < map_height * tile_size: # Клик по карте
                tile_x = mouse_x // tile_size
                tile_y = mouse_y // tile_size
                tiles[tile_y][tile_x] = current_tile_type
            else: # Клик по панели
                panel_x = mouse_x // tile_size
                current_tile_type = list(tile_emojis.keys())[panel_x] # Выбор типа тайла

    # Отрисовка карты
    screen.fill((255, 255, 255))
    print(map_height);
    print(map_width);
    for y in range(map_height):
        for x in range(map_width):
            tile_type = tiles[y][x]
            tile_color = tile_colors.get(tile_type, (200, 200, 200))
            pygame.draw.rect(screen, tile_color, (x * tile_size, y * tile_size, tile_size, tile_size))

            emoji = tile_emojis.get(tile_type, "?")
            text_surface = font.render(emoji, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(x * tile_size + tile_size // 2, y * tile_size + tile_size // 2))
            screen.blit(text_surface, text_rect)
    
    #Отрисовка панели
    pygame.draw.rect(screen, (200, 200, 200), (0, map_height * tile_size, screen_width, 2 * tile_size)) # Панель сверху
    x_offset = 0
    for tile_type, emoji in tile_emojis.items():
        text_surface = font.render(emoji, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(x_offset * tile_size + tile_size // 2, (map_height+1) * tile_size ))
        screen.blit(text_surface, text_rect)
        x_offset+=1

    pygame.display.flip()

pygame.quit()