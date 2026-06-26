"""
Data Cleaner - 数据清洗模块
整合现有数据格式,提供标准化接口
"""

import os
import json
from datetime import datetime, timedelta
from lib.tz import cutoff_str
from typing import Dict, List

# 路径配置 - 使用环境变量或相对路径
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # lib/ -> whoop-guru/
WORKSPACE_DIR = os.environ.get("OPENCLAW_WORKSPACE", os.path.dirname(os.path.dirname(SKILL_DIR)))  # whoop-guru/ -> skill/ -> workspace
PROCESSED_DIR = os.environ.get("WHOOP_DATA_DIR", os.path.join(WORKSPACE_DIR, "data", "processed"))


class WhoopDataProvider:
    """WHOOP数据提供者 - 从现有数据系统获取"""

    def __init__(self):
        self.latest_file = os.path.join(PROCESSED_DIR, "latest.json")

    def get_latest_data(self) -> Dict:
        """获取最新数据"""
        if not os.path.exists(self.latest_file):
            return {}
        try:
            with open(self.latest_file, 'r') as f:
                return json.load(f)
        except Exception:
            return {}

    def get_metrics(self) -> Dict:
        """获取聚合指标"""
        data = self.get_latest_data()
        return data.get("metrics", {})

    def get_processed_recovery(self, days: int = 7) -> List[Dict]:
        """获取处理后的恢复记录"""
        data = self.get_latest_data()
        processed = data.get("processed", {})
        recovery = processed.get("recovery", [])

        cutoff = cutoff_str(days)

        return [r for r in recovery if r.get("date", "") >= cutoff]

    def get_processed_sleep(self, days: int = 7) -> List[Dict]:
        """获取处理后的睡眠记录"""
        data = self.get_latest_data()
        processed = data.get("processed", {})
        sleep = processed.get("sleep", [])

        cutoff = cutoff_str(days)

        return [s for s in sleep if s.get("date", "") >= cutoff]


class DataAggregator:
    """数据聚合器"""

    def __init__(self):
        self.provider = WhoopDataProvider()

    def get_coach_summary(self, days: int = 7) -> Dict:
        """获取教练汇总数据"""
        metrics = self.provider.get_metrics()
        recovery = self.provider.get_processed_recovery(days)
        sleep = self.provider.get_processed_sleep(days)

        # 从metrics获取汇总数据
        return {
            "days": days,
            "avg_recovery": metrics.get("avg_recovery", 0),
            "avg_hrv": metrics.get("avg_hrv", 0),
            "avg_rhr": metrics.get("avg_rhr", 0),
            "avg_sleep_hours": metrics.get("avg_sleep_hours", 0),
            "total_strain": metrics.get("total_strain", 0),
            "training_days": metrics.get("workout_count", 0),
            "sleep_debt": metrics.get("sleep_debt_estimate", 0),
            "recovery_count": len(recovery),
            "sleep_count": len(sleep),
            "recovery_trend": self._calc_trend(recovery),
        }

    def _calc_trend(self, recovery: List[Dict]) -> str:
        """计算恢复趋势"""
        if len(recovery) < 3:
            return "stable"

        values = [r.get("recovery_score", 50) for r in recovery]
        recent = sum(values[:3]) / 3
        older = sum(values[3:6]) / 3 if len(values) > 5 else recent

        diff = recent - older
        if diff > 5:
            return "up"
        elif diff < -5:
            return "down"
        return "stable"

    def get_today_status(self) -> Dict:
        """获取今日状态"""
        data = self.provider.get_latest_data()
        metrics = data.get("metrics", {})

        # 今日数据从最新记录获取
        processed = data.get("processed", {})
        recovery = processed.get("recovery", [])
        sleep = processed.get("sleep", [])

        today_recovery = recovery[0] if recovery else {}
        today_sleep = sleep[0] if sleep else {}

        return {
            "date": today_recovery.get("date", ""),
            "recovery": today_recovery.get("recovery_score", 0),
            "hrv": today_recovery.get("hrv", 0),
            "rhr": today_recovery.get("rhr", 0),
            "sleep_hours": today_sleep.get("total_in_bed_hours", 0),
        }


def get_whoop_data(days: int = 7) -> Dict:
    """获取WHOOP数据"""
    aggregator = DataAggregator()
    return aggregator.get_coach_summary(days)


def get_today_data() -> Dict:
    """获取今日数据"""
    aggregator = DataAggregator()
    return aggregator.get_today_status()


if __name__ == "__main__":
    print("Testing WhoopDataProvider...")
    provider = WhoopDataProvider()
    metrics = provider.get_metrics()
    print(f"Metrics: {json.dumps(metrics, indent=2)}")

    print("\nTesting DataAggregator...")
    aggregator = DataAggregator()
    summary = aggregator.get_coach_summary(7)
    print(f"Coach summary: {json.dumps(summary, indent=2)}")
