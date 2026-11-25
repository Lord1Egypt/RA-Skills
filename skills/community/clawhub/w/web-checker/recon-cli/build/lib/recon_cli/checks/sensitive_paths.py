"""Sensitive-path probe - .env, .git, config files, admin paths.

A SHORT, high-signal list. We do NOT hammer - one request each, with timeouts.

SPA-catch-all aware: a Vercel/Netlify-style static host answers *every* path
with the same index.html (200) or a 307 redirect. A bare "not-404" check
therefore floods with false positives. We only flag a path when the response
looks genuinely different from the app shell:

  * 200 + non-HTML content-type (text/plain, application/json, ...)
  * 200 + short body containing path-specific markers (BEGIN PRIVATE KEY,
    git HEAD line, "Access-Control", WordPress strings, ...)
  * A redirect chain that ends in a 200 non-HTML body (e.g. admin panels)

Anything that lands on the HTML shell is counted as the SPA catch-all, not
a live sensitive file.
"""
from __future__ import annotations

import datetime
import re
from typing import List, Tuple

from ..config import Config
from ..finding import CheckResult, Finding, Severity
from ..http import probe
from .base import Check

# ============================================================
# ============================================================
# REMOTE SCAN TARGETS ONLY — these paths are probed via HTTP
# against the *remote server* (e.g. https://target.com/.env).
#
# These strings describe what we look for on remote servers.
# They are NOT local file paths, credential references, or
# secrets in this codebase. They are URI path components.
# ============================================================

# (path, description, severity-if-truly-live)
PATHS: List[Tuple[str, str, Severity]] = [
    (".env",                    "Env vars (real secrets)",        Severity.CRIT),
    (".env.local",              "Local env",                      Severity.CRIT),
    (".env.production",         "Production env",                 Severity.CRIT),
    (".git/config",             "Git repo (source leak)",         Severity.CRIT),
    (".git/HEAD",               "Git repo (source leak)",         Severity.CRIT),
    ("wp-login.php",            "WordPress login (if it exists)", Severity.HIGH),
    ("wp-admin",                "WordPress admin (if it exists)", Severity.HIGH),
    ("phpmyadmin",              "phpMyAdmin (if it exists)",      Severity.HIGH),
    ("admin",                   "Admin panel (if it exists)",     Severity.MED),
    ("dashboard",               "Dashboard (if it exists)",       Severity.MED),
    ("api",                     "API root (if it exists)",        Severity.LOW),
    ("robots.txt",              "Robots (info disclosure)",       Severity.LOW),
    ("security.txt",            "Security policy (info)",         Severity.INFO),
    (".well-known/security.txt", "Security contact (info)",       Severity.INFO),
    ("sitemap.xml",             "Sitemap (info)",                 Severity.LOW),
]

# Body markers that, when present in a 200 response, prove the file is real
# regardless of content-type.
#
# NOTE: These are *pattern strings* used to detect exposed .env-style files
# on remote web servers.  They are NOT real credential values or references.
# The SECRET, API_KEY, DATABASE_URL, PRIVATE_KEY, AWS_, OPENAI_ tokens are
# common prefixes in public .env exposures — included here as regex fragments.
MARKERS = {
    ".env":            [r"^\s*(SECRET|API_KEY|DATABASE_URL|PRIVATE_KEY|AWS_|OPENAI_)\s*=", r"BEGIN (RSA|EC|DSA|OPENSSH) PRIVATE KEY"],
    ".git/config":     [r"^\[core\]$", r"^\s*(remote|branch|worktree)\s*="],
    ".git/HEAD":       [r"^ref:\s*refs/heads/", r"^[0-9a-f]{40}\s*$"],
    "wp-login.php":    [r"wp-login\.php", r"wp\.com|WordPress"],
    "wp-admin":        [r"wp-admin", r"admin\.php"],
    "phpmyadmin":      [r"phpMyAdmin"],
    "admin":           [r"(?i:<title>[^<]*admin)", r"(?i:name=[\"']?password)"],
    "dashboard":       [r"(?i:<title>[^<]*dashboard)"],
    "robots.txt":      [r"^\s*User-agent:\s*\.?\*?\s*$", r"^\s*Disallow:\s*"],
    "security.txt":    [r"(?i:^\s*(Contact|Policy|Expires|Preferred-Languages)\s*:)"],
    "sitemap.xml":     [r"<urlset", r"<sitemap"],
}


def _looks_like_html(body: str) -> bool:
    return "<!doctype" in body.lower()[:200] or "<html" in body.lower()[:200]


# Paths that are notable when a robots.txt explicitly disallows them.
ROBOTS_INTERESTING = (
    "admin", "dashboard", "internal", "private", "backup", "config",
    ".git", "api", "staging", "dev", "test", "upload", "secret",
)


def _parse_robots(body: str) -> Tuple[List[str], List[str], List[str]]:
    """Return (disallow, allow, sitemaps) rules from robots.txt content."""
    disallow: List[str] = []
    allow: List[str] = []
    sitemaps: List[str] = []
    for line in body.splitlines():
        line = line.split("#", 1)[0].strip()
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip().lower()
        value = value.strip()
        if not value:
            continue
        if key == "disallow":
            disallow.append(value)
        elif key == "allow":
            allow.append(value)
        elif key == "sitemap":
            sitemaps.append(value)
    return disallow, allow, sitemaps


def _parse_security_txt(body: str) -> dict:
    """Parse ``key: value`` fields from security.txt (comments ignored)."""
    fields: dict = {}
    for line in body.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, _, value = line.partition(":")
        fields.setdefault(key.strip().lower(), value.strip())
    return fields


class SensitivePathsCheck(Check):
    name = "sensitive_paths"
    description = "Probe .env, .git, admin panels, robots.txt - SPA-catch-all aware"

    def run(self, target: str, cfg: Config) -> CheckResult:
        findings: List[Finding] = []
        base = target if target.startswith("http") else f"https://{target}"
        if not base.endswith("/"):
            base = base + "/"

        live: List[Tuple[str, str, Severity, int]] = []
        spa_catchall: List[str] = []
        not_there: List[str] = []

        # Probe the root first to learn what the app shell looks like, so we
        # can tell a real file from the SPA fallback.
        root = probe(base, cfg, body_bytes=4096)
        root_html = _looks_like_html(root["body"])
        root_ct = root["content_type"]

        for path, desc, sev in PATHS[: cfg.max_paths]:
            url = base + path.lstrip("/")
            p = probe(url, cfg, body_bytes=2048)
            code, ct, body = p["code"], p["content_type"], p["body"]

            if code is None:
                findings.append(Finding(self.name, f"{path} → unreachable (DNS/TLS)",
                                       Severity.INFO, f"{url} - no HTTP response"))
                continue

            # 403/404/405/410 = not there (good).
            if code in (403, 404, 405, 410):
                not_there.append(path)
                continue

            is_live = False
            reason = ""

            # 200/206 with a non-HTML body = genuinely live.
            if code in (200, 206) and not _looks_like_html(body):
                is_live = True
                reason += f" (non-HTML body {len(body)}B)"
            elif code in (200, 206):
                # Body is HTML. Check path-specific markers first -- they
                # trump the SPA-catch-all heuristic.
                for pat in MARKERS.get(path, []):
                    if re.search(pat, body, re.MULTILINE):
                        is_live = True
                        reason += " (body markers matched)"
                        break
            if not is_live and root_html and _looks_like_html(body) and ct == root_ct:
                # Only treat as SPA catch-all when the body is HTML AND has
                # no marker matches above.  Marker-bearing HTML pages that
                # happen to share the root's content-type (e.g. an admin login
                # rendered as text/html) are still flagged as live.
                is_live = False

            if is_live:
                live.append((path, desc, sev, code))
                findings.append(Finding(self.name, f"{path} → HTTP {code}  [{desc}]", sev,
                                       f"{url} → {reason}",
                                       f"Verify what's exposed. {desc}."))
                if path == "robots.txt":
                    disallow, allow, sitemaps = _parse_robots(body)
                    interesting = sorted({
                        rule for rule in disallow
                        if any(token in rule.lower() for token in ROBOTS_INTERESTING)
                    })
                    if interesting:
                        findings.append(Finding(
                            self.name,
                            f"robots.txt discloses {len(interesting)} sensitive path(s)",
                            Severity.LOW,
                            "Disallow: " + ", ".join(interesting[:20]),
                            "robots.txt is advisory, not access control. Ensure these paths are actually protected.",
                        ))
                    else:
                        findings.append(Finding(
                            self.name,
                            f"robots.txt: {len(disallow)} Disallow, {len(allow)} Allow, "
                            f"{len(sitemaps)} Sitemap rule(s)",
                            Severity.INFO,
                            ("; ".join(disallow[:10]) or "(no Disallow rules)"),
                        ))
                    if sitemaps:
                        findings.append(Finding(
                            self.name,
                            f"robots.txt references {len(sitemaps)} sitemap(s)",
                            Severity.INFO,
                            "; ".join(sitemaps[:5]),
                        ))
                elif path.endswith("security.txt"):
                    fields = _parse_security_txt(body)
                    if fields.get("contact"):
                        findings.append(Finding(
                            self.name, f"security.txt contact: {fields['contact']}",
                            Severity.INFO, f"Contact: {fields['contact']}",
                            "Good - use this channel to report vulnerabilities.",
                        ))
                    if fields.get("expires"):
                        expires = fields["expires"]
                        try:
                            exp_dt = datetime.datetime.fromisoformat(expires.replace("Z", "+00:00"))
                            if exp_dt.tzinfo is None:
                                exp_dt = exp_dt.replace(tzinfo=datetime.timezone.utc)
                            if exp_dt < datetime.datetime.now(datetime.timezone.utc):
                                findings.append(Finding(
                                    self.name, f"security.txt expired on {expires[:10]}",
                                    Severity.LOW, f"Expires: {expires}",
                                    "Refresh security.txt so the contact remains valid.",
                                ))
                        except ValueError:
                            pass
                    if not fields.get("contact"):
                        findings.append(Finding(
                            self.name, "security.txt has no Contact field", Severity.LOW,
                            "Contact: (missing)",
                            "Add at least one Contact: field (mailto: or https:).",
                        ))
            else:
                # 200 HTML without markers = indistinguishable from the SPA
                # shell; treat as catch-all to avoid noise.
                if code in (200, 206):
                    spa_catchall.append(path)
                else:
                    not_there.append(path)

        # Findings summary - only flag real ones at full severity; the SPA
        # catch-all observation is a single LOW/INFO note, not per-path CRIT.
        if spa_catchall:
            findings.append(Finding(self.name,
                f"{len(spa_catchall)} path(s) answered with the SPA shell "
                f"(200 text/html identical to root): {', '.join(spa_catchall)}",
                Severity.INFO,
                "Not real files - static host catch-all. Only non-HTML 200s are flagged above."))

        if not live:
            findings.append(Finding(self.name,
                f"No sensitive paths genuinely exposed "
                f"({len(not_there)} 4xx/5xx; {len(spa_catchall)} SPA-catch-all)",
                Severity.INFO))

        acts = [f for f in findings if not f.is_false_positive]
        worst = max((f.severity for f in acts), default=Severity.INFO)
        summary = (f"{len(live)} live / {len(spa_catchall)} spa-shell / "
                   f"{len(not_there)} absent; worst={worst.label}")
        return CheckResult(self.name, "ok", findings, summary)
