#!/usr/bin/env python3
"""
L3: Biweekly Consolidator + InfinityDB Writer（方案A：单一数据源）
读取 L2 区数据，写入 InfinityDB（唯一写入）
触发时间：每两天 03:00（Asia/Shanghai）

流程（单一数据源，无双写）：
  ① 读取 L2 区 graph_written=False 的 chunks
  ② 收集神经元 + 元数据 + 关系
  ③ 批量写入 InfinityDB（add_neuron_with_metadata）
  ④ 更新 recall_config 到 InfinityDB
  ⑤ 增量删除 L2
"""

import json
import os
import math
import time
import struct
from datetime import datetime, timezone
from pathlib import Path
from collections import defaultdict, Counter
from typing import Optional


PROJECT_ROOT = Path(__file__).parent.parent.parent
L2_DIR = PROJECT_ROOT / "memory" / "layers" / "l2"
INFINITYDB_DIR = PROJECT_ROOT / "memory" / "layers" / "infinitydb"
OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "bge-m3")
VECTOR_DIM = 1024

# 批量优化
OLLAMA_BATCH_SIZE = 20
OLLAMA_TIMEOUT_SEC = 30
OLLAMA_MAX_RETRIES = 3
OLLAMA_RETRY_SLEEP_SEC = 1.0
OLLAMA_IDLE_BETWEEN_BATCHES = 0.1
HNSW_BATCH_SIZE = 500

import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "recall"))
from infinitydb_lite import InfinityDBLite


def compute_cosine(vec1: list[float], vec2: list[float]) -> float:
    dot = sum(a * b for a, b in zip(vec1, vec2))
    norm1 = math.sqrt(sum(a * a for a in vec1))
    norm2 = math.sqrt(sum(b * b for b in vec2))
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot / (norm1 * norm2)


class OllamaEncoder:
    def __init__(self, base_url: str = OLLAMA_BASE_URL, model: str = OLLAMA_MODEL,
                 batch_size: int = 20, timeout_sec: int = 30, max_retries: int = 3):
        self.base_url = base_url
        self.model = model
        self.batch_size = batch_size
        self.timeout_sec = timeout_sec
        self.max_retries = max_retries

    def encode_batch(self, texts: list[str]) -> list[list[float]]:
        """Ollama /api/embeddings 不支持 batch，逐条编码"""
        if not texts:
            return []
        import httpx
        results = []
        for i, text in enumerate(texts):
            text = text.strip()
            if not text:
                results.append([0.0] * VECTOR_DIM)
                continue
            for attempt in range(self.max_retries):
                try:
                    client = httpx.Client(base_url=self.base_url, timeout=self.timeout_sec)
                    resp = client.post(
                        "/api/embeddings",
                        json={"model": self.model, "prompt": text}
                    )
                    if resp.status_code == 200:
                        data = resp.json()
                        emb = data.get("embedding", [])
                        if isinstance(emb, list) and len(emb) == VECTOR_DIM:
                            results.append(emb)
                            break
                        else:
                            results.append([0.0] * VECTOR_DIM)
                            break
                    elif resp.status_code == 422:
                        results.append([0.0] * VECTOR_DIM)
                        break
                except (httpx.ConnectError, httpx.TimeoutException) as e:
                    if attempt == self.max_retries - 1:
                        print(f"[OllamaEncoder] 第 {attempt+1} 次失败，跳过: {e}")
                        results.append([0.0] * VECTOR_DIM)
                    time.sleep(OLLAMA_RETRY_SLEEP_SEC * (attempt + 1))
                except Exception as e:
                    print(f"[OllamaEncoder] encode error: {e}")
                    results.append([0.0] * VECTOR_DIM)
                    break
            time.sleep(OLLAMA_IDLE_BETWEEN_BATCHES)
        return results


def load_l2_chunks(date_str: str = None) -> tuple[list[dict], list[Path]]:
    """加载 L2 区数据"""
    l2_files = list(L2_DIR.glob("*.jsonl")) if L2_DIR.exists() else []

    if date_str:
        l2_files = [f for f in l2_files if f.stem == date_str]

    if not l2_files:
        if date_str:
            print(f"[L3] L2 文件不存在: {L2_DIR / date_str}.jsonl")
        else:
            print(f"[L3] L2 目录无任何文件: {L2_DIR}")
        return [], []

    chunks = []
    for l2_file in sorted(l2_files):
        with open(l2_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    obj = json.loads(line)
                    if not obj.get("graph_written"):
                        chunks.append(obj)

    print(f"[L3] 加载 L2 chunks: {len(chunks)} 条（来自 {len(l2_files)} 个文件）")
    return chunks, sorted(l2_files)


def generate_schema_neuron(session_chunks: list[dict], encoder: OllamaEncoder) -> Optional[dict]:
    """生成 SCHEMA 神经元（session≥5 chunks）"""
    if len(session_chunks) < 5:
        return None

    contents = [c["content"] for c in session_chunks]
    keywords = tfidf_extract_keywords(contents, top_n=5)
    schema_content = f"Session summary: {', '.join(keywords)}"

    vectors = encoder.encode_batch([schema_content])
    vector = vectors[0] if vectors else []

    return {
        "id": f"schema_{session_chunks[0]['session_id']}",
        "content": schema_content,
        "memory_type": "schema",
        "priority": 4,
        "tier": "warm",
        "vector": vector,
        "connected_chunks": [c["id"] for c in session_chunks],
        "keywords": keywords,
    }


def tfidf_extract_keywords(contents: list[str], top_n: int = 5) -> list[str]:
    word_freq = Counter()
    for content in contents:
        words = content.split()
        word_freq.update(w for w in words if len(w) >= 2)
    return [w for w, _ in word_freq.most_common(top_n)]


class L3Processor:
    """
    L3 处理器（方案A：单一数据源）

    写入流程：
      write_chunks() → 收集神经元数据
      sync_to_infinitydb() → 批量写入 InfinityDB（唯一写入）
    """

    def __init__(self):
        self.encoder = OllamaEncoder()
        self.infinitydb = InfinityDBLite(str(INFINITYDB_DIR))
        self._pending_neurons: list[dict] = []
        self._pending_relations: list[dict] = []
        # cost tracker stats
        self._ollama_calls = 0
        self._tokens_approx = 0

    def write_chunks(self, chunks: list[dict], inferred_relations: list[dict]) -> dict:
        """
        收集神经元数据（只写 InfinityDB，不写 Brain.db）
        """
        now = datetime.now(timezone.utc).isoformat()

        session_groups = defaultdict(list)
        for chunk in chunks:
            session_groups[chunk["session_id"]].append(chunk)

        written_count = 0
        schema_count = 0
        written_ids = []

        for session_id, session_chunks in session_groups.items():
            for chunk in session_chunks:
                neuron_id = chunk["id"]
                content = chunk.get("content", "")
                memory_type = chunk.get("memory_type", "context")
                priority = chunk.get("priority", 3)
                tier = chunk.get("tier", "cold")

                # 重新编码向量
                vector = chunk.get("vector", [])
                if not vector:
                    vectors = self.encoder.encode_batch([content])
                    self._ollama_calls += 1
                    self._tokens_approx += len(content) * 2  # 估算
                    vector = vectors[0] if vectors else []

                # 零向量跳过
                if not vector or len(vector) != VECTOR_DIM or vector == [0.0] * VECTOR_DIM:
                    print(f"[L3] 跳过零向量 chunk: {neuron_id}")
                    continue

                self._pending_neurons.append({
                    "id": neuron_id,
                    "content": content,
                    "vector": vector,
                    "memory_type": memory_type,
                    "priority": priority,
                    "tier": tier,
                    "timestamp": chunk.get("timestamp", now),
                })
                written_ids.append(neuron_id)
                written_count += 1

            # SCHEMA 生成
            schema = generate_schema_neuron(session_chunks, self.encoder)
            if schema:
                self._ollama_calls += 1
                self._tokens_approx += len(schema["content"]) * 2
                self._pending_neurons.append({
                    "id": schema["id"],
                    "content": schema["content"],
                    "vector": schema.get("vector", []),
                    "memory_type": "schema",
                    "priority": 4,
                    "tier": "warm",
                    "timestamp": now,
                })
                written_ids.append(schema["id"])
                schema_count += 1

                for chunk in session_chunks:
                    self._pending_relations.append({
                        "from": schema["id"],
                        "to": chunk["id"],
                        "weight": 1.0,
                        "rel_type": "schema_of",
                    })

        # 收集 inferred relations
        relations_count = 0
        for rel in inferred_relations:
            from_id = rel.get("from")
            to_id = rel.get("to")
            rel_type = rel.get("rel_type", "CAUSED_BY")
            weight = rel.get("weight", 0.5)
            if from_id and to_id:
                self._pending_relations.append({
                    "from": from_id,
                    "to": to_id,
                    "weight": weight,
                    "rel_type": rel_type,
                })
                relations_count += 1

        print(f"[L3] 收集 neurons: {written_count}, schemas: {schema_count}")

        return {
            "neurons_written": written_count,
            "schemas_written": schema_count,
            "relations_written": relations_count,
            "written_ids": written_ids,
            "all_neurons": written_ids,
        }

    def get_stats(self) -> dict:
        """返回 cost tracker 用的统计"""
        return {
            "ollama_calls": self._ollama_calls,
            "tokens_approx": self._tokens_approx,
        }

    def sync_to_infinitydb(self):
        """批量写入 InfinityDB（唯一数据源）"""
        if not self._pending_neurons:
            print("[L3] InfinityDB: 无待写入 neurons")
            return

        adjacencies: dict[str, dict[str, float]] = defaultdict(dict)
        for rel in self._pending_relations:
            adjacencies[rel["from"]][rel["to"]] = rel["weight"]

        total = len(self._pending_neurons)
        for i, neuron in enumerate(self._pending_neurons):
            nid = neuron["id"]
            vector = neuron.get("vector", [])
            neighbors = adjacencies.get(nid, {})

            if vector and len(vector) == VECTOR_DIM:
                self.infinitydb.add_neuron_with_metadata(
                    node_id=nid,
                    vector=vector,
                    neighbors=neighbors,
                    content=neuron.get("content", ""),
                    memory_type=neuron.get("memory_type", "context"),
                    priority=neuron.get("priority", 3),
                    tier=neuron.get("tier", "cold"),
                    timestamp=neuron.get("timestamp", ""),
                )

            if (i + 1) % HNSW_BATCH_SIZE == 0:
                print(f"[L3] InfinityDB 写入进度: {i+1}/{total}")
                time.sleep(OLLAMA_IDLE_BETWEEN_BATCHES)

        self.infinitydb.save()
        print(f"[L3] InfinityDB 写入完成: {total} neurons, {len(self._pending_relations)} relations")

        self._pending_neurons.clear()
        self._pending_relations.clear()

    def update_recall_config(self):
        """更新 recall_config 到 InfinityDB"""
        recall_config = {
            "max_spread_hops": 3,
            "activation_threshold": 0.3,
            "diminishing_returns_enabled": True,
            "diminishing_returns_threshold": 0.15,
            "diminishing_returns_min_neurons": 2,
            "diminishing_returns_grace_hops": 1,
        }
        self.infinitydb.update_config(recall_config)
        print(f"[L3] recall_config 已更新到 InfinityDB")


def mark_l2_graph_written(result: dict, l2_files: list):
    """标记 L2 中已写入的 chunks（atomic write 防 crash）"""
    written_ids = set(result.get("written_ids", []))

    for l2_file in l2_files:
        if not l2_file.exists():
            continue

        remaining = []
        with open(l2_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    obj = json.loads(line)
                    if obj.get("id") not in written_ids:
                        remaining.append(obj)

        tmp_file = l2_file.with_suffix('.tmp')
        with open(tmp_file, 'w', encoding='utf-8') as f:
            for obj in remaining:
                f.write(json.dumps(obj, ensure_ascii=False) + '\n')
        tmp_file.rename(l2_file)

        print(f"[L3] L2 文件清理完成: {l2_file.name}，剩余 {len(remaining)} 条未写入")


def run():
    """L3 入口（方案A：单一 InfinityDB 数据源），返回 stats dict"""
    print(f"[L3] 开始执行: {datetime.now().isoformat()}")

    # Step 1: 加载 L2 数据
    l2_chunks, l2_files = load_l2_chunks()
    if not l2_chunks:
        print("[L3] 无待处理 chunks")
        return {}
    chunks_in = len(l2_chunks)

    inferred_relations = []
    for chunk in l2_chunks:
        inferred_relations.extend(chunk.get("inferred_relations", []))

    # Step 2: 收集神经元数据
    processor = L3Processor()
    result = processor.write_chunks(l2_chunks, inferred_relations)

    # Step 3: 批量写入 InfinityDB
    processor.sync_to_infinitydb()

    # Step 4: 更新 recall_config
    processor.update_recall_config()

    # Step 5: 增量删除 L2
    mark_l2_graph_written(result, l2_files)

    print(f"[L3] 完成: neurons={result['neurons_written']}, schemas={result['schemas_written']}")
    print(f"[L3] 结束: {datetime.now().isoformat()}")

    # 返回 stats（供 cost tracker 用）
    c_stats = processor.get_stats()
    return {
        "chunks_in": chunks_in,
        "neurons_written": result["neurons_written"],
        "schemas_written": result["schemas_written"],
        "relations_written": result["relations_written"],
        "ollama_calls": c_stats["ollama_calls"],
        "tokens_approx": c_stats["tokens_approx"],
        "l2_files_cleared": [str(f.name) for f in l2_files],
    }


if __name__ == "__main__":
    run()
