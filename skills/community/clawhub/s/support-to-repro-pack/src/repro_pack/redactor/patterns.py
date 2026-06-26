"""PII detection regex patterns."""

import re

# Each pattern: (PIIType name, compiled regex, description)
# Order matters: more specific patterns first to avoid partial matches

PATTERNS: list[tuple[str, re.Pattern[str], str]] = [
    # AWS Access Key
    (
        "aws_key",
        re.compile(r"(?:AKIA|ASIA)[A-Z0-9]{16}"),
        "AWS access key ID",
    ),
    # Private key block
    (
        "private_key",
        re.compile(r"-----BEGIN (?:RSA |EC |DSA )?PRIVATE KEY-----"),
        "Private key header",
    ),
    # JWT token (3 base64 segments separated by dots)
    (
        "jwt",
        re.compile(r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}"),
        "JWT token",
    ),
    # Bearer token
    (
        "auth_token",
        re.compile(r"Bearer\s+[A-Za-z0-9_\-\.]{20,}"),
        "Bearer auth token",
    ),
    # Generic API key patterns (key=xxx, api_key: xxx, etc.)
    (
        "api_key",
        re.compile(
            r"(?:api[_-]?key|api[_-]?secret|access[_-]?token|secret[_-]?key)"
            r"[\s]*[=:]\s*['\"]?([A-Za-z0-9_\-\.]{16,})['\"]?",
            re.IGNORECASE,
        ),
        "API key/secret in config",
    ),
    # Password in URL or config (English + Chinese keywords)
    (
        "password",
        re.compile(
            r"(?:password|passwd|pwd|密码)\s*(?:[是=:])\s*['\"]?(\S{4,})['\"]?",
            re.IGNORECASE,
        ),
        "Password in config",
    ),
    # Stripe-style API keys (sk_live_, sk_test_, pk_live_, pk_test_, rk_live_, rk_test_)
    (
        "api_key",
        re.compile(r"\b(?:sk|pk|rk)_(?:live|test)_[A-Za-z0-9]{10,}\b"),
        "Stripe-style API key",
    ),
    # URL with embedded credentials (any scheme)
    (
        "url_with_credentials",
        re.compile(r"\w+://[^:]+:[^@]+@[^\s]+"),
        "URL with embedded credentials",
    ),
    # Credit card (Visa, MC, Amex, etc.)
    (
        "credit_card",
        re.compile(r"\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13}|6(?:011|5[0-9]{2})[0-9]{12})\b"),
        "Credit card number",
    ),
    # SSN (US)
    (
        "ssn",
        re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
        "US Social Security Number",
    ),
    # China ID card (18 digits)
    (
        "id_card",
        re.compile(r"\b[1-9]\d{5}(?:19|20)\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])\d{3}[\dXx]\b"),
        "China national ID card",
    ),
    # Cookie header
    (
        "cookie",
        re.compile(r"(?:Cookie|Set-Cookie):\s*.{10,}", re.IGNORECASE),
        "HTTP cookie header",
    ),
    # Email
    (
        "email",
        re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"),
        "Email address",
    ),
    # Phone numbers: international and China formats
    (
        "phone",
        re.compile(
            r"(?:"
            r"\+?1[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}"  # US/CA with +1
            r"|"
            r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}"  # US/CA without country code
            r"|"
            r"\+?86[-.\s]?1[3-9]\d{9}"  # China +86
            r"|"
            r"\b1[3-9]\d[-.\s]?\d{4}[-.\s]?\d{4}\b"  # China mobile
            r"|"
            r"\+?44[-.\s]?\d{2}[-.\s]?\d{4}[-.\s]?\d{4}"  # UK
            r")",
        ),
        "Phone number",
    ),
    # IPv4
    (
        "ip_address",
        re.compile(r"\b(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\b"),
        "IPv4 address",
    ),
    # IPv6 (simplified)
    (
        "ip_address",
        re.compile(r"\b(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}\b"),
        "IPv6 address",
    ),
    # UUID
    (
        "uuid",
        re.compile(r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b"),
        "UUID",
    ),
]


def mask_snippet(text: str, max_visible: int = 3) -> str:
    """Create a masked version of matched text for the report.

    Shows first few chars + asterisks, e.g. 'joh***@***.com'
    """
    if len(text) <= max_visible:
        return "*" * len(text)
    return text[:max_visible] + "*" * min(len(text) - max_visible, 10)
