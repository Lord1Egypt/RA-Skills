"""video_compose.py 单元测试。

mock seedance.submit_and_wait 避免打真实 API。ffmpeg 部分用 skip_concat=True 避免依赖。
"""

import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from content_engine import video_compose
from content_engine.seedance import SeedanceError, TaskFailed
from content_engine.video_compose import (
    Shot,
    compose,
    concat_with_ffmpeg,
    parse_shots,
    write_partial_report,
)


# 真实的 seedance prompt 样本（5 个 shot）
SAMPLE_MD = """## Shot 1 (0–6s)

**Shot type**: wide
**Subject + action**: A silk vest hangs centered.
**Duration**: 6s

---

## Shot 2 (7–13s)

**Shot type**: medium close-up
**Subject + action**: collar detail.
**Duration**: 7s

---

## Shot 3 (14-20s)

**Shot type**: extreme close-up
**Duration**: 6s
"""


class TestParseShots(unittest.TestCase):

    def test_parses_3_shots(self):
        shots = parse_shots(SAMPLE_MD)
        self.assertEqual(len(shots), 3)

    def test_shot_indices_in_order(self):
        shots = parse_shots(SAMPLE_MD)
        self.assertEqual([s.index for s in shots], [1, 2, 3])

    def test_durations_calculated(self):
        shots = parse_shots(SAMPLE_MD)
        self.assertEqual(shots[0].duration, 6)   # 0–6
        self.assertEqual(shots[1].duration, 6)   # 7–13
        self.assertEqual(shots[2].duration, 6)   # 14-20

    def test_handles_fullwidth_dash(self):
        # "0–6s" 是全角 –，"14-20s" 是半角 -
        shots = parse_shots(SAMPLE_MD)
        self.assertEqual(len(shots), 3)

    def test_empty_returns_empty(self):
        self.assertEqual(parse_shots(""), [])

    def test_no_match_returns_empty(self):
        self.assertEqual(parse_shots("# Some heading\nno shots here"), [])

    def test_body_excludes_next_header(self):
        shots = parse_shots(SAMPLE_MD)
        for s in shots[:-1]:
            self.assertNotIn("## Shot", s.body)


class TestCompose(unittest.TestCase):

    def _mock_submit_and_wait(self, side_effects):
        """side_effects: 每次调用返回 (Path, task_id) 或抛异常"""
        idx = [0]

        def fake(prompt, out_path, **kwargs):
            i = idx[0]
            idx[0] += 1
            item = side_effects[i]
            if isinstance(item, Exception):
                raise item
            # 模拟下载：写一个小文件
            out_path = Path(out_path)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_bytes(b"FAKE_VIDEO_BYTES")
            return out_path, item
        return fake

    def test_all_succeed_skip_concat(self):
        """3 个 shot 全成功，跳 ffmpeg。"""
        with tempfile.TemporaryDirectory() as tmp:
            shots_dir = Path(tmp) / "shots"
            with mock.patch.object(
                video_compose, "submit_and_wait",
                side_effect=self._mock_submit_and_wait(["t1", "t2", "t3"]),
            ):
                report = compose(SAMPLE_MD, shots_dir, skip_concat=True, api_key="fake")
        self.assertEqual(report.shots_total, 3)
        self.assertEqual(report.shots_succeeded, 3)
        self.assertTrue(report.all_succeeded)

    def test_partial_failure(self):
        """中间 shot 失败，其他保留。"""
        with tempfile.TemporaryDirectory() as tmp:
            shots_dir = Path(tmp) / "shots"
            with mock.patch.object(
                video_compose, "submit_and_wait",
                side_effect=self._mock_submit_and_wait([
                    "t1",
                    TaskFailed("nsfw blocked"),
                    "t3",
                ]),
            ):
                report = compose(SAMPLE_MD, shots_dir, skip_concat=True, api_key="fake")
        self.assertEqual(report.shots_total, 3)
        self.assertEqual(report.shots_succeeded, 2)
        self.assertTrue(report.has_partial_failure)
        self.assertFalse(report.all_succeeded)
        # 失败 shot 应有 error 信息
        failed = [r for r in report.individual if not r.success]
        self.assertEqual(len(failed), 1)
        self.assertIn("nsfw", failed[0].error)
        self.assertEqual(failed[0].shot.index, 2)

    def test_all_fail(self):
        with tempfile.TemporaryDirectory() as tmp:
            shots_dir = Path(tmp) / "shots"
            with mock.patch.object(
                video_compose, "submit_and_wait",
                side_effect=self._mock_submit_and_wait([
                    SeedanceError("api down"),
                    SeedanceError("api down"),
                    SeedanceError("api down"),
                ]),
            ):
                report = compose(SAMPLE_MD, shots_dir, skip_concat=True, api_key="fake")
        self.assertEqual(report.shots_succeeded, 0)
        self.assertIn("全部 shot 都失败", report.skipped_concat_reason)

    def test_unparseable_prompt(self):
        with tempfile.TemporaryDirectory() as tmp:
            shots_dir = Path(tmp) / "shots"
            report = compose("no shots here", shots_dir, api_key="fake")
        self.assertEqual(report.shots_total, 0)
        self.assertIn("解析不出 shot", report.skipped_concat_reason)

    def test_progress_callback_invoked(self):
        seen = []
        with tempfile.TemporaryDirectory() as tmp:
            shots_dir = Path(tmp) / "shots"
            # 让 submit_and_wait 内部触发 on_progress
            def fake(prompt, out_path, on_progress=None, **kwargs):
                if on_progress:
                    on_progress("submitted", 0)
                Path(out_path).parent.mkdir(parents=True, exist_ok=True)
                Path(out_path).write_bytes(b"x")
                return Path(out_path), "tid"

            with mock.patch.object(video_compose, "submit_and_wait", side_effect=fake):
                compose(
                    SAMPLE_MD, shots_dir, skip_concat=True, api_key="fake",
                    on_shot_progress=lambda idx, status, e: seen.append((idx, status)),
                )
        # 每个 shot 应至少触发一次 progress
        shot_indices = {s[0] for s in seen}
        self.assertEqual(shot_indices, {1, 2, 3})


class TestWritePartialReport(unittest.TestCase):

    def test_report_lists_failures_with_prompts(self):
        from content_engine.video_compose import ComposeReport, ShotResult
        report = ComposeReport(
            shots_total=2,
            shots_succeeded=1,
            individual=[
                ShotResult(
                    shot=Shot(index=1, duration=5, body="prompt body 1"),
                    success=True, video_path=Path("/tmp/shot_01.mp4"), task_id="t1",
                ),
                ShotResult(
                    shot=Shot(index=2, duration=5, body="prompt body 2"),
                    success=False, error="api error",
                ),
            ],
        )
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "partial-video.md"
            write_partial_report(report, out)
            text = out.read_text(encoding="utf-8")
        # 状态计数
        self.assertIn("**Succeeded**: 1", text)
        self.assertIn("**Failed**: 1", text)
        # 失败 shot 的 prompt 应在报告里方便重跑
        self.assertIn("prompt body 2", text)
        self.assertIn("api error", text)
        # 成功 shot 的 task_id
        self.assertIn("t1", text)


class TestConcatFfmpeg(unittest.TestCase):
    """ffmpeg 集成测试 — 跳过如果系统没装 ffmpeg。"""

    def test_raises_if_no_ffmpeg(self):
        with mock.patch.object(video_compose.shutil, "which", return_value=None):
            with self.assertRaises(FileNotFoundError) as cm:
                concat_with_ffmpeg([Path("/x")], Path("/y.mp4"))
            self.assertIn("ffmpeg", str(cm.exception))

    def test_raises_if_empty_list(self):
        with mock.patch.object(video_compose.shutil, "which", return_value="/usr/bin/ffmpeg"):
            with self.assertRaises(ValueError):
                concat_with_ffmpeg([], Path("/y.mp4"))


if __name__ == "__main__":
    unittest.main()
