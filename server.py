from fastapi import FastAPI,WebSocket, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import os
import asyncio
import random
import logging

app = FastAPI()
logger = logging.getLogger(__name__)
FILE = "test.log"

template = Jinja2Templates(directory="./")

@app.get("/logs/")
async def home(request:Request):
    return template.TemplateResponse(request=request,name="index.html")

@app.websocket("/logs/")
async def logs(websocket:WebSocket):
    await websocket.accept()
    N=10
    file_size = os.stat(FILE).st_size
    buff_size = 8192
    iter = 0
    with open(FILE) as f:
        while True:
            if buff_size > file_size:
                fetched_lines = []
                while True:
                    buff_size = file_size-1
                    iter+=1
                    f.seek(file_size-buff_size*iter) # keep on seeking further above
                    fetched_lines.extend(f.readlines()) #extending the last lines into it
                    if len(fetched_lines)>N or f.tell()==0:
                        for i in fetched_lines[-N:]:
                            await websocket.send_text(i)
                        break
          
            line = f.readline()
            while not line:  # until and unless we get a new line
                await asyncio.sleep(random.random()*2)
                line = f.readline()
            await websocket.send_text(line)
