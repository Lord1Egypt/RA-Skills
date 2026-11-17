"""tests/test_orchestrate.py - 路径B 验收：retrieve() 外部 docs 注入 + connector 默认收敛。

覆盖：
- 外部 docs 喂入时跳过 connector.load（直进质量层）
- 返回结构含 findings / sources / fact_verdicts
- connector._select 默认仅 [Baidu, Sogou]；SearXNG 启用时折叠为 __searxng__
"""

import json
import os
import sys

HERE = os.path.dirname(__file__)
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import connector
import dedup
import deepfetch
import extract
import orchestrate
import verify

CONFIG_PATH = os.path.join(ROOT, "config.json")


def _fast_cfg():
    with open(CONFIG_PATH, encoding="utf-8") as f:
        cfg = json.load(f)
    cfg["compliance"]["rate_limit_per_sec"] = 100.0  # 加速，不触发 14s 限速
    return cfg


def _ext_doc(url, text, source_type="media"):
    return {
        "url": url,
        "raw_html": f"<html><body>{text}</body></html>",
        "title": "t",
        "engine": "external",
        "source_type": source_type,
        "snippet": text[:40],
        "text": text,
        "landing_resolved": True,
    }


def test_retrieval_external_docs_skips_connector(monkeypatch):
    # 外部 docs 路径不应调用 connector.load（多引擎抓取已交 agent/web_fetch）
    calls = {"n": 0}

    def _boom(*a, **k):
        calls["n"] += 1
        raise AssertionError("外部 docs 路径误调了 connector.load")

    monkeypatch.setattr(connector, "load", _boom)
    cfg = _fast_cfg()
    docs = [
        _ext_doc("https://gov.cn/a", "政策 5000 元", "gov"),
        _ext_doc("https://news.com/b", "媒体报道 400 万辆", "media"),
    ]
    res = orchestrate.retrieve("中国现行个税起征点", {}, cfg=cfg, docs=docs)
    assert calls["n"] == 0, "外部 docs 路径误调了 connector.load"
    assert len(res["sources"]) == 2
    assert {s["url"] for s in res["sources"]} == {"https://gov.cn/a", "https://news.com/b"}
    assert isinstance(res["findings"], str) and res["findings"]
    assert "fact_verdicts" in res and isinstance(res["fact_verdicts"], list)


def test_connector_default_select_baidu_sogou():
    cfg = _fast_cfg()
    assert connector._select("任意查询", {}, cfg) == ["Baidu", "Sogou"]


def test_connector_select_searxng_folds(monkeypatch):
    cfg = _fast_cfg()
    cfg["searxng"] = {"enabled": True, "url": "http://localhost:8080"}
    assert connector._select("任意查询", {}, cfg) == ["__searxng__"]


def test_external_uses_semantic_verify(monkeypatch):
    """外部(web_fetch 短摘要)输入应自动路由到 M51 语义核验（A/B 证据驱动）。"""
    calls = {"sem": 0, "kw": 0}

    def _sem(*a, **k):
        calls["sem"] += 1
        return [{"fact": "x", "verdict": "UNCERTAIN", "source": None}]

    def _kw(*a, **k):
        calls["kw"] += 1
        return [{"fact": "x", "verdict": "UNCERTAIN", "source": None}]

    monkeypatch.setattr(verify, "semantic_fact_verify", _sem)
    monkeypatch.setattr(verify, "fact_level_verify", _kw)
    cfg = _fast_cfg()
    docs = [_ext_doc("https://gov.cn/a", "政策 5000 元", "gov")]
    orchestrate.retrieve("个税起征点", {}, cfg=cfg, docs=docs)
    assert calls["sem"] == 1 and calls["kw"] == 0


def test_internal_default_keyword_verify(monkeypatch):
    """内部路径默认走关键词基线（除非 config.verify.semantic 显式开启）。"""
    calls = {"sem": 0, "kw": 0}

    def _sem(*a, **k):
        calls["sem"] += 1
        return [{"fact": "x", "verdict": "UNCERTAIN", "source": None}]

    def _kw(*a, **k):
        calls["kw"] += 1
        return [{"fact": "x", "verdict": "UNCERTAIN", "source": None}]

    monkeypatch.setattr(verify, "semantic_fact_verify", _sem)
    monkeypatch.setattr(verify, "fact_level_verify", _kw)
    monkeypatch.setattr(
        connector, "load", lambda *a, **k: [_ext_doc("https://x.com/a", "内容", "media")]
    )
    monkeypatch.setattr(deepfetch, "resolve", lambda d, cf: d)
    monkeypatch.setattr(extract, "extract", lambda d, cf: None)
    cfg = _fast_cfg()
    cfg["verify"]["semantic"] = False
    orchestrate.retrieve("个税起征点", {}, cfg=cfg)
    assert calls["kw"] == 1 and calls["sem"] == 0


def test_external_dedup_loosened(monkeypatch):
    """外部输入去重阈值应严于内部（保留跨引擎候选源供 M51 锚定）。"""
    seen = {}

    def _spy(docs, threshold=3):
        seen["threshold"] = threshold
        return docs

    monkeypatch.setattr(dedup, "near_dup", _spy)
    cfg = _fast_cfg()
    docs = [
        _ext_doc("https://gov.cn/a", "政策 5000 元", "gov"),
        _ext_doc("https://news.com/b", "媒体报道 400 万辆", "media"),
    ]
    orchestrate.retrieve("个税起征点", {}, cfg=cfg, docs=docs)
    assert seen.get("threshold") == 1  # 外部用 external_threshold=1


def test_internal_dedup_default_threshold(monkeypatch):
    """内部路径去重阈值应为默认 3。"""
    seen = {}

    def _spy(docs, threshold=3):
        seen["threshold"] = threshold
        return docs

    monkeypatch.setattr(dedup, "near_dup", _spy)
    monkeypatch.setattr(
        connector, "load", lambda *a, **k: [_ext_doc("https://x.com/a", "内容", "media")]
    )
    monkeypatch.setattr(deepfetch, "resolve", lambda d, cf: d)
    monkeypatch.setattr(extract, "extract", lambda d, cf: None)
    cfg = _fast_cfg()
    orchestrate.retrieve("个税起征点", {}, cfg=cfg)
    assert seen.get("threshold") == 3
