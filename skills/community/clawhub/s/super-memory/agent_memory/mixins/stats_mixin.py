from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


class StatsMixin:
    def get_stats(self) -> dict:
        """系统整体统计（有界查询，不再全量加载）"""
        total = self.store.conn.execute("SELECT COUNT(*) FROM memories").fetchone()[0]
        stats = {
            "total_memories": total,
            "quality": self.quality.get_stats(),
            "causal": self.causal.get_stats(),
            "hierarchy": self.hierarchy.get_stats(),
            "self_healing": self.self_healing.get_stats(),
            "distill": self.distiller.get_distill_stats(),
            "timeline": self.timeline.get_timeline_stats(),
        }
        if total > 0:
            stats["decay"] = self.decay.analyze_all()
        else:
            stats["decay"] = {}
        if self.dedup:
            stats["dedup"] = self.dedup.get_stats()
        if self.embedding_store:
            try:
                stats["vectors"] = self.embedding_store.count()
            except Exception:
                stats["vectors"] = "unavailable"
        if self.reranker:
            stats["reranker"] = self.reranker.get_stats()
        stats["reactor"] = self.reactor.get_stats()
        stats["self_model"] = self.self_model.get_stats()
        stats["metacognition"] = self.metacognition.get_stats()
        stats["motivation"] = self.motivation.get_stats()
        stats["narrative"] = self.narrative.get_stats()
        stats["digital_twin"] = {"status": "ok"}
        return stats