"""
消息转换引擎 - 企微消息 ⟷ 标准化 JSON
"""

import json
from datetime import datetime
from typing import Optional


# ============================================================
# 企微 → 标准化 JSON（给 Agent）
# ============================================================

def wecom_to_standard(frame: dict) -> dict:
    """
    将企微智能机器人长连接的消息回调，转换为 Agent 可消费的标准 JSON。
    
    输入（企微 aibot_msg_callback）：
    {
        "cmd": "aibot_msg_callback",
        "headers": {"req_id": "REQ123"},
        "body": {
            "msgid": "MSGID",
            "aibotid": "BOTID",
            "chatid": "CHATID",
            "chattype": "single",
            "from": {"userid": "USERID"},
            "msgtype": "text",
            "text": {"content": "hello"}
        }
    }
    
    输出（标准化 JSON）：
    {
        "msg_id": "MSGID",
        "req_id": "REQ123",
        "from": {
            "user_id": "USERID",
            "chat_id": "CHATID",
            "chat_type": "single"
        },
        "content": "hello",
        "msg_type": "text",
        "timestamp": "2026-05-29T15:00:00",
        "channel": "wecom"
    }
    """
    body = frame.get("body", {})
    headers = frame.get("headers", {})

    msg_id = body.get("msgid", "")
    msg_type = body.get("msgtype", "text")
    chat_type = body.get("chattype", "single")

    # 提取文本内容
    content = ""
    if msg_type == "text":
        content = body.get("text", {}).get("content", "")
    elif msg_type == "mixed":
        # 图文混排：提取所有 text 子项
        items = body.get("mixed", {}).get("msg_item", [])
        content = " ".join(
            item.get("text", {}).get("content", "")
            for item in items
            if item.get("msgtype") == "text"
        )
    elif msg_type == "voice":
        content = body.get("voice", {}).get("content", "[语音消息]")
    elif msg_type == "image":
        content = "[图片消息]"
    elif msg_type == "file":
        filename = body.get("file", {}).get("file_name", "unknown")
        content = f"[文件: {filename}]"
    elif msg_type == "event":
        event_type = body.get("event", {}).get("eventtype", "unknown")
        content = f"[事件: {event_type}]"
    else:
        content = f"[{msg_type} 消息]"

    return {
        "msg_id": msg_id,
        "req_id": headers.get("req_id", ""),
        "from": {
            "user_id": body.get("from", {}).get("userid", ""),
            "chat_id": body.get("chatid", ""),
            "chat_type": chat_type,
        },
        "content": content,
        "msg_type": msg_type,
        "timestamp": datetime.now().isoformat(),
        "channel": "wecom",
    }


# ============================================================
# 标准化 JSON → 企微回复体（给 SDK 的 reply/send_message）
# ============================================================

def standard_to_wecom_reply(reply: dict, msg_type: str = "markdown") -> dict:
    """
    将 Agent 的标准 JSON 回复，转换为企微 SDK 可用的回复体。
    
    输入（Agent 返回）：
    {"reply_to": "MSGID", "content": "订单 1288 已发货", "msg_type": "text"}
    
    输出（企微回复体）：
    {"msgtype": "markdown", "markdown": {"content": "订单 1288 已发货"}}
    """
    content = reply.get("content", "")

    if msg_type == "markdown":
        return {
            "msgtype": "markdown",
            "markdown": {"content": content},
        }
    elif msg_type == "text":
        return {
            "msgtype": "text",
            "text": {"content": content},
        }
    else:
        return {
            "msgtype": "markdown",
            "markdown": {"content": content},
        }


def standard_to_wecom_card(card_data: dict) -> dict:
    """
    将 Agent 的卡片数据转为企微模板卡片格式。
    
    Agent 返回：
    {
        "reply_to": "MSGID",
        "msg_type": "card",
        "card": {
            "title": "供应商A报价",
            "content": "XX-500个: ¥6,250\n交期: 6月10日",
            "buttons": [
                {"text": "确认下单", "key": "confirm_order", "style": 1},
                {"text": "再询价", "key": "requote", "style": 0}
            ]
        }
    }
    """
    card = card_data.get("card", {})
    buttons = card.get("buttons", [])
    
    return {
        "msgtype": "template_card",
        "template_card": {
            "card_type": "text_notice",
            "main_title": {"title": card.get("title", "通知")},
            "emphasis_content": {"title": card.get("emphasis", card.get("content", ""))},
            "sub_title_text": card.get("subtitle", ""),
            "horizontal_content_list": [
                {"keyname": key, "value": value}
                for key, value in card.get("fields", {}).items()
            ],
        },
    }
