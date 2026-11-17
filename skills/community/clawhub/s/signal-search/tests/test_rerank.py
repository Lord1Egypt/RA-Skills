"""语义 rerank 的零依赖回归单测（覆盖 有/无 ST 两路径、hybrid、top_k、默认关、离线守卫）。

不依赖 pytest monkeypatch 可用性：对 embed 模块做手动 setattr 并在 finally 还原，
因此对任何"零依赖运行器"都可直接 collect 执行。
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import embed as _embed_mod
import rerank


def _patch_embed(try_st: bool, fake_embed):
    """手动 patch embed 模块的 _TRY_ST 与 embed 函数，返回还原闭包。"""
    orig_st = _embed_mod._TRY_ST
    orig_fn = _embed_mod.embed

    def _restore():
        _embed_mod._TRY_ST = orig_st
        _embed_mod.embed = orig_fn

    _embed_mod._TRY_ST = try_st
    _embed_mod.embed = fake_embed
    return _restore


def _docs():
    return [
        {
            "url": "http://a.com",
            "title": "无关主题：烹饪食谱",
            "snippet": "如何做蛋糕",
            "text": "烘焙技巧与烤箱温度",
        },
        {
            "url": "http://b.com",
            "title": "TCP 与 UDP 区别",
            "snippet": "传输层协议对比",
            "text": "TCP 面向连接，UDP 无连接，三次握手",
        },
        {
            "url": "http://c.com",
            "title": "网络协议概述",
            "snippet": "TCP UDP 核心差异",
            "text": "三次握手与拥塞控制",
        },
    ]


def _scores():
    return [{"weighted": 0.3}, {"weighted": 0.9}, {"weighted": 0.6}]


def test_default_off_returns_unchanged():
    docs, scores = _docs(), _scores()
    out_d, out_s = rerank.rerank(docs, scores, "TCP 和 UDP 区别", {"rerank": {"enabled": False}})
    assert out_d is docs and out_s is scores
    assert "rerank_score" not in scores[0]


def test_offline_guard_returns_unchanged():
    os.environ["SIGNAL_SEARCH_OFFLINE"] = "1"
    try:
        docs, scores = _docs(), _scores()
        out_d, out_s = rerank.rerank(docs, scores, "q", {"rerank": {"enabled": True}})
        assert out_d is docs and "rerank_score" not in scores[0]
    finally:
        os.environ.pop("SIGNAL_SEARCH_OFFLINE", None)


def _keyword_vec(texts, dims=("tcp", "udp", "区别", "协议")):
    """确定性向量：命中关键词的维度置 1，便于断言语义相关源被前置。"""
    out = []
    for t in texts:
        v = [0.0] * len(dims)
        tl = (t or "").lower()
        for i, k in enumerate(dims):
            if k in tl:
                v[i] += 1.0
        out.append(v)
    return out


def test_semantic_promotes_relevant_with_st():
    restore = _patch_embed(True, _keyword_vec)
    try:
        docs, scores = _docs(), _scores()
        out_d, out_s = rerank.rerank(
            docs,
            scores,
            "TCP 和 UDP 区别是什么",
            {"rerank": {"enabled": True, "method": "semantic", "top_k": 3}},
        )
        urls = [d["url"] for d in out_d]
        # 语义相关（b/c 含 tcp/udp）应排到原 weighted 最高项（a 权重 0.9）之前
        assert urls[0] in ("http://b.com", "http://c.com")
        assert "rerank_score" in out_s[0]
    finally:
        restore()


def test_hybrid_blend():
    restore = _patch_embed(True, _keyword_vec)
    try:
        docs, scores = _docs(), _scores()
        out_d, _ = rerank.rerank(
            docs,
            scores,
            "TCP UDP 区别",
            {"rerank": {"enabled": True, "method": "hybrid", "alpha": 0.5, "top_k": 3}},
        )
        # hybrid 仍把语义相关源（b 含 tcp/udp）前置，盖过纯 weighted 顺序
        assert out_d[0]["url"] == "http://b.com"
    finally:
        restore()


def test_fallback_to_lexical_without_st():
    # 无 ST：embed.embed 走真实降级关键词哈希向量；semantic 路径不崩溃且写入 rerank_score
    restore = _patch_embed(False, _embed_mod.embed)
    try:
        docs, scores = _docs(), _scores()
        out_d, out_s = rerank.rerank(
            docs,
            scores,
            "任意查询",
            {"rerank": {"enabled": True, "method": "semantic", "top_k": 3}},
        )
        assert len(out_d) == 3
        assert all("rerank_score" in s for s in out_s)
    finally:
        restore()


def test_top_k_truncates():
    restore = _patch_embed(True, lambda texts: [[1.0, 0.0, 0.0, 0.0] for _ in texts])
    try:
        docs = _docs() * 2  # 6 docs
        scores = [{"weighted": 0.5}] * 6
        out_d, _ = rerank.rerank(
            docs, scores, "q", {"rerank": {"enabled": True, "method": "semantic", "top_k": 2}}
        )
        assert len(out_d) == 2
    finally:
        restore()
