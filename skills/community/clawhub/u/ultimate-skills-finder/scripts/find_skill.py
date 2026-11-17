#!/usr/bin/env python3
"""
Ultimate Skills Finder
Multi-source agent skill discovery engine.

Searches 5 sources, cross-references, deduplicates, ranks, and optionally
requests advisory security-scan labels.

Design notes (v1.1.0):

* Install operations are carried as ARGV ARRAYS, never as shell strings.
  A command string is rendered only at display time via ``shlex.join``,
  and only from identifiers that passed ``validate_skill_id``.
* Sources are split into two classes:
    - "structured" registries (ClawHub, skills.sh) hand out real
      identifiers and therefore get an install command;
    - "browse-only" sources (SkillsMP, awesome-list, master-skills)
      surface a name and a link for a human to review. They never
      produce an install command, because their text is untrusted.
* ``--scan`` discloses URLs to a third party (Gen Digital) and therefore
  requires an explicit second consent flag.

Usage:
  python3 find_skill.py "web scraping"
  python3 find_skill.py "pdf editor" --scan --share-urls
  python3 find_skill.py "seo" --popular
  python3 find_skill.py "github" --show-install
  python3 find_skill.py "email" --json
  python3 find_skill.py "email" --source clawhub
"""

import argparse
import asyncio
import json
import math
import re
import shlex
import sys
import urllib.error
import urllib.parse
import urllib.request
from difflib import SequenceMatcher
from typing import Optional

# ── Configuration ────────────────────────────────────────────────────────────

REQUEST_TIMEOUT = 10
# Single source of truth for the version. Bump this BEFORE publishing.
#
# `clawhub publish --version X` rewrites the stamp in skill-card.md to X, but
# it does not touch this file. Publishing without bumping first therefore
# leaves the artifact claiming two different versions -- which has now
# happened twice (1.3.1 and 1.3.3), caught each time by
# DocsMatchTheCode.test_version_is_consistent_across_package.
#
# Publishing checklist: bump VERSION here, bump the "Skill Version(s)" line
# in skill-card.md, bump the "verified live against" line in
# references/sources.md, then publish with --version matching VERSION.
VERSION = "1.3.5"
USER_AGENT = f"UltimateSkillsFinder/{VERSION}"

CLAWHUB_SEARCH = "https://clawhub.ai/api/v1/search"
SKILLS_SH_SEARCH = "https://skills.sh/api/search"
SKILLSMP_SEARCH = "https://skillsmp.com/api/skills"
AWESOME_LIST_README = (
    "https://raw.githubusercontent.com/VoltAgent/awesome-openclaw-skills/main/README.md"
)
MASTER_SKILLS_README = (
    "https://raw.githubusercontent.com/LeoYeAI/openclaw-master-skills/main/README.md"
)

GEN_DIGITAL_URL = "https://ai.gendigital.com/api/scan/lookup"
GEN_DIGITAL_HOST = "ai.gendigital.com"

# Sources that hand out a machine-checkable identifier. Only these may
# produce an install command.
STRUCTURED_SOURCES = frozenset({"clawhub", "skills.sh"})

SOURCE_WEIGHTS = {
    "clawhub": 1.0,        # official OpenClaw registry
    "awesome-list": 0.9,   # curated README collection
    "skills.sh": 0.85,     # large directory with real install counts
    "master-skills": 0.85, # curated README collection
    "skillsmp": 0.7,       # raw aggregator, uncurated
}

# Shortest normalized name for which substring containment is treated as
# evidence that two results are the same skill. See fuzzy_match().
MIN_SUBSTRING = 3

# Control characters, C1, bidi overrides and zero-width joiners. Registry
# names and summaries are attacker-controlled and are printed raw, so an ESC
# sequence could forge a scan verdict or an install instruction on the user's
# terminal, and an OSC-52 sequence could write to their clipboard.
_UNSAFE_TEXT = re.compile(
    r"[\x00-\x1f\x7f-\x9f\u200b-\u200f\u2028\u2029\u202a-\u202e\u2060\ufeff]"
)


def sanitize_text(text) -> str:
    """Strip control and invisible characters from untrusted registry text."""
    if text is None:
        return ""
    return _UNSAFE_TEXT.sub(" ", str(text)).strip()


def is_disclosable_url(url) -> bool:
    """True when a URL is safe to display and safe to send.

    This is a disclosure gate, not a trust gate. Any http(s) URL may be sent
    to the scanner; `skills://`, `javascript:`, `file:` and `data:` must not.

    v1.2.2 checked only scheme and host, which left the hole the ClawHub
    security audit found: name, description, author and version all passed
    through sanitize_text(), but the URL did not. A listing could put ESC,
    OSC-52, BEL, a bidi override or zero-width characters in a URL and have
    them printed raw on the user's terminal.

    Hostile URLs are *rejected*, not cleaned. Silently rewriting one could
    point the user somewhere other than what the registry recorded.
    """
    if not url or not isinstance(url, str):
        return False
    if _UNSAFE_TEXT.search(url):
        return False
    try:
        parts = urllib.parse.urlsplit(url.strip())
    except ValueError:
        return False
    if parts.scheme.lower() not in ("http", "https"):
        return False
    if not parts.netloc:
        return False
    # Embedded credentials are a phishing shape; never display or transmit.
    if parts.username or parts.password:
        return False
    return True

# ClawHub returns skills.sh-origin entries under this prefix. It is stripped
# before validation because ":" is not legal in a bare identifier.
_SKILLS_SH_PREFIX = "skills-sh:"

# ── Identifier validation ────────────────────────────────────────────────────

# A skill identifier may only contain characters that are inert in a shell
# and safe as a path segment. Whitespace, ";", "|", "&", "$", backtick,
# parentheses, "<", ">", quotes, backslash, colon and control characters
# are all excluded by construction -- not filtered afterwards.
_SKILL_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._/-]{0,127}$")


def validate_skill_id(value) -> Optional[str]:
    """Return a safe identifier, or None if it cannot be trusted.

    Returns None rather than raising so that a hostile or malformed value
    simply drops out of the result set instead of aborting the search.
    """
    if not isinstance(value, str):
        return None
    candidate = value.strip()
    if not candidate or not _SKILL_ID_RE.fullmatch(candidate):
        return None
    # Reject path traversal and empty path segments even though the
    # character class above would allow the individual characters.
    if ".." in candidate or "//" in candidate or candidate.endswith("/"):
        return None
    return candidate


# ── Data Model ───────────────────────────────────────────────────────────────

class SkillResult:
    """One discovered skill.

    ``install_args`` is an argv list (for example
    ``["openclaw", "skills", "install", "@owner/slug"]``). It is never a
    shell string, so it cannot be split or re-interpreted by a shell.
    """

    def __init__(self, name: str, description: str = "", source: str = "",
                 install_args: Optional[list] = None, url: str = "",
                 stars: int = 0, downloads: int = 0,
                 author: str = "", version: str = ""):
        self.name = sanitize_text(name)[:120]
        self.description = sanitize_text(description)
        self.sources = [sanitize_text(source)] if source else []
        self.install_args = list(install_args) if install_args else []
        self.url = url if is_disclosable_url(url) else ""
        self.stars = max(int(stars or 0), 0)
        self.downloads = max(int(downloads or 0), 0)
        self.author = sanitize_text(author)
        self.version = sanitize_text(version)
        self.security = None  # SCAN_SEVERITIES | analysis_pending | None
        self.security_reasons = []

    @property
    def installable(self) -> bool:
        return bool(self.install_args)

    def merge(self, other: "SkillResult"):
        """Fold a duplicate finding from another source into this one."""
        for s in other.sources:
            if s and s not in self.sources:
                self.sources.append(s)
        self.stars = max(self.stars, other.stars)
        self.downloads = max(self.downloads, other.downloads)
        # A structured source (ClawHub, skills.sh) outranks a browse-only
        # index. "Longest wins" let a hostile SkillsMP or README entry replace
        # the registry's own summary with a longer attacker-written one.
        self_struct = any(s in STRUCTURED_SOURCES for s in self.sources)
        other_struct = any(s in STRUCTURED_SOURCES for s in other.sources)
        if other_struct != self_struct:
            if other_struct and other.description:
                self.description = other.description
        elif len(other.description) > len(self.description):
            self.description = other.description
        # A URL only ever fills an empty slot, and only if it is disclosable.
        if not self.url and is_disclosable_url(other.url):
            self.url = other.url
        if other.author and not self.author:
            self.author = other.author
        if other.version and not self.version:
            self.version = other.version
        # Only inherit install args if we do not already have them.
        if other.install_args and not self.install_args:
            self.install_args = list(other.install_args)
        if other.security and not self.security:
            self.security = other.security
        if other.security_reasons and not self.security_reasons:
            self.security_reasons = list(other.security_reasons)

    def _pop_log(self) -> float:
        """Log-scaled popularity in 0..1.

        v1.3.0 used ``installs / 10000`` clamped to 1.0. In a measured corpus
        of 93 results across 8 queries, 21 sat at or above that cap, so
        11 installs and 1,069,913 both scored exactly 1.00 and the term
        carried no information between popular skills. Log scaling keeps the
        ordering across five orders of magnitude.
        """
        if self.downloads:
            return min(math.log1p(self.downloads) / POP_LOG_CAP, 1.0)
        return min(math.log1p(self.stars) / math.log1p(POP_STAR_CAP), 1.0)

    def score(self, query: Optional[str] = None) -> float:
        """Ranking score in the 0-1 range.

        With a query, relevance leads and the social/authority terms are
        demoted: a good fit beats a popular near-miss. Without one, the
        v1.2.x weighting is preserved so callers that pass nothing keep their
        existing behaviour rather than silently changing rank.
        """
        # Use the strongest source we saw, not merely the first one.
        authority = max(
            (SOURCE_WEIGHTS.get(s, 0.5) for s in self.sources), default=0.5
        )
        breadth = min(len(self.sources) / len(SOURCE_WEIGHTS), 1.0)
        if self.downloads:
            popularity = min(self.downloads / 10000.0, 1.0)
        else:
            popularity = min(self.stars / 100.0, 1.0)
        if query is None:
            return breadth * 0.35 + popularity * 0.35 + authority * 0.30
        fit = relevance(query, self)
        return (fit * 0.40 + breadth * 0.20
                + self._pop_log() * 0.25 + authority * 0.15)

    def security_label(self) -> str:
        if not self.security:
            return "not scanned"
        # Gen Digital's live vocabulary is SAFE/LOW/MEDIUM/HIGH/CRITICAL.
        # A live probe returned MEDIUM, which the pre-v1.2.0 set did not
        # contain. WARNING/DANGEROUS/MALICIOUS are the old names, kept so a
        # verdict already recorded elsewhere still renders.
        labels = {
            "SAFE": "SAFE (advisory)",
            "LOW": "LOW severity",
            "MEDIUM": "MEDIUM severity",
            "HIGH": "HIGH severity",
            "CRITICAL": "CRITICAL severity",
            "analysis_pending": "pending review",
            "WARNING": "WARNING",
            "DANGEROUS": "DANGEROUS",
            "MALICIOUS": "MALICIOUS",
        }
        return labels.get(self.security, self.security)

    def as_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description[:200],
            "sources": self.sources,
            "score": round(self.score(), 3),
            "downloads": self.downloads,
            "stars": self.stars,
            "installable": self.installable,
            "install_args": list(self.install_args),
            "security": self.security,
            "security_reasons": list(self.security_reasons),
            "url": self.url,
            "author": self.author,
            "version": self.version,
        }


def render_command(args: list) -> str:
    """Render an argv array as a copy-pasteable, correctly quoted command."""
    return shlex.join([str(a) for a in args])


# ── HTTP helpers ─────────────────────────────────────────────────────────────

def _fetch_json_sync(url: str) -> Optional[dict]:
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": USER_AGENT}, method="GET"
        )
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, ValueError, OSError):
        return None


def _fetch_text_sync(url: str) -> Optional[str]:
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": USER_AGENT}, method="GET"
        )
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except (urllib.error.URLError, OSError):
        return None


async def fetch_json(url: str) -> Optional[dict]:
    """Async JSON GET. Runs the blocking call in a worker thread."""
    return await asyncio.to_thread(_fetch_json_sync, url)


async def fetch_text(url: str) -> Optional[str]:
    """Async text GET. Runs the blocking call in a worker thread."""
    return await asyncio.to_thread(_fetch_text_sync, url)


# ── Source searchers ─────────────────────────────────────────────────────────

async def search_clawhub(query: str, limit: int = 5) -> list:
    """ClawHub official registry.

    The public search endpoint returns a structured ``install.reference``
    of the form ``owner/slug``. Only that field is ever used to build an
    install command, and only after validation.
    """
    url = f"{CLAWHUB_SEARCH}?q={urllib.parse.quote(query)}&limit={limit}"
    data = await fetch_json(url)
    if not data:
        return []
    results = []
    for item in (data.get("results") or [])[:limit]:
        if not isinstance(item, dict):
            continue
        install = item.get("install") or {}
        kind = install.get("kind") or ""
        reference = install.get("reference") or ""
        slug = item.get("slug") or ""
        display = item.get("displayName") or slug
        stats = ((item.get("native") or {}).get("skill") or {}).get("stats") or {}

        # ClawHub indexes both its own skills and skills.sh ones, and the
        # two use different reference formats. Branch on install.kind
        # rather than guessing, so each is validated in its own shape.
        install_args = []
        if kind == "clawhub":
            # reference is "owner/slug"
            safe = validate_skill_id(reference)
            if safe:
                install_args = ["openclaw", "skills", "install", f"@{safe}"]
        elif kind == "skills-sh":
            # reference is "skills-sh:owner/repo/skill"
            payload = reference[len(_SKILLS_SH_PREFIX):] \
                if reference.startswith(_SKILLS_SH_PREFIX) else ""
            safe = validate_skill_id(payload)
            if safe:
                install_args = [
                    "openclaw", "skills", "install",
                    f"{_SKILLS_SH_PREFIX}{safe}",
                ]
        if not display:
            continue
        # Attribute by ORIGIN, not by surface. ClawHub mirrors skills.sh
        # entries (measured: 12 of 77 sampled results carried
        # kind == "skills-sh" with no native block). Crediting those to
        # clawhub handed skills.sh's skills clawhub's 1.00 authority for
        # merely passing through, and inflated their rank.
        origin = "skills.sh" if kind == "skills-sh" else "clawhub"
        results.append(SkillResult(
            name=display,
            description=item.get("summary") or "",
            source=origin,
            install_args=install_args,
            url=f"https://clawhub.ai{item.get('canonicalUrl') or ''}"
                if item.get("canonicalUrl") else "",
            downloads=item.get("downloads") or stats.get("downloads") or 0,
            stars=stats.get("stars") or 0,
            author=item.get("ownerHandle") or "",
            version=item.get("version") or "",
        ))
    return results


async def search_skills_sh(query: str, limit: int = 5) -> list:
    """skills.sh directory (Algolia-backed).

    Returns ``id`` as ``owner/repo/skill`` with no free-text field, so
    the identifier is already structured. Descriptions are not provided
    by this endpoint, so a skills.sh-only hit shows a blank description.
    """
    url = f"{SKILLS_SH_SEARCH}?q={urllib.parse.quote(query)}&limit={limit}"
    data = await fetch_json(url)
    if not data:
        return []
    results = []
    for item in (data.get("skills") or [])[:limit]:
        if not isinstance(item, dict):
            continue
        source_slug = validate_skill_id(item.get("source"))
        skill_slug = validate_skill_id(item.get("skillId"))
        name = item.get("name") or skill_slug or ""
        if not name:
            continue
        install_args = (
            ["openclaw", "skills", "install",
             f"skills-sh:{source_slug}/{skill_slug}"]
            if source_slug and skill_slug else []
        )
        results.append(SkillResult(
            name=name,
            description="",
            source="skills.sh",
            install_args=install_args,
            url=f"https://skills.sh/{source_slug}/{skill_slug}"
                if source_slug and skill_slug else "",
            downloads=item.get("installs") or 0,
            author=(source_slug or "").split("/")[0],
        ))
    return results


async def search_skillsmp(query: str, limit: int = 5) -> list:
    """SkillsMP aggregator.

    Browse-only. This index is raw and uncurated, so no install command
    is generated -- only a name, a description and a GitHub link.
    """
    url = f"{SKILLSMP_SEARCH}?search={urllib.parse.quote(query)}&limit={limit}"
    data = await fetch_json(url)
    if not data:
        return []
    results = []
    for item in (data.get("skills") or [])[:limit]:
        if not isinstance(item, dict):
            continue
        name = item.get("name") or ""
        if not name or not validate_skill_id(name):
            continue
        results.append(SkillResult(
            name=name,
            description=item.get("description") or "",
            source="skillsmp",
            install_args=[],
            url=item.get("githubUrl") or "",
            # Deliberately not populated. SkillsMP returns the *repository*
            # star count, not a per-skill figure, so treating it as skill
            # popularity saturates the ranking term and floats unrelated
            # results above genuinely-installed ones.
            stars=0,
            author=item.get("author") or "",
        ))
    return results


def _extract_markdown_entries(lines: list, query: str) -> list:
    """Pull candidate (name, description, url) triples out of a README.

    Shared by the two browse-only curated-list sources.
    """
    needle = query.lower()
    found = []
    for line in lines:
        if needle not in line.lower():
            continue
        stripped = line.strip()
        if stripped.startswith(("#", "![", "<")):
            continue
        if "img.shields.io" in stripped:
            continue

        # Markdown table row: | `name` | description |
        table = re.search(r"\|\s*`([^`]+)`\s*\|\s*([^|]*)", stripped)
        if table:
            found.append((table.group(1), table.group(2).strip(), ""))
            continue

        # Link list: [name](url)
        for name, link in re.findall(r"\[([^\]]+)\]\(([^)]+)\)", stripped):
            low = name.lower()
            if any(word in low for word in ("img", "badge", "http", "license")):
                continue
            if not any(token in link.lower() for token in ("skill", "github", "clawhub")):
                continue
            found.append((name, "", link))
    return found


async def search_curated_readme(query: str, limit: int, readme_url: str,
                               source: str, fallback_url: str) -> list:
    """Generic browse-only search over a curated GitHub README.

    Names come from text a third party can edit, so they are never turned
    into an install command. We deliberately do not even display a
    reconstructed command for these: the identifier is not trustworthy
    enough to render as if it were a real product code.
    """
    text = await fetch_text(readme_url)
    if not text:
        return []
    found = _extract_markdown_entries(text.split("\n"), query)
    results, seen = [], set()
    for raw_name, desc, link in found:
        name = raw_name.strip().strip("`").strip("*").strip()
        key = name.lower()
        if not name or key in seen:
            continue
        seen.add(key)
        results.append(SkillResult(
            name=name,
            description=desc[:200],
            source=source,
            install_args=[],
            url=link or fallback_url,
        ))
        if len(results) >= limit:
            break
    return results


async def search_awesome_list(query: str, limit: int = 5) -> list:
    return await search_curated_readme(
        query, limit, AWESOME_LIST_README, "awesome-list",
        "https://github.com/VoltAgent/awesome-openclaw-skills",
    )


async def search_master_skills(query: str, limit: int = 5) -> list:
    return await search_curated_readme(
        query, limit, MASTER_SKILLS_README, "master-skills",
        "https://github.com/LeoYeAI/openclaw-master-skills",
    )


SOURCE_SEARCHERS = {
    "clawhub": search_clawhub,
    "skills.sh": search_skills_sh,
    "skillsmp": search_skillsmp,
    "awesome-list": search_awesome_list,
    "master-skills": search_master_skills,
}


# ── Deduplication ────────────────────────────────────────────────────────────

def normalize_name(name: str) -> str:
    name = (name or "").lower().strip()
    name = re.sub(r"[^a-z0-9-]", "-", name)
    return re.sub(r"-+", "-", name).strip("-")


# Script ranges. Han is listed separately from kana because Han characters
# are also Japanese kanji: kana present means Japanese, and a naive
# "contains CJK" filter would delete Japanese skills as collateral damage.
_HAN = ((0x3400, 0x4DBF), (0x4E00, 0x9FFF), (0xF900, 0xFAFF),
        (0x20000, 0x2A6DF))
_KANA = ((0x3040, 0x309F), (0x30A0, 0x30FF))
_HANGUL = ((0x1100, 0x11FF), (0x3130, 0x318F), (0xA960, 0xA97F),
           (0xAC00, 0xD7AF))

CJK_SHARE_THRESHOLD = 0.15


def script_counts(text) -> tuple:
    """(han, kana, hangul, other-letter-or-digit) counts for `text`."""
    han = kana = hangul = other = 0
    for ch in (text or ""):
        o = ord(ch)
        if any(a <= o <= b for a, b in _HAN):
            han += 1
        elif any(a <= o <= b for a, b in _KANA):
            kana += 1
        elif any(a <= o <= b for a, b in _HANGUL):
            hangul += 1
        elif ch.isalpha() or ch.isdigit():
            other += 1
    return han, kana, hangul, other


def is_chinese_text(text, threshold: float = CJK_SHARE_THRESHOLD) -> bool:
    """True when `text` is predominantly written in Chinese.

    Presence-based detection is wrong in both directions: a single emoji or
    stray glyph must not delete an English skill, and a long English sentence
    quoting a product name must not read as Chinese. So this requires Han to
    make up a meaningful share of the letters, and treats any kana as proof
    the text is Japanese rather than Chinese.
    """
    han, kana, _hangul, other = script_counts(text)
    if not han or kana:
        return False
    return han / float(han + other) >= threshold


def is_chinese_result(result) -> bool:
    return is_chinese_text(result.name) or is_chinese_text(result.description)


def filter_chinese(results: list) -> list:
    """Drop Chinese-language results, saying how many went.

    Never silent: a filter that quietly removes candidates is indistinguishable
    from a registry that simply has nothing.
    """
    if not results:
        return []
    kept = [r for r in results if not is_chinese_result(r)]
    dropped = len(results) - len(kept)
    if dropped:
        print(f"  Filtered out {dropped} result(s) written in Chinese",
              file=sys.stderr)
    return kept


QUERY_STOPWORDS = frozenset({
    "a", "an", "and", "are", "as", "at", "be", "best", "but", "by", "can",
    "do", "does", "for", "from", "get", "give", "good", "help", "how", "i",
    "in", "into", "is", "it", "make", "me", "my", "need", "of", "on", "or",
    "our", "should", "skill", "skills", "so", "some", "that", "the", "their",
    "them", "then", "there", "this", "to", "tool", "tools", "up", "us", "use",
    "using", "want", "was", "what", "when", "which", "will", "with", "you",
    "your",
})

_TOKEN_RE = re.compile(r"[a-z0-9]+")

POP_LOG_CAP = math.log1p(1_000_000)
POP_STAR_CAP = 2_000


def _tokens(text) -> list:
    return _TOKEN_RE.findall((text or "").lower())


def relevance(query: str, result) -> float:
    """How well a result fits the query, in 0..1.

    v1.3.0. `score()` previously had no query term at all, so a popular skill
    matching one query word outranked a better-fitting one -- a live
    "pdf editor" search ranked a Japanese visa-translation skill fourth on
    the word "PDF" alone.

    Name matches count double description matches, partial (prefix) matches
    count 0.6, and an exact normalised name match saturates the term. An empty
    or all-stopword query returns a neutral 0.5 rather than 0, because such a
    query carries no signal and must not bury every result.
    """
    tokens = [t for t in _tokens(query) if t not in QUERY_STOPWORDS]
    if not tokens:
        return 0.5
    name_pool = _tokens(result.name)
    desc_pool = _tokens(result.description)

    def hit(token: str, pool: list) -> float:
        if token in pool:
            return 1.0
        for item in pool:
            if item.startswith(token) or token.startswith(item):
                return 0.6
        return 0.0

    name_hits = sum(hit(t, name_pool) for t in tokens)
    desc_hits = sum(hit(t, desc_pool) for t in tokens)
    score = (name_hits * 2.0 + desc_hits) / (len(tokens) * 3.0)

    # Phrase bonus must be built from the *filtered* tokens, not the raw
    # query: normalising "a pdf editor for the" yields "pdf-editor-for-the",
    # which never matches the name "pdf-editor" and silently loses the bonus.
    norm_q = "-".join(tokens)
    norm_n = normalize_name(result.name)
    if norm_q and norm_q == norm_n:
        score = 1.0
    elif norm_q and norm_q in norm_n:
        score += 0.15
    return min(1.0, max(0.0, score))


def fuzzy_match(name1: str, name2: str, threshold: float = 0.90) -> bool:
    """Decide whether two names refer to the same skill.

    Normalised equality is the contract. Beyond that, a match requires the
    shorter name's tokens to be a *prefix* of the longer one's and the overall
    strings to be very similar.

    Raw substring containment was tried first and rejected: it matched
    distinct skills ("mail"/"email", "sql"/"mysql", "bar"/"foobar") and it
    composed transitively, so `pdf`, `pdf-editor`, `pdf-editor-pro` and
    `pdf-editor-pro-max` collapsed into a single result that then inherited
    all four sources, inflating its own breadth score.
    """
    n1, n2 = normalize_name(name1), normalize_name(name2)
    if not n1 or not n2:
        return False
    if n1 == n2:
        return True
    t1, t2 = n1.split("-"), n2.split("-")
    shorter, longer = (t1, t2) if len(t1) <= len(t2) else (t2, t1)
    if shorter != longer[:len(shorter)]:
        return False
    return SequenceMatcher(None, n1, n2).ratio() >= threshold


def deduplicate(results: list) -> list:
    merged = []
    for r in results:
        for existing in merged:
            if fuzzy_match(r.name, existing.name):
                existing.merge(r)
                break
        else:
            merged.append(r)
    return merged


# ── Advisory security scan (third-party disclosure) ──────────────────────────

SCAN_SEVERITIES = ("SAFE", "LOW", "MEDIUM", "HIGH", "CRITICAL")
SCAN_RETRY_DELAY = 2.0   # seconds, linear backoff between attempts
SCAN_ATTEMPTS = 3

# Live 2026-10-16: outages arrive with HTTP 200 and status "error", so the
# HTTP status alone cannot separate a retryable outage from a real answer.
SCAN_TRANSIENT_MARKERS = ("temporarily unavailable", "try again later")


def normalize_scan_url(url: str) -> str:
    """Reduce a ClawHub URL to the {owner}/{skill} form Gen Digital parses.

    ClawHub canonical URLs may carry a repo-style middle segment, e.g.
    ``/utromaya-code/skills/nano-pdf-editor``. Sent verbatim, the scanner read
    "skills" as the skill name and answered "Skill not found" for every skill
    under such a path. Live-verified: the raw form 404s on the scanner while
    ``/utromaya-code/nano-pdf-editor`` returns a real verdict.

    Only clawhub.ai is rewritten. Every other host is returned untouched, and
    a path with fewer than two segments is left alone.
    """
    if not isinstance(url, str) or not url:
        return url
    if not is_disclosable_url(url):
        # Fail closed. A URL carrying terminal-control characters must never
        # reach the scanner, and must not be "cleaned" into a different target.
        return ""
    parts = urllib.parse.urlsplit(url)
    if parts.netloc.lower() not in ("clawhub.ai", "www.clawhub.ai"):
        return url
    segments = [s for s in parts.path.split("/") if s]
    if len(segments) < 2:
        return url
    if len(segments) > 2:
        segments = [segments[0], segments[-1]]
    return urllib.parse.urlunsplit(
        (parts.scheme, parts.netloc, "/" + "/".join(segments),
         parts.query, parts.fragment)
    )


def _in_band_transient(data: dict) -> bool:
    """True when a response is a retryable outage reported at HTTP 200.

    'Skill not found on ClawHub or failed to fetch metadata' is permanent and
    must not be retried; 'Skill analyzer temporarily unavailable' should be.
    """
    if not isinstance(data, dict) or data.get("status") != "error":
        return False
    message = str(data.get("message") or "").lower()
    return any(marker in message for marker in SCAN_TRANSIENT_MARKERS)


MAX_RESPONSE_BYTES = 2_000_000


def _post_scan_sync(payload: bytes) -> dict:
    """Blocking POST, run in a worker thread by scan_skill."""
    req = urllib.request.Request(
        GEN_DIGITAL_URL,
        data=payload,
        headers={"Content-Type": "application/json",
                 "User-Agent": USER_AGENT},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
        raw = resp.read(MAX_RESPONSE_BYTES)
    return json.loads(raw.decode("utf-8", errors="replace"))


async def scan_skill(url: str, attempts: int = SCAN_ATTEMPTS,
                     reasons_into: Optional[list] = None) -> Optional[str]:
    """Ask Gen Digital for an advisory verdict on one skill URL.

    A verdict looks like ``{"severity": "...", "reasons": [...]}``. There is
    no ``status`` key on a completed lookup: v1.0.0 gated on
    ``status == "done"``, which never matched a live response, so every scan
    silently returned None.

    Errors arrive in-band -- HTTP 200 with ``status: "error"`` -- so an
    outage is detected from the message, not the HTTP status.

    Returns a value from SCAN_SEVERITIES, ``analysis_pending``, or None.
    None means "no verdict available" -- never "this skill is fine".
    """
    target = normalize_scan_url(url)
    if not target:
        return None
    payload = json.dumps({"skillUrl": target}).encode()
    data: dict = {}
    for attempt in range(1, max(1, attempts) + 1):
        try:
            data = await asyncio.to_thread(_post_scan_sync, payload)
        except urllib.error.HTTPError as exc:
            # 429 and 5xx may clear; other 4xx will not resolve on retry.
            if not (exc.code == 429 or exc.code >= 500):
                return None
            if attempt >= attempts:
                return None
            await asyncio.sleep(SCAN_RETRY_DELAY * attempt)
        except (urllib.error.URLError, TimeoutError, OSError):
            if attempt >= attempts:
                return None
            await asyncio.sleep(SCAN_RETRY_DELAY * attempt)
        except Exception:
            return None
        else:
            if _in_band_transient(data) and attempt < attempts:
                await asyncio.sleep(SCAN_RETRY_DELAY * attempt)
                continue
            break

    if not isinstance(data, dict):
        return None
    if data.get("status") == "analysis_pending":
        return "analysis_pending"
    severity = data.get("severity")
    if isinstance(severity, str):
        severity = severity.strip().upper()
        if severity in SCAN_SEVERITIES:
            if reasons_into is not None:
                reasons = data.get("reasons")
                if isinstance(reasons, list):
                    reasons_into.extend(
                        sanitize_text(x) for x in reasons if x)
            return severity
    return None


async def scan_results(results: list):
    """Scan results, throttled. Caller must have obtained consent."""
    targets = [r for r in results if r.url]
    print(f"  Disclosing {len(targets)} URL(s) to {GEN_DIGITAL_HOST}...",
          file=sys.stderr)
    sem = asyncio.Semaphore(3)

    async def one(r: SkillResult):
        reasons: list = []
        async with sem:
            r.security = await scan_skill(r.url, reasons_into=reasons)
            r.security_reasons = list(reasons)
            if r.security:
                print(f"    {r.name}: {r.security_label()}", file=sys.stderr)
        # Throttle outside the semaphore. Sleeping while holding a slot makes
        # effective concurrency 3/(0.5 + latency) rather than 3.
        await asyncio.sleep(0.5)

    await asyncio.gather(*(one(r) for r in targets))


# ── Orchestrator ─────────────────────────────────────────────────────────────

async def find_skills(query: str, limit: int = 5, scan: bool = False,
                      popular: bool = False, sources: Optional[list] = None,
                      exclude_chinese: bool = False) -> list:
    selected = dict(SOURCE_SEARCHERS)
    if sources:
        selected = {k: v for k, v in selected.items() if k in sources}
    if not selected:
        return []

    print(f"  Searching {len(selected)} source(s) for \"{query}\"...",
          file=sys.stderr)

    batches = await asyncio.gather(
        *(searcher(query, limit) for searcher in selected.values()),
        return_exceptions=True,
    )

    raw = []
    failed = []
    for name, batch in zip(selected, batches):
        if isinstance(batch, BaseException):
            failed.append((name, batch))
        elif isinstance(batch, list):
            raw.extend(batch)

    # A source that crashed is not a source with no results. Saying so is the
    # difference between "this skill does not exist" and "the registry broke".
    if failed:
        print(f"  {len(failed)} source(s) failed:", file=sys.stderr)
        for name, exc in failed:
            print(f"    {name}: {type(exc).__name__}: {exc}", file=sys.stderr)

    if not raw:
        return []

    merged = deduplicate(raw)
    print(f"  {len(raw)} raw result(s) -> {len(merged)} unique", file=sys.stderr)

    if exclude_chinese:
        merged = filter_chinese(merged)

    if popular:
        merged.sort(key=lambda r: (r.downloads, r.stars), reverse=True)
    else:
        # v1.3.0: the query finally reaches the ranking function.
        merged.sort(key=lambda r: r.score(query), reverse=True)

    if scan and merged:
        await scan_results(merged)

    return merged


# ── Output ───────────────────────────────────────────────────────────────────

def display_results(results: list, query: str, show_install: bool = False,
                    json_output: bool = False):
    if not results:
        print(f"\n  No skills found for \"{query}\".")
        print("  Try a broader or synonymous term, or browse:")
        print("    https://clawhub.ai   https://skills.sh")
        return

    if json_output:
        print(json.dumps([r.as_dict() for r in results], indent=2))
        return

    medals = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
    print("\n  " + "=" * 60)
    print(f"  Results for \"{query}\" - {len(results)} unique skill(s)")
    print("  " + "=" * 60)

    for i, r in enumerate(results[:10]):
        rank = medals[i] if i < len(medals) else str(i + 1)
        pop = f"{r.downloads:,} installs" if r.downloads else (
            f"{r.stars:,} stars" if r.stars else "")
        print(f"\n  {rank:>2}. {r.name}")
        print(f"      {' | '.join(r.sources)}"
              + (f"   ({pop})" if pop else ""))
        if r.description:
            desc = r.description[:160]
            print(f"      {desc}{'...' if len(r.description) > 160 else ''}")
        elif r.sources == ["skills.sh"]:
            print("      (skills.sh returns no description for this entry)")
        if r.url:
            print(f"      {sanitize_text(r.url)}")
        if r.security:
            print(f"      scan: {r.security_label()}")
            for reason in (r.security_reasons or [])[:3]:
                print(f"        - {reason[:160]}")
        if show_install and r.installable:
            print(f"      install: {render_command(r.install_args)}")

    installable = sum(1 for r in results if r.installable)
    if installable:
        print(f"\n  {installable} of {len(results)} have a verified install path.")
        print("  The rest are browse-only (uncurated indexes). Review those yourself.")
    else:
        print("\n  No installable entries in this result set.")


def main():
    parser = argparse.ArgumentParser(
        description="Ultimate Skills Finder - multi-source skill discovery",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 find_skill.py "web scraping"           Basic search
  python3 find_skill.py "pdf" --show-install     Include install commands
  python3 find_skill.py "seo" --popular          Sort by popularity
  python3 find_skill.py "email" --json           JSON output
  python3 find_skill.py "email" --source clawhub One source only
  python3 find_skill.py "pdf" --scan --share-urls   Advisory scan (sends URLs)
        """,
    )
    parser.add_argument("query", help="Search query")
    parser.add_argument("--limit", type=int, default=5,
                        help="Max results per source (default: 5)")
    parser.add_argument("--scan", action="store_true",
                        help="Request advisory security labels from Gen Digital "
                             "(requires --share-urls)")
    parser.add_argument("--share-urls", action="store_true",
                        help="Consent to sending result URLs to Gen Digital")
    parser.add_argument("--popular", action="store_true",
                        help="Sort by popularity instead of relevance")
    parser.add_argument("--exclude-chinese", action="store_true",
                        help="Drop results whose name or description is "
                             "written in Chinese. Japanese and Korean text "
                             "is kept.")
    parser.add_argument("--show-install", action="store_true",
                        help="Show install commands for sources that have a "
                             "verified install path")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--source", choices=sorted(SOURCE_SEARCHERS) + ["all"],
                        default="all", help="Limit to a specific source")
    args = parser.parse_args()

    # A non-positive limit produced "No skills found" -- the exact signature of
    # an empty registry, so a typo looked like a missing skill.
    if args.limit < 1:
        parser.error("--limit must be at least 1, got %d" % args.limit)

    if args.scan and not args.share_urls:
        parser.error(
            "--scan sends the URL of every result to %s, a third party.\n"
            "Re-run with --scan --share-urls to consent to that disclosure,\n"
            "or drop --scan to search without any external disclosure."
            % GEN_DIGITAL_HOST
        )

    sources = None if args.source == "all" else [args.source]

    results = asyncio.run(find_skills(
        query=args.query,
        limit=args.limit,
        scan=args.scan,
        popular=args.popular,
        sources=sources,
        exclude_chinese=args.exclude_chinese,
    ))

    display_results(results, args.query,
                    show_install=args.show_install,
                    json_output=args.json)


if __name__ == "__main__":
    main()