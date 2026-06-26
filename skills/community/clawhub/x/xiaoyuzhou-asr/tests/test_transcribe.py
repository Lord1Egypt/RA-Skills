#!/usr/bin/env python3
"""Unit tests for transcribe_podcast.py (no external dependencies)."""

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from transcribe_podcast import (
    ApiError,
    AudioError,
    DependencyError,
    FORMATTERS,
    TokenExpiredError,
    TranscriptionError,
    _detect_asr_bin,
    _detect_model_dir,
    _ensure_local_proxy_bypass,
    episode_file_stem,
    extract_episode_id_from_url,
    stitch_segments,
    check_env,
    format_output,
    format_json,
    format_srt,
    format_txt,
    get_all_episodes,
    get_episode_list,
    get_episode_detail,
    get_podcast_detail,
    load_config,
    output_extension,
    read_json_response,
    resolve_setting,
    run_transcription,
    sanitize_filename,
    save_config,
    search_all_episodes,
    search_all_podcasts,
    search_episodes,
    search_podcasts,
    transcribe_segments,
    validate_asr_environment,
)


MOCK_EPISODE = {
    "title": "测试单集标题",
    "eid": "test123",
    "podcast": {"title": "测试播客"},
    "pubDate": "2026-05-05T10:00:00Z",
    "duration": 3661,
    "playCount": 1000,
    "media": {"source": {"url": "https://example.com/audio.m4a"}, "size": 10485760},
}


class TestExceptionHierarchy(unittest.TestCase):
    def test_base_exception(self):
        with self.assertRaises(TranscriptionError):
            raise TranscriptionError("test")

    def test_api_error(self):
        with self.assertRaises(ApiError):
            raise ApiError("test", status_code=500)

    def test_token_expired_is_api_error(self):
        with self.assertRaises(ApiError):
            raise TokenExpiredError("expired", status_code=401)

    def test_dependency_error(self):
        with self.assertRaises(TranscriptionError):
            raise DependencyError("missing")

    def test_audio_error(self):
        with self.assertRaises(TranscriptionError):
            raise AudioError("failed")


class TestFormatMarkdown(unittest.TestCase):
    def test_basic_format(self):
        result = format_output(MOCK_EPISODE, "转录文本内容")
        self.assertIn("# 测试单集标题", result)
        self.assertIn("**节目**: 测试播客", result)
        self.assertIn("**日期**: 2026-05-05", result)
        self.assertIn("**时长**: 61分1秒", result)
        self.assertIn("**播放量**: 1,000", result)
        self.assertIn("## 转录文本", result)
        self.assertIn("转录文本内容", result)

    def test_no_play_count(self):
        ep = {**MOCK_EPISODE, "playCount": 0}
        result = format_output(ep, "text")
        self.assertNotIn("播放量", result)

    def test_missing_fields(self):
        result = format_output({}, "text")
        self.assertIn("未知标题", result)
        self.assertIn("未知节目", result)


class TestFormatSrt(unittest.TestCase):
    def test_basic_srt(self):
        result = format_srt(MOCK_EPISODE, "第一句话。第二句话。第三句话。")
        self.assertIn("-->", result)
        self.assertIn("第一句话", result)
        # Should have 3 numbered entries
        self.assertTrue(result.startswith("1\n"))
        self.assertIn("\n\n2\n", result)
        self.assertIn("\n\n3\n", result)

    def test_srt_with_segment_timings(self):
        timings = [
            ("第一句。第二句。", 0.0, 120.0),
            ("第三句。", 120.0, 300.0),
        ]
        result = format_srt({"duration": 300}, "unused", timings)
        # Should have 3 entries
        self.assertTrue(result.startswith("1\n"))
        self.assertIn("\n\n2\n", result)
        self.assertIn("\n\n3\n", result)
        # First sentence starts at 0
        self.assertIn("00:00:00,000", result)
        # Third sentence starts at 120s
        self.assertIn("00:02:00", result)

    def test_empty_transcript(self):
        result = format_srt({"duration": 120}, "")
        self.assertIn("-->", result)

    def test_zero_duration(self):
        result = format_srt({"duration": 0}, "一些文字。")
        self.assertIn("一些文字", result)


class TestFormatTxt(unittest.TestCase):
    def test_basic_txt(self):
        result = format_txt(MOCK_EPISODE, "转录内容")
        self.assertEqual(result.split("\n\n")[0], "测试单集标题 | 测试播客 | 2026-05-05")
        self.assertIn("转录内容", result)

    def test_no_podcast(self):
        result = format_txt({"title": "T"}, "text")
        self.assertTrue(result.startswith("T"))


class TestFormattersRegistry(unittest.TestCase):
    def test_all_formats_registered(self):
        self.assertEqual(set(FORMATTERS.keys()), {"markdown", "srt", "txt", "json"})

    def test_each_formatter_callable(self):
        for name, fn in FORMATTERS.items():
            result = fn(MOCK_EPISODE, "test text")
            self.assertIsInstance(result, str, f"Formatter {name} did not return str")

    def test_output_extensions(self):
        self.assertEqual(output_extension("markdown"), "md")
        self.assertEqual(output_extension("srt"), "srt")
        self.assertEqual(output_extension("txt"), "txt")
        self.assertEqual(output_extension("json"), "json")
        self.assertEqual(output_extension("unknown"), "txt")


class TestFormatJson(unittest.TestCase):
    def test_json_output(self):
        result = format_json(MOCK_EPISODE, "转录内容")
        parsed = json.loads(result)
        self.assertEqual(parsed["title"], "测试单集标题")
        self.assertEqual(parsed["podcast"], "测试播客")
        self.assertEqual(parsed["date"], "2026-05-05")
        self.assertEqual(parsed["duration"], 3661)
        self.assertEqual(parsed["transcript"], "转录内容")

    def test_json_missing_fields(self):
        result = format_json({}, "text")
        parsed = json.loads(result)
        self.assertEqual(parsed["title"], "")


class TestProxyBypass(unittest.TestCase):
    def test_local_xyz_base_url_adds_no_proxy_entries(self):
        with patch.dict(os.environ, {"HTTP_PROXY": "http://127.0.0.1:8001"}, clear=True):
            _ensure_local_proxy_bypass("http://localhost:23020")
            no_proxy = os.environ.get("NO_PROXY", "")
        self.assertIn("localhost", no_proxy)
        self.assertIn("127.0.0.1", no_proxy)

    def test_remote_base_url_keeps_existing_proxy_config(self):
        with patch.dict(os.environ, {"NO_PROXY": "example.com"}, clear=True):
            _ensure_local_proxy_bypass("https://api.example.com")
            self.assertEqual(os.environ.get("NO_PROXY"), "example.com")


class TestPathDetection(unittest.TestCase):
    def test_model_dir_env_override(self):
        with patch.dict(os.environ, {"QWEN3_ASR_MODEL_DIR": "/fake/path"}):
            with patch.object(Path, "exists", return_value=True):
                self.assertEqual(_detect_model_dir(), "/fake/path")

    def test_asr_bin_env_override(self):
        with patch.dict(os.environ, {"QWEN3_ASR_BIN": "/fake/bin"}):
            with patch.object(Path, "exists", return_value=True):
                self.assertEqual(_detect_asr_bin(), "/fake/bin")


class TestApiFunctions(unittest.TestCase):
    @patch("transcribe_podcast.api")
    def test_search_episodes(self, mock_api):
        mock_api.return_value = {
            "data": {"data": [
                {"type": "EPISODE", "eid": "1", "title": "Ep1"},
                {"type": "PODCAST", "pid": "p1"},
                {"type": "EPISODE", "eid": "2", "title": "Ep2"},
            ], "loadMoreKey": {"loadMoreKey": 20, "searchId": "123"}}
        }
        episodes, next_key = search_episodes("token", "test", limit=2)
        self.assertEqual(len(episodes), 2)
        self.assertEqual(episodes[0]["eid"], "1")
        self.assertIsNotNone(next_key)

    @patch("transcribe_podcast.api")
    def test_get_episode_detail(self, mock_api):
        mock_api.return_value = {"data": {"data": {"eid": "abc", "title": "Test"}}}
        result = get_episode_detail("token", "abc")
        self.assertEqual(result["title"], "Test")

    @patch("transcribe_podcast.api")
    def test_get_episode_list(self, mock_api):
        mock_api.return_value = {"data": {"data": [
            {"eid": "1"}, {"eid": "2"}, {"eid": "3"},
        ], "loadMoreKey": {"direction": "NEXT", "id": "abc", "pubDate": "2026-01-01"}}}
        episodes, next_key = get_episode_list("token", "pid", count=2)
        self.assertEqual(len(episodes), 2)
        self.assertIsNotNone(next_key)


class TestCheckEnv(unittest.TestCase):
    @patch("urllib.request.urlopen")
    @patch("transcribe_podcast.shutil.which")
    @patch("transcribe_podcast.Path.exists")
    def test_check_env_all_missing(self, mock_exists, mock_which, mock_urlopen):
        import urllib.error

        mock_which.return_value = None
        mock_exists.return_value = False
        mock_urlopen.side_effect = urllib.error.URLError("refused")
        result = check_env(None)
        self.assertFalse(result)

    @patch("transcribe_podcast.api")
    @patch("urllib.request.urlopen")
    @patch("transcribe_podcast.shutil.which")
    @patch("transcribe_podcast._detect_asr_bin", return_value="/bin/local_transcribe")
    @patch("transcribe_podcast._detect_model_dir", return_value="/model")
    def test_check_env_treats_root_404_as_running(
        self, _mock_model_dir, _mock_asr_bin, mock_which, mock_urlopen, mock_api
    ):
        import urllib.error

        mock_which.return_value = "/bin/ffmpeg"
        mock_urlopen.side_effect = urllib.error.HTTPError(
            url="http://localhost:23020/", code=404, msg="Not Found", hdrs=None, fp=None
        )
        mock_api.return_value = {"data": {"data": []}}
        with patch("transcribe_podcast.Path.exists", return_value=True):
            with patch("transcribe_podcast.Path.glob", return_value=[Path("model.safetensors")]):
                result = check_env("token")
        self.assertTrue(result)


class TestSanitizeFilename(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(sanitize_filename("hello world"), "hello world")

    def test_special_chars(self):
        result = sanitize_filename("a/b:c|d")
        self.assertNotIn("/", result)
        self.assertNotIn(":", result)
        self.assertNotIn("|", result)

    def test_empty(self):
        self.assertEqual(sanitize_filename(""), "untitled")

    def test_truncation(self):
        long_title = "x" * 200
        result = sanitize_filename(long_title, max_len=50)
        self.assertLessEqual(len(result), 50)

    def test_chinese(self):
        result = sanitize_filename("中文标题测试")
        self.assertEqual(result, "中文标题测试")

    def test_strip_whitespace(self):
        self.assertEqual(sanitize_filename("  spaces  "), "spaces")


class TestEpisodeFileStem(unittest.TestCase):
    def test_includes_date_title_and_eid(self):
        result = episode_file_stem(MOCK_EPISODE)
        self.assertIn("2026-05-05", result)
        self.assertIn("测试单集标题", result)
        self.assertIn("test123", result)

    def test_same_title_different_eids_do_not_collide(self):
        ep1 = {"title": "同名标题", "eid": "eid-a", "pubDate": "2026-01-01T00:00:00Z"}
        ep2 = {"title": "同名标题", "eid": "eid-b", "pubDate": "2026-01-01T00:00:00Z"}
        self.assertNotEqual(episode_file_stem(ep1), episode_file_stem(ep2))


class TestEpisodeUrlParsing(unittest.TestCase):
    def test_extract_from_episode_path(self):
        url = "https://www.xiaoyuzhoufm.com/episode/abc123"
        self.assertEqual(extract_episode_id_from_url(url), "abc123")

    def test_extract_from_query(self):
        url = "https://www.xiaoyuzhoufm.com/episode?eid=abc123"
        self.assertEqual(extract_episode_id_from_url(url), "abc123")

    def test_rejects_unsupported_domain(self):
        with self.assertRaises(TranscriptionError):
            extract_episode_id_from_url("https://example.com/episode/abc123")


class TestNewApiFunctions(unittest.TestCase):
    @patch("transcribe_podcast.api")
    def test_search_podcasts(self, mock_api):
        mock_api.return_value = {
            "data": {"data": [
                {"type": "PODCAST", "pid": "p1", "title": "Pod1"},
                {"type": "EPISODE", "eid": "e1"},
            ], "loadMoreKey": None}
        }
        podcasts, next_key = search_podcasts("token", "test")
        self.assertEqual(len(podcasts), 1)
        self.assertEqual(podcasts[0]["pid"], "p1")
        self.assertIsNone(next_key)

    @patch("transcribe_podcast.api")
    def test_get_podcast_detail(self, mock_api):
        mock_api.return_value = {"data": {"data": {"pid": "abc", "title": "Podcast"}}}
        result = get_podcast_detail("token", "abc")
        self.assertEqual(result["title"], "Podcast")


class FakeResponse:
    def __init__(self, body: bytes, status: int = 200):
        self._body = body
        self.status = status

    def read(self):
        return self._body


class TestReadJsonResponse(unittest.TestCase):
    def test_valid_json_object(self):
        result = read_json_response(FakeResponse(b'{"ok": true}'), "测试")
        self.assertEqual(result, {"ok": True})

    def test_empty_body_raises_api_error(self):
        with self.assertRaises(ApiError) as ctx:
            read_json_response(FakeResponse(b'', status=200), "登录")
        self.assertIn("响应为空", str(ctx.exception))

    def test_non_json_body_raises_api_error(self):
        with self.assertRaises(ApiError) as ctx:
            read_json_response(FakeResponse(b'not json', status=200), "登录")
        self.assertIn("非 JSON", str(ctx.exception))


class TestConfigFile(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.config_path = Path(self.tmpdir) / "test-config.json"

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    @patch("transcribe_podcast.CONFIG_PATH")
    def test_load_nonexistent(self, mock_path):
        mock_path.__str__ = lambda s: "/nonexistent/path.json"
        mock_path.exists.return_value = False
        config = load_config()
        self.assertEqual(config, {})

    @patch("transcribe_podcast.CONFIG_PATH")
    def test_save_and_load(self, mock_path):
        mock_path.__str__ = lambda s: str(self.config_path)
        mock_path.exists.return_value = True
        mock_path.write_text = lambda data, encoding: self.config_path.write_text(data, encoding=encoding)
        mock_path.read_text = lambda encoding: self.config_path.read_text(encoding=encoding)

        save_config({"token": "test123", "model_dir": "/tmp/models"})
        config = load_config()
        self.assertEqual(config["token"], "test123")
        self.assertEqual(config["model_dir"], "/tmp/models")

    def test_resolve_setting_cli_wins(self):
        with patch.dict(os.environ, {"TEST_VAR": "env_val"}):
            result = resolve_setting("cli_val", "TEST_VAR", "key")
            self.assertEqual(result, "cli_val")

    def test_resolve_setting_env_fallback(self):
        with patch.dict(os.environ, {"TEST_VAR": "env_val"}):
            result = resolve_setting(None, "TEST_VAR", "key")
            self.assertEqual(result, "env_val")

    @patch("transcribe_podcast.load_config")
    def test_resolve_setting_config_fallback(self, mock_config):
        mock_config.return_value = {"my_key": "config_val"}
        result = resolve_setting(None, "NONEXISTENT_VAR", "my_key")
        self.assertEqual(result, "config_val")

    def test_resolve_setting_none(self):
        result = resolve_setting(None, "NONEXISTENT_VAR", "missing_key")
        self.assertIsNone(result)

    def test_save_config_locks_down_permissions(self):
        with patch("transcribe_podcast.CONFIG_PATH", self.config_path):
            with patch("transcribe_podcast.os.chmod") as mock_chmod:
                save_config({"token": "secret"})
        mock_chmod.assert_called_once_with(self.config_path, 0o600)


class TestStitchSegments(unittest.TestCase):
    def test_single_segment(self):
        self.assertEqual(stitch_segments(["完整句子。"]), "完整句子。")

    def test_empty(self):
        self.assertEqual(stitch_segments([]), "")

    def test_merge_cut_sentence(self):
        result = stitch_segments([
            "领跑汽车的董事长在车展",
            "他们计划将海外销量的占比提升到四成。",
        ])
        self.assertIn("车展他们计划", result)
        self.assertNotIn("车展\n\n他们", result)

    def test_keep_complete_sentences(self):
        result = stitch_segments([
            "第一段完整句子。",
            "第二段完整句子。",
        ])
        self.assertEqual(result, "第一段完整句子。\n\n第二段完整句子。")

    def test_mixed_boundaries(self):
        result = stitch_segments([
            "完整段落。接下来被切断",
            "的部分继续。新的完整句。",
            "最后一段。",
        ])
        self.assertIn("切断的部分继续", result)
        self.assertIn("完整句。\n\n最后一段", result)

    def test_exclamation_mark_is_boundary(self):
        result = stitch_segments(["太好了！", "新的内容"])
        self.assertIn("太好了！\n\n新的内容", result)


class TestTranscribeSegments(unittest.TestCase):
    @patch("transcribe_podcast.get_duration_sec", return_value=10.0)
    @patch("transcribe_podcast.transcribe_segment", side_effect=["", "第二句。"])
    def test_empty_segment_still_advances_timing(self, _mock_transcribe, _mock_duration):
        segments = [Path("seg_000.wav"), Path("seg_001.wav")]
        transcript, timings = transcribe_segments(segments, "/model", "/bin")
        self.assertEqual(transcript, "第二句。")
        self.assertEqual(timings, [("第二句。", 10.0, 20.0)])


class TestValidateAsrEnvironment(unittest.TestCase):
    def test_valid_environment(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            model = root / "model"
            model.mkdir()
            for name in ["config.json", "vocab.json", "merges.txt", "tokenizer_config.json"]:
                (model / name).write_text("{}", encoding="utf-8")
            (model / "model.safetensors").write_text("weights", encoding="utf-8")
            asr_bin = root / "local_transcribe"
            asr_bin.write_text("#!/bin/sh\n", encoding="utf-8")
            validate_asr_environment(str(model), str(asr_bin))

    def test_missing_asr_binary_fails_before_download(self):
        with tempfile.TemporaryDirectory() as tmp:
            model = Path(tmp) / "model"
            model.mkdir()
            with self.assertRaises(DependencyError):
                validate_asr_environment(str(model), str(Path(tmp) / "missing"))


class TestRunTranscription(unittest.TestCase):
    @patch("transcribe_podcast.transcribe_episode")
    def test_url_mode_extracts_eid(self, mock_transcribe):
        mock_transcribe.return_value = (MOCK_EPISODE, "转录文本", [])
        args = type("Args", (), {
            "token": "token",
            "model_dir": "/model",
            "asr_bin": "/bin",
            "format": "markdown",
            "pid": None,
            "count": 3,
            "output": None,
            "keep_audio": False,
            "eid": None,
            "url": "https://www.xiaoyuzhoufm.com/episode/abc123",
            "keyword": None,
        })()
        output = run_transcription(args)
        self.assertIn("转录文本", output)
        mock_transcribe.assert_called_once_with("token", "abc123", "/model", "/bin", False)


if __name__ == "__main__":
    unittest.main()
