"""Subtitle entry data model and equivalence helpers.

Defines the core :class:`SubtitleEntry` dataclass used throughout the skill
(parsing, translation, TTS, alignment) and the text/entry equivalence helpers
underpinning the SRT/VTT round-trip correctness properties.

Equivalence (used by R4 round-trip properties)::

    a ≡ b  ⇔
      len(a) == len(b)
      ∧ ∀i. a[i].index    == b[i].index
      ∧ ∀i. a[i].start_ms == b[i].start_ms
      ∧ ∀i. a[i].end_ms   == b[i].end_ms
      ∧ ∀i. normalize_text(a[i].text) == normalize_text(b[i].text)

where :func:`normalize_text` unifies CRLF/CR → LF and strips trailing
whitespace from each line.

Corresponds to requirements R2.3 and R4.3.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class SubtitleEntry:
    """An immutable subtitle entry.

    Attributes:
        index: 1-based ordinal as it appears in the source subtitle stream.
        start_ms: Start time in milliseconds (inclusive).
        end_ms: End time in milliseconds (exclusive). Should be ``> start_ms``;
            parsers enforce this invariant and raise ``InvalidTimestampError``
            when violated.
        text: Subtitle text; may contain embedded newlines.
    """

    index: int
    start_ms: int
    end_ms: int
    text: str


def normalize_text(text: str) -> str:
    """Normalize subtitle text for equivalence comparison.

    Rules:
      - Unify line endings: ``\\r\\n`` and standalone ``\\r`` both become ``\\n``.
      - Strip trailing whitespace from each line.

    Leading whitespace and blank interior lines are preserved; only *trailing*
    whitespace on each line is removed. A fully-blank final line is likewise
    normalized (to an empty string) but not removed, so line counts stay
    stable across round-trips.

    Args:
        text: Raw subtitle text.

    Returns:
        Normalized text suitable for equivalence comparison.
    """
    # Unify CRLF and lone CR to LF first so splitlines-style processing is
    # consistent regardless of the platform that produced the input.
    unified = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = unified.split("\n")
    return "\n".join(line.rstrip() for line in lines)


def entries_equivalent(
    a: Sequence[SubtitleEntry],
    b: Sequence[SubtitleEntry],
) -> bool:
    """Return whether two subtitle entry sequences are equivalent.

    Two sequences are equivalent when they have the same length and every
    pair of entries agrees on ``index``, ``start_ms``, ``end_ms``, and
    ``normalize_text(text)``.

    Args:
        a: First sequence of entries.
        b: Second sequence of entries.

    Returns:
        ``True`` if the sequences are equivalent under the relation above,
        ``False`` otherwise.
    """
    if len(a) != len(b):
        return False
    for left, right in zip(a, b):
        if left.index != right.index:
            return False
        if left.start_ms != right.start_ms:
            return False
        if left.end_ms != right.end_ms:
            return False
        if normalize_text(left.text) != normalize_text(right.text):
            return False
    return True


__all__ = ["SubtitleEntry", "normalize_text", "entries_equivalent"]
