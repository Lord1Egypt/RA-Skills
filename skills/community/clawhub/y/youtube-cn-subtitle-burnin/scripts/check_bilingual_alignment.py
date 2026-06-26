#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


SRT_TS = re.compile(r"(\d{2}:\d{2}:\d{2}),(\d{3})\s+-->\s+(\d{2}:\d{2}:\d{2}),(\d{3})")


@dataclass
class Cue:
    idx: int
    start: float
    end: float
    text: str


def parse_time(hms: str, ms: str) -> float:
    hh, mm, ss = hms.split(":")
    return int(hh) * 3600 + int(mm) * 60 + int(ss) + int(ms) / 1000


def format_time(seconds: float) -> str:
    total = max(0, int(round(seconds)))
    hh = total // 3600
    mm = (total % 3600) // 60
    ss = total % 60
    return f"{hh:02d}:{mm:02d}:{ss:02d}"


def parse_srt(path: Path) -> list[Cue]:
    cues: list[Cue] = []
    for block in re.split(r"\n\s*\n", path.read_text(encoding="utf-8-sig").strip()):
        lines = [line.rstrip() for line in block.splitlines() if line.strip()]
        if not lines:
            continue
        ts_index = next((i for i, line in enumerate(lines) if SRT_TS.search(line)), None)
        if ts_index is None:
            continue
        match = SRT_TS.search(lines[ts_index])
        assert match is not None
        raw_idx = lines[0] if ts_index > 0 else str(len(cues) + 1)
        idx = int(raw_idx) if raw_idx.isdigit() else len(cues) + 1
        text = " ".join(lines[ts_index + 1 :]).strip()
        if text:
            cues.append(Cue(idx, parse_time(match.group(1), match.group(2)), parse_time(match.group(3), match.group(4)), text))
    return cues


def overlap(a: Cue, b: Cue) -> float:
    return min(a.end, b.end) - max(a.start, b.start)


def matching_text(zh: Cue, en_cues: list[Cue], min_overlap: float) -> str:
    parts = [cue.text for cue in en_cues if overlap(zh, cue) >= min_overlap]
    return re.sub(r"\s+", " ", " ".join(parts)).strip()


def choose_samples(zh_cues: list[Cue], en_cues: list[Cue], count: int, min_overlap: float) -> list[tuple[Cue, str]]:
    if not zh_cues:
        return []
    positions = [0, len(zh_cues) // 2, len(zh_cues) - 1]
    dense = sorted(zh_cues, key=lambda cue: len(cue.text) / max(0.4, cue.end - cue.start), reverse=True)
    picked: list[Cue] = []
    for index in positions:
        cue = zh_cues[index]
        if cue not in picked:
            picked.append(cue)
    for cue in dense:
        if cue not in picked:
            picked.append(cue)
        if len(picked) >= count:
            break
    return [(cue, matching_text(cue, en_cues, min_overlap)) for cue in picked[:count]]


def write_report(path: Path, zh_path: Path, en_path: Path, samples: list[tuple[Cue, str]], issues: list[str], warnings: list[str]) -> None:
    lines = [
        "# Bilingual Alignment Check",
        "",
        f"Chinese SRT: {zh_path}",
        f"English SRT: {en_path}",
        f"Status: {'fail' if issues else 'pass with manual samples'}",
        "",
        "## Automatic Findings",
        "",
    ]
    if issues:
        lines.extend(f"- FAIL: {issue}" for issue in issues)
    if warnings:
        lines.extend(f"- WARN: {warning}" for warning in warnings)
    if not issues and not warnings:
        lines.append("- No missing English overlap or obvious timing drift detected.")
    lines.extend(["", "## Manual Samples", "", "| Time | Chinese | English reference | Review |", "|---|---|---|---|"])
    for cue, en_text in samples:
        zh = cue.text.replace("|", " / ")
        en = (en_text or "[missing]").replace("|", " / ")
        lines.append(f"| {format_time(cue.start)} | {zh} | {en} | needs agent/user meaning check |")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Check bilingual subtitle timing correspondence and emit review samples.")
    parser.add_argument("--zh-srt", type=Path, required=True)
    parser.add_argument("--en-srt", type=Path, required=True)
    parser.add_argument("--min-overlap", type=float, default=0.05)
    parser.add_argument("--max-start-drift", type=float, default=1.2)
    parser.add_argument("--sample-count", type=int, default=6)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()

    if not args.zh_srt.exists():
        print(f"FAIL: missing Chinese SRT {args.zh_srt}")
        return 1
    if not args.en_srt.exists():
        print(f"FAIL: missing English SRT {args.en_srt}")
        return 1
    zh_cues = parse_srt(args.zh_srt)
    en_cues = parse_srt(args.en_srt)
    if not zh_cues or not en_cues:
        print("FAIL: both Chinese and English SRT files must contain cues")
        return 1

    issues: list[str] = []
    warnings: list[str] = []
    for zh in zh_cues:
        matches = [cue for cue in en_cues if overlap(zh, cue) >= args.min_overlap]
        if not matches:
            issues.append(f"cue #{zh.idx} at {format_time(zh.start)} has no overlapping English reference")
            continue
        closest = min(matches, key=lambda cue: abs(cue.start - zh.start))
        drift = abs(closest.start - zh.start)
        if drift > args.max_start_drift:
            warnings.append(f"cue #{zh.idx} at {format_time(zh.start)} start differs from closest English by {drift:.2f}s")
    samples = choose_samples(zh_cues, en_cues, max(3, args.sample_count), args.min_overlap)
    if args.report:
        write_report(args.report, args.zh_srt, args.en_srt, samples, issues, warnings)

    print(f"Checked {len(zh_cues)} Chinese cues against {len(en_cues)} English cues")
    if warnings:
        print(f"WARN: {len(warnings)} timing drift warning(s)")
        for warning in warnings[:50]:
            print(f"- {warning}")
        if len(warnings) > 50:
            print(f"- ... {len(warnings) - 50} more")
    if issues:
        print(f"FAIL: {len(issues)} alignment issue(s)")
        for issue in issues[:80]:
            print(f"- {issue}")
        if len(issues) > 80:
            print(f"- ... {len(issues) - 80} more")
        return 1
    if args.report:
        print(f"PASS: wrote alignment review samples to {args.report}")
    else:
        print("PASS: no missing English overlap detected")
    return 0


if __name__ == "__main__":
    sys.exit(main())
