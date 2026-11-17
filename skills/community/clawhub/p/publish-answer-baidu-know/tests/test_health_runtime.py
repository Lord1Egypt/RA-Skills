# -*- coding: utf-8 -*-
"""health / runtime 诊断：验证委托 platform-kit 公共 API。"""
from __future__ import annotations

import io
import os
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

from _support import IsolatedDataRoot, get_skill_root, platform_kit_version_patch

import jiangchang_skill_core
from cli.app import main
from jiangchang_skill_core import (
    collect_runtime_diagnostics,
    format_runtime_health_lines,
    is_jiangchang_skill_core_from_skill_tree,
    runtime_diagnostics_dict,
)
from util.config_bootstrap import bootstrap_skill_config
from util.constants import PLATFORM_KIT_MIN_VERSION, SKILL_SLUG
from util.runtime_paths import get_skill_root as skill_root_path


def _collect_diag():
    return collect_runtime_diagnostics(
        skill_slug=SKILL_SLUG,
        platform_kit_min_version=PLATFORM_KIT_MIN_VERSION,
        skill_root=skill_root_path(),
    )


class TestHealthRuntimeDiagnostics(unittest.TestCase):
    def test_collect_runtime_diagnostics_fields(self) -> None:
        with IsolatedDataRoot(user_id="_health_rt"):
            os.environ["OPENCLAW_RECORD_VIDEO"] = "0"
            diag = _collect_diag()
            payload = runtime_diagnostics_dict(diag)
            for key in (
                "skill_slug",
                "python_executable",
                "platform_kit_version",
                "jiangchang_skill_core_file",
                "resolved_data_root",
                "media_assets_root",
                "ffmpeg_available",
                "background_music_mp3_count",
                "runtime_issues",
            ):
                self.assertIn(key, payload)
            self.assertEqual(diag.skill_slug, SKILL_SLUG)
            self.assertEqual(diag.platform_kit_min_version, PLATFORM_KIT_MIN_VERSION)

    def test_format_runtime_health_lines_contains_core_fields(self) -> None:
        diag = _collect_diag()
        text = "\n".join(format_runtime_health_lines(diag))
        self.assertIn("skill_slug:", text)
        self.assertIn("python_executable:", text)
        self.assertIn("platform_kit_version:", text)
        self.assertIn("jiangchang_skill_core_file:", text)
        self.assertIn("media_assets_root:", text)
        self.assertIn("background_music_mp3_count:", text)

    def test_health_cli_prints_runtime_diagnostics(self) -> None:
        with IsolatedDataRoot(user_id="_health_cli"):
            os.environ["OPENCLAW_RECORD_VIDEO"] = "0"
            bootstrap_skill_config()
            buf = io.StringIO()
            with platform_kit_version_patch(), redirect_stdout(buf), redirect_stderr(io.StringIO()):
                rc = main(["health"])
            out = buf.getvalue()
            self.assertEqual(rc, 0, msg=out)
            self.assertIn("python_executable:", out)
            self.assertIn("platform_kit_version:", out)
            self.assertIn("jiangchang_skill_core_file:", out)
            self.assertIn("media_assets_root:", out)
            self.assertIn("background_music_mp3_count:", out)
            self.assertIn("env_path:", out)
            self.assertIn("example_path:", out)

    def test_health_fails_when_platform_kit_missing(self) -> None:
        with IsolatedDataRoot(user_id="_health_no_pkg"):
            os.environ["OPENCLAW_RECORD_VIDEO"] = "0"
            bootstrap_skill_config()
            with patch(
                "jiangchang_skill_core.runtime_diagnostics._platform_kit_version",
                return_value=None,
            ):
                buf = io.StringIO()
                with redirect_stdout(buf), redirect_stderr(io.StringIO()):
                    rc = main(["health"])
            self.assertEqual(rc, 1)
            self.assertIn("platform_kit_not_installed", buf.getvalue())

    def test_background_music_issue_is_warning_not_fatal(self) -> None:
        from jiangchang_skill_core.media_assets import MediaAssetsStatus

        with IsolatedDataRoot(user_id="_health_music_warn"):
            os.environ["OPENCLAW_RECORD_VIDEO"] = "1"
            media_root = Path(os.environ["JIANGCHANG_DATA_ROOT"]) / "shared" / "media-assets"
            ffmpeg_path = media_root / "tools" / "ffmpeg.exe"
            ffmpeg_path.parent.mkdir(parents=True, exist_ok=True)
            ffmpeg_path.write_bytes(b"x" * 256)
            status = MediaAssetsStatus(
                root=media_root,
                exists=True,
                ready=False,
                source="local",
                warnings=["music_dir_missing"],
                ffmpeg_path=ffmpeg_path,
                music_dir=None,
            )
            music_probe = {
                "music_root": None,
                "mp3_count": 0,
                "usable_count": 0,
                "sample_path": None,
                "issue": "music_dir_missing",
            }
            with patch(
                "jiangchang_skill_core.runtime_diagnostics.probe_media_assets",
                return_value=status,
            ), patch(
                "jiangchang_skill_core.runtime_diagnostics.probe_background_music",
                return_value=music_probe,
            ), platform_kit_version_patch():
                diag = _collect_diag()
        music_issues = [i for i in diag.issues if i.code == "background_music_unavailable"]
        self.assertTrue(music_issues)
        self.assertEqual(music_issues[0].severity, "warning")
        self.assertFalse(diag.has_fatal_issues)

    def test_skill_tree_core_load_detected_as_issue(self) -> None:
        skill_root = get_skill_root()
        fake_core = os.path.join(
            skill_root, "scripts", "fake_pkg", "jiangchang_skill_core", "__init__.py"
        )
        self.assertTrue(
            is_jiangchang_skill_core_from_skill_tree(
                skill_root=skill_root, core_file=fake_core
            )
        )
        self.assertFalse(
            is_jiangchang_skill_core_from_skill_tree(
                skill_root=skill_root,
                core_file=jiangchang_skill_core.__file__,
            )
        )

    def test_skill_tree_core_load_issue_in_diagnostics(self) -> None:
        skill_root = get_skill_root()
        fake_core = os.path.join(skill_root, "scripts", "jiangchang_skill_core", "__init__.py")
        with patch.object(jiangchang_skill_core, "__file__", fake_core):
            diag = _collect_diag()
        codes = diag.issue_codes()
        self.assertIn("jiangchang_skill_core_loaded_from_skill_tree", codes)
        messages = [issue.message for issue in diag.issues]
        self.assertTrue(any("skill tree" in msg.lower() for msg in messages))


class TestHealthRuntimeWithFakeMedia(unittest.TestCase):
    def test_probe_counts_mp3_without_download(self) -> None:
        with IsolatedDataRoot(user_id="_health_media"):
            media_root = Path(os.environ["JIANGCHANG_DATA_ROOT"]) / "shared" / "media-assets"
            music_dir = media_root / "music"
            music_dir.mkdir(parents=True)
            (music_dir / "demo.mp3").write_bytes(b"\x00" * 1024)
            os.environ["OPENCLAW_RECORD_VIDEO"] = "0"
            diag = _collect_diag()
            self.assertGreaterEqual(diag.background_music_mp3_count, 1)
            self.assertGreaterEqual(diag.background_music_usable_count, 1)
            self.assertIsNone(diag.background_music_issue)


if __name__ == "__main__":
    unittest.main()
