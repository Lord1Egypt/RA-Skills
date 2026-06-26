"""
诊断报告生成器 — Skills Monitor 系统健康诊断 + 优化建议
=========================================================
整合评估引擎、推荐引擎、基准对比，生成完善的诊断报告：
  - 系统健康度评分
  - Skills 使用情况诊断
  - 性能瓶颈识别
  - 覆盖度分析
  - 可操作的优化建议
  - 企微推送支持
"""

from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from skills_monitor.data.store import DataStore
from skills_monitor.adapters.skill_registry import SkillRegistry
from skills_monitor.adapters.clawhub_client import ClawHubClient
from skills_monitor.core.evaluator import SkillEvaluator, SkillScore
from skills_monitor.core.recommender import SkillRecommender, Recommendation
from skills_monitor.core.benchmark import BenchmarkRunner


# ──────── 健康度评级 ────────

def _health_grade(score: float) -> Tuple[str, str]:
    """综合健康度 → (等级, emoji)"""
    if score >= 90:
        return "优秀", "🟢"
    elif score >= 75:
        return "良好", "🟡"
    elif score >= 60:
        return "一般", "🟠"
    else:
        return "需关注", "🔴"


class DiagnosticReporter:
    """系统诊断报告生成器"""

    def __init__(
        self,
        store: DataStore,
        registry: SkillRegistry,
        agent_id: str,
        reports_dir: str = "reports/diagnostic",
    ):
        self.store = store
        self.registry = registry
        self.agent_id = agent_id
        self.reports_dir = reports_dir
        Path(reports_dir).mkdir(parents=True, exist_ok=True)

    def _load_community_data(self, skill_ids: List[str]) -> Dict[str, Dict[str, Any]]:
        """加载社区热度与评分数据，供 7 因子评分使用"""
        if not skill_ids:
            return {}
        try:
            client = ClawHubClient()
            metadata = client.batch_fetch(skill_ids)
            community_data = {}
            for slug, meta in metadata.items():
                community_data[slug] = {
                    "downloads": meta.get("installs") or 0,
                    "stars": meta.get("stars") or 0,
                    "current_installs": meta.get("installs") or 0,
                }
            return community_data
        except Exception:
            return {}

    def generate_diagnostic_report(
        self,
        trigger: str = "scheduled",
        extra_context: Optional[str] = None,
    ) -> str:
        """
        生成完整诊断报告（Markdown 格式）

        Args:
            trigger: 触发方式 — "scheduled"(定时) / "post_install"(安装后) / "manual"(手动)
            extra_context: 额外上下文（如刚安装的 skills 列表）
        """
        now = datetime.now()
        today = now.strftime("%Y-%m-%d")

        # 收集所有分析数据
        runnable = self.registry.get_runnable_skills()
        all_skills = self.registry.list_skills()
        skill_ids = [s.slug for s in runnable]
        evaluator = SkillEvaluator(
            self.store,
            self.agent_id,
            community_data=self._load_community_data(skill_ids),
        )
        scores = evaluator.evaluate_all(skill_ids)

        recommender = SkillRecommender(self.registry, self.store, self.agent_id)
        recommendations = recommender.get_all_recommendations(max_per_type=3)

        # 运行历史
        all_runs = self.store.get_runs(agent_id=self.agent_id, limit=5000)
        today_runs = [r for r in all_runs if r["start_time"].startswith(today)]
        user_runs = [r for r in today_runs if not (r.get("task_name", "").startswith("[benchmark]"))]

        # 7 天运行数据
        week_runs = []
        for r in all_runs:
            try:
                run_date = datetime.fromisoformat(r["start_time"].replace("Z", ""))
                if run_date >= now - timedelta(days=7):
                    week_runs.append(r)
            except (ValueError, TypeError):
                pass

        # 计算总体健康度
        health_score = self._calculate_health_score(
            all_skills, runnable, scores, user_runs, week_runs, recommendations
        )
        health_label, health_icon = _health_grade(health_score)

        # 触发方式标签
        trigger_labels = {
            "scheduled": "⏰ 每日定时诊断",
            "launchagent": "⏰ LaunchAgent 定时诊断",
            "crontab": "⏰ Crontab 定时诊断",
            "retry": "🔁 失败后重试诊断",
            "post_install": "📦 安装后自动诊断",
            "manual": "🔍 手动诊断",
            "first_sync_fallback": "🛟 首次同步兜底诊断",
        }
        trigger_label = trigger_labels.get(trigger, trigger)

        # ── 构建报告 ──
        lines = [
            f"# 🏥 Skills Monitor 诊断报告",
            f"",
            f"> **触发方式**: {trigger_label}  ",
            f"> **日期**: {today}  ",
            f"> **生成时间**: {now.strftime('%H:%M:%S')}  ",
            f"> **Agent ID**: `{self.agent_id[:12]}...`",
            f"",
        ]

        # 额外上下文（安装后触发时）
        if extra_context:
            lines.extend([
                f"> **触发原因**: {extra_context}",
                f"",
            ])

        lines.extend([
            f"---",
            f"",
        ])

        # ── 1. 系统健康度总览 ──
        lines.extend(self._section_health_overview(
            health_score, health_label, health_icon,
            all_skills, runnable, scores, user_runs, week_runs,
        ))

        # ── 2. Skills 覆盖度分析 ──
        lines.extend(self._section_coverage(all_skills, runnable))

        # ── 3. 性能诊断 ──
        lines.extend(self._section_performance(scores))

        # ── 4. 使用情况诊断 ──
        lines.extend(self._section_usage(scores, user_runs, week_runs))

        # ── 5. 问题发现 ──
        lines.extend(self._section_issues(scores, all_skills, runnable, recommendations))

        # ── 6. 优化建议 ──
        lines.extend(self._section_recommendations(
            scores, recommendations, all_skills, runnable, week_runs,
        ))

        # ── 7. 推荐安装 ──
        if recommendations:
            lines.extend(self._section_install_recommendations(recommendations))

        # ── 页脚 ──
        lines.extend([
            f"",
            f"---",
            f"",
            f"*🏥 诊断报告由 Skills Monitor v0.3.0 自动生成（隐性评分引擎）*  ",
            f"*详细数据: `skills-monitor evaluate -v` | Web: `skills-monitor web`*",
        ])

        return "\n".join(lines)

    def _calculate_health_score(
        self,
        all_skills, runnable, scores, today_runs, week_runs, recommendations,
    ) -> float:
        """计算系统综合健康度（0-100）"""
        score = 0.0
        total_weight = 0.0

        # 1. 可运行率（20%）
        if all_skills:
            runnable_ratio = len(runnable) / len(all_skills)
            score += runnable_ratio * 100 * 0.20
            total_weight += 0.20

        # 2. 平均评分（30%）
        if scores:
            avg_total = sum(s.total_score for s in scores) / len(scores)
            score += avg_total * 0.30
            total_weight += 0.30

        # 3. 活跃度 — 7 天有运行记录（20%）
        if runnable:
            active_skills = set(r["skill_id"] for r in week_runs)
            active_ratio = len(active_skills) / len(runnable) if runnable else 0
            score += min(active_ratio * 1.5, 1.0) * 100 * 0.20  # 50%活跃就满分
            total_weight += 0.20

        # 4. 成功率（20%）
        if week_runs:
            success = sum(1 for r in week_runs if r["status"] == "success")
            success_rate = success / len(week_runs) * 100
            score += success_rate * 0.20
            total_weight += 0.20

        # 5. 缺失覆盖度惩罚（10%）
        complement_recs = [r for r in recommendations if r.reason_type == "complement"]
        if complement_recs:
            penalty = min(len(complement_recs) * 10, 30)
            score += max(0, 100 - penalty) * 0.10
        else:
            score += 100 * 0.10
        total_weight += 0.10

        return round(score / total_weight, 1) if total_weight > 0 else 50.0

    def _section_health_overview(
        self, health_score, health_label, health_icon,
        all_skills, runnable, scores, today_runs, week_runs,
    ) -> List[str]:
        """系统健康度总览"""
        success_today = [r for r in today_runs if r["status"] == "success"]
        success_week = [r for r in week_runs if r["status"] == "success"]
        durations = [r["duration_ms"] for r in success_week if r.get("duration_ms")]
        avg_dur = sum(durations) / len(durations) if durations else 0

        active_week = set(r["skill_id"] for r in week_runs)

        avg_score = sum(s.total_score for s in scores) / len(scores) if scores else 0
        top_skill = scores[0] if scores else None
        worst_skill = scores[-1] if len(scores) > 1 else None

        lines = [
            f"## {health_icon} 系统健康度: {health_score:.0f}/100 — {health_label}",
            f"",
            f"| 维度 | 数值 | 状态 |",
            f"|------|------|------|",
            f"| 📦 已安装 Skills | {len(all_skills)} 个 | — |",
            f"| ⚡ 可运行 Skills | {len(runnable)} 个 ({len(runnable)}/{len(all_skills)}) | {'✅' if len(runnable)/max(len(all_skills),1) >= 0.5 else '⚠️'} |",
            f"| 📈 今日运行 | {len(today_runs)} 次 (成功 {len(success_today)}) | {'✅' if len(today_runs) > 0 else '💤'} |",
            f"| 📊 7 天运行 | {len(week_runs)} 次 (成功 {len(success_week)}) | — |",
            f"| 🎯 7 天活跃 Skills | {len(active_week)} 个 | {'✅' if len(active_week) >= 3 else '⚠️'} |",
            f"| ⏱ 7 天平均响应 | {avg_dur:.0f}ms | {'✅' if avg_dur < 5000 else '⚠️'} |",
            f"| 🏆 平均综合评分 | {avg_score:.1f}/100 | {'✅' if avg_score >= 70 else '⚠️'} |",
        ]

        if top_skill:
            lines.append(
                f"| 👑 最佳 Skill | {top_skill.skill_id} ({top_skill.total_score:.1f}分) | 🏆 |"
            )
        if worst_skill and worst_skill.total_score < 60:
            lines.append(
                f"| ⚠️ 需关注 Skill | {worst_skill.skill_id} ({worst_skill.total_score:.1f}分) | 🔧 |"
            )

        lines.extend([f"", f"---", f""])
        return lines

    def _section_coverage(self, all_skills, runnable) -> List[str]:
        """Skills 覆盖度分析"""
        categories = self.registry.get_skills_by_category()

        lines = [
            f"## 📋 Skills 覆盖度分析",
            f"",
            f"| 分类 | 已安装 | 可运行 | 覆盖度 |",
            f"|------|--------|--------|--------|",
        ]

        for cat, skills in sorted(categories.items()):
            total = len(skills)
            run = len([s for s in skills if s.entry_type != "none"])
            ratio = f"{run/total*100:.0f}%" if total > 0 else "0%"
            status = "✅" if run / max(total, 1) >= 0.5 else "⚠️"
            lines.append(f"| {cat} | {total} | {run} | {ratio} {status} |")

        lines.extend([f"", f"---", f""])
        return lines

    def _section_performance(self, scores: List[SkillScore]) -> List[str]:
        """性能诊断"""
        if not scores:
            return [f"## ⚡ 性能诊断", f"", f"暂无评估数据。", f"", f"---", f""]

        lines = [
            f"## ⚡ 性能诊断",
            f"",
            f"| Skill | 综合评分 | 等级 | 成功率 | 平均响应 | 满意度(隐性) | 稳定性 |",
            f"|-------|---------|------|--------|---------|-------------|--------|",
        ]

        for score in scores:
            sr = f"{score.factors['success_rate']:.0f}%" if score.factors['success_rate'] is not None else "-"
            rt = f"{score.factors['response_time']:.0f}ms" if score.factors['response_time'] is not None else "-"
            ur = f"{score.factors['satisfaction']:.1f}/5" if score.factors.get('satisfaction') else "-"
            cv = score.factors.get('stability')
            st = f"{cv:.2f}" if cv is not None else "-"
            grade_short = score.grade.split("(")[0].strip()
            lines.append(
                f"| {score.skill_id} | **{score.total_score:.1f}** | {grade_short} | {sr} | {rt} | {ur} | {st} |"
            )

        lines.extend([f"", f"---", f""])
        return lines

    def _section_usage(self, scores, today_runs, week_runs) -> List[str]:
        """使用情况诊断"""
        lines = [
            f"## 📊 使用情况诊断",
            f"",
        ]

        if not week_runs:
            lines.extend([f"过去 7 天无运行记录。建议增加 Skills 使用频率。", f"", f"---", f""])
            return lines

        # 7 天各 skill 使用频次
        from collections import Counter
        skill_counter = Counter(r["skill_id"] for r in week_runs)
        top5 = skill_counter.most_common(5)

        lines.extend([
            f"### 7 天使用 TOP5",
            f"",
            f"| 排名 | Skill | 使用次数 | 成功次数 | 成功率 |",
            f"|------|-------|---------|---------|--------|",
        ])

        for i, (sid, count) in enumerate(top5, 1):
            success = sum(1 for r in week_runs if r["skill_id"] == sid and r["status"] == "success")
            rate = f"{success/count*100:.0f}%" if count > 0 else "-"
            lines.append(f"| {i} | {sid} | {count} | {success} | {rate} |")

        # 未使用的可运行 skills
        runnable_slugs = {s.slug for s in self.registry.get_runnable_skills()}
        used_slugs = set(skill_counter.keys())
        unused = runnable_slugs - used_slugs

        if unused:
            lines.extend([
                f"",
                f"### 💤 未使用的可运行 Skills ({len(unused)} 个)",
                f"",
            ])
            for slug in sorted(unused):
                lines.append(f"- `{slug}`")

        lines.extend([f"", f"---", f""])
        return lines

    def _section_issues(self, scores, all_skills, runnable, recommendations) -> List[str]:
        """问题发现"""
        issues = []

        # 1. 低评分 skills
        low_scores = [s for s in scores if s.total_score < 60]
        if low_scores:
            for s in low_scores:
                issues.append(
                    f"⚠️ **{s.skill_id}** 综合评分仅 {s.total_score:.1f} 分，等级 {s.grade.split('(')[0].strip()}"
                )

        # 2. 高失败率
        high_fail = [s for s in scores if s.factors.get("success_rate", 100) < 80]
        for s in high_fail:
            if s not in low_scores:
                issues.append(
                    f"⚠️ **{s.skill_id}** 成功率仅 {s.factors['success_rate']:.0f}%，建议排查"
                )

        # 3. 不可运行比例高
        non_runnable = len(all_skills) - len(runnable)
        if non_runnable > len(runnable):
            issues.append(
                f"⚠️ 有 {non_runnable} 个 Skills 不可运行（纯文档型），可运行率偏低"
            )

        # 4. 覆盖缺失
        complement_recs = [r for r in recommendations if r.reason_type == "complement"]
        if complement_recs:
            cats = set(r.skill_info["category"] for r in complement_recs)
            issues.append(
                f"💡 缺少以下能力类别的 Skills: {', '.join(cats)}"
            )

        # 5. 需要升级的
        upgrade_recs = [r for r in recommendations if r.reason_type == "upgrade"]
        if upgrade_recs:
            for r in upgrade_recs:
                issues.append(
                    f"⬆️ **{r.related_installed}** 建议升级为 **{r.skill_info['name']}**"
                )

        lines = [
            f"## 🔍 问题发现",
            f"",
        ]

        if issues:
            for issue in issues:
                lines.append(f"- {issue}")
        else:
            lines.append(f"✅ 未发现明显问题，系统运行状况良好！")

        lines.extend([f"", f"---", f""])
        return lines

    def _section_recommendations(
        self, scores, recommendations, all_skills, runnable, week_runs,
    ) -> List[str]:
        """优化建议"""
        suggestions = []
        priority = 1

        # 建议 1: 低评分 skill 处理
        low_scores = [s for s in scores if s.total_score < 60]
        if low_scores:
            names = ", ".join(f"`{s.skill_id}`" for s in low_scores[:3])
            suggestions.append(
                f"**P{priority}** 🔧 关注低评分 Skills: {names} — "
                f"可通过 `skills-monitor evaluate -s <skill_id> -v` 查看详细问题"
            )
            priority += 1

        # 建议 2: 满意度数据不足的 skill
        needs_data = [s for s in scores if s.factors.get("satisfaction") is None]
        if needs_data:
            names = ", ".join(f"`{s.skill_id}`" for s in needs_data[:3])
            suggestions.append(
                f"**P{priority}** 📊 以下 Skills 满意度数据不足: {names} — "
                f"多使用即可自动积累对话满意度评估数据"
            )
            priority += 1

        # 建议 3: 未使用的 skill
        used_week = set(r["skill_id"] for r in week_runs)
        runnable_slugs = {s.slug for s in runnable}
        unused = runnable_slugs - used_week
        if len(unused) > 3:
            suggestions.append(
                f"**P{priority}** 💤 有 {len(unused)} 个可运行 Skills 过去 7 天未使用 — "
                f"建议评估是否需要保留或替换"
            )
            priority += 1

        # 建议 4: 覆盖度补充
        complement_recs = [r for r in recommendations if r.reason_type == "complement"]
        if complement_recs:
            names = ", ".join(f"**{r.skill_info['name']}**" for r in complement_recs[:2])
            suggestions.append(
                f"**P{priority}** 💡 补充缺失能力: 推荐安装 {names} — "
                f"查看推荐: `skills-monitor recommend`"
            )
            priority += 1

        # 建议 5: 定期基准测试
        if scores and len(scores) >= 3:
            suggestions.append(
                f"**P{priority}** 📊 建议对核心 Skills 定期运行基准测试 — "
                f"`skills-monitor benchmark <skill_id>`"
            )

        lines = [
            f"## 💡 优化建议",
            f"",
        ]

        if suggestions:
            for s in suggestions:
                lines.append(f"{s}")
                lines.append(f"")
        else:
            lines.append(f"✅ 系统状态良好，暂无需要优化的地方！继续保持 🎉")
            lines.append(f"")

        lines.extend([f"---", f""])
        return lines

    def _section_install_recommendations(self, recommendations: List[Recommendation]) -> List[str]:
        """推荐安装区块"""
        lines = [
            f"## 📦 推荐安装",
            f"",
            f"| 优先级 | 名称 | 分类 | 推荐分 | 类型 | 理由 |",
            f"|--------|------|------|--------|------|------|",
        ]

        type_labels = {
            "complement": "💡 互补",
            "upgrade": "⬆️ 升级",
            "collaborative": "🤝 协同",
            "popular": "🔥 热门",
        }

        for i, rec in enumerate(recommendations[:5], 1):
            label = type_labels.get(rec.reason_type, rec.reason_type)
            detail = rec.reason_detail[:40]
            lines.append(
                f"| {i} | **{rec.skill_info['name']}** (`{rec.skill_info['slug']}`) | "
                f"{rec.skill_info['category']} | {rec.score:.0f} | {label} | {detail} |"
            )

        lines.extend([f"", f"---", f""])
        return lines

    def save_report(self, content: str, trigger: str = "scheduled") -> str:
        """保存报告到文件"""
        now = datetime.now()
        filename = f"diagnostic_{trigger}_{now.strftime('%Y%m%d_%H%M%S')}.md"
        filepath = str(Path(self.reports_dir) / filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        return filepath

    def generate_and_save(
        self,
        trigger: str = "scheduled",
        extra_context: Optional[str] = None,
    ) -> Tuple[str, str]:
        """生成并保存诊断报告，返回 (报告内容, 文件路径)"""
        content = self.generate_diagnostic_report(trigger=trigger, extra_context=extra_context)
        filepath = self.save_report(content, trigger=trigger)
        return content, filepath

    def generate_wecom_summary(self, full_report: str) -> str:
        """
        从完整报告中提取适合企微推送的摘要版本
        企微 Markdown 消息有 4096 字节限制，这里提取关键部分
        """
        lines = full_report.split("\n")
        summary_lines = []
        in_section = False
        target_sections = {
            "系统健康度", "问题发现", "优化建议",
        }

        for line in lines:
            # 报告标题
            if line.startswith("# "):
                summary_lines.append(line)
                summary_lines.append("")
                continue

            # 引用头信息
            if line.startswith("> "):
                summary_lines.append(line)
                continue

            # 分割线
            if line.strip() == "---":
                if in_section:
                    summary_lines.append("")
                in_section = False
                continue

            # 检测目标区块
            if line.startswith("## "):
                in_section = any(s in line for s in target_sections)
                if in_section:
                    summary_lines.append(line)
                    summary_lines.append("")
                continue

            # 目标区块内容
            if in_section:
                summary_lines.append(line)

        # 添加页脚
        summary_lines.extend([
            "",
            "---",
            "*完整报告请查看本地文件 | `skills-monitor diagnose`*",
        ])

        return "\n".join(summary_lines)
