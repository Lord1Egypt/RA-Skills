#!/usr/bin/env python3
"""No-people mode: strip named people from a signal-scout analysis.

Public surfaces (plugin directories, MCP registries, Apify, proof pages) must
carry zero named people. `--focus companies` only prioritizes; this module is
the hard filter that finalize.py and mcp-server/server.py both call.

Two phases, because source verification fuzzy-matches `evidence` against the
live page and redacting a quote first could fail a real claim:

  1. drop_people(data)        before verification. Removes the `individuals`
                              array and any segment, company, or battlecard
                              entry whose own `source_url` is a personal
                              profile or personal post (the link itself names
                              the person). Returns the names to redact later.
  2. redact_people(obj, names) after verification. Walks every string in the
                              JSON and replaces known Individual names,
                              @handles, u/handles, personal emails, and
                              personal profile URLs. List items that are only
                              a personal URL are removed outright.

strip_people(data) runs both phases in one call for callers that do not
verify in between (generate_report.py, tests).

Boundary, stated plainly: this is pattern matching plus removal of the names
the analysis itself recorded as Individuals. It is not named-entity
recognition. A person mentioned only by a bare name inside a quote, who was
never recorded as an Individual, is not detected.
"""

from __future__ import annotations

import copy
import re
import unicodedata
from typing import Any
from urllib.parse import parse_qs, unquote, urlparse

NAME_PLACEHOLDER = "[person removed]"
URL_PLACEHOLDER = "[profile link removed]"
EMAIL_PLACEHOLDER = "[email removed]"

PEOPLE_LIMITS_PREFIX = "No-people mode:"

URL_RE = re.compile(r"https?://[^\s<>\"'()\[\]{}]+")
EMAIL_RE = re.compile(r"\b[\w.%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+\b")
# "jane [at] acme [dot] com", "jane(at)acme.com"
OBFUSCATED_EMAIL_RE = re.compile(
    r"\b([\w.%+-]+)\s*[\[(]\s*at\s*[\])]\s*[\w-]+(?:\s*(?:\.|[\[(]\s*dot\s*[\])])\s*[\w-]+)+", re.IGNORECASE
)
# A URL written without its scheme (linkedin.com/in/jane). Only replaced when it is personal.
BARE_URL_RE = re.compile(r"(?<![\w@/.:-])(?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,}/[^\s<>\"'()\[\]{}]+")
# The trailing lookahead keeps npm scopes and paths (@vercel/og, @types/node)
# intact and stops a handle being cut short to dodge it. A handle followed by
# /status is a post under that account, not a package path.
HANDLE_RE = re.compile(r"(?<![\w@./])@\w(?:[\w.-]{0,48}\w)?(?!\w|/(?!status\b)|[.-]\w)")
REDDIT_USER_RE = re.compile(r"(?<![\w/])/?u/[A-Za-z0-9_-]{2,30}\b")

# Shared role inboxes are a published company channel, not a person.
ROLE_INBOXES = {
    "partners", "partnerships", "partner", "bd", "bizdev", "sales", "hello", "info",
    "contact", "support", "press", "media", "team", "developers", "devrel", "integrations",
}

# Hosts where any path below the root is an account (person or brand). Strict on
# purpose: a company account post cited as a source is dropped too.
ACCOUNT_HOSTS = {
    "twitter.com", "x.com", "instagram.com", "facebook.com", "tiktok.com",
    "threads.net", "threads.com",
}
# Separators between a name and a title or employer: "Jane Doe (CTO)",
# "Jane Doe, CTO", "Jane Doe | Acme", "Jane Doe <em dash or en dash> CTO",
# "Jane Doe - CTO", "Jane Doe at Acme".
NAME_SPLIT_RE = re.compile(r"\s+(?:-|at)\s+|\s*[(\[|,\u2013\u2014]")
TITLE_RE = re.compile(r"^(?:(?:dr|mr|mrs|ms|prof|sir)\b\.?\s*)+", re.IGNORECASE)
# Tokens of a full name that are never redacted on their own.
NAME_PARTICLES = {"the", "and", "for", "von", "van", "der", "den", "del", "dos", "das", "bin", "ibn", "san", "blog"}

# Single-token names that are also everyday words are never redacted on their
# own: redacting "Will" would turn "Acme will launch" into nonsense.
COMMON_WORDS = {
    "will", "mark", "bill", "grace", "hope", "joy", "rose", "may", "june", "april", "august",
    "faith", "frank", "pat", "sue", "dawn", "rob", "art", "ray", "guy", "jack", "max", "chase",
    "hunter", "page", "lane", "drew", "rich", "sky", "summer", "autumn", "sunny", "earl", "dean",
    "king", "angel", "sage", "river", "reed", "wade", "glen", "cliff", "gene", "don", "buck",
    "bob", "sam", "jay", "victor", "miles", "penny", "rusty", "holly", "ivy", "iris", "amber",
    "crystal", "ruby", "pearl", "violet", "lily", "daisy", "heath", "forrest", "stone", "hale",
    "young", "brown", "white", "black", "green", "gray", "grey", "long", "short", "little",
    "admin", "user", "team", "support", "dev", "devops", "founder", "builder", "maker", "hacker",
    "anonymous", "deleted", "guest", "help", "test", "hello", "info", "sales", "product", "design",
}
ACCOUNT_HOST_NON_PROFILE = {"", "i", "home", "search", "hashtag", "explore", "intent", "share", "about", "tos", "privacy"}


def _host(parsed) -> str:
    host = (parsed.hostname or "").lower()
    return host[4:] if host.startswith("www.") else host


def _on(host: str, domain: str) -> bool:
    """host is domain or a subdomain of it (mobile.twitter.com, m.facebook.com)."""
    return host == domain or host.endswith("." + domain)


def is_personal_url(url: str) -> bool:
    """True when the URL is a person's profile or a post under a person's
    account, i.e. the link itself identifies someone."""
    try:
        parsed = urlparse(url.strip())
    except ValueError:
        return False
    host = _host(parsed)
    if not host:
        return False
    segments = [s for s in parsed.path.split("/") if s]
    first = segments[0].lower() if segments else ""

    if _on(host, "linkedin.com"):
        # /in/ and /pub/ are profiles; /posts/<name>_<slug> and /pulse/<slug>-<name> are
        # a post and an article under a person's account.
        return first in {"in", "pub", "posts", "pulse"}
    if any(_on(host, h) for h in ACCOUNT_HOSTS):
        return first not in ACCOUNT_HOST_NON_PROFILE
    if _on(host, "reddit.com"):
        return first in {"user", "u"}
    if host == "news.ycombinator.com":
        return parsed.path.rstrip("/") in {"/user", "/submitted", "/threads"} and "id" in parse_qs(parsed.query)
    if host in {"github.com", "gist.github.com"}:
        # A bare github.com/<name> is a user (or org) profile; repo and issue
        # URLs carry two or more segments and stay.
        return len(segments) == 1
    if _on(host, "bsky.app"):
        return first == "profile"
    if _on(host, "youtube.com") and first in {"c", "user", "channel"}:
        return True
    if _on(host, "youtube.com") or _on(host, "medium.com") or first.startswith("@"):
        # medium.com/@x, youtube.com/@x, mastodon-style host/@x
        return first.startswith("@")
    return False


def _is_redactable_name(name: str) -> bool:
    """A full name (2+ tokens) always qualifies. A single token qualifies
    unless it is an everyday word or a single character."""
    tokens = name.split()
    if len(tokens) >= 2:
        return True
    if len(tokens) != 1:
        return False
    token = tokens[0].strip("@")
    return len(token) >= 2 and token.lower() not in COMMON_WORDS


def _unaccented(text: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", text) if not unicodedata.combining(c))


def _is_non_latin(text: str) -> bool:
    """Scripts written without spaces between words (CJK) or with attached
    prefixes and endings (Hebrew, Arabic, Cyrillic): word boundaries do not apply."""
    return any(c.isalpha() and ord(c) > 0x024F for c in text)


def _name_pattern(name: str) -> re.Pattern[str]:
    """Case-insensitive. Tokens of a multi-token name may be joined by up to
    three non-letters or by nothing: "Jane Doe", "Jane\u00a0Doe", "Jane-Doe", "JaneDoe"."""
    tokens = re.findall(r"[^\W_]+", name)
    body = r"[\W_]{0,3}".join(re.escape(t) for t in tokens) if len(tokens) >= 2 else re.escape(name)
    if _is_non_latin(name):
        return re.compile(body, re.IGNORECASE)
    return re.compile(r"(?<![\w@])" + body + r"(?!\w)", re.IGNORECASE)


def _text_names(names: list[str]) -> list[str]:
    """`names` plus each token of a multi-token name ("Jane Doe" also redacts
    "Jane" and "Doe"), longest first. Everyday words, particles and tokens
    under three characters are not redacted on their own. Used for text only:
    a URL is matched against the recorded names, not their single tokens."""
    out = set(names)
    for name in names:
        tokens = re.findall(r"[^\W_]+", name)
        if len(tokens) < 2:
            continue
        for token in tokens:
            low = token.lower()
            if low in COMMON_WORDS or low in NAME_PARTICLES or (len(token) < 3 and not _is_non_latin(token)):
                continue
            out.add(token)
    return sorted(out, key=len, reverse=True)


def url_names_person(url: str, names: list[str]) -> bool:
    """True when a URL that is not a profile still carries a recorded name or
    handle in its host, path, or query, e.g. /t/janedoe-ci-woes or ?author=JaneDoe.
    Multi-token names match with any separator (jane-doe, jane_doe, jane%20doe)."""
    text = unquote(url).lower()
    for name in names:
        # Unicode-aware tokens and boundaries, so "José Álvarez" matches /t/josé-álvarez.
        tokens = re.findall(r"[^\W_]+", name.lower())
        if not tokens:
            continue
        joined = r"[\W_]?".join(re.escape(t) for t in tokens)
        if re.search(r"(?<![^\W_])" + joined + r"(?![^\W_])", text):
            return True
    return False


def url_has_personal_contact(url: str) -> bool:
    """True when the decoded URL carries a personal email or an @handle in its
    path or query (?contact=alice@example.com, ?via=@someone). Role inboxes and
    path-style npm scopes (/package/@vercel/og) are not personal."""
    text = unquote(url)
    for match in EMAIL_RE.finditer(text):
        if match.group(0).split("@", 1)[0].lower() not in ROLE_INBOXES:
            return True
    return HANDLE_RE.search(EMAIL_RE.sub(" ", text)) is not None


def _names_url(url: str, names: list[str]) -> bool:
    return is_personal_url(url) or url_names_person(url, names) or url_has_personal_contact(url)


def collect_person_names(data: dict[str, Any]) -> list[str]:
    """Every string that names an Individual: the `name` itself, the part before
    a title or employer (`Jane Doe (@jdoe)`, `Jane Doe, CTO`, `Jane Doe at Acme`)
    without a leading honorific (`Dr. Jane Doe`), any handle inside it, and the
    unaccented spelling of each. Single everyday words are left out."""
    names: set[str] = set()
    for item in data.get("individuals") or []:
        if not isinstance(item, dict):
            continue
        raw = unicodedata.normalize("NFC", str(item.get("name") or "")).strip()
        if not raw:
            continue
        names.add(raw)
        base = TITLE_RE.sub("", NAME_SPLIT_RE.split(raw, maxsplit=1)[0].strip()).strip()
        if base:
            names.add(base)
        for handle in HANDLE_RE.findall(raw) + REDDIT_USER_RE.findall(raw):
            names.add(handle.lstrip("/"))
            names.add(handle.lstrip("/@").removeprefix("u/"))
    names |= {_unaccented(n) for n in names}
    # Longest first so "Jane Doe" is replaced before "Jane".
    return sorted((n for n in names if _is_redactable_name(n)), key=len, reverse=True)


def drop_people(data: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    """Phase 1 (pre-verification). Returns (copy without person records, stats).
    stats["names"] carries what redact_people needs in phase 2."""
    out = copy.deepcopy(data)
    names = collect_person_names(out)
    individuals = out.pop("individuals", None) or []
    dropped_for_source: list[str] = []
    for kind in ("segments", "companies"):
        items = out.get(kind)
        if not isinstance(items, list):
            continue
        kept = []
        for item in items:
            if isinstance(item, dict) and _names_url(str(item.get("source_url") or ""), names):
                dropped_for_source.append(f"{kind}:{item.get('name', '')}")
                continue
            kept.append(item)
        if kept:
            out[kind] = kept
        else:
            out.pop(kind, None)
    ctx = out.get("competitive_context")
    if isinstance(ctx, dict) and isinstance(ctx.get("battlecard"), list):
        kept_cards = []
        for entry in ctx["battlecard"]:
            if isinstance(entry, dict) and _names_url(str(entry.get("source_url") or ""), names):
                dropped_for_source.append(f"battlecard:{entry.get('competitor', '')}")
                continue
            kept_cards.append(entry)
        ctx["battlecard"] = kept_cards
    out["people"] = False
    stats = {
        "names": names,
        "individuals_removed": len(individuals),
        "dropped_for_personal_source": len(dropped_for_source),
        "redactions": 0,
    }
    return out, stats


def _redact_plain(text: str, name_res: list[re.Pattern[str]], names: list[str]) -> tuple[str, int]:
    count = 0

    def email_sub(match: re.Match[str]) -> str:
        nonlocal count
        local, _, domain = match.group(0).partition("@")
        # hello@janedoe.com is a person's inbox when the domain is a recorded name.
        if local.lower() in ROLE_INBOXES and not url_names_person(domain, names):
            return match.group(0)
        count += 1
        return EMAIL_PLACEHOLDER

    def obfuscated_sub(match: re.Match[str]) -> str:
        nonlocal count
        if match.group(1).lower() in ROLE_INBOXES:
            return match.group(0)
        count += 1
        return EMAIL_PLACEHOLDER

    def bare_url_sub(match: re.Match[str]) -> str:
        nonlocal count
        url = match.group(0).rstrip(".,;:!?")
        if not _names_url("https://" + url, names):
            return match.group(0)
        count += 1
        return URL_PLACEHOLDER + match.group(0)[len(url):]

    text = EMAIL_RE.sub(email_sub, text)
    text = OBFUSCATED_EMAIL_RE.sub(obfuscated_sub, text)
    text = BARE_URL_RE.sub(bare_url_sub, text)
    for pattern in name_res:
        text, n = pattern.subn(NAME_PLACEHOLDER, text)
        count += n
    for pattern in (HANDLE_RE, REDDIT_USER_RE):
        text, n = pattern.subn(NAME_PLACEHOLDER, text)
        count += n
    return text, count


def redact_text(text: str, names: list[str]) -> tuple[str, int]:
    """Redact one string. URLs are handled whole (a non-personal URL is never
    edited, so citations to threads, repos, and company pages stay intact)."""
    # Composed form, so a decomposed accent matches the recorded name; the
    # fullwidth at sign is read as "@".
    text = unicodedata.normalize("NFC", text).replace("\uff20", "@")
    name_res = [_name_pattern(n) for n in _text_names(names)]
    pieces: list[str] = []
    count = 0
    last = 0
    for match in URL_RE.finditer(text):
        chunk, n = _redact_plain(text[last:match.start()], name_res, names)
        pieces.append(chunk)
        count += n
        url = match.group(0)
        if _names_url(url.rstrip(".,;:!?"), names):
            pieces.append(URL_PLACEHOLDER)
            count += 1
        else:
            pieces.append(url)
        last = match.end()
    chunk, n = _redact_plain(text[last:], name_res, names)
    pieces.append(chunk)
    count += n
    return "".join(pieces), count


def redact_people(obj: Any, names: list[str]) -> tuple[Any, int]:
    """Phase 2 (post-verification). Recursively redacts every string and every dict
    key that is not a schema identifier; drops list
    items that are nothing but a personal profile URL. Returns (copy, count)."""
    if isinstance(obj, str):
        return redact_text(obj, names)
    if isinstance(obj, list):
        out_list = []
        total = 0
        for item in obj:
            if isinstance(item, str) and URL_RE.fullmatch(item.strip()) and _names_url(item.strip(), names):
                total += 1
                continue
            value, n = redact_people(item, names)
            out_list.append(value)
            total += n
        return out_list, total
    if isinstance(obj, dict):
        out_dict = {}
        total = 0
        for key, value in obj.items():
            # Schema keys are snake_case identifiers; anything else may be a name or address.
            if isinstance(key, str) and not re.fullmatch(r"[a-z_][a-z0-9_]*", key):
                key, n = redact_text(key, names)
                total += n
            out_dict[key], n = redact_people(value, names)
            total += n
        return out_dict, total
    return obj, 0


def add_limits_note(data: dict[str, Any], stats: dict[str, Any]) -> None:
    """Disclose what the filter removed, once (re-runs replace the old note)."""
    note = (
        f"{PEOPLE_LIMITS_PREFIX} {stats['individuals_removed']} Individual(s) removed, "
        f"{stats['dropped_for_personal_source']} prospect(s) dropped because their only source "
        f"is a personal profile or post, {stats['redactions']} person reference(s) redacted from text. "
        "Pattern filter applied; review before publishing."
    )
    limits = [x for x in (data.get("limits") or []) if not str(x).startswith(PEOPLE_LIMITS_PREFIX)]
    limits.append(note)
    data["limits"] = limits


def has_prospects(data: dict[str, Any]) -> bool:
    return any(data.get(k) for k in ("individuals", "segments", "companies"))


def strip_people(data: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    """Both phases in one call, for callers that do not verify in between.
    Adds the `limits` disclosure only when something was removed, so running it
    again on already-filtered data keeps the original note."""
    dropped, stats = drop_people(data)
    redacted, count = redact_people(dropped, stats["names"])
    stats["redactions"] = count
    if stats["individuals_removed"] or stats["dropped_for_personal_source"] or count:
        add_limits_note(redacted, stats)
    return redacted, stats
