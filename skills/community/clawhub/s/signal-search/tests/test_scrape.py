"""scrape 模块的零依赖回归单测：TLS 校验开关 + 抓取失败隔离。

不依赖 pytest monkeypatch：对 fetch 函数与 time.sleep 做手动 setattr，并在 finally 还原。
"""

import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import scrape as _scrape


def _noop_sleep(*_a, **_k):
    return None


def _patch_fetch(kind):
    """kind='ok' 返回足够长的假 html（避免触发系统 curl 兜底）；kind='fail' 抛出模拟单源失败。"""
    orig_cffi = _scrape._fetch_curl_cffi
    orig_req = _scrape._fetch_requests

    def _restore():
        _scrape._fetch_curl_cffi = orig_cffi
        _scrape._fetch_requests = orig_req

    if kind == "ok":
        _body = "<html>" + "OK_CONTENT " * 30 + "</html>"

        def fake(*_a, **_k):
            return 200, _body, "http://x"

    else:

        def fake(*_a, **_k):
            raise RuntimeError("simulated fetch failure")

    _scrape._fetch_curl_cffi = fake
    _scrape._fetch_requests = fake
    return _restore


def _patch_sleep():
    orig = time.sleep
    time.sleep = _noop_sleep
    return lambda: setattr(time, "sleep", orig)


def _cfg(tls_verify):
    return {
        "scrape": {"tls_verify": tls_verify},
        "compliance": {"respect_robots": False, "rate_limit_per_sec": 0},
        "warmup_domains": [],
    }


def test_tls_verify_default_true():
    assert _scrape._tls_verify(None) is True
    assert _scrape._tls_verify({}) is True
    assert _scrape._tls_verify({"scrape": {}}) is True


def test_tls_verify_explicit_false():
    assert _scrape._tls_verify({"scrape": {"tls_verify": False}}) is False


def test_scrape_warns_on_tls_disabled():
    restore_f = _patch_fetch("ok")
    restore_s = _patch_sleep()
    try:
        meta = {"cfg": _cfg(False), "warnings": []}
        html, _info = _scrape.scrape("http://ok-a.test", meta)
        assert "OK_CONTENT" in html
        assert any("MITM" in w for w in meta["warnings"])
    finally:
        restore_f()
        restore_s()


def test_scrape_no_warn_on_tls_enabled():
    restore_f = _patch_fetch("ok")
    restore_s = _patch_sleep()
    try:
        meta = {"cfg": _cfg(True), "warnings": []}
        html, _info = _scrape.scrape("http://ok-b.test", meta)
        assert "OK_CONTENT" in html
        assert not any("MITM" in w for w in meta["warnings"])
    finally:
        restore_f()
        restore_s()


def test_scrape_isolates_fetch_failure():
    restore_f = _patch_fetch("fail")
    restore_s = _patch_sleep()
    try:
        meta = {"cfg": _cfg(True), "warnings": []}
        # 单源抓取失败不应抛出，应优雅返回空 html + 带 error 的 info（失败隔离）
        html, info = _scrape.scrape("http://fail-c.test", meta)
        assert not html
        assert isinstance(info, dict)
        assert info.get("error")
    finally:
        restore_f()
        restore_s()
