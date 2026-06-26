#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


TS = re.compile(r"(\d\d:\d\d:\d\d),(\d{3})\s+-->\s+(\d\d:\d\d:\d\d),(\d{3})")
DANGLING = re.compile(r"(然后|所以，?|并且|而且|但是|不过|如果|因为|以及|接下来|接下来要|我要|它会|这会|通过|如何|[，、：；,:;])\s*$")
BREAK_RE = re.compile(r"(?<=[。！？；])|(?<=，)")


def parse_time(hms: str, ms: str) -> float:
    hh, mm, ss = hms.split(":")
    return int(hh) * 3600 + int(mm) * 60 + int(ss) + int(ms) / 1000


def format_srt_time(seconds: float) -> str:
    total_ms = max(0, int(round(seconds * 1000)))
    hh = total_ms // 3_600_000
    total_ms %= 3_600_000
    mm = total_ms // 60_000
    total_ms %= 60_000
    ss = total_ms // 1000
    ms = total_ms % 1000
    return f"{hh:02d}:{mm:02d}:{ss:02d},{ms:03d}"


def parse_srt(path: Path) -> list[dict[str, object]]:
    cues: list[dict[str, object]] = []
    for block in re.split(r"\n\s*\n", path.read_text(encoding="utf-8-sig").strip()):
        lines = [line.strip() for line in block.splitlines()]
        ts_index = next((i for i, line in enumerate(lines) if TS.search(line)), None)
        if ts_index is None:
            continue
        match = TS.search(lines[ts_index])
        assert match is not None
        text = " ".join(line for line in lines[ts_index + 1 :] if line).strip()
        if text:
            cues.append(
                {
                    "start": parse_time(match.group(1), match.group(2)),
                    "end": parse_time(match.group(3), match.group(4)),
                    "text": text,
                }
            )
    return cues


def repair(cues: list[dict[str, object]]) -> list[dict[str, object]]:
    changed = True
    while changed:
        changed = False
        repaired: list[dict[str, object]] = []
        index = 0
        while index < len(cues):
            cue = cues[index]
            if index + 1 < len(cues) and DANGLING.search(str(cue["text"])):
                nxt = cues[index + 1]
                repaired.append({"start": cue["start"], "end": nxt["end"], "text": str(cue["text"]) + str(nxt["text"])})
                index += 2
                changed = True
            else:
                repaired.append(cue)
                index += 1
        cues = repaired
    for index in range(len(cues) - 1):
        if abs(float(cues[index]["start"]) - float(cues[index + 1]["start"])) < 0.01:
            cues[index + 1]["text"] = str(cues[index]["text"]) + str(cues[index + 1]["text"])
            cues[index]["text"] = ""
            continue
        if float(cues[index]["end"]) >= float(cues[index + 1]["start"]):
            cues[index]["end"] = max(float(cues[index]["start"]) + 0.35, float(cues[index + 1]["start"]) - 0.05)
    return [cue for cue in cues if str(cue["text"]).strip()]


def split_text(text: str, max_chars: int = 46) -> list[str]:
    text = re.sub(r"然后\s*所以，?", "所以，", text)
    text = re.sub(r"然后\s+所以，?", "所以，", text)
    parts = [part.strip() for part in BREAK_RE.split(text) if part.strip()]
    chunks: list[str] = []
    current = ""
    for part in parts:
        if not current:
            current = part
        elif len(current) + len(part) <= max_chars:
            current += part
        else:
            chunks.append(current)
            current = part
    if current:
        chunks.append(current)
    final: list[str] = []
    for chunk in chunks:
        while len(chunk) > max_chars * 1.2:
            cut = max(chunk.rfind("，", 0, max_chars), chunk.rfind("、", 0, max_chars), chunk.rfind(" ", 0, max_chars))
            if cut < max_chars * 0.45:
                cut = max_chars
            final.append(chunk[: cut + 1].strip())
            chunk = chunk[cut + 1 :].strip()
        if chunk:
            final.append(chunk)
    merged: list[str] = []
    index = 0
    while index < len(final):
        chunk = final[index]
        while index + 1 < len(final) and DANGLING.search(chunk):
            index += 1
            chunk = f"{chunk}{final[index]}"
        merged.append(chunk)
        index += 1
    out: list[str] = []
    for chunk in merged:
        while len(chunk) > max_chars * 1.2:
            cut = max(chunk.rfind("。", 0, max_chars), chunk.rfind("！", 0, max_chars), chunk.rfind("？", 0, max_chars), chunk.rfind("，", 0, max_chars), chunk.rfind("、", 0, max_chars), chunk.rfind(" ", 0, max_chars))
            if cut < max_chars * 0.45:
                cut = max_chars
            out.append(chunk[: cut + 1].strip())
            chunk = chunk[cut + 1 :].strip()
        if chunk:
            out.append(chunk)
    return out


def split_long(cues: list[dict[str, object]]) -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    for cue in cues:
        duration = float(cue["end"]) - float(cue["start"])
        text = str(cue["text"])
        if duration <= 8.5 and len(text) <= 72:
            out.append(cue)
            continue
        chunks = split_text(text)
        if len(chunks) <= 1:
            out.append(cue)
            continue
        total_chars = sum(max(1, len(chunk)) for chunk in chunks)
        cursor = float(cue["start"])
        for index, chunk in enumerate(chunks):
            if index == len(chunks) - 1:
                end = float(cue["end"])
            else:
                share = max(1, len(chunk)) / total_chars
                end = max(cursor + 1.2, cursor + duration * share)
                end = min(end, float(cue["end"]))
            out.append({"start": cursor, "end": end, "text": chunk})
            cursor = end
    return out


def write_srt(cues: list[dict[str, object]], path: Path) -> None:
    lines: list[str] = []
    for index, cue in enumerate(cues, 1):
        lines.append(str(index))
        lines.append(f"{format_srt_time(float(cue['start']))} --> {format_srt_time(float(cue['end']))}")
        lines.append(str(cue["text"]).strip())
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Repair common Chinese subtitle segmentation/timing failures.")
    parser.add_argument("srt", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--force", action="store_true", help="Overwrite existing SRT output")
    args = parser.parse_args()

    cues = parse_srt(args.srt)
    if not cues:
        print(f"FAIL: no cues found in {args.srt}")
        return 1
    if args.out.exists() and not args.force:
        print(f"FAIL: output already exists, choose a new version or pass --force: {args.out}")
        return 1
    repaired = split_long(repair(cues))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    write_srt(repaired, args.out)
    print(f"PASS: wrote {len(repaired)} repaired cues to {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
