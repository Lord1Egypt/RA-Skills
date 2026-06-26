#!/usr/bin/env python3
"""
L1: Classifier - 去噪 / Chunk / MemoryType / Priority / Tier / Hash / Vector / Cosine Dedup

流程（Scanner 之后）：
  Stage 2: 去噪（21+ 条正则规则）
  Stage 2: Chunk 拆分（≤250字/段，50字 overlap，防止断裂）
  Stage 2: MemoryType 分类（14 种）
  Stage 2: Priority / Tier 分配
  Stage 2: content_hash 精确去重（第1级）
  Stage 2: simhash 近似去重（第2级，纯文本，海明距离<3）
  Stage 2: Ollama bge-m3 向量编码（batch=10，1024d）
  Stage 2: cosine similarity > 0.85 粗去重（第3级）
  Stage 3: 语义密度质量过滤（中文≥4字符 OR 英文≥3词）
  Stage 4: 输出到 L2A 区

防断裂原则：
  - Scanner 层只丢弃100%噪音，边界情况保留
  - Classifier 做二次语义密度检查
  - Chunk 拆分保证 50 字 overlap，不丢失边界内容

输出：/workspace/fusion/memory/layers/l2a/YYYY-MM-DD.jsonl
"""

import json
import os
import re
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
import math
import struct

# 项目根目录（向上推导）
PROJECT_ROOT = Path(__file__).parent.parent.parent


# ============================================================
# Simhash 去重（纯文本，Python 标准库）
# ============================================================

def compute_simhash(content: str) -> int:
    """计算内容的 simhash 值（64位）"""
    try:
        import hashlib
        h = hashlib.md5(content.encode('utf-8')).digest()
        return struct.unpack('>Q', h[:8])[0]
    except Exception:
        return 0


def hamming_distance(hash1: int, hash2: int) -> int:
    """计算两个 simhash 的 Hamming 距离"""
    xor = hash1 ^ hash2
    return bin(xor).count('1')


class SimhashIndex:
    """Simhash 近似去重索引（内存）"""

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

# ============================================================
# 配置
# ============================================================
L2A_DIR = PROJECT_ROOT / "memory" / "layers" / "l2a"
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL = "bge-m3"
OLLAMA_BATCH_SIZE = 20
OLLAMA_TIMEOUT_SEC = 30
OLLAMA_MAX_RETRIES = 3
OLLAMA_IDLE_BETWEEN_BATCHES = 0.1

MAX_CHUNK_CHARS = 250      # 每个 chunk 最大字符数
OVERLAP_CHARS = 50          # chunk 之间的 overlap 字符数（防断裂）
COSINE_THRESHOLD_L1 = 0.85  # cosine similarity 阈值（>0.85 即为近似重复）

# ============================================================
# 去噪规则（DENOISE_PATTERNS）
# 说明：这些规则用于清理 Scanner 阶段未处理的残留噪音。
# Scanner 阶段已过滤大部分噪音，这里做二次清理。
# ============================================================
DENOISE_PATTERNS = [
    # ----- 元信息残留 -----
    (r'^[{]\s*"label"\s*:', ''),                   # metadata JSON 残留
    (r'^[{]\s*"id"\s*:', ''),                      # metadata JSON 残留
    (r'^```json\s*\n?[{}"\']*?\n?```', ''),         # 空 json 代码块

    # ----- 系统前缀 -----
    (r'^\s*\[system[^\]]*\]\s*', ''),
    (r'^\s*\[agent[^\]]*\]\s*', ''),
    (r'^\s*\[openclaw[^\]]*\]\s*', ''),

    # ----- 时间戳线 -----
    (r'^\s*\[(Mon|Tue|Wed|Thu|Fri|Sat|Sun)\s+\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}\s+GMT[+-]\d+\]\s*', ''),

    # ----- 空代码块残留 -----
    (r'^```(json|python|bash|sh|text)?\s*```\s*$', ''),
    (r'^```\s*$', ''),

    # ----- 特殊分隔符行 -----
    (r'^[-*_]{3,}\s*$', ''),                       # --- 或 *** 或 ___

    # ----- 调试/测试残留 -----
    (r'^DEBUG:\s*', ''),
    (r'^TEST:\s*', ''),
    (r'^LOG:\s*', ''),

    # ----- 纯数字/纯符号行 -----
    (r'^\s*\d+\s*$', ''),
    (r'^\s*[.,;:!?]{1,3}\s*$', ''),

    # ----- Session 元信息 -----
    (r'^Session ID:\s*', ''),
    (r'^Session:\s*', ''),
    (r'^Time:\s*', ''),
    (r'^Date:\s*', ''),

    # ----- OpenClaw 内部标记 -----
    (r'^\s*HEARTBEAT(_OK)?\s*$', ''),
    (r'^\s*_SESSION\s*$', ''),
    (r'^\s*_CONTEXT\s*$', ''),

    # ----- 反序列化残留 -----
    (r'^"""\s*$', ''),                             # 空 triple-quote
    (r"^'''\s*$", ''),
]

# ============================================================
# MemoryType 分类规则（按优先级排序，先匹配优先）
# ============================================================
MEMORY_TYPE_PATTERNS = [
    # (pattern, memory_type, priority)
    (r'(TODO|FIXME|BUG|ISSUE|计划|待办|修复|改进)', 'task', 10),
    (r'(决策|决定|结论|结论是|最终方案|选型|架构|技术方案)', 'decision', 9),
    (r'(错误|失败|异常|报错|exception|error|crash)', 'error', 8),
    (r'(密码|secret|token|api_key|私钥|凭证)', 'security', 7),
    (r'(调试|debug|排查|诊断|分析)', 'debug', 6),
    (r'(配置文件|config|settings|参数|配置)', 'config', 5),
    (r'(http|https|localhost|端口|port|endpoint|api)', 'technical', 4),
    (r'(版本|version|V\d+\.\d+|release)', 'version', 3),
    (r'(文件路径|目录|folder|path|directory)', 'file_path', 2),
    (r'(会话|对话|session|chat|聊天)', 'conversation', 1),
]

# ============================================================
# MemoryType 中文标签映射
# ============================================================
MEMORY_TYPE_LABELS = {
    'task': '任务',
    'decision': '决策',
    'error': '错误',
    'security': '安全',
    'debug': '调试',
    'config': '配置',
    'technical': '技术',
    'version': '版本',
    'file_path': '路径',
    'conversation': '对话',
    'fact': '事实',
    'preference': '偏好',
    'custom': '自定义',
    'other': '其他',
}

# ============================================================
# Tier 优先级映射
# ============================================================
TIER_MAP = {
    'task': 1,
    'decision': 1,
    'error': 1,
    'security': 1,
    'debug': 2,
    'config': 2,
    'technical': 2,
    'version': 3,
    'file_path': 3,
    'conversation': 3,
    'fact': 3,
    'preference': 2,
    'custom': 3,
    'other': 4,
}


# ============================================================
# Ollama Encoder（带重试）
# ============================================================
class OllamaEncoder:
    """Ollama bge-m3 向量编码器，带重试和错误处理。"""

    def __init__(self, base_url: str = OLLAMA_BASE_URL, model: str = OLLAMA_MODEL):
        self.base_url = base_url
        self.model = model
        self._client = None

    @property
    def client(self):
        """懒加载 httpx client。"""
        if self._client is None:
            import httpx
            self._client = httpx.Client(base_url=self.base_url, timeout=OLLAMA_TIMEOUT_SEC)
        return self._client

    def encode_batch(self, texts: list[str]) -> Optional[list[list[float]]]:
        """
        批量编码文本为向量。
        返回 None 表示失败（所有重试都失败）。
        每个向量是 1024 维 float。
        """
        import httpx

        valid_texts = []
        for t in texts:
            t = t.strip()
            if t:
                valid_texts.append(t)

        if not valid_texts:
            return []

        results = []
        for i, text in enumerate(valid_texts):
            for attempt in range(OLLAMA_MAX_RETRIES):
                try:
                    resp = self.client.post(
                        "/api/embeddings",
                        json={"model": self.model, "prompt": text}
                    )
                    if resp.status_code == 200:
                        data = resp.json()
                        emb = data.get("embedding", [])
                        if isinstance(emb, list) and len(emb) == 1024:
                            results.append(emb)
                            break
                        else:
                            results.append([0.0] * 1024)
                            break
                    # else: 非 200，重试
                except (httpx.ConnectError, httpx.TimeoutException) as e:
                    print(f"[OllamaEncoder] Attempt {attempt+1} failed for text[{i}]: {e}")
                    import time
                    time.sleep(1 * (attempt + 1))
            else:
                print(f"[OllamaEncoder] All {OLLAMA_MAX_RETRIES} attempts failed for text[{i}]")
                results.append([0.0] * 1024)

        return results if results else None


# ============================================================
# 向量工具
# ============================================================
def cosine_similarity(a: list[float], b: list[float]) -> float:
    """计算两个向量的 cosine similarity。"""
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


# ============================================================
# 内容质量检查（语义密度）
# ============================================================
def content_quality_check(content: str) -> tuple[bool, str]:
    """
    Stage 3: 语义密度检查
    判断内容是否有实质语义（不是噪音残留）。

    返回 (should_keep, reason)
    """
    if not content or len(content.strip()) < 5:
        return False, "too_short"

    # 统计中文字符
    chinese_chars = re.findall(r'[\u4e00-\u9fff]', content)
    # 统计英文单词
    english_words = re.findall(r'[a-zA-Z]{3,}', content)

    # 通过条件（满足任一）：
    # 1. 中文 ≥ 4 字符
    # 2. 英文 ≥ 3 个单词
    # 3. 内容长度 ≥ 30 字符（混合内容或符号为主）
    if len(chinese_chars) >= 4:
        return True, "ok"
    if len(english_words) >= 3:
        return True, "ok"
    if len(content.strip()) >= 30:
        return True, "ok"

    return False, "no_semantic_density"


# ============================================================
# 去噪
# ============================================================
def denoise_content(content: str, memory_type: str = "other") -> str:
    """
    Stage 2: 去噪
    应用 21+ 条正则规则，清理残留噪音。
    """
    result = content

    for pattern, replacement in DENOISE_PATTERNS:
        result = re.sub(pattern, replacement, result, flags=re.IGNORECASE | re.MULTILINE)

    # 清理多余空白行
    result = re.sub(r'\n{3,}', '\n\n', result)
    result = result.strip()

    return result


# ============================================================
# Chunk 拆分（防断裂：50字 overlap）
# ============================================================
def chunk_content(content: str, max_chars: int = MAX_CHUNK_CHARS, overlap: int = OVERLAP_CHARS) -> list[str]:
    """
    Stage 2: Chunk 拆分
    按最大字符数拆分，边界处保证 50 字 overlap，防止内容断裂。
    返回 chunk 列表。
    """
    if len(content) <= max_chars:
        return [content]

    chunks = []
    start = 0

    while start < len(content):
        end = start + max_chars
        chunk = content[start:end]

        # 如果不是最后一个 chunk，需要处理边界
        if end < len(content):
            # 尝试在句号、换行、逗号处断开
            for sep in ['\n\n', '\n', '。', '，', '、', '. ', ', ', ' ']:
                sep_pos = chunk.rfind(sep)
                if sep_pos > max_chars * 0.5:
                    chunk = chunk[:sep_pos + len(sep)]
                    end = start + len(chunk)
                    break

        chunks.append(chunk)
        start = end - overlap if end < len(content) else end

    # 合并过小的 chunk（最后一个 chunk 太小则合并到前一个）
    if len(chunks) > 1 and len(chunks[-1]) < max_chars * 0.3:
        chunks[-2] += chunks[-1]
        chunks.pop()

    return chunks


# ============================================================
# MemoryType 分类
# ============================================================
def classify_memory_type(content: str) -> str:
    """
    Stage 2: MemoryType 分类
    根据内容关键词匹配，返回 memory_type。
    """
    for pattern, mem_type, priority in MEMORY_TYPE_PATTERNS:
        if re.search(pattern, content, re.IGNORECASE):
            return mem_type
    return "other"


# ============================================================
# Priority / Tier 分配
# ============================================================
def assign_priority_tier(content: str, memory_type: str) -> tuple[int, int]:
    """
    Stage 2: Priority / Tier 分配
    Priority: 1-5（1最高，5最低）
    Tier: 1-4（1最高，4最低）
    """
    tier = TIER_MAP.get(memory_type, 4)

    # 根据内容长度和质量微调
    priority = min(max(3, tier), 5)

    # 重要标记提升优先级
    if re.search(r'(重要|关键|核心|必须|紧急|critical|important|urgent)', content):
        priority = min(priority, 1)

    return priority, tier


# ============================================================
# L1 Classifier
# ============================================================
class L1Classifier:
    """L1 分类器：去噪 / Chunk / Type / Priority / Hash / Simhash / Vector / Cosine Dedup"""

    def __init__(self):
        self.encoder = OllamaEncoder()
        self.seen_hashes: set[str] = set()  # content_hash 去重（第1级）
        self.seen_vectors: list[tuple[str, list[float]]] = []  # (content_hash, vector)
        self.simhash_index = SimhashIndex(threshold=3)  # simhash 去重（第2级）
        # cost tracker stats
        self._dedup_level1 = 0  # content_hash 去重数
        self._dedup_level2 = 0  # simhash 去重数
        self._dedup_level3 = 0  # cosine 去重数
        self._ollama_encode_batches = 0  # Ollama encode_batch 调用次数
        self._ollama_tokens_approx = 0  # 估算 token 数

    def process(self, raw_chunks: list[dict]) -> list[dict]:
        """
        完整处理流程（正确顺序）：
          1. 去噪（先清理噪音）
          2. 内容质量检查（语义密度，去噪后）
          3. MemoryType 分类（去噪后，关键词更干净）
          4. Priority / Tier 分配（基于去噪后内容）
          5. Chunk 拆分（基于去噪后内容）
          6. content_hash 精确去重（第1级）
          7. Ollama 向量编码
          8. cosine similarity 近似去重（第2级，宽松阈值）
          9. 返回处理后的 chunks
        """
        processed = []

        for raw in raw_chunks:
            content = raw.get("content", "")

            # Step 1: 去噪（先清理噪音，再做后续判断）
            denoised = denoise_content(content)

            # Step 2: 内容质量检查（去噪后，防止噪音干扰判断）
            should_keep, reason = content_quality_check(denoised)
            if not should_keep:
                raw["_dropped"] = True
                raw["_drop_reason"] = reason
                processed.append(raw)
                continue

            # Step 3: MemoryType 分类（去噪后，关键词更干净）
            memory_type = classify_memory_type(denoised)

            # Step 4: Priority / Tier 分配（基于去噪后内容）
            priority, tier = assign_priority_tier(denoised, memory_type)

            # Step 5: Chunk 拆分（基于去噪后内容）
            chunks = chunk_content(denoised)
            if not chunks:
                raw["_dropped"] = True
                raw["_drop_reason"] = "chunk_empty"
                processed.append(raw)
                continue

            # content_hash（第1级精确去重）
            content_hash = hashlib.sha256(denoised.encode()).hexdigest()[:16]

            for i, chunk_text in enumerate(chunks):
                chunk_hash = hashlib.sha256(f"{content_hash}:{i}".encode()).hexdigest()[:16]

                # 第1级去重：精确 hash（chunk 级别）
                if chunk_hash in self.seen_hashes:
                    self._dedup_level1 += 1
                    continue
                self.seen_hashes.add(chunk_hash)

                # 第2级去重：simhash 近似去重（纯文本，海明距离<3）
                chunk_simhash = compute_simhash(chunk_text)
                sim_dups = self.simhash_index.find_duplicates(chunk_simhash)
                if sim_dups:
                    # simhash 命中，说明和已有 chunk 表述近似
                    # 跳过，不加入 processed_chunk（由 cosine 做最终判断）
                    self._dedup_level2 += 1
                    continue

                chunk_id = hashlib.sha256(
                    f"{raw['session_id']}:{raw['byte_offset']}:{i}:{chunk_text[:50]}".encode()
                ).hexdigest()[:16]

                # simhash 索引注册（供后续 chunks 比对）
                self.simhash_index.add(chunk_simhash, chunk_id)

                processed_chunk = {
                    "id": chunk_id,
                    "session_id": raw["session_id"],
                    "content": chunk_text,
                    "byte_offset": raw["byte_offset"],
                    "timestamp": raw.get("timestamp", datetime.now(timezone.utc).isoformat()),
                    "source": raw.get("source", "user_message"),
                    "memory_type": memory_type,
                    "priority": priority,
                    "tier": tier,
                    "content_hash": content_hash,
                    "chunk_index": i,
                    "total_chunks": len(chunks),
                    "dedup_level": 0,
                    "_scan_filter_reason": raw.get("_scan_filter_reason", ""),
                }
                processed.append(processed_chunk)

        # ============================================================
        # 向量编码 + cosine 去重（第2级）
        # ============================================================
        self._encode_and_dedup(processed)

        return processed

    def _encode_and_dedup(self, chunks: list[dict]):
        """
        Stage 2: Ollama bge-m3 向量编码 + cosine similarity 去重
        cosine > 0.85 的 chunk 被标记为 dedup_level=1（近似重复）
        """
        unencoded = [c for c in chunks if c.get("dedup_level") == 0]
        if not unencoded:
            return

        texts = [c["content"] for c in unencoded]
        embeddings = self.encoder.encode_batch(texts)

        if embeddings is None:
            print(f"[L1 Classifier] 向量编码失败，所有 chunk 标记为 _dropped（不写入 L2A）")
            for c in unencoded:
                c["_dropped"] = True
                c["_drop_reason"] = "encoding_failed"
            return

        for chunk, embedding in zip(unencoded, embeddings):
            chunk["vector"] = embedding

            # cosine 去重（第3级）
            is_dup = False
            for existing_hash, existing_vec in self.seen_vectors:
                sim = cosine_similarity(embedding, existing_vec)
                if sim > COSINE_THRESHOLD_L1:
                    chunk["dedup_level"] = 1
                    chunk["dup_of"] = existing_hash
                    is_dup = True
                    self._dedup_level3 += 1
                    break

            if not is_dup:
                chunk["dedup_level"] = 0
                self.seen_vectors.append((chunk["content_hash"], embedding))

        # Ollama encode_batch 调用 + token 估算（按每条 ~50 token）
        self._ollama_encode_batches += 1
        self._ollama_tokens_approx += len(texts) * 50

    def get_stats(self) -> dict:
        """返回 cost tracker 用的统计"""
        return {
            "ollama_calls": self._ollama_encode_batches,
            "tokens_approx": self._ollama_tokens_approx,
            "dedup_level1": self._dedup_level1,
            "dedup_level2": self._dedup_level2,
            "dedup_level3": self._dedup_level3,
        }

    def process_from_tmp(self) -> list[dict]:
        """
        从 tmp 文件恢复并处理（crash 恢复路径）。
        """
        from scan_sessions_incremental import RAW_CHUNKS_TMP_FILE

        if not os.path.exists(RAW_CHUNKS_TMP_FILE):
            return []

        chunks = []
        with open(RAW_CHUNKS_TMP_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    chunks.append(json.loads(line))

        if not chunks:
            return []

        processed = self.process(chunks)

        # 清理 tmp
        os.remove(RAW_CHUNKS_TMP_FILE)

        return processed


# ============================================================
# 写入 L2A（atomic write）
# ============================================================
def save_to_l2a(chunks: list[dict], date_str: str = None):
    """
    Stage 4: 写入 L2A 区
    过滤掉 _dropped=True 的 chunk，使用 atomic write。
    """
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")

    L2A_DIR.mkdir(parents=True, exist_ok=True)
    output_file = L2A_DIR / f"{date_str}.jsonl"
    tmp_file = output_file.with_suffix('.tmp.jsonl')

    # 过滤掉 _dropped=True 或 dedup_level > 0 的 chunk
    # _dropped=True：质量检查未通过或编码失败
    # dedup_level > 0：cosine 近似重复，不需要重复写入 L2A
    valid_chunks = [
        c for c in chunks
        if not c.get("_dropped") and c.get("dedup_level", 0) == 0
    ]

    with open(tmp_file, 'w', encoding='utf-8') as f:
        for chunk in valid_chunks:
            # 不写入 vector（节省 L2A 空间，向量只在 L3 使用）
            out = {k: v for k, v in chunk.items() if k != "vector"}
            f.write(json.dumps(out, ensure_ascii=False) + '\n')

    tmp_file.rename(output_file)
    print(f"[L1 Classifier] 写入 L2A: {output_file} ({len(valid_chunks)} 条有效)")


# ============================================================
# 入口
# ============================================================
def run():
    """手动运行 L1 Classifier（测试用）。"""
    from scan_sessions_incremental import ByteOffsetScanner

    scanner = ByteOffsetScanner()
    raw_chunks = scanner.scan()

    if not raw_chunks:
        print("无新 chunks")
        return

    classifier = L1Classifier()
    processed = classifier.process(raw_chunks)

    drop_count = sum(1 for c in processed if c.get("_dropped"))
    valid_count = len(processed) - drop_count

    print(f"处理完成: {valid_count} 有效, {drop_count} 过滤")
    date_str = datetime.now().strftime("%Y-%m-%d")
    save_to_l2a(processed, date_str)


if __name__ == "__main__":
    run()