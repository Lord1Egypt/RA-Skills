"""P3 升级测试：D4 显式深度档位、D5 引用导出、D2 逻辑闭环停。"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SYSCR = os.path.join(HERE, "..", "scripts")
if SYSCR not in sys.path:
    sys.path.insert(0, SYSCR)

import research as research_mod
import vault as vault_mod


def _cfg():
    return {
        "compliance": {"rate_limit_per_sec": 100.0},
        "dedup": {"default_threshold": 3, "external_threshold": 1},
        "verify": {"semantic": False},
        "research": {
            "default_tier": "auto",
            "clarify_l2l3": False,
            "max_iterations": 3,
            "time_range": "近3年",
            "agent_dispatch": False,
            "model_tier": False,
            "closure_check": True,
        },
    }


def _fake_retriever(query, cfg=None, schema=None, prior_evidence=None, web_fetch=None, **kw):
    """普通假检索：单条锚定来源，文本不含维度关键词（不触发闭环停）。"""
    return {
        "findings": f"关于{query}的研究发现",
        "uncertainties": [],
        "sources": [
            {
                "url": f"https://e.com/{abs(hash(query)) % 100000}",
                "text": "TCP 面向连接",
                "snippet": "TCP 面向连接",
                "source_type": "web",
            }
        ],
    }


def _fake_retriever_full(query, cfg=None, schema=None, prior_evidence=None, web_fetch=None, **kw):
    """闭环假检索：文本覆盖所有 L3 维度关键词（定义/原理/对比/应用/局限）。"""
    txt = "定义明确、原理清晰、对比充分、应用广泛、局限已知"
    return {
        "findings": txt,
        "uncertainties": [],
        "sources": [
            {"url": "https://e.com/full", "text": txt, "snippet": txt, "source_type": "web"}
        ],
    }


# ---------- D4 显式深度档位 ----------
def test_depth_mapping():
    # depth 覆盖启发式：quick→L1 / standard→L2 / deep→L3
    assert (
        research_mod.research(
            "TCP 是什么", vault_dir=None, cfg=_cfg(), depth="quick", retriever=_fake_retriever
        )["tier"]
        == "L1"
    )
    assert (
        research_mod.research(
            "TCP 是什么", vault_dir=None, cfg=_cfg(), depth="standard", retriever=_fake_retriever
        )["tier"]
        == "L2"
    )
    assert (
        research_mod.research(
            "TCP 是什么", vault_dir=None, cfg=_cfg(), depth="deep", retriever=_fake_retriever
        )["tier"]
        == "L3"
    )
    # depth=None 走既有启发式（含「区别」→ L2）
    assert (
        research_mod.research(
            "TCP 和 UDP 的区别", vault_dir=None, cfg=_cfg(), depth=None, retriever=_fake_retriever
        )["tier"]
        == "L2"
    )
    # 未知 depth 回落 auto 不崩
    assert research_mod.research(
        "TCP 是什么", vault_dir=None, cfg=_cfg(), depth="weird", retriever=_fake_retriever
    )["tier"] in ("L0", "L1")


# ---------- D5 引用导出 ----------
def test_citation_export(tmp_path):
    vd = str(tmp_path)
    out = research_mod.research(
        "某主题",
        cfg=_cfg(),
        tier="L3",
        retriever=_fake_retriever,
        vault_dir=vd,
        export_citations="bibtex",
    )
    rp = vault_mod.vault_path(vd, "某主题")
    report_txt = open(os.path.join(rp, "report.md"), encoding="utf-8").read()
    assert "## 引用" in report_txt  # report.md 含引用区
    bib = open(os.path.join(rp, "citations.bib"), encoding="utf-8").read()
    assert "@misc" in bib and "https://e.com" in bib  # bibtex 格式正确（纯 web 退化为 URL）
    assert out["meta"]["vault"]["citations"]["format"] == "bibtex"


def test_citation_md_export(tmp_path):
    vd = str(tmp_path)
    research_mod.research(
        "某主题",
        cfg=_cfg(),
        tier="L2",
        retriever=_fake_retriever,
        vault_dir=vd,
        export_citations="md",
    )
    rp = vault_mod.vault_path(vd, "某主题")
    md = open(os.path.join(rp, "references.md"), encoding="utf-8").read()
    assert "](" in md and "https://e.com" in md  # Markdown 引用块（[title](url)）


# ---------- D2 逻辑闭环停 ----------
def test_closure_early_stop():
    # 证据已覆盖全部子目标 → L3 循环提前停（iter < max_iter）
    out = research_mod.research(
        "某研究主题",
        cfg=_cfg(),
        tier="L3",
        max_iter=3,
        retriever=_fake_retriever_full,
        vault_dir=None,
    )
    assert out["iterations"] == 1  # 仅质量层一轮，未进入精炼循环
    # closure_check=False 时回覆盖率停（跑满 max_iter）
    out2 = research_mod.research(
        "某研究主题",
        cfg=_cfg(),
        tier="L3",
        max_iter=3,
        closure_check=False,
        retriever=_fake_retriever_full,
        vault_dir=None,
    )
    assert out2["iterations"] == 3
