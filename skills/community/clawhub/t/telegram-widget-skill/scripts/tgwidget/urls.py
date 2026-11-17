"""Link allowlist: which URLs a widget may open.

The allowlist comes from the operator (environment variable
``TG_WIDGETS_ALLOWED_LINKS``), never from the widget or the command line.
Entries are comma or whitespace separated:

    example.com            this host only, any path
    *.example.com          any subdomain of example.com (not example.com itself)
    t.me/MyBot             this host, and paths equal to /MyBot or below it

An empty allowlist (the default) means the widget may open no links at all.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from typing import List, Optional, Tuple
from urllib.parse import urlsplit

ENV_VAR = "TG_WIDGETS_ALLOWED_LINKS"
TELEGRAM_HOSTS = {"t.me", "telegram.me", "telegram.dog"}
MAX_LINK_LENGTH = 256

# Anything that may become a link: a scheme, a protocol-relative //host, a
# bare www. host or a Telegram short link.
URLISH = re.compile(
    r"(?i)(?:\b[a-z][a-z0-9+.-]*:)?//[^\s'\"<>()`\\]+"
    r"|\bwww\.[a-z0-9-]+\.[^\s'\"<>()`\\]+"
    r"|\b(?:t\.me|telegram\.me|telegram\.dog)/[^\s'\"<>()`\\]*"
)


@dataclass(frozen=True)
class AllowEntry:
    host: str
    wildcard: bool
    path: str  # "" means any path

    def matches(self, host: str, path: str) -> bool:
        if self.wildcard:
            if not host.endswith("." + self.host):
                return False
        elif host != self.host:
            return False
        if not self.path:
            return True
        p, want = path or "/", self.path
        if host in TELEGRAM_HOSTS:  # Telegram usernames are case-insensitive
            p, want = p.lower(), want.lower()
        return p == want or p.startswith(want.rstrip("/") + "/")


def parse_allowlist(text: str) -> List[AllowEntry]:
    entries = []
    for raw in re.split(r"[\s,]+", text or ""):
        raw = raw.strip()
        if not raw or raw.startswith("#"):
            continue
        raw = re.sub(r"(?i)^https?://", "", raw)
        host, _, path = raw.partition("/")
        host = host.lower()
        wildcard = host.startswith("*.")
        if wildcard:
            host = host[2:]
        if not re.fullmatch(r"[a-z0-9-]+(\.[a-z0-9-]+)+", host):
            raise ValueError("bad allowlist entry: %r" % raw)
        entries.append(AllowEntry(host, wildcard, "/" + path if path else ""))
    return entries


def load_allowlist() -> List[AllowEntry]:
    return parse_allowlist(os.environ.get(ENV_VAR, ""))


def link_problem(url: str, allow: List[AllowEntry], method: str = "href") -> Optional[str]:
    """Why `url` may not be opened from a widget, or None if it may.

    `method` is "openLink", "openTelegramLink", or "href" (a tapped <a href> or
    window.open, which the app routes to either one by host).
    """
    if len(url) > MAX_LINK_LENGTH:
        return "longer than %d characters" % MAX_LINK_LENGTH
    if any(ch.isspace() for ch in url):
        return "contains whitespace"
    try:
        parts = urlsplit(url)
    except ValueError:
        return "not a valid URL"
    if parts.scheme.lower() != "https":
        return "not an https: URL"
    if parts.username is not None or parts.password is not None or "@" in parts.netloc:
        return "has a user name or password"
    try:
        host = (parts.hostname or "").lower()
        _ = parts.port
    except ValueError:
        return "has a bad port"
    if not host:
        return "has no host"
    if method == "openTelegramLink" and host not in TELEGRAM_HOSTS:
        return "openTelegramLink only opens https://t.me/... links"
    if method == "openLink" and host in TELEGRAM_HOSTS:
        return "openLink refuses t.me links: use openTelegramLink"
    for entry in allow:
        if entry.matches(host, parts.path):
            return None
    target = host + (parts.path if host in TELEGRAM_HOSTS else "")
    if not allow:
        return "%s is not allowed: the link allowlist is empty (operator setting %s)" % (target, ENV_VAR)
    return "%s is not on the link allowlist (operator setting %s)" % (target, ENV_VAR)


# XML namespace names look like URLs but are never opened (createElementNS, xmlns=).
NAMESPACE_URIS = re.compile(
    r"(?i)https?://www\.w3\.org/(?:2000/svg|1999/xhtml|1999/xlink|2000/xmlns/?|xml/1998/namespace)(?![\w/.-])"
)


def find_urls(text: str) -> List[str]:
    return [m.group(0) for m in URLISH.finditer(text or "")]


def scan_text(text: str, allow: List[AllowEntry]) -> List[Tuple[str, str]]:
    """Every URL-like piece of `text` that is not allowed, with the reason."""
    found = []
    for url in find_urls(NAMESPACE_URIS.sub(" ", text or "")):
        full = url if "//" in url[:12] else "https://" + url.lstrip("/")
        problem = link_problem(full, allow, "href")
        if problem:
            found.append((url, problem))
    return found
