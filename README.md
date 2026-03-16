# Simple Python Tetris Server

A minimal Tetris game with a web UI and Python server.

## Run

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start server:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```
3. Open http://localhost:8000

## Controls
- Arrow keys to move/rotate
- Space to hard drop
- Buttons for left/right/rotate/down/drop/restart

This is intentionally simple. You can extend it by adding score persistence, next-piece preview panel, sounds, and improved rotation/kick logic.
