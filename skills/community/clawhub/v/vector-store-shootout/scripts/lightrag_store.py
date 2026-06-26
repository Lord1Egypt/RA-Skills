"""LightRAG graph-enhanced vector store.

Combines cosine vector similarity with a lightweight entity-relationship
graph built at index time using regex-based NER. At query time, top cosine
matches are expanded via graph traversal to pull in related context that
pure vector search might miss.

Backend string: ``"lightrag"``

Graph model (v1):
    - **Nodes**: entities extracted via regex (capitalized phrases, numbers,
      technical terms like acronyms or hyphenated compounds).
    - **Edges**: co-occurrence within the same chunk. Edge weight = number
      of chunks where both entities appear together.

Query pipeline:
    1. Embed query → cosine similarity over corpus → top-k candidates
    2. Extract entities from top candidates
    3. Graph-expand: 1-hop neighbours of matched entities
    4. Retrieve chunks containing neighbour entities
    5. Deduplicate + blend (vector results first, then graph expansions)

No external API calls in the indexing path — all entity extraction is
regex-based for speed.
"""
from __future__ import annotations

import hashlib
import logging
import re
from collections import defaultdict
from typing import Callable, Optional

import networkx as nx

from .base import BaseVectorStore, RetrievedChunk

logger = logging.getLogger(__name__)

# Regex patterns for entity extraction
_CAPITALIZED_PHRASE = re.compile(r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b")
_ACRONYM = re.compile(r"\b([A-Z]{2,})\b")
_TECHNICAL_TERM = re.compile(r"\b([a-zA-Z]+-[a-zA-Z]+(?:-[a-zA-Z]+)*)\b")
_NUMBER_WITH_UNIT = re.compile(r"\b(\d+(?:\.\d+)?(?:\s*(?:GB|MB|KB|TB|GHz|MHz|ms|km|kg|m|s|%)))\b")

# Ollama defaults (same as numpy_store)
_OLLAMA_EMBED_URL = "http://localhost:11434/api/embed"
_OLLAMA_EMBED_MODEL = "nomic-embed-text"


def _extract_entities(text: str) -> set[str]:
    """Extract entities from text using regex heuristics."""
    entities: set[str] = set()
    for pattern in (_CAPITALIZED_PHRASE, _ACRONYM, _TECHNICAL_TERM, _NUMBER_WITH_UNIT):
        for match in pattern.finditer(text):
            ent = match.group(1).strip()
            if len(ent) > 1:  # skip single chars
                entities.add(ent)
    return entities


class LightRAGStore(BaseVectorStore):
    """Graph-enhanced vector store using networkx + cosine similarity.

    Args:
        ollama_url:     Ollama embed API URL.
        openai_api_key: Optional OpenAI fallback key.
        embed_fn:       Test injection for embeddings.
        graph_hops:     Number of hops for graph expansion (default: 1).
        graph_boost:    Max extra chunks from graph expansion (default: 2).
    """

    def __init__(
        self,
        ollama_url: Optional[str] = _OLLAMA_EMBED_URL,
        openai_api_key: Optional[str] = None,
        embed_fn: Optional[Callable[[list[str]], list[list[float]]]] = None,
        graph_hops: int = 1,
        graph_boost: int = 2,
    ) -> None:
        self._ollama_url = ollama_url
        self._openai_key = openai_api_key
        self._embed_fn = embed_fn
        self._graph_hops = graph_hops
        self._graph_boost = graph_boost

        # Vector data
        self._texts: list[str] = []
        self._ids: list[str] = []
        self._metadatas: list[dict] = []
        self._embeddings: list[list[float]] = []

        # Graph data
        self._graph = nx.Graph()
        # entity → set of chunk indices
        self._entity_to_chunks: dict[str, set[int]] = defaultdict(set)

    @property
    def size(self) -> int:
        return len(self._texts)

    @property
    def backend_name(self) -> str:
        return "lightrag"

    @property
    def graph(self) -> nx.Graph:
        """Expose graph for inspection/testing."""
        return self._graph

    def add_documents(
        self,
        texts: list[str],
        ids: Optional[list[str]] = None,
        metadatas: Optional[list[dict]] = None,
    ) -> None:
        if not texts:
            return

        auto_ids = ids or [hashlib.md5(t.encode()).hexdigest()[:8] for t in texts]
        auto_meta = metadatas or [{} for _ in texts]

        embeddings = self._embed(texts)

        base_idx = len(self._texts)
        self._texts.extend(texts)
        self._ids.extend(auto_ids)
        self._metadatas.extend(auto_meta)
        self._embeddings.extend(embeddings)

        # Build graph from new documents
        for i, text in enumerate(texts):
            chunk_idx = base_idx + i
            entities = _extract_entities(text)
            ent_list = list(entities)

            for ent in ent_list:
                self._graph.add_node(ent)
                self._entity_to_chunks[ent].add(chunk_idx)

            # Co-occurrence edges
            for a_idx in range(len(ent_list)):
                for b_idx in range(a_idx + 1, len(ent_list)):
                    a, b = ent_list[a_idx], ent_list[b_idx]
                    if self._graph.has_edge(a, b):
                        self._graph[a][b]["weight"] += 1
                    else:
                        self._graph.add_edge(a, b, weight=1)

        logger.debug(
            "LightRAG indexed %d docs, graph: %d nodes, %d edges",
            len(texts), self._graph.number_of_nodes(), self._graph.number_of_edges(),
        )

    def query(self, query_text: str, n_results: int = 3) -> list[RetrievedChunk]:
        if not self._embeddings:
            return []

        try:
            import numpy as np
        except ImportError:
            logger.error("numpy required for LightRAGStore")
            return []

        # Step 1: Cosine similarity
        q_emb = self._embed([query_text])
        if not q_emb:
            return []

        q_vec = np.array(q_emb[0], dtype=float)
        corpus = np.array(self._embeddings, dtype=float)
        q_norm = q_vec / (np.linalg.norm(q_vec) + 1e-10)
        norms = np.linalg.norm(corpus, axis=1, keepdims=True) + 1e-10
        scores = (corpus / norms) @ q_norm

        # Get top-k vector results
        k = min(n_results, len(self._texts))
        top_idx = list(np.argsort(scores)[::-1][:k])

        # Step 2: Graph expansion
        # Extract entities from top vector results
        query_entities = _extract_entities(query_text)
        for idx in top_idx:
            query_entities |= _extract_entities(self._texts[idx])

        # Find graph neighbours
        expanded_chunks: set[int] = set()
        for ent in query_entities:
            if ent in self._graph:
                for hop in range(self._graph_hops):
                    neighbours = set()
                    targets = {ent} if hop == 0 else expanded_chunks.copy()
                    for target in targets:
                        if isinstance(target, str) and target in self._graph:
                            neighbours |= set(self._graph.neighbors(target))
                    for neighbour in neighbours:
                        expanded_chunks |= self._entity_to_chunks.get(neighbour, set())

        # Step 3: Blend results (vector first, then graph expansions)
        seen = set(top_idx)
        graph_additions = []
        for chunk_idx in expanded_chunks:
            if chunk_idx not in seen and len(graph_additions) < self._graph_boost:
                graph_additions.append(chunk_idx)
                seen.add(chunk_idx)

        result_indices = top_idx + graph_additions

        results = []
        for idx in result_indices:
            results.append(RetrievedChunk(
                text=self._texts[idx],
                doc_id=self._ids[idx],
                score=float(scores[idx]),
                metadata=self._metadatas[idx],
            ))

        return results[:n_results + self._graph_boost]

    # ── Private helpers ───────────────────────────────────────────────────

    def _embed(self, texts: list[str]) -> list[list[float]]:
        if self._embed_fn:
            return self._embed_fn(texts)
        if self._ollama_url:
            try:
                return self._ollama_embed(texts)
            except Exception as exc:
                logger.warning("Ollama embed failed: %s", exc)
        if self._openai_key:
            try:
                return self._openai_embed(texts)
            except Exception as exc:
                logger.warning("OpenAI embed failed: %s", exc)
        # TF-IDF fallback
        return self._tfidf_embed(texts)

    def _ollama_embed(self, texts: list[str]) -> list[list[float]]:
        import requests
        resp = requests.post(
            self._ollama_url,
            json={"model": _OLLAMA_EMBED_MODEL, "input": texts},
            timeout=60,
        )
        resp.raise_for_status()
        return resp.json()["embeddings"]

    def _openai_embed(self, texts: list[str]) -> list[list[float]]:
        import requests
        resp = requests.post(
            "https://api.openai.com/v1/embeddings",
            headers={"Authorization": f"Bearer {self._openai_key}"},
            json={"input": texts, "model": "text-embedding-3-small"},
            timeout=30,
        )
        resp.raise_for_status()
        return [item["embedding"]
                for item in sorted(resp.json()["data"], key=lambda x: x["index"])]

    @staticmethod
    def _tfidf_embed(texts: list[str]) -> list[list[float]]:
        import math
        tokenised = [t.lower().split() for t in texts]
        vocab: dict[str, int] = {}
        for tokens in tokenised:
            for w in tokens:
                if w not in vocab:
                    vocab[w] = len(vocab)
        n_vocab = len(vocab) or 1
        vecs: list[list[float]] = []
        for tokens in tokenised:
            tf: dict[str, float] = {}
            for w in tokens:
                tf[w] = tf.get(w, 0) + 1
            max_tf = max(tf.values(), default=1)
            vec = [0.0] * n_vocab
            for w, count in tf.items():
                if w in vocab:
                    vec[vocab[w]] = (count / max_tf) * math.log((len(texts) + 1) / 1 + 1)
            vecs.append(vec)
        return vecs
