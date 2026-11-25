"""DNS check - A/AAAA, CNAME, MX, NS, TXT. Uses `dig` if available, falls back to stdlib."""
from __future__ import annotations

import re
import shutil
import socket
import subprocess
from typing import List, Optional

from ..config import Config
from ..finding import CheckResult, Finding, Severity
from ..util import base_domain, strip_host
from .base import Check

_SAFE_DIG_HOST = re.compile(r"[A-Za-z0-9._-]+")


def _dig(host: str, rtype: str, timeout: float = 10.0) -> Optional[str]:
    if not shutil.which("dig"):
        return None
    if not host or not _SAFE_DIG_HOST.fullmatch(host):
        return None
    try:
        p = subprocess.run(
            ["dig", "+short", host, rtype],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return p.stdout.strip()
    except Exception:  # noqa: BLE001 - treat a failed lookup like "no dig"
        return None


def _resolve_a(host: str) -> List[str]:
    out = []
    try:
        for info in socket.getaddrinfo(host, None, socket.AF_INET):
            out.append(info[4][0])
    except Exception:  # noqa: BLE001
        pass
    return sorted(set(out))


def _resolve_aaaa(host: str) -> List[str]:
    out = []
    try:
        for info in socket.getaddrinfo(host, None, socket.AF_INET6):
            out.append(info[4][0])
    except Exception:  # noqa: BLE001
        pass
    return sorted(set(out))


def _cname(host: str, timeout: float) -> Optional[str]:
    out = _dig(host, "CNAME", timeout)
    if out and "error" not in out:
        first = out.splitlines()[0].strip().rstrip(".")
        if first:
            return first
    return None


def _mx(host: str, timeout: float) -> List[str]:
    out = _dig(host, "MX", timeout)
    if not out or "error" in out:
        return []
    return [l.strip() for l in out.splitlines() if l.strip()]


def _ns(domain: str, timeout: float) -> List[str]:
    out = _dig(domain, "NS", timeout)
    if not out or "error" in out:
        return []
    return [l.strip().rstrip(".") for l in out.splitlines() if l.strip()]


def _txt(host: str, timeout: float) -> List[str]:
    out = _dig(host, "TXT", timeout)
    if not out or "error" in out:
        return []
    return [l.strip().strip('"') for l in out.splitlines() if l.strip()]


def _spf_looks_open(spf_records: List[str]) -> bool:
    """Heuristic: SPF with -all is strict (good); +all / ~all / missing is open-ish."""
    joined = " ".join(spf_records)
    if "-all" in joined:
        return False
    if "+all" in joined:
        return True
    if not spf_records:
        return False  # no SPF; not necessarily open
    return "all" in joined  # ~all (softfail) - mildly permissive


class DnsCheck(Check):
    name = "dns"
    description = "A/AAAA, CNAME, MX, NS, TXT (SPF/DMARC) - map the network + email surface"

    def run(self, target: str, cfg: Config) -> CheckResult:
        findings: List[Finding] = []
        host = strip_host(target)
        domain = base_domain(host)

        # A records
        a = _dig(host, "A", cfg.timeout)
        if a is None:
            a_records = _resolve_a(host)
            src = "python-socket"
        else:
            a_records = [x for x in a.splitlines() if x.strip()]
            src = "dig"
        if a_records:
            findings.append(Finding(self.name, f"A: {', '.join(a_records)}  (via {src})", Severity.INFO,
                                 "; ".join(a_records)))
        else:
            findings.append(Finding(self.name, "No A record", Severity.LOW, "dig A returned nothing",
                                   "If this host is expected to resolve, investigate."))

        # AAAA
        aaaa = _dig(host, "AAAA", cfg.timeout)
        if aaaa is None:
            aaaa_records = _resolve_aaaa(host)
        else:
            aaaa_records = [x for x in aaaa.splitlines() if x.strip()]
        if aaaa_records:
            findings.append(Finding(self.name, f"AAAA: {', '.join(aaaa_records)}", Severity.INFO))

        # CNAME - a CNAME pointing at a shared platform is the #1 signal of a SaaS host
        cn = _cname(host, cfg.timeout)
        if cn:
            if any(t in cn.lower() for t in ("vercel", "cloudflare", "netlify", "heroku", "amazonaws", "fastly")):
                findings.append(Finding(self.name, f"CNAME → {cn}  (SaaS platform - likely Vercel/Cloudflare/Netlify)",
                                       Severity.INFO, f"CNAME {host} → {cn}",
                                       "Confirms shared infrastructure. Low risk but means: no direct port scans, no brute force - those hit the platform."))
            else:
                findings.append(Finding(self.name, f"CNAME → {cn}", Severity.INFO))

        # MX - email surface (separate from web surface). Mail records live on
        # the registrable domain, not on an arbitrary subdomain.
        mx = _mx(domain, cfg.timeout)
        if mx:
            findings.append(Finding(self.name, f"MX: {mx}", Severity.INFO,
                                   "Email is a separate attack surface - check SPF/DMARC next."))
        else:
            findings.append(Finding(self.name, "No MX (or inherited from parent)", Severity.INFO))

        # NS
        ns = _ns(domain, cfg.timeout)
        if ns:
            findings.append(Finding(self.name, f"NS: {', '.join(ns)}", Severity.INFO,
                                   "Authoritative DNS providers."))

        # TXT - SPF on the domain, DMARC at _dmarc.<domain>
        txt = _txt(domain, cfg.timeout)
        spf = [t for t in txt if t.lower().startswith("v=spf1")]
        dmarc = _txt(f"_dmarc.{domain}", cfg.timeout)
        if spf:
            for s in spf[:2]:
                findings.append(Finding(self.name, f"SPF: {s}", Severity.INFO, s,
                                       "SPF present. Verify it's not too permissive (check -all vs ~all vs +all)."))
                if _spf_looks_open([s]):
                    findings.append(Finding(self.name, f"SPF may be permissive: {s}", Severity.LOW, s,
                                           "Tighten to -all (hardfail) if you own the domain."))
        else:
            findings.append(Finding(self.name, "No SPF record on this domain", Severity.LOW,
                                   "No v=spf1 TXT. If this domain sends email, add SPF.",
                                   ))
        if not dmarc:
            findings.append(Finding(self.name, f"No DMARC record at _dmarc.{domain}", Severity.LOW,
                                   "No v=dmarc1 TXT. DMARC is the modern standard for email auth."))
        # other TXT (verifications, tokens) - could leak config
        other = [t for t in txt if t not in spf and len(t) > 10]
        for t in other[:5]:
            findings.append(Finding(self.name, f"TXT: {t[:80]}", Severity.INFO, t[:200],
                                   "Could be a 3rd-party verification token (Google/Cloudflare/MS). Informational."))

        summary = (f"A={len(a_records)}; AAAA={len(aaaa_records)}; "
                   f"CNAME={cn or '-'}; MX={len(mx)}; SPF={'yes' if spf else 'no'}; DMARC={'yes' if dmarc else 'no'}")
        return CheckResult(self.name, "ok", findings, summary)
