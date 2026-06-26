"""Stage-2 URL red-flag scoring based on Mohammad et al. (2014) features.

Each URL is scanned for binary red flags. Aggregate score caps at 100:
    url_score = min(100, red_flags_hit * 15)
"""

from __future__ import annotations

import ipaddress
import re
from dataclasses import asdict, dataclass, field
from urllib.parse import urlparse

# Subset of attacker-favored "cheap" TLDs
_CHEAP_TLDS = {"tk", "ml", "ga", "cf", "gq", "xyz", "top", "click", "zip", "country"}

# Common brand tokens attackers impersonate
_BRAND_TOKENS = {
    "paypal", "microsoft", "apple", "google", "amazon", "facebook", "instagram",
    "bank", "chase", "wellsfargo", "citi", "hsbc", "netflix", "linkedin",
}

_SHORTENERS = {
    "bit.ly", "tinyurl.com", "t.co", "goo.gl", "ow.ly", "buff.ly",
    "is.gd", "cutt.ly", "rb.gy", "shorturl.at",
}


@dataclass
class UrlFeatures:
    url: str
    ip_literal: bool = False
    shortener: bool = False
    at_in_url: bool = False
    double_slash_in_path: bool = False
    subdomain_depth: int = 0
    deep_subdomain: bool = False       # > 3
    hyphenated_hostname: bool = False
    long_url: bool = False             # > 75 chars
    https_token_in_hostname: bool = False
    punycode: bool = False
    explicit_port: bool = False
    cheap_tld_with_brand: bool = False

    # Names of binary-red-flag fields (excludes url/subdomain_depth which is a count)
    _FLAG_FIELDS = (
        "ip_literal", "shortener", "at_in_url", "double_slash_in_path",
        "deep_subdomain", "hyphenated_hostname", "long_url",
        "https_token_in_hostname", "punycode", "explicit_port",
        "cheap_tld_with_brand",
    )

    @classmethod
    def from_url(cls, url: str) -> UrlFeatures:
        parsed = urlparse(url)
        host = (parsed.hostname or "").lower()
        feats = cls(url=url)

        feats.ip_literal = _is_ip(host)
        feats.shortener = host in _SHORTENERS
        feats.at_in_url = "@" in url[url.find("://") + 3:]  # after scheme
        feats.double_slash_in_path = "//" in (parsed.path or "")
        feats.subdomain_depth = _subdomain_depth(host)
        feats.deep_subdomain = feats.subdomain_depth > 3
        feats.hyphenated_hostname = "-" in host
        feats.long_url = len(url) > 75
        feats.https_token_in_hostname = "https" in host
        feats.punycode = "xn--" in host
        feats.explicit_port = bool(parsed.port) and parsed.port not in (80, 443)
        feats.cheap_tld_with_brand = _cheap_tld_with_brand(host)
        return feats

    def red_flag_names(self) -> list[str]:
        return [name for name in self._FLAG_FIELDS if getattr(self, name)]

    def red_flag_count(self) -> int:
        return len(self.red_flag_names())


def score_urls(urls: list[str]) -> dict:
    per_url_flags = []
    total_flags = 0
    for url in urls:
        feats = UrlFeatures.from_url(url)
        flags = feats.red_flag_names()
        per_url_flags.append({"url": url, "flags": flags})
        total_flags += len(flags)

    score = min(100, total_flags * 15)
    return {
        "score": score,
        "red_flags_hit": total_flags,
        "per_url_flags": per_url_flags,
    }


def _is_ip(host: str) -> bool:
    if not host:
        return False
    try:
        ipaddress.ip_address(host)
        return True
    except ValueError:
        return False


def _subdomain_depth(host: str) -> int:
    """Count subdomain labels (labels beyond the eTLD+1).

    Simplification: treat the last two labels as eTLD+1. This is inaccurate
    for multi-part TLDs like `.co.uk` but fine for our scoring purposes.
    Returns 0 for `paypal.com`, 1 for `mail.google.com`, etc.
    """
    if not host or _is_ip(host):
        return 0
    labels = host.split(".")
    return max(0, len(labels) - 2)


def _cheap_tld_with_brand(host: str) -> bool:
    if not host:
        return False
    labels = host.split(".")
    if len(labels) < 2:
        return False
    tld = labels[-1]
    if tld not in _CHEAP_TLDS:
        return False
    return any(any(brand in label for brand in _BRAND_TOKENS) for label in labels[:-1])
