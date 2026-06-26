import logging
import uvicorn
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.config import config
from app.webhook import router as webhook_router

# Logging setup
logging.basicConfig(
    level=logging.DEBUG if config.DEBUG else logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup & shutdown events."""
    config.validate()
    logger.info("✅ Webhook-to-Telegram is running")
    logger.info(f"   → Listening on {config.HOST}:{config.PORT}")
    logger.info(f"   → Telegram chat: {config.TELEGRAM_CHAT_ID}")
    yield
    logger.info("🛑 Shutting down...")


app = FastAPI(
    title="Webhook-to-Telegram Signal Router",
    description="Lightweight open-source bridge: forward trading alerts & webhooks to Telegram.",
    version="1.0.0",
    lifespan=lifespan,
)

# Routes
app.include_router(webhook_router, tags=["Webhook"])


@app.get("/", tags=["Health"])
async def root():
    return {"status": "ok", "service": "Webhook-to-Telegram Signal Router"}


@app.get("/health", tags=["Health"])
async def health():
    return JSONResponse({"status": "healthy"})


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=config.HOST,
        port=config.PORT,
        reload=config.DEBUG,
    )
