"""
综合评估引擎 v0.5.0 — 7 因子加权评分模型
==========================================
本地因子（85%）：
  成功率          0.25
  响应时间        0.18
  满意度(隐性)    0.20
  复用率          0.12
  稳定性          0.10
社区因子（15%）：
  社区热度  🆕    0.08   ← ClawHub 下载量+星标
  社区评分  🆕    0.07   ← ClawHub 星标密度

安全机制：
  - 评分因子可展示给用户，但权重比例不暴露
  - API/CLI 响应中不含 weights 字段
  - 社区数据不可用时，权重自动回退分配到本地因子
"""

import math
import statistics
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

from skills_monitor.data.store import DataStore


# ──────── 权重配置（仅内部使用，不暴露） ────────

_WEIGHTS_V2 = {
    "success_rate": 0.25,
    "response_time": 0.18,
    "satisfaction": 0.20,
    "reuse_rate": 0.12,
    "stability": 0.10,
    "community_popularity": 0.08,
    "community_rating": 0.07,
}

# v0.4 兼容权重（无社区数据时自动回退）
_WEIGHTS_V1_FALLBACK = {
    "success_rate": 0.30,
    "response_time": 0.20,
    "satisfaction": 0.25,
    "reuse_rate": 0.15,
    "stability": 0.10,
}

# 因子展示标签
FACTOR_LABELS = {
    "success_rate": "成功率",
    "response_time": "响应时间",
    "satisfaction": "满意度(隐性)",
    "reuse_rate": "复用率",
    "stability": "稳定性",
    "community_popularity": "社区热度",
    "community_rating": "社区评分",
}

# 归一化参考值
NORMALIZATION_REFS = {
    "response_time_excellent_ms": 1000,
    "response_time_poor_ms": 30000,
    "min_runs_for_reuse": 3,
    "reuse_high_threshold": 10,
    "stability_window_days": 7,
}


# ──────── 归一化函数 ────────

def normalize_success_rate(rate: float) -> float:
    if rate >= 100:
        return 1.0
    if rate <= 0:
        return 0.0
    if rate >= 90:
        return 0.8 + (rate - 90) / 50
    return rate / 100 * 0.8


def normalize_response_time(avg_ms: Optional[float]) -> float:
    if avg_ms is None:
        return 0.5
    excellent = NORMALIZATION_REFS["response_time_excellent_ms"]
    poor = NORMALIZATION_REFS["response_time_poor_ms"]
    if avg_ms <= excellent:
        return 1.0
    if avg_ms >= poor:
        return 0.0
    ratio = (avg_ms - excellent) / (poor - excellent)
    return max(0, 1 - math.pow(ratio, 0.7))


def normalize_satisfaction(avg_rating: Optional[float]) -> float:
    if avg_rating is None:
        return 0.5
    return max(0, min(1, (avg_rating - 1) / 4))


# ──────── 向后兼容别名（旧测试/旧代码引用） ────────
def normalize_user_rating(avg_rating: Optional[float]) -> float:
    return normalize_satisfaction(avg_rating)


def normalize_reuse_rate(total_runs: int, days_active: int = 7) -> float:
    if total_runs < NORMALIZATION_REFS["min_runs_for_reuse"]:
        return 0.2
    daily_avg = total_runs / max(days_active, 1)
    threshold = NORMALIZATION_REFS["reuse_high_threshold"] / 7
    if daily_avg >= threshold:
        return 1.0
    return min(1.0, daily_avg / threshold)


def normalize_stability(durations: List[float]) -> float:
    if len(durations) < 2:
        return 0.5
    mean = statistics.mean(durations)
    if mean == 0:
        return 1.0
    cv = statistics.stdev(durations) / mean
    if cv <= 0.1:
        return 1.0
    if cv >= 1.0:
        return 0.0
    return max(0, 1 - cv)


def normalize_community_popularity(downloads: int, max_downloads: int = 100000) -> float:
    """社区热度归一化：对数归一化 log(d+1)/log(max+1)"""
    if downloads <= 0:
        return 0.0
    return min(1.0, math.log(downloads + 1) / math.log(max_downloads + 1))


def normalize_community_rating(stars: int, installs: int) -> float:
    """社区评分归一化：stars/installs 密度，范围 [0, 1]"""
    if installs <= 0 or stars <= 0:
        return 0.0
    density = stars / installs
    # 密度上限约 0.5（50% 的人给 star），归一化到 [0,1]
    return min(1.0, density / 0.5)


# ──────── 等级 ────────

def _score_to_grade(score: float) -> str:
    if score >= 90:
        return "A+"
    elif score >= 80:
        return "A"
    elif score >= 70:
        return "B"
    elif score >= 60:
        return "C"
    elif score >= 50:
        return "D"
    else:
        return "F"


def _grade_emoji(grade: str) -> str:
    return {"A+": "🏆", "A": "🥇", "B": "🥈", "C": "🥉", "D": "⚠️", "F": "❌"}.get(grade, "")


def _grade_label(grade: str) -> str:
    return {"A+": "卓越", "A": "优秀", "B": "良好", "C": "合格", "D": "待改进", "F": "不合格"}.get(grade, "")


def _factor_level(normalized_score: float) -> str:
    """归一化分数 → 等级描述"""
    if normalized_score >= 0.9:
        return "优秀"
    elif normalized_score >= 0.7:
        return "良好"
    elif normalized_score >= 0.5:
        return "中等"
    elif normalized_score >= 0.3:
        return "偏低"
    else:
        return "不足"


# ──────── SkillScore ────────

class SkillScore:
    """单个 skill 的综合评分"""

    def __init__(
        self,
        skill_id: str,
        factors: Dict[str, float],
        normalized: Dict[str, float],
        weighted: Dict[str, float],
        total_score: float,
        grade: str,
        details: Dict[str, Any],
    ):
        self.skill_id = skill_id
        self.factors = factors
        self.normalized = normalized
        self.weighted = weighted
        self.total_score = total_score
        self.grade = grade
        self.details = details

    def to_dict(self, include_weights: bool = False) -> Dict[str, Any]:
        """
        输出评分字典
        
        ⚠️ include_weights 默认 False：不暴露权重信息
           仅内部诊断/调试时设为 True
        """
        result = {
            "skill_id": self.skill_id,
            "total_score": round(self.total_score, 1),
            "grade": self.grade,
            "grade_label": f"{_grade_emoji(self.grade)} {self.grade} ({_grade_label(self.grade)})",
            "factors": {},
            "raw_factors": {k: round(v, 4) if isinstance(v, float) else v for k, v in self.factors.items()},
            "normalized_factors": {k: round(v * 100, 1) for k, v in self.normalized.items()},
            "details": self.details,
        }

        for key in self.normalized:
            norm_val = self.normalized[key]
            factor_info = {
                "score": round(norm_val * 100, 1),
                "level": _factor_level(norm_val),
            }
            # 生成描述（不含权重）
            factor_info["desc"] = self._factor_desc(key)
            result["factors"][FACTOR_LABELS.get(key, key)] = factor_info

        if include_weights:
            result["_weights"] = {k: round(v, 3) for k, v in self.weighted.items()}

        return result

    def _factor_desc(self, key: str) -> str:
        """生成因子的自然语言描述（不含权重信息）"""
        raw = self.factors.get(key)
        if key == "success_rate" and raw is not None:
            return f"近期成功率{raw:.1f}%"
        elif key == "response_time" and raw is not None:
            return f"平均响应{raw:.0f}ms"
        elif key == "satisfaction" and raw is not None:
            return f"对话满意度{raw:.1f}/5"
        elif key == "reuse_rate" and raw is not None:
            return f"累计使用{int(raw)}次"
        elif key == "stability" and raw is not None:
            return f"响应波动CV={raw:.2f}"
        elif key == "community_popularity" and raw is not None:
            return f"社区下载量{int(raw)}"
        elif key == "community_rating" and raw is not None:
            return f"社区星标{int(raw)}"
        return "数据不足"

    def format_report(self) -> str:
        """格式化评分报告（不含权重列）"""
        grade_full = f"{_grade_emoji(self.grade)} {self.grade} ({_grade_label(self.grade)})"
        lines = [
            f"📊 [{self.skill_id}] 综合评分: {self.total_score:.1f}/100  {grade_full}",
            f"{'─' * 50}",
            f"  {'因子':<14} {'得分':<10} {'等级':<8} {'说明':<20}",
            f"  {'─' * 48}",
        ]
        for key in self.normalized:
            label = FACTOR_LABELS.get(key, key)
            norm = self.normalized[key]
            score_100 = round(norm * 100, 1)
            level = _factor_level(norm)
            desc = self._factor_desc(key)
            lines.append(f"  {label:<14} {score_100:<10} {level:<8} {desc}")

        lines.append(f"  {'─' * 48}")
        return "\n".join(lines)


# ──────── SkillEvaluator ────────

class SkillEvaluator:
    """综合评估引擎 v0.5.0 — 7 因子"""

    def __init__(self, store: DataStore, agent_id: str = "", community_data: Dict = None):
        self.store = store
        self.agent_id = agent_id
        self._community_data = community_data or {}

    def set_community_data(self, data: Dict[str, Dict]):
        """设置社区数据（从 ClawHub 获取）"""
        self._community_data = data

    def _get_active_weights(self, has_community: bool) -> Dict[str, float]:
        """根据社区数据可用性选择权重组"""
        if has_community:
            return dict(_WEIGHTS_V2)
        else:
            return dict(_WEIGHTS_V1_FALLBACK)

    def evaluate_skill(self, skill_id: str) -> SkillScore:
        """对单个 skill 进行 7 因子综合评估"""
        summary = self.store.get_skill_summary(skill_id, self.agent_id)

        all_runs = self.store.get_runs(skill_id=skill_id, agent_id=self.agent_id, limit=500)
        user_runs = [r for r in all_runs if not (r.get("task_name", "").startswith("[benchmark]"))]

        success_rate = summary["success_rate"]
        avg_duration = summary["avg_duration_ms"]
        avg_rating = summary["avg_rating"]
        total_runs = summary["total_runs"]

        durations = [
            r["duration_ms"] for r in user_runs
            if r.get("duration_ms") and r["status"] == "success"
        ]
        cv = None
        if len(durations) >= 2:
            mean_d = statistics.mean(durations)
            if mean_d > 0:
                cv = statistics.stdev(durations) / mean_d

        # 社区数据
        community = self._community_data.get(skill_id, {})
        downloads = community.get("downloads", 0)
        stars = community.get("stars", 0)
        installs = community.get("current_installs", downloads)
        has_community = downloads > 0 or stars > 0

        # 原始值
        factors = {
            "success_rate": success_rate,
            "response_time": avg_duration,
            "satisfaction": avg_rating,
            "reuse_rate": total_runs,
            "stability": cv,
        }
        if has_community:
            factors["community_popularity"] = downloads
            factors["community_rating"] = stars

        # 归一化
        normalized = {
            "success_rate": normalize_success_rate(success_rate),
            "response_time": normalize_response_time(avg_duration),
            "satisfaction": normalize_satisfaction(avg_rating),
            "reuse_rate": normalize_reuse_rate(total_runs),
            "stability": normalize_stability(durations),
        }
        if has_community:
            normalized["community_popularity"] = normalize_community_popularity(downloads)
            normalized["community_rating"] = normalize_community_rating(stars, installs)

        # 选择权重并加权
        weights = self._get_active_weights(has_community)
        weighted = {}
        for key in weights:
            weighted[key] = normalized.get(key, 0) * weights[key]

        total_score = sum(weighted.values()) * 100
        total_score = round(min(100, max(0, total_score)), 1)
        grade = _score_to_grade(total_score)

        details = {
            "total_runs": total_runs,
            "success_runs": summary["success_count"],
            "implicit_feedback_count": summary.get("implicit_feedback_count", 0),
            "avg_confidence": summary.get("avg_confidence"),
            "recent_durations_count": len(durations),
            "has_community_data": has_community,
            "weight_mode": "7-factor" if has_community else "5-factor-fallback",
            "evaluated_at": datetime.now().isoformat(),
        }

        return SkillScore(
            skill_id=skill_id,
            factors=factors,
            normalized=normalized,
            weighted=weighted,
            total_score=total_score,
            grade=grade,
            details=details,
        )

    def evaluate_all(self, skill_ids: List[str] = None) -> List[SkillScore]:
        """批量评估所有 skill"""
        if skill_ids is None:
            skill_ids = []
        scores = []
        self.last_failures: List[Tuple[str, str]] = []
        for sid in skill_ids:
            try:
                score = self.evaluate_skill(sid)
                if score.details["total_runs"] > 0:
                    scores.append(score)
            except Exception as e:
                # 不要吞掉：记录失败，便于排障（不会影响主流程）
                self.last_failures.append((sid, f"{type(e).__name__}: {e}"))
        scores.sort(key=lambda s: s.total_score, reverse=True)
        return scores

    def generate_evaluation_report(self, scores: List[SkillScore]) -> str:
        """生成综合评估报告（Markdown，不含权重）"""
        now = datetime.now()
        lines = [
            f"# 📊 Skills 综合评估报告",
            f"",
            f"> **生成时间**: {now.strftime('%Y-%m-%d %H:%M:%S')}  ",
            f"> **评估模型**: 7 因子加权评分 v0.5.0  ",
            f"> **评估 Skills 数**: {len(scores)}",
            f"",
            f"---",
            f"",
            f"## 评分排行",
            f"",
            f"| 排名 | Skill | 总分 | 等级 | 成功率 | 响应 | 满意度 | 复用 | 稳定性 | 社区 |",
            f"|------|-------|------|------|--------|------|--------|------|--------|------|",
        ]

        for i, score in enumerate(scores, 1):
            sr = f"{score.factors['success_rate']:.0f}%" if score.factors.get('success_rate') is not None else "-"
            rt = f"{score.factors['response_time']:.0f}ms" if score.factors.get('response_time') is not None else "-"
            sa = f"{score.factors['satisfaction']:.1f}" if score.factors.get('satisfaction') is not None else "-"
            rr = str(score.factors.get('reuse_rate', '-'))
            st = f"{score.factors['stability']:.2f}" if score.factors.get('stability') is not None else "-"
            cm = "✅" if score.details.get("has_community_data") else "-"
            grade_short = f"{_grade_emoji(score.grade)} {score.grade}"

            lines.append(
                f"| {i} | {score.skill_id} | **{score.total_score:.1f}** | {grade_short} | "
                f"{sr} | {rt} | {sa} | {rr} | {st} | {cm} |"
            )

        lines.extend([
            f"", f"---", f"",
            f"## 详细评分", f"",
        ])

        for score in scores:
            lines.append(f"### {score.skill_id}")
            lines.append(f"")
            lines.append(f"```")
            lines.append(score.format_report())
            lines.append(f"```")
            lines.append(f"")

        # 评分说明（不含权重！）
        lines.extend([
            f"---", f"",
            f"## 评分模型说明", f"",
            f"| 因子 | 说明 |",
            f"|------|------|",
            f"| 成功率 | 执行成功率越高越好 |",
            f"| 响应时间 | 平均响应时间越短越好 |",
            f"| 满意度 | 对话语义隐性推断 |",
            f"| 复用率 | 使用频次越高说明价值越大 |",
            f"| 稳定性 | 响应时间变异系数越小越稳定 |",
            f"| 社区热度 | 社区下载量和安装量 |",
            f"| 社区评分 | 社区星标和口碑 |",
            f"",
            f"> 注：各因子均为 0-100 分制，总分为加权综合。",
        ])

        return "\n".join(lines)

    def trend_analysis(self, skill_id: str, days: int = 7) -> Dict[str, Any]:
        """趋势分析：最近 N 天的指标变化"""
        metrics = self.store.get_metrics(skill_id=skill_id, agent_id=self.agent_id, days=days)
        if not metrics:
            return {"skill_id": skill_id, "trend": "no_data", "days": days}

        metrics.sort(key=lambda m: m["date"])
        dates = [m["date"] for m in metrics]
        success_rates = [
            round(m["success_count"] / m["total_runs"] * 100, 1) if m["total_runs"] > 0 else 0
            for m in metrics
        ]
        avg_durations = [m["avg_duration_ms"] for m in metrics if m.get("avg_duration_ms")]

        if len(success_rates) >= 2:
            if success_rates[-1] > success_rates[0]:
                sr_trend = "improving"
            elif success_rates[-1] < success_rates[0]:
                sr_trend = "declining"
            else:
                sr_trend = "stable"
        else:
            sr_trend = "insufficient"

        return {
            "skill_id": skill_id,
            "days": days,
            "data_points": len(metrics),
            "success_rate_trend": sr_trend,
            "success_rates": dict(zip(dates, success_rates)),
            "avg_durations": avg_durations,
            "latest_success_rate": success_rates[-1] if success_rates else None,
            "first_success_rate": success_rates[0] if success_rates else None,
        }
