"""
推送调度器 — 每日定时推送微信模板消息
====================================
使用 APScheduler 定时任务框架。
"""

import logging
from datetime import datetime, date

from server.models.database import db, User, Agent, UserAgent, DailyDigest, SkillReport
from server.services.wechat_service import wechat_service
from server.config import H5_BASE_URL

logger = logging.getLogger("push_scheduler")


def push_daily_reports(app):
    """
    推送每日报告（在 Flask app 上下文中调用）
    遍历所有启用推送的用户，为其每个绑定的 Agent 推送模板消息
    """
    with app.app_context():
        now = datetime.now()
        current_hour = now.hour

        # 查找当前时间段应该推送的用户
        users = User.query.filter(
            User.push_enabled == True,
            User.subscribe == True,
            User.push_hour == current_hour,
        ).all()

        logger.info(f"[推送] 开始推送 {len(users)} 个用户 (hour={current_hour})")

        success_count = 0
        fail_count = 0

        for user in users:
            bindings = UserAgent.query.filter_by(user_id=user.id).all()

            for ua in bindings:
                agent = ua.agent
                if not agent:
                    continue

                try:
                    result = _push_one(user, agent, ua)
                    if result:
                        success_count += 1
                    else:
                        fail_count += 1
                except Exception as e:
                    logger.error(f"[推送] 用户 {user.id} Agent {agent.agent_id} 失败: {e}")
                    fail_count += 1

        logger.info(f"[推送] 完成: 成功 {success_count}, 失败 {fail_count}")


def _push_one(user: User, agent: Agent, ua: UserAgent) -> bool:
    """推送单个用户的单个 Agent 报告"""
    today = date.today()

    # 检查是否已推送
    existing = DailyDigest.query.filter_by(
        user_id=user.id,
        agent_db_id=agent.id,
        digest_date=today,
    ).first()

    if existing and existing.push_status == "sent":
        return True  # 已推送过

    # 获取最新报告
    latest = SkillReport.query.filter_by(
        agent_db_id=agent.id,
        report_type="daily",
    ).order_by(SkillReport.report_date.desc()).first()

    if not latest:
        logger.debug(f"[推送] Agent {agent.agent_id} 无报告数据，跳过")
        return False

    # 提取推送数据
    health_score = latest.health_score or 0
    total_runs = latest.total_runs or 0
    success_rate = latest.success_rate or 0

    top_skill = "无"
    if latest.top_skills_json:
        try:
            import json
            top3 = json.loads(latest.top_skills_json)
            if top3:
                top_skill = f"{top3[0]['skill_id']} ({top3[0].get('score', 0):.0f}分)"
        except Exception:
            pass

    agent_name = ua.alias or agent.name or f"Agent-{agent.agent_id[:8]}"
    h5_url = f"{H5_BASE_URL}/h5/report/{agent.agent_id}"

    # v0.5.0: 推送模板消息（支持跳转小程序）
    ok, result = wechat_service.push_daily_report(
        openid=user.openid,
        agent_name=agent_name,
        health_score=health_score,
        total_runs=total_runs,
        success_rate=success_rate,
        top_skill=top_skill,
        h5_url=h5_url,
        agent_id=agent.agent_id,
    )

    # 记录推送结果
    import json as json_mod
    digest = existing or DailyDigest(
        user_id=user.id,
        agent_db_id=agent.id,
        digest_date=today,
    )
    digest.push_status = "sent" if ok else "failed"
    digest.push_result = json_mod.dumps(result, ensure_ascii=False)
    digest.h5_url = h5_url
    digest.push_type = "template_msg"

    if not existing:
        db.session.add(digest)
    db.session.commit()

    if ok:
        logger.info(f"[推送] ✅ 用户 {user.id} Agent {agent.agent_id} 推送成功")
    else:
        logger.warning(f"[推送] ❌ 用户 {user.id} Agent {agent.agent_id} 推送失败: {result}")

    return ok
