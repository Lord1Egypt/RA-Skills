#!/usr/bin/env python3
"""Sidecar tool-output offloader.

Scans a JSONL transcript for large toolResult entries and moves their content
to sidecar files, replacing the inline content with a compact stub.

Usage:
    sidecar.py <jsonl_file> <session_id> [min_entry_bytes]

Sidecar layout:
    <jsonl_dir>/<session_id>.toolcache/<tool-call-id>.txt

Stub format (replaces inline content):
    [tool output offloaded to .toolcache/<tool-call-id>.txt — <N> bytes.
     Use the Read tool to access it if needed.]

- Idempotent: entries already containing a stub are skipped.
- Atomic write: original is overwritten only if ≥1 entry was changed.
- Restart-safe: sidecar files are adjacent to the transcript, survive gateway
  restarts and config changes.

Exits:
    0 — success (even if nothing was sidecared)
    1 — error
"""
import json
import os
import sys
import shutil
from pathlib import Path
from datetime import datetime, timezone

STUB_MARKER = "[tool output offloaded to"
IMAGE_STUB_MARKER = "[image offloaded to"
DEFAULT_MIN_BYTES = 5120  # 5 KB per entry
IMAGE_MIN_BYTES = 1024  # 1 KB — offload any non-trivial base64 image


def entry_content_size(entry: dict) -> int:
    """Return approximate byte size of a toolResult entry's content."""
    raw = entry.get("message", {}).get("content", [])
    if isinstance(raw, str):
        return len(raw.encode("utf-8"))
    total = 0
    for block in raw:
        if isinstance(block, dict) and block.get("type") == "text":
            total += len(block.get("text", "").encode("utf-8"))
    return total


def is_already_stubbed(entry: dict) -> bool:
    raw = entry.get("message", {}).get("content", [])
    if isinstance(raw, str):
        return STUB_MARKER in raw
    for block in raw:
        if isinstance(block, dict) and block.get("type") == "text":
            if STUB_MARKER in block.get("text", ""):
                return True
    return False


def extract_text(entry: dict) -> str:
    """Extract full text content from a toolResult entry."""
    raw = entry.get("message", {}).get("content", [])
    if isinstance(raw, str):
        return raw
    parts = []
    for block in raw:
        if isinstance(block, dict) and block.get("type") == "text":
            parts.append(block.get("text", ""))
    return "\n".join(parts)


def make_stub_content(sidecar_filename: str, byte_count: int) -> list:
    return [
        {
            "type": "text",
            "text": (
                f"{STUB_MARKER} .toolcache/{sidecar_filename} — {byte_count} bytes. "
                "Use the Read tool to access it if needed.]"
            ),
        }
    ]


def offload_images_in_entry(entry, toolcache_dir, session_id, img_counter):
    """Scan any entry's content for inline base64 images and offload them.

    Returns (modified_entry, count_offloaded, new_img_counter).
    """
    import copy
    import base64

    msg = entry.get("message", {})
    content = msg.get("content", [])
    if not isinstance(content, list):
        return entry, 0, img_counter

    modified = False
    new_content = []
    offloaded = 0

    for block in content:
        if not isinstance(block, dict):
            new_content.append(block)
            continue

        # Check for inline base64 image: {type: "image", data: "<base64>"}
        if block.get("type") == "image" and block.get("data"):
            b64_data = block["data"]
            if len(b64_data) < IMAGE_MIN_BYTES:
                new_content.append(block)
                continue

            # Already offloaded?
            if IMAGE_STUB_MARKER in b64_data:
                new_content.append(block)
                continue

            # Determine extension from mimeType
            mime = block.get("mimeType", block.get("media_type", "image/jpeg"))
            ext = {"image/jpeg": ".jpg", "image/png": ".png",
                   "image/gif": ".gif", "image/webp": ".webp"}.get(mime, ".jpg")

            entry_id = entry.get("id", f"unk-{img_counter}")
            safe_id = "".join(c if c.isalnum() or c in "-." else "_" for c in entry_id)
            sidecar_filename = f"{safe_id}_img_{img_counter}{ext}"
            sidecar_path = toolcache_dir / sidecar_filename

            # Decode and write binary image
            toolcache_dir.mkdir(parents=True, exist_ok=True)
            try:
                img_bytes = base64.b64decode(b64_data)
                sidecar_path.write_bytes(img_bytes)
            except Exception:
                # Fallback: write raw base64 as text
                sidecar_path.write_text(b64_data, encoding="utf-8")
            actual_bytes = sidecar_path.stat().st_size

            # Replace image block with text stub
            stub_text = (
                f"{IMAGE_STUB_MARKER} .toolcache/{sidecar_filename} — "
                f"{actual_bytes} bytes ({mime}). "
                f"Use the Read/image tool to access it if needed.]"
            )
            new_content.append({"type": "text", "text": stub_text})
            offloaded += 1
            img_counter += 1

            b64_kb = len(b64_data) // 1024
            print(f"  offloaded image ({entry_id[:12]}): {b64_kb}KB b64 → .toolcache/{sidecar_filename}")
            modified = True
            continue

        # Also handle Anthropic-style source.data images:
        # {type: "image", source: {type: "base64", media_type: "...", data: "..."}}
        if block.get("type") == "image" and isinstance(block.get("source"), dict):
            src = block["source"]
            b64_data = src.get("data", "")
            if len(b64_data) < IMAGE_MIN_BYTES:
                new_content.append(block)
                continue
            if IMAGE_STUB_MARKER in b64_data:
                new_content.append(block)
                continue

            mime = src.get("media_type", "image/jpeg")
            ext = {"image/jpeg": ".jpg", "image/png": ".png",
                   "image/gif": ".gif", "image/webp": ".webp"}.get(mime, ".jpg")

            entry_id = entry.get("id", f"unk-{img_counter}")
            safe_id = "".join(c if c.isalnum() or c in "-." else "_" for c in entry_id)
            sidecar_filename = f"{safe_id}_img_{img_counter}{ext}"
            sidecar_path = toolcache_dir / sidecar_filename

            toolcache_dir.mkdir(parents=True, exist_ok=True)
            try:
                img_bytes = base64.b64decode(b64_data)
                sidecar_path.write_bytes(img_bytes)
            except Exception:
                sidecar_path.write_text(b64_data, encoding="utf-8")
            actual_bytes = sidecar_path.stat().st_size

            stub_text = (
                f"{IMAGE_STUB_MARKER} .toolcache/{sidecar_filename} — "
                f"{actual_bytes} bytes ({mime}). "
                f"Use the Read/image tool to access it if needed.]"
            )
            new_content.append({"type": "text", "text": stub_text})
            offloaded += 1
            img_counter += 1

            b64_kb = len(b64_data) // 1024
            print(f"  offloaded image ({entry_id[:12]}): {b64_kb}KB b64 → .toolcache/{sidecar_filename}")
            modified = True
            continue

        new_content.append(block)

    if not modified:
        return entry, 0, img_counter

    new_entry = copy.deepcopy(entry)
    new_entry["message"]["content"] = new_content
    return new_entry, offloaded, img_counter


def main():
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <jsonl_file> <session_id> [min_entry_bytes]", file=sys.stderr)
        sys.exit(1)

    jsonl_path = Path(sys.argv[1])
    session_id = sys.argv[2]
    min_bytes = int(sys.argv[3]) if len(sys.argv) > 3 else DEFAULT_MIN_BYTES

    if not jsonl_path.exists():
        print(f"ERROR: {jsonl_path} not found", file=sys.stderr)
        sys.exit(1)

    # Read transcript
    entries = []
    with open(jsonl_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"WARN: skipping malformed line: {e}", file=sys.stderr)
                continue

    if not entries:
        print("No entries — nothing to do")
        sys.exit(0)

    # Sidecar dir adjacent to the transcript
    toolcache_dir = jsonl_path.parent / f"{session_id}.toolcache"
    sidecared = 0
    images_offloaded = 0
    img_counter = 0
    changed = []

    for entry in entries:
        # --- Phase 1: offload inline base64 images from ANY entry ---
        entry, img_count, img_counter = offload_images_in_entry(
            entry, toolcache_dir, session_id, img_counter
        )
        images_offloaded += img_count

        # --- Phase 2: offload large toolResult text (existing behavior) ---
        msg = entry.get("message", {})
        if msg.get("role") != "toolResult":
            changed.append(entry)
            continue

        if is_already_stubbed(entry):
            changed.append(entry)
            continue

        size = entry_content_size(entry)
        if size < min_bytes:
            changed.append(entry)
            continue

        # Determine sidecar filename
        tcid = msg.get("toolCallId") or msg.get("id") or f"unknown-{sidecared}"
        # Sanitize for filesystem
        safe_id = "".join(c if c.isalnum() or c in "-_." else "_" for c in tcid)
        sidecar_filename = f"{safe_id}.txt"
        sidecar_path = toolcache_dir / sidecar_filename

        # Extract text and write to sidecar
        text = extract_text(entry)
        toolcache_dir.mkdir(parents=True, exist_ok=True)
        sidecar_path.write_text(text, encoding="utf-8")
        actual_bytes = sidecar_path.stat().st_size

        # Replace content with stub
        import copy
        new_entry = copy.deepcopy(entry)
        new_entry["message"]["content"] = make_stub_content(sidecar_filename, actual_bytes)
        new_entry["message"]["_sidecaredBytes"] = actual_bytes
        changed.append(new_entry)
        sidecared += 1

        tool_name = msg.get("toolName", "tool")
        print(
            f"  sidecared {tool_name} ({tcid[:12]}): "
            f"{actual_bytes // 1024}KB → .toolcache/{sidecar_filename}"
        )

    total_offloaded = sidecared + images_offloaded
    if total_offloaded == 0:
        print(f"No entries exceeded {min_bytes} bytes — nothing sidecared")
        sys.exit(0)

    # Atomic write
    tmp_path = jsonl_path.with_suffix(".jsonl.sidecar-tmp")
    with open(tmp_path, "w", encoding="utf-8") as f:
        for entry in changed:
            f.write(json.dumps(entry) + "\n")

    shutil.move(str(tmp_path), str(jsonl_path))

    orig_kb = sum(len(json.dumps(e)) for e in entries) // 1024
    new_kb = jsonl_path.stat().st_size // 1024
    parts = []
    if sidecared:
        parts.append(f"{sidecared} tool outputs")
    if images_offloaded:
        parts.append(f"{images_offloaded} images")
    print(
        f"Sidecar complete: {' + '.join(parts)} offloaded, "
        f"{orig_kb}KB → {new_kb}KB "
        f"(sidecar dir: {toolcache_dir})"
    )
    sys.exit(0)


if __name__ == "__main__":
    main()
