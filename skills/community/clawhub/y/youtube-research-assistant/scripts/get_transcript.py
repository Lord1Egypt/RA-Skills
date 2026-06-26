#!/usr/bin/env python3

import argparse
import sys
import re
import subprocess
import tempfile
import threading
import shutil
import json
import time
from pathlib import Path
from datetime import datetime
from typing import Optional, List

# --------------------------------
# Paths
# --------------------------------
DATA_DIR = Path.home() / ".openclaw/workspace/skills/youtube-research-assistant/data"
INDEX_FILE = DATA_DIR / "index.json"
SESSION_FILE = DATA_DIR / "session.json"

MAX_TRANSCRIPT_LINES = 20000

STOPWORDS = {
    "the","a","an","is","are","was","were","what","how","why","who",
    "when","where","does","do","this","that","in","on","of","and",
    "or","to","for","with","about"
}

# --------------------------------
# Dependency check
# --------------------------------
def check_dependencies():
    yt_dlp_path = shutil.which("yt-dlp")

    if not yt_dlp_path:
        print("❌ yt-dlp not installed. Run: pip install yt-dlp", file=sys.stderr)
        sys.exit(1)

    try:
        version = subprocess.run(
            ["yt-dlp", "--version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=5
        ).stdout.decode().strip()

        print(f"✅ yt-dlp version: {version}", file=sys.stderr)

    except Exception:
        pass


# --------------------------------
# Session management
# --------------------------------
def load_session() -> dict:
    if SESSION_FILE.exists():
        try:
            return json.loads(SESSION_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass

    return {"active_video": None, "videos": []}


def save_session(state: dict):

    SESSION_FILE.parent.mkdir(parents=True, exist_ok=True)

    tmp = SESSION_FILE.with_suffix(".tmp")

    tmp.write_text(
        json.dumps(state, indent=2),
        encoding="utf-8"
    )

    tmp.replace(SESSION_FILE)


def set_active_video(video_id: str):

    state = load_session()

    state["active_video"] = video_id

    if video_id not in state["videos"]:
        state["videos"].append(video_id)

    save_session(state)


def get_active_video() -> Optional[str]:

    state = load_session()

    return state.get("active_video")


# --------------------------------
# Extract video ID
# --------------------------------
def extract_video_id(url: str) -> str:

    patterns = [
        r"(?:v=|\/)([0-9A-Za-z_-]{11})",
        r"youtu\.be\/([0-9A-Za-z_-]{11})",
        r"embed\/([0-9A-Za-z_-]{11})"
    ]

    for pattern in patterns:

        match = re.search(pattern, url)

        if match:
            return match.group(1)

    print("❌ Invalid YouTube URL", file=sys.stderr)

    sys.exit(1)


# --------------------------------
# Cleanup old transcripts
# --------------------------------
def cleanup_old():

    if not DATA_DIR.exists():
        return

    cutoff = time.time() - 86400

    for f in DATA_DIR.glob("*.txt"):

        if f.stat().st_mtime < cutoff:
            f.unlink()


# --------------------------------
# Save transcript
# --------------------------------
def save_transcript(video_id: str, transcript: str, url: str):

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    path = DATA_DIR / f"{video_id}.txt"

    path.write_text(transcript, encoding="utf-8")

    index = {}

    if INDEX_FILE.exists():
        try:
            index = json.loads(INDEX_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass

    index[video_id] = {
        "url": url,
        "saved": datetime.now().isoformat(),
        "lines": transcript.count("\n")
    }

    tmp = INDEX_FILE.with_suffix(".tmp")

    tmp.write_text(
        json.dumps(index, indent=2),
        encoding="utf-8"
    )

    tmp.replace(INDEX_FILE)


# --------------------------------
# Load transcript
# --------------------------------
def load_transcript(video_id: str) -> Optional[str]:

    path = DATA_DIR / f"{video_id}.txt"

    if not path.exists():
        return None

    return path.read_text(encoding="utf-8")


# --------------------------------
# Fetch subtitles using yt-dlp
# --------------------------------
def fetch_subtitles(url: str, lang: str = "en") -> Optional[str]:

    with tempfile.TemporaryDirectory() as temp_dir:

        cmd = [
            "yt-dlp",
            "--extractor-args", "youtube:player_client=android",
            "--skip-download",
            "--write-subs",
            "--write-auto-subs",
            "--sub-langs", lang,
            "--sub-format", "vtt",
            "--convert-subs", "vtt",
            "--no-playlist",
            "--no-write-info-json",
            "--no-write-playlist-metafiles",
            "--force-ipv4",
            "--retries", "3",
            "--fragment-retries", "3",
            "--sleep-requests", "1",
            "--no-check-certificates",
            "--output", "subs",
            url
        ]

        try:

            proc = subprocess.Popen(
                cmd,
                cwd=temp_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

        except Exception as e:

            print(f"❌ Failed to start yt-dlp: {e}", file=sys.stderr)

            return None

        try:

            proc.wait(timeout=60)

        except subprocess.TimeoutExpired:

            proc.kill()

            print("❌ yt-dlp timeout", file=sys.stderr)

            return None

        if proc.returncode != 0:

            print("❌ yt-dlp failed", file=sys.stderr)

            return None

        vtt_files = list(Path(temp_dir).glob("*.vtt"))

        if not vtt_files:
            return None

        content = vtt_files[0].read_text(encoding="utf-8")

        return clean_vtt(content)


# --------------------------------
# Clean VTT
# --------------------------------
def clean_vtt(content: str) -> str:

    lines = content.splitlines()

    result = []

    seen = set()

    current_time = None

    for line in lines:

        line = line.strip()

        if not line or line == "WEBVTT" or line.isdigit():
            continue

        if "-->" in line:

            start = line.split(" --> ")[0]

            parts = start.split(":")

            if len(parts) == 3:
                _, m, s = parts
            else:
                m, s = parts

            current_time = f"[{m}:{s[:2]}]"

            continue

        clean = re.sub(r"<[^>]+>", "", line)

        clean = clean.replace("&nbsp;", " ").strip()

        if clean and current_time and clean not in seen:

            seen.add(clean)

            result.append(f"{current_time} {clean}")

    return "\n".join(result[:MAX_TRANSCRIPT_LINES])


# --------------------------------
# Retrieval
# --------------------------------
def retrieve_chunks(transcript: str, question: str) -> List[str]:

    lines = transcript.splitlines()

    chunks = []

    chunk_size = 10

    step = chunk_size // 2

    for i in range(0, len(lines), step):

        chunk = lines[i:i+chunk_size]

        if chunk:
            chunks.append(chunk)

    keywords = set(re.findall(r"\b\w+\b", question.lower())) - STOPWORDS

    def score(chunk):

        text = " ".join(chunk).lower()

        return sum(1 for kw in keywords if kw in text)

    ranked = sorted(chunks, key=score, reverse=True)

    top = ranked[:5]

    return ["\n".join(c) for c in top]


# --------------------------------
# Fetch command
# --------------------------------
def cmd_fetch(args):

    check_dependencies()

    cleanup_old()

    video_id = extract_video_id(args.url)

    existing = load_transcript(video_id)

    if existing:

        set_active_video(video_id)

        print(existing)

        return

    transcript = fetch_subtitles(args.url, args.lang)

    if not transcript:

        print("❌ Could not fetch transcript.")

        sys.exit(1)

    save_transcript(video_id, transcript, args.url)

    set_active_video(video_id)

    print(transcript)


# --------------------------------
# Ask command
# --------------------------------
def cmd_ask(args):

    video_id = args.video_id

    if video_id in ("ACTIVE_VIDEO", "-", ""):

        video_id = get_active_video()

        if not video_id:
            print("❌ No active video in session.")

            sys.exit(1)

    transcript = load_transcript(video_id)

    if not transcript:

        print("❌ Transcript not found.")

        sys.exit(1)

    chunks = retrieve_chunks(transcript, args.question)

    if not chunks:

        print("This topic is not covered in the video.")

        return

    for c in chunks:

        print(c)

        print()


# --------------------------------
# Session command
# --------------------------------
def cmd_session(args):

    state = load_session()

    print(json.dumps(state, indent=2))


# --------------------------------
# List command
# --------------------------------
def cmd_list(args):

    if not INDEX_FILE.exists():

        print("No transcripts stored")

        return

    index = json.loads(INDEX_FILE.read_text())

    for vid in index:

        print(vid, index[vid]["url"])


# --------------------------------
# Cleanup command
# --------------------------------
def cmd_cleanup(args):

    cleanup_old()

    print("Cleanup complete")


# --------------------------------
# CLI
# --------------------------------
def main():

    parser = argparse.ArgumentParser()

    sub = parser.add_subparsers(dest="cmd", required=True)

    f = sub.add_parser("fetch")

    f.add_argument("url")

    f.add_argument("--lang", default="en")

    f.set_defaults(func=cmd_fetch)

    q = sub.add_parser("ask")

    q.add_argument("video_id")

    q.add_argument("question")

    q.set_defaults(func=cmd_ask)

    s = sub.add_parser("session")

    s.set_defaults(func=cmd_session)

    l = sub.add_parser("list")

    l.set_defaults(func=cmd_list)

    c = sub.add_parser("cleanup")

    c.set_defaults(func=cmd_cleanup)

    args = parser.parse_args()

    args.func(args)


if __name__ == "__main__":

    main()