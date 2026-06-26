"""graphrag.py — GraphRAG 知识图谱增强检索引擎 (v9.0)

在现有 memory_links 和 memory_graph.py 的基础上，新增：
1. 实体-关系知识图谱构建（自动从记忆中抽取实体）
2. PageRank 节点重要性排序
3. 社区发现（Louvain 风格模块度优化）
4. 多跳推理路径（BFS + 边权重剪枝）
5. 图谱增强检索 — 将图谱上下文注入 RRF 融合结果

纯 Python 实现，零外部依赖。
"""

from __future__ import annotations

import hashlib
import logging
from collections import defaultdict, deque
from math import log, sqrt

logger = logging.getLogger(__name__)


def _cosine_sim(a: list[float], b: list[float]) -> float:
    if not a or not b or len(a) != len(b):
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    na = sqrt(sum(x * x for x in a))
    nb = sqrt(sum(x * x for x in b))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


class EntityNode:
    __slots__ = ("id", "name", "type", "memories", "embedding")

    def __init__(self, entity_id: str, name: str, entity_type: str = "concept"):
        self.id = entity_id
        self.name = name
        self.type = entity_type
        self.memories: list[str] = []
        self.embedding: list[float] | None = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "memory_count": len(self.memories),
        }


class RelationEdge:
    __slots__ = ("source_id", "target_id", "rel_type", "weight", "evidence")

    def __init__(self, source_id: str, target_id: str, rel_type: str,
                 weight: float = 1.0, evidence: str = ""):
        self.source_id = source_id
        self.target_id = target_id
        self.rel_type = rel_type
        self.weight = weight
        self.evidence = evidence

    def to_dict(self) -> dict:
        return {
            "source_id": self.source_id,
            "target_id": self.target_id,
            "rel_type": self.rel_type,
            "weight": self.weight,
            "evidence": self.evidence[:100],
        }


class GraphRAG:
    """图谱增强检索 — 在文本检索之上叠加知识图谱多跳推理。

    用法:
        graph = GraphRAG(store, embedder=my_embed_fn)
        graph.build_from_memories(memories)        # 构建知识图谱
        paths = graph.reason(query, max_hops=3)     # 多跳推理
        enhanced = graph.augment_recall(recall_results, query)  # 图谱增强
    """

    _ENTITY_KEYWORDS = {
        "person": ["用户", "同事", "老板", "客户", "朋友", "老师", "学生", "团队成员"],
        "tool": ["Python", "SQL", "Docker", "Kubernetes", "Git", "VS Code", "PostgreSQL",
                 "Redis", "MongoDB", "React", "Vue", "Node.js", "FastAPI", "LLM", "GPT"],
        "concept": ["微服务", "CI/CD", "敏捷", "DevOps", "机器学习", "深度学习",
                    "RAG", "Agent", "Prompt", "向量数据库", "知识图谱", "GraphRAG"],
        "action": ["配置", "部署", "调试", "优化", "重构", "测试", "发布", "监控",
                   "备份", "迁移", "集成", "拆分"],
    }

    def __init__(self, store=None, embedder=None, max_nodes: int = 10000):
        self.store = store
        self.embedder = embedder
        self.max_nodes = max_nodes

        self.nodes: dict[str, EntityNode] = {}
        self.edges: list[RelationEdge] = []
        self._adj_out: dict[str, list[RelationEdge]] = defaultdict(list)
        self._adj_in: dict[str, list[RelationEdge]] = defaultdict(list)

        self._pagerank: dict[str, float] = {}
        self._communities: dict[str, int] = {}
        self._built = False

    def build_from_memories(self, memories: list[dict], extract_entities: bool = True):
        if extract_entities:
            self._extract_entities(memories)

        self._build_edges_from_links(memories)
        self._run_pagerank()
        self._detect_communities()
        self._built = True
        logger.info("GraphRAG: built graph with %d nodes, %d edges, %d communities",
                    len(self.nodes), len(self.edges), len(set(self._communities.values())))

    def _extract_entities(self, memories: list[dict]):
        for mem in memories:
            content = mem.get("content", "")
            memory_id = mem.get("memory_id", "")
            if not content:
                continue

            for entity_type, keywords in self._ENTITY_KEYWORDS.items():
                for kw in keywords:
                    if kw.lower() in content.lower():
                        eid = self._entity_id(kw, entity_type)
                        if eid not in self.nodes:
                            self.nodes[eid] = EntityNode(eid, kw, entity_type)
                        if memory_id not in self.nodes[eid].memories:
                            self.nodes[eid].memories.append(memory_id)

            # 基于主题的实体
            topics = mem.get("topics", [])
            for t in topics:
                code = t.get("code", "") if isinstance(t, dict) else t
                if code:
                    eid = self._entity_id(code, "topic")
                    if eid not in self.nodes:
                        self.nodes[eid] = EntityNode(eid, code, "topic")
                    if memory_id not in self.nodes[eid].memories:
                        self.nodes[eid].memories.append(memory_id)

            # 基于 person_id
            person = mem.get("person_id", "")
            if person:
                eid = self._entity_id(person, "person")
                if eid not in self.nodes:
                    self.nodes[eid] = EntityNode(eid, person, "person")
                if memory_id not in self.nodes[eid].memories:
                    self.nodes[eid].memories.append(memory_id)

        # 修剪孤立节点
        orphan = [eid for eid, node in self.nodes.items() if not node.memories]
        for eid in orphan:
            del self.nodes[eid]

    def _build_edges_from_links(self, memories: list[dict]):
        memory_ids = {m.get("memory_id", "") for m in memories}

        # 从 memory_links 构建边
        links = []
        if self.store and hasattr(self.store, "conn"):
            try:
                rows = self.store.conn.execute(
                    "SELECT source_id, target_id, link_type, weight, reason FROM memory_links"
                ).fetchall()
                for row in rows:
                    sid = row["source_id"] if hasattr(row, "keys") else row[0]
                    tid = row["target_id"] if hasattr(row, "keys") else row[1]
                    if sid not in memory_ids or tid not in memory_ids:
                        continue
                    links.append({
                        "source_id": sid, "target_id": tid,
                        "link_type": row["link_type"] if hasattr(row, "keys") else row[2],
                        "weight": row["weight"] if hasattr(row, "keys") else (row[3] or 1.0),
                        "reason": row["reason"] if hasattr(row, "keys") else (row[4] or ""),
                    })
            except Exception as e:
                logger.warning("graphrag: %s", e)

        for link in links:
            edge = RelationEdge(
                link["source_id"], link["target_id"],
                link.get("link_type", "related"),
                link.get("weight", 1.0),
                link.get("reason", ""),
            )
            self.edges.append(edge)
            self._adj_out[edge.source_id].append(edge)
            self._adj_in[edge.target_id].append(edge)

        # 共享实体 → 隐含边
        eid_to_mems: dict[str, list[str]] = defaultdict(list)
        for eid, node in self.nodes.items():
            for mid in node.memories:
                eid_to_mems[mid].append(eid)

        seen_pairs: set[tuple[str, str]] = set()
        for _, mem_list in eid_to_mems.items():
            for i in range(len(mem_list)):
                for j in range(i + 1, len(mem_list)):
                    a, b = mem_list[i], mem_list[j]
                    if a == b:
                        continue
                    pair = (a, b) if a < b else (b, a)
                    if pair in seen_pairs:
                        continue
                    seen_pairs.add(pair)
                    edge = RelationEdge(a, b, "shares_entity", 0.5)
                    self.edges.append(edge)
                    self._adj_out[a].append(edge)
                    self._adj_in[b].append(edge)

    def _run_pagerank(self, damping: float = 0.85, iterations: int = 50):
        node_ids = list(self.nodes.keys()) + list({
            e.source_id for e in self.edges
        }.union({e.target_id for e in self.edges}))
        node_ids = list(dict.fromkeys(node_ids))

        if not node_ids:
            return

        N = len(node_ids)
        scores = {nid: 1.0 / N for nid in node_ids}

        out_degree = defaultdict(int)
        out_weight = defaultdict(float)
        for edge in self.edges:
            out_degree[edge.source_id] += 1
            out_weight[edge.source_id] += edge.weight

        for _ in range(iterations):
            new_scores = {nid: (1.0 - damping) / N for nid in node_ids}
            for edge in self.edges:
                src, tgt, w = edge.source_id, edge.target_id, edge.weight
                ow = out_weight.get(src, 1.0)
                if ow > 0:
                    new_scores[tgt] = new_scores.get(tgt, 0) + damping * scores.get(src, 0) * w / ow

            # 孤立节点保持基础分
            for nid in node_ids:
                if out_degree.get(nid, 0) == 0:
                    new_scores[nid] = new_scores.get(nid, 0) + scores.get(nid, 0) * damping / N

            scores = new_scores

        total = sum(scores.values()) or 1.0
        self._pagerank = {k: v / total for k, v in scores.items()}

    def _detect_communities(self, min_modularity_gain: float = 1e-5):
        node_ids = list(self.nodes.keys())
        if len(node_ids) < 3:
            self._communities = {nid: 0 for nid in node_ids}
            return

        self._communities = {nid: i for i, nid in enumerate(node_ids)}

        edge_set: set[tuple[str, str]] = set()
        edge_weights: dict[tuple[str, str], float] = {}
        for edge in self.edges:
            pair = (edge.source_id, edge.target_id) if edge.source_id < edge.target_id \
                else (edge.target_id, edge.source_id)
            edge_set.add(pair)
            edge_weights[pair] = edge_weights.get(pair, 0) + edge.weight

        total_weight = sum(edge_weights.values()) or 1.0

        community_weights: dict[int, float] = defaultdict(float)
        node_weight: dict[str, float] = defaultdict(float)
        for (a, b), w in edge_weights.items():
            community_weights[self._communities[a]] += w
            node_weight[a] += w
            node_weight[b] += w

        for _ in range(30):
            moved = False
            for nid in node_ids:
                current_comm = self._communities[nid]
                neighbor_comms: dict[int, float] = defaultdict(float)
                for edge in self._adj_out.get(nid, []):
                    neighbor_comms[self._communities[edge.target_id]] += edge.weight
                for edge in self._adj_in.get(nid, []):
                    neighbor_comms[self._communities[edge.source_id]] += edge.weight

                best_comm = current_comm
                best_gain = 0.0
                ki = node_weight.get(nid, 0)

                for comm, w_nc in neighbor_comms.items():
                    if comm == current_comm:
                        continue
                    sigma_tot = community_weights.get(comm, 0)
                    gain = w_nc / total_weight - ki * sigma_tot / (total_weight * total_weight)
                    if gain > best_gain:
                        best_gain = gain
                        best_comm = comm

                if best_gain > min_modularity_gain and best_comm != current_comm:
                    self._communities[nid] = best_comm
                    moved = True

            if not moved:
                break

        compact = {}
        next_id = 0
        for nid in node_ids:
            c = self._communities[nid]
            if c not in compact:
                compact[c] = next_id
                next_id += 1
            self._communities[nid] = compact[c]

    def reason(self, query: str, max_hops: int = 3, top_k: int = 10,
               min_pagerank: float = 0.001) -> list[dict]:
        if not self._built:
            return []

        seed_ids = self._find_seed_nodes(query)
        if not seed_ids:
            return []

        paths: list[dict] = []
        visited: set[str] = set()

        queue = deque()
        for sid in seed_ids:
            queue.append((sid, [sid], 1.0, 0))
            visited.add(sid)

        while queue:
            current, path, cumulative_weight, hops = queue.popleft()
            if hops >= max_hops:
                if len(path) >= 2 and cumulative_weight > 0.01:
                    paths.append({
                        "path": list(path),
                        "hops": hops,
                        "score": round(cumulative_weight * self._pagerank.get(current, 0.001) * 10, 4),
                        "path_detail": self._describe_path(path),
                    })
                continue

            extended = False
            for edge in self._adj_out.get(current, []):
                nxt = edge.target_id
                if nxt in visited:
                    continue
                pr = self._pagerank.get(nxt, 0)
                if pr < min_pagerank:
                    continue
                new_path = path + [nxt]
                new_weight = cumulative_weight * edge.weight
                visited.add(nxt)
                queue.append((nxt, new_path, new_weight, hops + 1))
                extended = True

            if not extended and hops > 0 and len(path) >= 2:
                paths.append({
                    "path": list(path),
                    "hops": hops,
                    "score": round(cumulative_weight * self._pagerank.get(current, 0.001) * 10, 4),
                    "path_detail": self._describe_path(path),
                })

        paths.sort(key=lambda x: (-x["score"], x["hops"]))
        return paths[:top_k]

    def _find_seed_nodes(self, query: str) -> list[str]:
        seeds: list[tuple[str, float]] = []

        ql = query.lower()
        for eid, node in self.nodes.items():
            if node.name.lower() in ql:
                seeds.append((eid, 1.0))

        if self.embedder and self.nodes:
            try:
                q_emb = self.embedder(query)
                for eid, node in self.nodes.items():
                    if node.embedding:
                        sim = _cosine_sim(q_emb, node.embedding)
                        if sim > 0.6:
                            seeds.append((eid, sim))
            except Exception as e:
                logger.debug("Embedding search for seeds failed: %s", e)

        seeds.sort(key=lambda x: -x[1])
        seed_ids = list(dict.fromkeys(s[0] for s in seeds))
        return seed_ids[:5]

    def _describe_path(self, path: list[str]) -> str:
        parts = []
        for i, nid in enumerate(path):
            node = self.nodes.get(nid)
            if node:
                tag = f"{node.type}:{node.name}"
            else:
                tag = nid[:20]
            parts.append(tag)
            if i < len(path) - 1:
                edge_found = False
                for e in self._adj_out.get(nid, []):
                    if e.target_id == path[i + 1]:
                        parts.append(f"-[{e.rel_type}]→")
                        edge_found = True
                        break
                if not edge_found:
                    parts.append("→")
        return " ".join(parts)

    def augment_recall(self, recall_results: list[dict], query: str,
                       top_paths: int = 5) -> list[dict]:
        if not self._built or not recall_results:
            return recall_results

        paths = self.reason(query, max_hops=3, top_k=top_paths)

        path_memory_ids: set[str] = set()
        for path_info in paths:
            for nid in path_info["path"]:
                node = self.nodes.get(nid)
                if node:
                    path_memory_ids.update(node.memories)

        existing_ids = {r.get("memory_id", "") for r in recall_results}
        graph_boost_ids = path_memory_ids - existing_ids

        for r in recall_results:
            mid = r.get("memory_id", "")
            community = self._communities.get(mid)
            pr = self._pagerank.get(mid, 0)

            # 图谱增强分数
            graph_boost = 0.0
            if mid in path_memory_ids:
                graph_boost += 0.15
            if community is not None:
                # 同社区的检索结果互相增强
                for r2 in recall_results:
                    if r2.get("memory_id") != mid and self._communities.get(r2.get("memory_id")) == community:
                        graph_boost += 0.05
                        break
            graph_boost += min(pr * 5, 0.1)

            r["graph_score"] = round(graph_boost, 4)
            r["score"] = round(r.get("score", 0) + graph_boost, 4)
            r["community_id"] = community

        # 追加图谱独有记忆
        if graph_boost_ids and self.store:
            for mid in list(graph_boost_ids)[:top_paths]:
                try:
                    mem = self.store.get_memory(mid)
                    if mem:
                        recall_results.append({
                            "memory_id": mid,
                            "score": 0.15,
                            "graph_score": 0.15,
                            "content": mem.get("content", ""),
                            "source": "graph_boost",
                        })
                except Exception as e:
                    logger.warning("graphrag: %s", e)

        recall_results.sort(key=lambda x: -x.get("score", 0))
        return recall_results

    def get_entity_graph(self) -> dict:
        return {
            "nodes": [n.to_dict() for n in self.nodes.values()],
            "edges": [e.to_dict() for e in self.edges],
            "node_count": len(self.nodes),
            "edge_count": len(self.edges),
            "community_count": len(set(self._communities.values())),
        }

    def get_top_entities(self, top_k: int = 10) -> list[dict]:
        ranked = sorted(
            [(eid, self._pagerank.get(eid, 0), node) for eid, node in self.nodes.items()],
            key=lambda x: -x[1],
        )
        return [
            {"id": eid, "name": node.name, "type": node.type,
             "pagerank": round(pr, 6), "memory_count": len(node.memories),
             "community": self._communities.get(eid)}
            for eid, pr, node in ranked[:top_k]
        ]

    def get_communities(self) -> list[dict]:
        comm_groups: dict[int, list[str]] = defaultdict(list)
        for nid, cid in self._communities.items():
            comm_groups[cid].append(nid)

        result = []
        for cid, members in sorted(comm_groups.items(), key=lambda x: -len(x[1])):
            top_entities = sorted(
                members, key=lambda n: self._pagerank.get(n, 0), reverse=True
            )[:5]
            result.append({
                "community_id": cid,
                "size": len(members),
                "top_entities": [
                    {"id": eid, "name": self.nodes[eid].name if eid in self.nodes else eid}
                    for eid in top_entities
                ],
            })
        return result

    def get_stats(self) -> dict:
        return {
            "node_count": len(self.nodes),
            "edge_count": len(self.edges),
            "community_count": len(set(self._communities.values())),
            "avg_degree": len(self.edges) * 2 / max(len(self.nodes), 1),
            "built": self._built,
        }

    @staticmethod
    def _entity_id(name: str, entity_type: str) -> str:
        h = hashlib.md5(f"{entity_type}:{name}".encode()).hexdigest()[:12]
        return f"ent_{h}"


class GraphReasoningPath:
    __slots__ = ("nodes", "edges", "score", "explanation")

    def __init__(self):
        self.nodes: list[str] = []
        self.edges: list[tuple[str, str, str]] = []
        self.score: float = 0.0
        self.explanation: str = ""

    def to_dict(self) -> dict:
        return {
            "nodes": self.nodes,
            "edges": [{"from": s, "to": t, "relation": r} for s, t, r in self.edges],
            "score": self.score,
            "explanation": self.explanation,
        }