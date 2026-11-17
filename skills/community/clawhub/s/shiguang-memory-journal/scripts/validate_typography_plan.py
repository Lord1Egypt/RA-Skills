#!/usr/bin/env python3
"""Validate a portable Shiguang poster typography plan without rendering pixels."""

from __future__ import annotations

import json
import hashlib
import re
import sys
from pathlib import Path


EFFECTS = {"none", "cinematic-shadow", "outline", "ink-edge"}
RELATIONS = {"crown", "anchor", "hinge", "blade", "seal", "whisper", "weave"}
ORIENTATIONS = {"horizontal", "vertical"}
CANDIDATE_IDS = {"reference-led", "story-led", "wild-card"}


def intersection_area(left: dict, right: dict) -> float:
    width = max(0, min(left["x"] + left["width"], right["x"] + right["width"]) - max(left["x"], right["x"]))
    height = max(0, min(left["y"] + left["height"], right["y"] + right["height"]) - max(left["y"], right["y"]))
    return width * height


def candidate_signature(candidate: dict) -> str:
    payload = {key: candidate.get(key) for key in ("id", "plan", "safeRegion", "placements")}
    canonical = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def validate_placement(
    placement: object,
    expected_text: str,
    safe_region: object,
    avoid_regions: list,
    label: str,
    issues: list[str],
    canvas_width: float,
    canvas_height: float,
) -> None:
    if not isinstance(placement, dict):
        issues.append(f"{label} is required")
        return
    values = [placement.get(key) for key in ("x", "y", "width", "height")]
    if not all(isinstance(value, (int, float)) for value in values):
        issues.append(f"{label} must contain numeric x/y/width/height")
        return
    x, y, width, height = values
    if x < 0 or y < 0 or width <= 0 or height <= 0 or x + width > canvas_width or y + height > canvas_height:
        issues.append(f"{label} must stay inside the canvas")
    lines = placement.get("displayLines")
    if not isinstance(lines, list) or not lines or "".join(str(line) for line in lines) != expected_text:
        issues.append(f"{label}.displayLines must exactly preserve the approved copy")
    if isinstance(safe_region, dict) and all(isinstance(safe_region.get(key), (int, float)) for key in ("x", "y", "width", "height")):
        safe = {
            "x": safe_region["x"] * canvas_width,
            "y": safe_region["y"] * canvas_height,
            "width": safe_region["width"] * canvas_width,
            "height": safe_region["height"] * canvas_height,
        }
        rect = {"x": x, "y": y, "width": width, "height": height}
        if x < safe["x"] - 1 or y < safe["y"] - 1 or x + width > safe["x"] + safe["width"] + 1 or y + height > safe["y"] + safe["height"] + 1:
            issues.append(f"{label} must stay inside its candidate safeRegion")
        for region in avoid_regions:
            if not isinstance(region, dict) or region.get("reason") == "high-detail":
                continue
            try:
                avoid = {
                    "x": region["x"] * canvas_width,
                    "y": region["y"] * canvas_height,
                    "width": region["width"] * canvas_width,
                    "height": region["height"] * canvas_height,
                }
                if intersection_area(rect, avoid) > 1:
                    issues.append(f"{label} overlaps a semantic avoidRegion")
                    break
            except (KeyError, TypeError):
                pass


def validate_region(region: object, label: str, issues: list[str]) -> None:
    if not isinstance(region, dict):
        issues.append(f"{label} must be an object")
        return
    values = [region.get(key) for key in ("x", "y", "width", "height")]
    if not all(isinstance(value, (int, float)) for value in values):
        issues.append(f"{label} must contain numeric x/y/width/height")
        return
    x, y, width, height = values
    if x < 0 or y < 0 or width <= 0 or height <= 0 or x + width > 1 or y + height > 1:
        issues.append(f"{label} must stay inside the normalized canvas")
    if region.get("orientation", "horizontal") not in ORIENTATIONS:
        issues.append(f"{label}.orientation is unsupported")


def validate(data: dict) -> list[str]:
    issues: list[str] = []
    title = str(data.get("approvedTitle") or data.get("title") or "")
    plan = data.get("typography") if isinstance(data.get("typography"), dict) else data
    rendered = str(data.get("renderedTitle") or title)
    if not title:
        issues.append("approvedTitle is required")
    elif rendered != title:
        issues.append("renderedTitle must exactly equal approvedTitle")
    lines = plan.get("displayLines") or plan.get("semanticBreaks") or [title]
    if not isinstance(lines, list) or not 1 <= len(lines) <= 3:
        issues.append("displayLines must contain one to three lines")
        lines = []
    elif "".join(str(item) for item in lines) != title:
        issues.append("displayLines must preserve every approved character in order")
    if any(not str(line).strip() for line in lines):
        issues.append("displayLines must not contain an empty or whitespace-only line")
    if any(str(line) != str(line).lstrip() for line in lines[1:]):
        issues.append("displayLines must not start a continuation line with layout whitespace")
    if len(lines) > 1 and len(str(lines[-1])) == 1:
        issues.append("last line must not be an orphan glyph")
    if any(re.match(r"^[，。！？；：、）》】〕〉」』…,.!?;:)\]}]", str(line)) for line in lines[1:]):
        issues.append("displayLines must not start a continuation line with closing punctuation")
    if any(re.search(r"[（《【〔〈「『(\[{]$", str(line)) for line in lines[:-1]):
        issues.append("displayLines must not end a line with opening punctuation")
    if any(re.search(r"[A-Za-z0-9]$", str(lines[index])) and re.match(r"^[A-Za-z0-9]", str(lines[index + 1])) for index in range(max(0, len(lines) - 1))):
        issues.append("displayLines must not split a Latin/number token")
    if plan.get("relation") not in RELATIONS:
        issues.append("relation is missing or unsupported")
    if plan.get("titleEffect", "none") not in EFFECTS:
        issues.append("titleEffect is unsupported")
    if plan.get("titleOrientation", "horizontal") not in ORIENTATIONS:
        issues.append("titleOrientation is unsupported")
    scale = plan.get("titleScaleRatio")
    if not isinstance(scale, (int, float)) or not .02 <= scale <= .2:
        issues.append("titleScaleRatio must be between 0.02 and 0.2")
    width = plan.get("titleWidthRatio")
    if not isinstance(width, (int, float)) or not .2 <= width <= 1:
        issues.append("titleWidthRatio must be between 0.2 and 1")
    reference_ocr = data.get("referenceOcrDenyList") or []
    if any(fragment and fragment in rendered for fragment in reference_ocr if fragment != title):
        issues.append("rendered title leaks reference OCR")
    safe_region = data.get("titleSafeRegion") or plan.get("titleSafeRegion")
    if safe_region is not None:
        validate_region(safe_region, "titleSafeRegion", issues)
    avoid_regions = data.get("avoidRegions") or []
    for index, region in enumerate(avoid_regions):
        validate_region(region, f"avoidRegions[{index}]", issues)
    if isinstance(safe_region, dict):
        for region in avoid_regions:
            if not isinstance(region, dict) or region.get("reason") == "high-detail":
                continue
            try:
                width = max(0, min(safe_region["x"] + safe_region["width"], region["x"] + region["width"]) - max(safe_region["x"], region["x"]))
                height = max(0, min(safe_region["y"] + safe_region["height"], region["y"] + region["height"]) - max(safe_region["y"], region["y"]))
                overlap = width * height / max(.0001, safe_region["width"] * safe_region["height"])
                if overlap > .02:
                    issues.append("titleSafeRegion overlaps a semantic avoidRegion")
                    break
            except (KeyError, TypeError):
                pass
    tournament = data.get("typographyTournament")
    if tournament is not None:
        candidates = tournament.get("candidates") if isinstance(tournament, dict) else None
        ids = [candidate.get("id") for candidate in candidates or [] if isinstance(candidate, dict)]
        if len(candidates or []) != 3 or set(ids) != CANDIDATE_IDS:
            issues.append("typographyTournament must contain the three canonical candidate IDs")
        if tournament.get("winnerCandidateId") not in ids:
            issues.append("typographyTournament winnerCandidateId must reference a candidate")
        structural_signatures = []
        canvas_width = float(data.get("canvasWidth") or 720)
        canvas_height = float(data.get("canvasHeight") or 1280)
        subtitle = str(data.get("approvedSubtitle") or data.get("subtitle") or "")
        for index, candidate in enumerate(candidates or []):
            candidate_plan = candidate.get("plan") if isinstance(candidate, dict) else None
            if not isinstance(candidate_plan, dict):
                issues.append("every typographyTournament candidate requires a plan")
                continue
            candidate_region = candidate.get("safeRegion")
            validate_region(candidate_region, f"typographyTournament.candidates[{index}].safeRegion", issues)
            placements = candidate.get("placements")
            if not isinstance(placements, list) or not placements:
                issues.append("every typographyTournament candidate requires rendered placements")
                continue
            title_placement = next((item for item in placements if isinstance(item, dict) and item.get("id") == "poster-title"), None)
            subtitle_placement = next((item for item in placements if isinstance(item, dict) and item.get("id") == "poster-subtitle"), None)
            validate_placement(title_placement, title, candidate_region, avoid_regions, f"candidate[{index}].poster-title", issues, canvas_width, canvas_height)
            if subtitle:
                validate_placement(subtitle_placement, subtitle, candidate_region, avoid_regions, f"candidate[{index}].poster-subtitle", issues, canvas_width, canvas_height)
            signature = candidate.get("signature")
            if not isinstance(signature, str) or not re.fullmatch(r"[0-9a-f]{64}", signature):
                issues.append(f"candidate[{index}].signature must be a lowercase SHA-256")
            elif signature != candidate_signature(candidate):
                issues.append(f"candidate[{index}].signature does not bind id/plan/safeRegion/placements")
            structural_signatures.append(json.dumps({
                "style": candidate_plan.get("style"),
                "relation": candidate_plan.get("relation"),
                "titleOrientation": candidate_plan.get("titleOrientation", "horizontal"),
                "titleLines": candidate_plan.get("titleLines"),
                "placement": {key: (title_placement or {}).get(key) for key in (
                    "x", "y", "width", "height", "fontSize", "orientation", "displayLines"
                )},
            }, sort_keys=True))
        if len(structural_signatures) == 3 and len(set(structural_signatures)) != 3:
            issues.append("typographyTournament candidates must be structurally distinct")
    return issues


def main() -> int:
    if len(sys.argv) == 2 and sys.argv[1] == "--self-test":
        base = {
            "approvedTitle": "广州欢迎，2026",
            "typography": {"relation": "anchor", "displayLines": ["广州欢迎，", "2026"], "titleWidthRatio": .8, "titleScaleRatio": .08, "titleEffect": "none"},
            "titleSafeRegion": {"x": .05, "y": .7, "width": .9, "height": .2, "orientation": "horizontal"},
            "avoidRegions": [],
            "typographyTournament": {"winnerCandidateId": "story-led", "candidates": [
                {"id": "reference-led", "plan": {"style": "editorial-serif", "relation": "anchor", "titleLines": 2}, "safeRegion": {"x": .05, "y": .68, "width": .9, "height": .24, "orientation": "horizontal"}, "placements": [{"id": "poster-title", "x": 40, "y": 880, "width": 620, "height": 180, "fontSize": 72, "orientation": "horizontal", "displayLines": ["广州欢迎，", "2026"]}]},
                {"id": "story-led", "plan": {"style": "brush-impact", "relation": "weave", "titleLines": 2}, "safeRegion": {"x": .05, "y": .04, "width": .9, "height": .23, "orientation": "horizontal"}, "placements": [{"id": "poster-title", "x": 52, "y": 80, "width": 580, "height": 220, "fontSize": 88, "orientation": "horizontal", "displayLines": ["广州欢迎，", "2026"]}]},
                {"id": "wild-card", "plan": {"style": "condensed-cinematic", "relation": "blade", "titleOrientation": "vertical", "titleLines": 1}, "safeRegion": {"x": .7, "y": .1, "width": .25, "height": .7, "orientation": "vertical"}, "placements": [{"id": "poster-title", "x": 520, "y": 160, "width": 140, "height": 760, "fontSize": 68, "orientation": "vertical", "displayLines": ["广州欢迎，2026"]}]},
            ]},
        }
        for candidate in base["typographyTournament"]["candidates"]:
            candidate["signature"] = candidate_signature(candidate)
        assert not validate(base), validate(base)
        punctuation = json.loads(json.dumps(base)); punctuation["typography"]["displayLines"] = ["广州欢迎", "，2026"]
        assert any("punctuation" in issue for issue in validate(punctuation))
        identical = json.loads(json.dumps(base)); identical["typographyTournament"]["candidates"] = [
            {"id": item, "plan": {"style": "editorial-serif", "relation": "anchor", "titleLines": 2}, "placements": [{"id": "poster-title", "x": 40, "y": 880, "width": 620, "height": 180, "fontSize": 72, "orientation": "horizontal", "displayLines": ["广州欢迎，", "2026"]}]}
            for item in ("reference-led", "story-led", "wild-card")
        ]
        assert any("structurally distinct" in issue for issue in validate(identical))
        overlap = json.loads(json.dumps(base)); overlap["avoidRegions"] = [{"x": .05, "y": .7, "width": .9, "height": .2, "confidence": 1, "reason": "protected-subject"}]
        assert any("overlaps" in issue for issue in validate(overlap))
        whitespace = json.loads(json.dumps(base)); whitespace["approvedTitle"] = "广州欢迎， 2026"; whitespace["typography"]["displayLines"] = ["广州欢迎，", " 2026"]
        assert any("whitespace" in issue for issue in validate(whitespace))
        wrong_copy = json.loads(json.dumps(base)); wrong_copy["typographyTournament"]["candidates"][0]["placements"][0]["displayLines"] = ["错误标题"]
        assert any("approved copy" in issue for issue in validate(wrong_copy))
        outside = json.loads(json.dumps(base)); outside["typographyTournament"]["candidates"][0]["placements"][0]["x"] = -999
        assert any("inside the canvas" in issue for issue in validate(outside))
        bad_signature = json.loads(json.dumps(base)); bad_signature["typographyTournament"]["candidates"][0]["signature"] = "0" * 64
        assert any("does not bind" in issue for issue in validate(bad_signature))
        subtitle_case = json.loads(json.dumps(base)); subtitle_case["approvedSubtitle"] = "城市的一封邀请"
        subtitle_placements = [
            {"id": "poster-subtitle", "x": 44, "y": 1080, "width": 500, "height": 50, "displayLines": ["城市的一封邀请"]},
            {"id": "poster-subtitle", "x": 54, "y": 172, "width": 300, "height": 18, "displayLines": ["城市的一封邀请"]},
            {"id": "poster-subtitle", "x": 522, "y": 930, "width": 138, "height": 50, "displayLines": ["城市的一封邀请"]},
        ]
        for candidate, placement in zip(subtitle_case["typographyTournament"]["candidates"], subtitle_placements):
            candidate["placements"].append(placement)
            candidate["signature"] = candidate_signature(candidate)
        assert not validate(subtitle_case), validate(subtitle_case)
        subtitle_case["typographyTournament"]["candidates"][0]["placements"][1]["y"] = 9999
        subtitle_case["typographyTournament"]["candidates"][0]["signature"] = candidate_signature(subtitle_case["typographyTournament"]["candidates"][0])
        assert any("poster-subtitle must stay inside" in issue for issue in validate(subtitle_case))
        print(json.dumps({"passed": True, "cases": 9}, ensure_ascii=False))
        return 0
    if len(sys.argv) != 2:
        print("usage: validate_typography_plan.py PLAN.json | --self-test", file=sys.stderr)
        return 2
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    issues = validate(data)
    print(json.dumps({"passed": not issues, "issues": issues}, ensure_ascii=False, indent=2))
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
