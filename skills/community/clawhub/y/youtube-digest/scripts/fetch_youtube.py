#!/usr/bin/env python3
import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


def run(cmd):
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return proc.returncode, proc.stdout, proc.stderr


def dedupe_keep_order(lines):
    seen = set()
    out = []
    for line in lines:
        if not line or line in seen:
            continue
        seen.add(line)
        out.append(line)
    return out


def subtitle_to_text(src: Path, txt_path: Path):
    text_lines = []
    for raw in src.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw.strip().replace("\ufeff", "")
        if not line:
            continue
        if line.upper() == "WEBVTT":
            continue
        if line.isdigit():
            continue
        if "-->" in line:
            continue
        if re.match(r"^\d{2}:\d{2}[:.]\d{2}", line):
            continue
        if line.startswith("NOTE") or line.startswith("Kind:") or line.startswith("Language:"):
            continue
        line = re.sub(r"<[^>]+>", "", line)
        line = re.sub(r"&nbsp;", " ", line)
        line = re.sub(r"\s+", " ", line).strip()
        if line:
            text_lines.append(line)
    text_lines = dedupe_keep_order(text_lines)
    txt_path.write_text("\n".join(text_lines) + ("\n" if text_lines else ""), encoding="utf-8")


def choose_subtitle_file(out_dir: Path):
    preferred = []
    for pattern in ["video*.zh*.vtt", "video*.zh*.srt", "video*.en*.vtt", "video*.en*.srt", "video*.vtt", "video*.srt"]:
        preferred.extend(sorted(out_dir.glob(pattern)))
    for p in preferred:
        if p.exists() and p.stat().st_size > 0:
            return p
    return None


def main():
    parser = argparse.ArgumentParser(description="Fetch YouTube metadata and subtitles with yt-dlp")
    parser.add_argument("url")
    parser.add_argument("--out", required=True)
    parser.add_argument("--langs", default="zh.*,en.*,en")
    parser.add_argument("--proxy", default=None, help="HTTP proxy for yt-dlp")
    args = parser.parse_args()

    if shutil.which("yt-dlp") is None:
        print("ERROR: yt-dlp not found in PATH", file=sys.stderr)
        sys.exit(2)

    out_dir = Path(args.out).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    prefix = out_dir / "video"

    proxy_args = ["--proxy", args.proxy] if args.proxy else []
    rc, stdout, stderr = run(["yt-dlp"] + proxy_args + ["--dump-single-json", "--skip-download", args.url])
    if rc != 0:
        print(stderr, file=sys.stderr)
        sys.exit(rc)
    meta = json.loads(stdout)

    # Step 1: try manual subtitles only (avoids 429 from auto-translate requests)
    sub_cmd = [
        "yt-dlp",
    ] + proxy_args + [
        "--skip-download",
        "--write-subs",
        "--sub-langs", args.langs,
        "-o", str(prefix) + ".%(ext)s",
        args.url,
    ]
    rc2, stdout2, stderr2 = run(sub_cmd)

    # Step 2: if no subtitle files were downloaded, try auto subs as fallback
    # Use only original-language auto captions (e.g. "en") to avoid 429 from translation API
    if not list(out_dir.glob("video*.*tt")) and not list(out_dir.glob("video*.srt")):
        # Detect original language from metadata, default to "en"
        orig_lang = "en"
        auto_caps = meta.get("automatic_captions", {})
        for lang_code in ["en", "en-orig"]:
            if lang_code in auto_caps:
                orig_lang = lang_code
                break
        auto_cmd = [
            "yt-dlp",
        ] + proxy_args + [
            "--skip-download",
            "--write-auto-subs",
            "--sub-langs", orig_lang,
            "-o", str(prefix) + ".%(ext)s",
            args.url,
        ]
        rc2, stdout2, stderr2 = run(auto_cmd)

    chosen = choose_subtitle_file(out_dir)
    transcript_txt = out_dir / "transcript.txt"
    if chosen:
        subtitle_to_text(chosen, transcript_txt)

    summary = {
        "title": meta.get("title"),
        "uploader": meta.get("uploader"),
        "channel": meta.get("channel"),
        "duration": meta.get("duration"),
        "webpage_url": meta.get("webpage_url") or args.url,
        "description": meta.get("description"),
        "subtitles_available": bool(meta.get("subtitles")),
        "automatic_captions_available": bool(meta.get("automatic_captions")),
        "subtitle_extract_exit_code": rc2,
        "subtitle_extract_stderr": stderr2[-2000:],
        "chosen_subtitle_file": str(chosen) if chosen else None,
        "transcript_txt": str(transcript_txt) if chosen else None,
    }

    (out_dir / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if chosen:
        print(f"\nTranscript: {transcript_txt}")
    else:
        print("\nNo subtitles were downloaded. Consider ASR/Whisper as a fallback.")


if __name__ == "__main__":
    main()
