"""
Skill 推荐引擎
基于已安装 skills 的分类分布、使用频率和隐性满意度，推荐扩展 skills

推荐策略：
1. 互补推荐 — 找出用户缺少的分类，推荐该分类的热门 skill
2. 升级推荐 — 对低满意度的 skill 推荐同类替代品
3. 协同推荐 — "使用 A 的用户也在使用 B"（基于分类相关性模拟）
4. 热门兜底推荐 — 当用户尚未安装任何 skill 时，从官方 TOP10 精选 3 个
"""

import json
import math
from pathlib import Path
from collections import Counter
from typing import Any, Dict, List, Optional

from skills_monitor.data.store import DataStore
from skills_monitor.adapters.skill_registry import SkillRegistry
from skills_monitor.adapters.clawhub_client import ClawHubClient


# ──────── SkillHub 模拟目录 ────────
# 真实场景中从 SkillHub API 获取，Demo 阶段用硬编码模拟

SKILLHUB_CATALOG: List[Dict[str, Any]] = [
    # 数据采集
    {"slug": "tushare-data", "name": "TuShare 数据源", "category": "数据采集",
     "description": "基于 TuShare Pro 的 A 股全量数据接口", "rating": 4.5, "installs": 1200},
    {"slug": "eastmoney-data", "name": "东方财富数据", "category": "数据采集",
     "description": "东方财富实时行情和公告数据", "rating": 4.2, "installs": 890},
    {"slug": "crypto-data-feed", "name": "加密货币数据", "category": "数据采集",
     "description": "主流加密货币实时行情和链上数据", "rating": 4.0, "installs": 650},

    # 宏观分析
    {"slug": "global-macro-tracker", "name": "全球宏观追踪", "category": "宏观分析",
     "description": "全球主要经济体的宏观经济指标追踪", "rating": 4.3, "installs": 520},
    {"slug": "fed-policy-analyzer", "name": "美联储政策分析", "category": "宏观分析",
     "description": "美联储议息会议决议及政策影响分析", "rating": 4.1, "installs": 380},

    # 新闻情报
    {"slug": "ai-news-digest", "name": "AI 新闻摘要", "category": "新闻情报",
     "description": "基于大模型的金融新闻智能摘要和情感分析", "rating": 4.6, "installs": 1500},
    {"slug": "social-sentiment", "name": "社交媒体情绪", "category": "新闻情报",
     "description": "雪球/东方财富等平台的投资者情绪分析", "rating": 3.9, "installs": 780},

    # 技术筛选
    {"slug": "quant-factor-screener", "name": "量化因子筛选器", "category": "技术筛选",
     "description": "多因子量化选股模型，支持自定义因子组合", "rating": 4.7, "installs": 2100},
    {"slug": "pattern-recognition", "name": "K线形态识别", "category": "技术筛选",
     "description": "基于深度学习的 K 线形态自动识别", "rating": 4.4, "installs": 920},

    # 交易信号
    {"slug": "options-signal", "name": "期权信号生成", "category": "交易信号",
     "description": "基于隐含波动率和 Greeks 的期权交易信号", "rating": 4.3, "installs": 450},
    {"slug": "crypto-signal-pro", "name": "加密货币信号", "category": "交易信号",
     "description": "加密货币多因子交易信号生成器", "rating": 4.0, "installs": 670},

    # 策略回测
    {"slug": "quantitative-backtest", "name": "量化回测引擎 v2", "category": "策略回测",
     "description": "高性能量化策略回测框架，支持分钟级数据", "rating": 4.8, "installs": 3200},
    {"slug": "portfolio-optimizer", "name": "组合优化器", "category": "策略回测",
     "description": "基于 MPT 的投资组合权重优化", "rating": 4.5, "installs": 890},

    # 量化监控
    {"slug": "realtime-alert", "name": "实时预警系统", "category": "量化监控",
     "description": "价格、成交量、技术指标的实时预警", "rating": 4.2, "installs": 760},
    {"slug": "risk-monitor", "name": "风险监控", "category": "量化监控",
     "description": "投资组合实时风险监控和预警", "rating": 4.4, "installs": 540},

    # 可视化
    {"slug": "interactive-charts", "name": "交互式图表", "category": "可视化",
     "description": "基于 ECharts 的金融数据交互可视化", "rating": 4.5, "installs": 1800},

    # 资金追踪
    {"slug": "institution-tracker", "name": "机构资金追踪", "category": "资金追踪",
     "description": "主力机构资金流向实时追踪", "rating": 4.3, "installs": 990},
    {"slug": "northbound-flow", "name": "北向资金追踪", "category": "资金追踪",
     "description": "沪深港通北向资金实时监控", "rating": 4.6, "installs": 1100},
]

OFFICIAL_TOP_DATASET = Path(__file__).resolve().parent.parent / "data" / "top1000_skills_dataset.json"


class RecommendationReason:
    """推荐理由"""

    COMPLEMENT = "complement"    # 互补推荐
    UPGRADE = "upgrade"          # 升级推荐
    COLLABORATIVE = "collaborative"  # 协同推荐
    POPULAR = "popular"          # 热门推荐

    LABELS = {
        COMPLEMENT: "💡 互补推荐 — 补充你缺少的能力",
        UPGRADE: "⬆️ 升级推荐 — 替代低满意度的 skill",
        COLLABORATIVE: "🤝 协同推荐 — 同类用户也在使用",
        POPULAR: "🔥 热门推荐 — 官方 TOP 热门精选",
    }


class Recommendation:
    """单条推荐"""

    def __init__(
        self,
        skill_info: Dict[str, Any],
        reason_type: str,
        reason_detail: str,
        score: float,
        related_installed: Optional[str] = None,
    ):
        self.skill_info = skill_info
        self.reason_type = reason_type
        self.reason_detail = reason_detail
        self.score = score  # 推荐分 (0-100)
        self.related_installed = related_installed

    def to_dict(self) -> Dict[str, Any]:
        slug = self.skill_info["slug"]
        return {
            "slug": slug,
            "name": self.skill_info["name"],
            "category": self.skill_info.get("category", "未分类"),
            "description": self.skill_info.get("description", ""),
            "hub_rating": self.skill_info.get("rating"),
            "hub_installs": self.skill_info.get("installs"),
            "reason_type": self.reason_type,
            "reason_label": RecommendationReason.LABELS.get(self.reason_type, ""),
            "reason_detail": self.reason_detail,
            "recommendation_score": round(self.score, 1),
            "related_installed": self.related_installed,
            "official_rank": self.skill_info.get("rank"),
            "selection_logic": self.skill_info.get("selection_logic"),
            "source": self.skill_info.get("source", "catalog"),
            "benchmark_quality": self.skill_info.get("baseline_quality"),
            "benchmark_success_rate": self.skill_info.get("baseline_success_rate"),
            "tags": self.skill_info.get("tags", []),
            # 安装相关 URL
            "detail_url": f"https://clawhub.ai/skills/{slug}",
            "install_url": f"https://clawhub.ai/api/v1/download?slug={slug}",
            "install_command": f"python install_skills.py {slug}",
        }

    def format_line(self) -> str:
        """格式化为单行"""
        label = RecommendationReason.LABELS.get(self.reason_type, "")
        rating = f"⭐{self.skill_info.get('rating', 'N/A')}"
        installs = self.skill_info.get("installs", 0)
        extras = []
        if self.skill_info.get("rank"):
            extras.append(f"TOP{self.skill_info['rank']}")
        if self.skill_info.get("selection_logic"):
            extras.append(self.skill_info["selection_logic"])
        extra_text = f" | {'；'.join(extras)}" if extras else ""
        return (
            f"  {label}\n"
            f"    📦 {self.skill_info['name']} ({self.skill_info['slug']})\n"
            f"       {self.skill_info.get('description', '')}\n"
            f"       {rating}  安装量: {installs}  推荐分: {self.score:.0f}{extra_text}\n"
            f"       💬 {self.reason_detail}"
        )


class SkillRecommender:
    """Skill 推荐引擎"""

    def __init__(
        self,
        registry: SkillRegistry,
        store: DataStore,
        agent_id: str,
        catalog: Optional[List[Dict[str, Any]]] = None,
    ):
        self.registry = registry
        self.store = store
        self.agent_id = agent_id
        self.catalog = catalog or SKILLHUB_CATALOG
        self._installed_slugs = {s.slug for s in registry.list_skills()}

    def _get_user_category_profile(self) -> Dict[str, Any]:
        """分析用户的分类使用情况"""
        installed = self.registry.list_skills()
        category_counts = Counter(s.category for s in installed)

        category_usage = {}
        for skill in installed:
            summary = self.store.get_skill_summary(skill.slug, self.agent_id)
            cat = skill.category
            if cat not in category_usage:
                category_usage[cat] = {"runs": 0, "avg_rating": []}
            category_usage[cat]["runs"] += summary["total_runs"]
            if summary.get("avg_rating"):
                category_usage[cat]["avg_rating"].append(summary["avg_rating"])

        for cat in category_usage:
            ratings = category_usage[cat]["avg_rating"]
            category_usage[cat]["avg_rating"] = (
                round(sum(ratings) / len(ratings), 1) if ratings else None
            )

        return {
            "installed_categories": dict(category_counts),
            "usage": category_usage,
        }

    def _get_available_catalog(self) -> List[Dict[str, Any]]:
        """过滤掉已安装的 skill"""
        return [s for s in self.catalog if s["slug"] not in self._installed_slugs]

    def _get_official_top10_candidates(self) -> List[Dict[str, Any]]:
        """读取官方 TOP10 候选池（优先线上热门榜，降级到本地基准数据集）"""
        candidates: List[Dict[str, Any]] = []

        try:
            client = ClawHubClient()
            online_items = client.get_popular_skills(limit=10)
            for idx, item in enumerate(online_items, 1):
                candidates.append({
                    "rank": item.get("rank", idx),
                    "slug": item.get("slug", ""),
                    "name": item.get("name") or item.get("slug", "unknown"),
                    "category": item.get("category") or (item.get("tags") or ["通用"])[0],
                    "description": item.get("description", ""),
                    "rating": round(item.get("star_density", 0) * 25, 1) if item.get("star_density") is not None else None,
                    "installs": item.get("installs", 0),
                    "stars": item.get("stars", 0),
                    "baseline_quality": item.get("baseline_quality"),
                    "baseline_success_rate": item.get("baseline_success_rate"),
                    "tags": item.get("tags", []),
                    "source": item.get("source", "official_popular"),
                })
        except Exception:
            candidates = []

        if candidates:
            deduped = []
            seen = set()
            for item in candidates:
                slug = item.get("slug")
                if slug and slug not in seen and slug not in self._installed_slugs:
                    seen.add(slug)
                    deduped.append(item)
            if deduped:
                return deduped[:10]

        try:
            with open(OFFICIAL_TOP_DATASET, "r", encoding="utf-8") as f:
                dataset = json.load(f)
            items = []
            for raw in dataset[:10]:
                slug = raw.get("slug")
                if not slug or slug in self._installed_slugs:
                    continue
                items.append({
                    "rank": raw.get("rank"),
                    "slug": slug,
                    "name": raw.get("name", slug),
                    "category": raw.get("category", "通用"),
                    "description": raw.get("description", ""),
                    "rating": round((raw.get("stars", 0) / max(raw.get("installs", 1), 1)) * 25, 1),
                    "installs": raw.get("installs", 0),
                    "stars": raw.get("stars", 0),
                    "baseline_quality": raw.get("baseline_quality"),
                    "baseline_success_rate": raw.get("baseline_success_rate"),
                    "tags": raw.get("tags", []),
                    "source": "official_top10_dataset",
                })
            return items[:10]
        except Exception:
            return []

    def _score_official_top_candidate(self, skill: Dict[str, Any], chosen_categories: set) -> float:
        """对官方 TOP10 候选 skill 做精选排序，兼顾热度、成功率、质量与分类多样性"""
        installs = float(skill.get("installs") or 0)
        baseline_quality = float(skill.get("baseline_quality") or 0)
        baseline_success_rate = float(skill.get("baseline_success_rate") or 0)
        rank = int(skill.get("rank") or 99)
        category = skill.get("category", "通用")

        install_component = min(20.0, math.log10(max(installs, 1)) * 4.0)
        quality_component = baseline_quality * 0.45
        success_component = baseline_success_rate * 100 * 0.30
        rank_component = max(0, 12 - rank)
        diversity_bonus = 8 if category not in chosen_categories else 0

        return round(
            install_component + quality_component + success_component + rank_component + diversity_bonus,
            1,
        )

    def recommend_official_top(self, max_items: int = 3) -> List[Recommendation]:
        """当用户未安装任何 skill 时，从官方 TOP10 精选 3 个"""
        top10 = self._get_official_top10_candidates()
        if not top10:
            return []

        selected: List[Recommendation] = []
        chosen_categories = set()
        remaining = list(top10)

        while remaining and len(selected) < max_items:
            scored = []
            for skill in remaining:
                score = self._score_official_top_candidate(skill, chosen_categories)
                scored.append((score, skill))
            scored.sort(key=lambda x: x[0], reverse=True)
            final_score, best = scored[0]
            chosen_categories.add(best.get("category", "通用"))

            logic_parts = [
                f"官方 TOP{best.get('rank', '?')} 热门",
                f"安装量 {best.get('installs', 0)}",
            ]
            if best.get("baseline_quality") is not None:
                logic_parts.append(f"基准质量 {best['baseline_quality']:.1f}")
            if best.get("baseline_success_rate") is not None:
                logic_parts.append(f"成功率 {best['baseline_success_rate'] * 100:.1f}%")
            if best.get("category"):
                logic_parts.append(f"补齐 {best['category']} 能力")

            best["selection_logic"] = "；".join(logic_parts)
            detail = (
                f"当前未检测到已安装 skills，兜底从官方 TOP10 中精选。"
                f"优先选择高安装量、高成功率且覆盖不同能力类别的 skill，"
                f"本次选择 {best['name']} 以补齐 {best.get('category', '通用')} 能力。"
            )
            selected.append(Recommendation(
                skill_info=best,
                reason_type=RecommendationReason.POPULAR,
                reason_detail=detail,
                score=min(100, final_score),
            ))
            remaining = [item for item in remaining if item.get("slug") != best.get("slug")]

        return selected

    def recommend_complement(self, max_items: int = 3) -> List[Recommendation]:
        """互补推荐：找出用户缺少的分类"""
        profile = self._get_user_category_profile()
        installed_cats = set(profile["installed_categories"].keys())

        all_hub_cats = set(s["category"] for s in self.catalog)
        missing_cats = all_hub_cats - installed_cats

        thin_cats = {
            cat for cat, count in profile["installed_categories"].items()
            if count <= 1
        }

        target_cats = missing_cats | thin_cats
        available = self._get_available_catalog()

        recommendations = []
        for skill in available:
            if skill["category"] in target_cats:
                score = (skill.get("rating", 3) * 15 + skill.get("installs", 0) / 100)
                if skill["category"] in missing_cats:
                    score += 20

                detail = (
                    f"你的 [{skill['category']}] 类 skill 不足，"
                    f"该 skill 在社区评分 {skill.get('rating', 'N/A')} 星"
                )

                recommendations.append(Recommendation(
                    skill_info=skill,
                    reason_type=RecommendationReason.COMPLEMENT,
                    reason_detail=detail,
                    score=min(100, score),
                ))

        recommendations.sort(key=lambda r: r.score, reverse=True)
        return recommendations[:max_items]

    def recommend_upgrade(self, max_items: int = 3) -> List[Recommendation]:
        """升级推荐：对低满意度的 skill 推荐替代品"""
        available = self._get_available_catalog()
        recommendations = []

        for skill in self.registry.list_skills():
            summary = self.store.get_skill_summary(skill.slug, self.agent_id)
            avg_rating = summary.get("avg_rating")
            success_rate = summary.get("success_rate", 100)

            if (avg_rating is not None and avg_rating < 3.5) or success_rate < 70:
                same_cat = [
                    s for s in available
                    if s["category"] == skill.category
                    and s.get("rating", 0) > (avg_rating or 3)
                ]

                for alt in same_cat:
                    score = alt.get("rating", 3) * 15 + 10
                    if avg_rating and avg_rating < 3:
                        score += 15

                    detail = (
                        f"你的 [{skill.slug}] 满意度仅 {avg_rating or 'N/A'}，"
                        f"成功率 {success_rate}%。推荐升级到 {alt['name']}"
                    )

                    recommendations.append(Recommendation(
                        skill_info=alt,
                        reason_type=RecommendationReason.UPGRADE,
                        reason_detail=detail,
                        score=min(100, score),
                        related_installed=skill.slug,
                    ))

        recommendations.sort(key=lambda r: r.score, reverse=True)
        return recommendations[:max_items]

    def recommend_collaborative(self, max_items: int = 3) -> List[Recommendation]:
        """协同推荐：基于分类相关性"""
        profile = self._get_user_category_profile()
        usage = profile["usage"]

        top_cats = sorted(
            usage.items(),
            key=lambda x: x[1]["runs"],
            reverse=True,
        )[:3]

        available = self._get_available_catalog()
        recommendations = []

        related_categories = {
            "交易信号": ["策略回测", "量化监控", "技术筛选"],
            "技术筛选": ["交易信号", "数据采集", "量化监控"],
            "数据采集": ["技术筛选", "宏观分析", "新闻情报"],
            "宏观分析": ["新闻情报", "数据采集"],
            "策略回测": ["交易信号", "量化监控"],
            "量化监控": ["交易信号", "技术筛选"],
            "新闻情报": ["宏观分析", "交易信号"],
            "资金追踪": ["交易信号", "技术筛选"],
            "可视化": ["数据采集", "技术筛选"],
        }

        for cat, _ in top_cats:
            related = related_categories.get(cat, [])
            for rel_cat in related:
                for skill in available:
                    if skill["category"] == rel_cat:
                        score = skill.get("rating", 3) * 12 + skill.get("installs", 0) / 150
                        detail = (
                            f"你经常使用 [{cat}] 类 skill，"
                            f"同类用户 Top30% 也在使用 [{rel_cat}] 类工具"
                        )
                        recommendations.append(Recommendation(
                            skill_info=skill,
                            reason_type=RecommendationReason.COLLABORATIVE,
                            reason_detail=detail,
                            score=min(100, score),
                        ))

        seen = set()
        unique = []
        for r in sorted(recommendations, key=lambda x: x.score, reverse=True):
            if r.skill_info["slug"] not in seen:
                seen.add(r.skill_info["slug"])
                unique.append(r)

        return unique[:max_items]

    def get_all_recommendations(self, max_per_type: int = 3) -> List[Recommendation]:
        """获取所有类型的推荐，去重后返回"""
        if not self._installed_slugs:
            return self.recommend_official_top(max_items=min(3, max_per_type))

        all_recs: List[Recommendation] = []
        all_recs.extend(self.recommend_complement(max_per_type))
        all_recs.extend(self.recommend_upgrade(max_per_type))
        all_recs.extend(self.recommend_collaborative(max_per_type))

        seen = set()
        unique = []
        for r in sorted(all_recs, key=lambda x: x.score, reverse=True):
            if r.skill_info["slug"] not in seen:
                seen.add(r.skill_info["slug"])
                unique.append(r)

        if unique:
            return unique
        return self.recommend_official_top(max_items=min(3, max_per_type))

    def generate_recommendation_report(self, recommendations: Optional[List[Recommendation]] = None) -> str:
        """生成推荐报告"""
        if recommendations is None:
            recommendations = self.get_all_recommendations()

        from datetime import datetime
        now = datetime.now()

        lines = [
            f"# 💡 Skills 推荐报告",
            f"",
            f"> **生成时间**: {now.strftime('%Y-%m-%d %H:%M:%S')}  ",
            f"> **已安装**: {len(self.registry.list_skills())} 个 skills  ",
            f"> **推荐数量**: {len(recommendations)} 个",
            f"",
            f"---",
            f"",
        ]

        if not recommendations:
            lines.append("暂无推荐。你的 skills 配置已经很完善！👍")
            return "\n".join(lines)

        by_type: Dict[str, List[Recommendation]] = {}
        for r in recommendations:
            by_type.setdefault(r.reason_type, []).append(r)

        for rtype, recs in by_type.items():
            label = RecommendationReason.LABELS.get(rtype, rtype)
            lines.append(f"## {label}")
            lines.append("")

            for r in recs:
                rating = f"⭐ {r.skill_info.get('rating', 'N/A')}"
                installs = r.skill_info.get("installs", 0)
                lines.extend([
                    f"### 📦 {r.skill_info['name']} (`{r.skill_info['slug']}`)",
                    f"",
                    f"- **分类**: {r.skill_info.get('category', '未分类')}",
                    f"- **描述**: {r.skill_info.get('description', '')}",
                    f"- **社区评分**: {rating}  |  **安装量**: {installs}",
                    f"- **推荐分**: {r.score:.0f}/100",
                    f"- **推荐理由**: {r.reason_detail}",
                    *( [f"- **精选逻辑**: {r.skill_info['selection_logic']}"] if r.skill_info.get("selection_logic") else [] ),
                    f"",
                ])

            lines.append("---")
            lines.append("")

        top3 = recommendations[:3]
        if top3:
            lines.extend([
                f"## 🚀 快速安装",
                f"",
                f"```bash",
            ])
            for r in top3:
                lines.append(f"python install_skills.py {r.skill_info['slug']}")
            lines.extend([
                f"```",
                f"",
            ])

        return "\n".join(lines)
