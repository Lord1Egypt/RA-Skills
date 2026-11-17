"""SRT/VTT subtitle serializer (Pretty Printer).

Implements :class:`SubtitleSerializer` with three entry points:

- :meth:`SubtitleSerializer.to_srt` — format entries as SubRip (``.srt``).
- :meth:`SubtitleSerializer.to_vtt` — format entries as WebVTT (``.vtt``).
- :meth:`SubtitleSerializer.write_file` — write a serialized string to disk
  using UTF-8 encoding (R3.4).

Normal Form
-----------

The serializer emits a deterministic, round-trippable *Normal Form* so
that ``parse(serialize(entries))`` is equivalent to ``entries`` under the
relation defined in :mod:`translation_dubbing_skill.models.subtitle_entry`
(see R4.1–R4.3).

- Timestamps use ``HH:MM:SS,mmm`` for SRT and ``HH:MM:SS.mmm`` for VTT.
- Line endings are LF (``\\n``) only.
- Entries are separated by exactly one blank line (``\\n\\n`` between the
  last text line of one entry and the index/timestamp line of the next).
- The output ends with a trailing ``\\n`` so text editors and downstream
  tooling see a canonical newline-terminated file.
- Each text line has its trailing whitespace stripped; interior and
  leading whitespace is preserved because the equivalence relation only
  looks at trailing whitespace.
- CRLF or lone CR sequences inside ``SubtitleEntry.text`` are normalized
  to LF before emission, so round-tripping Windows-authored input
  produces a canonical LF-only Normal Form.
- The per-entry ``index`` field is preserved in the SRT output and is
  emitted as a cue identifier in the VTT output, so round-trips retain
  the original ordinal even when it does not start at 1 or has gaps.
- The VTT output starts with the mandatory ``WEBVTT`` header followed by
  a blank line (per the WebVTT spec), so the parser's header sniffing
  succeeds.

Corresponds to requirements R3.1, R3.2, R3.3, R3.4.
"""

from __future__ import annotations

from pathlib import Path
from typing import Final, Iterable

from translation_dubbing_skill.models import SubtitleEntry

# Milliseconds per second / minute / hour. Kept as named constants so the
# timestamp formatting logic stays self-documenting.
_MS_PER_SECOND: Final[int] = 1_000
_MS_PER_MINUTE: Final[int] = 60 * _MS_PER_SECOND
_MS_PER_HOUR: Final[int] = 60 * _MS_PER_MINUTE

# VTT spec permits ``HH:MM:SS.mmm`` with hours up to three digits; the
# serializer emits exactly two digits for hours (matching common player
# behaviour) and lets the parser accept up to three digits on input.
_HH_MM_SS_MMM_TEMPLATE: Final[str] = "{hours:02d}:{minutes:02d}:{seconds:02d}{sep}{millis:03d}"


def _format_timestamp(ms: int, sep: str) -> str:
    """Format a millisecond timestamp as ``HH:MM:SS<sep>mmm``.

    Negative millisecond values are a programmer error (the parser and
    the dataclass contract guarantee non-negative timestamps), so this
    helper raises :class:`ValueError` instead of silently clamping.
    """
    if ms < 0:
        raise ValueError(f"timestamp must be non-negative, got {ms}")
    hours, remainder = divmod(ms, _MS_PER_HOUR)
    minutes, remainder = divmod(remainder, _MS_PER_MINUTE)
    seconds, millis = divmod(remainder, _MS_PER_SECOND)
    return _HH_MM_SS_MMM_TEMPLATE.format(
        hours=hours,
        minutes=minutes,
        seconds=seconds,
        sep=sep,
        millis=millis,
    )


def _normalize_text_lines(text: str) -> list[str]:
    """Split ``text`` into lines and strip trailing whitespace per line.

    CRLF and lone CR sequences are unified to LF first so the Normal Form
    is stable across platforms.
    """
    unified = text.replace("\r\n", "\n").replace("\r", "\n")
    return [line.rstrip() for line in unified.split("\n")]


class SubtitleSerializer:
    """Pretty-printer for :class:`SubtitleEntry` lists.

    The class is stateless; instances exist so callers can depend on a
    stable interface without importing module-level functions.
    """

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def to_srt(self, entries: Iterable[SubtitleEntry]) -> str:
        """Serialize ``entries`` as SubRip (``.srt``) text.

        Each entry is emitted as::

            <index>
            HH:MM:SS,mmm --> HH:MM:SS,mmm
            <text line 1>
            <text line 2>
            ...

        Entries are separated by a single blank line, and the result ends
        with a trailing ``\\n``. An empty entry list produces an empty
        string (not ``"\\n"``) so callers can distinguish "no content" from
        "one empty cue".
        """
        blocks = [self._format_srt_block(entry) for entry in entries]
        if not blocks:
            return ""
        return "\n\n".join(blocks) + "\n"

    def to_vtt(self, entries: Iterable[SubtitleEntry]) -> str:
        """Serialize ``entries`` as WebVTT (``.vtt``) text.

        The output begins with the mandatory ``WEBVTT`` header followed
        by a blank line, then one block per entry::

            <index>
            HH:MM:SS.mmm --> HH:MM:SS.mmm
            <text line 1>
            ...

        Each block uses the entry's ``index`` as the cue identifier so
        round-tripping preserves the original ordinal. Entries are
        separated by a single blank line and the result ends with a
        trailing ``\\n``.
        """
        header = "WEBVTT\n"
        blocks = [self._format_vtt_block(entry) for entry in entries]
        if not blocks:
            # Header-only VTT is still valid; emit a trailing newline so
            # the file ends canonically.
            return header
        return header + "\n" + "\n\n".join(blocks) + "\n"

    def write_file(self, path: Path | str, content: str) -> None:
        """Write ``content`` to ``path`` using UTF-8 encoding (R3.4).

        ``newline=""`` disables Python's universal-newlines translation
        so the LF-only Normal Form produced by :meth:`to_srt` and
        :meth:`to_vtt` survives the write verbatim, even on Windows.
        """
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("w", encoding="utf-8", newline="") as fp:
            fp.write(content)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _format_srt_block(entry: SubtitleEntry) -> str:
        start = _format_timestamp(entry.start_ms, sep=",")
        end = _format_timestamp(entry.end_ms, sep=",")
        lines = [str(entry.index), f"{start} --> {end}"]
        lines.extend(_normalize_text_lines(entry.text))
        return "\n".join(lines)

    @staticmethod
    def _format_vtt_block(entry: SubtitleEntry) -> str:
        start = _format_timestamp(entry.start_ms, sep=".")
        end = _format_timestamp(entry.end_ms, sep=".")
        # Emit the ordinal as a cue identifier so parsers that assign
        # sequential indices (including our own) can still recover the
        # original numbering during a round-trip.
        lines = [str(entry.index), f"{start} --> {end}"]
        lines.extend(_normalize_text_lines(entry.text))
        return "\n".join(lines)


__all__ = ["SubtitleSerializer"]
