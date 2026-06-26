"""
运营闭环追踪器 v0.5.0 — 操作追踪 + 告警推送 + 闭环链路
=======================================================
核心功能:
  1. 操作追踪 — 记录用户从推送→打开→操作的完整链路
  2. 告警推送 — Skill 异常/性能下降时自动推送告警消息
  3. 闭环链路 — 公众号→小程序 跳转参数透传 + 回溯分析
  4. 推送效果分析 — 打开率、点击率、留存率

流程:
  Agent 上报异常 → 服务端检测 → 触发告警 → 推送公众号模板消息
  → 用户点击 → 跳转小程序详情页 → 记录操作 → 形成闭环
"""

import json
import logging
import hashlib
from datetime import datetime, date, timedelta
from typing import Any, Dict, List, Optional, Tuple
from enum import Enum

from server.models.database import db, User, Agent, UserAgent, SkillReport, DailyDigest
from server.services.wechat_service import wechat_service
from server.config import (
    WECHAT_TEMPLATE_ALERT,
    WECHAT_TEMPLATE_DAILY_REPORT,
    WECHAT_MP_APP_ID,
    H5_BASE_URL,
)

logger = logging.getLogger("operation_tracker")


# ──────── 告警级别 ────────

class AlertLevel(str, Enum):
    INFO = "info"           # 信息
    WARNING = "warning"     # 警告
    CRITICAL = "critical"   # 严重


# ──────── 告警规则 ────────

ALERT_RULES = [
    {
        "name": "success_rate_drop",
        "desc": "成功率下降",
        "condition": lambda current, prev: (
            prev.get("success_rate", 100) - current.get("success_rate", 0) > 15
        ),
        "level": AlertLevel.WARNING,
        "template": "⚠️ {agent_name} 成功率从 {prev_rate:.0f}% 降至 {curr_rate:.0f}%",
    },
    {
        "name": "health_score_drop",
        "desc": "健康度下降",
        "condition": lambda current, prev: (
            (prev.get("health_score") or 100) - (current.get("health_score") or 0) > 20
        ),
        "level": AlertLevel.CRITICAL,
        "template": "🔴 {agent_name} 健康度从 {prev_score:.0f} 降至 {curr_score:.0f}",
    },
    {
        "name": "skill_all_fail",
        "desc": "Skill 全部失败",
        "condition": lambda current, prev: (
            current.get("success_rate", 100) == 0 and current.get("total_runs", 0) > 3
        ),
        "level": AlertLevel.CRITICAL,
        "template": "❌ {agent_name} 所有 Skill 执行失败！({runs} 次运行全部失败)",
    },
    {
        "name": "long_idle",
        "desc": "长时间无数据",
        "condition": lambda current, prev: current.get("total_runs", 0) == 0,
        "level": AlertLevel.INFO,
        "template": "💤 {agent_name} 今日无任何 Skill 运行记录",
    },
]


# ──────── 操作事件类型 ────────

class TrackEvent(str, Enum):
    PUSH_SENT = "push_sent"             # 推送已发送
    PUSH_OPENED = "push_opened"         # 用户打开推送
    REPORT_VIEWED = "report_viewed"     # 查看报告详情
    SKILL_VIEWED = "skill_viewed"       # 查看 Skill 详情
    ACTION_TAKEN = "action_taken"       # 用户执行了操作
    MP_LAUNCHED = "mp_launched"         # 从公众号跳转到小程序


class OperationTracker:
    """
    运营闭环追踪器

    职责:
      1. 检测告警条件 → 触发推送
      2. 记录用户操作链路
      3. 分析推送效果
    """

    # ──────── 告警检测 ────────

    @staticmethod
    def check_alerts(agent: Agent) -> List[Dict[str, Any]]:
        """
        检测 Agent 是否触发告警规则

        Args:
            agent: Agent 实例

        Returns:
            触发的告警列表 [{rule_name, level, message, data}]
        """
        alerts = []

        # 获取今日和昨日报告
        today = date.today()
        yesterday = today - timedelta(days=1)

        current_report = SkillReport.query.filter_by(
            agent_db_id=agent.id,
            report_type="daily",
            report_date=today,
        ).first()

        prev_report = SkillReport.query.filter_by(
            agent_db_id=agent.id,
            report_type="daily",
            report_date=yesterday,
        ).first()

        current_data = {
            "success_rate": current_report.success_rate if current_report else None,
            "health_score": current_report.health_score if current_report else None,
            "total_runs": current_report.total_runs if current_report else 0,
        }
        prev_data = {
            "success_rate": prev_report.success_rate if prev_report else 100,
            "health_score": prev_report.health_score if prev_report else 100,
            "total_runs": prev_report.total_runs if prev_report else 0,
        }

        for rule in ALERT_RULES:
            try:
                if rule["condition"](current_data, prev_data):
                    alert = {
                        "rule_name": rule["name"],
                        "desc": rule["desc"],
                        "level": rule["level"].value,
                        "message": rule["template"].format(
                            agent_name=agent.name or f"Agent-{agent.agent_id[:8]}",
                            prev_rate=prev_data.get("success_rate", 0),
                            curr_rate=current_data.get("success_rate", 0),
                            prev_score=prev_data.get("health_score", 0),
                            curr_score=current_data.get("health_score", 0),
                            runs=current_data.get("total_runs", 0),
                        ),
                        "current_data": current_data,
                        "prev_data": prev_data,
                        "timestamp": datetime.now().isoformat(),
                    }
                    alerts.append(alert)
            except Exception as e:
                logger.debug(f"告警规则 {rule['name']} 检测异常: {e}")

        return alerts

    # ──────── 告警推送 ────────

    @staticmethod
    def send_alert(
        user: User,
        agent: Agent,
        alert: Dict[str, Any],
        binding: UserAgent = None,
    ) -> Tuple[bool, Dict]:
        """
        发送告警模板消息

        消息点击后跳转到小程序对应页面（公众号→小程序闭环）
        """
        agent_name = (binding.alias if binding else None) or agent.name or f"Agent-{agent.agent_id[:8]}"
        level = alert.get("level", "info")

        level_icons = {
            "info": "ℹ️",
            "warning": "⚠️",
            "critical": "🔴",
        }
        level_colors = {
            "info": "#3498db",
            "warning": "#f39c12",
            "critical": "#e74c3c",
        }

        # 生成追踪 ID（用于闭环追踪）
        track_id = hashlib.md5(
            f"{user.id}:{agent.agent_id}:{alert['rule_name']}:{datetime.now().isoformat()}".encode()
        ).hexdigest()[:12]

        # 模板消息数据
        data = {
            "first": {
                "value": f"{level_icons.get(level, '📢')} Skills Monitor 告警通知",
                "color": level_colors.get(level, "#333"),
            },
            "keyword1": {
                "value": agent_name,
                "color": "#333333",
            },
            "keyword2": {
                "value": alert.get("desc", "未知告警"),
                "color": level_colors.get(level, "#333"),
            },
            "keyword3": {
                "value": alert.get("message", ""),
                "color": "#333333",
            },
            "keyword4": {
                "value": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "color": "#999999",
            },
            "remark": {
                "value": "点击查看详情并处理 →",
                "color": "#667eea",
            },
        }

        # 小程序跳转路径（带追踪参数）
        miniprogram_config = {
            "appid": WECHAT_MP_APP_ID,
            "pagepath": (
                f"pages/dashboard/dashboard"
                f"?from=alert"
                f"&track_id={track_id}"
                f"&agent_id={agent.agent_id}"
                f"&alert={alert['rule_name']}"
            ),
        }

        # H5 备用链接
        h5_url = f"{H5_BASE_URL}/h5/report/{agent.agent_id}?track_id={track_id}"

        # 使用告警模板或每日报告模板（取决于配置）
        template_id = WECHAT_TEMPLATE_ALERT or WECHAT_TEMPLATE_DAILY_REPORT

        ok, result = wechat_service.send_template_message(
            openid=user.openid,
            template_id=template_id,
            data=data,
            url=h5_url,
            miniprogram=miniprogram_config if WECHAT_MP_APP_ID else None,
        )

        # 记录推送事件
        OperationTracker.track(
            user_id=user.id,
            agent_id=agent.agent_id,
            event=TrackEvent.PUSH_SENT,
            data={
                "push_type": "alert",
                "alert_rule": alert["rule_name"],
                "alert_level": level,
                "track_id": track_id,
                "push_result": "success" if ok else "failed",
            },
        )

        return ok, {"track_id": track_id, "result": result}

    # ──────── 操作追踪 ────────

    @staticmethod
    def track(
        user_id: int,
        agent_id: str,
        event: TrackEvent,
        data: Dict[str, Any] = None,
    ):
        """
        记录用户操作事件

        Args:
            user_id: 用户 ID
            agent_id: Agent ID
            event: 事件类型
            data: 事件数据
        """
        try:
            # 写入 daily_digests 的 push_result 字段（复用现有表）
            # 更完善的方案是建立独立的 events 表
            today = date.today()

            agent = Agent.query.filter_by(agent_id=agent_id).first()
            if not agent:
                return

            digest = DailyDigest.query.filter_by(
                user_id=user_id,
                agent_db_id=agent.id,
                digest_date=today,
            ).first()

            if digest:
                # 追加事件到 push_result
                existing = {}
                if digest.push_result:
                    try:
                        existing = json.loads(digest.push_result)
                    except (json.JSONDecodeError, TypeError):
                        existing = {"raw": digest.push_result}

                events = existing.get("events", [])
                events.append({
                    "event": event.value,
                    "timestamp": datetime.now().isoformat(),
                    "data": data or {},
                })
                existing["events"] = events
                digest.push_result = json.dumps(existing, ensure_ascii=False)
                db.session.commit()

            logger.debug(f"[追踪] user={user_id} agent={agent_id} event={event.value}")

        except Exception as e:
            logger.warning(f"操作追踪记录失败: {e}")

    # ──────── 推送效果分析 ────────

    @staticmethod
    def get_push_analytics(days: int = 7) -> Dict[str, Any]:
        """
        分析最近 N 天的推送效果

        Returns:
            {
                "total_pushes": int,
                "successful_pushes": int,
                "opened_count": int,
                "open_rate": float,
                "daily_breakdown": [...],
            }
        """
        start_date = date.today() - timedelta(days=days)

        digests = DailyDigest.query.filter(
            DailyDigest.digest_date >= start_date,
        ).all()

        total = len(digests)
        sent = sum(1 for d in digests if d.push_status == "sent")
        opened = 0
        actions = 0

        for d in digests:
            if d.push_result:
                try:
                    result = json.loads(d.push_result)
                    events = result.get("events", [])
                    if any(e.get("event") == TrackEvent.PUSH_OPENED.value for e in events):
                        opened += 1
                    if any(e.get("event") == TrackEvent.ACTION_TAKEN.value for e in events):
                        actions += 1
                except (json.JSONDecodeError, TypeError):
                    pass

        return {
            "period_days": days,
            "total_digests": total,
            "successful_pushes": sent,
            "opened_count": opened,
            "open_rate": round(opened / max(sent, 1) * 100, 1),
            "action_count": actions,
            "action_rate": round(actions / max(opened, 1) * 100, 1),
            "funnel": {
                "push": sent,
                "open": opened,
                "action": actions,
            },
        }

    # ──────── 批量告警检查 + 推送 ────────

    @staticmethod
    def run_alert_check(app=None):
        """
        检查所有 Agent 的告警条件并推送

        通常由定时任务调用（与 push_daily_reports 配合）
        """
        context = app.app_context() if app else _NullContext()

        with context:
            agents = Agent.query.all()
            total_alerts = 0
            total_pushed = 0

            for agent in agents:
                alerts = OperationTracker.check_alerts(agent)
                if not alerts:
                    continue

                # 只推送最高级别的告警
                critical = [a for a in alerts if a["level"] == "critical"]
                warnings = [a for a in alerts if a["level"] == "warning"]
                to_push = critical or warnings

                if not to_push:
                    continue

                total_alerts += len(to_push)
                alert = to_push[0]  # 推送最严重的一条

                # 获取关联用户
                bindings = UserAgent.query.filter_by(agent_id=agent.id).all()
                for ua in bindings:
                    user = ua.user
                    if user and user.subscribe and user.push_enabled:
                        try:
                            ok, _ = OperationTracker.send_alert(user, agent, alert, ua)
                            if ok:
                                total_pushed += 1
                        except Exception as e:
                            logger.error(f"告警推送失败: user={user.id} agent={agent.agent_id}: {e}")

            logger.info(f"[告警检查] 完成: {total_alerts} 条告警, {total_pushed} 条推送")
            return {"alerts": total_alerts, "pushed": total_pushed}


class _NullContext:
    """空上下文管理器（无 Flask app 时使用）"""
    def __enter__(self): return self
    def __exit__(self, *args): pass


# ──────── 增强推送调度器 ────────

def enhanced_push_daily_reports(app):
    """
    增强版每日推送 — 同时检查告警

    替代原 push_scheduler.push_daily_reports
    """
    from server.services.push_scheduler import push_daily_reports

    # 1. 原有每日报告推送
    push_daily_reports(app)

    # 2. 新增告警检查 + 推送
    OperationTracker.run_alert_check(app)
