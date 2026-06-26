"""
模拟 Agent — 用于端到端测试 Connector

启动: python test_agent.py
监听: http://localhost:3000/chat

收到的消息会打印到控制台，自动返回确认消息。
"""

import json
import logging
from datetime import datetime
from aiohttp import web

logging.basicConfig(level=logging.INFO, format="%(asctime)s [Agent] %(message)s", datefmt="%H:%M:%S")
logger = logging.getLogger("test-agent")

call_count = 0


async def chat_handler(request):
    global call_count
    body = await request.json()
    call_count += 1

    msg_id = body.get("msg_id", "?")
    user_id = body.get("from", {}).get("user_id", "?")
    content = body.get("content", "")

    logger.info(f"← [{call_count}] from={user_id} | msg={msg_id[:8]}... | {content[:60]}")

    # 模拟处理：直接回确认
    reply = {
        "reply_to": msg_id,
        "content": f"✅ 已收到消息 #{call_count}\n\n"
                   f"你说: _{content[:100]}_\n\n"
                   f"> 这是模拟 Agent 的自动回复。\n"
                   f"> 替换为你的 Agent 端点即可获得真实 AI 回复。",
        "msg_type": "markdown",
    }

    logger.info(f"→ 回复: {reply['content'][:60]}...")
    return web.json_response(reply)


async def health_handler(request):
    return web.json_response({"status": "ok", "calls": call_count})


if __name__ == "__main__":
    app = web.Application()
    app.router.add_post("/chat", chat_handler)
    app.router.add_get("/", health_handler)

    logger.info("=" * 40)
    logger.info("模拟 Agent 启动")
    logger.info("  监听: http://localhost:3000/chat")
    logger.info("  健康: http://localhost:3000/")
    logger.info("=" * 40)

    web.run_app(app, host="0.0.0.0", port=3000)
