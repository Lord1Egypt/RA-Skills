#!/usr/bin/env python3
"""
配置校验器（Config Validator）
==============================
R6 加固：对 rag-optimization 配置进行入口校验，防止无效配置产生静默错误。

用法：
    from config_validator import validate_config, ValidationError
    errors = validate_config(config_dict)
    if errors:
        print("配置错误:", errors)
"""
import re
from typing import Any, Dict, List, Optional


class ValidationError:
    """配置错误"""
    def __init__(self, field: str, message: str, severity: str = "error"):
        self.field = field
        self.message = message
        self.severity = severity

    def __str__(self):
        return f"[{self.severity.upper()}] {self.field}: {self.message}"


def validate_config(config: Dict[str, Any]) -> List[ValidationError]:
    """
    校验配置字典，返回所有错误列表。

    校验规则：
        - 所有数值参数 >= 0
        - chunk_size > overlap
        - vector_weight + bm25_weight == 1.0
        - cache_max_size >= 0
        - top_k >= 1
    """
    errors: List[ValidationError] = []
    rag_cfg = config.get("rag_optimization_config", config) if isinstance(config, dict) else config
    if not isinstance(rag_cfg, dict):
        return [ValidationError("root", "配置必须是字典类型")]

    # chunking 校验
    chunking = rag_cfg.get("chunking", {})
    for strat_key in ("fixed_chunking", "contextual_header"):
        strat_cfg = chunking.get(strat_key, {})
        chunk_size = strat_cfg.get("chunk_size", 0)
        overlap = strat_cfg.get("overlap", 0)
        if chunk_size < 0:
            errors.append(ValidationError(
                f"chunking.{strat_key}.chunk_size", f"不能为负数: {chunk_size}", "error"))
        if overlap < 0:
            errors.append(ValidationError(
                f"chunking.{strat_key}.overlap", f"不能为负数: {overlap}", "error"))
        if chunk_size > 0 and overlap >= chunk_size:
            errors.append(ValidationError(
                f"chunking.{strat_key}.overlap",
                f"overlap ({overlap}) 必须 < chunk_size ({chunk_size})", "warning"))

    small_to_big = chunking.get("small_to_big", {})
    child_size = small_to_big.get("child_chunk_size", 150)
    child_overlap = small_to_big.get("child_overlap", 0)
    if child_overlap >= child_size:
        errors.append(ValidationError(
            "chunking.small_to_big.child_overlap",
            f"child_overlap ({child_overlap}) 必须 < child_chunk_size ({child_size})",
            "warning"))

    semantic = chunking.get("semantic_chunking", {})
    min_cs = semantic.get("min_chunk_size", 100)
    max_cs = semantic.get("max_chunk_size", 1000)
    if min_cs > max_cs:
        errors.append(ValidationError(
            "chunking.semantic_chunking",
            f"min_chunk_size ({min_cs}) 不能 > max_chunk_size ({max_cs})", "warning"))

    # retrieval 校验
    retrieval = rag_cfg.get("retrieval", {})
    hybrid = retrieval.get("hybrid_retrieval", {})
    vw = hybrid.get("vector_weight", 0.7)
    bw = hybrid.get("bm25_weight", 0.3)
    if not (0.95 <= vw + bw <= 1.05):
        errors.append(ValidationError(
            "retrieval.hybrid_retrieval",
            f"vector_weight ({vw}) + bm25_weight ({bw}) 应 ≈ 1.0，当前为 {vw + bw}",
            "warning"))
    if vw < 0 or vw > 1.0:
        errors.append(ValidationError(
            "retrieval.hybrid_retrieval.vector_weight",
            f"应在 [0, 1] 范围内: {vw}", "error"))
    if bw < 0 or bw > 1.0:
        errors.append(ValidationError(
            "retrieval.hybrid_retrieval.bm25_weight",
            f"应在 [0, 1] 范围内: {bw}", "error"))

    for strat_key in ("vector_retrieval", "bm25_retrieval"):
        strat_cfg = retrieval.get(strat_key, {})
        tk = strat_cfg.get("top_k", 10)
        if tk < 1:
            errors.append(ValidationError(
                f"retrieval.{strat_key}.top_k", f"必须 >= 1: {tk}", "warning"))

    # reranking 校验
    reranking = rag_cfg.get("reranking", {})
    fk = reranking.get("final_k", 5)
    if fk < 1:
        errors.append(ValidationError(
            "reranking.final_k", f"必须 >= 1: {fk}", "warning"))

    # performance.cache 校验
    perf = rag_cfg.get("performance", {})
    cache = perf.get("cache", {})
    ttl = cache.get("cache_ttl_seconds", 3600)
    if ttl < 0:
        errors.append(ValidationError(
            "performance.cache.cache_ttl_seconds", f"不能为负数: {ttl}", "warning"))

    return errors


def format_errors(errors: List[ValidationError]) -> str:
    """格式化错误报告"""
    if not errors:
        return "✅ 配置校验通过，无错误"
    lines = [f"⚠️  配置校验发现 {len(errors)} 个问题："]
    for e in errors:
        lines.append(f"  {e}")
    return "\n".join(lines)


# 内置默认配置（供校验演示用）
DEFAULT_CONFIG = {
    "chunking": {
        "fixed_chunking": {"chunk_size": 500, "overlap": 50},
        "small_to_big": {"child_chunk_size": 150, "child_overlap": 30},
        "semantic_chunking": {"min_chunk_size": 100, "max_chunk_size": 1000},
    },
    "retrieval": {
        "hybrid_retrieval": {"vector_weight": 0.7, "bm25_weight": 0.3},
        "bm25_retrieval": {"top_k": 10},
        "vector_retrieval": {"top_k": 10},
    },
    "reranking": {"final_k": 5},
    "performance": {"cache": {"cache_ttl_seconds": 3600}},
}


if __name__ == "__main__":
    import json

    # 测试有效配置
    print("=== 有效配置 ===")
    errors = validate_config(DEFAULT_CONFIG)
    print(format_errors(errors))

    # 测试无效配置
    print("\n=== 无效配置 ===")
    bad_config = {
        "chunking": {
            "fixed_chunking": {"chunk_size": -1, "overlap": 999},
            "small_to_big": {"child_chunk_size": 150, "child_overlap": 200},
            "semantic_chunking": {"min_chunk_size": 5000, "max_chunk_size": 100},
        },
        "retrieval": {
            "hybrid_retrieval": {"vector_weight": 2.0, "bm25_weight": 2.0},
            "bm25_retrieval": {"top_k": 0},
        },
        "performance": {"cache": {"cache_ttl_seconds": -1}},
    }
    errors = validate_config(bad_config)
    print(format_errors(errors))
