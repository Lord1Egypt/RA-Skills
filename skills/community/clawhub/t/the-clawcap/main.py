"""
The ClawCap (龙虾脑控帽) — FastAPI Web 入口

高保真头像配饰合成引擎
戴上 ClawCap，不是为了自己思考，而是放弃思考。
"""

import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from api.routes import router
from config import GEMINI_API_KEY

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

# 启动时校验 API Key
if not GEMINI_API_KEY:
    logger.error(
        "⚠️  GEMINI_API_KEY 未设置！"
        "请在 .env 文件中配置，或设置环境变量。"
    )

app = FastAPI(
    title="The ClawCap",
    description="龙虾脑控帽 — 高保真头像配饰合成 API",
    version="0.3.0",
)

# 限速：每个 IP 每分钟最多 3 次调用
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS（开发阶段允许所有来源）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(router)

# 挂载静态文件（测试前端）
app.mount("/static", StaticFiles(directory="static"), name="static")

# 根路径跳转到测试页面
from fastapi.responses import RedirectResponse

@app.get("/")
async def root():
    return RedirectResponse(url="/static/index.html")


if __name__ == "__main__":
    import os
    import uvicorn
    dev_mode = os.getenv("DEV", "").lower() in ("1", "true")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=dev_mode)
