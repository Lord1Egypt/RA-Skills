# -*- coding: utf-8 -*-
"""
BM25 检索器（纯标准库实现）
===========================
让 config-template.json 中的 hybrid 检索策略真正可运行：
- bm25:     Okapi BM25 关键词检索（零依赖）
- vector:   语义检索（需 embedding_model，未配置时回退 bm25）
- hybrid:   α·vector + (1-α)·bm25 加权融合

文档契约（与 self_rag.py 保持一致）：
    documents = [{"id": str, "text": str, "metadata": dict, ...}]
    retrieve() 返回按相关性降序的文档列表（含 score 字段）

运行 demo：
    python bm25_retriever.py
"""
import json
import logging
import math
import re
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

# Phase 1 数据协议集成：继承统一检索器基类
from retriever_base import BaseRetriever
from functools import lru_cache
from collections import OrderedDict

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@dataclass
class RetrievalResult:
    """检索结果（兼容 RetrievalHit 接口，增加 content 属性）"""
    id: str
    text: str
    score: float = 0.0
    metadata: Dict = field(default_factory=dict)

    @property
    def content(self) -> str:
        """兼容 retriever_base.RetrievalHit 的 content 字段"""
        return self.text


class BM25Retriever(BaseRetriever):
    """
    Okapi BM25 检索器，支持 bm25 / vector / hybrid 三种策略。
    纯标准库实现，中英文兼容分词。
    继承 retriever_base.BaseRetriever，与 VectorRetriever/HybridRetriever 可组合。
    """

    # 中文停用字（与 segment_extractor 保持一致）
    _STOP_CHARS = set('的了吗呢啊吧么呀哦哈什么如何怎样怎么是否与和或等这那之以及于被把让给有没有没')

    def __init__(self, config: Dict = None, embedding_model=None):
        """
        Args:
            config: 检索配置（k1/b 参数、vector_weight 等）
            embedding_model: 可选向量模型，需提供 encode(texts) -> List[List[float]]
        """
        self.config = config or {}
        self.k1 = self.config.get('k1', 1.5)                # BM25 词频饱和参数
        self.b = self.config.get('b', 0.75)                 # 文档长度归一化参数
        # R9: 混合权重校验与归一化
        self.vector_weight = self.config.get('vector_weight', 0.7)
        if self.vector_weight < 0 or self.vector_weight > 1.0:
            logger.warning(f"vector_weight ({self.vector_weight}) 超出 [0, 1]，限制为 0.7")
            self.vector_weight = 0.7
        self.bm25_weight = 1.0 - self.vector_weight  # 自动计算
        self.embedding_model = embedding_model

        self._documents: Dict[str, dict] = {}               # id -> doc
        self._doc_freq: Dict[str, int] = {}                 # term -> 含该词的文档数
        self._doc_terms: Dict[str, Dict[str, int]] = {}     # id -> term -> 词频
        self._doc_lens: Dict[str, int] = {}                 # id -> 词数
        self._avgdl: float = 0.0
        self._idf_cache: Dict[str, float] = {}              # R7: 预计算 IDF 缓存
        self._indexed = False
        # R8: 嵌入模型指纹（用于维度迁移检测）
        self._embedding_model_fingerprint = id(self.embedding_model) if self.embedding_model else None
        # Phase 2b: LRU 查询缓存（性能缓存，减少重复检索）
        # R5: 真正 LRU 缓存（OrderedDict 支持 O(1) 淘汰）
        #
        # H18：缓存条目带写入时间戳，兑现 config-template 里
        # `performance.cache.cache_ttl_seconds` 的承诺——此前该配置项零消费者，
        # 缓存一旦写入便永久有效，索引内容更新后（若调用方忘了 invalidate_cache）
        # 会无限期返回陈旧结果。
        # 结构：cache_key -> (写入时间戳, 结果列表)
        self._query_cache: "OrderedDict[str, Tuple[float, List[RetrievalResult]]]" = OrderedDict()
        self._cache_max_size = self.config.get("cache_max_size", 128)
        # ttl <= 0 或 None 视为「不过期」，与 cache_ttl_seconds=0 的直觉一致
        ttl = self.config.get("cache_ttl_seconds", 3600)
        self._cache_ttl_seconds = ttl if (ttl is not None and ttl > 0) else None

    # ------------------------------------------------------------------
    # 分词
    # ------------------------------------------------------------------
    @classmethod
    def _tokenize(cls, text: str) -> List[str]:
        """中英文兼容分词：英文/数字词 + 中文单字（过滤停用字）"""
        text = text.lower()
        tokens = []
        for w in re.findall(r'[a-z0-9]+', text):
            if len(w) >= 2:
                tokens.append(w)
        for ch in re.findall(r'[\u4e00-\u9fff]', text):
            if ch not in cls._STOP_CHARS:
                tokens.append(ch)
        return tokens

    # ------------------------------------------------------------------
    # 索引
    # ------------------------------------------------------------------
    def index(self, documents: List[Dict]) -> int:
        """
        建立索引（兼容 retriever_base.BaseRetriever 接口）。
        
        文档格式：[{"id": str, "content": str, "metadata": dict}] 或
                  [{"id": str, "text": str, "metadata": dict}]
        自动兼容 content 和 text 两种键名。
        """
        # 将 content 键映射为 text（本模块内部统一使用 text）
        normalized = []
        for doc in documents:
            d = dict(doc)
            if 'content' in d and 'text' not in d:
                d['text'] = d['content']
            normalized.append(d)
        return self.index_documents(normalized)

    def _invalidate_caches(self) -> None:
        """
        H6/H7 单一职责点：**任何**使索引发生变化的操作都必须调用本方法。

        此前失效逻辑只在 add_document() 里手写了一次，且只清了 _query_cache，
        导致 index_documents() 重建索引后：
          - _idf_cache 仍是旧文档集的 IDF（H6，分数静默失真）
          - _query_cache 仍返回已被删除的文档（H7）
        """
        # IDF 缓存：文档集变了，旧的 IDF 不再适用
        self._idf_cache = {}
        # 查询缓存：旧结果可能引用已不存在的文档
        if hasattr(self, "_query_cache"):
            self._query_cache.clear()

    def invalidate_cache(self) -> None:
        """
        对外的缓存失效接口（H13：SKILL.md「架构约束」承诺的方法）。

        索引变更后调用本方法。与重建索引内部走的是同一个 _invalidate_caches()，
        不存在两份逻辑。
        """
        self._invalidate_caches()
        logger.info("已失效 IDF 缓存与查询缓存")

    def index_documents(self, documents: List[dict]) -> int:
        """建立 BM25 索引。documents: [{"id", "text", "metadata"?}]"""
        # H6/H7：重建索引同样要让 IDF 与查询缓存失效
        self._invalidate_caches()

        self._documents = {}
        self._doc_freq = {}
        self._doc_terms = {}
        self._doc_lens = {}
        total_len = 0

        for doc in documents:
            doc_id = str(doc.get('id', len(self._documents)))
            text = doc.get('text', '')
            terms = self._tokenize(text)
            self._documents[doc_id] = doc
            self._doc_terms[doc_id] = {}
            for term in terms:
                self._doc_terms[doc_id][term] = self._doc_terms[doc_id].get(term, 0) + 1
            self._doc_lens[doc_id] = len(terms)
            total_len += len(terms)

        # 文档频率（DF）
        for terms in self._doc_terms.values():
            for term in terms:
                self._doc_freq[term] = self._doc_freq.get(term, 0) + 1

        n = len(self._documents)
        self._avgdl = total_len / n if n else 0.0
        self._indexed = n > 0
        logger.info(f"已索引 {n} 篇文档，平均长度 {self._avgdl:.1f} 词")
        return n

    def _add_single_document(self, doc: dict) -> None:
        """内部方法：增量添加单篇文档，不重置已有索引"""
        doc_id = str(doc.get('id', len(self._documents)))
        text = doc.get('text', '')
        terms = self._tokenize(text)
        self._documents[doc_id] = doc
        self._doc_terms[doc_id] = {}
        for term in terms:
            self._doc_terms[doc_id][term] = self._doc_terms[doc_id].get(term, 0) + 1
        self._doc_lens[doc_id] = len(terms)
        # 更新文档频率
        for term in terms:
            self._doc_freq[term] = self._doc_freq.get(term, 0) + 1
        # 更新平均文档长度
        n = len(self._documents)
        total_len = sum(self._doc_lens.values())
        self._avgdl = total_len / n if n else 0.0
        self._indexed = n > 0

    def add_document(self, doc: dict) -> None:
        """增量添加单篇文档。
        
        修复 Bug 5：旧实现调用 index_documents([doc]) 会重置所有索引状态，
        导致每次 add 覆盖已有数据。现改用 _add_single_document 增量更新。
        R7: 添加后触发 IDF 增量重算。
        """
        if self._indexed:
            self._add_single_document(doc)
            # H6/H7：先失效全部缓存，再按新文档集重算 IDF
            #（顺序不能颠倒——先算后清会把刚算好的 IDF 一起清掉）
            self._invalidate_caches()
            # R7: 增量添加后重新计算 IDF
            self._recalc_idf()
        else:
            self.index_documents([doc])

    def _recalc_idf(self) -> None:
        """R7: 基于当前完整文档集合重新计算 IDF 缓存"""
        n = len(self._documents)
        if n == 0:
            return
        self._idf_cache = {}
        for term, df in self._doc_freq.items():
            self._idf_cache[term] = math.log((n - df + 0.5) / (df + 0.5) + 1.0)

    # ------------------------------------------------------------------
    # 评分
    # ------------------------------------------------------------------
    def _idf(self, term: str, n: int) -> float:
        df = self._doc_freq.get(term, 0)
        return math.log((n - df + 0.5) / (df + 0.5) + 1.0)

    def _bm25_score(self, query_terms: List[str], doc_id: str, n: int,
                    k1: float = None, b: float = None) -> float:
        """
        Okapi BM25 打分。

        Args:
            k1 / b: 本次调用使用的参数；缺省时回退到实例属性 self.k1 / self.b。
                    H5：self_rag 重试时传入变体参数，这里必须真正生效。
        """
        k1 = self.k1 if k1 is None else k1
        b = self.b if b is None else b
        score = 0.0
        doc_len = self._doc_lens.get(doc_id, 0)
        terms = self._doc_terms.get(doc_id, {})
        for term in query_terms:
            tf = terms.get(term, 0)
            if tf == 0:
                continue
            # R7: 优先使用预计算 IDF 缓存，回退到实时计算
            idf = self._idf_cache.get(term, self._idf(term, n))
            denom = tf + k1 * (1 - b + b * (doc_len / self._avgdl if self._avgdl else 1.0))
            score += idf * (tf * (k1 + 1)) / denom
        return score

    def _encode_query_once(self, query: str):
        """预编码查询向量（修复 Bug 12：避免每篇文档重复编码）"""
        if not self.embedding_model:
            return None
        try:
            import numpy as np
            vec = self.embedding_model.encode([query])[0]
            q_vec = np.array(vec)
            return q_vec
        except Exception as e:
            logger.error(f"查询向量编码失败: {e}")
            return None

    def _cosine_similarity(self, query_vec, doc_text: str) -> float:
        """计算预编码查询向量与文档的余弦相似度"""
        if not query_vec or not self.embedding_model:
            return 0.0
        try:
            import numpy as np
            d_vec = np.array(self.embedding_model.encode([doc_text])[0])
            dot = np.dot(query_vec, d_vec)
            denom = np.linalg.norm(query_vec) * np.linalg.norm(d_vec) + 1e-9
            return float(dot / denom)
        except Exception as e:
            logger.error(f"向量评分失败: {e}")
            return 0.0

    # ------------------------------------------------------------------
    # 检索
    # ------------------------------------------------------------------
    def retrieve(self, query: str, top_k: int = 10, strategy: str = 'hybrid', **kwargs) -> List[RetrievalResult]:
        """
        检索 top_k 相关文档。

        Args:
            query: 查询文本
            top_k: 返回数量
            strategy: bm25 / vector / hybrid

        Returns:
            [RetrievalResult, ...] 按分数降序

        Keyword Args:
            k1 / b: 覆盖本次检索使用的 BM25 参数（H5）。
                    self_rag 重试时会传不同变体，此前这些参数被收下后零引用，
                    导致"重试三次得到相同结果"的原缺陷并未真正修复。
            min_score: 相关性下限，缺省 0.0。得分 <= 下限的文档不进入结果集（H24）。
                       传 None 可关闭过滤，保留修复前的"零分文档也返回"行为。
        """
        if not self._indexed:
            raise RuntimeError("尚未建立索引，请先调用 index_documents()")

        # H5：真正消费 kwargs（此前 **kwargs 只是摆设）
        k1 = kwargs.get('k1', self.k1)
        b = kwargs.get('b', self.b)
        # H24：相关性下限。调用方可通过 min_score 放宽/收紧，缺省过滤零分文档。
        min_score = kwargs.get('min_score', 0.0)

        # R8: 嵌入模型变更检测（维度不匹配时自动触发重索引警告）
        if self.embedding_model and self._embedding_model_fingerprint:
            current_fp = id(self.embedding_model)
            if current_fp != self._embedding_model_fingerprint:
                logger.warning("嵌入模型已变更，请重建索引以确保向量维度一致")

        n = len(self._documents)
        query_terms = self._tokenize(query)
        if not query_terms:
            logger.warning("查询分词为空，返回空结果")
            return []

        # Bug 11 修复：无 embedding 时降级为纯 BM25，不打印 error
        if strategy in ('vector', 'hybrid') and not self.embedding_model:
            strategy = 'bm25'
            logger.debug(f"无 embedding_model，{strategy} 策略降级为 bm25")

        # 修复 Bug 12：预编码查询向量（避免每篇文档重复编码 N 次）
        # Phase 2b: 查询缓存（命中则直接返回，但注意 results 列表在后续赋值）
        query_vec = self._encode_query_once(query) if self.embedding_model else None

        # H5 配套环节②：cache key 必须含 k1/b，
        # 否则换了参数仍命中旧缓存，变体重试依旧拿到同一份结果。
        cache_key = f"{strategy}:{top_k}:{k1}:{b}:{min_score}:{query}"
        entry = self._query_cache.get(cache_key)
        if entry is not None:
            cached_at, cached_results = entry
            # H18：TTL 兑现。过期条目直接丢弃并重新计算，
            # 不再让配置里的 cache_ttl_seconds 形同虚设。
            if (self._cache_ttl_seconds is not None
                    and (time.time() - cached_at) > self._cache_ttl_seconds):
                del self._query_cache[cache_key]
                logger.debug(f"查询缓存条目已过期（TTL={self._cache_ttl_seconds}s），重新检索")
            else:
                # R5: LRU — 命中时移到末尾（最近访问）
                self._query_cache.move_to_end(cache_key)
                return cached_results

        results = []
        for doc_id, doc in self._documents.items():
            # H5 配套环节①：把 k1/b 真正传进打分函数。
            # 只从 kwargs 读出来而不往下传，等于修复只做了一半——self_rag 的变体重试
            # 依旧得到完全相同的分数。改实例属性之所以有效，正是因为那条路径绕过了
            # 这个漏传点，很容易在自测时被「看起来能用」掩盖过去。
            bm25 = self._bm25_score(query_terms, doc_id, n, k1=k1, b=b)
            doc_text = doc.get('text', '')

            if strategy == 'bm25':
                score = bm25
            elif strategy == 'vector':
                v = self._cosine_similarity(query_vec, doc_text) if self.embedding_model else 0.0
                score = v if self.embedding_model else bm25
            elif strategy == 'hybrid':
                v = self._cosine_similarity(query_vec, doc_text) if self.embedding_model else 0.0
                if self.embedding_model:
                    score = self.vector_weight * v + (1 - self.vector_weight) * bm25
                else:
                    score = bm25
            else:
                raise ValueError(f"未知检索策略: {strategy}（可选 bm25/vector/hybrid）")

            # H24：零分文档不进结果集。
            # BM25 得 0 分意味着与查询零词项重合。此前这类文档照样被返回，
            # 于是出现「查『检索』却返回只含『苹果 香蕉 橙子』的文档」——top_k
            # 被完全无关的文档填满，下游重排与生成拿到的是纯噪声。
            # 缓存失效修好之后这个缺陷才暴露出来：旧缓存本来会直接送回旧结果，
            # 掩盖了「重新算也会算出垃圾」这一层。
            # min_score=None 表示调用方显式要求关闭过滤（保留修复前行为）
            if min_score is not None and score <= min_score:
                continue

            results.append(RetrievalResult(
                id=doc_id,
                text=doc.get('text', ''),
                score=round(score, 4),
                metadata=doc.get('metadata', {}),
            ))

        results.sort(key=lambda r: r.score, reverse=True)
        logger.info(f"[{strategy}] 查询 {len(query_terms)} 词，返回 top-{min(top_k, len(results))}")
        top_results = results[:top_k]
        # H18 配套环节：max_size <= 0 表示缓存被显式关闭（对应配置里
        # performance.cache.query_cache_enabled=false）。不能只做 LRU 淘汰，
        # 否则 popitem() 会在空字典上抛 KeyError。
        if self._cache_max_size > 0:
            # R5: 真正 LRU 存储 — 超限时淘汰最久未访问条目
            if len(self._query_cache) >= self._cache_max_size:
                self._query_cache.popitem(last=False)  # 淘汰最久未访问
            self._query_cache[cache_key] = (time.time(), top_results)
        return top_results


if __name__ == '__main__':
    # 示例语料
    corpus = [
        {"id": "doc_1", "text": "RAG（检索增强生成）是一种结合信息检索和生成模型的技术，能显著降低大模型的幻觉问题。"},
        {"id": "doc_2", "text": "由小到大检索是RAG优化的核心策略：用小块检索，返回大块上下文，准确率可从0.3提升到0.85。"},
        {"id": "doc_3", "text": "混合检索结合向量语义与BM25关键词匹配，短查询偏关键词、长查询偏语义，权重α通常取0.5-0.8。"},
        {"id": "doc_4", "text": "重排序用Cross-Encoder对粗筛结果精排，可将准确率从0.5提升到0.7，常用模型包括BGE Reranker。"},
        {"id": "doc_5", "text": "产品A的供应商位于广东省，每年向全球提供超过10万件配件，交期约45天。"},
    ]
    retriever = BM25Retriever(config={'vector_weight': 0.7})
    retriever.index_documents(corpus)

    print("\n=== BM25 检索: 'RAG优化的核心策略' ===")
    for r in retriever.retrieve("RAG优化的核心策略", top_k=3, strategy='bm25'):
        print(f"  [{r.id}] score={r.score:.3f}  {r.text[:40]}")

    print("\n=== Hybrid 检索（无向量模型，退化 BM25）: 'RAG幻觉' ===")
    for r in retriever.retrieve("RAG幻觉", top_k=3, strategy='hybrid'):
        print(f"  [{r.id}] score={r.score:.3f}  {r.text[:40]}")

    print("\n=== 查询: '供应商在哪里' ===")
    for r in retriever.retrieve("供应商在哪里", top_k=3, strategy='bm25'):
        print(f"  [{r.id}] score={r.score:.3f}  {r.text[:40]}")
