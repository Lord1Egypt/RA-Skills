#!/usr/bin/env python3
"""
L2: Daily Consolidator
读取 L2A 区数据，执行四级去重 + Transitive Closure + 关系补全 + Dynamic priority
触发时间：每天 00:30（Asia/Shanghai）

流程：
  ① 读取 L2A 区所有 chunks（processed=False）
  ② 按 session_id 分组
  ③ 双模式窗口（≤500全量，>500滑动200/100 overlap50%）
  ④ Transitive Closure 传递闭包补全
  ⑤ 四级去重（content_hash → Type协同cos → simhash → hnsw）
  ⑥ Type 二次校验
  ⑦ Dynamic priority（session内引用≥3次 → priority+2）
  ⑧ processed=True 标记
  ⑨ 增量删除 L2A
  ⑩ 写入 L2 区
"""

import json
import os
import math
import hashlib
import time
from datetime import datetime, timezone
from pathlib import Path

# 项目根目录（向上推导）
PROJECT_ROOT = Path(__file__).parent.parent.parent

from collections import defaultdict
from typing import Optional


# 项目根目录（向上推导）
PROJECT_ROOT = Path(__file__).parent.parent.parent
# 配置
L2A_DIR = PROJECT_ROOT / "memory" / "layers" / "l2a"
L2_DIR = PROJECT_ROOT / "memory" / "layers" / "l2"
OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "bge-m3")
VECTOR_DIM = 1024
BATCH_SIZE = 10

# ===== 批量优化配置（防断裂防护）=====
OLLAMA_BATCH_SIZE = 20           # 单次 HTTP 最大条数
OLLAMA_TIMEOUT_SEC = 30          # 单次请求超时（秒）
OLLAMA_MAX_RETRIES = 3          # 失败重试次数
OLLAMA_RETRY_SLEEP_SEC = 1.0    # 重试间隔（秒）
OLLAMA_IDLE_BETWEEN_BATCHES = 0.1  # 每批次之间喘息（秒），防止 Ollama 过载

MAX_L2A_CHUNKS_PER_RUN = 5000    # 单次运行最大处理量（防止内存溢出）

# Type 协同去重阈值
TYPE_COS_THRESHOLDS = {
    "boundary": 0.85,
    "error": 0.87,
    "decision": 0.88,
    "fact": 0.88,
    "context": 0.88,
    "workflow": 0.88,
    "reference": 0.88,
    "instruction": 0.88,
    "default": 0.90,
    "preference": 0.93,
    "insight": 0.93,
    "todo": 0.93,
    "hypothesis": 0.93,
    "prediction": 0.93,
    "schema": 0.93,
    "tool": 0.93,
}

def get_cos_threshold(memory_type: str) -> float:
    return TYPE_COS_THRESHOLDS.get(memory_type, TYPE_COS_THRESHOLDS["default"])


def cosine_similarity(vec1: list[float], vec2: list[float]) -> float:
    dot = sum(a * b for a, b in zip(vec1, vec2))
    norm1 = math.sqrt(sum(a * a for a in vec1))
    norm2 = math.sqrt(sum(b * b for b in vec2))
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot / (norm1 * norm2)


def compute_simhash(content: str) -> int:
    """计算内容的 simhash 值（64位）"""
    import struct
    try:
        import hashlib
        h = hashlib.md5(content.encode('utf-8')).digest()
        return struct.unpack('>Q', h[:8])[0]
    except:
        return 0


def hamming_distance(hash1: int, hash2: int) -> int:
    """计算两个 simhash 的 Hamming 距离"""
    xor = hash1 ^ hash2
    return bin(xor).count('1')


class SimhashIndex:
    """Simhash 近似去重索引"""

    def __init__(self, threshold: int = 3):
        self.hashes: list[tuple[int, str]] = []  # (simhash, chunk_id)
        self.threshold = threshold

    def add(self, simhash: int, chunk_id: str):
        self.hashes.append((simhash, chunk_id))

    def find_duplicates(self, simhash: int) -> list[str]:
        """查找与给定 simhash 距离 < threshold 的所有 chunk_id"""
        dup_ids = []
        for h, cid in self.hashes:
            if hamming_distance(simhash, h) < self.threshold:
                dup_ids.append(cid)
        return dup_ids


class HnswIndex:
    """HNSW 向量索引（用于第4级去重）"""

    def __init__(self, dim: int = VECTOR_DIM, max_elements: int = 10000):
        self.dim = dim
        self.max_elements = max_elements
        self.elements: list[list[float]] = []
        self.ids: list[str] = []
        self._index = None

    def add(self, chunk_id: str, vector: list[float]):
        self.ids.append(chunk_id)
        self.elements.append(vector)
        if len(self.elements) >= self.max_elements * 0.8:
            self._rebuild()

    def _rebuild(self):
        """延迟构建 hnswlib"""
        try:
            import hnswlib
            self._index = hnswlib.Index(space='cosine', dim=self.dim)
            self._index.init_index(max_elements=self.max_elements)
            for i, vec in enumerate(self.elements):
                self._index.add_items(vec, i)
        except ImportError:
            pass

    def search(self, vector: list[float], k: int = 5, threshold: float = 0.95) -> list[tuple[str, float]]:
        """搜索相似向量，返回 (chunk_id, cosine)"""
        if self._index is None:
            return []
        try:
            labels, distances = self._index.knn_query(vector, k=k)
            results = []
            for label, dist in zip(labels[0], distances[0]):
                cos = 1.0 - dist  # hnswlib cosine 返回的是距离
                if cos > threshold:
                    results.append((self.ids[label], cos))
            return results
        except:
            return []


class OllamaEncoder:
    """Ollama 向量编码器（带超时重试 + 空内容过滤）"""

    def __init__(self, base_url: str = OLLAMA_BASE_URL, model: str = OLLAMA_MODEL,
                 batch_size: int = 20, timeout_sec: int = 30, max_retries: int = 3):
        self.base_url = base_url
        self.model = model
        self.batch_size = batch_size        # 单次 HTTP 最大条数
        self.timeout_sec = timeout_sec      # 单次请求超时
        self.max_retries = max_retries       # 失败重试次数

    def encode_batch(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        # 过滤空内容
        filtered = [t.strip() for t in texts if t and t.strip()]
        if not filtered:
            return []

        results = []
        for i in range(0, len(filtered), self.batch_size):
            batch = filtered[i:i + self.batch_size]
            vecs = self._encode_batch_with_retry(batch)
            results.extend(vecs)
            # 喘息（防止 Ollama 过载）
            time.sleep(OLLAMA_IDLE_BETWEEN_BATCHES)

        # 映射回原始顺序（空内容补零）
        result_map = {}
        for t, v in zip(filtered, results):
            result_map[t] = v

        output = []
        for t in texts:
            if t and t.strip() in result_map:
                output.append(result_map[t.strip()])
            else:
                output.append([0.0] * VECTOR_DIM)
        return output

    def _encode_batch_with_retry(self, texts: list[str]) -> list[list[float]]:
        """单批次编码，失败重试"""
        import urllib.request
        import time

        url = f"{self.base_url}/api/embeddings"
        headers = {'Content-Type': 'application/json'}

        for attempt in range(self.max_retries):
            try:
                batch_results = []
                for text in texts:
                    payload = json.dumps({"model": self.model, "prompt": text}).encode('utf-8')
                    req = urllib.request.Request(url, data=payload, headers=headers)
                    with urllib.request.urlopen(req, timeout=self.timeout_sec) as resp:
                        result = json.loads(resp.read())
                        embedding = result.get("embedding")
                        if embedding and len(embedding) == VECTOR_DIM:
                            batch_results.append(embedding)
                        else:
                            batch_results.append([0.0] * VECTOR_DIM)
                return batch_results
            except Exception as e:
                print(f"[OllamaEncoder] 第 {attempt+1} 次失败: {e}")
                if attempt == self.max_retries - 1:
                    print(f"[OllamaEncoder] 放弃，跳过 {len(texts)} 条")
                    return [[0.0] * VECTOR_DIM for _ in texts]
                time.sleep(1)
        return [[0.0] * VECTOR_DIM for _ in texts]

def sliding_windows(chunks: list[dict], window_size: int = 200, overlap: int = 100) -> list[list[dict]]:
    """生成滑动窗口"""
    if len(chunks) <= window_size:
        return [chunks]
    windows = []
    step = window_size - overlap
    start = 0
    while start < len(chunks):
        end = min(start + window_size, len(chunks))
        windows.append(chunks[start:end])
        start += step
    return windows


def build_session_graph(chunks: list[dict]) -> dict[str, list[str]]:
    """
    构建 session 内引用关系图（用于 Dynamic priority）
    
    使用中文友好的重叠检测：
    - 英文：按空格分词，词长 >= 3
    - 中文：按字符（2-4字词），有意义的词汇
    - 重叠阈值：>= 3 个重叠词（提高 precision，减少 false positive）
    - 排除常见停用词（中文：的、了、在、是、和、等；英文：the、a、an、is、to）
    """
    import re
    
    # 停用词列表
    STOPWORDS = {
        # 中文常见停用词
        '的', '了', '在', '是', '和', '与', '或', '等', '之', '于', '被', '有', '个', '为', '上', '下', '中', '来', '去', '到', '把', '让', '给', '用', '从', '向', '对', '这', '那', '什', '么', '怎', '吗', '呢', '吧', '啊', '哦', '呀', '哇', '嘿', '喂', '嗯', '噢', '哼',
        # 英文停用词
        'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'shall', 'can', 'to', 'of', 'in', 'for', 'on', 'with', 'at', 'by', 'from', 'as', 'or', 'and', 'but', 'if', 'then', 'than', 'so', 'that', 'this', 'it', 'its', 'i', 'you', 'he', 'she', 'we', 'they', 'what', 'which', 'who', 'how', 'when', 'where', 'why',
    }
    
    def extract_words(text: str) -> set:
        """中英文混合分词"""
        words = set()
        # 英文按空格分词
        english_parts = text.lower().split()
        for part in english_parts:
            # 清理标点
            clean = re.sub(r'[^a-z0-9]', '', part)
            if len(clean) >= 3 and clean not in STOPWORDS:
                words.add(clean)
        # 中文：提取 2-4 字的有意义词组（简单 N-gram）
        chinese_only = re.sub(r'[a-z0-9]', '', text)
        for n in [2, 3, 4]:
            for i in range(len(chinese_only) - n + 1):
                word = chinese_only[i:i+n]
                # 排除纯停用词组合
                if word not in STOPWORDS and not all(c in '的了是在和与' for c in word):
                    words.add(word)
        return words
    
    relations = defaultdict(list)  # chunk_id -> [referenced_chunk_ids]
    word_map = {}
    for c in chunks:
        cid = c["id"]
        word_map[cid] = extract_words(c["content"])

    for chunk in chunks:
        chunk_id = chunk["id"]
        chunk_words = word_map[chunk_id]
        
        if len(chunk_words) < 3:
            continue  # 内容太短，跳过
        
        for other_id, other_words in word_map.items():
            if other_id == chunk_id:
                continue
            if len(other_words) < 3:
                continue
            
            # 计算重叠词（至少 3 个有意义词重叠）
            overlap = chunk_words & other_words
            # 过滤掉停用词造成的重叠
            meaningful_overlap = {w for w in overlap if len(w) >= 2}
            
            if len(meaningful_overlap) >= 3:
                relations[chunk_id].append(other_id)

    return relations


def transitive_closure(chunks: list[dict], relations: dict[str, list[str]]) -> list[dict]:
    """传递闭包：A→B→C → A→C（weight=0.5×min）"""
    # 构建邻接表
    adj = defaultdict(list)  # from_id -> [(to_id, weight)]
    for chunk in chunks:
        for rel in relations.get(chunk["id"], []):
            adj[chunk["id"]].append((rel, 1.0))

    # BFS 找传递路径
    inferred = []
    for chunk in chunks:
        visited = {chunk["id"]}
        queue = [(chunk["id"], 1.0)]

        while queue:
            current, weight = queue.pop(0)
            for next_id, w in adj.get(current, []):
                if next_id not in visited:
                    visited.add(next_id)
                    new_weight = min(weight, w) * 0.5  # 0.5 × min
                    inferred.append({
                        "from": chunk["id"],
                        "to": next_id,
                        "rel_type": "CAUSED_BY",
                        "weight": new_weight,
                        "inferred": True
                    })
                    queue.append((next_id, new_weight))

    return inferred


class L2Processor:
    """L2 处理器：双模式窗口 + 四级去重 + Transitive Closure + Dynamic priority"""

    def __init__(self):
        self.encoder = OllamaEncoder()
        self.simhash_index = SimhashIndex(threshold=3)
        self.hnsw_index = HnswIndex()
        self.content_hash_index: dict[str, dict] = {}  # hash -> chunk_info

    def process(self, l2a_chunks: list[dict]) -> list[dict]:
        """处理 L2A chunks"""
        # Step 1: 按 session_id 分组
        session_groups = defaultdict(list)
        for chunk in l2a_chunks:
            session_groups[chunk["session_id"]].append(chunk)

        results = []
        all_inferred_relations = []

        # Step 2: 对每个 session 处理
        for session_id, session_chunks in session_groups.items():
            windows = sliding_windows(session_chunks, window_size=200, overlap=100)

            # ============================================================
            # 正确顺序（修复版）
            # 1. 先四级去重（窗口内 dedup）
            # 2. 再基于去重后的 unique chunks 构建 session graph
            # 3. 最后做 Transitive Closure
            # 这样保证图的完整性，防止 dedup 后图断裂
            # ============================================================

            for window in windows:
                # Step 3: 四级去重（先 dedup，去掉 duplicate chunks）
                deduped = self._dedup_window(window)

                # Step 4: 关系补全（基于去重后的 unique chunks，防止图断裂）
                # 注意：这里用 deduped 而不是 window，确保图只包含 unique chunks
                unique_chunks = [c for c in deduped if not c.get("dup_of")]
                relations = build_session_graph(unique_chunks)

                # Step 5: Transitive Closure（在 unique chunks 上做，路径完整）
                inferred = transitive_closure(unique_chunks, relations)
                all_inferred_relations.extend(inferred)

                # 为 deduped 中的每个 chunk 附加 inferred relations
                inferred_map = defaultdict(list)
                for inf in inferred:
                    inferred_map[inf["from"]].append(inf)

                for chunk in deduped:
                    chunk["inferred_relations"] = inferred_map.get(chunk["id"], [])

                results.extend(deduped)

        return results

    def _dedup_window(self, chunks: list[dict]) -> list[dict]:
        """四级去重"""
        output = []

        for chunk in chunks:
            chunk_id = chunk.get("id", "")

            # 第1级：content_hash 精确匹配（L1 已完成，这里做校验）
            content_hash = chunk.get("content_hash", hashlib.sha256(chunk["content"].encode()).hexdigest()[:16])
            if content_hash in self.content_hash_index:
                existing = self.content_hash_index[content_hash]
                output.append({
                    **chunk,
                    "dup_of": existing["id"],
                    "dedup_level": 1,
                    "processed": True
                })
                continue

            # 第2级：Type 协同 cosine
            memory_type = chunk.get("memory_type", "default")
            threshold = get_cos_threshold(memory_type)
            vector = chunk.get("vector", [])

            dup_found = False
            if vector:
                for hist_hash, hist_info in self.content_hash_index.items():
                    hist_vector = hist_info.get("vector", [])
                    if hist_vector:
                        cos = cosine_similarity(vector, hist_vector)
                        if cos > threshold:
                            output.append({
                                **chunk,
                                "dup_of": hist_info["id"],
                                "dedup_level": 2,
                                "cosine": cos,
                                "processed": True
                            })
                            dup_found = True
                            break

            if dup_found:
                continue

            # 第3级：simhash 近似去重
            simhash = compute_simhash(chunk["content"])
            sim_dups = self.simhash_index.find_duplicates(simhash)
            if sim_dups:
                output.append({
                    **chunk,
                    "dup_of": sim_dups[0],
                    "dedup_level": 3,
                    "processed": True
                })
                continue

            # 第4级：hnsw 向量（最后兜底）
            if vector:
                hnsw_results = self.hnsw_index.search(vector, k=5, threshold=0.95)
                if hnsw_results:
                    output.append({
                        **chunk,
                        "dup_of": hnsw_results[0][0],
                        "dedup_level": 4,
                        "processed": True
                    })
                    continue

            # 通过所有去重，作为新 chunk
            self.content_hash_index[content_hash] = chunk
            self.simhash_index.add(simhash, chunk_id)
            if vector:
                self.hnsw_index.add(chunk_id, vector)

            output.append({
                **chunk,
                "dup_of": None,
                "dedup_level": 0,
                "processed": True
            })

        return output

    def apply_dynamic_priority(self, chunks: list[dict]) -> list[dict]:
        """Dynamic priority：session 内引用≥3次 → priority+2"""
        session_groups = defaultdict(list)
        for chunk in chunks:
            session_groups[chunk["session_id"]].append(chunk)

        ref_count = defaultdict(int)  # chunk_id -> count

        for session_id, session_chunks in session_groups.items():
            content_map = {c["id"]: c["content"].lower() for c in session_chunks}
            for chunk in session_chunks:
                content = chunk.get("content", "").lower()
                chunk_id = chunk["id"]
                count = 0
                for other_id, other_content in content_map.items():
                    if other_id == chunk_id:
                        continue
                    words = set(other_content.split())
                    if len(words) > 3:
                        overlap = sum(1 for w in words if w in content)
                        if overlap >= 2:
                            count += 1
                ref_count[chunk_id] = count

        # 应用 priority 调整
        for chunk in chunks:
            if ref_count[chunk["id"]] >= 3:
                chunk["priority"] = chunk.get("priority", 3) + 2
                chunk["priority_boosted"] = True

        return chunks


def load_l2a_chunks(date_str: str = None) -> list[dict]:
    """加载 L2A 区数据"""
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")

    l2a_file = L2A_DIR / f"{date_str}.jsonl"
    if not l2a_file.exists():
        print(f"[L2] L2A 文件不存在: {l2a_file}")
        return []

    chunks = []
    with open(l2a_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                obj = json.loads(line)
                if not obj.get("processed"):  # 只处理未处理的
                    chunks.append(obj)

    print(f"[L2] 加载 L2A chunks: {len(chunks)} 条")
    return chunks


def save_to_l2(chunks: list[dict], inferred_relations: list[dict], date_str: str = None):
    """写入 L2 区（atomic write：先写 tmp，再 rename）"""
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")

    L2_DIR.mkdir(parents=True, exist_ok=True)
    l2_file = L2_DIR / f"{date_str}.jsonl"
    tmp_file = l2_file.with_suffix('.tmp.jsonl')

    with open(tmp_file, 'w', encoding='utf-8') as f:
        for chunk in chunks:
            # 写入时移除 vector（减少文件大小），L3 会重新编码
            output = {k: v for k, v in chunk.items() if k != 'vector'}
            output["inferred_relations"] = [r for r in inferred_relations if r["from"] == chunk["id"]]
            f.write(json.dumps(output, ensure_ascii=False) + '\n')

    # atomic rename（防 crash）
    tmp_file.rename(l2_file)
    print(f"[L2] 写入 L2 区: {l2_file}")


def mark_l2a_processed(l2a_chunks: list[dict], date_str: str = None):
    """标记 L2A 中已处理的 chunks（增量删除，atomic write 防 crash）"""
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")

    l2a_file = L2A_DIR / f"{date_str}.jsonl"
    if not l2a_file.exists():
        return

    processed_ids = {c["id"] for c in l2a_chunks if c.get("processed")}

    # 读出现有数据
    remaining = []
    with open(l2a_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                obj = json.loads(line)
                if obj.get("id") not in processed_ids:
                    remaining.append(obj)

    # atomic write：先写 tmp，再 rename
    tmp_file = l2a_file.with_suffix('.tmp')
    with open(tmp_file, 'w', encoding='utf-8') as f:
        for obj in remaining:
            f.write(json.dumps(obj, ensure_ascii=False) + '\n')
    tmp_file.rename(l2a_file)

    print(f"[L2] L2A 增量删除完成（atomic write），剩余 {len(remaining)} 条未处理")


def run():
    """L2 入口，返回 stats dict"""
    print(f"[L2] 开始执行: {datetime.now().isoformat()}")

    # Step 0: 加载 checkpoint（断点恢复）
    from l2_checkpoint import load_checkpoint, save_checkpoint, clear_checkpoint, CHECKPOINT_INTERVAL
    cp = load_checkpoint()
    date_str = datetime.now().strftime("%Y-%m-%d")
    checkpoint_line = 0  # 当前已checkpoint的行号
    processed_ids_from_cp = set()
    if cp and cp.get("date_str") == date_str:
        processed_ids_from_cp = set(cp.get("processed_ids", []))
        print(f"[L2] Checkpoint 恢复: {len(processed_ids_from_cp)} 条已处理，跳过")

    # Step 1: 加载 L2A 数据
    l2a_chunks = load_l2a_chunks(date_str)
    if not l2a_chunks:
        print("[L2] 无待处理 chunks")
        return {}

    # Step 1b: 过滤掉 checkpoint 中已处理的 chunks
    # L2A chunks 用 content_hash 作为稳定 ID
    if processed_ids_from_cp:
        before = len(l2a_chunks)
        l2a_chunks = [c for c in l2a_chunks if c.get("content_hash") not in processed_ids_from_cp]
        print(f"[L2] Checkpoint 过滤后: {before} → {len(l2a_chunks)} 条")

    chunks_in = len(l2a_chunks)
    if not l2a_chunks:
        # checkpoint 恢复完了，但没有新 chunks
        clear_checkpoint()
        print("[L2] 无待处理 chunks（全部已被 checkpoint 覆盖）")
        return {}

    # Step 2: 处理
    processor = L2Processor()
    processed = processor.process(l2a_chunks)

    # Step 3: Dynamic priority
    processed = processor.apply_dynamic_priority(processed)

    # 统计
    new_count = sum(1 for c in processed if c["dedup_level"] == 0)
    dedup_counts = defaultdict(int)
    for c in processed:
        if c["dedup_level"] > 0:
            dedup_counts[c["dedup_level"]] += 1

    print(f"[L2] 处理完成: 新增={new_count}")
    for level, count in sorted(dedup_counts.items()):
        print(f"  Level-{level} 去重: {count}")

    # Step 4: 收集 inferred relations
    inferred_relations = []
    for chunk in processed:
        inferred_relations.extend(chunk.get("inferred_relations", []))

    # Step 5: 写 checkpoint（先于 mark，防止 crash 重复处理）
    # 每处理 CHECKPOINT_INTERVAL 条写一次，累积 processed_ids
    all_processed_ids = set(processed_ids_from_cp)
    for i, chunk in enumerate(processed):
        all_processed_ids.add(chunk["id"])
        if (i + 1) % CHECKPOINT_INTERVAL == 0:
            save_checkpoint(date_str, all_processed_ids, checkpoint_line + i + 1)
            print(f"[L2] Checkpoint 已保存: {len(all_processed_ids)} 条已处理")

    # Step 6: 先标记 L2A 已处理（atomic write）
    mark_l2a_processed(processed, date_str)

    # Step 7: 再写入 L2 区
    save_to_l2(processed, inferred_relations, date_str)

    # Step 8: 成功完成，清除 checkpoint
    clear_checkpoint()

    print(f"[L2] 结束: {datetime.now().isoformat()}")

    # 返回 stats（供 cost tracker 用）
    return {
        "chunks_in": chunks_in,
        "chunks_out": new_count,
        "dedup_level1": dedup_counts.get(1, 0),
        "dedup_level2": dedup_counts.get(2, 0),
        "dedup_level3": dedup_counts.get(3, 0),
        "dedup_level4": dedup_counts.get(4, 0),
        "ollama_calls": 0,
        "tokens_approx": 0,
    }


if __name__ == "__main__":
    run()