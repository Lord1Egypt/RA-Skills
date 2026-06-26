"""Parse the `Authentication-Results` header into SPF/DKIM/DMARC verdicts.

Used by pipeline stage 1's hard-gate for authoritative spoof detection.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

_METHOD_RE = re.compile(r"\b(spf|dkim|dmarc)\s*=\s*([a-z]+)", re.IGNORECASE)


@dataclass
class AuthVerdict:
    spf: str | None = None
    dkim: str | None = None
    dmarc: str | None = None

    @property
    def all_fail(self) -> bool:
        return all(v == "fail" for v in (self.spf, self.dkim, self.dmarc))

    @property
    def any_fail(self) -> bool:
        return any(v == "fail" for v in (self.spf, self.dkim, self.dmarc))


def parse_authentication_results(header: str | None) -> AuthVerdict:
    """Return SPF/DKIM/DMARC verdicts from a raw Authentication-Results header.

    Strips parenthetical reasons, lowercases values, and treats anything that
    isn't the literal string `fail` as not-a-fail (so `softfail`, `temperror`,
    `neutral`, `none` do NOT trip the stage-1 hard gate — matches real-world
    best practice per RFC 8601).
    """
    if not header:
        return AuthVerdict()

    verdict = AuthVerdict()
    for match in _METHOD_RE.finditer(header):
        method = match.group(1).lower()
        result = match.group(2).lower()
        if method == "spf" and verdict.spf is None:
            verdict.spf = result
        elif method == "dkim" and verdict.dkim is None:
            verdict.dkim = result
        elif method == "dmarc" and verdict.dmarc is None:
            verdict.dmarc = result
    return verdict
