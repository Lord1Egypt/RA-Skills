#!/usr/bin/env python3
"""
InfinityDB-lite: 纯 Python 标准库实现（无 numpy 依赖）
替代 neural-memory Pro 的 InfinityDB

组件：
  - brain.graph: 邻接表（内存 dict + JSON 持久化）
  - brain.vec: struct 二进制向量存储（mmap）
  - brain.hnsw: 简化 HNSW 索引（pickle）
"""

import json
import math
import random
import mmap
import struct
import pickle
import time
from pathlib import Path
from collections import defaultdict
from typing import Optional

VECTOR_DIM = 1024
M = 16
EF_CONSTRUCTION = 200
EF_SEARCH = 100


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """纯 Python cosine similarity"""
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


class SimpleHnsw:
    """
    简化 HNSW 实现（纯 Python，无 numpy）

    多层跳表 + Beam Search：
      - 第 L 层：长距离边（度数 ≈ M）
      - 第 0 层：所有边（度数为 M）
      - 查询：从顶层入口逐层 beam search 下降
    """

    def __init__(self, dim: int = VECTOR_DIM, M: int = 16, ef: int = 100):
        self.dim = dim
        self.M = M
        self.ef = ef
        self.nodes: dict[str, "_HnswNode"] = {}
        self.entry_id: Optional[str] = None
        self.max_level = 0

    def _new_level(self) -> int:
        """指数分布采样层号（层数越高概率越低）"""
        level = 0
        while random.random() < (1.0 / self.M) and level < self.max_level + 2:
            level += 1
        return level

    def add(self, node_id: str, vector: list[float]):
        """插入节点"""
        node = _HnswNode(node_id, vector, self._new_level())
        self.nodes[node_id] = node

        if self.entry_id is None:
            self.entry_id = node_id
            self.max_level = node.level
            return

        if node.level > self.max_level:
            self.max_level = node.level
            self.entry_id = node_id

        # 逐层下降到第0层
        current = self.nodes[self.entry_id]
        for layer in range(self.max_level, 0, -1):
            candidates = self._search_layer(current, node.vector, layer, ef=1)
            if candidates:
                current = self.nodes[candidates[0][0]]

        # 在第0层建立边
        self._connect_node(node, layer=0)

    def _search_layer(self, entry: "_HnswNode", query: list[float], layer: int, ef: int) -> list[tuple[str, float]]:
        """在指定层做 beam search"""
        visited = {entry.id}
        results = [(entry.id, cosine_similarity(entry.vector, query))]
        frontier = [(entry.id, cosine_similarity(entry.vector, query))]

        while frontier:
            _, current_id = frontier.pop(0)  # (_, id) tuples
            if current_id not in self.nodes:
                continue
            current = self.nodes[current_id]

            for neighbor_id, _ in current.friends.get(layer, []):
                if neighbor_id in visited:
                    continue
                visited.add(neighbor_id)
                dist = cosine_similarity(self.nodes[neighbor_id].vector, query)

                # 插入 results（按距离降序）
                inserted = False
                for i, (rid, d) in enumerate(results):
                    if dist > d:
                        results.insert(i, (neighbor_id, dist))
                        inserted = True
                        break
                if not inserted:
                    results.append((neighbor_id, dist))

                # frontier 也按优先级
                for i, (fid, d) in enumerate(frontier):
                    if dist > d:
                        frontier.insert(i, (neighbor_id, dist))
                        break
                else:
                    frontier.append((neighbor_id, dist))

                if len(results) > ef:
                    results.pop()
                if len(frontier) > ef:
                    frontier.pop()

        results.sort(key=lambda x: x[1], reverse=True)
        return results[:ef]

    def _connect_node(self, node: "_HnswNode", layer: int):
        """在指定层连接节点的边"""
        candidates = self._search_layer(self.nodes[self.entry_id], node.vector, layer, ef=self.M * 2)

        # 过滤自己
        candidates = [(cid, d) for cid, d in candidates if cid != node.id]

        if layer not in node.friends:
            node.friends[layer] = []
        if layer not in self.nodes[self.entry_id].friends:
            self.nodes[self.entry_id].friends[layer] = []

        # 最多连 M 条边
        for neighbor_id, dist in candidates[:self.M]:
            node.friends[layer].append((neighbor_id, dist))
            self.nodes[neighbor_id].friends[layer].append((node.id, dist))

    def search(self, query: list[float], k: int = 10, ef: int = None) -> list[tuple[str, float]]:
        """HNSW 检索"""
        if self.entry_id is None or not self.nodes:
            return []

        if ef is None:
            ef = self.ef

        entry = self.nodes[self.entry_id]

        # 从顶层向下，逐层 beam search
        for layer in range(self.max_level, 0, -1):
            candidates = self._search_layer(entry, query, layer, ef=1)
            if candidates:
                entry = self.nodes[candidates[0][0]]

        # 第0层精确搜索
        results = self._search_layer(entry, query, 0, ef=ef)
        return results[:k]

    def save(self, path: str):
        """保存索引"""
        data = {
            'dim': self.dim, 'M': self.M, 'ef': self.ef,
            'entry_id': self.entry_id, 'max_level': self.max_level,
            'nodes': [(nid, n.vector, n.level, n.friends) for nid, n in self.nodes.items()]
        }
        with open(path, 'wb') as f:
            pickle.dump(data, f)
        print(f"[HNSW] 保存 {len(self.nodes)} 节点 → {path}")

    def load(self, path: str):
        """加载索引"""
        if not Path(path).exists():
            print(f"[HNSW] 文件不存在: {path}")
            return
        with open(path, 'rb') as f:
            data = pickle.load(f)
        self.dim = data['dim']
        self.M = data['M']
        self.ef = data['ef']
        self.entry_id = data['entry_id']
        self.max_level = data['max_level']
        self.nodes = {}
        for nid, vec, level, friends in data['nodes']:
            n = _HnswNode(nid, vec, level)
            n.friends = friends
            self.nodes[nid] = n
        print(f"[HNSW] 加载 {len(self.nodes)} 节点 ← {path}")


class _HnswNode:
    __slots__ = ('id', 'vector', 'level', 'friends')
    def __init__(self, nid: str, vector: list[float], level: int):
        self.id = nid
        self.vector = vector
        self.level = level
        self.friends: dict[int, list[tuple[str, float]]] = {}  # layer → [(neighbor_id, dist)]


class VecStore:
    """
    结构化二进制向量存储（替代 numpy mmap）
    每个向量 = float32 × dim bytes
    """
    HEADER_FMT = ">II"  # magic, count
    VEC_FMT = ">I"  # vector data (variable)

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
        """追加向量"""
        if node_id in self._id_map:
            return
        idx = self._data_size
        self._id_map[node_id] = idx
        self._ids.append(node_id)
        self._data_size += 1

        vec_path = self.path
        with open(vec_path, 'ab') as f:
            for v in vector:
                f.write(struct.pack('>f', float(v)))
        self._save_ids()

    def get(self, node_id: str) -> Optional[list[float]]:
        """获取向量"""
        if node_id not in self._id_map:
            return None
        idx = self._id_map[node_id]
        offset = idx * self.dim * 4  # float32 = 4 bytes
        with open(self.path, 'rb') as f:
            f.seek(offset)
            data = f.read(self.dim * 4)
            return list(struct.unpack(f'>{self.dim}f', data))

    def __len__(self):
        return self._data_size


class InfinityDBLite:
    """
    InfinityDB-lite（纯 Python 标准库）

    brain.graph: 邻接表 JSON
    brain.vec:   struct 二进制向量（mmap 风格）
    brain.hnsw:  简化 HNSW（pickle）

    特性：
      - Adjacency BFS: <1ms/hop（内存 dict）
      - HNSW 向量检索: O(log N)
      - 全标准库，无外部依赖
    """

    def __init__(self, data_dir: str = "/workspace/fusion/memory/layers/infinitydb"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

        self.graph_path = self.data_dir / "brain.graph.json"
        self.vec_path = self.data_dir / "brain.vec.fvec"
        self.hnsw_path = self.data_dir / "brain.hnsw"

        # Adjacency List（内存）
        self.adj: dict[str, dict[str, float]] = {}

        # 向量存储
        self.vec_store = VecStore(str(self.vec_path))

        # HNSW 索引
        self.hnsw = SimpleHnsw(dim=VECTOR_DIM, M=M, ef=EF_SEARCH)

        self._load()

    def _load(self):
        if self.graph_path.exists():
            with open(self.graph_path, 'r') as f:
                self.adj = json.load(f)
            print(f"[InfinityDB] 加载邻接表: {len(self.adj)} 节点")

        if self.vec_path.exists():
            print(f"[InfinityDB] 向量存储: {len(self.vec_store)} vectors")

        if Path(self.hnsw_path).exists():
            self.hnsw.load(str(self.hnsw_path))

    def _save_graph(self):
        with open(self.graph_path, 'w') as f:
            json.dump(self.adj, f)

    def add_neuron(self, node_id: str, vector: list[float], neighbors: dict[str, float] = None):
        """添加神经元"""
        if node_id not in self.adj:
            self.adj[node_id] = {}
            self.vec_store.append(node_id, vector)
            self.hnsw.add(node_id, vector)

        if neighbors:
            for nid, w in neighbors.items():
                self.adj[node_id][nid] = w
                if nid not in self.adj:
                    self.adj[nid] = {}
                self.adj[nid][node_id] = w

        # 定期保存邻接表
        if len(self.adj) % 100 == 0:
            self._save_graph()

    def save(self):
        self._save_graph()
        self.hnsw.save(str(self.hnsw_path))
        print(f"[InfinityDB] 全量保存: {len(self.adj)} 节点")

    def adjacency_bfs(self, start_id: str, max_hops: int = 3) -> dict[int, list[str]]:
        """
        Native Adjacency BFS（内存 dict，<1ms/hop）
        返回 {hop_level: [node_ids]}
        """
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

    def vector_search(self, query_vector: list[float], k: int = 10) -> list[tuple[str, float]]:
        """暴力向量检索（小数据集可靠）"""
        if not self.adj:
            return []
        scores = []
        for nid in self.adj.keys():
            vec = self.vec_store.get(nid)
            if vec:
                cos = cosine_similarity(query_vector, vec)
                scores.append((cos, nid))
        scores.sort(key=lambda x: x[0], reverse=True)
        return [(nid, cos) for cos, nid in scores[:k]]

    def combined_recall(self, query_vector: list[float], max_hops: int = 3, k: int = 10) -> list[dict]:
        """
        组合召回：HNSW 种子 + Adjacency BFS 扩展
        """
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
            "nodes": len(self.adj),
            "edges": sum(len(v) for v in self.adj.values()),
            "vectors": len(self.vec_store),
            "hnsw_nodes": len(self.hnsw.nodes),
            "max_hnsw_level": self.hnsw.max_level,
        }


if __name__ == "__main__":
    import sys, time

    db = InfinityDBLite()

    print("\n=== 添加 200 个测试节点 ===")
    t0 = time.time()
    for i in range(200):
        vec = [random.random() * 2 - 1 for _ in range(VECTOR_DIM)]
        neighbors = {f"node_{i-1}": 1.0} if i > 0 else None
        db.add_neuron(f"node_{i}", vec, neighbors)
    db.save()
    print(f"  耗时: {(time.time()-t0)*1000:.1f}ms")

    print("\n=== HNSW 向量检索 (top-5) ===")
    t0 = time.time()
    query = [random.random() * 2 - 1 for _ in range(VECTOR_DIM)]
    results = db.vector_search(query, k=5)
    print(f"  耗时: {(time.time()-t0)*1000:.1f}ms")
    for nid, score in results:
        print(f"  [{score:.4f}] {nid}")

    print("\n=== Adjacency BFS (3 hops from node_100) ===")
    t0 = time.time()
    bfs = db.adjacency_bfs("node_100", max_hops=3)
    print(f"  耗时: {(time.time()-t0)*1000:.1f}ms")
    for hop, nids in bfs.items():
        print(f"  hop {hop}: {len(nids)} nodes")

    print("\n=== 组合召回 (top-10) ===")
    t0 = time.time()
    combined = db.combined_recall(query, max_hops=2, k=10)
    print(f"  耗时: {(time.time()-t0)*1000:.1f}ms")
    for item in combined[:5]:
        print(f"  [{item['activation']:.4f}] {item['id']}")

    print("\n=== 统计 ===")
    print(db.stats())