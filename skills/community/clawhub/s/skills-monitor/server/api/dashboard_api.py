"""
后台分析仪表盘 API — 提供汇总分析数据
======================================
- GET  /dashboard/<agent_id>             仪表盘主页
- GET  /api/dashboard/<agent_id>/data    仪表盘 JSON 数据
"""

from datetime import date, datetime, timedelta
from collections import Counter
from flask import Blueprint, request, render_template, jsonify

from server.models.database import Agent, SkillReport
from server.config import DASHBOARD_TOKEN

dashboard_bp = Blueprint("dashboard_api", __name__)


def _require_dashboard_token() -> bool:
    """
    若配置了 SM_DASHBOARD_TOKEN，则要求请求携带 token：
      - Header: X-Dashboard-Token
      - Query:  ?token=...
    """
    if not DASHBOARD_TOKEN:
        return True
    token = request.headers.get("X-Dashboard-Token", "") or request.args.get("token", "")
    return bool(token) and token == DASHBOARD_TOKEN


def _extract_raw_factors(score_payload: dict) -> dict:
    raw = score_payload.get("raw_factors")
    if isinstance(raw, dict) and raw:
        return raw

    factors = score_payload.get("factors", {})
    if isinstance(factors, dict) and factors:
        if all(not isinstance(v, dict) for v in factors.values()):
            return factors
    return {}


def _collect_dashboard_data(agent: Agent, days: int = 30) -> dict:
    """汇总 Agent 的所有分析数据，供仪表盘使用"""
    end_date = date.today()
    start_date = end_date - timedelta(days=days - 1)

    all_reports = SkillReport.query.filter(
        SkillReport.agent_db_id == agent.id,
    ).order_by(SkillReport.report_date.desc(), SkillReport.created_at.desc()).all()

    daily_reports = [r for r in all_reports if r.report_type == "daily"]
    diag_reports = [r for r in all_reports if r.report_type == "diagnostic"]

    latest_daily = daily_reports[0] if daily_reports else None
    latest_diag = diag_reports[0] if diag_reports else None
    first_diag = diag_reports[-1] if diag_reports else None

    latest_data = latest_daily.get_data() if latest_daily else {}
    latest_diag_data = latest_diag.get_data() if latest_diag else {}
    first_diag_data = first_diag.get_data() if first_diag else {}

    preferred_payload = latest_data or latest_diag_data
    overview = preferred_payload.get("overview", {})
    recommendations = preferred_payload.get("recommendations") or latest_diag_data.get("recommendations", [])
    installed_skills = preferred_payload.get("installed_skills") or latest_diag_data.get("installed_skills", [])
    installed_map = {
        item.get("slug"): item for item in installed_skills
        if isinstance(item, dict) and item.get("slug")
    }

    overview_metrics = {
        "health_score": latest_daily.health_score if latest_daily else (latest_diag.health_score if latest_diag else (agent.health_score or 0)),
        "total_installed": overview.get("total_installed", agent.total_skills or 0),
        "total_runnable": overview.get("total_runnable", agent.runnable_skills or 0),
        "total_runs": overview.get("total_runs", latest_daily.total_runs if latest_daily else 0),
        "success_rate": overview.get("success_rate", latest_daily.success_rate if latest_daily else 0),
        "active_skills": overview.get("active_skills", latest_daily.active_skills if latest_daily else 0),
        "avg_duration_ms": overview.get("avg_duration_ms", 0),
        "total_reports": len(all_reports),
        "last_report_at": agent.last_report_at.strftime("%Y-%m-%d %H:%M") if agent.last_report_at else "未上报",
    }

    total = overview_metrics["total_installed"]
    runnable = overview_metrics["total_runnable"]
    overview_metrics["runnable_rate"] = round(runnable / total * 100, 1) if total > 0 else 0

    range_reports = SkillReport.query.filter(
        SkillReport.agent_db_id == agent.id,
        SkillReport.report_type == "daily",
        SkillReport.report_date >= start_date,
        SkillReport.report_date <= end_date,
    ).order_by(SkillReport.report_date.asc()).all()

    trend_data = []
    for report in range_reports:
        trend_data.append({
            "date": report.report_date.isoformat(),
            "health_score": report.health_score or 0,
            "total_runs": report.total_runs or 0,
            "success_rate": report.success_rate or 0,
            "active_skills": report.active_skills or 0,
            "avg_duration_ms": report.avg_duration_ms or 0,
        })

    scores = preferred_payload.get("scores", [])
    skill_rankings = []
    grade_distribution = Counter()
    score_distribution = {"excellent": 0, "good": 0, "average": 0, "poor": 0}

    for score in scores:
        grade = score.get("grade", "C")
        grade_distribution[grade] += 1
        raw_factors = _extract_raw_factors(score)
        skill_id = score.get("skill_id", "unknown")
        inventory = installed_map.get(skill_id, {})
        skill_rankings.append({
            "skill_id": skill_id,
            "skill_name": inventory.get("name", skill_id),
            "category": inventory.get("category", "未分类"),
            "description": inventory.get("description", ""),
            "total_score": score.get("total_score", 0),
            "grade": grade,
            "grade_label": score.get("grade_label", grade),
            "success_rate": raw_factors.get("success_rate"),
            "response_time": raw_factors.get("response_time"),
            "satisfaction": raw_factors.get("satisfaction"),
            "stability": raw_factors.get("stability"),
            "raw_factors": raw_factors,
            "factor_cards": score.get("factors", {}),
            "details": score.get("details", {}),
        })

        total_score = score.get("total_score", 0)
        if total_score >= 90:
            score_distribution["excellent"] += 1
        elif total_score >= 75:
            score_distribution["good"] += 1
        elif total_score >= 60:
            score_distribution["average"] += 1
        else:
            score_distribution["poor"] += 1

    report_history = []
    for report in all_reports[:20]:
        report_history.append({
            "id": report.id,
            "date": report.report_date.isoformat() if report.report_date else "",
            "type": report.report_type,
            "health_score": report.health_score or 0,
            "total_runs": report.total_runs or 0,
            "success_rate": report.success_rate or 0,
            "active_skills": report.active_skills or 0,
            "data_size": report.data_size_bytes or 0,
            "compressed": report.is_compressed,
            "created_at": report.created_at.strftime("%m-%d %H:%M") if report.created_at else "",
        })

    health_changes = []
    if len(trend_data) >= 2:
        for i in range(1, len(trend_data)):
            prev = trend_data[i - 1]["health_score"]
            curr = trend_data[i]["health_score"]
            change = curr - prev
            health_changes.append({
                "date": trend_data[i]["date"],
                "score": curr,
                "change": round(change, 1),
                "direction": "up" if change > 0 else ("down" if change < 0 else "flat"),
            })

    agent_info = {
        "agent_id": agent.agent_id,
        "name": agent.name or f"Agent-{agent.agent_id[:8]}",
        "os_info": agent.os_info or "未知",
        "python_version": agent.python_version or "未知",
        "monitor_version": agent.monitor_version or "未知",
        "created_at": agent.created_at.strftime("%Y-%m-%d %H:%M") if agent.created_at else "",
        "last_heartbeat": agent.last_heartbeat_at.strftime("%Y-%m-%d %H:%M") if agent.last_heartbeat_at else "无",
    }

    diagnostic_summary = None
    if latest_diag_data:
        diag_payload = latest_diag_data.get("diagnostics", {})
        diagnostic_summary = {
            "date": latest_diag.report_date.isoformat() if latest_diag else "",
            "markdown": latest_diag_data.get("report_markdown", ""),
            "health_score": latest_diag.health_score if latest_diag else 0,
            "trigger": latest_diag_data.get("trigger"),
            "issues": diag_payload.get("issues", []),
            "suggestions": diag_payload.get("suggestions", []),
            "recommendations": latest_diag_data.get("recommendations", []),
        }

    first_diagnostic = None
    if first_diag:
        first_diagnostic = {
            "date": first_diag.report_date.isoformat() if first_diag.report_date else "",
            "created_at": first_diag.created_at.strftime("%Y-%m-%d %H:%M") if first_diag.created_at else "",
            "health_score": first_diag.health_score or 0,
            "trigger": first_diag_data.get("trigger"),
            "markdown": first_diag_data.get("report_markdown", ""),
        }

    recent_daily_count = sum(1 for r in daily_reports if r.report_date and r.report_date >= end_date - timedelta(days=6))
    report_sync = {
        "daily_count": len(daily_reports),
        "diagnostic_count": len(diag_reports),
        "recent_daily_count": recent_daily_count,
        "has_initial_diagnostic": bool(first_diag),
        "first_report_date": all_reports[-1].report_date.isoformat() if all_reports and all_reports[-1].report_date else "",
        "latest_daily_date": latest_daily.report_date.isoformat() if latest_daily and latest_daily.report_date else "",
        "latest_diag_date": latest_diag.report_date.isoformat() if latest_diag and latest_diag.report_date else "",
        "first_diagnostic_date": first_diag.report_date.isoformat() if first_diag and first_diag.report_date else "",
        "status": "healthy" if first_diag and recent_daily_count >= 5 else ("warning" if daily_reports or diag_reports else "empty"),
        "status_label": "同步正常" if first_diag and recent_daily_count >= 5 else ("待补齐" if daily_reports or diag_reports else "未开始"),
    }

    return {
        "generated_at": datetime.now().isoformat(),
        "period_days": days,
        "agent": agent_info,
        "overview": overview_metrics,
        "trend": trend_data,
        "skill_rankings": skill_rankings,
        "score_distribution": score_distribution,
        "grade_distribution": dict(grade_distribution),
        "report_history": report_history,
        "health_changes": health_changes,
        "diagnostic_summary": diagnostic_summary,
        "first_diagnostic": first_diagnostic,
        "report_sync": report_sync,
        "recommendations": recommendations[:6],
        "installed_skills": installed_skills[:50],
    }


@dashboard_bp.route("/dashboard/<agent_id_str>")
def dashboard_page(agent_id_str):
    """后台分析仪表盘页面"""
    if not _require_dashboard_token():
        return render_template("h5_error.html", message="未授权访问"), 401

    agent = Agent.query.filter_by(agent_id=agent_id_str).first()
    if not agent:
        return render_template("h5_error.html", message="Agent 不存在"), 404

    days = min(int(request.args.get("days", "30")), 90)
    data = _collect_dashboard_data(agent, days)
    return render_template("dashboard.html", agent=agent, data=data)


@dashboard_bp.route("/api/dashboard/<agent_id_str>/data")
def dashboard_data(agent_id_str):
    """仪表盘 JSON 数据接口"""
    if not _require_dashboard_token():
        return jsonify({"error": "未授权访问"}), 401

    agent = Agent.query.filter_by(agent_id=agent_id_str).first()
    if not agent:
        return jsonify({"error": "Agent 不存在"}), 404

    days = min(int(request.args.get("days", "30")), 90)
    data = _collect_dashboard_data(agent, days)
    return jsonify({"ok": True, "data": data})
