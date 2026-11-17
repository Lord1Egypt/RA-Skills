#!/usr/bin/env python3
"""
配置加载与管道装配（Config Loader / Pipeline Builder）
======================================================
H2：`assets/config-template.json` 此前**没有任何运行时消费者**——
用户按 SKILL.md 步骤 3 改了配置，却没有任何组件读到它。
本模块把「配置文件 → 组件实例」这条缺失的链路补上。

H10：`config_validator.validate_config()` 此前零调用方。
本模块在 `load_config()` 内调用它，让校验层真正落在入口上。

用法：
    from config_loader import load_config, build_pipeline

    cfg   = load_config("assets/config-template.json")   # 自动解包 + 校验
    parts = build_pipeline(cfg)                          # 按配置装配组件
    chunks = parts["chunker"]("你的长文档……")
    hits   = parts["retriever"].retrieve("查询", top_k=5)

命令行自检：
    python config_loader.py [配置文件路径]
"""
import json
import logging
import os
from typing import Any, Callable, Dict, List, Optional

from config_validator import validate_config, format_errors

logger = logging.getLogger(__name__)

__all__ = [
    "ConfigError",
    "load_config",
    "strip_meta",
    "build_pipeline",
    "DEFAULT_CONFIG_PATH",
]

DEFAULT_CONFIG_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "assets", "config-template.json",
)

# 配置模板里的元信息键（描述性字段，不应透传给组件）
_META_KEYS = {"comment", "_status", "comment_"}

# chunking.strategy 取值 → 配置模板里对应的参数块名
_CHUNK_CONFIG_KEYS: Dict[str, str] = {
    "fixed": "fixed_chunking",
    "semantic": "semantic_chunking",
    "small_to_big": "small_to_big",
    "proposition": "proposition_chunking",
    "contextual_header": "contextual_header",
}


class ConfigError(Exception):
    """配置严重错误（strict 模式下抛出）"""

    def __init__(self, errors: List[Any]):
        self.errors = errors
        super().__init__(format_errors(errors))


def strip_meta(cfg: Dict[str, Any]) -> Dict[str, Any]:
    """去掉配置块里的描述性键（comment / _status），只保留真正的参数。"""
    if not isinstance(cfg, dict):
        return cfg
    return {k: v for k, v in cfg.items() if k not in _META_KEYS}


def load_config(path: str = None, strict: bool = False) -> Dict[str, Any]:
    """
    加载配置文件并做入口校验。

    Args:
        path: 配置文件路径；缺省使用 `assets/config-template.json`
        strict: True 时，severity=error 的校验失败直接抛 ConfigError；
                False 时仅告警（warning 级别无论 strict 与否都只告警）

    Returns:
        解包后的 `rag_optimization_config` 字典（已是组件可直接消费的形状）

    Raises:
        FileNotFoundError: 配置文件不存在
        ConfigError: strict 模式下存在 error 级校验失败
    """
    path = path or DEFAULT_CONFIG_PATH
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    # 兼容两种形状：带 rag_optimization_config 外壳 / 直接是配置体
    cfg = raw.get("rag_optimization_config", raw) if isinstance(raw, dict) else raw
    if not isinstance(cfg, dict):
        raise ConfigError([type("", (), {
            "__str__": lambda self: "配置根节点必须是字典"})()])

    # H10：校验层在入口真正执行（此前零调用方）
    errors = validate_config(raw)
    if errors:
        hard = [e for e in errors if getattr(e, "severity", "error") == "error"]
        if hard and strict:
            raise ConfigError(hard)
        for e in errors:
            level = getattr(e, "severity", "error")
            (logger.error if level == "error" else logger.warning)(str(e))

    return cfg


def _chunker_config(cfg: Dict[str, Any]) -> tuple:
    """解析分块策略与其参数块。返回 (strategy, chunk_config)"""
    chunking = cfg.get("chunking", {}) or {}
    strategy = chunking.get("strategy", "small_to_big")
    block_key = _CHUNK_CONFIG_KEYS.get(strategy, strategy)
    block = chunking.get(block_key, {}) or {}
    return strategy, strip_meta(block)


def build_pipeline(cfg: Dict[str, Any],
                   llm_client=None,
                   embedding_model=None,
                   retriever=None,
                   generator=None) -> Dict[str, Any]:
    """
    按配置装配 RAG 组件。

    只装配配置中 `enabled: true`（或未提供该开关）的模块，
    但**所有被装配的组件都会真正收到配置参数**——这是 H2 的核心：
    此前配置只是文档，现在它决定组件行为。

    Args:
        cfg: `load_config()` 的返回值
        llm_client: 外部注入的 LLM（任意形态，内部统一用 wrap_llm 归一）
        embedding_model: 外部注入的嵌入模型
        retriever: 外部注入的检索器（不传则按 retrieval.strategy 装配 BM25Retriever）
        generator: 外部注入的答案生成器（供 Self-RAG 使用）

    Returns:
        {组件名: 实例} 字典，至少含 "chunker" 与 "retriever"
    """
    from llm_client import wrap_llm

    llm = wrap_llm(llm_client)
    parts: Dict[str, Any] = {"config": cfg}

    # ---------------- 分块 ----------------
    from chunker_factory import get_chunker
    strategy, chunk_cfg = _chunker_config(cfg)
    parts["chunking_strategy"] = strategy
    # get_chunker 返回的 callable 已绑定配置，调用方只需传 document
    parts["chunker"] = get_chunker(strategy, chunk_cfg)

    def _chunk_document(document: str) -> List[Any]:
        return parts["chunker"](document)

    parts["chunk_document"] = _chunk_document

    # ---------------- 检索 ----------------
    retrieval = strip_meta(cfg.get("retrieval", {}) or {})
    hybrid_cfg = strip_meta(retrieval.get("hybrid_retrieval", {}) or {})
    if retriever is not None:
        parts["retriever"] = retriever
    else:
        from bm25_retriever import BM25Retriever
        retr_cfg = dict(hybrid_cfg)
        # BM25 自身的 k1/b 也允许在配置里指定
        retr_cfg.update(strip_meta(retrieval.get("bm25_retrieval", {}) or {}))

        # H18 配套环节：把 performance.cache 的开关与 TTL 真正送进检索器。
        # 此前 config-template 里写了 cache_ttl_seconds=3600，但没有任何组件读取——
        # 配置与实现之间这段路一直没接通。
        perf_cache = strip_meta(
            (strip_meta(cfg.get("performance", {}) or {}).get("cache", {}) or {})
        )
        if perf_cache:
            retr_cfg["cache_ttl_seconds"] = perf_cache.get(
                "cache_ttl_seconds", retr_cfg.get("cache_ttl_seconds", 3600))
            # 显式关闭查询缓存时，用 max_size=0 让缓存彻底不生效
            retr_cfg["cache_max_size"] = (
                retr_cfg.get("cache_max_size", 128)
                if perf_cache.get("query_cache_enabled", True) else 0
            )

        parts["retriever"] = BM25Retriever(config=retr_cfg,
                                           embedding_model=embedding_model)

    # ---------------- 查询转换 ----------------
    qo = strip_meta(cfg.get("query_optimization", {}) or {})
    if qo.get("enabled", True):
        from query_transformer import QueryTransformer
        parts["query_transformer"] = QueryTransformer(
            llm_client=llm, config={**qo, "mode": qo.get("mode", "auto")})

    # ---------------- 重排序 ----------------
    rr = strip_meta(cfg.get("reranking", {}) or {})
    if rr.get("enabled", False):
        from reranker import Reranker
        parts["reranker"] = Reranker(
            model_name=rr.get("model", "BAAI/bge-reranker-base"),
            batch_size=rr.get("batch_size", 32),
            config=rr,
        )

    # ---------------- 相关片段提取 ----------------
    se = strip_meta(cfg.get("segment_extraction", {}) or {})
    if se.get("enabled", False):
        from segment_extractor import RelevantSegmentExtractor
        parts["segment_extractor"] = RelevantSegmentExtractor(
            llm_client=llm, embedding_model=embedding_model, config=se)

    # ---------------- 上下文压缩 ----------------
    cc = strip_meta(cfg.get("context_compression", {}) or {})
    if cc.get("enabled", False):
        from context_compression import ContextCompressor
        parts["context_compressor"] = ContextCompressor(
            llm_client=llm, embedding_model=embedding_model, config=cc)

    # ---------------- 引用溯源 ----------------
    ct = strip_meta(cfg.get("citation_tracking", {}) or {})
    if ct.get("enabled", False):
        from citation_tracker import CitationTracker
        parts["citation_tracker"] = CitationTracker(llm_client=llm, config=ct)

    # ---------------- 查询意图 ----------------
    qi = strip_meta(cfg.get("query_intent", {}) or {})
    if qi.get("enabled", False):
        from query_intent import QueryIntentRecognizer
        parts["query_intent"] = QueryIntentRecognizer(llm_client=llm, config=qi)

    # ---------------- Self-RAG / CRAG ----------------
    sr = strip_meta(cfg.get("self_rag", {}) or {})
    if sr.get("enabled", False) and generator is not None:
        from self_rag import CorrectiveRAG, SelfRAG
        cls = SelfRAG if sr.get("mode") == "self" else CorrectiveRAG
        parts["self_rag"] = cls(
            retriever=parts["retriever"],
            generator=generator,
            llm_client=llm,
            config=sr,
            retrievers=[parts["retriever"]],
        )

    # ---------------- 多跳检索 ----------------
    mh = strip_meta(cfg.get("multi_hop", {}) or {})
    if mh.get("enabled", False):
        from multi_hop_retriever import MultiHopRetriever
        parts["multi_hop"] = MultiHopRetriever(
            retriever=parts["retriever"], llm_client=llm, config=mh)

    # ---------------- Graph RAG ----------------
    adv = strip_meta(cfg.get("advanced_features", {}) or {})
    gr = strip_meta(adv.get("graph_rag", {}) or {})
    if gr.get("enabled", False):
        from graph_rag import GraphRAG
        parts["graph_rag"] = GraphRAG(llm_client=llm, config=gr)

    # ---------------- 查询路由 ----------------
    routing = strip_meta(adv.get("routing", {}) or {})
    if routing.get("enabled", False):
        from query_router import QueryRouter
        parts["router"] = QueryRouter(
            intent_classifier=parts.get("query_intent"),
            retrievers={"default": parts["retriever"]},
            config=routing,
        )

    return parts


def main() -> int:
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_CONFIG_PATH
    try:
        cfg = load_config(path)
    except FileNotFoundError:
        print(f"配置文件不存在: {path}")
        return 1
    except ConfigError as e:
        print(str(e))
        return 2

    print(f"已加载配置: {path}")
    print(f"  分块策略: {cfg.get('chunking', {}).get('strategy')}")

    parts = build_pipeline(cfg)
    print("\n已装配组件:")
    for name, obj in parts.items():
        if name in ("config", "chunking_strategy"):
            continue
        print(f"  - {name}: {type(obj).__module__}.{type(obj).__name__}")

    # 冒烟：真的用配置里的参数分一次块
    strategy, chunk_cfg = _chunker_config(cfg)
    doc = "RAG 是一种检索增强生成技术。它能显著降低大语言模型的幻觉问题。" * 5
    chunks = parts["chunk_document"](doc)
    print(f"\n冒烟：{strategy} 策略（{chunk_cfg}）把 {len(doc)} 字文档切成 {len(chunks)} 块")
    return 0


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - %(levelname)s - %(message)s")
    raise SystemExit(main())
