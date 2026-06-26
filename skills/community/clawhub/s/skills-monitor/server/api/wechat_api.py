"""
微信公众号回调 API
==================
- GET  /api/wechat/callback    接口验证
- POST /api/wechat/callback    消息/事件接收
"""

import xml.etree.ElementTree as ET
from datetime import datetime
from flask import Blueprint, request, make_response, current_app

from server.models.database import db, User
from server.services.wechat_service import wechat_service
from server.services.report_service import bind_user_agent

wechat_bp = Blueprint("wechat_api", __name__, url_prefix="/api/wechat")


def _xml_response(to_user: str, from_user: str, content: str) -> str:
    """构建文本消息 XML 响应"""
    return f"""<xml>
<ToUserName><![CDATA[{to_user}]]></ToUserName>
<FromUserName><![CDATA[{from_user}]]></FromUserName>
<CreateTime>{int(datetime.now().timestamp())}</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[{content}]]></Content>
</xml>"""


def _get_or_create_user(openid: str) -> User:
    """获取或创建微信用户"""
    user = User.query.filter_by(openid=openid).first()
    if not user:
        user = User(openid=openid, subscribe=True, subscribe_time=datetime.utcnow())
        db.session.add(user)
        db.session.commit()

        # 尝试获取用户信息
        try:
            info = wechat_service.get_user_info(openid)
            if info.get("nickname"):
                user.nickname = info["nickname"]
                user.avatar_url = info.get("headimgurl", "")
                user.union_id = info.get("unionid")
                db.session.commit()
        except Exception:
            pass

    return user


# ──────── 接口验证 ────────

@wechat_bp.route("/callback", methods=["GET"])
def verify():
    """微信接口验证（GET 请求）"""
    signature = request.args.get("signature", "")
    timestamp = request.args.get("timestamp", "")
    nonce = request.args.get("nonce", "")
    echostr = request.args.get("echostr", "")

    if wechat_service.verify_signature(signature, timestamp, nonce):
        return make_response(echostr)
    return make_response("验证失败", 403)


# ──────── 消息/事件接收 ────────

@wechat_bp.route("/callback", methods=["POST"])
def receive():
    """接收微信消息和事件推送"""
    try:
        xml_data = request.data.decode("utf-8")
        root = ET.fromstring(xml_data)

        msg_type = root.findtext("MsgType", "")
        from_user = root.findtext("FromUserName", "")  # 用户 openid
        to_user = root.findtext("ToUserName", "")       # 公众号 ID

        # 事件消息
        if msg_type == "event":
            event = root.findtext("Event", "").lower()
            return _handle_event(event, root, from_user, to_user)

        # 文本消息
        if msg_type == "text":
            content = root.findtext("Content", "").strip()
            return _handle_text(content, from_user, to_user)

        return make_response("success")

    except Exception as e:
        current_app.logger.error(f"微信回调处理异常: {e}")
        return make_response("success")


def _handle_event(event: str, root, from_user: str, to_user: str):
    """处理事件消息"""

    # 关注事件
    if event == "subscribe":
        user = _get_or_create_user(from_user)
        user.subscribe = True
        user.subscribe_time = datetime.utcnow()
        db.session.commit()

        # 带参二维码关注（扫码绑定 Agent）
        event_key = root.findtext("EventKey", "")
        if event_key.startswith("qrscene_bind:"):
            return _handle_bind_scan(event_key.replace("qrscene_", ""), from_user, to_user)

        reply = (
            "🎉 欢迎关注 Skills Monitor！\n\n"
            "我可以帮您：\n"
            "📊 每天推送 Skills 健康报告\n"
            "🔗 绑定您的 Agent 查看详情\n"
            "📱 通过小程序随时查看\n\n"
            "回复「绑定」或点击菜单开始使用"
        )
        resp = make_response(_xml_response(from_user, to_user, reply))
        resp.content_type = "application/xml"
        return resp

    # 取消关注
    if event == "unsubscribe":
        user = User.query.filter_by(openid=from_user).first()
        if user:
            user.subscribe = False
            db.session.commit()
        return make_response("success")

    # 扫码事件（已关注用户扫码）
    if event == "scan":
        event_key = root.findtext("EventKey", "")
        if event_key.startswith("bind:"):
            return _handle_bind_scan(event_key, from_user, to_user)
        return make_response("success")

    # 菜单点击事件
    if event == "click":
        event_key = root.findtext("EventKey", "")
        if event_key == "BIND_AGENT":
            reply = (
                "🔗 绑定 Agent\n\n"
                "请在本地终端运行：\n"
                "  skills-monitor bind --server\n\n"
                "然后扫描终端显示的二维码即可完成绑定。"
            )
            resp = make_response(_xml_response(from_user, to_user, reply))
            resp.content_type = "application/xml"
            return resp

    return make_response("success")


def _handle_bind_scan(event_key: str, from_user: str, to_user: str):
    """处理扫码绑定"""
    # event_key: "bind:{agent_id}:{token_prefix}"
    parts = event_key.split(":")
    if len(parts) >= 3:
        agent_id = parts[1]
        token_prefix = parts[2]

        user = _get_or_create_user(from_user)
        ok, msg = bind_user_agent(user, agent_id, token_prefix)

        if ok:
            reply = f"✅ 绑定成功！\n\nAgent: {agent_id[:8]}...\n\n您将开始收到每日健康报告推送。"
        else:
            reply = f"❌ 绑定失败：{msg}\n\n请确认 Agent ID 和 Token 是否正确。"
    else:
        reply = "❌ 二维码格式无效，请重新生成。"

    resp = make_response(_xml_response(from_user, to_user, reply))
    resp.content_type = "application/xml"
    return resp


def _handle_text(content: str, from_user: str, to_user: str):
    """处理文本消息"""

    # 绑定指令
    if content in ("绑定", "bind", "绑定Agent", "绑定agent"):
        reply = (
            "🔗 绑定 Agent 方法：\n\n"
            "1️⃣ 在终端运行：\n"
            "   skills-monitor bind --server\n\n"
            "2️⃣ 扫描终端显示的二维码\n\n"
            "3️⃣ 绑定成功后即可接收每日推送"
        )
    # 报告指令
    elif content in ("报告", "report", "今日报告"):
        reply = (
            "📊 查看报告：\n\n"
            "• 点击菜单「查看报告」\n"
            "• 或打开小程序查看详情"
        )
    # 帮助指令
    elif content in ("帮助", "help", "?", "？"):
        reply = (
            "📖 Skills Monitor 帮助\n\n"
            "回复以下关键词：\n"
            "  「绑定」— 绑定 Agent\n"
            "  「报告」— 查看今日报告\n"
            "  「帮助」— 显示本帮助\n\n"
            "或点击下方菜单操作 👇"
        )
    else:
        reply = "回复「帮助」查看功能说明 📖"

    resp = make_response(_xml_response(from_user, to_user, reply))
    resp.content_type = "application/xml"
    return resp
