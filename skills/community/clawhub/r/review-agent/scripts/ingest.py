#!/usr/bin/env python3
"""Multi-modal input ingest for review-agent.

Scans sessions/<id>/input/ for artifacts, dispatches to appropriate extractors,
and produces sessions/<id>/normalized.md as the canonical text for review.

Supported:
  - .md / .txt / .markdown → copy as-is
  - .pdf → pdftotext (if available) / python pdfminer (fallback)
  - .png / .jpg / .jpeg / .webp → OCR (tesseract if available)
  - .wav / .mp3 / .m4a / .ogg / .flac → whisper transcription
  - Lark / Feishu doc or wiki URL → v2 expects the subagent to pre-resolve
    these via native feishu_doc/feishu_wiki tools and drop the resulting
    text into input/ as .txt. If the subagent forgot and only the URL is
    present, we record the URL but cannot fetch (v2 has no shell wrapper).
  - Google Docs URL → gdrive CLI (if available)
  - .jsonl → pretty-print text content
  - unknown → warn + skip

Also scans input/*.txt files for URLs and fetches those inline.

Exit codes:
  0 — all artifacts ingested cleanly
  2 — bad invocation (e.g. session dir missing)
  3 — at least one attachment required a tool we couldn't find, and no
      usable text was produced. Writes ingest_failed.json with a
      Lark-ready, Requester-facing message the orchestrator can relay.
      This is the v1.1.1 hard-fail — previous behavior silently returned
      a placeholder "[PDF ingest unavailable …]" and let scan.py run on
      nonsense.

Usage:
  ingest.py <session_dir> [--force]
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path


class IngestError(Exception):
    """Raised when an attachment requires a tool that isn't installed.
    The .user_message field is a short, non-technical string that can be
    shown to the Requester in Lark (no stack traces, no file paths)."""
    def __init__(self, user_message: str, detail: str = ""):
        super().__init__(user_message)
        self.user_message = user_message
        self.detail = detail


def which(cmd):
    return shutil.which(cmd)


def log(session_dir, msg):
    with open(Path(session_dir) / "ingest.log", "a") as f:
        f.write(f"[{datetime.now().astimezone().isoformat(timespec='seconds')}] {msg}\n")


def read_text(p: Path):
    try:
        return p.read_text(encoding="utf-8")
    except Exception as e:
        return f"[could not read {p.name}: {e}]"


def extract_pdf(path: Path) -> str:
    if which("pdftotext"):
        r = subprocess.run(["pdftotext", "-layout", str(path), "-"],
                          capture_output=True, text=True, timeout=60)
        if r.returncode == 0 and r.stdout.strip():
            return r.stdout
    try:
        from pdfminer.high_level import extract_text
        txt = extract_text(str(path))
        if txt and txt.strip():
            return txt
    except ImportError:
        pass
    raise IngestError(
        user_message=(
            f"我这边没法提取 PDF（{path.name}）的文字内容——server 上既没装 "
            f"`pdftotext` 也没装 `pdfminer.six`。\n"
            f"两个办法:\n"
            f"  1. 让 Admin 在 server 上装一下（macOS: `brew install poppler`；"
            f"Linux: `sudo apt install poppler-utils` 或 `pip3 install pdfminer.six`）\n"
            f"  2. 你直接把 PDF 的正文贴在 Lark 消息里，我一样能 review。"
        ),
        detail=f"pdftotext={bool(which('pdftotext'))} pdfminer.six=missing; file={path.name}",
    )


def extract_image(path: Path) -> str:
    if which("tesseract"):
        r = subprocess.run(["tesseract", str(path), "-", "-l", "chi_sim+eng"],
                          capture_output=True, text=True, timeout=60)
        if r.returncode == 0 and r.stdout.strip():
            return r.stdout
    raise IngestError(
        user_message=(
            f"我这边没法 OCR 图片（{path.name}）——server 上没装 `tesseract`。\n"
            f"两个办法:\n"
            f"  1. 让 Admin 装一下（macOS: `brew install tesseract tesseract-lang`；"
            f"Linux: `sudo apt install tesseract-ocr tesseract-ocr-chi-sim`）\n"
            f"  2. 你直接把图片里的文字打出来发给我，我一样能 review。"
        ),
        detail=f"tesseract=missing; file={path.name}",
    )


def extract_audio(path: Path) -> str:
    if which("whisper"):
        try:
            out_dir = path.parent / f"_whisper_{path.stem}"
            out_dir.mkdir(exist_ok=True)
            r = subprocess.run(
                ["whisper", str(path), "--output_dir", str(out_dir),
                 "--output_format", "txt", "--language", "auto", "--model", "base"],
                capture_output=True, text=True, timeout=600
            )
            txt_file = out_dir / (path.stem + ".txt")
            if txt_file.exists() and txt_file.read_text().strip():
                return txt_file.read_text()
        except Exception as e:
            raise IngestError(
                user_message=(
                    f"语音转文字时出错（{path.name}）。你把关键点打出来发我就行。"
                ),
                detail=f"whisper-run-failed: {e}; file={path.name}",
            )
    raise IngestError(
        user_message=(
            f"我这边没法转写语音（{path.name}）——server 上没装 `whisper`。\n"
            f"两个办法:\n"
            f"  1. 让 Admin 装一下（`pip3 install openai-whisper`，macOS 先 `brew install ffmpeg`）\n"
            f"  2. 你把关键点打出来发我，我一样能 review。"
        ),
        detail=f"whisper=missing; file={path.name}",
    )


LARK_URL_RE = re.compile(
    r'https?://[\w.-]*(?:larksuite\.com|feishu\.cn)/(?:wiki|docx|docs|sheets)/\S+',
    re.IGNORECASE
)
GDOCS_URL_RE = re.compile(
    r'https?://docs\.google\.com/\S+', re.IGNORECASE
)


def fetch_lark(url: str, session_dir: Path) -> str:
    """v2: no shell wrapper. The subagent should pre-resolve Lark URLs via
    native feishu_doc / feishu_wiki tools and drop text into input/ BEFORE
    invoking ingest. If we still see a bare URL here, log it and note in
    normalized.md that content is missing."""
    log(session_dir, f"lark URL not pre-resolved: {url}")
    return (f"## Lark doc URL (content not fetched)\n\n"
            f"URL: {url}\n\n"
            f"⚠️ The subagent should have pre-resolved this via the native "
            f"`feishu_doc.read` / `feishu_wiki.read` tool and dropped the "
            f"text into `input/` before calling ingest.")


def fetch_gdocs(url: str) -> str:
    gdrive = Path.home() / "bin" / "gdrive"
    if not gdrive.exists():
        return f"[~/bin/gdrive not installed; URL: {url}]"
    m = re.search(r'/d/([a-zA-Z0-9_-]+)', url)
    if not m:
        return f"[could not extract doc id from {url}]"
    doc_id = m.group(1)
    try:
        r = subprocess.run([str(gdrive), "read-file-content", doc_id],
                          capture_output=True, text=True, timeout=60)
        if r.returncode == 0:
            return f"## Google Doc content from {url}\n\n{r.stdout}"
        return f"[gdrive read failed: {r.stderr[:200]}]"
    except Exception as e:
        return f"[gdrive error {e}; URL: {url}]"


def process_artifact(path: Path, session_dir: Path) -> str:
    """Return markdown text extracted from this artifact.
    Raises IngestError if a required tool is missing."""
    ext = path.suffix.lower()
    header = f"\n## Input: `{path.name}` ({ext or 'no ext'})\n\n"

    if ext in (".md", ".markdown", ".txt"):
        text = read_text(path)
        urls_lark = LARK_URL_RE.findall(text)
        urls_gdocs = GDOCS_URL_RE.findall(text)
        expansions = []
        for u in urls_lark:
            log(session_dir, f"fetching lark: {u}")
            expansions.append(fetch_lark(u, session_dir))
        for u in urls_gdocs:
            log(session_dir, f"fetching gdocs: {u}")
            expansions.append(fetch_gdocs(u))
        return header + text + ("\n\n" + "\n\n".join(expansions) if expansions else "")

    if ext == ".pdf":
        log(session_dir, f"pdf: {path.name}")
        return header + extract_pdf(path)

    if ext in (".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp"):
        log(session_dir, f"image: {path.name}")
        return header + extract_image(path)

    if ext in (".wav", ".mp3", ".m4a", ".ogg", ".flac", ".aac"):
        log(session_dir, f"audio: {path.name}")
        return header + extract_audio(path)

    if ext == ".jsonl":
        lines = [json.dumps(json.loads(l), ensure_ascii=False)
                 for l in read_text(path).splitlines() if l.strip()]
        return header + "\n".join(f"- {l}" for l in lines)

    if ext == ".url":
        url = read_text(path).strip()
        if LARK_URL_RE.match(url):
            return header + fetch_lark(url, session_dir)
        if GDOCS_URL_RE.match(url):
            return header + fetch_gdocs(url)
        return header + f"URL: {url}\n[unknown URL type]"

    log(session_dir, f"unknown: {path.name} (ext={ext})")
    return header + f"[unsupported format {ext}; file preserved in input/]"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("session_dir")
    ap.add_argument("--force", action="store_true",
                   help="re-ingest even if normalized.md exists")
    args = ap.parse_args()

    sd = Path(args.session_dir)
    if not sd.is_dir():
        print(f"error: {sd} not a directory", file=sys.stderr)
        sys.exit(2)
    input_dir = sd / "input"
    normalized = sd / "normalized.md"

    if normalized.exists() and not args.force:
        print("normalized.md exists; use --force to re-ingest", file=sys.stderr)
        return

    if not input_dir.exists() or not any(input_dir.iterdir()):
        print(f"warn: no files in {input_dir}", file=sys.stderr)
        return

    parts = [
        f"# Normalized input — {sd.name}\n",
        f"_Ingested at {datetime.now().astimezone().isoformat(timespec='seconds')}_\n",
    ]
    errors = []

    for p in sorted(input_dir.iterdir()):
        if not p.is_file() or p.name.startswith("."):
            continue
        try:
            parts.append(process_artifact(p, sd))
        except IngestError as e:
            log(sd, f"ingest error on {p.name}: {e.detail}")
            errors.append({
                "file": p.name,
                "user_message": e.user_message,
                "detail": e.detail,
            })

    # If every attachment failed and the only text we got is the header,
    # hard-fail: write ingest_failed.json and exit 3.
    real_body = "".join(parts[2:]).strip()
    if errors and not real_body:
        failure = {
            "failed_at": datetime.now().astimezone().isoformat(timespec="seconds"),
            "errors": errors,
            # First error's user_message is what the orchestrator should send
            # to the Requester. Collapse multiple to one if they all share
            # the same root cause.
            "lark_message": _compose_lark_message(errors),
        }
        (sd / "ingest_failed.json").write_text(
            json.dumps(failure, indent=2, ensure_ascii=False)
        )
        # Still write a skeleton normalized.md so downstream readers don't
        # crash, but mark it clearly.
        normalized.write_text(
            "# Normalized input — INGEST FAILED\n\n"
            + failure["lark_message"] + "\n"
        )
        print(failure["lark_message"])
        sys.exit(3)

    # Soft-fail: some artifacts failed but at least one succeeded. Append the
    # error messages to the normalized text so the Requester sees them during
    # confirm-topic too.
    if errors:
        parts.append("\n\n## ⚠️ 部分附件没法处理\n\n")
        for e in errors:
            parts.append(f"- **{e['file']}**: {e['user_message']}\n")

    normalized.write_text("\n".join(parts))
    print(f"wrote {normalized}")


def _compose_lark_message(errors):
    """Collapse multiple errors into one Lark-ready message."""
    if len(errors) == 1:
        return errors[0]["user_message"]
    lines = ["我这边处理不了你发的附件，具体:\n"]
    for e in errors:
        lines.append(f"- **{e['file']}**: {e['user_message']}")
    return "\n".join(lines)


if __name__ == "__main__":
    main()
