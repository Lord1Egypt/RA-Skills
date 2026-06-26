"""Unified API Gateway — single entry point for all Agent Memory services.

Combines:
- REST API (v3) — /api/v3/...
- Playground UI — /playground/...
- Health check — /health

Usage:
    python -m agent_memory.unified_api
    # or
    agent-memory serve
"""

import os
import logging

logger = logging.getLogger(__name__)


def create_unified_app(mem=None) -> "FastAPI":
    """Create unified FastAPI application."""
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware

    app = FastAPI(
        title="Agent Memory",
        description="Production-grade memory layer for AI agents",
        version="12.0.0",
    )

    # CORS
    cors_origins = os.environ.get("AGENT_MEMORY_CORS_ORIGINS", "").split(",")
    cors_origins = [o.strip() for o in cors_origins if o.strip()]
    if cors_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=cors_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # Mount v3 API
    try:
        from agent_memory.api_v3 import app as v3_app
        app.mount("/api/v3", v3_app)
    except Exception as e:
        logger.warning("Failed to mount v3 API: %s", e)

    # Mount Playground
    try:
        from agent_memory.playground.app import create_app as create_playground_app
        db_path = mem.db_path if mem else None
        playground_app = create_playground_app(db_path=db_path)
        app.mount("/playground", playground_app)
    except Exception as e:
        logger.warning("Failed to mount Playground: %s", e)

    # Health check at root
    @app.get("/health")
    async def health():
        if mem:
            return mem.health_check()
        return {"status": "ok", "healthy": True}

    @app.get("/")
    async def root():
        return {
            "service": "Agent Memory",
            "version": "12.0.0",
            "endpoints": {
                "api": "/api/v3/docs",
                "playground": "/playground",
                "health": "/health",
            },
        }

    return app


def main():
    """Run unified API server."""
    import uvicorn
    from agent_memory import AgentMemory

    mem = AgentMemory()
    app = create_unified_app(mem)

    host = os.environ.get("AGENT_MEMORY_HOST", "0.0.0.0")
    port = int(os.environ.get("AGENT_MEMORY_PORT", "8000"))

    logger.info("Starting Agent Memory unified API on %s:%d", host, port)
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    main()
