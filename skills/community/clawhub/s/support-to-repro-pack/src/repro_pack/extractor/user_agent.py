"""User-Agent string parser."""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass
class UAInfo:
    browser: str | None = None
    browser_version: str | None = None
    os: str | None = None
    os_version: str | None = None
    device: str | None = None
    raw: str = ""

    def to_dict(self) -> dict[str, str | None]:
        return {k: v for k, v in self.__dict__.items() if v is not None and k != "raw"}


_BROWSER_PATTERNS = [
    # Order matters: check specific before generic
    (re.compile(r"Edg(?:e)?/([\d.]+)"), "Edge"),
    (re.compile(r"OPR/([\d.]+)"), "Opera"),
    (re.compile(r"Brave/([\d.]+)"), "Brave"),
    (re.compile(r"Vivaldi/([\d.]+)"), "Vivaldi"),
    (re.compile(r"Firefox/([\d.]+)"), "Firefox"),
    (re.compile(r"Chrome/([\d.]+)"), "Chrome"),
    (re.compile(r"Safari/([\d.]+)"), "Safari"),
    (re.compile(r"MSIE\s+([\d.]+)"), "Internet Explorer"),
    (re.compile(r"Trident/.*rv:([\d.]+)"), "Internet Explorer"),
]

_OS_PATTERNS = [
    (re.compile(r"Windows NT 10\.0"), "Windows", "10/11"),
    (re.compile(r"Windows NT 6\.3"), "Windows", "8.1"),
    (re.compile(r"Windows NT 6\.1"), "Windows", "7"),
    (re.compile(r"Mac OS X ([\d_]+)"), "macOS", None),  # version from group
    (re.compile(r"iPhone OS ([\d_]+)"), "iOS", None),
    (re.compile(r"iPad.*OS ([\d_]+)"), "iPadOS", None),
    (re.compile(r"Android ([\d.]+)"), "Android", None),
    (re.compile(r"Linux"), "Linux", None),
    (re.compile(r"CrOS"), "ChromeOS", None),
]


def parse_user_agent(ua_string: str) -> UAInfo:
    """Parse a User-Agent string into structured info."""
    info = UAInfo(raw=ua_string)

    # Detect browser
    for pattern, name in _BROWSER_PATTERNS:
        m = pattern.search(ua_string)
        if m:
            info.browser = name
            info.browser_version = m.group(1)
            break

    # Detect OS
    for pattern, os_name, fixed_version in _OS_PATTERNS:
        m = pattern.search(ua_string)
        if m:
            info.os = os_name
            if fixed_version:
                info.os_version = fixed_version
            elif m.lastindex:
                info.os_version = m.group(1).replace("_", ".")
            break

    # Detect device type
    if "Mobile" in ua_string or "iPhone" in ua_string:
        info.device = "mobile"
    elif "iPad" in ua_string or "Tablet" in ua_string:
        info.device = "tablet"
    else:
        info.device = "desktop"

    return info


def find_user_agents(text: str) -> list[UAInfo]:
    """Find and parse all User-Agent strings in text."""
    # Match User-Agent header lines or Mozilla/5.0 strings
    ua_pattern = re.compile(r"(?:User-Agent:\s*)?Mozilla/5\.0\s+\([^)]+\)[^\n]+", re.IGNORECASE)
    results = []
    seen: set[str] = set()
    for m in ua_pattern.finditer(text):
        ua = m.group(0).strip()
        if ua.lower().startswith("user-agent:"):
            ua = ua.split(":", 1)[1].strip()
        if ua not in seen:
            seen.add(ua)
            results.append(parse_user_agent(ua))
    return results
