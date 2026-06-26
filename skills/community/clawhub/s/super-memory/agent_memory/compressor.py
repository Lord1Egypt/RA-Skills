"""
compressor.py - LLM 驱动的记忆压缩器
将衰减的同主题记忆压缩为结构化摘要，减少存储冗余

Fix (P1 #7): 压缩质量安全网
- 压缩前后关键信息保留率检查
- 压缩质量自动评估
- 压缩失败自动回滚
"""

from __future__ import annotations

import json
import logging
import re
import time
from datetime import datetime

logger = logging.getLogger(__name__)


class MemoryCompressor:
    """
    记忆压缩流程：
    1. 找出需要压缩的记忆（decay 状态的 medium/low）
    2. 按主题分组
    3. 调用 LLM 生成压缩摘要
    4. 写入新的聚合记忆，标记 is_aggregated=True
    5. 原始记忆标记为已压缩（软删除）

    LLM 调用签名: llm_fn(prompt: str) -> str
    """

    COMPRESS_PROMPT = """你是一个记忆压缩器。请将以下多条对话记忆压缩为一条结构化摘要。

主题: {topic}
记忆条数: {count}
时间跨度: {time_range}

原始记忆:
{memories}

要求：
1. 保留所有关键信息：决策、结论、事实、待办
2. 丢弃闲聊、重复、过渡性内容
3. 输出简洁的结构化摘要，不超过 300 字
4. 标注哪些是"关键决策"、"事实记录"、"待办事项"

输出格式：
## 摘要
[一段话概括核心内容]

## 关键决策
- [决策1]
- [决策2]

## 事实记录
- [事实1]

## 待办事项
- [待办1]
"""

    # 压缩策略
    BATCH_SIZE = 10           # 每批最多压缩几条
    MIN_GROUP_SIZE = 3        # 至少几条才触发压缩
    MAX_CONTENT_LENGTH = 500  # 每条记忆截断长度

    MAX_LLM_CALLS_PER_SESSION = 10  # 每次 compress 会话的最大 LLM 调用次数

    def __init__(self, store, encoder=None, llm_fn=None):
        """
        store: MemoryStore 实例
        encoder: DimensionEncoder 实例
        llm_fn: LLM 调用函数，签名 fn(prompt: str) -> str
                如果为 None，使用启发式 fallback（保留关键句）
        """
        self.store = store
        self.encoder = encoder
        self.llm_fn = llm_fn or self._heuristic_compress
        self._llm_call_count: int = 0

    def compress(
        self,
        topic_code: str = None,
        importance: str = None,
        dry_run: bool = False,
    ) -> dict:
        """
        执行压缩操作。

        参数:
            topic_code: 只压缩指定主题（None=全部）
            importance: 只压缩指定重要度（None=全部可压缩的）
            dry_run: True=只分析不执行

        返回:
        {
            "total_candidates": int,
            "groups": [{"topic": str, "count": int, "memories": [...]}],
            "compressed": [{"summary_id": str, "topic": str, "source_count": int}],
            "dry_run": bool,
        }
        """
        if not self.llm_fn:
            return {"error": "Compression unavailable", "llm_available": False}

        self._llm_call_count = 0

        # 1. 找出可压缩的记忆
        candidates = self._find_candidates(topic_code, importance)
        if not candidates:
            return {"total_candidates": 0, "groups": [], "compressed": [], "dry_run": dry_run}

        # 2. 按主题分组
        groups = self._group_by_topic(candidates)

        # 3. 过滤太小的组
        groups = [g for g in groups if len(g["memories"]) >= self.MIN_GROUP_SIZE]

        if dry_run:
            return {
                "total_candidates": len(candidates),
                "groups": groups,
                "compressed": [],
                "dry_run": True,
            }

        # 4. 逐组压缩
        compressed = []
        for group in groups:
            result = self._compress_group(group)
            if result:
                compressed.append(result)

        return {
            "total_candidates": len(candidates),
            "groups": groups,
            "compressed": compressed,
            "dry_run": False,
        }

    def _find_candidates(self, topic_code: str = None, importance: str = None) -> list[dict]:
        """
        找出需要压缩的记忆。
        条件：importance=medium 且 age>=180天，或 importance=low 且 age>=30天
        """
        now = time.time()
        candidates = []

        # 查询 medium 和 low 的记忆
        for imp in [importance] if importance else ["medium", "low"]:
            memories = self.store.query(importance=imp, limit=500, topic_code=topic_code)
            for mem in memories:
                if mem.get("is_aggregated"):
                    continue  # 跳过已聚合的
                age_days = (now - mem.get("time_ts", now)) / 86400
                if imp == "medium" and age_days >= 180:
                    candidates.append(mem)
                elif imp == "low" and age_days >= 30:
                    candidates.append(mem)

        return candidates

    def _group_by_topic(self, memories: list[dict]) -> list[dict]:
        """按主主题分组"""
        topic_groups: dict[str, list[dict]] = {}

        for mem in memories:
            topics = mem.get("topics", [])
            primary = None
            for t in topics:
                if isinstance(t, dict) and t.get("is_primary"):
                    primary = t["code"]
                    break
                elif isinstance(t, str):
                    primary = t
                    break
            if not primary:
                primary = "misc"

            # 归到一级主题下（减少碎片化）
            top_topic = primary.split(".")[0]
            if top_topic not in topic_groups:
                topic_groups[top_topic] = []
            topic_groups[top_topic].append(mem)

        groups = []
        for topic, mems in topic_groups.items():
            # 按时间排序
            mems.sort(key=lambda m: m.get("time_ts", 0))
            time_range = self._format_time_range(mems)
            groups.append({
                "topic": topic,
                "count": len(mems),
                "time_range": time_range,
                "memories": mems,
            })

        # 大的组优先
        groups.sort(key=lambda g: -g["count"])
        return groups

    # ── Fix #7: 压缩质量检查 ──────────────────────────────

    def _extract_key_facts(self, text: str) -> list[str]:
        """从文本中提取关键信息片段（决策、数字、名称等）"""
        facts = []
        for line in text.split("\n"):
            line = line.strip()
            if len(line) < 5:
                continue
            # 决策/结论类
            if any(kw in line for kw in ["决定", "选择", "采用", "结论", "发现", "修复", "解决", "配置", "部署"]):
                facts.append(line[:80])
            # 含具体数据的
            elif re.search(r'\d+\.\d+|\d+%|port\s*\d+|v\d+\.\d+', line, re.IGNORECASE):
                facts.append(line[:80])
            # 含文件路径/类名/方法名的
            elif re.search(r'[\w/]+\.(py|js|ts|json|yaml|sql)\b|[A-Z]\w+\.\w+', line):
                facts.append(line[:80])
        return facts

    def _compute_retention_score(self, original_memories: list[dict], summary: str) -> float:
        """
        计算压缩信息保留率。

        策略：从原始记忆中提取关键片段（决策词、数据、实体），
        检查这些片段在压缩摘要中是否被保留。

        返回: 0.0 ~ 1.0 的保留率
        """
        # 从所有原始记忆中提取关键事实
        all_content = "\n".join(m.get("content", "") for m in original_memories)
        key_facts = self._extract_key_facts(all_content)

        if not key_facts:
            return 1.0  # 没有可提取的关键信息，默认通过

        # 检查关键片段是否出现在摘要中
        summary_lower = summary.lower()
        retained = 0
        for fact in key_facts:
            # 取事实中的关键词（去停用词后）
            keywords = [w for w in re.findall(r'[\w\u4e00-\u9fff]+', fact.lower()) if len(w) >= 2]
            # 至少 50% 的关键词在摘要中出现
            if keywords:
                hit_count = sum(1 for kw in keywords if kw in summary_lower)
                if hit_count / len(keywords) >= 0.5:
                    retained += 1

        return retained / len(key_facts) if key_facts else 1.0

    MIN_RETENTION_SCORE = 0.6  # 最低保留率阈值

    def _validate_compression(self, original_memories: list[dict], summary: str) -> dict:
        """
        Fix #7: 验证压缩质量，不合格则拒绝。

        返回: {"passed": bool, "retention_score": float, "issues": list[str]}
        """
        issues = []

        # 1. 保留率检查
        retention = self._compute_retention_score(original_memories, summary)
        if retention < self.MIN_RETENTION_SCORE:
            issues.append(f"信息保留率过低: {retention:.0%} (最低要求 {self.MIN_RETENTION_SCORE:.0%})")

        # 2. 摘要不应为空或过短
        if len(summary.strip()) < 20:
            issues.append(f"摘要过短: {len(summary.strip())} 字符")

        # 3. 摘要不应只是原始内容的简单拼接
        total_original = sum(len(m.get("content", "")) for m in original_memories)
        if total_original > 0 and len(summary) > total_original * 0.9:
            issues.append(f"摘要未有效压缩: {len(summary)}/{total_original} 字符")

        # 4. 摘要不应全是通用模板内容
        template_phrases = ["多条记忆的自动压缩摘要", "压缩摘要", "无内容"]
        if any(phrase in summary and len(summary) < 100 for phrase in template_phrases):
            issues.append("摘要内容过于模板化")

        return {
            "passed": len(issues) == 0,
            "retention_score": round(retention, 2),
            "issues": issues,
        }

    def _rollback_compression(self, summary_id: str, original_memories: list[dict]):
        """
        Fix #7: 压缩失败回滚 — 删除摘要记录，恢复原始记忆标记。
        """
        try:
            # 删除摘要记忆及其链接
            self.store.conn.execute("DELETE FROM memory_links WHERE source_id = ?", (summary_id,))
            self.store.conn.execute("DELETE FROM memory_topics WHERE memory_id = ?", (summary_id,))
            self.store.conn.execute("DELETE FROM memories WHERE memory_id = ?", (summary_id,))
            self.store.conn.commit()

            # 移除原始记忆的 compressed_to 链接
            for mem in original_memories:
                self.store.conn.execute(
                    "DELETE FROM memory_links WHERE source_id = ? AND target_id = ? AND link_type = 'compressed_to'",
                    (mem["memory_id"], summary_id),
                )
            self.store.conn.commit()
            logger.warning(f"🔄 压缩回滚完成: {summary_id}")
        except Exception as e:
            logger.error(f"压缩回滚失败: {e}")

    # ── 压缩主流程 ────────────────────────────────────

    def _compress_group(self, group: dict) -> dict | None:
        """压缩一个主题组（含质量验证 + 自动回滚 + LLM 预算追踪）"""
        if self._llm_call_count >= self.MAX_LLM_CALLS_PER_SESSION:
            logger.info(
                "已达到LLM调用预算上限(%d次)，跳过剩余压缩",
                self.MAX_LLM_CALLS_PER_SESSION,
            )
            return None

        topic = group["topic"]
        memories = group["memories"][:self.BATCH_SIZE]  # 限制每批数量
        time_range = group["time_range"]

        # 构建记忆文本
        mem_texts = []
        for i, mem in enumerate(memories):
            content = mem.get("content", "")[:self.MAX_CONTENT_LENGTH]
            ts = mem.get("time_ts", 0)
            dt = datetime.fromtimestamp(ts).strftime("%m-%d %H:%M") if ts else "?"
            mem_texts.append(f"[{i+1}] ({dt}) {content}")

        memories_block = "\n\n".join(mem_texts)

        prompt = self.COMPRESS_PROMPT.format(
            topic=topic,
            count=len(memories),
            time_range=time_range,
            memories=memories_block,
        )

        try:
            summary_text = self.llm_fn(prompt)
            self._llm_call_count += 1
        except Exception as e:
            logger.error(f"LLM compression failed for topic {topic}: {e}")
            return None

        # Fix #7: 压缩质量验证
        validation = self._validate_compression(memories, summary_text)
        if not validation["passed"]:
            logger.warning(
                f"⚠️ 压缩质量不合格 [{topic}]: {validation['issues']} "
                f"(保留率={validation['retention_score']:.0%})"
            )
            return None

        # 生成压缩记忆的 memory_id
        import hashlib
        first_ts = memories[0].get("time_ts", int(time.time()))
        time_id = self.encoder.encode_time(first_ts, precision="second") if self.encoder else f"T{first_ts}"
        person_id = memories[0].get("person_id", "P01")
        summary_id = f"{time_id}_{person_id}_{topic.replace('.', '_')}_compressed"

        # 写入聚合记忆
        self.store.insert_memory(
            memory_id=summary_id,
            time_id=time_id,
            time_ts=int(time.time()),
            person_id=person_id,
            nature_id="D09",  # retro/回溯
            content=summary_text,
            content_hash=hashlib.sha256(summary_text.encode()).hexdigest(),
            topics=[topic],
            importance=memories[0].get("importance", "medium"),
            is_aggregated=True,
            source_count=len(memories),
        )

        # 建立关联：压缩记忆 → 原始记忆
        for mem in memories:
            self.store.insert_link(
                source_id=summary_id,
                target_id=mem["memory_id"],
                link_type="compressed_from",
                weight=0.5,
                reason=f"压缩自 {len(memories)} 条原始记忆",
            )

        # 原始记忆标记为已压缩（通过 content 追加标记）
        # 注意：不删除，保留用于溯源
        for mem in memories:
            self._mark_compressed(mem["memory_id"], summary_id)

        # 迁移原始记忆的因果/主题关联到压缩摘要
        self._migrate_links_to_summary(summary_id, memories)

        # Fix #7: 写入后二次验证（检查数据库中摘要是否完整写入）
        try:
            written = self.store.get_memory(summary_id)
            if not written or not written.get("content"):
                logger.error(f"压缩写入验证失败: {summary_id} 未找到")
                self._rollback_compression(summary_id, memories)
                return None
        except Exception as e:
            logger.error(f"压缩写入验证异常: {e}")
            self._rollback_compression(summary_id, memories)
            return None

        logger.info(
            f"📦 压缩完成: {topic} ({len(memories)}条 → 1条摘要, "
            f"保留率={validation['retention_score']:.0%})"
        )
        return {
            "summary_id": summary_id,
            "topic": topic,
            "source_count": len(memories),
            "time_range": time_range,
            "retention_score": validation["retention_score"],
        }

    def _mark_compressed(self, memory_id: str, summary_id: str):
        """标记原始记忆为已压缩（添加关联）"""
        self.store.insert_link(
            source_id=memory_id,
            target_id=summary_id,
            link_type="compressed_to",
            weight=0.3,
            reason="已压缩为摘要",
        )

    def _migrate_links_to_summary(self, summary_id: str, original_memories: list[dict]):
        """
        修复 (P2): 将原始记忆的因果/主题关联迁移到压缩摘要。

        问题：压缩后，其他记忆通过 causal/temporal/topic 链接指向原始记忆，
        但原始记忆已经是碎片，导致图谱查询断裂。

        解决：将原始记忆的入向链接（被其他记忆引用）复制一份指向摘要。
        原始链接保留（溯源用），新增的链接标记为 migrated_for_compression。
        """
        original_ids = {m["memory_id"] for m in original_memories}
        migrated = 0

        for mem in original_memories:
            mid = mem["memory_id"]
            # 查找指向这条原始记忆的链接（入向）
            inbound_links = self.store.conn.execute(
                """SELECT * FROM memory_links
                   WHERE target_id = ?
                   AND link_type IN ('causal.decision_based_on', 'causal.led_to',
                                     'causal.supports', 'causal.timeline_before',
                                     'temporal', 'topic')""",
                (mid,),
            ).fetchall()

            for link in inbound_links:
                source_id = link["source_id"]
                # 跳过：如果源也在被压缩的组内
                if source_id in original_ids:
                    continue
                # 跳过：如果已经有一条从 source 到 summary 的同类型链接
                existing = self.store.conn.execute(
                    """SELECT 1 FROM memory_links
                       WHERE source_id = ? AND target_id = ? AND link_type = ?""",
                    (source_id, summary_id, link["link_type"]),
                ).fetchone()
                if existing:
                    continue

                try:
                    self.store.insert_link(
                        source_id=source_id,
                        target_id=summary_id,
                        link_type=link["link_type"],
                        weight=link["weight"] * 0.8,
                        reason=f"migrated from compressed {mid[:12]}",
                    )
                    migrated += 1
                except Exception as e:
                    logger.warning("compressor: %s", e)

        if migrated > 0:
            logger.debug(f"📦 关联迁移: {migrated} 条链接 → 摘要 {summary_id[:12]}")

    def _format_time_range(self, memories: list[dict]) -> str:
        """格式化时间范围"""
        if not memories:
            return "?"
        timestamps = [m.get("time_ts", 0) for m in memories if m.get("time_ts")]
        if not timestamps:
            return "?"
        earliest = datetime.fromtimestamp(min(timestamps)).strftime("%Y-%m-%d")
        latest = datetime.fromtimestamp(max(timestamps)).strftime("%Y-%m-%d")
        if earliest == latest:
            return earliest
        return f"{earliest} ~ {latest}"

    def get_compression_stats(self) -> dict:
        """获取压缩统计"""
        # 查询已压缩的记忆数
        rows = self.store.conn.execute(
            """SELECT COUNT(DISTINCT m.memory_id) as cnt
               FROM memories m
               WHERE m.is_aggregated = 1"""
        ).fetchone()

        aggregated_count = rows["cnt"] if rows else 0

        # 查询被压缩的原始记忆数
        rows2 = self.store.conn.execute(
            """SELECT COUNT(*) as cnt
               FROM memory_links
               WHERE link_type = 'compressed_to'"""
        ).fetchone()
        compressed_source_count = rows2["cnt"] if rows2 else 0

        # 查询候选压缩数
        candidates = self._find_candidates()
        pending_count = len(candidates)

        return {
            "aggregated_summaries": aggregated_count,
            "compressed_sources": compressed_source_count,
            "pending_compression": pending_count,
            "llm_available": self.llm_fn is not None and self.llm_fn is not self._heuristic_compress,
            "has_fallback": True,
        }

    def generate_compression_report(self) -> str:
        """生成压缩状态报告"""
        stats = self.get_compression_stats()
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")

        lines = [
            "# 📦 记忆压缩报告",
            "",
            f"**生成时间**: {now_str}",
            f"**LLM 可用**: {'✅' if stats['llm_available'] else '⚠️ 启发式模式'}",
            "",
            "## 统计",
            "",
            f"- 聚合摘要数: **{stats['aggregated_summaries']}**",
            f"- 已压缩原始记忆: **{stats['compressed_sources']}**",
            f"- 待压缩候选: **{stats['pending_compression']}**",
        ]

        if stats["pending_compression"] > 0:
            lines.extend([
                "",
                "## ⚠️ 待压缩主题分布",
                "",
            ])
            candidates = self._find_candidates()
            groups = self._group_by_topic(candidates)
            for g in groups:
                lines.append(f"- **{g['topic']}**: {g['count']} 条 ({g['time_range']})")

        return "\n".join(lines)

    @staticmethod
    def _heuristic_compress(prompt: str) -> str:
        """
        无 LLM 时的启发式压缩 fallback。

        策略：从原始记忆中提取关键句（含决策词/数据/结论），拼接为摘要。
        效果不如 LLM，但保证压缩功能可用，不阻塞流程。
        """
        # 从 prompt 中提取原始记忆块
        lines = prompt.split("\n")
        mem_lines = []
        in_memories = False
        for line in lines:
            if line.strip().startswith("[") and "]" in line:
                in_memories = True
            if in_memories:
                mem_lines.append(line)

        if not mem_lines:
            # 兜底：直接取 prompt 最后部分
            mem_lines = lines[-10:]

        # 关键句提取
        decision_keywords = [
            "决定", "选择", "采用", "用", "改为", "放弃", "推荐",
            "结论", "总结", "关键", "重要", "发现", "踩坑", "注意",
            "配置", "设置", "部署", "发布", "修复", "解决",
        ]

        key_sentences = []
        for line in mem_lines:
            line = line.strip()
            if len(line) < 5:
                continue
            # 包含决策/数据关键词的行优先保留
            if any(kw in line for kw in decision_keywords):
                key_sentences.append(line)
            # 包含数字/代码的行也保留
            elif any(c.isdigit() for c in line) and len(line) > 10:
                key_sentences.append(line)

        # 如果关键句太少，补充最长的几行
        if len(key_sentences) < 2:
            sorted_by_len = sorted(mem_lines, key=lambda l: -len(l.strip()))
            for line in sorted_by_len[:5]:
                stripped = line.strip()
                if stripped and stripped not in key_sentences and len(stripped) > 10:
                    key_sentences.append(stripped)

        # 构建摘要
        summary_lines = ["## 摘要"]
        if key_sentences:
            summary_lines.append("、".join(s[:60] for s in key_sentences[:5]))
        else:
            summary_lines.append("多条记忆的自动压缩摘要")

        summary_lines.extend(["", "## 关键内容"])
        for s in key_sentences[:8]:
            # 清理前缀标记
            clean = s
            if clean.startswith("[") and "]" in clean:
                clean = clean.split("]", 1)[-1].strip()
            if clean:
                summary_lines.append(f"- {clean[:100]}")

        return "\n".join(summary_lines)

    def smart_compress(
        self,
        embedding_store=None,
        topic_code: str = None,
    ) -> dict:
        """
        智能压缩：用向量聚类区分核心记忆 vs 边缘记忆。

        核心记忆（聚类中心）→ 保留原文
        边缘记忆（远离中心）→ 压缩为摘要，可物理删除

        参数:
            embedding_store: EmbeddingStore 实例
            topic_code: 指定主题

        返回:
        {
            "topic": str,
            "core_memories": [memory_ids],    # 保留的核心记忆
            "edge_memories": [memory_ids],    # 被压缩的边缘记忆
            "summary_id": str,
            "saved_tokens": int,              # 预估节省的 token
        }
        """
        if not self.llm_fn:
            return {"error": "LLM function not set"}

        candidates = self._find_candidates(topic_code=topic_code)
        if len(candidates) < self.MIN_GROUP_SIZE:
            return {"error": f"候选记忆不足 {self.MIN_GROUP_SIZE} 条"}

        groups = self._group_by_topic(candidates)
        results = []

        for group in groups:
            if len(group["memories"]) < self.MIN_GROUP_SIZE:
                continue

            # 向量聚类：找核心 vs 边缘
            core, edge = self._cluster_core_edge(
                group["memories"],
                embedding_store,
            )

            if not edge:
                # 没有边缘记忆，跳过
                continue

            # 只压缩边缘记忆
            edge_group = {
                "topic": group["topic"],
                "count": len(edge),
                "time_range": self._format_time_range(edge),
                "memories": edge,
            }
            compress_result = self._compress_group(edge_group)

            if compress_result:
                compress_result["core_memories"] = [m["memory_id"] for m in core]
                compress_result["edge_memories"] = [m["memory_id"] for m in edge]
                compress_result["saved_tokens"] = sum(
                    len(m.get("content", "")) // 2 for m in edge
                )
                results.append(compress_result)

        if not results:
            return {"error": "无有效压缩"}

        return results[0] if len(results) == 1 else {"multi_topic": results}

    def _cluster_core_edge(
        self,
        memories: list[dict],
        embedding_store=None,
    ) -> tuple[list[dict], list[dict]]:
        """
        将记忆分为核心和边缘。

        有 embedding 时：用向量聚类
        无 embedding 时：用重要度 + 时间启发式
        """
        if not embedding_store or not memories:
            # 启发式：high 重要度或最新的是核心
            sorted_mems = sorted(
                memories,
                key=lambda m: (
                    0 if m.get("importance") == "high" else 1,
                    -(m.get("time_ts", 0)),
                ),
            )
            # 前 30% 为核心
            split = max(1, len(sorted_mems) // 3)
            return sorted_mems[:split], sorted_mems[split:]

        # 向量聚类：计算每个记忆到其他记忆的平均相似度
        # 平均相似度最高的 = 最核心的
        try:
            contents = [m.get("content", "") for m in memories]
            vectors = []
            for c in contents:
                try:
                    results = embedding_store.search(c, top_k=1)
                    # 用 search 的 score 作为与其他记忆关系的代理
                    vectors.append(results[0]["score"] if results else 0)
                except Exception:
                    vectors.append(0)

            # 按 score 排序（高 = 核心）
            indexed = list(enumerate(vectors))
            indexed.sort(key=lambda x: -x[1])

            split = max(1, len(memories) // 3)
            core_indices = {idx for idx, _ in indexed[:split]}
            edge_indices = {idx for idx, _ in indexed[split:]}

            core = [memories[i] for i in core_indices]
            edge = [memories[i] for i in edge_indices]
            return core, edge

        except Exception:
            # 降级到启发式
            return self._cluster_core_edge(memories, None)
