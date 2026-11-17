"""OData quoting, clause building and JSON dimension keys.

Surface agnostic: both Vercel query APIs speak the same OData family, so
nothing here knows which one a clause is destined for. Which *operators* a
surface accepts is that surface's business; this module only ever emits ``eq``
and ``in``, which both surfaces document.
"""

from __future__ import annotations

import re
from collections.abc import Sequence

from . import ConfigError

#: One segment of a JSON dimension key, per the OpenAPI schema
#: ``^(flags)(/([0-9A-Za-z_]+|'([^']|'')*'))+$``: either bare word characters,
#: or a single quoted string whose embedded quotes are doubled.
_BARE_JSON_KEY_RE = re.compile(r"^[0-9A-Za-z_]+$")
_QUOTED_JSON_KEY_RE = re.compile(r"^'(?:[^']|'')*'$")

JSON_KEY_HELP = (
    "each key segment must be either bare letters, digits and underscores "
    "(flags/beta_banner) or a single quoted string with every embedded quote "
    "doubled (eventData/'sign-up', eventData/'it''s')"
)


def quote_odata(value: str) -> str:
    """Wrap a value in single quotes, doubling any quote it already contains."""
    escaped = value.replace("'", "''")
    return f"'{escaped}'"


def build_clause(dimension: str, value: str) -> str:
    """Build one filter clause for a dimension and a user supplied value.

    A comma separated value becomes an ``in (...)`` clause; anything else
    becomes an ``eq`` clause. Only operators the API documents are ever emitted.

    Raises:
        ConfigError: If the value is empty, or is only commas.
    """
    parts = [part.strip() for part in value.split(",")]
    parts = [part for part in parts if part]
    if not parts:
        raise ConfigError(
            f"filter value for {dimension} is empty; pass a value such as "
            f"{dimension}=example, or a comma separated list for a set"
        )
    if len(parts) == 1:
        return f"{dimension} eq {quote_odata(parts[0])}"
    joined = ", ".join(quote_odata(part) for part in parts)
    return f"{dimension} in ({joined})"


def _has_top_level_or(clause: str) -> bool:
    """True when ``clause`` contains an ``or`` outside quotes and parentheses."""
    depth = 0
    in_quote = False
    index = 0
    length = len(clause)
    while index < length:
        char = clause[index]
        if in_quote:
            if char == "'":
                if index + 1 < length and clause[index + 1] == "'":
                    index += 2
                    continue
                in_quote = False
        elif char == "'":
            in_quote = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth = max(0, depth - 1)
        elif depth == 0 and clause[index : index + 2].lower() == "or":
            before = clause[index - 1] if index > 0 else " "
            after = clause[index + 2] if index + 2 < length else " "
            if not _is_word_char(before) and not _is_word_char(after):
                return True
        index += 1
    return False


def _is_word_char(char: str) -> bool:
    return char.isalnum() or char == "_"


def combine_filters(clauses: Sequence[str]) -> str | None:
    """Join filter clauses with ``and``, protecting any top-level ``or``.

    Args:
        clauses: Individual OData clauses, in the order they should appear.

    Returns:
        The combined expression, or ``None`` when there is nothing to filter on.
    """
    cleaned = [clause.strip() for clause in clauses if clause and clause.strip()]
    if not cleaned:
        return None
    protected = [
        f"({clause})" if _has_top_level_or(clause) else clause for clause in cleaned
    ]
    return " and ".join(protected)


def split_key_segments(key: str) -> list[str] | None:
    """Split a JSON dimension key into its OData segments, honouring quotes.

    ``a/b`` is two segments, while ``'a/b'`` is one, because a slash inside a
    quoted segment is part of the key name rather than a separator.

    Returns:
        The segments, or ``None`` when a single quote is left unbalanced.
    """
    segments: list[str] = []
    current: list[str] = []
    index = 0
    length = len(key)
    in_quote = False
    while index < length:
        char = key[index]
        if in_quote:
            if char == "'":
                if index + 1 < length and key[index + 1] == "'":
                    current.append("''")
                    index += 2
                    continue
                in_quote = False
            current.append(char)
        elif char == "'":
            in_quote = True
            current.append(char)
        elif char == "/":
            segments.append("".join(current))
            current = []
        else:
            current.append(char)
        index += 1
    if in_quote:
        return None
    segments.append("".join(current))
    return segments


def is_valid_key_segment(segment: str) -> bool:
    """True for a segment the OpenAPI schema for ``by`` accepts.

    Bare segments are word characters only; anything else has to be a single
    quoted string with its embedded quotes doubled. An empty quoted segment is
    rejected because it names no key at all.
    """
    if _BARE_JSON_KEY_RE.match(segment):
        return True
    return bool(_QUOTED_JSON_KEY_RE.match(segment)) and segment != "''"


def _key_path_is_valid(key: str) -> bool:
    """True when every segment of a JSON dimension key is well formed."""
    segments = split_key_segments(key)
    if segments is None:
        return False
    return bool(segments) and all(is_valid_key_segment(seg) for seg in segments)


def validate_key_segments(base: str, name: str, key: str) -> None:
    """Check every segment of a JSON dimension key, naming the exact problem.

    Args:
        base: The JSON dimension base, for example ``eventData``.
        name: The dimension as the user wrote it, quoted back in the message.
        key: The part after the first slash.

    Raises:
        ConfigError: With the offending segment and the fix. Accepting a key
            that merely looks quoted is how extra OData gets injected into
            ``by`` and ``filter``, so anything not matching the schema is
            refused rather than passed through.
    """
    segments = split_key_segments(key)
    if segments is None:
        raise ConfigError(
            f"{name!r} leaves a single quote unbalanced in its key; {JSON_KEY_HELP}"
        )
    for segment in segments:
        if is_valid_key_segment(segment):
            continue
        if segment == "''" or not segment:
            raise ConfigError(f"{name!r} has an empty key segment; use {base}/plan")
        if "'" in segment:
            raise ConfigError(
                f"{name!r} has a key segment {segment!r} that is not a legal "
                f"quoted string; {JSON_KEY_HELP}"
            )
        raise ConfigError(
            f"{name!r} has a key with characters outside letters, digits and "
            f"underscores; single quote it as {base}/{quote_odata(segment)}"
        )


def json_dimension(base: str, key: str) -> str:
    """Compose a JSON dimension such as ``eventData/plan``, quoting when needed.

    A key that is already valid OData is passed through unchanged. A plain name
    carrying punctuation is quoted here rather than being left to the user. A
    key that is neither is rejected: accepting it verbatim because it merely
    looks quoted is how extra OData gets injected into ``by`` and ``filter``.

    Raises:
        ConfigError: If the key is empty, or cannot be made into a legal key.
    """
    name = key.strip()
    if not name:
        raise ConfigError(
            f"{base} needs a key, for example {base}/plan; an empty key groups by "
            "nothing"
        )
    if _key_path_is_valid(name):
        return f"{base}/{name}"
    if "'" in name or "/" in name:
        raise ConfigError(
            f"{base} key {name!r} is not a legal OData key: {JSON_KEY_HELP}"
        )
    return f"{base}/{quote_odata(name)}"
