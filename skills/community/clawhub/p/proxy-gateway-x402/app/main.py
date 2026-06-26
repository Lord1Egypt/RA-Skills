"""
Proxy Gateway x402 - 主入口
Agent-to-Agent Commerce with automatic USDC payments
"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.proxy import router as proxy_router


def create_app() -> FastAPI:
    """创建 FastAPI 应用"""
    
    app = FastAPI(
        title="Proxy Gateway x402",
        description="HTTP Proxy with x402 automatic payments",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )
    
    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # 注册路由
    app.include_router(proxy_router, prefix="/api/v1")
    
    @app.get("/")
    async def root():
        return {
            "name": "Proxy Gateway x402",
            "version": "0.1.0",
            "protocol": "x402",
            "docs": "/docs"
        }
    
    return app


# 创建应用实例
app = create_app()

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
