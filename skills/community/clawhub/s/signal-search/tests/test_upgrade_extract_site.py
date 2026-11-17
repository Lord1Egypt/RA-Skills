import extract

_ARXIV_HTML = """<html><body>
<h1>Title</h1>
<div class="abstract">This is the abstract content about attention.</div>
<nav>noise nav should be excluded</nav>
</body></html>"""


def test_extract_site_selector():
    doc = {"raw_html": _ARXIV_HTML, "url": "https://arxiv.org/abs/2301.00001"}
    out = extract.extract(doc, cfg={})
    assert "abstract content" in out["text"]
    assert "noise nav" not in out["text"]
