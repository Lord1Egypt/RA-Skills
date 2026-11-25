#!/usr/bin/env python3
"""Dependency-free checks for requested coverage and output limits."""

from __future__ import annotations

import argparse
import importlib.util
import os
import sys
import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch

CLI = Path(__file__).resolve().parents[1] / "scripts" / "video_frame_review.py"
spec = importlib.util.spec_from_file_location("video_frame_review", CLI)
assert spec and spec.loader
review = importlib.util.module_from_spec(spec)
spec.loader.exec_module(review)


def options(**changes):
    values = dict(start=0.0, end=None, interval=2.0, dense=[], full=[], max_frames=240, page_size=20, thumb_width=320)
    values.update(changes)
    return argparse.Namespace(**values)


class SamplingTests(unittest.TestCase):
    def test_regular_dense_and_selected_targets(self):
        end, samples = review.targets(options(dense=[(1.0, 2.0, 0.2)], full=[3.1], page_size=4), 6.0)
        self.assertEqual(end, 6.0)
        self.assertEqual([sample["requested_seconds"] for sample in samples], [0.0, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 3.1, 4.0])
        self.assertEqual(samples[7]["reasons"], ["full"])

    def test_frame_and_page_limits_reject_uncovered_output(self):
        with self.assertRaisesRegex(review.ReviewError, "exceed --max-frames"):
            review.targets(options(max_frames=2), 6.0)
        with self.assertRaisesRegex(review.ReviewError, "more than 12 pages"):
            review.targets(options(page_size=1), 26.0)
        with self.assertRaisesRegex(review.ReviewError, "at most 24"):
            review.targets(options(full=[i / 10 for i in range(25)]), 6.0)

    def test_dense_interval_must_be_inside_coverage(self):
        with self.assertRaisesRegex(review.ReviewError, "inside the requested coverage"):
            review.targets(options(start=2.0, end=4.0, dense=[(1.0, 3.0, 0.2)]), 6.0)


@unittest.skipIf(os.name == "nt", "synthetic ffprobe executable uses a POSIX shebang")
class FrameScanTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.executable = Path(directory.name) / "ffprobe"
        environment = patch.dict(os.environ, PATH=directory.name + os.pathsep + os.environ["PATH"])
        self.addCleanup(environment.stop)
        environment.start()

    def install_probe(self, body):
        self.executable.write_text(f"#!{sys.executable}\n" + body)
        self.executable.chmod(0o755)

    def test_frame_scan_handles_large_stderr(self):
        self.install_probe("import sys\nsys.stderr.write('diagnostic\\n' * 20000)\nprint('0.0')\nprint('1.0')\n")
        result = review.locate_frames(Path("synthetic.mp4"), [{"requested_seconds": 0.5}], 5)
        self.assertEqual(result, [{"requested_seconds": 0.5, "frame_index": 1, "pts_seconds": 1.0}])

    def test_stalled_frame_scan_reports_deadline(self):
        self.install_probe("import time\nprint('0.0', flush=True)\ntime.sleep(10)\n")
        with self.assertRaisesRegex(review.ReviewError, "ffprobe timed out after 0.2s"):
            review.locate_frames(Path("synthetic.mp4"), [{"requested_seconds": 0.5}], 0.2)


if __name__ == "__main__":
    unittest.main()
