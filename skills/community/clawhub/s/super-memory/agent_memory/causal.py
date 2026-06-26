"""
causal.py - 记忆因果链
追踪记忆之间的因果关系：哪些记忆影响了哪些决策

v5.3 增强:
- 时间线连接: 6h 窗口内按时间线串联因果
- 主题相似度连接: 跨时间窗口、不同主题但语义相近的记忆建立关联
- 多维因果强度: 结合时间距离 + 主题重叠 + 性质匹配 综合评分
"""

from __future__ import annotations

import os
import json
import time
import logging
import hashlib
from datetime import datetime
from collections import defaultdict

logger = logging.getLogger(__name__)


class CausalChain:
    """
    因果关系类型：
    1. decision_based_on — 决策基于某条记忆
    2. led_to — 某条记忆导致了某个结果
    3. contradicts — 两条记忆矛盾
    4. supports — 互相印证
    5. evolved_from — 概念演进（旧认知 → 新认知）

    v5.3 新增:
    6. timeline_before — 时间线前序（6h 窗口内 A 发生在 B 之前，且有因果可能）
    7. topic_similar — 跨时窗口主题相似（不同时间段但讨论相似内容）
    8. chain_trigger — 链式触发（A→B→C 的传递因果）

    自动发现 + 手动标注
    """

    CAUSAL_LINK_TYPES = {
        "decision_based_on": {"weight": 0.9, "icon": "🎯→", "desc": "决策依据"},
        "led_to":            {"weight": 0.8, "icon": "→🌱", "desc": "导致结果"},
        "contradicts":       {"weight": 0.3, "icon": "⚡",  "desc": "互相矛盾"},
        "supports":          {"weight": 0.7, "icon": "🤝",  "desc": "互相印证"},
        "evolved_from":      {"weight": 0.6, "icon": "🔄",  "desc": "概念演进"},
        # v5.3 新增
        "timeline_before":   {"weight": 0.5, "icon": "⏱️→", "desc": "时间线前序"},
        "topic_similar":     {"weight": 0.4, "icon": "🔗",  "desc": "主题相似"},
        "chain_trigger":     {"weight": 0.75,"icon": "⛓️",  "desc": "链式触发"},
        # Phase 2: 自我指涉
        "self_derived_from": {"weight": 0.85,"icon": "🧠→", "desc": "推理依据"},
        "revised_from":      {"weight": 0.7, "icon": "📝",  "desc": "修正理解"},
        "uncertain_about":   {"weight": 0.4, "icon": "❓",  "desc": "不确定"},
    }

    # 因果检测参数（可通过环境变量或构造函数覆盖）
    _ENV_WINDOW = os.environ.get("AGENT_MEMORY_CAUSAL_WINDOW_SEC")
    TIMELINE_WINDOW_SEC = int(_ENV_WINDOW) if _ENV_WINDOW else 6 * 3600  # 默认 6h
    TIMELINE_MAX_GAP_SEC = 30 * 60        # 同一时间线链中最大间隔 30min
    TOPIC_SIMILARITY_THRESHOLD = 0.3      # 主题相似度阈值（Jaccard）
    SEMANTIC_SIMILARITY_THRESHOLD = 0.65  # 语义相似度阈值（有 embedding 时）
    MAX_TIMELINE_DEPTH = 10               # 单条时间线最大深度

    def __init__(self, store, window_hours: int = None, llm_fn=None):
        self.store = store
        self.llm_fn = llm_fn
        if window_hours is not None:
            self.TIMELINE_WINDOW_SEC = window_hours * 3600

    def add_causal_link(
        self,
        source_id: str,
        target_id: str,
        link_type: str,
        explanation: str = None,
    ) -> dict:
        """
        手动添加因果关系。

        参数:
            source_id: 原因记忆 ID
            target_id: 结果记忆 ID
            link_type: decision_based_on / led_to / contradicts / supports / evolved_from
            explanation: 因果解释
        """
        if link_type not in self.CAUSAL_LINK_TYPES:
            raise ValueError(f"无效因果类型: {link_type}，可选: {list(self.CAUSAL_LINK_TYPES.keys())}")

        config = self.CAUSAL_LINK_TYPES[link_type]

        self.store.insert_link(
            source_id=source_id,
            target_id=target_id,
            link_type=f"causal.{link_type}",
            weight=config["weight"],
            reason=explanation or config["desc"],
        )

        logger.info(f"🔗 因果链: {source_id} {config['icon']} {target_id} ({link_type})")
        return {
            "source": source_id,
            "target": target_id,
            "link_type": link_type,
            "weight": config["weight"],
        }

    def auto_detect_causality(self, window_hours: int = 6) -> list[dict]:
        """
        自动检测因果关系（启发式规则）。

        修复 (P0): O(n²) 两两比对 → O(n) 滑动窗口，只比较相邻对
        - 窗口从 24h 缩小到 6h（与 timeline 一致）
        - 只看最近 100 条（不再全量）
        - 不再嵌套 for i/for j，只比较排序后的相邻对

        参数:
            window_hours: 检测时间窗口（默认 6h）
        """
        import time
        now = int(time.time())
        window_start = now - window_hours * 3600

        MAX_CAUSAL_MEMORIES = 100

        memories = self.store.query(limit=MAX_CAUSAL_MEMORIES, time_from=window_start)
        memories.sort(key=lambda m: m.get("time_ts", 0))

        if len(memories) < 2:
            return []

        detected = []

        # O(n) 滑动窗口：只比较相邻对（不再 O(n²) 全量两两）
        for i in range(len(memories) - 1):
            mem_a = memories[i]
            mem_b = memories[i + 1]

            time_gap = mem_b.get("time_ts", 0) - mem_a.get("time_ts", 0)
            if time_gap > self.TIMELINE_MAX_GAP_SEC:  # 30min 超过则跳过
                continue

            # 检查是否同主题
            topics_a = self._extract_topics(mem_a)
            topics_b = self._extract_topics(mem_b)
            shared_topics = topics_a & topics_b

            if not shared_topics:
                continue

            # 推断因果类型
            nature_a = mem_a.get("nature_id", "")
            nature_b = mem_b.get("nature_id", "")

            link_type = None
            explanation = None

            # explore/ask → decision/task/output
            if nature_a in ("D04", "D12") and nature_b in ("D03", "D06", "D07"):
                link_type = "decision_based_on"
                explanation = f"探索后的决策 ({nature_a}→{nature_b})"

            # todo → output
            elif nature_a == "D07" and nature_b == "D06":
                link_type = "led_to"
                explanation = "待办导致产出"

            # 同性质的 note 互相印证
            elif nature_a == nature_b == "D05":
                link_type = "supports"
                explanation = "同类型笔记互相印证"

            if link_type:
                link = self.add_causal_link(
                    mem_a["memory_id"],
                    mem_b["memory_id"],
                    link_type,
                    explanation,
                )
                detected.append(link)

        logger.info(f"🔍 启发式因果检测: {len(detected)} 条 (O(n) 滑动窗口)")
        return detected

    def get_causal_chain(self, memory_id: str, max_depth: int = 3) -> dict:
        """
        获取一条记忆的完整因果链。

        返回:
        {
            "root": memory_id,
            "caused_by": [...],    # 原因链（向上追溯）
            "led_to": [...],       # 结果链（向下展开）
            "contradictions": [...],  # 矛盾项
            "chain_depth": int,
        }
        """
        caused_by = self._traverse_causality(memory_id, direction="up", max_depth=max_depth)
        led_to = self._traverse_causality(memory_id, direction="down", max_depth=max_depth)
        contradictions = self._find_contradictions(memory_id)

        return {
            "root": memory_id,
            "caused_by": caused_by,
            "led_to": led_to,
            "contradictions": contradictions,
            "chain_depth": max(
                max((c.get("_depth", 0) for c in caused_by), default=0),
                max((c.get("_depth", 0) for c in led_to), default=0),
            ),
        }

    def _traverse_causality(self, memory_id: str, direction: str, max_depth: int) -> list[dict]:
        """遍历因果链"""
        visited = set()
        results = []

        def _walk(current_id, depth):
            if depth > max_depth or current_id in visited:
                return
            visited.add(current_id)

            if direction == "up":
                # 找"导致 current"的记忆（target=current）
                links = self.store.conn.execute(
                    """SELECT * FROM memory_links
                       WHERE target_id = ? AND link_type LIKE 'causal.%'""",
                    (current_id,),
                ).fetchall()
            else:
                # 找"被 current 导致"的记忆（source=current）
                links = self.store.conn.execute(
                    """SELECT * FROM memory_links
                       WHERE source_id = ? AND link_type LIKE 'causal.%'""",
                    (current_id,),
                ).fetchall()

            for link in links:
                related_id = link["source_id"] if direction == "up" else link["target_id"]
                if related_id not in visited:
                    mem = self.store.get_memory(related_id)
                    if mem:
                        causal_type = link["link_type"].replace("causal.", "")
                        config = self.CAUSAL_LINK_TYPES.get(causal_type, {})
                        mem["_causal_type"] = causal_type
                        mem["_causal_icon"] = config.get("icon", "→")
                        mem["_causal_desc"] = config.get("desc", "")
                        mem["_depth"] = depth
                        results.append(mem)
                    _walk(related_id, depth + 1)

        _walk(memory_id, 1)
        return results

    def _find_contradictions(self, memory_id: str) -> list[dict]:
        """找到与指定记忆矛盾的记录"""
        links = self.store.conn.execute(
            """SELECT * FROM memory_links
               WHERE (source_id = ? OR target_id = ?)
               AND link_type = 'causal.contradicts'""",
            (memory_id, memory_id),
        ).fetchall()

        results = []
        for link in links:
            other_id = link["target_id"] if link["source_id"] == memory_id else link["source_id"]
            mem = self.store.get_memory(other_id)
            if mem:
                results.append(mem)
        return results

    def format_causal_chain(self, chain: dict) -> str:
        """格式化因果链为可读文本"""
        lines = []
        root_id = chain["root"][:30]

        if chain["caused_by"]:
            lines.append("⬆️ 原因链:")
            for m in chain["caused_by"]:
                indent = "  " * m.get("_depth", 1)
                icon = m.get("_causal_icon", "→")
                content = m.get("content", "")[:50]
                lines.append(f"{indent}{icon} {content}")

        lines.append(f"🎯 当前: {root_id}...")

        if chain["led_to"]:
            lines.append("⬇️ 结果链:")
            for m in chain["led_to"]:
                indent = "  " * m.get("_depth", 1)
                icon = m.get("_causal_icon", "→")
                content = m.get("content", "")[:50]
                lines.append(f"{indent}{icon} {content}")

        if chain["contradictions"]:
            lines.append("⚡ 矛盾项:")
            for m in chain["contradictions"]:
                lines.append(f"  ⚡ {m.get('content', '')[:50]}")

        return "\n".join(lines) if lines else "无因果链"

    def get_stats(self) -> dict:
        """因果关系统计"""
        rows = self.store.conn.execute(
            """SELECT link_type, COUNT(*) as cnt
               FROM memory_links
               WHERE link_type LIKE 'causal.%'
               GROUP BY link_type"""
        ).fetchall()

        by_type = {}
        for r in rows:
            causal_type = r["link_type"].replace("causal.", "")
            by_type[causal_type] = r["cnt"]

        return {
            "total_causal_links": sum(by_type.values()),
            "by_type": by_type,
        }

    # ══════════════════════════════════════════════════════
    # v5.3: 时间线因果连接
    # ══════════════════════════════════════════════════════

    def detect_timeline_causality(self, window_hours: int = 6, embedding_store=None) -> list[dict]:
        """
        时间线因果检测。

        核心思想：6h 窗口内的记忆，按时间排序后，
        相邻且有因果信号的对 → timeline_before
        传递链条（A→B→C）→ chain_trigger

        检测维度：
        1. 时间邻近性: 间隔越短因果可能性越高
        2. 主题重叠: 共享主题 → 因果信号
        3. 性质序列: explore→decision, todo→output 是强因果模式
        4. 内容关键词: "因为…所以"、"基于…决定" 等显式因果词
        5. 语义相似度: 有 embedding 时用余弦相似度补充

        参数:
            window_hours: 检测窗口（默认 6h）
            embedding_store: 可选，语义相似度计算

        返回: 检测到的因果关系列表
        """
        now = int(time.time())
        window_start = now - window_hours * 3600

        # 获取窗口内记忆，按时间排序
        memories = self.store.query(limit=500)
        memories = [m for m in memories if m.get("time_ts", 0) >= window_start]
        memories.sort(key=lambda m: m.get("time_ts", 0))

        if len(memories) < 2:
            return []

        detected = []

        # ── Pass 1: 邻近对检测（O(n) 滑动窗口）──
        for i in range(len(memories) - 1):
            mem_a = memories[i]
            mem_b = memories[i + 1]

            time_gap = mem_b.get("time_ts", 0) - mem_a.get("time_ts", 0)
            if time_gap > self.TIMELINE_MAX_GAP_SEC:
                continue

            # 计算因果强度
            score, reason = self._compute_causal_score(
                mem_a, mem_b, time_gap, embedding_store
            )

            if score >= 0.4:  # 因果阈值
                link_type = self._infer_causal_type(mem_a, mem_b, score)
                link = self.add_causal_link(
                    mem_a["memory_id"],
                    mem_b["memory_id"],
                    link_type,
                    f"{reason} (score={score:.2f}, gap={time_gap}s)",
                )
                link["_score"] = score
                detected.append(link)

        # ── Pass 2: 链式传递检测（A→B→C → A→C chain_trigger）──
        chain_links = self._detect_chain_triggers(memories, detected)
        detected.extend(chain_links)

        # ── Pass 3: 跨时窗口主题相似度 ──
        topic_sim_links = self._detect_topic_similarity(memories, embedding_store)
        detected.extend(topic_sim_links)

        logger.info(
            f"🔍 时间线因果检测: {len(detected)} 条 "
            f"(邻近={sum(1 for d in detected if 'timeline' in d.get('link_type', ''))}, "
            f"链式={sum(1 for d in detected if 'chain' in d.get('link_type', ''))}, "
            f"主题相似={sum(1 for d in detected if 'topic_similar' in d.get('link_type', ''))})"
        )
        return detected

    def _compute_causal_score(
        self, mem_a: dict, mem_b: dict, time_gap: int, embedding_store=None
    ) -> tuple[float, str]:
        """
        计算两条记忆之间的因果强度评分。

        综合维度:
        - 时间衰减: 越近越高 (0~0.3)
        - 主题重叠: 共享主题数/总主题数 (0~0.3)
        - 性质匹配: explore→decision 等模式 (0~0.2)
        - 显式因果词: 内容中出现因果连接词 (0~0.2)
        - 语义相似度: embedding 余弦 (0~0.2, 有 embedding 时)

        返回: (score, reason)
        """
        score = 0.0
        reasons = []

        # 1. 时间衰减因子 (0~0.3)
        if time_gap <= 60:
            time_score = 0.3
            reasons.append("1min内")
        elif time_gap <= 300:
            time_score = 0.25
            reasons.append("5min内")
        elif time_gap <= 1800:
            time_score = 0.15
            reasons.append("30min内")
        elif time_gap <= self.TIMELINE_WINDOW_SEC:
            time_score = 0.08
            reasons.append("6h内")
        else:
            time_score = 0.0
        score += time_score

        # 2. 主题重叠 (0~0.3)
        topics_a = self._extract_topics(mem_a)
        topics_b = self._extract_topics(mem_b)
        if topics_a and topics_b:
            shared = topics_a & topics_b
            union = topics_a | topics_b
            jaccard = len(shared) / len(union) if union else 0
            topic_score = jaccard * 0.3
            score += topic_score
            if shared:
                reasons.append(f"主题重叠={jaccard:.1%}")
        else:
            # 没有主题信息，尝试内容相似度
            content_sim = self._content_keyword_overlap(mem_a, mem_b)
            score += content_sim * 0.2
            if content_sim > 0.1:
                reasons.append(f"关键词重叠={content_sim:.1%}")

        # 3. 性质匹配模式 (0~0.2)
        nature_a = mem_a.get("nature_id", "")
        nature_b = mem_b.get("nature_id", "")
        nature_score = self._nature_causal_score(nature_a, nature_b)
        score += nature_score
        if nature_score > 0.1:
            reasons.append(f"性质模式({nature_a}→{nature_b})")

        # 4. 显式因果词 (0~0.2)
        causal_word_score = self._detect_causal_words(mem_a, mem_b)
        score += causal_word_score
        if causal_word_score > 0:
            reasons.append("含因果连接词")

        # 5. 语义相似度 (0~0.2, 有 embedding 时)
        if embedding_store:
            try:
                sem_sim = self._semantic_similarity(
                    mem_a.get("content", ""), mem_b.get("content", ""), embedding_store
                )
                sem_score = sem_sim * 0.2
                score += sem_score
                if sem_sim > 0.5:
                    reasons.append(f"语义相似={sem_sim:.2f}")
            except Exception as e:
                logger.debug(f"语义相似度计算失败: {e}")

        reason_str = " + ".join(reasons) if reasons else "弱因果信号"
        return min(score, 1.0), reason_str

    def _extract_topics(self, mem: dict) -> set:
        """提取记忆的主题集合"""
        topics = mem.get("topics", [])
        result = set()
        for t in topics:
            if isinstance(t, dict):
                code = t.get("code", "")
            elif isinstance(t, str):
                code = t
            else:
                continue
            if code:
                # 保留完整主题和一级主题
                result.add(code)
                result.add(code.split(".")[0])
        return result

    def _content_keyword_overlap(self, mem_a: dict, mem_b: dict) -> float:
        """计算内容关键词重叠度"""
        content_a = mem_a.get("content", "")
        content_b = mem_b.get("content", "")
        if not content_a or not content_b:
            return 0.0

        # 中文：按字符 bigram 分词
        def bigrams(text):
            return set(text[i:i+2] for i in range(len(text)-1) if text[i:i+2].strip())

        grams_a = bigrams(content_a)
        grams_b = bigrams(content_b)
        if not grams_a or not grams_b:
            return 0.0

        shared = grams_a & grams_b
        union = grams_a | grams_b
        return len(shared) / len(union) if union else 0.0

    def _nature_causal_score(self, nature_a: str, nature_b: str) -> float:
        """性质对的因果评分"""
        # 强因果模式
        strong_patterns = {
            ("D04", "D03"): 0.2,   # explore → decision
            ("D12", "D03"): 0.2,   # ask → decision
            ("D07", "D06"): 0.2,   # todo → output
            ("D04", "D07"): 0.15,  # explore → todo
            ("D12", "D07"): 0.15,  # ask → todo
            ("D05", "D03"): 0.15,  # note → decision (先记录后决策)
        }
        return strong_patterns.get((nature_a, nature_b), 0.0)

    def _detect_causal_words(self, mem_a: dict, mem_b: dict) -> float:
        """检测内容中的显式因果连接词"""
        # A 中的"前因"词
        cause_words_a = ["因为", "由于", "鉴于", "基于", "考虑到", "发现", "分析", "研究"]
        # B 中的"后果"词
        effect_words_b = ["所以", "因此", "于是", "决定", "选择", "改为", "最终", "结论"]

        content_a = mem_a.get("content", "")
        content_b = mem_b.get("content", "")

        has_cause = any(w in content_a for w in cause_words_a)
        has_effect = any(w in content_b for w in effect_words_b)

        if has_cause and has_effect:
            return 0.2
        if has_cause or has_effect:
            return 0.08
        return 0.0

    def _semantic_similarity(self, text_a: str, text_b: str, embedding_store) -> float:
        """用 embedding 计算语义相似度"""
        try:
            # 搜索 text_a，看 text_b 是否在 top 结果中
            results = embedding_store.search(text_a, top_k=20)
            # 这是一个近似——如果 text_b 被索引，应该在结果中
            # 但由于我们没有直接的 pair 相似度 API，用 search score 代理
            if results:
                return min(r.get("score", 0) for r in results[:1]) if results else 0.0
        except Exception as e:
            logger.debug(f"语义因果搜索失败: {e}")
        return 0.0

    def _infer_causal_type(self, mem_a: dict, mem_b: dict, score: float) -> str:
        """根据性质和评分推断因果类型"""
        nature_a = mem_a.get("nature_id", "")
        nature_b = mem_b.get("nature_id", "")

        # 探索/提问 → 决策
        if nature_a in ("D04", "D12") and nature_b == "D03":
            return "decision_based_on"
        # 待办 → 产出
        if nature_a == "D07" and nature_b == "D06":
            return "led_to"
        # 同性质 → 互相印证
        if nature_a == nature_b == "D05":
            return "supports"
        # 默认：时间线前序
        return "timeline_before"

    # ══════════════════════════════════════════════════════
    # v5.3: 链式触发检测
    # ══════════════════════════════════════════════════════

    def _detect_chain_triggers(self, memories: list[dict], existing_links: list[dict]) -> list[dict]:
        """
        检测链式因果传递。

        如果 A→B 和 B→C 都被检测到，推导 A→C (chain_trigger)
        链式关系比单步关系的权重略低，但提供重要的上下文连接。
        """
        # 构建邻接表: source_id -> [target_id, ...]
        adjacency = defaultdict(set)
        for link in existing_links:
            adjacency[link.get("source", "")].add(link.get("target", ""))

        chain_links = []
        visited_chains = set()

        for source in list(adjacency.keys()):
            for mid in adjacency[source]:
                if mid in adjacency:
                    for target in adjacency[mid]:
                        if target == source:
                            continue  # 避免环

                        chain_key = tuple(sorted([source, target]))
                        if chain_key in visited_chains:
                            continue
                        visited_chains.add(chain_key)

                        # 检查是否已有直接链接
                        existing_direct = any(
                            (link.get("source") == source and link.get("target") == target)
                            or (link.get("source") == target and link.get("target") == source)
                            for link in existing_links
                        )
                        if existing_direct:
                            continue

                        # 获取记忆对象
                        mem_source = self.store.get_memory(source)
                        mem_target = self.store.get_memory(target)
                        if not mem_source or not mem_target:
                            continue

                        # 检查时间距离（链式传递要求不超过 6h）
                        time_gap = abs(
                            mem_target.get("time_ts", 0) - mem_source.get("time_ts", 0)
                        )
                        if time_gap > self.TIMELINE_WINDOW_SEC:
                            continue

                        # 创建链式触发链接
                        explanation = f"链式传递: {source[:8]}→{mid[:8]}→{target[:8]}"
                        link = self.add_causal_link(
                            source, target, "chain_trigger", explanation
                        )
                        chain_links.append(link)

        return chain_links

    # ══════════════════════════════════════════════════════
    # v5.3: 跨时窗口主题相似度连接
    # ══════════════════════════════════════════════════════

    def _detect_topic_similarity(
        self, memories: list[dict], embedding_store=None
    ) -> list[dict]:
        """
        跨时窗口主题相似度连接。

        将当前窗口的记忆与更早的记忆（7天内）做主题相似度比较，
        找到"不同时间段讨论相似内容"的关联。

        触发条件：
        1. 时间距离 > 6h（否则已经被时间线检测覆盖）
        2. 主题 Jaccard 相似度 >= 阈值，或语义相似度 >= 阈值
        3. 性质不同（同性质的简单重复不值得关联）

        应用场景：
        - 用户在不同天讨论同一个项目的技术选型
        - 某个概念在多天内反复出现并逐步演进
        - 跨天的决策链条
        """
        now = int(time.time())
        recent_window_start = now - 6 * 3600      # 6h 内（已被时间线覆盖）
        extended_window_start = now - 7 * 24 * 3600  # 7 天内

        # 获取 7 天内但不在 6h 窗口内的记忆
        extended_memories = self.store.query(limit=500)
        extended_memories = [
            m for m in extended_memories
            if extended_window_start <= m.get("time_ts", 0) < recent_window_start
        ]

        if not extended_memories or not memories:
            return []

        links = []
        seen_pairs = set()

        # 用主题索引加速：先按主题分组
        topic_index = defaultdict(list)  # topic_code -> [memory, ...]
        for mem in extended_memories:
            for topic in self._extract_topics(mem):
                topic_index[topic].append(mem)

        for current_mem in memories:
            current_topics = self._extract_topics(current_mem)
            if not current_topics:
                continue

            # 找到共享主题的历史记忆
            candidate_mems = set()
            for topic in current_topics:
                for hist_mem in topic_index.get(topic, []):
                    candidate_mems.add(hist_mem["memory_id"])

            for hist_id in candidate_mems:
                hist_mem = self.store.get_memory(hist_id)
                if not hist_mem:
                    continue

                # 避免重复
                pair_key = tuple(sorted([current_mem["memory_id"], hist_id]))
                if pair_key in seen_pairs:
                    continue
                seen_pairs.add(pair_key)

                # 时间距离 > 6h（已经过滤了，再确认一下）
                time_gap = abs(
                    current_mem.get("time_ts", 0) - hist_mem.get("time_ts", 0)
                )
                if time_gap <= self.TIMELINE_WINDOW_SEC:
                    continue

                # 计算主题相似度
                hist_topics = self._extract_topics(hist_mem)
                shared = current_topics & hist_topics
                union = current_topics | hist_topics
                jaccard = len(shared) / len(union) if union else 0

                # 性质是否不同（同性质重复不关联）
                same_nature = current_mem.get("nature_id") == hist_mem.get("nature_id")

                if jaccard >= self.TOPIC_SIMILARITY_THRESHOLD and not same_nature:
                    explanation = (
                        f"跨时主题相似: 共享 {len(shared)} 个主题 "
                        f"(jaccard={jaccard:.2f}, "
                        f"gap={time_gap//3600}h)"
                    )
                    weight = min(0.4, jaccard * 0.5)
                    link = self.add_causal_link(
                        hist_id,
                        current_mem["memory_id"],
                        "topic_similar",
                        explanation,
                    )
                    # 覆盖默认权重
                    self.store.conn.execute(
                        """UPDATE memory_links SET weight = ?
                           WHERE source_id = ? AND target_id = ? AND link_type = 'causal.topic_similar'""",
                        (weight, hist_id, current_mem["memory_id"]),
                    )
                    self.store.conn.commit()
                    links.append(link)

                # 有 embedding 时，也检查语义相似度
                if embedding_store and jaccard < self.TOPIC_SIMILARITY_THRESHOLD:
                    try:
                        sem_sim = self._semantic_similarity(
                            current_mem.get("content", ""),
                            hist_mem.get("content", ""),
                            embedding_store,
                        )
                        if sem_sim >= self.SEMANTIC_SIMILARITY_THRESHOLD:
                            explanation = (
                                f"语义相似跨时连接: "
                                f"sim={sem_sim:.2f}, gap={time_gap//3600}h"
                            )
                            link = self.add_causal_link(
                                hist_id,
                                current_mem["memory_id"],
                                "topic_similar",
                                explanation,
                            )
                            links.append(link)
                    except Exception as e:
                        logger.debug(f"跨时主题相似检测失败: {e}")

        return links

    # ══════════════════════════════════════════════════════
    # v5.3: 完整因果检测入口（替代旧的 auto_detect_causality）
    # ══════════════════════════════════════════════════════

    def full_causal_analysis(self, window_hours: int = 6, embedding_store=None) -> dict:
        """
        完整因果分析（v5.3 统一入口）。

        执行所有因果检测：
        1. 原有启发式规则（explore→decision 等）
        2. 时间线因果（6h 滑动窗口 + 多维评分）
        3. 链式传递（A→B→C → A→C）
        4. 跨时窗口主题相似

        参数:
            window_hours: 检测窗口
            embedding_store: 可选语义引擎

        返回: 各类检测的统计
        """
        result = {
            "heuristic": [],
            "timeline": [],
            "total": 0,
        }

        # 1. 原有启发式规则
        try:
            result["heuristic"] = self.auto_detect_causality(window_hours=window_hours)
        except Exception as e:
            logger.warning("causal: %s", e)

        # 2. 时间线 + 链式 + 主题相似度（合并为一个调用）
        try:
            result["timeline"] = self.detect_timeline_causality(
                window_hours=window_hours,
                embedding_store=embedding_store,
            )
        except Exception as e:
            logger.warning("causal: %s", e)

        result["total"] = len(result["heuristic"]) + len(result["timeline"])

        logger.info(
            f"🔗 完整因果分析: {result['total']} 条 "
            f"(启发式={len(result['heuristic'])}, 时间线+链式+相似={len(result['timeline'])})"
        )
        return result

    # ══════════════════════════════════════════════════════
    # v8.3: LLM 辅助隐式因果识别
    # ══════════════════════════════════════════════════════

    def llm_causal_analysis(
        self,
        source_content: str,
        target_content: str,
        source_id: str = "",
        target_id: str = "",
    ) -> dict:
        """
        使用 LLM 分析两条记忆之间的隐式因果关系。

        当启发式规则无法检测到因果，但语义上存在因果可能时，
        通过 LLM 进行深度分析。

        参数:
            source_content: 前一条记忆内容
            target_content: 后一条记忆内容
            source_id: 前一条记忆 ID
            target_id: 后一条记忆 ID

        返回: {
            "has_causal": bool,
            "link_type": str,
            "confidence": float,
            "explanation": str,
            "causal_direction": str,  # "forward"|"backward"|"bidirectional"|"none"
        }
        """
        if not self.llm_fn:
            return {
                "has_causal": False,
                "link_type": "",
                "confidence": 0.0,
                "explanation": "LLM 不可用",
                "causal_direction": "none",
            }

        prompt = f"""分析以下两条记忆之间是否存在隐式因果关系。

记忆A（较早）: {source_content[:500]}
记忆B（较晚）: {target_content[:500]}

请判断：
1. A是否导致了B？（因果）
2. A和B是否互相矛盾？（矛盾）
3. A是否是B的决策依据？（决策）
4. B是否修正了A中的认知？（演进）
5. 两者是否只是时间上相邻但无因果？

请用以下JSON格式回答（不要包含其他文字）：
{{
    "has_causal": true/false,
    "link_type": "led_to/contradicts/decision_based_on/evolved_from/supports/none",
    "confidence": 0.0-1.0,
    "explanation": "简短解释为什么存在/不存在因果关系",
    "causal_direction": "forward/backward/bidirectional/none"
}}"""

        try:
            raw = self.llm_fn(prompt)
            result = self._parse_llm_causal_response(raw)
            if result.get("has_causal") and result.get("link_type", "none") != "none":
                if source_id and target_id:
                    weight = result.get("confidence", 0.5)
                    link_type = result.get("link_type", "led_to")
                    if link_type not in self.CAUSAL_LINK_TYPES:
                        link_type = "led_to"
                    self.store.insert_link(
                        source_id, target_id,
                        link_type=f"causal.{link_type}",
                        weight=weight,
                        reason=f"LLM因果分析: {result.get('explanation', '')[:100]}",
                    )
            return result
        except Exception as e:
            logger.warning("causal: %s", e)
            return {
                "has_causal": False,
                "link_type": "",
                "confidence": 0.0,
                "explanation": f"分析失败: {e}",
                "causal_direction": "none",
            }

    def batch_llm_causal_analysis(
        self,
        memory_pairs: list[tuple[str, str, str, str]] = None,
        window_hours: int = 2,
        max_pairs: int = 20,
        min_confidence: float = 0.3,
    ) -> list[dict]:
        """
        批量 LLM 因果分析。

        对指定时间窗口内的时间相邻记忆对进行 LLM 因果分析。
        仅对启发式规则未检测到因果的记忆对进行分析。

        参数:
            memory_pairs: 手动指定的记忆对 [(source_id, target_id, source_content, target_content), ...]
            window_hours: 自动扫描的时间窗口（仅当 memory_pairs 为 None 时使用）
            max_pairs: 最大分析对数
            min_confidence: 最低置信度阈值

        返回: [{"source_id": str, "target_id": str, ...llm_causal_analysis result}]
        """
        if not self.llm_fn:
            logger.debug("LLM 不可用，跳过批量因果分析")
            return []

        pairs = memory_pairs
        if not pairs:
            pairs = self._find_candidate_pairs(window_hours, max_pairs)

        if not pairs:
            return []

        results = []
        for source_id, target_id, source_content, target_content in pairs[:max_pairs]:
            existing = self.store.query_links(source_id, target_id) if hasattr(self.store, 'query_links') else []
            causal_existing = [l for l in existing if l.get("link_type", "").startswith("causal")]
            if causal_existing:
                continue

            result = self.llm_causal_analysis(
                source_content, target_content,
                source_id, target_id,
            )
            if result.get("has_causal") and result.get("confidence", 0) >= min_confidence:
                result["source_id"] = source_id
                result["target_id"] = target_id
                results.append(result)

        logger.info(f"🧠 LLM 批量因果分析: {len(pairs)} 对 → {len(results)} 条因果")
        return results

    def _find_candidate_pairs(
        self, window_hours: int, max_pairs: int
    ) -> list[tuple[str, str, str, str]]:
        """
        在指定时间窗口内查找候选因果记忆对。

        策略：查找同一 person 的连续记忆对，且尚未建立因果 link。
        """
        cutoff = int(time.time()) - window_hours * 3600
        try:
            rows = self.store.conn.execute(
                "SELECT memory_id, content, person_id, time_ts "
                "FROM memories WHERE time_ts >= ? ORDER BY person_id, time_ts",
                (cutoff,),
            ).fetchall()
        except Exception:
            return []

        by_person = defaultdict(list)
        for r in rows:
            by_person[r[2]].append((r[0], r[3], r[1]))

        pairs = []
        for person_id, mems in by_person.items():
            mems.sort(key=lambda x: x[1])
            for i in range(len(mems) - 1):
                if len(pairs) >= max_pairs:
                    break
                s_id, s_ts, s_content = mems[i]
                t_id, t_ts, t_content = mems[i + 1]
                if t_ts - s_ts < 300:
                    pairs.append((s_id, t_id, s_content, t_content))

        return pairs

    def _parse_llm_causal_response(self, raw: str) -> dict:
        """解析 LLM 返回的因果分析 JSON"""
        import re
        json_match = re.search(r'\{[^{}]+\}', raw, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group())
            except (json.JSONDecodeError, ValueError) as e:
                logger.debug("causal: JSON parse: %s", e)

        has_causal = "true" in raw.lower()[:100] and "has_causal" in raw.lower()
        return {
            "has_causal": has_causal,
            "link_type": "led_to" if has_causal else "none",
            "confidence": 0.3 if has_causal else 0.0,
            "explanation": raw[:200],
            "causal_direction": "forward" if has_causal else "none",
        }

    # ══════════════════════════════════════════════════════
    # v8.3: 矛盾检测增强
    # ══════════════════════════════════════════════════════

    def detect_contradictions(
        self,
        topic_code: str = None,
        window_hours: int = 720,
        use_llm: bool = True,
    ) -> list[dict]:
        """
        检测记忆中的矛盾/认知变化。

        策略：
        1. 同一主题下的记忆，如果情感极性翻转（正→负或负→正），可能是矛盾
        2. 同一主题下 importance 显著变化（如 medium → breakthrough），可能是认知升级
        3. LLM 辅助：对比同一主题的早期和晚期记忆，检测观点变化

        参数:
            topic_code: 限定主题（None=全部）
            window_hours: 检测窗口（默认30天）
            use_llm: 是否使用 LLM 辅助

        返回: [{"memory_a": dict, "memory_b": dict, "contradiction_type": str, "confidence": float}]
        """
        cutoff = int(time.time()) - window_hours * 3600
        contradictions = []

        try:
            if topic_code:
                rows = self.store.conn.execute(
                    "SELECT m.memory_id, m.content, m.valence, m.importance, m.time_ts, "
                    "m.significance, m.primary_emotions "
                    "FROM memories m JOIN memory_topics mt ON m.memory_id = mt.memory_id "
                    "WHERE mt.topic_code = ? AND m.time_ts >= ? "
                    "ORDER BY m.time_ts",
                    (topic_code, cutoff),
                ).fetchall()
            else:
                rows = self.store.conn.execute(
                    "SELECT memory_id, content, valence, importance, time_ts, "
                    "significance, primary_emotions FROM memories "
                    "WHERE time_ts >= ? ORDER BY time_ts",
                    (cutoff,),
                ).fetchall()
        except Exception as e:
            logger.warning("causal: %s", e)
            return []

        by_topic = defaultdict(list)
        for r in rows:
            mid, content, valence, importance, ts, significance, pe = r[:7]
            if topic_code:
                key = topic_code
            else:
                try:
                    topics = self.store.conn.execute(
                        "SELECT topic_code FROM memory_topics WHERE memory_id = ? AND is_primary = 1",
                        (mid,),
                    ).fetchall()
                    key = topics[0][0] if topics else "misc"
                except Exception:
                    key = "misc"
            by_topic[key].append({
                "memory_id": mid,
                "content": content,
                "valence": valence or 0.0,
                "importance": importance or "medium",
                "time_ts": ts,
                "significance": significance or "notable",
                "primary_emotions": pe or "{}",
            })

        for tpc, mems in by_topic.items():
            if len(mems) < 2:
                continue
            mems.sort(key=lambda x: x["time_ts"])

            for i in range(len(mems) - 1):
                early, late = mems[i], mems[i + 1]
                valence_flip = (early["valence"] > 0.3 and late["valence"] < -0.3) or \
                               (early["valence"] < -0.3 and late["valence"] > 0.3)

                importance_shift = False
                importance_order = {"trivial": 0, "notable": 1, "medium": 2, "important": 3,
                                    "breakthrough": 4, "crisis": 4, "milestone": 5}
                if importance_order.get(early["importance"], 0) < importance_order.get(late["importance"], 0) - 1:
                    importance_shift = True

                if valence_flip:
                    contradictions.append({
                        "memory_a": early,
                        "memory_b": late,
                        "contradiction_type": "valence_flip",
                        "confidence": min(1.0, abs(early["valence"] - late["valence"]) / 2.0),
                        "topic": tpc,
                    })

                if importance_shift:
                    contradictions.append({
                        "memory_a": early,
                        "memory_b": late,
                        "contradiction_type": "importance_shift",
                        "confidence": 0.6,
                        "topic": tpc,
                    })

        if use_llm and self.llm_fn and contradictions:
            contradictions = self._llm_verify_contradictions(contradictions)

        for c in contradictions:
            if c.get("confidence", 0) >= 0.4:
                self.store.insert_link(
                    c["memory_a"]["memory_id"],
                    c["memory_b"]["memory_id"],
                    link_type="causal.contradicts",
                    weight=c.get("confidence", 0.5),
                    reason=f"矛盾检测({c['contradiction_type']}): {c.get('topic', '')}",
                )

        logger.info(f"⚡ 矛盾检测: {len(contradictions)} 条潜在矛盾")
        return contradictions

    def _llm_verify_contradictions(self, candidates: list[dict]) -> list[dict]:
        """用 LLM 验证候选矛盾是否为真矛盾"""
        verified = []
        for c in candidates[:10]:
            if not self.llm_fn:
                verified.append(c)
                continue
            prompt = f"""判断以下两条记忆是否存在矛盾或认知变化。

记忆A: {c['memory_a']['content'][:300]}
记忆B: {c['memory_b']['content'][:300]}

请用JSON回答：
{{"is_contradiction": true/false, "type": "观点变化/事实矛盾/无矛盾", "confidence": 0.0-1.0, "explanation": "简短说明"}}"""

            try:
                raw = self.llm_fn(prompt)
                import re
                match = re.search(r'\{[^{}]+\}', raw, re.DOTALL)
                if match:
                    parsed = json.loads(match.group())
                    if parsed.get("is_contradiction"):
                        c["confidence"] = parsed.get("confidence", c.get("confidence", 0.5))
                        c["llm_explanation"] = parsed.get("explanation", "")
                        verified.append(c)
                else:
                    verified.append(c)
            except Exception:
                verified.append(c)

        return verified

    # ══════════════════════════════════════════════════════
    # v8.3: 因果链可视化
    # ══════════════════════════════════════════════════════

    def visualize_causal_chain(
        self,
        root_memory_id: str,
        max_depth: int = 5,
        direction: str = "both",
    ) -> dict:
        """
        生成从指定记忆出发的因果链可视化数据。

        参数:
            root_memory_id: 起始记忆 ID
            max_depth: 最大遍历深度
            direction: "forward"（只看后果）/ "backward"（只看原因）/ "both"

        返回: {
            "nodes": [{"id": str, "content_preview": str, "nature": str, "time_ts": int}],
            "edges": [{"source": str, "target": str, "type": str, "weight": float, "reason": str}],
            "chains": [[memory_id, ...]],  # 完整因果链
            "summary": str,
        }
        """
        nodes = {}
        edges = []
        visited = set()

        def _traverse(mid: str, depth: int):
            if depth > max_depth or mid in visited:
                return
            visited.add(mid)

            mem = self.store.get_memory(mid)
            if not mem:
                return
            nodes[mid] = {
                "id": mid,
                "content_preview": (mem.get("content") or "")[:80],
                "nature": mem.get("nature_id", ""),
                "time_ts": mem.get("time_ts", 0),
            }

            if direction in ("forward", "both"):
                forward_links = self.store.conn.execute(
                    "SELECT target_id, link_type, weight, reason FROM memory_links "
                    "WHERE source_id = ? AND link_type LIKE 'causal%'",
                    (mid,),
                ).fetchall()
                for link in forward_links:
                    target_id, link_type, weight, reason = link
                    edges.append({
                        "source": mid,
                        "target": target_id,
                        "type": link_type,
                        "weight": weight or 1.0,
                        "reason": reason or "",
                    })
                    _traverse(target_id, depth + 1)

            if direction in ("backward", "both"):
                backward_links = self.store.conn.execute(
                    "SELECT source_id, link_type, weight, reason FROM memory_links "
                    "WHERE target_id = ? AND link_type LIKE 'causal%'",
                    (mid,),
                ).fetchall()
                for link in backward_links:
                    source_id, link_type, weight, reason = link
                    edges.append({
                        "source": source_id,
                        "target": mid,
                        "type": link_type,
                        "weight": weight or 1.0,
                        "reason": reason or "",
                    })
                    _traverse(source_id, depth + 1)

        _traverse(root_memory_id, 0)

        chains = self._extract_chains(nodes, edges, root_memory_id)

        node_count = len(nodes)
        edge_count = len(edges)
        chain_count = len(chains)
        summary = f"因果链: {node_count} 个节点, {edge_count} 条边, {chain_count} 条链路"

        return {
            "nodes": list(nodes.values()),
            "edges": edges,
            "chains": chains,
            "summary": summary,
        }

    def _extract_chains(
        self, nodes: dict, edges: list[dict], root_id: str
    ) -> list[list[str]]:
        """从边列表中提取完整因果链"""
        forward_map = defaultdict(list)
        for e in edges:
            forward_map[e["source"]].append(e["target"])

        chains = []

        def _dfs(current: str, path: list[str]):
            children = forward_map.get(current, [])
            if not children:
                if len(path) > 1:
                    chains.append(path[:])
                return
            for child in children:
                if child in path:
                    continue
                path.append(child)
                _dfs(child, path)
                path.pop()

        _dfs(root_id, [root_id])
        return chains
