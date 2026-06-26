"""
WorkBuddy 智能学习系统 - 主入口（整合六大模块）
反馈收集 | 隐式信号 | 任务画像 | 模式识别 | 知识蒸馏 | 实时警报
"""

import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

sys.stdout.reconfigure(encoding='utf-8')

skill_dir = Path(__file__).parent
sys.path.insert(0, str(skill_dir))

from feedback import FeedbackCollector, generate_feedback_prompt
from signal_collector import SignalCollector
from task_profiler import TaskProfile, TaskProfilerAnalyzer
from pattern_recognizer import PatternRecognizer, AdaptiveThresholds, run_pattern_recognition, run_with_alerts
from knowledge_distiller import KnowledgeDistiller, run_distillation, _compute_adaptive_threshold


class SmartLearningSystem:
    """智能学习系统 - 整合六大模块"""

    def __init__(self, workspace_root: str):
        self.workspace = workspace_root
        self.feedback = FeedbackCollector(workspace_root)
        self.signal = SignalCollector(workspace_root)
        self.profiler = TaskProfile(workspace_root)
        self.profiler_analyzer = TaskProfilerAnalyzer(workspace_root)
        self.pattern = PatternRecognizer(workspace_root)
        self.adaptive_thresholds = AdaptiveThresholds(workspace_root)
        self.distiller = KnowledgeDistiller(workspace_root)

    def check_and_trigger_template(self, user_request: str) -> Optional[dict]:
        """用户请求进来时调用，返回匹配模板供推荐"""
        return self.distiller.match_template(user_request)

    def record_template_used(self, template_name: str, template_id: str):
        """记录本次使用了模板"""
        self.profiler.use_template(template_id, template_name)

    def record_alert_rejected(self, alert_task: str):
        """记录警报被拒绝（误报）"""
        self.adaptive_thresholds.record_alert_feedback(alert_task, confirmed=False)

    def record_alert_confirmed(self, alert_task: str):
        """记录警报被确认（有效）"""
        self.adaptive_thresholds.record_alert_feedback(alert_task, confirmed=True)

    def run_full_cycle(self) -> dict:
        """运行完整学习周期：反馈→信号→模式→警报→蒸馏→综合报告"""
        # Phase 1: 反馈 & 隐式信号
        recent_feedback = self.feedback.get_recent_feedback(days=7)
        feedback_rate = self.signal.get_feedback_rate(days=7)
        signal_report = self.signal.generate_signal_report(days=7)

        fb_summary = {
            "total": len(recent_feedback),
            "good": len([f for f in recent_feedback if f["rating"] == "good"]),
            "bad": len([f for f in recent_feedback if f["rating"] == "bad"]),
            "feedback_rate": feedback_rate,
            "recent": recent_feedback[:3]
        }

        # Phase 2: 模式识别 + 警报
        alert_result = run_with_alerts(self.workspace)
        patterns = alert_result["patterns"]
        alerts = alert_result["alerts"]
        alert_report = alert_result["alert_report"]
        thresholds = alert_result.get("thresholds", {})

        pattern_summary = {
            "high_value_count": len(patterns.get("patterns", [])),
            "total_tasks_30d": patterns.get("summary", {}).get("total_tasks", 0),
            "top_3": patterns.get("summary", {}).get("top_3", [])
        }

        # Phase 3: 知识蒸馏（自适应阈值）
        good_feedbacks = [f for f in recent_feedback if f["rating"] == "good"]
        auto_result = self.distiller.check_and_auto_distill(good_feedbacks, feedback_rate)
        distill_result = self.distiller.distill_from_feedback(good_feedbacks)
        distill_result["auto_distill"] = auto_result

        # Phase 4: 画像对比
        comparison = self.profiler_analyzer.compare_template_vs_free(days=30)

        # Phase 5: 综合报告
        combined_report = self._generate_combined_report(
            fb_summary, pattern_summary, alerts,
            auto_result, comparison, thresholds
        )

        return {
            "timestamp": datetime.now().isoformat(),
            "feedback_summary": fb_summary,
            "pattern_summary": pattern_summary,
            "alerts": alerts,
            "alert_report": alert_report,
            "distillation": distill_result,
            "template_comparison": comparison,
            "signal_report": signal_report,
            "combined_report": combined_report
        }

    def _generate_combined_report(
        self, fb_summary: dict, pattern_summary: dict, alerts: list,
        auto_result: dict, comparison: dict, thresholds: dict
    ) -> str:
        lines = [
            "=" * 55,
            "WorkBuddy 智能学习综合报告",
            datetime.now().strftime("生成时间: %Y-%m-%d %H:%M"),
            "=" * 55,
            "",
            "## 1. 反馈摘要",
            f"  近7天反馈: {fb_summary['total']} 条",
            f"  满意/不满意: {fb_summary['good']} / {fb_summary['bad']}",
            f"  反馈填写率: {fb_summary['feedback_rate']*100:.1f}%",
            ""
        ]

        lines.extend([
            "## 2. 模式识别（近30天）",
            f"  高价值模式: {pattern_summary['high_value_count']} 个",
            f"  任务总量: {pattern_summary['total_tasks_30d']} 个"
        ])
        if pattern_summary["top_3"]:
            lines.append("  Top 3 高频任务:")
            for task, count in pattern_summary["top_3"]:
                lines.append(f"    - {task}: {count}次")
        lines.append("")

        lines.append("## 3. 实时警报")
        if alerts:
            for a in alerts[:5]:
                lines.append(f"  [{a['level']}] {a['message']}")
        else:
            lines.append("  (当前无警报)")
        lines.append("")

        lines.append("## 4. 知识蒸馏")
        lines.append(f"  {auto_result.get('message', '')}")
        if auto_result.get("threshold"):
            lines.append(f"  当前阈值: {auto_result['threshold']} | 反馈率: {fb_summary['feedback_rate']:.1%}")
        lines.append("")

        lines.append("## 5. 模板 vs 自由执行（近30天）")
        wt = comparison.get("with_template", {})
        wo = comparison.get("without_template", {})
        lines.extend([
            f"  有模板: {wt.get('count',0)}个 | 成功率{wt.get('success_rate',0)*100:.0f}% | "
            f"平均{wt.get('avg_duration',0):.1f}s",
            f"  自由执行: {wo.get('count',0)}个 | 成功率{wo.get('success_rate',0)*100:.0f}% | "
            f"平均{wo.get('avg_duration',0):.1f}s",
            f"  时间节省: {comparison.get('time_saved_pct',0):.1f}%"
        ])

        lines.extend(["", "=" * 55])
        return "\n".join(lines)

    def record_quick_feedback(self, rating: str, task_summary: str = None, tags: list = None):
        """快速记录反馈"""
        fb = self.feedback.record_feedback(
            task_id=f"manual-{len(self.feedback.get_recent_feedback())}",
            rating=rating, tags=tags or [], note=task_summary
        )
        self.signal.flush_session()
        return fb

    def check_and_suggest(self) -> str:
        """检查并给出建议"""
        alert_result = run_with_alerts(self.workspace)
        return self.pattern.generate_insight_report(alert_result["patterns"])

    def match_request(self, user_request: str) -> Optional[str]:
        """模板关键词匹配入口"""
        return self.distiller.generate_match_suggestion(user_request)


def main():
    workspace = "c:/Users/Administrator/WorkBuddy/20260412210819"
    system = SmartLearningSystem(workspace)

    if len(sys.argv) == 1:
        print(system.check_and_suggest())
        return

    command = sys.argv[1]

    if command == "full":
        result = system.run_full_cycle()
        print(result["combined_report"])

    elif command == "patterns":
        print(system.check_and_suggest())

    elif command == "feedback":
        rating = sys.argv[2] if len(sys.argv) > 2 else "good"
        fb = system.record_quick_feedback(rating)
        print(f"已记录反馈: {fb['feedback_id']}")

    elif command == "distill":
        result = run_distillation(workspace)
        print(system.distiller.generate_distillation_report(result))

    elif command == "signals":
        print(system.signal.generate_signal_report(days=7))

    elif command == "alerts":
        alert_result = run_with_alerts(workspace)
        print(alert_result["alert_report"])
        th = alert_result.get("thresholds", {})
        if th:
            print(f"\n阈值: urgent={th.get('urgent')} high={th.get('high')} trend={th.get('trend')}")

    elif command == "profiler":
        print(system.profiler_analyzer.generate_profiler_report(days=30))

    elif command == "match":
        if len(sys.argv) < 3:
            print("用法: python learn.py match \"用户请求内容\"")
            return
        query = sys.argv[2]
        suggestion = system.match_request(query)
        print(suggestion if suggestion else "[无匹配模板]")

    else:
        print(
            "用法: python learn.py [full|patterns|feedback|distill|signals|alerts|profiler|match]\n"
            "  full      - 完整学习周期（含警报+信号+蒸馏）\n"
            "  patterns  - 模式识别\n"
            "  feedback  - 记录反馈\n"
            "  distill   - 知识蒸馏\n"
            "  signals   - 隐式信号报告\n"
            "  alerts    - 实时警报检查\n"
            "  profiler  - 任务画像分析\n"
            "  match     - 模板关键词匹配\n"
        )


if __name__ == "__main__":
    main()
