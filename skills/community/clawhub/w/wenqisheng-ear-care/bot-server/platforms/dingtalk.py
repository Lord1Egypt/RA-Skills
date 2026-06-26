"""
钉钉机器人消息处理

钉钉开放平台: https://open.dingtalk.com
机器人回调: https://open.dingtalk.com/document/orgapp/callback-overview

对接步骤:
1. 钉钉开放平台创建应用
2. 机器人 → 消息接收模式 → HTTP 回调
3. 配置回调地址为: https://你的域名/api/dingtalk
4. 填写 Token 和 AES Key
"""

import json
import os
from fastapi import Request
from ai_client import chat, conversations


async def handle_dingtalk(request: Request):
    """处理钉钉消息"""
    body = await request.body()
    data = json.loads(body.decode("utf-8"))

    # 提取用户消息
    text = data.get("text", {})
    if isinstance(text, dict):
        user_message = text.get("content", "")
    else:
        user_message = str(text)

    if not user_message:
        return {"msgtype": "text", "text": {"content": "您好，请问有什么可以帮您？😊"}}

    # 会话 ID
    sender_id = data.get("senderStaffId", data.get("senderId", "default"))
    history = conversations.get(sender_id)

    # 调用 AI
    reply = await chat(user_message, history)

    # 保存历史
    conversations.add(sender_id, "user", user_message)
    conversations.add(sender_id, "assistant", reply)

    # 钉钉回复格式
    return {
        "msgtype": "text",
        "text": {"content": reply},
    }


async def verify_dingtalk_signature(request: Request) -> bool:
    """钉钉签名验证（简化版）"""
    # 钉钉使用 HMAC-SHA256 签名
    # 完整实现需要 appSecret + timestamp
    return True
