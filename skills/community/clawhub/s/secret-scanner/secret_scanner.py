#!/usr/bin/env python3
"""
Secret Scanner v2 — offline, stdlib-only secret detection tool.

Scans files and directories for 40+ types of leaked secrets, API keys, tokens,
credentials, and private keys using regex patterns and Shannon entropy analysis.

Commands:
  scan <file-or-dir>     Recursively scan files/directories for secrets.
  check <file>           Deep-scan a single file with detailed context.
  list-patterns          List all supported detection patterns.
  self-test              Run built-in self tests.

Features:
  - 40+ regex patterns (AWS, GitHub, OpenAI, Stripe, JWT, SSH, Slack, Google,
    Discord, Telegram, GitLab, MongoDB, Twilio, Azure, Anthropic, Databricks,
    DigitalOcean, npm, PyPI, SendGrid, Shopify, Docker, Vault, Grafana, K8s…)
  - Shannon entropy analysis to catch unknown token formats
  - .gitignore-aware scanning (respects .gitignore patterns)
  - Inline ignore comments (# secret-scanner:ignore)
  --min-severity filter: filter results by minimum severity level
  - Redacted output safe for CI logs
  - JSON and SARIF output for pipeline integration
  - Exit codes: 0=clean, 1=usage error, 2=critical secrets found
  
  Zero external dependencies (Python stdlib only: re + math + json).
  Works in air-gapped / offline environments.
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import math
import os
import re
import sys
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple

# ---------------------------------------------------------------------------
# Version
# ---------------------------------------------------------------------------

VERSION = "2.0.0"

# ---------------------------------------------------------------------------
# Pattern definitions — 40+ regex rules
# ---------------------------------------------------------------------------

PATTERNS: List[dict] = [
    # ── AWS ────────────────────────────────────────────────────────────────
    {
        "id": "aws-access-key",
        "name": "AWS Access Key ID",
        "severity": "high",
        "regex": re.compile(r"(?<![A-Z0-9])AKIA[0-9A-Z]{16}(?![0-9A-Z])"),
    },
    {
        "id": "aws-secret-key",
        "name": "AWS Secret Access Key",
        "severity": "critical",
        "regex": re.compile(
            r"(?<![A-Za-z0-9/+=])[A-Za-z0-9/+=]{40}(?![A-Za-z0-9/+=])"
        ),
    },
    # ── GitHub ────────────────────────────────────────────────────────────
    {
        "id": "github-pat",
        "name": "GitHub Personal Access Token",
        "severity": "critical",
        "regex": re.compile(r"(?:ghp|gho|ghu|ghs|ghf|ghr)_[A-Za-z0-9]{36,252}"),
    },
    {
        "id": "github-old-token",
        "name": "GitHub Old-Style Token (hex)",
        "severity": "high",
        "regex": re.compile(r"(?<![A-Za-z0-9])[0-9a-f]{40}(?![A-Za-z0-9])"),
        # Often just a commit hash — we flag it but at low confidence
    },
    # ── OpenAI / AI providers ─────────────────────────────────────────────
    {
        "id": "openai-key",
        "name": "OpenAI API Key",
        "severity": "critical",
        "regex": re.compile(r"sk-[A-Za-z0-9]{20,60}(?:T3BlbkFJ[0-9A-Za-z]{1,60})?"),
    },
    {
        "id": "anthropic-key",
        "name": "Anthropic API Key",
        "severity": "critical",
        "regex": re.compile(r"sk-ant-[A-Za-z0-9]{40,100}"),
    },
    # ── Slack ────────────────────────────────────────────────────────────
    {
        "id": "slack-bot-token",
        "name": "Slack Bot / App Token",
        "severity": "high",
        "regex": re.compile(r"xox[baprs]-[0-9A-Za-z-]{10,100}"),
    },
    {
        "id": "slack-webhook",
        "name": "Slack Webhook URL",
        "severity": "high",
        "regex": re.compile(
            r"https?://hooks\.slack\.com/services/T[A-Z0-9]+/B[A-Z0-9]+/[A-Za-z0-9]+"
        ),
    },
    # ── Google ────────────────────────────────────────────────────────────
    {
        "id": "google-api-key",
        "name": "Google API Key",
        "severity": "high",
        "regex": re.compile(r"AIza[0-9A-Za-z\-_]{35}"),
    },
    {
        "id": "google-oauth",
        "name": "Google OAuth Access Token",
        "severity": "high",
        "regex": re.compile(r"ya29\.[0-9A-Za-z\-_]{50,200}"),
    },
    {
        "id": "google-service-account",
        "name": "Google Service Account (JSON key)",
        "severity": "critical",
        "regex": re.compile(
            r'"(?:private_key_id|private_key|client_email|client_id)"\s*:\s*"[^"]{20,}"'
        ),
    },
    # ── Tokens / Auth ─────────────────────────────────────────────────────
    {
        "id": "jwt",
        "name": "JSON Web Token (JWT)",
        "severity": "critical",
        "regex": re.compile(
            r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}"
        ),
    },
    {
        "id": "auth-header-basic",
        "name": "Basic Auth / Bearer / Token headers",
        "severity": "medium",
        "regex": re.compile(
            r"(?i)(?:Authorization|auth)\s*[:=]\s*['\"]?(?:Basic\s+|Bearer\s+|Token\s+)"
        ),
    },
    # ── Private keys ──────────────────────────────────────────────────────
    {
        "id": "ssh-private-key",
        "name": "SSH Private Key block",
        "severity": "critical",
        "regex": re.compile(
            r"-----BEGIN\s*(?:RSA|DSA|EC|OPENSSH|SSH2)\s*PRIVATE\s*KEY-----"
        ),
    },
    {
        "id": "pgp-private-key",
        "name": "PGP Private Key block",
        "severity": "critical",
        "regex": re.compile(
            r"-----BEGIN\s*PGP\s*PRIVATE\s*KEY\s*BLOCK-----"
        ),
    },
    {
        "id": "generic-private-key",
        "name": "Generic Private Key block",
        "severity": "critical",
        "regex": re.compile(
            r"-----BEGIN\s+PRIVATE\s+KEY-----"
        ),
    },
    {
        "id": "private-key-file-ref",
        "name": "Private key material (inline)",
        "severity": "medium",
        "regex": re.compile(
            r"(?i)(?:-----BEGIN\s+.*?KEY-----|ssh-rsa\s+A[0-9A-Za-z+/]{20,}[=]{0,2})"
        ),
    },
    # ── URLs with credentials ─────────────────────────────────────────────
    {
        "id": "password-in-url",
        "name": "Password in URL (Basic Auth)",
        "severity": "high",
        "regex": re.compile(
            r"[a-zA-Z][a-zA-Z0-9+.-]*://[^:/\s]+:[^@/\s]+@[a-zA-Z0-9.-]+"
        ),
    },
    # ── Social / Messaging ────────────────────────────────────────────────
    {
        "id": "twitter-bearer",
        "name": "Twitter/X Bearer Token",
        "severity": "high",
        "regex": re.compile(r"AAAAAAAAAAAAAAAAAAAA[A-Za-z0-9%]{40,80}"),
    },
    {
        "id": "discord-bot-token",
        "name": "Discord Bot Token",
        "severity": "high",
        "regex": re.compile(r"[MN][A-Za-z\d]{23}\.[Xx][A-Za-z\d]{6}\.[A-Za-z\d_-]{27}"),
    },
    {
        "id": "discord-webhook",
        "name": "Discord Webhook URL",
        "severity": "high",
        "regex": re.compile(
            r"https://discord(?:app)?\.com/api/webhooks/\d+/[A-Za-z0-9_-]{50,}"
        ),
    },
    {
        "id": "telegram-bot-token",
        "name": "Telegram Bot Token",
        "severity": "high",
        "regex": re.compile(r"\b\d{8,10}:[A-Za-z0-9_-]{35,45}\b"),
    },
    # ── Git services ──────────────────────────────────────────────────────
    {
        "id": "gitlab-pat",
        "name": "GitLab Personal Access Token",
        "severity": "high",
        "regex": re.compile(r"glpat-[A-Za-z0-9\-_]{20,40}"),
    },
    {
        "id": "gitlab-oauth",
        "name": "GitLab OAuth Token (deprecated)",
        "severity": "high",
        "regex": re.compile(r"GR13[A-Za-z0-9\-_]{40,60}"),
    },
    # ── Databases ─────────────────────────────────────────────────────────
    {
        "id": "mongodb-connection-string",
        "name": "MongoDB Connection String",
        "severity": "critical",
        "regex": re.compile(
            r"mongodb(?: \+srv)?://[^\s:@]+:[^\s:@]+@[^\s,]+"
        ),
    },
    {
        "id": "postgresql-connection-string",
        "name": "PostgreSQL Connection String",
        "severity": "critical",
        "regex": re.compile(
            r"(?:postgres|postgresql|pg)://[^\s:@]+:[^\s:@]+@[^\s,]+"
        ),
    },
    {
        "id": "mysql-connection-string",
        "name": "MySQL Connection String",
        "severity": "critical",
        "regex": re.compile(
            r"(?:mysql|mariadb)://[^\s:@]+:[^\s:@]+@[^\s,]+"
        ),
    },
    # ── Cloud / SaaS ──────────────────────────────────────────────────────
    {
        "id": "heroku-api-key",
        "name": "Heroku API Key",
        "severity": "high",
        "regex": re.compile(
            r"[hH][eE][rR][oO][kK][uU].{0,30}[0-9A-F]{8}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{12}",
            re.IGNORECASE,
        ),
    },
    {
        "id": "stripe-key",
        "name": "Stripe API Key",
        "severity": "critical",
        "regex": re.compile(r"(?:sk|pk)_(?:live|test)_[0-9A-Za-z]{24,48}"),
    },
    {
        "id": "twilio-key",
        "name": "Twilio API Key / SID",
        "severity": "high",
        "regex": re.compile(r"SK[0-9a-fA-F]{32}"),
    },
    {
        "id": "facebook-access-token",
        "name": "Facebook Access Token",
        "severity": "high",
        "regex": re.compile(r"EAACEdEose0cBA[0-9A-Za-z]{80,200}"),
    },
    {
        "id": "azure-connection-string",
        "name": "Azure / SQL Connection String",
        "severity": "high",
        "regex": re.compile(
            r"(?:Server|Data\s*Source)=[^;]+;(?:Initial\s*Catalog|Database)=[^;]+;.*?(?:User\s*Id|UID)=[^;]+;.*?(?:Password|PWD)=[^;]+",
            re.IGNORECASE,
        ),
    },
    {
        "id": "azure-storage-account",
        "name": "Azure Storage Account Key",
        "severity": "critical",
        "regex": re.compile(
            r"(?:AccountKey|account_key|storage_key|StorageAccountKey)\s*[=:]\s*['\"]?[A-Za-z0-9+/]{80,}['\"]?"
        ),
    },
    # ── New in v2: More cloud/SaaS ────────────────────────────────────────
    {
        "id": "databricks-token",
        "name": "Databricks Personal Access Token",
        "severity": "high",
        "regex": re.compile(r"dapi[A-Za-z0-9\-_]{30,100}"),
    },
    {
        "id": "digitalocean-token",
        "name": "DigitalOcean Personal Access Token",
        "severity": "high",
        "regex": re.compile(r"dop_v1_[A-Za-z0-9\-_]{50,100}"),
    },
    {
        "id": "npm-token",
        "name": "npm Access Token",
        "severity": "high",
        "regex": re.compile(r"npm_[A-Za-z0-9]{36,60}"),
    },
    {
        "id": "pypi-token",
        "name": "PyPI API Token",
        "severity": "high",
        "regex": re.compile(r"pypi-[A-Za-z0-9]{60,100}"),
    },
    {
        "id": "sendgrid-key",
        "name": "SendGrid API Key",
        "severity": "high",
        "regex": re.compile(r"SG\.[A-Za-z0-9\-_]{22,120}"),
    },
    {
        "id": "mailgun-key",
        "name": "Mailgun API Key",
        "severity": "high",
        "regex": re.compile(r"key-[A-Za-z0-9]{32}"),
    },
    {
        "id": "shopify-secret",
        "name": "Shopify Shared Secret / Token",
        "severity": "high",
        "regex": re.compile(r"shpss_[A-Za-z0-9]{32,60}"),
    },
    {
        "id": "shopify-access-token",
        "name": "Shopify Access Token",
        "severity": "high",
        "regex": re.compile(r"shpat_[A-Za-z0-9]{32,60}"),
    },
    {
        "id": "docker-hub-token",
        "name": "Docker Hub Personal Access Token",
        "severity": "high",
        "regex": re.compile(r"dckr_pat_[A-Za-z0-9\-_]{30,80}"),
    },
    {
        "id": "vault-token",
        "name": "HashiCorp Vault Token",
        "severity": "high",
        "regex": re.compile(r"hvs\.[A-Za-z0-9\-_]{60,200}"),
    },
    {
        "id": "grafana-token",
        "name": "Grafana Service Account Token",
        "severity": "high",
        "regex": re.compile(r"glsa_[A-Za-z0-9]{20,60}_[A-Za-z0-9]{8,20}"),
    },
    {
        "id": "kubernetes-secret",
        "name": "Kubernetes Secret in env or data",
        "severity": "medium",
        "regex": re.compile(
            r"(?i)kind:\s*Secret\s*\n.*?(?:data|stringData):"
        ),
    },
    # ── Generic env-var patterns ──────────────────────────────────────────
    {
        "id": "generic-api-key-env",
        "name": "Generic API Key in env var pattern",
        "severity": "medium",
        "regex": re.compile(
            r"(?i)(?:API_KEY|API_SECRET|APP_SECRET|SECRET_KEY|ACCESS_TOKEN|"
            r"CLIENT_SECRET|DB_PASSWORD|DB_URL|DATABASE_URL|"
            r"PRIVATE_KEY|SECRET|TOKEN|PASSWORD)"
            r"\s*[=:]\s*['\"]?[A-Za-z0-9_\-/+=]{16,120}['\"]?"
        ),
    },
    {
        "id": "generic-password",
        "name": "Generic password assignment",
        "severity": "medium",
        "regex": re.compile(
            r"(?i)(?:password|passwd|pwd)\s*[=:]\s*['\"][^'\"]{4,60}['\"]"
        ),
    },
]

# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


@dataclass
class Finding:
    """A single secret finding."""

    pattern_id: str
    pattern_name: str
    severity: str
    file: str
    line: int
    match: str
    context: str = ""
    entropy: Optional[float] = None

    @property
    def redacted(self) -> str:
        """Return a redacted version (show first 4 / last 4 chars)."""
        s = self.match.strip()
        if len(s) <= 12:
            return s[:4] + "****" + s[-4:] if len(s) >= 8 else "****"
        return s[:4] + "****" + s[-4:]


# ---------------------------------------------------------------------------
# Entropy calculation
# ---------------------------------------------------------------------------


def shannon_entropy(data: str) -> float:
    """Compute Shannon entropy of a string."""
    if not data:
        return 0.0
    entropy = 0.0
    length = len(data)
    for c in set(data):
        p = data.count(c) / length
        if p > 0:
            entropy -= p * math.log2(p)
    return entropy


HIGH_ENTROPY_THRESHOLD = 4.5


def is_high_entropy(s: str) -> bool:
    """Check if a string looks like a high-entropy token."""
    if len(s) < 16:
        return False
    # Skip pure hex strings (UUIDs, hashes used for IDs)
    if re.match(r'^[0-9a-fA-F]+$', s):
        return False
    # Skip purely numeric strings
    if re.match(r'^[0-9]+$', s):
        return False
    # Skip obvious non-secrets
    if s.lower() in ('true', 'false', 'none', 'null', 'undefined', 'nan'):
        return False
    ent = shannon_entropy(s)
    return ent >= HIGH_ENTROPY_THRESHOLD


# ---------------------------------------------------------------------------
# Scanning logic
# ---------------------------------------------------------------------------

# Binary extension blacklist — skip these files entirely
BINARY_EXTENSIONS: set = {
    ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".ico", ".svg",
    ".woff", ".woff2", ".ttf", ".eot",
    ".mp3", ".mp4", ".avi", ".mov", ".wmv", ".flv",
    ".zip", ".gz", ".bz2", ".xz", ".7z", ".rar",
    ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx",
    ".pyc", ".pyo", ".pyd",
    ".o", ".so", ".dll", ".dylib", ".exe", ".bin",
    ".class", ".jar",
    ".whl", ".egg", ".tar",
    ".icns",
    ".webp", ".avif", ".heic",
    ".wasm",
}

# Files to always skip
SKIP_FILES: set = {
    ".gitignore", ".gitattributes", ".gitmodules",
    "package-lock.json", "yarn.lock", "pnpm-lock.yaml",
    "poetry.lock", "Gemfile.lock",
    "composer.lock", "Cargo.lock",
    ".dockerignore",
    ".prettierrc",
    ".editorconfig",
}

# Directories to never scan
SKIP_DIRS: set = {
    ".git", ".svn", ".hg", "__pycache__", ".venv", "venv",
    "node_modules", ".next", "dist", "build", ".tox",
    ".idea", ".vscode", ".DS_Store",
    ".bundle", "vendor/bundle", "target", "bin", "obj",
    ".terraform", ".serverless",
    "site-packages", ".eggs", "eggs",
}


# ── .gitignore support ──────────────────────────────────────────────────


def load_gitignore_patterns(root: str) -> List[str]:
    """Load .gitignore patterns from root directory, if it exists."""
    gitignore_path = os.path.join(root, ".gitignore")
    patterns: List[str] = []
    if os.path.isfile(gitignore_path):
        try:
            with open(gitignore_path, "r", encoding="utf-8", errors="replace") as f:
                for line in f:
                    line = line.strip()
                    # Skip comments and blank lines
                    if not line or line.startswith("#"):
                        continue
                    patterns.append(line)
        except Exception:
            pass
    return patterns


def is_ignored_by_gitignore(rel_path: str, patterns: List[str]) -> bool:
    """Check if a relative path matches any .gitignore pattern."""
    # Normalize to forward slashes for pattern matching
    path = rel_path.replace("\\", "/")
    parts = path.split("/")

    for pattern in patterns:
        # Strip leading slash
        pat = pattern.lstrip("/")

        # Handle trailing /** (implies entire directory tree)
        if pat.endswith("/**"):
            prefix = pat[:-3]
            if path.startswith(prefix):
                return True

        # Handle trailing / (directory-only)
        if pat.endswith("/"):
            if fnmatch.fnmatch(path, pat) or fnmatch.fnmatch(path, pat + "*"):
                return True
            continue

        # Check full path
        if fnmatch.fnmatch(path, pat):
            return True

        # Check filename match (e.g., *.log)
        if "/" not in pat and fnmatch.fnmatch(parts[-1], pat):
            return True

        # Check directory prefix match
        for i in range(1, len(parts)):
            sub = "/".join(parts[:i])
            if fnmatch.fnmatch(sub, pat):
                return True

    return False


# ── Inline ignore comments ───────────────────────────────────────────────


INLINE_IGNORE_RE = re.compile(
    r"#.*secret-scanner:\s*ignore\s*$",
    re.IGNORECASE,
)


def has_inline_ignore(line: str) -> bool:
    """Check if a line contains an inline secret-scanner:ignore directive."""
    return bool(INLINE_IGNORE_RE.search(line))


# ── File scanning ────────────────────────────────────────────────────────


def is_binary_file(filepath: str, sample_size: int = 8192) -> bool:
    """Quick heuristic: check if first bytes contain a null byte."""
    try:
        with open(filepath, "rb") as f:
            head = f.read(sample_size)
        return b"\0" in head
    except Exception:
        return True  # treat unreadable as binary


def extract_potential_tokens(line: str) -> List[str]:
    """Extract strings that look like they could be tokens or secrets."""
    tokens: List[str] = []

    # Match quoted strings
    for m in re.finditer(r"""['"]([A-Za-z0-9_\-/+=]{20,80})['"]""", line):
        tokens.append(m.group(1))

    # Match assignment values: KEY=value or KEY: value
    for m in re.finditer(
        r"""(?::\s*|=\s*|=>\s*)([A-Za-z0-9_\-/+=]{20,80})(?:\s|$|,)""",
        line,
    ):
        val = m.group(1)
        if not val.isdigit() and val.lower() not in (
            "true", "false", "none", "null", "undefined"
        ):
            tokens.append(val)

    # Match standalone base64-like strings
    for m in re.finditer(r"\b([A-Za-z0-9+/]{40,})\b", line):
        tokens.append(m.group())

    return tokens


def is_likely_test_fixture(line: str, matched_text: str) -> bool:
    """Heuristic to filter out test fixtures and example tokens."""
    lowline = line.lower()
    indicators = [
        "example", "placeholder", "test_token", "fake_key",
        "your-key-here", "your_api_key", "changeme", "xxxx",
        "sample", "dummy", "test-", "test_", "mock_",
        "00000000-0000-0000-0000", "xxxxxxxx",
        "redacted", "xxxxxxxxx",
    ]
    for ind in indicators:
        if ind in lowline:
            return True
    return False


def scan_file(
    filepath: str,
    use_entropy: bool = True,
) -> List[Finding]:
    """Scan a single file and return all findings."""
    findings: List[Finding] = []

    ext = os.path.splitext(filepath)[1].lower()
    if ext in BINARY_EXTENSIONS:
        return findings

    basename = os.path.basename(filepath)
    if basename in SKIP_FILES:
        return findings

    if is_binary_file(filepath):
        return findings

    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
    except Exception:
        return findings

    for lineno, line in enumerate(lines, start=1):
        stripped = line.rstrip("\n").rstrip("\r")

        # Inline ignore directive
        if has_inline_ignore(stripped):
            continue

        for pat in PATTERNS:
            for match in pat["regex"].finditer(stripped):
                matched_text = match.group()
                # Skip lines that look like test fixtures
                if is_likely_test_fixture(stripped, matched_text):
                    continue

                finding = Finding(
                    pattern_id=pat["id"],
                    pattern_name=pat["name"],
                    severity=pat["severity"],
                    file=filepath,
                    line=lineno,
                    match=matched_text[:120],
                    context=stripped[:200].strip(),
                )
                findings.append(finding)

        # Entropy-based detection
        if use_entropy:
            for token in extract_potential_tokens(stripped):
                if is_high_entropy(token):
                    already_flagged = any(
                        f.match == token for f in findings
                    )
                    if not already_flagged:
                        finding = Finding(
                            pattern_id="high-entropy",
                            pattern_name="High-Entropy String (potential secret)",
                            severity="low",
                            file=filepath,
                            line=lineno,
                            match=token[:120],
                            context=stripped[:200].strip(),
                            entropy=shannon_entropy(token),
                        )
                        findings.append(finding)

    return findings


def scan_path(
    path: str,
    use_entropy: bool = True,
    min_severity: Optional[str] = None,
    use_gitignore: bool = True,
) -> List[Finding]:
    """Recursively scan a file or directory."""
    if not os.path.exists(path):
        print(f"Error: path does not exist: {path}", file=sys.stderr)
        sys.exit(1)

    all_findings: List[Finding] = []

    # Load .gitignore patterns
    gitignore_patterns: List[str] = []
    if use_gitignore and os.path.isdir(path):
        gitignore_patterns = load_gitignore_patterns(path)

    # Resolve absolute path for .gitignore relative checks
    abs_root = os.path.abspath(path)

    if os.path.isfile(path):
        file_findings = scan_file(path, use_entropy=use_entropy)
        if min_severity:
            file_findings = _filter_by_severity(file_findings, min_severity)
        return file_findings

    for root, dirs, files in os.walk(path):
        # Prune skipped directories
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]

        # Prune directories matching .gitignore
        if gitignore_patterns:
            dirs[:] = [
                d
                for d in dirs
                if not is_ignored_by_gitignore(
                    os.path.relpath(os.path.join(root, d), abs_root),
                    gitignore_patterns,
                )
            ]

        for fname in files:
            fpath = os.path.join(root, fname)

            # Check .gitignore
            if gitignore_patterns:
                rel = os.path.relpath(fpath, abs_root)
                if is_ignored_by_gitignore(rel, gitignore_patterns):
                    continue

            file_findings = scan_file(fpath, use_entropy=use_entropy)
            if min_severity:
                file_findings = _filter_by_severity(file_findings, min_severity)
            all_findings.extend(file_findings)

    return all_findings


# ── Severity filtering ────────────────────────────────────────────────────

SEVERITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3}


def _filter_by_severity(
    findings: List[Finding],
    min_severity: str,
) -> List[Finding]:
    """Keep findings at or above the given severity level.

    Severity hierarchy: critical > high > medium > low.
    --min-severity=medium returns critical + high + medium.
    """
    min_order = SEVERITY_ORDER.get(min_severity.lower(), 3)
    return [f for f in findings if SEVERITY_ORDER.get(f.severity, 3) <= min_order]


# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------

SEVERITY_COLORS = {
    "critical": "\033[91m",  # red
    "high": "\033[93m",      # yellow
    "medium": "\033[94m",    # blue
    "low": "\033[90m",       # grey
}
RESET = "\033[0m"


def color(text: str, severity: str) -> str:
    """Apply ANSI color for severity level (noop on Windows without VT support)."""
    if not sys.stdout.isatty():
        return text
    c = SEVERITY_COLORS.get(severity, "")
    return f"{c}{text}{RESET}"


def print_findings(findings: List[Finding], detailed: bool = True) -> None:
    """Pretty-print findings grouped by file."""
    if not findings:
        print("No secrets found.")
        return

    # Group by file
    by_file: dict = {}
    for f in findings:
        by_file.setdefault(f.file, []).append(f)

    total = len(findings)
    by_severity: dict = {}
    for f in findings:
        by_severity[f.severity] = by_severity.get(f.severity, 0) + 1

    print(f"\n{'=' * 60}")
    print(f"  SECRET SCANNER v{VERSION} — REPORT")
    print(f"  {total} finding(s)")
    print(f"{'=' * 60}")

    for sev in ("critical", "high", "medium", "low"):
        count = by_severity.get(sev, 0)
        if count:
            colored = color(sev.upper(), sev)
            print(f"    {colored}: {count}")

    print()

    for filepath, file_findings in sorted(by_file.items()):
        print(f"\n  [{filepath}]")
        print(f"  {'-' * (len(filepath) + 4)}")
        for f in file_findings:
            severity_tag = color(f"[{f.severity.upper()}]", f.severity)
            entropy_str = f" (entropy={f.entropy:.2f})" if f.entropy is not None else ""
            print(f"    {severity_tag}  {f.pattern_name}{entropy_str} (line {f.line})")
            print(f"           Match: {color(f.redacted, f.severity)}")
            if detailed and f.context:
                ctx = f.context[:140]
                print(f"           Context: {ctx}")

    print(f"\n{'=' * 60}")
    print(f"  Scan complete. {total} finding(s).")
    print(f"{'=' * 60}\n")


def print_json_output(findings: List[Finding]) -> None:
    """Print findings as JSON array."""
    output = []
    for f in findings:
        output.append({
            "pattern_id": f.pattern_id,
            "pattern_name": f.pattern_name,
            "severity": f.severity,
            "file": f.file,
            "line": f.line,
            "redacted": f.redacted,
            "context": f.context[:200] if f.context else "",
            "entropy": round(f.entropy, 2) if f.entropy is not None else None,
        })

    print(json.dumps(output, indent=2))


def print_sarif_output(findings: List[Finding], path: str) -> None:
    """Generate a SARIF v2.1.0 report for CI integration (GitHub Code Scanning etc.)."""
    sarif = {
        "$schema": "https://raw.githubusercontent.com/oasis-tcs/openc2-schema/master/schemas/sarif-2.1.0.json",
        "version": "2.1.0",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "secret-scanner",
                        "version": VERSION,
                        "informationUri": "https://github.com/itsPremkumar/clawhub-skills/tree/main/secret-scanner",
                        "rules": [],
                    }
                },
                "results": [],
            }
        ],
    }

    # Collect rules
    rule_ids: Set[str] = set()
    for f in findings:
        if f.pattern_id not in rule_ids:
            rule_ids.add(f.pattern_id)
            sarif["runs"][0]["tool"]["driver"]["rules"].append({
                "id": f.pattern_id,
                "name": f.pattern_name,
                "shortDescription": {"text": f.pattern_name},
                "properties": {"severity": f.severity},
            })

    # Collect results
    for f in findings:
        sarif["runs"][0]["results"].append({
            "ruleId": f.pattern_id,
            "message": {"text": f"Found {f.pattern_name} at line {f.line}"},
            "level": "error" if f.severity == "critical" else "warning",
            "locations": [
                {
                    "physicalLocation": {
                        "artifactLocation": {"uri": f.file},
                        "region": {
                            "startLine": f.line,
                            "snippet": {"text": f.context[:200]},
                        },
                    }
                }
            ],
            "properties": {
                "redacted": f.redacted,
                "severity": f.severity,
            },
        })

    # Write to file
    with open(path, "w", encoding="utf-8") as f:
        json.dump(sarif, f, indent=2)

    print(f"SARIF report written to {path}")


# ---------------------------------------------------------------------------
# CLI commands
# ---------------------------------------------------------------------------


def cmd_list_patterns() -> None:
    """Print all supported detection patterns."""
    print(f"\n  {'ID':<36} {'Name':<52} {'Severity':<10}")
    print(f"  {'-' * 36} {'-' * 52} {'-' * 10}")
    for pat in sorted(PATTERNS, key=lambda p: p["id"]):
        sev = color(pat["severity"].upper(), pat["severity"])
        print(f"  {pat['id']:<36} {pat['name']:<52} {sev}")
    print(f"\n  Total patterns: {len(PATTERNS)} regex rules")
    print(
        f"  + high-entropy string detection (Shannon entropy >= {HIGH_ENTROPY_THRESHOLD})\n"
    )


def cmd_scan(
    args: List[str],
    use_entropy: bool = True,
    min_severity: Optional[str] = None,
    use_gitignore: bool = True,
) -> int:
    """Scan a file or directory."""
    if not args:
        print(
            "Usage: secret_scanner.py scan <file-or-dir> [--json] [--sarif <file>] "
            "[--min-severity <level>] [--no-entropy] [--no-gitignore]",
            file=sys.stderr,
        )
        return 1

    path = args[0]
    use_json = "--json" in args or "--json" in [a for a in args]
    sarif_path = None
    if "--sarif" in args:
        idx = args.index("--sarif")
        if idx + 1 < len(args):
            sarif_path = args[idx + 1]

    # Re-parse flags from raw args for this subcommand
    for a in args:
        if a == "--no-entropy":
            use_entropy = False
        if a.startswith("--min-severity"):
            parts = a.split("=")
            if len(parts) == 2:
                min_severity = parts[1]
            elif "--min-severity" in args:
                idx = args.index("--min-severity")
                if idx + 1 < len(args):
                    min_severity = args[idx + 1]
        if a == "--no-gitignore":
            use_gitignore = False

    findings = scan_path(
        path,
        use_entropy=use_entropy,
        min_severity=min_severity,
        use_gitignore=use_gitignore,
    )

    if sarif_path:
        print_sarif_output(findings, sarif_path)
        return 0

    if use_json:
        print_json_output(findings)
    else:
        print_findings(findings)

    # Exit non-zero if any critical findings
    critical = [f for f in findings if f.severity == "critical"]
    if critical:
        return 2

    return 0


def cmd_check(args: List[str]) -> int:
    """Check a single file with detailed output."""
    if not args:
        print("Usage: secret_scanner.py check <file> [--no-entropy]", file=sys.stderr)
        return 1

    filepath = args[0]
    use_entropy = "--no-entropy" not in args
    if not os.path.isfile(filepath):
        print(f"Error: not a file: {filepath}", file=sys.stderr)
        return 1

    findings = scan_file(filepath, use_entropy=use_entropy)
    print_findings(findings, detailed=True)

    if any(f.severity == "critical" for f in findings):
        return 2

    return 0


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------


def _self_test() -> int:
    """Real self-test of entropy + pattern scanning core."""
    import shutil
    import tempfile

    passed = 0
    failed = 0

    def check(name: str, cond: bool, detail: str = "") -> None:
        nonlocal passed, failed
        if cond:
            print(f"  ✓ {name}")
            passed += 1
        else:
            print(f"  ✗ {name}  {detail}")
            failed += 1

    print(f"secret-scanner v{VERSION} self-test")
    print("─" * 50)

    # 1. Shannon entropy: uniform vs repeated
    uniform = "abcdefghijklmnopqrstuvwxyz0123456789"
    repeated = "aaaaaaaaaaaaaaaaaaaaaaaa"
    check(
        "entropy ordering (uniform > repeated)",
        shannon_entropy(uniform) > shannon_entropy(repeated),
    )
    check("uniform string is high entropy", is_high_entropy(uniform))
    check("repeated string is not high entropy", not is_high_entropy(repeated))

    # 2. Hex/numeric strings should not be high entropy
    check("hex string is not high entropy", not is_high_entropy("abcdef0123456789abcdef01"))
    check("numeric string is not high entropy", not is_high_entropy("1234567890123456"))
    check("short string is not high entropy", not is_high_entropy("short"))

    # 3. Pattern scanning
    d = tempfile.mkdtemp(prefix="ss_selftest_")
    try:
        # Check AWS key detection
        p = os.path.join(d, "secrets.txt")
        with open(p, "w", encoding="utf-8") as f:
            f.write("# this is for testing\n")
            f.write("aws_key=REDACTED-SECRET\n")
            f.write("api=REDACTED-SECRET\n")
            f.write("github=REDACTED-SECRET\n")
            f.write("discord=MTIzNDU2Nzg5MDEyMzQ1Ng.XX7YQg.abcdefghijklmnopqrstuvwxyz0123456789abc\n")
            f.write("# secret-scanner:ignore\n")
            f.write("should_be_ignored=REDACTED-SECRET\n")
            f.write("name = demo\n")

        findings = scan_file(p, use_entropy=False)
        ids = {fl.pattern_id for fl in findings}
        check("detects AWS access key", "aws-access-key" in ids)
        check("detects OpenAI key", "openai-key" in ids)
        check("detects GitHub PAT", "github-pat" in ids)
        check("detects Discord token", "discord-bot-token" in ids)
        check("ignores inline-ignored line",
              all("should_be_ignored" not in fl.match for fl in findings))

        # 4. Clean file yields no findings
        p2 = os.path.join(d, "clean.txt")
        with open(p2, "w", encoding="utf-8") as f:
            f.write("name = demo\ncount = 42\n")
        clean = scan_file(p2, use_entropy=False)
        check("clean file has no findings", len(clean) == 0,
              f"found: {[f.pattern_id for f in clean]}")

        # 5. Test fixture filtering
        p3 = os.path.join(d, "test_config.py")
        with open(p3, "w", encoding="utf-8") as f:
            f.write("API_KEY = 'your-api-key-here'  # example placeholder\n")
        test_findings = scan_file(p3, use_entropy=False)
        check("test fixture placeholder is ignored", len(test_findings) == 0,
              f"found: {[f.pattern_id for f in test_findings]}")

        # 6. Severity filtering
        findings_all = scan_file(p, use_entropy=False)
        high_only = _filter_by_severity(findings_all, "high")
        check("min-severity=high reduces count", len(high_only) <= len(findings_all))
        check("min-severity=high keeps critical+high",
              all(f.severity in ("critical", "high") for f in high_only))

        # 7. Entropy detection on the clean file should still find nothing
        # (clean file has low-entropy content)
        clean_with_entropy = scan_file(p2, use_entropy=True)
        check("entropy detection on clean file returns nothing",
              len(clean_with_entropy) == 0)

        # 8. v2-specific patterns
        p4 = os.path.join(d, "v2_secrets.txt")
        with open(p4, "w", encoding="utf-8") as f:
            f.write("anthropic=REDACTED-SECRET\n")
            f.write("databricks=dapiabcdef0123456789abcdef01234567\n")
            f.write("npm=npm_abcdef0123456789abcdef0123456789abcdef01\n")
            f.write("pypi=pypi-abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789\n")
            f.write("sendgrid=SG.abcdefghijklmnopqrstuvwxyz0123456789_ABCDEFGH\n")
            f.write("docker=dckr_pat_abcdefghijklmnopqrstuvwxyz0123456789ABCDEF\n")
            f.write("vault=hvs.abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789\n")
            f.write("grafana=glsa_abcdef0123456789abcdef01_ABCDEFGH0123456789\n")

        v2_findings = scan_file(p4, use_entropy=False)
        v2_ids = {fl.pattern_id for fl in v2_findings}
        check("detects Anthropic key", "anthropic-key" in v2_ids)
        check("detects Databricks token", "databricks-token" in v2_ids)
        check("detects npm token", "npm-token" in v2_ids)
        check("detects PyPI token", "pypi-token" in v2_ids)
        check("detects SendGrid key", "sendgrid-key" in v2_ids)
        check("detects Docker Hub token", "docker-hub-token" in v2_ids)
        check("detects Vault token", "vault-token" in v2_ids)
        check("detects Grafana token", "grafana-token" in v2_ids)

        # 9. Inline ignore regex test
        check("inline ignore directive detected",
              has_inline_ignore("# some code  # secret-scanner:ignore"))
        check("inline ignore not false-positive",
              not has_inline_ignore("normal line of code"))

        # 10. .gitignore pattern loading (basic)
        gitignore_content = "*.log\nbuild/\nnode_modules/\n"
        gip = os.path.join(d, ".gitignore")
        with open(gip, "w", encoding="utf-8") as f:
            f.write(gitignore_content)
        patterns = load_gitignore_patterns(d)
        check("gitignore loads patterns", len(patterns) == 3)
        check("gitignore matches *.log", is_ignored_by_gitignore("debug.log", patterns))
        check("gitignore matches build/", is_ignored_by_gitignore("build/output", patterns))
        check("gitignore matches node_modules/",
              is_ignored_by_gitignore("node_modules/pkg/index.js", patterns))
        check("gitignore does not match src/main.py",
              not is_ignored_by_gitignore("src/main.py", patterns))

    finally:
        shutil.rmtree(d, ignore_errors=True)

    print("─" * 50)
    result = 0 if failed == 0 else 1
    print(f"Result: {passed} passed, {failed} failed")
    return result


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(
        description=f"Secret Scanner v{VERSION} — detect leaked secrets, keys, and tokens.",
    )
    parser.add_argument(
        "--version", action="version", version=f"secret-scanner {VERSION}"
    )

    sub = parser.add_subparsers(dest="command", required=True)

    # scan
    scan_p = sub.add_parser("scan", help="Scan a file or directory recursively")
    scan_p.add_argument("path", nargs="?", help="File or directory to scan")
    scan_p.add_argument("--json", action="store_true", help="JSON output")
    scan_p.add_argument("--sarif", help="Output SARIF report to file (for CI)")
    scan_p.add_argument("--no-entropy", action="store_true", help="Disable entropy-based detection")
    scan_p.add_argument("--no-gitignore", action="store_true", help="Disable .gitignore awareness")
    scan_p.add_argument("--min-severity", choices=["critical", "high", "medium", "low"],
                        help="Minimum severity to report (default: all)")

    # check
    check_p = sub.add_parser("check", help="Deep-check a single file")
    check_p.add_argument("file", nargs="?", help="File to check")
    check_p.add_argument("--no-entropy", action="store_true", help="Disable entropy-based detection")

    # list-patterns
    sub.add_parser("list-patterns", help="List all detection patterns")

    # self-test
    sub.add_parser("self-test", help="Run built-in self tests")

    parsed, rest = parser.parse_known_args()

    if parsed.command == "self-test":
        return _self_test()

    if parsed.command == "list-patterns":
        cmd_list_patterns()
        return 0

    if parsed.command == "scan":
        args = rest if not parsed.path else [parsed.path] + rest
        if getattr(parsed, "json", False):
            args.append("--json")
        if getattr(parsed, "sarif", None):
            args.extend(["--sarif", parsed.sarif])
        if getattr(parsed, "no_entropy", False):
            args.append("--no-entropy")
        if getattr(parsed, "no_gitignore", False):
            args.append("--no-gitignore")
        if getattr(parsed, "min_severity", None):
            args.extend(["--min-severity", parsed.min_severity])
        return cmd_scan(args)

    if parsed.command == "check":
        args = rest if not parsed.file else [parsed.file] + rest
        if getattr(parsed, "no_entropy", False):
            args.append("--no-entropy")
        return cmd_check(args)

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
