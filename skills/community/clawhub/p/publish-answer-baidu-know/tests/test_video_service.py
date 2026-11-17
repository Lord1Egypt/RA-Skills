# -*- coding: utf-8 -*-
"""RpaVideoSession 模板示范与 result_summary / CLI 输出测试。"""
from __future__ import annotations

import io
import json
import os
import re
import unittest
from contextlib import redirect_stderr, redirect_stdout
from unittest.mock import AsyncMock, MagicMock, patch

from _support import IsolatedDataRoot, get_skill_root

from jiangchang_skill_core import config


class TestEnvExampleVideoDefaults(unittest.TestCase):
    def test_env_example_contains_required_keys(self) -> None:
        path = os.path.join(get_skill_root(), ".env.example")
        with open(path, encoding="utf-8") as f:
            text = f.read()
        for key in (
            "OPENCLAW_TEST_TARGET=mock",
            "OPENCLAW_RECORD_VIDEO=1",
            "OPENCLAW_ARTIFACTS_ON_FAILURE=1",
            "OPENCLAW_BROWSER_HEADLESS=0",
            "OPENCLAW_PLAYWRIGHT_STEALTH=1",
        ):
            self.assertIn(key, text, msg=f"missing {key!r} in .env.example")


class TestPrintVideoSummary(unittest.TestCase):
    def test_cli_prints_video_path_when_enabled(self) -> None:
        from service.task_run_support import _print_video_summary

        buf = io.StringIO()
        with redirect_stdout(buf), redirect_stderr(io.StringIO()):
            _print_video_summary(
                {
                    "enabled": True,
                    "path": r"D:\data\videos\your-skill-slug_demo.mp4",
                    "record_log_path": r"D:\data\logs\ffmpeg-record.log",
                    "warnings": [],
                }
            )
        out = buf.getvalue()
        self.assertIn("录屏路径", out)
        self.assertIn("your-skill-slug_demo.mp4", out)
        self.assertIn("录屏日志", out)

    def test_disabled_video_prints_nothing(self) -> None:
        from service.task_run_support import _print_video_summary

        buf = io.StringIO()
        with redirect_stdout(buf), redirect_stderr(io.StringIO()):
            _print_video_summary({"enabled": False, "path": r"D:\tmp\x.mp4"})
        self.assertEqual(buf.getvalue(), "")


class TestMergeVideoIntoResultSummary(unittest.TestCase):
    def test_result_summary_includes_video_fields(self) -> None:
        from service.task_run_support import merge_video_into_result_summary

        video_info = {
            "enabled": True,
            "path": r"D:\data\videos\demo.mp4",
            "capture_path": r"D:\data\capture.mp4",
            "record_log_path": r"D:\data\logs\ffmpeg-record.log",
            "warnings": ["test_warning"],
            "voiceover_path": r"D:\data\voiceover.wav",
            "music_path": r"D:\data\music.mp3",
            "audio_warnings": ["tts_skipped"],
        }
        payload = merge_video_into_result_summary({"demo": True}, video_info)
        self.assertIn("video", payload)
        self.assertEqual(payload["video_path"], video_info["path"])
        self.assertEqual(payload["raw_video"], video_info["capture_path"])
        self.assertEqual(payload["video_log"], video_info["record_log_path"])
        self.assertEqual(payload["video_warnings"], ["test_warning"])
        self.assertEqual(payload["voiceover_path"], video_info["voiceover_path"])
        self.assertEqual(payload["music_path"], video_info["music_path"])
        self.assertEqual(payload["audio_warnings"], ["tts_skipped"])


class TestTemplateRunVideoSession(unittest.TestCase):
    def _fake_video_session(self, mock_video: MagicMock):
        class _FakeVideoSession:
            def __init__(self, **kwargs):
                self.kwargs = kwargs

            async def __aenter__(self):
                return mock_video

            async def __aexit__(self, *args):
                return None

        return _FakeVideoSession

    def test_cmd_run_creates_video_session_with_chinese_titles(self) -> None:
        with IsolatedDataRoot(user_id="_video_run"):
            os.environ["OPENCLAW_RECORD_VIDEO"] = "0"
            config.reset_cache()

            from service import task_service

            mock_video = MagicMock()
            mock_video.add_step = MagicMock()
            mock_video.summary.return_value = {
                "enabled": False,
                "path": None,
                "capture_path": None,
                "record_log_path": None,
                "warnings": [],
                "voiceover_path": None,
                "music_path": None,
                "audio_warnings": [],
            }

            created: list[dict] = []

            class _CapturingFakeSession:
                def __init__(self, **kwargs):
                    created.append(kwargs)

                async def __aenter__(self):
                    return mock_video

                async def __aexit__(self, *args):
                    return None

            with patch.object(task_service, "RpaVideoSession", _CapturingFakeSession):
                buf = io.StringIO()
                with redirect_stdout(buf), redirect_stderr(io.StringIO()):
                    rc = task_service.cmd_run(target="demo-target", input_id="42")

            self.assertEqual(rc, 1)
            self.assertTrue(created, "RpaVideoSession should be constructed")
            kwargs = created[0]
            self.assertEqual(kwargs.get("title"), "开始执行示例任务")
            self.assertEqual(kwargs.get("closing_title"), "示例任务执行完成")
            self.assertTrue(re.search(r"[\u4e00-\u9fff]", kwargs.get("title", "")))
            self.assertTrue(re.search(r"[\u4e00-\u9fff]", kwargs.get("closing_title", "")))
            mock_video.add_step.assert_any_call("准备执行示例任务")
            mock_video.add_step.assert_any_call("示例任务执行完成")
            mock_video.summary.assert_called()

            out = buf.getvalue()
            self.assertIn("模板", out)

            from db import task_logs_repository as tlr

            rows = tlr.list_task_logs(1)
            self.assertTrue(rows)
            summary = json.loads(rows[0][7])
            self.assertIn("video", summary)
            self.assertIn("video_path", summary)


if __name__ == "__main__":
    unittest.main()
