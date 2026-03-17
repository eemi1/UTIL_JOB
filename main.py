from fastapi import FastAPI
from services.osint import enrich_content
from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/resources", StaticFiles(directory="resources"), name="resources")

templates = Jinja2Templates(directory="templates")

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "restaurants": []}
    )

@app.post("/restaurants")
async def restaurants(request: Request):
    body = await request.json()
    search = body.get("search", "")
    
    data = await enrich_content(search)
    
    # Limpiar markdown wrapper si existe
    if data.strip().startswith("```"):
        lines = data.strip().split("\n")
        data = "\n".join(lines[1:-1])  # Quitar ```json y ```
    
    restaurants = json.loads(data)
    
    return restaurants