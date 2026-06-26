"""
Weekly Report - 周报生成模块
生成训练周报
"""

import os
import json
from datetime import datetime, timedelta
from typing import Dict, List

# 数据路径 - 使用环境变量
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # reports/ -> lib/ -> whoop-guru/
WORKSPACE_DIR = os.environ.get("OPENCLAW_WORKSPACE", os.path.dirname(os.path.dirname(SKILL_DIR)))  # whoop-guru/ -> skill/ -> workspace
PROCESSED_DIR = os.environ.get("WHOOP_DATA_DIR", os.path.join(WORKSPACE_DIR, "data", "processed"))
DATA_FILE = os.path.join(PROCESSED_DIR, "latest.json")
GOALS_DIR = os.path.join(SKILL_DIR, "data", "profiles")


class WeeklyReporter:
    """周报生成器"""
    
    def __init__(self, user_id: str = "default"):
        self.user_id = user_id
        self.goals_file = os.path.join(GOALS_DIR, f"goals_{user_id}.json")
    
    def load_data(self) -> Dict:
        """加载数据"""
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except Exception:
            return {}
    
    def generate_weekly_report(self) -> Dict:
        """生成周报"""
        data = self.load_data()
        metrics = data.get("metrics", {})
        processed = data.get("processed", {})
        
        # 本周数据
        recovery = processed.get("recovery", [])[:7]
        sleep = processed.get("sleep", [])[:7]
        
        # 计算统计数据
        avg_recovery = metrics.get("avg_recovery", 0)
        avg_hrv = metrics.get("avg_hrv", 0)
        avg_rhr = metrics.get("avg_rhr", 0)
        avg_sleep = metrics.get("avg_sleep_hours", 0)
        training_days = metrics.get("workout_count", 0)
        total_strain = metrics.get("total_strain", 0)
        sleep_debt = metrics.get("sleep_debt_estimate", 0)
        
        # 计算恢复趋势
        if len(recovery) >= 3:
            recent = sum(r.get("recovery_score", 0) for r in recovery[:3]) / 3
            older = sum(r.get("recovery_score", 0) for r in recovery[3:6]) / 3 if len(recovery) > 5 else recent
            trend_change = recent - older
            if trend_change > 3:
                recovery_trend = "📈 上升"
            elif trend_change < -3:
                recovery_trend = "📉 下降"
            else:
                recovery_trend = "➡️ 稳定"
        else:
            recovery_trend = "➡️ 稳定"
        
        # 训练状态
        if total_strain >= 70:
            training_status = "💪 训练充实"
        elif total_strain >= 40:
            training_status = "🏃 训练适度"
        else:
            training_status = "😴 训练不足"
        
        # 恢复评价
        if avg_recovery >= 75:
            recovery_status = "🟢 优秀"
        elif avg_recovery >= 55:
            recovery_status = "🟡 一般"
        else:
            recovery_status = "🔴 较差"
        
        # 睡眠评价
        if avg_sleep >= 7.5:
            sleep_status = "✅ 睡眠充足"
        elif avg_sleep >= 6:
            sleep_status = "⚠️ 睡眠偏少"
        else:
            sleep_status = "❌ 睡眠不足"
        
        # 周几
        week_num = datetime.now().isocalendar()[1]
        
        report = {
            "type": "weekly",
            "generated_at": datetime.now().isoformat(),
            "week": f"第{week_num}周",
            "stats": {
                "avg_recovery": round(avg_recovery, 1),
                "avg_hrv": round(avg_hrv, 1),
                "avg_rhr": round(avg_rhr, 1),
                "avg_sleep_hours": round(avg_sleep, 1),
                "training_days": training_days,
                "total_strain": round(total_strain, 1),
                "sleep_debt": round(sleep_debt, 1),
            },
            "status": {
                "recovery_trend": recovery_trend,
                "training_status": training_status,
                "recovery_status": recovery_status,
                "sleep_status": sleep_status,
            },
            "message": self._format_message(avg_recovery, training_days, avg_sleep, sleep_debt, recovery_trend),
        }
        
        return report
    
    def _format_message(self, recovery: float, training_days: int, sleep: float, sleep_debt: float, recovery_trend: str) -> str:
        """格式化周报消息"""
        # 本周总结
        msg = f"""📊 **本周训练周报**

━━━━━━━━━━━━━━━
📈 **数据统计**
平均恢复：{recovery:.0f}% {recovery_trend}
训练天数：{training_days}天
睡眠时长：{sleep:.1f}小时
睡眠债务：{sleep_debt:.1f}小时
━━━━━━━━━━━━━━━

"""
        
        # 恢复评价
        if recovery >= 75:
            msg += "💪 **恢复状态优秀**\n"
            msg += "身体状态很好，可以适当提高训练强度\n\n"
        elif recovery >= 55:
            msg += "⚖️ **恢复状态一般**\n"
            msg += "注意休息和睡眠质量\n\n"
        else:
            msg += "🔴 **恢复状态欠佳**\n"
            msg += "建议降低训练强度，增加休息\n\n"
        
        # 训练评价
        if training_days >= 5:
            msg += "💪 训练很充实，保持好状态！\n\n"
        elif training_days >= 3:
            msg += "🏃 训练适中，继续保持\n\n"
        else:
            msg += "📝 训练较少，可适当增加\n\n"
        
        # 睡眠建议
        if sleep_debt > 10:
            msg += "⚠️ 睡眠债务较重，本周重点补觉\n"
        elif sleep_debt > 5:
            msg += "⚠️ 有一定睡眠债务，注意休息\n"
        
        return msg


def generate_weekly_report(user_id: str = "default") -> Dict:
    """生成周报"""
    reporter = WeeklyReporter(user_id)
    return reporter.generate_weekly_report()


if __name__ == "__main__":
    print("=== Weekly Report ===")
    reporter = WeeklyReporter()
    report = reporter.generate_weekly_report()
    print(f"Week: {report['week']}")
    print(f"Avg Recovery: {report['stats']['avg_recovery']}%")
    print(f"Training Days: {report['stats']['training_days']}")
    print("\nMessage:")
    print(report['message'])
