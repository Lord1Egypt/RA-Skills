"""P1 源池扩展防复发测试：金融(B1) / GitHub(B2) / 反爬级联(B3) / 意图路由。

不依赖真实外网：finance 走 monkeypatch scrape._fetch_system_curl，github 走 monkeypatch
github._api_get。仅验证路由、解析、兜底与 warning 透传逻辑。
"""

import json

import connector
import finance
import github
import orchestrate
import scrape


# ---------- 意图路由 ----------
def test_source_intent_finance():
    assert connector._source_intent("贵州茅台 股价 近半年波动") == "finance"
    assert connector._source_intent("600519 市盈率") == "finance"


def test_source_intent_github():
    assert connector._source_intent("github 上有什么好用的 llama 框架") == "github"
    assert connector._source_intent("查一个开源项目 repo") == "github"


def test_source_intent_general():
    assert connector._source_intent("人工智能 发展 现状") == "general"


def test_source_intent_pe_not_false_positive():
    # 子串 "pe" 不应把 people/open 等词误判为金融
    assert connector._source_intent("people 行为研究") == "general"
    assert connector._source_intent("开放的 API 设计") == "general"


# ---------- 金融源（mock 系统 curl） ----------
_QUOTE = {
    "rc": 0,
    "data": {
        "f43": "1685.00",
        "f57": "600519",
        "f58": "贵州茅台",
        "f60": "1666.00",
        "f116": "2116800000000",
        "f168": "0.5",
        "f170": "28.5",
    },
}
_KLINE = {
    "rc": 0,
    "data": {
        "klines": [
            "2026-01-02,1600,1685,1700,1590,10000,1.6e9,2.1,1.1,0.5,0.4",
            "2026-01-03,1685,1690,1695,1680,9000,1.5e9,1.0,0.3,0.4,0.3",
        ]
    },
}
_FFLOW = {
    "rc": 0,
    "data": {
        "klines": [
            "2026-01-02,1000000,200000,300000,400000,500000,600000,0.1",
            "2026-01-03,1200000,250000,350000,450000,550000,650000,0.12",
        ]
    },
}


def _fake_curl_ok(url, headers, proxy, timeout=15):
    if "search/prefix" in url:
        return (
            200,
            json.dumps({"rc": 0, "data": {"list": [{"code": "600519", "name": "贵州茅台"}]}}),
            url,
        )
    if "stock/get" in url:
        return 200, json.dumps(_QUOTE), url
    if "kline" in url:
        return 200, json.dumps(_KLINE), url
    if "fflow" in url:
        return 200, json.dumps(_FFLOW), url
    return 0, "", url


def test_finance_fetch_builds_doc(monkeypatch):
    monkeypatch.setattr(scrape, "_fetch_system_curl", _fake_curl_ok)
    docs, warns = finance.fetch("600519 股价", cfg={})
    assert len(docs) == 1
    d = docs[0]
    assert d["source_type"] == "finance"
    assert d["code"] == "600519"
    assert d["name"] == "贵州茅台"
    assert "东方财富行情" in d["text"]
    assert d["landing_resolved"] is True
    assert warns == []


def test_finance_fetch_name_resolve(monkeypatch):
    monkeypatch.setattr(scrape, "_fetch_system_curl", _fake_curl_ok)
    docs, _ = finance.fetch("贵州茅台 近半年股市波动", cfg={})
    assert len(docs) == 1 and docs[0]["code"] == "600519"


def test_finance_fetch_no_code():
    docs, warns = finance.fetch("今天天气怎么样", cfg={})
    assert docs == []
    assert any("股票代码" in w for w in warns)


def test_finance_fetch_fail_fallback_web_fetch(monkeypatch):
    monkeypatch.setattr(scrape, "_fetch_system_curl", lambda *a, **k: (0, "", a[0]))
    captured = {}

    def fake_web_fetch(url):
        captured["url"] = url
        return "<html>东财网页兜底内容</html>"

    docs, warns = finance.fetch("600519 股价", cfg={}, web_fetch=fake_web_fetch)
    assert len(docs) == 1
    assert "东财网页兜底" in docs[0]["text"]
    assert captured["url"].endswith("sh600519.html")


def test_finance_fetch_fail_no_web_fetch(monkeypatch):
    monkeypatch.setattr(scrape, "_fetch_system_curl", lambda *a, **k: (0, "", a[0]))
    docs, warns = finance.fetch("600519 股价", cfg={})
    assert docs == []
    assert any("web_fetch" in w for w in warns)


# ---------- GitHub 源（mock API） ----------
_REPO = {
    "items": [
        {
            "full_name": "org/llama",
            "description": "大模型",
            "stargazers_count": 1234,
            "language": "Python",
            "html_url": "https://github.com/org/llama",
        }
    ]
}


def test_github_search_ok(monkeypatch):
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    monkeypatch.setattr(github, "_api_get", lambda url, tok: (200, _REPO, {}))
    docs, warns = github.search("llama 框架", cfg={})
    assert len(docs) == 1
    d = docs[0]
    assert d["source_type"] == "github"
    assert d["repo"] == "org/llama"
    assert "llama" in d["text"]


def test_github_search_no_token_warns(monkeypatch):
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    monkeypatch.setattr(github, "_api_get", lambda url, tok: (403, None, {}))
    docs, warns = github.search("llama 框架", cfg={})
    assert docs == []
    assert any("GITHUB_TOKEN" in w for w in warns)


def test_github_search_no_token_web_fetch_fallback(monkeypatch):
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    monkeypatch.setattr(github, "_api_get", lambda url, tok: (403, None, {}))
    captured = {}

    def fake_web_fetch(url):
        captured["url"] = url
        return "<html>github 搜索页</html>"

    docs, warns = github.search("llama 框架", cfg={}, web_fetch=fake_web_fetch)
    assert len(docs) == 1
    assert "github 搜索页" in docs[0]["text"]
    assert "github.com/search" in captured["url"]
    assert any("GITHUB_TOKEN" in w for w in warns)


def test_github_search_token_rotation(monkeypatch):
    monkeypatch.setenv("GITHUB_TOKEN", "a,b")

    def fake_api(url, tok):
        if tok == "a":
            return 403, None, {}
        return 200, _REPO, {}

    monkeypatch.setattr(github, "_api_get", fake_api)
    docs, warns = github.search("llama 框架", cfg={})
    assert len(docs) == 1
    assert warns == []  # 轮换到有效 token，成功无 warning


# ---------- connector 路由集成 ----------
def test_connector_routes_finance(monkeypatch):
    monkeypatch.setattr(scrape, "_fetch_system_curl", _fake_curl_ok)
    docs = connector.load("600519 股价", cfg={})
    assert len(docs) == 1 and docs[0]["source_type"] == "finance"


def test_connector_routes_github(monkeypatch):
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    monkeypatch.setattr(github, "_api_get", lambda url, tok: (200, _REPO, {}))
    docs = connector.load("github llama 框架", cfg={})
    assert len(docs) == 1 and docs[0]["source_type"] == "github"


def test_github_search_token_injected_preferred(monkeypatch):
    """由调用方提供：调用方注入 github_token 应优先于 env GITHUB_TOKEN。"""
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    captured = {}

    def fake_api(url, tok):
        captured["tok"] = tok
        return (200, _REPO, {})

    monkeypatch.setattr(github, "_api_get", fake_api)
    docs, warns = github.search("llama 框架", cfg={}, github_token="injected_xyz")
    assert captured.get("tok") == "injected_xyz"
    assert len(docs) == 1 and docs[0]["source_type"] == "github"


def test_research_passes_github_token(monkeypatch):
    """research(github_token=) 应透传到 GitHub 源（端到端调用方注入口子）。"""
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    captured = {}

    def fake_api(url, tok):
        captured["tok"] = tok
        return (200, _REPO, {})

    monkeypatch.setattr(github, "_api_get", fake_api)
    monkeypatch.setattr(connector, "_source_intent", lambda q: "github")
    import research as research_mod

    research_mod.research(
        "github 上有什么好用的 llama 框架", tier="L1", github_token="from_research"
    )
    assert captured.get("tok") == "from_research"


def test_connector_general_no_crash():
    # 通用路径（沙箱不可达外网）应返回 list 且不抛
    docs = connector.load("人工智能 发展", cfg={})
    assert isinstance(docs, list)


# ---------- retrieve 透出 warnings ----------
def test_retrieve_surfaces_warnings(monkeypatch):
    monkeypatch.setattr(scrape, "_fetch_system_curl", _fake_curl_ok)
    res = orchestrate.retrieve("600519 股价", cfg={})
    assert "warnings" in res
    assert isinstance(res["warnings"], list)
    assert len(res["sources"]) >= 1
    assert res["sources"][0]["source_type"] == "finance"
