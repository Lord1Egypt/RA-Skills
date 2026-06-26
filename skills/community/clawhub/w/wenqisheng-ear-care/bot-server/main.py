"""
闻其声耳轻松可视采耳 · 多平台 Bot 服务器
=========================================
支持: 飞书 / 钉钉 / 企业微信

启动:
  pip install -r requirements.txt
  cp .env.example .env  # 编辑填好 API Key
  python main.py

部署建议: Railway / 阿里云函数计算 / VPS
"""

import os
import sys
from fastapi import FastAPI, Request, HTTPException
from dotenv import load_dotenv

load_dotenv()

# 添加当前目录到 path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from platforms.feishu import handle_feishu
from platforms.dingtalk import handle_dingtalk
from platforms.wecom import handle_wecom_get, handle_wecom_post
from ai_client import chat, conversations
from skill_loader import get_skill_version

app = FastAPI(
    title="闻其声耳轻松 · Bot Server",
    version="1.0.0",
)


@app.get("/")
def root():
    """根路径"""
    return {
        "service": "协同开发 Bot Server · 多角色任务编排",
        "version": "2.0.0",
        "workflow": "用户 → 审查Bot(调度) → 前端Bot+后端Bot(执行) → 审查Bot(检查) → 用户",
        "endpoints": {
            "feishu": "/api/feishu",
            "feishu_reviewer": "/api/feishu/reviewer",
            "feishu_frontend": "/api/feishu/frontend",
            "feishu_backend": "/api/feishu/backend",
            "dingtalk": "/api/dingtalk",
            "wecom": "/api/wecom",
            "health": "/health",
            "test": "/test?msg=你们几点开门",
        },
    }


@app.get("/health")
def health():
    """健康检查"""
    return {"status": "ok", "data_version": get_skill_version()}


@app.post("/test")
async def test(request: Request):
    """
    测试端点 —— 无需配置任何平台即可验证 AI 回复。
    POST /test  body: {"msg": "你们几点开门？"}
    """
    body = await request.json() if await request.body() else {}
    msg = body.get("msg", "你好")
    reply = await chat(msg)
    return {"reply": reply, "data_version": get_skill_version()}


# ============================================================
# 飞书 — 多角色机器人
# ============================================================

# 默认路由（兼容旧配置，角色为 default）
@app.post("/api/feishu")
async def feishu(request: Request):
    try:
        return await handle_feishu(request)
    except Exception as e:
        return {"code": -1, "msg": str(e)}


# 审查机器人
@app.post("/api/feishu/reviewer")
async def feishu_reviewer(request: Request):
    try:
        return await handle_feishu(request, role="reviewer")
    except Exception as e:
        return {"code": -1, "msg": str(e)}


# 前端机器人
@app.post("/api/feishu/frontend")
async def feishu_frontend(request: Request):
    try:
        return await handle_feishu(request, role="frontend")
    except Exception as e:
        return {"code": -1, "msg": str(e)}


# 后端机器人
@app.post("/api/feishu/backend")
async def feishu_backend(request: Request):
    try:
        return await handle_feishu(request, role="backend")
    except Exception as e:
        return {"code": -1, "msg": str(e)}


# ============================================================
# 钉钉
# ============================================================
@app.post("/api/dingtalk")
async def dingtalk(request: Request):
    try:
        return await handle_dingtalk(request)
    except Exception as e:
        return {"msgtype": "text", "text": {"content": f"系统异常: {e}"}}


# ============================================================
# 企业微信
# ============================================================
@app.get("/api/wecom")
async def wecom_get(request: Request):
    from platforms.wecom import handle_wecom_get
    return await handle_wecom_get(**dict(request.query_params))


@app.post("/api/wecom")
async def wecom_post(request: Request):
    try:
        return await handle_wecom_post(request)
    except Exception as e:
        return "success"


if __name__ == "__main__":
    import uvicorn

    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", "8000"))

    print(f"""
╔══════════════════════════════════════════╗
║  协同开发 Bot Server · 多角色任务编排  ║
╠══════════════════════════════════════════╣
║  工作流: 用户→审查→前端/后端→审查→用户 ║
║  地址: http://{host}:{port:<24}║
╠══════════════════════════════════════════╣
║  审查Bot:  /api/feishu/reviewer        ║
║  前端Bot:  /api/feishu/frontend        ║
║  后端Bot:  /api/feishu/backend         ║
║  测试:     POST /test                  ║
╚══════════════════════════════════════════╝
    """)

    uvicorn.run(app, host=host, port=port)
