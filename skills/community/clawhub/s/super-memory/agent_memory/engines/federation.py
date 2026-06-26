"""
engines/federation.py — Cross-Agent Knowledge Federation

Enables multiple AgentMemory instances to share knowledge while respecting privacy boundaries.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional
import time
import logging

logger = logging.getLogger(__name__)


@dataclass
class FederationPolicy:
    allow_share_public: bool = True
    allow_share_team: bool = True
    allow_share_private: bool = False
    allow_share_restricted: bool = False
    require_confirmation: bool = True
    max_share_per_request: int = 50
    excluded_topics: list = field(default_factory=list)
    excluded_nature_codes: list = field(default_factory=list)


@dataclass
class FederationRequest:
    requesting_agent: str
    target_agent: str
    query: str
    topics: list = field(default_factory=list)
    max_results: int = 10
    min_confidence: float = 0.3
    timestamp: float = field(default_factory=time.time)


@dataclass
class FederationResponse:
    request_id: str
    source_agent: str
    granted: bool
    results: list = field(default_factory=list)
    denied_reason: str = ""
    privacy_level: str = "team"
    timestamp: float = field(default_factory=time.time)


@dataclass
class KnowledgeConflict:
    topic: str
    agent_a: str
    agent_a_claim: str
    agent_b: str
    agent_b_claim: str
    conflict_type: str
    resolution: str = "unresolved"
    confidence_a: float = 0.0
    confidence_b: float = 0.0
    merged_claim: str = ""


class FederationEngine:
    """
    Cross-Agent Knowledge Federation Engine.

    Enables:
    1. Knowledge negotiation: request/share with privacy controls
    2. Federated search: search across multiple agent memories
    3. Conflict detection: find contradictions between agents
    4. Conflict resolution: merge or arbitrate conflicting knowledge
    """

    def __init__(self, store, recall_engine=None, embedding_store=None, policy=None):
        self.store = store
        self.recall_engine = recall_engine
        self.embedding_store = embedding_store
        self.policy = policy or FederationPolicy()
        self._peers: dict[str, 'FederationEngine'] = {}
        self._conflict_log: list[KnowledgeConflict] = []
        self._share_history: list[dict] = []

    def register_peer(self, agent_id: str, peer_engine: 'FederationEngine'):
        self._peers[agent_id] = peer_engine

    def unregister_peer(self, agent_id: str):
        self._peers.pop(agent_id, None)

    def list_peers(self) -> list[str]:
        return list(self._peers.keys())

    def request_knowledge(self, request: FederationRequest) -> FederationResponse:
        peer = self._peers.get(request.target_agent)
        if peer is None:
            return FederationResponse(
                request_id=f"freq_{int(time.time())}",
                source_agent=request.target_agent,
                granted=False,
                denied_reason="peer_not_found",
            )
        return peer.handle_request(request)

    def handle_request(self, request: FederationRequest) -> FederationResponse:
        if not self._check_policy(request):
            return FederationResponse(
                request_id=f"freq_{int(time.time())}",
                source_agent=self.store.agent_id if hasattr(self.store, 'agent_id') and self.store.agent_id else "local",
                granted=False,
                denied_reason="policy_denied",
            )

        results = self._search_local(request.query, request.topics, request.max_results)
        filtered = self._filter_by_privacy(results)

        if self.policy.excluded_topics:
            filtered = [r for r in filtered if not any(
                t in self.policy.excluded_topics for t in r.get("topics", [])
            )]

        self._share_history.append({
            "requesting_agent": request.requesting_agent,
            "query": request.query,
            "results_shared": len(filtered),
            "timestamp": time.time(),
        })

        return FederationResponse(
            request_id=f"freq_{int(time.time())}",
            source_agent=self.store.agent_id if hasattr(self.store, 'agent_id') and self.store.agent_id else "local",
            granted=True,
            results=filtered[:request.max_results],
            privacy_level="team",
        )

    def federated_search(self, query: str, topics=None, max_per_peer: int = 5) -> dict:
        all_results = []
        peer_stats = {}

        local_results = self._search_local(query, topics, max_per_peer)
        all_results.extend(local_results)
        peer_stats["local"] = len(local_results)

        for peer_id, peer_engine in self._peers.items():
            try:
                request = FederationRequest(
                    requesting_agent=self.store.agent_id if hasattr(self.store, 'agent_id') and self.store.agent_id else "local",
                    target_agent=peer_id,
                    query=query,
                    topics=topics or [],
                    max_results=max_per_peer,
                )
                response = peer_engine.handle_request(request)
                if response.granted:
                    for r in response.results:
                        r["_source_agent"] = peer_id
                        r["_federated"] = True
                    all_results.extend(response.results)
                    peer_stats[peer_id] = len(response.results)
                else:
                    peer_stats[peer_id] = f"denied:{response.denied_reason}"
            except Exception as e:
                logger.warning("联邦检索 %s 失败: %s", peer_id, e)
                peer_stats[peer_id] = f"error:{e}"

        merged = self._merge_federated_results(all_results, query)

        return {
            "total": len(merged),
            "results": merged,
            "peer_stats": peer_stats,
            "query": query,
        }

    def detect_conflicts(self, topic: str = None) -> list[KnowledgeConflict]:
        conflicts = []

        for peer_id, peer_engine in self._peers.items():
            try:
                peer_conflicts = self._detect_conflicts_with_peer(peer_id, peer_engine, topic)
                conflicts.extend(peer_conflicts)
            except Exception as e:
                logger.warning("冲突检测 %s 失败: %s", peer_id, e)

        self._conflict_log.extend(conflicts)
        return conflicts

    def _detect_conflicts_with_peer(self, peer_id, peer_engine, topic=None) -> list[KnowledgeConflict]:
        conflicts = []

        local_topics = [topic] if topic else []
        local_results = self._search_local("", local_topics, 20)

        request = FederationRequest(
            requesting_agent=self.store.agent_id if hasattr(self.store, 'agent_id') and self.store.agent_id else "local",
            target_agent=peer_id,
            query="",
            topics=local_topics,
            max_results=20,
        )
        response = peer_engine.handle_request(request)
        if not response.granted:
            return conflicts

        peer_results = response.results

        for local_mem in local_results:
            for peer_mem in peer_results:
                conflict = self._check_conflict(local_mem, peer_mem, peer_id)
                if conflict:
                    conflicts.append(conflict)

        return conflicts

    def _check_conflict(self, local_mem, peer_mem, peer_id) -> Optional[KnowledgeConflict]:
        """Enhanced conflict detection using multiple signals."""
        local_topics = set(local_mem.get("topics", []))
        peer_topics = set(peer_mem.get("topics", []))
        shared = local_topics & peer_topics
        if not shared:
            return None

        local_content = local_mem.get("content", "")
        peer_content = peer_mem.get("content", "")

        def _char_ngrams(text, n=3):
            return set(text[i:i+n] for i in range(max(0, len(text)-n+1)))
        ng_local = _char_ngrams(local_content.lower())
        ng_peer = _char_ngrams(peer_content.lower())
        if not ng_local or not ng_peer:
            return None
        overlap_ratio = len(ng_local & ng_peer) / max(len(ng_local), len(ng_peer))
        if overlap_ratio < 0.10:
            return None

        embedding_sim = 0.0
        if self.embedding_store:
            try:
                local_id = local_mem.get("memory_id", "")
                peer_id_mem = peer_mem.get("memory_id", "")
                vec_local = self.embedding_store.get_vector(local_id)
                vec_peer = self.embedding_store.get_vector(peer_id_mem)
                if vec_local is not None and vec_peer is not None:
                    import numpy as np
                    v1, v2 = np.array(vec_local), np.array(vec_peer)
                    n1, n2 = np.linalg.norm(v1), np.linalg.norm(v2)
                    if n1 > 0 and n2 > 0:
                        embedding_sim = float(np.dot(v1, v2) / (n1 * n2))
            except Exception as e:
                logger.debug("_detect_conflict embedding_sim: %s", e)

        positive_words = {"好", "优秀", "推荐", "成功", "正确", "适合", "有效", "赞成", "支持", "good", "great", "best", "excellent", "recommend", "support", "agree"}
        negative_words = {"差", "糟糕", "避免", "失败", "错误", "不适合", "无效", "反对", "抵制", "bad", "worst", "avoid", "fail", "oppose", "disagree", "against"}

        local_lower = local_content.lower()
        peer_lower = peer_content.lower()

        local_pos = sum(1 for w in positive_words if w in local_lower)
        local_neg = sum(1 for w in negative_words if w in local_lower)
        peer_pos = sum(1 for w in positive_words if w in peer_lower)
        peer_neg = sum(1 for w in negative_words if w in peer_lower)

        sentiment_conflict = (local_pos > local_neg and peer_neg > peer_pos) or (local_neg > local_pos and peer_pos > peer_neg)

        negation_words = {"不", "非", "没", "无", "未", "别", "勿", "not", "no", "never", "don't", "isn't", "won't", "can't"}
        local_has_negation = any(w in local_lower for w in negation_words)
        peer_has_negation = any(w in peer_lower for w in negation_words)
        negation_conflict = local_has_negation != peer_has_negation and overlap_ratio > 0.2

        conflict_score = 0.0
        conflict_type = "contradiction"

        if sentiment_conflict:
            conflict_score += 0.5
        if negation_conflict:
            conflict_score += 0.3
        if embedding_sim > 0.8 and (sentiment_conflict or negation_conflict):
            conflict_score += 0.2

        if conflict_score >= 0.3:
            return KnowledgeConflict(
                topic=",".join(sorted(shared)),
                agent_a=self.store.agent_id or "local",
                agent_a_claim=local_content[:100],
                agent_b=peer_id,
                agent_b_claim=peer_content[:100],
                conflict_type=conflict_type,
                confidence_a=local_mem.get("quality_score", 0.5),
                confidence_b=peer_mem.get("quality_score", 0.5),
            )

        return None

    def resolve_conflict(self, conflict: KnowledgeConflict, strategy: str = "higher_confidence") -> KnowledgeConflict:
        if strategy == "higher_confidence":
            conflict.resolution = "a_wins" if conflict.confidence_a >= conflict.confidence_b else "b_wins"
        elif strategy == "newer_wins":
            conflict.resolution = "newer_wins"
        elif strategy == "merged":
            conflict.resolution = "merged"
            conflict.merged_claim = f"[{conflict.agent_a}]: {conflict.agent_a_claim} | [{conflict.agent_b}]: {conflict.agent_b_claim}"
        elif strategy == "both_kept":
            conflict.resolution = "both_kept"

        if conflict.resolution == "a_wins" and conflict.confidence_b < conflict.confidence_a:
            try:
                losing_mems = self.store.query(query=conflict.agent_b_claim[:50], limit=1)
                for m in losing_mems:
                    self.store.update_memory(m["memory_id"], {"quality_score": m.get("quality_score", 0.5) * 0.8})
            except Exception as e:
                logger.debug("resolve_conflict a_wins downgrade: %s", e)
        elif conflict.resolution == "b_wins" and conflict.confidence_a < conflict.confidence_b:
            try:
                losing_mems = self._search_local(conflict.agent_a_claim[:50], [], 1)
                for m in losing_mems:
                    self.store.update_memory(m.get("memory_id", ""), {"quality_score": m.get("quality_score", 0.5) * 0.8})
            except Exception as e:
                logger.debug("resolve_conflict b_wins downgrade: %s", e)

        return conflict

    def _check_policy(self, request) -> bool:
        if request.requesting_agent == (self.store.agent_id or "local"):
            return False
        if not self.policy.allow_share_team:
            return False
        if self.policy.require_confirmation:
            pass
        if self.policy.excluded_topics:
            if any(t in self.policy.excluded_topics for t in request.topics):
                return False
        return True

    def _search_local(self, query, topics, max_results):
        try:
            if self.recall_engine:
                result = self.recall_engine.recall(query=query, limit=max_results)
                if isinstance(result, dict):
                    return result.get("results", result.get("primary", []))
                if hasattr(result, "to_dict"):
                    d = result.to_dict()
                    return d.get("results", d.get("primary", []))
            return self.store.query(query=query, limit=max_results) if query else self.store.query(limit=max_results)
        except Exception as e:
            logger.debug("_search_local: %s", e)
            return []

    def _filter_by_privacy(self, results):
        filtered = []
        for r in results:
            visibility = r.get("visibility", "team")
            if visibility == "public" and self.policy.allow_share_public:
                filtered.append(r)
            elif visibility == "team" and self.policy.allow_share_team:
                filtered.append(r)
            elif visibility == "private" and self.policy.allow_share_private:
                filtered.append(r)
        return filtered

    def _merge_federated_results(self, all_results, query):
        seen = set()
        merged = []
        for r in all_results:
            content = r.get("content", "")
            content_key = content[:100]
            if content_key not in seen:
                seen.add(content_key)
                merged.append(r)

        merged.sort(key=lambda x: x.get("quality_score", 0.5), reverse=True)
        return merged

    def get_stats(self) -> dict:
        return {
            "peers": len(self._peers),
            "peer_ids": list(self._peers.keys()),
            "conflicts_detected": len(self._conflict_log),
            "shares_completed": len(self._share_history),
            "policy": {
                "allow_share_public": self.policy.allow_share_public,
                "allow_share_team": self.policy.allow_share_team,
                "allow_share_private": self.policy.allow_share_private,
            },
        }
