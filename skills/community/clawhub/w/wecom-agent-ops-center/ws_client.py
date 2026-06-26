"""
WebSocket 客户端封装 - 基于 wecom-aibot-sdk，管理企微长连接生命周期

职责：
1. 建立/维持/重建企微 WebSocket 连接
2. 接收消息回调 → 转为标准化 JSON → 调用 on_message_handler
3. 回复消息、主动推送消息
4. 心跳监控和状态上报
"""

import asyncio
import logging
from typing import Callable, Optional, Awaitable

logger = logging.getLogger("wecom.connector")

# 消息处理器类型：async func(standard_msg: dict) -> None
MessageHandler = Callable[[dict], Awaitable[None]]


class WeComWSClient:
    """企微智能机器人 WebSocket 客户端"""

    def __init__(self, bot_id: str, bot_secret: str, ws_url: str = "wss://openws.work.weixin.qq.com"):
        self.bot_id = bot_id
        self.bot_secret = bot_secret
        self.ws_url = ws_url
        
        self._client = None          # wecom-aibot-sdk WSClient 实例
        self._handler: Optional[MessageHandler] = None
        self._connected = False
        self._last_message_time: Optional[float] = None
        self._message_count: int = 0
        self._error_count: int = 0

    # ----------------------------------------------------------
    # 公开属性
    # ----------------------------------------------------------
    @property
    def is_connected(self) -> bool:
        return self._connected and self._client is not None and self._client.is_connected

    @property
    def stats(self) -> dict:
        return {
            "connected": self.is_connected,
            "message_count": self._message_count,
            "error_count": self._error_count,
            "last_message_time": self._last_message_time,
            "bot_id": self.bot_id[:8] + "..." if len(self.bot_id) > 8 else self.bot_id,
        }

    # ----------------------------------------------------------
    # 连接管理
    # ----------------------------------------------------------
    async def connect(self, on_message: MessageHandler) -> bool:
        """
        建立企微 WebSocket 连接。
        
        Args:
            on_message: 消息回调，接收标准化 JSON dict
        
        Returns:
            True = 连接成功
        """
        self._handler = on_message

        try:
            from wecom_aibot_sdk import WSClient

            self._client = WSClient(
                botid=self.bot_id,
                secret=self.bot_secret,
                ws_url=self.ws_url,
            )

            # 注册消息回调
            self._client.on("message", self._on_raw_message)
            self._client.on("error", self._on_error)
            self._client.on("close", self._on_close)

            await self._client.connect()
            self._connected = True
            logger.info(f"企微 WebSocket 已连接 | bot={self.bot_id[:8]}...")
            return True

        except ImportError:
            logger.error("wecom_aibot_sdk 未安装，请运行: pip install wecom-aibot-sdk")
            return False
        except Exception as e:
            self._connected = False
            logger.error(f"企微连接失败: {e}")
            return False

    async def disconnect(self):
        """主动断开连接"""
        self._connected = False
        if self._client:
            try:
                await self._client.disconnect()
            except Exception:
                pass
            self._client = None
        logger.info("企微 WebSocket 已断开")

    # ----------------------------------------------------------
    # 消息处理（内部）
    # ----------------------------------------------------------
    async def _on_raw_message(self, frame: dict):
        """接收企微原始回调 → 转为标准化 JSON → 调用外部 handler"""
        from msg_converter import wecom_to_standard

        # 只处理消息回调，忽略事件
        cmd = frame.get("cmd", "")
        if cmd != "aibot_msg_callback":
            return

        import time
        self._message_count += 1
        self._last_message_time = time.time()

        standard_msg = wecom_to_standard(frame)
        user_id = standard_msg.get("from", {}).get("user_id", "?")
        content_preview = standard_msg.get("content", "")[:50]

        logger.info(f"← 消息 | from={user_id} | {content_preview}")

        if self._handler:
            try:
                await self._handler(standard_msg)
            except Exception as e:
                logger.error(f"消息处理异常: {e}")

    async def _on_error(self, error):
        self._error_count += 1
        logger.error(f"WebSocket 错误: {error}")

    async def _on_close(self, reason):
        self._connected = False
        logger.warning(f"WebSocket 关闭: {reason}")

    # ----------------------------------------------------------
    # 消息发送
    # ----------------------------------------------------------
    async def reply(self, frame: dict, body: dict):
        """
        被动回复（必须在收到消息的上下文中调用）
        
        Args:
            frame: 原始企微回调帧（用于关联 req_id）
            body: 回复体（msg_converter.standard_to_wecom_reply 输出）
        """
        if not self._client or not self.is_connected:
            logger.warning("无法回复：未连接")
            return False

        try:
            await self._client.reply(frame, body)
            logger.info(f"→ 已回复")
            return True
        except Exception as e:
            logger.error(f"回复失败: {e}")
            return False

    async def send_message(self, chatid: str, body: dict, chat_type: int = 1):
        """
        主动推送消息（不依赖回调帧）
        
        Args:
            chatid: 会话 ID
            body: 消息体
            chat_type: 1=单聊, 2=群聊
        """
        if not self._client or not self.is_connected:
            logger.warning("无法推送：未连接")
            return False

        try:
            await self._client.send_message(chatid, body, chat_type=chat_type)
            logger.info(f"→ 已推送 | chatid={chatid[:8]}...")
            return True
        except Exception as e:
            logger.error(f"推送失败: {e}")
            return False
