"""
企业微信机器人消息处理

企业微信管理后台: https://work.weixin.qq.com/wework_admin
机器人配置: 应用管理 → 自建应用 → 接收消息

对接步骤:
1. 企业微信管理后台创建自建应用
2. 接收消息 → 设置 API 接收
3. URL: https://你的域名/api/wecom
4. Token 和 EncodingAESKey 填入 .env
"""

import os
import json
from fastapi import Request, Query, HTTPException
from ai_client import chat, conversations

try:
    from defusedxml import ElementTree as ET
except ImportError:
    from xml.etree import ElementTree as ET


def _decrypt_wecom(encrypted: str) -> str:
    """
    企业微信消息解密（简化版）。
    完整实现需要 WXBizMsgCrypt 库处理 AES 解密。
    这里提供框架，实际使用时建议用 wecom-sdk 或 wxwork 库。
    """
    return encrypted  # 占位


async def handle_wecom_get(
    msg_signature: str = Query(...),
    timestamp: str = Query(...),
    nonce: str = Query(...),
    echostr: str = Query(...),
):
    """
    企业微信 URL 验证（GET 请求）。
    首次配置时，企业微信会发送此请求验证 URL 有效性。
    """
    token = os.environ.get("WECOM_TOKEN", "")
    encoding_aes_key = os.environ.get("WECOM_ENCODING_AES_KEY", "")

    if not token or not encoding_aes_key:
        # 未配置时直接返回 echostr
        return int(echostr) if echostr.isdigit() else echostr

    # 完整实现需要验证签名后解密 echostr
    return int(echostr) if echostr.isdigit() else echostr


async def handle_wecom_post(request: Request):
    """处理企业微信消息（POST 请求）"""
    body = await request.body()
    body_str = body.decode("utf-8")

    # 企业微信消息是 XML 格式
    try:
        root = ET.fromstring(body_str)
        msg_type = root.findtext("MsgType", "text")
        user_message = root.findtext("Content", "")
        from_user = root.findtext("FromUserName", "default")
    except ET.ParseError:
        # 也可能是 JSON
        data = json.loads(body_str)
        msg_type = data.get("MsgType", "text")
        user_message = data.get("Content", "")
        from_user = data.get("FromUserName", "default")

    if not user_message or msg_type != "text":
        return "success"

    # 调用 AI
    history = conversations.get(from_user)
    reply = await chat(user_message, history)

    # 保存历史
    conversations.add(from_user, "user", user_message)
    conversations.add(from_user, "assistant", reply)

    # 返回 XML 格式
    xml_response = f"""<xml>
<ToUserName><![CDATA[{from_user}]]></ToUserName>
<FromUserName><![CDATA[wenqisheng]]></FromUserName>
<CreateTime>{int(__import__('time').time())}</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[{reply}]]></Content>
</xml>"""

    return xml_response
