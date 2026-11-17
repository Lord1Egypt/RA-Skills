import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SYSCR = os.path.join(HERE, "..", "scripts")
if SYSCR not in sys.path:
    sys.path.insert(0, SYSCR)

import orchestrate
import research as research_mod
import verify as verify_mod


def _cfg():
    return {
        "compliance": {"rate_limit_per_sec": 100.0},
        "dedup": {"default_threshold": 3, "external_threshold": 1},
        "verify": {"semantic": False},
        "research": {
            "default_tier": "auto",
            "clarify_l2l3": True,
            "max_iterations": 3,
            "time_range": "近3年",
        },
    }


def _doc(url, text, snippet=None, source_type="media"):
    return {
        "url": url,
        "engine": "external",
        "source_type": source_type,
        "text": text,
        "snippet": snippet or text,
        "landing_resolved": True,
    }


# ---------- A: 维度化输出 schema ----------
def test_retrieve_schema_dimension_segmentation():
    cfg = _cfg()
    docs = [_doc("https://e.com/def", "定义：TCP 是传输层协议，提供可靠传输。", "TCP 是传输层协议")]
    schema = [
        {"name": "定义与概念", "detail_level": "简要"},
        {"name": "机制/原理", "detail_level": "详细"},
    ]
    res = orchestrate.retrieve("TCP 是什么", cfg=cfg, docs=docs, schema=schema)
    assert "## 定义与概念（简要）" in res["findings"]
    assert "## 机制/原理（详细）" in res["findings"]


def test_retrieve_no_schema_backward_compat():
    cfg = _cfg()
    docs = [_doc("https://e.com/1", "TCP 面向连接，UDP 无连接。", "TCP 面向连接")]
    res = orchestrate.retrieve("TCP 是什么", cfg=cfg, docs=docs)
    assert res["findings"].startswith("先答：")


def test_retrieve_schema_external_docs_no_empty_shell():
    # 外部/web_fetch 英文 docs + 中文 schema → 不应出现空壳"该维度暂无直接来源"
    cfg = _cfg()
    docs = [
        _doc(
            "https://e.com/udp",
            "UDP is a connectionless transport protocol used for DNS and streaming.",
        )
    ]
    schema = [
        {"name": "定义与概念", "detail_level": "简要"},
        {"name": "机制/原理", "detail_level": "详细"},
    ]
    res = orchestrate.retrieve("TCP 和 UDP 的区别", cfg=cfg, docs=docs, schema=schema)
    assert "该维度暂无直接来源" not in res["findings"]
    assert "## 定义与概念（简要）" in res["findings"]


def test_uncertainties_excludes_synthesize_metadata():
    # synthesize 生成的维度标题/占位行不应进 uncertainties
    findings = (
        "## 定义与概念（简要）\n（该维度暂无直接来源）\n" "来源：\n- https://e.com/1\n\n置信度：0.5"
    )
    src = [{"url": "https://e.com/1", "snippet": "x", "text": "x"}]
    verdicts = verify_mod.fact_level_verify(findings, src)
    unc = verify_mod.aggregate_uncertainties(verdicts, docs=src)
    assert all("该维度暂无直接来源" not in u["fact"] for u in unc)
    assert all(not u["fact"].startswith("## ") for u in unc)


# ---------- B: uncertain 顶层槽 ----------
def test_aggregate_uncertainties_no_overlap():
    verdicts = [
        {
            "fact": "某未知事实XYZ",
            "verdict": "UNCERTAIN",
            "source": None,
            "reason": "no_overlap_source",
        },
        {
            "fact": "TCP 面向连接",
            "verdict": "TRUE",
            "source": "https://e.com/1",
            "reason": "source_overlap",
        },
    ]
    out = verify_mod.aggregate_uncertainties(verdicts, docs=None)
    assert len(out) == 1
    assert out[0]["fact"] == "某未知事实XYZ"
    assert out[0]["reason"] == "no_overlap_source"


def test_aggregate_uncertainties_cross_conflict():
    verdicts = [
        {
            "fact": "TCP 可靠",
            "verdict": "TRUE",
            "source": "https://a.com",
            "reason": "source_overlap",
        },
        {
            "fact": "TCP 可靠",
            "verdict": "TRUE",
            "source": "https://b.com",
            "reason": "source_overlap",
        },
    ]
    docs = [
        {"url": "https://a.com", "snippet": "TCP 是可靠的传输协议"},
        {"url": "https://b.com", "snippet": "TCP 并非可靠，会丢包"},
    ]
    out = verify_mod.aggregate_uncertainties(verdicts, docs=docs)
    assert any(u["reason"] == "cross_source_conflict" for u in out)


def test_retrieve_returns_uncertainties_key():
    cfg = _cfg()
    docs = [_doc("https://e.com/1", "TCP 面向连接", "TCP 面向连接")]
    res = orchestrate.retrieve("TCP 是什么", cfg=cfg, docs=docs)
    assert "uncertainties" in res
    assert isinstance(res["uncertainties"], list)


# ---------- C: 跨轮证据累积 ----------
def test_retrieve_prior_evidence_carried():
    cfg = _cfg()
    docs = [_doc("https://e.com/fresh", "TCP 面向连接的新研究", "TCP 面向连接")]
    prior = [_doc("https://e.com/old", "UDP 是无连接协议", "UDP 无连接")]
    res = orchestrate.retrieve("TCP 是什么", cfg=cfg, docs=docs, prior_evidence=[prior[0]])
    carried = [s for s in res["sources"] if s.get("carried")]
    assert len(carried) == 1
    assert carried[0]["url"] == "https://e.com/old"


# ---------- research() 编排层 ----------
def _fake_retriever(query, cfg=None, schema=None, prior_evidence=None, docs=None, **kw):
    _fake_retriever.calls.append(
        {"query": query, "schema": schema, "prior_evidence": prior_evidence}
    )
    # url 随 query 变化：不同维度=不同来源，同一 query 重复调用=同一来源（供 url 去重断言）
    slug = str(abs(hash(query)) % 100000)
    return {
        "findings": f"关于{query}的研究发现",
        "uncertainties": (
            [{"fact": "未知X", "reason": "no_overlap_source"}] if "未知" in query else []
        ),
        "sources": [
            {"url": f"https://e.com/{slug}", "snippet": "TCP 面向连接", "text": "TCP 面向连接"}
        ],
    }


_fake_retriever.calls = []


def test_research_L0_flat_no_schema():
    _fake_retriever.calls = []
    out = research_mod.research(
        "TCP 是什么", vault_dir=None, cfg=_cfg(), tier="L0", retriever=_fake_retriever
    )
    assert out["tier"] == "L0"
    assert out["schema"] == []
    assert len(_fake_retriever.calls) == 1
    assert _fake_retriever.calls[0]["schema"] == []


def test_research_L2_schema_and_dispatch():
    _fake_retriever.calls = []
    out = research_mod.research(
        "TCP 和 UDP 的区别及原理", vault_dir=None, cfg=_cfg(), tier="L2", retriever=_fake_retriever
    )
    assert out["tier"] == "L2"
    assert len(out["schema"]) == 5
    assert len(_fake_retriever.calls) == 1
    assert _fake_retriever.calls[0]["schema"] == out["schema"]


def test_research_L3_loop_iterations():
    _fake_retriever.calls = []
    out = research_mod.research(
        "研究 TCP 拥塞控制的演进",
        vault_dir=None,
        cfg=_cfg(),
        tier="L3",
        max_iter=3,
        retriever=_fake_retriever,
    )
    assert out["tier"] == "L3"
    assert out["iterations"] == 3
    assert len(_fake_retriever.calls) == 3


def test_research_prior_evidence_passed():
    _fake_retriever.calls = []
    prior = [{"url": "https://e.com/base", "text": "基础事实", "snippet": "基础事实"}]
    research_mod.research(
        "TCP 原理", cfg=_cfg(), tier="L2", prior_evidence=prior, retriever=_fake_retriever
    )
    assert _fake_retriever.calls[0]["prior_evidence"] is not None
    assert len(_fake_retriever.calls[0]["prior_evidence"]) == 1


def test_research_agent_dispatch_merges_evidence():
    _fake_retriever.calls = []

    def agent(prompt, dim=None, fetch_fn=None):
        return {
            "url": f"https://agent/{dim['name']}",
            "text": f"{dim['name']}结论",
            "snippet": f"{dim['name']}结论",
        }

    research_mod.research(
        "TCP 和 UDP 的区别及原理", cfg=_cfg(), tier="L2", agent_fn=agent, retriever=_fake_retriever
    )
    pe = _fake_retriever.calls[0]["prior_evidence"]
    assert pe is not None
    assert len(pe) == 5  # 5 维度各产 1 条证据, 并入 prior_evidence


def test_research_uncertainties_propagated():
    _fake_retriever.calls = []
    out = research_mod.research(
        "某未知主题的研究", vault_dir=None, cfg=_cfg(), tier="L2", retriever=_fake_retriever
    )
    assert out["uncertainties"]


# ---------- 默认激活(agent_dispatch=true / model_tier=true) ----------
def test_research_internal_dispatch_when_agent_dispatch_true():
    _fake_retriever.calls = []
    cfg = _cfg()
    cfg["research"]["agent_dispatch"] = True
    out = research_mod.research(
        "TCP 和 UDP 的区别及原理", vault_dir=None, cfg=cfg, tier="L2", retriever=_fake_retriever
    )
    assert out["tier"] == "L2"
    # 库内按维度派发: 5 维各 1 次 + 最终合成 1 次 = 6 次
    assert len(_fake_retriever.calls) == 6
    last = _fake_retriever.calls[-1]
    assert last["prior_evidence"] is not None
    assert len(last["prior_evidence"]) == 5  # 5 维证据已并入


def test_research_model_tier_fallback_without_fn():
    _fake_retriever.calls = []
    cfg = _cfg()
    cfg["research"]["model_tier"] = True  # 无 tier_classify_fn 注入
    out = research_mod.research(
        "对比 TCP 和 UDP 的拥塞控制",
        vault_dir=None,
        cfg=cfg,
        tier="auto",
        retriever=_fake_retriever,
    )
    assert out["tier"] == "L2"  # 回退启发式(含"对比"→L2), 不崩


def test_research_model_tier_injects_fn():
    _fake_retriever.calls = []
    cfg = _cfg()
    cfg["research"]["model_tier"] = True
    cfg["research"]["tier_classify_fn"] = lambda q, tmpl: "L3"
    out = research_mod.research(
        "某问题", vault_dir=None, cfg=cfg, tier="auto", retriever=_fake_retriever
    )
    assert out["tier"] == "L3"
