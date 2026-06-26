"""
对比分析器 — 用户实际数据 vs 基准数据
生成对比报告，计算排名百分位
"""

from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from skills_monitor.core.benchmark import BenchmarkStats
from skills_monitor.data.store import DataStore


class ComparisonResult:
    """单个 skill 的对比结果"""

    def __init__(
        self,
        skill_id: str,
        user_data: Dict[str, Any],
        benchmark_data: Dict[str, Any],
    ):
        self.skill_id = skill_id
        self.user_data = user_data
        self.benchmark_data = benchmark_data

        # 计算对比指标
        self.success_rate_diff = self._calc_diff("success_rate")
        self.avg_duration_diff = self._calc_diff("avg_duration_ms", lower_is_better=True)
        self.percentile = self._calc_percentile()
        self.verdict = self._compute_verdict()

    def _calc_diff(self, key: str, lower_is_better: bool = False) -> Dict[str, Any]:
        """计算差值和方向"""
        user_val = self.user_data.get(key)
        bench_val = self.benchmark_data.get(key)

        if user_val is None or bench_val is None:
            return {"user": user_val, "benchmark": bench_val, "diff": None, "better": None}

        diff = user_val - bench_val
        if lower_is_better:
            better = diff < 0
        else:
            better = diff > 0

        return {
            "user": round(user_val, 2),
            "benchmark": round(bench_val, 2),
            "diff": round(diff, 2),
            "diff_pct": round(diff / bench_val * 100, 1) if bench_val != 0 else 0,
            "better": better,
        }

    def _calc_percentile(self) -> Optional[int]:
        """根据成功率估算百分位排名"""
        user_rate = self.user_data.get("success_rate", 0)
        bench_rate = self.benchmark_data.get("success_rate", 0)

        if bench_rate == 0:
            return None

        # 简化估算：假设正态分布
        ratio = user_rate / bench_rate if bench_rate > 0 else 1
        if ratio >= 1.2:
            return min(95, int(50 + ratio * 30))
        elif ratio >= 1.0:
            return int(50 + (ratio - 1) * 200)
        elif ratio >= 0.8:
            return int(50 - (1 - ratio) * 200)
        else:
            return max(5, int(50 - (1 - ratio) * 150))

    def _compute_verdict(self) -> str:
        """综合评价"""
        sr = self.success_rate_diff
        dr = self.avg_duration_diff

        sr_better = sr.get("better") if sr.get("better") is not None else False
        dr_better = dr.get("better") if dr.get("better") is not None else False

        if sr_better and dr_better:
            return "🏆 优秀 — 成功率和响应速度均超越基准"
        elif sr_better:
            return "✅ 良好 — 成功率超越基准，响应速度可优化"
        elif dr_better:
            return "⚡ 合格 — 响应速度优秀，成功率有提升空间"
        else:
            return "⚠️ 待改进 — 成功率和响应速度均低于基准"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "skill_id": self.skill_id,
            "user_data": self.user_data,
            "benchmark_data": self.benchmark_data,
            "success_rate_diff": self.success_rate_diff,
            "avg_duration_diff": self.avg_duration_diff,
            "percentile": self.percentile,
            "verdict": self.verdict,
        }

    def format_report(self) -> str:
        """格式化对比报告"""
        lines = [
            f"📊 [{self.skill_id}] 基准对比报告",
            f"{'─' * 50}",
        ]

        # 成功率对比
        sr = self.success_rate_diff
        if sr.get("diff") is not None:
            icon = "🟢" if sr["better"] else "🔴"
            sign = "+" if sr["diff"] > 0 else ""
            lines.append(
                f"  成功率:  你 {sr['user']}%  vs  基准 {sr['benchmark']}%  "
                f"{icon} ({sign}{sr['diff']}%)"
            )
        else:
            lines.append("  成功率:  数据不足")

        # 响应时间对比
        dr = self.avg_duration_diff
        if dr.get("diff") is not None:
            icon = "🟢" if dr["better"] else "🔴"
            sign = "+" if dr["diff"] > 0 else ""
            lines.append(
                f"  响应时间: 你 {dr['user']:.0f}ms  vs  基准 {dr['benchmark']:.0f}ms  "
                f"{icon} ({sign}{dr['diff']:.0f}ms)"
            )
        else:
            lines.append("  响应时间: 数据不足")

        # 排名
        if self.percentile is not None:
            lines.append(f"  排名:    P{self.percentile} (超过 {self.percentile}% 的用户)")

        # 结论
        lines.append(f"\n  {self.verdict}")

        return "\n".join(lines)


class SkillComparator:
    """Skill 对比分析器"""

    def __init__(self, store: DataStore, agent_id: str):
        self.store = store
        self.agent_id = agent_id

    def compare_with_benchmark(
        self,
        skill_id: str,
        benchmark_stats: BenchmarkStats,
    ) -> ComparisonResult:
        """将用户的实际数据与基准数据对比"""
        # 获取用户数据
        user_summary = self.store.get_skill_summary(skill_id, self.agent_id)

        # 排除基准运行记录（task_name 以 [benchmark] 开头的）
        all_runs = self.store.get_runs(skill_id=skill_id, agent_id=self.agent_id, limit=1000)
        user_runs = [r for r in all_runs if not (r.get("task_name", "").startswith("[benchmark]"))]

        if user_runs:
            success_runs = [r for r in user_runs if r["status"] == "success"]
            durations = [r["duration_ms"] for r in success_runs if r.get("duration_ms")]

            user_data = {
                "total_runs": len(user_runs),
                "success_count": len(success_runs),
                "success_rate": round(len(success_runs) / len(user_runs) * 100, 1) if user_runs else 0,
                "avg_duration_ms": sum(durations) / len(durations) if durations else None,
                "avg_satisfaction": user_summary.get("avg_rating"),
            }
        else:
            user_data = {
                "total_runs": user_summary["total_runs"],
                "success_count": user_summary["success_count"],
                "success_rate": user_summary["success_rate"],
                "avg_duration_ms": user_summary["avg_duration_ms"],
                "avg_satisfaction": user_summary.get("avg_rating"),
            }

        # 基准数据
        benchmark_data = {
            "total_runs": benchmark_stats.total_runs,
            "success_count": benchmark_stats.success_count,
            "success_rate": benchmark_stats.success_rate,
            "avg_duration_ms": benchmark_stats.avg_duration_ms,
            "p95_duration_ms": benchmark_stats.p95_duration_ms,
        }

        return ComparisonResult(skill_id, user_data, benchmark_data)

    def compare_multiple(
        self,
        benchmarks: Dict[str, BenchmarkStats],
    ) -> List[ComparisonResult]:
        """批量对比多个 skill"""
        results = []
        for skill_id, bench_stats in benchmarks.items():
            try:
                result = self.compare_with_benchmark(skill_id, bench_stats)
                results.append(result)
            except Exception:
                pass
        return results

    def generate_comparison_report(
        self,
        comparisons: List[ComparisonResult],
    ) -> str:
        """生成完整的对比报告（Markdown 格式）"""
        now = datetime.now()
        lines = [
            f"# 📊 Skills 基准对比报告",
            f"",
            f"> **生成时间**: {now.strftime('%Y-%m-%d %H:%M:%S')}  ",
            f"> **Agent ID**: {self.agent_id[:12]}...  ",
            f"> **对比 Skills 数**: {len(comparisons)}",
            f"",
            f"---",
            f"",
            f"## 总览",
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

            # 简短评价
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

        lines.extend([
            f"",
            f"---",
            f"",
            f"## 详细分析",
            f"",
        ])

        for comp in comparisons:
            lines.append(f"### {comp.skill_id}")
            lines.append(f"")
            lines.append(f"```")
            lines.append(comp.format_report())
            lines.append(f"```")
            lines.append(f"")

        # 总体建议
        excellent = [c for c in comparisons if c.verdict.startswith("🏆")]
        good = [c for c in comparisons if c.verdict.startswith("✅")]
        needs_work = [c for c in comparisons if c.verdict.startswith("⚠️")]

        lines.extend([
            f"---",
            f"",
            f"## 💡 建议",
            f"",
        ])

        if excellent:
            lines.append(f"- 🏆 **表现优秀**: {', '.join(c.skill_id for c in excellent)} — 继续保持")
        if good:
            lines.append(f"- ✅ **表现良好**: {', '.join(c.skill_id for c in good)} — 关注响应时间优化")
        if needs_work:
            lines.append(
                f"- ⚠️ **需要关注**: {', '.join(c.skill_id for c in needs_work)} "
                f"— 建议检查网络状况或考虑替换为同类更稳定的 skill"
            )

        return "\n".join(lines)
