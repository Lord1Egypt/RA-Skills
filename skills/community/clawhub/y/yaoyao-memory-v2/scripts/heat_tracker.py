#!/usr/bin/env python3
"""
记忆热度追踪模块 - v1.0.0
统计记忆被引用次数，追踪热度变化

功能：
1. 记录每次记忆被搜索/引用的时间
2. 统计累计引用次数
3. 标记冷记忆（长期未被引用）
4. 生成热度报告
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
from collections import defaultdict

# 配置
MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / "memory"
HEAT_FILE = MEMORY_DIR / ".heat_data.json"

# 热度阈值
HOT_THRESHOLD = 5       # 累计引用 >5 为热记忆
COLD_THRESHOLD = 0      # 累计引用 =0 为冷记忆
RECENCY_WEIGHT = 0.3    # 最近引用权重因子

class HeatTracker:
    """记忆热度追踪器"""
    
    def __init__(self):
        self.memory_dir = MEMORY_DIR
        self.heat_file = HEAT_FILE
        self._load_data()
    
    def _load_data(self):
        """加载热度数据"""
        if self.heat_file.exists():
            try:
                self.data = json.loads(self.heat_file.read_text(encoding="utf-8"))
            except:
                self.data = {"access_log": [], "memory_stats": {}}
        else:
            self.data = {"access_log": [], "memory_stats": {}}
    
    def _save_data(self):
        """保存热度数据"""
        try:
            self.heat_file.parent.mkdir(parents=True, exist_ok=True)
            self.heat_file.write_text(json.dumps(self.data, ensure_ascii=False), encoding="utf-8")
        except:
            pass
    
    def record_access(self, memory_id: str, memory_title: str = ""):
        """
        记录一次记忆访问
        - memory_id: 记忆ID或标题
        - memory_title: 记忆标题（可选）
        """
        now = datetime.now()
        
        # 记录访问日志
        self.data["access_log"].append({
            "memory_id": memory_id,
            "title": memory_title,
            "timestamp": now.isoformat(),
            "date": now.strftime("%Y-%m-%d")
        })
        
        # 更新统计
        if memory_id not in self.data["memory_stats"]:
            self.data["memory_stats"][memory_id] = {
                "title": memory_title,
                "total_access": 0,
                "first_access": now.isoformat(),
                "last_access": now.isoformat(),
                "access_dates": []
            }
        
        stats = self.data["memory_stats"][memory_id]
        stats["total_access"] += 1
        stats["last_access"] = now.isoformat()
        if now.strftime("%Y-%m-%d") not in stats["access_dates"]:
            stats["access_dates"].append(now.strftime("%Y-%m-%d"))
        
        self._save_data()
    
    def get_memory_heat(self, memory_id: str) -> Dict:
        """获取单条记忆的热度信息"""
        if memory_id not in self.data["memory_stats"]:
            return {
                "memory_id": memory_id,
                "total_access": 0,
                "heat_level": "cold",
                "days_since_access": None
            }
        
        stats = self.data["memory_stats"][memory_id]
        last_access = datetime.fromisoformat(stats["last_access"])
        days_since = (datetime.now() - last_access).days
        
        # 计算热度等级
        if stats["total_access"] > HOT_THRESHOLD and days_since <= 7:
            heat_level = "hot"
        elif stats["total_access"] > COLD_THRESHOLD:
            heat_level = "warm"
        else:
            heat_level = "cold"
        
        return {
            "memory_id": memory_id,
            "title": stats.get("title", ""),
            "total_access": stats["total_access"],
            "access_dates_count": len(stats["access_dates"]),
            "first_access": stats["first_access"],
            "last_access": stats["last_access"],
            "days_since_access": days_since,
            "heat_level": heat_level
        }
    
    def get_hot_memories(self, limit: int = 10) -> List[Dict]:
        """获取最热门的记忆"""
        all_heats = [
            self.get_memory_heat(mid) 
            for mid in self.data["memory_stats"].keys()
        ]
        # 按访问次数排序
        sorted_heats = sorted(
            all_heats, 
            key=lambda x: x["total_access"], 
            reverse=True
        )
        return sorted_heats[:limit]
    
    def get_cold_memories(self, limit: int = 10) -> List[Dict]:
        """获取最冷的记忆（长期未访问）"""
        all_heats = [
            self.get_memory_heat(mid) 
            for mid in self.data["memory_stats"].keys()
        ]
        # 按最后访问时间排序（最老的在前）
        cold = [h for h in all_heats if h["days_since_access"] is not None]
        sorted_cold = sorted(cold, key=lambda x: x["days_since_access"], reverse=True)
        return sorted_cold[:limit]
    
    def analyze(self) -> Dict:
        """分析整体热度"""
        stats = self.data["memory_stats"]
        
        if not stats:
            return {
                "total_tracked": 0,
                "hot_count": 0,
                "warm_count": 0,
                "cold_count": 0,
                "total_access": 0,
                "avg_access": 0
            }
        
        all_heats = [self.get_memory_heat(mid) for mid in stats.keys()]
        
        hot = len([h for h in all_heats if h["heat_level"] == "hot"])
        warm = len([h for h in all_heats if h["heat_level"] == "warm"])
        cold = len([h for h in all_heats if h["heat_level"] == "cold"])
        
        total_access = sum(h["total_access"] for h in all_heats)
        avg_access = total_access / len(all_heats) if all_heats else 0
        
        return {
            "total_tracked": len(stats),
            "hot_count": hot,
            "warm_count": warm,
            "cold_count": cold,
            "total_access": total_access,
            "avg_access": round(avg_access, 2),
            "hot_threshold": HOT_THRESHOLD,
            "cold_threshold": COLD_THRESHOLD
        }
    
    def report(self) -> str:
        """生成热度报告"""
        analysis = self.analyze()
        hot_memories = self.get_hot_memories(5)
        cold_memories = self.get_cold_memories(5)
        
        lines = [
            "📊 记忆热度报告",
            "=" * 40,
            f"追踪记忆: {analysis['total_tracked']}",
            f"总访问: {analysis['total_access']}",
            f"平均访问: {analysis['avg_access']}",
            "",
            f"🔥 热记忆: {analysis['hot_count']}",
            f"🌡️ 温记忆: {analysis['warm_count']}",
            f"❄️ 冷记忆: {analysis['cold_count']}",
            "",
        ]
        
        if hot_memories:
            lines.append("🔥 TOP 热度记忆:")
            for h in hot_memories[:3]:
                lines.append(f"  • {h['title'] or h['memory_id'][:20]} ({h['total_access']}次)")
        
        if cold_memories:
            lines.append("")
            lines.append("❄️ 最久未访问:")
            for c in cold_memories[:3]:
                days = c['days_since_access'] or 0
                lines.append(f"  • {c['title'] or c['memory_id'][:20]} ({days}天未访问)")
        
        return "\n".join(lines)


if __name__ == "__main__":
    tracker = HeatTracker()
    print(tracker.report())
