#!/usr/bin/env python3
"""
向量工具
"""
import math
from typing import Optional


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """
    计算两个向量的 cosine similarity

    Args:
        a: 向量 A
        b: 向量 B

    Returns:
        cosine similarity (0.0 ~ 1.0)
    """
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot / (norm_a * norm_b)


def is_zero_vector(vec: list[float], dim: int = 1024) -> bool:
    """判断是否是零向量"""
    return not vec or len(vec) != dim or vec == [0.0] * dim


def normalize_vector(vec: list[float]) -> list[float]:
    """L2 归一化向量"""
    norm = math.sqrt(sum(x * x for x in vec))
    if norm == 0:
        return vec
    return [x / norm for x in vec]


def batch_encode_vectors(encoder, texts: list[str], batch_size: int = 20) -> list[list[float]]:
    """
    批量编码向量（带分片）

    Args:
        encoder: OllamaEncoder 实例
        texts: 文本列表
        batch_size: 每批大小

    Returns:
        向量列表
    """
    results = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        vecs = encoder.encode_batch(batch)
        results.extend(vecs)
    return results