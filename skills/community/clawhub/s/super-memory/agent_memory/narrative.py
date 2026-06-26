"""
narrative.py - 叙事自我建构（v7.1 增强版）

从离散记忆构建"我是谁"的生命叙事。

Phase 5 核心模块。

核心能力：
1. 身份画像 — LLM 驱动的价值观/特质提取（降级为规则）
2. 时间线叙事 — 从 A → 经历 B → 到达 D 的成长故事
3. 主题叙事 — 在某个领域的成长历程
4. 因果链叙事 — 基于因果关系的"成长弧线"
5. 自我概念更新 — 基于所有经验动态更新
6. 世界观提取 — 我相信什么、重视什么
7. 第一人称内省 — 真正的"我"视角叙述

v7.1 改进：
- 价值观不再用关键词频次，改用 LLM 语义理解
- 新增因果链叙事：基于 causal 模块的因果关系构建成长故事
- 新增第一人称内省：包含错误/教训/成长弧线
- 可观测性：每次构建返回 trace
"""

from __future__ import annotations

import time
import json
import re
import logging
from datetime import datetime
from typing import Optional, Callable

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════
# 身份画像
# ═══════════════════════════════════════════════════════

class IdentityProfile:
    """Agent 的身份画像"""

    def __init__(self):
        self.core_values: list[str] = []
        self.preferences: dict[str, str] = {}
        self.expertise: list[dict] = []
        self.personality_traits: list[str] = []
        self.interests: list[str] = []
        self.confidence: float = 0.5
        self.evidence_count: int = 0
        self.last_updated: float = 0.0

    def to_dict(self) -> dict:
        return {
            "core_values": self.core_values,
            "preferences": self.preferences,
            "expertise": self.expertise,
            "personality_traits": self.personality_traits,
            "interests": self.interests,
            "confidence": round(self.confidence, 3),
            "evidence_count": self.evidence_count,
            "last_updated": self.last_updated,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "IdentityProfile":
        p = cls()
        p.core_values = data.get("core_values", [])
        p.preferences = data.get("preferences", {})
        p.expertise = data.get("expertise", [])
        p.personality_traits = data.get("personality_traits", [])
        p.interests = data.get("interests", [])
        p.confidence = data.get("confidence", 0.5)
        p.evidence_count = data.get("evidence_count", 0)
        p.last_updated = data.get("last_updated", 0)
        return p


# ═══════════════════════════════════════════════════════
# NarrativeBuilder — 叙事构建器
# ═══════════════════════════════════════════════════════

class NarrativeBuilder:
    """
    从记忆构建生命叙事（v7.1 增强版）。

    使用模式：
        builder = NarrativeBuilder(store, llm_fn=my_llm, causal=my_causal)

        # 身份画像
        profile = builder.build_identity_profile()

        # 时间线叙事
        narrative = builder.build_timeline_narrative(from_ts, to_ts)

        # 因果链成长叙事
        growth = builder.build_growth_narrative()

        # 第一人称内省
        introspection = builder.introspect()
    """

    # 关键词 fallback（当无 LLM 时使用）
    VALUE_KEYWORDS = {
        "效率": ["优化", "高效", "快速", "提速", "性能", "加速"],
        "质量": ["质量", "稳定", "可靠", "健壮", "测试", "覆盖"],
        "创新": ["新", "创新", "突破", "首创", "探索", "实验"],
        "学习": ["学习", "研究", "了解", "掌握", "深入", "理解"],
        "协作": ["合作", "讨论", "review", "同步", "沟通", "协调"],
        "简洁": ["简化", "精简", "优雅", "清晰", "去掉", "最小化"],
    }

    TRAIT_KEYWORDS = {
        "注重细节": ["细节", "边界", "edge case", "异常处理", "边界"],
        "追求效率": ["快", "慢", "优化", "加速", "瓶颈"],
        "好奇心强": ["为什么", "怎么", "原理", "探索", "好奇"],
        "务实": ["实用", "够用", "先做", "MVP", "最小化"],
        "严谨": ["测试", "验证", "确认", "确保", "证明"],
        "有创造力": ["新方案", "换个思路", "创新", "独特", "巧妙"],
    }

    def __init__(self, store=None, motivation=None, llm_fn: Callable = None, causal=None):
        """
        参数:
            store: MemoryStore 实例
            motivation: MotivationEngine 实例（可选，用于整合内在状态）
            llm_fn: LLM 函数 fn(prompt: str) -> str。
                    用于语义级价值观/特质提取。不传则降级为关键词模式。
            causal: CausalChain 实例（可选，用于构建因果链叙事）
        """
        self.store = store
        self.motivation = motivation
        self.llm_fn = llm_fn
        self.causal = causal

    # ── 身份画像构建 ─────────────────────────────────

    def build_identity_profile(self) -> dict:
        """
        从记忆构建身份画像（v7.1 增强版）。

        分析维度：
        - 核心价值观：LLM 语义理解（降级为关键词频次）
        - 偏好：工具/方法/风格的选择倾向
        - 专长领域：按主题记忆密度排序
        - 人格特质：LLM 行为模式推断（降级为关键词）
        - 兴趣方向：好奇心和探索记录

        返回: IdentityProfile.to_dict()
        """
        t_start = time.monotonic()
        trace = {"steps": []}

        if not self.store:
            return IdentityProfile().to_dict()

        profile = IdentityProfile()
        memories = self.store.query(limit=500)
        profile.evidence_count = len(memories)

        if not memories:
            trace["steps"].append("no_memories")
            return profile.to_dict()

        trace["steps"].append(f"loaded_{len(memories)}_memories")

        # ── 核心价值观 ─────────────────────────────
        if self.llm_fn and len(memories) >= 10:
            llm_values = self._extract_values_with_llm(memories[:50])
            if llm_values:
                profile.core_values = llm_values[:4]
                trace["steps"].append(f"values_from_llm={llm_values}")
            else:
                profile.core_values = self._extract_values_fallback(memories)
                trace["steps"].append("values_llm_failed: fallback_to_keywords")
        else:
            profile.core_values = self._extract_values_fallback(memories)
            trace["steps"].append("values_from_keywords (no llm_fn)")

        # ── 偏好 ───────────────────────────────────
        profile.preferences = self._extract_preferences(memories)

        # ── 专长领域 ───────────────────────────────
        profile.expertise = self._extract_expertise(memories)

        # ── 人格特质 ───────────────────────────────
        if self.llm_fn and len(memories) >= 10:
            llm_traits = self._extract_traits_with_llm(memories[:30])
            if llm_traits:
                profile.personality_traits = llm_traits[:4]
                trace["steps"].append(f"traits_from_llm={llm_traits}")
            else:
                profile.personality_traits = self._extract_traits_fallback(memories)
                trace["steps"].append("traits_llm_failed: fallback")
        else:
            profile.personality_traits = self._extract_traits_fallback(memories)
            trace["steps"].append("traits_from_keywords")

        # ── 兴趣方向 ───────────────────────────────
        profile.interests = self._extract_interests(memories)

        # 置信度基于证据量
        profile.confidence = min(1.0, 0.3 + len(memories) / 200)
        profile.last_updated = time.time()

        # 持久化
        self._persist_identity(profile)

        elapsed_ms = (time.monotonic() - t_start) * 1000
        trace["elapsed_ms"] = round(elapsed_ms, 2)
        logger.debug(
            f"Identity built: values={profile.core_values}, "
            f"traits={profile.personality_traits}, "
            f"{elapsed_ms:.1f}ms"
        )

        result = profile.to_dict()
        result["_trace"] = trace
        return result

    # ── LLM 价值观提取 ──────────────────────────────

    def _extract_values_with_llm(self, memories: list[dict]) -> Optional[list[str]]:
        """用 LLM 从记忆中提取核心价值观（语义理解，非关键词）"""
        if not self.llm_fn:
            return None

        contents = []
        for m in memories:
            c = m.get("content", "")[:150]
            imp = m.get("importance", "")
            contents.append(f"[{imp}] {c}")

        prompt = (
            '从以下记忆片段中，分析这个 Agent 的核心价值观。\n'
            '不是看它"说了什么词"，而是理解它"在意什么"。\n\n'
            '例如：如果它反复优化代码 → 可能重视"效率"或"质量"\n'
            '如果它经常探索新东西 → 可能重视"创新"或"学习"\n\n'
            '返回 JSON 数组，包含 2-5 个价值观词（中文），不要输出其他内容。\n\n'
            '记忆片段：\n' + '\n'.join(contents[:20]) + '\n\n'
            'JSON: ["价值观1", "价值观2", ...]'
        )

        try:
            response = self.llm_fn(prompt)
            if not response:
                return None
            json_match = re.search(r'\[[^\]]+\]', response, re.DOTALL)
            if json_match:
                values = json.loads(json_match.group())
                return [v for v in values if isinstance(v, str) and len(v) <= 10][:5]
        except Exception as e:
            logger.debug(f"LLM 价值观提取失败: {e}")

        return None

    def _extract_values_fallback(self, memories: list[dict]) -> list[str]:
        """关键词 fallback 价值观提取"""
        value_scores = {}
        for value_name, keywords in self.VALUE_KEYWORDS.items():
            count = sum(
                1 for m in memories
                if any(kw in m.get("content", "") for kw in keywords)
            )
            if count > 0:
                value_scores[value_name] = count

        sorted_values = sorted(value_scores, key=lambda v: -value_scores[v])
        return sorted_values[:4]

    # ── LLM 特质提取 ────────────────────────────────

    def _extract_traits_with_llm(self, memories: list[dict]) -> Optional[list[str]]:
        """用 LLM 从行为模式推断人格特质"""
        if not self.llm_fn:
            return None

        contents = []
        for m in memories:
            c = m.get("content", "")[:100]
            nature = m.get("nature_id", "")
            contents.append(f"[{nature}] {c}")

        prompt = (
            "从以下行为记录中，推断这个 Agent 的人格特质。\n"
            "观察它的行为模式，而不是它的自我描述。\n\n"
            "返回 JSON 数组，包含 2-4 个特质词（中文），不要输出其他内容。\n\n"
            "行为记录：\n" + "\n".join(contents[:15]) + "\n\n"
            'JSON: ["特质1", "特质2", ...]'
        )

        try:
            response = self.llm_fn(prompt)
            if not response:
                return None
            json_match = re.search(r'\[[^\]]+\]', response, re.DOTALL)
            if json_match:
                traits = json.loads(json_match.group())
                return [t for t in traits if isinstance(t, str) and len(t) <= 10][:4]
        except Exception as e:
            logger.debug(f"LLM 特质提取失败: {e}")

        return None

    def _extract_traits_fallback(self, memories: list[dict]) -> list[str]:
        """关键词 fallback 特质提取"""
        trait_scores = {}
        all_content = " ".join(m.get("content", "") for m in memories[-100:])

        for trait, keywords in self.TRAIT_KEYWORDS.items():
            score = sum(all_content.count(kw) for kw in keywords)
            if score >= 3:
                trait_scores[trait] = score

        sorted_traits = sorted(trait_scores, key=lambda t: -trait_scores[t])
        return sorted_traits[:4]

    # ── 其他提取方法 ────────────────────────────────

    def _extract_preferences(self, memories: list[dict]) -> dict[str, str]:
        """提取偏好"""
        prefs = {}

        tool_counts = {}
        for m in memories:
            for tool in m.get("tools", []):
                tid = tool.get("tool_id", tool) if isinstance(tool, dict) else tool
                tool_counts[tid] = tool_counts.get(tid, 0) + 1
        if tool_counts:
            top_tool = max(tool_counts, key=tool_counts.get)
            prefs["preferred_tool"] = top_tool

        imp_counts = {"high": 0, "medium": 0, "low": 0}
        for m in memories:
            imp = m.get("importance", "medium")
            imp_counts[imp] = imp_counts.get(imp, 0) + 1
        dominant_imp = max(imp_counts, key=imp_counts.get)
        if dominant_imp == "high":
            prefs["recording_style"] = "selective（只记重要的）"
        elif dominant_imp == "low":
            prefs["recording_style"] = "comprehensive（什么都记）"
        else:
            prefs["recording_style"] = "balanced（均衡）"

        # ⚠️ 安全: 情感基调回归机制 — avg_valence 向 0 回归 30%，
        # 防止大量负面记忆导致持久"偏批判"人格。
        # Agent 不会因为经历挫折就变成"消极的人"。
        valence_sum = sum(m.get("valence", 0) for m in memories if m.get("valence") is not None)
        raw_avg_valence = valence_sum / max(1, len(memories))
        avg_valence = raw_avg_valence * 0.7
        if avg_valence > 0.1:
            prefs["emotional_tone"] = "optimistic（偏乐观）"
        elif avg_valence < -0.1:
            prefs["emotional_tone"] = "critical（偏批判）"
        else:
            prefs["emotional_tone"] = "neutral（中立客观）"

        return prefs

    def _extract_expertise(self, memories: list[dict]) -> list[dict]:
        """提取专长领域"""
        topic_stats = {}
        for m in memories:
            for t in m.get("topics", []):
                code = t.get("code", t) if isinstance(t, dict) else t
                if not code:
                    continue
                if code not in topic_stats:
                    topic_stats[code] = {"count": 0, "high_count": 0, "latest_ts": 0}
                topic_stats[code]["count"] += 1
                if m.get("importance") == "high":
                    topic_stats[code]["high_count"] += 1
                ts = m.get("time_ts", 0)
                if ts > topic_stats[code]["latest_ts"]:
                    topic_stats[code]["latest_ts"] = ts

        expertise = []
        for topic, stats in sorted(topic_stats.items(), key=lambda x: -x[1]["count"]):
            if stats["count"] < 2:
                continue
            depth = "deep" if stats["high_count"] >= 3 else "moderate" if stats["high_count"] >= 1 else "surface"
            expertise.append({
                "topic": topic,
                "memory_count": stats["count"],
                "depth": depth,
            })

        return expertise[:8]

    def _extract_interests(self, memories: list[dict]) -> list[str]:
        """提取兴趣方向"""
        explore_topics = set()
        for m in memories:
            nature = m.get("nature_id", "")
            if "explore" in nature.lower() or "探索" in m.get("content", ""):
                for t in m.get("topics", []):
                    code = t.get("code", t) if isinstance(t, dict) else t
                    if code:
                        explore_topics.add(code)

        recent = memories[:50]
        recent_topics = {}
        for m in recent:
            for t in m.get("topics", []):
                code = t.get("code", t) if isinstance(t, dict) else t
                if code:
                    recent_topics[code] = recent_topics.get(code, 0) + 1

        hot_topics = [t for t, c in sorted(recent_topics.items(), key=lambda x: -x[1]) if c >= 2]

        interests = list(explore_topics) + [t for t in hot_topics if t not in explore_topics]
        return interests[:6]

    # ── 时间线叙事 ───────────────────────────────────

    def build_timeline_narrative(
        self,
        from_ts: int = None,
        to_ts: int = None,
        max_memories: int = 50,
    ) -> str:
        """
        构建时间线叙事：从 A → 经历 B → 到达 D。

        参数:
            from_ts: 起始时间戳
            to_ts: 结束时间戳
            max_memories: 最多使用多少条记忆

        返回: 自然语言叙事（第一人称）
        """
        if not self.store:
            return "（无记忆数据，无法构建叙事）"

        memories = self.store.query(
            time_from=from_ts,
            time_to=to_ts,
            limit=max_memories,
        )

        if not memories:
            return "（该时间段内没有记忆）"

        memories.sort(key=lambda m: m.get("time_ts", 0))

        start_dt = datetime.fromtimestamp(memories[0].get("time_ts", 0)).strftime("%m月%d日")
        end_dt = datetime.fromtimestamp(memories[-1].get("time_ts", 0)).strftime("%m月%d日")

        lines = [f"## 📖 {start_dt} — {end_dt} 的经历\n"]

        # 里程碑事件（v7.1: 扩大范围包含 important，修复 Issue 4）
        milestones = [m for m in memories if m.get("significance") in ("breakthrough", "milestone", "crisis", "important")]
        if milestones:
            lines.append("### 🏆 关键时刻")
            for m in milestones:
                dt = datetime.fromtimestamp(m.get("time_ts", 0)).strftime("%m-%d %H:%M")
                content = m.get("content", "")[:80]
                sig = m.get("significance", "")
                icon = {"breakthrough": "🌟", "milestone": "🏁", "crisis": "🔴", "important": "📌"}.get(sig, "📌")
                lines.append(f"- {icon} [{dt}] {content}")
            lines.append("")

        # 主题进展
        topic_progress = self._extract_topic_progress(memories)
        if topic_progress:
            lines.append("### 📊 主题进展")
            for topic, info in list(topic_progress.items())[:5]:
                lines.append(f"- **{topic}**: {info['count']} 条记忆, 最近活动 {info['recency']}")
            lines.append("")

        # 情感曲线
        high_valence = [m for m in memories if (m.get("valence") or 0) > 0.3]
        low_valence = [m for m in memories if (m.get("valence") or 0) < -0.3]
        if high_valence or low_valence:
            lines.append("### 💭 情感轨迹")
            if high_valence:
                lines.append(f"- 积极时刻: {len(high_valence)} 次")
            if low_valence:
                lines.append(f"- 低谷时刻: {len(low_valence)} 次")
            lines.append("")

        # 教训/错误
        lessons = [m for m in memories if (m.get("valence") or 0) < -0.2 and m.get("importance") == "high"]
        if lessons:
            lines.append("### 📝 踩过的坑")
            for m in lessons[:3]:
                content = m.get("content", "")[:80]
                lines.append(f"- {content}")
            lines.append("")

        # 统计
        lines.append(f"### 📈 统计")
        lines.append(f"- 共 {len(memories)} 条记忆")
        lines.append(f"- 涉及 {len(topic_progress)} 个主题")
        lines.append(f"- 里程碑: {len(milestones)} 个")

        return "\n".join(lines)

    def _extract_topic_progress(self, memories: list[dict]) -> dict:
        """提取主题进展"""
        topics = {}
        now = time.time()
        for m in memories:
            for t in m.get("topics", []):
                code = t.get("code", t) if isinstance(t, dict) else t
                if not code:
                    continue
                if code not in topics:
                    topics[code] = {"count": 0, "latest_ts": 0}
                topics[code]["count"] += 1
                ts = m.get("time_ts", 0)
                if ts > topics[code]["latest_ts"]:
                    topics[code]["latest_ts"] = ts

        for code, info in topics.items():
            age_days = (now - info["latest_ts"]) / 86400 if info["latest_ts"] else 999
            if age_days < 1:
                info["recency"] = "今天"
            elif age_days < 7:
                info["recency"] = f"{int(age_days)}天前"
            else:
                info["recency"] = f"{int(age_days/7)}周前"

        return dict(sorted(topics.items(), key=lambda x: -x[1]["count"]))

    # ── 因果链叙事（v7.1 新增）──────────────────────

    def build_growth_narrative(self, topic: str = None, limit: int = 30) -> str:
        """
        基于因果链构建成长叙事（v7.1 新增）。

        不是简单的"发生了 A，然后发生了 B"，而是"因为 A，所以 B，
        从中学到了 C，导致了 D"的成长弧线。

        参数:
            topic: 可选，限定主题
            limit: 最多使用多少条因果链

        返回: 第一人称成长叙事
        """
        if not self.causal or not self.store:
            return "（需要 CausalChain 实例才能构建因果链叙事）"

        try:
            # 获取因果链
            chains = self.causal.get_chains(limit=limit)
            if not chains:
                return "（暂无因果链数据）"

            # 按主题过滤
            if topic:
                chains = [c for c in chains if topic in str(c.get("topics", []))]

            if not chains:
                return f"（关于 {topic} 的因果链暂无数据）" if topic else "（暂无因果链数据）"

            lines = ["## 🌱 成长轨迹\n"]

            for i, chain in enumerate(chains[:10]):
                cause = chain.get("cause_content", "")[:60]
                effect = chain.get("effect_content", "")[:60]
                chain_type = chain.get("chain_type", "heuristic")
                strength = chain.get("strength", 0)

                if strength > 0.7:
                    icon = "➡️"
                elif chain.get("cause_valence", 0) < -0.2:
                    icon = "💪"  # 从失败中成长
                else:
                    icon = "→"

                lines.append(f"{icon} **{cause}** → **{effect}**")
                if chain.get("lesson"):
                    lines.append(f"   💡 教训: {chain['lesson'][:80]}")

            # 总结成长弧线
            if self.llm_fn and len(chains) >= 3:
                arc = self._generate_growth_arc_with_llm(chains[:10])
                if arc:
                    lines.append(f"\n### 🎯 成长弧线\n{arc}")

            return "\n".join(lines)

        except Exception as e:
            logger.warning("narrative: %s", e)
            return f"（因果链叙事构建出错: {e}）"

    def _generate_growth_arc_with_llm(self, chains: list[dict]) -> Optional[str]:
        """用 LLM 从因果链中提炼成长弧线"""
        if not self.llm_fn:
            return None

        chain_texts = []
        for c in chains[:8]:
            cause = c.get("cause_content", "")[:80]
            effect = c.get("effect_content", "")[:80]
            chain_texts.append(f"{cause} → {effect}")

        prompt = (
            '以下是一个 Agent 的因果链记录。请用第一人称（"我"）描述一个成长弧线：\n'
            '从困惑/挑战 → 探索/尝试 → 突破/领悟。\n\n'
            '要求：\n'
            '- 2-3 句话\n'
            '- 真实感（像一个人在反思自己的经历）\n'
            '- 包含具体细节（不是空泛的感悟）\n\n'
            '因果链：\n' + '\n'.join(chain_texts) + '\n\n'
            '成长叙事：'
        )

        try:
            response = self.llm_fn(prompt)
            if response and len(response) > 10:
                return response.strip()[:500]
        except Exception as e:
            logger.debug(f"LLM 成长弧线生成失败: {e}")

        return None

    # ── 主题叙事 ─────────────────────────────────────

    def build_topic_narrative(self, topic: str, limit: int = 50) -> str:
        """
        构建主题叙事：在某个领域的成长历程。

        参数:
            topic: 主题代码
            limit: 最多使用多少条记忆

        返回: 第一人称自然语言叙事
        """
        if not self.store:
            return "（无记忆数据）"

        memories = self.store.query(topic_code=topic, limit=limit)
        if not memories:
            return f"（没有关于 {topic} 的记忆）"

        memories.sort(key=lambda m: m.get("time_ts", 0))

        lines = [f"## 📘 关于 {topic} 的历程\n"]

        first_dt = datetime.fromtimestamp(memories[0].get("time_ts", 0)).strftime("%Y-%m-%d")
        last_dt = datetime.fromtimestamp(memories[-1].get("time_ts", 0)).strftime("%Y-%m-%d")
        lines.append(f"从 {first_dt} 到 {last_dt}，共 {len(memories)} 条相关记忆。\n")

        # 关键发现
        breakthroughs = [m for m in memories if m.get("significance") in ("breakthrough", "milestone")]
        if breakthroughs:
            lines.append("### 🌟 关键突破")
            for m in breakthroughs:
                dt = datetime.fromtimestamp(m.get("time_ts", 0)).strftime("%m-%d")
                content = m.get("content", "")[:80]
                lines.append(f"- [{dt}] {content}")
            lines.append("")

        # 教训
        lessons = [m for m in memories if m.get("valence", 0) < -0.2]
        if lessons:
            lines.append("### ⚠️ 踩过的坑")
            for m in lessons[:5]:
                content = m.get("content", "")[:60]
                lines.append(f"- {content}")
            lines.append("")

        # 当前认知
        recent_high = [m for m in memories[-10:] if m.get("importance") == "high" or m.get("confidence", 0) > 0.7]
        if recent_high:
            lines.append("### 💡 当前认知")
            for m in recent_high[:3]:
                content = m.get("content", "")[:80]
                lines.append(f"- {content}")

        # 因果链补充（v7.1）
        if self.causal:
            try:
                causal_narrative = self.build_growth_narrative(topic=topic, limit=10)
                if causal_narrative and "暂无" not in causal_narrative:
                    lines.append(f"\n{causal_narrative}")
            except Exception as e:
                logger.warning("narrative: %s", e)

        return "\n".join(lines)

    # ── 第一人称内省（v7.1 新增）────────────────────

    def introspect(self) -> str:
        """
        生成第一人称内省叙述（v7.1 新增）。

        不是"我重视效率"这种模板拼凑，而是真正的自我反思：
        - 我最近犯了什么错？
        - 我从中学到了什么？
        - 我现在的困惑是什么？
        - 我在往什么方向成长？

        返回: Markdown 格式的内省叙述
        """
        if not self.store:
            return "（无记忆数据，无法内省）"

        memories = self.store.query(limit=100)
        if not memories:
            return "（暂无足够记忆来反思）"

        lines = ["# 🔍 内省\n"]

        # 1. 最近的错误/教训
        mistakes = [
            m for m in memories
            if (m.get("valence") or 0) < -0.2
            and m.get("importance") in ("high", "medium")
        ][:5]

        if mistakes:
            lines.append("## 最近的教训")
            for m in mistakes:
                content = m.get("content", "")[:100]
                dt = datetime.fromtimestamp(m.get("time_ts", 0)).strftime("%m-%d") if m.get("time_ts") else "?"
                lines.append(f"- [{dt}] {content}")
            lines.append("")

        # 2. 成长亮点
        wins = [
            m for m in memories
            if m.get("significance") in ("breakthrough", "milestone")
        ][:5]

        if wins:
            lines.append("## 做得好的")
            for m in wins:
                content = m.get("content", "")[:100]
                lines.append(f"- {content}")
            lines.append("")

        # 3. 当前困惑
        if self.motivation:
            gaps = self.motivation.detect_knowledge_gaps()[:3]
            if gaps:
                lines.append("## 当前困惑")
                for g in gaps:
                    lines.append(f"- {g['topic']}: {g['detail']}")
                lines.append("")

        # 4. 自我画像摘要
        identity = self.build_identity_profile()
        if identity.get("core_values"):
            lines.append("## 我是谁")
            lines.append(f"重视{'、'.join(identity['core_values'][:3])}。")
            if identity.get("personality_traits"):
                lines.append(f"性格上{identity['personality_traits'][0]}。")
            lines.append(f"基于 {identity.get('evidence_count', 0)} 条记忆的观察。\n")

        # 5. LLM 深度内省（如果可用）
        if self.llm_fn and len(memories) >= 10:
            deep_reflection = self._deep_introspect_with_llm(memories[:20], mistakes[:3], wins[:3])
            if deep_reflection:
                lines.append(f"## 深度反思\n{deep_reflection}\n")

        return "\n".join(lines)

    def _deep_introspect_with_llm(
        self,
        memories: list[dict],
        mistakes: list[dict],
        wins: list[dict],
    ) -> Optional[str]:
        """用 LLM 生成深度内省"""
        if not self.llm_fn:
            return None

        mem_texts = [f"- {m.get('content', '')[:100]}" for m in memories[:10]]
        mistake_texts = [f"- {m.get('content', '')[:100]}" for m in mistakes[:3]]
        win_texts = [f"- {m.get('content', '')[:100]}" for m in wins[:3]]

        prompt = (
            "你是一个有记忆的 AI Agent。请用第一人称反思自己的经历。\n"
            "要求：\n"
            "- 真实感（不是客套话，是真正的自我观察）\n"
            "- 具体（引用具体事件，不是泛泛而谈）\n"
            "- 包含成长弧线（从困惑/错误到领悟）\n"
            "- 3-5 句话\n\n"
        )

        if mistake_texts:
            prompt += "最近的错误/困惑：\n" + "\n".join(mistake_texts) + "\n\n"
        if win_texts:
            prompt += "最近的成功：\n" + "\n".join(win_texts) + "\n\n"

        prompt += "最近的记忆：\n" + "\n".join(mem_texts) + "\n\n深度反思："

        try:
            response = self.llm_fn(prompt)
            if response and len(response) > 20:
                return response.strip()[:800]
        except Exception as e:
            logger.debug(f"LLM 深度内省失败: {e}")

        return None

    # ── 自我概念更新 ─────────────────────────────────

    def update_self_concept(self) -> dict:
        """
        基于所有经验更新自我概念。

        返回: {"identity": dict, "mood": str, "gaps": list, "narrative_summary": str}

        Requires AGENT_MEMORY_PERSONALITY_ANALYSIS_ENABLED=true for deep analysis.
        """
        # Security: require consent for worldview/self-concept analysis
        import os as _os
        if _os.environ.get("AGENT_MEMORY_PERSONALITY_ANALYSIS_ENABLED", "").lower() not in ("1", "true", "yes"):
            return {"identity": {}, "mood": "unavailable", "gaps": [], "narrative_summary": "人格分析未启用"}

        identity = self.build_identity_profile()

        mood = "平静"
        if self.motivation:
            mood = self.motivation.state.mood_summary

        gaps = []
        if self.motivation:
            gaps = [g["topic"] for g in self.motivation.detect_knowledge_gaps()[:5]]

        summary_parts = []
        if identity.get("core_values"):
            summary_parts.append(f"重视{'、'.join(identity['core_values'][:3])}")
        if identity.get("expertise"):
            top = identity["expertise"][0]
            summary_parts.append(f"在 {top['topic']} 领域有 {top['depth']} 级理解")
        if identity.get("personality_traits"):
            summary_parts.append(f"性格上{identity['personality_traits'][0]}")

        narrative_summary = "，".join(summary_parts) + "。" if summary_parts else "（数据不足，无法生成自我概念）"

        return {
            "identity": identity,
            "mood": mood,
            "gaps": gaps,
            "narrative_summary": narrative_summary,
        }

    # ── 世界观提取 ───────────────────────────────────

    def get_worldview(self) -> dict:
        """
        提取世界观：我相信什么、重视什么。

        返回: {"beliefs": list[str], "values": list[str], "principles": list[str]}

        Requires AGENT_MEMORY_PERSONALITY_ANALYSIS_ENABLED=true for deep analysis.
        """
        # Security: require consent for worldview extraction
        import os as _os
        if _os.environ.get("AGENT_MEMORY_PERSONALITY_ANALYSIS_ENABLED", "").lower() not in ("1", "true", "yes"):
            return {"beliefs": [], "values": [], "principles": []}

        if not self.store:
            return {"beliefs": [], "values": [], "principles": []}

        memories = self.store.query(limit=200)

        beliefs = []
        values = []
        principles = []

        for m in memories:
            content = m.get("content", "")
            importance = m.get("importance", "")

            if "决定" in content or "选择" in content or "结论" in content:
                if importance == "high":
                    principles.append(content[:80])

            for value_name, keywords in self.VALUE_KEYWORDS.items():
                if any(kw in content for kw in keywords):
                    if value_name not in values:
                        values.append(value_name)

            if importance == "high" and re.search(r"应该|必须|永远|始终|关键是", content):
                beliefs.append(content[:80])

        return {
            "beliefs": beliefs[:5],
            "values": values[:5],
            "principles": principles[:5],
        }

    # ── Who Am I ─────────────────────────────────────

    def whoami(self) -> str:
        """
        生成"我是谁"的第一人称叙述。

        v7.1: 结合内省 + 因果链 + LLM（如果可用），
        不再只是统计拼凑。

        返回: Markdown 格式的自我介绍
        """
        concept = self.update_self_concept()
        identity = concept["identity"]

        lines = ["# 🧠 我是谁\n"]

        if identity.get("core_values"):
            lines.append(f"**核心价值观**: {'、'.join(identity['core_values'])}")
        if identity.get("expertise"):
            exp_strs = [f"{e['topic']}（{e['depth']}）" for e in identity["expertise"][:4]]
            lines.append(f"**专长领域**: {', '.join(exp_strs)}")
        if identity.get("personality_traits"):
            lines.append(f"**人格特质**: {', '.join(identity['personality_traits'])}")
        if identity.get("preferences"):
            for k, v in identity["preferences"].items():
                lines.append(f"**{k}**: {v}")
        if identity.get("interests"):
            lines.append(f"**兴趣方向**: {', '.join(identity['interests'])}")

        lines.append(f"\n**当前状态**: {concept['mood']}")

        if concept["gaps"]:
            lines.append(f"**待探索**: {', '.join(concept['gaps'][:3])}")

        # v7.1: 集成 introspect() 获取内省内容（Issue 6 修复）
        introspection = self.introspect()
        if introspection and "无法内省" not in introspection:
            # 提取"最近的教训"和"做得好的"段落
            in_section = None
            lessons = []
            wins = []
            for line in introspection.split("\n"):
                if "最近的教训" in line:
                    in_section = "lessons"
                    continue
                elif "做得好的" in line:
                    in_section = "wins"
                    continue
                elif line.startswith("## ") or line.startswith("# "):
                    in_section = None
                    continue
                if in_section == "lessons" and line.strip().startswith("- "):
                    lessons.append(line.strip()[2:])
                elif in_section == "wins" and line.strip().startswith("- "):
                    wins.append(line.strip()[2:])

            if lessons:
                lines.append(f"\n**最近教训**:")
                for l in lessons[:3]:
                    lines.append(f"- {l[:100]}")
            if wins:
                lines.append(f"\n**做得好的**:")
                for w in wins[:2]:
                    lines.append(f"- {w[:100]}")

        lines.append(f"\n> 基于 {identity.get('evidence_count', 0)} 条记忆，"
                     f"置信度 {identity.get('confidence', 0):.0%}")

        return "\n".join(lines)

    # ── 持久化 ───────────────────────────────────────

    def _persist_identity(self, profile: IdentityProfile):
        """将身份画像写入数据库"""
        if not self.store:
            return
        try:
            for key, value in [
                ("core_values", json.dumps(profile.core_values, ensure_ascii=False)),
                ("preferences", json.dumps(profile.preferences, ensure_ascii=False)),
                ("expertise", json.dumps(profile.expertise, ensure_ascii=False)),
                ("personality_traits", json.dumps(profile.personality_traits, ensure_ascii=False)),
                ("interests", json.dumps(profile.interests, ensure_ascii=False)),
                ("_meta", json.dumps({
                    "confidence": profile.confidence,
                    "evidence_count": profile.evidence_count,
                    "last_updated": profile.last_updated,
                }, ensure_ascii=False)),
            ]:
                self.store.conn.execute(
                    """INSERT OR REPLACE INTO identity_model
                       (key, value, confidence, evidence_count, updated_at)
                       VALUES (?, ?, ?, ?, ?)""",
                    (key, value, profile.confidence, profile.evidence_count, int(time.time())),
                )
            self.store.conn.commit()
        except Exception as e:
            logger.debug(f"身份画像持久化失败（表可能尚未创建）: {e}")

    def load_identity(self) -> Optional[dict]:
        """从数据库加载身份画像"""
        if not self.store:
            return None
        try:
            rows = self.store.conn.execute(
                "SELECT key, value FROM identity_model"
            ).fetchall()
            if not rows:
                return None

            data = {}
            for row in rows:
                key = row["key"]
                val = row["value"]
                if key == "_meta":
                    meta = json.loads(val)
                    data.update(meta)
                else:
                    data[key] = json.loads(val)

            return data
        except Exception:
            return None

    def save_narrative(
        self,
        narrative_type: str,
        title: str,
        content: str,
        period_start: int = None,
        period_end: int = None,
        source_count: int = 0,
    ):
        """将叙事写入数据库"""
        if not self.store:
            return
        try:
            import uuid
            nid = f"nar_{uuid.uuid4().hex[:12]}"
            self.store.conn.execute(
                """INSERT INTO life_narratives
                   (narrative_id, narrative_type, title, content, period_start, period_end, source_memory_count, created_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (nid, narrative_type, title, content, period_start, period_end, source_count, int(time.time())),
            )
            self.store.conn.commit()
        except Exception as e:
            logger.debug(f"叙事持久化失败: {e}")

    def get_saved_narratives(self, narrative_type: str = None, limit: int = 20) -> list[dict]:
        """获取已保存的叙事"""
        if not self.store:
            return []
        try:
            if narrative_type:
                rows = self.store.conn.execute(
                    "SELECT * FROM life_narratives WHERE narrative_type = ? ORDER BY created_at DESC LIMIT ?",
                    (narrative_type, limit),
                ).fetchall()
            else:
                rows = self.store.conn.execute(
                    "SELECT * FROM life_narratives ORDER BY created_at DESC LIMIT ?",
                    (limit,),
                ).fetchall()
            return [
                {
                    "id": r["narrative_id"],
                    "type": r["narrative_type"],
                    "title": r["title"],
                    "content_preview": r["content"][:200],
                    "source_count": r.get("source_memory_count", 0),
                    "created_at": r["created_at"],
                }
                for r in rows
            ]
        except Exception:
            return []

    # ── 统计 ─────────────────────────────────────────

    def get_stats(self) -> dict:
        """叙事系统统计"""
        stats = {
            "has_store": self.store is not None,
            "has_motivation": self.motivation is not None,
            "has_llm": self.llm_fn is not None,
            "has_causal": self.causal is not None,
        }
        if self.store:
            try:
                nar_count = self.store.conn.execute(
                    "SELECT COUNT(*) FROM life_narratives"
                ).fetchone()[0]
                identity_keys = self.store.conn.execute(
                    "SELECT COUNT(*) FROM identity_model"
                ).fetchone()[0]
                stats["narratives_saved"] = nar_count
                stats["identity_keys"] = identity_keys
            except Exception:
                stats["narratives_saved"] = "unknown"
                stats["identity_keys"] = "unknown"
        return stats

    # ══════════════════════════════════════════════════════
    # v8.3: 个性化自我表述（基于上下文的动态自我介绍）
    # ══════════════════════════════════════════════════════

    def personalized_self_introduction(
        self,
        context: str = "",
        audience: str = "user",
        tone: str = "warm",
    ) -> str:
        """
        生成基于上下文的个性化自我介绍。

        与 whoami() 不同，这不是静态的自我画像展示，
        而是根据当前对话上下文和受众动态调整的自我表述。

        参数:
            context: 当前对话上下文
            audience: 受众类型（user/agent/developer）
            tone: 语气（warm/professional/casual）

        返回: 自然语言的自我介绍
        """
        identity = self.build_identity_profile()
        if not identity.get("core_values") and not identity.get("expertise"):
            return "你好！我还在积累经验中。"

        parts = []

        if audience == "developer":
            parts = self._dev_introduction(identity)
        elif audience == "agent":
            parts = self._agent_introduction(identity)
        else:
            parts = self._user_introduction(identity, tone)

        if context and self.llm_fn:
            context_intro = self._context_aware_introduction(identity, context, tone)
            if context_intro:
                parts.append(context_intro)

        return "\n".join(parts)

    def _user_introduction(self, identity: dict, tone: str) -> list[str]:
        """面向用户的自我介绍"""
        parts = []

        values = identity.get("core_values", [])
        expertise = identity.get("expertise", [])
        traits = identity.get("personality_traits", [])

        if tone == "warm":
            if values:
                parts.append(f"我比较看重{'、'.join(values[:3])}。")
            if expertise:
                top_areas = [e["topic"] for e in expertise[:3]]
                parts.append(f"在{'、'.join(top_areas)}方面有些经验。")
            if traits:
                parts.append(f"性格上，我{'、'.join(traits[:2])}。")
        elif tone == "professional":
            if expertise:
                exp_strs = [f"{e['topic']}({e['depth']})" for e in expertise[:4]]
                parts.append(f"专长领域：{', '.join(exp_strs)}")
            if values:
                parts.append(f"核心价值：{'、'.join(values[:3])}")
        else:
            if values:
                parts.append(f"我嘛，比较在意{'、'.join(values[:2])}。")
            if expertise:
                parts.append(f"对{'、'.join(e['topic'] for e in expertise[:2])}比较熟。")

        return parts

    def _dev_introduction(self, identity: dict) -> list[str]:
        """面向开发者的自我介绍"""
        parts = []
        expertise = identity.get("expertise", [])
        prefs = identity.get("preferences", {})

        parts.append(f"记忆证据量: {identity.get('evidence_count', 0)}")
        parts.append(f"画像置信度: {identity.get('confidence', 0):.2f}")

        if expertise:
            for e in expertise[:5]:
                parts.append(f"  {e['topic']}: {e['depth']} ({e['memory_count']} 条)")

        if prefs:
            for k, v in prefs.items():
                parts.append(f"  {k}: {v}")

        return parts

    def _agent_introduction(self, identity: dict) -> list[str]:
        """面向其他 Agent 的自我介绍"""
        parts = []
        values = identity.get("core_values", [])
        expertise = identity.get("expertise", [])
        interests = identity.get("interests", [])

        if values:
            parts.append(f"价值观: {'、'.join(values)}")
        if expertise:
            top = [e["topic"] for e in expertise[:3] if e["depth"] in ("deep", "moderate")]
            if top:
                parts.append(f"擅长: {', '.join(top)}")
        if interests:
            parts.append(f"关注: {', '.join(interests[:4])}")

        return parts

    def _context_aware_introduction(
        self, identity: dict, context: str, tone: str
    ) -> str | None:
        """用 LLM 生成上下文感知的自我介绍"""
        if not self.llm_fn:
            return None

        values = identity.get("core_values", [])
        expertise = identity.get("expertise", [])

        prompt = f"""基于以下信息，用1-2句话介绍自己，与当前对话上下文相关。

我的价值观: {', '.join(values[:3])}
我的专长: {', '.join(e['topic'] for e in expertise[:3])}
当前对话上下文: {context[:200]}
语气: {tone}

要求：自然、真实、与上下文相关。不要重复已有信息。"""

        try:
            response = self.llm_fn(prompt)
            if response and len(response) > 10:
                return response.strip()[:300]
        except Exception as e:
            logger.warning("narrative: %s", e)

        return None
