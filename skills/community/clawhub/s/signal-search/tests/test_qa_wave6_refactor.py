"""test_qa_wave6_refactor.py - 进一步收尾：scrape/verify 复杂度拆分的回归锁。

全部离线：scrape 测试的休眠/网络一律 monkeypatch 掉；verify 用假 embed 向量。
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import scrape
import verify

# ---------- scrape 编排器分解 ----------


def test_scrape_guard_loginwall():
    cfg = {"compliance": {"skip_loginwall_paywall": True}}
    info = scrape._init_info("http://x.com/login")
    out = scrape._scrape_guards("http://x.com/login", cfg, {}, info)
    assert out is not None and out[0] is None and out[1]["loginwall"] is True


def test_scrape_guard_robots(monkeypatch):
    cfg = {"compliance": {"respect_robots": True}}
    monkeypatch.setattr(scrape, "_robots_ok", lambda *a, **k: False)
    info = scrape._init_info("http://x.com/p")
    out = scrape._scrape_guards("http://x.com/p", cfg, {}, info)
    assert out is not None and out[1]["error"] == "robots.txt disallow (M55)"


def test_scrape_guard_blocked_domain(monkeypatch):
    cfg = {"compliance": {}}
    monkeypatch.setattr(scrape, "_robots_ok", lambda *a, **k: True)
    fake = type("B", (), {"get": lambda self, k, d=None: "err"})()
    monkeypatch.setattr(scrape, "_blocked_domains", fake)
    info = scrape._init_info("http://x.com/p")
    out = scrape._scrape_guards("http://x.com/p", cfg, {}, info)
    assert out is not None and "cooldown" in out[1]["error"]


def test_scrape_guard_passes_when_clear(monkeypatch):
    cfg = {"compliance": {}}
    monkeypatch.setattr(scrape, "_robots_ok", lambda *a, **k: True)
    fake_none = type("B", (), {"get": lambda self, k, d=None: None})()
    monkeypatch.setattr(scrape, "_blocked_domains", fake_none)
    info = scrape._init_info("http://x.com/p")
    assert scrape._scrape_guards("http://x.com/p", cfg, {}, info) is None


def test_scrape_retry_429_then_success(monkeypatch):
    """修复点：首次 429 重试，二次成功 → 返回正文且 blocked=False（不再残留 blocked）。"""
    cfg = {"compliance": {"respect_robots": False}, "proxies": []}
    monkeypatch.setattr(scrape.time, "sleep", lambda *a, **k: None)
    calls = {"n": 0}

    def fake_attempt(url, headers, proxy, timeout, cfg_, info):
        calls["n"] += 1
        if calls["n"] == 1:
            return "retry", None, "status 429"
        return "ok", "<html>real content</html>", None

    monkeypatch.setattr(scrape, "_scrape_attempt", fake_attempt)
    html, info = scrape.scrape("http://x.com/p", {"cfg": cfg})
    assert html == "<html>real content</html>"
    assert info["blocked"] is False
    assert calls["n"] == 2


def test_scrape_retry_all_fail_blocks(monkeypatch):
    cfg = {"compliance": {"respect_robots": False}, "proxies": []}
    monkeypatch.setattr(scrape.time, "sleep", lambda *a, **k: None)
    monkeypatch.setattr(scrape, "_scrape_attempt", lambda *a, **k: ("retry", None, "status 503"))
    html, info = scrape.scrape("http://x.com/p", {"cfg": cfg})
    assert html is None
    assert info["blocked"] is True
    assert info["error"] == "status 503"


def test_scrape_attempt_challenge_blocks(monkeypatch):
    cfg = {"compliance": {"pii_redact": False}}
    info = scrape._init_info("http://x.com/p")
    # 用含挑战标记的假 html 直接验证分支（不触网）
    monkeypatch.setattr(
        scrape,
        "_fetch_requests",
        lambda *a, **k: (
            200,
            "<html>" + "captcha just a moment " * 20 + "</html>",
            "http://x.com/p",
        ),
    )
    monkeypatch.setattr(scrape, "_HAS_CURL_CFFI", False)
    outcome, html, _err = scrape._scrape_attempt(
        "http://x.com/p", {"User-Agent": "x"}, None, 15, cfg, info
    )
    assert outcome == "blocked" and info["challenge"] is True


def test_scrape_attempt_empty_falls_back(monkeypatch):
    cfg = {"compliance": {"pii_redact": False}}
    info = scrape._init_info("http://x.com/p")
    monkeypatch.setattr(scrape, "_HAS_CURL_CFFI", False)
    # 主通道空响应
    monkeypatch.setattr(scrape, "_fetch_requests", lambda *a, **k: (200, "", "http://x.com/p"))
    # 系统 curl 兜底成功
    monkeypatch.setattr(
        scrape,
        "_fetch_system_curl",
        lambda *a, **k: (200, "<html>" + "fallback body ok " * 20 + "</html>", "http://x.com/p"),
    )
    outcome, html, _err = scrape._scrape_attempt(
        "http://x.com/p", {"User-Agent": "x"}, None, 15, cfg, info
    )
    assert outcome == "ok" and "fallback" in html and info["method"] == "system_curl"


# ---------- verify 语义核验分解 ----------


def test_split_facts_strips_metadata():
    findings = "结论一成立。来源：https://a.com 置信度：高 未确认项：x\n## 维度标题\n（该维度暂无直接来源）"
    facts = verify._split_facts(findings)
    assert all("来源" not in f and "置信度" not in f for f in facts)
    assert all("维度标题" not in f for f in facts)
    assert facts  # 至少保留"结论一成立"


def test_score_fact_true(monkeypatch):
    def fake_embed(texts):
        return [[1.0, 0.0] if "TCP" in t else [0.0, 1.0] for t in texts]

    def fake_sim(a, b):
        return 1.0 if a == b else 0.0

    src_ctx = verify._source_ctx([{"url": "u", "text": "TCP 是面向连接的传输层协议"}])
    verdict, source, _score, _reason = verify._score_fact(
        "TCP 是面向连接的", {"TCP", "面向连接"}, src_ctx, 0.55, fake_embed, fake_sim
    )
    assert verdict == "TRUE" and source == "u"


def test_score_fact_uncertain_below_threshold(monkeypatch):
    def fake_embed(texts):
        return [[1.0, 0.0], [0.0, 1.0]]

    def fake_sim(a, b):
        return 0.1

    src_ctx = verify._source_ctx([{"url": "u", "text": "TCP 是面向连接的传输层协议"}])
    verdict, source, _score, _reason = verify._score_fact(
        "月球是地球的卫星", {"月球", "卫星"}, src_ctx, 0.55, fake_embed, fake_sim
    )
    assert verdict == "UNCERTAIN" and source is None


def test_semantic_backend_unavailable_falls_back(monkeypatch):
    monkeypatch.setattr("embed._TRY_ST", False)
    findings = "TCP 是面向连接的传输层协议。"
    sources = [{"url": "https://x.com/a", "text": "TCP 是面向连接的传输层协议，提供可靠传输。"}]
    res = verify.semantic_fact_verify(findings, sources, {"verify": {"semantic_threshold": 0.55}})
    # 回退 fact_level_verify → 关键词重叠 ≥1 → TRUE
    assert res and res[0]["verdict"] == "TRUE" and res[0]["source"] == "https://x.com/a"
