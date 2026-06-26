#!/usr/bin/env python3
from datetime import datetime


class MessageFormatter:
    @staticmethod
    def task_report(
        task_name: str, status: str, message: str = "", details: str = ""
    ) -> str:
        status_emoji = {
            "success": "✅",
            "failed": "❌",
            "running": "🔄",
            "warning": "⚠️",
            "info": "ℹ️",
        }.get(status.lower(), "ℹ️")

        report = f"""📋 任务报告

━━━━━━━━━━
🏷️ 任务名称: {task_name}
📊 执行状态: {status_emoji} {status.upper()}
⏰ 执行时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
━━━━━━━━━━"""

        if message:
            report += f"\n📝 简要说明: {message}"

        if details:
            report += f"\n📌 详细信息:\n{details}"

        return report

    @staticmethod
    def job_notification(job_name: str, event: str, message: str = "") -> str:
        event_emoji = {
            "started": "🚀",
            "completed": "🏁",
            "failed": "💥",
            "scheduled": "⏰",
        }.get(event.lower(), "📌")

        return f"""🚀 任务通知

━━━━━━━━━━
📦 任务名称: {job_name}
📌 事件类型: {event_emoji} {event}
⏰ 通知时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
━━━━━━━━━━

{message}"""

    @staticmethod
    def system_alert(level: str, title: str, message: str, details: str = "") -> str:
        level_config = {
            "critical": ("🔴 严重", "🚨"),
            "error": ("🟠 错误", "❌"),
            "warning": ("🟡 警告", "⚠️"),
            "info": ("🔵 信息", "ℹ️"),
        }.get(level.lower(), ("🔵 信息", "ℹ️"))

        alert_emoji, level_text = level_config

        alert = f"""🚨 系统告警

━━━━━━━━━━
⚠️ 告警级别: {alert_emoji} {level_text}
📌 告警标题: {title}
⏰ 发生时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
━━━━━━━━━━

📝 告警内容:
{message}"""

        if details:
            alert += f"\n\n📌 处理建议:\n{details}"

        return alert

    @staticmethod
    def daily_summary(date: str = "", stats: dict = None, highlights: str = "") -> str:
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")

        summary = f"""📊 每日汇总

━━━━━━━━━━
📅 汇总日期: {date}
⏰ 生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
━━━━━━━━━━"""

        if stats:
            summary += "\n\n📈 统计数据:"
            for key, value in stats.items():
                summary += f"\n  • {key}: {value}"

        if highlights:
            summary += f"\n\n✨ 今日要点:\n{highlights}"

        return summary

    @staticmethod
    def custom(title: str, content: str = "", fields: dict = None) -> str:
        msg = f"""📌 {title}

━━━━━━━━━━"""

        if content:
            msg += f"\n{content}"

        if fields:
            for key, value in fields.items():
                msg += f"\n  • {key}: {value}"

        return msg


if __name__ == "__main__":
    print(
        MessageFormatter.task_report(
            task_name="数据备份",
            status="success",
            message="数据库备份任务已成功完成",
            details="备份文件: backup_2024.db\n备份大小: 1.2GB\n耗时: 5分30秒",
        )
    )
