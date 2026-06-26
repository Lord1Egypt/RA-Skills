"""
WorkBuddy 智能学习系统 - 模式识别模块
功能：分析记忆文件，识别高频任务模式，生成沉淀建议
增强：AdaptiveThresholds 类 + 实时警报（突发/趋势/稳定三级）
"""

import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

# 基础警报阈值
_BASE_URGENT_THRESHOLD = 75   # 突发警报（立即通知）
_BASE_HIGH_THRESHOLD = 70     # 高优先级（本周关注）
_BASE_TREND_THRESHOLD = 60    # 趋势标记（周报标记）
_TREND_BOOST_RATE = 1.5       # 环比增长超过此比例触发趋势警报


class AdaptiveThresholds:
    """
    自适应阈值引擎
    警报阈值根据历史警报准确率动态调节：
    - 准确率高（用户确认多）→ 更敏感，降低阈值
    - 准确率低（误报多）→ 提高门槛抑制噪音
    """

    def __init__(self, workspace_root: str):
        self.workspace = Path(workspace_root)
        self.state_file = self.workspace / ".workbuddy" / "memory" / "patterns" / "threshold_state.json"
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        self._state = self._load_state()

    def _load_state(self) -> dict:
        if self.state_file.exists():
            try:
                with open(self.state_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, OSError):
                pass

        return {
            "alert_history": [],   # [{task, confirmed, timestamp}]
            "base_urgent": _BASE_URGENT_THRESHOLD,
            "base_high": _BASE_HIGH_THRESHOLD,
            "base_trend": _BASE_TREND_THRESHOLD,
            "version": "2.0"
        }

    def _save_state(self):
        with open(self.state_file, "w", encoding="utf-8") as f:
            json.dump(self._state, f, ensure_ascii=False, indent=2)

    def record_alert_feedback(self, task: str, confirmed: bool):
        """
        记录警报反馈（由主系统调用）
        - confirmed=True: 用户确认警报有效
        - confirmed=False: 误报
        """
        self._state["alert_history"].append({
            "task": task,
            "confirmed": confirmed,
            "timestamp": datetime.now().isoformat()
        })

        # 只保留最近100条
        if len(self._state["alert_history"]) > 100:
            self._state["alert_history"] = self._state["alert_history"][-100:]

        self._save_state()

    def get_thresholds(self) -> dict:
        """
        根据历史准确率返回当前阈值
        准确率 = confirmed / total
        """
        history = self._state["alert_history"]
        if len(history) < 5:
            # 数据不足，使用基础值
            return {
                "urgent": _BASE_URGENT_THRESHOLD,
                "high": _BASE_HIGH_THRESHOLD,
                "trend": _BASE_TREND_THRESHOLD
            }

        confirmed = sum(1 for h in history if h["confirmed"])
        total = len(history)
        accuracy = confirmed / total

        # 准确率 > 0.7 → 敏感模式（降阈值）
        # 准确率 < 0.4 → 保守模式（升阈值）
        if accuracy >= 0.7:
            factor = 0.85  # 降低15%阈值，更敏感
        elif accuracy >= 0.4:
            factor = 1.0  # 保持不变
        else:
            factor = 1.3  # 提高30%阈值，抑制噪音

        return {
            "urgent": int(_BASE_URGENT_THRESHOLD * factor),
            "high": int(_BASE_HIGH_THRESHOLD * factor),
            "trend": int(_BASE_TREND_THRESHOLD * factor),
            "_accuracy": round(accuracy, 3),
            "_sample_size": total
        }

    def get_alert_stats(self) -> dict:
        """获取警报统计"""
        history = self._state["alert_history"]
        if not history:
            return {"total": 0, "confirmed": 0, "accuracy": 0.0}

        confirmed = sum(1 for h in history if h["confirmed"])
        return {
            "total": len(history),
            "confirmed": confirmed,
            "accuracy": round(confirmed / len(history), 3)
        }


class PatternRecognizer:
    """模式识别器 - 从记忆文件中提取高频任务模式"""

    def __init__(self, workspace_root: str):
        self.workspace = Path(workspace_root)
        self.memory_dir = self.workspace / ".workbuddy" / "memory"
        self.patterns_dir = self.memory_dir / "patterns"
        self.patterns_dir.mkdir(parents=True, exist_ok=True)

    def scan_memory_for_patterns(self, days: int = 30) -> dict:
        """扫描记忆文件，识别任务模式"""
        patterns = []
        task_counter = Counter()
        date_range = datetime.now() - timedelta(days=days)

        for mem_file in self.memory_dir.glob("*.md"):
            if mem_file.name in ["MEMORY.md"]:
                continue

            try:
                file_date = datetime.strptime(mem_file.stem, "%Y-%m-%d")
                if file_date < date_range:
                    continue
            except ValueError:
                continue

            content = mem_file.read_text(encoding="utf-8")

            task_keywords = [
                "文件整理", "内容推送", "数据分析", "报告生成",
                "记忆保存", "技能安装", "健康检查", "搜索分析",
                "模板创建", "自动化", "系统优化", "信息检索"
            ]

            for keyword in task_keywords:
                count = content.count(keyword)
                if count > 0:
                    task_counter[keyword] += count

            action_pattern = r'###\s+([^#\n]+)'
            actions = re.findall(action_pattern, content)
            for action in actions:
                action = action.strip()
                if action and len(action) < 50:
                    patterns.append({"action": action, "date": mem_file.stem, "type": "task"})

        scored_patterns = []
        for task, count in task_counter.most_common(20):
            score = self._calculate_pattern_score(
                frequency=count, recency=days, stability=0.8
            )

            if score >= 60:
                scored_patterns.append({
                    "task": task,
                    "frequency": count,
                    "score": score,
                    "suggestion": self._generate_suggestion(task, count),
                    "estimated_saving_minutes": count * 3
                })

        return {
            "patterns": scored_patterns,
            "summary": {
                "total_tasks": sum(task_counter.values()),
                "unique_tasks": len(task_counter),
                "top_3": task_counter.most_common(3)
            }
        }

    def _calculate_pattern_score(self, frequency: int, recency: int, stability: float) -> float:
        """计算模式价值分数"""
        max_freq = 50
        max_recency = 30

        freq_score = min(frequency / max_freq, 1.0) * 50
        recency_score = min(recency / max_recency, 1.0) * 20
        stability_score = stability * 30

        return round(freq_score + recency_score + stability_score, 1)

    def _generate_suggestion(self, task: str, count: int) -> str:
        templates = {
            "文件整理": "创建「文件整理自动化模板」，包含分类规则和命名规范",
            "内容推送": "创建「CodeBuddy推送模板」，标准化4领域内容格式",
            "记忆保存": "创建「记忆回写SOP」，规范每日总结格式",
            "技能安装": "创建「Skill安装检查清单」，沉淀安全审计流程",
            "健康检查": "创建「市场健康检查自动化」，定时监控URL可用性",
            "数据分析": "创建「数据分析报告模板」，标准化输出格式",
        }
        return templates.get(task, f"创建「{task}」标准化模板，提高执行一致性")

    def save_recognition_result(self, result: dict) -> Path:
        """保存识别结果"""
        month_key = datetime.now().strftime("%Y-%m")
        output_file = self.patterns_dir / f"patterns_{month_key}.json"

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        return output_file

    # ─── 警报系统 ────────────────────────────────────────

    def check_alerts(self, adaptive_thresholds: AdaptiveThresholds = None) -> list[dict]:
        """
        检查是否触发实时警报
        三级警报：突发 / 趋势 / 稳定
        """
        if adaptive_thresholds:
            thresholds = adaptive_thresholds.get_thresholds()
        else:
            thresholds = {
                "urgent": _BASE_URGENT_THRESHOLD,
                "high": _BASE_HIGH_THRESHOLD,
                "trend": _BASE_TREND_THRESHOLD
            }

        # 当前月 vs 上月 趋势对比
        this_month = self._get_patterns_by_month(months_back=0)
        last_month = self._get_patterns_by_month(months_back=1)

        alerts = []

        for task, freq in this_month.items():
            score = self._calculate_pattern_score(frequency=freq, recency=30, stability=0.8)

            # 突发警报（>= urgent阈值）
            if score >= thresholds["urgent"]:
                alerts.append({
                    "type": "urgent",
                    "level": "URGENT",
                    "task": task,
                    "frequency": freq,
                    "score": score,
                    "message": f"[突发] {task} 热度骤升（评分{score}），建议立即优化",
                    "threshold_used": thresholds["urgent"]
                })

            # 趋势警报（环比增长显著）
            elif task in last_month:
                growth = (freq - last_month[task]) / last_month[task]
                if growth >= _TREND_BOOST_RATE and score >= thresholds["trend"]:
                    alerts.append({
                        "type": "trend",
                        "level": "TREND",
                        "task": task,
                        "frequency": freq,
                        "last_month": last_month[task],
                        "growth_rate": round(growth * 100, 1),
                        "score": score,
                        "message": f"[趋势] {task} 环比增长{growth*100:.0f}%，需关注",
                        "threshold_used": thresholds["trend"]
                    })

            # 稳定警报（长期高频）
            elif score >= thresholds["high"]:
                alerts.append({
                    "type": "stable",
                    "level": "STABLE",
                    "task": task,
                    "frequency": freq,
                    "score": score,
                    "message": f"[稳定] {task} 持续高频（评分{score}），建议固化为模板",
                    "threshold_used": thresholds["high"]
                })

        return alerts

    def _get_patterns_by_month(self, months_back: int = 0) -> dict:
        """获取N个月前的任务频率"""
        target = datetime.now() - timedelta(days=30 * months_back)
        month_key = target.strftime("%Y-%m")

        counter = Counter()
        target_file = self.patterns_dir / f"patterns_{month_key}.json"

        if target_file.exists():
            try:
                with open(target_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for p in data.get("patterns", []):
                        counter[p["task"]] = p.get("frequency", 0)
            except (json.JSONDecodeError, OSError):
                pass

        # 如果月度文件不存在，扫描当月记忆
        if not counter and months_back == 0:
            day_cutoff = datetime.now() - timedelta(days=30)
            for mem_file in self.memory_dir.glob("*.md"):
                if mem_file.name in ["MEMORY.md"]:
                    continue
                try:
                    file_date = datetime.strptime(mem_file.stem, "%Y-%m-%d")
                    if file_date < day_cutoff:
                        continue
                except ValueError:
                    continue

                content = mem_file.read_text(encoding="utf-8")
                keywords = ["文件整理", "内容推送", "数据分析", "报告生成",
                            "记忆保存", "技能安装", "健康检查", "搜索分析"]
                for kw in keywords:
                    count = content.count(kw)
                    if count > 0:
                        counter[kw] += count

        return dict(counter)

    def generate_alert_report(self, alerts: list[dict]) -> str:
        """生成警报报告"""
        if not alerts:
            return "[OK] 当前无实时警报。"

        lines = ["=" * 50, "WorkBuddy 实时警报", "=" * 50, ""]

        by_type = {"urgent": [], "trend": [], "stable": []}
        for a in alerts:
            by_type.get(a["type"], []).append(a)

        if by_type["urgent"]:
            lines.append("## [突发警报]")
            for a in by_type["urgent"]:
                lines.append(f"  [!] {a['task']}: {a['message']}")

        if by_type["trend"]:
            lines.append("\n## [趋势预警]")
            for a in by_type["trend"]:
                lines.append(f"  [^] {a['task']}: {a['message']}（上月{a['last_month']}次）")

        if by_type["stable"]:
            lines.append("\n## [稳定关注]")
            for a in by_type["stable"]:
                lines.append(f"  [*] {a['task']}: {a['message']}")

        lines.append("")
        lines.append(f"共 {len(alerts)} 条警报 | 请及时处理")

        return "\n".join(lines)

    def generate_insight_report(self, patterns_result: dict) -> str:
        """生成洞察报告（用于向用户展示）"""
        if not patterns_result["patterns"]:
            return "[OK] 未发现高价值沉淀模式，当前任务模式已充分优化。"

        lines = ["## 模式识别报告\n"]

        for p in patterns_result["patterns"][:5]:
            level = "高" if p["score"] >= 80 else "中" if p["score"] >= 70 else "低"
            lines.append(f"[{level}] **{p['task']}** (评分: {p['score']})")
            lines.append(f"   - 30天内出现: {p['frequency']} 次")
            lines.append(f"   - 建议: {p['suggestion']}")
            lines.append(f"   - 预估节省: ~{p['estimated_saving_minutes']} 分钟\n")

        lines.append("---")
        lines.append(f"**统计**: 共识别 {len(patterns_result['patterns'])} 个高价值模式")
        lines.append(f"**总计**: 30天内完成约 {patterns_result['summary']['total_tasks']} 个任务")

        return "\n".join(lines)


def run_pattern_recognition(workspace: str) -> dict:
    """运行模式识别主函数"""
    recognizer = PatternRecognizer(workspace)
    result = recognizer.scan_memory_for_patterns(days=30)
    recognizer.save_recognition_result(result)
    return result


def run_with_alerts(workspace: str) -> dict:
    """
    运行模式识别 + 警报检查
    返回：{patterns, alerts, alert_report, combined_report}
    """
    recognizer = PatternRecognizer(workspace)
    adaptive = AdaptiveThresholds(workspace)

    patterns = run_pattern_recognition(workspace)
    alerts = recognizer.check_alerts(adaptive)

    return {
        "patterns": patterns,
        "alerts": alerts,
        "alert_report": recognizer.generate_alert_report(alerts),
        "thresholds": adaptive.get_thresholds()
    }


if __name__ == "__main__":
    result = run_with_alerts("c:/Users/Administrator/WorkBuddy/20260412210819")
    recognizer = PatternRecognizer("c:/Users/Administrator/WorkBuddy/20260412210819")
    print(recognizer.generate_insight_report(result["patterns"]))
    print()
    print(result["alert_report"])
