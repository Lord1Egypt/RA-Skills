import academic
import connector
import scrape
import vault

_ARXIV_XML = """<?xml version="1.0"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <entry>
    <id>http://arxiv.org/abs/2301.00001v1</id>
    <title>Attention Is All You Need Again</title>
    <summary>We propose a new attention mechanism.</summary>
    <published>2023-01-02T00:00:00Z</published>
    <author><name>Jane Doe</name></author>
  </entry>
</feed>"""


def test_academic_intent(monkeypatch):
    assert connector._source_intent("查 arxiv 上注意力机制的论文") == "academic"
    assert connector._source_intent("github 上的 transformer 实现") == "github"
    assert connector._source_intent("某公司 股价 600519") == "finance"


def test_academic_search_parses(monkeypatch):
    monkeypatch.setattr(
        scrape, "_fetch_system_curl", lambda *a, **k: (200, _ARXIV_XML, a[0] if a else "")
    )
    docs, warns = academic.search("attention mechanism", web_fetch=None)
    assert docs and docs[0]["source_type"] == "academic"
    assert docs[0]["citation"]["key"].startswith("arxiv-")
    assert isinstance(warns, list)


def test_academic_bibtex_doi():
    src = [
        {
            "url": "http://arxiv.org/abs/2301.00001",
            "title": "X",
            "citation": {
                "key": "arxiv-x",
                "doi": "10.1/abc",
                "authors": "A",
                "year": "2023",
                "source": "arxiv",
            },
        }
    ]
    bib = vault._citation_bibtex(src)
    assert "@article{arxiv-x" in bib and "doi = {10.1/abc}" in bib


def test_academic_doi_resolver(monkeypatch):
    """D3 调用方注入 resolver：注入 doi_resolver 即回填 DOI，不内置任何书目源。"""
    monkeypatch.setattr(scrape, "_fetch_system_curl", lambda *a, **k: (200, _ARXIV_XML, ""))

    def fake_resolver(aid):
        return f"10.1/{aid}"

    docs, _ = academic.search("attention mechanism", web_fetch=None, doi_resolver=fake_resolver)
    assert docs and docs[0]["citation"]["doi"] == "10.1/2301.00001"


def test_academic_no_resolver_no_doi(monkeypatch):
    """未注入 resolver 时绝不伪造 DOI（保持 @misc 诚实退化）。"""
    monkeypatch.setattr(scrape, "_fetch_system_curl", lambda *a, **k: (200, _ARXIV_XML, ""))
    docs, _ = academic.search("attention mechanism", web_fetch=None)
    assert docs and docs[0]["citation"]["doi"] == ""


def test_connector_forwards_doi_resolver(monkeypatch):
    """connector.load 把 doi_resolver 透传给学术源（调用方注入贯穿）。"""
    captured = {}

    def spy(q, cfg=None, web_fetch=None, max_results=10, doi_resolver=None):
        captured["doi_resolver"] = doi_resolver
        return [], []

    monkeypatch.setattr(academic, "search", spy)
    connector.load("arxiv 论文", cfg={"engines": {}}, doi_resolver="R")
    assert captured.get("doi_resolver") == "R"


def test_research_forwards_doi_resolver():
    """research() 把 doi_resolver 透传到 retriever（顶层调用方注入贯穿）。"""
    from research import research

    captured = {}

    def fake_retriever(q, **kw):
        captured.update(kw)
        return {"sources": [], "findings": "", "uncertainties": [], "scores": []}

    research("arxiv 论文", retriever=fake_retriever, doi_resolver="R")
    assert captured.get("doi_resolver") == "R"
