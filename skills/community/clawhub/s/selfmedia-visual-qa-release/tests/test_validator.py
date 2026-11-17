from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import validate_release_package as validator

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = json.loads((ROOT / "contracts" / "douyin-five-file.json").read_text(encoding="utf-8"))


def media_probe(path: Path) -> dict:
    if path.name == "01-发布视频.mp4":
        return {"streams": [
            {"codec_type": "video", "codec_name": "h264", "avg_frame_rate": "30/1"},
        ], "format": {"duration": "2.0"}}
    dims = {"02-竖封面-3比4.png": (1080, 1440), "03-横封面-4比3.png": (1440, 1080)}
    width, height = dims.get(path.name, (1440, 1080))
    return {"streams": [{"codec_type": "video", "width": width, "height": height}], "format": {"duration": "0"}}


class PackageValidatorTests(unittest.TestCase):
    def make_package(self, directory: Path) -> None:
        for name in CONTRACT["required_files"]:
            (directory / name).write_bytes(b"test")
        (directory / "04-字幕.srt").write_text(
            "1\n00:00:00,000 --> 00:00:01,000\n测试字幕\n", encoding="utf-8"
        )

    def test_complete_package_passes_declared_contract(self) -> None:
        with tempfile.TemporaryDirectory() as td, patch.object(validator, "probe_media", side_effect=media_probe):
            directory = Path(td)
            self.make_package(directory)
            self.assertEqual(validator.validate_package(directory, CONTRACT), [])

    def test_missing_and_unexpected_assets_fail(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            directory = Path(td)
            (directory / "extra.txt").touch()
            errors = validator.validate_package(directory, CONTRACT)
            self.assertTrue(any("missing required file" in e for e in errors))
            self.assertIn("unexpected file: extra.txt", errors)

    def test_contract_rejects_directory_traversal(self) -> None:
        contract = json.loads(json.dumps(CONTRACT))
        contract["required_files"][0] = "../outside.txt"
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "contract.json"
            path.write_text(json.dumps(contract), encoding="utf-8")
            with self.assertRaisesRegex(validator.ContractError, "simple filenames"):
                validator.load_contract(path)

    def test_media_metadata_mismatch_is_reported(self) -> None:
        wrong = dict(CONTRACT)
        wrong["video"] = {**CONTRACT["video"], "frame_rate": "24/1"}
        with tempfile.TemporaryDirectory() as td, patch.object(validator, "probe_media", side_effect=media_probe):
            directory = Path(td)
            self.make_package(directory)
            errors = validator.validate_package(directory, wrong)
            self.assertTrue(any("frame rate expected 24/1" in e for e in errors))

    def test_subtitle_past_video_duration_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as td, patch.object(validator, "probe_media", side_effect=media_probe):
            directory = Path(td)
            self.make_package(directory)
            (directory / "04-字幕.srt").write_text(
                "1\n00:00:03,000 --> 00:00:04,000\n越界字幕\n", encoding="utf-8"
            )
            errors = validator.validate_package(directory, CONTRACT)
            self.assertTrue(any("after video duration" in e for e in errors))

    def test_contract_can_require_contiguous_subtitles(self) -> None:
        contract = json.loads(json.dumps(CONTRACT))
        contract["subtitles"]["allow_gaps"] = False
        with tempfile.TemporaryDirectory() as td, patch.object(validator, "probe_media", side_effect=media_probe):
            directory = Path(td)
            self.make_package(directory)
            (directory / "04-字幕.srt").write_text(
                "1\n00:00:00,000 --> 00:00:00,300\n第一句\n\n2\n00:00:00,500 --> 00:00:01,000\n第二句\n", encoding="utf-8"
            )
            errors = validator.validate_package(directory, contract)
            self.assertTrue(any("gaps between subtitle cues" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
