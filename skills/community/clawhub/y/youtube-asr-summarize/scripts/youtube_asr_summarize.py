#!/usr/bin/env python3
"""Local YouTube ASR -> summary -> (optional) thumbnails/frames.

- Downloads audio with yt-dlp
- Transcribes with faster-whisper
- Writes transcript.txt + transcript.srt
- Produces summary.md (simple, deterministic)
- Optionally downloads video (<=360p) and extracts frames

No external API keys required.

Usage:
  youtube_asr_summarize.py --url <youtube-url> --out <dir> [--model small] [--lang zh]
                          [--frames 4 --frame-every 300]

Dependencies:
  - yt-dlp (brew)
  - ffmpeg (brew)
  - python + faster-whisper (pip)

Notes:
  - ASR quality depends on model size; CPU small/int8 is a good trade-off.
  - This script avoids leaking any credentials and does not upload content.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
from pathlib import Path


def run(cmd: list[str], cwd: Path | None = None):
    p = subprocess.run(cmd, cwd=str(cwd) if cwd else None, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    if p.returncode != 0:
        raise RuntimeError(f"Command failed ({p.returncode}): {' '.join(cmd)}\n{p.stdout[-4000:]}")
    return p.stdout


def have(bin_name: str) -> bool:
    return shutil.which(bin_name) is not None


def safe_slug(s: str) -> str:
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"[^\w\-\. ]+", "", s, flags=re.UNICODE)
    s = s.replace(" ", "_")
    return s[:80] or "video"


def format_ts(t: float) -> str:
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = int(t % 60)
    ms = int((t - int(t)) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def _mmss(seconds: float) -> str:
    m = int(seconds // 60)
    s = int(seconds % 60)
    return f"{m:02d}:{s:02d}"


def parse_srt(srt_path: Path) -> list[tuple[float, float, str]]:
    """Return list of (start_sec, end_sec, text)."""
    if not srt_path.exists():
        return []

    ts_re = re.compile(
        r"^(\d{2}):(\d{2}):(\d{2}),(\d{3})\s+-->\s+(\d{2}):(\d{2}):(\d{2}),(\d{3})"
    )

    def to_sec(h, m, s, ms):
        return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000.0

    out: list[tuple[float, float, str]] = []
    cur_start = None
    cur_end = None
    cur_text: list[str] = []

    for line in srt_path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line:
            if cur_start is not None and cur_end is not None and cur_text:
                out.append((cur_start, cur_end, " ".join(cur_text).strip()))
            cur_start = None
            cur_end = None
            cur_text = []
            continue
        m = ts_re.match(line)
        if m:
            cur_start = to_sec(*m.group(1, 2, 3, 4))
            cur_end = to_sec(*m.group(5, 6, 7, 8))
            continue
        if cur_start is not None and not line.isdigit():
            cur_text.append(line)

    if cur_start is not None and cur_end is not None and cur_text:
        out.append((cur_start, cur_end, " ".join(cur_text).strip()))

    return out


def summarize_bucket(bucket_text: str) -> str:
    """Heuristic summary of a bucket: pick 1-2 representative sentences."""
    text = re.sub(r"\s+", " ", bucket_text).strip()
    if not text:
        return ""

    # Split by Chinese punctuation / sentence-ish boundaries.
    parts = re.split(r"(?<=[。！？!?])\s*", text)
    parts = [p.strip() for p in parts if p.strip()]
    if not parts:
        parts = [text]

    keys = [
        "油价",
        "原油",
        "西德州",
        "布伦特",
        "熔断",
        "衰退",
        "通胀",
        "美联储",
        "降息",
        "战争",
        "供应",
        "需求",
        "库存",
        "OPEC",
        "沙特",
        "伊朗",
    ]

    def score(s: str) -> int:
        sc = 0
        sc += sum(3 for k in keys if k in s)
        sc += 2 if re.search(r"\d", s) else 0
        sc += 1 if len(s) >= 16 else 0
        sc -= 2 if len(s) > 120 else 0
        return sc

    ranked = sorted(parts, key=score, reverse=True)
    top = []
    for s in ranked:
        if s not in top:
            top.append(s)
        if len(top) >= 2:
            break
    return " ".join(top).strip()


def _keywords(s: str) -> set[str]:
    s = re.sub(r"\s+", " ", s).strip()
    # very lightweight tokenization for zh+numbers+latin words
    tokens = re.findall(r"[A-Za-z]{2,}|\d+(?:\.\d+)?|[\u4e00-\u9fff]{1,2}", s)
    # drop too-common 1-char words by keeping only 2-char CJK chunks above
    return set(t.lower() for t in tokens if t)


def _jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union if union else 0.0


def build_segment_timeline(srt_path: Path, every_seconds: int = 180, merge_threshold: float = 0.18) -> list[str]:
    """Timeline with ranges: [mm:ss-mm:ss] summary.

    - First builds fixed buckets (every_seconds)
    - Then merges adjacent buckets when their summaries are similar
      (keyword Jaccard overlap)

    This avoids a rigid "every N seconds" feel while staying local+deterministic.
    """
    items = parse_srt(srt_path)
    if not items:
        return []

    buckets: dict[int, list[str]] = {}
    starts: dict[int, float] = {}
    ends: dict[int, float] = {}

    for start, end, text in items:
        b = int(start // every_seconds)
        buckets.setdefault(b, []).append(text)
        starts[b] = min(starts.get(b, start), start)
        ends[b] = max(ends.get(b, end), end)

    segs: list[tuple[float, float, str]] = []
    for b in sorted(buckets.keys()):
        s = starts[b]
        e = ends[b]
        summ = summarize_bucket(" ".join(buckets[b]))
        if summ:
            segs.append((s, e, summ))

    if not segs:
        return []

    merged: list[tuple[float, float, str]] = []
    cur_s, cur_e, cur_t = segs[0]
    cur_kw = _keywords(cur_t)

    for s, e, t in segs[1:]:
        kw = _keywords(t)
        if _jaccard(cur_kw, kw) >= merge_threshold:
            # merge
            cur_e = e
            # keep the better/longer summary text, but avoid getting too long
            if len(t) > len(cur_t):
                cur_t = t
            cur_kw = _keywords(cur_t)
        else:
            merged.append((cur_s, cur_e, cur_t))
            cur_s, cur_e, cur_t = s, e, t
            cur_kw = kw

    merged.append((cur_s, cur_e, cur_t))

    out: list[str] = []
    for s, e, t in merged:
        out.append(f"[{_mmss(s)}-{_mmss(e)}] {t}")
    return out


def transcript_to_summary(text: str, title: str, url: str, timeline: list[str]) -> str:
    """A lightweight deterministic summarizer.

    For best results, users can later feed transcript to an LLM, but this keeps
    the skill self-contained and free.
    """
    # Heuristic bullets: keep first ~40 lines (often contains framing), then pick key lines
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]

    # Build keyword hit list
    keys = [
        "油价",
        "原油",
        "西德州",
        "布伦特",
        "熔断",
        "衰退",
        "通胀",
        "美联储",
        "降息",
        "战争",
        "供应",
        "需求",
        "库存",
        "OPEC",
        "沙特",
        "伊朗",
    ]

    picked: list[str] = []
    seen = set()

    for ln in lines[:60]:
        if ln not in seen:
            picked.append(ln)
            seen.add(ln)

    for ln in lines:
        if any(k in ln for k in keys):
            if ln not in seen:
                picked.append(ln)
                seen.add(ln)
        if len(picked) >= 140:
            break

    # Group into a compact markdown
    out = []
    out.append(f"# {title}\n")
    out.append(f"链接：{url}\n")
    out.append("## 摘要（基于本地ASR转写，可能有个别同音错字）\n")

    out.append("- 主题：围绕油价的异常波动、战争溢价与宏观传导（通胀/利率/衰退预期）。")
    out.append("- 形式：先讲当天油价极端波动与市场反应，再解释为何爆冲、以及风险如何传导。\n")

    if timeline:
        out.append("## 时间轴（分段总结）\n")
        for ln in timeline:
            out.append(f"- {ln}")
        out.append("")

    out.append("## 关键转写片段（用于快速定位）\n")
    for ln in picked[:40]:
        out.append(f"- {ln}")

    out.append("\n## 备注\n")
    out.append("- 如需更高质量总结：可用更大的 whisper 模型（medium/large），或把 transcript.txt 交给大模型做结构化摘要。")
    return "\n".join(out) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--model", default=os.getenv("WHISPER_MODEL", "small"))
    ap.add_argument("--lang", default=os.getenv("WHISPER_LANG", "zh"))
    ap.add_argument("--compute", default=os.getenv("WHISPER_COMPUTE", "int8"))
    ap.add_argument("--frames", type=int, default=1)
    ap.add_argument("--frame-every", type=int, default=300, help="seconds between frames")
    ap.add_argument("--timeline-every", type=int, default=int(os.getenv("TIMELINE_EVERY", "180")), help="seconds per timeline bucket")
    args = ap.parse_args()

    out_dir = Path(args.out).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    if not have("yt-dlp"):
        raise SystemExit("Missing yt-dlp. Install via: brew install yt-dlp")
    if not have("ffmpeg"):
        raise SystemExit("Missing ffmpeg. Install via: brew install ffmpeg")

    # 1) Get metadata
    meta_json = run(["yt-dlp", "-J", args.url], cwd=out_dir)
    meta = json.loads(meta_json)
    vid = meta.get("id")
    title = meta.get("title") or vid or "YouTube video"
    safe = safe_slug(title)

    transcript_txt = out_dir / "transcript.txt"
    transcript_srt = out_dir / "transcript.srt"

    # 2) Prefer subtitles if available (no ASR needed)
    # Try to fetch human subs and/or auto-subs as SRT.
    try:
        run(
            [
                "yt-dlp",
                "--skip-download",
                "--write-subs",
                "--write-auto-subs",
                "--sub-format",
                "srt",
                "--sub-langs",
                "zh,zh-Hans,zh-Hant,en",
                "-o",
                str(out_dir / f"subs_{vid}.%(ext)s"),
                args.url,
            ],
            cwd=out_dir,
        )
    except Exception:
        # If subtitle fetching fails, we can still fall back to ASR.
        pass

    srt_candidates = sorted(out_dir.glob(f"subs_{vid}*.srt"))
    if srt_candidates:
        # Use the first found SRT (usually best match lang order)
        transcript_srt.write_text(srt_candidates[0].read_text(encoding="utf-8", errors="ignore"), encoding="utf-8")
        # Also produce a plain transcript.txt from SRT text
        items = parse_srt(transcript_srt)
        transcript_txt.write_text("\n".join([t for _, _, t in items if t]) + "\n", encoding="utf-8")
    else:
        # 3) Download audio and extract mp3
        audio_mp3 = out_dir / f"audio_{vid}.mp3"
        run(
            [
                "yt-dlp",
                "-x",
                "--audio-format",
                "mp3",
                "--audio-quality",
                "0",
                "-o",
                str(out_dir / f"audio_{vid}.%(ext)s"),
                args.url,
            ],
            cwd=out_dir,
        )

        if not audio_mp3.exists():
            mp3s = list(out_dir.glob(f"audio_{vid}*.mp3"))
            if not mp3s:
                raise RuntimeError("Audio mp3 not found after yt-dlp")
            audio_mp3 = mp3s[0]

        # 4) Transcribe
        from faster_whisper import WhisperModel  # type: ignore

        model = WhisperModel(args.model, device="cpu", compute_type=args.compute)
        segments, info = model.transcribe(
            str(audio_mp3),
            language=args.lang,
            vad_filter=True,
            vad_parameters=dict(min_silence_duration_ms=600),
        )

        text_lines: list[str] = []
        srt_lines: list[str] = []
        idx = 1
        for seg in segments:
            t = (seg.text or "").strip()
            if not t:
                continue
            text_lines.append(t)
            srt_lines.append(str(idx))
            srt_lines.append(f"{format_ts(seg.start)} --> {format_ts(seg.end)}")
            srt_lines.append(t)
            srt_lines.append("")
            idx += 1

        transcript_txt.write_text("\n".join(text_lines) + "\n", encoding="utf-8")
        transcript_srt.write_text("\n".join(srt_lines), encoding="utf-8")

    # 4) Summary
    timeline = build_segment_timeline(transcript_srt, every_seconds=max(30, args.timeline_every))

    summary_md = out_dir / "summary.md"
    summary_md.write_text(
        transcript_to_summary(
            transcript_txt.read_text(encoding="utf-8"),
            title,
            args.url,
            timeline,
        ),
        encoding="utf-8",
    )

    # 5) Optional: download a low-res mp4 and extract frames
    frames_dir = out_dir / "frames"
    frames_dir.mkdir(exist_ok=True)

    if args.frames > 0:
        mp4 = out_dir / f"video_{vid}.mp4"
        run(
            [
                "yt-dlp",
                "-f",
                "bv*[ext=mp4][height<=360]+ba[ext=m4a]/b[ext=mp4][height<=360]/b",
                "-o",
                str(out_dir / f"video_{vid}.%(ext)s"),
                args.url,
            ],
            cwd=out_dir,
        )
        if mp4.exists():
            # extract frames every N seconds
            fps_expr = f"fps=1/{max(1, args.frame_every)}"
            run(
                [
                    "ffmpeg",
                    "-hide_banner",
                    "-loglevel",
                    "error",
                    "-y",
                    "-i",
                    str(mp4),
                    "-vf",
                    fps_expr,
                    "-frames:v",
                    str(args.frames),
                    str(frames_dir / "frame_%02d.jpg"),
                ],
                cwd=out_dir,
            )

    print(f"OK: {title}")
    print(f"out: {out_dir}")
    print(f"audio: {audio_mp3.name}")
    print(f"transcript: {transcript_txt.name} ({len(text_lines)} lines)")
    print(f"summary: {summary_md.name}")


if __name__ == "__main__":
    main()
