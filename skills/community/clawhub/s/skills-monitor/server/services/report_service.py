"""
报告服务层 — 数据上报处理 + 报告生成 + 推送调度
==============================================
"""

import gzip
import hashlib
import json
from datetime import datetime, date
from typing import Any, Dict, List, Optional, Tuple

from server.models.database import db, Agent, User, UserAgent, SkillReport, DailyDigest


def verify_agent_token(agent_id: str, token: str) -> Optional[Agent]:
    """
    验证 Agent Token
    token 存储为 SHA256 哈希
    """
    agent = Agent.query.filter_by(agent_id=agent_id).first()
    if not agent:
        return None

    token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()
    if agent.token_hash != token_hash:
        return None

    return agent


def register_agent(agent_id: str, token: str, **kwargs) -> Agent:
    """
    注册新 Agent 或更新已有 Agent
    """
    token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()

    agent = Agent.query.filter_by(agent_id=agent_id).first()
    if agent:
        # 更新
        agent.token_hash = token_hash
        agent.updated_at = datetime.utcnow()
    else:
        # 新建
        agent = Agent(
            agent_id=agent_id,
            token_hash=token_hash,
        )
        db.session.add(agent)

    # 更新附加信息
    for key in ("name", "os_info", "python_version", "monitor_version",
                "total_skills", "runnable_skills"):
        if key in kwargs and kwargs[key] is not None:
            setattr(agent, key, kwargs[key])

    db.session.commit()
    return agent


def process_report_upload(
    agent: Agent,
    report_data: dict,
    report_type: str = "daily",
    report_date: Optional[date] = None,
    compress_threshold: int = 10240,
) -> SkillReport:
    """
    处理 Agent 上报的数据
    - 自动判断是否压缩
    - 提取关键指标存储
    - 更新 Agent 状态
    """
    if report_date is None:
        report_date = date.today()

    # 查找是否有同日同类型报告（upsert）
    existing = SkillReport.query.filter_by(
        agent_db_id=agent.id,
        report_date=report_date,
        report_type=report_type,
    ).first()

    if existing:
        report = existing
    else:
        report = SkillReport(
            agent_db_id=agent.id,
            agent_id_str=agent.agent_id,
            report_date=report_date,
            report_type=report_type,
        )

    # 设置数据（自动压缩）
    report.set_data(report_data, compress_threshold)

    # 提取关键指标
    overview = report_data.get("overview", {})
    report.health_score = report_data.get("health_score", overview.get("health_score"))
    report.total_runs = overview.get("total_runs", 0)
    report.success_rate = overview.get("success_rate", 0)
    report.active_skills = overview.get("active_skills", 0)
    report.avg_duration_ms = overview.get("avg_duration_ms")

    # Top Skills
    scores = report_data.get("scores", [])
    top3 = [
        {"skill_id": s["skill_id"], "score": s["total_score"], "grade": s.get("grade", "")}
        for s in scores[:3]
    ] if scores else []
    report.top_skills_json = json.dumps(top3, ensure_ascii=False)

    if not existing:
        db.session.add(report)

    # 更新 Agent 状态
    agent.last_report_at = datetime.utcnow()
    agent.health_score = report.health_score
    agent.total_skills = overview.get("total_installed", agent.total_skills)
    agent.runnable_skills = overview.get("total_runnable", agent.runnable_skills)

    db.session.commit()
    return report


def get_agent_reports(
    agent_id: str,
    report_type: Optional[str] = None,
    days: int = 30,
    limit: int = 30,
) -> List[Dict]:
    """获取某 Agent 的历史报告"""
    query = SkillReport.query.filter_by(agent_id_str=agent_id)
    if report_type:
        query = query.filter_by(report_type=report_type)

    reports = query.order_by(SkillReport.report_date.desc()).limit(limit).all()
    return [r.to_dict(include_data=False) for r in reports]


def get_report_detail(report_id: int) -> Optional[Dict]:
    """获取报告详情（含完整数据）"""
    report = SkillReport.query.get(report_id)
    if not report:
        return None
    return report.to_dict(include_data=True)


def bind_user_agent(user: User, agent_id: str, token: str, alias: str = "") -> Tuple[bool, str]:
    """
    绑定用户和 Agent
    验证 token 后创建关联
    """
    agent = verify_agent_token(agent_id, token)
    if not agent:
        return False, "智能体 ID 或 Key 无效"

    # 检查是否已绑定
    existing = UserAgent.query.filter_by(user_id=user.id, agent_id=agent.id).first()
    if existing:
        return True, "已绑定"

    # 创建绑定
    ua = UserAgent(
        user_id=user.id,
        agent_id=agent.id,
        alias=alias,
        is_primary=user.agents.count() == 0,  # 第一个设为主 Agent
    )
    db.session.add(ua)
    db.session.commit()

    return True, "绑定成功"


def get_user_agents(user: User) -> List[Dict]:
    """获取用户绑定的所有 Agent"""
    bindings = UserAgent.query.filter_by(user_id=user.id).all()
    results = []
    for ua in bindings:
        agent_dict = ua.agent.to_dict() if ua.agent else {}
        agent_dict["alias"] = ua.alias
        agent_dict["is_primary"] = ua.is_primary
        agent_dict["bind_id"] = ua.id
        results.append(agent_dict)
    return results
