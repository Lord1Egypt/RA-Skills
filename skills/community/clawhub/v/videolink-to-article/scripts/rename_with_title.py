"""
Rename the final transcript file(s) in a per-task <WORK_DIR>/<video_id>/
directory to include the video title (sanitized) as a prefix, while keeping
the video_id as a stable suffix for uniqueness.

Since intermediate files (SRT, sentences.txt, metadata.json, etc.) are cleaned
up separately and not delivered, this script only handles the final transcript
output(s).

Usage:
    python rename_with_title.py <work_dir> [--dry-run]

    <work_dir> must contain a metadata.json with at minimum:
        { "video_id": "...", "title": "..." }

Behavior (which files get renamed):
- `transcript.md` and `transcript_*.md` (e.g. `transcript_translated_zh.md`)
  — renamed to include the sanitized title prefix.
- `metadata.json` — never renamed (needed until this script reads it).
- All other files — ignored (they will be cleaned up separately).

Result name format:
    <sanitized_title>__<video_id>.md
    <sanitized_title>__<video_id>_translated_zh.md

`__` (double underscore) is the title/id separator.

Sanitization rules:
- Strip Windows-illegal chars: <>:"/\\|?*
- Replace POSIX-illegal "/" with " "
- Collapse runs of whitespace to a single space
- Strip leading/trailing whitespace and dots (Windows quirk)
- Keep CJK and most Unicode unchanged — modern filesystems handle it fine
- Truncate to 80 visible chars to avoid 260-char Windows path limits;
  cut on a word/character boundary, not mid-codepoint

Exit codes:
    0 success (or nothing to do)
    1 bad CLI usage
    2 metadata.json missing or unreadable
    3 metadata.json missing required fields
"""
import sys, os, re, json, argparse, unicodedata

# Make our own stdout/stderr UTF-8 so log lines that include CJK filenames
# don't render as "???" on Windows consoles using a legacy code page.
for _stream_name in ("stdout", "stderr"):
    _stream = getattr(sys, _stream_name, None)
    if _stream is not None and hasattr(_stream, "reconfigure"):
        try:
            _stream.reconfigure(encoding="utf-8")
        except Exception:
            pass


ILLEGAL_WIN = re.compile(r'[<>:"/\\|?*\x00-\x1f]')
WHITESPACE = re.compile(r"\s+")
SEPARATOR = "__"   # title<sep>video_id

# Only the final transcript files are renamed
TRANSCRIPT_PATTERN = re.compile(r"^transcript(?:_([^.]+))?\.md$")
NEVER_RENAME = {"metadata.json"}


def sanitize_title(title: str, max_len: int = 80) -> str:
    """Convert a video title into a safe filename component."""
    if not title:
        return "untitled"
    t = unicodedata.normalize("NFC", title)
    t = ILLEGAL_WIN.sub(" ", t)
    t = WHITESPACE.sub(" ", t).strip()
    t = t.strip(" .")
    if not t:
        return "untitled"
    if len(t) > max_len:
        t = t[:max_len].rstrip(" .-_")
    return t or "untitled"


def main():
    ap = argparse.ArgumentParser(
        description="Rename final transcript file(s) to include the video title."
    )
    ap.add_argument("work_dir",
                    help="Per-task directory containing metadata.json and transcript files.")
    ap.add_argument("--dry-run", action="store_true",
                    help="Print what would be renamed without changing anything.")
    args = ap.parse_args()

    work = os.path.abspath(args.work_dir)
    meta_path = os.path.join(work, "metadata.json")
    if not os.path.isfile(meta_path):
        print(f"error: metadata.json not found in {work}", file=sys.stderr)
        sys.exit(2)
    try:
        with open(meta_path, "r", encoding="utf-8") as f:
            meta = json.load(f)
    except Exception as e:
        print(f"error: cannot read metadata.json: {e}", file=sys.stderr)
        sys.exit(2)

    vid = meta.get("video_id")
    title = meta.get("title")
    if not vid or not title:
        print("error: metadata.json missing required fields (video_id, title)", file=sys.stderr)
        sys.exit(3)

    safe = sanitize_title(title)
    new_prefix = f"{safe}{SEPARATOR}{vid}"

    renamed = 0
    skipped = 0
    for entry in sorted(os.listdir(work)):
        full = os.path.join(work, entry)
        if not os.path.isfile(full):
            continue
        if entry in NEVER_RENAME:
            continue

        m = TRANSCRIPT_PATTERN.match(entry)
        if not m:
            skipped += 1
            continue

        # Build new name: <title>__<vid>.md or <title>__<vid>_translated_zh.md
        suffix = m.group(1)  # e.g. "translated_zh" or None
        if suffix:
            new_name = f"{new_prefix}_{suffix}.md"
        else:
            new_name = f"{new_prefix}.md"

        # Skip if already renamed
        if entry == new_name:
            skipped += 1
            continue

        new_full = os.path.join(work, new_name)
        if os.path.exists(new_full):
            print(f"skip: target already exists: {new_name}", file=sys.stderr)
            continue
        if args.dry_run:
            print(f"DRY {entry}  ->  {new_name}")
        else:
            os.rename(full, new_full)
            print(f"rename {entry}  ->  {new_name}")
        renamed += 1

    summary = f"done: renamed={renamed} skipped={skipped}"
    if args.dry_run:
        summary = "[dry-run] " + summary
    print(summary)


if __name__ == "__main__":
    main()
