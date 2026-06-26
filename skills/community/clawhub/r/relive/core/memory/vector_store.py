"""
BM25 检索：持久化存 documents/metadatas/ids，加载时建索引，查询返回按相关度排序的结果。
不做 embedding，不依赖 Chroma/FAISS，仅依赖 rank_bm25。
"""
import json
import logging
import os
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)


def _tokenize(text: str) -> List[str]:
    """字符级分词，避免引入 jieba 等依赖。"""
    return list(text) if text else []


class VectorStore:
    def __init__(
        self,
        persist_directory: str,
        collection_name: str = "relive",
    ):
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        self.persist_path = persist_directory
        self._documents: List[str] = []
        self._metadatas: List[Dict] = []
        self._ids: List[str] = []
        self._bm25 = None

    def _load_index(self):
        if not self.persist_path:
            return
        bm25_file = os.path.join(self.persist_path, "bm25_index.json")
        tfidf_file = os.path.join(self.persist_path, "tfidf_index.json")
        if os.path.exists(bm25_file):
            try:
                with open(bm25_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self._documents = data.get("documents", [])
                self._metadatas = data.get("metadatas", [])
                self._ids = data.get("ids", [])
            except Exception as e:
                logger.warning("Failed to load BM25 index: %s", e)
        elif os.path.exists(tfidf_file):
            try:
                with open(tfidf_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self._documents = data.get("documents", [])
                self._metadatas = data.get("metadatas", [])
                self._ids = data.get("ids", [])
                self._save_index()
            except Exception as e:
                logger.warning("Failed to migrate from tfidf index: %s", e)

    def _save_index(self):
        if not self.persist_path:
            return
        os.makedirs(self.persist_path, exist_ok=True)
        index_file = os.path.join(self.persist_path, "bm25_index.json")
        with open(index_file, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "documents": self._documents,
                    "metadatas": self._metadatas,
                    "ids": self._ids,
                },
                f,
                ensure_ascii=False,
            )

    def _build_bm25(self):
        if not self._documents:
            self._bm25 = None
            return
        try:
            from rank_bm25 import BM25Okapi
        except ImportError:
            logger.warning("rank_bm25 not installed, pip install rank_bm25")
            self._bm25 = None
            return
        tokenized = [_tokenize(d) for d in self._documents]
        self._bm25 = BM25Okapi(tokenized)

    def add_texts(
        self,
        texts: List[str],
        metadatas: Optional[List[Dict]] = None,
        ids: Optional[List[str]] = None,
    ):
        self._load_index()
        if ids is None:
            ids = [f"doc_{len(self._documents) + i}" for i in range(len(texts))]
        if metadatas is None:
            metadatas = [{} for _ in texts]
        self._documents.extend(texts)
        self._metadatas.extend(metadatas)
        self._ids.extend(ids)
        self._save_index()
        self._build_bm25()

    def similarity_search(
        self,
        query: str,
        k: int = 5,
        filter_metadata: Optional[Dict] = None,
    ) -> List[Dict[str, Any]]:
        self._load_index()
        self._build_bm25()
        if not self._bm25 or not self._documents:
            return []
        tokenized_query = _tokenize(query)
        scores = self._bm25.get_scores(tokenized_query)
        top_indices = scores.argsort()[::-1][:k]
        out = []
        for i in top_indices:
            score = max(float(scores[i]), 1e-9)
            out.append({
                "content": self._documents[i],
                "metadata": self._metadatas[i] if i < len(self._metadatas) else {},
                "distance": 1.0 / (1.0 + score),
                "index": int(i),
                "id": self._ids[i] if i < len(self._ids) else f"doc_{i}",
            })
        return out

    def get_document_at(self, index: int) -> Optional[Dict[str, Any]]:
        """按下标取一条文档，用于拼上下文。"""
        self._load_index()
        if index < 0 or index >= len(self._documents):
            return None
        return {
            "content": self._documents[index],
            "metadata": self._metadatas[index] if index < len(self._metadatas) else {},
        }

    def delete(self, ids: Optional[List[str]] = None):
        self._load_index()
        if not ids:
            return
        to_drop = [i for i, id_ in enumerate(self._ids) if id_ in ids]
        for i in reversed(to_drop):
            del self._documents[i]
            del self._metadatas[i]
            del self._ids[i]
        self._save_index()
        self._build_bm25()

    def clear(self):
        self._documents = []
        self._metadatas = []
        self._ids = []
        self._bm25 = None
        self._save_index()
