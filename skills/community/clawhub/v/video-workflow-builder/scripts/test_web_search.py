import json
import urllib.error

import web_search as ws


class _FakeResp:
    def __init__(self, payload):
        self._data = json.dumps(payload).encode("utf-8")

    def read(self):
        return self._data

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


def _ok_payload(titles):
    return {"request_id": "req-1", "references": [
        {"title": t, "url": "https://example.com/%s" % t,
         "snippet": "snip-%s" % t, "content": "body-%s" % t,
         "date": "2026-07-29", "website": "示例站"}
        for t in titles]}


def _ok_image_payload(titles):
    return {"request_id": "img-1", "references": [
        {"title": t, "type": "image", "url": "https://page.com/%s" % t,
         "website": "图站",
         "image": {"url": "https://img.com/%s.jpg" % t,
                   "width": "1080", "height": "1920"}}
        for t in titles]}


class _FakeHeaders:
    def __init__(self, charset):
        self._cs = charset

    def get_content_charset(self):
        return self._cs


class _FakeHtmlResp:
    def __init__(self, html, charset="utf-8"):
        self._data = html.encode(charset)
        self.headers = _FakeHeaders(charset)

    def read(self):
        return self._data

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


def test_search_success(monkeypatch):
    monkeypatch.setenv("QIANFAN_WEBSEARCH_API_KEY", "bsk-test")
    monkeypatch.setenv("QIANFAN_WEBSEARCH_API_BASE", "https://test-gw/v2/ai_search/web_search")
    monkeypatch.setattr(ws.urllib.request, "urlopen",
                        lambda req, timeout=20: _FakeResp(_ok_payload(["A", "B", "C"])))
    results = ws.search("q", top=2)
    assert [r["title"] for r in results] == ["A", "B", "C"]
    assert results[0]["url"] == "https://example.com/A"
    assert results[0]["snippet"] == "snip-A"


def test_search_images_success(monkeypatch):
    monkeypatch.setenv("QIANFAN_WEBSEARCH_API_KEY", "bsk-test")
    monkeypatch.setenv("QIANFAN_WEBSEARCH_API_BASE", "https://test-gw/v2/ai_search/web_search")
    monkeypatch.setattr(ws.urllib.request, "urlopen",
                        lambda req, timeout=20: _FakeResp(_ok_image_payload(["A", "B"])))
    results = ws.search_images("q", top=2)
    assert [r["title"] for r in results] == ["A", "B"]
    assert results[0]["image_url"] == "https://img.com/A.jpg"
    assert results[0]["source_url"] == "https://page.com/A"
    assert (results[0]["width"], results[0]["height"]) == ("1080", "1920")


def test_search_images_missing_image_field(monkeypatch):
    # 网关某条结果没有 image 子对象时不应崩，字段降级为空串
    monkeypatch.setenv("QIANFAN_WEBSEARCH_API_KEY", "bsk-test")
    monkeypatch.setenv("QIANFAN_WEBSEARCH_API_BASE", "https://test-gw/v2/ai_search/web_search")
    payload = {"request_id": "x", "references": [{"title": "no-img", "url": "u"}]}
    monkeypatch.setattr(ws.urllib.request, "urlopen",
                        lambda req, timeout=20: _FakeResp(payload))
    results = ws.search_images("q")
    assert results[0]["image_url"] == ""
    assert results[0]["title"] == "no-img"


_SAMPLE_HTML = (
    "<html><head><title>  英伟达财报  </title></head><body>"
    "<script>var x=1;</script>"
    "<nav>导航 无关</nav>"
    "<p>第一段：<b>营收</b>大涨。</p>"
    "<p>  第二段：净利润创纪录。  </p>"
    "<style>.a{color:red}</style>"
    "<p></p>"
    "</body></html>")


def test_fetch_page_extracts_text(monkeypatch):
    monkeypatch.setattr(ws.urllib.request, "urlopen",
                        lambda req, timeout=20: _FakeHtmlResp(_SAMPLE_HTML))
    page = ws.fetch_page("https://example.com/a")
    assert page["title"] == "英伟达财报"
    # script/style/nav 被剥掉，只剩两段正文
    assert page["text"] == "第一段：营收大涨。\n\n第二段：净利润创纪录。"
    assert page["chars"] == len(page["text"])
    assert "var x" not in page["text"]
    assert "导航" not in page["text"]


def test_fetch_page_truncates(monkeypatch):
    monkeypatch.setattr(ws.urllib.request, "urlopen",
                        lambda req, timeout=20: _FakeHtmlResp(_SAMPLE_HTML))
    page = ws.fetch_page("https://example.com/a", max_chars=5)
    assert page["text"].startswith("第一段：营")
    assert "已截断" in page["text"]
    assert page["chars"] == 5


def test_fetch_page_empty_body_raises(monkeypatch):
    # 抓到页面但没正文时报错，不返回空正文冒充抓到
    html = "<html><head><title>t</title></head><body><script>x</script></body></html>"
    monkeypatch.setattr(ws.urllib.request, "urlopen",
                        lambda req, timeout=20: _FakeHtmlResp(html))
    try:
        ws.fetch_page("https://example.com/a")
        assert False, "无正文时应抛错"
    except RuntimeError as e:
        assert "正文" in str(e)


def test_fetch_page_no_p_falls_back(monkeypatch):
    # 没有 <p> 时退化为整页去标签，不返回空
    html = "<html><body><div>正文直接放在 div 里</div></body></html>"
    monkeypatch.setattr(ws.urllib.request, "urlopen",
                        lambda req, timeout=20: _FakeHtmlResp(html))
    page = ws.fetch_page("https://example.com/a")
    assert "正文直接放在 div 里" in page["text"]


def test_missing_key_raises(monkeypatch):
    # 铁律：没配密钥必须报错，不能静默降级
    monkeypatch.delenv("QIANFAN_WEBSEARCH_API_KEY", raising=False)
    monkeypatch.setattr(ws, "_load_api_key", lambda: None)
    try:
        ws.search("q")
        assert False, "缺密钥时应抛错"
    except RuntimeError as e:
        assert "QIANFAN_WEBSEARCH_API_KEY" in str(e)


def test_network_failure_propagates_not_stale(monkeypatch):
    # 铁律：搜不到就抛错，绝不返回空结果/旧数据
    monkeypatch.setenv("QIANFAN_WEBSEARCH_API_KEY", "bsk-test")
    monkeypatch.setenv("QIANFAN_WEBSEARCH_API_BASE", "https://test-gw/v2/ai_search/web_search")

    def _boom(req, timeout=20):
        raise urllib.error.URLError("connection refused")

    monkeypatch.setattr(ws.urllib.request, "urlopen", _boom)
    try:
        ws.search("q")
        assert False, "网络失败时应抛错，不得返回空结果"
    except urllib.error.URLError:
        pass


def test_bad_payload_raises(monkeypatch):
    monkeypatch.setenv("QIANFAN_WEBSEARCH_API_KEY", "bsk-test")
    monkeypatch.setenv("QIANFAN_WEBSEARCH_API_BASE", "https://test-gw/v2/ai_search/web_search")
    monkeypatch.setattr(ws.urllib.request, "urlopen",
                        lambda req, timeout=20: _FakeResp({"request_id": "x"}))
    try:
        ws.search("q")
        assert False, "网关无 references 时应抛错"
    except RuntimeError:
        pass


def test_main_network_failure_returns_1(monkeypatch, capsys):
    monkeypatch.setenv("QIANFAN_WEBSEARCH_API_KEY", "bsk-test")
    monkeypatch.setenv("QIANFAN_WEBSEARCH_API_BASE", "https://test-gw/v2/ai_search/web_search")

    def _boom(req, timeout=20):
        raise urllib.error.URLError("down")

    monkeypatch.setattr(ws.urllib.request, "urlopen", _boom)
    rc = ws.main(["q"])
    assert rc == 1
    assert "不返回缓存" in capsys.readouterr().err
