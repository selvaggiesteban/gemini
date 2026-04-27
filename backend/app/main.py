
import os
import pty
import fcntl
import asyncio
import subprocess
import select
from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Gemini Cloud IDE")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ROOT_DIR = "/root"

class FilePath(BaseModel):
    path: str

class FileContent(BaseModel):
    path: str
    content: str

def safe_path(req_path: str) -> str:
    target = os.path.abspath(os.path.join(ROOT_DIR, req_path.lstrip('/')))
    if req_path.startswith('/'):
        return os.path.abspath(req_path)
    return target

@app.post("/api/fs/list")
def list_directory(req: FilePath):
    path = safe_path(req.path)
    if not os.path.exists(path) or not os.path.isdir(path):
        raise HTTPException(status_code=404, detail="Directorio no encontrado")
    entries = []
    try:
        for item in os.listdir(path):
            full_path = os.path.join(path, item)
            is_dir = os.path.isdir(full_path)
            entries.append({
                "name": item, "path": full_path, "is_dir": is_dir,
                "size": os.path.getsize(full_path) if not is_dir else 0
            })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    entries.sort(key=lambda x: (not x["is_dir"], x["name"].lower()))
    return {"directory": path, "items": entries}

@app.post("/api/fs/read")
def read_file(req: FilePath):
    path = safe_path(req.path)
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return {"content": f.read()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/fs/write")
def write_file(req: FileContent):
    path = safe_path(req.path)
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(req.content)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.websocket("/ws/gemini")
async def gemini_terminal(websocket: WebSocket):
    await websocket.accept()
    master_fd, slave_fd = pty.openpty()
    p = subprocess.Popen(["bash"], preexec_fn=os.setsid, stdin=slave_fd, stdout=slave_fd, stderr=slave_fd, universal_newlines=True)
    os.close(slave_fd)
    
    async def read_from_pty():
        while p.poll() is None:
            await asyncio.sleep(0.01)
            r, _, _ = select.select([master_fd], [], [], 0)
            if r:
                data = os.read(master_fd, 4096).decode('utf-8', errors='replace')
                await websocket.send_text(data)

    async def read_from_ws():
        try:
            while True:
                data = await websocket.receive_text()
                os.write(master_fd, data.encode('utf-8'))
        except: pass

    await asyncio.gather(read_from_pty(), read_from_ws())

# Static Files
app.mount("/static", StaticFiles(directory="/frontend"), name="static")
@app.get("/")
def serve_ide():
    return FileResponse("/frontend/index.html")
