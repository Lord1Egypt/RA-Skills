import research as research_mod


def _fake_retriever(query, **kw):
    return {
        "findings": "f",
        "uncertainties": [],
        "sources": [{"url": "https://e.com/1", "text": "x"}],
    }


def test_conflict_check_fn():
    captured = {}

    def cf(q, ev):
        captured["q"] = q
        return [{"a": "https://e.com/1", "b": "https://e.com/2", "reason": "conflict"}]

    out = research_mod.research(
        "某研究问题",
        cfg={},
        tier="L2",
        retriever=_fake_retriever,
        vault_dir=None,
        conflict_check_fn=cf,
    )
    assert out["conflicts"] and out["conflicts"][0]["reason"] == "conflict"
    assert captured["q"] == "某研究问题"


def test_closure_fn_stops_early():
    calls = {"n": 0}

    def ret(query, **kw):
        calls["n"] += 1
        return {
            "findings": "f",
            "uncertainties": [],
            "sources": [{"url": "https://e.com/1", "text": "x"}],
        }

    def cf(q, ev, f):
        return True  # 主问题已答

    out = research_mod.research(
        "深度研究 X",
        cfg={},
        tier="L3",
        retriever=ret,
        vault_dir=None,
        max_iter=3,
        closure_check=False,
        closure_fn=cf,
    )
    # 首轮 retriever + 循环首次 res2 前判 closure_fn 即停 → 共 2 次（无 closure_fn 为 3 次）
    assert calls["n"] == 2
    assert out["tier"] == "L3"
