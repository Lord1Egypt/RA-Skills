#!/usr/bin/env python3
"""
v20.50 P3-22 Vector DB 语义搜索 (2026-06-15)
- BM25 算法 (Okapi BM25)
- 内存索引 (无 ChromaDB 依赖, 纯 Python)
- 中文友好 (jieba 分词 - 备选, 先用字符 n-gram)
- 端点: POST /v1/semantic_search {query, num=10}
- 缓存: 30min (query 归一化 key)
- 数据源: 走 16 引擎 search + 用结果集建索引
"""
import re
import math
import time
import asyncio
import hashlib
import json
import os
from collections import Counter
from typing import List, Dict, Tuple

# ==================== 中文友好分词 ====================
# 字符级 n-gram (2-3 字符) 兼顾中英文
def _tokenize(text: str) -> List[str]:
    """字符 n-gram + 英文词混合"""
    if not text:
        return []
    text = text.lower().strip()
    # 英文/数字按词切
    words = re.findall(r'[a-z0-9]+', text)
    # 中文字符 2-gram
    cn_chars = re.findall(r'[\u4e00-\u9fa5]+', text)
    cn_grams = []
    for s in cn_chars:
        for i in range(len(s) - 1):
            cn_grams.append(s[i:i+2])
        if len(s) >= 1:
            cn_grams.append(s)  # 单字
    return words + cn_grams

# ==================== BM25 索引 ====================
class BM25Index:
    """Okapi BM25 内存索引 - v20.50 v1 简化版"""

    def __init__(self, k1=1.5, b=0.75):
        self.k1 = k1
        self.b = b
        self.docs = []           # [{id, title, url, summary, text, tokens}]
        self.doc_lens = []       # [len_tokens]
        self.avgdl = 0.0
        self.df = Counter()      # doc freq
        self.tf = []             # [[(term_idx, freq), ...], ...]
        self.idf = {}            # term -> idf
        self._cache = {}         # query_hash -> [(score, doc_idx), ...]

    def add(self, docs: List[Dict]):
        """批量加文档"""
        for doc in docs:
            text = f"{doc.get('title','')} {doc.get('summary','')}"
            tokens = _tokenize(text)
            if not tokens:
                tokens = ['__empty__']
            doc['tokens'] = tokens
            self.docs.append(doc)
            self.doc_lens.append(len(tokens))
            # tf
            tf_dict = Counter(tokens)
            self.tf.append(tf_dict)
            # df
            for term in set(tokens):
                self.df[term] += 1
        # 算 avgdl + idf
        N = len(self.docs)
        self.avgdl = sum(self.doc_lens) / max(N, 1)
        self.idf = {term: math.log((N - df + 0.5) / (df + 0.5) + 1.0)
                    for term, df in self.df.items()}
        # 清缓存
        self._cache.clear()

    def search(self, query: str, num: int = 10) -> List[Tuple[float, Dict]]:
        """BM25 检索 - 返 [(score, doc), ...]"""
        # 缓存
        q_hash = hashlib.md5(f"{query}|{num}|{len(self.docs)}".encode()).hexdigest()[:16]
        if q_hash in self._cache:
            return [(s, self.docs[i]) for s, i in self._cache[q_hash]]

        q_tokens = _tokenize(query)
        if not q_tokens or not self.docs:
            return []

        scores = []
        for i, tf_dict in enumerate(self.tf):
            score = 0.0
            doc_len = self.doc_lens[i]
            for qt in q_tokens:
                if qt in tf_dict and qt in self.idf:
                    f = tf_dict[qt]
                    idf = self.idf[qt]
                    numerator = f * (self.k1 + 1)
                    denominator = f + self.k1 * (1 - self.b + self.b * doc_len / max(self.avgdl, 1))
                    score += idf * numerator / denominator
            if score > 0:
                scores.append((score, i))
        # 排序
        scores.sort(reverse=True)
        result = scores[:num]
        # 缓存
        self._cache[q_hash] = result
        return [(s, self.docs[i]) for s, i in result]

    def size(self):
        return len(self.docs)

    def clear(self):
        self.docs.clear()
        self.doc_lens.clear()
        self.df.clear()
        self.tf.clear()
        self.idf.clear()
        self._cache.clear()

# ==================== 全局索引 ====================
_index = BM25Index()
_index_lock = asyncio.Lock()

async def index_results(query: str, results: List[Dict]):
    """把搜索结果加入索引 (异步, 后续可改持久化)"""
    async with _index_lock:
        if _index.size() > 5000:  # 防止内存爆
            _index.clear()
        # 把 query 也加进去, 让 "类似 query" 也能命中
        docs_to_add = list(results) + [{
            'title': query,
            'url': '',
            'summary': query,
            'engine': 'query_seed',
        }]
        _index.add(docs_to_add)

async def semantic_search(query: str, num: int = 10) -> List[Dict]:
    """语义搜索 - 返 doc dict 列表"""
    async with _index_lock:
        results = _index.search(query, num)
    out = []
    for score, doc in results:
        out.append({
            'title': doc.get('title', ''),
            'url': doc.get('url', ''),
            'summary': doc.get('summary', ''),
            'engine': doc.get('engine', 'semantic_bm25'),
            'category': doc.get('category', ''),
            'date': doc.get('date', ''),
            'score': round(score, 2),
        })
    return out

def get_index_stats() -> Dict:
    """看索引状态"""
    return {
        'docs': _index.size(),
        'vocab': len(_index.df),
        'avgdl': round(_index.avgdl, 1),
        'cache_size': len(_index._cache),
    }
