# Repository Guidelines

## Rules for AI
- всегда пиши на русском языке
- в разговоре можно шутить и прикалываться

## Project Structure and Module Organization
This repository is a small Python game prototype with a FastAPI server and a Pygame client.
- `WorldOneServer.py` runs the FastAPI WebSocket server and loads the map from `map.json`.
- `WorldOneClient.py` is the Pygame client that connects to the server and renders the map.
- `mapeditor.py` is a Pygame-based map editor for `map.json`.
- `maps/` stores example map data (for example `maps/Proto.json`).
- `NotoEmoji-VariableFont_wght.ttf` is the emoji font used by the client and editor.

## Build, Test, and Development Commands
Run scripts directly with Python from the repo root:
- `pip install -r requirements.txt` installs runtime dependencies, including WebSocket support for Uvicorn.
- `python WorldOneServer.py` starts the WebSocket server at `http://127.0.0.1:8000`.
- `python WorldOneClient.py` starts the Pygame client and connects to `ws://localhost:8000/ws`.
- `python mapeditor.py` opens the map editor for `map.json`.

## Coding Style and Naming Conventions
Follow the current Python style in the repo:
- Use 4-space indentation and keep lines readable.
- Use `snake_case` for functions and variables (examples: `send_move`, `tile_size`).
- Keep script filenames in the existing CamelCase style (examples: `WorldOneServer.py`).
No formatter or linter is configured; keep changes consistent with nearby code.

## Testing Guidelines
There are no automated tests yet. If you add tests, document the framework and provide a single command to run them (for example `pytest`).

## Commit and Pull Request Guidelines
Git history uses short, version-style messages (examples: `0.1.1 WORK`). Keep commit messages concise and consistent with this pattern unless the team agrees on a new convention.
For pull requests, include:
- A short description of the change and affected files.
- Steps to run the server/client or editor when relevant.
- Screenshots or short clips for visible UI changes.

## Configuration and Data Files
`map.json` is the live map consumed by the server and editor. Keep its schema consistent with existing keys (`map_size`, `tile_size`, `tiles`), and update related scripts if the schema changes.
