import json

import connector
import scrape
import searxng_client

_SX_JSON = json.dumps(
    {
        "results": [
            {"url": "https://real.com/a", "title": "A", "content": "about a"},
            {"url": "https://real.com/b", "title": "B", "content": "about b"},
        ]
    }
)


def test_searxng_fetch_curl(monkeypatch):
    monkeypatch.setattr(
        scrape, "_fetch_system_curl", lambda *a, **k: (200, _SX_JSON, a[0] if a else "")
    )
    docs = searxng_client.fetch(
        "python", cfg={"searxng": {"enabled": True, "url": "http://sx"}}, web_fetch=None
    )
    assert len(docs) == 2 and docs[0]["engine"] == "SearXNG"


def test_searxng_routed_via_connector(monkeypatch):
    monkeypatch.setattr(
        scrape, "_fetch_system_curl", lambda *a, **k: (200, _SX_JSON, a[0] if a else "")
    )
    cfg = {"searxng": {"enabled": True, "url": "http://sx"}}
    docs = connector.load("通用查询 python 教程", cfg=cfg, web_fetch=None)
    assert any(d.get("engine") == "SearXNG" for d in docs)
