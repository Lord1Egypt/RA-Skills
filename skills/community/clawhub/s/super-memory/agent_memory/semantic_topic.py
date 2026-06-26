"""
semantic_topic.py - 语义级主题匹配
用 embedding 向量余弦相似度替代关键词子串匹配
"""

from __future__ import annotations

import json
import logging
import os
import re
from pathlib import Path

logger = logging.getLogger(__name__)


class SemanticTopicMatcher:
    """
    基于向量相似度的语义主题匹配器。

    工作原理：
    1. 为每个主题构建代表文本（名称 + 关键词 + 描述）
    2. 编码为主题向量，持久化缓存
    3. 匹配时编码输入文本，计算与所有主题的余弦相似度
    4. 返回超过阈值的匹配主题，按相似度降序
    """

    DEFAULT_THRESHOLD = 0.35   # 语义相似度阈值（低于此值视为无匹配）
    TOP_K = 3                  # 最多返回的主题数

    def __init__(self, embedding_store=None, registry_path: str = None):
        """
        embedding_store: EmbeddingStore 实例（复用已有模型，避免重复加载）
        registry_path: dimensions.json 路径
        """
        self.embedding_store = embedding_store
        self._model = None
        self._model_load_attempted = False

        # 加载注册表
        reg_path = Path(registry_path) if registry_path else Path(__file__).parent / "dimensions.json"
        with open(reg_path, "r", encoding="utf-8") as f:
            self.registry = json.load(f)

        # 主题代表文本 {topic_path: representative_text}
        self._topic_texts: dict[str, str] = {}
        # 主题向量缓存 {topic_path: list[float]}
        self._topic_vectors: dict[str, list[float]] = {}
        # 缓存文件路径
        self._cache_path = Path(__file__).parent / "registry" / "topic_vectors_cache.json"

        self._build_topic_texts()
        self._load_cache()

    def _get_model(self):
        """延迟加载 embedding 模型（优先复用 embedding_store 的模型）"""
        if self._model is not None:
            return self._model
        # 已确定无法加载，不再重试
        if self._model_load_attempted:
            return None
        self._model_load_attempted = True
        if self.embedding_store and self.embedding_store._use_model:
            self._model = self.embedding_store.model
            return self._model
        # 独立加载（快速失败，不重试网络）
        try:
            from sentence_transformers import SentenceTransformer
            self._model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")
            logger.info("SemanticTopicMatcher: embedding model loaded")
        except Exception as e:
            logger.warning("semantic_topic: %s", e)
            self._model = None
        return self._model

    def _encode(self, text: str) -> list[float]:
        """编码文本为向量"""
        model = self._get_model()
        if model:
            return model.encode(text).tolist()
        # 降级：hash embedding（仅供测试，无语义能力）
        return self._hash_embedding(text)

    @staticmethod
    def _hash_embedding(text: str, dim: int = 384) -> list[float]:
        import hashlib
        h = hashlib.sha256(text.encode("utf-8")).digest()
        return [((h[(i * 7 + 3) % len(h)] / 255.0) * 2 - 1) for i in range(dim)]

    def _build_topic_texts(self):
        """
        为每个主题构建代表文本。
        格式：主题名称 + 关键词 + 上下文路径语义扩展
        """
        self._collect_topic_texts(self.registry["topics"], "")

    def _collect_topic_texts(self, node: dict, prefix: str):
        for key, val in node.items():
            full_path = f"{prefix}.{key}" if prefix else key
            name = val.get("name", key)
            keywords = val.get("keywords", [])

            # 代表文本 = 路径语义 + 名称 + 关键词
            # 路径本身也携带语义信息: "ai.rag.vdb" → "ai rag vdb"
            path_words = full_path.replace(".", " ")
            text_parts = [path_words, name]
            if keywords:
                text_parts.extend(keywords)
            self._topic_texts[full_path] = " ".join(text_parts)

            if "children" in val:
                self._collect_topic_texts(val["children"], full_path)

    def _load_cache(self):
        """从缓存文件加载已计算的向量"""
        if self._cache_path.exists():
            try:
                with open(self._cache_path, "r", encoding="utf-8") as f:
                    cache = json.load(f)
                # 验证缓存完整性：所有当前主题都有向量
                if all(t in cache for t in self._topic_texts):
                    self._topic_vectors = cache
                    logger.info(f"Loaded {len(cache)} topic vectors from cache")
                    return
            except Exception as e:
                logger.warning("semantic_topic: %s", e)
        # 缓存缺失或不完整，需要重新计算
        self._compute_all_vectors()

    def _compute_all_vectors(self):
        """计算所有主题的向量并缓存"""
        logger.info(f"Computing vectors for {len(self._topic_texts)} topics...")
        for topic_path, text in self._topic_texts.items():
            self._topic_vectors[topic_path] = self._encode(text)
        self._save_cache()
        logger.info(f"Computed and cached {len(self._topic_vectors)} topic vectors")

    def _save_cache(self):
        """持久化向量缓存"""
        self._cache_path.parent.mkdir(parents=True, exist_ok=True)
        tmp = str(self._cache_path) + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(self._topic_vectors, f)
        os.replace(tmp, str(self._cache_path))

    def refresh_vectors(self):
        """强制重新计算所有向量（如注册表有变更时调用）"""
        self._compute_all_vectors()

    def add_topic_vector(self, topic_path: str, keywords: list[str] = None):
        """为新注册的主题计算并缓存向量"""
        if topic_path in self._topic_vectors:
            return

        # 构建代表文本
        path_words = topic_path.replace(".", " ")
        name = topic_path.split(".")[-1]
        parts = [path_words, name]
        if keywords:
            parts.extend(keywords)
        text = " ".join(parts)

        self._topic_texts[topic_path] = text
        self._topic_vectors[topic_path] = self._encode(text)
        self._save_cache()
        logger.info(f"Added vector for new topic: {topic_path}")

    def match(self, text: str, top_k: int = None, threshold: float = None) -> list[dict]:
        """
        语义匹配：找到与输入文本最相似的主题。

        参数:
            text: 输入文本
            top_k: 最多返回几个主题
            threshold: 最低相似度阈值

        返回: [{"topic": str, "score": float}, ...] 按 score 降序
        """
        top_k = top_k or self.TOP_K
        threshold = threshold or self.DEFAULT_THRESHOLD

        if not self._topic_vectors:
            return []

        query_vec = self._encode(text)
        scores = []

        for topic_path, topic_vec in self._topic_vectors.items():
            score = self._cosine_similarity(query_vec, topic_vec)
            if score >= threshold:
                scores.append({"topic": topic_path, "score": round(score, 4)})

        scores.sort(key=lambda x: -x["score"])

        # 去重父子关系：保留得分更高的
        filtered = []
        for item in scores:
            topic = item["topic"]
            is_child = any(topic.startswith(f["topic"] + ".") for f in filtered)
            is_parent = any(f["topic"].startswith(topic + ".") for f in filtered)
            if not is_child and not is_parent:
                filtered.append(item)
            if len(filtered) >= top_k:
                break

        return filtered

    @staticmethod
    def _cosine_similarity(a: list[float], b: list[float]) -> float:
        """计算两个向量的余弦相似度"""
        if len(a) != len(b):
            min_len = min(len(a), len(b))
            a = a[:min_len]
            b = b[:min_len]

        dot = sum(x * y for x, y in zip(a, b))
        norm_a = sum(x * x for x in a) ** 0.5
        norm_b = sum(x * x for x in b) ** 0.5

        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot / (norm_a * norm_b)

    def get_stats(self) -> dict:
        return {
            "total_topics": len(self._topic_vectors),
            "cache_path": str(self._cache_path),
            "cache_exists": self._cache_path.exists(),
            "model_loaded": self._model is not None,
            "threshold": self.DEFAULT_THRESHOLD,
        }
