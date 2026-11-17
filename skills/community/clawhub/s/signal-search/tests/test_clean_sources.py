"""干净源预灌（clean_sources）单测：注册表 / 扇出 / 去重 / 档位 / keyed opt-in / NBS 适配 / retrieve 接线。

设计：全程不触网。供给器底层 `_fetch_one` 与 `build_clean_fetch` 均由 monkeypatch 接管，
联网路径用 `SIGNAL_SEARCH_CLEAN_ON` 显式开闸、或用 fake 供给器替代，保证门禁不退步。
"""

import os
import sys
import types

HERE = os.path.dirname(__file__)
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import clean_sources as cs
import orchestrate

# 真理源配置：全部非 keyed 类开启，ai_search 默认关（keyed 走 opt-in）
CFG = {
    "clean_sources": {
        "enabled": True,
        "default_tier": "standard",
        "timeout": 1.0,
        "max_workers": 4,
        "overall_timeout": 5.0,
        "categories": {
            "intl_engines": {"enabled": True},
            "reference": {"enabled": True},
            "academic_api": {"enabled": True},
            "authoritative": {"enabled": True},
            "industry_keyless": {"enabled": True},
            "privacy_extra": {"enabled": True},
            "cn_official": {"enabled": True},
            "ai_search": {"enabled": False, "keys": {}},
        },
    },
    "searxng": {"url": "http://localhost:8080"},  # 仅用于解除 SearxNG gate，单元测不真连
}


def _fake_doc(src, query):
    return [{"url": f"https://{src['id']}.example/{query}", "title": src["name"], "snippet": "x"}]


def _fake_fetch_one(src, query, cfg, fetcher, timeout):
    return _fake_doc(src, query)


def _fake_expand(docs, scores, *a, **k):
    exp = types.SimpleNamespace(
        docs=docs, scores=scores, exhausted=False, budget_hit=False, prev_rounds=[], new_batch=[]
    )
    return exp, []


# ---------------------------------------------------------------------------
# 1) 注册表完整性
# ---------------------------------------------------------------------------
def test_describe_registry():
    d = cs.describe_clean_sources()
    assert d["total"] == 65
    cats = d["by_category"]
    assert len(cats) == 8
    counts = {k: len(v) for k, v in cats.items()}
    assert counts == {
        "intl_engines": 9,
        "reference": 3,
        "academic_api": 7,
        "authoritative": 8,
        "industry_keyless": 16,
        "privacy_extra": 3,
        "cn_official": 15,
        "ai_search": 4,
    }
    assert set(d["tiers_preset"]) == {"lite", "standard", "full"}


# ---------------------------------------------------------------------------
# 2) standard 档扇出层：仅 keyless、无 ai_search（关闭路由以验证扇出层本身不变量）
# ---------------------------------------------------------------------------
def test_standard_fanout_keyless_only(monkeypatch):
    monkeypatch.setattr(cs, "_fetch_one", _fake_fetch_one)
    # 关路由 → 全扇出旧行为，验证「keyed 排除 + 所有 keyless 活跃源参与」这一层不变量
    cfg_off = dict(CFG)
    cfg_off["clean_sources"] = dict(CFG["clean_sources"])
    cfg_off["clean_sources"]["routing"] = {"enabled": False}
    provider = cs.build_clean_fetch(cfg=cfg_off, tiers="standard")
    docs = provider("quantum")
    assert len(docs) == 61  # 65 - 4 keyed
    engines = {d["engine"] for d in docs}
    assert "Tavily" not in engines and "Exa" not in engines
    assert "Perplexity" not in engines and "BraveAPI" not in engines
    for d in docs:
        assert d["clean_source"] is True
        assert d["landing_resolved"] is False
        assert d["source_type"] in ("academic", "gov", "vendor", "unknown")
        assert d["quality"] in ("A", "B")


# ---------------------------------------------------------------------------
# 3) lite 档过滤：仅国际引擎 + 通用参考
# ---------------------------------------------------------------------------
def test_lite_tier_filter(monkeypatch):
    monkeypatch.setattr(cs, "_fetch_one", _fake_fetch_one)
    provider = cs.build_clean_fetch(cfg=CFG, tiers="lite")
    docs = provider("test")
    assert len(docs) == 12  # intl_engines(9)+reference(3)
    assert {d["category"] for d in docs} == {"intl_engines", "reference"}


# ---------------------------------------------------------------------------
# 4) 跨源 URL 去重
# ---------------------------------------------------------------------------
def test_dedup_by_url(monkeypatch):
    def fake(src, query, cfg, fetcher, timeout):
        return [{"url": "https://shared.example/x", "title": src["name"], "snippet": "x"}]

    monkeypatch.setattr(cs, "_fetch_one", fake)
    provider = cs.build_clean_fetch(cfg=CFG, tiers="standard")
    docs = provider("q")
    # 61 个源都回同一 URL → 去重后仅 1 条
    assert len(docs) == 1
    assert docs[0]["url"] == "https://shared.example/x"


# ---------------------------------------------------------------------------
# 5) keyed AI 搜索 API：默认关，env 注入即活（绕过 category.enabled 与 tier 分组）
# ---------------------------------------------------------------------------
def test_keyed_optin_via_env(monkeypatch):
    monkeypatch.setattr(cs, "_fetch_one", _fake_fetch_one)
    # 默认（无 key）：ai_search 不出现
    provider = cs.build_clean_fetch(cfg=CFG, tiers="standard")
    assert not any(
        d["engine"] in {"Tavily", "Exa", "Perplexity", "BraveAPI"} for d in provider("q")
    )
    # 注入 env key：Tavily 激活（即使 ai_search.enabled=false、tiers 不含 ai_search）
    monkeypatch.setenv("TAVILY_API_KEY", "x")
    provider2 = cs.build_clean_fetch(cfg=CFG, tiers="standard")
    engines = {d["engine"] for d in provider2("q")}
    assert "Tavily" in engines
    assert any(d["access"] == "keyed" for d in provider2("q"))


# ---------------------------------------------------------------------------
# 6) rest_adapter：国家统计局 NBS 通路 + 空内容不产空占位 doc
# ---------------------------------------------------------------------------
def test_rest_adapter_nbs():
    nbs = next(s for s in cs.CLEAN_SOURCES if s["id"] == "NBS")
    assert nbs["method"] == "rest_adapter"

    def fetcher_ok(url, timeout=4.0):
        return ("指标:A0101 名称:国内生产总值 值:1200000", "text/plain")

    out = cs._adapt_nbs(nbs, "GDP", CFG, fetcher_ok)
    assert len(out) == 1
    assert "stats.gov.cn" in out[0]["url"]

    def fetcher_empty(url, timeout=4.0):
        return ("", "text/plain")

    assert cs._adapt_nbs(nbs, "GDP", CFG, fetcher_empty) == []  # 无内容即跳过


# ---------------------------------------------------------------------------
# 7) retrieve 接线：干净源并入质量层（hermetic，fake 供给器）
# ---------------------------------------------------------------------------
def test_retrieve_merges_clean_sources(monkeypatch):
    monkeypatch.setenv("SIGNAL_SEARCH_CLEAN_ON", "1")
    monkeypatch.setattr(orchestrate, "_gather_internal_docs", lambda *a, **k: ([], []))
    monkeypatch.setattr(orchestrate, "_expand_if_needed", _fake_expand)

    def fake_provider(query):
        return [
            {
                "url": "https://openalex.org/fake",
                "title": "Fake",
                "snippet": "x",
                "source_type": "academic",
                "quality": "A",
                "engine": "OpenAlex",
                "category": "academic_api",
                "access": "keyless",
                "clean_source": True,
                "landing_resolved": False,
            }
        ]

    monkeypatch.setattr(cs, "build_clean_fetch", lambda *a, **k: fake_provider)

    r = orchestrate.retrieve("test query", {}, 2000, cfg=CFG, web_fetch=None)
    engines = {d.get("engine") for d in r["sources"]}
    assert "OpenAlex" in engines
    # trace 应记录 clean_sources 事件
    kinds = {ev["name"] for ev in r["trace"]["events"]}
    assert "clean_sources" in kinds


# ---------------------------------------------------------------------------
# 8) 门禁：默认 pytest 环境下不触发联网（除非显式 SIGNAL_SEARCH_CLEAN_ON）
# ---------------------------------------------------------------------------
def test_clean_sources_gate_off_under_pytest(monkeypatch):
    monkeypatch.setattr(orchestrate, "_gather_internal_docs", lambda *a, **k: ([], []))
    monkeypatch.setattr(orchestrate, "_expand_if_needed", _fake_expand)
    called = {"n": 0}

    def fake_bcf(*a, **k):
        called["n"] += 1
        return lambda q: []

    monkeypatch.setattr(cs, "build_clean_fetch", fake_bcf)

    orchestrate.retrieve("q", {}, 1000, cfg=CFG, web_fetch=None)
    assert called["n"] == 0  # 默认 pytest 下不调用 build_clean_fetch → 不联网


# ---------------------------------------------------------------------------
# 9) 源路由层（按需选源，避免全扇出）
# ---------------------------------------------------------------------------
CFG_R = {
    "clean_sources": {
        "enabled": True,
        "default_tier": "standard",
        "timeout": 1.0,
        "max_workers": 4,
        "overall_timeout": 5.0,
        "routing": {
            "enabled": True,
            "mode": "select",
            "max_sources": 16,
            "include_general_floor": True,
            "fallback_to_tier": False,
        },
        "categories": {
            "intl_engines": {"enabled": True},
            "reference": {"enabled": True},
            "academic_api": {"enabled": True},
            "authoritative": {"enabled": True},
            "industry_keyless": {"enabled": True},
            "privacy_extra": {"enabled": True},
            "cn_official": {"enabled": True},
            "ai_search": {"enabled": False, "keys": {}},
        },
    },
    "searxng": {"url": "http://localhost:8080"},
}

CORE_CATS = {"intl_engines", "reference"}


def _active(srcs_cfg=None):
    cfg = srcs_cfg or CFG_R
    return [
        s
        for s in cs.CLEAN_SOURCES
        if any(cs._source_active(s, t, cfg, None) for t in ("lite", "standard", "full"))
    ]


def test_route_selects_topic_subset():
    active = _active()
    sel = cs.select_sources("深度学习最新论文综述 arxiv", active, CFG_R)
    ids = {s["id"] for s in sel}
    # 学术主题 → 命中学术 API；不命中无关源（如健康/法律）
    assert {"OpenAlex", "Crossref", "SemanticScholar", "PubMed", "arXiv"} & ids
    assert not ({"WHO", "CDC", "CourtListener", "FlkNPC"} & ids)
    # 通用保底恒在
    assert {s["id"] for s in sel if s["category"] in CORE_CATS}


def test_route_general_query_hits_only_floor():
    active = _active()
    sel = cs.select_sources("性价比高的咖啡机推荐 家用", active, CFG_R)
    # 未识别主题 → 仅返回保底集（通用引擎 + 参考），不误伤专业源
    assert all(s["category"] in CORE_CATS for s in sel)
    assert len(sel) <= 12  # 仅保底，无专家源


def test_route_max_sources_cap():
    active = _active()
    # 多主题查询：学术+法律+医疗+宏观同时命中，专家源会很多
    q = "论文 法律 判例 医疗 疫苗 经济 GDP 通胀 气候"
    sel = cs.select_sources(q, active, CFG_R)
    assert len(sel) <= CFG_R["clean_sources"]["routing"]["max_sources"]
    # 通用保底仍在
    assert any(s["category"] in CORE_CATS for s in sel)


def test_route_off_mode_returns_all():
    cfg = dict(CFG_R)
    cfg["clean_sources"] = dict(cfg["clean_sources"])
    cfg["clean_sources"]["routing"] = {"enabled": False}
    active = _active(cfg)
    sel = cs.select_sources("某公司最新财报", active, cfg)
    assert len(sel) == len(active)  # 全扇出旧行为


def test_route_fallback_to_tier_fills_others():
    cfg = dict(CFG_R)
    cfg["clean_sources"] = dict(cfg["clean_sources"])
    cfg["clean_sources"]["routing"] = {
        "enabled": True,
        "mode": "select",
        "max_sources": 16,
        "fallback_to_tier": True,
    }
    active = _active(cfg)
    # 未识别主题 + 开启回退 → 应补满其余源（受 cap）
    sel = cs.select_sources("随便聊聊今天天气不错", active, cfg)
    assert len(sel) > 12  # 超出纯保底，补了专家源
    assert len(sel) <= 16


def test_route_never_empty_via_floor():
    active = _active()
    sel = cs.select_sources("", active, CFG_R)  # 空查询
    assert len(sel) >= 1  # 保底恒非空


def test_router_fn_injection_overrides_heuristic():
    # 调用方注入 LLM 路由器：provider 仅打 router_fn 返回的源
    picked = [cs.CLEAN_SOURCES[0], cs.CLEAN_SOURCES[1], cs.CLEAN_SOURCES[2]]
    called = []

    def fake_fetch_one(src, query, cfg, fetcher, timeout):
        called.append(src["id"])
        return _fake_doc(src, query)

    provider = cs.build_clean_fetch(cfg=CFG_R, router_fn=lambda q, srcs: picked)
    import unittest.mock as _mock

    with _mock.patch.object(cs, "_fetch_one", fake_fetch_one):
        docs = provider("任意查询")
    assert {d["engine"] for d in docs} == {s["id"] for s in picked}
    assert set(called) == {s["id"] for s in picked}


def test_describe_includes_routing():
    d = cs.describe_clean_sources()
    assert "routing_topics" in d and len(d["routing_topics"]) >= 8
    assert d["routing_source_overrides"] >= 30  # industry_keyless(16)+cn_official(15)


# ---------------------------------------------------------------------------
# 11) 自定义（私有 / 内部）源：配置驱动接入，零代码改写（差异化卖点）
# ---------------------------------------------------------------------------
def test_custom_source_plugs_in_real_extraction():
    """私有源经 url_template + json_items + item_map 接入，走真实 rest 抽取链路，
    并与 65 公开源平等进质量层（source_type/quality/clean_source 等元数据齐全）。"""
    import json as _json

    cfg = dict(CFG)
    cfg["clean_sources"] = dict(cfg["clean_sources"])
    cfg["clean_sources"]["custom_sources"] = [
        {
            "id": "mykb",
            "name": "公司内部知识库",
            "url_template": "https://kb.internal/api/search?q={q}",
            "json_items": "results",
            "item_map": {"url": "link", "title": "t", "snippet": "s"},
            "quality": "A",
            "source_type": "internal",
        }
    ]

    def fake_fetcher(url, timeout=4.0):
        assert "q=" in url  # {q} 已编码注入（url 构造链路生效）
        body = _json.dumps(
            {
                "results": [
                    {"link": "https://kb.internal/doc1", "t": "Doc One", "s": "snippet one"},
                    {"link": "https://kb.internal/doc2", "t": "Doc Two", "s": "snippet two"},
                ]
            }
        ).encode("utf-8")
        return (body, "application/json")

    provider = cs.build_clean_fetch(cfg=cfg, tiers="standard", fetcher=fake_fetcher)
    docs = provider("产品上线 checklist")
    ids = {d["engine"] for d in docs}
    assert "mykb" in ids  # 私有源默认必打（force_include）
    kb = [d for d in docs if d["engine"] == "mykb"]
    assert len(kb) == 2
    assert kb[0]["url"] == "https://kb.internal/doc1"
    assert kb[0]["title"] == "Doc One"
    assert kb[0]["snippet"] == "snippet one"
    assert kb[0]["source_type"] == "internal"
    assert kb[0]["quality"] == "A"
    assert kb[0]["clean_source"] is True


def test_custom_source_keyed_optin(monkeypatch):
    """自定义源带 key_env → 自动变 keyed opt-in：无 key 不激活，env 注入即活。"""
    cfg = dict(CFG)
    cfg["clean_sources"] = dict(cfg["clean_sources"])
    cfg["clean_sources"]["custom_sources"] = [
        {
            "id": "securekb",
            "name": "加密内网库",
            "url_template": "https://secure.internal/search?q={q}&token={token}",
            "key_env": "SECURE_KB_KEY",
        }
    ]
    monkeypatch.setattr(cs, "_fetch_one", _fake_fetch_one)
    # 无 key：securekb 不出现
    provider = cs.build_clean_fetch(cfg=cfg, tiers="standard")
    assert "securekb" not in {d["engine"] for d in provider("q")}
    # 注入 env：securekb 激活（{token} 从该 env 取值）
    monkeypatch.setenv("SECURE_KB_KEY", "secret")
    provider2 = cs.build_clean_fetch(cfg=cfg, tiers="standard")
    assert "securekb" in {d["engine"] for d in provider2("q")}


# ---------------------------------------------------------------------------
# 12) 缓存纪律：内容键 / 有界 / 并发安全（上线 QA，根除内存泄漏）
# ---------------------------------------------------------------------------
def test_load_config_caches_same_object():
    """load_config() 无参返回进程级单例（同对象）；传入 cfg 原样返回。"""
    import common

    a = common.load_config()
    b = common.load_config()
    assert a is b
    own = {"clean_sources": {"default_tier": "standard", "categories": {}}}
    assert common.load_config(own) is own


def test_active_srcs_cache_bounded_under_distinct_cfg_objects():
    """长驻服务场景：每次传入「内容相同但身份不同」的 cfg 对象（修复前的泄漏根因：
    id(cfg) 每调用唯一 → 缓存只增不减）。修复后内容指纹键 → 缓存条目恒定、绝不超上限。"""
    for _ in range(300):
        cfg = {"clean_sources": {"default_tier": "standard", "categories": {}}}
        cs.build_clean_fetch(cfg=cfg)
    assert len(cs._ACTIVE_SRCS_CACHE) <= cs._ACTIVE_SRCS_MAX


def test_concurrent_build_threadsafe():
    """并发 build_clean_fetch 不崩、结果一致（缓存读-改-写已加锁）。"""
    import threading

    errs = []

    def worker():
        try:
            cs.build_clean_fetch(
                cfg={"clean_sources": {"default_tier": "standard", "categories": {}}}
            )
        except Exception as e:  # pragma: no cover - 仅用于断言收集
            errs.append(repr(e))

    threads = [threading.Thread(target=worker) for _ in range(16)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert not errs, errs


def test_custom_source_missing_q_warns():
    """私有源 rest 且 url_template 缺 {q} 且未声明 static → _normalize_custom 收集到边界告警
    （不抛、不误伤正常 static 源）。"""
    cfg = dict(CFG)
    cfg["clean_sources"] = dict(cfg["clean_sources"])
    cfg["clean_sources"]["custom_sources"] = [
        {
            "id": "staticfeed",
            "name": "静态订阅源",
            "url_template": "https://feed.internal/latest",  # 缺 {q} 且非 static
            "response": "json",
            "json_items": "items",
        }
    ]
    warn: list = []
    list(cs._custom_sources(cfg, warn))
    assert any("缺 {q}" in w for w in warn)
    # 声明 static 的正常源不应告警
    cfg["clean_sources"]["custom_sources"][0]["static"] = True
    warn2: list = []
    list(cs._custom_sources(cfg, warn2))
    assert not any("缺 {q}" in w for w in warn2)
