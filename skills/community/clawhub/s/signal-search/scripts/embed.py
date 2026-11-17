"""scripts/embed.py - 向量化（默认关，V11 补强）。sentence-transformers 优先，缺失降级关键词向量。

注意：sentence-transformers / transformers 未必安装；本模块永不因缺失而崩溃，缺失时返回
降级向量（关键词哈希），由调用方决定是否用于语义去重/rerank / M51 语义核验。默认关，仅开启后启用。

模型默认 paraphrase-multilingual-MiniLM-L12-v2（中文友好，多语语义）；可在 config.embed.model
覆盖（如英文 all-MiniLM-L6-v2）。懒加载，首次调用才下载/实例化。
"""

import hashlib
import json
import os
import re
import threading
from typing import List, Optional

CONFIG_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config.json"
)

_DEFAULT_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"

_TRY_ST = False
try:
    from sentence_transformers import SentenceTransformer  # type: ignore

    _TRY_ST = True
except Exception:
    _TRY_ST = False

_model = None
_model_name = None
_model_lock = threading.Lock()  # D7：模型懒加载加锁，避免并发首调重复实例化/竞态


def _load_model_name():
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return (json.load(f).get("embed", {}) or {}).get("model", _DEFAULT_MODEL)
    except Exception:
        return _DEFAULT_MODEL


def _get_model():
    global _model, _model_name
    if _model is not None:
        return _model
    with _model_lock:  # 持锁再判一次（double-checked locking）
        if _model is not None:
            return _model
        if not _TRY_ST:
            return None
        _model_name = _load_model_name()
        try:
            _model = SentenceTransformer(_model_name)
        except Exception:
            _model = None
        return _model


def embed(texts: List[str]) -> Optional[List[List[float]]]:
    """返回 list[vector]，无可用后端时返回降级关键词向量（仍可用余弦相似度）。"""
    if not texts:
        return None
    m = _get_model()
    if m is not None:
        return m.encode(texts).tolist()
    out = []
    for t in texts:
        toks = set(re.findall(r"[\w\u4e00-\u9fa5]{2,}", t or ""))
        vec = [0.0] * 64
        for tok in toks:
            h = int(hashlib.md5(tok.encode("utf-8")).hexdigest(), 16)
            vec[h % 64] += 1.0
        out.append(vec)
    return out


def similarity(a: List[float], b: List[float]) -> float:
    try:
        import math

        dot = sum(x * y for x, y in zip(a, b))
        na = math.sqrt(sum(x * x for x in a))
        nb = math.sqrt(sum(y * y for y in b))
        return dot / (na * nb) if na and nb else 0.0
    except Exception:
        return 0.0
