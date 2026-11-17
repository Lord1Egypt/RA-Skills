"""P2 Research Vault 收集层防复发测试（A1-A5）。

覆盖：落盘结构生成 / resume 跳过重抓 / report 幂等 / STORM outline 持久化 / 显式关闭退纯内存。
"""

import json
import os

import research as research_mod
import vault as vault_mod


def _fake_retriever(query, cfg=None, schema=None, prior_evidence=None, docs=None, **kw):
    slug = str(abs(hash(query)) % 100000)
    return {
        "findings": f"关于{query}的研究发现",
        "uncertainties": [],
        "sources": [
            {"url": f"https://e.com/{slug}", "snippet": "TCP 面向连接", "text": "TCP 面向连接详情"}
        ],
    }


def _cfg():
    return {"research": {"agent_dispatch": False, "model_tier": False}}


def test_vault_emit_creates_structure(tmp_path):
    """vault_dir 给定：跑完生成 INDEX/outline/items/report + .state.json。"""
    vd = str(tmp_path)
    out = research_mod.research(
        "TCP 和 UDP 的区别及原理", cfg=_cfg(), tier="L2", retriever=_fake_retriever, vault_dir=vd
    )
    vp = vault_mod.vault_path(vd, "TCP 和 UDP 的区别及原理")
    assert os.path.isdir(vp)
    assert os.path.isfile(os.path.join(vp, "INDEX.md"))
    assert os.path.isfile(os.path.join(vp, "outline.md"))
    assert os.path.isfile(os.path.join(vp, "report.md"))
    assert os.path.isfile(os.path.join(vp, ".state.json"))
    items = os.listdir(os.path.join(vp, "items"))
    assert any(f.endswith(".md") for f in items)
    # state 含 completed
    st = json.load(open(os.path.join(vp, ".state.json"), encoding="utf-8"))
    assert st.get("completed")
    # meta.vault 提醒调用方可关
    assert out["meta"]["vault"]["enabled"] is True
    assert "vault_dir=None" in out["meta"]["vault"]["note"]


def test_vault_resume_skips_repeat(tmp_path):
    """resume=True 且已完成：跳过重抓（不调 retriever）。"""
    vd = str(tmp_path)
    calls = []

    def _count(query, cfg=None, schema=None, prior_evidence=None, docs=None, **kw):
        calls.append(query)
        return _fake_retriever(query, cfg=cfg, schema=schema, prior_evidence=prior_evidence)

    # 第一次
    research_mod.research(
        "TCP 和 UDP 的区别及原理", cfg=_cfg(), tier="L2", retriever=_count, vault_dir=vd
    )
    first_n = len(calls)
    assert first_n >= 1
    # 第二次 resume
    out2 = research_mod.research(
        "TCP 和 UDP 的区别及原理",
        cfg=_cfg(),
        tier="L2",
        retriever=_count,
        vault_dir=vd,
        resume=True,
    )
    # 不应再调 retriever
    assert len(calls) == first_n
    assert out2.get("resumed") is True


def test_vault_idempotent_report(tmp_path):
    """report.md 幂等：重跑内容一致（不重复）。"""
    vd = str(tmp_path)
    research_mod.research(
        "TCP 原理研究", cfg=_cfg(), tier="L2", retriever=_fake_retriever, vault_dir=vd
    )
    vp = vault_mod.vault_path(vd, "TCP 原理研究")
    r1 = open(os.path.join(vp, "report.md"), encoding="utf-8").read()
    # 重渲染（再跑一次，非 resume）
    research_mod.research(
        "TCP 原理研究", cfg=_cfg(), tier="L2", retriever=_fake_retriever, vault_dir=vd
    )
    r2 = open(os.path.join(vp, "report.md"), encoding="utf-8").read()
    assert r1 == r2


def test_outline_persist_storm(tmp_path):
    """outline.md 含 STORM 多视角 + 可验证清单。"""
    vd = str(tmp_path)
    research_mod.research("某主题", cfg=_cfg(), tier="L3", retriever=_fake_retriever, vault_dir=vd)
    vp = vault_mod.vault_path(vd, "某主题")
    txt = open(os.path.join(vp, "outline.md"), encoding="utf-8").read()
    assert "STORM" in txt
    assert "Domain Expert" in txt
    assert "Skeptic" in txt
    assert "[ ]" in txt  # 可验证清单勾选框


def test_vault_off_is_pure_memory(tmp_path):
    """显式 vault_dir=None：不落盘、meta.vault.enabled=False、行为同前。"""
    # tmp_path 不应被创建 vault 子目录
    out = research_mod.research(
        "TCP 是什么", cfg=_cfg(), tier="L0", retriever=_fake_retriever, vault_dir=None
    )
    assert out["meta"]["vault"]["enabled"] is False
    # L0 扁平：无 schema、单次检索
    assert out["schema"] == []
    # 不写任何文件
    assert not any(f.startswith(vault_mod.slug("TCP 是什么")) for f in os.listdir(str(tmp_path)))
