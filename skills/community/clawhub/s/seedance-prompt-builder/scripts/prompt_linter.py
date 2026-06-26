#!/usr/bin/env python3
"""Lightweight Seedance prompt checker.

Usage:
    python prompt_linter.py prompt.txt
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REF_VIDEO = "\u53c2\u8003\u89c6\u9891"
STRICT_EDIT = "\u4e25\u683c\u7f16\u8f91"
EXTEND = "\u5ef6\u957f"
IMAGE = "\u56fe\u7247"
VIDEO = "\u89c6\u9891"
SHOT = "\u955c\u5934"
NO_SUBTITLE = "\u65e0\u5b57\u5e55"
SUBTITLE = "\u5b57\u5e55"
WATERMARK = "\u6c34\u5370"
LOGO = "logo"

CAMERA_TERMS = [
    "\u63a8\u955c",  # push shot
    "\u62c9\u8fdc",  # pull away
    "\u6a2a\u79fb",  # lateral move
    "\u8ddf\u62cd",  # follow shot
    "\u73af\u7ed5",  # orbit
    "\u4fef\u51b2",  # dive
    "\u6447\u955c",  # pan
    "\u56fa\u5b9a\u673a\u4f4d",  # fixed camera
]


def lint(text: str) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    compact = re.sub(r"\s+", "", text.lower())

    if REF_VIDEO in text and (STRICT_EDIT in text or EXTEND in text):
        issues.append({
            "severity": "high",
            "issue": "possible task routing conflict",
            "fix": "for edit or extension tasks, refer directly to videoN instead of saying reference videoN for the source clip",
        })

    if re.search(r"\b\d+\s*[-~]\s*\d+\s*(s|sec|second|seconds)\b", text.lower()) or re.search(r"\d+\s*[-~]\s*\d+\s*\u79d2", text):
        issues.append({
            "severity": "medium",
            "issue": "exact timestamp ranges detected",
            "fix": "prefer shot 1, shot 2, shot 3 unless exact timing is explicitly required",
        })

    if (IMAGE in text or VIDEO in text) and ("define" not in text.lower()) and ("\u5b9a\u4e49" not in text):
        issues.append({
            "severity": "medium",
            "issue": "asset references appear without subject definitions",
            "fix": "for multi-subject or multi-asset scenes, define stable labels for each subject and reuse them",
        })

    shot_chunks = re.split(r"(?:shot\s*\d+|\u955c\u5934\s*\d+)", text, flags=re.IGNORECASE)
    for index, chunk in enumerate(shot_chunks[1:], start=1):
        count = sum(1 for term in CAMERA_TERMS if term in chunk)
        if count > 1:
            issues.append({
                "severity": "medium",
                "issue": f"shot {index} may contain multiple camera moves",
                "fix": "keep one primary camera movement per shot",
            })

    if SUBTITLE not in text and NO_SUBTITLE not in text:
        issues.append({
            "severity": "low",
            "issue": "no explicit subtitle constraint detected",
            "fix": "if no text is desired, add a no-subtitle and no-text constraint",
        })

    if WATERMARK not in text and LOGO not in compact:
        issues.append({
            "severity": "low",
            "issue": "no logo or watermark constraint detected",
            "fix": "if branding is not desired, add no-logo and no-watermark constraints",
        })

    return issues


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python prompt_linter.py prompt.txt", file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    text = path.read_text(encoding="utf-8")
    print(json.dumps({"issues": lint(text)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
