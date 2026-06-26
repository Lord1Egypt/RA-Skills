#!/usr/bin/env python3
"""
InfinityDB-lite: 纯 Python 标准库实现（无 numpy 依赖）
替代 neural-memory Pro 的 InfinityDB

方案A：单一数据源
  - brain.graph: 神经元元数据 + 邻接关系（JSON）
  - brain.vec: struct 二进制向量存储
  - brain.hnsw: 简化 HNSW 索引（pickle）

新存储格式：
  {
    "neurons": {
      "neuron_id": {
        "content": "记忆内容...",
        "memory_type": "task",
        "priority": 3,
        "tier": "warm",
        "timestamp": "2026-04-26T...",
        "neighbors": { "other_id": 0.5 }
      }
    },
    "config": { "recall": { ... } }
  }
"""

import json
import math
import random
import struct
import pickle
from pathlib import Path
from collections import defaultdict
from typing import Optional

VECTOR_DIM = 1024
M = 16
EF_CONSTRUCTION = 200
EF_SEARCH = 100


def cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


class SimpleHnsw:
    """简化 HNSW（纯 Python，多层跳表 + Beam Search）"""

    def __init__(self, dim: int = VECTOR_DIM, M: int = 16, ef: int = 100):
        self.dim = dim
        self.M = M
        self.ef = ef
        self.nodes: dict[str, "_HnswNode"] = {}
        self.entry_id: Optional[str] = None
        self.max_level = 0

    def _new_level(self) -> int:
        level = 0
        while random.random() < (1.0 / self.M) and level < self.max_level + 2:
            level += 1
        return level

    def add(self, node_id: str, vector: list[float]):
        node = _HnswNode(node_id, vector, self._new_level())
        self.nodes[node_id] = node

        if self.entry_id is None:
            self.entry_id = node_id
            self.max_level = node.level
            return

        if node.level > self.max_level:
            self.max_level = node.level
            self.entry_id = node_id

        current = self.nodes[self.entry_id]
        for layer in range(self.max_level, 0, -1):
            candidates = self._search_layer(current, node.vector, layer, ef=1)
            if candidates:
                current = self.nodes[candidates[0][0]]

        self._connect_node(node, layer=0)

    def _search_layer(self, entry: "_HnswNode", query: list[float], layer: int, ef: int) -> list[tuple[str, float]]:
        visited = {entry.id}
        results = [(entry.id, cosine_similarity(entry.vector, query))]
        frontier = [(entry.id, cosine_similarity(entry.vector, query))]

        while frontier:
            _, current_id = frontier.pop(0)
            if current_id not in self.nodes:
                continue
            current = self.nodes[current_id]

            for neighbor_id, _ in current.friends.get(layer, []):
                if neighbor_id not in visited:
                    visited.add(neighbor_id)
                    neighbor = self.nodes[neighbor_id]
                    dist = cosine_similarity(neighbor.vector, query)
                    results.append((neighbor_id, dist))
                    frontier.append((neighbor_id, dist))

            results.sort(key=lambda x: x[1], reverse=True)
            frontier = frontier[:ef]

        return results[:ef]

    def _connect_node(self, node: "_HnswNode", layer: int):
        candidates = self._search_layer(node, node.vector, layer, ef=self.M * 2)
        for neighbor_id, _ in candidates[1:]:
            if neighbor_id == node.id:
                continue
            neighbor = self.nodes[neighbor_id]
            node.friends.setdefault(layer, []).append((neighbor_id, 1.0))
            neighbor.friends.setdefault(layer, []).append((node.id, 1.0))

    def search(self, query: list[float], k: int = 10, ef: int = None) -> list[tuple[str, float]]:
        if self.entry_id is None or not self.nodes:
            return []
        if ef is None:
            ef = self.ef

        entry = self.nodes[self.entry_id]
        for layer in range(self.max_level, 0, -1):
            candidates = self._search_layer(entry, query, layer, ef=1)
            if candidates:
                entry = self.nodes[candidates[0][0]]

        results = self._search_layer(entry, query, layer=0, ef=ef)
        return [(nid, 1.0 - dist) for nid, dist in results[:k] if nid in self.nodes]

    def save(self, path: str):
        with open(path, 'wb') as f:
            pickle.dump({
                'nodes': [(nid, n.vector, n.level, n.friends) for nid, n in self.nodes.items()],
                'entry_id': self.entry_id,
                'max_level': self.max_level,
            }, f)

    def load(self, path: str):
        with open(path, 'rb') as f:
            data = pickle.load(f)
        self.nodes = {}
        for nid, vec, level, friends in data['nodes']:
            node = _HnswNode(nid, vec, level)
            node.friends = friends
            self.nodes[nid] = node
        self.entry_id = data['entry_id']
        self.max_level = data['max_level']


class _HnswNode:
    __slots__ = ('id', 'vector', 'level', 'friends')
    def __init__(self, nid: str, vector: list[float], level: int):
        self.id = nid
        self.vector = vector
        self.level = level
        self.friends: dict[int, list[tuple[str, float]]] = {}


class VecStore:
    """二进制向量存储（替代 numpy mmap）"""
    def __init__(self, path: str, dim: int = VECTOR_DIM):
        self.path = Path(path)
        self.dim = dim
        self._ids: list[str] = []
        self._id_map: dict[str, int] = {}
        self._data_size = 0
        self._load_ids()

    def _load_ids(self):
        idx_path = self.path.with_suffix('.idx')
        if idx_path.exists():
            with open(idx_path, 'r') as f:
                self._ids = json.load(f)
            self._id_map = {nid: i for i, nid in enumerate(self._ids)}
            self._data_size = len(self._ids)

    def _save_ids(self):
        idx_path = self.path.with_suffix('.idx')
        with open(idx_path, 'w') as f:
            json.dump(self._ids, f)

    def append(self, node_id: str, vector: list[float]):
        if node_id in self._id_map:
            return
        idx = self._data_size
        self._id_map[node_id] = idx
        self._ids.append(node_id)
        self._data_size += 1

        with open(self.path, 'ab') as f:
            for v in vector:
                f.write(struct.pack('>f', float(v)))
        self._save_ids()

    def get(self, node_id: str) -> Optional[list[float]]:
        if node_id not in self._id_map:
            return None
        idx = self._id_map[node_id]
        offset = idx * self.dim * 4
        with open(self.path, 'rb') as f:
            f.seek(offset)
            data = f.read(self.dim * 4)
            return list(struct.unpack(f'>{self.dim}f', data))

    def __len__(self):
        return self._data_size


class InfinityDBLite:
    """
    InfinityDB-lite（单一数据源）

    brain.graph: 神经元元数据 + 邻接关系
    brain.vec: 二进制向量
    brain.hnsw: HNSW 索引

    特性：
      - Adjacency BFS: <1ms/hop
      - HNSW 向量检索: O(log N)
      - 全标准库，无外部依赖
      - 单一数据源，无同步问题
    """

    def __init__(self, data_dir: str = "/workspace/fusion/memory/layers/infinitydb"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

        self.graph_path = self.data_dir / "brain.graph.json"
        self.vec_path = self.data_dir / "brain.vec.fvec"
        self.hnsw_path = self.data_dir / "brain.hnsw"

        # 单一数据源：神经元元数据 + 邻接关系
        self.data: dict = {"neurons": {}, "config": {}}

        # 邻接表视图（从 self.data["neurons"] 派生）
        self.adj: dict[str, dict[str, float]] = {}

        self.vec_store = VecStore(str(self.vec_path))
        self.hnsw = SimpleHnsw(dim=VECTOR_DIM, M=M, ef=EF_SEARCH)
        self._load()

    def _load(self):
        """加载 brain.graph.json，支持旧格式迁移"""
        if self.graph_path.exists():
            with open(self.graph_path, 'r') as f:
                raw = json.load(f)

            # 旧格式迁移：{"id1": {"id2": 0.5}} → 新格式
            if "neurons" in raw:
                self.data = raw
            else:
                self.data = {"neurons": {}, "config": {}}
                for nid, neighbors in raw.items():
                    self.data["neurons"][nid] = {
                        "content": "",
                        "memory_type": "unknown",
                        "priority": 3,
                        "tier": "cold",
                        "timestamp": "",
                        "neighbors": neighbors if isinstance(neighbors, dict) else {}
                    }

        self._rebuild_adj_view()
        print(f"[InfinityDB] 加载邻接表: {len(self.adj)} 节点")

        if self.vec_path.exists():
            print(f"[InfinityDB] 向量存储: {len(self.vec_store)} vectors")

        if Path(self.hnsw_path).exists():
            self.hnsw.load(str(self.hnsw_path))

    def _rebuild_adj_view(self):
        """从神经元数据重建邻接表视图"""
        self.adj = {}
        for nid, neuron in self.data["neurons"].items():
            self.adj[nid] = neuron.get("neighbors", {})

    def _save_graph(self):
        with open(self.graph_path, 'w') as f:
            json.dump(self.data, f)

    def add_neuron_with_metadata(
        self,
        node_id: str,
        vector: list[float],
        neighbors: dict[str, float] = None,
        content: str = "",
        memory_type: str = "context",
        priority: int = 3,
        tier: str = "cold",
        timestamp: str = ""
    ):
        """原子写入神经元元数据 + 向量 + 邻接关系"""
        if node_id not in self.data["neurons"]:
            self.data["neurons"][node_id] = {
                "content": content,
                "memory_type": memory_type,
                "priority": priority,
                "tier": tier,
                "timestamp": timestamp,
                "neighbors": {}
            }
            self.vec_store.append(node_id, vector)
            self.hnsw.add(node_id, vector)

        if neighbors:
            self.data["neurons"][node_id]["neighbors"].update(neighbors)
            for nid, w in neighbors.items():
                if nid not in self.data["neurons"]:
                    self.data["neurons"][nid] = {
                        "content": "", "memory_type": "unknown",
                        "priority": 3, "tier": "cold", "timestamp": "", "neighbors": {}
                    }
                self.data["neurons"][nid]["neighbors"][node_id] = w

        self.adj[node_id] = self.data["neurons"][node_id].get("neighbors", {})

        if len(self.data["neurons"]) % 100 == 0:
            self._save_graph()

    def add_neuron(self, node_id: str, vector: list[float], neighbors: dict[str, float] = None):
        """向后兼容版本（不带元数据）"""
        if node_id not in self.data["neurons"]:
            self.data["neurons"][node_id] = {
                "content": "", "memory_type": "unknown",
                "priority": 3, "tier": "cold", "timestamp": "", "neighbors": {}
            }
            self.vec_store.append(node_id, vector)
            self.hnsw.add(node_id, vector)

        if neighbors:
            self.data["neurons"][node_id]["neighbors"].update(neighbors)
            for nid, w in neighbors.items():
                if nid not in self.data["neurons"]:
                    self.data["neurons"][nid] = {
                        "content": "", "memory_type": "unknown",
                        "priority": 3, "tier": "cold", "timestamp": "", "neighbors": {}
                    }
                self.data["neurons"][nid]["neighbors"][node_id] = w

        self.adj[node_id] = self.data["neurons"][node_id].get("neighbors", {})

    def save(self):
        self._save_graph()
        self.hnsw.save(str(self.hnsw_path))
        print(f"[InfinityDB] 全量保存: {len(self.data['neurons'])} 节点")

    def adjacency_bfs(self, start_id: str, max_hops: int = 3) -> dict[int, list[str]]:
        """Adjacency BFS（图扩散）"""
        if start_id not in self.adj:
            return {}

        result: dict[int, list[str]] = defaultdict(list)
        visited = {start_id}
        frontier = {start_id}

        for hop in range(1, max_hops + 1):
            next_frontier = set()
            for node_id in frontier:
                for neighbor_id in self.adj.get(node_id, {}):
                    if neighbor_id not in visited:
                        visited.add(neighbor_id)
                        next_frontier.add(neighbor_id)
                        result[hop].append(neighbor_id)
            frontier = next_frontier
            if not frontier:
                break
        return dict(result)

    def has_warm_nodes(self) -> bool:
        """检查是否有 warm 节点（避免空搜索浪费）"""
        for neuron in self.data["neurons"].values():
            if neuron.get("tier") == "warm":
                return True
        return False

    def update_access(self, neuron_ids: list[str]):
        """
        更新 access_count / last_accessed / tier（Recall 时调用）。
        tier 规则：priority >= 4 或 access_count > 10 → warm，否则 cold。
        """
        from datetime import datetime, timezone
        now = datetime.now(timezone.utc).isoformat()
        changed = False
        for nid in neuron_ids:
            if nid not in self.data["neurons"]:
                continue
            neuron = self.data["neurons"][nid]
            neuron["access_count"] = neuron.get("access_count", 0) + 1
            neuron["last_accessed"] = now
            priority = neuron.get("priority", 3)
            access_count = neuron["access_count"]
            if priority >= 4 or access_count > 10:
                new_tier = "warm"
            else:
                new_tier = "cold"
            if neuron.get("tier") != new_tier:
                neuron["tier"] = new_tier
                changed = True
        if changed:
            self._save_graph()

    def vector_search(
        self,
        query_vector: list[float],
        k: int = 10,
        tier_filter: str = None,
    ) -> list[tuple[str, float]]:
        """
        暴力向量检索（小数据集可靠）。
        tier_filter="warm"：只搜 warm 节点
        tier_filter="cold"：只搜 cold 节点
        tier_filter=None：搜全部
        """
        if not self.adj:
            return []
        scores = []
        for nid in self.adj.keys():
            if tier_filter:
                if self.data["neurons"].get(nid, {}).get("tier") != tier_filter:
                    continue
            vec = self.vec_store.get(nid)
            if vec:
                cos = cosine_similarity(query_vector, vec)
                scores.append((cos, nid))
        scores.sort(key=lambda x: x[0], reverse=True)
        return [(nid, cos) for cos, nid in scores[:k]]

    def get_neurons(self, neuron_ids: list[str]) -> dict[str, dict]:
        """批量获取神经元元数据"""
        result = {}
        for nid in neuron_ids:
            if nid in self.data["neurons"]:
                neuron = self.data["neurons"][nid].copy()
                neuron["id"] = nid
                neuron.pop("neighbors", None)
                result[nid] = neuron
        return result

    def get_all_neurons(self) -> dict[str, dict]:
        """获取所有神经元"""
        return self.data["neurons"]

    def keyword_search(self, query: str, k: int = 20) -> list[tuple[str, float]]:
        """
        关键词全文搜索（O(n) 全表）
        在 recall 并行路径中使用：先 HNSW 拿到候选，再在候选里关键词过滤
        """
        query_lower = query.lower()
        results = []
        for nid, neuron in self.data["neurons"].items():
            content = neuron.get("content", "")
            if query_lower in content.lower():
                priority = neuron.get("priority", 3)
                results.append((nid, float(priority) / 10.0))

        results.sort(key=lambda x: x[1], reverse=True)
        return results[:k]

    def update_config(self, config: dict):
        """更新 recall_config"""
        self.data["config"]["recall"] = config
        self._save_graph()

    def get_config(self) -> dict:
        """获取 recall_config"""
        return self.data.get("config", {}).get("recall", {})

    def combined_recall(self, query_vector: list[float], max_hops: int = 3, k: int = 10) -> list[dict]:
        """组合召回：HNSW + BFS"""
        seeds = self.vector_search(query_vector, k=k)
        activations = {nid: float(score) for nid, score in seeds}

        for seed_id in list(activations.keys()):
            bfs = self.adjacency_bfs(seed_id, max_hops=max_hops)
            for hop, node_ids in bfs.items():
                weight = activations.get(seed_id, 0.0) * (0.5 ** hop)
                for nid in node_ids:
                    activations[nid] = max(activations.get(nid, 0.0), weight)

        sorted_act = sorted(activations.items(), key=lambda x: x[1], reverse=True)
        return [{"id": nid, "activation": round(score, 4)} for nid, score in sorted_act[:k]]

    def stats(self) -> dict:
        return {
            "nodes": len(self.data["neurons"]),
            "edges": sum(len(v) for v in self.adj.values()),
            "vectors": len(self.vec_store),
            "hnsw_nodes": len(self.hnsw.nodes),
            "max_hnsw_level": self.hnsw.max_level,
        }


if __name__ == "__main__":
    import time
    db = InfinityDBLite()

    print("\n=== 添加 200 个测试节点 ===")
    t0 = time.time()
    for i in range(200):
        vec = [random.random() * 2 - 1 for _ in range(VECTOR_DIM)]
        neighbors = {f"node_{i-1}": 1.0} if i > 0 else None
        db.add_neuron(f"node_{i}", vec, neighbors)
    db.save()
    print(f"  耗时: {(time.time()-t0)*1000:.1f}ms")

    print("\n=== 向量检索 (top-5) ===")
    t0 = time.time()
    query = [random.random() * 2 - 1 for _ in range(VECTOR_DIM)]
    results = db.vector_search(query, k=5)
    print(f"  耗时: {(time.time()-t0)*1000:.1f}ms")
    for nid, score in results:
        print(f"  [{score:.4f}] {nid}")

    print("\n=== BFS (3 hops from node_100) ===")
    t0 = time.time()
    bfs = db.adjacency_bfs("node_100", max_hops=3)
    print(f"  耗时: {(time.time()-t0)*1000:.1f}ms")
    for hop, nids in bfs.items():
        print(f"  hop {hop}: {len(nids)} nodes")

    print("\n=== 统计 ===")
    print(db.stats())
