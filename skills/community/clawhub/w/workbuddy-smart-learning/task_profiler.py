"""
WorkBuddy 智能学习系统 - 任务画像与执行追踪模块
功能：记录每个任务的执行轨迹，对比"有模板执行" vs "自由执行"的效率差异
"""

import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

sys.stdout.reconfigure(encoding='utf-8')


class TaskProfile:
    """单个任务的执行画像"""

    def __init__(self, workspace_root: str):
        self.workspace = Path(workspace_root)
        self.profiles_dir = self.workspace / ".workbuddy" / "memory" / "task_profiles"
        self.profiles_dir.mkdir(parents=True, exist_ok=True)
        self._current: Optional[dict] = None

    def start_task(self, task_id: str, summary: str = ""):
        """标记任务开始"""
        self._current = {
            "task_id": task_id,
            "summary": summary,
            "started_at": datetime.now().isoformat(),
            "tools": [],
            "template_used": None,
            "template_id": None,
            "ended_at": None,
            "outcome": None,
            "success": None,
            "duration_seconds": None
        }

    def use_template(self, template_id: str, template_name: str):
        """标记本次使用了模板"""
        if self._current:
            self._current["template_id"] = template_id
            self._current["template_name"] = template_name

    def record_tool_call(self, tool_name: str, success: bool, duration: float = 0.0):
        """记录工具调用"""
        if self._current:
            self._current["tools"].append({
                "tool": tool_name,
                "success": success,
                "duration": duration,
                "time": datetime.now().isoformat()
            })

    def end_task(self, outcome: str = "success", success: bool = True):
        """标记任务结束"""
        if not self._current:
            return

        self._current["ended_at"] = datetime.now().isoformat()
        self._current["outcome"] = outcome
        self._current["success"] = success

        start = datetime.fromisoformat(self._current["started_at"])
        end = datetime.fromisoformat(self._current["ended_at"])
        self._current["duration_seconds"] = round((end - start).total_seconds(), 1)

        self._save_current_profile()

    def _save_current_profile(self):
        """保存当前画像到月度文件"""
        if not self._current:
            return

        month_key = datetime.now().strftime("%Y-%m")
        profile_file = self.profiles_dir / f"profile_{month_key}.json"

        profiles = []
        if profile_file.exists():
            with open(profile_file, "r", encoding="utf-8") as f:
                profiles = json.load(f)

        new_profiles = [p for p in profiles if p.get("task_id") != self._current.get("task_id")]
        new_profiles.append(self._current)

        with open(profile_file, "w", encoding="utf-8") as f:
            json.dump(new_profiles, f, ensure_ascii=False, indent=2)

    def get_current(self) -> Optional[dict]:
        return self._current


class TaskProfilerAnalyzer:
    """任务画像分析器"""

    def __init__(self, workspace_root: str):
        self.workspace = Path(workspace_root)
        self.profiles_dir = self.workspace / ".workbuddy" / "memory" / "task_profiles"

    def _load_all_profiles(self, days: int = 30) -> list:
        """加载最近N天的画像数据"""
        profiles = []
        cutoff = datetime.now() - timedelta(days=days)

        if not self.profiles_dir.exists():
            return profiles

        for pf in self.profiles_dir.glob("profile_*.json"):
            try:
                with open(pf, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for p in data:
                        try:
                            pdate = datetime.fromisoformat(p["started_at"])
                            if pdate >= cutoff:
                                profiles.append(p)
                        except (KeyError, ValueError):
                            profiles.append(p)
            except (json.JSONDecodeError, OSError):
                continue

        return profiles

    def get_complexity_distribution(self, days: int = 30) -> dict:
        """计算任务复杂度分布"""
        profiles = self._load_all_profiles(days)
        if not profiles:
            return {"low": 0, "medium": 0, "high": 0, "total": 0}

        tool_counts = [len(p.get("tools", [])) for p in profiles]
        durations = [p.get("duration_seconds", 0) for p in profiles]

        low = sum(1 for c, d in zip(tool_counts, durations) if c <= 2 and d < 120)
        medium = sum(1 for c, d in zip(tool_counts, durations)
                     if (2 < c <= 5) or (120 <= d < 600))
        high = sum(1 for c, d in zip(tool_counts, durations) if c > 5 or d >= 600)

        return {"low": low, "medium": medium, "high": high, "total": len(profiles)}

    def compare_template_vs_free(self, days: int = 30) -> dict:
        """对比有模板 vs 自由执行"""
        profiles = self._load_all_profiles(days)

        with_template = [p for p in profiles if p.get("template_id")]
        without_template = [p for p in profiles if not p.get("template_id")]

        def stats(plist):
            if not plist:
                return {"count": 0, "success_rate": 0.0, "avg_duration": 0.0}
            success_count = sum(1 for p in plist if p.get("success"))
            durations = [p.get("duration_seconds", 0) for p in plist if p.get("duration_seconds")]
            return {
                "count": len(plist),
                "success_rate": round(success_count / len(plist), 3),
                "avg_duration": round(sum(durations) / len(durations), 1) if durations else 0.0
            }

        with_stats = stats(with_template)
        without_stats = stats(without_template)

        time_saved = 0.0
        if without_stats["avg_duration"] > 0 and with_stats["avg_duration"] > 0:
            time_saved = (
                (without_stats["avg_duration"] - with_stats["avg_duration"])
                / without_stats["avg_duration"]
            )

        return {
            "with_template": with_stats,
            "without_template": without_stats,
            "time_saved_pct": round(time_saved * 100, 1),
            "sample_size": len(profiles)
        }

    def get_tool_usage_stats(self, days: int = 30) -> list:
        """获取高频工具使用统计"""
        profiles = self._load_all_profiles(days)
        tool_counter: dict = defaultdict(lambda: {"total": 0, "success": 0})

        for p in profiles:
            for call in p.get("tools", []):
                tool = call.get("tool", "unknown")
                tool_counter[tool]["total"] += 1
                if call.get("success"):
                    tool_counter[tool]["success"] += 1

        result = []
        for tool, stats in sorted(tool_counter.items(), key=lambda x: x[1]["total"], reverse=True):
            result.append({
                "tool": tool,
                "total": stats["total"],
                "success_rate": round(stats["success"] / stats["total"], 3)
                if stats["total"] > 0 else 0.0
            })

        return result[:10]

    def generate_profiler_report(self, days: int = 30) -> str:
        """生成任务画像分析报告"""
        complexity = self.get_complexity_distribution(days)
        comparison = self.compare_template_vs_free(days)
        tool_stats = self.get_tool_usage_stats(days)
        total = complexity["total"]

        lines = [
            "=" * 50,
            "WorkBuddy 任务画像报告",
            f"统计周期：最近 {days} 天  样本: {total} 个任务",
            "=" * 50,
            "",
            "## 复杂度分布"
        ]

        if total > 0:
            lines.extend([
                f"  简单任务: {complexity['low']} ({complexity['low']/total*100:.0f}%)",
                f"  中等任务: {complexity['medium']} ({complexity['medium']/total*100:.0f}%)",
                f"  复杂任务: {complexity['high']} ({complexity['high']/total*100:.0f}%)"
            ])
        else:
            lines.append("  (暂无数据)")

        lines.extend(["", "## 模板 vs 自由执行对比"])

        wt = comparison["with_template"]
        wo = comparison["without_template"]
        lines.extend([
            f"  有模板: {wt['count']} 个 | 成功率 {wt['success_rate']*100:.0f}% | "
            f"平均 {wt['avg_duration']:.1f}s",
            f"  自由执行: {wo['count']} 个 | 成功率 {wo['success_rate']*100:.0f}% | "
            f"平均 {wo['avg_duration']:.1f}s",
            f"  时间节省: {comparison['time_saved_pct']:.1f}%"
        ])

        if tool_stats:
            lines.extend(["", "## 高频工具 Top 10"])
            for t in tool_stats:
                status = "OK" if t["success_rate"] >= 0.9 else "WARN" if t["success_rate"] >= 0.7 else "FAIL"
                lines.append(f"  [{status}] {t['tool']}: {t['total']}次 ({t['success_rate']*100:.0f}%)")
        else:
            lines.extend(["", "## 高频工具 Top 10", "  (暂无数据)"])

        lines.append("=" * 50)
        return "\n".join(lines)


def run_profiler_report(days: int = 30) -> str:
    """命令行：生成画像报告"""
    workspace = "c:/Users/Administrator/WorkBuddy/20260412210819"
    analyzer = TaskProfilerAnalyzer(workspace)
    return analyzer.generate_profiler_report(days)


if __name__ == "__main__":
    print(run_profiler_report(days=30))
