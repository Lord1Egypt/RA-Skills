"""
WorkBuddy 智能学习系统 - 隐式信号采集模块
功能：无感采集5类行为信号，为模式识别和知识蒸馏提供数据基础
"""

import json
import os
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

# Windows UTF-8 兼容
sys.stdout.reconfigure(encoding='utf-8')


class SignalCollector:
    """
    隐式信号采集器
    采集5类行为信号：
    1. 反馈填写率（显式反馈 vs 任务总量）
    2. 任务取消率（用户中断/撤回）
    3. 任务时长（执行效率代理）
    4. 工具成功率（工具调用质量）
    5. 重复修正率（同一任务是否被多次修正）
    """

    def __init__(self, workspace_root: str):
        self.workspace = Path(workspace_root)
        self.signals_dir = self.workspace / ".workbuddy" / "memory" / "signals"
        self.signals_dir.mkdir(parents=True, exist_ok=True)

        # 内存缓存（单次会话内）
        self._session_tasks: dict = {}  # task_id -> {start_time, tool_calls, ended, outcome}
        self._tool_stats: dict = defaultdict(lambda: {"total": 0, "success": 0})

    # ─── 记录 API ────────────────────────────────────────────

    def record_task_start(self, task_id: str, task_summary: str = ""):
        """记录任务开始"""
        self._session_tasks[task_id] = {
            "task_summary": task_summary,
            "start_time": datetime.now().isoformat(),
            "tool_calls": [],
            "ended": False,
            "outcome": None
        }

    def record_tool_call(self, task_id: str, tool_name: str, success: bool):
        """记录工具调用结果"""
        self._tool_stats[tool_name]["total"] += 1
        if success:
            self._tool_stats[tool_name]["success"] += 1

        if task_id in self._session_tasks:
            self._session_tasks[task_id]["tool_calls"].append({
                "tool": tool_name,
                "success": success,
                "time": datetime.now().isoformat()
            })

    def record_task_metric(self, task_id: str, metric_type: str, value):
        """记录自定义任务指标"""
        if task_id in self._session_tasks:
            metrics = self._session_tasks[task_id].setdefault("custom_metrics", {})
            metrics[metric_type] = value

    def record_task_end(self, task_id: str, outcome: str = "success",
                        cancelled: bool = False, notes: str = ""):
        """记录任务结束"""
        if task_id not in self._session_tasks:
            return

        task = self._session_tasks[task_id]
        task["ended"] = True
        task["outcome"] = outcome
        task["cancelled"] = cancelled
        task["end_time"] = datetime.now().isoformat()
        task["notes"] = notes

        # 追加到历史信号文件
        self._flush_task_signal(task, task_id)

    def flush_session(self):
        """将会话内未结束的任务flush到磁盘（用于会话结束时的兜底保存）"""
        for task_id, task in self._session_tasks.items():
            if not task["ended"]:
                task["outcome"] = "unknown"
                task["ended"] = True
                self._flush_task_signal(task, task_id)

    # ─── 读取 API ────────────────────────────────────────────

    def get_signal_data(self, days: int = 7) -> list:
        """获取最近N天的信号数据"""
        signals = []
        cutoff = datetime.now() - timedelta(days=days)

        for sig_file in self.signals_dir.glob("*.json"):
            try:
                sig_date = datetime.strptime(sig_file.stem, "%Y-%m-%d")
                if sig_date < cutoff:
                    continue
            except ValueError:
                continue

            with open(sig_file, "r", encoding="utf-8") as f:
                signals.extend(json.load(f))

        return signals

    def get_feedback_rate(self, days: int = 7) -> float:
        """
        计算反馈填写率
        = 有显式反馈的任务数 / 总任务数
        """
        signals = self.get_signal_data(days)
        if not signals:
            return 0.0

        total = len(signals)
        with_feedback = sum(1 for s in signals if s.get("has_feedback"))
        return round(with_feedback / total, 3) if total > 0 else 0.0

    def get_cancel_rate(self, days: int = 7) -> float:
        """计算任务取消率"""
        signals = self.get_signal_data(days)
        if not signals:
            return 0.0

        total = len(signals)
        cancelled = sum(1 for s in signals if s.get("cancelled"))
        return round(cancelled / total, 3) if total > 0 else 0.0

    def get_avg_task_duration_seconds(self, days: int = 7) -> float:
        """计算平均任务时长（秒）"""
        signals = self.get_signal_data(days)
        durations = []

        for s in signals:
            dur = s.get("duration_seconds")
            if dur and dur > 0:
                durations.append(dur)

        return round(sum(durations) / len(durations), 1) if durations else 0.0

    def get_tool_success_rates(self, days: int = 7) -> dict:
        """获取各工具成功率"""
        signals = self.get_signal_data(days)
        tool_totals: dict = defaultdict(lambda: {"total": 0, "success": 0})

        for s in signals:
            for call in s.get("tool_calls", []):
                tool = call.get("tool", "unknown")
                tool_totals[tool]["total"] += 1
                if call.get("success"):
                    tool_totals[tool]["success"] += 1

        return {
            tool: round(stats["success"] / stats["total"], 3)
            if stats["total"] > 0 else 0.0
            for tool, stats in tool_totals.items()
        }

    def get_repeat_rate(self, days: int = 7) -> float:
        """计算重复修正率（同一任务被重复执行的比例）"""
        signals = self.get_signal_data(days)
        if not signals:
            return 0.0

        # 按任务摘要聚合
        summary_count: Counter = Counter()
        for s in signals:
            summary = s.get("task_summary", "")[:50]  # 取前50字符作聚合键
            if summary:
                summary_count[summary] += 1

        repeated = sum(1 for c in summary_count.values() if c > 1)
        total = len(summary_count)
        return round(repeated / total, 3) if total > 0 else 0.0

    # ─── 报告生成 ────────────────────────────────────────────

    def generate_signal_report(self, days: int = 7) -> str:
        """生成隐式信号报告"""
        feedback_rate = self.get_feedback_rate(days)
        cancel_rate = self.get_cancel_rate(days)
        avg_duration = self.get_avg_task_duration_seconds(days)
        tool_rates = self.get_tool_success_rates(days)
        repeat_rate = self.get_repeat_rate(days)
        total_tasks = len(self.get_signal_data(days))

        lines = [
            "=" * 50,
            "WorkBuddy 隐式信号报告",
            f"统计周期：最近 {days} 天",
            "=" * 50,
            "",
            f"  任务总量: {total_tasks}",
            f"  反馈填写率: {feedback_rate * 100:.1f}%",
            f"  任务取消率: {cancel_rate * 100:.1f}%",
            f"  重复修正率: {repeat_rate * 100:.1f}%",
            f"  平均任务时长: {avg_duration:.1f}s",
            "",
            "  工具成功率:"
        ]

        if tool_rates:
            for tool, rate in sorted(tool_rates.items(), key=lambda x: x[1]):
                status = "[OK]" if rate >= 0.9 else "[WARN]" if rate >= 0.7 else "[FAIL]"
                lines.append(f"    {status} {tool}: {rate * 100:.1f}%")
        else:
            lines.append("    (暂无数据)")

        # 健康评分（0-100）
        health_score = self._calculate_signal_health(
            feedback_rate, cancel_rate, repeat_rate, tool_rates
        )
        lines.extend([
            "",
            f"  信号健康评分: {health_score}/100",
            "=" * 50
        ])

        return "\n".join(lines)

    def _calculate_signal_health(
        self,
        feedback_rate: float,
        cancel_rate: float,
        repeat_rate: float,
        tool_rates: dict
    ) -> int:
        """计算综合信号健康评分"""
        score = 50  # 基础分

        # 反馈率贡献（+25分）
        score += feedback_rate * 25

        # 取消率惩罚（-25分）
        score -= cancel_rate * 25

        # 重复率惩罚（-15分）
        score -= repeat_rate * 15

        # 工具成功率贡献（+15分，取平均）
        if tool_rates:
            avg_tool_rate = sum(tool_rates.values()) / len(tool_rates)
            score += avg_tool_rate * 15

        return max(0, min(100, int(score)))

    # ─── 内部方法 ────────────────────────────────────────────

    def _flush_task_signal(self, task: dict, task_id: str):
        """将单条任务信号追加到月度文件"""
        today = datetime.now().strftime("%Y-%m-%d")
        sig_file = self.signals_dir / f"{today}.json"

        # 读取已有数据
        if sig_file.exists():
            with open(sig_file, "r", encoding="utf-8") as f:
                signals = json.load(f)
        else:
            signals = []

        # 计算时长
        start = datetime.fromisoformat(task["start_time"])
        end_str = task.get("end_time", datetime.now().isoformat())
        end = datetime.fromisoformat(end_str)
        duration_seconds = (end - start).total_seconds()

        # 构建信号条目
        entry = {
            "task_id": task_id,
            "task_summary": task.get("task_summary", ""),
            "start_time": task["start_time"],
            "end_time": end_str,
            "duration_seconds": round(duration_seconds, 1),
            "outcome": task.get("outcome", "unknown"),
            "cancelled": task.get("cancelled", False),
            "has_feedback": task.get("has_feedback", False),
            "tool_calls": task.get("tool_calls", []),
            "custom_metrics": task.get("custom_metrics", {})
        }

        signals.append(entry)

        with open(sig_file, "w", encoding="utf-8") as f:
            json.dump(signals, f, ensure_ascii=False, indent=2)

    def mark_task_has_feedback(self, task_id: str):
        """标记某任务已有显式反馈（由 learn.py 在记录反馈后调用）"""
        if task_id in self._session_tasks:
            self._session_tasks[task_id]["has_feedback"] = True


def run_signal_report(days: int = 7) -> str:
    """命令行：生成信号报告"""
    workspace = "c:/Users/Administrator/WorkBuddy/20260412210819"
    collector = SignalCollector(workspace)
    return collector.generate_signal_report(days)


if __name__ == "__main__":
    print(run_signal_report(days=7))
