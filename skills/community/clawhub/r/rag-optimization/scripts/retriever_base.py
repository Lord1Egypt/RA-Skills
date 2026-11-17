#!/usr/bin/env python3
"""
检索器基类与策略
==================
定义统一的检索器接口，让 BM25 / Vector / Hybrid 成为可组合的检索器。

之前 bm25_retriever.py 内嵌了三种策略（bm25/vector/hybrid），违反单一职责。
此模块将策略分离：
    - BM25Retriever：纯 BM25 关键词检索（继承自现有实现）
    - VectorRetriever：纯向量检索
    - HybridRetriever：组合两个检索器，加权融合

组合示例：
    bm25 = BM25Retriever()
    vec = VectorRetriever(embedding_model=model)
    hybrid = HybridRetriever(left=bm25, right=vec, weight=0.7)
    results = hybrid.retrieve("RAG 优化策略", top_k=10)

降级行为：所有检索器在无依赖时回退为可用的纯标准库实现。
"""
import logging
import math
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# ============================================================
# 检索结果
# ============================================================

@dataclass
class RetrievalHit:
    """检索结果条目"""
    id: str
    content: str
    score: float = 0.0
    metadata: Dict = field(default_factory=dict)


# ============================================================
# 基类
# ============================================================

class BaseRetriever:
    """
    检索器基类。

    所有检索器必须实现：
        - index(): 建立索引
        - retrieve(): 执行检索

    支持组合：HybridRetriever 组合两个检索器并加权融合。
    """

    def index(self, documents: List[Dict]) -> int:
        """
        建立索引。

        Args:
            documents: 文档列表，每个元素为 dict：{"id": str, "content": str, "metadata": dict}

        Returns:
            索引的文档数
        """
        raise NotImplementedError

    def retrieve(self, query: str, top_k: int = 10) -> List[RetrievalHit]:
        """
        检索 top_k 相关文档。

        Args:
            query: 查询文本
            top_k: 返回数量

        Returns:
            按相关性降序的 RetrievalHit 列表
        """
        raise NotImplementedError

    def _normalize_score(self, score: float, min_score: float, max_score: float) -> float:
        """归一化分数到 [0, 1]。"""
        if max_score == min_score:
            return 1.0
        return max(0.0, min(1.0, (score - min_score) / (max_score - min_score)))


# ============================================================
# BM25 检索器（H21：适配层，真实实现统一在 scripts/bm25_retriever.py）
# ============================================================

class BM25Retriever(BaseRetriever):
    """
    Okapi BM25 检索器 —— 指向真实现的兼容适配层。

    H21：此前这里是第二份平行实现。两份副本各自演化，所有加固
    （IDF 缓存失效 H6/H7、查询缓存 TTL H18、k1/b 变参 H5、零分文档
    过滤 H24）都只落在 scripts/bm25_retriever.py 的真实现上，这份副本
    静默落后——谁 import 到它，谁就拿到带旧缺陷的检索器。

    现改为延迟导入的适配层：
      - 保持 BaseRetriever 的接口契约（index()/retrieve() → RetrievalHit），
        老调用方零改动；
      - 构造签名 (k1, b) 映射到真实现的 config；
      - 延迟导入（在方法内 import）规避循环依赖：
        bm25_retriever.py 顶部 from retriever_base import BaseRetriever。
    """

    def __init__(self, k1: float = 1.5, b: float = 0.75):
        from bm25_retriever import BM25Retriever as _RealBM25
        self._impl = _RealBM25(config={"k1": k1, "b": b})

    def index(self, documents: List[Dict]) -> int:
        # 真实现的 index() 已兼容 {"id","content"} 与 {"id","text"} 两种格式
        return self._impl.index(documents)

    def retrieve(self, query: str, top_k: int = 10) -> List[RetrievalHit]:
        results = self._impl.retrieve(query, top_k=top_k, strategy="bm25")
        return [RetrievalHit(
            id=r.id,
            content=r.text,
            score=r.score,
            metadata=r.metadata,
        ) for r in results]

    def invalidate_cache(self):
        """透传缓存失效（与真实现保持同一套能力面）。"""
        return self._impl.invalidate_cache()


# ============================================================
# 向量检索器
# ============================================================

class VectorRetriever(BaseRetriever):
    """
    向量检索器：使用嵌入模型计算余弦相似度。

    需要 embedding_model（提供 encode(texts) -> List[List[float]]）。
    无模型时回退为 BM25。
    """

    def __init__(self, embedding_model=None, fallback: BaseRetriever = None):
        self.embedding_model = embedding_model
        self.fallback = fallback
        self._vectors: Dict[str, List[float]] = {}
        self._documents: Dict[str, Dict] = {}

    def index(self, documents: List[Dict]) -> int:
        self._documents = {}
        self._vectors = {}

        if not self.embedding_model:
            if self.fallback:
                return self.fallback.index(documents)
            logger.warning("无 embedding_model，回退为 BM25")
            bm25 = BM25Retriever()
            return bm25.index(documents)

        for doc in documents:
            doc_id = str(doc.get('id', len(self._documents)))
            text = doc.get('content', doc.get('text', ''))
            vecs = self.embedding_model.encode([text])
            vec = vecs[0].tolist() if hasattr(vecs[0], 'tolist') else vecs[0]
            self._vectors[doc_id] = vec
            self._documents[doc_id] = doc

        logger.info(f"向量索引了 {len(self._documents)} 篇文档")
        return len(self._documents)

    def retrieve(self, query: str, top_k: int = 10) -> List[RetrievalHit]:
        if not self.embedding_model:
            if self.fallback and hasattr(self.fallback, '_indexed') and self.fallback._indexed:
                return self.fallback.retrieve(query, top_k)
            bm25 = BM25Retriever()
            bm25.index(list(self._documents.values()))
            return bm25.retrieve(query, top_k)

        query_vec = self.embedding_model.encode([query])[0]
        q_list = query_vec.tolist() if hasattr(query_vec, 'tolist') else query_vec
        q_norm = sum(v * v for v in q_list) ** 0.5

        results = []
        for doc_id, doc_vec in self._vectors.items():
            dot = sum(a * b for a, b in zip(q_list, doc_vec))
            d_norm = sum(v * v for v in doc_vec) ** 0.5
            score = dot / (q_norm * d_norm) if (q_norm and d_norm) else 0.0
            results.append(RetrievalHit(
                id=doc_id,
                content=self._documents[doc_id].get('content', ''),
                score=round(float(score), 4),
                metadata=self._documents[doc_id].get('metadata', {}),
            ))

        results.sort(key=lambda r: r.score, reverse=True)
        return results[:top_k]


# ============================================================
# 混合检索器（组合两个检索器）
# ============================================================

class HybridRetriever(BaseRetriever):
    """
    混合检索器：组合两个检索器，加权融合分数。

    使用方式：
        hybrid = HybridRetriever(
            left=BM25Retriever(),
            right=VectorRetriever(model),
            weight=0.7  # left 的权重
        )
        results = hybrid.retrieve("RAG 优化", top_k=10)

    权重说明：
        weight=0.7 → 左侧检索器占 70%，右侧占 30%
        weight=0.5 → 各占 50%（等权）
    """

    def __init__(self, left: BaseRetriever, right: BaseRetriever, weight: float = 0.7):
        """
        Args:
            left: 第一个检索器（权重 = weight）
            right: 第二个检索器（权重 = 1 - weight）
            weight: 左侧检索器的权重（0-1），默认 0.7
        """
        self.left = left
        self.right = right
        self.weight = max(0.0, min(1.0, weight))

    def index(self, documents: List[Dict]) -> int:
        n_left = self.left.index(documents)
        n_right = self.right.index(documents)
        return max(n_left, n_right)

    def retrieve(self, query: str, top_k: int = 10) -> List[RetrievalHit]:
        left_hits = self.left.retrieve(query, top_k=top_k * 2)  # 多取一些供融合
        right_hits = self.right.retrieve(query, top_k=top_k * 2)

        # 构建 id -> score 映射
        left_scores = {h.id: h.score for h in left_hits}
        right_scores = {h.id: h.score for h in right_hits}

        # 归一化
        left_max = max(left_scores.values()) if left_scores else 1.0
        left_min = min(left_scores.values()) if left_scores else 0.0
        right_max = max(right_scores.values()) if right_scores else 1.0
        right_min = min(right_scores.values()) if right_scores else 0.0

        # 合并所有文档
        all_ids = set(left_scores.keys()) | set(right_scores.keys())
        # 获取文档内容（从任意一侧）
        all_docs = {}
        for h in left_hits:
            all_docs[h.id] = (h.content, h.metadata)
        for h in right_hits:
            if h.id not in all_docs:
                all_docs[h.id] = (h.content, h.metadata)

        results = []
        for doc_id in all_ids:
            ls = self._normalize_score(left_scores.get(doc_id, 0), left_min, left_max)
            rs = self._normalize_score(right_scores.get(doc_id, 0), right_min, right_max)
            final = self.weight * ls + (1 - self.weight) * rs
            content, metadata = all_docs[doc_id]
            results.append(RetrievalHit(
                id=doc_id,
                content=content,
                score=round(float(final), 4),
                metadata=metadata,
            ))

        results.sort(key=lambda r: r.score, reverse=True)
        return results[:top_k]


# ============================================================
# 使用示例
# ============================================================

if __name__ == '__main__':
    corpus = [
        {"id": "doc_1", "content": "RAG 是一种结合信息检索和生成模型的技术，能降低幻觉。"},
        {"id": "doc_2", "content": "由小到大检索是 RAG 优化的核心策略，用小块检索，返回大块上下文。"},
        {"id": "doc_3", "content": "混合检索结合向量语义与 BM25 关键词匹配，适合短查询和长查询。"},
        {"id": "doc_4", "content": "重排序使用 Cross-Encoder 对粗筛结果精排，将准确率从 0.5 提升到 0.7。"},
        {"id": "doc_5", "content": "产品 A 的供应商位于广东省，年产能超过 10 万件。"},
    ]

    # BM25 检索
    bm25 = BM25Retriever()
    bm25.index(corpus)
    print("=== BM25 检索 ===")
    for h in bm25.retrieve("RAG 优化策略", top_k=3):
        print(f"  [{h.id}] score={h.score:.3f}  {h.content[:40]}")

    # 混合检索（BM25 + BM25，等权示例）
    hybrid = HybridRetriever(left=BM25Retriever(), right=BM25Retriever(), weight=0.7)
    hybrid.index(corpus)
    print("\n=== 混合检索 ===")
    for h in hybrid.retrieve("RAG 优化策略", top_k=3):
        print(f"  [{h.id}] score={h.score:.3f}  {h.content[:40]}")
