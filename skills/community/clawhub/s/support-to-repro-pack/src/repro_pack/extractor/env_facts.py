"""Extract structured environment facts from text."""

from __future__ import annotations

import re

from ..models import EnvironmentFacts


# Version patterns
_VERSION_PATTERNS = [
    # v2.4.1, version 2.4.1, Version: 2.4.1
    re.compile(r"(?:version|ver|v)[:\s]*(\d+\.\d+(?:\.\d+)?(?:-[\w.]+)?)", re.IGNORECASE),
    # build 8837, Build: 8837
    re.compile(r"(?:build)[:\s]*(\d+)", re.IGNORECASE),
]

# Environment patterns
_ENV_PATTERNS = [
    (re.compile(r"\b(production|prod)\b", re.IGNORECASE), "production"),
    (re.compile(r"\b(staging|stg)\b", re.IGNORECASE), "staging"),
    (re.compile(r"\b(development|dev)\b", re.IGNORECASE), "development"),
    (re.compile(r"\b(sandbox)\b", re.IGNORECASE), "sandbox"),
    (re.compile(r"\b(canary)\b", re.IGNORECASE), "canary"),
]

# Region patterns
_REGION_PATTERNS = re.compile(
    r"\b(us-east-\d|us-west-\d|eu-west-\d|eu-central-\d|ap-southeast-\d"
    r"|ap-northeast-\d|cn-north-\d|cn-northwest-\d)\b",
    re.IGNORECASE,
)

# Feature flag patterns: flag_name=true/false, --enable-xxx, feature: xxx = on
_FLAG_PATTERNS = [
    re.compile(r"(?:feature[_\s]?flag|ff)[:\s]+(\w+)\s*=\s*(\w+)", re.IGNORECASE),
    re.compile(r"(\w+)\s*=\s*(true|false|on|off|enabled|disabled)", re.IGNORECASE),
]

# User role patterns
_ROLE_PATTERNS = re.compile(
    r"(?:role|角色|权限)[:\s]*([A-Za-z][\w-]*)",
    re.IGNORECASE,
)

# HTTP error codes
_HTTP_CODE_PATTERN = re.compile(r"\b([1-5]\d{2})\b")

# Application error codes (e.g., ERR_001, E1234, error code: 5001)
_APP_ERROR_PATTERN = re.compile(
    r"(?:error[_\s]?code|err)[:\s]*([A-Z_]*\d+)",
    re.IGNORECASE,
)

# URL patterns
_URL_PATTERN = re.compile(r"https?://[^\s\"'<>]+")


def extract_env_facts(text: str) -> EnvironmentFacts:
    """Extract environment facts from text using deterministic patterns."""
    facts = EnvironmentFacts()

    # Version
    for pat in _VERSION_PATTERNS:
        m = pat.search(text)
        if m:
            val = m.group(1)
            if "build" in pat.pattern.lower():
                facts.build_number = val
            else:
                facts.app_version = val

    # Environment
    for pat, env_name in _ENV_PATTERNS:
        if pat.search(text):
            facts.environment = env_name
            break

    # Region
    region_match = _REGION_PATTERNS.search(text)
    if region_match:
        facts.region = region_match.group(1)

    # Feature flags
    for pat in _FLAG_PATTERNS:
        for m in pat.finditer(text):
            key = m.group(1)
            val = m.group(2)
            # Filter out common false positives
            if key.lower() not in ("version", "build", "status", "level", "debug"):
                facts.feature_flags[key] = val

    # Role
    role_match = _ROLE_PATTERNS.search(text)
    if role_match:
        facts.user_role = role_match.group(1)

    # Error codes (HTTP + application)
    http_codes = set()
    for m in _HTTP_CODE_PATTERN.finditer(text):
        code = int(m.group(1))
        if code >= 400:  # Only error codes
            http_codes.add(str(code))
    for m in _APP_ERROR_PATTERN.finditer(text):
        http_codes.add(m.group(1))
    facts.error_codes = sorted(http_codes)

    # URLs
    facts.urls = list(set(_URL_PATTERN.findall(text)))

    return facts
