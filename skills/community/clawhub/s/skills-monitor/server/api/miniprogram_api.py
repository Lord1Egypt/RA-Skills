"""
微信小程序后端 API
==================
- POST /api/mp/login            小程序登录 (code2session)
- GET  /api/mp/agents           获取绑定的 Agent 列表
- GET  /api/mp/dashboard        仪表盘数据
- GET  /api/mp/reports          报告列表
- GET  /api/mp/report/<id>      报告详情
- GET  /api/mp/skills/<agent>   Skill 列表
- POST /api/mp/bind             绑定 Agent
- POST /api/mp/unbind           解绑 Agent
"""

import json
import hashlib
import secrets
from datetime import datetime, date, timedelta
from flask import Blueprint, request, jsonify, session

from server.models.database import db, User, Agent, UserAgent, SkillReport
from server.services.wechat_service import wechat_service
from server.services.report_service import bind_user_agent, get_user_agents

mp_bp = Blueprint("miniprogram_api", __name__, url_prefix="/api/mp")


def _get_current_user():
    """从请求中获取当前用户（通过 session + token 双重验证）"""
    # 从 session 获取用户 ID
    user_id = session.get("mp_user_id")
    if not user_id:
        return None

    # 验证请求中携带的 token 与 session 中一致（防止 session 劫持）
    req_token = request.headers.get("X-MP-Token", "")
    session_token = session.get("mp_token", "")
    if session_token and req_token != session_token:
        return None

    return User.query.get(user_id)


def _require_user(f):
    """装饰器：要求登录"""
    from functools import wraps

    @wraps(f)
    def wrapper(*args, **kwargs):
        user = _get_current_user()
        if not user:
            return jsonify({"error": "请先登录", "code": 401}), 401
        return f(user, *args, **kwargs)

    return wrapper


# ──────── 登录 ────────

@mp_bp.route("/login", methods=["POST"])
def mp_login():
    """
    小程序登录
    Body: {code: "wx_login_code"}
    """
    data = request.get_json(force=True)
    code = data.get("code", "")

    if not code:
        return jsonify({"error": "缺少 code"}), 400

    # 调用微信 code2session
    result = wechat_service.mp_code2session(code)
    openid = result.get("openid")
    session_key = result.get("session_key")

    if not openid:
        return jsonify({"error": "登录失败", "detail": result}), 400

    # 查找或创建用户
    user = User.query.filter_by(mp_openid=openid).first()
    if not user:
        # 检查是否有同 unionid 的公众号用户
        union_id = result.get("unionid")
        if union_id:
            user = User.query.filter_by(union_id=union_id).first()
            if user:
                user.mp_openid = openid

        if not user:
            user = User(
                openid=f"mp_{openid}",  # 区分公众号 openid
                mp_openid=openid,
                union_id=result.get("unionid"),
                subscribe=False,
            )
            db.session.add(user)

        db.session.commit()

    # 设置 session
    session["mp_user_id"] = user.id
    session["mp_session_key"] = session_key

    # 生成自定义 token（用于后续 API 调用）
    custom_token = secrets.token_hex(32)
    session["mp_token"] = custom_token

    return jsonify({
        "ok": True,
        "user": user.to_dict(),
        "token": custom_token,
    })


# ──────── Agent 列表 ────────

@mp_bp.route("/agents", methods=["GET"])
@_require_user
def mp_agents(user):
    """获取用户绑定的 Agent 列表"""
    agents = get_user_agents(user)
    return jsonify({"ok": True, "agents": agents})


# ──────── 仪表盘 ────────

@mp_bp.route("/dashboard", methods=["GET"])
@_require_user
def mp_dashboard(user):
    """仪表盘数据 — 所有 Agent 汇总"""
    bindings = UserAgent.query.filter_by(user_id=user.id).all()

    if not bindings:
        return jsonify({
            "ok": True,
            "has_agents": False,
            "message": "未绑定任何智能体",
        })

    agents_summary = []
    for ua in bindings:
        agent = ua.agent
        if not agent:
            continue

        latest = SkillReport.query.filter_by(
            agent_db_id=agent.id, report_type="daily"
        ).order_by(SkillReport.report_date.desc()).first()

        agents_summary.append({
            "agent_id": agent.agent_id,
            "name": ua.alias or agent.name or f"Agent-{agent.agent_id[:8]}",
            "is_primary": ua.is_primary,
            "health_score": agent.health_score,
            "total_skills": agent.total_skills,
            "runnable_skills": agent.runnable_skills,
            "last_report": latest.to_dict() if latest else None,
        })

    return jsonify({
        "ok": True,
        "has_agents": True,
        "agents": agents_summary,
    })


# ──────── 报告列表 ────────

@mp_bp.route("/reports", methods=["GET"])
@_require_user
def mp_reports(user):
    """获取报告列表"""
    agent_id_str = request.args.get("agent_id", "")
    limit = min(int(request.args.get("limit", "20")), 50)

    # 获取用户有权查看的 Agent
    bindings = UserAgent.query.filter_by(user_id=user.id).all()
    allowed_agent_ids = {ua.agent.agent_id for ua in bindings if ua.agent}

    if agent_id_str and agent_id_str not in allowed_agent_ids:
        return jsonify({"error": "无权查看该 Agent"}), 403

    query = SkillReport.query.filter(
        SkillReport.agent_id_str.in_(allowed_agent_ids if not agent_id_str else [agent_id_str])
    )

    reports = query.order_by(
        SkillReport.report_date.desc()
    ).limit(limit).all()

    return jsonify({
        "ok": True,
        "reports": [r.to_dict() for r in reports],
    })


# ──────── 报告详情 ────────

@mp_bp.route("/report/<int:report_id>", methods=["GET"])
@_require_user
def mp_report_detail(user, report_id):
    """报告详情"""
    report = SkillReport.query.get(report_id)
    if not report:
        return jsonify({"error": "报告不存在"}), 404

    # 验证权限
    bindings = UserAgent.query.filter_by(user_id=user.id).all()
    allowed_agent_ids = {ua.agent.agent_id for ua in bindings if ua.agent}

    if report.agent_id_str not in allowed_agent_ids:
        return jsonify({"error": "无权查看该报告"}), 403

    return jsonify({
        "ok": True,
        "report": report.to_dict(include_data=True),
    })


# ──────── Skill 列表 ────────

@mp_bp.route("/skills/<agent_id_str>", methods=["GET"])
@_require_user
def mp_skills(user, agent_id_str):
    """获取某 Agent 的 Skill 列表"""
    # 验证权限
    bindings = UserAgent.query.filter_by(user_id=user.id).all()
    allowed_agent_ids = {ua.agent.agent_id for ua in bindings if ua.agent}

    if agent_id_str not in allowed_agent_ids:
        return jsonify({"error": "无权查看该 Agent"}), 403

    # 从最新报告中提取 Skill 列表
    agent = Agent.query.filter_by(agent_id=agent_id_str).first()
    if not agent:
        return jsonify({"error": "Agent 不存在"}), 404

    latest = SkillReport.query.filter_by(
        agent_db_id=agent.id, report_type="daily"
    ).order_by(SkillReport.report_date.desc()).first()

    skills = []
    if latest:
        data = latest.get_data()
        scores = data.get("scores", [])
        skills = scores

    return jsonify({
        "ok": True,
        "agent_id": agent_id_str,
        "skills": skills,
    })


# ──────── 绑定/解绑 ────────

@mp_bp.route("/bind", methods=["POST"])
@_require_user
def mp_bind(user):
    """
    绑定 Agent
    Body: {agent_id, token, alias?}
    """
    data = request.get_json(force=True)
    agent_id = data.get("agent_id", "")
    token = data.get("token", "")
    alias = data.get("alias", "")

    if not agent_id or not token:
        return jsonify({"error": "智能体 ID 和 Key 必填"}), 400

    ok, msg = bind_user_agent(user, agent_id, token, alias)

    if ok:
        return jsonify({"ok": True, "message": msg})
    return jsonify({"error": msg}), 400


@mp_bp.route("/unbind", methods=["POST"])
@_require_user
def mp_unbind(user):
    """
    解绑 Agent
    Body: {agent_id}
    """
    data = request.get_json(force=True)
    agent_id_str = data.get("agent_id", "")

    agent = Agent.query.filter_by(agent_id=agent_id_str).first()
    if not agent:
        return jsonify({"error": "Agent 不存在"}), 404

    binding = UserAgent.query.filter_by(user_id=user.id, agent_id=agent.id).first()
    if not binding:
        return jsonify({"error": "未绑定该 Agent"}), 400

    db.session.delete(binding)
    db.session.commit()

    return jsonify({"ok": True, "message": "已解绑"})


# ──────── v0.5.0: 公众号关注状态 + 推送设置 + 操作追踪 ────────

@mp_bp.route("/oa-follow-status", methods=["GET"])
@_require_user
def mp_oa_follow_status(user):
    """
    检查用户是否已关注公众号（通过 unionid 关联）
    GET /api/mp/oa-follow-status
    """
    has_followed = False
    recent_articles = []

    # 通过 unionid 检查是否有公众号关注记录
    if user.union_id:
        oa_user = User.query.filter(
            User.union_id == user.union_id,
            User.subscribe == True,
            User.openid != user.openid,  # 排除自己（小程序 openid）
        ).first()
        has_followed = oa_user is not None
    elif user.subscribe:
        has_followed = True

    return jsonify({
        "ok": True,
        "has_followed": has_followed,
        "recent_articles": recent_articles,
    })


@mp_bp.route("/push-settings", methods=["POST"])
@_require_user
def mp_push_settings(user):
    """
    更新推送设置
    Body: {push_enabled: bool, push_hour?: int}
    """
    data = request.get_json(force=True)

    if "push_enabled" in data:
        user.push_enabled = bool(data["push_enabled"])
    if "push_hour" in data:
        hour = int(data["push_hour"])
        if 0 <= hour <= 23:
            user.push_hour = hour

    db.session.commit()

    return jsonify({
        "ok": True,
        "push_enabled": user.push_enabled,
        "push_hour": user.push_hour,
    })


@mp_bp.route("/track", methods=["POST"])
@_require_user
def mp_track_event(user):
    """
    上报操作追踪事件（小程序端调用）
    Body: {agent_id, event, track_id?, ...}
    """
    data = request.get_json(force=True)
    agent_id = data.get("agent_id", "")
    event = data.get("event", "")

    if not agent_id or not event:
        return jsonify({"error": "agent_id 和 event 必填"}), 400

    try:
        from server.services.operation_tracker import OperationTracker, TrackEvent

        # 校验事件类型
        valid_events = {e.value for e in TrackEvent}
        if event not in valid_events:
            return jsonify({"error": f"无效事件类型: {event}"}), 400

        OperationTracker.track(
            user_id=user.id,
            agent_id=agent_id,
            event=TrackEvent(event),
            data={k: v for k, v in data.items() if k not in ("agent_id", "event")},
        )
        return jsonify({"ok": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@mp_bp.route("/push-analytics", methods=["GET"])
@_require_user
def mp_push_analytics(user):
    """
    获取推送效果分析
    GET /api/mp/push-analytics?days=7
    """
    days = min(int(request.args.get("days", "7")), 30)

    try:
        from server.services.operation_tracker import OperationTracker
        analytics = OperationTracker.get_push_analytics(days=days)
        return jsonify({"ok": True, **analytics})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
