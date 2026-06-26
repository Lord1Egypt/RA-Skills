#!/usr/bin/env python3
"""
记忆可视化模块 - v1.0.0
生成记忆系统的可视化展示

功能：
1. 记忆分布 ASCII 可视化
2. 热度条形图
3. 记忆结构树状图
4. 生成统计图表（文本格式）
"""

import sys
from pathlib import Path
from collections import Counter
from datetime import datetime, timedelta

sys.path.insert(0, str(Path(__file__).parent))

from forget_detector import ForgetDetector
from heat_tracker import HeatTracker
from memory_stats import MemoryStats

MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / "memory"

class MemoryViz:
    """记忆可视化器"""
    
    def __init__(self):
        self.memory_dir = MEMORY_DIR
        self.forget_detector = ForgetDetector()
        self.heat_tracker = HeatTracker()
        self.stats = MemoryStats()
    
    def bar_chart(self, data: dict, max_width: int = 40, title: str = "") -> str:
        """生成横向条形图"""
        if not data:
            return ""
        
        max_val = max(data.values())
        if max_val == 0:
            max_val = 1
        
        lines = []
        if title:
            lines.append(title)
            lines.append("-" * len(title))
        
        for key, val in sorted(data.items(), key=lambda x: x[1], reverse=True):
            bar_len = int(val / max_val * max_width)
            bar = "█" * bar_len
            lines.append(f"{key:15} {bar} {val}")
        
        return "\n".join(lines)
    
    def memory_tree(self, limit: int = 10) -> str:
        """生成记忆树状图"""
        memories = sorted(
            self.memory_dir.glob("*.md"),
            key=lambda x: x.stat().st_mtime,
            reverse=True
        )
        memories = [m for m in memories if not m.name.startswith('.') and '合并版' not in m.name][:limit]
        
        lines = ["📂 记忆结构", "=" * 40]
        
        for i, m in enumerate(memories, 1):
            stat = m.stat()
            mtime = datetime.fromtimestamp(stat.st_mtime)
            age = (datetime.now() - mtime).days
            
            # 根据年龄选择图标
            if age == 0:
                icon = "🆕"
            elif age <= 3:
                icon = "🔥"
            elif age <= 7:
                icon = "📅"
            elif age <= 30:
                icon = "📆"
            else:
                icon = "📚"
            
            # 截断文件名
            name = m.stem[:25]
            size = stat.st_size
            
            lines.append(f"{icon} {name}")
            lines.append(f"   └─ {size:>5} bytes | {mtime.strftime('%m-%d %H:%M')}")
        
        return "\n".join(lines)
    
    def heat_map(self, days: int = 7) -> str:
        """生成热度热力图（文本版）"""
        memories = list(self.memory_dir.glob("*.md"))
        memories = [m for m in memories if not m.name.startswith('.') and '合并版' not in m.name]
        
        # 按小时统计
        hour_counts = Counter()
        
        for m in memories:
            try:
                mtime = datetime.fromtimestamp(m.stat().st_mtime)
                if (datetime.now() - mtime).days <= days:
                    hour_key = mtime.strftime("%H:00")
                    hour_counts[hour_key] += 1
            except:
                pass
        
        if not hour_counts:
            return "📊 热力图：暂无数据"
        
        # 找到最大值
        max_val = max(hour_counts.values()) if hour_counts else 1
        
        # 生成热力图
        lines = ["📊 热度热力图（最近7天）", "=" * 40]
        
        # 按小时排序
        for hour in sorted(hour_counts.keys()):
            count = hour_counts[hour]
            # 字符密度表示热度
            density = min(count / max_val, 1.0)
            
            if density >= 0.8:
                bar = "████████"
            elif density >= 0.6:
                bar = "██████░░"
            elif density >= 0.4:
                bar = "████░░░░"
            elif density >= 0.2:
                bar = "██░░░░░░"
            else:
                bar = "█░░░░░░░"
            
            lines.append(f"{hour} {bar} {count}")
        
        return "\n".join(lines)
    
    def type_distribution(self) -> str:
        """类型分布可视化"""
        type_stats = self.stats.type_analysis()
        dist = type_stats.get("distribution", {})
        
        if not dist:
            return "📊 类型分布：暂无数据"
        
        total = sum(dist.values())
        
        lines = ["📊 类型分布", "=" * 40]
        
        # 饼图（ASCII版）
        for mem_type, count in sorted(dist.items(), key=lambda x: x[1], reverse=True):
            pct = count / total * 100 if total > 0 else 0
            bar_len = int(pct / 5)  # 每5%一个方块
            bar = "■" * bar_len + "□" * (20 - bar_len)
            lines.append(f"{mem_type:12} {bar} {pct:5.1f}%")
        
        return "\n".join(lines)
    
    def forget_risk_view(self) -> str:
        """遗忘风险视图"""
        analysis = self.forget_detector.analyze()
        
        cold = analysis.get("cold", [])
        warm = analysis.get("warm", [])
        hot = analysis.get("hot", [])
        
        lines = [
            "⚠️ 遗忘风险视图",
            "=" * 40,
            f"🔥 热记忆: {len(hot)}",
            f"🌡️ 温记忆: {len(warm)}",
            f"❄️ 冷记忆: {len(cold)}",
            "",
        ]
        
        if cold:
            lines.append("❄️ 需要关注的冷记忆:")
            for m in cold[:5]:
                days = m.get("days_since_modified", 0)
                score = m.get("forget_score", 0)
                lines.append(f"   • {m.get('file', m.get('id', 'unknown'))[:30]}")
                lines.append(f"     {days}天未修改 | 遗忘分数: {score}")
        
        return "\n".join(lines)
    
    def full_dashboard(self) -> str:
        """完整仪表盘"""
        lines = [
            "╔" + "═" * 48 + "╗",
            "║" + " 📊 yaoyao-memory 仪表盘 ".center(48) + "║",
            "╠" + "═" * 48 + "╣",
        ]
        
        # 统计信息
        time_stats = self.stats.time_analysis()
        total = time_stats.get("total", 0)
        
        lines.append(f"║  总记忆数: {total:>3} 个" + " " * 33 + "║")
        
        # 类型分布
        type_stats = self.stats.type_analysis()
        dist = type_stats.get("distribution", {})
        
        if dist:
            top_type = max(dist.items(), key=lambda x: x[1])
            lines.append(f"║  主要类型: {top_type[0]} ({top_type[1]}个)" + " " * 27 + "║")
        
        # 热度分布
        forget_analysis = self.forget_detector.analyze()
        hot = forget_analysis.get("hot_count", 0)
        warm = forget_analysis.get("warm_count", 0)
        cold = forget_analysis.get("cold_count", 0)
        
        lines.append(f"║  热度分布: 🔥{hot} 🌡️{warm} ❄️{cold}" + " " * 27 + "║")
        
        # 风险
        risk = len(forget_analysis.get("high_risk", []))
        
        risk_icon = "⚠️" if risk > 0 else "✅"
        lines.append(f"║  高风险: {risk_icon} {risk} 个" + " " * 34 + "║")
        
        lines.append("╚" + "═" * 48 + "╝")
        
        return "\n".join(lines)
    
    def report(self) -> str:
        """生成完整可视化报告"""
        parts = [
            self.full_dashboard(),
            "",
            self.memory_tree(),
            "",
            self.type_distribution(),
            "",
            self.heat_map(),
            "",
            self.forget_risk_view(),
        ]
        
        return "\n".join(parts)


if __name__ == "__main__":
    viz = MemoryViz()
    print(viz.report())
