"""
PWA API — 供 Skills Monitor PWA 单页应用使用
=============================================
登录方式: Agent ID + API Key → 签发 Token
所有接口均通过 X-PWA-Token 认证

路由前缀: /api/pwa
"""

import hashlib
import secrets
from datetime import date, timedelta
from functools import wraps

from flask import Blueprint, request, jsonify, render_template

from server.models.database import db, User, Agent, UserAgent, SkillReport
from server.services.report_service import verify_agent_token

pwa_bp = Blueprint("pwa_api", __name__)

# ──────── Token 管理 ────────
# 简单的内存 token store（重启后失效，用户需重新登录）
_pwa_tokens: dict[str, dict] = {}


def _hash_token(raw: str) -> str:
    return hashlib.sha256(raw.encode()).hexdigest()


def _require_pwa_auth(f):
    """PWA Token 认证装饰器"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("X-PWA-Token", "")
        if not token or token not in _pwa_tokens:
            return jsonify({"ok": False, "error": "未登录，请先登录"}), 401
        request._pwa_user_id = _pwa_tokens[token]["user_id"]
        return f(*args, **kwargs)
    return decorated


def _get_pwa_user():
    """获取当前 PWA 登录用户"""
    user_id = getattr(request, "_pwa_user_id", None)
    if not user_id:
        return None
    return User.query.get(user_id)


def _get_user_agents(user):
    """获取用户绑定的所有 Agent"""
    bindings = UserAgent.query.filter_by(user_id=user.id).all()
    return [(ua, ua.agent) for ua in bindings if ua.agent]


# ──────── PWA 页面 ────────

@pwa_bp.route("/pwa/")
def pwa_index():
    """PWA 入口页面"""
    return render_template("pwa.html")


# ──────── 登录 ────────

@pwa_bp.route("/api/pwa/login", methods=["POST"])
def pwa_login():
    """用 Agent ID + API Key 登录"""
    data = request.get_json(force=True)
    agent_id = data.get("agent_id", "").strip()
    agent_token = data.get("agent_token", "").strip()

    if not agent_id or not agent_token:
        return jsonify({"ok": False, "error": "请输入智能体 ID 和 Key"})

    agent = verify_agent_token(agent_id, agent_token)
    if not agent:
        # 区分是 agent 不存在还是 key 不对
        check = Agent.query.filter_by(agent_id=agent_id).first()
        if not check:
            return jsonify({"ok": False, "error": "智能体不存在，请检查智能体 ID"})
        return jsonify({"ok": False, "error": "Key 不正确"})

    # 查找或创建 PWA 用户（使用 agent_id 作为 openid）
    pwa_openid = f"pwa_{agent_id}"
    user = User.query.filter_by(openid=pwa_openid).first()
    if not user:
        user = User(openid=pwa_openid, nickname="PWA 用户")
        db.session.add(user)
        db.session.flush()

    # 确保绑定关系
    binding = UserAgent.query.filter_by(user_id=user.id, agent_id=agent.id).first()
    if not binding:
        binding = UserAgent(user_id=user.id, agent_id=agent.id, is_primary=True)
        db.session.add(binding)

    db.session.commit()

    # 签发 token
    raw_token = secrets.token_hex(32)
    _pwa_tokens[raw_token] = {"user_id": user.id, "agent_id": agent.id}

    agent_count = UserAgent.query.filter_by(user_id=user.id).count()

    return jsonify({
        "ok": True,
        "token": raw_token,
        "user": {
            "id": user.id,
            "nickname": user.nickname or "PWA 用户",
            "agent_count": agent_count,
        }
    })


# ──────── 用户信息 ────────

@pwa_bp.route("/api/pwa/user")
@_require_pwa_auth
def pwa_user():
    user = _get_pwa_user()
    if not user:
        return jsonify({"ok": False, "error": "用户不存在"}), 404

    agent_count = UserAgent.query.filter_by(user_id=user.id).count()

    return jsonify({
        "ok": True,
        "user": {
            "id": user.id,
            "nickname": user.nickname or "PWA 用户",
            "agent_count": agent_count,
        }
    })


# ──────── 仪表盘（增强版：含最新报告的推荐/诊断数据） ────────

@pwa_bp.route("/api/pwa/dashboard")
@_require_pwa_auth
def pwa_dashboard():
    user = _get_pwa_user()
    if not user:
        return jsonify({"ok": False, "error": "用户不存在"}), 404

    bindings = _get_user_agents(user)
    if not bindings:
        return jsonify({"ok": True, "dashboard": {
            "total_agents": 0, "total_skills": 0, "total_runs": 0,
            "avg_health": 0, "avg_success_rate": 0, "trend": [], "agents": [],
            "latest_report": None,
        }})

    agents_data = []
    total_health = 0
    total_success = 0
    total_runs = 0
    total_skills = 0

    for ua, agent in bindings:
        latest = SkillReport.query.filter_by(agent_db_id=agent.id).order_by(
            SkillReport.report_date.desc(), SkillReport.created_at.desc()
        ).first()

        health = latest.health_score if latest else 0
        total_health += health
        total_success += (latest.success_rate if latest else 0)
        total_runs += (latest.total_runs if latest else 0)
        total_skills += (latest.active_skills if latest else 0)

        # 统计该 Agent 的已安装技能总数（从最新报告中取）
        skill_count = 0
        if latest:
            rd = latest.get_data()
            ov = rd.get("overview", {})
            skill_count = ov.get("total_installed", 0)

        agents_data.append({
            "agent_id": agent.agent_id,
            "name": agent.name or f"Agent-{agent.agent_id[:8]}",
            "health_score": health,
            "is_primary": ua.is_primary,
            "total_skills": skill_count,
        })

    n = len(bindings)
    avg_health = total_health / n if n else 0
    avg_success = total_success / n if n else 0

    # 趋势数据（取主 Agent 的）
    primary_agent = next((a for ua, a in bindings if ua.is_primary), bindings[0][1] if bindings else None)
    trend = _get_trend(primary_agent.id, 7) if primary_agent else []

    # ── 增强部分：获取最新报告的完整数据 ──
    latest_report_summary = None
    if primary_agent:
        # 优先取最新诊断报告（内容最丰富），fallback 到最新日报
        latest_diag = SkillReport.query.filter_by(
            agent_db_id=primary_agent.id, report_type="diagnostic"
        ).order_by(SkillReport.report_date.desc(), SkillReport.created_at.desc()).first()

        latest_daily = SkillReport.query.filter_by(
            agent_db_id=primary_agent.id, report_type="daily"
        ).order_by(SkillReport.report_date.desc(), SkillReport.created_at.desc()).first()

        best_report = latest_diag or latest_daily
        if best_report:
            rd = best_report.get_data()

            # 推荐安装
            recs = rd.get("recommendations", [])

            # 诊断数据
            diag = rd.get("diagnostics", {})

            # 已安装技能
            installed = rd.get("installed_skills", [])

            # 概览
            overview = rd.get("overview", {})

            latest_report_summary = {
                "id": best_report.id,
                "report_type": best_report.report_type,
                "report_date": best_report.report_date.isoformat() if best_report.report_date else "",
                "health_score": best_report.health_score,
                "overview": overview,
                "recommendations": recs[:6],
                "diagnostics": {
                    "issues": diag.get("issues", []),
                    "suggestions": diag.get("suggestions", []),
                    "coverage": diag.get("coverage", []),
                    "unused_runnable": diag.get("unused_runnable", []),
                },
                "installed_skills": installed[:15],
                "installed_skills_total": len(installed),
            }

    return jsonify({
        "ok": True,
        "dashboard": {
            "total_agents": n,
            "total_skills": total_skills or (agents_data[0].get("total_skills", 0) if agents_data else 0),
            "total_runs": total_runs,
            "avg_health": round(avg_health, 1),
            "avg_success_rate": round(avg_success, 1),
            "trend": trend,
            "agents": agents_data,
            "latest_report": latest_report_summary,
        }
    })


# ──────── 报告列表 ────────

@pwa_bp.route("/api/pwa/reports")
@_require_pwa_auth
def pwa_reports():
    user = _get_pwa_user()
    if not user:
        return jsonify({"ok": False, "error": "用户不存在"}), 404

    limit = min(int(request.args.get("limit", "30")), 100)
    report_type = request.args.get("type", "all")

    bindings = _get_user_agents(user)
    agent_ids = [a.id for _, a in bindings]
    agent_map = {a.id: a for _, a in bindings}

    query = SkillReport.query.filter(SkillReport.agent_db_id.in_(agent_ids))
    if report_type != "all":
        query = query.filter_by(report_type=report_type)

    reports = query.order_by(
        SkillReport.report_date.desc(), SkillReport.created_at.desc()
    ).limit(limit).all()

    result = []
    for r in reports:
        agent = agent_map.get(r.agent_db_id)
        result.append({
            "id": r.id,
            "report_type": r.report_type,
            "report_date": r.report_date.isoformat() if r.report_date else "",
            "health_score": r.health_score,
            "total_runs": r.total_runs,
            "success_rate": r.success_rate,
            "active_skills": r.active_skills,
            "agent_id": agent.agent_id if agent else "",
            "agent_name": agent.name if agent else "",
        })

    return jsonify({"ok": True, "reports": result})


# ──────── 报告详情 ────────

@pwa_bp.route("/api/pwa/report/<int:report_id>")
@_require_pwa_auth
def pwa_report_detail(report_id):
    user = _get_pwa_user()
    if not user:
        return jsonify({"ok": False, "error": "用户不存在"}), 404

    report = SkillReport.query.get(report_id)
    if not report:
        return jsonify({"ok": False, "error": "报告不存在"}), 404

    # 权限校验
    bindings = _get_user_agents(user)
    agent_ids = [a.id for _, a in bindings]
    if report.agent_db_id not in agent_ids:
        return jsonify({"ok": False, "error": "无权查看该报告"}), 403

    agent = Agent.query.get(report.agent_db_id)
    rd = report.get_data()

    return jsonify({
        "ok": True,
        "report": {
            "id": report.id,
            "report_type": report.report_type,
            "report_date": report.report_date.isoformat() if report.report_date else "",
            "health_score": report.health_score,
            "total_runs": report.total_runs,
            "success_rate": report.success_rate,
            "active_skills": report.active_skills,
            "data_size_bytes": report.data_size_bytes,
            "created_at": report.created_at.isoformat() if report.created_at else "",
            "agent_id": agent.agent_id if agent else "",
            "agent_name": agent.name if agent else "",
            "trigger": rd.get("trigger", ""),
            "overview": rd.get("overview", {}),
            "scores": rd.get("scores", []),
            "recommendations": rd.get("recommendations", []),
            "diagnostics": rd.get("diagnostics", {}),
            "report_markdown": rd.get("report_markdown", ""),
        }
    })


# ──────── Agent Skills ────────

@pwa_bp.route("/api/pwa/skills/<agent_id_str>")
@_require_pwa_auth
def pwa_agent_skills(agent_id_str):
    user = _get_pwa_user()
    if not user:
        return jsonify({"ok": False, "error": "用户不存在"}), 404

    agent = Agent.query.filter_by(agent_id=agent_id_str).first()
    if not agent:
        return jsonify({"ok": False, "error": "智能体不存在"}), 404

    # 权限校验
    binding = UserAgent.query.filter_by(user_id=user.id, agent_id=agent.id).first()
    if not binding:
        return jsonify({"ok": False, "error": "无权查看"}), 403

    # 从最新报告中取 scores
    latest = SkillReport.query.filter_by(agent_db_id=agent.id).order_by(
        SkillReport.report_date.desc(), SkillReport.created_at.desc()
    ).first()

    skills = []
    if latest:
        rd = latest.get_data()
        skills = rd.get("scores", [])

    return jsonify({
        "ok": True,
        "agent_name": agent.name or f"Agent-{agent.agent_id[:8]}",
        "skills": skills,
    })


# ──────── Agent 列表 ────────

@pwa_bp.route("/api/pwa/agents")
@_require_pwa_auth
def pwa_agents():
    user = _get_pwa_user()
    if not user:
        return jsonify({"ok": False, "error": "用户不存在"}), 404

    bindings = _get_user_agents(user)

    agents = []
    for ua, agent in bindings:
        latest = SkillReport.query.filter_by(agent_db_id=agent.id).order_by(
            SkillReport.report_date.desc(), SkillReport.created_at.desc()
        ).first()

        skill_count = 0
        if latest:
            rd = latest.get_data()
            skill_count = rd.get("overview", {}).get("total_installed", 0)

        agents.append({
            "agent_id": agent.agent_id,
            "name": agent.name or f"Agent-{agent.agent_id[:8]}",
            "health_score": latest.health_score if latest else 0,
            "total_skills": skill_count,
            "is_primary": ua.is_primary,
        })

    return jsonify({"ok": True, "agents": agents})


# ──────── 绑定新 Agent ────────

@pwa_bp.route("/api/pwa/bind", methods=["POST"])
@_require_pwa_auth
def pwa_bind():
    user = _get_pwa_user()
    if not user:
        return jsonify({"ok": False, "error": "用户不存在"}), 404

    data = request.get_json(force=True)
    agent_id = data.get("agent_id", "").strip()
    agent_token = data.get("agent_token", "").strip()

    if not agent_id or not agent_token:
        return jsonify({"ok": False, "error": "请输入智能体 ID 和 Key"})

    agent = verify_agent_token(agent_id, agent_token)
    if not agent:
        check = Agent.query.filter_by(agent_id=agent_id).first()
        if not check:
            return jsonify({"ok": False, "error": "智能体不存在"})
        return jsonify({"ok": False, "error": "Key 不正确"})

    existing = UserAgent.query.filter_by(user_id=user.id, agent_id=agent.id).first()
    if existing:
        return jsonify({"ok": False, "error": "已经绑定过该智能体"})

    binding = UserAgent(user_id=user.id, agent_id=agent.id, is_primary=False)
    db.session.add(binding)
    db.session.commit()

    return jsonify({"ok": True})


# ──────── 工具函数 ────────

def _get_trend(agent_db_id: int, days: int = 7) -> list:
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
