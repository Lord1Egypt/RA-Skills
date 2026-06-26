from __future__ import annotations

import hashlib
import logging
import time
from collections import defaultdict
from typing import Optional, Callable

logger = logging.getLogger(__name__)


class KnowledgeBuilder:
    """Auto-construct knowledge graph from fragment memories.

    Scans unstructured memories and:
    1. Extracts entities (topics, tools, concepts, people)
    2. Identifies relationships (causal, temporal, hierarchical)
    3. Builds/updates the GraphRAG knowledge graph
    4. Creates summary memories for clusters
    """

    def __init__(
        self,
        store,
        embedding_store=None,
        graphrag=None,
        causal=None,
        llm_fn: Optional[Callable] = None,
    ):
        self.store = store
        self.embedding_store = embedding_store
        self.graphrag = graphrag
        self.causal = causal
        self.llm_fn = llm_fn
        self._cooc_index = {}
        self._term_doc_freq: dict[str, int] = {}
        self._total_docs_indexed: int = 0

    def build_from_memories(self, limit: int = 100, agent_id: Optional[str] = None) -> dict:
        """Scan recent memories and build knowledge graph.

        Returns dict with stats about entities, relationships, and clusters built.
        """
        result = {
            "memories_scanned": 0,
            "entities_extracted": 0,
            "relationships_found": 0,
            "clusters_summarized": 0,
            "graph_nodes_added": 0,
            "graph_edges_added": 0,
        }

        memories = self._get_recent_memories(limit, agent_id)
        result["memories_scanned"] = len(memories)
        if not memories:
            return result

        all_entities: dict[str, dict] = {}
        for mem in memories:
            entities = self._extract_entities(mem)
            mid = mem.get("memory_id", "")
            for edata in entities:
                eid = edata["id"]
                if eid not in all_entities:
                    all_entities[eid] = {
                        "name": edata["name"],
                        "type": edata["type"],
                        "memory_ids": {mid},
                    }
                else:
                    all_entities[eid]["memory_ids"].add(mid)

        result["entities_extracted"] = len(all_entities)

        relationships = []
        seen_pairs: set[tuple[str, str]] = set()
        sorted_mems = sorted(memories, key=lambda m: m.get("time_ts", 0))

        for i in range(len(sorted_mems) - 1):
            mem_a = sorted_mems[i]
            mem_b = sorted_mems[i + 1]

            rels = self._find_relationships(mem_a, mem_b)
            for rel in rels:
                pair_key = (rel["from"], rel["to"])
                if pair_key not in seen_pairs:
                    seen_pairs.add(pair_key)
                    relationships.append(rel)

        result["relationships_found"] = len(relationships)

        if self.graphrag:
            nodes_added, edges_added = self._update_graphrag(all_entities, relationships)
            result["graph_nodes_added"] = nodes_added
            result["graph_edges_added"] = edges_added

        clusters = self._find_clusters(all_entities, memories)
        for cluster in clusters:
            if len(cluster["memory_ids"]) >= 3:
                self._create_cluster_summary(cluster)
                result["clusters_summarized"] += 1

        logger.info(
            "KnowledgeBuilder: scanned=%d entities=%d rels=%d clusters=%d",
            result["memories_scanned"],
            result["entities_extracted"],
            result["relationships_found"],
            result["clusters_summarized"],
        )
        return result

    def _get_recent_memories(self, limit: int, agent_id: Optional[str] = None) -> list[dict]:
        try:
            kwargs = {"limit": limit}
            if agent_id and hasattr(self.store, "query"):
                kwargs["query_agent_id"] = agent_id
            return self.store.query(**kwargs)
        except Exception as e:
            logger.warning("KnowledgeBuilder._get_recent_memories: %s", e)
            return []

    def _extract_entities(self, memory: dict) -> list[dict]:
        entities = []
        content = memory.get("content", "")
        mid = memory.get("memory_id", "")

        # Strategy 1: Metadata fields
        for code in memory.get("topic_codes", []) or []:
            entities.append({"id": self._entity_id("topic", code), "name": code, "type": "topic", "source": "metadata"})
        person = memory.get("person_id") or memory.get("owner_agent_id")
        if person and person != "_system":
            entities.append({"id": self._entity_id("person", person), "name": person, "type": "person", "source": "metadata"})
        for code in memory.get("tool_codes", []) or []:
            entities.append({"id": self._entity_id("tool", code), "name": code, "type": "tool", "source": "metadata"})

        # Strategy 2: TF-IDF scoring for candidate entities
        candidates = self._extract_candidate_entities(content)
        for cand in candidates:
            score = self._tfidf_score(cand, content)
            if score > 0.3:
                entities.append({
                    "id": self._entity_id("concept", cand),
                    "name": cand,
                    "type": "concept",
                    "source": "tfidf",
                    "score": score,
                })

        # Strategy 3: Co-occurrence entities (from pre-built index)
        cooc_entities = self._cooccurrence_entities(content)
        for ce in cooc_entities:
            if not any(e["name"] == ce for e in entities):
                entities.append({
                    "id": self._entity_id("cooc", ce),
                    "name": ce,
                    "type": "related_concept",
                    "source": "cooccurrence",
                })

        # Strategy 4: Pattern-based extraction (enhanced)
        pattern_entities = self._pattern_extract(content)
        for pe in pattern_entities:
            if not any(e["name"] == pe["name"] for e in entities):
                entities.append(pe)

        return entities

    def _extract_candidate_entities(self, content: str) -> list[str]:
        """Extract candidate entity terms from content using multiple strategies."""
        import re
        candidates = []

        zh_phrases = re.findall(r'[\u4e00-\u9fff]{2,6}', content)

        stop_words = {"的是", "在了", "不是", "一个", "这个", "那个", "什么", "怎么", "可以", "因为", "所以", "但是", "而且", "如果", "虽然", "已经", "还是", "或者", "以及", "之后", "之前", "关于", "通过", "进行", "使用", "需要", "包括", "其中"}

        for phrase in zh_phrases:
            if phrase not in stop_words and len(phrase) >= 2:
                candidates.append(phrase)

        en_terms = re.findall(r'[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+', content)
        candidates.extend(en_terms)

        tech_terms = re.findall(r'[a-z]+[A-Z][a-zA-Z]*|[a-z]+(?:_[a-z]+)+|[A-Z]{2,}[A-Z_]*', content)
        candidates.extend(tech_terms)

        return list(set(candidates))[:30]

    def _tfidf_score(self, term: str, content: str) -> float:
        """Simple TF-IDF scoring for a term."""
        tf = content.count(term) / max(len(content) / len(term), 1)

        idf = self._compute_idf(term)

        boost = 1.0
        if term != term.lower():
            boost = 1.5

        score = tf * idf * boost
        return min(1.0, score)

    def _compute_idf(self, term: str) -> float:
        """Compute IDF properly: log(N / df)."""
        import math
        df = self._term_doc_freq.get(term, 1)
        total = max(self._total_docs_indexed, 1)
        return math.log(total / max(df, 1)) + 1.0

    def _cooccurrence_entities(self, content: str) -> list[str]:
        """Find entities that frequently co-occur with terms in this content."""
        if not hasattr(self, '_cooc_index') or not self._cooc_index:
            self._build_cooccurrence_index()

        related = set()
        # Use Chinese-aware tokenization consistent with index building
        try:
            import jieba  # type: ignore
            content_terms = set(w for w in jieba.cut(content) if len(w.strip()) > 1)
        except ImportError:
            import re
            content_terms = set(re.findall(r'[a-zA-Z]{2,}|[\u4e00-\u9fff]{2,}', content))

        for term in content_terms:
            if term in self._cooc_index:
                for cooc_term, count in self._cooc_index[term].items():
                    if count >= 2 and cooc_term not in content_terms:
                        related.add(cooc_term)

        return list(related)[:10]

    def _build_cooccurrence_index(self):
        """Build co-occurrence index from existing memories with Chinese-aware tokenization."""
        self._cooc_index = {}
        self._term_doc_freq = {}
        self._total_docs_indexed = 0
        try:
            rows = self.store.execute_sql(
                "SELECT content FROM memories ORDER BY created_at DESC LIMIT 200",
                fetch=True,
            )
            self._total_docs_indexed = len(rows)

            for row in rows:
                content = row["content"] if row["content"] else ""
                if not content:
                    continue

                # Try jieba for Chinese, fall back to regex tokenization
                try:
                    import jieba  # type: ignore
                    tokens = [w for w in jieba.cut(content) if len(w.strip()) > 1]
                except ImportError:
                    import re
                    tokens = re.findall(r'[a-zA-Z]{2,}|[\u4e00-\u9fff]{2,}', content)

                # Update term document frequency
                unique_tokens = set(tokens)
                for t in unique_tokens:
                    self._term_doc_freq[t] = self._term_doc_freq.get(t, 0) + 1

                # Build co-occurrence pairs (within sliding window of 5)
                for i in range(len(tokens)):
                    if tokens[i] not in self._cooc_index:
                        self._cooc_index[tokens[i]] = {}
                    for j in range(i + 1, min(i + 5, len(tokens))):
                        cooc_term = tokens[j]
                        self._cooc_index[tokens[i]][cooc_term] = self._cooc_index[tokens[i]].get(cooc_term, 0) + 1
        except Exception as e:
            logger.debug("_build_cooc_index: %s", e)

    def _pattern_extract(self, content: str) -> list[dict]:
        """Enhanced pattern-based entity extraction."""
        import re
        entities = []

        for url in re.findall(r'https?://[^\s<>]+', content):
            entities.append({"id": self._entity_id("url", url), "name": url[:50], "type": "url", "source": "pattern"})

        for ver in re.findall(r'v?\d+\.\d+(?:\.\d+)?', content):
            entities.append({"id": self._entity_id("version", ver), "name": ver, "type": "version", "source": "pattern"})

        for name in re.findall(r'(?:的|是|叫|名为|叫做|称为)\s*([^\s，。！？]{2,8})', content):
            entities.append({"id": self._entity_id("proper", name), "name": name, "type": "proper_noun", "source": "pattern"})

        for name in re.findall(r'(?:is|called|named)\s+([A-Z][a-zA-Z\s]{1,20})', content):
            name = name.strip()
            entities.append({"id": self._entity_id("proper", name), "name": name, "type": "proper_noun", "source": "pattern"})

        return entities

    def _find_relationships(self, mem1: dict, mem2: dict) -> list[dict]:
        """Identify relationships between two memories using multiple signals."""
        relationships = []
        mid1 = mem1.get("memory_id", "")
        mid2 = mem2.get("memory_id", "")

        # Signal 1: Causal (from nature_codes)
        n1 = set(mem1.get("nature_codes", []) or [])
        n2 = set(mem2.get("nature_codes", []) or [])
        causal_sources = {"D04", "D12"}
        causal_targets = {"D03", "D06", "D07"}
        if n1 & causal_sources and n2 & causal_targets:
            relationships.append({"type": "causes", "from": mid1, "to": mid2, "confidence": 0.7})

        # Signal 2: Topic overlap
        topics1 = set(mem1.get("topic_codes", []) or [])
        topics2 = set(mem2.get("topic_codes", []) or [])
        if topics1 & topics2:
            overlap = len(topics1 & topics2) / max(len(topics1 | topics2), 1)
            relationships.append({"type": "related", "from": mid1, "to": mid2, "confidence": overlap})

        # Signal 3: Temporal proximity + content overlap
        t1 = mem1.get("created_at", 0)
        t2 = mem2.get("created_at", 0)
        if t1 and t2 and abs(t1 - t2) < 3600:
            content_overlap = self._content_keyword_overlap(
                mem1.get("content", ""), mem2.get("content", "")
            )
            if content_overlap > 0.15:
                relationships.append({"type": "follows", "from": mid1, "to": mid2, "confidence": content_overlap})

        # Signal 4: Embedding similarity (if available)
        if self.embedding_store:
            try:
                sim = self._embedding_similarity(mid1, mid2)
                if sim > 0.7:
                    relationships.append({"type": "semantically_similar", "from": mid1, "to": mid2, "confidence": sim})
            except Exception as e:
                logger.debug("_find_relationships embedding_similarity: %s", e)

        return relationships

    def _embedding_similarity(self, mid1: str, mid2: str) -> float:
        """Compute embedding similarity between two memories."""
        try:
            vec1 = self.embedding_store.get_vector(mid1)
            vec2 = self.embedding_store.get_vector(mid2)
            if vec1 is not None and vec2 is not None:
                import numpy as np
                v1 = np.array(vec1)
                v2 = np.array(vec2)
                norm1 = np.linalg.norm(v1)
                norm2 = np.linalg.norm(v2)
                if norm1 > 0 and norm2 > 0:
                    return float(np.dot(v1, v2) / (norm1 * norm2))
        except Exception as e:
            logger.debug("_embedding_similarity: %s", e)
        return 0.0

    def _find_clusters(self, entities: dict, memories: list[dict]) -> list[dict]:
        """Find clusters of memories sharing entities."""
        entity_to_mems: dict[str, set[str]] = defaultdict(set)
        for eid, edata in entities.items():
            entity_to_mems[eid] = edata["memory_ids"]

        mem_to_entities: dict[str, set[str]] = defaultdict(set)
        for eid, mids in entity_to_mems.items():
            for mid in mids:
                mem_to_entities[mid].add(eid)

        clusters: list[dict] = []
        visited: set[str] = set()

        for mid, eids in mem_to_entities.items():
            if mid in visited:
                continue

            cluster_mids = {mid}
            queue = [mid]
            while queue:
                current = queue.pop(0)
                visited.add(current)
                for eid in mem_to_entities.get(current, set()):
                    for neighbor in entity_to_mems.get(eid, set()):
                        if neighbor not in visited:
                            cluster_mids.add(neighbor)
                            queue.append(neighbor)

            if len(cluster_mids) >= 3:
                shared_entities = set()
                for cmid in cluster_mids:
                    shared_entities.update(mem_to_entities.get(cmid, set()))

                cluster_entity_names = []
                for eid in shared_entities:
                    if eid in entities:
                        cluster_entity_names.append(entities[eid]["name"])

                clusters.append({
                    "memory_ids": cluster_mids,
                    "entity_ids": shared_entities,
                    "entity_names": cluster_entity_names[:5],
                })

        return clusters

    def _create_cluster_summary(self, cluster: dict) -> Optional[str]:
        """Create a summary memory for a cluster of related memories."""
        memory_ids = cluster["memory_ids"]
        entity_names = cluster.get("entity_names", [])

        contents = []
        for mid in list(memory_ids)[:10]:
            mem = self.store.get_memory(mid)
            if mem:
                contents.append(mem.get("content", "")[:200])

        if not contents:
            return None

        if self.llm_fn:
            try:
                prompt = (
                    "将以下相关记忆合并为一条简洁的摘要记忆。\n"
                    "保留关键事实、实体和关系。\n"
                    "用与输入相同的语言输出。\n\n"
                    f"相关实体: {', '.join(entity_names)}\n\n"
                    f"记忆内容:\n" + "\n---\n".join(contents) + "\n\n摘要:"
                )
                summary = self.llm_fn(prompt)
                if summary and len(summary) > 10:
                    self._store_summary_memory(summary, entity_names, memory_ids)
                    return summary
            except Exception as e:
                logger.debug("KnowledgeBuilder._create_cluster_summary LLM: %s", e)

        key_points = []
        for c in contents[:5]:
            first_sentence = c.split("。")[0].split(".")[0]
            if first_sentence:
                key_points.append(first_sentence)

        summary = f"[知识聚类: {', '.join(entity_names)}] " + "；".join(key_points)
        self._store_summary_memory(summary, entity_names, memory_ids)
        return summary

    def _store_summary_memory(self, summary: str, entity_names: list[str], source_ids: set[str]):
        try:
            self.store.insert_memory(
                content=summary,
                person_code="system",
                nature_code="D05",
                importance="medium",
                metadata={
                    "is_cluster_summary": True,
                    "source_count": len(source_ids),
                    "entities": entity_names[:5],
                },
            )
        except Exception as e:
            logger.debug("KnowledgeBuilder._store_summary_memory: %s", e)

    def _update_graphrag(self, entities: dict, relationships: list[dict]) -> tuple[int, int]:
        if not self.graphrag:
            return 0, 0

        nodes_added = 0
        edges_added = 0

        try:
            from graphrag import EntityNode, RelationEdge

            for eid, edata in entities.items():
                if eid not in self.graphrag.nodes:
                    node = EntityNode(eid, edata["name"], edata["type"])
                    node.memories = list(edata["memory_ids"])
                    self.graphrag.nodes[eid] = node
                    nodes_added += 1
                else:
                    existing = self.graphrag.nodes[eid]
                    for mid in edata["memory_ids"]:
                        if mid not in existing.memories:
                            existing.memories.append(mid)

            for rel in relationships:
                edge = RelationEdge(
                    source_id=rel["from"],
                    target_id=rel["to"],
                    rel_type=rel["type"],
                    weight=rel.get("confidence", 0.5),
                    evidence=rel.get("evidence", ""),
                )
                self.graphrag.edges.append(edge)
                self.graphrag._adj_out[edge.source_id].append(edge)
                self.graphrag._adj_in[edge.target_id].append(edge)
                edges_added += 1

        except Exception as e:
            logger.warning("KnowledgeBuilder._update_graphrag: %s", e)

        return nodes_added, edges_added

    def _get_topic_codes(self, mem: dict) -> set[str]:
        topics = mem.get("topics", [])
        result = set()
        for t in topics:
            code = t.get("code", "") if isinstance(t, dict) else t
            if code:
                result.add(code)
                result.add(code.split(".")[0])
        return result

    def _content_keyword_overlap(self, text_a: str, text_b: str) -> float:
        if not text_a or not text_b:
            return 0.0

        def bigrams(text):
            return set(text[i:i+2] for i in range(len(text)-1) if text[i:i+2].strip())

        grams_a = bigrams(text_a)
        grams_b = bigrams(text_b)
        if not grams_a or not grams_b:
            return 0.0

        shared = grams_a & grams_b
        union = grams_a | grams_b
        return len(shared) / len(union) if union else 0.0

    @staticmethod
    def _entity_id(entity_type: str, name: str) -> str:
        h = hashlib.md5(f"{entity_type}:{name}".encode()).hexdigest()[:12]
        return f"ent_{h}"

    def get_stats(self) -> dict:
        stats = {
            "graphrag_available": self.graphrag is not None,
            "causal_available": self.causal is not None,
            "llm_available": self.llm_fn is not None,
        }
        if self.graphrag:
            stats["graphrag"] = self.graphrag.get_stats()
        return stats
