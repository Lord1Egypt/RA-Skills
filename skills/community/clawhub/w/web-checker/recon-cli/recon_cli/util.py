"""Small shared helpers (host/domain parsing)."""
from __future__ import annotations

import re

# Common second-level public suffixes. Not a full PSL implementation, but
# enough to avoid the classic ``example.co.uk -> co.uk`` mistake.
SECOND_LEVEL_SUFFIXES = {
    "co.uk", "org.uk", "me.uk", "ac.uk", "gov.uk", "ltd.uk", "plc.uk",
    "com.au", "net.au", "org.au", "edu.au", "gov.au",
    "co.jp", "ne.jp", "or.jp", "ac.jp", "go.jp",
    "com.br", "net.br", "org.br",
    "com.cn", "net.cn", "org.cn", "gov.cn",
    "com.mx", "com.tr", "com.sg", "com.hk", "com.tw",
    "co.nz", "co.in", "co.za", "co.kr",
}


def strip_host(target: str) -> str:
    """Turn a URL or bare host into a lowercase hostname (no port/path)."""
    host = target.strip()
    host = re.sub(r"^[a-z][a-z0-9+.-]*://", "", host, flags=re.I)
    host = host.split("/", 1)[0]
    host = host.rsplit("@", 1)[-1]
    host = host.rstrip(".")
    # Drop an explicit port (but leave IPv6 literals alone).
    if not host.startswith("["):
        host = re.sub(r":\d+$", "", host)
    return host.lower()


def base_domain(host: str) -> str:
    """Best-effort registrable domain for a hostname."""
    host = strip_host(host)
    parts = host.split(".")
    if len(parts) <= 2:
        return host
    if ".".join(parts[-2:]) in SECOND_LEVEL_SUFFIXES:
        return ".".join(parts[-3:])
    return ".".join(parts[-2:])
