"""Light subdomain sweep - common prefixes + wildcard detection.

Kept GENTLE: a small wordlist of common subdomain prefixes, one request each,
with a short pause between probes. This is NOT a full subdomain enumeration
(that's for subfinder/assetfinder); it's just enough to catch the obvious ones
(mail, dev, staging, api, admin, wp, blog, test, www, app).

Wildcard DNS is detected first: if every random label answers with the same
response as a real prefix, the prefix is not reported as a live host.
"""
from __future__ import annotations

import secrets
import time
from typing import List, Tuple

from ..config import Config
from ..finding import CheckResult, Finding, Severity
from ..http import probe
from ..util import base_domain, strip_host
from .base import Check

# common, high-value subdomain prefixes
PREFIXES = [
    "www", "mail", "dev", "staging", "stage", "test", "staging1",
    "api", "app", "admin", "blog", "wp", "shop", "status", "help",
    "dashboard", "portal", "docs", "cdn", "assets", "static",
    "git", "ci", "ci2", "build", "internal", "private",
    "old", "new", "beta", "alpha", "preview",
    "oauth", "auth", "login", "sso",
]

# Codes that mean "there is no host here" (or we are being rate-limited).
_ABSENT_CODES = {404, 410, 429}


def _is_live_code(code: int | None) -> bool:
    return code is not None and code < 500 and code not in _ABSENT_CODES


def _signature(res: dict) -> Tuple[object, str, str]:
    """Rough fingerprint used to recognise a wildcard catch-all."""
    ct = (res.get("content_type") or "").split(";")[0].strip().lower()
    body = (res.get("body") or "")[:200]
    return (res.get("code"), ct, body)


class SubdomainCheck(Check):
    name = "subdomains"
    description = "Light sweep of common subdomain prefixes + wildcard detection"

    def run(self, target: str, cfg: Config) -> CheckResult:
        findings: List[Finding] = []
        host = strip_host(target)
        base = base_domain(host)
        # strip leading www. from the base so we don't probe www.www
        if base.startswith("www."):
            base = base[4:]
        if "." not in base:
            return CheckResult(self.name, "skipped", summary="need a real domain")

        # 1. wildcard probe with an unlikely label
        wildcard_label = f"recon-{secrets.token_hex(6)}.{base}"
        wildcard = probe(f"https://{wildcard_label}", cfg, body_bytes=512)
        wildcard_sig = _signature(wildcard) if _is_live_code(wildcard["code"]) else None
        if wildcard_sig:
            findings.append(Finding(
                self.name,
                f"Wildcard DNS detected (*.{base} answers HTTP {wildcard['code']})",
                Severity.INFO,
                f"https://{wildcard_label} → HTTP {wildcard['code']} "
                f"{wildcard.get('content_type', '')}",
                "Wildcard responses are filtered out of the live-subdomain list below.",
            ))

        found: List[str] = []
        wildcard_filtered: List[str] = []
        probed = 0
        for p in PREFIXES[: cfg.max_subdomains]:
            sub = f"{p}.{base}"
            res = probe(f"https://{sub}", cfg, body_bytes=512)
            probed += 1
            code = res["code"]
            if not _is_live_code(code):
                time.sleep(0.05)
                continue
            if wildcard_sig is not None and _signature(res) == wildcard_sig:
                wildcard_filtered.append(sub)
                time.sleep(0.05)
                continue
            found.append(sub)
            findings.append(Finding(
                self.name, f"subdomain live: {sub} (HTTP {code})", Severity.LOW,
                f"https://{sub} → HTTP {code} {res.get('content_type', '')}",
                "Probe it: same stack? Same headers? Different security posture?",
            ))
            time.sleep(0.05)

        if wildcard_filtered:
            findings.append(Finding(
                self.name,
                f"{len(wildcard_filtered)} prefix(es) matched the wildcard response "
                f"and were not counted as live",
                Severity.INFO,
                ", ".join(wildcard_filtered),
            ))
        if not found:
            findings.append(Finding(
                self.name, "No common subdomains resolved", Severity.INFO,
                "Tried: " + ", ".join(PREFIXES[:10]) + ", …",
                "Wildcard or clean DNS. For full enumeration use subfinder/assetfinder (out of scope here).",
            ))

        summary = f"{len(found)} of {probed} probed subdomains live"
        return CheckResult(self.name, "ok", findings, summary)
