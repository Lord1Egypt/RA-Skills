import builtins

import research_cli


def _fake_retriever(query, **kw):
    return {
        "findings": "结论文本",
        "uncertainties": [],
        "sources": [{"url": "https://e.com/1", "text": "x"}],
    }


def test_cli_continue(monkeypatch, tmp_path):
    monkeypatch.setattr(builtins, "input", lambda prompt: "continue")
    out = research_cli.research_interactive(
        "大纲测试", cfg={}, vault_dir=str(tmp_path), tier="L2", retriever=_fake_retriever
    )
    # continue → 不应被取消；二次跑出完整结果
    assert "cancelled" not in out
    assert out.get("findings") == "结论文本"


def test_cli_cancel(monkeypatch, tmp_path):
    monkeypatch.setattr(builtins, "input", lambda prompt: "no")
    out = research_cli.research_interactive(
        "大纲测试", cfg={}, vault_dir=str(tmp_path), tier="L2", retriever=_fake_retriever
    )
    assert out.get("cancelled") is True
