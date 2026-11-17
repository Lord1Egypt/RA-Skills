import json
import os
import sys

HERE = os.path.dirname(__file__)
ROOT = os.path.join(HERE, "..")
CONFIG_PATH = os.path.join(ROOT, "config.json")
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import connector
import extract
import parallel


# ---- 默认关硬门槛（M55 例外）：config.json 开关断言 ----
def test_default_off_hard_gate():
    with open(CONFIG_PATH, encoding="utf-8") as f:
        cfg = json.load(f)
    off_keys = [
        "rerank",
        "searxng",
        "dynamic_profiling",
        "conflict_typing",
        "entity_resolution",
        "observability.trace",
    ]
    for k in off_keys:
        if k == "observability.trace":
            assert cfg["observability"]["trace"] is False, "observability.trace 必须为 false"
        else:
            assert cfg[k]["enabled"] is False, f"{k}.enabled 必须为 false（默认关硬门槛）"
    # P2-10：cache 经计划明确改为默认开（TTL+内容哈希），从默认关硬门槛中移除；
    # 其余增强项仍保持默认关，避免开箱即产生意外行为/副作用。
    assert cfg["cache"]["enabled"] is True, "cache.enabled 必须为 true（P2-10 默认开）"
    # M55 例外：compliance 默认开
    assert cfg["compliance"]["enabled"] is True


# ---- retrieve() 契约（monkeypatch 绕过联网/限速） ----
def _fake_doc(url, snippet, source_type="media"):
    return {
        "url": url,
        "raw_html": f"<html><body>{snippet}</body></html>",
        "title": "t",
        "fetched_at": "",
        "engine": "Baidu",
        "source_type": source_type,
        "snippet": snippet,
        "text": snippet,
    }


def _fake_load(query, freshness="中", constraints=None, cfg=None, web_fetch=None, **kwargs):
    return [
        _fake_doc("https://gov.cn/a", "政策发布 5000 元", "gov"),
        _fake_doc("https://news.com/b", "媒体报道 400 万辆", "media"),
    ]


def _fake_l3(query, constraints=None, cfg=None, **kwargs):
    return [
        _fake_doc("https://a.com/1", "开源实现 GPT Researcher", "vendor"),
        _fake_doc("https://a.com/2", "方法 Self-RAG CRAG", "academic"),
        _fake_doc("https://a.com/3", "趋势 检索推理协同", "media"),
    ]


def _fast_cfg():
    with open(CONFIG_PATH, encoding="utf-8") as f:
        cfg = json.load(f)
    cfg["compliance"]["rate_limit_per_sec"] = 100.0  # 加速测试，不触发 14s 限速
    return cfg


def test_retrieval_contract_all_tiers(monkeypatch):
    monkeypatch.setattr(connector, "load", _fake_load)
    monkeypatch.setattr(extract, "extract", lambda d, cfg=None: d)
    monkeypatch.setattr(parallel, "run_l3", _fake_l3)
    cfg = _fast_cfg()

    cases = [
        ("2026-08-07 是星期几", "L0"),
        ("中国现行个人所得税起征点", "L1"),
        ("对比 Redis 与 Memcached 作为缓存", "L2"),
        ("调研 agentic search 前沿方案与开源实现", "L3"),
    ]
    for q, exp_tier in cases:
        res = __import__("orchestrate").retrieve(q, {}, cfg=cfg)
        assert set(
            [
                "findings",
                "sources",
                "scores",
                "confidence",
                "token_used",
                "exhausted",
                "tier_used",
                "trace",
            ]
        ) <= set(res.keys())
        assert res["tier_used"] == exp_tier
        assert isinstance(res["findings"], str) and res["findings"]
        assert len(res["sources"]) >= 1
        assert isinstance(res["confidence"], float)
        assert isinstance(res["token_used"], int) and res["token_used"] >= 0
        # 验证护栏：findings 中引用 url 必 ∈ sources
        assert res["verify_issues"] == [] or all(
            i["url"] in {s["url"] for s in res["sources"]} for i in res["verify_issues"]
        )
