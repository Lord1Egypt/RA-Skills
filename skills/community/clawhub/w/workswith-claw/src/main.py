"""
Workswith Claw - FastAPI 应用入口
"""
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from src.api.routes import health, intent, scenes, insights, suggestions, dashboard, apply, devices, semantic, insights_v2 as insights2

app = FastAPI(
    title="Workswith Claw",
    description="具身智能家居中间件",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(intent.router, prefix="/api/v1", tags=["intent"])
app.include_router(scenes.router, prefix="/api/v1", tags=["scenes"])
app.include_router(insights.router, prefix="/api/v1", tags=["insights"])
app.include_router(suggestions.router, prefix="/api/v1", tags=["suggestions"])
app.include_router(dashboard.router, prefix="/api/v1", tags=["dashboard"])
app.include_router(apply.router, prefix="/api/v1", tags=["apply"])
app.include_router(devices.router, prefix="/api/v1", tags=["devices"])
app.include_router(semantic.router, prefix="/api/v1", tags=["semantic"])
app.include_router(insights2.router, prefix="/api/v1", tags=["insights2"])

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return {"name": "Workswith Claw", "version": "0.1.0"}

@app.get("/dashboard")
async def dashboard_page():
    return FileResponse("static/dashboard.html")

@app.get("/debug")
async def debug_page():
    return FileResponse("static/debug.html")
