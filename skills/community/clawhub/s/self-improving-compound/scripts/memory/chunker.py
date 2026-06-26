"""Markdown → bounded chunks with stable sequence numbers.

Port of OpenHuman's `src/openhuman/memory/tree/chunker.rs` (814 lines → ~200).

Dispatch by source kind:
  - **Chat**: split at ``## `` message boundaries.
  - **Email**: split at ``---\nFrom:`` separators.
  - **Document**: paragraph-based greedy packing.

Oversize units fall back to a paragraph → line → character splitter.
"""

from __future__ import annotations

import datetime
from dataclasses import dataclass, field
from typing import List, Optional

from .types import Chunk, Metadata, SourceKind, approx_token_count, chunk_id

# Default upper bound on per-chunk tokens (3k → ~12k chars).
DEFAULT_CHUNK_MAX_TOKENS = 3_000


@dataclass
class ChunkerOptions:
    max_tokens: int = DEFAULT_CHUNK_MAX_TOKENS


@dataclass
class ChunkerInput:
    """Input to the chunker: the canonicalised source and its provenance."""
    source_kind: SourceKind
    source_id: str
    markdown: str
    metadata: Metadata


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def chunk_markdown(
    input: ChunkerInput,
    opts: ChunkerOptions = ChunkerOptions(),
) -> List[Chunk]:
    """Slice ``input.markdown`` into chunks ≤ ``opts.max_tokens`` tokens.

    Returns chunks in source order with stable sequence numbers starting at 0.
    Chunk IDs are deterministic, so re-chunking yields the same ids.
    """
    max_chars = max(1, opts.max_tokens * 4)
    now = datetime.datetime.now(datetime.timezone.utc)
    out: List[Chunk] = []

    # Dispatch by source kind.
    if input.source_kind == SourceKind.CHAT:
        units = _split_chat_messages(input.markdown)
        sep = ""
    elif input.source_kind == SourceKind.EMAIL:
        units = _split_email_messages(input.markdown)
        sep = "\n\n"
    else:
        # Document: paragraph-based.
        units = [input.markdown]
        sep = "\n\n"

    # If only one unit and small enough, return as-is.
    if len(units) == 1 and approx_token_count(units[0]) <= opts.max_tokens:
        cid = chunk_id(input.source_kind, input.source_id, 0, units[0])
        out.append(Chunk(
            id=cid,
            content=units[0],
            metadata=input.metadata,
            token_count=approx_token_count(units[0]),
            seq_in_source=0,
            created_at=now,
            partial_message=False,
        ))
        return out

    # Greedy pack units into chunks.
    acc: List[str] = []
    acc_chars = 0

    def flush() -> None:
        nonlocal acc, acc_chars
        if not acc:
            return
        merged = sep.join(acc)
        seq = len(out)
        cid = chunk_id(input.source_kind, input.source_id, seq, merged)
        out.append(Chunk(
            id=cid,
            content=merged,
            metadata=input.metadata,
            token_count=approx_token_count(merged),
            seq_in_source=seq,
            created_at=now,
            partial_message=False,
        ))
        acc = []
        acc_chars = 0

    for unit in units:
        unit_chars = len(unit)
        if unit_chars > max_chars:
            flush()
            # Oversize: sub-split the unit.
            for piece in _split_by_token_budget(unit, opts.max_tokens):
                seq = len(out)
                cid = chunk_id(input.source_kind, input.source_id, seq, piece)
                out.append(Chunk(
                    id=cid,
                    content=piece,
                    metadata=input.metadata,
                    token_count=approx_token_count(piece),
                    seq_in_source=seq,
                    created_at=now,
                    partial_message=True,
                ))
            continue

        projected = unit_chars if not acc else acc_chars + len(sep) + unit_chars
        if projected > max_chars:
            flush()
        if acc:
            acc_chars += len(sep)
        acc_chars += unit_chars
        acc.append(unit)

    flush()

    if not out:
        cid = chunk_id(input.source_kind, input.source_id, 0, "")
        out.append(Chunk(
            id=cid,
            content="",
            metadata=input.metadata,
            token_count=0,
            seq_in_source=0,
            created_at=now,
            partial_message=False,
        ))

    return out


# ---------------------------------------------------------------------------
# Chat splitter
# ---------------------------------------------------------------------------

def _split_chat_messages(md: str) -> List[str]:
    """Split at ``## `` boundaries. Each message becomes one unit."""
    pieces: List[str] = []
    current: Optional[str] = None
    for line in md.splitlines(keepends=True):
        if line.startswith("## "):
            if current is not None:
                trimmed = current.rstrip()
                if trimmed:
                    pieces.append(trimmed)
            current = line
        elif current is not None:
            current += line
    if current is not None:
        trimmed = current.rstrip()
        if trimmed:
            pieces.append(trimmed)
    if not pieces and md.strip():
        pieces.append(md.rstrip())
    return pieces


# ---------------------------------------------------------------------------
# Email splitter
# ---------------------------------------------------------------------------

def _split_email_messages(md: str) -> List[str]:
    """Split at ``---`` followed by ``From:`` within 8 lines."""
    lines = md.split("\n")
    n = len(lines)
    split_positions: List[int] = []
    for i in range(n):
        if lines[i].rstrip() == "---":
            window_end = min(i + 9, n)
            for j in range(i + 1, window_end):
                if lines[j].startswith("From:"):
                    split_positions.append(i)
                    break
                if lines[j].strip():
                    break
    if not split_positions:
        trimmed = md.rstrip()
        return [trimmed] if trimmed else []
    pieces: List[str] = []
    for idx, pos in enumerate(split_positions):
        start = pos
        end = split_positions[idx + 1] if idx + 1 < len(split_positions) else n
        piece_lines = lines[start:end]
        piece = "\n".join(piece_lines).rstrip()
        if piece:
            pieces.append(piece)
    return pieces


# ---------------------------------------------------------------------------
# Token-budget splitter
# ---------------------------------------------------------------------------

def _split_by_token_budget(text: str, max_tokens: int) -> List[str]:
    """Split text into pieces each ≤ max_tokens.

    Preference order:
    1. Paragraph (\\n\\n)
    2. Line (\\n)
    3. Hard character cut (preserving UTF-8)
    """
    max_tokens = max(1, max_tokens)
    if not text:
        return [""]
    if approx_token_count(text) <= max_tokens:
        return [text]

    max_chars = max_tokens * 4

    # Try paragraph split.
    paragraphs = text.split("\n\n")
    if len(paragraphs) > 1:
        result = _pack_segments(paragraphs, "\n\n", max_chars)
        if result is not None:
            return result

    # Fall back to line split.
    lines = text.split("\n")
    if len(lines) > 1:
        result = _pack_segments(lines, "\n", max_chars)
        if result is not None:
            return result

    # Hard character cut.
    return _hard_split_by_chars(text, max_chars)


def _pack_segments(segments: List[str], sep: str, max_chars: int) -> Optional[List[str]]:
    """Greedily pack segments into chunks ≤ max_chars.

    Returns None if any single segment exceeds max_chars.
    """
    sep_len = len(sep)
    out: List[str] = []
    current: List[str] = []
    current_chars = 0

    for seg in segments:
        seg_chars = len(seg)
        if seg_chars > max_chars:
            return None
        projected = seg_chars if not current else current_chars + sep_len + seg_chars
        if projected > max_chars:
            out.append(sep.join(current))
            current = []
            current_chars = 0
        if current:
            current_chars += sep_len
        current_chars += seg_chars
        current.append(seg)

    if current:
        out.append(sep.join(current))

    return out if out else None


def _hard_split_by_chars(text: str, max_chars: int) -> List[str]:
    """Split text by character count, preserving UTF-8 code points."""
    out: List[str] = []
    for i in range(0, len(text), max_chars):
        out.append(text[i:i + max_chars])
    return out if out else [""]
