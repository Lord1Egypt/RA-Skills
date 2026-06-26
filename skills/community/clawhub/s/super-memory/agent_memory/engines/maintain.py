from __future__ import annotations

import os
import time
import logging
from enum import Enum
from dataclasses import dataclass, field
from typing import Optional, Callable

from ..decay import MemoryDecay
from ..memory_tier import MemoryTierManager, TierConfig, LRUCache
from ..memory_lifecycle import MemoryLifecycle
from ..hierarchical import HierarchicalMemory
from ..self_healing import SelfHealing
from ..compressor import MemoryCompressor
from ..correction_detector import CorrectionDetector
from .decay_policy import DecayPolicy, DEFAULT_DECAY_POLICY

logger = logging.getLogger(__name__)


class MemoryState(Enum):
    ACTIVE = "active"
    DORMANT = "dormant"
    ARCHIVED = "archived"
    SUPERSEDED = "superseded"
    MERGED = "merged"
    DEPRECATED = "deprecated"


@dataclass
class ConsolidationResult:
    merged_id: str
    source_ids: list[str] = field(default_factory=list)
    topic: str = ""
    source_count: int = 0
    retention_score: float = 0.0


_VALID_OPERATIONS = {"decay", "heal", "consolidate", "compress", "build_knowledge", "learn", "all"}


class MaintainEngine:
    """
    统一维护引擎 — 整合衰减、修复、合并、压缩

    三层衰减:  active → dormant → archived (会忘)
    语义取代:  新记忆覆盖旧记忆 (superseded)
    矛盾修复:  self_healing + correction_detector 联合检测与修正
    记忆合并:  相似记忆融合为摘要 (consolidation / 会成)
    压缩衰减:  衰减记忆压缩为结构化摘要
    """

    MAX_LLM_CALLS_PER_SESSION: int = 10  # 每次 maintain() 会话的最大 LLM 调用次数

    def __init__(
        self,
        store,
        encoder=None,
        embedding_store=None,
        llm_fn: Optional[Callable] = None,
        embedder=None,
        distill=None,
        quality=None,
        tier_config: Optional[TierConfig] = None,
        timeline=None,
        reactor=None,
        decay_policy: Optional[DecayPolicy] = None,
        knowledge_builder=None,
        feedback_learner=None,
    ):
        self.store = store
        self.encoder = encoder
        self.embedding_store = embedding_store
        self.llm_fn = llm_fn
        self.embedder = embedder
        self.timeline = timeline
        self.reactor = reactor
        self.decay_policy = decay_policy or DEFAULT_DECAY_POLICY
        self.knowledge_builder = knowledge_builder
        self.feedback_learner = feedback_learner

        self.decay = MemoryDecay(store, encoder=encoder, embedding_store=embedding_store)
        self.tier = MemoryTierManager(store=store, config=tier_config, distill=distill)
        self.lifecycle = MemoryLifecycle(store=store, embedder=embedder, llm_fn=llm_fn)
        self.hierarchy = HierarchicalMemory(store=store, quality=quality)
        self.healing = SelfHealing(store=store, embedding_store=embedding_store)
        self.correction = CorrectionDetector(embedding_store=embedding_store)
        self.compressor = MemoryCompressor(store=store, encoder=encoder, llm_fn=llm_fn)

        self._llm_call_count: int = 0

    def maintain(
        self,
        operations: Optional[list[str]] = None,
        dry_run: bool = False,
        agent_id: Optional[str] = None,
    ) -> dict:
        """
        执行维护操作列表。

        operations:
            'decay'       — 三层衰减: active → dormant → archived
            'heal'        — 矛盾检测 + 修正循环
            'consolidate' — 合并相似记忆
            'compress'    — 压缩衰减记忆
            'all'         — 依次执行以上全部

        dry_run: True 则只分析不写入
        agent_id: 限定作用域（可选）
        """
        if operations is None:
            operations = ["all"]

        invalid = set(operations) - _VALID_OPERATIONS
        if invalid:
            raise ValueError(f"未知操作: {invalid}，可选: {_VALID_OPERATIONS}")

        if "all" in operations:
            operations = ["decay", "heal", "consolidate", "compress", "build_knowledge", "learn"]

        self._llm_call_count = 0

        result: dict = {
            "operations": list(operations),
            "dry_run": dry_run,
            "started_at": int(time.time()),
            "decay": {},
            "heal": {},
            "consolidate": {},
            "compress": {},
            "build_knowledge": {},
            "learn": {},
        }

        for op in operations:
            if op == "decay":
                result["decay"] = self._run_decay(dry_run=dry_run, agent_id=agent_id)
            elif op == "heal":
                result["heal"] = self._run_heal(agent_id=agent_id)
            elif op == "consolidate":
                result["consolidate"] = self._run_consolidate(agent_id=agent_id)
            elif op == "compress":
                result["compress"] = self._run_compress(dry_run=dry_run)
            elif op == "build_knowledge":
                result["build_knowledge"] = self._run_build_knowledge(agent_id=agent_id)
            elif op == "learn":
                result["learn"] = self._run_learn(dry_run=dry_run)

        result["finished_at"] = int(time.time())
        result["elapsed_sec"] = result["finished_at"] - result["started_at"]

        # GDPR compliance: auto-purge soft-deleted PII if env var is set
        auto_purge_days = os.environ.get("AGENT_MEMORY_AUTO_PURGE_DAYS")
        auto_purge_enabled = os.environ.get("AGENT_MEMORY_AUTO_PURGE_ENABLED", "").lower() in ("1", "true", "yes")
        if auto_purge_days and auto_purge_enabled:
            try:
                days = int(auto_purge_days)
                if days > 0:
                    purge_result = self.store.purge_deleted(older_than_days=days)
                    purged_count = purge_result.get("purged", 0) if isinstance(purge_result, dict) else 0
                    if purged_count:
                        logger.info(f"Auto-purged {purged_count} soft-deleted memories (>{days} days old)")
            except (ValueError, TypeError):
                pass

        if self.timeline:
            try:
                self.timeline.auto_snapshot_if_needed()
                result["snapshot"] = "taken"
            except Exception as e:
                logger.exception("时间旅行快照失败: %s", e)
                result["snapshot"] = "failed"

        if self.reactor:
            try:
                scan_result = self.reactor.scan(
                    self.store,
                    decay=self.decay,
                    self_healing=self.healing,
                    causal=None,
                )
                result["reactor"] = {
                    "notifications": len(scan_result.get("notifications", [])),
                }
            except Exception as e:
                logger.exception("反应器扫描失败: %s", e)
                result["reactor"] = "failed"

        logger.info(
            "MaintainEngine 完成: ops=%s dry_run=%s elapsed=%ds",
            operations, dry_run, result["elapsed_sec"],
        )
        return result

    def _run_decay(self, dry_run: bool = False, agent_id: Optional[str] = None) -> dict:
        """
        三层衰减: active → dormant → archived

        流程:
        1. MemoryDecay 分析衰减状态
        2. MemoryLifecycle 执行语义层衰减 (on_decay)
        3. MemoryTierManager 执行物理层分层 (scan_and_tier)
        4. 将衰减状态映射到 MemoryState 三层模型
        5. 执行归档 / 删除
        """
        result: dict = {
            "analysis": {},
            "tier_scan": {},
            "lifecycle_decay": 0,
            "transitions": {"active_to_dormant": 0, "dormant_to_archived": 0},
            "archived": 0,
            "deleted": 0,
        }

        analysis = self.decay.analyze_all()
        result["analysis"] = {
            "total": analysis["total"],
            "by_status": analysis["by_status"],
            "summary": analysis["summary"],
        }

        if not dry_run:
            lifecycle_stats = self.lifecycle.scan_and_maintain(agent_id=agent_id)
            result["lifecycle_decay"] = lifecycle_stats.get("decayed", 0)

            tier_result = self.tier.scan_and_tier()
            result["tier_scan"] = tier_result

        now = int(time.time())
        if self.store:
            try:
                batch_size = 2000
                offset = 0
                while True:
                    memories = self.store.query(limit=batch_size, offset=offset, query_agent_id=agent_id)
                    if not memories:
                        break
                    for mem in memories:
                        if mem.get("lifecycle_state") in ("superseded", "merged", "deprecated"):
                            continue

                        age_days = (now - mem.get("time_ts", now)) / 86400
                        current_state = self._resolve_memory_state(mem)

                        importance = mem.get("importance", "medium")
                        quality_score = mem.get("quality_score", 0.5)
                        decay_state = self.decay_policy.should_decay(age_days, importance, quality_score)

                        if current_state == MemoryState.ACTIVE and decay_state in ("dormant", "archived", "deleted"):
                            result["transitions"]["active_to_dormant"] += 1
                            if not dry_run:
                                self._mark_state(mem, MemoryState.DORMANT)

                        elif current_state == MemoryState.DORMANT and decay_state in ("archived", "deleted"):
                            result["transitions"]["dormant_to_archived"] += 1

                    if len(memories) < batch_size:
                        break
                    offset += batch_size
            except Exception as e:
                logger.warning("MaintainEngine._run_decay: %s", e)

        if not dry_run:
            archive_result = self.decay.archive_memories(dry_run=False)
            delete_result = self.decay.delete_expired(dry_run=False)
            result["archived"] = archive_result.get("archived", 0)
            result["deleted"] = delete_result.get("deleted", 0)
        else:
            archive_result = self.decay.archive_memories(dry_run=True)
            delete_result = self.decay.delete_expired(dry_run=True)
            result["archived_dry"] = archive_result.get("archived", 0)
            result["deleted_dry"] = delete_result.get("deleted", 0)

        return result

    def _run_heal(self, agent_id: Optional[str] = None) -> dict:
        """
        矛盾检测 + 修正循环

        # Layer 1: Signal-word level (correction_detector)
        # Detects explicit correction signals: "不对", "应该是", "更正" etc.
        # Action: mark as retracted or create correction link

        # Layer 2: Semantic level (self_healing)
        # Detects implicit contradictions: opposing conclusions, numeric conflicts
        # Action: mark older as superseded, newer as reinforced

        流程:
        1. CorrectionDetector.smart_detect — 修正信号检测 (Layer 1)
        2. SelfHealing.detect_contradictions — 语义矛盾检测 (Layer 2)
        3. SelfHealing.detect_outdated — 过时检测 (语义取代)
        4. SelfHealing.heal_importance_consistency — 重要度一致性修复
        5. 对检测到的矛盾/取代执行 MemoryLifecycle.on_contradict
        """
        result: dict = {
            "contradictions": [],
            "outdated": [],
            "corrections": [],
            "superseded": 0,
            "importance_healed": 0,
            "total_issues": 0,
        }

        # Layer 1: Signal-word level — explicit correction signals
        if self.store:
            try:
                recent = self.store.query(limit=20, query_agent_id=agent_id)
                if recent:
                    newest = recent[0]
                    correction_result = self.correction.smart_detect(
                        new_text=newest.get("content", ""),
                        recent_memories=recent[1:],
                    )
                    if correction_result.get("is_correction"):
                        result["corrections"].append({
                            "type": correction_result.get("type"),
                            "confidence": correction_result.get("confidence"),
                            "suggested_action": correction_result.get("suggested_action"),
                            "target_count": len(correction_result.get("target_memories", [])),
                        })
                        if correction_result.get("suggested_action") == "mark_retracted":
                            self.correction.process_correction(self.store, correction_result)
            except Exception as e:
                logger.warning("MaintainEngine._run_heal correction: %s", e)

        # Layer 2: Semantic level — implicit contradictions
        contradictions = self.healing.detect_contradictions()
        result["contradictions"] = contradictions

        outdated = self.healing.detect_outdated()
        result["outdated"] = outdated

        superseded_count = 0
        for item in contradictions:
            if self.store:
                try:
                    mem_a = self.store.get_memory(item["memory_a"])
                    mem_b = self.store.get_memory(item["memory_b"])
                    if mem_a and mem_b:
                        older = mem_a if mem_a.get("time_ts", 0) <= mem_b.get("time_ts", 0) else mem_b
                        newer = mem_b if older is mem_a else mem_a
                        self.lifecycle.on_contradict(older, newer)
                        superseded_count += 1
                except Exception as e:
                    logger.warning("MaintainEngine._run_heal contradict: %s", e)

        for item in outdated:
            if self.store:
                try:
                    old_mem = self.store.get_memory(item["outdated_id"])
                    new_mem = self.store.get_memory(item["updated_id"])
                    if old_mem and new_mem:
                        self.lifecycle.on_contradict(old_mem, new_mem)
                        superseded_count += 1
                except Exception as e:
                    logger.warning("MaintainEngine._run_heal outdated: %s", e)

        result["superseded"] = superseded_count

        importance_result = self.healing.heal_importance_consistency()
        result["importance_healed"] = importance_result.get("count", 0)

        result["total_issues"] = (
            len(contradictions) + len(outdated) + len(result["corrections"]) + result["importance_healed"]
        )

        return result

    def _run_consolidate(self, agent_id: Optional[str] = None) -> dict:
        """
        记忆合并 (会成) — 将相似记忆融合为摘要

        流程:
        1. MemoryLifecycle.batch_merge_similar — 语义层合并
        2. HierarchicalMemory.auto_consolidate — L1 层合并
        3. 收集 ConsolidationResult
        """
        result: dict = {
            "lifecycle_merges": [],
            "l1_consolidation": {},
            "consolidation_results": [],
            "total_merged": 0,
        }

        merge_results = self.lifecycle.batch_merge_similar(agent_id=agent_id, threshold=self.decay_policy.merge_similarity_threshold)
        result["lifecycle_merges"] = merge_results

        for mr in merge_results:
            cr = ConsolidationResult(
                merged_id=mr.get("merged_id", ""),
                source_ids=[],
                topic=mr.get("topic", ""),
                source_count=mr.get("sources", 0),
            )
            result["consolidation_results"].append(cr)
            result["total_merged"] += mr.get("sources", 0)

        l1_result = self.hierarchy.auto_consolidate(threshold=self.decay_policy.merge_similarity_threshold)
        result["l1_consolidation"] = l1_result
        result["total_merged"] += l1_result.get("merged", 0)

        if self.knowledge_builder:
            try:
                kb_result = self.knowledge_builder.build_from_memories(limit=100, agent_id=agent_id)
                result["knowledge_build"] = kb_result
            except Exception as e:
                logger.warning("MaintainEngine._run_consolidate knowledge: %s", e)

        return result

    def _run_compress(self, dry_run: bool = False) -> dict:
        """
        压缩衰减记忆

        流程:
        1. MemoryCompressor.compress — LLM 驱动的主题压缩
        2. MemoryCompressor.smart_compress — 向量聚类区分核心/边缘
        """
        result: dict = {
            "compress": {},
            "smart_compress": {},
            "total_compressed": 0,
        }

        if self._llm_call_count >= self.MAX_LLM_CALLS_PER_SESSION:
            logger.info(
                "已达到LLM调用预算上限(%d次)，跳过压缩",
                self.MAX_LLM_CALLS_PER_SESSION,
            )
            result["compress"] = {"skipped": True, "reason": "llm_budget_exhausted"}
            return result

        compress_result = self.compressor.compress(dry_run=dry_run)
        self._llm_call_count += len(compress_result.get("compressed", []))
        result["compress"] = {
            "total_candidates": compress_result.get("total_candidates", 0),
            "groups_count": len(compress_result.get("groups", [])),
            "compressed_count": len(compress_result.get("compressed", [])),
            "dry_run": compress_result.get("dry_run", dry_run),
        }

        if not dry_run:
            for item in compress_result.get("compressed", []):
                result["total_compressed"] += item.get("source_count", 0)

            try:
                if self._llm_call_count >= self.MAX_LLM_CALLS_PER_SESSION:
                    result["smart_compress"] = {"skipped": True, "reason": "llm_budget_exhausted"}
                else:
                    smart_result = self.compressor.smart_compress(embedding_store=self.embedding_store)
                    self._llm_call_count += 1
                    if "error" not in smart_result:
                        result["smart_compress"] = {
                            "summary_id": smart_result.get("summary_id", ""),
                            "core_count": len(smart_result.get("core_memories", [])),
                            "edge_count": len(smart_result.get("edge_memories", [])),
                            "saved_tokens": smart_result.get("saved_tokens", 0),
                        }
                        result["total_compressed"] += len(smart_result.get("edge_memories", []))
                    else:
                        result["smart_compress"] = {"skipped": True, "reason": smart_result.get("error", "")}
            except Exception as e:
                logger.warning("MaintainEngine._run_compress smart: %s", e)
                result["smart_compress"] = {"skipped": True, "reason": str(e)}

        return result

    def _run_build_knowledge(self, agent_id: Optional[str] = None) -> dict:
        """自主知识建构 — 从碎片记忆自动构建知识图谱"""
        if not self.knowledge_builder:
            return {"skipped": True, "reason": "knowledge_builder not configured"}

        try:
            return self.knowledge_builder.build_from_memories(limit=100, agent_id=agent_id)
        except Exception as e:
            logger.warning("MaintainEngine._run_build_knowledge: %s", e)
            return {"error": str(e)}

    def _run_learn(self, dry_run: bool = False) -> dict:
        """持续学习 — 从用户反馈自动调整质量/重要度"""
        if not self.feedback_learner:
            return {"skipped": True, "reason": "feedback_learner not configured"}

        try:
            return self.feedback_learner.apply_learning(dry_run=dry_run)
        except Exception as e:
            logger.warning("MaintainEngine._run_learn: %s", e)
            return {"error": str(e)}

    def _resolve_memory_state(self, memory: dict) -> MemoryState:
        """将记忆的内部状态映射到 MemoryState 枚举"""
        lifecycle_state = memory.get("lifecycle_state", "active")
        decay_status = memory.get("_decay_status", "")

        if lifecycle_state == "superseded":
            return MemoryState.SUPERSEDED
        if lifecycle_state == "merged":
            return MemoryState.MERGED
        if lifecycle_state == "deprecated":
            return MemoryState.DEPRECATED

        if decay_status in ("archive", "delete"):
            return MemoryState.ARCHIVED
        if decay_status in ("review", "decay"):
            return MemoryState.DORMANT
        if lifecycle_state == "decaying":
            return MemoryState.DORMANT

        return MemoryState.ACTIVE

    def _mark_state(self, memory: dict, state: MemoryState):
        """将记忆标记为指定状态"""
        mid = memory.get("memory_id", "")
        if not mid or not self.store:
            return

        state_to_lifecycle = {
            MemoryState.DORMANT: "decaying",
            MemoryState.ARCHIVED: "deprecated",
            MemoryState.SUPERSEDED: "superseded",
            MemoryState.MERGED: "merged",
            MemoryState.DEPRECATED: "deprecated",
        }

        lifecycle_value = state_to_lifecycle.get(state)
        if lifecycle_value:
            try:
                with self.store.transaction() as conn:
                    conn.execute(
                        "UPDATE memories SET lifecycle_state = ? WHERE memory_id = ?",
                        (lifecycle_value, mid),
                    )
                self.store._invalidate_cache()
            except Exception as e:
                logger.warning("MaintainEngine._mark_state: %s", e)

    def get_state_distribution(self, agent_id: Optional[str] = None) -> dict:
        """获取各 MemoryState 的记忆分布"""
        distribution = {s.value: 0 for s in MemoryState}

        if not self.store:
            return distribution

        try:
            memories = self.store.query(limit=5000, query_agent_id=agent_id)
            for mem in memories:
                state = self._resolve_memory_state(mem)
                distribution[state.value] += 1
        except Exception as e:
            logger.warning("MaintainEngine.get_state_distribution: %s", e)

        return distribution

    def get_maintain_stats(self) -> dict:
        """获取维护引擎的综合统计"""
        return {
            "decay": self.decay.analyze_all(),
            "tier": self.tier.get_tier_distribution(),
            "lifecycle": self.lifecycle.get_stats(),
            "healing": self.healing.get_stats(),
            "compression": self.compressor.get_compression_stats(),
            "hierarchy": self.hierarchy.get_stats(),
            "state_distribution": self.get_state_distribution(),
        }

    def diagnose(self) -> dict:
        """
        统一诊断接口 — 供 HealthChecker 委托调用。

        返回各维度的诊断结果，避免 HealthChecker 重复遍历 store。

        返回:
            {
                "contradictions": [...],
                "fragmentation": [...],
                "stale": {...},
                "low_quality": [...],
                "knowledge_gaps": [...],
            }
        """
        result = {
            "contradictions": [],
            "fragmentation": [],
            "stale": {"count": 0, "ids": []},
            "low_quality": [],
            "knowledge_gaps": [],
        }

        all_memories = self.store.query(limit=5000)

        # 1. 矛盾检测 — 委托 healing 子引擎
        try:
            if self.healing:
                contradictions = self.healing.detect_contradictions()
                result["contradictions"] = contradictions[:20]
        except Exception as e:
            logger.debug("diagnose.contradictions: %s", e)

        # 2. 碎片化检测 — 委托 lifecycle 子引擎
        try:
            topic_groups: dict[str, list[dict]] = {}
            for mem in all_memories:
                for t in mem.get("topics", []):
                    code = t.get("code", "") if isinstance(t, dict) else str(t)
                    if code:
                        root = code.split(".")[0]
                        topic_groups.setdefault(root, []).append(mem)

            for topic, group in topic_groups.items():
                short_mems = [m for m in group if len(m.get("content", "")) < 30]
                if len(short_mems) >= 5:
                    result["fragmentation"].append({
                        "topic": topic,
                        "count": len(short_mems),
                        "ids": [m.get("memory_id", "") for m in short_mems[:10]],
                    })
        except Exception as e:
            logger.debug("diagnose.fragmentation: %s", e)

        # 3. 闲置检测 — 委托 decay 子引擎
        try:
            now = int(time.time())
            stale_threshold = now - 30 * 86400
            stale = [
                m for m in all_memories
                if m.get("time_ts", now) < stale_threshold
                and m.get("importance", "medium") != "high"
                and m.get("lifecycle_state", "active") == "active"
            ]
            result["stale"] = {
                "count": len(stale),
                "ids": [m.get("memory_id", "") for m in stale[:10]],
            }
        except Exception as e:
            logger.debug("diagnose.stale: %s", e)

        # 4. 低质量检测
        try:
            low_quality = [
                m for m in all_memories
                if m.get("_quality_score", 1.0) < 0.3
                or (m.get("importance") == "low" and len(m.get("content", "")) < 10)
            ]
            result["low_quality"] = [
                {"memory_id": m.get("memory_id", ""), "content": m.get("content", "")[:50]}
                for m in low_quality[:10]
            ]
        except Exception as e:
            logger.debug("diagnose.low_quality: %s", e)

        # 5. 知识缺口检测
        try:
            topic_counts: dict[str, int] = {}
            for mem in all_memories:
                for t in mem.get("topics", []):
                    code = t.get("code", "") if isinstance(t, dict) else str(t)
                    if code:
                        root = code.split(".")[0]
                        topic_counts[root] = topic_counts.get(root, 0) + 1

            gap_topics = {
                topic: count for topic, count in topic_counts.items()
                if count < 3
            }
            result["knowledge_gaps"] = [
                {"topic": t, "count": c} for t, c in sorted(gap_topics.items(), key=lambda x: x[1])
            ]
        except Exception as e:
            logger.debug("diagnose.knowledge_gaps: %s", e)

        return result
