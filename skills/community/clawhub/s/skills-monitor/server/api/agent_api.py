"""
Agent API v0.5.0 — 供本地 Agent 调用的接口
===========================================
- POST /api/agent/register        注册/更新 Agent
- POST /api/agent/heartbeat       心跳
- POST /api/agent/report          上报数据
- GET  /api/agent/reports         查询历史报告
- GET  /api/agent/report/<id>     报告详情
- POST /api/agent/rotate-key      轮换 API Key (v0.5.0)
- POST /api/agent/revoke-key      撤销 API Key (v0.5.0)
- GET  /api/agent/export-data     导出全部数据 (v0.5.0 GDPR)
- POST /api/agent/delete-data     删除全部数据 (v0.5.0 GDPR)
"""

import hashlib
from datetime import datetime
from flask import Blueprint, request, jsonify

from server.models.database import db, Agent
from server.services.report_service import (
    register_agent,
    verify_agent_token,
    process_report_upload,
    get_agent_reports,
    get_report_detail,
)

agent_bp = Blueprint("agent_api", __name__, url_prefix="/api/agent")


def _auth_agent():
    """从请求头中提取并验证 Agent 身份"""
    agent_id = request.headers.get("X-Agent-ID", "")
    token = request.headers.get("X-Agent-Token", "")
    if not agent_id or not token:
        return None, jsonify({"error": "缺少 X-Agent-ID 或 X-Agent-Token"}), 401
    agent = verify_agent_token(agent_id, token)
    if not agent:
        return None, jsonify({"error": "Agent 认证失败"}), 401
    return agent, None, None


# ──────── 注册 / 更新 ────────

@agent_bp.route("/register", methods=["POST"])
def api_register():
    """
    POST /api/agent/register
    Body: {agent_id, token, name?, os_info?, python_version?, monitor_version?, total_skills?, runnable_skills?}
    """
    data = request.get_json(force=True)
    agent_id = data.get("agent_id")
    token = data.get("token")

    if not agent_id or not token:
        return jsonify({"error": "agent_id 和 token 必填"}), 400

    agent = register_agent(
        agent_id=agent_id,
        token=token,
        name=data.get("name"),
        os_info=data.get("os_info"),
        python_version=data.get("python_version"),
        monitor_version=data.get("monitor_version"),
        total_skills=data.get("total_skills"),
        runnable_skills=data.get("runnable_skills"),
    )

    return jsonify({
        "ok": True,
        "agent": agent.to_dict(),
        "message": "注册成功",
    })


# ──────── 心跳 ────────

@agent_bp.route("/heartbeat", methods=["POST"])
def api_heartbeat():
    """
    POST /api/agent/heartbeat
    Headers: X-Agent-ID, X-Agent-Token
    """
    agent, err, code = _auth_agent()
    if err:
        return err, code

    agent.last_heartbeat_at = datetime.utcnow()
    db.session.commit()

    return jsonify({"ok": True, "message": "心跳已记录"})


# ──────── 数据上报 ────────

@agent_bp.route("/report", methods=["POST"])
def api_upload_report():
    """
    POST /api/agent/report
    Headers: X-Agent-ID, X-Agent-Token
    Body: {report_type?, report_date?, data: {...}}
    """
    agent, err, code = _auth_agent()
    if err:
        return err, code

    body = request.get_json(force=True)
    report_data = body.get("data", {})
    report_type = body.get("report_type", "daily")
    report_date_str = body.get("report_date")

    report_date = None
    if report_date_str:
        try:
            from datetime import date as date_cls
            report_date = date_cls.fromisoformat(report_date_str)
        except ValueError:
            pass

    report = process_report_upload(
        agent=agent,
        report_data=report_data,
        report_type=report_type,
        report_date=report_date,
    )

    return jsonify({
        "ok": True,
        "report": report.to_dict(include_data=False),
        "message": "上报成功",
    })


# ──────── 查询历史报告 ────────

@agent_bp.route("/reports", methods=["GET"])
def api_get_reports():
    """
    GET /api/agent/reports?agent_id=xxx&type=daily&limit=30
    Headers: X-Agent-ID, X-Agent-Token
    """
    agent, err, code = _auth_agent()
    if err:
        return err, code

    report_type = request.args.get("type")
    limit = min(int(request.args.get("limit", "30")), 100)

    reports = get_agent_reports(
        agent_id=agent.agent_id,
        report_type=report_type,
        limit=limit,
    )

    return jsonify({"ok": True, "reports": reports, "count": len(reports)})


# ──────── 报告详情 ────────

@agent_bp.route("/report/<int:report_id>", methods=["GET"])
def api_get_report_detail(report_id):
    """
    GET /api/agent/report/<id>
    Headers: X-Agent-ID, X-Agent-Token
    """
    agent, err, code = _auth_agent()
    if err:
        return err, code

    detail = get_report_detail(report_id)
    if not detail:
        return jsonify({"error": "报告不存在"}), 404

    # 验证报告归属
    if detail.get("agent_id") != agent.agent_id:
        return jsonify({"error": "无权访问该报告"}), 403

    return jsonify({"ok": True, "report": detail})


# ──────── v0.5.0: Key 轮换 ────────

@agent_bp.route("/rotate-key", methods=["POST"])
def api_rotate_key():
    """
    POST /api/agent/rotate-key
    Headers: X-Agent-ID, X-Agent-Token
    Body: {new_token_hash: "sha256_of_new_key"}
    """
    agent, err, code = _auth_agent()
    if err:
        return err, code

    body = request.get_json(force=True)
    new_hash = body.get("new_token_hash")
    if not new_hash:
        return jsonify({"error": "需要 new_token_hash 参数"}), 400

    # 更新 token_hash
    old_hash = agent.token_hash
    agent.token_hash = new_hash
    agent.updated_at = datetime.utcnow()
    db.session.commit()

    return jsonify({
        "ok": True,
        "message": "Key 已轮换",
        "old_hash_prefix": old_hash[:8] + "...",
        "new_hash_prefix": new_hash[:8] + "...",
    })


# ──────── v0.5.0: Key 撤销 ────────

@agent_bp.route("/revoke-key", methods=["POST"])
def api_revoke_key():
    """
    POST /api/agent/revoke-key
    Headers: X-Agent-ID, X-Agent-Token
    """
    agent, err, code = _auth_agent()
    if err:
        return err, code

    # 使 token_hash 失效（设为空 hash）
    agent.token_hash = hashlib.sha256(b"__revoked__").hexdigest()
    agent.updated_at = datetime.utcnow()
    db.session.commit()

    return jsonify({"ok": True, "message": "Key 已撤销，Agent 需要重新注册"})


# ──────── v0.5.0: GDPR 数据导出 ────────

@agent_bp.route("/export-data", methods=["GET"])
def api_export_data():
    """
    GET /api/agent/export-data
    Headers: X-Agent-ID, X-Agent-Token
    导出该 Agent 在服务端的全部数据
    """
    agent, err, code = _auth_agent()
    if err:
        return err, code

    from server.models.database import SkillReport, DailyDigest

    # 收集所有报告
    reports = SkillReport.query.filter_by(agent_id_str=agent.agent_id).all()
    reports_data = [r.to_dict(include_data=True) for r in reports]

    # 收集推送记录
    digests = DailyDigest.query.filter_by(agent_db_id=agent.id).all()
    digests_data = []
    for d in digests:
        digests_data.append({
            "digest_date": d.digest_date.isoformat() if d.digest_date else None,
            "push_type": d.push_type,
            "push_status": d.push_status,
            "created_at": d.created_at.isoformat() if d.created_at else None,
        })

    export = {
        "export_version": "1.0",
        "exported_at": datetime.utcnow().isoformat(),
        "agent": agent.to_dict(),
        "reports": reports_data,
        "digests": digests_data,
        "total_reports": len(reports_data),
        "total_digests": len(digests_data),
    }

    return jsonify({"ok": True, "data": export})


# ──────── v0.5.0: GDPR 数据删除 ────────

@agent_bp.route("/delete-data", methods=["POST"])
def api_delete_data():
    """
    POST /api/agent/delete-data
    Headers: X-Agent-ID, X-Agent-Token
    删除该 Agent 在服务端的全部数据（被遗忘权）
    """
    agent, err, code = _auth_agent()
    if err:
        return err, code

    from server.models.database import SkillReport, DailyDigest, UserAgent

    deleted = {}

    # 删除报告
    count = SkillReport.query.filter_by(agent_id_str=agent.agent_id).delete()
    deleted["reports"] = count

    # 删除推送记录
    count = DailyDigest.query.filter_by(agent_db_id=agent.id).delete()
    deleted["digests"] = count

    # 解除用户绑定
    count = UserAgent.query.filter_by(agent_id=agent.id).delete()
    deleted["bindings"] = count

    # 删除 Agent 记录
    db.session.delete(agent)
    db.session.commit()
    deleted["agent"] = 1

    return jsonify({
        "ok": True,
        "message": "全部数据已删除",
        "deleted": deleted,
    })
