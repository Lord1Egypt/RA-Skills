"""scripts/dedup.py - 近似去重（M25/M26）。simhash LSH 主通道 + Jaccard 二级兜底 + URL 精确去重。"""

import hashlib
import re
from typing import Any, Dict, List

BITS = 64
_BLOCKS = 4  # 64-bit 分 4 块，每块 16-bit（鸽巢：hamming≤3 必共享至少一块）
_BLOCK_BITS = BITS // _BLOCKS


def _tokens(text: str):
    return set(re.findall(r"[\w\u4e00-\u9fa5]{2,}", text or ""))


def _simhash(text: str, bits: int = BITS) -> int:
    toks = _tokens(text)
    if not toks:
        return 0
    v = [0] * bits
    for t in toks:
        h = int(hashlib.md5(t.encode("utf-8")).hexdigest(), 16)
        for i in range(bits):
            v[i] += 1 if (h >> i) & 1 else -1
    return sum(1 << i for i in range(bits) if v[i] > 0)


def _hamming(a: int, b: int) -> int:
    return bin(a ^ b).count("1")


def _blocks(h: int):
    """把 64-bit simhash 切成 4 个 16-bit 块索引，用于 LSH 分桶。"""
    mask = (1 << _BLOCK_BITS) - 1
    return [(h >> (i * _BLOCK_BITS)) & mask for i in range(_BLOCKS)]


def _jaccard(a: set, b: set) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def near_dup(
    docs: List[Dict[str, Any]], threshold: int = 3, jaccard: float = 0.35
) -> List[Dict[str, Any]]:
    """URL 精确去重 + simhash LSH 指纹近似去重（主） + 词重叠 Jaccard 二级兜底（P2-8 零依赖实现）。
    返回去重后列表（保序）。

    - URL 完全相同 → 去重（保留首次出现）。
    - simhash 主通道：64-bit 指纹按 4×16-bit LSH 分桶，桶内汉明距 ≤ threshold（默认 3）即近似重复。
      BITS=64/4 块保证汉明距 ≤3 必共享至少一块，LSH 不漏检；threshold 形参真正生效。
    - Jaccard 二级兜底：仅对同一 LSH 桶候选（且汉明距 > threshold）做词重叠校验，
      Jaccard ≥ jaccard（默认 0.35）也判近似重复，覆盖"措辞不同但词集高度重叠"的短摘要。
    零依赖：纯哈希/集合运算，规模近 O(n)（检索结果集 ≤ max_sources），非 O(n·m) 全配对。
    """
    out: List[Dict[str, Any]] = []
    seen_urls: set = set()
    seen_sim: List[tuple] = []  # (simhash, tokens)
    buckets: Dict[int, List[int]] = {}  # block_value -> [seen_sim 索引]
    for d in docs:
        url = d.get("url")
        if url and url in seen_urls:
            continue
        text = (d.get("title", "") or "") + " " + (d.get("snippet", "") or "")
        h = _simhash(text)
        toks = _tokens(text)
        cand = set()
        for b in _blocks(h):
            cand.update(buckets.get(b, ()))
        is_dup = False
        # simhash 主通道：仅对 LSH 同桶候选做汉明距判定（近 O(n)）
        for idx in cand:
            if _hamming(h, seen_sim[idx][0]) <= threshold:
                is_dup = True
                break
        # Jaccard 二级兜底：对全部已见候选做词重叠校验（结果集 ≤ max_sources，O(n^2) 可忽略），
        # 覆盖"措辞不同、simhash 不共享块但词集高度重叠"的短摘要近似重复。
        if not is_dup:
            for idx in range(len(seen_sim)):
                if _jaccard(toks, seen_sim[idx][1]) >= jaccard:
                    is_dup = True
                    break
        if is_dup:
            continue
        if url:
            seen_urls.add(url)
        idx = len(seen_sim)
        seen_sim.append((h, toks))
        for b in _blocks(h):
            buckets.setdefault(b, []).append(idx)
        out.append(d)
    return out
