"""
报告生成器 — 综合日报 + 各类报告模板
支持一键生成包含所有维度的完整日报（Markdown 格式）
"""

from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

from skills_monitor.data.store import DataStore
from skills_monitor.adapters.skill_registry import SkillRegistry
from skills_monitor.core.benchmark import BenchmarkRunner
from skills_monitor.core.comparator import SkillComparator, ComparisonResult
from skills_monitor.core.evaluator import SkillEvaluator, SkillScore
from skills_monitor.core.recommender import SkillRecommender, Recommendation


class ReportGenerator:
    """综合报告生成器"""

    def __init__(
        self,
        store: DataStore,
        registry: SkillRegistry,
        agent_id: str,
        reports_dir: str = "reports/monitor",
    ):
        self.store = store
        self.registry = registry
        self.agent_id = agent_id
        self.reports_dir = reports_dir
        Path(reports_dir).mkdir(parents=True, exist_ok=True)

    def generate_daily_report(
        self,
        scores: Optional[List[SkillScore]] = None,
        comparisons: Optional[List[ComparisonResult]] = None,
        recommendations: Optional[List[Recommendation]] = None,
        date: Optional[str] = None,
    ) -> str:
        """
        生成完整日报（Markdown 格式）
        整合：今日概况 + 评分排行 + 基准对比 + 趋势分析 + 推荐 + 建议
        """
        now = datetime.now()
        report_date = date or now.strftime("%Y-%m-%d")

        lines = [
            f"# 📊 Skills Monitor — 每日监控报告",
            f"",
            f"> **日期**: {report_date}  ",
            f"> **生成时间**: {now.strftime('%Y-%m-%d %H:%M:%S')}  ",
            f"> **Agent ID**: {self.agent_id[:12]}...  ",
            f"> **已安装 Skills**: {len(self.registry.list_skills())} 个  ",
            f"> **可运行 Skills**: {len(self.registry.get_runnable_skills())} 个",
            f"",
            f"---",
            f"",
        ]

        # ── 今日概况 ──
        lines.extend(self._section_overview(report_date))

        # ── 评分排行 ──
        if scores:
            lines.extend(self._section_scores(scores))

        # ── 基准对比 ──
        if comparisons:
            lines.extend(self._section_comparisons(comparisons))

        # ── 趋势分析 ──
        if scores:
            lines.extend(self._section_trends(scores))

        # ── 推荐 ──
        if recommendations:
            lines.extend(self._section_recommendations(recommendations))

        # ── 操作建议 ──
        lines.extend(self._section_suggestions(scores, comparisons))

        # ── 页脚 ──
        lines.extend([
            f"",
            f"---",
            f"",
            f"*本报告由 Skills Monitor v0.1.0 自动生成*  ",
            f"*查看详细数据: `python skills_monitor_cli.py summary`*  ",
            f"*Web 面板: `python skills_monitor_web.py` → http://localhost:5050*",
        ])

        return "\n".join(lines)

    def _section_overview(self, report_date: str) -> List[str]:
        """今日概况区块"""
        lines = [
            f"## 📈 今日概况",
            f"",
        ]

        # 获取今日运行数据
        all_runs = self.store.get_runs(agent_id=self.agent_id, limit=2000)
        today_runs = [r for r in all_runs if r["start_time"].startswith(report_date)]

        # 排除基准运行
        user_runs = [r for r in today_runs if not (r.get("task_name", "").startswith("[benchmark]"))]
        success_runs = [r for r in user_runs if r["status"] == "success"]
        error_runs = [r for r in user_runs if r["status"] == "error"]

        # 活跃 skills
        active_skills = set(r["skill_id"] for r in user_runs)

        # 响应时间
        durations = [r["duration_ms"] for r in success_runs if r.get("duration_ms")]
        avg_duration = sum(durations) / len(durations) if durations else 0

        # 成功率
        success_rate = round(len(success_runs) / len(user_runs) * 100, 1) if user_runs else 0

        lines.extend([
            f"| 指标 | 数值 |",
            f"|------|------|",
            f"| 📊 任务执行 | **{len(user_runs)}** 次 (成功 {len(success_runs)} / 失败 {len(error_runs)}) |",
            f"| ✅ 成功率 | **{success_rate}%** |",
            f"| ⚡ 活跃 Skills | **{len(active_skills)}** 个 |",
            f"| ⏱ 平均响应 | **{avg_duration:.0f}ms** |",
            f"",
        ])

        # 各 skill 今日运行明细
        if active_skills:
            lines.extend([
                f"### 各 Skill 今日运行",
                f"",
                f"| Skill | 运行次数 | 成功率 | 平均响应 |",
                f"|-------|---------|--------|---------|",
            ])

            for sid in sorted(active_skills):
                s_runs = [r for r in user_runs if r["skill_id"] == sid]
                s_success = [r for r in s_runs if r["status"] == "success"]
                s_durs = [r["duration_ms"] for r in s_success if r.get("duration_ms")]
                s_rate = round(len(s_success) / len(s_runs) * 100, 1) if s_runs else 0
                s_avg = f"{sum(s_durs) / len(s_durs):.0f}ms" if s_durs else "N/A"
                lines.append(f"| {sid} | {len(s_runs)} | {s_rate}% | {s_avg} |")

            lines.append(f"")

        lines.extend([f"---", f""])
        return lines

    def _section_scores(self, scores: List[SkillScore]) -> List[str]:
        """评分排行区块"""
        lines = [
            f"## 🏆 综合评分排行",
            f"",
            f"| 排名 | Skill | 总分 | 等级 | 成功率 | 响应 | 满意度 | 复用 | 稳定性 |",
            f"|------|-------|------|------|--------|------|--------|------|--------|",
        ]

        for i, score in enumerate(scores, 1):
            sr = f"{score.factors['success_rate']:.0f}%" if score.factors['success_rate'] is not None else "-"
            rt = f"{score.factors['response_time']:.0f}ms" if score.factors['response_time'] is not None else "-"
            ur = f"{score.factors['satisfaction']:.1f}" if score.factors['satisfaction'] is not None else "-"
            rr = str(score.factors['reuse_rate']) if score.factors['reuse_rate'] is not None else "-"
            st = f"{score.factors['stability']:.2f}" if score.factors['stability'] is not None else "-"
            grade_short = score.grade.split("(")[0].strip()

            # 排名 emoji
            rank_emoji = {1: "🥇", 2: "🥈", 3: "🥉"}.get(i, f"{i}")

            lines.append(
                f"| {rank_emoji} | {score.skill_id} | **{score.total_score:.1f}** | {grade_short} | "
                f"{sr} | {rt} | {ur} | {rr} | {st} |"
            )

        lines.extend([f"", f"---", f""])
        return lines

    def _section_comparisons(self, comparisons: List[ComparisonResult]) -> List[str]:
        """基准对比区块"""
        lines = [
            f"## 📊 基准对比",
            f"",
            f"| Skill | 你的成功率 | 基准成功率 | 差值 | 你的响应 | 基准响应 | 排名 | 评价 |",
            f"|-------|-----------|-----------|------|---------|---------|------|------|",
        ]

        for comp in comparisons:
            sr = comp.success_rate_diff
            dr = comp.avg_duration_diff

            user_sr = f"{sr['user']}%" if sr.get("user") is not None else "N/A"
            bench_sr = f"{sr['benchmark']}%" if sr.get("benchmark") is not None else "N/A"
            sr_diff = f"{'+' if sr.get('diff', 0) > 0 else ''}{sr['diff']}%" if sr.get("diff") is not None else "-"
            user_dr = f"{dr['user']:.0f}ms" if dr.get("user") is not None else "N/A"
            bench_dr = f"{dr['benchmark']:.0f}ms" if dr.get("benchmark") is not None else "N/A"
            pct = f"P{comp.percentile}" if comp.percentile is not None else "-"

            if comp.verdict.startswith("🏆"):
                verdict_short = "🏆 优秀"
            elif comp.verdict.startswith("✅"):
                verdict_short = "✅ 良好"
            elif comp.verdict.startswith("⚡"):
                verdict_short = "⚡ 合格"
            else:
                verdict_short = "⚠️ 待改进"

            lines.append(
                f"| {comp.skill_id} | {user_sr} | {bench_sr} | {sr_diff} | "
                f"{user_dr} | {bench_dr} | {pct} | {verdict_short} |"
            )

        lines.extend([f"", f"---", f""])
        return lines

    def _section_trends(self, scores: List[SkillScore]) -> List[str]:
        """趋势分析区块"""
        evaluator = SkillEvaluator(self.store, self.agent_id)
        lines = [
            f"## 📈 7 天趋势",
            f"",
        ]

        has_trend = False
        for score in scores:
            trend = evaluator.trend_analysis(score.skill_id, days=7)
            if trend.get("success_rate_trend") == "no_data":
                continue

            has_trend = True
            trend_icon = {
                "improving": "📈 上升",
                "declining": "📉 下降",
                "stable": "➡️ 平稳",
                "insufficient": "❓ 数据不足",
            }.get(trend["success_rate_trend"], "❓")

            first = trend.get("first_success_rate", "?")
            latest = trend.get("latest_success_rate", "?")
            points = trend.get("data_points", 0)

            lines.append(f"- **{score.skill_id}**: {trend_icon} ({first}% → {latest}%), {points} 个数据点")

        if not has_trend:
            lines.append("暂无足够的历史数据生成趋势分析。")

        lines.extend([f"", f"---", f""])
        return lines

    def _section_recommendations(self, recommendations: List[Recommendation]) -> List[str]:
        """推荐区块"""
        lines = [
            f"## 💡 Skill 推荐",
            f"",
            f"| 排名 | 名称 | 分类 | 推荐分 | 类型 | 理由 |",
            f"|------|------|------|--------|------|------|",
        ]

        for i, rec in enumerate(recommendations[:5], 1):
            reason_short = {
                "complement": "💡 互补",
                "upgrade": "⬆️ 升级",
                "collaborative": "🤝 协同",
                "popular": "🔥 热门",
            }.get(rec.reason_type, rec.reason_type)

            detail = rec.reason_detail[:50]
            lines.append(
                f"| {i} | **{rec.skill_info['name']}** | {rec.skill_info['category']} | "
                f"{rec.score:.0f} | {reason_short} | {detail} |"
            )

        lines.extend([f"", f"---", f""])
        return lines

    def _section_suggestions(
        self,
        scores: Optional[List[SkillScore]],
        comparisons: Optional[List[ComparisonResult]],
    ) -> List[str]:
        """操作建议区块"""
        lines = [
            f"## 🔧 操作建议",
            f"",
        ]

        suggestions = []

        if scores:
            best = scores[0]
            worst = scores[-1] if len(scores) > 1 else None

            suggestions.append(
                f"1. 🏆 **最佳 Skill**: `{best.skill_id}` ({best.total_score:.1f}分) — 表现稳定，继续使用"
            )

            if worst and worst.total_score < 60:
                suggestions.append(
                    f"2. ⚠️ **关注**: `{worst.skill_id}` ({worst.total_score:.1f}分) — "
                    f"建议排查稳定性问题或考虑替代方案"
                )

            # 满意度数据不足的 skill
            needs_data = [s for s in scores if s.factors.get("satisfaction") is None]
            if needs_data:
                names = ", ".join(f"`{s.skill_id}`" for s in needs_data[:3])
                suggestions.append(
                    f"3. 📊 **数据不足**: {names} — 多使用以积累对话满意度数据"
                )

        if comparisons:
            needs_work = [c for c in comparisons if c.verdict.startswith("⚠️")]
            if needs_work:
                names = ", ".join(f"`{c.skill_id}`" for c in needs_work)
                suggestions.append(
                    f"4. 🔍 **低于基准**: {names} — 建议检查网络环境或考虑替换"
                )

        if not suggestions:
            suggestions.append("✅ 当前系统运行状况良好，暂无需要关注的问题。")

        lines.extend(suggestions)
        lines.extend([f""])
        return lines

    def save_report(self, content: str, name: str = "daily") -> str:
        """保存报告到文件"""
        now = datetime.now()
        filename = f"{name}_{now.strftime('%Y%m%d_%H%M%S')}.md"
        filepath = str(Path(self.reports_dir) / filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        return filepath

    def generate_and_save_daily(
        self,
        scores: Optional[List[SkillScore]] = None,
        comparisons: Optional[List[ComparisonResult]] = None,
        recommendations: Optional[List[Recommendation]] = None,
    ) -> str:
        """生成并保存日报，返回文件路径"""
        content = self.generate_daily_report(scores, comparisons, recommendations)
        return self.save_report(content, "daily")

    # ── 辅助方法 ──

    def get_dashboard_data(self) -> Dict[str, Any]:
        """
        获取仪表盘所需的所有数据（供 Web 面板使用）
        返回结构化数据而非 Markdown
        """
        now = datetime.now()
        today = now.strftime("%Y-%m-%d")

        # 今日运行数据
        all_runs = self.store.get_runs(agent_id=self.agent_id, limit=2000)
        today_runs = [r for r in all_runs if r["start_time"].startswith(today)]
        user_runs = [r for r in today_runs if not (r.get("task_name", "").startswith("[benchmark]"))]
        success_runs = [r for r in user_runs if r["status"] == "success"]
        durations = [r["duration_ms"] for r in success_runs if r.get("duration_ms")]

        # 活跃 skills
        active_skills = sorted(set(r["skill_id"] for r in user_runs))

        # 评分
        evaluator = SkillEvaluator(self.store, self.agent_id)
        runnable = self.registry.get_runnable_skills()
        skill_ids = [s.slug for s in runnable]
        scores = evaluator.evaluate_all(skill_ids)

        # 7 天趋势数据
        trends = {}
        for score in scores:
            trend = evaluator.trend_analysis(score.skill_id, days=7)
            trends[score.skill_id] = trend

        # 最近隐性反馈
        implicit_feedbacks = self.store.get_implicit_feedback(limit=10)

        # 7 天运行次数趋势（按天汇总）
        daily_runs = {}
        for i in range(7):
            day = (now - timedelta(days=i)).strftime("%Y-%m-%d")
            day_runs = [r for r in all_runs if r["start_time"].startswith(day)]
            day_user_runs = [r for r in day_runs if not (r.get("task_name", "").startswith("[benchmark]"))]
            day_success = [r for r in day_user_runs if r["status"] == "success"]
            daily_runs[day] = {
                "total": len(day_user_runs),
                "success": len(day_success),
                "error": len(day_user_runs) - len(day_success),
            }

        return {
            "date": today,
            "generated_at": now.isoformat(),
            "overview": {
                "total_runs": len(user_runs),
                "success_runs": len(success_runs),
                "error_runs": len(user_runs) - len(success_runs),
                "success_rate": round(len(success_runs) / len(user_runs) * 100, 1) if user_runs else 0,
                "active_skills": len(active_skills),
                "avg_duration_ms": round(sum(durations) / len(durations), 1) if durations else 0,
                "total_installed": len(self.registry.list_skills()),
                "total_runnable": len(runnable),
            },
            "scores": [s.to_dict() for s in scores],
            "trends": trends,
            "daily_runs": daily_runs,
            "active_skills": active_skills,
            "recent_feedbacks": implicit_feedbacks,
        }
