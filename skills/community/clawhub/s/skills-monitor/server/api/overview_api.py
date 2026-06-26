"""
多 Agent 汇总总览 API — 全局分析仪表盘
========================================
- GET  /overview                     总览主页（所有 Agent 汇总）
- GET  /api/overview/data            总览 JSON 数据
"""

import json
from datetime import date, datetime, timedelta
from collections import Counter, defaultdict
from flask import Blueprint, request, render_template, jsonify

from server.models.database import db, Agent, SkillReport

overview_bp = Blueprint("overview_api", __name__)


def _collect_overview_data(days: int = 30) -> dict:
    """
    汇总所有 Agent 的全局分析数据
    """
    end_date = date.today()
    start_date = end_date - timedelta(days=days - 1)

    # ── 获取所有 Agent ──
    all_agents = Agent.query.order_by(Agent.last_report_at.desc().nullslast()).all()
    total_agents = len(all_agents)

    if total_agents == 0:
        return {
            "generated_at": datetime.now().isoformat(),
            "period_days": days,
            "total_agents": 0,
            "agents": [],
            "fleet_overview": {},
            "trend": [],
            "skill_global_rankings": [],
            "score_distribution": {"excellent": 0, "good": 0, "average": 0, "poor": 0},
            "agent_comparison": [],
            "os_distribution": {},
            "version_distribution": {},
            "alert_summary": [],
        }

    # ── 1. 各 Agent 摘要信息 ──
    agents_summary = []
    active_agents = 0
    total_health = 0
    total_health_count = 0
    total_skills_installed = 0
    total_skills_runnable = 0
    total_reports = 0
    os_counter = Counter()
    version_counter = Counter()
    all_latest_scores = []  # 所有 Agent 的 skill 评分汇总

    for agent in all_agents:
        # 最新 daily 报告
        latest = SkillReport.query.filter_by(
            agent_db_id=agent.id, report_type="daily"
        ).order_by(SkillReport.report_date.desc()).first()

        # 报告总数
        report_count = SkillReport.query.filter_by(agent_db_id=agent.id).count()
        total_reports += report_count

        # 最近 7 天报告数
        recent_reports = SkillReport.query.filter(
            SkillReport.agent_db_id == agent.id,
            SkillReport.report_type == "daily",
            SkillReport.report_date >= end_date - timedelta(days=6),
        ).count()

        # 判断是否活跃（7 天内有上报）
        is_active = recent_reports > 0
        if is_active:
            active_agents += 1

        # 健康度统计
        health = agent.health_score or (latest.health_score if latest else None)
        if health is not None:
            total_health += health
            total_health_count += 1

        # Skill 数量
        total_skills_installed += (agent.total_skills or 0)
        total_skills_runnable += (agent.runnable_skills or 0)

        # OS / 版本统计
        if agent.os_info:
            os_key = agent.os_info.split()[0] if agent.os_info else "Unknown"
            os_counter[os_key] += 1
        if agent.monitor_version:
            version_counter[agent.monitor_version] += 1

        # 最新评分数据
        latest_data = latest.get_data() if latest else {}
        scores = latest_data.get("scores", [])
        for s in scores:
            s["_agent_name"] = agent.name or f"Agent-{agent.agent_id[:8]}"
            s["_agent_id"] = agent.agent_id
        all_latest_scores.extend(scores)

        # 最新运行数据
        overview = latest_data.get("overview", {})

        # 确定状态
        if not latest:
            status = "offline"
            status_label = "未上报"
        elif not is_active:
            status = "idle"
            status_label = "不活跃"
        elif health is not None and health < 50:
            status = "warning"
            status_label = "需关注"
        else:
            status = "healthy"
            status_label = "正常"

        agents_summary.append({
            "agent_id": agent.agent_id,
            "name": agent.name or f"Agent-{agent.agent_id[:8]}",
            "health_score": round(health, 1) if health else None,
            "total_skills": agent.total_skills or 0,
            "runnable_skills": agent.runnable_skills or 0,
            "total_runs": overview.get("total_runs", latest.total_runs if latest else 0),
            "success_rate": overview.get("success_rate", latest.success_rate if latest else 0),
            "active_skills": overview.get("active_skills", latest.active_skills if latest else 0),
            "avg_duration_ms": overview.get("avg_duration_ms", 0),
            "os_info": agent.os_info or "未知",
            "python_version": agent.python_version or "",
            "monitor_version": agent.monitor_version or "",
            "report_count": report_count,
            "recent_reports_7d": recent_reports,
            "last_report_at": agent.last_report_at.strftime("%Y-%m-%d %H:%M") if agent.last_report_at else "未上报",
            "created_at": agent.created_at.strftime("%Y-%m-%d") if agent.created_at else "",
            "status": status,
            "status_label": status_label,
        })

    # ── 2. 舰队全局概览 ──
    avg_health = round(total_health / total_health_count, 1) if total_health_count > 0 else 0

    # 全局总运行次数、成功率
    global_runs = sum(a["total_runs"] or 0 for a in agents_summary)
    rates = [a["success_rate"] for a in agents_summary if a["success_rate"] and a["success_rate"] > 0]
    global_avg_rate = round(sum(rates) / len(rates), 1) if rates else 0
    global_active_skills = sum(a["active_skills"] or 0 for a in agents_summary)

    fleet_overview = {
        "total_agents": total_agents,
        "active_agents": active_agents,
        "inactive_agents": total_agents - active_agents,
        "avg_health_score": avg_health,
        "total_skills_installed": total_skills_installed,
        "total_skills_runnable": total_skills_runnable,
        "global_runnable_rate": round(total_skills_runnable / total_skills_installed * 100, 1) if total_skills_installed > 0 else 0,
        "global_total_runs": global_runs,
        "global_avg_success_rate": global_avg_rate,
        "global_active_skills": global_active_skills,
        "total_reports": total_reports,
    }

    # ── 3. 全局趋势（按天聚合所有 Agent） ──
    range_reports = SkillReport.query.filter(
        SkillReport.report_type == "daily",
        SkillReport.report_date >= start_date,
        SkillReport.report_date <= end_date,
    ).order_by(SkillReport.report_date.asc()).all()

    # 按日期聚合
    date_agg = defaultdict(lambda: {
        "health_scores": [], "total_runs": 0, "success_rates": [],
        "active_skills": 0, "agent_count": 0,
    })
    for r in range_reports:
        d = r.report_date.isoformat()
        date_agg[d]["health_scores"].append(r.health_score or 0)
        date_agg[d]["total_runs"] += (r.total_runs or 0)
        if r.success_rate and r.success_rate > 0:
            date_agg[d]["success_rates"].append(r.success_rate)
        date_agg[d]["active_skills"] += (r.active_skills or 0)
        date_agg[d]["agent_count"] += 1

    trend_data = []
    for d_str in sorted(date_agg.keys()):
        agg = date_agg[d_str]
        avg_h = round(sum(agg["health_scores"]) / len(agg["health_scores"]), 1) if agg["health_scores"] else 0
        avg_r = round(sum(agg["success_rates"]) / len(agg["success_rates"]), 1) if agg["success_rates"] else 0
        trend_data.append({
            "date": d_str,
            "avg_health_score": avg_h,
            "total_runs": agg["total_runs"],
            "avg_success_rate": avg_r,
            "total_active_skills": agg["active_skills"],
            "reporting_agents": agg["agent_count"],
        })

    # ── 4. 全局 Skill 评分排行（跨 Agent 合并） ──
    skill_agg = defaultdict(lambda: {"scores": [], "agents": set()})
    for s in all_latest_scores:
        sid = s.get("skill_id", "unknown")
        skill_agg[sid]["scores"].append(s.get("total_score", 0))
        skill_agg[sid]["agents"].add(s.get("_agent_name", ""))

    skill_global_rankings = []
    for sid, info in skill_agg.items():
        avg_score = round(sum(info["scores"]) / len(info["scores"]), 1)
        # 等级判定
        if avg_score >= 90:
            grade = "S(卓越)"
        elif avg_score >= 80:
            grade = "A(优秀)"
        elif avg_score >= 70:
            grade = "B(良好)"
        elif avg_score >= 60:
            grade = "C(一般)"
        else:
            grade = "D(需改善)"

        skill_global_rankings.append({
            "skill_id": sid,
            "avg_score": avg_score,
            "grade": grade,
            "agent_count": len(info["agents"]),
            "agents": sorted(info["agents"]),
            "min_score": round(min(info["scores"]), 1),
            "max_score": round(max(info["scores"]), 1),
        })
    skill_global_rankings.sort(key=lambda x: -x["avg_score"])

    # ── 5. 全局评分分布 ──
    score_distribution = {"excellent": 0, "good": 0, "average": 0, "poor": 0}
    for s in all_latest_scores:
        sc = s.get("total_score", 0)
        if sc >= 90:
            score_distribution["excellent"] += 1
        elif sc >= 75:
            score_distribution["good"] += 1
        elif sc >= 60:
            score_distribution["average"] += 1
        else:
            score_distribution["poor"] += 1

    # ── 6. Agent 对比数据（雷达图用） ──
    agent_comparison = []
    for a in agents_summary:
        agent_comparison.append({
            "name": a["name"],
            "agent_id": a["agent_id"],
            "health": a["health_score"] or 0,
            "runs": a["total_runs"] or 0,
            "rate": a["success_rate"] or 0,
            "active": a["active_skills"] or 0,
            "skills": a["runnable_skills"] or 0,
        })

    # ── 7. 告警摘要 ──
    alert_summary = []
    for a in agents_summary:
        if a["status"] == "offline":
            alert_summary.append({
                "level": "error",
                "agent": a["name"],
                "message": f"Agent 从未上报数据",
            })
        elif a["status"] == "idle":
            alert_summary.append({
                "level": "warning",
                "agent": a["name"],
                "message": f"已超过 7 天未上报（最后: {a['last_report_at']}）",
            })
        elif a["health_score"] is not None and a["health_score"] < 50:
            alert_summary.append({
                "level": "warning",
                "agent": a["name"],
                "message": f"健康度仅 {a['health_score']}，低于 50 分警戒线",
            })

    # 低评分 Skill 告警
    for sk in skill_global_rankings:
        if sk["avg_score"] < 60:
            alert_summary.append({
                "level": "info",
                "agent": "全局",
                "message": f"Skill [{sk['skill_id']}] 平均评分仅 {sk['avg_score']}，需关注",
            })

    return {
        "generated_at": datetime.now().isoformat(),
        "period_days": days,
        "total_agents": total_agents,
        "fleet_overview": fleet_overview,
        "agents": agents_summary,
        "trend": trend_data,
        "skill_global_rankings": skill_global_rankings[:50],  # 支持更多 Skill
        "score_distribution": score_distribution,
        "agent_comparison": agent_comparison,
        "os_distribution": dict(os_counter),
        "version_distribution": dict(version_counter),
        "alert_summary": alert_summary,
    }


# ──────── 页面路由 ────────

@overview_bp.route("/overview")
def overview_page():
    """多 Agent 汇总总览页面"""
    days = min(int(request.args.get("days", "30")), 90)
    data = _collect_overview_data(days)
    return render_template("overview.html", data=data)


# ──────── 数据 API ────────

@overview_bp.route("/api/overview/data")
def overview_data():
    """总览 JSON 数据接口"""
    days = min(int(request.args.get("days", "30")), 90)
    data = _collect_overview_data(days)
    return jsonify({"ok": True, "data": data})
