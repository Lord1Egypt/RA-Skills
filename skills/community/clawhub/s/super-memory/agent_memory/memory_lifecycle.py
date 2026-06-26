"""v8.9 — memory_lifecycle.py — 记忆语义层生命周期引擎

状态机:
    active → reinforced (高频检索强化)
    active → decaying  (长期未访问衰减)
    active → superseded (被新版本取代)
    active → merged     (N条相似记忆融合)
    active → deprecated (显式废弃)

与 v8.6 memory_tier.py 的关系:
    memory_tier.py = 物理层生命周期 (HOT/WARM/COLD/EXPIRED)
    memory_lifecycle.py = 语义层生命周期 (版本/演化/合并/衰减)
"""

from __future__ import annotations

import time
import json
import hashlib
import logging
from datetime import datetime
from typing import Optional, Callable

logger = logging.getLogger(__name__)

LIFECYCLE_STATES = (
    "active", "reinforced", "decaying",
    "superseded", "merged", "deprecated",
)

LIFECYCLE_TRANSITIONS = {
    "active": {"reinforce", "decay", "evolve", "merge", "deprecate"},
    "reinforced": {"decay", "evolve", "merge"},
    "decaying": {"reinforce"},
    "superseded": set(),
    "merged": set(),
    "deprecated": set(),
}

_REINFORCE_THRESHOLD = 10
_DECAY_GRACE_DAYS = 7
_MERGE_SIMILARITY_THRESHOLD = 0.85
_MERGE_MIN_COUNT = 5


class MemoryLifecycle:
    """记忆语义层生命周期管理器"""

    def __init__(self, store=None, embedder=None, llm_fn: Callable = None):
        self.store = store
        self.embedder = embedder
        self.llm_fn = llm_fn

    def on_create(self, memory: dict) -> dict:
        memory["lifecycle_state"] = "active"
        memory["version"] = 1
        memory["lifecycle_events"] = json.dumps([
            {"ts": int(time.time()), "event": "created", "state": "active"}
        ])
        if self.store:
            self._persist_meta(memory["memory_id"], memory)
        return memory

    def on_contradict(self, old: dict, new: dict) -> dict:
        if new.get("confidence", 0.5) <= old.get("confidence", 0.5):
            logger.debug(f"新记忆置信度不高于旧版本，跳过: {new.get('memory_id', '?')}")
            new["lifecycle_state"] = "active"
            return new

        old["lifecycle_state"] = "superseded"
        old["superseded_by"] = new["memory_id"]
        old["lifecycle_events"] = self._append_event(
            old, "contradicted",
            f"被 {new['memory_id'][:16]}... 取代 (confidence {old['confidence']}→{new['confidence']})"
        )

        new["lifecycle_state"] = "current"
        new["supersedes"] = old["memory_id"]
        new["version"] = old.get("version", 1) + 1
        new["lifecycle_events"] = json.dumps([
            {"ts": int(time.time()), "event": "superseded_old", "old_id": old["memory_id"]}
        ])

        if self.store:
            self._persist_meta(old["memory_id"], old)
            self._persist_meta(new["memory_id"], new)
            self.store.insert_link(
                source_id=new["memory_id"],
                target_id=old["memory_id"],
                link_type="causal.revised_from",
                weight=0.7,
                reason=f"v{new['version']} 取代 v{old.get('version',1)}",
            )
        return new

    def on_reinforce(self, memory: dict, times: int) -> dict:
        if times >= _REINFORCE_THRESHOLD and memory.get("importance") == "medium":
            memory["importance"] = "high"
            memory["reinforced_at"] = int(time.time())
            memory["lifecycle_state"] = "reinforced"
            memory["lifecycle_events"] = self._append_event(
                memory, "reinforced",
                f"高频检索 ({times}次) → importance: medium→high"
            )
            if self.store:
                self._persist_meta(memory["memory_id"], memory)
        return memory

    def on_decay(self, memory: dict, days_since_access: int) -> dict:
        if days_since_access <= _DECAY_GRACE_DAYS:
            return memory
        if memory.get("importance") == "high":
            return memory

        if memory.get("importance") == "medium" and days_since_access > 90:
            memory["confidence"] = max(0.1, memory.get("confidence", 0.5) * 0.5)
            memory["lifecycle_state"] = "decaying"
        elif memory.get("importance") == "low" and days_since_access > 30:
            memory["confidence"] = max(0.05, memory.get("confidence", 0.5) * 0.3)
            memory["lifecycle_state"] = "decaying"

        memory["decayed_at"] = int(time.time())
        memory["lifecycle_events"] = self._append_event(
            memory, "decayed",
            f"{days_since_access}天未访问 → confidence→{memory['confidence']:.2f}"
        )
        if self.store:
            self._persist_meta(memory["memory_id"], memory)
        return memory

    def on_merge(self, memories: list[dict]) -> dict:
        if len(memories) < _MERGE_MIN_COUNT:
            raise ValueError(f"至少需要 {_MERGE_MIN_COUNT} 条记忆才能合并，当前 {len(memories)}")
        if self.embedder and not self._check_similarity(memories):
            logger.warning("记忆间相似度不足，跳过合并")
            raise ValueError("相似度不足")

        merged_content = self._summarize(memories)
        merged_id = self._gen_merged_id(memories)
        now = int(time.time())

        merged = {
            "memory_id": merged_id,
            "content": merged_content,
            "content_hash": hashlib.sha256(merged_content.encode()).hexdigest(),
            "merged_from": [m["memory_id"] for m in memories],
            "lifecycle_state": "merged",
            "version": max(m.get("version", 1) for m in memories) + 1,
            "importance": self._highest_importance(memories),
            "confidence": min(1.0, max(m.get("confidence", 0.5) for m in memories)),
            "created_at": now,
            "lifecycle_events": json.dumps([
                {"ts": now, "event": "merged",
                 "sources": [m["memory_id"] for m in memories]}
            ]),
        }

        if self.store:
            for m in memories:
                m["lifecycle_state"] = "superseded"
                m["merged_into"] = merged_id
                m["lifecycle_events"] = self._append_event(
                    m, "absorbed", f"合并入 {merged_id[:16]}..."
                )
                self._persist_meta(m["memory_id"], m)

        return merged

    def on_evolve(self, memory: dict, new_evidence: dict) -> dict:
        new_id = f"{memory['memory_id']}_v{memory.get('version', 1) + 1}"

        if self.llm_fn:
            prompt = (
                f"原始记忆: {memory.get('content', '')}\n"
                f"新证据: {new_evidence.get('content', '')}\n"
                f"请基于新证据更新原始记忆内容，保留关键原始信息，只输出更新后的内容。"
            )
            evolved_content = self.llm_fn(prompt)
        else:
            evolved_content = f"{memory.get('content', '')}\n[更新] {new_evidence.get('content', '')}"

        now = int(time.time())
        evolved = {
            "memory_id": new_id,
            "content": evolved_content,
            "content_hash": hashlib.sha256(evolved_content.encode()).hexdigest(),
            "time_id": memory.get("time_id", ""),
            "time_ts": now,
            "person_id": memory.get("person_id", ""),
            "nature_id": memory.get("nature_id", ""),
            "importance": memory.get("importance", "medium"),
            "confidence": memory.get("confidence", 0.5),
            "lifecycle_state": "current",
            "version": memory.get("version", 1) + 1,
            "evolved_from": memory["memory_id"],
            "created_at": now,
            "lifecycle_events": json.dumps([
                {"ts": now, "event": "evolved",
                 "from": memory["memory_id"]}
            ]),
        }

        memory["lifecycle_state"] = "superseded"
        memory["evolved_to"] = new_id
        memory["lifecycle_events"] = self._append_event(
            memory, "evolved", f"演化至 {new_id[:16]}..."
        )

        if self.store:
            self._persist_meta(memory["memory_id"], memory)
            self.store.insert_link(
                source_id=new_id,
                target_id=memory["memory_id"],
                link_type="causal.evolved_from",
                weight=0.6,
                reason=f"v{memory.get('version', 1)}→v{evolved['version']} 基于新证据演化",
            )
        return evolved

    def on_deprecate(self, memory: dict, reason: str = "") -> dict:
        memory["lifecycle_state"] = "deprecated"
        memory["deprecated_at"] = int(time.time())
        memory["lifecycle_events"] = self._append_event(
            memory, "deprecated", reason or "显式废弃"
        )
        if self.store:
            self._persist_meta(memory["memory_id"], memory)
        return memory

    def trace(self, memory_id: str) -> list[dict]:
        chain = []
        current = memory_id
        visited = set()

        while current and current not in visited:
            visited.add(current)
            mem = self.store.get_memory(current) if self.store else None
            if not mem:
                break
            chain.append({
                "memory_id": current[:32],
                "version": mem.get("version", 1),
                "lifecycle_state": mem.get("lifecycle_state", "active"),
                "importance": mem.get("importance", "medium"),
                "confidence": mem.get("confidence", 0.5),
                "content_preview": (mem.get("content", "") or "")[:80],
            })

            if mem.get("evolved_to") or mem.get("superseded_by"):
                current = mem.get("evolved_to") or mem.get("superseded_by")
            elif mem.get("merged_into"):
                current = mem.get("merged_into")
            else:
                break
        return chain

    def scan_and_maintain(self, agent_id: str = None) -> dict:
        stats = {"reinforced": 0, "decayed": 0, "deprecated": 0}
        if not self.store:
            return stats

        now = int(time.time())
        memories = self.store.query(limit=500, query_agent_id=agent_id)

        for mem in memories:
            mid = mem.get("memory_id", "")
            if not mid:
                continue
            state = mem.get("lifecycle_state", "active")
            if state in ("superseded", "merged", "deprecated"):
                continue

            last_access = mem.get("created_at", now)
            days_since = (now - last_access) / 86400

            if days_since > _DECAY_GRACE_DAYS:
                self.on_decay(mem, int(days_since))
                stats["decayed"] += 1
            elif mem.get("reinforced_at") and state == "reinforced":
                pass

        logger.info(
            f"生命周期维护完成: "
            f"decayed={stats['decayed']}"
        )
        return stats

    def should_deprecate(self, memory: dict) -> bool:
        if memory.get("importance") == "high":
            return False
        if memory.get("lifecycle_state") == "decaying":
            confidence = memory.get("confidence", 0.5)
            return confidence < 0.1
        return False

    def batch_merge_similar(self, agent_id: str = None, topic_code: str = None, threshold: float = 0.85) -> list[dict]:
        results = []
        if not self.store:
            return results

        memories = self.store.query(limit=500, query_agent_id=agent_id)
        groups = self._group_by_topic(memories)

        for topic, group in groups.items():
            if len(group) < _MERGE_MIN_COUNT:
                continue
            active_group = [m for m in group
                           if m.get("lifecycle_state", "active") in ("active", "reinforced")]
            if len(active_group) < _MERGE_MIN_COUNT:
                continue
            if not self._check_similarity(active_group, threshold=threshold):
                continue
            try:
                merged = self.on_merge(active_group[:_MERGE_MIN_COUNT + 2])
                results.append({"merged_id": merged["memory_id"], "topic": topic,
                               "sources": len(active_group)})
            except ValueError as e:
                logger.debug(f"跳过合并 topic={topic}: {e}")
        return results

    def _check_similarity(self, memories: list[dict], threshold: float = 0.85) -> bool:
        if not self.embedder or len(memories) < 2:
            return len(memories) >= 2
        try:
            contents = [m.get("content", "") for m in memories[:5]]
            vectors = self.embedder.encode_batch(contents)
            sim_sum = 0.0
            count = 0
            for i in range(len(vectors)):
                for j in range(i + 1, len(vectors)):
                    sim = self._cosine_sim(vectors[i], vectors[j])
                    sim_sum += sim
                    count += 1
            avg_sim = sim_sum / count if count > 0 else 0
            return avg_sim >= threshold
        except Exception as e:
            logger.debug(f"相似度检测失败，回退到关键词匹配: {e}")
            return True

    def _summarize(self, memories: list[dict]) -> str:
        if self.llm_fn:
            lines = [f"[{i+1}] {m.get('content', '')[:200]}" for i, m in enumerate(memories[:10])]
            prompt = (
                "将以下多条相关记忆融合为一条简洁的摘要，保留所有关键事实：\n\n" +
                "\n".join(lines)
            )
            try:
                return self.llm_fn(prompt)
            except Exception as e:
                logger.error(f"LLM 摘要失败: {e}")
        return " | ".join(m.get("content", "")[:100] for m in memories[:3])

    @staticmethod
    def _gen_merged_id(memories: list[dict]) -> str:
        content = "".join(m.get("content", "")[:50] for m in memories[:3])
        h = hashlib.sha256(content.encode()).hexdigest()[:12]
        return f"MERGED_{h}"

    @staticmethod
    def _highest_importance(memories: list[dict]) -> str:
        order = {"high": 3, "medium": 2, "low": 1}
        best = "low"
        best_score = 1
        for m in memories:
            imp = m.get("importance", "low")
            if order.get(imp, 0) > best_score:
                best = imp
                best_score = order[imp]
        return best

    @staticmethod
    def _append_event(memory: dict, event: str, detail: str) -> str:
        try:
            events = json.loads(memory.get("lifecycle_events", "[]"))
        except (json.JSONDecodeError, TypeError):
            events = []
        events.append({"ts": int(time.time()), "event": event, "detail": detail})
        return json.dumps(events, ensure_ascii=False)

    def _persist_meta(self, memory_id: str, memory: dict):
        try:
            self.store.conn.execute(
                """UPDATE memories SET importance = ?, confidence = ?,
                   lifecycle_state = ?, lifecycle_events = ?
                   WHERE memory_id = ?""",
                (
                    memory.get("importance", "medium"),
                    memory.get("confidence", 0.5),
                    memory.get("lifecycle_state", "active"),
                    memory.get("lifecycle_events", "[]"),
                    memory_id,
                ),
            )
            self.store.conn.commit()
        except Exception as e:
            logger.warning("memory_lifecycle: %s", e)

    @staticmethod
    def _group_by_topic(memories: list[dict]) -> dict[str, list[dict]]:
        groups = {}
        for mem in memories:
            topics = mem.get("topics", [])
            if not topics:
                continue
            primary = topics[0].get("code", "") if isinstance(topics[0], dict) else str(topics[0])
            if not primary:
                continue
            groups.setdefault(primary, []).append(mem)
        return groups

    @staticmethod
    def _cosine_sim(a, b) -> float:
        if hasattr(a, 'tolist'):
            a = a.tolist()
        if hasattr(b, 'tolist'):
            b = b.tolist()
        dot = sum(x * y for x, y in zip(a, b))
        na = sum(x * x for x in a) ** 0.5
        nb = sum(x * x for x in b) ** 0.5
        if na == 0 or nb == 0:
            return 0.0
        return dot / (na * nb)

    def get_stats(self) -> dict:
        stats = {"total": 0}
        for state in LIFECYCLE_STATES:
            stats[state] = 0
        if not self.store:
            return stats
        try:
            rows = self.store.conn.execute(
                "SELECT lifecycle_state, COUNT(*) as cnt FROM memories GROUP BY lifecycle_state"
            ).fetchall()
            for row in rows:
                state = row[0] or "active"
                stats[state] = row[1]
                stats["total"] += row[1]
        except Exception as e:
            logger.warning("memory_lifecycle: %s", e)
        return stats