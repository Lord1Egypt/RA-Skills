"""Headers check - HSTS/preload, CSP, XCTO, CORS, redirect safety."""
from __future__ import annotations

import json
import re
from typing import Dict, List, Optional, Tuple

from ..config import Config
from ..finding import CheckResult, Finding, Severity
from ..http import get, head
from ..util import base_domain, strip_host
from .base import Check


def _normalise(raw: str) -> str:
    return raw.replace("\r\n", "\n").replace("\r", "\n")


def _parse_headers(raw: str) -> Dict[str, str]:
    """curl -D - output may include a status line; keep last header block."""
    # take the last HTTP/xxx status section if -L followed redirects
    blocks = re.split(r"\n\n(?=HTTP/)", _normalise(raw))
    last = blocks[-1] if blocks else raw
    headers: Dict[str, str] = {}
    for line in last.splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            headers[k.strip().lower()] = v.strip()
    return headers


def _all_header_blocks(raw: str) -> List[Dict[str, str]]:
    """Every status block in a redirect chain, in order (first→last)."""
    blocks = re.split(r"\n\n(?=HTTP/)", _normalise(raw))
    out: List[Dict[str, str]] = []
    for b in blocks:
        h: Dict[str, str] = {}
        for line in b.splitlines():
            if ":" in line:
                k, _, v = line.partition(":")
                h[k.strip().lower()] = v.strip()
        if h:
            out.append(h)
    return out


def _status_line(raw: str) -> str:
    first = next((l for l in raw.splitlines() if l.startswith("HTTP/")), "")
    last = raw.rstrip().splitlines()[-1] if raw else ""
    # status line is the first HTTP/ line (entry hop)
    return first or last


def _status_code(status_line: str) -> Optional[int]:
    m = re.match(r"HTTP/\S+\s+(\d{3})", status_line.strip())
    return int(m.group(1)) if m else None


def _parse_csp(value: str) -> Dict[str, str]:
    """Parse a CSP header into ``{directive: sources}`` (lowercased keys)."""
    out: Dict[str, str] = {}
    for part in value.split(";"):
        part = part.strip()
        if not part:
            continue
        bits = part.split()
        if not bits:
            continue
        out[bits[0].lower()] = " ".join(bits[1:])
    return out


def _csp_findings(value: str) -> List[Tuple[str, Severity, str, str]]:
    """Return (title, severity, evidence, recommendation) for a CSP header."""
    directives = _parse_csp(value)
    out: List[Tuple[str, Severity, str, str]] = []
    out.append(("Content-Security-Policy present", Severity.INFO,
                f"content-security-policy: {value}",
                "Review the policy against the actual script/style origins."))
    if "default-src" not in directives and "script-src" not in directives:
        out.append(("CSP has no default-src or script-src", Severity.LOW,
                    f"content-security-policy: {value}",
                    "Add a default-src or script-src directive; otherwise the policy barely constrains scripts."))
    script = directives.get("script-src", directives.get("default-src", ""))
    if "unsafe-inline" in script:
        out.append(("CSP script-src allows 'unsafe-inline'", Severity.LOW,
                    f"script-src: {script}",
                    "Prefer nonces or hashes; 'unsafe-inline' weakens XSS protection."))
    if "unsafe-eval" in script:
        out.append(("CSP script-src allows 'unsafe-eval'", Severity.LOW,
                    f"script-src: {script}",
                    "Remove 'unsafe-eval' if the app does not need dynamic code evaluation."))
    if "*" in script.split():
        out.append(("CSP script-src allows any origin (*)", Severity.LOW,
                    f"script-src: {script}",
                    "Restrict script-src to the specific origins you load from."))
    if "object-src" not in directives and "default-src" not in directives:
        out.append(("CSP has no object-src/default-src fallback", Severity.LOW,
                    f"content-security-policy: {value}",
                    "Add object-src 'none' to block legacy plugin content."))
    return out


def _preload_findings(status_json: str, domain: str) -> List[Tuple[str, Severity, str, str]]:
    """Interpret the hstspreload.org status API response."""
    try:
        data = json.loads(status_json)
    except (ValueError, TypeError):
        return []
    status = str(data.get("status", "")).lower()
    preloaded = str(data.get("preloadedDomain", "") or "")
    if status == "preloaded":
        return [(f"HSTS preload: {preloaded or domain} is on the preload list", Severity.INFO,
                 f"hstspreload.org status: preloaded ({preloaded or domain})", "")]
    if status == "pending":
        return [("HSTS preload: submission is pending", Severity.LOW,
                 "hstspreload.org status: pending",
                 "Ensure the HSTS header includes max-age, includeSubDomains, and preload.")]
    if status == "unknown":
        return [("HSTS preload: domain is not on the preload list", Severity.LOW,
                 "hstspreload.org status: unknown",
                 "Optional: submit at https://hstspreload.org after adding includeSubDomains; preload.")]
    return []


# Standard security headers are expected and should not be reported as
# "infra header exposed" noise.
SECURITY_HEADERS = {
    "x-content-type-options", "x-frame-options", "x-xss-protection",
    "x-permitted-cross-domain-policies", "x-download-options",
    "x-dns-prefetch-control",
}

# Headers that reveal infrastructure/runtime details.
INFRA_HEADER_PREFIXES = (
    "x-vercel", "x-request-id", "x-runtime", "x-served-by", "x-cache",
    "x-amz", "x-azure", "x-goog", "x-backend", "x-debug", "x-generator",
    "x-drupal", "x-litespeed", "x-aspnet", "x-sharepoint", "x-sp-",
    "x-powered-by",
)


class HeadersCheck(Check):
    name = "headers"
    description = "HSTS/preload, CSP, XCTO, CORS, version leaks, HTTP→HTTPS redirect"

    def run(self, target: str, cfg: Config) -> CheckResult:
        findings: List[Finding] = []
        url = target if target.startswith("http") else f"https://{target}"

        ok, raw = head(url, cfg, follow=True)
        if not ok:
            return CheckResult(self.name, "error", error=raw[:400])

        h = _parse_headers(raw)
        blocks = _all_header_blocks(raw)
        status_line = _status_line(raw)

        # HSTS - check across the *entire* redirect chain; a header on any hop
        # (e.g. the entry apex) satisfies the protocol requirement for that host.
        hsts = ""; hsts_on = ""
        for i, b in enumerate(blocks):
            v = b.get("strict-transport-security", "")
            if v:
                hsts = v
                hsts_on = f"hop {i+1}/{len(blocks)}"
                break
        if not hsts:
            findings.append(Finding(self.name, "No HSTS header - clients may hit plain HTTP", Severity.MED,
                                   f"strict-transport-security: (missing)\n{status_line}",
                                   "Add: Strict-Transport-Security: max-age=31536000; includeSubDomains; preload"))
        else:
            if "includeSubdomains" not in hsts.lower():
                findings.append(Finding(self.name, f"HSTS missing includeSubDomains ({hsts_on})", Severity.LOW,
                                       f"strict-transport-security: {hsts}  [{hsts_on}]",
                                       "Add includeSubDomains before introducing subdomains."))
            else:
                findings.append(Finding(self.name, f"HSTS configured ({hsts}) [{hsts_on}]", Severity.INFO))

        # HSTS preload list status (external, passive lookup; no API key).
        domain = base_domain(strip_host(url))
        if "." in domain:
            ok_pre, pre_body = get(
                "https://hstspreload.org/api/v2/status?domain=" + domain, cfg, follow=True
            )
            if ok_pre:
                for title, sev, evidence, rec in _preload_findings(pre_body, domain):
                    findings.append(Finding(self.name, title, sev, evidence, rec))

        # Server version leak
        srv = h.get("server", "")
        if re.search(r"nginx/\d|apache/\d|Microsoft-IIS/[\d.]+", srv, re.I):
            findings.append(Finding(self.name, f"Server header leaks version: {srv}", Severity.MED,
                                   f"server: {srv}", "Strip the version token (server_tokens off / custom server header)."))
        elif srv:
            findings.append(Finding(self.name, f"Server header generic: {srv}", Severity.INFO))

        # CORS
        cors = h.get("access-control-allow-origin", "")
        if cors == "*":
            findings.append(Finding(self.name, "CORS access-control-allow-origin: *", Severity.LOW,
                                   "access-control-allow-origin: *",
                                   "OK if public/no-secrets. Scope it if the site ever serves auth + cookies."))

        # Debug / infra headers (info disclosure, minor). Only flag headers
        # that actually reveal infrastructure; skip standard security headers.
        for k in h:
            if k in SECURITY_HEADERS:
                continue
            if k == "x-powered-by":
                findings.append(Finding(self.name, f"x-powered-by: {h[k]}", Severity.LOW,
                                       f"x-powered-by: {h[k]}", "Remove the X-Powered-By header."))
            elif k.startswith(INFRA_HEADER_PREFIXES):
                findings.append(Finding(self.name, f"Infra header exposed: {k}: {h[k]}", Severity.INFO,
                                       f"{k}: {h[k]}", "Minor info disclosure; optional to suppress."))

        # Content-Type
        ct = h.get("content-type", "")
        if "text/html" in ct and "charset" not in ct.lower():
            findings.append(Finding(self.name, "HTML response without charset", Severity.LOW,
                                   f"content-type: {ct}", "Add charset=utf-8 to prevent charset-based XSS."))
        elif ct.startswith("text/html"):
            findings.append(Finding(self.name, f"Content-Type: {ct}", Severity.INFO))

        # X-Content-Type-Options
        xcto = h.get("x-content-type-options", "")
        if not xcto:
            findings.append(Finding(self.name, "No X-Content-Type-Options header", Severity.LOW,
                                   "x-content-type-options: (missing)",
                                   "Add: X-Content-Type-Options: nosniff"))
        elif xcto.strip().lower() != "nosniff":
            findings.append(Finding(self.name, f"X-Content-Type-Options is not nosniff: {xcto}", Severity.LOW,
                                   f"x-content-type-options: {xcto}",
                                   "Set X-Content-Type-Options: nosniff."))
        else:
            findings.append(Finding(self.name, "X-Content-Type-Options: nosniff", Severity.INFO))

        # Content-Security-Policy
        csp = h.get("content-security-policy", "")
        csp_ro = h.get("content-security-policy-report-only", "")
        if csp:
            for title, sev, evidence, rec in _csp_findings(csp):
                findings.append(Finding(self.name, title, sev, evidence, rec))
        elif csp_ro:
            findings.append(Finding(self.name, "CSP is report-only, not enforced", Severity.MED,
                                   f"content-security-policy-report-only: {csp_ro}",
                                   "Enforce the policy with Content-Security-Policy once reports are clean."))
        else:
            findings.append(Finding(self.name, "No Content-Security-Policy header", Severity.MED,
                                   "content-security-policy: (missing)",
                                   "Add a CSP starting with default-src 'self' and tighten script-src."))

        # Plain HTTP should redirect to HTTPS (independent of HSTS).
        http_url = re.sub(r"^https?://", "http://", url)
        ok_http, http_raw = head(http_url, cfg, follow=False)
        if ok_http:
            http_status = _status_line(http_raw)
            http_code = _status_code(http_status)
            http_h = _parse_headers(http_raw)
            location = http_h.get("location", "")
            if http_code in (301, 302, 307, 308) and location.lower().startswith("https://"):
                findings.append(Finding(self.name, f"HTTP redirects to HTTPS ({http_code})", Severity.INFO,
                                       f"http → {http_code} location: {location}"))
            elif http_code in (301, 302, 307, 308):
                findings.append(Finding(self.name, "HTTP redirects somewhere other than HTTPS", Severity.LOW,
                                       f"http → {http_code} location: {location or '(none)'}",
                                       "Redirect plain HTTP to the HTTPS URL."))
            elif http_code in (200, 204):
                findings.append(Finding(self.name, "HTTP serves content without redirecting to HTTPS", Severity.MED,
                                       f"http → HTTP {http_code} (no HTTPS redirect)",
                                       "Redirect all plain-HTTP requests to HTTPS with a 301."))
        else:
            findings.append(Finding(self.name, "Plain HTTP is not reachable (HTTPS-only)", Severity.INFO,
                                   http_raw[:200]))

        acts = [f for f in findings if not f.is_false_positive]
        worst = max((f.severity for f in acts), default=Severity.INFO)
        summary = f"{len(acts)} note(s), worst {worst.label}"
        return CheckResult(self.name, "ok", findings, summary)
