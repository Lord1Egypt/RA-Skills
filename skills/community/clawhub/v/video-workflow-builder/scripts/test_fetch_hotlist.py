import io
import json
import urllib.error

import fetch_hotlist as fh


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
    return {"code": 200, "title": "热榜",
            "data": [{"title": t, "hot": 100} for t in titles]}


def test_fetch_success(monkeypatch):
    monkeypatch.setenv("DAILYHOT_API_BASE", "http://localhost:6688")
    monkeypatch.setattr(fh.urllib.request, "urlopen",
                        lambda req, timeout=10: _FakeResp(_ok_payload(["A", "B", "C"])))
    result = fh.fetch(["douyin"], top=2)
    assert list(result) == ["douyin"]
    assert [i["title"] for i in result["douyin"]["items"]] == ["A", "B"]


def test_missing_base_raises(monkeypatch):
    # 铁律：没配数据源必须报错，不能静默降级
    monkeypatch.delenv("DAILYHOT_API_BASE", raising=False)
    monkeypatch.setattr(fh, "_load_api_base", lambda: None)
    try:
        fh.fetch(["douyin"])
        assert False, "缺 base 时应抛错"
    except RuntimeError as e:
        assert "DAILYHOT_API_BASE" in str(e)


def test_network_failure_propagates_not_stale(monkeypatch):
    # 铁律：抓不到就抛错，绝不返回任何旧数据/部分数据
    monkeypatch.setenv("DAILYHOT_API_BASE", "http://localhost:6688")

    def _boom(req, timeout=10):
        raise urllib.error.URLError("connection refused")

    monkeypatch.setattr(fh.urllib.request, "urlopen", _boom)
    try:
        fh.fetch(["douyin"])
        assert False, "网络失败时应抛错，不得返回缓存"
    except urllib.error.URLError:
        pass


def test_bad_code_raises(monkeypatch):
    monkeypatch.setenv("DAILYHOT_API_BASE", "http://localhost:6688")
    monkeypatch.setattr(fh.urllib.request, "urlopen",
                        lambda req, timeout=10: _FakeResp({"code": 500, "data": []}))
    try:
        fh.fetch(["douyin"])
        assert False, "接口返回错误 code 时应抛错"
    except RuntimeError:
        pass


def test_main_network_failure_returns_1(monkeypatch, capsys):
    monkeypatch.setenv("DAILYHOT_API_BASE", "http://localhost:6688")

    def _boom(req, timeout=10):
        raise urllib.error.URLError("down")

    monkeypatch.setattr(fh.urllib.request, "urlopen", _boom)
    rc = fh.main(["--platforms", "douyin"])
    assert rc == 1
    assert "不返回缓存" in capsys.readouterr().err
