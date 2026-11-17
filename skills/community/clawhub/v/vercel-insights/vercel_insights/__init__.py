"""Read-only command line client for Vercel's analytics query APIs.

This package answers the everyday questions about a Vercel project: how many
page views and visitors it had, which pages and referrers drove them, where the
visitors came from, and how custom events break down.

Read-only guarantee
-------------------
Every request this package can issue comes from a fixed operation allowlist in
:mod:`vercel_insights.http`. The dispatcher takes an operation key, never a
method or a host, so no user input can select, extend or override an entry. The
access token is only ever placed in the ``Authorization`` header, never in a
URL, a query parameter, a log line, an exception, or any rendered output.

This module holds only what every other module needs: the version, the API
root, and the exception types. It deliberately imports no submodule, so the
dependency graph inside the package stays acyclic.
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from typing import Any

VERSION = "1.1.1"

#: The REST API root. Every allowlisted operation is built from this prefix.
BASE_URL = "https://api.vercel.com"

#: The dashboard host. Exactly one operation lives here rather than on
#: :data:`BASE_URL`: Vercel serves historical request logs from
#: ``vercel.com/api/logs/request-logs``, which is what the official CLI calls
#: and the only endpoint that answers a "what broke in the last hour" question.
#: The documented alternative on api.vercel.com is an endless stream, and the
#: metrics route needs Observability Plus. See docs/api-notes.md.
LOGS_BASE_URL = "https://vercel.com"

DOCS_TOKEN_URL = "https://vercel.com/docs/rest-api#creating-an-access-token"

#: Rows collapsed by the API once ``limit`` is exceeded arrive under this label.
OTHERS_LABEL = "Others"

__all__ = [
    "BASE_URL",
    "DOCS_TOKEN_URL",
    "LOGS_BASE_URL",
    "OTHERS_LABEL",
    "VERSION",
    "ApiError",
    "ConfigError",
    "RateLimitError",
    "sanitize_label",
    "sanitize_message",
]


# ---------------------------------------------------------------------------
# The untrusted-input boundary
# ---------------------------------------------------------------------------

#: Every C0 control character, DEL, and every C1 control character. Anything a
#: response carries is remote input in the strongest sense: a UTM campaign is
#: whatever a visitor typed into a query string, and request paths, referrer
#: hostnames, event names, routes, a server supplied error message and a
#: ``Location`` header are no better. Any of them can carry an ANSI escape
#: sequence, a carriage return that rewrites the line already printed, or a byte
#: that breaks a CSV cell open, so the whole class is escaped rather than any one
#: sequence being pattern matched.
_CONTROL_CHARACTERS = re.compile(r"[\x00-\x1f\x7f-\x9f]")


def _escape_control(match: re.Match[str]) -> str:
    """Render one control character as a visible, unambiguous escape."""
    return f"\\x{ord(match.group()):02x}"


def sanitize_label(text: str) -> str:
    """Make a response-derived string safe to print, in any output format.

    Control characters become visible escapes (``\\x1b`` for ESC), so the value
    still reads as what came back rather than being silently dropped, and can
    no longer move the cursor, set a colour, blank the screen, forge a plausible
    looking second line of output, or split a row across two lines of CSV.
    Everything else, printable Unicode included, is left exactly as the API sent
    it.

    This lives in the package root rather than in :mod:`vercel_insights.render`
    because it guards more than labels: metric names claimed from a response
    become column headers, and :mod:`vercel_insights.http` puts a ``Location``
    header and Vercel's own error message straight onto stderr.
    """
    return _CONTROL_CHARACTERS.sub(_escape_control, text)


#: Same class as above minus the line feed, for text where line structure is
#: part of the meaning.
_CONTROL_EXCEPT_NEWLINE = re.compile(r"[\x00-\x09\x0b-\x1f\x7f-\x9f]")


def sanitize_message(text: str) -> str:
    """Neutralise a multi-line server message while keeping it readable.

    An API error body is often pretty-printed JSON, and escaping its newlines
    turns a legible complaint into one long line of ``\\x0a`` noise, which is
    exactly when a reader most needs to read it. So line feeds survive here,
    unlike in :func:`sanitize_label`.

    The reason newlines are escaped elsewhere is that a server-supplied string
    could otherwise start a line of its own and forge something plausible, for
    example ``error: everything fine``, under this tool's own prefix. Indenting
    every line after the first removes that: nothing the server sends can reach
    column zero, so a forged line is visibly quoted rather than impersonating
    the program's own output. Every other control character is still escaped.
    """
    escaped = _CONTROL_EXCEPT_NEWLINE.sub(_escape_control, text)
    first, sep, rest = escaped.partition("\n")
    if not sep:
        return first
    indented = "\n".join(f"  {line}" for line in rest.split("\n"))
    return f"{first}\n{indented}"


class ConfigError(Exception):
    """A configuration or usage problem detected before any network call.

    Every ``ConfigError`` message names the offending value and the fix, and is
    reported to the user as a single line with exit code 2.
    """


class ApiError(Exception):
    """The API returned an error, or the network failed after every retry.

    ``message`` holds Vercel's ``error.message`` verbatim whenever the response
    carried one. The rendered string prefixes it with the HTTP status and the
    API error code, and notes the attempt count when retries were used up.
    """

    def __init__(
        self,
        status: int | None,
        code: str | None,
        message: str,
        *,
        attempts: int = 1,
    ) -> None:
        self.status = status
        self.code = code
        self.message = message
        self.attempts = attempts
        super().__init__(self._render())

    def _render(self) -> str:
        prefix = f"HTTP {self.status}" if self.status is not None else "Network error"
        if self.code:
            prefix = f"{prefix} ({self.code})"
        text = f"{prefix}: {self.message}"
        if self.attempts > 1:
            text = f"{text} [gave up after {self.attempts} attempts]"
        return text

    def __str__(self) -> str:
        return self._render()


class RateLimitError(ApiError):
    """A ``rate_limited`` response. ``limit`` holds Vercel's limit object."""

    def __init__(
        self,
        status: int | None,
        code: str | None,
        message: str,
        *,
        attempts: int = 1,
        limit: Mapping[str, Any] | None = None,
    ) -> None:
        super().__init__(status, code, message, attempts=attempts)
        self.limit: Mapping[str, Any] = dict(limit or {})
