#!/usr/bin/env python3
"""
predictive_maintenance.py - 预测性维护
基于历史数据预测何时需要维护
"""
import sqlite3
import json
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict


MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / "memory"
STATS_FILE = MEMORY_DIR / ".stats_history.json"


class PredictiveMaintenance:
    """预测性维护"""
    
    def __init__(self):
        self.db_path = MEMORY_DIR / "memory.db"
        self.stats_history = self._load_stats_history()
    
    def _load_stats_history(self) -> dict:
        """加载历史统计数据"""
        if STATS_FILE.exists():
            with open(STATS_FILE) as f:
                return json.load(f)
        return {"growth": [], "queries": []}
    
    def _save_stats_history(self):
        """保存历史统计数据"""
        with open(STATS_FILE, "w") as f:
            json.dump(self.stats_history, f, indent=2)
    
    def record_stats(self, memory_count: int, query_count: int):
        """记录当前统计数据"""
        now = datetime.now().isoformat()
        
        self.stats_history.setdefault("growth", []).append({
            "date": now[:10],
            "count": memory_count,
            "queries": query_count
        })
        
        # 只保留90天数据
        cutoff = (datetime.now() - timedelta(days=90)).isoformat()
        self.stats_history["growth"] = [
            g for g in self.stats_history["growth"]
            if g["date"] >= cutoff[:10]
        ]
        
        self._save_stats_history()
    
    def predict_growth(self) -> dict:
        """预测记忆增长"""
        growth = self.stats_history.get("growth", [])
        if len(growth) < 7:
            return {
                "predicted_30d": "数据不足",
                "daily_avg": "数据不足",
                "trend": "unknown"
            }
        
        # 计算日均增长
        recent = growth[-7:]
        total_growth = sum(g[-1]["count"] - g[0]["count"] for g in [recent])
        daily_avg = total_growth / 7 if len(recent) > 1 else 0
        
        # 预测30天后
        current = growth[-1]["count"] if growth else 0
        predicted_30d = current + (daily_avg * 30)
        
        # 判断趋势
        if len(growth) >= 14:
            older = growth[-14:-7]
            newer = growth[-7:]
            older_avg = sum(g[-1]["count"] - g[0]["count"] for g in [older]) / 7
            newer_avg = sum(g[-1]["count"] - g[0]["count"] for g in [newer]) / 7
            
            if newer_avg > older_avg * 1.2:
                trend = "📈 加速增长"
            elif newer_avg < older_avg * 0.8:
                trend = "📉 增长放缓"
            else:
                trend = "➡️ 稳定增长"
        else:
            trend = "➡️ 稳定"
        
        return {
            "current": current,
            "predicted_30d": round(predicted_30d),
            "daily_avg": round(daily_avg, 1),
            "trend": trend
        }
    
    def check_maintenance_needs(self) -> list:
        """检查维护需求"""
        needs = []
        
        # 检查数据库大小
        if self.db_path.exists():
            size_mb = self.db_path.stat().st_size / 1024 / 1024
            if size_mb > 50:
                needs.append({
                    "type": "db_size",
                    "severity": "high",
                    "message": f"数据库过大 ({size_mb:.1f}MB)",
                    "action": "建议执行 VACUUM"
                })
            elif size_mb > 30:
                needs.append({
                    "type": "db_size",
                    "severity": "medium",
                    "message": f"数据库较大 ({size_mb:.1f}MB)",
                    "action": "可考虑 VACUUM"
                })
        
        # 检查遗忘检测
        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute(
            "SELECT COUNT(*) FROM memories WHERE type = 'episodic' AND last_accessed < ?",
            ((datetime.now() - timedelta(days=30)).isoformat(),)
        )
        old_memories = cursor.fetchone()[0]
        conn.close()
        
        if old_memories > 100:
            needs.append({
                "type": "old_memories",
                "severity": "low",
                "message": f"有 {old_memories} 条记忆超过30天未访问",
                "action": "可考虑归档或删除"
            })
        
        return needs
    
    def get_maintenance_schedule(self) -> dict:
        """获取维护计划"""
        needs = self.check_maintenance_needs()
        growth = self.predict_growth()
        
        schedule = {
            "daily": [],
            "weekly": [],
            "monthly": [],
            "predictions": growth,
            "alerts": needs
        }
        
        # 基于预测添加建议
        if growth.get("daily_avg", 0) > 10:
            schedule["weekly"].append({
                "task": "检查点-1",
                "description": "记忆增长较快，建议加强遗忘检测"
            })
        
        # 基于告警添加建议
        for need in needs:
            if need["severity"] == "high":
                schedule["daily"].append({
                    "task": "紧急维护",
                    "description": need["message"],
                    "action": need["action"]
                })
        
        return schedule


def main():
    print("🔮 预测性维护分析")
    print("=" * 40)
    
    pm = PredictiveMaintenance()
    
    # 预测
    print("\n📈 增长预测:")
    pred = pm.predict_growth()
    for k, v in pred.items():
        print(f"  {k}: {v}")
    
    # 维护需求
    print("\n🔧 维护需求:")
    needs = pm.check_maintenance_needs()
    if not needs:
        print("  ✅ 无需维护")
    else:
        for need in needs:
            icon = "🔴" if need["severity"] == "high" else "🟡" if need["severity"] == "medium" else "🟢"
            print(f"  {icon} {need['message']}")
            print(f"      操作: {need['action']}")
    
    # 维护计划
    print("\n📅 维护计划:")
    schedule = pm.get_maintenance_schedule()
    
    if schedule["daily"]:
        print("  每日:")
        for task in schedule["daily"]:
            print(f"    - {task['task']}: {task['description']}")
    
    if schedule["weekly"]:
        print("  每周:")
        for task in schedule["weekly"]:
            print(f"    - {task['task']}: {task['description']}")
    
    if not any(schedule.values()):
        print("  ✅ 无待执行维护任务")


if __name__ == "__main__":
    main()
