import asyncio
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.tetris import Game

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")

game = Game()

@app.on_event("startup")
async def start_ticker():
    async def ticker():
        while True:
            await asyncio.sleep(0.45)
            game.tick()
    asyncio.create_task(ticker())

@app.get("/")
async def read_index():
    return FileResponse("app/static/index.html")

@app.get("/state")
async def get_state():
    return game.get_state()

@app.post("/command/{action}")
async def command(action: str):
    if action == "left":
        game.move(-1, 0)
    elif action == "right":
        game.move(1, 0)
    elif action == "down":
        game.move(0, 1)
    elif action == "rotate":
        game.rotate()
    elif action == "drop":
        game.hard_drop()
    elif action == "restart":
        game.reset()
    return game.get_state()
