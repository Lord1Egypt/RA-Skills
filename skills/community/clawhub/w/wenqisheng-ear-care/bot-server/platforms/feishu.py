"""
飞书（Lark）多角色协同机器人 — 任务编排模式

工作流: 用户 → 审查Bot(调度) → 前端Bot+后端Bot(执行) → 审查Bot(检查) → 用户

飞书开放平台: https://open.feishu.cn

部署步骤:
1. 创建 3 个飞书企业自建应用，分别开启「机器人」能力
2. 重要: 3 个应用的机器人设置中，requireMention 设为 false（接收群内所有消息）
3. 每个应用的事件订阅 → 添加「接收消息」事件
4. 分别配置请求地址:
   - 审查Bot: https://你的域名/api/feishu/reviewer
   - 前端Bot: https://你的域名/api/feishu/frontend
   - 后端Bot: https://你的域名/api/feishu/backend
5. .env 中配置各应用的 App ID / Secret
"""

import json
import hashlib
import os
import re
from fastapi import Request
from ai_client import chat_with_role, conversations

ROLE_LABELS = {
    "reviewer": "审查Bot",
    "frontend": "前端Bot",
    "backend": "后端Bot",
    "default": "Bot",
}

ROLE_CREDENTIALS = {
    "reviewer": {
        "app_id": os.environ.get("FEISHU_REVIEWER_APP_ID", os.environ.get("FEISHU_APP_ID", "")),
        "app_secret": os.environ.get("FEISHU_REVIEWER_APP_SECRET", os.environ.get("FEISHU_APP_SECRET", "")),
    },
    "frontend": {
        "app_id": os.environ.get("FEISHU_FRONTEND_APP_ID", os.environ.get("FEISHU_APP_ID", "")),
        "app_secret": os.environ.get("FEISHU_FRONTEND_APP_SECRET", os.environ.get("FEISHU_APP_SECRET", "")),
    },
    "backend": {
        "app_id": os.environ.get("FEISHU_BACKEND_APP_ID", os.environ.get("FEISHU_APP_ID", "")),
        "app_secret": os.environ.get("FEISHU_BACKEND_APP_SECRET", os.environ.get("FEISHU_APP_SECRET", "")),
    },
    "default": {
        "app_id": os.environ.get("FEISHU_APP_ID", ""),
        "app_secret": os.environ.get("FEISHU_APP_SECRET", ""),
    },
}


def _get_credentials(role: str) -> dict:
    creds = ROLE_CREDENTIALS.get(role, ROLE_CREDENTIALS["default"])
    if not creds["app_secret"]:
        creds = ROLE_CREDENTIALS["default"]
    return creds


def _is_mentioned(label: str, message: str) -> bool:
    """检测 Bot 是否在消息中被 @提及。

    飞书 @mention 在消息文本中有两种格式:
    - <at user_id="xxx">BotName</at>  (用户 @ 了机器人)
    - @BotName (纯文本，如审查Bot 派发任务时写的)
    """
    # Feishu <at> tag format
    if f"<at" in message and f">{label}</at>" in message:
        return True
    # Plain text @mention
    if f"@{label}" in message:
        return True
    return False


def _should_respond(role: str, label: str, message: str, sender_open_id: str) -> bool:
    """判断当前 Bot 是否应该响应这条消息。

    规则:
    - 被 @提及 → 一定响应
    - 审查Bot → 当消息中含「完成/请检查/请审查/done」时响应（开发者汇报）
    - 其余消息不响应（群内闲聊、其他 Bot 的对话等）
    """
    if _is_mentioned(label, message):
        return True

    # 审查Bot: 监听开发者的完成汇报
    if role == "reviewer":
        report_keywords = ["请检查", "请审查", "任务完成", "已完成", "done", "review"]
        if any(kw in message.lower() for kw in report_keywords):
            # 确认不是审查Bot 自己发的（自己的消息里可能也有这些词）
            if not _is_mentioned(label, message):
                return True

    return False


async def verify_signature(request: Request, role: str = "default") -> bool:
    """飞书请求签名验证"""
    timestamp = request.headers.get("X-Lark-Request-Timestamp", "")
    nonce = request.headers.get("X-Lark-Request-Nonce", "")
    signature = request.headers.get("X-Lark-Signature", "")

    app_secret = _get_credentials(role)["app_secret"]
    if not app_secret:
        return True

    body = await request.body()
    body_str = body.decode("utf-8")
    sign_str = f"{timestamp}{nonce}{app_secret}{body_str}"
    return signature == hashlib.sha256(sign_str.encode()).hexdigest()


async def handle_feishu(request: Request, role: str = "default"):
    """处理飞书消息。

    协同关键:
    - 所有机器人共享同一 chat_id 的对话历史
    - 非 @当前Bot 的消息也存入历史（被动感知群内所有内容）
    - assistant 消息打上 [BotName] 标签，方便区分来源
    """
    body = await request.body()
    data = json.loads(body.decode("utf-8"))

    if data.get("type") == "url_verification":
        return {"challenge": data.get("challenge", "")}

    if data.get("type") != "event_callback":
        return {"code": 0}

    event = data.get("event", {})
    msg_type = event.get("message", {}).get("message_type", "")

    if msg_type != "text":
        return {"code": 0}

    # 解析消息内容
    text = event.get("message", {}).get("content", "{}")
    try:
        text_data = json.loads(text)
        user_message = text_data.get("text", "")
    except json.JSONDecodeError:
        user_message = text

    if not user_message:
        return {"code": 0}

    chat_id = event.get("message", {}).get("chat_id", "default")
    sender_id = event.get("sender", {}).get("sender_id", "")
    label = ROLE_LABELS.get(role, "Bot")

    # 始终记录到共享对话历史（无论是否响应）
    conversations.add(chat_id, "user", user_message)

    # 判断是否应该响应
    if not _should_respond(role, label, user_message, sender_id):
        return {"code": 0}

    # 获取共享对话历史（包含所有 Bot 的往来消息）
    history = conversations.get(chat_id)

    # 调用 Claude，注入角色 system prompt
    reply = await chat_with_role(user_message, role, history)

    # 回复打上 bot 标签存入共享历史
    conversations.add(chat_id, "assistant", f"[{label}] {reply}")

    return {
        "code": 0,
        "reply": reply,
        "reply_type": "text",
    }


async def send_feishu_message(chat_id: str, content: str, role: str = "default"):
    """通过飞书 API 主动发送消息到群聊（非事件回复）"""
    import httpx

    creds = _get_credentials(role)

    async with httpx.AsyncClient() as client:
        token_resp = await client.post(
            "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
            json={"app_id": creds["app_id"], "app_secret": creds["app_secret"]},
        )
        token = token_resp.json().get("tenant_access_token", "")

        await client.post(
            f"https://open.feishu.cn/open-apis/im/v1/messages/{chat_id}/reply",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "content": json.dumps({"text": content}),
                "msg_type": "text",
            },
        )
