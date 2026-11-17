"""SRT/VTT subtitle parser.

Implements :class:`SubtitleParser` with three entry points:

- :meth:`SubtitleParser.parse_srt` — parses SubRip (``.srt``) text.
- :meth:`SubtitleParser.parse_vtt` — parses WebVTT (``.vtt``) text.
- :meth:`SubtitleParser.parse_auto` — dispatches based on a caller-provided
  hint or by sniffing the ``WEBVTT`` header.

Format overview
---------------

SRT
    Blocks separated by blank lines. Each block has:

        1. An integer index line (1-based, per the SubRip convention).
        2. A timestamp line ``HH:MM:SS,mmm --> HH:MM:SS,mmm``.
        3. Zero or more text lines until the next blank line or EOF.

VTT
    The file opens with a ``WEBVTT`` line (optionally followed by whitespace
    and a free-form header text on the same line). Cue blocks are separated
    by blank lines and consist of:

        1. Optional cue identifier line (ignored for indexing).
        2. Timestamp line ``HH:MM:SS.mmm --> HH:MM:SS.mmm`` (also accepts
           the short ``MM:SS.mmm`` form on either side).
        3. Zero or more text lines.

    ``NOTE``, ``STYLE``, and ``REGION`` blocks are skipped. Because cue
    identifiers are free-form, this parser assigns sequential 1-based
    indices to every cue regardless of whether an identifier was present.

Error model
-----------

- Syntax violations raise :class:`SubtitleParseError` with
  ``context={"line_number": N}`` where ``N`` is the 1-based line at which
  the offending content was seen.
- Timestamps where ``start_ms > end_ms`` raise
  :class:`InvalidTimestampError` with ``context={"entry_index": N}``
  where ``N`` is the 1-based index of the affected cue as reported in
  the output list.

Both errors subclass :class:`SkillError` and carry the canonical
``stage="parsing"`` tag.

Corresponds to requirements R2.1, R2.2, R2.3, R2.4, R2.5.
"""

from __future__ import annotations

import re
from typing import Final, Literal

from translation_dubbing_skill.errors import (
    InvalidTimestampError,
    SubtitleParseError,
)
from translation_dubbing_skill.models import SubtitleEntry

# Unicode BOM that may appear at the start of SRT/VTT files produced on
# Windows editors. Stripped before parsing.
_BOM: Final[str] = "\ufeff"

# SRT timestamps use a comma as the millisecond separator; VTT uses a dot.
# The short ``MM:SS.mmm`` form is WebVTT-only.
_SRT_TIMESTAMP_RE: Final[re.Pattern[str]] = re.compile(
    r"^(\d{1,3}):([0-5]?\d):([0-5]?\d),(\d{1,3})$"
)
_VTT_TIMESTAMP_RE: Final[re.Pattern[str]] = re.compile(
    r"^(?:(\d{1,3}):)?([0-5]?\d):([0-5]?\d)\.(\d{1,3})$"
)

_TIMESTAMP_ARROW: Final[str] = "-->"


def _split_lines(text: str) -> list[str]:
    """Split ``text`` into lines, treating CRLF/CR/LF uniformly.

    Unlike :meth:`str.splitlines`, this routine preserves a trailing empty
    line when the input ends with a newline so that line numbers reported
    to the caller remain stable. Consecutive newline boundaries therefore
    produce empty strings, which block-parsers interpret as block
    separators.
    """
    unified = text.replace("\r\n", "\n").replace("\r", "\n")
    # ``split`` preserves an empty trailing field when the input ends with
    # ``\n``; that is the behaviour we want so that blank-line delimiters
    # near EOF are still observed.
    return unified.split("\n")


def _parse_srt_timestamp(token: str, line_number: int) -> int:
    """Parse a single SRT timestamp (``HH:MM:SS,mmm``) into milliseconds."""
    match = _SRT_TIMESTAMP_RE.match(token)
    if match is None:
        raise SubtitleParseError(
            f"invalid SRT timestamp {token!r}",
            context={"line_number": line_number, "token": token},
        )
    hours, minutes, seconds, millis = (int(g) for g in match.groups())
    # Pad/truncate the millisecond field so ``,9`` means 900ms, ``,10``
    # means 100ms, and ``,123`` means 123ms — matching de-facto SRT
    # tooling behaviour.
    raw_ms = match.group(4)
    millis = int(raw_ms.ljust(3, "0")[:3])
    return ((hours * 60 + minutes) * 60 + seconds) * 1000 + millis


def _parse_vtt_timestamp(token: str, line_number: int) -> int:
    """Parse a single VTT timestamp (``[HH:]MM:SS.mmm``) into milliseconds."""
    match = _VTT_TIMESTAMP_RE.match(token)
    if match is None:
        raise SubtitleParseError(
            f"invalid VTT timestamp {token!r}",
            context={"line_number": line_number, "token": token},
        )
    hours = int(match.group(1)) if match.group(1) is not None else 0
    minutes = int(match.group(2))
    seconds = int(match.group(3))
    raw_ms = match.group(4)
    millis = int(raw_ms.ljust(3, "0")[:3])
    return ((hours * 60 + minutes) * 60 + seconds) * 1000 + millis


def _split_timestamp_line(
    line: str, line_number: int
) -> tuple[str, str]:
    """Split a ``A --> B`` timestamp line, ignoring trailing VTT settings.

    VTT timestamp lines may carry cue settings after the end timestamp
    (e.g. ``align:start line:50%``) separated by whitespace; those are
    stripped here because the parser does not model cue settings.
    """
    if _TIMESTAMP_ARROW not in line:
        raise SubtitleParseError(
            f"expected timestamp line containing '-->', got {line!r}",
            context={"line_number": line_number},
        )
    left, _, right = line.partition(_TIMESTAMP_ARROW)
    start_token = left.strip()
    # For VTT, ``right`` may carry trailing cue settings after whitespace.
    # For SRT those settings are not defined but tolerating them does no
    # harm — the timestamp regex still validates the leading token.
    end_token = right.strip().split(None, 1)[0] if right.strip() else ""
    if not start_token or not end_token:
        raise SubtitleParseError(
            f"missing start or end timestamp in {line!r}",
            context={"line_number": line_number},
        )
    return start_token, end_token


class SubtitleParser:
    """Parser for SRT and WebVTT subtitle text.

    The class is stateless; instances exist only so callers can depend on
    a stable interface without importing module-level functions.
    """

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def parse_srt(self, text: str) -> list[SubtitleEntry]:
        """Parse SRT subtitle text into a list of :class:`SubtitleEntry`.

        Raises:
            SubtitleParseError: the text is not valid SRT.
            InvalidTimestampError: a cue has ``start_ms > end_ms``.
        """
        return self._parse_srt(self._prepare(text))

    def parse_vtt(self, text: str) -> list[SubtitleEntry]:
        """Parse VTT subtitle text into a list of :class:`SubtitleEntry`.

        Raises:
            SubtitleParseError: the text is not valid WebVTT (including a
                missing ``WEBVTT`` header).
            InvalidTimestampError: a cue has ``start_ms > end_ms``.
        """
        return self._parse_vtt(self._prepare(text))

    def parse_auto(
        self,
        text: str,
        hint_format: Literal["srt", "vtt"] | None = None,
    ) -> list[SubtitleEntry]:
        """Parse text whose format is either hinted by the caller or sniffed.

        When ``hint_format`` is provided, the corresponding dedicated parser
        is used directly. Otherwise the text is sniffed: any text whose
        first non-empty line begins with ``WEBVTT`` (case-sensitive, per
        the WebVTT spec) is treated as VTT; everything else is parsed as
        SRT.
        """
        prepared = self._prepare(text)
        if hint_format == "srt":
            return self._parse_srt(prepared)
        if hint_format == "vtt":
            return self._parse_vtt(prepared)
        if hint_format is not None:
            raise ValueError(
                f"unsupported hint_format {hint_format!r}; "
                "expected 'srt', 'vtt', or None"
            )
        if self._looks_like_vtt(prepared):
            return self._parse_vtt(prepared)
        return self._parse_srt(prepared)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _prepare(text: str) -> str:
        """Strip a leading UTF-8 BOM if present; other normalization is
        deferred to :func:`_split_lines`."""
        if text.startswith(_BOM):
            return text[len(_BOM):]
        return text

    @staticmethod
    def _looks_like_vtt(text: str) -> bool:
        """Return whether ``text`` starts with a ``WEBVTT`` header line."""
        for raw_line in _split_lines(text):
            if raw_line == "":
                continue
            # The header is ``WEBVTT`` optionally followed by whitespace
            # and arbitrary description text. Anything else means SRT.
            return raw_line == "WEBVTT" or raw_line.startswith(("WEBVTT ", "WEBVTT\t"))
        return False

    # ------------------------------------------------------------------
    # SRT
    # ------------------------------------------------------------------

    def _parse_srt(self, text: str) -> list[SubtitleEntry]:
        lines = _split_lines(text)
        entries: list[SubtitleEntry] = []
        i = 0
        total = len(lines)

        while i < total:
            # Skip blank separators between blocks (and any leading blanks
            # at the top of the file).
            while i < total and lines[i].strip() == "":
                i += 1
            if i >= total:
                break

            index_line_number = i + 1
            index_text = lines[i].strip()
            try:
                original_index = int(index_text)
            except ValueError as exc:
                raise SubtitleParseError(
                    f"expected numeric SRT index, got {index_text!r}",
                    context={"line_number": index_line_number},
                ) from exc
            i += 1

            if i >= total:
                raise SubtitleParseError(
                    "missing timestamp line after SRT index",
                    context={"line_number": index_line_number},
                )

            timestamp_line_number = i + 1
            start_token, end_token = _split_timestamp_line(
                lines[i].strip(), timestamp_line_number
            )
            start_ms = _parse_srt_timestamp(start_token, timestamp_line_number)
            end_ms = _parse_srt_timestamp(end_token, timestamp_line_number)
            i += 1

            # Collect text lines up to the next blank line or EOF. Empty
            # entries are allowed — the subtitle block may have no text
            # lines at all (e.g. cue with only a timestamp).
            text_lines: list[str] = []
            while i < total and lines[i] != "":
                text_lines.append(lines[i])
                i += 1

            entry_index = len(entries) + 1
            if start_ms > end_ms:
                raise InvalidTimestampError(
                    f"start_ms ({start_ms}) > end_ms ({end_ms})",
                    context={
                        "entry_index": entry_index,
                        "start_ms": start_ms,
                        "end_ms": end_ms,
                    },
                )

            entries.append(
                SubtitleEntry(
                    index=original_index,
                    start_ms=start_ms,
                    end_ms=end_ms,
                    text="\n".join(text_lines),
                )
            )

        return entries

    # ------------------------------------------------------------------
    # VTT
    # ------------------------------------------------------------------

    def _parse_vtt(self, text: str) -> list[SubtitleEntry]:
        lines = _split_lines(text)
        total = len(lines)
        i = 0

        # Skip leading blank lines so a BOM-padded or awkwardly saved file
        # still validates, but the header itself must be the first
        # non-blank line.
        while i < total and lines[i] == "":
            i += 1
        if i >= total:
            raise SubtitleParseError(
                "empty VTT input: missing WEBVTT header",
                context={"line_number": 1},
            )

        header_line_number = i + 1
        header = lines[i]
        if not (
            header == "WEBVTT"
            or header.startswith(("WEBVTT ", "WEBVTT\t"))
        ):
            raise SubtitleParseError(
                f"VTT input must start with 'WEBVTT' header, got {header!r}",
                context={"line_number": header_line_number},
            )
        i += 1

        # Skip the rest of the header block (free-form description lines)
        # until the first blank line that terminates it.
        while i < total and lines[i] != "":
            i += 1

        entries: list[SubtitleEntry] = []

        while i < total:
            # Skip blank separators between blocks.
            while i < total and lines[i] == "":
                i += 1
            if i >= total:
                break

            # NOTE/STYLE/REGION blocks are metadata — consume through the
            # next blank line and move on.
            first = lines[i]
            first_stripped = first.strip()
            if (
                first_stripped == "NOTE"
                or first_stripped.startswith(("NOTE ", "NOTE\t"))
                or first_stripped == "STYLE"
                or first_stripped == "REGION"
            ):
                while i < total and lines[i] != "":
                    i += 1
                continue

            # A cue block may begin with an identifier line (any line
            # without ``-->``) followed by the timestamp line. Or it may
            # start directly with the timestamp line.
            timestamp_line_index: int
            if _TIMESTAMP_ARROW in first:
                timestamp_line_index = i
            else:
                # Identifier line present; timestamp must be on the next
                # non-blank line and must not itself be blank.
                if i + 1 >= total or lines[i + 1] == "":
                    raise SubtitleParseError(
                        "cue identifier not followed by a timestamp line",
                        context={"line_number": i + 1},
                    )
                timestamp_line_index = i + 1
                if _TIMESTAMP_ARROW not in lines[timestamp_line_index]:
                    raise SubtitleParseError(
                        f"expected timestamp line containing '-->', "
                        f"got {lines[timestamp_line_index]!r}",
                        context={"line_number": timestamp_line_index + 1},
                    )

            timestamp_line_number = timestamp_line_index + 1
            start_token, end_token = _split_timestamp_line(
                lines[timestamp_line_index].strip(), timestamp_line_number
            )
            start_ms = _parse_vtt_timestamp(start_token, timestamp_line_number)
            end_ms = _parse_vtt_timestamp(end_token, timestamp_line_number)
            i = timestamp_line_index + 1

            text_lines: list[str] = []
            while i < total and lines[i] != "":
                text_lines.append(lines[i])
                i += 1

            entry_index = len(entries) + 1
            if start_ms > end_ms:
                raise InvalidTimestampError(
                    f"start_ms ({start_ms}) > end_ms ({end_ms})",
                    context={
                        "entry_index": entry_index,
                        "start_ms": start_ms,
                        "end_ms": end_ms,
                    },
                )

            entries.append(
                SubtitleEntry(
                    index=entry_index,
                    start_ms=start_ms,
                    end_ms=end_ms,
                    text="\n".join(text_lines),
                )
            )

        return entries


__all__ = ["SubtitleParser"]
