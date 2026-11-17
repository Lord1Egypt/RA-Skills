"""Clean a YouTube auto-caption WebVTT file into sentence-level cues.

YouTube's auto-generated captions have three artefacts that hurt
downstream translation quality:

1. Inline timing markers like ``<00:00:00.200><c> is</c>``.
2. A rolling 2-line window where each cue's first line is the tail of
   the previous cue (for on-screen scrolling).
3. Cues that wrap at an arbitrary character budget — a single English
   sentence routinely spans 3–5 cues, which gives a per-cue translator
   no complete clause to work with.

The cleaner performs two passes:

* **Pass 1** strips inline markup and collapses the rolling window so
  every remaining cue carries exactly the "new" line added by that cue
  (one atomic unit of on-screen text).
* **Pass 2** re-packs atomic lines into *sentence* cues whose start/end
  spans the underlying atomic cues' time range. A sentence boundary is
  any ``.``, ``!``, ``?`` (with optional trailing quotes/brackets), or
  a long-ish pause between atomic cues. Time stamps are carried over
  from the underlying atomic cues, so the re-packed cue's start == first
  atomic start and end == last atomic end.

Run::

    python scripts/clean_youtube_vtt.py <input.vtt> <output.vtt>
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

# ---------------------------------------------------------------------------
# Low-level YouTube artefacts
# ---------------------------------------------------------------------------

_INLINE_TIMESTAMP_RE = re.compile(r"<\d{2}:\d{2}:\d{2}\.\d{3}>")
_C_TAG_RE = re.compile(r"</?c(?:\.[^>]*)?>")
# Accept both ``HH:MM:SS.mmm`` (WebVTT) and ``HH:MM:SS,mmm`` (SubRip)
# separators in a single pattern so we can parse either format with the
# same regex.
_TIMESTAMP_LINE_RE = re.compile(
    r"^(?P<start>\d{1,3}:\d{2}:\d{2}[.,]\d{3})\s*-->\s*(?P<end>\d{1,3}:\d{2}:\d{2}[.,]\d{3})"
)

# Sentence-terminator punctuation allowed at a sentence boundary,
# optionally followed by closing quotes/brackets (e.g. ``he said.")``).
_SENTENCE_END_RE = re.compile(r"[.!?…][\"'\]\)]*\s*$")

# In-line sentence-boundary splitter. We match a sentence terminator
# (``.``, ``!``, ``?``, ``…``) followed by an optional closing quote /
# bracket, whitespace, and a capital letter starting the next sentence.
# The capital-letter requirement keeps decimals like ``6,830.`` intact —
# the next character is always a digit there, never uppercase. Python's
# lookbehind requires fixed-width so we match the terminator inside a
# non-capturing group and use ``re.split`` with a positive trailing
# match to reconstruct the split position in :func:`_merge_into_sentences`.
_SENTENCE_SPLIT_RE = re.compile(
    r"([.!?…][\"'\]\)]?)\s+(?=[A-Z\u4e00-\u9fff])"
)

# A *hard* sentence boundary is reached when we see one of these + a
# word boundary, even if there is no whitespace after. Keeps e.g.
# "Mr." / "6,830." from being split, while still reacting to the end of
# a real sentence.
_HARD_TERMINATORS: tuple[str, ...] = (".", "!", "?", "…")

# If two atomic cues are separated by more than this many milliseconds of
# silence, treat it as a sentence boundary even when punctuation is
# missing — YouTube sometimes drops the final period.
_PAUSE_BOUNDARY_MS = 1_200

# Upper bound for a single sentence cue before we force a split. Long
# uninterrupted speech (monologues, interview answers) often goes
# minutes without a period; without a cap the TTS step would be asked
# to synthesise the whole monologue as one audio clip and the
# translator would see a single giant input. Keeping cues below ~20 s
# keeps both downstream stages well-behaved; once the buffer reaches
# this duration we split at the nearest comma / conjunction.
_MAX_SENTENCE_MS = 20_000

# Same idea, as a character upper bound — regardless of how fast the
# speaker is talking, we never emit a single cue longer than this.
# 400 characters is roughly 25–40 seconds of speech in English.
_MAX_SENTENCE_CHARS = 400

# Soft sentence boundaries used when a hard terminator hasn't arrived
# but the buffer is already oversized. Order matters: we try commas
# first (most natural pause), then semicolons, then spaces before
# common conjunctions, then any whitespace as a last resort.
_SOFT_BOUNDARIES: tuple[str, ...] = (
    ", ",
    "; ",
    " — ",
    " and ",
    " but ",
    " so ",
    " because ",
    " which ",
    " that ",
)


# ---------------------------------------------------------------------------
# Timestamp helpers
# ---------------------------------------------------------------------------


def _ts_to_ms(ts: str) -> int:
    """Convert ``HH:MM:SS.mmm`` or ``HH:MM:SS,mmm`` to total milliseconds."""
    # SubRip uses a comma separator; WebVTT uses a dot. Both forms show
    # up in the wild (YouTube auto-captions export as either).
    ts = ts.replace(",", ".")
    h, m, rest = ts.split(":")
    s, ms = rest.split(".")
    return int(h) * 3_600_000 + int(m) * 60_000 + int(s) * 1_000 + int(ms)


def _ms_to_ts(ms: int) -> str:
    """Inverse of :func:`_ts_to_ms`, padded to the canonical WebVTT width."""
    h, r = divmod(ms, 3_600_000)
    m, r = divmod(r, 60_000)
    s, ms_only = divmod(r, 1_000)
    return f"{h:02d}:{m:02d}:{s:02d}.{ms_only:03d}"


# ---------------------------------------------------------------------------
# Pass 1 — markup stripping + rolling-window dedup
# ---------------------------------------------------------------------------


def _strip_inline_markup(text: str) -> str:
    """Remove ``<c>`` tags and inline timestamps; trim each line."""
    text = _INLINE_TIMESTAMP_RE.sub("", text)
    text = _C_TAG_RE.sub("", text)
    return text.strip()


@dataclass
class _AtomicCue:
    """Single atomic line produced by the de-rolled Pass 1."""

    start_ms: int
    end_ms: int
    text: str


def _parse_cues(vtt_text: str) -> list[_AtomicCue]:
    """Parse raw VTT or SRT into atomic (single-line) cues after removing rolling.

    Handles both formats:
      * WebVTT — starts with a ``WEBVTT`` header, timestamps use ``.``.
      * SubRip — each cue begins with an integer index line, timestamps
        use ``,``. No file-level header.

    Each returned cue has exactly one line of text (the newest line
    contributed by that cue), with inline markup stripped.
    """
    normalised = vtt_text.replace("\r\n", "\n").replace("\r", "\n").lstrip("\ufeff")
    lines = normalised.split("\n")

    raw_cues: list[tuple[int, int, str]] = []
    i = 0

    # Skip the WEBVTT header and any metadata before the first blank
    # line. SRT files have no header — the first non-blank line is
    # either a cue identifier or an integer index, both of which the
    # block loop below handles.
    if i < len(lines) and lines[i].startswith("WEBVTT"):
        i += 1
        while i < len(lines) and lines[i].strip() != "":
            i += 1

    while i < len(lines):
        while i < len(lines) and lines[i].strip() == "":
            i += 1
        if i >= len(lines):
            break

        # Cue may start with an identifier line (no ``-->``).
        if "-->" not in lines[i]:
            i += 1
            if i >= len(lines):
                break

        match = _TIMESTAMP_LINE_RE.match(lines[i].strip())
        if match is None:
            # Malformed block; skip to next blank.
            while i < len(lines) and lines[i].strip() != "":
                i += 1
            continue

        start_ms = _ts_to_ms(match.group("start"))
        end_ms = _ts_to_ms(match.group("end"))
        i += 1

        text_lines: list[str] = []
        while i < len(lines) and lines[i].strip() != "":
            text_lines.append(_strip_inline_markup(lines[i]))
            i += 1

        non_empty = [line for line in text_lines if line]
        text = "\n".join(non_empty).strip()
        raw_cues.append((start_ms, end_ms, text))

    # Dedup the rolling window: each cue's new content is its last line;
    # if that line equals the previous cue's last line, we just extend
    # the previous cue's end time.
    kept: list[_AtomicCue] = []
    last_emitted_line: str | None = None

    for start_ms, end_ms, text in raw_cues:
        if not text:
            continue
        lines_only = [line for line in text.split("\n") if line.strip()]
        if not lines_only:
            continue

        if last_emitted_line is None:
            # First real cue: emit every line it carries as separate atomic
            # cues so the downstream sentence builder gets every word.
            # Timestamps are evenly-divided across the lines so atomic
            # ordering is preserved.
            for j, line in enumerate(lines_only):
                span = end_ms - start_ms
                chunk_start = start_ms + (span * j) // max(1, len(lines_only))
                chunk_end = start_ms + (span * (j + 1)) // max(1, len(lines_only))
                kept.append(_AtomicCue(chunk_start, chunk_end, line))
            last_emitted_line = lines_only[-1]
            continue

        new_line = lines_only[-1]
        if new_line == last_emitted_line:
            # Pure duplicate: extend the previous atomic cue.
            kept[-1] = _AtomicCue(kept[-1].start_ms, end_ms, kept[-1].text)
            continue

        kept.append(_AtomicCue(start_ms, end_ms, new_line))
        last_emitted_line = new_line

    return kept


# ---------------------------------------------------------------------------
# Pass 2 — atomic cues → sentence cues
# ---------------------------------------------------------------------------


def _ends_with_sentence_terminator(text: str) -> bool:
    """Return True if ``text`` ends at a real sentence boundary.

    A trailing ``.``/``!``/``?``/``…`` counts; allowances are made for a
    following quote or closing bracket (``he said."``). The check is
    intentionally strict about the *last* non-whitespace character so we
    don't treat decimal numbers or honorifics as sentence breaks.
    """
    stripped = text.rstrip()
    if not stripped:
        return False
    # Trim trailing quotes/brackets before inspecting the terminator so
    # patterns like ``word."`` and ``word.)`` still register.
    while stripped and stripped[-1] in "\"'])":
        stripped = stripped[:-1]
    if not stripped:
        return False
    return stripped[-1] in _HARD_TERMINATORS


def _trailing_overlap(buffer: str, atom_text: str) -> int:
    """Return how many trailing characters of ``buffer`` came from ``atom_text``.

    The join separator is a single space (see the buffer-building loop
    in :func:`_merge_into_sentences`); beyond that, ``atom_text`` is
    appended verbatim. So the trailing overlap is either ``len(atom_text)``
    (when the atom is entirely inside the buffer) or whatever initial
    prefix of the atom still fits in the buffer. We clamp to
    ``len(atom_text)`` to keep callers' time-proportioning arithmetic
    stable.
    """
    n = min(len(buffer), len(atom_text))
    while n > 0 and not buffer.endswith(atom_text[:n]):
        n -= 1
    return n


def _force_split_if_oversized(
    sentences: list[_AtomicCue],
    atoms: list[_AtomicCue],
    current_atom: _AtomicCue,
    buffer_start_idx: int,
    buffer_end_idx: int,
    buffer_text: str,
    current_index: int,
) -> tuple[str, int] | None:
    """Emit a soft-boundary cue when the sentence buffer outgrows its budget.

    Monologue-style speech (interviews, lectures) can go minutes
    without a terminator; without a safety net we'd pile the whole
    monologue into one cue and starve the downstream translator / TTS
    of anything workable.

    When a split fires this helper:
      * appends the emitted sentence to ``sentences``,
      * returns the new ``(buffer_text, buffer_start_idx)`` the caller
        should use for the subsequent loop iteration.

    Returns ``None`` when no split was needed or possible, so the
    caller can keep its existing buffer state.

    Split strategy, in order:
      1. Soft terminator (``, `` / ``; `` / ``— ``) near the tail of
         the buffer; keeps the split reading naturally.
      2. A common conjunction (``and``, ``but``, ``so``, ``because``,
         ``which``, ``that``) with whitespace on both sides.
      3. As an absolute fallback, the last whitespace character in
         the second half of the buffer — we never split mid-word.
    """
    span_ms = current_atom.end_ms - atoms[buffer_start_idx].start_ms
    if span_ms < _MAX_SENTENCE_MS and len(buffer_text) < _MAX_SENTENCE_CHARS:
        return None

    head_end = _find_soft_split_point(buffer_text)
    if head_end is None:
        return None

    head = buffer_text[:head_end]
    tail = buffer_text[head_end:].lstrip()
    if not head.strip() or not tail:
        return None

    # Proportion the current atom's time based on how much of the atom
    # landed inside the emitted head — same trick as the hard-split path.
    atom_text = current_atom.text
    overlap = _trailing_overlap(head, atom_text)
    atom_span = max(1, current_atom.end_ms - current_atom.start_ms)
    if len(atom_text):
        split_ms = current_atom.start_ms + (atom_span * overlap) // len(atom_text)
    else:
        split_ms = current_atom.end_ms

    sentences.append(
        _AtomicCue(
            start_ms=atoms[buffer_start_idx].start_ms,
            end_ms=split_ms,
            text=re.sub(r"\s+", " ", head).strip(),
        )
    )
    return tail, current_index


def _find_soft_split_point(buffer_text: str) -> int | None:
    """Pick a split offset inside ``buffer_text`` at a natural pause.

    Searches the second half of the buffer so we offload the
    middle/end of an oversized buffer rather than emit a tiny cue
    when a comma happens to appear near the start.
    """
    start = len(buffer_text) // 2
    search_region = buffer_text[start:]
    best_offset: int | None = None
    for boundary in _SOFT_BOUNDARIES:
        found = search_region.rfind(boundary)
        if found == -1:
            continue
        # Keep the comma / semicolon attached to the head.
        split = start + found + len(boundary.rstrip())
        if best_offset is None or split > best_offset:
            best_offset = split
    if best_offset is not None:
        return best_offset

    fallback = buffer_text.rfind(" ", start)
    if fallback != -1:
        return fallback + 1
    return None


def _merge_into_sentences(atoms: list[_AtomicCue]) -> list[_AtomicCue]:
    """Collapse atomic cues into sentence-level cues.

    Strategy: join every atomic cue's text with a space into a running
    buffer and split that buffer on sentence boundaries whenever we
    encounter one. A boundary is either:

      * An intra-text terminator (``.``/``!``/``?``/``…``) followed by
        whitespace and an upper-case letter — caught by
        :data:`_SENTENCE_SPLIT_RE`; this handles the "``… huge position.
        So, if we …``" case where several sentences land inside a
        single atomic cue.
      * A silent pause longer than ``_PAUSE_BOUNDARY_MS`` between two
        adjacent atomic cues — YouTube occasionally drops the final
        period at scene / speaker changes.

    Timestamps are propagated proportionally when an atomic cue
    contributes to more than one output sentence: each completed
    sentence gets a ``(start, end)`` taken from the slice of original
    atomic cues that contributed characters to it, which keeps the
    result aligned with the video timeline without fractional
    sub-atomic precision that we can't defend.
    """
    sentences: list[_AtomicCue] = []
    # Running characters waiting to be emitted, together with the index
    # of the first and last atomic cue that contributed to them.
    buffer_text = ""
    buffer_start_idx: int | None = None
    buffer_end_idx: int | None = None

    def _flush_buffer() -> None:
        nonlocal buffer_text, buffer_start_idx, buffer_end_idx
        if not buffer_text.strip() or buffer_start_idx is None or buffer_end_idx is None:
            buffer_text = ""
            buffer_start_idx = None
            buffer_end_idx = None
            return
        sentences.append(
            _AtomicCue(
                start_ms=atoms[buffer_start_idx].start_ms,
                end_ms=atoms[buffer_end_idx].end_ms,
                text=re.sub(r"\s+", " ", buffer_text).strip(),
            )
        )
        buffer_text = ""
        buffer_start_idx = None
        buffer_end_idx = None

    for i, atom in enumerate(atoms):
        # Pause boundary — emit whatever we have before taking in the
        # next atom.
        if buffer_end_idx is not None:
            prev_end = atoms[buffer_end_idx].end_ms
            if atom.start_ms - prev_end >= _PAUSE_BOUNDARY_MS:
                _flush_buffer()

        if buffer_start_idx is None:
            buffer_start_idx = i
        buffer_end_idx = i
        buffer_text = (buffer_text + " " + atom.text) if buffer_text else atom.text

        # Punctuation splits inside the (growing) buffer. Keep splitting
        # from the front so every completed sentence gets its own cue.
        # ``_SENTENCE_SPLIT_RE`` captures the terminator in group 1 so
        # the sentence we emit keeps its trailing period / question
        # mark; the whitespace + next-sentence lookahead is consumed.
        #
        # When the split occurs *inside* an atomic cue's contribution,
        # we proportion the atom's time window between the emitted head
        # and the residual tail. This avoids having adjacent sentences
        # share the same atom's full end timestamp (which would look
        # like overlapping cues to downstream tooling).
        while True:
            match = _SENTENCE_SPLIT_RE.search(buffer_text)
            if match is None:
                break
            head_end = match.start() + len(match.group(1))
            tail_start = match.end()
            head = buffer_text[:head_end]
            tail = buffer_text[tail_start:]

            # Work out how far into the *current* atom we should draw
            # the sentence boundary. ``head_in_atom_chars`` counts the
            # characters in the current atom that belong to the emitted
            # sentence — i.e. everything from the atom's original text
            # up to, and including, the terminator.
            atom_text = atom.text
            # ``head`` ends at the terminator; its last ``len(atom_text)``
            # characters (or fewer) came from this atom. Find how many.
            overlap = _trailing_overlap(head, atom_text)
            span = max(1, atom.end_ms - atom.start_ms)
            if len(atom_text):
                split_ms = atom.start_ms + (span * overlap) // len(atom_text)
            else:
                split_ms = atom.end_ms

            sentences.append(
                _AtomicCue(
                    start_ms=atoms[buffer_start_idx].start_ms,
                    end_ms=split_ms,
                    text=re.sub(r"\s+", " ", head).strip(),
                )
            )
            buffer_text = tail
            # Tail continues from ``split_ms`` inside the current atom,
            # so we pin ``buffer_start_idx`` to this atom and remember
            # the in-atom offset. Subsequent flushes will read
            # ``atoms[buffer_start_idx].start_ms`` which is the atom's
            # own start — that can sit a little earlier than the split
            # for this one transitional cue, which is acceptable: the
            # scheduler's aligner truncates overshoots gracefully.
            buffer_start_idx = i

        # Oversize safety net: if no hard terminator has arrived for a
        # long time, force a soft split so downstream stages never see
        # an enormous single cue. This matters for monologue-style
        # speech (interviews, classes) where the speaker can go
        # minutes between periods.
        if buffer_start_idx is not None and buffer_end_idx is not None:
            split_result = _force_split_if_oversized(
                sentences,
                atoms,
                atom,
                buffer_start_idx,
                buffer_end_idx,
                buffer_text,
                i,
            )
            if split_result is not None:
                buffer_text, buffer_start_idx = split_result
                buffer_end_idx = i

    _flush_buffer()
    return sentences


# ---------------------------------------------------------------------------
# Serialization
# ---------------------------------------------------------------------------


def _render_vtt(sentences: list[_AtomicCue]) -> str:
    """Render ``sentences`` as a deterministic WebVTT document."""
    lines = ["WEBVTT", ""]
    for index, cue in enumerate(sentences, start=1):
        lines.append(str(index))
        lines.append(f"{_ms_to_ts(cue.start_ms)} --> {_ms_to_ts(cue.end_ms)}")
        lines.append(cue.text)
        lines.append("")
    return "\n".join(lines)


def _render_srt(sentences: list[_AtomicCue]) -> str:
    """Render ``sentences`` as a deterministic SubRip document."""
    lines: list[str] = []
    for index, cue in enumerate(sentences, start=1):
        # SRT uses a comma between seconds and milliseconds.
        start = _ms_to_ts(cue.start_ms).replace(".", ",")
        end = _ms_to_ts(cue.end_ms).replace(".", ",")
        lines.append(str(index))
        lines.append(f"{start} --> {end}")
        lines.append(cue.text)
        lines.append("")
    return "\n".join(lines)


def clean(vtt_text: str, *, output_format: str = "vtt") -> str:
    """Return a cleaned, sentence-merged subtitle document.

    Args:
        vtt_text: Raw input text (WebVTT or SubRip).
        output_format: ``"vtt"`` to emit WebVTT, ``"srt"`` to emit SubRip.
            Defaults to ``"vtt"`` so the original behaviour of the script
            (single ``.vtt`` in / ``.vtt`` out) is preserved.
    """
    atoms = _parse_cues(vtt_text)
    sentences = _merge_into_sentences(atoms)
    if output_format.lower() == "srt":
        return _render_srt(sentences)
    return _render_vtt(sentences)


def main() -> int:
    parser = argparse.ArgumentParser(description="Clean a YouTube auto-caption .vtt / .srt file.")
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    vtt_text = args.input.read_text(encoding="utf-8")
    output_format = "srt" if args.output.suffix.lower() == ".srt" else "vtt"
    cleaned = clean(vtt_text, output_format=output_format)
    args.output.write_text(cleaned, encoding="utf-8")

    original_cues = vtt_text.count("-->")
    cleaned_cues = cleaned.count("-->")
    print(f"cues: {original_cues} -> {cleaned_cues}")
    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
