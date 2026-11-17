#!/usr/bin/env python3
"""Run the real CLI on a local synthetic clip; print images for human visual QC."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys
import tempfile

from PIL import Image

SKILL = Path(__file__).resolve().parents[1]
CLI = SKILL / "scripts" / "video_frame_review.py"


def run(*command: str) -> None:
    subprocess.run(command, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pause", action="store_true", help="pause for visual inspection before removing temporary files")
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix="video-frame-review-proof-") as directory:
        root = Path(directory)
        clip = root / "synthetic.mp4"
        output = root / "review"
        run("ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi", "-i", "testsrc2=size=640x360:rate=10", "-f", "lavfi", "-i", "sine=frequency=440:sample_rate=48000", "-t", "6", "-c:v", "mpeg4", "-q:v", "2", "-c:a", "aac", str(clip))
        run(sys.executable, str(CLI), str(clip), "--output", str(output), "--interval", "2", "--dense", "1:2:0.2", "--full", "3.1", "--page-size", "4")
        data = json.loads((output / "manifest.json").read_text())
        assert data["audio_stream_present"] and not data["audio_reviewed"]
        assert len(data["samples"]) == 9, data["samples"]
        assert len(data["contact_sheets"]) == 3
        assert len(data["full_frames"]) == 1
        dense = [sample for sample in data["samples"] if "dense" in sample["reasons"]]
        assert len(dense) == 5
        assert len({sample["frame_index"] for sample in dense}) == 5, dense
        assert all(0 <= sample["pts_seconds"] - sample["requested_seconds"] <= 0.101 for sample in dense), dense
        for sheet in data["contact_sheets"]:
            with Image.open(output / sheet["file"]) as image:
                assert image.width > 0 and image.height > 0
        for frame in data["full_frames"]:
            with Image.open(output / frame["file"]) as image:
                assert list(image.size) == frame["dimensions"] == [640, 360]
        print(f"PASS: 2s regular coverage, 0.2s dense extraction, PTS labels, pagination, full-size frame, audio limit: {output}")
        print("Visual QC: inspect the sheet files and full frame before accepting the skill.")
        for sheet in data["contact_sheets"]:
            print(output / sheet["file"])
        print(output / data["full_frames"][0]["file"])
        if args.pause:
            input("Press Enter after visual QC to remove this temporary fixture.")


if __name__ == "__main__":
    main()
