"""v8.5 — BM25 稀疏检索索引
与向量检索并行，三路融合: BM25 + Vector + Keyword → RRF
"""
from __future__ import annotations

import logging
import math
import re
from collections import defaultdict

logger = logging.getLogger(__name__)


class BM25Index:

    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self._k1 = k1
        self._b = b
        self._documents: dict[str, dict] = {}
        self._term_freq: dict[str, dict[str, int]] = defaultdict(dict)
        self._total_length = 0
        self._avg_length = 0.0

    def add(self, doc_id: str, content: str, extra: dict = None):
        tokens = self._tokenize(content)
        self._documents[doc_id] = {
            "content": content,
            "tokens": tokens,
            "length": len(tokens),
            "extra": extra or {},
        }
        tf = defaultdict(int)
        for t in tokens:
            tf[t] += 1
        self._term_freq[doc_id] = dict(tf)
        self._total_length += len(tokens)
        if self._documents:
            self._avg_length = self._total_length / len(self._documents)

    def remove(self, doc_id: str):
        self._documents.pop(doc_id, None)
        self._term_freq.pop(doc_id, None)
        self._total_length = 0
        for d in self._documents.values():
            self._total_length += d["length"]
        if self._documents:
            self._avg_length = self._total_length / len(self._documents)

    def search(self, query: str, top_k: int = 20) -> list[dict]:
        if not self._documents:
            return []

        tokens = self._tokenize(query)
        N = len(self._documents)
        scores = []

        for doc_id, doc in self._documents.items():
            score = 0.0
            dl = doc["length"]
            tf = self._term_freq.get(doc_id, {})
            for t in tokens:
                f = tf.get(t, 0)
                if f == 0:
                    continue
                n_t = sum(1 for di in self._term_freq if t in self._term_freq[di])
                idf = math.log((N - n_t + 0.5) / (n_t + 0.5) + 1.0)
                numerator = f * (self._k1 + 1.0)
                denominator = f + self._k1 * (1.0 - self._b + self._b * dl / self._avg_length)
                score += idf * numerator / denominator
            if score > 0:
                scores.append({
                    "id": doc_id,
                    "bm25_score": score,
                    "content": doc["content"],
                    **doc["extra"],
                })

        scores.sort(key=lambda x: -x["bm25_score"])
        return scores[:top_k]

    def get_stats(self) -> dict:
        return {
            "documents": len(self._documents),
            "vocabulary": sum(len(tf) for tf in self._term_freq.values()),
            "avg_length": round(self._avg_length, 1),
            "k1": self._k1,
            "b": self._b,
        }

    def _tokenize(self, text: str) -> list[str]:
        tokens = []
        for chunk in re.findall(r'[\u4e00-\u9fff]+|[a-zA-Z0-9]+', text.lower()):
            if re.match(r'[\u4e00-\u9fff]', chunk):
                for c in chunk:
                    if '\u4e00' <= c <= '\u9fff':
                        tokens.append(c)
                if len(chunk) >= 2:
                    for i in range(len(chunk) - 1):
                        tokens.append(chunk[i:i + 2])
                if len(chunk) >= 3:
                    tokens.append(chunk)
            elif len(chunk) >= 2:
                tokens.append(chunk)
        return tokens