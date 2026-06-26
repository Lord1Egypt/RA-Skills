"""
H5 报告页 API — 供微信公众号 H5 页面使用
=========================================
- GET  /h5/dashboard                  仪表盘（重定向到主 Agent 报告）
- GET  /h5/report/<agent_id>          某 Agent 最新报告页
- GET  /h5/report/<agent_id>/<date>   指定日期报告
- GET  /h5/agents                     Agent 列表页
- GET  /h5/settings                   推送设置页
- GET  /api/h5/trend/<agent_id>       趋势数据 JSON
"""

from datetime import date, timedelta
from flask import Blueprint, request, render_template, jsonify

from server.models.database import db, User, Agent, UserAgent, SkillReport

h5_bp = Blueprint("h5_api", __name__)


def _get_user_by_openid(openid: str):
    """通过 openid 获取用户"""
    if not openid:
        return None
    return User.query.filter_by(openid=openid).first()


def _build_h5_context(agent: Agent, report_date: str = None) -> dict:
    daily_query = SkillReport.query.filter_by(agent_db_id=agent.id, report_type="daily")
    if report_date:
        try:
            target_day = date.fromisoformat(report_date)
            daily_query = daily_query.filter_by(report_date=target_day)
        except ValueError:
            pass

    selected_daily = daily_query.order_by(SkillReport.report_date.desc(), SkillReport.created_at.desc()).first()
    latest_daily = SkillReport.query.filter_by(
        agent_db_id=agent.id, report_type="daily"
    ).order_by(SkillReport.report_date.desc(), SkillReport.created_at.desc()).first()
    latest_diag = SkillReport.query.filter_by(
        agent_db_id=agent.id, report_type="diagnostic"
    ).order_by(SkillReport.report_date.desc(), SkillReport.created_at.desc()).first()
    first_diag = SkillReport.query.filter_by(
        agent_db_id=agent.id, report_type="diagnostic"
    ).order_by(SkillReport.report_date.asc(), SkillReport.created_at.asc()).first()

    report = selected_daily or latest_diag
    report_data = report.get_data() if report else {}
    latest_daily_data = latest_daily.get_data() if latest_daily else {}
    latest_diag_data = latest_diag.get_data() if latest_diag else {}
    first_diag_data = first_diag.get_data() if first_diag else {}

    preferred_payload = report_data or latest_daily_data or latest_diag_data
    recommendations = preferred_payload.get("recommendations") or latest_diag_data.get("recommendations", [])
    installed_skills = preferred_payload.get("installed_skills") or latest_diag_data.get("installed_skills", [])
    diagnostic_payload = report_data.get("diagnostics") or latest_diag_data.get("diagnostics") or {}

    daily_reports = SkillReport.query.filter_by(agent_db_id=agent.id, report_type="daily").all()
    diag_reports = SkillReport.query.filter_by(agent_db_id=agent.id, report_type="diagnostic").all()
    end_date = date.today()
    recent_daily_count = sum(1 for r in daily_reports if r.report_date and r.report_date >= end_date - timedelta(days=6))

    sync_status = {
        "daily_count": len(daily_reports),
        "diagnostic_count": len(diag_reports),
        "recent_daily_count": recent_daily_count,
        "has_initial_diagnostic": bool(first_diag),
        "latest_daily_date": latest_daily.report_date.isoformat() if latest_daily and latest_daily.report_date else "",
        "latest_diag_date": latest_diag.report_date.isoformat() if latest_diag and latest_diag.report_date else "",
        "first_diagnostic_date": first_diag.report_date.isoformat() if first_diag and first_diag.report_date else "",
        "status": "healthy" if first_diag and recent_daily_count >= 5 else ("warning" if daily_reports or diag_reports else "empty"),
        "status_label": "同步正常" if first_diag and recent_daily_count >= 5 else ("待补齐" if daily_reports or diag_reports else "未开始"),
    }

    return {
        "report": report,
        "report_data": report_data,
        "latest_daily": latest_daily,
        "latest_daily_data": latest_daily_data,
        "latest_diag": latest_diag,
        "latest_diag_data": latest_diag_data,
        "first_diag": first_diag,
        "first_diag_data": first_diag_data,
        "recommendations": recommendations,
        "installed_skills": installed_skills,
        "diagnostic_payload": diagnostic_payload,
        "sync_status": sync_status,
        "trend": _get_trend_data(agent.id, 7),
    }


@h5_bp.route("/h5/dashboard")
def h5_dashboard():
    """仪表盘入口 — 展示用户主 Agent 的最新报告"""
    openid = request.args.get("openid", "")
    user = _get_user_by_openid(openid)

    if not user:
        return render_template("h5_bind_guide.html")

    primary = UserAgent.query.filter_by(user_id=user.id, is_primary=True).first()
    if not primary:
        primary = UserAgent.query.filter_by(user_id=user.id).first()

    if not primary or not primary.agent:
        return render_template("h5_bind_guide.html")

    agent = primary.agent
    ctx = _build_h5_context(agent)
    return render_template("h5_report.html", agent=agent, user=user, **ctx)


@h5_bp.route("/h5/report/<agent_id_str>")
@h5_bp.route("/h5/report/<agent_id_str>/<report_date>")
def h5_report(agent_id_str, report_date=None):
    """指定 Agent / 日期的报告页（需要验证用户对该 Agent 的绑定关系）"""
    openid = request.args.get("openid", "")
    user = _get_user_by_openid(openid)
    if not user:
        return render_template("h5_error.html", message="请先登录"), 403

    agent = Agent.query.filter_by(agent_id=agent_id_str).first()
    if not agent:
        return render_template("h5_error.html", message="智能体不存在"), 404

    binding = UserAgent.query.filter_by(user_id=user.id, agent_id=agent.id).first()
    if not binding:
        return render_template("h5_error.html", message="您未绑定该智能体，无权查看"), 403

    ctx = _build_h5_context(agent, report_date)
    return render_template("h5_report.html", agent=agent, user=user, **ctx)


@h5_bp.route("/h5/agents")
def h5_agents():
    """Agent 列表页"""
    openid = request.args.get("openid", "")
    user = _get_user_by_openid(openid)
    if not user:
        return render_template("h5_bind_guide.html")

    bindings = UserAgent.query.filter_by(user_id=user.id).all()
    agents_data = []
    for ua in bindings:
        if ua.agent:
            agents_data.append({
                "agent": ua.agent,
                "alias": ua.alias,
                "is_primary": ua.is_primary,
            })

    return render_template("h5_agents.html", agents=agents_data, user=user)


@h5_bp.route("/h5/settings")
def h5_settings():
    """推送设置页"""
    openid = request.args.get("openid", "")
    user = _get_user_by_openid(openid)
    if not user:
        return render_template("h5_bind_guide.html")

    return render_template("h5_settings.html", user=user)


@h5_bp.route("/api/h5/trend/<agent_id_str>")
def api_trend(agent_id_str):
    """获取 Agent 趋势数据（需验证用户权限）"""
    openid = request.args.get("openid", "")
    user = _get_user_by_openid(openid)
    if not user:
        return jsonify({"error": "请先登录"}), 403

    agent = Agent.query.filter_by(agent_id=agent_id_str).first()
    if not agent:
        return jsonify({"error": "智能体不存在"}), 404

    binding = UserAgent.query.filter_by(user_id=user.id, agent_id=agent.id).first()
    if not binding:
        return jsonify({"error": "无权查看该智能体数据"}), 403

    days = min(int(request.args.get("days", "30")), 90)
    trend = _get_trend_data(agent.id, days)
    return jsonify({"ok": True, "trend": trend})


@h5_bp.route("/api/h5/settings", methods=["POST"])
def api_update_settings():
    """更新推送设置"""
    data = request.get_json(force=True)
    openid = data.get("openid", "")
    user = _get_user_by_openid(openid)
    if not user:
        return jsonify({"error": "用户不存在"}), 404

    if "push_enabled" in data:
        user.push_enabled = bool(data["push_enabled"])
    if "push_hour" in data:
        user.push_hour = max(0, min(23, int(data["push_hour"])))

    db.session.commit()
    return jsonify({"ok": True, "user": user.to_dict()})


def _get_trend_data(agent_db_id: int, days: int = 7) -> list:
    """获取趋势数据"""
    end_date = date.today()
    start_date = end_date - timedelta(days=days - 1)

    reports = SkillReport.query.filter(
        SkillReport.agent_db_id == agent_db_id,
        SkillReport.report_type == "daily",
        SkillReport.report_date >= start_date,
        SkillReport.report_date <= end_date,
    ).order_by(SkillReport.report_date.asc()).all()

    return [
        {
            "date": r.report_date.isoformat(),
            "health_score": r.health_score,
            "total_runs": r.total_runs,
            "success_rate": r.success_rate,
            "active_skills": r.active_skills,
        }
        for r in reports
    ]
