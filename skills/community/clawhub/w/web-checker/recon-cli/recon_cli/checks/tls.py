"""TLS certificate check - SANs, expiry, signature, unexpected hostnames."""
from __future__ import annotations

import datetime
import re
import shutil
import subprocess
from email.utils import parsedate_to_datetime
from typing import List, Optional

from ..config import Config
from ..finding import CheckResult, Finding, Severity
from ..util import base_domain, strip_host
from .base import Check


def _openssl(host: str, port: int, cfg: Config) -> Optional[str]:
    if not shutil.which("openssl"):
        return None
    if not host or not re.fullmatch(r"[A-Za-z0-9._-]+", host):
        return None
    if not isinstance(port, int) or not 0 < port < 65536:
        return None
    try:
        p = subprocess.run(
            ["openssl", "s_client", "-connect", f"{host}:{port}", "-servername", host],
            input=b"\n",
            capture_output=True,
            timeout=cfg.timeout,
        )
        return p.stdout.decode("utf-8", errors="replace") + p.stderr.decode("utf-8", errors="replace")
    except Exception as e:  # noqa: BLE001
        return f"openssl error: {e}"


def _x509(s_client_out: str, cfg: Config) -> Optional[str]:
    """Extract subject/issuer/dates/SAN from openssl s_client output."""
    try:
        p = subprocess.run(
            ["openssl", "x509", "-noout", "-subject", "-issuer", "-dates",
             "-ext", "subjectAltName"],
            input=s_client_out.encode("utf-8"),
            capture_output=True,
            timeout=cfg.timeout,
        )
    except Exception:  # noqa: BLE001
        return None
    out = p.stdout.decode("utf-8", errors="replace")
    return out if p.returncode == 0 and out.strip() else None


def _signature(s_client_out: str, cfg: Config) -> Optional[str]:
    """Read the signature algorithm (not included in the short x509 dump)."""
    try:
        p = subprocess.run(
            ["openssl", "x509", "-noout", "-text"],
            input=s_client_out.encode("utf-8"),
            capture_output=True,
            timeout=cfg.timeout,
        )
    except Exception:  # noqa: BLE001
        return None
    out = p.stdout.decode("utf-8", errors="replace")
    m = re.search(r"Signature Algorithm:\s*(\S+)", out)
    return m.group(1) if m else None


def _expiry_finding(not_after: str) -> Optional[Finding]:
    try:
        expires = parsedate_to_datetime(not_after.strip())
    except (TypeError, ValueError):
        return None
    if expires.tzinfo is None:
        expires = expires.replace(tzinfo=datetime.timezone.utc)
    now = datetime.datetime.now(datetime.timezone.utc)
    days = (expires - now).days
    if days < 0:
        return Finding("tls", f"Certificate EXPIRED ({not_after.strip()})", Severity.HIGH,
                       f"notAfter: {not_after.strip()}",
                       "Renew the certificate immediately.")
    if days <= 14:
        return Finding("tls", f"Certificate expires in {days} day(s)", Severity.MED,
                       f"notAfter: {not_after.strip()}",
                       "Renew now and confirm automated renewal is working.")
    if days <= 30:
        return Finding("tls", f"Certificate expires in {days} day(s)", Severity.LOW,
                       f"notAfter: {not_after.strip()}",
                       "Check that automated renewal is configured.")
    return None


class TlsCheck(Check):
    name = "tls"
    description = "SANs, expiry, signature algorithm, unexpected hostnames on the cert"

    def run(self, target: str, cfg: Config) -> CheckResult:
        findings: List[Finding] = []
        host = strip_host(target)

        out = _openssl(host, 443, cfg)
        if out is None:
            return CheckResult(self.name, "skipped", error="openssl not available")
        if out.startswith("openssl error:"):
            return CheckResult(self.name, "error", error=out[:400])

        x = _x509(out, cfg)
        if x is None:
            return CheckResult(self.name, "error", error="could not read the certificate")

        findings.append(Finding(self.name, x.strip(), Severity.INFO, x.strip()[:400]))

        # SANs
        sans = re.findall(r"DNS:([^,\s]+)", x)
        if sans:
            findings.append(Finding(self.name, f"{len(sans)} SAN(s): {', '.join(sans)}", Severity.INFO,
                                 "Cert covers these hostnames. Any you don't expect = potential cross-tenant exposure."))
            expect = base_domain(host)
            for s in sans:
                # flag hostnames not matching our target's registrable domain
                if expect and expect not in s and s != host:
                    findings.append(Finding(self.name, f"SAN does not match target: {s}", Severity.LOW,
                                           f"cert SAN: {s}; target: {host}",
                                           "If this is a shared cert (Let's Encrypt multi-SAN), it's normal. "
                                           "Otherwise investigate - could be a misconfigured tenant."))
        else:
            findings.append(Finding(self.name, "No SAN found (unusual for modern certs)", Severity.MED,
                                   "Modern certs should have SAN. Investigate."))

        # expiry
        m = re.search(r"notAfter\s*=\s*([^,\n]+)", x)
        not_after = ""
        if m:
            not_after = m.group(1).strip()
            findings.append(Finding(self.name, f"notAfter: {not_after}", Severity.INFO,
                                   "Check it's not close to expiry (would cause cert errors)."))
            expiry = _expiry_finding(not_after)
            if expiry:
                findings.append(expiry)
        m = re.search(r"notBefore\s*=\s*([^,\n]+)", x)
        if m:
            findings.append(Finding(self.name, f"notBefore: {m.group(1).strip()}", Severity.INFO))

        # signature algorithm
        alg = _signature(out, cfg)
        if alg:
            if alg.lower() in ("sha256withrsaencryption", "ecdsa-with-sha256",
                               "sha384withrsaencryption", "ecdsa-with-sha384"):
                findings.append(Finding(self.name, f"Signature: {alg} (OK)", Severity.INFO))
            else:
                findings.append(Finding(self.name, f"Signature: {alg}", Severity.LOW,
                                       f"signatureAlgorithm: {alg}",
                                       "Prefer SHA-256+ / ECDSA. SHA-1 / MD5 are broken."))
        else:
            findings.append(Finding(self.name, "Signature algorithm: unknown", Severity.INFO))

        summary = f"{len(sans)} SAN(s); sig={alg or '?'}"
        return CheckResult(self.name, "ok", findings, summary)
