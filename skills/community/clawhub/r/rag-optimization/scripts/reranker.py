#!/usr/bin/env python3
"""
重排序器（Reranker）
=====================
补全 config-template.json 中声明但未实现的 reranking 功能。

两阶段检索：
    粗筛（top-50）→ 重排序（top-5）

降级行为：无重排序模型时，使用 BM25 分数作为 fallback。

使用方式：
    from reranker import Reranker

    # 方式 1：使用 bge-reranker 模型（需安装 sentence-transformers）
    reranker = Reranker(model_name="BAAI/bge-reranker-base")
    top_k = reranker.rerank("RAG 优化策略是什么？", candidates, top_k=5)

    # 方式 2：无模型时自动降级
    reranker = Reranker()
    top_k = reranker.rerank("RAG 优化策略是什么？", candidates, top_k=5)
"""
import logging
import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# ============================================================
# 重排序结果数据类
# ============================================================

@dataclass
class RerankResult:
    """重排序结果"""
    rank: int                          # 排序位置（从 1 开始）
    original_rank: int                 # 原始排序位置
    document_id: str                   # 文档 ID
    content: str                       # 文档内容
    score: float                       # 重排序分数
    delta: float = 0.0                 # 与原始排名的差值


# ============================================================
# 重排序器
# ============================================================

class Reranker:
    """
    重排序器：对粗筛结果进行二次精排。

    支持两种模式：
    - bge-reranker（推荐）：使用 BAAI 的交叉编码器模型
    - cross-encoder（备选）：使用 ms-marco 系列模型
    - fallback（降级）：使用 BM25 关键词匹配分数

    模型推荐：
    - 英文：cross-encoder/ms-marco-MiniLM-L-6-v2（快速）
            cross-encoder/ms-marco-MiniLM-L-12-v2（高精度）
    - 中文：BAAI/bge-reranker-base（基础）
            BAAI/bge-reranker-large（高精度）
    """

    # 内置模型配置
    _MODELS = {
        'BAAI/bge-reranker-base': {
            'language': 'zh',
            'type': 'bge',
            'speed': 'fast',
            'accuracy': 'medium'
        },
        'BAAI/bge-reranker-large': {
            'language': 'zh',
            'type': 'bge',
            'speed': 'slow',
            'accuracy': 'high'
        },
        'cross-encoder/ms-marco-MiniLM-L-6-v2': {
            'language': 'en',
            'type': 'cross-encoder',
            'speed': 'fast',
            'accuracy': 'medium'
        },
        'cross-encoder/ms-marco-MiniLM-L-12-v2': {
            'language': 'en',
            'type': 'cross-encoder',
            'speed': 'slow',
            'accuracy': 'high'
        },
    }

    def __init__(self,
                 model_name: str = "BAAI/bge-reranker-base",
                 batch_size: int = 32,
                 config: Dict = None):
        """
        Args:
            model_name: 重排序模型名称
            batch_size: 批量大小（影响速度 vs 显存）
            config: 其他配置
        """
        self.config = config or {}
        self.model_name = model_name
        self.batch_size = batch_size
        self._model = None
        self._mode = "fallback"

        # 尝试加载模型
        self._load_model()

    def _load_model(self):
        """尝试加载交叉编码器模型。"""
        if self.model_name not in self._MODELS:
            logger.warning(f"未知模型 {self.model_name}，使用 fallback 模式")
            return

        try:
            from sentence_transformers import CrossEncoder
            self._model = CrossEncoder(self.model_name, max_length=512)
            self._mode = "bge" if "bge" in self.model_name else "cross-encoder"
            logger.info(f"重排序模型加载成功: {self.model_name} ({self._mode})")
        except ImportError:
            logger.info("sentence-transformers 未安装，使用 fallback 重排序（BM25 关键词匹配）")
        except Exception as e:
            logger.warning(f"模型加载失败 ({e})，使用 fallback 重排序")

    def rerank(self,
               query: str,
               candidates: List[Dict],
               top_k: int = 5) -> List[RerankResult]:
        """
        对候选文档进行重排序。

        Args:
            query: 用户查询
            candidates: 候选文档列表，每个元素为 dict：
                {"id": str, "content": str, "score": float (optional)}
            top_k: 返回数量

        Returns:
            重排序后的结果列表
        """
        if not candidates:
            return []

        if self._mode in ("bge", "cross-encoder"):
            return self._model_rerank(query, candidates, top_k)
        else:
            return self._fallback_rerank(query, candidates, top_k)

    def _model_rerank(self,
                      query: str,
                      candidates: List[Dict],
                      top_k: int) -> List[RerankResult]:
        """使用交叉编码器模型进行重排序。"""
        import numpy as np

        pairs = []
        valid_indices = []
        for i, doc in enumerate(candidates):
            doc_text = doc.get('content', doc.get('text', ''))
            if doc_text.strip():
                pairs.append([query, doc_text])
                valid_indices.append(i)

        if not pairs:
            return []

        # 批量计算分数
        scores = self._model.predict(pairs, batch_size=self.batch_size)
        scores = scores.tolist() if hasattr(scores, 'tolist') else [float(s) for s in scores]

        # 构建结果并排序
        results = []
        for j, (idx, score) in enumerate(zip(valid_indices, scores)):
            doc = candidates[idx]
            results.append(RerankResult(
                rank=0,  # 稍后设置
                original_rank=j + 1,
                document_id=doc.get('id', f"doc_{idx}"),
                content=doc.get('content', doc.get('text', '')),
                score=float(score)
            ))

        # 按分数降序排序
        results.sort(key=lambda r: r.score, reverse=True)

        # 设置最终排名
        for i, result in enumerate(results[:top_k]):
            result.rank = i + 1
            result.delta = result.original_rank - result.rank

        return results[:top_k]

    def _fallback_rerank(self,
                         query: str,
                         candidates: List[Dict],
                         top_k: int) -> List[RerankResult]:
        """
        Fallback 模式：使用 BM25 风格的关键词匹配重排。

        当无交叉编码器模型时，基于查询词在文档中的覆盖度和位置计算分数。
        """
        query_words = self._tokenize(query)
        if not query_words:
            return []

        results = []
        for i, doc in enumerate(candidates):
            doc_text = doc.get('content', doc.get('text', ''))
            score = self._keyword_score(query_words, doc_text)
            results.append(RerankResult(
                rank=0,
                original_rank=i + 1,
                document_id=doc.get('id', f"doc_{i}"),
                content=doc_text,
                score=score
            ))

        results.sort(key=lambda r: r.score, reverse=True)

        for i, result in enumerate(results[:top_k]):
            result.rank = i + 1
            result.delta = result.original_rank - result.rank

        return results[:top_k]

    # ------------------------------------------------------------------
    # 辅助方法
    # ------------------------------------------------------------------

    @staticmethod
    def _tokenize(text: str) -> List[str]:
        """中英文兼容分词。"""
        text = text.lower()
        tokens = []
        for w in re.findall(r'[a-z0-9]+', text):
            if len(w) >= 2:
                tokens.append(w)
        for ch in re.findall(r'[一-鿿]', text):
            tokens.append(ch)
        return tokens

    @staticmethod
    def _keyword_score(query_words: List[str], doc_text: str) -> float:
        """计算查询词在文档中的匹配分数。"""
        doc_lower = doc_text.lower()
        doc_words = doc_lower.replace(' ', '')

        if not query_words:
            return 0.0

        total_score = 0.0
        for word in query_words:
            if word in doc_words:
                # 词频加分
                count = doc_words.count(word)
                total_score += min(2.0, 1.0 + count * 0.1)
            elif word and len(word) > 1:
                # 部分匹配（前缀）
                if doc_words.startswith(word[:3]):
                    total_score += 0.3

        return total_score / len(query_words)

    def get_stats(self, query: str, candidates: List[Dict]) -> Dict[str, Any]:
        """
        获取重排序统计信息。

        Returns:
            包含排序质量指标的字典
        """
        if not candidates:
            return {}

        # 用 fallback 模式计算（不依赖模型）
        query_words = self._tokenize(query)
        covered = 0
        for doc in candidates:
            doc_text = doc.get('content', doc.get('text', ''))
            if any(w in doc_text.lower().replace(' ', '') for w in query_words):
                covered += 1

        return {
            'total_candidates': len(candidates),
            'keyword_coverage': covered / len(candidates),
            'mode': self._mode
        }


# ============================================================
# 使用示例
# ============================================================

if __name__ == '__main__':
    # 示例候选文档
    candidates = [
        {"id": "doc_1", "content": "RAG（检索增强生成）是一种结合信息检索和生成模型的技术，能降低幻觉。",
         "score": 0.85},
        {"id": "doc_2", "content": "由小到大检索是RAG优化的核心策略，用小块检索，返回大块上下文。",
         "score": 0.90},
        {"id": "doc_3", "content": "重排序使用Cross-Encoder对粗筛结果精排，将准确率从0.5提升到0.7。",
         "score": 0.80},
        {"id": "doc_4", "content": "混合检索结合向量语义与BM25关键词匹配，适合短查询和长查询。",
         "score": 0.75},
        {"id": "doc_5", "content": "产品A的供应商位于广东省，年产能超过10万件。",
         "score": 0.60},
    ]

    # 初始化重排序器（无模型时自动 fallback）
    reranker = Reranker()

    # 执行重排序
    results = reranker.rerank("RAG 优化策略", candidates, top_k=3)

    print("=== 重排序结果 ===")
    for r in results:
        print(f"  [{r.rank}] {r.document_id} | score={r.score:.3f} | delta={r.delta:+.0f}")
        print(f"       {r.content[:50]}...")
        print()

    # 统计信息
    stats = reranker.get_stats("RAG 优化策略", candidates)
    print(f"重排序模式: {stats.get('mode', 'unknown')}")
    print(f"关键词覆盖率: {stats.get('keyword_coverage', 0):.0%}")
