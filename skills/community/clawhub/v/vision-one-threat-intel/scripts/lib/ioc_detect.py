"""Auto-detect IOC type from a raw indicator value."""

import re

# Patterns ordered from most specific to least specific
_SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")
_SHA1_RE = re.compile(r"^[0-9a-fA-F]{40}$")
_MD5_RE = re.compile(r"^[0-9a-fA-F]{32}$")
_IPV4_RE = re.compile(
    r"^(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)$"
)
_IPV6_RE = re.compile(r"^([0-9a-fA-F]{0,4}:){2,7}[0-9a-fA-F]{0,4}$")
_URL_RE = re.compile(r"^https?://", re.IGNORECASE)
_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
_DOMAIN_RE = re.compile(
    r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$"
)

# Maps detection result to Vision One API object types
IOC_TYPE_MAP = {
    "fileSha256": "fileSha256",
    "fileSha1": "fileSha1",
    "ip": "ip",
    "url": "url",
    "domain": "domain",
    "senderMailAddress": "senderMailAddress",
}


def detect_ioc_type(value):
    """Detect IOC type from raw string value.

    Returns (ioc_type, normalized_value) or (None, error_message).
    """
    v = value.strip()

    if _SHA256_RE.match(v):
        return "fileSha256", v.lower()
    if _SHA1_RE.match(v):
        return "fileSha1", v.lower()
    if _MD5_RE.match(v):
        return "md5", v.lower()
    if _URL_RE.match(v):
        return "url", v
    if _EMAIL_RE.match(v):
        return "senderMailAddress", v.lower()
    if _IPV4_RE.match(v):
        return "ip", v
    if _IPV6_RE.match(v):
        return "ip", v
    if _DOMAIN_RE.match(v):
        return "domain", v.lower()

    return None, (
        f"Could not detect IOC type for '{v}'\n"
        "EXPECTED: An IP address, domain, URL, SHA-1 hash, SHA-256 hash, or email address\n"
        "EXAMPLE: v1ti.py lookup 198.51.100.23"
    )


def build_feed_filter(ioc_type, value):
    """Build an OData-style filter string for the feedIndicators endpoint.

    The feedIndicators endpoint uses STIX patterns in the 'pattern' field.
    We search using 'contains' on the objectValue or use the appropriate filter.
    """
    # feedIndicators typically uses objectValue or pattern-based filtering
    # Use the value directly in a contains filter on the response
    return None  # Server-side filtering may not support arbitrary IOC search;
    # we'll do client-side filtering after fetching


def build_suspicious_filter(ioc_type, value):
    """Build filter params for the suspiciousObjects endpoint."""
    type_map = {
        "fileSha256": "fileSha256",
        "fileSha1": "fileSha1",
        "ip": "ip",
        "url": "url",
        "domain": "domain",
        "senderMailAddress": "senderMailAddress",
    }
    obj_type = type_map.get(ioc_type)
    if not obj_type:
        return {}
    return {"type": obj_type, "value": value}
