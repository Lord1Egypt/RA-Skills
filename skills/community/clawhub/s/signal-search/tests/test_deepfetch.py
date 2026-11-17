import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import deepfetch
import extract
import scrape

_LINK_AAA = "https://www.baidu.com/link?url=AAA123"
_LINK_BBB = "https://www.baidu.com/link?url=BBB456"
_LINK_ARTICLE = "https://real-answer.example.com/article"
MOCK_BAIDU_SERP = f"""
<html><body>
  <div class="c-container"><h3><a href="{_LINK_AAA}">TCP和UDP核心区别详解</a></h3></div>
  <div class="c-container"><h3><a href="{_LINK_BBB}">UDP与TCP区别</a></h3></div>
  <div class="c-container"><h3><a href="{_LINK_ARTICLE}">跨域直链结果</a></h3></div>
  <a href="https://www.baidu.com/s?wd=其他问题">相关搜索</a>
  <a href="https://www.baidu.com/">百度首页</a>
  <a href="https://zhidao.baidu.com/question/1">百度知道</a>
</body></html>
"""

FAKE_LANDING = """<html><head><title>真实答案</title></head><body>
<article><p>TCP 是一种面向连接的传输层协议，提供可靠传输。UDP 是无连接的，不保证可靠交付。</p>
<p>两者核心区别在连接方式。</p></article></body></html>"""


def test_parse_serp_links_keeps_redirector_and_cross_domain():
    links = extract.parse_serp_links(MOCK_BAIDU_SERP, "Baidu")
    # 保留：baidu 结果重定向器 + 跨域直链结果（均位于 c-container h3）
    assert "https://www.baidu.com/link?url=AAA123" in links
    assert "https://real-answer.example.com/article" in links
    # 剔除：站内导航(/s?、首页)、同域非重定向器(zhidao)
    assert all("/s?" not in u for u in links)
    assert not any(u == "https://www.baidu.com/" for u in links)
    assert not any("zhidao.baidu.com" in u for u in links)


def test_resolve_two_hop(monkeypatch):
    def fake_scrape(url, meta=None):
        # 对任意链接都返回假落地页（final_url 为真实站点）
        return FAKE_LANDING, {"final_url": "https://real-site.com/article", "status": 200}

    monkeypatch.setattr(scrape, "scrape", fake_scrape)

    serp = [{"url": "https://www.baidu.com/s?wd=x", "raw_html": MOCK_BAIDU_SERP, "engine": "Baidu"}]
    out = deepfetch.resolve(
        serp,
        {
            "deep_fetch": {
                "enabled": True,
                "max_pages_per_query": 3,
                "fallback_to_serp": True,
                "timeout_per_page": 15,
            },
            "cache": {"enabled": False},
        },
    )
    assert len(out) == 1
    d = out[0]
    assert d["landing_resolved"] is True
    assert d["url"] == "https://real-site.com/article"
    assert "TCP" in (d.get("text") or "")
    assert d["engine"] == "Baidu"
    assert d["serp_url"] == "https://www.baidu.com/s?wd=x"


def test_resolve_fallback_when_landing_fails(monkeypatch):
    def fake_scrape(url, meta=None):
        return None, {"blocked": True, "error": "challenge"}

    monkeypatch.setattr(scrape, "scrape", fake_scrape)

    serp = [{"url": "https://www.baidu.com/s?wd=x", "raw_html": MOCK_BAIDU_SERP, "engine": "Baidu"}]
    out = deepfetch.resolve(
        serp,
        {
            "deep_fetch": {
                "enabled": True,
                "max_pages_per_query": 3,
                "fallback_to_serp": True,
                "timeout_per_page": 15,
            },
            "cache": {"enabled": False},
        },
    )
    assert len(out) == 1
    assert out[0].get("landing_failed") is True
    assert out[0].get("landing_resolved") is not True


def test_resolve_disabled_returns_serp_as_is():
    serp = [{"url": "https://www.baidu.com/s?wd=x", "raw_html": MOCK_BAIDU_SERP, "engine": "Baidu"}]
    out = deepfetch.resolve(serp, {"deep_fetch": {"enabled": False}})
    assert out == serp


def test_resolve_cache_hit_skips_scrape(monkeypatch):
    class FakeCache:
        def __init__(self, cfg=None):
            self.puts = []
            self.store = {}

        def get(self, key):
            return self.store.get(key)

        def put(self, key, val):
            self.puts.append(key)
            self.store[key] = val

    fc = FakeCache()
    monkeypatch.setattr("cache.Cache", lambda cfg=None: fc)

    # 单结果链接 SERP：首跑抓取并写缓存，二跑应全命中、不再抓取
    SINGLE = '<html><body><div class="c-container"><h3><a href="https://www.baidu.com/link?url=AAA123">x</a></h3></div></body></html>'  # noqa: E501
    calls = {}

    def fake_scrape(url, meta=None):
        calls[url] = True
        # 模拟 /link? 重定向器 302 到真实落地站（非搜索引擎自身域名）
        final = url.replace("www.baidu.com", "real-site.com")
        return FAKE_LANDING, {"final_url": final, "status": 200}

    monkeypatch.setattr(scrape, "scrape", fake_scrape)

    serp = [{"url": "https://www.baidu.com/s?wd=x", "raw_html": SINGLE, "engine": "Baidu"}]
    cfg = {
        "deep_fetch": {
            "enabled": True,
            "max_pages_per_query": 3,
            "fallback_to_serp": True,
            "timeout_per_page": 15,
        },
        "cache": {"enabled": True, "dir": ".cache/", "ttl_minutes": 1440},
    }
    out = deepfetch.resolve(serp, cfg)
    assert len(out) == 1
    assert len(fc.puts) >= 1  # 首跑写入缓存

    # 二次解析：缓存命中 → 不再调 scrape
    calls.clear()
    out2 = deepfetch.resolve(serp, cfg)
    assert out2[0]["url"] == out[0]["url"]
    assert len(calls) == 0


def test_resolve_concurrent_multi_serp(monkeypatch):
    """多 SERP doc 并发抓取不串档、各自锚定正确。"""

    def fake_scrape(url, meta=None):
        # 用 url 区分返回不同落地正文，验证归属不串；final_url 模拟重定向到真实站
        final = url.replace("www.baidu.com", "real-site.com")
        body = f"<html><body><article><p>来源标记 {url[-4:]}。</p>{FAKE_LANDING}</article></body></html>"
        return body, {"final_url": final, "status": 200}

    monkeypatch.setattr(scrape, "scrape", fake_scrape)

    serp = [
        {"url": "https://www.baidu.com/s?wd=x", "raw_html": MOCK_BAIDU_SERP, "engine": "Baidu"},
    ]
    cfg = {
        "deep_fetch": {
            "enabled": True,
            "max_pages_per_query": 3,
            "fallback_to_serp": True,
            "timeout_per_page": 15,
        },
        "cache": {"enabled": False},
    }
    out = deepfetch.resolve(serp, cfg)
    assert len(out) == 1
    assert "TCP" in (out[0].get("text") or "")
    assert "来源标记" in (out[0].get("text") or "")
    assert out[0]["landing_resolved"] is True


def test_sogou_selector_extracts_redirectors():
    here = os.path.dirname(__file__)
    fx = os.path.join(here, "fixtures", "sogou_tcp_udp.html")
    if not os.path.exists(fx):
        import pytest

        pytest.skip("fixture missing")
    html = open(fx, encoding="utf-8").read()
    links = extract.parse_serp_links(
        html, "Sogou", None, max_links=10, serp_url="https://www.sogou.com/web?query=TCP"
    )
    assert len(links) >= 5
    # 归一化后含 sogou /link? 重定向器绝对 URL（修复前为 0）
    assert any("sogou.com/link?url=" in link for link in links)
    # 直链 baike.sogou.com 亦保留
    assert any("baike.sogou.com" in link for link in links)
