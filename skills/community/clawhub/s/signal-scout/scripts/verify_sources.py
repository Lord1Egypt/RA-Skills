#!/usr/bin/env python3
"""Verify signal-scout prospect sources before generating the report.

For each prospect in analysis.json, checks that source_url resolves and that
the cited `evidence` actually appears on the fetched page. This catches dead
links, wrong URLs, evidence paraphrased from a search snippet rather than the
page itself, and — the case that matters most — claims that are simply not in
the source at all, which self-graded `evidence_quality` scores never catch
because the model grading the evidence is the model that invented it.

It is a containment check, not proof of authenticity: it can tell you a claim
is absent from a page, and it can tell you a claim is quoted from one. It
cannot tell you the page is honest, or that a correctly-quoted line means what
the prospect record says it means.

Every prospect is stamped with `verified_at` (today's date) regardless of
tier, so a report generated later can show how stale its verification is —
that's a display concern, handled by generate_report.py, not this script.
Every individual's outreach `opener` is also checked against its own
`evidence` (not the live page) and flagged with `opener_grounding_note` if it
references specifics the evidence doesn't support — a softer, separate signal
from verification_tier that doesn't fail the run or drop the prospect.

Usage:
    python3 verify_sources.py analysis.json [--timeout 10]
        [--annotate-out OUT.json] [--handoff-out HANDOFF.json]

Exit code is non-zero if any source is unreachable (dead link, invalid URL) or
any claim is missing from its live page. Paraphrase is reported, not failed —
rewording a real signal is legitimate; inventing one is not.

Every fetch goes through safe_fetch.py: source_url is untrusted, so non-http(s)
schemes and loopback, private and cloud-metadata addresses are refused, also
after a redirect or a DNS answer, and tier as Broken. --allow-private-addresses
turns the address check off for checking a local copy of a page. HTTP(S)_PROXY
is ignored unless --use-proxy is passed.

Reddit's new UI (reddit.com / www.reddit.com) serves a client-side
bot-verification interstitial to script fetches — HTTP 200, but the page is
just a "please wait for verification" stub, not the real thread. old.reddit.com
serves the same content server-rendered, with no such wall, so reddit.com and
www.reddit.com URLs are fetched via their old.reddit.com equivalent instead
(the URL recorded on the prospect is left untouched — only the fetch target
changes). Other known bot-walled platforms (X/Twitter, LinkedIn, Glassdoor,
Indeed) still 403/429 real script fetches outright — that's a platform
anti-bot wall, not evidence the link is broken, so those fall back to the
Wayback Machine like any other unreadable page before tiering as
snippet-only.
"""

from __future__ import annotations

import argparse
import dataclasses
import json
import re
import sys
import urllib.error
import urllib.request
from datetime import date
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from safe_fetch import BlockedURL, FetchPolicy, open_url
from signal_scout_core import (
    TIER_BROKEN,
    TIER_DISQUALIFYING,
    TIER_LABELS,
    TIER_SNIPPET_ONLY,
    TIER_UNSUPPORTED,
    opener_grounding_note,
    tier_for_evidence,
)

# Direct connections by default, so every address is checked at connect time.
# Proxy mode is opt-in (--use-proxy): the proxy connects, so the check runs
# before the request and a rebinding DNS answer can still differ.
POLICY = FetchPolicy()
PROXY_HINT = ("HTTP(S)_PROXY is set but was not used. If this machine has no direct route out "
              "(a sandbox), re-run with --use-proxy; the address check is weaker through a proxy.")


def env_proxy_set() -> bool:
    return any(urllib.request.getproxies().get(s) for s in ("http", "https"))


BOT_WALLED_DOMAINS = (
    "reddit.com",
    "x.com",
    "twitter.com",
    "linkedin.com",
    "glassdoor.com",
    "indeed.com",
)


def bot_walled_host(url: str) -> str | None:
    """Return the matched domain if url's host is a platform known to 403/429
    scripted fetches regardless of whether the page is actually live, else None."""
    host = urlparse(url).netloc.lower()
    for domain in BOT_WALLED_DOMAINS:
        if host == domain or host.endswith("." + domain):
            return domain
    return None


CHALLENGE_MARKERS = ("please wait for verification", "checking your browser")


def canonicalize_for_fetch(url: str) -> str:
    """reddit.com/www.reddit.com serve a client-side bot-verification stub to script
    fetches; old.reddit.com serves the same page server-rendered with no such wall.
    Rewrite just the fetch target — the URL shown to the user is untouched."""
    parsed = urlparse(url)
    if parsed.netloc.lower() in ("reddit.com", "www.reddit.com"):
        return parsed._replace(netloc="old.reddit.com").geturl()
    return url


def is_challenge_page(status: int | None, text: str) -> bool:
    if status != 200 or len(text) > 200:
        return False
    lowered = text.lower()
    return any(marker in lowered for marker in CHALLENGE_MARKERS)


# Meta keys whose content is worth harvesting on JS-rendered pages — an SPA
# shell often carries the page's real substance only here and in JSON-LD.
_META_KEYS = frozenset({
    "description", "og:description", "og:title", "twitter:description", "twitter:title",
})


def _ldjson_strings(raw: str) -> str:
    """Extract the human-readable string values from a JSON-LD block. On parse
    failure return the raw text — partial signal beats none."""
    try:
        parsed = json.loads(raw)
    except (json.JSONDecodeError, ValueError):
        return raw
    found: list[str] = []

    def walk(node: Any) -> None:
        if isinstance(node, str):
            found.append(node)
        elif isinstance(node, dict):
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    walk(parsed)
    return " ".join(found)


# Tags that sit inside a word or sentence. Every other tag ends a block, and
# its text must not run into the next block's ("<li>a</li><li>b</li>").
_INLINE_TAGS = frozenset({
    "a", "abbr", "b", "bdi", "bdo", "cite", "code", "del", "dfn", "em", "font", "i", "ins", "kbd", "mark",
    "q", "s", "samp", "small", "span", "strong", "sub", "sup", "time", "u", "var", "wbr",
})


class _TextExtractor(HTMLParser):
    """Visible text, plus meta descriptions and JSON-LD string values —
    the latter two are what a JS-rendered page still exposes to a plain fetch,
    and are often enough to verify a claim that would otherwise be Unverified."""

    def __init__(self) -> None:
        super().__init__()
        self._chunks: list[str] = []
        self._skip = False
        self._in_ldjson = False

    def handle_starttag(self, tag: str, attrs: Any) -> None:
        if tag not in _INLINE_TAGS:
            self._chunks.append(" ")
        if tag == "script":
            attr_map = dict(attrs)
            self._in_ldjson = (attr_map.get("type") or "").strip().lower() == "application/ld+json"
            self._skip = not self._in_ldjson
        elif tag == "style":
            self._skip = True
        elif tag == "meta":
            attr_map = dict(attrs)
            key = (attr_map.get("name") or attr_map.get("property") or "").strip().lower()
            content = attr_map.get("content")
            if key in _META_KEYS and content:
                self._chunks.append(f" {content} ")

    def handle_endtag(self, tag: str) -> None:
        if tag not in _INLINE_TAGS:
            self._chunks.append(" ")
        if tag in ("script", "style"):
            self._skip = False
            self._in_ldjson = False

    def handle_data(self, data: str) -> None:
        if self._in_ldjson:
            self._chunks.append(f" {_ldjson_strings(data)} ")
        elif not self._skip:
            self._chunks.append(data)

    def text(self) -> str:
        return re.sub(r"\s+", " ", "".join(self._chunks)).strip()


def fetch_text(url: str, timeout: int) -> tuple[int | None, str]:
    """(status, text), or (None, "") if the fetch failed. Raises BlockedURL if
    the fetch policy refuses the URL, a redirect or a resolved address."""
    request = urllib.request.Request(
        canonicalize_for_fetch(url), headers={"User-Agent": "Mozilla/5.0 (signal-scout verifier)"}
    )
    try:
        with open_url(request, timeout, POLICY) as response:
            status = response.status
            charset = response.headers.get_content_charset() or "utf-8"
            raw = response.read(2_000_000).decode(charset, errors="ignore")
    except BlockedURL:
        raise
    except urllib.error.HTTPError as exc:
        return exc.code, ""
    except Exception as exc:
        if isinstance(getattr(exc, "reason", None), BlockedURL):
            raise exc.reason from exc
        print(f"fetch_text: {url} — {exc}", file=sys.stderr)
        return None, ""
    parser = _TextExtractor()
    parser.feed(raw)
    return status, parser.text()


WAYBACK_API = "https://archive.org/wayback/available?url="


def _is_archive_url(snapshot_url: str) -> bool:
    """A snapshot must live on archive.org or the API's own host, so a spoofed
    availability answer cannot point the fetcher anywhere else."""
    host = (urlparse(snapshot_url).hostname or "").lower()
    return host == urlparse(WAYBACK_API).hostname or host == "archive.org" or host.endswith(".archive.org")


def fetch_wayback(url: str, timeout: int) -> tuple[str, str, str]:
    """Try the Wayback Machine for a page we couldn't read live.

    Returns (snapshot_url, snapshot_date, page_text) or ("", "", "") if no
    usable archived copy exists. A claim verified against an archived copy is
    still a claim verified against the page as it was published — strictly
    better than giving up as Broken/Unverified, and honestly disclosed in the
    verification note."""
    try:
        request = urllib.request.Request(
            WAYBACK_API + urllib.parse.quote(url, safe=""),
            headers={"User-Agent": "Mozilla/5.0 (signal-scout verifier)"},
        )
        with open_url(request, timeout, POLICY) as response:
            info = json.load(response)
        closest = (info.get("archived_snapshots") or {}).get("closest") or {}
        snapshot_url = closest.get("url") if closest.get("available") else ""
        snapshot_date = str(closest.get("timestamp", ""))[:8]
    except Exception as exc:
        print(f"fetch_wayback: {url} — {exc}", file=sys.stderr)
        return "", "", ""
    if not snapshot_url or not _is_archive_url(snapshot_url):
        return "", "", ""
    try:
        status, text = fetch_text(snapshot_url, timeout)
    except BlockedURL as exc:
        print(f"fetch_wayback: {url} — {exc}", file=sys.stderr)
        return "", "", ""
    if status is not None and status < 400 and text:
        return snapshot_url, snapshot_date, text
    return "", "", ""


ARCHIVE_PH_NEWEST = "https://archive.ph/newest/"


def fetch_archive_ph(url: str, timeout: int) -> tuple[str, str]:
    """Try archive.ph for a page Wayback has no snapshot of.

    Second-tier fallback, tried only after fetch_wayback comes up empty:
    archive.ph has no official lookup API (unlike Wayback's `available`
    endpoint) and is heavily rate-limited (confirmed manually: a single
    unthrottled request returned HTTP 429), so this is best-effort — a miss
    here falls through to the existing Broken/SnippetOnly handling exactly as
    if Wayback alone had been tried. `/newest/<url>` redirects straight to
    the latest snapshot when one exists, or serves a non-2xx/challenge page
    when it doesn't; fetch_text follows the redirect and returns whatever
    text comes back, so a snapshot's actual URL is never recovered here --
    only the fact that one had usable text is (nothing downstream needs the
    snapshot URL itself, unlike Wayback's timestamped citation)."""
    try:
        status, text = fetch_text(ARCHIVE_PH_NEWEST + url, timeout)
    except Exception as exc:
        print(f"fetch_archive_ph: {url} — {exc}", file=sys.stderr)
        return "", ""
    if status is not None and status < 400 and len(text.strip()) >= 200:
        return ARCHIVE_PH_NEWEST + url, text
    return "", ""


def check_source(url: str, evidence: str, timeout: int) -> tuple[str, str, float, float]:
    """Fetch a source (live first, Wayback then archive.ph fallback) and tier its evidence.

    The archive fallbacks fire when the live page is unreachable, bot-walled
    (Reddit 403, any 429), or yields too little text to check (JS-rendered) —
    each a fetch problem, not a fabrication signal, and each recoverable when
    an archived copy of the page exists. Wayback is tried first (it has a
    real lookup API); archive.ph is tried only if Wayback has no snapshot,
    since it's best-effort and more likely to be rate-limited.

    A URL the fetch policy refuses is Broken with no archive lookup: that
    would hand an internal address to a third party."""
    try:
        status, page_text = fetch_text(url, timeout)
    except BlockedURL as exc:
        return TIER_BROKEN, f"Refused to fetch: {exc}", 0.0, 0.0

    live_failed = status is None or status >= 400
    too_thin = not live_failed and len(page_text.strip()) < 200
    if live_failed or too_thin:
        snapshot_url, snapshot_date, archive_text = fetch_wayback(url, timeout)
        if archive_text:
            tier, note, quoted, topical = tier_for_evidence(evidence, archive_text)
            suffix = f" — checked against Wayback archive ({snapshot_date or 'undated'}), live page {'unreachable' if live_failed else 'yielded no text'}"
            return tier, (note + suffix).strip(" —") if not note else note + suffix, quoted, topical
        _, archive_ph_text = fetch_archive_ph(url, timeout)
        if archive_ph_text:
            tier, note, quoted, topical = tier_for_evidence(evidence, archive_ph_text)
            suffix = f" — checked against archive.ph copy, live page {'unreachable' if live_failed else 'yielded no text'}"
            return tier, (note + suffix).strip(" —") if not note else note + suffix, quoted, topical

    if status == 429:
        # 429 always means "you're being throttled," on any domain — it is never
        # evidence the link is dead. Conflating it with TIER_BROKEN would fail a
        # real, live source over a rate limit (this happened during dogfooding:
        # heavy HN fetching in one run rate-limited a later run's IP).
        return (TIER_SNIPPET_ONLY,
                "Source rate-limited the fetch (HTTP 429) and no archived copy found; evidence is snippet-sourced only",
                0.0, 0.0)
    domain = bot_walled_host(url)
    if (status in (403, 429) or is_challenge_page(status, page_text)) and domain:
        # These platforms block automated fetches (403/429) even for real, live
        # pages — a platform anti-bot wall, not evidence the link is dead. Don't
        # fail the run over it; the agent should trust the discovery-search
        # snippet that surfaced this URL and note the gap in `limits` instead.
        return (TIER_SNIPPET_ONLY,
                f"{domain} blocks automated fetch and no archived copy found; evidence is snippet-sourced only",
                0.0, 0.0)
    if live_failed:
        return TIER_BROKEN, f"Source unreachable (status {status}) and no archived copy found", 0.0, 0.0
    return tier_for_evidence(evidence, page_text)


def iter_prospects(data: dict[str, Any]):
    for kind in ("individuals", "segments", "companies"):
        for index, item in enumerate(data.get(kind) or []):
            if isinstance(item, dict):
                yield kind, index, item


def battlecard_entries(data: dict[str, Any]) -> list[dict[str, Any]]:
    ctx = data.get("competitive_context")
    if not isinstance(ctx, dict):
        return []
    return [e for e in (ctx.get("battlecard") or []) if isinstance(e, dict)]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--timeout", type=int, default=10)
    parser.add_argument(
        "--allow-private-addresses",
        action="store_true",
        help="Let source_url reach loopback and private addresses. For checking a local copy "
        "of a page; never on input you did not write.",
    )
    parser.add_argument(
        "--use-proxy",
        action="store_true",
        help="Fetch through HTTP(S)_PROXY, for a machine with no direct route out. The proxy "
        "makes the connection, so addresses are checked before the request and DNS rebinding "
        "is not prevented.",
    )
    parser.add_argument(
        "--annotate-out",
        type=Path,
        help="Write the input JSON back out with a verification_tier/verification_note "
        "added to every prospect (including broken ones), for generate_report.py to "
        "render as a badge. Does not drop anything — this is for visibility, not filtering.",
    )
    parser.add_argument(
        "--handoff-out",
        type=Path,
        help="Write a filtered copy of the input JSON — same schema, broken-source and "
        "not-on-page prospects dropped — ready to hand to signal-outreach (or any other "
        "consumer) without carrying dead links or unsupported claims forward.",
    )
    args = parser.parse_args()
    global POLICY
    if args.allow_private_addresses:
        POLICY = dataclasses.replace(POLICY, allow_private=True)
    if args.use_proxy:
        POLICY = dataclasses.replace(POLICY, use_env_proxy=True)

    data = json.loads(args.input.read_text(encoding="utf-8"))
    results: list[tuple[str, str, str, str, float, float]] = []
    counts: dict[str, int] = {}

    def record(kind: str, name: str, url: str, tier: str, note: str, quoted: float, topical: float, item: dict[str, Any]) -> None:
        item["verification_tier"] = tier
        item["verification_note"] = note
        item["verified_at"] = date.today().isoformat()
        counts[tier] = counts.get(tier, 0) + 1
        results.append((kind, name, url, tier, quoted, topical))

    ungrounded_openers = 0
    for kind, _index, item in iter_prospects(data):
        name = str(item.get("name", "(unnamed)"))
        url = str(item.get("source_url", "")).strip()
        if kind == "individuals":
            note = opener_grounding_note(str(item.get("opener", "")), str(item.get("evidence", "")))
            if note:
                item["opener_grounding_note"] = note
                ungrounded_openers += 1
        if not url.startswith(("http://", "https://")):
            record(kind, name, url, TIER_BROKEN, "Invalid source_url", 0.0, 0.0, item)
            continue
        tier, note, quoted, topical = check_source(url, str(item.get("evidence", "")), args.timeout)
        record(kind, name, url, tier, note, quoted, topical, item)

    # Battlecard entries are factual claims about competitors and go through the
    # same verification — but they fail individually (dropped from the report and
    # handoff), never the run: a bad competitor claim shouldn't block a shipped
    # shortlist of good prospects the way a fabricated prospect must.
    battlecard = battlecard_entries(data)
    battlecard_disqualified = 0
    if battlecard:
        mentions = [
            str(item.get("competitor_mentioned", "")).strip().lower()
            for _, _, item in iter_prospects(data)
            if str(item.get("competitor_mentioned", "")).strip()
        ]
        for entry in battlecard:
            name = str(entry.get("competitor", "(unnamed competitor)"))
            url = str(entry.get("source_url", "")).strip()
            if not url.startswith(("http://", "https://")):
                tier, note, quoted, topical = TIER_BROKEN, "Invalid source_url", 0.0, 0.0
            else:
                tier, note, quoted, topical = check_source(url, str(entry.get("evidence", "")), args.timeout)
            entry["verification_tier"] = tier
            entry["verification_note"] = note
            entry["verified_at"] = date.today().isoformat()
            if tier in TIER_DISQUALIFYING:
                battlecard_disqualified += 1
            results.append(("battlecard", name, url, tier, quoted, topical))
            # Cross-examination: does any prospect in this run independently
            # mention this competitor? Zero corroboration doesn't fail the entry,
            # but it must be visible — a single-source competitor claim shipped
            # as consensus is exactly the kind of thing a client will repeat.
            comp = name.strip().lower()
            entry["corroboration_count"] = sum(1 for m in mentions if comp and (comp in m or m in comp))
            if entry["corroboration_count"] == 0:
                entry["corroboration_note"] = (
                    "No prospect in this run independently mentions this competitor — single-source claim"
                )

    print(f"{'TYPE':<11} {'NAME':<26} {'TIER':<14} {'QUOTED':>6} {'TOPICAL':>7}  URL")
    for kind, name, url, tier, quoted, topical in results:
        label = TIER_LABELS.get(tier, tier)
        print(f"{kind:<11} {name[:26]:<26} {label:<14} {quoted:>6.2f} {topical:>7.2f}  {url}")

    total = len(results)
    summary = ", ".join(f"{n} {TIER_LABELS.get(t, t).lower()}" for t, n in sorted(counts.items())) or "none"
    print(f"\n{total} sources checked — prospects: {summary}.")
    if battlecard:
        single_source = sum(1 for e in battlecard if e.get("corroboration_count", 0) == 0)
        print(f"Battlecard: {len(battlecard)} entr(ies) checked, {battlecard_disqualified} disqualified "
              f"(dropped from report/handoff, run not failed), {single_source} single-source (no corroborating prospect).")

    unsupported = counts.get(TIER_UNSUPPORTED, 0)
    broken = counts.get(TIER_BROKEN, 0)
    if unsupported:
        print(
            f"\n{unsupported} claim(s) are NOT ON THE PAGE they cite. The source loaded and was "
            "readable, and the evidence isn't in it — treat as fabricated until proven otherwise. "
            "Drop the prospect or replace the evidence with text that is actually on the page."
        )
    if broken:
        print(f"\n{broken} source(s) are unreachable or invalid. Drop the prospect or find a working source.")
        if not POLICY.use_env_proxy and env_proxy_set():
            print(PROXY_HINT)
    if counts.get(TIER_SNIPPET_ONLY):
        print("\nSnippet-only entries: keep only if the evidence came from a real discovery-search "
              "snippet, and disclose the unverified status in `limits`.")
    if ungrounded_openers:
        print(
            f"\n{ungrounded_openers} opener(s) reference specifics not found in their own checked "
            "evidence — tighten them to what the evidence actually supports before sending."
        )

    if args.annotate_out:
        args.annotate_out.parent.mkdir(parents=True, exist_ok=True)
        args.annotate_out.write_text(json.dumps(data, indent=2), encoding="utf-8")
        print(f"\nAnnotated JSON written: {args.annotate_out.resolve()}")

    if args.handoff_out:
        handoff = json.loads(json.dumps(data))
        dropped = 0
        ctx = handoff.get("competitive_context")
        if isinstance(ctx, dict) and ctx.get("battlecard"):
            kept_entries = [
                e for e in ctx["battlecard"]
                if not (isinstance(e, dict) and e.get("verification_tier") in TIER_DISQUALIFYING)
            ]
            dropped += len(ctx["battlecard"]) - len(kept_entries)
            if kept_entries:
                ctx["battlecard"] = kept_entries
            else:
                ctx.pop("battlecard", None)
        for kind in ("individuals", "segments", "companies"):
            kept = [
                item for item in (handoff.get(kind) or [])
                if isinstance(item, dict) and item.get("verification_tier") not in TIER_DISQUALIFYING
            ]
            dropped += len(handoff.get(kind) or []) - len(kept)
            if kept:
                handoff[kind] = kept
            else:
                handoff.pop(kind, None)
        args.handoff_out.parent.mkdir(parents=True, exist_ok=True)
        args.handoff_out.write_text(json.dumps(handoff, indent=2), encoding="utf-8")
        print(f"Handoff JSON written: {args.handoff_out.resolve()} "
              f"({dropped} broken-source / not-on-page prospect(s) dropped)")

    if broken or unsupported:
        sys.exit(1)


if __name__ == "__main__":
    main()
