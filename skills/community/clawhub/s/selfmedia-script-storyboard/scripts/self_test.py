from __future__ import annotations

import copy
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_timeline import TimelineError, load_timeline, validate

ROOT = Path(__file__).resolve().parents[1]


class TimelineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.timeline = load_timeline(ROOT / "examples" / "timeline.json")
        self.captions = ROOT / "examples" / "captions.srt"

    def test_example_matches_voiceover_preview_and_srt(self) -> None:
        validate(self.timeline, voiceover_duration=2.8, preview_duration=3.0, captions=self.captions)

    def test_gap_or_overlap_is_rejected(self) -> None:
        for start in (44, 46):
            timeline = copy.deepcopy(self.timeline)
            timeline["scenes"][1]["start_frame"] = start
            with self.subTest(start=start), self.assertRaises(TimelineError):
                validate(timeline)

    def test_duplicate_scene_id_is_rejected(self) -> None:
        timeline = copy.deepcopy(self.timeline)
        timeline["scenes"][1]["id"] = timeline["scenes"][0]["id"]
        with self.assertRaisesRegex(TimelineError, "duplicate scene id"):
            validate(timeline)

    def test_overlong_voiceover_is_rejected(self) -> None:
        with self.assertRaisesRegex(TimelineError, "exceeds timeline duration"):
            validate(self.timeline, voiceover_duration=4.0)

    def test_preview_must_match_timeline_within_one_frame(self) -> None:
        with self.assertRaisesRegex(TimelineError, "does not match timeline duration"):
            validate(self.timeline, preview_duration=3.2)

    def test_caption_past_timeline_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            srt = Path(td) / "late.srt"
            srt.write_text("1\n00:00:03,100 --> 00:00:03,300\nlate\n", encoding="utf-8")
            with self.assertRaisesRegex(TimelineError, "after timeline duration"):
                validate(self.timeline, captions=srt)

    def test_frame_total_must_be_fully_covered(self) -> None:
        timeline = copy.deepcopy(self.timeline)
        timeline["duration_frames"] = 100
        with self.assertRaisesRegex(TimelineError, "last scene ends"):
            validate(timeline)


if __name__ == "__main__":
    unittest.main()
