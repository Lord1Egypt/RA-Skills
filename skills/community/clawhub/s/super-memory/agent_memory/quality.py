"""
quality.py - 记忆质量评分系统
追踪记忆的有用性，反向优化检索排序
"""

from __future__ import annotations

import time
import json
import logging
import os
import threading
from pathlib import Path

logger = logging.getLogger(__name__)

# Fix (Bug 4): 线程锁，替代 fcntl 文件锁保护 quality_stats.json 并发写入
_quality_save_lock = threading.Lock()


class MemoryQuality:
    """
    记忆质量评估：

    1. 显式反馈 — 用户标记"有用/没用"
    2. 隐式信号 — 被检索次数、被引用次数
    3. 衰减修正 — 质量高的记忆延缓衰减
    4. 冷启动 — 基于规则的初始评分

    质量分数：0.0（无用）~ 1.0（极高价值）
    """

    # 隐式信号权重（总和 = 1.0，可外部覆盖）
    DEFAULT_WEIGHTS = {
        "retrieval_count": 0.10,    # 被检索次数（注意：高频检索可能意味着记忆不准，见下）
        "reference_count": 0.10,    # 被其他记忆引用次数
        "age_bonus": 0.05,          # 存活时间越长价值越高（适度）
        "explicit_feedback": 0.30,  # 用户显式反馈
        "content_quality": 0.20,    # 内容质量启发式
        "importance_base": 0.25,    # 重要度基础分（冷启动关键）
    }

    # 检索次数信号模式
    # "positive": 检索越多 = 越重要（传统假设）
    # "negative": 检索越多 = 可能记忆不准（实际场景更常见）
    # "bell": 倒 U 型 — 适度检索是好的，过多检索反而降分
    RETRIEVAL_SIGNAL_MODE = "bell"

    # bell 曲线参数：检索次数达到此值时分数最高
    BELL_SWEET_SPOT = 3
    # 超过此值分数开始显著下降
    BELL_PENALTY_THRESHOLD = 10

    def __init__(self, store, stats_path: str = None, weights: dict = None):
        self.store = store
        self._stats_path = Path(stats_path) if stats_path else Path(__file__).parent / "quality_stats.json"
        self.WEIGHTS = dict(self.DEFAULT_WEIGHTS)
        if weights:
            self.WEIGHTS.update(weights)
        self._stats = self._load_stats()
        # Fix (新功能): 确保 utility tracking 数据结构存在
        if "utility" not in self._stats:
            self._stats["utility"] = {}
        if "usage_signals" not in self._stats:
            self._stats["usage_signals"] = {}

    def _load_stats(self) -> dict:
        """加载质量统计数据"""
        if self._stats_path.exists():
            try:
                with open(self._stats_path, "r") as f:
                    return json.load(f)
            except Exception as e:
                logger.warning("quality: %s", e)
        return {"retrievals": {}, "feedback": {}, "references": {}}

    def _save_stats(self):
        """持久化统计数据（Fix (Bug 4): 线程锁防并发写入损坏）"""
        self._stats_path.parent.mkdir(parents=True, exist_ok=True)
        tmp = str(self._stats_path) + ".tmp"
        with _quality_save_lock:
            try:
                with open(tmp, "w") as f:
                    json.dump(self._stats, f, ensure_ascii=False)
                os.replace(tmp, str(self._stats_path))
            except Exception as e:
                logger.warning("quality: %s", e)

    # ── 信号记录 ────────────────────────────────────────

    def record_retrieval(self, memory_id: str):
        """记录一次检索命中"""
        retrievals = self._stats["retrievals"]
        retrievals[memory_id] = retrievals.get(memory_id, 0) + 1
        self._save_stats()

    def record_reference(self, memory_id: str):
        """记录一次被引用"""
        refs = self._stats["references"]
        refs[memory_id] = refs.get(memory_id, 0) + 1
        self._save_stats()

    def record_feedback(self, memory_id: str, useful: bool, note: str = None):
        """
        记录用户显式反馈。

        参数:
            useful: True=有用, False=没用
            note: 可选备注
        """
        feedback = self._stats["feedback"]
        feedback[memory_id] = {
            "useful": useful,
            "note": note,
            "timestamp": int(time.time()),
        }
        self._save_stats()
        logger.info(f"📝 反馈记录: {memory_id} → {'👍' if useful else '👎'}")

    # ── 质量计算 ────────────────────────────────────────

    def compute_quality(self, memory: dict) -> dict:
        """
        计算单条记忆的质量分数。

        返回:
        {
            "memory_id": str,
            "quality_score": float,    # 0.0 ~ 1.0
            "grade": str,              # A/B/C/D/F
            "breakdown": dict,         # 各维度得分
            "recommendation": str,     # 建议操作
        }
        """
        mid = memory.get("memory_id", "")
        breakdown = {}

        # 1. 被检索次数信号（支持 positive/negative/bell 模式）
        retrieval_count = self._stats["retrievals"].get(mid, 0)
        retrieval_score = self._compute_retrieval_signal(retrieval_count)
        breakdown["retrieval"] = retrieval_score * self.WEIGHTS["retrieval_count"]

        # 2. 被引用次数 (0~1)
        ref_count = self._stats["references"].get(mid, 0)
        breakdown["reference"] = min(1.0, ref_count / 5) * self.WEIGHTS["reference_count"]

        # 3. 存活时间 (适度奖励)
        age_days = (time.time() - memory.get("time_ts", time.time())) / 86400
        if age_days > 30:
            breakdown["age"] = min(1.0, age_days / 365) * self.WEIGHTS["age_bonus"]
        else:
            breakdown["age"] = 0

        # 4. 显式反馈
        feedback = self._stats["feedback"].get(mid)
        if feedback:
            breakdown["feedback"] = (1.0 if feedback["useful"] else 0.0) * self.WEIGHTS["explicit_feedback"]
        else:
            breakdown["feedback"] = 0.5 * self.WEIGHTS["explicit_feedback"]  # 无反馈给中性分

        # 5. 内容质量启发式
        content = memory.get("content", "")
        quality_signals = 0
        if len(content) > 50:
            quality_signals += 0.3
        if len(content) > 200:
            quality_signals += 0.2
        if memory.get("is_aggregated"):
            quality_signals += 0.2
        breakdown["content"] = min(1.0, quality_signals) * self.WEIGHTS["content_quality"]

        # 6. 重要度基础分（确保新记忆不会因冷启动被埋没）
        imp = memory.get("importance", "medium")
        imp_scores = {"high": 1.0, "medium": 0.5, "low": 0.2}
        breakdown["importance_base"] = imp_scores.get(imp, 0.5) * self.WEIGHTS["importance_base"]

        # 总分
        total = sum(breakdown.values())
        total = round(min(1.0, max(0.0, total)), 4)

        # 等级
        if total >= 0.8:
            grade = "A"
        elif total >= 0.6:
            grade = "B"
        elif total >= 0.4:
            grade = "C"
        elif total >= 0.2:
            grade = "D"
        else:
            grade = "F"

        # 建议
        if grade == "F" and age_days > 90:
            recommendation = "考虑删除或归档"
        elif grade == "D":
            recommendation = "价值较低，可压缩"
        elif grade == "A":
            recommendation = "高价值记忆，永不衰减"
        else:
            recommendation = "正常保留"

        return {
            "memory_id": mid,
            "quality_score": total,
            "grade": grade,
            "breakdown": breakdown,
            "recommendation": recommendation,
        }

    def _compute_retrieval_signal(self, count: int) -> float:
        """
        将检索次数转化为 0~1 的质量信号。

        模式:
        - positive: 线性增长（传统假设）
        - negative: 检索越多分越低（用户反复查 = 记忆不准）
        - bell: 倒 U 型（适度检索好，过多反而差）
        """
        if count == 0:
            return 0.0

        mode = self.RETRIEVAL_SIGNAL_MODE

        if mode == "positive":
            return min(1.0, count / 10)

        elif mode == "negative":
            # 检索 1-2 次是正常的，超过越多扣分越多
            if count <= 2:
                return 0.8
            return max(0.0, 0.8 - (count - 2) * 0.15)

        elif mode == "bell":
            # 倒 U 型：在 sweet_spot 处最高，超过 penalty_threshold 后急剧下降
            sweet = self.BELL_SWEET_SPOT
            threshold = self.BELL_PENALTY_THRESHOLD

            if count <= sweet:
                return count / sweet
            elif count <= threshold:
                # 从 1.0 缓慢下降到 0.5
                return 1.0 - 0.5 * (count - sweet) / (threshold - sweet)
            else:
                # 超过阈值快速下降
                excess = count - threshold
                return max(0.0, 0.5 - excess * 0.1)

        return min(1.0, count / 10)  # fallback

    def rank_by_quality(self, memories: list[dict], blend_relevance: bool = True) -> list[dict]:
        """
        按质量+相关性综合排序检索结果。

        如果已有 _rank_score（来自 recall 引擎），则按 40% 质量 + 60% 相关性混合排序，
        避免质量分覆盖语义搜索的排序结果。
        """
        for mem in memories:
            q = self.compute_quality(mem)
            mem["_quality_score"] = q["quality_score"]
            mem["_quality_grade"] = q["grade"]

        if blend_relevance:
            # 混合排序：保留相关性信号，用质量分做微调
            memories.sort(
                key=lambda m: (
                    0.6 * m.get("_rank_score", 0.5)
                    + 0.4 * m.get("_quality_score", 0.3)
                ),
                reverse=True,
            )
        else:
            memories.sort(key=lambda m: m.get("_quality_score", 0), reverse=True)
        return memories

    def get_low_quality_memories(self, threshold: float = 0.2, limit: int = 50) -> list[dict]:
        """找出低质量记忆（可考虑清理）"""
        all_memories = self.store.query(limit=200)
        low_quality = []
        for mem in all_memories:
            q = self.compute_quality(mem)
            if q["quality_score"] < threshold:
                low_quality.append({**mem, "_quality": q})
        low_quality.sort(key=lambda m: m["_quality"]["quality_score"])
        return low_quality[:limit]

    def get_stats(self) -> dict:
        """质量系统统计"""
        total_feedback = len(self._stats["feedback"])
        useful_count = sum(1 for f in self._stats["feedback"].values() if f.get("useful"))
        total_retrievals = sum(self._stats["retrievals"].values())

        return {
            "total_feedback": total_feedback,
            "useful_ratio": useful_count / total_feedback if total_feedback else 0,
            "total_retrieval_events": total_retrievals,
            "unique_retrieved": len(self._stats["retrievals"]),
            "unique_referenced": len(self._stats["references"]),
        }

    def generate_quality_report(self) -> str:
        """生成质量分析报告"""
        stats = self.get_stats()
        all_memories = self.store.query(limit=200)

        # 计算所有记忆的质量
        quality_dist = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}
        for mem in all_memories:
            q = self.compute_quality(mem)
            quality_dist[q["grade"]] = quality_dist.get(q["grade"], 0) + 1

        lines = [
            "# 📊 记忆质量报告",
            "",
            f"**总记忆数**: {len(all_memories)}",
            f"**总反馈数**: {stats['total_feedback']}",
            f"**有用率**: {stats['useful_ratio']:.0%}",
            f"**总检索事件**: {stats['total_retrieval_events']}",
            "",
            "## 质量分布",
            "",
        ]

        grade_icons = {"A": "🏆", "B": "✅", "C": "📝", "D": "⚠️", "F": "🗑️"}
        for grade in ["A", "B", "C", "D", "F"]:
            count = quality_dist.get(grade, 0)
            if count:
                icon = grade_icons[grade]
                bar = "█" * min(count, 20)
                lines.append(f"- {icon} **{grade}**: {count} {bar}")

        return "\n".join(lines)

    # ── 记忆效用追踪（新功能）────────────────────────────

    def record_recommendation(self, memory_ids: list[str], query: str = None):
        """
        记录一批记忆被推荐给用户。

        在 recall() 返回结果后调用，标记这些记忆为"已推荐"状态。
        后续如果用户对话中引用了这些记忆，自动标记为"有用"。

        参数:
            memory_ids: 被推荐的记忆 ID 列表
            query: 原始查询（用于后续匹配）
        """
        now = int(time.time())
        utility = self._stats.get("utility", {})

        for mid in memory_ids:
            if mid not in utility:
                utility[mid] = {"recommended": 0, "used": 0, "ignored": 0}
            utility[mid]["recommended"] = utility[mid].get("recommended", 0) + 1

        # 记录最近推荐批次（最多保留 50 批）
        if "recent_recommendations" not in self._stats:
            self._stats["recent_recommendations"] = []

        self._stats["recent_recommendations"].append({
            "memory_ids": memory_ids,
            "query": query,
            "timestamp": now,
        })
        # 只保留最近 50 批
        self._stats["recent_recommendations"] = self._stats["recent_recommendations"][-50:]

        self._stats["utility"] = utility
        self._save_stats()

    def check_usage_signal(self, content: str, window_seconds: int = 300) -> list[str]:
        """
        检查用户后续对话内容是否引用了最近推荐的记忆。

        在用户发送新消息后调用，检查消息内容是否与最近推荐的记忆相关。
        如果相关，自动标记该记忆为"有用"。

        参数:
            content: 用户的新消息内容
            window_seconds: 检查时间窗口（秒），只看最近推荐的记忆

        返回: 被标记为"已使用"的记忆 ID 列表
        """
        now = int(time.time())
        recent = self._stats.get("recent_recommendations", [])
        if not recent:
            return []

        used_ids = []
        content_lower = content.lower()

        for batch in recent:
            # 超过时间窗口的跳过
            if now - batch.get("timestamp", 0) > window_seconds:
                continue

            query = batch.get("query", "")
            for mid in batch.get("memory_ids", []):
                # 简单匹配：用户消息包含查询关键词或记忆内容片段
                if query and query.lower() in content_lower:
                    self._mark_as_used(mid)
                    used_ids.append(mid)
                    continue

                # 获取记忆内容做模糊匹配
                mem = self.store.get_memory(mid)
                if mem:
                    mem_content = mem.get("content", "")
                    # 提取关键词（>4字的连续词）
                    keywords = [w for w in mem_content.split() if len(w) >= 4]
                    match_count = sum(1 for kw in keywords[:5] if kw in content)
                    if match_count >= 2:
                        self._mark_as_used(mid)
                        used_ids.append(mid)

        return used_ids

    def _mark_as_used(self, memory_id: str):
        """标记一条记忆为"已使用"（隐式正反馈）"""
        utility = self._stats.get("utility", {})
        if memory_id not in utility:
            utility[memory_id] = {"recommended": 0, "used": 0, "ignored": 0}
        utility[memory_id]["used"] = utility[memory_id].get("used", 0) + 1
        self._stats["utility"] = utility
        self._save_stats()

    def record_manual_update(self, memory_id: str, field: str, old_value: str, new_value: str):
        """
        记录记忆的手动更新（用于流式记忆更新追踪）。

        当记忆内容被版本化更新时，记录更新历史。
        这个信号用于质量评分：频繁被更新的记忆说明是"活的"知识。

        参数:
            memory_id: 记忆 ID
            field: 更新的字段（如 "content", "importance"）
            old_value: 旧值
            new_value: 新值
        """
        if "update_history" not in self._stats:
            self._stats["update_history"] = {}

        if memory_id not in self._stats["update_history"]:
            self._stats["update_history"][memory_id] = []

        self._stats["update_history"][memory_id].append({
            "field": field,
            "old": old_value[:200] if old_value else "",
            "new": new_value[:200] if new_value else "",
            "timestamp": int(time.time()),
        })
        self._save_stats()

    def get_utility_stats(self, memory_id: str = None) -> dict:
        """获取记忆效用统计"""
        utility = self._stats.get("utility", {})

        if memory_id:
            return utility.get(memory_id, {"recommended": 0, "used": 0, "ignored": 0})

        # 全局统计
        total_recommended = sum(u.get("recommended", 0) for u in utility.values())
        total_used = sum(u.get("used", 0) for u in utility.values())
        useful_memories = sum(1 for u in utility.values() if u.get("used", 0) > 0)

        return {
            "total_recommended": total_recommended,
            "total_used": total_used,
            "useful_ratio": total_used / total_recommended if total_recommended > 0 else 0,
            "useful_memory_count": useful_memories,
            "tracked_memory_count": len(utility),
        }
