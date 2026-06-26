"""seedance.py 单元测试。

不打真实 API（成本太高），用 monkeypatch 替换 urllib.request.urlopen。
"""

import io
import json
import sys
import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from content_engine import seedance
from content_engine.seedance import (
    SeedanceError,
    TaskFailed,
    TaskTimeout,
    download_video,
    estimate_cost_usd,
    extract_video_url,
    poll_task,
    query_task,
    submit_and_wait,
    submit_task,
)


class _FakeResponse:
    """模仿 urllib HTTPResponse 的 read() 接口。"""

    def __init__(self, body: bytes):
        self._body = body

    def read(self) -> bytes:
        return self._body

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass


def _make_urlopen(responses: list):
    """把一串 dict / bytes 包成 urlopen 顺序返回。"""
    iterator = iter(responses)

    def fake_urlopen(req, timeout=None):
        item = next(iterator)
        if isinstance(item, Exception):
            raise item
        if isinstance(item, dict):
            return _FakeResponse(json.dumps(item).encode("utf-8"))
        if isinstance(item, bytes):
            return _FakeResponse(item)
        raise TypeError(f"unsupported response type: {type(item)}")

    return fake_urlopen


@contextmanager
def _patch_urlopen(responses):
    """便捷 with 块。"""
    with mock.patch.object(
        seedance.urllib.request, "urlopen", side_effect=_make_urlopen(responses),
    ):
        yield


# ─── estimate_cost ───

class TestEstimateCost(unittest.TestCase):

    def test_default_5_shot_5s(self):
        self.assertAlmostEqual(estimate_cost_usd(5, 5), 1.0)

    def test_single_shot(self):
        self.assertGreater(estimate_cost_usd(1), 0)


# ─── submit_task ───

class TestSubmitTask(unittest.TestCase):

    def test_submit_returns_task_id(self):
        with _patch_urlopen([{"id": "cgt-fake-001"}]):
            task_id = submit_task("test prompt", api_key="fake-key")
        self.assertEqual(task_id, "cgt-fake-001")

    def test_submit_missing_id_raises(self):
        with _patch_urlopen([{"foo": "bar"}]):
            with self.assertRaises(SeedanceError) as cm:
                submit_task("test prompt", api_key="fake-key")
        self.assertIn("missing 'id'", str(cm.exception))

    def test_submit_no_key_raises(self):
        # 临时清空 env / .env 加载（用空字符串 api_key 不行因为有 fallback；用 _load_ark_key mock）
        with mock.patch.object(seedance, "_load_ark_key", return_value=None):
            with self.assertRaises(SeedanceError) as cm:
                submit_task("test prompt")
        self.assertIn("ARK_API_KEY", str(cm.exception))

    def test_submit_http_error(self):
        import urllib.error
        err = urllib.error.HTTPError(
            url="https://x", code=401, msg="Unauthorized", hdrs={},
            fp=io.BytesIO(b'{"error": "invalid token"}'),
        )
        with _patch_urlopen([err]):
            with self.assertRaises(SeedanceError) as cm:
                submit_task("test prompt", api_key="fake-key")
        self.assertEqual(cm.exception.status, 401)


# ─── query_task ───

class TestQueryTask(unittest.TestCase):

    def test_query_returns_full_response(self):
        body = {"id": "cgt-001", "status": "running"}
        with _patch_urlopen([body]):
            result = query_task("cgt-001", api_key="fake-key")
        self.assertEqual(result["status"], "running")


# ─── poll_task ───

class TestPollTask(unittest.TestCase):

    def test_poll_succeeds_after_running(self):
        responses = [
            {"id": "x", "status": "queued"},
            {"id": "x", "status": "running"},
            {"id": "x", "status": "succeeded", "content": {"video_url": "https://cdn/x.mp4"}},
        ]
        with _patch_urlopen(responses):
            with mock.patch.object(seedance.time, "sleep"):  # 加速
                result = poll_task("x", api_key="fake-key", poll_interval=0)
        self.assertEqual(result["status"], "succeeded")
        self.assertEqual(extract_video_url(result), "https://cdn/x.mp4")

    def test_poll_raises_on_failed(self):
        responses = [
            {"id": "x", "status": "running"},
            {"id": "x", "status": "failed", "error": {"message": "nsfw content blocked"}},
        ]
        with _patch_urlopen(responses):
            with mock.patch.object(seedance.time, "sleep"):
                with self.assertRaises(TaskFailed) as cm:
                    poll_task("x", api_key="fake-key", poll_interval=0)
        self.assertIn("nsfw", str(cm.exception))

    def test_poll_raises_on_expired(self):
        with _patch_urlopen([{"id": "x", "status": "expired"}]):
            with self.assertRaises(TaskFailed):
                poll_task("x", api_key="fake-key", poll_interval=0)

    def test_poll_raises_on_cancelled(self):
        with _patch_urlopen([{"id": "x", "status": "cancelled"}]):
            with self.assertRaises(TaskFailed):
                poll_task("x", api_key="fake-key", poll_interval=0)

    def test_poll_timeout(self):
        # 持续返回 running，且 timeout=0 → 应立即超时
        with _patch_urlopen([{"id": "x", "status": "running"}]):
            with self.assertRaises(TaskTimeout):
                poll_task("x", api_key="fake-key", timeout=0, poll_interval=0)

    def test_poll_progress_callback(self):
        responses = [
            {"id": "x", "status": "running"},
            {"id": "x", "status": "succeeded", "content": {"video_url": "u"}},
        ]
        seen = []
        with _patch_urlopen(responses):
            with mock.patch.object(seedance.time, "sleep"):
                poll_task(
                    "x", api_key="fake-key", poll_interval=0,
                    on_progress=lambda s, e: seen.append(s),
                )
        self.assertEqual(seen, ["running", "succeeded"])


# ─── download_video ───

class TestDownloadVideo(unittest.TestCase):

    def test_download_writes_file(self):
        with _patch_urlopen([b"\x00\x00\x00\x18ftypmp42fake video bytes"]):
            with tempfile.TemporaryDirectory() as tmp:
                out = Path(tmp) / "x.mp4"
                download_video("https://cdn/x.mp4", out)
                self.assertTrue(out.exists())
                self.assertGreater(out.stat().st_size, 0)


# ─── submit_and_wait（端到端编排）───

class TestSubmitAndWait(unittest.TestCase):

    def test_full_happy_path(self):
        responses = [
            {"id": "cgt-007"},                                                       # submit
            {"id": "cgt-007", "status": "running"},                                  # poll 1
            {"id": "cgt-007", "status": "succeeded", "content": {"video_url": "https://cdn/v.mp4"}},  # poll 2
            b"VIDEOBYTES" * 100,                                                     # download
        ]
        with _patch_urlopen(responses), \
             mock.patch.object(seedance.time, "sleep"), \
             tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "shot.mp4"
            result_path, task_id = submit_and_wait(
                "test prompt", out, api_key="fake-key", poll_interval=0,
            )
            self.assertEqual(task_id, "cgt-007")
            self.assertTrue(result_path.exists())
            self.assertEqual(result_path.read_bytes(), b"VIDEOBYTES" * 100)

    def test_succeeded_but_no_video_url_raises(self):
        responses = [
            {"id": "cgt-008"},
            {"id": "cgt-008", "status": "succeeded", "content": {}},
        ]
        with _patch_urlopen(responses), \
             mock.patch.object(seedance.time, "sleep"), \
             tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "shot.mp4"
            with self.assertRaises(SeedanceError) as cm:
                submit_and_wait("p", out, api_key="fake-key", poll_interval=0)
            self.assertIn("no video_url", str(cm.exception))


# ─── extract_video_url ───

class TestExtractVideoUrl(unittest.TestCase):

    def test_nested_content(self):
        self.assertEqual(
            extract_video_url({"content": {"video_url": "u"}}), "u",
        )

    def test_top_level_fallback(self):
        self.assertEqual(extract_video_url({"video_url": "u2"}), "u2")

    def test_missing_returns_none(self):
        self.assertIsNone(extract_video_url({"status": "running"}))


if __name__ == "__main__":
    unittest.main()
