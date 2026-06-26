#!/usr/bin/env python3
"""Score the primary README for launch-readiness."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


REFERENCE_NAMES = re.compile(r"\b(optillm|openevolve|autoresearch|symphony|paperclip|codex|claude|openai)\b", re.IGNORECASE)
INTERNAL_TERMS = re.compile(r"\b(oauth|subagent|workflow contract|benchmark contract|operator|control plane|paid api key)\b", re.IGNORECASE)


def display_input_label(raw_arg: str, resolved: Path) -> str:
    raw_path = Path(raw_arg).expanduser()
    if not raw_path.is_absolute():
        return raw_path.as_posix() or "."
    return resolved.name or "."


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--readme", required=True, help="Path to the README to score.")
    parser.add_argument("--out", required=True, help="Output JSON file.")
    args = parser.parse_args()

    readme = Path(args.readme).expanduser().resolve()
    lines = readme.read_text(encoding="utf-8").splitlines()

    score = 100
    components: list[dict[str, object]] = []

    def adjust(name: str, delta: int, detail: str) -> None:
        nonlocal score
        score += delta
        components.append({"name": name, "delta": delta, "detail": detail})

    top_lines = lines[:60]
    top_text = "\n".join(top_lines)
    has_pitch = any(line.startswith("**") for line in lines[:15])
    quick_start_line = next((idx for idx, line in enumerate(lines, start=1) if "quick start" in line.lower()), None)
    first_code_block = next((idx for idx, line in enumerate(lines, start=1) if line.strip().startswith("```")), None)
    has_use_case_language = any("use this" in line.lower() or "when to use" in line.lower() for line in lines[:140])
    has_concrete_value = any("output" in line.lower() or "what it catches" in line.lower() or "what it checks" in line.lower() for line in lines[:140])

    if not has_pitch:
        adjust("missing-one-line-pitch", -35, "No clear one-line pitch near the top.")
    else:
        adjust("one-line-pitch", 5, "One-line pitch is present near the top.")

    has_early_quick_start = quick_start_line is not None and quick_start_line <= 80
    if quick_start_line is None:
        adjust("missing-quick-start", -20, "Quick Start section is missing.")
    elif quick_start_line > 80:
        adjust("buried-quick-start", -12, "Quick Start exists but is buried.")
    else:
        adjust("early-quick-start", 5, "Quick Start appears early.")

    has_early_code_example = first_code_block is not None and first_code_block <= 100
    if first_code_block is None or first_code_block > 100:
        adjust("late-code-example", -10, "No early code example near the top.")
    else:
        adjust("early-code-example", 5, "Runnable code appears near the top.")

    if len(lines) > 220:
        adjust("readme-length", -15, "README is longer than 220 lines.")
    elif len(lines) > 140:
        adjust("readme-length", -5, "README is somewhat long for a launch page.")

    reference_hits = len(REFERENCE_NAMES.findall(top_text))
    if reference_hits >= 4:
        adjust("too-many-comparisons", -10, "Top of README compares itself to too many external projects.")

    internal_hits = len(INTERNAL_TERMS.findall(top_text))
    if internal_hits >= 4:
        adjust("internal-language", -15, "Top of README uses too much internal workflow language.")

    if has_use_case_language:
        adjust("use-case-language", 5, "README explains when to use the project.")
    else:
        adjust("missing-use-case-language", -10, "README does not explain when to use the project.")

    if has_concrete_value:
        adjust("concrete-value", 5, "README explains the concrete output or catches.")
    else:
        adjust("missing-concrete-value", -25, "README does not explain the concrete output or what it catches.")

    score = max(0, min(100, score))
    if not has_pitch or not has_concrete_value:
        verdict = "not-ready"
    elif not has_early_quick_start or not has_early_code_example:
        verdict = "revise-before-publish"
    elif score >= 80:
        verdict = "publish-ready"
    elif score >= 60:
        verdict = "revise-before-publish"
    else:
        verdict = "not-ready"

    payload = {
        "readme": display_input_label(args.readme, readme),
        "score": score,
        "verdict": verdict,
        "line_count": len(lines),
        "components": components,
    }
    out_path = Path(args.out).expanduser().resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
