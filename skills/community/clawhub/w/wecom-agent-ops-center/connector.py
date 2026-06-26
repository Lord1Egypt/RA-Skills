"""
企微 Agent Connector — 主入口

一键启动：python connector.py

架构：
  企微智能机器人 ←→ WebSocket ←→ ws_client ←→ connector 核心 ←→ agent_bridge ←→ HTTP ←→ 你的 Agent
                                                      ↓
                                              msg_converter (格式转换)
                                                      ↓
                                              状态面板 HTTP :9527
"""

import asyncio
import json
import logging
import signal
import sys
import time
from pathlib import Path

# ============================================================
# 初始化
# ============================================================
from config import load_config, validate_config
from ws_client import WeComWSClient
from agent_bridge import AgentBridge
from msg_converter import standard_to_wecom_reply, standard_to_wecom_card

# 加载配置
config = load_config()

# 日志
log_level = getattr(logging, config.connector.log_level.upper(), logging.INFO)
logging.basicConfig(
    level=log_level,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("connector")

# 组件
ws_client = WeComWSClient(
    bot_id=config.wecom.bot_id,
    bot_secret=config.wecom.bot_secret,
    ws_url=config.wecom.ws_url,
)
agent_bridge = AgentBridge(
    endpoint=config.agent.endpoint,
    timeout=config.agent.timeout,
    retry=config.agent.retry,
)

# 状态
_start_time = time.time()
_shutdown_event = asyncio.Event()

# ============================================================
# 核心逻辑：消息流
# ============================================================

async def on_wecom_message(standard_msg: dict):
    """
    接收企微消息 → 转发 Agent → 获取回复 → 推回企微
    
    这是整个 Connector 的核心数据流：
    企微消息 (JSON) → Agent (HTTP) → 回复 (JSON) → 企微 (WebSocket)
    """
    # 保存原始帧引用（用于被动回复时关联 req_id）
    # 注意：ws_client 里我们已经丢失了原始帧
    # 所以这里用 send_message 主动推送（更通用）
    
    # 转发给 Agent
    reply = await agent_bridge.forward(standard_msg)
    
    if reply is None:
        return  # Agent 无回复，跳过

    # 根据回复类型选择处理方式
    msg_type = reply.get("msg_type", "text")
    chatid = standard_msg.get("from", {}).get("chat_id", "")
    chat_type = 1 if standard_msg.get("from", {}).get("chat_type") == "single" else 2

    if msg_type == "card":
        # 模板卡片
        body = standard_to_wecom_card(reply)
    else:
        # 文本 / Markdown
        body = standard_to_wecom_reply(reply, msg_type="markdown")

    # 主动推送到企微
    if chatid:
        await ws_client.send_message(chatid, body, chat_type=chat_type)
    else:
        logger.warning("chatid 为空，无法推送回复")


# ============================================================
# 状态面板（轻量 HTTP）
# ============================================================

async def status_handler(request):
    """GET / → 状态 JSON"""
    import aiohttp
    from aiohttp import web
    
    uptime = round(time.time() - _start_time)
    return web.json_response({
        "service": "wecom-agent-connector",
        "version": "1.0.0",
        "uptime_seconds": uptime,
        "wecom": ws_client.stats,
        "agent": agent_bridge.stats,
        "p2p": {"enabled": config.p2p.enabled},
    })


async def health_handler(request):
    """GET /health → 健康检查"""
    from aiohttp import web
    
    if ws_client.is_connected and agent_bridge._call_count >= 0:
        return web.json_response({"status": "ok"}, status=200)
    elif ws_client.is_connected:
        return web.json_response({"status": "degraded", "reason": "no agent calls yet"}, status=200)
    else:
        return web.json_response({"status": "unhealthy", "reason": "wecom not connected"}, status=503)


async def start_status_server():
    """启动状态面板 HTTP 服务"""
    from aiohttp import web
    
    app = web.Application()
    app.router.add_get("/", status_handler)
    app.router.add_get("/health", health_handler)
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, config.connector.host, config.connector.port)
    await site.start()
    
    logger.info(f"状态面板: http://{config.connector.host}:{config.connector.port}")
    logger.info(f"健康检查: http://{config.connector.host}:{config.connector.port}/health")
    return runner


# ============================================================
# 主流程
# ============================================================

async def main():
    logger.info("=" * 50)
    logger.info("企微 Agent Connector v1.0.0")
    logger.info("=" * 50)

    # 验证配置
    errors = validate_config(config)
    if errors:
        for e in errors:
            logger.error(f"配置错误: {e}")
        logger.error("请编辑 config.yaml 填写 bot_id 和 bot_secret")
        return

    # 启动状态面板
    status_runner = await start_status_server()

    # 建立企微连接
    connected = await ws_client.connect(on_message=on_wecom_message)
    if not connected:
        logger.error("企微连接失败，退出")
        await status_runner.cleanup()
        return

    logger.info(f"Agent 端点: {config.agent.endpoint}")
    logger.info("✓ 企微 Agent Connector 运行中...")
    logger.info("  按 Ctrl+C 退出")

    # 等待退出信号
    await _shutdown_event.wait()

    # 优雅退出
    logger.info("正在关闭...")
    await ws_client.disconnect()
    await status_runner.cleanup()
    logger.info("已关闭")


def _signal_handler(sig, frame):
    logger.info(f"收到信号 {sig}，准备退出...")
    _shutdown_event.set()


# ============================================================
# 入口
# ============================================================
if __name__ == "__main__":
    signal.signal(signal.SIGTERM, _signal_handler)
    signal.signal(signal.SIGINT, _signal_handler)

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("已退出")
    except Exception as e:
        logger.error(f"致命错误: {e}")
        sys.exit(1)
