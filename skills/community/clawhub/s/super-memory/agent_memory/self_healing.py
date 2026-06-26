"""
self_healing.py - 记忆自我修复
检测矛盾、过时信息、自动修正或标记

v2: 语义化矛盾检测 — 替代纯关键词对立匹配
"""

from __future__ import annotations

import time
import re
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class SelfHealing:
    """
    三种自我修复能力：

    1. 矛盾检测 — 同主题下结论相反的记忆
    2. 过时检测 — 事实性记忆被更新版本替代
    3. 一致性修复 — 关联记忆的元数据同步

    检测策略：
    - 同主题 + 同性质（note/note）→ 检查是否矛盾
    - 时间较新的覆盖较旧的 → 标记旧的为过时
    - 关联记忆的 importance 差异过大 → 同步
    """

    def __init__(self, store, embedding_store=None):
        self.store = store
        self.embedding_store = embedding_store

    def detect_contradictions(self, topic_code: str = None, limit: int = 50) -> list[dict]:
        """
        检测矛盾记忆。

        修复 (P0): O(n²) 两两比对 → O(n) 相邻滑动窗口
        - 只看最近 50 条 note（原 100），按时间排序后只比较相邻对
        - 主题分桶后桶内比较，不跨桶

        规则：
        - 同主题、同性质(note/note)、但内容中的结论词相反
        """
        memories = self.store.query(limit=limit, topic_code=topic_code)
        notes = [m for m in memories if m.get("nature_id") == "D05"]

        if len(notes) < 2:
            return []

        # 按时间排序
        notes.sort(key=lambda m: m.get("time_ts", 0))

        # 按主主题分桶，桶内做相邻比较
        topic_buckets: dict[str, list[dict]] = {}
        for mem in notes:
            for topic in self._get_primary_topics(mem):
                if topic not in topic_buckets:
                    topic_buckets[topic] = []
                topic_buckets[topic].append(mem)

        contradictions = []
        checked = set()

        for topic, bucket in topic_buckets.items():
            if len(bucket) < 2:
                continue
            # 桶内按时间排序后只比较相邻对
            bucket.sort(key=lambda m: m.get("time_ts", 0))
            for i in range(len(bucket) - 1):
                mem_a = bucket[i]
                mem_b = bucket[i + 1]

                pair_key = tuple(sorted([mem_a["memory_id"], mem_b["memory_id"]]))
                if pair_key in checked:
                    continue
                checked.add(pair_key)

                score = self._contradiction_score(
                    mem_a.get("content", ""),
                    mem_b.get("content", ""),
                )

                if score > 0.6:
                    contradictions.append({
                        "memory_a": mem_a["memory_id"],
                        "memory_b": mem_b["memory_id"],
                        "content_a": mem_a.get("content", "")[:80],
                        "content_b": mem_b.get("content", "")[:80],
                        "contradiction_score": round(score, 2),
                        "shared_topics": [topic],
                        "action": "needs_review",
                    })

        if contradictions:
            logger.info(f"⚡ 检测到 {len(contradictions)} 组矛盾记忆")
            for c in contradictions:
                self.store.insert_link(
                    source_id=c["memory_a"],
                    target_id=c["memory_b"],
                    link_type="causal.contradicts",
                    weight=0.3,
                    reason=f"矛盾检测 (score={c['contradiction_score']})",
                )

        return contradictions

    def detect_outdated(self, window_days: int = 30) -> list[dict]:
        """
        检测过时记忆。

        修复 (P0): 限制扫描量 100 条，按主题桶内时间排序检测替代关系
        """
        now = int(time.time())
        window_start = now - window_days * 86400

        memories = self.store.query(limit=100, time_from=window_start)
        notes = [m for m in memories if m.get("nature_id") == "D05"]

        # 按主题分组
        by_topic: dict[str, list[dict]] = {}
        for mem in notes:
            for topic in self._get_primary_topics(mem):
                top = topic.split(".")[0]
                if top not in by_topic:
                    by_topic[top] = []
                by_topic[top].append(mem)

        outdated = []

        for topic, group in by_topic.items():
            if len(group) < 2:
                continue

            # 按时间排序
            group.sort(key=lambda m: m.get("time_ts", 0))

            # 最新的可能替代旧的
            newest = group[-1]
            for old in group[:-1]:
                age_gap_days = (newest.get("time_ts", 0) - old.get("time_ts", 0)) / 86400

                # 时间差距足够大 + 旧的不是 high 重要度
                if age_gap_days >= 7 and old.get("importance") != "high":
                    # 检查内容是否有更新信号
                    if self._is_updated_content(old.get("content", ""), newest.get("content", "")):
                        outdated.append({
                            "outdated_id": old["memory_id"],
                            "updated_id": newest["memory_id"],
                            "outdated_content": old.get("content", "")[:60],
                            "updated_content": newest.get("content", "")[:60],
                            "age_gap_days": round(age_gap_days, 1),
                            "topic": topic,
                            "action": "mark_outdated",
                        })

                        # 标记过时关联
                        self.store.insert_link(
                            source_id=old["memory_id"],
                            target_id=newest["memory_id"],
                            link_type="outdated_by",
                            weight=0.2,
                            reason=f"被 {age_gap_days:.0f} 天后的新信息替代",
                        )

        if outdated:
            logger.info(f"📅 检测到 {len(outdated)} 条过时记忆")

        return outdated

    def heal_importance_consistency(self) -> dict:
        """
        修复重要度一致性。

        规则：
        - 关联记忆中，如果一个是 high，另一个是 low → 考虑同步
        - 同主题下的"决策"记忆应为 high

        Fix (P1): 原来直接 UPDATE 绕过事务 + 无缓存失效 + 无审计日志。
        修复后：通过 store.transaction() 写入 + 调用 _invalidate_cache + 记录审计日志。
        """
        healed = []

        # 找 importance 差异过大的关联对
        links = self.store.conn.execute(
            """SELECT * FROM memory_links
               WHERE link_type IN ('temporal', 'topic', 'causal.decision_based_on')"""
        ).fetchall()

        for link in links:
            mem_a = self.store.get_memory(link["source_id"])
            mem_b = self.store.get_memory(link["target_id"])

            if not mem_a or not mem_b:
                continue

            imp_a = mem_a.get("importance", "medium")
            imp_b = mem_b.get("importance", "medium")

            # high 和 low 差异大
            if {imp_a, imp_b} == {"high", "low"}:
                # 提升 low 为 medium
                low_mem = mem_a if imp_a == "low" else mem_b
                try:
                    with self.store.transaction() as conn:
                        conn.execute(
                            "UPDATE memories SET importance = 'medium' WHERE memory_id = ?",
                            (low_mem["memory_id"],),
                        )
                    # 事务提交后失效缓存
                    self.store._invalidate_cache()
                    healed.append({
                        "memory_id": low_mem["memory_id"],
                        "from": "low",
                        "to": "medium",
                        "reason": f"关联了 {imp_a} 级记忆",
                    })
                    logger.info(
                        f"重要度修复: {low_mem['memory_id']} low→medium "
                        f"(关联了 {imp_a} 级记忆 {link['source_id']}↔{link['target_id']})"
                    )
                except Exception as e:
                    logger.error(f"重要度修复失败 {low_mem['memory_id']}: {e}")

        return {"healed": healed, "count": len(healed)}

    def full_scan(self) -> dict:
        """
        执行完整的自我修复扫描。

        返回:
        {
            "contradictions": [...],
            "outdated": [...],
            "importance_healed": int,
            "total_issues": int,
        }
        """
        contradictions = self.detect_contradictions()
        outdated = self.detect_outdated()
        importance_result = self.heal_importance_consistency()

        total = len(contradictions) + len(outdated) + importance_result["count"]

        if total > 0:
            logger.info(f"🔧 自我修复扫描完成: {total} 个问题")

        return {
            "contradictions": contradictions,
            "outdated": outdated,
            "importance_healed": importance_result["count"],
            "total_issues": total,
        }

    def run(self) -> dict:
        """别名，等价于 full_scan()，供 maintain() 调用"""
        return self.full_scan()

    # ── 内部方法 ────────────────────────────────────────

    def _get_primary_topics(self, mem: dict) -> set[str]:
        topics = mem.get("topics", [])
        result = set()
        for t in topics:
            if isinstance(t, dict):
                result.add(t.get("code", ""))
            else:
                result.add(t)
        return {t for t in result if t}

    def _contradiction_score(self, text_a: str, text_b: str) -> float:
        """
        判断两段文本是否矛盾。

        v3 改进：接入语义向量 + 多信号融合
        1. 语义向量高相似 + 情感极性相反 → 高概率矛盾
        2. 语义向量低相似 → 不可能矛盾（不同话题）
        3. 多信号融合：结论词对立、选择对比、否定翻转、数值冲突
        4. 补充性语句降权
        """
        a_lower = text_a.lower().strip()
        b_lower = text_b.lower().strip()

        # 空文本或极短文本不判矛盾
        if len(a_lower) < 5 or len(b_lower) < 5:
            return 0.0

        # ── 0. 语义向量相似度（核心改进）─────────────
        # 如果有 embedding_store，先用语义向量判断话题相关性
        semantic_sim = None
        if self.embedding_store:
            try:
                vec_a = self.embedding_store._encode(text_a)
                vec_b = self.embedding_store._encode(text_b)
                # 余弦相似度
                dot = sum(x * y for x, y in zip(vec_a, vec_b))
                norm_a = sum(x * x for x in vec_a) ** 0.5
                norm_b = sum(x * x for x in vec_b) ** 0.5
                if norm_a > 0 and norm_b > 0:
                    semantic_sim = dot / (norm_a * norm_b)
            except Exception as e:
                logger.warning("self_healing: %s", e)

        # 降级：关键词实体重叠
        if semantic_sim is None:
            a_topics = self._extract_entities(a_lower)
            b_topics = self._extract_entities(b_lower)
            if a_topics and b_topics:
                topic_overlap = len(a_topics & b_topics) / max(len(a_topics | b_topics), 1)
                if topic_overlap < 0.15:
                    return 0.0
        else:
            # 语义相似度太低 → 话题不同，不可能矛盾
            if semantic_sim < 0.25:
                return 0.0

        score = 0.0

        # ── 1. 语义高相似 + 情感极性相反 → 强矛盾信号 ──
        if semantic_sim is not None and semantic_sim > 0.7:
            # 语义高度相似的两段话，如果情感极性相反，大概率是矛盾
            polarity_signal = self._polarity_opposite(text_a, text_b)
            if polarity_signal:
                score += 0.5  # 强信号
            else:
                score += 0.1  # 高相似本身是弱信号

        # ── 2. 结论词对立 ─────────────────────────────
        POSITIVE_SIGNALS = [
            "更好", "最好", "推荐", "好用", "优秀", "高效", "可靠", "稳定",
            "适合", "首选", "值得", "成功", "解决了", "效果好", "表现好",
            "better", "best", "recommend", "efficient", "reliable", "stable",
            "outperform", "superior", "excellent",
        ]
        NEGATIVE_SIGNALS = [
            "更差", "最差", "不推荐", "难用", "差", "低效", "不稳定", "不适合",
            "不值", "失败", "没解决", "效果差", "表现差", "问题多", "坑",
            "worse", "worst", "avoid", "inefficient", "unstable", "problematic",
            "inferior", "terrible", "bug",
        ]

        a_pos = sum(1 for w in POSITIVE_SIGNALS if w in a_lower)
        a_neg = sum(1 for w in NEGATIVE_SIGNALS if w in a_lower)
        b_pos = sum(1 for w in POSITIVE_SIGNALS if w in b_lower)
        b_neg = sum(1 for w in NEGATIVE_SIGNALS if w in b_lower)

        if (a_pos > 0 and b_neg > 0) or (a_neg > 0 and b_pos > 0):
            score += 0.35
            if a_pos >= 2 or a_neg >= 2:
                score += 0.1
            if b_pos >= 2 or b_neg >= 2:
                score += 0.1

        # ── 3. 选择对比矛盾 ───────────────────────────
        choose_patterns = [
            r"(?:选|选择|用|采用|决定用|用了|推荐)\s*(\S{1,10})",
            r"(?:use|choose|pick|select|recommend)\s+(\S{1,20})",
        ]
        a_choices = set()
        b_choices = set()
        for pat in choose_patterns:
            for m in re.finditer(pat, a_lower):
                a_choices.add(m.group(1))
            for m in re.finditer(pat, b_lower):
                b_choices.add(m.group(1))

        if a_choices and b_choices:
            if not a_choices & b_choices:
                # 有语义相似度就用，没有就用关键词
                if semantic_sim is not None:
                    if semantic_sim > 0.5:
                        score += 0.3
                else:
                    a_topics = self._extract_entities(a_lower)
                    b_topics = self._extract_entities(b_lower)
                    if a_topics & b_topics:
                        score += 0.3

        # ── 4. 否定翻转 ─────────────────────────────
        a_denied = re.sub(r"(不|没|非|无|别|未|never|not|no)\s*", "", a_lower)
        b_denied = re.sub(r"(不|没|非|无|别|未|never|not|no)\s*", "", b_lower)
        if a_denied != a_lower and b_denied != b_lower:
            similarity = self._text_similarity(a_denied, b_denied)
            if similarity > 0.5:
                score += 0.25

        # ── 5. 数值冲突 ─────────────────────────────
        a_nums = set(re.findall(r"\d+\.?\d*", a_lower))
        b_nums = set(re.findall(r"\d+\.?\d*", b_lower))
        if a_nums and b_nums and not a_nums & b_nums:
            if semantic_sim is not None:
                if semantic_sim > 0.4:
                    score += 0.15
            else:
                a_topics = self._extract_entities(a_lower)
                b_topics = self._extract_entities(b_lower)
                if a_topics & b_topics:
                    score += 0.15

        # ── 6. 排除"补充"而非"矛盾"的情况 ───────────
        COMPLEMENT_SIGNALS = [
            "另外", "此外", "补充", "还有", "顺便", "也", "同时",
            "additionally", "also", "moreover", "furthermore",
        ]
        has_complement = any(w in a_lower or w in b_lower for w in COMPLEMENT_SIGNALS)
        if has_complement and score < 0.5:
            score *= 0.5

        return min(1.0, score)

    @staticmethod
    def _polarity_opposite(text_a: str, text_b: str) -> bool:
        """判断两段文本的情感极性是否相反"""
        POS = {"好", "优秀", "推荐", "适合", "高效", "可靠", "稳定", "值得", "成功", "解决了",
               "better", "best", "recommend", "good", "great", "excellent", "reliable", "stable"}
        NEG = {"差", "不好", "难用", "坑", "失败", "不稳定", "不推荐", "不适合", "低效", "问题多",
               "worse", "worst", "bad", "terrible", "unstable", "inefficient", "problematic"}

        a_lower = text_a.lower()
        b_lower = text_b.lower()

        a_has_pos = any(w in a_lower for w in POS)
        a_has_neg = any(w in a_lower for w in NEG)
        b_has_pos = any(w in b_lower for w in POS)
        b_has_neg = any(w in b_lower for w in NEG)

        # A 纯正 B 纯负，或 A 纯负 B 纯正
        a_pure_pos = a_has_pos and not a_has_neg
        a_pure_neg = a_has_neg and not a_has_pos
        b_pure_pos = b_has_pos and not b_has_neg
        b_pure_neg = b_has_neg and not b_has_pos
        return (a_pure_pos and b_pure_neg) or (a_pure_neg and b_pure_pos)

    @staticmethod
    def _extract_entities(text: str) -> set[str]:
        """提取文本中的实体/主题词（简单实现）"""
        # 英文词
        en = set(re.findall(r"[a-zA-Z][a-zA-Z0-9_]{2,}", text.lower()))
        # 中文 2-4 字词
        cn = set(re.findall(r"[\u4e00-\u9fff]{2,4}", text))
        # 去停用词
        stop = {"的", "了", "是", "在", "和", "就", "不", "也", "都", "一", "一个",
                "the", "and", "for", "are", "but", "not", "you", "all", "can"}
        return (en | cn) - stop

    @staticmethod
    def _text_similarity(a: str, b: str) -> float:
        """快速文本相似度（Jaccard bigram）"""
        def bigrams(s):
            return set(s[i:i+2] for i in range(len(s) - 1))
        ba, bb = bigrams(a), bigrams(b)
        if not ba or not bb:
            return 0.0
        return len(ba & bb) / len(ba | bb)

    def _is_updated_content(self, old_content: str, new_content: str) -> bool:
        """检查新内容是否可能是旧内容的更新版"""
        old_lower = old_content.lower()
        new_lower = new_content.lower()

        # 更新信号词
        update_signals = ["更新", "改为", "现在", "改成", "最新", "修正", "修正为", "updated", "changed", "now"]

        has_signal = any(w in new_lower for w in update_signals)

        # 共享关键词多 → 可能是同一话题的更新
        old_words = set(old_lower.split())
        new_words = set(new_lower.split())
        if old_words and new_words:
            overlap = len(old_words & new_words) / min(len(old_words), len(new_words))
            return has_signal and overlap > 0.3

        return has_signal

    def get_stats(self) -> dict:
        """自我修复统计"""
        contradictions = self.store.conn.execute(
            "SELECT COUNT(*) as cnt FROM memory_links WHERE link_type = 'causal.contradicts'"
        ).fetchone()

        outdated = self.store.conn.execute(
            "SELECT COUNT(*) as cnt FROM memory_links WHERE link_type = 'outdated_by'"
        ).fetchone()

        return {
            "contradiction_links": contradictions["cnt"] if contradictions else 0,
            "outdated_links": outdated["cnt"] if outdated else 0,
        }
