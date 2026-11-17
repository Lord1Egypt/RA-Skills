#!/usr/bin/env python3
"""
Wikipedia MCP Server
Provides: search, summary, random, did_you_know, dino_fact
Uses Wikipedia REST API — free, no API key required.

Hand-rolled JSON-RPC stdio MCP for maximum portability (no SDK dependency).
"""

import difflib
import json
import random
import re
import sys
from collections import Counter
from datetime import datetime, timedelta, timezone
from html import unescape
from typing import Optional
from urllib.parse import quote as _url_quote, unquote as _url_unquote

import requests

API_VERSION = "2025-06-18"
SERVER_NAME = "wikipedia-mcp"
SERVER_VERSION = "1.1.37"

# Wikipedia requires a descriptive User-Agent with contact info.
USER_AGENT = (
    f"{SERVER_NAME}/{SERVER_VERSION} "
    "(https://github.com/evanfoglia/wikipedia-mcp; evan@example.com)"
)
DEFAULT_TIMEOUT = 10
SUPPORTED_LANGS = ("en", "de", "es", "fr", "ja", "zh", "pt", "it", "ru", "nl")


def _base(lang: str = "en") -> str:
    lang = lang if lang in SUPPORTED_LANGS else "en"
    return f"https://{lang}.wikipedia.org/api/rest_v1"


def _wiki(lang: str = "en") -> str:
    lang = lang if lang in SUPPORTED_LANGS else "en"
    return f"https://{lang}.wikipedia.org/w/api.php"


# Simple English Wikipedia — same read-only REST API, plain-language articles.
_SIMPLE_BASE = "https://simple.wikipedia.org/api/rest_v1"


def _get(url: str, params: Optional[dict] = None) -> requests.Response:
    return requests.get(
        url, params=params, headers={"User-Agent": USER_AGENT}, timeout=DEFAULT_TIMEOUT
    )


# ---------------------------------------------------------------------------
# Curated dinosaur list — Wikipedia's category pages change shape frequently,
# so we maintain a small high-quality list and let the API expand it.
# ---------------------------------------------------------------------------
DINOS = [
    "Tyrannosaurus", "Triceratops", "Velociraptor", "Spinosaurus",
    "Stegosaurus", "Ankylosaurus", "Brachiosaurus", "Parasaurolophus",
    "Pteranodon", "Mosasaurus", "Allosaurus", "Diplodocus",
    "Carnotaurus", "Giganotosaurus", "Carcharodontosaurus",
    "Acrocanthosaurus", "Argentinosaurus", "Therizinosaurus",
    "Utahraptor", "Oviraptor", "Troodon", "Deinonychus",
    "Dimorphodon", "Quetzalcoatlus", "Plateosaurus", "Coelophysis",
    "Mamenchisaurus", "Styracosaurus", "Protoceratops", "Pentaceratops",
    "Metriacanthosaurus", "Iguanodon", "Maiasaura", "Pachycephalosaurus",
]


# ---------------------------------------------------------------------------
# Curated list of famous quotes — short, well-attributed, time-tested.
# Each entry: (author, quote). The list is curated manually so attribution
# is reliable and quote quality is high (verified famous lines, not
# paraphrases). random.choice picks one per call. Adding entries is a
# trivial code change — same pattern as the DINOS list above.
# ---------------------------------------------------------------------------
FAMOUS_QUOTES = [
    ("Winston Churchill", "Success is not final, failure is not fatal: it is the courage to continue that counts."),
    ("Albert Einstein", "Imagination is more important than knowledge. Knowledge is limited. Imagination encircles the world."),
    ("Mark Twain", "The two most important days in your life are the day you are born and the day you find out why."),
    ("Mahatma Gandhi", "Be the change that you wish to see in the world."),
    ("Martin Luther King Jr.", "The arc of the moral universe is long, but it bends toward justice."),
    ("Abraham Lincoln", "Whatever you are, be a good one."),
    ("Nelson Mandela", "Education is the most powerful weapon which you can use to change the world."),
    ("Oscar Wilde", "Be yourself; everyone else is already taken."),
    ("Confucius", "It does not matter how slowly you go as long as you do not stop."),
    ("Voltaire", "I disapprove of what you say, but I will defend to the death your right to say it."),
    ("Maya Angelou", "I've learned that people will forget what you said, people will forget what you did, but people will never forget how you made them feel."),
    ("Steve Jobs", "Your time is limited, so don't waste it living someone else's life."),
    ("Mother Teresa", "If you judge people, you have no time to love them."),
    ("Dalai Lama", "Happiness is not something ready-made. It comes from your own actions."),
    ("C.S. Lewis", "You can't go back and change the beginning, but you can start where you are and change the ending."),
    ("Bob Marley", "Love the life you live. Live the life you love."),
    ("John Lennon", "Life is what happens when you're busy making other plans."),
    ("Laozi", "A journey of a thousand miles begins with a single step."),
    ("Friedrich Nietzsche", "He who has a why to live can bear almost any how."),
    ("Socrates", "The unexamined life is not worth living."),
    ("Plato", "The beginning is the most important part of the work."),
    ("Aristotle", "We are what we repeatedly do. Excellence, then, is not an act, but a habit."),
    ("Jane Austen", "It is a truth universally acknowledged, that a single man in possession of a good fortune, must be in want of a wife."),
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
_TAG_RE = re.compile(r"<[^>]+>")


def _strip_html(s: str) -> str:
    return _TAG_RE.sub("", s)


_STYLE_SCRIPT_RE = re.compile(r"<(style|script)[^>]*>.*?</\1\s*>", re.S | re.I)
_REF_SUP_RE = re.compile(r'<sup[^>]*\bclass="reference"[^>]*>.*?</sup\s*>', re.S | re.I)
_BLOCK_CLOSE_RE = re.compile(
    r"</(p|h[1-6]|li|dt|dd|tr|div|blockquote|figure|figcaption|table)[^>]*>"
    r"|<\s*(br|hr)[^>]*>",
    re.I,
)


def _html_to_text(html: str) -> str:
    """Convert rendered MediaWiki HTML to readable plain text (stdlib only).

    Drops <style>/<script> blocks (the parse API injects large inline CSS),
    citation-marker superscripts, and edit-section links; preserves
    paragraph/list structure as newlines; unescapes entities and collapses
    whitespace.
    """
    text = _STYLE_SCRIPT_RE.sub(" ", html)
    text = _REF_SUP_RE.sub(" ", text)
    # Preserve paragraph structure before stripping the remaining tags.
    text = _BLOCK_CLOSE_RE.sub("\n", text)
    text = _TAG_RE.sub("", text)
    text = unescape(text)
    lines = [re.sub(r"[ \t\xa0]+", " ", ln).strip() for ln in text.split("\n")]
    out_lines = []
    for ln in lines:
        if ln:
            out_lines.append(ln)
        elif out_lines and out_lines[-1] != "":
            out_lines.append("")
    return "\n".join(out_lines).strip("\n")


def _slug(title: str) -> str:
    return title.strip().replace(" ", "_")


# ---------------------------------------------------------------------------
# Infobox helpers — parse raw wikitext templates without new dependencies.
# ---------------------------------------------------------------------------
_INFOBOX_RE = re.compile(r"\{\{\s*[Ii]nfobox")


def _extract_template(wt: str, start: int):
    """Extract a template starting at wt[start:start+2] == '{{'.

    Returns (name, body, end_index) with balanced-brace matching; name is
    the text before the first top-level '|' (or the whole body if none).
    """
    depth = 0
    i, n = start, len(wt)
    while i < n - 1:
        if wt[i:i + 2] == "{{":
            depth += 1
            i += 2
        elif wt[i:i + 2] == "}}":
            depth -= 1
            i += 2
            if depth == 0:
                inner = wt[start + 2:i - 2]
                m = re.match(r"\s*([^|}]+)", inner)
                name = m.group(1).strip() if m else ""
                body = inner[len(m.group(0)):] if m else inner
                return name, body, i
        else:
            i += 1
    return None, None, n


def _split_top_level(s: str):
    """Split s on '|' characters not nested inside {{...}} or [[...]]."""
    parts, tdepth, bdepth, cur = [], 0, 0, ""
    i, n = 0, len(s)
    while i < n:
        if s[i:i + 2] == "{{":
            tdepth += 1
            cur += "{{"
            i += 2
        elif s[i:i + 2] == "}}":
            tdepth -= 1
            cur += "}}"
            i += 2
        elif s[i] == "[":
            bdepth += 1
            cur += "["
            i += 1
        elif s[i] == "]":
            bdepth -= 1
            cur += "]"
            i += 1
        elif s[i] == "|" and tdepth == 0 and bdepth == 0:
            parts.append(cur)
            cur = ""
            i += 1
        else:
            cur += s[i]
            i += 1
    parts.append(cur)
    return parts


# Date templates take (year, month, day) positionally — join with "-" so
# birth/death fields read as dates instead of comma-separated numbers.
_DATE_TEMPLATES = frozenset({
    "birth date", "birth date and age", "death date", "death date and age",
})


def _clean_infobox_value(v: str) -> str:
    """Render a raw wikitext infobox value as readable plain text."""
    v = re.sub(r"<ref[^>]*>.*?</ref>", "", v, flags=re.DOTALL)  # citations
    v = re.sub(r"<ref[^>]*/>", "", v)
    v = v.replace("<br>", ", ").replace("<br/>", ", ").replace("<br />", ", ")
    v = re.sub(r"<[^>]+>", "", v)
    v = unescape(v)

    def _tmpl(m):
        # Drop named params (df=yes, end=divorced, P548=Q2804309) and
        # pure wikidata tokens (P123); join positional params with ", ".
        params = _split_top_level(m.group(0)[2:-2])
        name = (params[0].strip().lower() if params else "")
        if name == "wikidata":
            return ""  # value is fetched from Wikidata at render time,
                       # not present in the wikitext — drop, don't show noise
        kept = [
            p.strip()
            for p in params[1:]
            if p.strip() and "=" not in p and not re.fullmatch(r"[PQ]\d+", p.strip())
        ]
        if name in _DATE_TEMPLATES and len(kept) >= 3:
            return "-".join(kept[:3])  # 1879-3-14, not "1879, 3, 14"
        return ", ".join(kept)

    prev = None
    while prev != v:  # innermost templates first, until none remain
        prev = v
        v = re.sub(r"\{\{[^{}]*\}\}", _tmpl, v)
    v = re.sub(r"\[\[([^|\]]+)\|([^\]]+)\]\]", r"\2", v)  # [[Page|text]] -> text
    v = re.sub(r"\[\[([^\]]+)\]\]", r"\1", v)  # [[Page]] -> Page
    v = v.replace("'''", "").replace("''", "")
    v = re.sub(r"(^|\s)\*\s*", r"\1• ", v)  # wikitext bullets -> bullet chars
    v = re.sub(r"\s+", " ", v).strip(" ,;•")
    return v


def _find_infoboxes(wt: str):
    """Return [(name, body)] for every {{Infobox ...}} template in wikitext."""
    boxes = []
    for m in _INFOBOX_RE.finditer(wt):
        name, body, _ = _extract_template(wt, m.start())
        if name and name.lower().startswith("infobox"):
            boxes.append((name, body))
    return boxes


def _summary_block(data: dict, fallback_title: str) -> str:
    """Render a Wikipedia summary response as Markdown text."""
    title = data.get("title", fallback_title)
    extract = data.get("extract", "No summary available.")
    desc = data.get("description", "")
    thumb = data.get("thumbnail", {}).get("source", "") if data.get("thumbnail") else ""
    desktop_url = (
        data.get("content_urls", {}).get("desktop", {}).get("page", "#")
    )

    out = f"## {title}\n\n{extract}\n\n"
    if desc:
        out += f"*({desc})*\n\n"
    out += f"[Read more →]({desktop_url})"
    if thumb:
        out += f"\n\n![{title}]({thumb})"
    return out


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------
def search_wikipedia(query: str, limit: int = 5, lang: str = "en") -> str:
    """Search Wikipedia for articles matching a query.

    Entry point when the exact article title is unknown. Returns a ranked,
    numbered list of matching titles with text snippets and URLs; feed the
    chosen title to summary/article_extract/links next.
    """
    try:
        limit = max(1, min(int(limit), 20))
    except (TypeError, ValueError):
        limit = 5  # fall back to default on garbage input
    params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "srlimit": limit,
        "format": "json",
        "origin": "*",
    }
    resp = _get(_wiki(lang), params=params)
    resp.raise_for_status()
    data = resp.json()
    results = data.get("query", {}).get("search", [])
    if not results:
        return f"No results found for '{query}'."

    out = f"**Search results for '{query}':**\n\n"
    for i, page in enumerate(results, 1):
        title = page.get("title", "Unknown")
        snippet = _strip_html(page.get("snippet", ""))
        out += f"{i}. **{title}**\n"
        if snippet:
            out += f"   {snippet[:200]}...\n"
        out += (
            f"   https://{lang}.wikipedia.org/wiki/{_slug(title)}\n\n"
        )
    return out


def get_summary(title: str, lang: str = "en") -> str:
    """Get a concise summary + thumbnail of a Wikipedia article by exact title.

    Fastest way to get the gist of a known topic. Use search first if the
    exact title is unknown; article_extract for full text.
    """
    resp = _get(f"{_base(lang)}/page/summary/{_slug(title)}")
    if resp.status_code == 404:
        return f"Article '{title}' not found on Wikipedia."
    resp.raise_for_status()
    return _summary_block(resp.json(), fallback_title=title)


def get_random(lang: str = "en") -> str:
    """Get a summary of a random Wikipedia article (serendipitous discovery)."""
    resp = _get(f"{_base(lang)}/page/random/summary")
    resp.raise_for_status()
    return _summary_block(resp.json(), fallback_title="Random Article")


def get_simple_summary(title: str) -> str:
    """Get the Simple English Wikipedia version of a topic — plain-language explanation.

    Same markdown shape as `summary` (title + extract + thumbnail + read-more link),
    but the prose is written for easy reading: short sentences, common words. Best
    when the caller wants "explain it simply" (kids, ESL readers, quick intuition)
    or the full article is too dense. Not every topic has a Simple English article —
    in that case the reply says so and points at `summary` for the full version.
    """
    resp = _get(f"{_SIMPLE_BASE}/page/summary/{_slug(title)}")
    if resp.status_code == 404:
        return (
            f"No Simple English article found for '{title}'. Not every topic has a "
            f"simplified version — use `summary` for the full English article."
        )
    resp.raise_for_status()
    return _summary_block(resp.json(), fallback_title=title)


def did_you_know(lang: str = "en") -> str:
    """Get a random 'Did You Know' style fact from Wikipedia."""
    resp = _get(f"{_base(lang)}/page/random/summary")
    resp.raise_for_status()
    data = resp.json()
    fact = data.get("extract", "")
    title = data.get("title", "")
    if not fact:
        return f"Did you know? {title} is a fascinating topic on Wikipedia!"
    desktop_url = (
        data.get("content_urls", {}).get("desktop", {}).get("page", "#")
    )
    return (
        f"**Did you know?**\n\n{fact}\n\n"
        f"*Source: [Wikipedia — {title}]({desktop_url})*"
    )


def dino_fact(species: str = "", lang: str = "en") -> str:
    """
    Get a 'Did You Know' style fact about dinosaurs or prehistoric life.
    If species is provided, returns a fact about that specific dinosaur.
    Otherwise picks a random dinosaur from the curated list.
    """
    if not species:
        species = random.choice(DINOS)

    resp = _get(f"{_base(lang)}/page/summary/{_slug(species)}")
    if resp.status_code == 404:
        # Species not found — pick a random one rather than dumping a search.
        # The curated list gives reliable coverage.
        fallback = random.choice([d for d in DINOS if d.lower() != species.lower()])
        return (
            f"Couldn't find '{species}' on Wikipedia. "
            f"Here's a random dino instead:\n\n"
            f"{dino_fact(fallback, lang=lang)}"
        )
    resp.raise_for_status()
    data = resp.json()
    fact = data.get("extract", "")
    title = data.get("title", species)
    if not fact:
        return f"Not enough data on {title} yet. Try a different species!"
    desktop_url = (
        data.get("content_urls", {}).get("desktop", {}).get("page", "#")
    )
    return (
        f"**Did you know about {title}?**\n\n{fact}\n\n"
        f"*Source: [Wikipedia — {title}]({desktop_url})*"
    )


def article_extract(title: str, lang: str = "en") -> str:
    """Get a Wikipedia article's full plain-text extract by title (vs `summary`).

    Uses the MediaWiki Action API `prop=extracts` with `explaintext=1` to return
    the full article body as plain text — typically several paragraphs, much
    longer than `summary`'s short extract. Complements `summary`: use `summary`
    for the lead + thumbnail, `article_extract` when you want to read more
    without parsing HTML.
    """
    params = {
        "action": "query",
        "prop": "extracts",
        "explaintext": 1,
        "exsectionformat": "plain",
        "titles": title,
        "format": "json",
        "origin": "*",
    }
    resp = _get(_wiki(lang), params=params)
    if resp.status_code == 404:
        return f"Article '{title}' not found on Wikipedia."
    resp.raise_for_status()
    data = resp.json()
    pages = data.get("query", {}).get("pages", {})
    page = next(iter(pages.values()), {}) if pages else {}
    # MediaWiki Action API returns 200 OK with a "missing" marker for
    # non-existent pages rather than a 404 HTTP status. Detect that
    # explicitly so users see the same "not found" message as `summary`.
    if not page or "missing" in page:
        return f"Article '{title}' not found on Wikipedia."
    extract = (page.get("extract") or "").strip()
    title_out = (page.get("title") or title) if page else title
    if not extract:
        return f"No extract available for '{title_out}'."
    desktop_url = f"https://{lang}.wikipedia.org/wiki/{_slug(title_out)}"
    return f"## {title_out}\n\n{extract}\n\n[Read more →]({desktop_url})"


def article_sections(title: str, lang: str = "en") -> str:
    """Get the table of contents (section headings) for a Wikipedia article.

    Returns the structured section list from Wikipedia's parse API —
    section number, heading text, nesting level, and anchor. Useful for
    navigating long articles before committing to reading the whole body
    via `article_extract`. Major articles (e.g. "World War II",
    "Tyrannosaurus") can have 50KB+ of plain-text body; `article_sections`
    gives you the TOC in a few hundred bytes so you can pick what to read
    next. Sections are rendered as a numbered, indented markdown list —
    indentation maps to Wikipedia's heading hierarchy (h2 = no indent,
    h3 = 2 spaces, h4 = 4 spaces, etc.) so the structure is visible
    without a tree widget.

    Pairs naturally with `article_extract` (full body) and `summary`
    (lead + thumbnail): use `summary` for the headline, `article_sections`
    to browse the structure, `article_extract` when you want the full
    read.
    """
    params = {
        "action": "parse",
        "page": title,
        "prop": "sections",
        "format": "json",
        "origin": "*",
    }
    resp = _get(_wiki(lang), params=params)
    if resp.status_code == 404:
        return f"Article '{title}' not found on Wikipedia."
    resp.raise_for_status()
    data = resp.json()

    # MediaWiki parse API returns 200 OK with an `error` block for
    # non-existent pages (code "missingtitle") rather than a 404 HTTP
    # status. The error info wording varies ("The page you specified
    # doesn't exist.", "Bad title ...", "missingtitle"), so check for
    # the common "not found" indicators rather than relying on one
    # string match. Surface the same friendly message as
    # `summary` / `article_extract` / `categories` / `links`.
    if "error" in data:
        info = data.get("error", {}).get("info", "")
        code = data.get("error", {}).get("code", "")
        info_lc = info.lower()
        if (
            "missing" in info_lc
            or "doesn't exist" in info_lc
            or "does not exist" in info_lc
            or "bad title" in info_lc
            or code == "missingtitle"
        ):
            return f"Article '{title}' not found on Wikipedia."
        return f"Could not fetch sections for '{title}': {info}"

    parse = data.get("parse") or {}
    title_out = parse.get("title", title) or title
    sections = parse.get("sections") or []

    if not sections:
        # Articles with no section structure (rare — stubs, redirects)
        # shouldn't be reported as errors; just acknowledge cleanly.
        return (
            f"**Sections in \"{title_out}\":**\n\n"
            f"_(No sections found — article may be a stub or redirect.)_\n\n"
            f"[View article]"
            f"(https://{lang}.wikipedia.org/wiki/{_slug(title_out)})"
        )

    # toclevel is the visual hierarchy in Wikipedia's rendered TOC
    # (1 = top-level h2, 2 = h3, etc.). Indent by 2 spaces per level
    # minus 1 so top-level entries are flush-left.
    out = f"**Sections in \"{title_out}\":** ({len(sections)} total)\n\n"
    for sec in sections:
        line = (sec.get("line") or "").strip()
        if not line:
            continue
        toclevel = sec.get("toclevel", 1) or 1
        try:
            toclevel = max(1, min(int(toclevel), 4))
        except (TypeError, ValueError):
            toclevel = 1
        indent = "  " * (toclevel - 1)
        number = sec.get("number", "")
        if number:
            out += f"{indent}{number}. {line}\n"
        else:
            out += f"{indent}- {line}\n"

    out += (
        f"\n[View article]"
        f"(https://{lang}.wikipedia.org/wiki/{_slug(title_out)})"
    )
    return out


def _fetch_sections(title: str, lang: str):
    """Fetch the parse-API section list for a title.

    Returns (page_title, sections). Raises ValueError with a user-facing
    message when the article is missing or the fetch fails.
    """
    params = {
        "action": "parse",
        "page": title,
        "prop": "sections",
        "redirects": 1,
        "format": "json",
        "formatversion": "2",
        "origin": "*",
    }
    resp = _get(_wiki(lang), params=params)
    if resp.status_code == 404:
        raise ValueError(f"Article '{title}' not found on Wikipedia.")
    resp.raise_for_status()
    data = resp.json()
    if "error" in data:
        info = data.get("error", {}).get("info", "")
        code = data.get("error", {}).get("code", "")
        info_lc = info.lower()
        if (
            "missing" in info_lc
            or "doesn't exist" in info_lc
            or "does not exist" in info_lc
            or "bad title" in info_lc
            or code == "missingtitle"
        ):
            raise ValueError(f"Article '{title}' not found on Wikipedia.")
        raise ValueError(f"Could not fetch sections for '{title}': {info}")
    parse = data.get("parse") or {}
    return (parse.get("title", title) or title, parse.get("sections") or [])


def _resolve_section(sections, section):
    """Resolve a section specifier to (flat_index, heading, anchor).

    Accepts a section number exactly as shown by `article_sections`
    (e.g. 2 or "2.1"), a heading name (case-insensitive), or 0 for the
    lead/intro. Raises ValueError with a helpful message — including
    close-match suggestions for misspelled names.
    """
    total = len(sections)
    if isinstance(section, bool):
        raise ValueError(
            "Invalid section: pass a section number as shown by "
            "`article_sections` (e.g. 2 or '2.1'), a heading name, or 0 "
            "for the lead/intro."
        )

    def entry(i):
        sec = sections[i]
        heading = _strip_html(unescape(sec.get("line") or "")).strip()
        heading = re.sub(r"\s+", " ", heading)
        return (i + 1, heading or "Section %d" % (i + 1), sec.get("anchor") or "")

    def range_error(key):
        return ValueError(
            "Section %s out of range: this article has %d numbered "
            "section(s) (0 = lead/intro). Use `article_sections` to browse "
            "them." % (key, total)
        )

    # Normalize the specifier to a section-number string ("2", "2.1"),
    # a heading name, or the lead (0).
    number_key = None
    if isinstance(section, int):
        if section == 0:
            return (0, "Introduction", "")
        if section < 0:
            raise range_error(section)
        number_key = str(section)
    elif isinstance(section, str):
        stripped = section.strip()
        if re.fullmatch(r"-?\d+", stripped):
            n = int(stripped)
            if n == 0:
                return (0, "Introduction", "")
            if n < 0:
                raise range_error(stripped)
            number_key = str(n)
        else:
            number_key = stripped
    else:
        raise ValueError(
            "Invalid section %r: pass a section number as shown by "
            "`article_sections` (e.g. 2 or '2.1'), a heading name, or 0 "
            "for the lead/intro." % (section,)
        )

    # Match against the hierarchical numbers printed by `article_sections`
    # ("1", "1.1", "2", ...) — so 2 means the section displayed as "2.",
    # not the 2nd row of the flat list.
    for i, sec in enumerate(sections):
        if (sec.get("number") or "").strip() == number_key:
            return entry(i)
    if re.fullmatch(r"\d+(\.\d+)*", number_key):
        raise range_error(number_key)

    # Heading name, case-insensitive.
    want = re.sub(r"\s+", " ", number_key).casefold()
    indexed = [
        (j, re.sub(r"\s+", " ", entry(j)[1]).casefold())
        for j in range(total)
    ]
    for j, name in indexed:
        if name == want:
            return entry(j)
    close = difflib.get_close_matches(
        want, [n for _, n in indexed], n=3, cutoff=0.6
    )
    hint = ""
    if close:
        shown = [entry(j)[1] for j, n in indexed if n in close][:3]
        hint = " Did you mean: %s?" % ", ".join(shown)
    raise ValueError(
        "No section named '%s'.%s Use `article_sections` to list this "
        "article's sections." % (section, hint)
    )


def section_text(title: str, section, lang: str = "en") -> str:
    """Read one section of a Wikipedia article as plain text.

    The targeted-reading companion to `article_sections`: that tool lists
    the table of contents, this one reads the section you picked — without
    pulling the whole 50KB+ article body via `article_extract`. Pass a section number exactly as shown by `article_sections`
    (e.g. 2 or "2.1"; 0 reads the lead/intro before the first heading),
    "2.1", or a heading name (case-insensitive, e.g. "Life and career");
    misspelled names get close-match suggestions.

    Renders the section through the MediaWiki parse API (read-only GET)
    and converts it to plain text: inline CSS/JS, citation markers, and
    edit-section links are stripped while paragraph structure is kept.
    Follows redirects. The link at the bottom deep-links to the section
    on the article page. Pairs with `article_sections` (browse),
    `summary` (lead gist), and `article_extract` (full body).
    """
    try:
        page_title, sections = _fetch_sections(title, lang)
    except ValueError as e:
        return str(e)
    if not sections and section not in (0, "0"):
        return (
            f'**Sections in "{page_title}":**\n\n'
            f"_(No sections found — article may be a stub or redirect.)_\n\n"
            f"[View article](https://{lang}.wikipedia.org/wiki/{_slug(page_title)})"
        )
    try:
        idx, heading, anchor = _resolve_section(sections, section)
    except ValueError as e:
        return str(e)

    params = {
        "action": "parse",
        "page": page_title,
        "prop": "text",
        "section": idx,
        "redirects": 1,
        "disableeditsection": 1,
        "disablelimitreport": 1,
        "format": "json",
        "formatversion": "2",
        "origin": "*",
    }
    resp = _get(_wiki(lang), params=params)
    if resp.status_code == 404:
        return f"Article '{title}' not found on Wikipedia."
    resp.raise_for_status()
    data = resp.json()
    if "error" in data:
        return f"Article '{title}' not found on Wikipedia."
    html_text = (data.get("parse") or {}).get("text", "")
    text = _html_to_text(html_text)
    if not text:
        return (
            f'**"{page_title}" — {heading}**\n\n'
            f"_(This section has no readable text — it may only contain "
            f"templates or media.)_\n\n"
            f"[View section]"
            f"(https://{lang}.wikipedia.org/wiki/{_slug(page_title)}"
            f"{('#' + anchor) if anchor else ''})"
        )
    frag = f"#{anchor}" if anchor else ""
    return (
        f"**\"{page_title}\" — {heading}**\n\n"
        f"{text}\n\n"
        f"[View section](https://{lang}.wikipedia.org/wiki/{_slug(page_title)}{frag})"
    )


def featured_article(lang: str = "en") -> str:
    """Get today's Wikipedia Featured Article — editors' daily showcase pick."""
    resp = _get(f"{_base(lang)}/feed/featured/{_today()}")
    if resp.status_code == 404:
        return f"No featured article available for {lang}.wikipedia.org today."
    resp.raise_for_status()
    payload = resp.json()
    # Feed wraps the article under "tfa" (today's featured article)
    data = payload.get("tfa") or payload
    return _summary_block(data, fallback_title=data.get("title", "Featured Article"))


def picture_of_the_day(date: str = "", lang: str = "en") -> str:
    """Get Wikimedia Commons' Picture of the Day.

    The Wikimedia REST "featured" feed publishes one curated image per day
    from the Commons Picture of the Day selection — the same image shown
    on the Wikipedia Main Page. Each entry carries the file title, a
    thumbnail URL, the full-size image URL, the photographer/artist, the
    license, and a short description of what the image shows.

    `date` is an optional YYYYMMDD string (default: today UTC) so past
    pictures can be browsed — e.g. picture_of_the_day(date="20260901").
    This is the visual counterpart to the other daily content hooks:
    `featured_article` (long-form), `on_this_day` (history), `news`
    (current events), `did_you_know` (facts) — together they form a
    complete "today in Wikipedia" daily digest. The `image`/`media_list`
    tools cover article-specific media; this tool covers the editorially
    curated daily pick.

    Returns markdown: image preview (embedded thumbnail), file name,
    photographer, license, description, plus links to the full-size
    image and the Commons file page.
    """
    lang = lang if lang in SUPPORTED_LANGS else "en"

    if date == "":
        dt = datetime.now(timezone.utc)
    else:
        try:
            dt = datetime.strptime(date, "%Y%m%d")
        except ValueError:
            return f"Error: date must be in YYYYMMDD format (got '{date}')"

    resp = _get(f"{_base(lang)}/feed/featured/{dt.strftime('%Y/%m/%d')}")
    if resp.status_code == 404:
        return f"No picture of the day found for {dt.strftime('%Y-%m-%d')}."
    resp.raise_for_status()
    img = resp.json().get("image")
    if not img:
        return f"No picture of the day found for {dt.strftime('%Y-%m-%d')}."

    title = img.get("title", "Picture of the Day")
    desc = _strip_html((img.get("description") or {}).get("text", "") or "").strip()
    artist = _strip_html((img.get("artist") or {}).get("text", "") or "").strip()
    license_info = img.get("license") or {}
    license_label = (license_info.get("type") or license_info.get("code") or "").strip()
    thumb = ((img.get("thumbnail") or {}).get("source", "") or "").split("?")[0]
    full = ((img.get("image") or {}).get("source", "") or "").split("?")[0]
    file_page = img.get("file_page", "")

    out = f"🖼️ **Picture of the Day — {dt.strftime('%B %d, %Y')}**\n\n"
    if thumb:
        out += f"![{desc[:80] if desc else title}]({thumb})\n\n"
    out += f"**File:** {title}\n"
    if artist:
        out += f"**Photographer:** {artist}\n"
    if license_label:
        out += f"**License:** {license_label}\n"
    if desc:
        out += f"\n{desc}\n"
    links = []
    if full:
        links.append(f"[Full-size image]({full})")
    if file_page:
        links.append(f"[View on Wikimedia Commons]({file_page})")
    if links:
        out += "\n" + " · ".join(links)
    return out


def media_of_the_day(date: str = "") -> str:
    """Get Wikimedia Commons' Media of the Day.

    Commons curates one freely-licensed video or audio file per day
    ("Media of the Day") — the motion-and-sound counterpart to
    `picture_of_the_day`'s daily image. It's a different daily pick
    (often a short video or field recording), so together they cover
    the full daily media digest: `picture_of_the_day` (still image),
    `featured_article` (long-form), `on_this_day` (history), `news`
    (current events), `did_you_know` (facts).

    `date` is an optional YYYYMMDD string (default: today UTC) so past
    media can be browsed — e.g. media_of_the_day(date="20250615").
    Some dates have no Media of the Day; those return a clear message.

    Implementation: reads the day's `Template:Motd/YYYY-MM-DD` on
    Commons for the selected file, then fetches its metadata (direct
    URL, duration, mime type, thumbnail, artist, license, description)
    via the read-only Commons action API — no new dependencies, same
    descriptive User-Agent.

    Returns markdown: media kind + duration, embedded preview thumbnail
    (video files) or a listen link (audio), file name, artist, license,
    description, plus links to the direct file and the Commons file page.
    """
    if date == "":
        dt = datetime.now(timezone.utc)
    else:
        try:
            dt = datetime.strptime(date, "%Y%m%d")
        except ValueError:
            return f"Error: date must be in YYYYMMDD format (got '{date}')"

    date_dash = dt.strftime("%Y-%m-%d")
    # The day's pick lives in a date-stamped template on Commons.
    resp = _get(_COMMONS_API, params={
        "action": "query",
        "titles": f"Template:Motd/{date_dash}",
        "prop": "revisions",
        "rvprop": "content",
        "rvslots": "main",
        "format": "json",
        "formatversion": "2",
    })
    resp.raise_for_status()
    pages = (resp.json().get("query") or {}).get("pages", [])
    page = pages[0] if pages else {}
    if page.get("missing"):
        return f"No media of the day found for {date_dash}."
    revs = page.get("revisions") or []
    content = ""
    if revs:
        content = ((revs[0].get("slots") or {}).get("main") or {}).get("content", "")
    m = re.search(r"\{\{\s*Motd filename\s*\|\s*1\s*=\s*([^|}]+)", content)
    if not m:
        return f"No media of the day found for {date_dash}."
    filename = m.group(1).strip()
    # A few MOTD templates redundantly include the namespace prefix.
    if filename.lower().startswith("file:"):
        filename = filename[5:].strip()
    file_title = f"File:{filename}"

    resp = _get(_COMMONS_API, params={
        "action": "query",
        "titles": file_title,
        "prop": "imageinfo",
        "iiprop": "url|size|mime|extmetadata",
        "iiurlwidth": 640,
        "iiextmetadatafilter": "ImageDescription|Artist|LicenseShortName",
        "format": "json",
        "formatversion": "2",
    })
    resp.raise_for_status()
    pages = (resp.json().get("query") or {}).get("pages", [])
    info = ((pages[0].get("imageinfo") if pages else None) or [{}])[0]
    if not info or not info.get("url"):
        return (
            f"Could not load the media of the day for {date_dash} "
            f"({file_title})."
        )

    mime = info.get("mime", "")
    kind = _media_kind(mime, file_title)
    icon = {"video": "🎬", "audio": "🎵", "image": "🖼️"}.get(kind, "📎")
    width = info.get("width")
    height = info.get("height")
    dims = f"{width}×{height}" if width and height else ""
    duration = info.get("duration")
    dur_str = ""
    if duration:
        total = int(float(duration))
        hours, rem = divmod(total, 3600)
        mins, secs = divmod(rem, 60)
        dur_str = f"{hours}:{mins:02d}:{secs:02d}" if hours else f"{mins}:{secs:02d}"

    meta = info.get("extmetadata") or {}
    desc = _strip_html(
        (meta.get("ImageDescription") or {}).get("value", "") or ""
    ).strip()
    artist = _strip_html(
        (meta.get("Artist") or {}).get("value", "") or ""
    ).strip()
    license_name = (meta.get("LicenseShortName") or {}).get("value", "")
    # imageinfo URLs carry ?utm_source=... tracking params; strip them.
    thumb = (info.get("thumburl") or "").split("?")[0]
    full = (info.get("url") or "").split("?")[0]
    file_page = (
        "https://commons.wikimedia.org/wiki/" + file_title.replace(" ", "_")
    )

    out = f"{icon} **Media of the Day — {dt.strftime('%B %d, %Y')}**\n\n"
    if thumb:
        out += f"![{desc[:80] if desc else filename}]({thumb})\n\n"
    out += f"**File:** {file_title}\n"
    out += f"**Type:** {kind}"
    if dur_str:
        out += f" ({dur_str})"
    out += "\n"
    if dims:
        out += f"**Dimensions:** {dims}\n"
    if artist:
        out += f"**Artist:** {artist}\n"
    if license_name:
        out += f"**License:** {license_name}\n"
    if desc:
        out += f"\n{desc}\n"
    verb = {"video": "Watch", "audio": "Listen"}.get(kind, "View")
    links = []
    if full:
        links.append(f"[{verb}]({full})")
    links.append(f"[View on Wikimedia Commons]({file_page})")
    out += "\n" + " · ".join(links)
    return out


def on_this_day(lang: str = "en", count: int = 5) -> str:
    """Get historical events that happened on today's date from Wikipedia.

    Returns a random sample of events from Wikipedia's "On This Day" feed
    for the current UTC date. Pairs well with featured_article for daily
    content hooks — e.g. "today in history" newsletter intros.
    """
    try:
        count = max(1, min(int(count), 10))
    except (TypeError, ValueError):
        count = 5
    today_mm_dd = datetime.now(timezone.utc).strftime("%m/%d")
    resp = _get(f"{_base(lang)}/feed/onthisday/events/{today_mm_dd}")
    if resp.status_code == 404:
        return f"No 'on this day' events available for {lang}.wikipedia.org today."
    resp.raise_for_status()
    events = resp.json().get("events", [])
    if not events:
        return f"No historical events found for today on {lang}.wikipedia.org."

    sample = random.sample(events, min(count, len(events)))
    out = "**On this day:**\n\n"
    for ev in sample:
        year = ev.get("year", "?")
        text = _strip_html(ev.get("text", ""))
        out += f"- **{year}** — {text}\n"
        pages = ev.get("pages", [])
        if pages:
            page_title = pages[0].get("title", "")
            if page_title:
                out += (
                    f"  [Read on Wikipedia]"
                    f"(https://{lang}.wikipedia.org/wiki/{page_title})\n"
                )
    return out


def deaths_on_this_day(lang: str = "en", count: int = 5) -> str:
    """Get notable deaths that happened on today's date from Wikipedia.

    Returns a random sample of deaths from Wikipedia's "On This Day" feed
    for the current UTC date — the companion to `on_this_day`, which
    covers events. Wikipedia exposes these as separate endpoints, so this
    tool queries `/feed/onthisday/deaths/{MM/DD}` directly to get the
    deaths subset rather than scraping the events feed.

    Useful for "in memoriam" content hooks, obituary-style social posts,
    newsletter intros, and any place where the "who died today in
    history" framing adds weight. Pairs naturally with `on_this_day`
    (events) and `featured_article` (today's long-form pick) for a full
    "today in Wikipedia" daily digest.
    """
    try:
        count = max(1, min(int(count), 10))
    except (TypeError, ValueError):
        count = 5
    today_mm_dd = datetime.now(timezone.utc).strftime("%m/%d")
    resp = _get(f"{_base(lang)}/feed/onthisday/deaths/{today_mm_dd}")
    if resp.status_code == 404:
        return f"No 'deaths on this day' available for {lang}.wikipedia.org today."
    resp.raise_for_status()
    deaths = resp.json().get("deaths", [])
    if not deaths:
        return f"No notable deaths found for today on {lang}.wikipedia.org."

    sample = random.sample(deaths, min(count, len(deaths)))
    out = "**Deaths on this day:**\n\n"
    for entry in sample:
        year = entry.get("year", "?")
        text = _strip_html(entry.get("text", ""))
        out += f"- **{year}** — {text}\n"
        pages = entry.get("pages", [])
        if pages:
            page_title = pages[0].get("title", "")
            if page_title:
                out += (
                    f"  [Read on Wikipedia]"
                    f"(https://{lang}.wikipedia.org/wiki/{page_title})\n"
                )
    return out


def births_on_this_day(lang: str = "en", count: int = 5) -> str:
    """Get notable births that happened on today's date from Wikipedia.

    Returns a random sample of births from Wikipedia's "On This Day" feed
    for the current UTC date — the companion to `on_this_day` (events)
    and `deaths_on_this_day` (deaths). Wikipedia exposes these as separate
    endpoints, so this tool queries `/feed/onthisday/births/{MM/DD}`
    directly to get the births subset.

    Useful for "born on this day" content hooks, birthday round-ups,
    newsletter intros, and any place where the "who was born today in
    history" framing fits. Pairs naturally with `on_this_day` (events)
    and `featured_article` (today's long-form pick) for a full "today
    in Wikipedia" daily digest.
    """
    try:
        count = max(1, min(int(count), 10))
    except (TypeError, ValueError):
        count = 5
    today_mm_dd = datetime.now(timezone.utc).strftime("%m/%d")
    resp = _get(f"{_base(lang)}/feed/onthisday/births/{today_mm_dd}")
    if resp.status_code == 404:
        return f"No 'births on this day' available for {lang}.wikipedia.org today."
    resp.raise_for_status()
    births = resp.json().get("births", [])
    if not births:
        return f"No notable births found for today on {lang}.wikipedia.org."

    sample = random.sample(births, min(count, len(births)))
    out = "**Births on this day:**\n\n"
    for entry in sample:
        year = entry.get("year", "?")
        text = _strip_html(entry.get("text", ""))
        out += f"- **{year}** — {text}\n"
        pages = entry.get("pages", [])
        if pages:
            page_title = pages[0].get("title", "")
            if page_title:
                out += (
                    f"  [Read on Wikipedia]"
                    f"(https://{lang}.wikipedia.org/wiki/{page_title})\n"
                )
    return out


def _today() -> str:
    return datetime.now(timezone.utc).strftime("%Y/%m/%d")


def image(title: str, lang: str = "en") -> str:
    """Get just the lead image for a Wikipedia article (no summary text).

    Returns both the 300px thumbnail URL and the full-resolution
    original URL from Wikipedia's REST summary endpoint. Useful when
    you want the article's image for embedding elsewhere (cards,
    Telegram posts, slide decks, README hero images) without the
    surrounding summary text — `summary` embeds the thumbnail inline,
    but exposes only one URL and bundles it with prose. `image`
    returns both URLs separately so downstream tools can fetch /
    display at any size.

    Returns a clean "no image available" message if the article has
    no thumbnail or original image (many lists, disambiguation pages,
    and stub articles don't).
    """
    resp = _get(f"{_base(lang)}/page/summary/{_slug(title)}")
    if resp.status_code == 404:
        return f"Article '{title}' not found on Wikipedia."
    resp.raise_for_status()
    data = resp.json()

    title_out = data.get("title", title)
    thumb = (
        data.get("thumbnail", {}).get("source", "")
        if data.get("thumbnail") else ""
    )
    original = (
        data.get("originalimage", {}).get("source", "")
        if data.get("originalimage") else ""
    )
    desktop_url = (
        data.get("content_urls", {}).get("desktop", {}).get("page", "#")
    )

    if not thumb and not original:
        return (
            f"No image available for '{title_out}' on {lang}.wikipedia."
        )

    out = f"## {title_out} — Lead Image\n\n"
    if original:
        out += f"**Original (full size):** {original}\n\n"
    if thumb:
        out += f"**Thumbnail (300px):** {thumb}\n\n"
    out += f"![{title_out}]({original or thumb})\n\n"
    out += f"[Read more →]({desktop_url})"
    return out


def links(title: str, limit: int = 20, lang: str = "en") -> str:
    """List Wikipedia article links (outgoing internal links) from a page.

    Returns the first N article titles that an article links to (the
    "see also" network in raw form, no filtering by section). Useful
    for graph-style discovery — e.g. given "Tyrannosaurus", see which
    genera, paleontologists, formations, and anatomical terms it
    references. Complements `categories` (taxonomy) and `search`
    (text-based) — `links` shows what the article itself points to.
    Filters to main namespace (ns=0) so talk/user/etc. don't pollute
    the result.
    """
    try:
        limit = max(1, min(int(limit), 50))
    except (TypeError, ValueError):
        limit = 20
    params = {
        "action": "query",
        "prop": "links",
        "titles": title,
        "pllimit": limit,
        "plnamespace": 0,
        "format": "json",
        "origin": "*",
    }
    resp = _get(_wiki(lang), params=params)
    if resp.status_code == 404:
        return f"Article '{title}' not found on Wikipedia."
    resp.raise_for_status()
    data = resp.json()
    pages = data.get("query", {}).get("pages", {})
    if not pages:
        return f"No links found for '{title}'."

    page = next(iter(pages.values()))
    if page.get("missing") is not None:
        return f"Article '{title}' not found on Wikipedia."
    out_links = page.get("links", [])
    if not out_links:
        return f"No links found for '{page.get('title', title)}'."

    page_title = page.get("title", title)
    out = f"**Links from \"{page_title}\":**\n\n"
    for lnk in out_links:
        name = lnk.get("title", "").strip()
        if name:
            out += f"- {name}\n"
    out += (
        f"\n[View article]"
        f"(https://{lang}.wikipedia.org/wiki/{_slug(page_title)})"
    )
    return out


def backlinks(title: str, limit: int = 20, lang: str = "en") -> str:
    """List incoming Wikipedia links to an article (backlinks).

    Returns the first N article titles that link TO the given article —
    i.e. "what links here" / backlinks / referrer pages. Inverse of
    `links` (which shows outgoing references). Useful for graph-style
    discovery in the opposite direction — given "Velociraptor", see
    which other articles reference it (cultural mentions, scientific
    citations, comparative anatomy pages, etc.). Complements `links`
    and `categories` for mapping an article's position in the
    encyclopedia network. Filters to main namespace (ns=0) so
    talk/user/etc. don't pollute the result.
    """
    try:
        limit = max(1, min(int(limit), 50))
    except (TypeError, ValueError):
        limit = 20
    params = {
        "action": "query",
        "prop": "linkshere",
        "titles": title,
        "lhlimit": limit,
        "lhnamespace": 0,
        "format": "json",
        "origin": "*",
    }
    resp = _get(_wiki(lang), params=params)
    if resp.status_code == 404:
        return f"Article '{title}' not found on Wikipedia."
    resp.raise_for_status()
    data = resp.json()
    pages = data.get("query", {}).get("pages", {})
    if not pages:
        return f"No backlinks found for '{title}'."

    page = next(iter(pages.values()))
    if page.get("missing") is not None:
        return f"Article '{title}' not found on Wikipedia."
    in_links = page.get("linkshere", [])
    if not in_links:
        return f"No backlinks found for '{page.get('title', title)}'."

    page_title = page.get("title", title)
    out = f"**Backlinks to \"{page_title}\":**\n\n"
    for lnk in in_links:
        name = lnk.get("title", "").strip()
        if name:
            out += f"- {name}\n"
    out += (
        f"\n[View article]"
        f"(https://{lang}.wikipedia.org/wiki/{_slug(page_title)})"
    )
    return out


def external_links(title: str, limit: int = 20, lang: str = "en") -> str:
    """List external (off-wiki) links from a Wikipedia article.

    Returns the first N external URLs the article links to — citations,
    references, primary sources, archives, and other off-wiki resources
    that the article uses to back up its claims. This is the outbound
    complement to `links` (internal outgoing) and `backlinks` (internal
    incoming): `external_links` shows what the article points to
    OUTSIDE Wikipedia. The trio (`links` + `backlinks` + `external_links`)
    maps the full network around an article.

    Wikipedia exposes external links via the MediaWiki Action API's
    `prop=extlinks` parameter — each entry is the raw URL (the `*` field
    in the JSON response). Useful for source verification (does the
    article actually cite the claim?), citation audits, building a
    bibliography, primary-source discovery, and fact-checking research.
    Pairs naturally with `links` (in-article reference network) and
    `categories` (taxonomy) for full article-network analysis.

    `limit` clamps the number of URLs returned (default 20, max 50).
    Articles with dense citation footers can easily have hundreds of
    external links — raise the limit if you need a full bibliography
    audit, or keep the default for a quick "what does this cite?" scan.
    """
    try:
        limit = max(1, min(int(limit), 50))
    except (TypeError, ValueError):
        limit = 20
    params = {
        "action": "query",
        "prop": "extlinks",
        "titles": title,
        "ellimit": limit,
        "format": "json",
        "origin": "*",
    }
    resp = _get(_wiki(lang), params=params)
    if resp.status_code == 404:
        return f"Article '{title}' not found on Wikipedia."
    resp.raise_for_status()
    data = resp.json()
    pages = data.get("query", {}).get("pages", {})
    if not pages:
        return f"No external links found for '{title}'."

    page = next(iter(pages.values()))
    if page.get("missing") is not None:
        return f"Article '{title}' not found on Wikipedia."
    ext = page.get("extlinks", [])
    if not ext:
        return f"No external links found for '{page.get('title', title)}'."

    page_title = page.get("title", title)
    out = f'**External links from "{page_title}":**\n\n'
    for entry in ext:
        url = (entry.get("*") or "").strip()
        if url:
            out += f"- {url}\n"
    out += (
        f"\n[View article]"
        f"(https://{lang}.wikipedia.org/wiki/{_slug(page_title)})"
    )
    return out


def nearby(title: str = "", lat=None, lon=None, radius: int = 1000,
           limit: int = 20, lang: str = "en") -> str:
    """List Wikipedia articles geographically near a location.

    Two ways to anchor the search (provide one):
    - title: an article title, e.g. 'Eiffel Tower' — finds articles near
      that article's recorded coordinates (no external geocoding needed).
    - lat + lon: explicit decimal coordinates, e.g. lat=48.8584, lon=2.2945.
      If both title and coordinates are given, the coordinates win.

    Returns nearby articles with their distance from the anchor, plus a
    link to the anchor article. Useful for location-based discovery —
    "what's notable around here", travel research, mapping notable places
    around a landmark. Filters to main namespace (ns=0).
    """
    try:
        limit = max(1, min(int(limit), 50))
    except (TypeError, ValueError):
        limit = 20
    try:
        radius = max(10, min(int(radius), 10000))
    except (TypeError, ValueError):
        radius = 1000

    params = {
        "action": "query",
        "list": "geosearch",
        "gsradius": radius,
        "gslimit": limit,
        "gsnamespace": 0,
        "format": "json",
        "formatversion": 2,
        "origin": "*",
    }

    title = (title or "").strip()
    anchor_label = ""
    anchor_link = ""
    used_coords = False
    if lat is not None and lon is not None and str(lat) != "" and str(lon) != "":
        try:
            lat_f = float(lat)
            lon_f = float(lon)
        except (TypeError, ValueError):
            return (
                "Invalid coordinates: lat and lon must be numbers "
                f"(got lat={lat!r}, lon={lon!r})."
            )
        if not (-90 <= lat_f <= 90) or not (-180 <= lon_f <= 180):
            return (
                "Invalid coordinates: lat must be between -90 and 90, "
                f"lon between -180 and 180 (got lat={lat_f}, lon={lon_f})."
            )
        params["gscoord"] = f"{lat_f}|{lon_f}"
        anchor_label = f"{lat_f}, {lon_f}"
        used_coords = True
    elif title:
        params["gspage"] = title
        anchor_label = f'"{title}"'
        anchor_link = (
            f"\n[View {title}]"
            f"(https://{lang}.wikipedia.org/wiki/{_slug(title)})"
        )
    else:
        return (
            "Provide a location: either `title` (an article title, e.g. "
            "'Eiffel Tower') or both `lat` and `lon` (decimal coordinates, "
            "e.g. lat=48.8584, lon=2.2945)."
        )

    resp = _get(_wiki(lang), params=params)
    resp.raise_for_status()
    data = resp.json()
    results = data.get("query", {}).get("geosearch", [])
    if not results:
        hint = (
            " — the article may not exist or has no coordinates recorded"
            if title and not used_coords
            else ""
        )
        return f"No nearby articles found for {anchor_label}{hint}."

    def _fmt_dist(m):
        m = float(m)
        return f"{m:,.0f} m" if m < 1000 else f"{m / 1000:,.1f} km"

    out = (
        f"**Articles near {anchor_label} "
        f"(within {_fmt_dist(radius)}):**\n\n"
    )
    for r in results:
        name = r.get("title", "").strip()
        if name:
            out += f"- {name} — {_fmt_dist(r.get('dist', 0))}\n"
    out += anchor_link
    return out


def categories(title: str, limit: int = 20, lang: str = "en") -> str:
    """List Wikipedia categories for an article.

    Returns the Wikipedia categories an article belongs to (e.g.
    "Late Cretaceous dinosaurs", "Articles containing Latin-language text").
    Useful for taxonomy-based discovery — finding related topics that
    don't show up in text search. Hidden/maintenance categories are
    filtered out so the result is high-signal.
    """
    try:
        limit = max(1, min(int(limit), 50))
    except (TypeError, ValueError):
        limit = 20
    params = {
        "action": "query",
        "prop": "categories",
        "titles": title,
        "cllimit": limit,
        "clshow": "!hidden",
        "clsort": "sortkey",
        "format": "json",
        "origin": "*",
    }
    resp = _get(_wiki(lang), params=params)
    if resp.status_code == 404:
        return f"Article '{title}' not found on Wikipedia."
    resp.raise_for_status()
    data = resp.json()
    pages = data.get("query", {}).get("pages", {})
    if not pages:
        return f"No categories found for '{title}'."

    # API returns pages as {pageid: {...}}; missing pages have id=-1
    page = next(iter(pages.values()))
    if page.get("missing") is not None or page.get("title", "") == "" and "categories" not in page:
        return f"Article '{title}' not found on Wikipedia."
    cats = page.get("categories", [])
    if not cats:
        return f"No categories found for '{page.get('title', title)}'."

    page_title = page.get("title", title)
    out = f"**Categories for \"{page_title}\":**\n\n"
    for cat in cats:
        # Strip "Category:" prefix for cleaner display
        name = cat.get("title", "").replace("Category:", "", 1)
        if name:
            out += f"- {name}\n"
    out += (
        f"\n[View article]"
        f"(https://{lang}.wikipedia.org/wiki/{_slug(page_title)})"
    )
    return out


def translations(title: str, limit: int = 30, lang: str = "en") -> str:
    """List all language versions of a Wikipedia article (langlinks).

    Returns the other-language editions of the article that Wikipedia
    knows about — e.g. for 'Tyrannosaurus' (en), returns de/fr/es/ja/zh
    titles where the equivalent article exists. Complements the
    one-way `lang` parameter used by the other tools: every tool can
    query a single language, but only `translations` reveals the
    article's full language coverage so callers can pick a target
    language to fetch next.

    Useful for translation research (which languages have full
    coverage vs. stubs), cross-language content sourcing, and
    language-coverage analysis. Uses Wikipedia's `prop=langlinks`
    API; the response is filtered to real articles (no redirects).
    `limit` clamps the number of entries (default 30, max 100) —
    popular articles can have 100+ language versions.
    """
    try:
        limit = max(1, min(int(limit), 100))
    except (TypeError, ValueError):
        limit = 30
    params = {
        "action": "query",
        "prop": "langlinks",
        "titles": title,
        "lllimit": limit,
        "format": "json",
        "origin": "*",
    }
    resp = _get(_wiki(lang), params=params)
    if resp.status_code == 404:
        return f"Article '{title}' not found on Wikipedia."
    resp.raise_for_status()
    data = resp.json()
    pages = data.get("query", {}).get("pages", {})
    if not pages:
        return f"No translations found for '{title}'."

    page = next(iter(pages.values()))
    if page.get("missing") is not None:
        return f"Article '{title}' not found on Wikipedia."
    ll = page.get("langlinks", [])
    if not ll:
        return f"No other-language versions found for '{page.get('title', title)}'."

    page_title = page.get("title", title)
    out = f'**Translations of "{page_title}":**\n\n'
    for entry in ll:
        tgt_lang = entry.get("lang", "?")
        # MediaWiki returns the localized title under the "*" key
        # (the legacy Action API convention); fall back to "title"
        # for safety if a future endpoint changes shape.
        tgt_title = (entry.get("*") or entry.get("title") or "").strip()
        if tgt_lang and tgt_title:
            out += f"- `{tgt_lang}`: [{tgt_title}]"
            out += f"(https://{tgt_lang}.wikipedia.org/wiki/{_slug(tgt_title)})\n"
    out += (
        f"\n[View article]"
        f"(https://{lang}.wikipedia.org/wiki/{_slug(page_title)})"
    )
    return out


def revisions(title: str, limit: int = 10, lang: str = "en") -> str:
    """Show an article's recent edit history ('View history').

    Returns the most recent revisions with revision id, timestamp,
    editor, edit summary, and byte-size delta vs the previous revision.
    Each revision links to its diff (Special:Diff/<revid>) so callers
    can inspect exactly what changed. Useful for tracking how an
    article evolves over time, auditing edits on a topic, or spotting
    edit activity around current events. Complements `pageviews`
    (popularity) with provenance (who changed what, when).
    """
    try:
        limit = max(1, min(int(limit), 50))
    except (TypeError, ValueError):
        limit = 10
    params = {
        "action": "query",
        "prop": "revisions",
        "titles": title,
        "rvprop": "ids|timestamp|user|comment|size|flags",
        "rvlimit": limit,
        "rvslots": "main",
        "format": "json",
        "origin": "*",
    }
    resp = _get(_wiki(lang), params=params)
    if resp.status_code == 404:
        return f"Article '{title}' not found on Wikipedia."
    resp.raise_for_status()
    data = resp.json()
    pages = data.get("query", {}).get("pages", {})
    if not pages:
        return f"No revisions found for '{title}'."

    page = next(iter(pages.values()))
    if page.get("missing") is not None:
        return f"Article '{title}' not found on Wikipedia."
    revs = page.get("revisions", [])
    if not revs:
        return f"No revisions found for '{page.get('title', title)}'."

    page_title = page.get("title", title)
    out = f'**Revision history of "{page_title}" ({len(revs)} most recent):**\n\n'
    # Revisions arrive newest-first; delta compares each revision against
    # the next (older) one, so the oldest shown revision has no delta.
    for i, rev in enumerate(revs):
        revid = rev.get("revid", "?")
        ts = (rev.get("timestamp") or "?")[:16].replace("T", " ")
        user = rev.get("user", "?")
        comment = (rev.get("comment") or "").strip() or "(no edit summary)"
        minor = " [m]" if "minor" in rev else ""
        size = rev.get("size")
        delta = ""
        if isinstance(size, int) and i + 1 < len(revs):
            older = revs[i + 1].get("size")
            if isinstance(older, int):
                d = size - older
                delta = f" ({d:+,d} bytes)"
        diff_url = f"https://{lang}.wikipedia.org/wiki/Special:Diff/{revid}"
        out += (
            f"- `{ts}` — **{user}**{minor}{delta}: {comment} "
            f"([diff]({diff_url}))\n"
        )
    out += (
        f"\n[Full history]"
        f"(https://{lang}.wikipedia.org/w/index.php"
        f"?title={_slug(page_title)}&action=history)"
    )
    return out


def pageviews(title: str, start: str = "", end: str = "", lang: str = "en") -> str:
    """Get daily view counts for a Wikipedia article over a date range.

    Uses Wikimedia's pageviews REST API (per-article, all-access, daily
    granularity). Useful for popularity research, trending topics, and
    historical interest — e.g. "how is X trending this week?" or
    "what was the spike on date Y?".

    Returns a markdown table with daily views, total, and daily average.
    Default window is the last 7 days ending yesterday (UTC). The
    article must have measurable traffic — very new or very niche
    articles may return 404 from the pageviews API.
    """
    if not title or not title.strip():
        return "Error: title is required."

    # Validate lang (use SUPPORTED_LANGS so the URL is consistent and
    # falls back to "en" rather than producing a 404 for typos).
    lang = lang if lang in SUPPORTED_LANGS else "en"

    # Default dates: 7-day window ending yesterday UTC.
    if end == "":
        end_dt = datetime.now(timezone.utc) - timedelta(days=1)
        end = end_dt.strftime("%Y%m%d")
    if start == "":
        try:
            end_dt = datetime.strptime(end, "%Y%m%d")
        except ValueError:
            return f"Error: end date must be in YYYYMMDD format (got '{end}')"
        start = (end_dt - timedelta(days=6)).strftime("%Y%m%d")

    try:
        datetime.strptime(start, "%Y%m%d")
        datetime.strptime(end, "%Y%m%d")
    except ValueError:
        return f"Error: dates must be in YYYYMMDD format (got start='{start}', end='{end}')"

    if start > end:
        return f"Error: start date {start} is after end date {end}"

    encoded_title = _slug(title)
    # Pageviews API is a cross-wiki metric hosted centrally on wikimedia.org,
    # not on the per-language wiki. Use wikimedia.org as the base regardless
    # of `lang`; the language-specific project (e.g. "en.wikipedia") lives in
    # the URL path, not the host.
    url = (
        f"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/"
        f"{lang}.wikipedia/all-access/user/{encoded_title}/daily/{start}00/{end}00"
    )

    try:
        resp = _get(url)
    except requests.RequestException as e:
        return f"Error fetching pageviews: {e}"

    if resp.status_code == 404:
        return (
            f"No pageviews data found for '{title}' in {lang}.wikipedia "
            f"between {start} and {end}. Article may not exist or have "
            f"insufficient history."
        )
    if resp.status_code != 200:
        return f"Error: pageviews API returned {resp.status_code} for '{title}'."

    data = resp.json()
    items = data.get("items", [])

    if not items:
        return f"No pageviews found for '{title}' in {lang} between {start} and {end}."

    total = sum(item["views"] for item in items)
    avg = total // len(items) if items else 0

    page_title = items[0].get("article", title).replace("_", " ")

    out = f'**Pageviews for "{page_title}"** ({lang}.wikipedia)\n\n'
    out += f"**Period:** {start} → {end} ({len(items)} days)  \n"
    out += f"**Total views:** {total:,}  |  **Daily average:** {avg:,}\n\n"
    out += "| Date | Views |\n"
    out += "|------|------:|\n"

    for item in items:
        ts = item["timestamp"]
        date_str = f"{ts[:4]}-{ts[4:6]}-{ts[6:8]}"
        out += f"| {date_str} | {item['views']:,} |\n"

    out += f"\n[View article](https://{lang}.wikipedia.org/wiki/{encoded_title})"
    return out


def news(lang: str = "en", limit: int = 5) -> str:
    """Get current events from Wikipedia's Main Page 'In the news' section.

    Returns today's curated list of recent notable events from the Main
    Page (Wikipedia's editorially-updated current-events feed). Pairs with
    `featured_article` (today's long-form pick) and `on_this_day`
    (historical) — `news` covers the present tense. The Main Page is
    rendered server-side, then the 'In the news' block is parsed out of
    the HTML so bold + linked article titles become Markdown.
    """
    try:
        limit = max(1, min(int(limit), 10))
    except (TypeError, ValueError):
        limit = 5

    params = {
        "action": "parse",
        "page": "Main_Page",
        "prop": "text",
        "format": "json",
        "origin": "*",
    }
    resp = _get(_wiki(lang), params=params)
    resp.raise_for_status()
    data = resp.json()

    if "error" in data:
        return f"Could not fetch news for {lang}.wikipedia.org today."

    html = data.get("parse", {}).get("text", {}).get("*", "")
    if not html:
        return f"No news available for {lang}.wikipedia.org today."

    # The Main Page renders "In the news" as a sibling <h2> + <div> block:
    # <h2 id="mp-itn-h2">In the news</h2>
    # <div id="mp-itn">...<ul><li>event text with links</li>...</ul></div>
    # Grab everything between that h2 and the next h2 in the page.
    m = re.search(
        r'<h2[^>]*id="mp-itn-h2"[^>]*>.*?</h2>(.*?)<h2',
        html,
        re.DOTALL,
    )
    if not m:
        return f"No 'In the news' section found on {lang}.wikipedia.org today."

    block = m.group(1)
    items = re.findall(r"<li>(.*?)</li>", block, re.DOTALL)
    if not items:
        return f"No news items found on {lang}.wikipedia.org today."

    sample = items[:limit]
    out = "**In the news:**\n\n"
    for item in sample:
        # Bold-linked article: <b><a href="/wiki/Title">Name</a></b>
        # Render as **[Name](url)** so the main subject stands out.
        md = re.sub(
            r'<b>\s*<a[^>]+href="/wiki/([^"#]+)"[^>]*>([^<]+)</a>\s*</b>',
            lambda mm: f'**[{mm.group(2)}](https://{lang}.wikipedia.org/wiki/{mm.group(1)})**',
            item,
        )
        # Plain wiki links: [Name](url)
        md = re.sub(
            r'<a[^>]+href="/wiki/([^"#]+)"[^>]*>([^<]+)</a>',
            lambda mm: f'[{mm.group(2)}](https://{lang}.wikipedia.org/wiki/{mm.group(1)})',
            md,
        )
        # Italics (e.g. "(pictured)") stay as *text*
        md = re.sub(r"<i>([^<]*)</i>", r"*\1*", md)
        # Strip any remaining tags
        md = re.sub(r"<[^>]+>", "", md)
        md = unescape(md)
        md = re.sub(r"\s+", " ", md).strip()
        if md:
            out += f"- {md}\n"

    out += f"\n[Wikipedia Main Page](https://{lang}.wikipedia.org/wiki/Main_Page)"
    return out


def top_reads(date: str = "", limit: int = 10, lang: str = "en") -> str:
    """Get the most-read articles on Wikipedia for a given date.

    Uses Wikimedia's top-pageviews endpoint (all-access, daily) to
    return the top-N most-viewed articles on a language Wikipedia for a
    single day. Default date is yesterday UTC — today's data is
    typically not yet finalized, so defaulting to yesterday reliably
    returns a populated list.

    Filters out non-content namespaces (Main_Page, Special:Search,
    Portal:Current_events, Wikipedia:*, Talk:*, etc.) so the result is
    real articles only. Useful for "what's trending on Wikipedia"
    research and daily content hooks — pairs with `pageviews` (which is
    per-article over a range) for trending-vs-popular comparisons.

    Returns a markdown table: rank, article title (linked), and view
    count for the day.
    """
    lang = lang if lang in SUPPORTED_LANGS else "en"

    if date == "":
        date = (datetime.now(timezone.utc) - timedelta(days=1)).strftime("%Y%m%d")

    try:
        dt = datetime.strptime(date, "%Y%m%d")
    except ValueError:
        return f"Error: date must be in YYYYMMDD format (got '{date}')"

    # Pageviews API is cross-wiki; lang is in the path, not the host.
    url = (
        f"https://wikimedia.org/api/rest_v1/metrics/pageviews/top/"
        f"{lang}.wikipedia/all-access/{dt.year:04d}/{dt.month:02d}/{dt.day:02d}"
    )

    try:
        resp = _get(url)
    except requests.RequestException as e:
        return f"Error fetching top-reads: {e}"

    if resp.status_code == 404:
        return f"No top-reads data found for {lang}.wikipedia on {date}."
    if resp.status_code != 200:
        return f"Error: pageviews API returned {resp.status_code} for {date}."

    data = resp.json()
    items = data.get("items", [])
    if not items:
        return f"No top-reads found for {lang}.wikipedia on {date}."

    all_articles = items[0].get("articles", [])
    if not all_articles:
        return f"No top-reads found for {lang}.wikipedia on {date}."

    # Filter out non-content namespaces so users get real articles, not
    # Wikipedia infrastructure pages. The top-reads feed always ranks
    # Main_Page #1 (millions of daily views), Special:Search #2 (the
    # search bar), and Wikipedia:Featured_pictures high — these are
    # useful as raw telemetry but useless as content hooks.
    SKIP_PREFIXES = (
        "Main_Page", "Special:", "Wikipedia:", "Portal:", "Help:",
        "Talk:", "Template:", "Category:", "MediaWiki:", "User:",
        "File:", "Draft:", "Module:",
    )
    filtered = [
        a for a in all_articles
        if not any(a["article"].startswith(p) for p in SKIP_PREFIXES)
    ]

    try:
        limit = max(1, min(int(limit), 50))
    except (TypeError, ValueError):
        limit = 10

    sample = filtered[:limit]
    if not sample:
        return f"No top-reads articles found for {lang}.wikipedia on {date} (after filtering)."

    pretty_date = f"{date[:4]}-{date[4:6]}-{date[6:8]}"
    out = f"**Top reads on {lang}.wikipedia — {pretty_date}:**\n\n"
    out += "| Rank | Article | Views |\n"
    out += "|------|---------|------:|\n"

    for art in sample:
        title = art["article"].replace("_", " ")
        rank = art.get("rank", "?")
        views = art.get("views", 0)
        slug = art["article"]
        out += (
            f"| {rank} | [{title}]"
            f"(https://{lang}.wikipedia.org/wiki/{slug}) "
            f"| {views:,} |\n"
        )

    out += (
        f"\n[View full list]"
        f"(https://wikimedia.org/api/rest_v1/metrics/pageviews/top/"
        f"{lang}.wikipedia/all-access/{dt.year:04d}/{dt.month:02d}/{dt.day:02d})"
    )
    return out


def media_list(title: str, limit: int = 25, lang: str = "en") -> str:
    """List all media (images, videos, audio) used in a Wikipedia article.

    Returns a structured markdown list of every media item the article
    uses — not just the lead thumbnail. Each entry shows the media type
    (image / video / audio), the file title on Wikimedia Commons, an
    optional caption (plain text, with HTML stripped), and the
    thumbnail URL at the smallest scale. Lead media is marked with a
    trophy so callers can skip it when they already have it via `image`.

    Complements `image` (which returns only the lead thumbnail + original
    URLs in a text block) — `media_list` is for callers that want the
    full inventory: gallery generation, fact-checking images cited in
    an article, slide decks, content audits. Uses Wikipedia's REST
    `/page/media-list` endpoint which returns structured JSON, no HTML
    parsing required.

    `limit` clamps the number of items returned (default 25, max 100).
    Wikipedia articles can easily have 50+ media items — raise the limit
    if you need the full set, or keep the default to keep responses
    concise.
    """
    try:
        limit = max(1, min(int(limit), 100))
    except (TypeError, ValueError):
        limit = 25
    resp = _get(f"{_base(lang)}/page/media-list/{_slug(title)}")
    if resp.status_code == 404:
        return f"Article '{title}' not found on Wikipedia."
    resp.raise_for_status()
    data = resp.json()
    items = data.get("items", [])
    if not items:
        return f"No media found for '{title}' on {lang}.wikipedia."

    sample = items[:limit]
    out = (
        f"**Media in \"{title}\":** "
        f"({len(items)} total, showing {len(sample)})\n\n"
    )
    for item in sample:
        file_title = item.get("title", "Unknown")
        media_type = item.get("type", "media")
        is_lead = item.get("leadImage", False)
        lead_marker = " 🏆 (lead)" if is_lead else ""
        caption = ""
        cap = item.get("caption")
        if isinstance(cap, dict):
            caption = (cap.get("text") or "").strip()
        elif isinstance(cap, str):
            caption = cap.strip()
        srcset = item.get("srcset", []) or []
        thumb_url = ""
        if srcset:
            thumb_url = srcset[0].get("src", "")
            # Protocol-relative URLs ("//upload.wikimedia.org/...") need
            # an explicit scheme so MCP clients can resolve them.
            if thumb_url.startswith("//"):
                thumb_url = "https:" + thumb_url

        out += f"- **{file_title}**{lead_marker}\n"
        out += f"  Type: {media_type}\n"
        if caption:
            cap_display = caption[:200] + ("..." if len(caption) > 200 else "")
            out += f"  Caption: {cap_display}\n"
        if thumb_url:
            out += f"  Thumbnail: {thumb_url}\n"
        out += "\n"

    desktop_url = f"https://{lang}.wikipedia.org/wiki/{_slug(title)}"
    out += f"[View article]({desktop_url})"
    return out


_COMMONS_API = "https://commons.wikimedia.org/w/api.php"

# CirrusSearch filetype filter per media_search() filetype argument.
# "image" covers both bitmap photos and drawings/SVGs (diagrams, maps).
_FILETYPE_FILTER = {
    "image": "filetype:bitmap|drawing",
    "video": "filetype:video",
    "audio": "filetype:audio",
}


# Commons sometimes reports generic mime types (e.g. application/ogg for
# both .oga audio and .ogv video), so fall back to the file extension when
# the mime type doesn't name a media kind directly.
_MEDIA_KIND_BY_EXT = {
    "jpg": "image", "jpeg": "image", "png": "image", "gif": "image",
    "svg": "image", "tif": "image", "tiff": "image", "webp": "image",
    "xcf": "image", "pdf": "document",
    "webm": "video", "mp4": "video", "ogv": "video", "mov": "video",
    "ogg": "audio", "oga": "audio", "opus": "audio", "flac": "audio",
    "wav": "audio", "mp3": "audio", "mid": "audio", "midi": "audio",
}


def _media_kind(mime: str, title: str) -> str:
    m = (mime or "").lower()
    if m.startswith(("image/", "video/", "audio/")):
        return m.split("/")[0]
    ext = title.rsplit(".", 1)[-1].lower() if "." in title else ""
    return _MEDIA_KIND_BY_EXT.get(ext, "media")


def media_search(query: str, limit: int = 10, filetype: str = "image") -> str:
    """Search Wikimedia Commons for freely-licensed media by keyword.

    Full-text search across the Commons media library (File: namespace)
    — the first tool in this skill that finds media by *topic* instead of
    by article. `image` returns only the lead image of a known article and
    `media_list` inventories media already used in an article; neither
    helps when you need an illustration for a topic with no article yet
    (a blog post, slide deck, README hero image, Wiki Rabbit Hole node).
    `media_search` fills that gap: give it a keyword, get back real files
    you can hotlink.

    Everything on Commons is freely licensed, and each result reports its
    license short name, the artist/uploader, a thumbnail URL (320px), the
    full-resolution URL, and a link to the file page — enough to embed
    and attribute correctly. `filetype` filters the result set:
    "image" (default, photos + diagrams/SVGs), "video", "audio", or "all".

    `limit` clamps the number of results (default 10, max 50).
    Uses the read-only Commons action API (generator=search on the File:
    namespace) — no new dependencies, same descriptive User-Agent.
    """
    if not query or not query.strip():
        return "Please provide a search query (e.g. media_search('aurora borealis'))."
    query = query.strip()
    try:
        limit = max(1, min(int(limit), 50))
    except (TypeError, ValueError):
        limit = 10

    filetype = (filetype or "image").lower()
    if filetype not in ("image", "video", "audio", "all"):
        return (
            f"Invalid filetype '{filetype}'. "
            "Use 'image', 'video', 'audio', or 'all'."
        )

    gsrsearch = query
    if filetype in _FILETYPE_FILTER:
        gsrsearch = f"{query} {_FILETYPE_FILTER[filetype]}"

    params = {
        "action": "query",
        "generator": "search",
        "gsrsearch": gsrsearch,
        "gsrnamespace": 6,
        "gsrlimit": limit,
        "prop": "imageinfo",
        "iiprop": "url|size|mime|extmetadata",
        "iiurlwidth": 320,
        "iiextmetadatafilter": "ImageDescription|Artist|LicenseShortName",
        "format": "json",
        "formatversion": "2",
    }
    resp = _get(_COMMONS_API, params=params)
    resp.raise_for_status()
    data = resp.json()
    pages = (data.get("query") or {}).get("pages", [])
    if not pages:
        return (
            f"No media found on Wikimedia Commons for '{query}'"
            + (f" (filetype '{filetype}')" if filetype != "all" else "")
            + "."
        )

    # API doesn't guarantee result order; keep it stable by title.
    pages = sorted(pages, key=lambda p: p.get("title", ""))[:limit]

    out = (
        f"## Media search: \"{query}\" "
        f"({len(pages)} result{'s' if len(pages) != 1 else ''}, "
        f"filetype: {filetype})\n\n"
    )
    for page in pages:
        file_title = page.get("title", "Unknown")
        info = (page.get("imageinfo") or [{}])[0]
        mime = info.get("mime", "")
        kind = _media_kind(mime, file_title)
        width = info.get("width")
        height = info.get("height")
        dims = f"{width}×{height}" if width and height else "unknown size"
        # imageinfo URLs carry ?utm_source=... tracking params; strip them.
        full_url = (info.get("url") or "").split("?")[0]
        thumb_url = (info.get("thumburl") or "").split("?")[0]
        file_page = (
            "https://commons.wikimedia.org/wiki/"
            + file_title.replace(" ", "_")
        )

        meta = info.get("extmetadata") or {}
        license_name = (meta.get("LicenseShortName") or {}).get("value", "")
        artist = _strip_html(
            (meta.get("Artist") or {}).get("value", "")
        ).strip()
        desc = _strip_html(
            (meta.get("ImageDescription") or {}).get("value", "")
        ).strip()

        out += f"- **{file_title}**\n"
        out += f"  Type: {kind} ({dims})\n"
        if license_name:
            out += f"  License: {license_name}\n"
        if artist:
            artist_display = (
                artist[:120] + ("..." if len(artist) > 120 else "")
            )
            out += f"  Artist: {artist_display}\n"
        if desc:
            desc_display = desc[:200] + ("..." if len(desc) > 200 else "")
            out += f"  Description: {desc_display}\n"
        if thumb_url:
            out += f"  Thumbnail (320px): {thumb_url}\n"
        if full_url:
            out += f"  Full size: {full_url}\n"
        out += f"  [Commons file page →]({file_page})\n\n"

    out += (
        "All files are freely licensed — check the license on the file "
        "page before reuse."
    )
    return out


def quote(lang: str = "en") -> str:
    """Get a random notable quote from a curated list of famous authors.

    Returns a randomly selected quote (author + attribution) from a
    curated list of 23 well-known authors spanning philosophers,
    scientists, statesmen, writers, and activists (Churchill, Einstein,
    Twain, Gandhi, Mandela, Wilde, Angelou, Jobs, Lennon, Socrates,
    etc.). Quotes are short, time-tested, and well-attributed — the
    same approach as `dino_fact`'s DINOS list (high-quality curated
    data, no scraping fragility). Useful for daily content hooks,
    social posts, newsletter intros, and any place where a pithy
    quotation adds weight to a message. Pairs with `did_you_know`
    (random encyclopedia fact) and `dino_fact` (random dino fact) for
    variety in "today's trivia" outputs.

    The `lang` parameter is accepted for API consistency with the
    other tools but is currently English-only — the curated list is
    English. Non-English values are accepted without error and still
    return English quotes. Multi-language quote support via Wikiquote
    is a possible future iteration.
    """
    author, text = random.choice(FAMOUS_QUOTES)
    return (
        f'💬 **"{text}"**\n\n'
        f"— *{author}*"
    )


# ---------------------------------------------------------------------------
# Recent changes — live edit activity on Wikipedia
# ---------------------------------------------------------------------------
RECENT_CHANGE_KINDS = ("all", "edit", "new", "categorize", "log")


def recent_changes(kind: str = "all", limit: int = 10, lang: str = "en") -> str:
    """Show the most recent changes to Wikipedia articles.

    Uses the MediaWiki `list=recentchanges` endpoint to stream live edit
    activity across the article namespace — a window into what's happening
    on Wikipedia *right now*. Complements `revisions` (history of one
    article) with the reverse angle: the freshest edits everywhere.

    `kind` filters the stream: "edit" (text changes), "new" (newly
    published articles — a discovery feed of brand-new pages),
    "categorize" (category membership changes), "log" (page moves,
    deletions, protections, etc.). "all" (default) mixes them all.

    Each entry shows the change kind, article link, byte-size delta,
    editor, timestamp, and edit comment (when present), so callers can
    spot breaking-news edits, new pages on emerging topics, and
    bot-maintenance sweeps at a glance. Read-only (HTTPS GET).
    """
    kind = str(kind or "all").lower()
    if kind not in RECENT_CHANGE_KINDS:
        kind = "all"
    try:
        limit = max(1, min(int(limit), 50))
    except (TypeError, ValueError):
        limit = 10

    params = {
        "action": "query",
        "list": "recentchanges",
        "rcnamespace": "0",  # article namespace only
        "rcprop": "title|ids|sizes|flags|user|comment|timestamp",
        "rclimit": str(limit),
        "format": "json",
    }
    if kind != "all":
        params["rctype"] = kind

    try:
        resp = _get(_wiki(lang), params=params)
        resp.raise_for_status()
        data = resp.json()
    except Exception:
        return "Could not fetch recent changes from Wikipedia."
    if "error" in data:
        return f"Could not fetch recent changes: {data['error'].get('info', 'API error')}"

    changes = data.get("query", {}).get("recentchanges", [])
    if not changes:
        return "No recent changes found on Wikipedia."

    labels = {
        "edit": "✏️ edit",
        "new": "🆕 new article",
        "categorize": "📁 categorize",
        "log": "📜 log",
    }
    base = _wiki(lang).replace("/w/api.php", "")
    out = f"**Recent changes on {lang}.wikipedia.org**\n\n"
    for c in changes:
        ctype = c.get("type", "edit")
        label = labels.get(ctype, ctype)
        title = c.get("title", "?")
        link = f"[{title}]({base}/wiki/{_slug(title)})"
        delta = c.get("newlen", 0) - c.get("oldlen", 0)
        size = f"{delta:+d} bytes"
        user = c.get("user", "?")
        flags = []
        if c.get("bot"):
            flags.append("bot")
        if c.get("minor"):
            flags.append("minor")
        ts = c.get("timestamp", "").replace("T", " ").rstrip("Z") + " UTC"
        comment = (c.get("comment") or "").strip()
        flags_txt = f" ({', '.join(flags)})" if flags else ""
        line = f"- {label} {link} — {size} by **{user}**{flags_txt} — {ts}"
        if comment:
            short = comment if len(comment) <= 120 else comment[:117] + "…"
            line += f'\n  _"{short}"_'
        revid, old_revid = c.get("revid"), c.get("old_revid")
        if revid and old_revid:
            line += f"\n  ([diff]({base}/w/index.php?diff={revid}&oldid={old_revid}))"
        out += line + "\n"
    return out


def category_members(category: str, limit: int = 20, lang: str = "en") -> str:
    """List Wikipedia articles filed under a category.

    Returns the articles in a Wikipedia category — the reverse direction
    of `categories` (which lists an article's categories). Each entry
    includes a one-to-two sentence extract plus a thumbnail URL when one
    exists, so the result is browsable at a glance.

    Useful for taxonomy-based discovery: given "Machine learning
    researchers" (found via `categories`), enumerate who's actually in
    it; browse topics when search misses the long tail; build reading
    lists. Filters to main-namespace articles so subcategories and files
    don't pollute the result. The "Category:" prefix is optional.
    """
    try:
        limit = max(1, min(int(limit), 50))
    except (TypeError, ValueError):
        limit = 20
    cat = (category or "").strip()
    if not cat:
        return "Please provide a category name."
    if not cat.lower().startswith("category:"):
        cat = f"Category:{cat}"
    params = {
        "action": "query",
        "generator": "categorymembers",
        "gcmtitle": cat,
        "gcmtype": "page",
        "gcmsort": "sortkey",
        "gcmlimit": limit,
        "prop": "extracts|pageimages",
        "exintro": 1,
        "explaintext": 1,
        "exsentences": 2,
        "pithumbsize": 200,
        "format": "json",
        "origin": "*",
    }
    resp = _get(_wiki(lang), params=params)
    resp.raise_for_status()
    data = resp.json()
    pages = data.get("query", {}).get("pages", {})
    if not pages:
        return (
            f"No articles found in category '{category}' on {lang}.wikipedia.org — "
            "the category may not exist or may be empty."
        )

    members = sorted(pages.values(), key=lambda p: p.get("title", ""))
    display = cat.replace("Category:", "", 1)
    out = f"**Articles in category \"{display}\":**\n\n"
    for p in members:
        title = p.get("title", "")
        extract = (p.get("extract") or "").strip().replace("\n", " ")
        thumb = ((p.get("thumbnail") or {}).get("source", "") or "").split("?")[0]
        line = f"- **{title}**"
        if extract:
            line += f" — {extract}"
        if thumb:
            line += f"\n  ![thumbnail]({thumb})"
        out += line + "\n"
    out += (
        f"\n[View category]"
        f"(https://{lang}.wikipedia.org/wiki/{_slug(cat)})"
    )
    return out


# Max infobox fields rendered, and max chars per value — keeps huge
# infoboxes (city articles can have 60+ fields) from flooding the model.
INFOBOX_MAX_FIELDS = 50
INFOBOX_MAX_VALUE_LEN = 400


def infobox(title: str, lang: str = "en") -> str:
    """Extract the structured fact box (infobox) from a Wikipedia article.

    Returns the article's infobox as a markdown field/value table: the
    structured facts editors curate at the top-right of the page — dates,
    people, places, statistics, founders, CEOs, populations, capitals.
    This is the fastest path to a concrete fact ("who founded X?", "what's
    the population of Y?") without wading through article prose.

    Uses the read-only parse API to fetch raw wikitext, extracts the first
    {{Infobox ...}} template with balanced-brace matching, and renders each
    |field = value| pair as plain text (wikilinks become plain text,
    citations and HTML are stripped, nested templates are flattened to
    their positional values). Fields are capped at 50 and values at 400
    characters. Reports clearly when the article has no infobox.

    Pairs with `summary` (prose gist) and `article_extract` (full text):
    use `infobox` when you want facts, the others when you want narrative.
    """
    title = (title or "").strip()
    if not title:
        return "Please provide an article title."
    lang = lang if lang in SUPPORTED_LANGS else "en"
    params = {
        "action": "parse",
        "page": title,
        "prop": "wikitext",
        "redirects": 1,
        "format": "json",
        "formatversion": "2",
    }
    try:
        resp = _get(_wiki(lang), params=params)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        return f"Could not fetch infobox for '{title}': {e}"
    if "error" in data:
        return (
            f"No article found for '{title}' on {lang}.wikipedia.org — "
            "check the title with `search` first."
        )
    parsed = data.get("parse", {})
    canon = parsed.get("title", title)
    boxes = _find_infoboxes(parsed.get("wikitext", ""))
    if not boxes:
        return (
            f"No infobox found on '{canon}' ({lang}.wikipedia.org). "
            "Not every article has one — try `summary` or `article_extract` "
            "for this topic instead."
        )
    name, body = boxes[0]
    fields = []
    for part in _split_top_level(body)[1:]:  # [0] is the template name
        if "=" not in part:
            continue
        key, _, value = part.partition("=")
        key = key.strip()
        value = _clean_infobox_value(value)
        if key and value and not any(f[0] == key for f in fields):
            fields.append((key, value))
    if not fields:
        return f"The infobox on '{canon}' has no readable fields."

    out = f"## {canon} — infobox (`{name}`)\n\n"
    if len(boxes) > 1:
        out += f"_{len(boxes)} infoboxes found; showing the first._\n\n"
    out += "| Field | Value |\n|---|---|\n"
    for key, value in fields[:INFOBOX_MAX_FIELDS]:
        if len(value) > INFOBOX_MAX_VALUE_LEN:
            value = value[:INFOBOX_MAX_VALUE_LEN].rstrip() + "…"
        key = key.replace("|", "\\|")
        value = value.replace("\n", " ").replace("|", "\\|")
        out += f"| {key} | {value} |\n"
    if len(fields) > INFOBOX_MAX_FIELDS:
        out += f"\n_…and {len(fields) - INFOBOX_MAX_FIELDS} more fields._\n"
    out += f"\n[View article](https://{lang}.wikipedia.org/wiki/{_slug(canon)})"
    return out


# ---------------------------------------------------------------------------
# Article quality — Wikipedia's own quality assessments (WikiProject grades).
# ---------------------------------------------------------------------------
# Quality ladder. FA/FL = featured (Wikipedia's best), A = near-featured,
# GA = good article, B/C = developed, Start = basic, Stub = minimal.
_QUALITY_RANK = {
    "FA": 7, "FL": 7,  # featured article / featured list
    "A": 6,
    "GA": 5,  # good article
    "B": 4,
    "C": 3,
    "Start": 2,
    "Stub": 1,
}
_QUALITY_LEGEND = "FA/FL (featured) > A > GA (good) > B > C > Start > Stub"


def article_quality(title: str, lang: str = "en") -> str:
    """Get Wikipedia's quality assessments for an article.

    Reports the WikiProject quality grades (FA, GA, B, C, Start, Stub) and
    importance ratings assigned to an article — the encyclopedia's own
    trust/quality signal. Useful before relying on an article: a GA/FA has
    passed formal review, a Stub is a skeleton. Aggregates an overall class
    (the best grade any project assigned) plus the per-project breakdown.
    Uses the read-only pageassessments action API. Note: assessment is only
    enabled on some language editions (e.g. en); others report no data.
    """
    params = {
        "action": "query",
        "prop": "pageassessments",
        "titles": title,
        "format": "json",
        "origin": "*",
    }
    assessments: dict = {}
    canon = title
    for _ in range(5):  # follow continuation; big articles span many projects
        resp = _get(_wiki(lang), params=params)
        if resp.status_code == 404:
            return f"Article '{title}' not found on Wikipedia."
        resp.raise_for_status()
        data = resp.json()
        pages = data.get("query", {}).get("pages", {})
        if not pages:
            break
        page = next(iter(pages.values()))
        if page.get("missing") is not None:
            return f"Article '{title}' not found on Wikipedia."
        canon = page.get("title", title)
        assessments.update(page.get("pageassessments", {}) or {})
        cont = data.get("continue", {})
        if "pacontinue" not in cont:
            break
        params["pacontinue"] = cont["pacontinue"]
    if not assessments:
        return (
            f"No quality assessments recorded for '{canon}' on "
            f"{lang}.wikipedia.org. (Article assessment isn't enabled on every "
            f"language edition — try `lang='en'`.)"
        )

    rows = []
    for project in sorted(assessments):
        a = assessments[project] or {}
        cls = (a.get("class") or "Unassessed").strip()
        imp = (a.get("importance") or "").strip() or "—"
        rows.append((project, cls, imp))
    overall = max(rows, key=lambda r: _QUALITY_RANK.get(r[1], -1))[1]

    out = f"**Quality assessments for \"{canon}\":**\n\n"
    out += f"Overall class: **{overall}**\n"
    out += f"_{_QUALITY_LEGEND}_\n\n"
    out += "| WikiProject | Class | Importance |\n|---|---|---|\n"
    for project, cls, imp in rows:
        out += f"| {project} | {cls} | {imp} |\n"
    out += f"\n[View article](https://{lang}.wikipedia.org/wiki/{_slug(canon)})"
    return out


def related_articles(title: str, limit: int = 5, lang: str = "en") -> str:
    """Find Wikipedia articles semantically similar to a given article.

    Returns the articles Wikipedia's own search engine judges most similar
    to the given title, using MoreLikeThis scoring over article text and
    link structure — a discovery tool for "what should I read next".
    Unlike `links` (raw outgoing links on the page) or `categories`
    (shared topic buckets), this is a similarity ranking: given
    "Velociraptor", expect dromaeosaurids, feathered dinosaurs, and
    "Deinonychus" rather than every linked term. Each result shows the
    article's short description and a thumbnail. The source article
    itself is excluded from the results.
    """
    try:
        limit = max(1, min(int(limit), 20))
    except (TypeError, ValueError):
        limit = 5
    params = {
        "action": "query",
        "generator": "search",
        "gsrsearch": f"morelike:{title}",
        "gsrlimit": limit + 1,  # +1 so dropping the source article keeps `limit`
        "gsrnamespace": 0,
        "prop": "pageimages|description",
        "pithumbsize": 200,
        "format": "json",
        "formatversion": "2",
        "origin": "*",
    }
    resp = _get(_wiki(lang), params=params)
    resp.raise_for_status()
    data = resp.json()
    pages = data.get("query", {}).get("pages", [])

    def _norm(t: str) -> str:
        return t.replace("_", " ").strip().lower()

    results = [p for p in pages if _norm(p.get("title", "")) != _norm(title)][:limit]
    if not results:
        return f"No related articles found for '{title}'."

    out = f'**Articles related to "{title}":**\n\n'
    for i, p in enumerate(results, 1):
        name = p.get("title", "").strip()
        desc = (p.get("description") or "").strip()
        line = f"{i}. **{name}**"
        if desc:
            line += f" — {desc}"
        out += line + "\n"
        thumb = (p.get("thumbnail") or {}).get("source")
        if thumb:
            out += f"   ![thumbnail]({thumb})\n"
    out += (
        f"\n[View article]"
        f"(https://{lang}.wikipedia.org/wiki/{_slug(title)})"
    )
    return out


def contributors(title: str, limit: int = 10, lang: str = "en") -> str:
    """Who writes and maintains an article — most active recent editors.

    Tallies the article's recent edit history (up to 500 revisions, read-only
    action API) into a ranked contributor table: top named editors by edit
    count, each with their share of the sampled edits and a link to their
    user page, plus the anonymous (IP) edit share. A provenance companion to
    `article_quality` (what grade the article earned) and `revisions` (the
    raw edit log): an article tended by a handful of veteran caretakers
    reads differently from one mostly touched by drive-by IP edits, and the
    top names are the people to credit — or to check for conflicts of
    interest. Follows redirects, so nicknames and old titles resolve.
    """
    try:
        limit = max(1, min(int(limit), 20))
    except (TypeError, ValueError):
        limit = 10
    params = {
        "action": "query",
        "prop": "revisions",
        "titles": title,
        "rvprop": "user|timestamp",
        "rvlimit": 500,
        "redirects": 1,
        "format": "json",
        "origin": "*",
    }
    resp = _get(_wiki(lang), params=params)
    if resp.status_code == 404:
        return f"Article '{title}' not found on Wikipedia."
    resp.raise_for_status()
    data = resp.json()
    pages = data.get("query", {}).get("pages", {})
    if not pages:
        return f"No revisions found for '{title}'."

    page = next(iter(pages.values()))
    if page.get("missing") is not None:
        return f"Article '{title}' not found on Wikipedia."
    revs = page.get("revisions", [])
    if not revs:
        return f"No revisions found for '{page.get('title', title)}'."

    page_title = page.get("title", title)
    named: dict = {}
    anon = 0
    for rev in revs:
        if "anon" in rev:
            anon += 1
        else:
            user = rev.get("user", "?")
            named[user] = named.get(user, 0) + 1
    total = len(revs)
    newest = (revs[0].get("timestamp") or "?")[:10]
    oldest = (revs[-1].get("timestamp") or "?")[:10]

    out = (
        f'**Top contributors to "{page_title}"** '
        f"({total} most recent edits sampled, {oldest} – {newest}):\n\n"
    )
    ranked = sorted(named.items(), key=lambda kv: kv[1], reverse=True)[:limit]
    for i, (user, count) in enumerate(ranked, 1):
        share = round(100 * count / total)
        user_url = f"https://{lang}.wikipedia.org/wiki/User:{_url_quote(_slug(user), safe='')}"
        out += f"{i}. **{user}** — {count} edits ({share}%) ([user page]({user_url}))\n"
    if anon:
        share = round(100 * anon / total)
        out += f"\nAnonymous (IP) editors: {anon} edits ({share}%)\n"
    return out


def references(title: str, limit: int = 20, lang: str = "en") -> str:
    """Show the sources an article cites — its bibliography.

    Returns the article's numbered reference list (what readers see under
    "References" / "Sources" at the bottom of the page): each citation's
    text plus the off-wiki URLs it points to (DOI, publisher, archive,
    and other primary-source links). This is the verification companion
    to `external_links`: `external_links` dumps EVERY off-wiki link on
    the page (templates, navboxes, see-also sections), while `references`
    returns only the sources the article actually cites — the bibliography
    you'd hand to a fact-checker. Useful for source verification (does the
    claim trace to a real paper?), citation audits, bibliography building,
    and primary-source discovery. Pairs naturally with `article_quality`
    (the trust signal) and `contributors` (who wrote it) for a full
    "can I rely on this article?" audit.

    Reads the rendered references list (`<ol class="references">`) from
    the MediaWiki parse API — read-only GET, no new dependencies.
    Follows redirects, so nicknames and old titles resolve. `limit`
    clamps the number of citations returned (default 20, max 50);
    well-sourced articles can cite hundreds of sources.
    """
    try:
        limit = max(1, min(int(limit), 50))
    except (TypeError, ValueError):
        limit = 20
    params = {
        "action": "parse",
        "page": title,
        "prop": "text",
        "redirects": 1,
        "format": "json",
        "formatversion": "2",
        "origin": "*",
    }
    resp = _get(_wiki(lang), params=params)
    if resp.status_code == 404:
        return f"Article '{title}' not found on Wikipedia."
    resp.raise_for_status()
    data = resp.json()

    # MediaWiki parse API returns 200 OK with an `error` block for
    # missing titles — handle it like a 404.
    if "error" in data:
        return f"Article '{title}' not found on Wikipedia."
    parsed = data.get("parse", {})
    page_title = parsed.get("title", title)
    html_text = parsed.get("text", "")

    items = []
    for block in re.findall(r'<ol class="references">(.*?)</ol>', html_text, re.S):
        items.extend(re.findall(r"<li[^>]*>(.*?)</li>", block, re.S))
    if not items:
        return (
            f"No references found for '{page_title}' on {lang}.wikipedia.org. "
            "Not every article cites sources — try `summary` or "
            "`article_extract` for this topic instead."
        )

    out = f'**References cited by "{page_title}"** ({len(items)} total):\n\n'
    for i, item in enumerate(items[:limit], 1):
        urls = []
        for href in re.findall(r'href="([^"]+)"', item):
            href = href.strip()
            if not href.startswith(("http://", "https://")):
                continue
            host = href.split("/", 3)[2].lower()
            if host.endswith((".wikipedia.org", ".wikimedia.org")):
                continue  # keep it to real off-wiki sources
            url = _url_unquote(href)
            if url not in urls:
                urls.append(url)
        text = re.sub(r"<[^>]+>", " ", item)
        text = unescape(text)
        text = re.sub(r"\s+", " ", text).strip()
        # Strip the citation backlink markers ("^ a b c", or "↑" on some
        # language editions) left behind after the anchor tags are removed.
        text = re.sub(r"^[\^↑]\s*([a-z]\s+)*", "", text)
        if len(text) > 420:
            text = text[:417] + "..."
        out += f"{i}. {text}\n"
        for url in urls[:5]:
            out += f"   - {url}\n"
    out += (
        f"\n[View article]"
        f"(https://{lang}.wikipedia.org/wiki/{_slug(page_title)})"
    )
    return out


# ---------------------------------------------------------------------------
# citation_sources — where does this article's evidence come from?
# ---------------------------------------------------------------------------
# Multi-level public suffixes we collapse when computing a link's
# "registrable domain" (so www.bbc.co.uk and news.bbc.co.uk both count
# as bbc.co.uk). Kept small and hand-curated — enough for Wikipedia's
# most-cited domains without pulling in a public-suffix dependency.
_DOMAIN_SUFFIXES = frozenset({
    "co.uk", "org.uk", "ac.uk", "gov.uk", "me.uk", "ltd.uk", "plc.uk",
    "com.au", "net.au", "org.au", "edu.au", "gov.au",
    "co.nz", "ac.nz", "govt.nz",
    "co.jp", "or.jp", "ac.jp", "go.jp", "ne.jp", "ed.jp",
    "co.kr", "or.kr", "ac.kr", "go.kr", "ne.kr",
    "com.br", "org.br", "gov.br", "edu.br", "net.br",
    "co.in", "org.in", "gov.in", "ac.in", "edu.in",
    "co.za", "org.za", "gov.za", "ac.za", "edu.za",
    "com.cn", "org.cn", "gov.cn", "edu.cn", "net.cn",
    "com.tr", "org.tr", "gov.tr", "edu.tr",
    "co.il", "org.il", "gov.il", "ac.il", "edu.il",
    "com.tw", "org.tw", "gov.tw", "edu.tw",
    "co.th", "or.th", "ac.th", "go.th",
    "com.mx", "org.mx", "gob.mx", "edu.mx",
    "com.ar", "org.ar", "gov.ar", "edu.ar",
    "com.co", "org.co", "gov.co", "edu.co",
    "com.pe", "org.pe", "gob.pe", "edu.pe",
    "com.ve", "org.ve", "gob.ve", "edu.ve",
    "com.ec", "org.ec", "gob.ec", "edu.ec",
    "com.uy", "org.uy", "gub.uy", "edu.uy",
    "com.py", "org.py", "gov.py", "edu.py",
    "com.bo", "org.bo", "gob.bo", "edu.bo",
    "com.cl", "gob.cl", "edu.cl",
    "com.hk", "org.hk", "gov.hk", "edu.hk",
    "com.sg", "org.sg", "gov.sg", "edu.sg",
})


def _registrable_domain(host: str) -> str:
    """Collapse a hostname to its registrable domain.

    Strips a leading www. and well-known second-level suffixes, so
    www.bbc.co.uk -> bbc.co.uk and en.wikipedia.org -> wikipedia.org.
    IP addresses and single-label hosts are returned unchanged.
    """
    host = (host or "").lower().split("@")[-1].split(":")[0].strip().strip(".")
    if host.startswith("www."):
        host = host[4:]
    if not host or re.fullmatch(r"[0-9.]+", host) or "." not in host:
        return host
    labels = host.split(".")
    if len(labels) > 2 and ".".join(labels[-2:]) in _DOMAIN_SUFFIXES:
        return ".".join(labels[-3:])
    return ".".join(labels[-2:])


def citation_sources(title: str, limit: int = 15, lang: str = "en") -> str:
    """Show which publishers an article leans on — its sources by domain.

    Aggregates the article's reference list into a publisher map: every
    off-wiki link cited in the numbered references is grouped by
    registrable domain (so all *.bbc.co.uk citations land under
    bbc.co.uk), then ranked by citation count with each domain's share of
    linked references. Also reports the share of citations with archived
    (Wayback Machine / archive.org) copies and the share pointing at
    DOI-linked scholarly works.

    This is the diversity lens for the "can I rely on this article?"
    audit: `references` shows you the full bibliography, `citation_sources`
    tells you at a glance whether it's balanced (dozens of independent
    publishers) or lopsided (half the evidence from one outlet) — and
    whether the evidence is archived or link-rotting. Pairs with
    `article_quality` (the grade earned), `article_flags` (editorial
    warnings), and `citation_needed` (unsourced claims).

    Reads the rendered references list from the MediaWiki parse API —
    read-only GET, no new dependencies. Follows redirects. `limit`
    clamps the number of domains shown (default 15, max 30).
    """
    title = str(title or "").strip()
    if not title:
        return "An article title is required."
    try:
        limit = max(1, min(int(limit), 30))
    except (TypeError, ValueError):
        limit = 15
    params = {
        "action": "parse",
        "page": title,
        "prop": "text",
        "redirects": 1,
        "format": "json",
        "formatversion": "2",
        "origin": "*",
    }
    resp = _get(_wiki(lang), params=params)
    if resp.status_code == 404:
        return f"Article '{title}' not found on Wikipedia."
    resp.raise_for_status()
    data = resp.json()
    if "error" in data:
        return f"Article '{title}' not found on Wikipedia."
    parsed = data.get("parse", {})
    page_title = parsed.get("title", title)
    html_text = parsed.get("text", "")

    items = []
    for block in re.findall(r'<ol class="references">(.*?)</ol>', html_text, re.S):
        items.extend(re.findall(r"<li[^>]*>(.*?)</li>", block, re.S))
    if not items:
        return (
            f"No references found for '{page_title}' on {lang}.wikipedia.org — "
            "nothing to aggregate. Try `references` to confirm, or `summary` "
            "for the article itself."
        )

    linked = 0          # references containing >=1 off-wiki link
    archived = 0        # references with a Wayback/archive.org link
    doi_refs = 0        # references linking a DOI
    domain_counts = Counter()
    for item in items:
        seen = set()
        has_link = False
        has_archive = False
        has_doi = False
        for href in re.findall(r'href="([^"]+)"', item):
            href = href.strip()
            if not href.startswith(("http://", "https://")):
                continue
            host = href.split("/", 3)[2].lower().split("@")[-1].split(":")[0]
            if host.endswith((".wikipedia.org", ".wikimedia.org")):
                continue  # keep it to real off-wiki sources
            has_link = True
            if host in ("web.archive.org", "archive.org") or host.endswith(
                (".web.archive.org", ".archive.org")
            ):
                has_archive = True
            if host in ("doi.org", "dx.doi.org"):
                has_doi = True
            domain = _registrable_domain(host)
            if domain and domain not in seen:
                seen.add(domain)
                domain_counts[domain] += 1
        if has_link:
            linked += 1
        if has_archive:
            archived += 1
        if has_doi:
            doi_refs += 1

    if not domain_counts:
        return (
            f'"{page_title}" cites {len(items)} references, but none link to '
            "off-wiki sources (they may be bare text citations). Try "
            "`references` to read them."
        )

    total = len(items)
    unique = len(domain_counts)
    ranked = domain_counts.most_common(limit)
    top_domain, top_count = ranked[0]
    top_share = top_count / max(linked, 1)

    if linked < 5:
        verdict = "thin — almost no linked sources to judge from"
    elif top_share >= 0.5:
        verdict = (f"lopsided — {top_domain} alone backs "
                   f"{top_share:.0%} of linked citations")
    elif top_share >= 0.3:
        verdict = (f"top-heavy — {top_domain} backs "
                   f"{top_share:.0%} of linked citations")
    elif unique >= 10:
        verdict = "diverse — evidence spread across many publishers"
    else:
        verdict = "balanced — no single publisher dominates"

    out = (f'**Citation sources for "{page_title}"** — {verdict}\n\n'
           f"{total} references · {linked} with off-wiki links · "
           f"{unique} unique publishers\n\n"
           f"| Source domain | Citations | Share of linked refs |\n"
           f"| --- | ---: | ---: |\n")
    for domain, count in ranked:
        share = count / max(linked, 1)
        out += f"| `{domain}` | {count} | {share:.0%} |\n"
    if unique > limit:
        out += f"\n_+{unique - limit} more publishers beyond the top {limit}._\n"
    out += ("\n"
            f"- **Archived:** {archived}/{linked} linked citations "
            f"({archived / max(linked, 1):.0%}) have a Wayback Machine / "
            "archive.org copy\n"
            f"- **Scholarly (DOI):** {doi_refs}/{linked} linked citations "
            f"({doi_refs / max(linked, 1):.0%}) point at DOI-linked works\n"
            "\n_The diversity lens for the \"can I rely on this article?\" "
            "audit — pair with `references` for the full bibliography, "
            "`article_quality` for the grade, and `article_flags` for "
            "editorial warnings._")
    return out


# article_path — the six-degrees finder: shortest click-path between two articles
# ---------------------------------------------------------------------------

# How many links/backlinks we sample per page per level, and how many pages
# we expand when searching 3-hop paths. Kept bounded: a 3-hop search costs
# at most 2 + _PATH_EXPAND_LIMIT read-only API calls.
_PATH_LINK_LIMIT = 500
_PATH_EXPAND_LIMIT = 25


def _page_link_graph(title: str, lang: str, prop: str) -> tuple:
    """Read one page's link neighbourhood from the read-only action API.

    prop="links" returns the page's outgoing article links; prop="linkshere"
    returns the non-redirect article pages linking *to* it. Main namespace
    only. Follows redirects.

    Returns (canonical_title, [titles]). Raises LookupError when the page
    does not exist.
    """
    titles = []
    cont = None
    canonical = title
    while True:
        params = {
            "action": "query",
            "titles": title,
            "prop": prop,
            "redirects": 1,
            "format": "json",
            "formatversion": 2,
            "origin": "*",
        }
        if prop == "links":
            params.update({"pllimit": _PATH_LINK_LIMIT, "plnamespace": 0})
            if cont:
                params["plcontinue"] = cont
            key, cont_key = "links", "plcontinue"
        else:
            params.update({"lhlimit": _PATH_LINK_LIMIT, "lhnamespace": 0,
                           "lhshow": "!redirect"})
            if cont:
                params["lhcontinue"] = cont
            key, cont_key = "linkshere", "lhcontinue"
        resp = _get(_wiki(lang), params=params)
        resp.raise_for_status()
        data = resp.json()
        if "error" in data:
            raise LookupError(data["error"].get("info", "API error"))
        query = data.get("query", {})
        for redir in query.get("redirects") or []:
            canonical = redir.get("to", canonical)
        pages = query.get("pages", [])
        if not pages or pages[0].get("missing"):
            raise LookupError(
                f"'{title}' was not found on {lang}.wikipedia.org.")
        page = pages[0]
        canonical = page.get("title", canonical)
        for entry in page.get(key, []):
            if entry.get("ns", 0) == 0:
                titles.append(entry["title"])
        cont = (data.get("continue") or {}).get(cont_key)
        if not cont or len(titles) >= _PATH_LINK_LIMIT:
            break
    return canonical, titles[:_PATH_LINK_LIMIT]


def article_path(start: str, target: str, max_hops: int = 2,
                 lang: str = "en") -> str:
    """Find the shortest click-path between two articles — the six-degrees game.

    Given two article titles, searches Wikipedia's link graph for the
    shortest chain of blue links connecting them, e.g.
    Banana → Africa → Anatolia → Trojan War (3 hops).

    The search is bidirectional and bounded, using only read-only action
    API GETs (no new dependencies):
      - 1 hop: `target` is directly linked from `start`
      - 2 hops: intersects `start`'s outgoing links with the pages linking
        *to* `target` — every middle found is a real start → middle →
        target path
      - 3 hops: expands a bounded sample of `start`'s outgoing links and
        looks for one whose own links land on a page linking to `target`

    Follows redirects (so "USA" → "United States" is 0 hops). Only the
    first 500 outgoing links and 500 backlinks per page are scanned, and at
    most 25 pages are expanded for 3-hop searches — the report states
    exactly what was scanned. `max_hops` clamps to 1..3 (default 2).

    The discovery companion to `links` (raw outgoing links) and
    `backlinks` (every page linking in): use it for six-degrees games,
    tracing how topics connect, or finding the surprising middle article
    that bridges two distant subjects.
    """
    start = str(start or "").strip()
    target = str(target or "").strip()
    if not start or not target:
        return "Both `start` and `target` article titles are required."
    try:
        max_hops = max(1, min(int(max_hops), 3))
    except (TypeError, ValueError):
        max_hops = 2

    def _mdlink(title: str) -> str:
        safe = title.replace(" ", "_")
        return f"[{title}](https://{lang}.wikipedia.org/wiki/{safe})"

    try:
        start_c, fwd = _page_link_graph(start, lang, "links")
        target_c, back = _page_link_graph(target, lang, "linkshere")
    except LookupError as exc:
        return f"Couldn't find a path: {exc}"
    except requests.RequestException as exc:
        return f"Couldn't find a path: the Wikipedia request failed ({exc})."

    header = f"## Path: {_mdlink(start_c)} → {_mdlink(target_c)}\n\n"
    footer = (
        f"\n\n_Scanned the first {len(fwd)} outgoing links of "
        f"\"{start_c}\" and the first {len(back)} pages linking to "
        f"\"{target_c}\". Explore the graph manually with `links` (outgoing) "
        f"and `backlinks` (every page linking in)._")

    if start_c == target_c:
        return (f"{header}**0 hops** — \"{start_c}\" and \"{target_c}\" are "
                "the same article (after resolving redirects).")

    if target_c in fwd:
        return (f"{header}**1 hop** — a direct link:\n\n"
                f"{_mdlink(start_c)} → {_mdlink(target_c)}{footer}")

    if max_hops >= 2:
        back_set = set(back)
        middles = [t for t in fwd
                   if t in back_set and t not in (start_c, target_c)]
        if middles:
            shown = middles[:10]
            lines = [f"{i + 1}. {_mdlink(start_c)} → {_mdlink(m)} → "
                     f"{_mdlink(target_c)}"
                     for i, m in enumerate(shown)]
            extra = (f"\n_…and {len(middles) - len(shown)} more._"
                     if len(middles) > len(shown) else "")
            noun = "middle article" if len(middles) == 1 else "middle articles"
            return (f"{header}**2 hops** — {len(middles)} {noun} connect "
                    f"them:\n\n" + "\n".join(lines) + extra + footer)

    if max_hops >= 3:
        back_set = set(back)
        scanned = 0
        for mid in fwd:
            if mid in (start_c, target_c):
                continue
            scanned += 1
            if scanned > _PATH_EXPAND_LIMIT:
                break
            try:
                _, mid_links = _page_link_graph(mid, lang, "links")
            except (LookupError, requests.RequestException):
                continue
            hit = next((y for y in mid_links
                        if y in back_set and y not in (start_c, target_c)),
                       None)
            if hit:
                return (
                    f"{header}**3 hops** — one route through the link graph:\n\n"
                    f"{_mdlink(start_c)} → {_mdlink(mid)} → {_mdlink(hit)} → "
                    f"{_mdlink(target_c)}\n\n"
                    f"_Expanded {scanned} of \"{start_c}\"'s outgoing links "
                    f"to find it._" + footer)

    if max_hops == 1:
        return (f"{header}No direct link from \"{start_c}\" to \"{target_c}\" "
                f"(checked the first {len(fwd)} outgoing links). Raise "
                "`max_hops` to 2 or 3 to search further.")
    return (f"{header}No path within {max_hops} hops from \"{start_c}\" to "
            f"\"{target_c}\". Try broader, better-connected articles, or "
            "check `links` and `backlinks` to explore the graph manually.")


def article_at_date(title: str, date: str, lang: str = "en") -> str:
    """Show what an article said on a given date — the time machine.

    Finds the latest surviving revision of the article at or before the
    end of `date` (YYYY-MM-DD) via the action API's revision listing
    (`rvstart` + `rvdir=older`), then renders that old revision through
    the parse API and returns its lead text — how the article read on
    that day. Follows redirects.

    The report leads with the revision metadata (revision ID, timestamp,
    editor, edit summary) and a permanent link to the exact revision, so
    the reader can verify the snapshot. If the article had no surviving
    revision before the date, the report says so and names the article's
    first surviving revision instead.

    The history companion to `summary` (the article as it reads now),
    `revisions` (the raw edit log), and `revision_diff` (what changed
    between two revisions): use it to see what an article claimed before
    an event, how a biography's lead evolved, or what a page looked like
    years ago. Read-only via the action API — GET only, no new
    dependencies.
    """
    title = str(title or "").strip()
    if not title:
        return "An article `title` is required."
    try:
        day = datetime.strptime(str(date or "").strip(), "%Y-%m-%d").date()
    except (TypeError, ValueError):
        return ("`date` must be a calendar date in YYYY-MM-DD format "
                f"(got {date!r}).")

    def _rev_query(extra: dict) -> dict:
        params = {
            "action": "query",
            "prop": "revisions",
            "titles": title,
            "redirects": 1,
            "rvlimit": 1,
            "rvprop": "ids|timestamp|user|comment",
            "format": "json",
            "origin": "*",
        }
        params.update(extra)
        resp = _get(_wiki(lang), params=params)
        resp.raise_for_status()
        return resp.json()

    try:
        # Latest revision at or before the end of the requested day.
        data = _rev_query({"rvstart": day.isoformat() + "T23:59:59Z",
                           "rvdir": "older"})
    except requests.RequestException as exc:
        return f"Couldn't look up the article's history: the Wikipedia request failed ({exc})."
    pages = data.get("query", {}).get("pages", {})
    page = next(iter(pages.values()), {}) if pages else {}
    if not page or "missing" in page:
        return f"Article '{title}' not found on Wikipedia."
    revs = page.get("revisions") or []
    resolved = page.get("title", title)
    if not revs:
        # Nothing existed yet on that date — name the first surviving
        # revision so the caller knows when the article's history starts.
        try:
            first = _rev_query({"rvdir": "newer"})
            fp = next(iter(first.get("query", {}).get("pages", {}).values()), {})
            fts = (fp.get("revisions") or [{}])[0].get("timestamp", "")
        except requests.RequestException:
            fts = ""
        note = (f" (the article's first surviving revision is from {fts})"
                if fts else "")
        return (f"No surviving revision of '{resolved}' existed before "
                f"{day.isoformat()}{note}.")

    rev = revs[0]
    revid = rev.get("revid")
    ts = rev.get("timestamp", "")
    editor = rev.get("user", "unknown")
    comment = (rev.get("comment") or "").strip() or "(no edit summary)"

    try:
        # TextExtracts supports revids: clean lead-section plain text of the
        # old revision, without the infobox/navbox noise of raw HTML.
        resp = _get(_wiki(lang), params={
            "action": "query",
            "prop": "extracts",
            "revids": revid,
            "explaintext": 1,
            "exintro": 1,
            "format": "json",
            "origin": "*",
        })
        resp.raise_for_status()
        pages = resp.json().get("query", {}).get("pages", {})
        old = next(iter(pages.values()), {}) if pages else {}
    except requests.RequestException as exc:
        return (f"Found the revision ({revid}, {ts}) but couldn't read "
                f"it: the Wikipedia request failed ({exc}).")
    lead = (old.get("extract") or "").strip()
    if not lead:
        return (f"Revision {revid} ({ts}) of '{resolved}' has no readable "
                f"lead text.")

    desktop_url = (f"https://{lang}.wikipedia.org/w/index.php?"
                   f"title={_slug(resolved)}&oldid={revid}")
    return (f"## {resolved} — as it read on {day.isoformat()}\n\n"
            f"_Revision {revid} from {ts}, edited by {editor}._\n"
            f"_Edit summary: {comment}_\n\n"
            f"{lead}\n\n"
            f"[View this exact revision →]({desktop_url})\n\n"
            f"_Compare with the current article via `summary`, or with "
            f"another snapshot via `revision_diff`._")


def revision_diff(title: str, rev_from: int, rev_to: int, limit: int = 100,
                  lang: str = "en") -> str:
    """Compare two revisions of an article and show exactly what changed.

    Returns a plain-text unified diff of the article's wikitext between
    revision rev_from and revision rev_to (get revision IDs from the
    `revisions` tool). Each side of the diff is labelled with its
    timestamp, editor, and edit summary, so the change is self-explanatory.
    This is the edit-auditing companion to `revisions` (which lists the
    log but not the content change): use it to see what a specific edit
    added or removed, review edits before trusting a new paragraph,
    audit what a breaking-news change rewrote, or spot stealth rewrites.

    Fetches both revisions' wikitext in a single read-only action API
    call (GET only, no new dependencies) and diffs locally with stdlib
    difflib, so the output is a familiar +/- unified diff instead of
    Wikipedia's HTML. `limit` clamps the number of diff lines shown
    (default 100, max 500); oversized diffs are truncated with a note.
    The footer links to the equivalent on-wiki side-by-side view.
    """
    try:
        limit = max(1, min(int(limit), 500))
    except (TypeError, ValueError):
        limit = 100
    try:
        rev_from = int(rev_from)
        rev_to = int(rev_to)
    except (TypeError, ValueError):
        return ("Error: rev_from and rev_to must be revision IDs (integers). "
                "Get revision IDs from the `revisions` tool.")
    if rev_from == rev_to:
        return "rev_from and rev_to are the same revision — nothing to diff."
    params = {
        "action": "query",
        "prop": "revisions",
        "revids": f"{rev_from}|{rev_to}",
        "rvprop": "ids|timestamp|user|comment|content",
        "rvslots": "main",
        "format": "json",
        "formatversion": "2",
        "origin": "*",
    }
    resp = _get(_wiki(lang), params=params)
    resp.raise_for_status()
    data = resp.json()

    # Invalid revision IDs come back as a 200 OK with an `error` block.
    if "error" in data:
        return (f"Couldn't fetch revisions {rev_from}/{rev_to}: "
                f"{data['error'].get('info', 'unknown error')}.")
    pages = data.get("query", {}).get("pages", [])
    if not pages:
        return (f"Couldn't fetch revisions {rev_from}/{rev_to}: "
                "no pages returned — check the revision IDs.")
    if len(pages) > 1:
        return ("Error: the two revision IDs belong to different articles — "
                "both revisions must come from the same page.")

    page = pages[0]
    page_title = page.get("title", title)
    revs = {r.get("revid"): r for r in page.get("revisions", [])}
    missing = [r for r in (rev_from, rev_to) if r not in revs]
    if missing:
        return (f"Revision(s) {', '.join(map(str, missing))} not found for "
                f"'{page_title}' — they may not exist, be deleted/suppressed, "
                "or be on another wiki.")

    def _label(revid):
        r = revs[revid]
        ts = (r.get("timestamp") or "?")[:16].replace("T", " ")
        user = r.get("user", "?")
        comment = (r.get("comment") or "").strip() or "(no edit summary)"
        if len(comment) > 160:
            comment = comment[:157] + "..."
        return f"rev {revid} — **{user}** ({ts}): {comment}"

    old = revs[rev_from]["slots"]["main"]["content"].splitlines()
    new = revs[rev_to]["slots"]["main"]["content"].splitlines()
    diff = list(difflib.unified_diff(
        old, new,
        fromfile=f"rev {rev_from}", tofile=f"rev {rev_to}",
        n=3, lineterm="",
    ))
    if not diff:
        return (
            f'**Revision diff for "{page_title}"**\n\n'
            f"From: {_label(rev_from)}\n"
            f"To: {_label(rev_to)}\n\n"
            "No differences — the two revisions have identical content."
        )

    truncated = len(diff) > limit
    out = (
        f'**Revision diff for "{page_title}"** '
        f"(rev {rev_from} → rev {rev_to})\n\n"
        f"From: {_label(rev_from)}\n"
        f"To: {_label(rev_to)}\n\n"
        "```diff\n" + "\n".join(diff[:limit]) + "\n```\n"
    )
    if truncated:
        out += (
            f"\n_Diff truncated at {limit} of {len(diff)} lines — "
            "raise `limit` (max 500) to see more._\n"
        )
    diff_url = (f"https://{lang}.wikipedia.org/w/index.php"
                f"?title={_slug(page_title)}&diff={rev_to}&oldid={rev_from}")
    out += f"\n[View on-wiki side-by-side diff]({diff_url})"
    return out


# ---------------------------------------------------------------------------
# Disambiguation helpers — detect dab pages and extract their option lists.
# ---------------------------------------------------------------------------
_DAB_SKIP_NS = (
    "File", "Image", "Category", "Template", "Help", "Wikipedia", "Portal",
    "Draft", "User", "Talk", "Special", "MediaWiki", "Module", "Wiktionary",
    "Wikiquote", "Wikisource", "Wikibooks", "Wikivoyage", "Wikinews",
    "Wikiversity", "Commons", "Meta",
)
_DAB_LINK_RE = re.compile(r"\[\[([^\]|]+?)(?:\|([^\]]+?))?\]\]")
_DAB_SECTION_RE = re.compile(r"^={2,}\s*(.+?)\s*={2,}\s*$")


def _strip_dab_markup(text: str) -> str:
    """Collapse wikitext markup in a disambiguation entry to plain text."""
    text = re.sub(r"<ref[^>]*>.*?</ref\s*>", "", text, flags=re.S | re.I)
    text = re.sub(r"<ref[^>]*/\s*>", "", text, flags=re.I)
    prev = None
    while prev != text:  # peel nested templates inside-out
        prev = text
        text = re.sub(r"\{\{[^{}]*\}\}", "", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = text.replace("'''", "").replace("''", "")
    text = re.sub(r"\[\[[^\]|]*\|([^\]]+)\]\]", r"\1", text)
    text = re.sub(r"\[\[([^\]]+)\]\]", r"\1", text)
    text = re.sub(r"\s+", " ", text).strip(" -,;:")
    return text


def disambiguation(title: str, limit: int = 30, lang: str = "en") -> str:
    """Resolve a Wikipedia disambiguation page into its candidate articles.

    Detects whether `title` is a disambiguation page (via the pageprops
    marker) and, if so, returns its options — article title plus a one-line
    description — grouped by the page's own sections. This resolves the
    classic agent dead-end where `search`/`summary` land on an ambiguous
    title and return mush: call this, pick the right candidate, then fetch
    it with `summary`/`article_extract`. Main-namespace article links
    only; file/category/template links are filtered out.
    """
    try:
        limit = max(1, min(int(limit), 100))
    except (TypeError, ValueError):
        limit = 30
    api = _wiki(lang)

    # 1. Confirm the title is actually a disambiguation page.
    resp = _get(api, params={
        "action": "query", "prop": "pageprops", "ppprop": "disambiguation",
        "titles": title, "redirects": 1, "format": "json", "origin": "*",
    })
    resp.raise_for_status()
    pages = resp.json().get("query", {}).get("pages", {})
    if not pages:
        return f"Article '{title}' not found on Wikipedia."
    page = next(iter(pages.values()))
    if page.get("missing") is not None:
        return f"Article '{title}' not found on Wikipedia."
    page_title = page.get("title", title)
    if "disambiguation" not in page.get("pageprops", {}):
        return (
            f"\"{page_title}\" is not a disambiguation page on Wikipedia — "
            "it's a regular article. Use `summary` for an overview, or "
            "`search` to find similarly-named articles."
        )

    # 2. Fetch the wikitext and parse its option list.
    resp = _get(api, params={
        "action": "parse", "page": page_title, "prop": "wikitext",
        "format": "json", "origin": "*",
    })
    resp.raise_for_status()
    pdata = resp.json().get("parse", {})
    wikitext = pdata.get("wikitext", {}).get("*", "")
    if not wikitext:
        return f"Could not read the disambiguation page for '{page_title}'."

    sections = []  # (section_name, [(target, display, description)])
    current = ("Top matches", [])
    sections.append(current)
    seen = set()
    total = 0
    truncated = False

    for raw in wikitext.split("\n"):
        line = raw.strip()
        if not line:
            continue
        sm = _DAB_SECTION_RE.match(line)
        if sm:
            name = _strip_dab_markup(sm.group(1))
            if name.lower() not in ("see also",):
                current = (name, [])
                sections.append(current)
            else:  # keep "See also" as its own labeled group
                current = ("See also", [])
                sections.append(current)
            continue
        if not line.startswith(("*", "#")):
            continue
        item = line.lstrip("*#:;").strip()
        lm = _DAB_LINK_RE.search(item)
        if not lm:
            continue  # unlinked prose — not a candidate article
        target = lm.group(1).strip()
        if "#" in target:  # section anchor — link the base article
            target = target.split("#", 1)[0].strip()
        if ":" in target:
            prefix = target.split(":", 1)[0]
            if prefix in _DAB_SKIP_NS:
                continue  # File:/Category:/etc. — not an article
        if not target or target.lower() in seen:
            continue
        seen.add(target.lower())
        display = _strip_dab_markup(lm.group(2) or target)
        desc = _strip_dab_markup(item[lm.end():])
        if total >= limit:
            truncated = True
            continue
        current[1].append((target, display, desc))
        total += 1

    nonempty = [(name, items) for name, items in sections if items]
    if not nonempty:
        return (
            f"\"{page_title}\" is marked as a disambiguation page, but no "
            "candidate articles could be extracted from it."
        )

    out = (f"**\"{page_title}\" is a disambiguation page** — "
           f"{total} option{'s' if total != 1 else ''}:\n")
    for name, items in nonempty:
        out += f"\n**{name}**\n"
        for target, display, desc in items:
            line = f"- **{display}**"
            if desc:
                line += f" — {desc}"
            out += line + "\n"
    if truncated:
        out += (f"\n_List truncated at {limit} options — raise `limit` "
                f"(max 100) to see more._\n")
    out += (f"\n[View disambiguation page]"
            f"(https://{lang}.wikipedia.org/wiki/{_slug(page_title)})")
    return out

def user_contribs(user: str, limit: int = 10, namespace: int = 0,
                  lang: str = "en") -> str:
    """What a Wikipedia editor has been doing — their recent contributions.

    Uses the read-only `list=usercontribs` action API to show the latest
    edits by a named account (or an IP address, e.g. ``user_contribs(user=
    "192.0.2.1")``) — edited pages, timestamps, byte-size deltas, edit
    comments, and flags for new pages, minor edits, and edits that are
    still the current version. The account header includes registration
    date and total edit count (when the account exists).

    The reverse angle of `contributors` (who edits *this article*): this
    shows what *one editor* touches across the encyclopedia. Use it to
    profile a top contributor, audit an anonymous IP's activity, or spot
    single-purpose accounts (e.g. an editor whose only contributions are
    to one company's article — a conflict-of-interest tell). `namespace`
    scopes the search (default 0 = articles; 3 = user talk, etc.).
    Read-only — GET only, no new dependencies.
    """
    user = str(user or "").strip()
    if not user:
        return "Provide a Wikipedia username or IP address."
    try:
        limit = max(1, min(int(limit), 50))
    except (TypeError, ValueError):
        limit = 10
    try:
        namespace = int(namespace)
    except (TypeError, ValueError):
        namespace = 0
    api = _wiki(lang)
    base = api.replace("/w/api.php", "")

    # 1. Account header — registration date and lifetime edit count.
    header = None
    try:
        uresp = _get(api, params={
            "action": "query", "list": "users", "ususers": user,
            "usprop": "editcount|registration", "format": "json", "origin": "*",
        })
        uresp.raise_for_status()
        udata = uresp.json()
        if "error" in udata:
            return f"Could not look up '{user}': {udata['error'].get('info', 'API error')}"
        uentry = (udata.get("query", {}).get("users") or [{}])[0]
        display = uentry.get("name", user)
        if "missing" in uentry:
            header = f"**{display}** — no registered account with this name"
        elif "invalid" in uentry:
            header = f"**{display}** — anonymous editor (no account, IP address)"
        else:
            reg = (uentry.get("registration") or "")[:10] or "unknown"
            count = uentry.get("editcount", "?")
            if isinstance(count, int):
                count = f"{count:,}"
            header = f"**{display}** — registered {reg}, {count} edits total"
    except Exception:
        header = f"**{user}**"

    # 2. The contributions themselves.
    try:
        cresp = _get(api, params={
            "action": "query", "list": "usercontribs", "ucuser": user,
            "uclimit": str(limit),
            "ucprop": "ids|title|timestamp|comment|sizediff|flags",
            "ucnamespace": str(namespace),
            "format": "json", "origin": "*",
        })
        cresp.raise_for_status()
        cdata = cresp.json()
    except Exception:
        return f"{header}\n\nCould not fetch contributions from Wikipedia."
    if "error" in cdata:
        info = cdata["error"].get("info", "API error")
        if "invalid" in str(info).lower():
            return f"'{user}' is not a valid Wikipedia username or IP address."
        return f"{header}\n\nCould not fetch contributions: {info}"

    contribs = cdata.get("query", {}).get("usercontribs", [])
    if not contribs:
        return (f"{header}\n\nNo contributions found in namespace {namespace} — "
                "the account may be new, renamed, or inactive.")

    nss = "articles" if namespace == 0 else f"namespace {namespace}"
    out = f"{header}\n**Latest contributions ({nss})**\n\n"
    for i, c in enumerate(contribs, 1):
        title = c.get("title", "?")
        link = f"[{title}]({base}/wiki/{_slug(title)})"
        ts = (c.get("timestamp") or "").replace("T", " ").rstrip("Z") + " UTC"
        delta = c.get("sizediff")
        size = f" ({delta:+,d} bytes)" if isinstance(delta, (int, float)) else ""
        flags = []
        if c.get("new"):
            flags.append("new page")
        if c.get("top"):
            flags.append("still current")
        if c.get("minor"):
            flags.append("minor")
        flags_txt = f" [{', '.join(flags)}]" if flags else ""
        out += f"{i}. {link} — {ts}{size}{flags_txt}\n"
        comment = (c.get("comment") or "").strip()
        if comment:
            short = comment if len(comment) <= 120 else comment[:117] + "…"
            out += f'   _"{short}"_\n'
        revid, parentid = c.get("revid"), c.get("parentid")
        if revid and parentid:
            out += f"   [diff]({base}/w/index.php?diff={revid}&oldid={parentid})\n"
    return out


# ---------------------------------------------------------------------------
# citation_needed — find unsourced statements ("citation needed" tags)
# ---------------------------------------------------------------------------
_CN_TAG_RE = re.compile(
    r"\{\{\s*(citation needed|cn|fact|verify source|cnf|unreferenced)\s*"
    r"(\|[^}]*)?\}\}",
    re.IGNORECASE,
)
_CN_TMPL_RE = re.compile(r"\{\{[^{}]*\}\}")
_CN_LINK_RE = re.compile(r"\[\[([^\]|]+\|)?([^\]]+)\]\]")


def _clean_cn_context(text: str) -> str:
    """Strip wiki markup from a claim context snippet (best effort)."""
    text = re.sub(r"<ref[^>/]*>.*?</ref>", "", text, flags=re.S | re.I)
    text = re.sub(r"<ref[^>]*/?>", "", text, flags=re.I)
    for _ in range(3):
        text = _CN_TMPL_RE.sub("", text)
    text = re.sub(r"\{\{[^{}]*$", "", text)  # template cut off mid-snippet
    text = re.sub(r"^[^{}]*\}\}", "", text)  # orphaned template close
    text = _CN_LINK_RE.sub(r"\2", text)
    text = text.replace("'''", "").replace("''", "")
    text = re.sub(r"==[^=\n]+==", "", text)  # section headers
    text = re.sub(r"\s+", " ", text).strip(" \n\t.,;:")
    return text


def _cn_claim_sentence(wikitext: str, match: re.Match) -> tuple:
    """Extract the tagged sentence and the tag's date (if any)."""
    params = match.group(2) or ""
    date = ""
    dm = re.search(r"date\s*=\s*([^|}]+)", params, re.I)
    if dm:
        date = dm.group(1).strip()
    # Walk back to the start of the sentence/paragraph, forward to its end.
    start = match.start()
    for boundary in ("\n\n", "\n", ". ", "; ", ": "):
        idx = wikitext.rfind(boundary, 0, start)
        if idx != -1:
            start = idx + len(boundary)
            break
    end = match.end()
    mend = re.search(r"[.!?](?=\s|$)", wikitext[end:])
    if mend:
        end = end + mend.end()
    else:
        end = min(len(wikitext), end + 80)
    return _clean_cn_context(wikitext[start:end]), date


def citation_needed(topic: str = "", article: str = "",
                    limit: int = 10, lang: str = "en") -> str:
    """Find statements Wikipedia has flagged as needing a source.

    Two angles on the same problem. With ``article`` set, it reads that
    article's wikitext (read-only parse API) and extracts every sentence
    carrying a {{citation needed}} (or {{cn}}/{{fact}}) tag — the exact
    claims editors have flagged as unsourced. With ``topic`` (or neither),
    it searches Wikipedia for articles containing "citation needed" tags
    on that topic via the read-only ``insource:`` search, returning each
    article plus the flagged claim's snippet. Use it to find sourcing work
    as an editor, or to spot the shakiest claims in a topic you're
    researching. Tag-name matching is English-Wikipedia-centric
    (other languages rename the template); ``lang`` is accepted for API
    consistency. Read-only — GET only, no new dependencies.
    """
    try:
        limit = max(1, min(int(limit), 25))
    except (TypeError, ValueError):
        limit = 10
    api = _wiki(lang)
    base = api.replace("/w/api.php", "")

    # --- Angle 1: a single article — extract its tagged claims precisely.
    article = str(article or "").strip()
    if article:
        try:
            resp = _get(api, params={
                "action": "parse", "page": article, "prop": "wikitext",
                "redirects": "1", "format": "json", "origin": "*",
            })
            resp.raise_for_status()
            data = resp.json()
        except Exception:
            return f"Could not fetch '{article}' from Wikipedia."
        if "error" in data:
            return (f"Could not scan '{article}': "
                    f"{data['error'].get('info', 'API error')}")
        page = data.get("parse", {})
        title = page.get("title", article)
        wt = (page.get("wikitext") or {}).get("*", "")
        matches = list(_CN_TAG_RE.finditer(wt))
        if not matches:
            return (f"**{title}** — no \"citation needed\" tags found. "
                    "Every claim currently carries a source (or nobody has "
                    "challenged one yet).")
        link = f"[{title}]({base}/wiki/{_slug(title)})"
        plural = "claim" if len(matches) == 1 else "claims"
        out = f"{link} — **{len(matches)} unsourced {plural}**\n\n"
        for i, m in enumerate(matches[:limit], 1):
            claim, date = _cn_claim_sentence(wt, m)
            claim = claim if len(claim) <= 280 else claim[:277] + "\u2026"
            dated = f" (tagged {date})" if date else ""
            out += f'{i}. _"{claim}"_{dated}\n'
        if len(matches) > limit:
            out += f"\n_Showing {limit} of {len(matches)} tagged claims._\n"
        return out

    # --- Angle 2: topic (or broad) search for tagged articles.
    topic = str(topic or "").strip()
    srsearch = 'insource:"citation needed"'
    if topic:
        srsearch += f" {topic}"
    try:
        resp = _get(api, params={
            "action": "query", "list": "search", "srsearch": srsearch,
            "srnamespace": "0", "srlimit": str(limit),
            "srprop": "snippet", "format": "json", "origin": "*",
        })
        resp.raise_for_status()
        data = resp.json()
    except Exception:
        return "Could not search Wikipedia for unsourced claims."
    if "error" in data:
        return f"Could not search: {data['error'].get('info', 'API error')}"
    results = (data.get("query") or {}).get("search", [])
    if not results:
        hint = f' on "{topic}"' if topic else ""
        return (f'No articles with "citation needed" tags found{hint} — try a '
                "broader topic, or drop the topic for a Wikipedia-wide sample.")
    scope = f' on "{topic}"' if topic else " across Wikipedia"
    out = (f"**Unsourced claims{scope}** — articles flagged with "
           "citation-needed tags\n\n")
    for i, r in enumerate(results, 1):
        title = r.get("title", "?")
        link = f"[{title}]({base}/wiki/{_slug(title)})"
        snippet = re.sub(r"<[^>]+>", "", r.get("snippet") or "")
        snippet = _clean_cn_context(unescape(re.sub(r"\s+", " ", snippet)))
        snippet = snippet if len(snippet) <= 280 else snippet[:277] + "…"
        snippet = snippet if len(snippet) <= 280 else snippet[:277] + "\u2026"
        out += f"{i}. {link}\n"
        if snippet:
            out += f'   _"{snippet}"_\n'
    return out


# ---------------------------------------------------------------------------
# talk — active discussion threads on an article's talk page
# ---------------------------------------------------------------------------
_TALK_SIG_RE = re.compile(r"(\d{1,2}:\d{2}, \d{1,2} \w+ \d{4}) \(UTC\)")
_TALK_SECTION_RE = re.compile(r"(?m)^==\s*(.+?)\s*==\s*$")
# Automated maintenance notices (redirect/deletion discussions) — not real threads
_TALK_NOISE_RES = (
    re.compile(r"<!--\s*Template:(RFDNote|Rfd|Afd|Cfd|Prod)", re.I),
    re.compile(r"\{\{\s*subst\s*:\s*(Rfd notice|Afd|Cfd|Prod)", re.I),
    re.compile(
        r"listed at \[\[Wikipedia:(Redirects for discussion|Articles for deletion"
        r"|Categories for discussion)",
        re.I,
    ),
)
# Closed-thread banners whose inner text (incl. the closing admin's signature)
# is not part of the discussion — strip before extracting timestamps.
_TALK_STRIP_TEMPLATES = ("archivetop", "archive top", "archivebottom", "archive bottom")


def _strip_talk_banners(body: str) -> str:
    """Remove closed-thread banner templates (archivetop etc.) from a section."""
    out, i, n = [], 0, len(body)
    while i < n:
        j = body.find("{{", i)
        if j == -1:
            out.append(body[i:])
            break
        name, _b, end = _extract_template(body, j)
        if name and name.lower().strip() in _TALK_STRIP_TEMPLATES:
            out.append(body[i:j])
            i = end
        else:
            out.append(body[i:j + 2])
            i = j + 2
    return "".join(out)


def _parse_talk_ts(ts: str):
    """Parse a Wikipedia signature timestamp; None when unparseable."""
    try:
        return datetime.strptime(ts, "%H:%M, %d %B %Y")
    except ValueError:
        return None


def _clean_talk_comment(text: str) -> str:
    """Collapse talk-page wikitext into readable plain text (best effort)."""
    text = re.sub(r"<ref[^>/]*>.*?</ref\s*>", "", text, flags=re.S | re.I)
    text = re.sub(r"<ref[^>]*/\s*>", "", text, flags=re.I)
    prev = None
    while prev != text:  # peel nested templates inside-out
        prev = text
        text = re.sub(r"\{\{[^{}]*\}\}", "", text)
    text = re.sub(r"<[^>]+>", "", text)  # signatures, spans, small tags
    text = text.replace("'''", "").replace("''", "")
    text = re.sub(r"\[(?:https?://[^\s\]]+)\s+([^\]]+)\]", r"\1", text)  # [url label]
    text = re.sub(r"https?://[^\s\]]+", "", text)  # bare urls
    text = re.sub(r"\[\[[^|\]]*\|([^\]]+)\]\]", r"\1", text)
    text = re.sub(r"\[\[([^\]]+)\]\]", r"\1", text)
    lines = [re.sub(r"^[:;*#\s]+", "", ln) for ln in text.splitlines()]
    return re.sub(r"\s+", " ", "\n".join(lines)).strip(" -,;:")


def talk(title: str, limit: int = 5, lang: str = "en") -> str:
    """Show the most recently active discussion threads on an article's talk page.

    The behind-the-scenes view of an article: what Wikipedia editors are
    currently debating, questioning, or proposing about the topic. Returns
    each thread's heading, last-activity timestamp, signed-comment count,
    and an excerpt of the latest comment — the fastest way to find
    controversies, open questions, and editorial disputes. Automated
    maintenance notices (redirect/deletion discussions) are filtered out;
    threads are ranked by recency. The discussion companion to
    `contributors` (who edits) and `article_quality` (how the article is
    graded): check all three for a full "can I rely on this article?" audit.

    Reads the Talk: page wikitext via the read-only MediaWiki API — GET
    only, no new dependencies. `limit` clamps the number of threads
    (default 5, max 15). Talk-page conventions are English-centric; `lang`
    is accepted for API consistency.
    """
    try:
        limit = max(1, min(int(limit), 15))
    except (TypeError, ValueError):
        limit = 5
    params = {
        "action": "query",
        "prop": "revisions",
        "rvprop": "content",
        "rvslots": "main",
        "rvlimit": 1,
        "titles": f"Talk:{title}",
        "redirects": 1,
        "format": "json",
        "formatversion": "2",
    }
    resp = _get(_wiki(lang), params=params)
    resp.raise_for_status()
    data = resp.json()
    pages = data.get("query", {}).get("pages", [])
    if not pages:
        return f"No talk page found for '{title}'."
    page = pages[0]
    if page.get("missing") or page.get("invalid"):
        return (
            f"No talk page for '{title}' yet on {lang}.wikipedia.org — no "
            "editor discussion exists. Check the spelling, or try `summary` "
            "to confirm the article itself exists."
        )
    talk_title = page.get("title", f"Talk:{title}")
    article_title = talk_title.split(":", 1)[1] if ":" in talk_title else talk_title
    revs = page.get("revisions") or []
    wikitext = revs[0].get("slots", {}).get("main", {}).get("content", "") if revs else ""

    parts = _TALK_SECTION_RE.split(wikitext)
    threads = []
    for i in range(1, len(parts), 2):
        heading = _clean_talk_comment(parts[i])[:120]
        body = _strip_talk_banners(parts[i + 1])
        if any(rx.search(body) for rx in _TALK_NOISE_RES):
            continue  # automated redirect/deletion notice, not discussion
        sigs = _TALK_SIG_RE.findall(body)
        if not sigs:
            continue
        parsed = [(d, s) for s in sigs for d in [_parse_talk_ts(s)] if d]
        if not parsed:
            continue
        last_dt, last_str = max(parsed)
        # Latest comment = text between the last two signatures.
        matches = list(_TALK_SIG_RE.finditer(body))
        seg_start = matches[-2].end() if len(matches) > 1 else 0
        excerpt = _clean_talk_comment(body[seg_start:matches[-1].start()])
        if len(excerpt) < 40:  # latest comment too thin — widen the window
            excerpt = _clean_talk_comment(body[max(0, matches[-1].start() - 700):matches[-1].start()])
        if len(excerpt) > 450:
            excerpt = excerpt[:447] + "…"
        threads.append(
            {
                "heading": heading or "(untitled thread)",
                "last": last_dt,
                "last_str": last_str,
                "replies": len(sigs),
                "excerpt": excerpt,
            }
        )
    threads.sort(key=lambda t: t["last"], reverse=True)
    threads = threads[:limit]
    if not threads:
        return (
            f'No signed discussion threads on "Talk:{article_title}" — the talk '
            "page exists but holds no dated editor comments (it may contain "
            "only templates, archive boxes, or bot notices)."
        )
    talk_url = f"https://{lang}.wikipedia.org/wiki/{_url_quote(_slug(talk_title), safe=':/')}"
    out = (
        f'**Talk: "{article_title}"** — {len(threads)} most recently active '
        f"discussion thread(s) ([full talk page]({talk_url}))\n\n"
    )
    for i, t in enumerate(threads, 1):
        out += f"{i}. **{t['heading']}**\n"
        out += f"   Last activity {t['last_str']} (UTC) · {t['replies']} signed comment(s)\n"
        if t["excerpt"]:
            out += f"   _\"{t['excerpt']}\"_\n"
    return out


# ---------------------------------------------------------------------------
# article_flags — maintenance banners editors placed on an article
# ---------------------------------------------------------------------------
# English maintenance template names (lowercased, singular canonical key)
# → (display name, plain-language meaning). Deliberately curated: only real
# editorial banners, so infobox/citation/formatting templates never leak in.
_AF_BANNERS = {
    "original research": ("Original research", "Contains original research — unverified analysis may be mixed in with facts"),
    "or": ("Original research", "Contains original research — unverified analysis may be mixed in with facts"),
    "pov": ("POV", "Neutral point of view is disputed — editors disagree the article presents a balanced view"),
    "npov": ("POV", "Neutral point of view is disputed — editors disagree the article presents a balanced view"),
    "neutrality": ("POV", "Neutral point of view is disputed — editors disagree the article presents a balanced view"),
    "unreferenced": ("Unreferenced", "No sources cited at all"),
    "refimprove": ("More citations needed", "Needs more citations to reliable sources"),
    "more citations needed": ("More citations needed", "Needs more citations to reliable sources"),
    "citations broken": ("Broken citations", "Some citation links are broken"),
    "cleanup": ("Cleanup needed", "Style, wording, or structural problems"),
    "weasel": ("Weasel words", "Vague claims not attributed to any source"),
    "weasel words": ("Weasel words", "Vague claims not attributed to any source"),
    "peacock": ("Peacock terms", "Self-promotional wording"),
    "tone": ("Tone", "Not written in an encyclopedic tone"),
    "advert": ("Advertisement-like", "Reads like an advertisement"),
    "advertisement": ("Advertisement-like", "Reads like an advertisement"),
    "coi": ("Conflict of interest", "A close connection to the subject is suspected"),
    "connected contributor": ("Conflict of interest", "A close connection to the subject is suspected"),
    "autobiography": ("Autobiographical", "May be written by or about the subject themselves"),
    "fringe theories": ("Fringe theories", "Covers fringe theories outside mainstream consensus"),
    "fringe": ("Fringe theories", "Covers fringe theories outside mainstream consensus"),
    "disputed": ("Disputed", "Factual accuracy is disputed"),
    "accuracy": ("Disputed", "Factual accuracy is disputed"),
    "accuracy dispute": ("Disputed", "Factual accuracy is disputed"),
    "contradict": ("Self-contradictory", "Statements in the article conflict with each other"),
    "self-contradictory": ("Self-contradictory", "Statements in the article conflict with each other"),
    "outdated": ("Outdated", "Facts or statements may no longer be current"),
    "update": ("Outdated", "Facts or statements may no longer be current"),
    "current": ("Outdated", "Facts or statements may no longer be current"),
    "out of date": ("Outdated", "Facts or statements may no longer be current"),
    "expand": ("Needs expansion", "Coverage is thin"),
    "notability": ("Notability questioned", "May not meet Wikipedia's inclusion criteria"),
    "orphan": ("Orphan", "Few or no other articles link to it"),
    "lead too long": ("Lead too long", "The lead section is too long"),
    "lead missing": ("Lead missing", "The lead section is missing"),
    "lead too short": ("Lead too short", "The lead section is too short"),
    "unbalanced": ("Unbalanced", "Gives undue weight to some viewpoints"),
    "unbalanced opinion": ("Unbalanced", "Gives undue weight to some viewpoints"),
    "globalize": ("Needs worldwide view", "Needs a worldwide perspective"),
    "worldwide view": ("Needs worldwide view", "Needs a worldwide perspective"),
    "rewrite": ("Needs rewrite", "The article needs to be rewritten"),
    "copy edit": ("Needs copy edit", "Grammar, style, or clarity problems"),
    "technical": ("Too technical", "Too technical for general readers"),
    "too technical": ("Too technical", "Too technical for general readers"),
    "fanpov": ("Fan POV", "Written from a fan's point of view"),
    "in-universe": ("In-universe", "Written from an in-universe (fan) perspective"),
    "recentism": ("Recentism", "Skewed toward recent events"),
    "unreliable sources": ("Unreliable sources", "Cites unreliable sources"),
    "primary sources": ("Primary sources", "Relies too heavily on primary sources"),
    "one source": ("Single source", "Relies on a single source"),
    "third-party": ("Needs independent sources", "Needs independent (third-party) sources"),
    "third party": ("Needs independent sources", "Needs independent (third-party) sources"),
    "self-published": ("Self-published sources", "Cites self-published sources"),
    "hoax": ("Possible hoax", "Authenticity is questioned"),
    "blp sources": ("BLP sourcing", "Biography of a living person has sourcing problems"),
    "blp unsourced": ("BLP sourcing", "Biography of a living person has sourcing problems"),
    "external links": ("External links", "External links may not comply with policy"),
    "overquote": ("Overquoting", "Overuses quotations"),
    "trivia": ("Excessive trivia", "Excessive trivia"),
    "in popular culture": ("Excessive pop culture", "Excessive pop-culture references"),
    "split": ("Split proposed", "A split into multiple articles is proposed"),
    "merge": ("Merge proposed", "A merge with another article is proposed"),
    "merge to": ("Merge proposed", "A merge with another article is proposed"),
    "merge from": ("Merge proposed", "A merge with another article is proposed"),
    "copyvio": ("Possible copyright violation", "Possible copyright violation"),
    "linkrot": ("Link rot", "External links need archiving"),
    "dead end": ("Dead end", "Has no links to other Wikipedia articles"),
    "deadend": ("Dead end", "Has no links to other Wikipedia articles"),
    "more footnotes": ("More footnotes needed", "Needs more inline citations (footnotes)"),
    "no footnotes": ("No footnotes", "Has no inline citations (footnotes)"),
}

_AF_TMPL_RE = re.compile(r"\{\{\s*([A-Za-z][A-Za-z0-9_\-. ]*?)\s*(?=[|}])")
_AF_DATE_RE = re.compile(r"\|\s*date\s*=\s*([^|}]+)")
_AF_SECTION_RE = re.compile(r"(?m)^={2,}\s*(.+?)\s*={2,}\s*$")
_AF_LINK_RE = re.compile(r"\[\[([^\]|]+\|)?([^\]]+)\]\]")


def _af_banner(raw: str) -> tuple:
    """Map a template name to (display, meaning); ('','') if not a banner."""
    name = re.sub(r"\s+", " ", raw.strip().lower())
    if name in _AF_BANNERS:
        return _AF_BANNERS[name]
    # Section-scoped variants: "POV section", "original research section".
    if name.endswith(" section"):
        base = name[: -len(" section")]
        if base in _AF_BANNERS:
            return _AF_BANNERS[base]
    return ("", "")


def _extract_article_flags(wikitext: str) -> list:
    """Scan wikitext for maintenance banners → [(display, date, section)]."""
    headings = [(m.start(), m.group(1).strip().strip("=").strip())
                for m in _AF_SECTION_RE.finditer(wikitext)]
    flags, seen = [], set()
    for m in _AF_TMPL_RE.finditer(wikitext):
        display, _ = _af_banner(m.group(1))
        if not display:
            continue
        section = "article top"
        for hpos, hname in reversed(headings):
            if hpos < m.start():
                section = _AF_LINK_RE.sub(r"\2", hname).strip()
                break
        dm = _AF_DATE_RE.search(wikitext[m.start():m.start() + 300])
        date = dm.group(1).strip() if dm else ""
        key = (display, date, section)
        if key not in seen:
            seen.add(key)
            flags.append((display, date, section))
    return flags


def article_flags(article: str = "", limit: int = 10, lang: str = "en") -> str:
    """Show the maintenance banners editors placed on an article.

    Wikipedia's own warning labels — the {{POV}}, {{Original research}},
    {{Unreferenced}}, {{Cleanup}}, {{Disputed}} ... templates editors stick
    at the top of an article or section when something is wrong with it.
    Reads the article's wikitext via the read-only parse API, matches banner
    templates against a curated English maintenance-template list, and
    returns each flag with its tag date, location (article top or section),
    and a plain-language meaning. The {{Multiple issues}} wrapper is
    unpacked into its individual flags. The trust-signal companion to
    `article_quality` (the grade), `citation_needed` (unsourced claims), and
    `talk` (editor discussion): check it to see exactly what editors think
    is wrong with an article before relying on it. Banner names are
    English-Wikipedia-centric (`lang` accepted for API consistency).
    Read-only — GET only, no new dependencies.
    """
    try:
        limit = max(1, min(int(limit), 25))
    except (TypeError, ValueError):
        limit = 10
    article = str(article or "").strip()
    if not article:
        return "An article title is required."
    api = _wiki(lang)
    base = api.replace("/w/api.php", "")
    try:
        resp = _get(api, params={
            "action": "parse", "page": article, "prop": "wikitext",
            "redirects": "1", "format": "json", "origin": "*",
        })
        resp.raise_for_status()
        data = resp.json()
    except Exception:
        return f"Could not fetch '{article}' from Wikipedia."
    if "error" in data:
        return (f"Could not check '{article}': "
                f"{data['error'].get('info', 'API error')}")
    page = data.get("parse", {})
    title = page.get("title", article)
    wt = (page.get("wikitext") or {}).get("*", "")
    flags = _extract_article_flags(wt)
    link = f"[{title}]({base}/wiki/{_slug(title)})"
    if not flags:
        return (
            f"**{title}** — no editorial flags. Editors haven't placed any "
            "maintenance banners (neutrality, sourcing, accuracy, cleanup) "
            "on this article."
        )
    plural = "flag" if len(flags) == 1 else "flags"
    out = (f"{link} — **{len(flags)} editorial {plural}** (maintenance "
           "banners placed by editors)\n\n")
    meanings = {d: m for d, m in _AF_BANNERS.values()}
    for i, (display, date, section) in enumerate(flags[:limit], 1):
        dated = f" (tagged {date})" if date else ""
        where = "" if section == "article top" else f" — section: {section}"
        out += f"{i}. **{display}**{dated}{where}\n"
        out += f"   _{meanings.get(display, '')}_\n"
    if len(flags) > limit:
        out += f"\n_Showing {limit} of {len(flags)} flags._\n"
    out += (
        "\n_Flags are Wikipedia's own editorial banners. Pair with "
        "`article_quality` (the grade), `citation_needed` (unsourced claims), "
        "and `talk` (editor discussion) for a full \"can I rely on this "
        "article?\" audit._"
    )
    return out


# ---------------------------------------------------------------------------
# article_protection — is this article locked, and for how long?
# ---------------------------------------------------------------------------
_AP_LEVEL_MEANINGS = {
    "autoconfirmed": "autoconfirmed accounts only (at least 4 days old with "
                     "10+ edits) — anonymous and brand-new accounts are blocked",
    "extendedconfirmed": "extended-confirmed accounts only (at least 30 days "
                         "old with 500+ edits)",
    "templateeditor": "template editors and administrators only",
    "sysop": "administrators only",
    "user": "registered users only",
}

_AP_TYPE_LABELS = {
    "edit": "editing",
    "move": "moving/renaming",
    "create": "creating",
    "upload": "uploading files over",
}


def _ap_expiry(expiry):
    """Human-readable expiry for a protection entry."""
    if not expiry or expiry == "infinity":
        return "indefinite"
    try:
        date = expiry.split("T")[0]
        parts = date.split("-")
        if len(parts) == 3:
            return f"until {date}"
    except Exception:
        pass
    return f"until {expiry}"


def article_protection(article: str = "", lang: str = "en") -> str:
    """Is this Wikipedia article locked, who can still touch it, and for how long.

    Reports the page's protection status via the read-only action API
    (prop=info, inprop=protection): which actions are restricted (editing,
    moving/renaming, creating a missing title, uploading), at what level
    (semi-protection, extended-confirmed, administrators-only), and when each
    restriction expires. Cascade-protected pages list the protection source
    instead of repeating every entry. Missing titles are reported too —
    salted titles carry a "create" protection. Follows redirects and names
    the redirect chain. The lockdown companion to the other trust signals:
    `article_quality` (the grade), `article_flags` (editorial warnings),
    `citation_needed` (unsourced claims), and `talk` (editor discussion).
    Read-only — GET only, no new dependencies.
    """
    article = str(article or "").strip()
    if not article:
        return "An article title is required."
    api = _wiki(lang)
    base = api.replace("/w/api.php", "")
    try:
        resp = _get(api, params={
            "action": "query", "prop": "info", "inprop": "protection",
            "titles": article, "redirects": "1", "format": "json",
            "origin": "*",
        })
        resp.raise_for_status()
        data = resp.json()
    except Exception:
        return f"Could not fetch '{article}' from Wikipedia."
    if "error" in data:
        return (f"Could not check '{article}': "
                f"{data['error'].get('info', 'API error')}")
    query = data.get("query", {})
    redirs = query.get("redirects", [])
    page = next(iter(query.get("pages", {}).values()), None)
    if page is None:
        return f"Could not check '{article}': unexpected API response."
    title = page.get("title", article)
    link = f"[{title}]({base}/wiki/{_slug(title)})"
    redirect_note = ""
    if redirs:
        chain = " → ".join(r["from"] for r in redirs) + " → " + redirs[-1]["to"]
        redirect_note = f" (via redirect {chain})"
    protections = page.get("protection", []) or []
    if "missing" in page:
        creates = [p for p in protections if p.get("type") == "create"]
        if not creates:
            return (f"{link} doesn't exist as an article, and its title is "
                    "not protected — anyone could create it.")
        p = creates[0]
        level = _AP_LEVEL_MEANINGS.get(p.get("level", ""),
                                       f"level '{p.get('level', '?')}'")
        return (f"{link} doesn't exist as an article, and its title is "
                f"**protected from creation**: only {level} can create it "
                f"({_ap_expiry(p.get('expiry', ''))}).")
    if not protections:
        return (f"{link} — **no protection**{redirect_note}. Fully open: "
                "anyone, including anonymous editors, can edit it.")
    # Strongest level first per action type; collapse cascade sources.
    order = {"sysop": 4, "templateeditor": 3, "extendedconfirmed": 2,
             "autoconfirmed": 1, "user": 1}
    by_type = {}
    cascades = []
    for p in protections:
        ptype = p.get("type", "")
        if "source" in p:
            cascades.append(p["source"])
            continue
        level = p.get("level", "")
        if ptype not in by_type or order.get(level, 0) > order.get(
                by_type[ptype].get("level", ""), 0):
            by_type[ptype] = p
    lines = []
    for ptype, p in by_type.items():
        label = _AP_TYPE_LABELS.get(ptype, ptype)
        level = p.get("level", "")
        meaning = _AP_LEVEL_MEANINGS.get(level, f"level '{level}'")
        lines.append(f"- **{label.capitalize()}**: {meaning} "
                     f"({_ap_expiry(p.get('expiry', ''))})")
    out = (f"{link} — **protected**{redirect_note} "
           f"({len(lines)} restriction{'s' if len(lines) != 1 else ''})\n\n"
           + "\n".join(lines))
    if cascades:
        uniq = sorted(set(cascades))
        shown = ", ".join(f"`{c}`" for c in uniq[:3])
        more = f" (+{len(uniq) - 3} more)" if len(uniq) > 3 else ""
        out += (f"\n\n_Also cascade-protected via: {shown}{more} — fully "
                "locked pages that include this one._")
    out += (
        "\n\n_Protection levels are Wikipedia's own lockdown status. Pair with "
        "`article_quality` (the grade), `article_flags` (editorial warnings), "
        "`citation_needed` (unsourced claims), and `talk` (editor discussion) "
        "for a full \"can I rely on this article?\" audit._"
    )
    return out


# ---------------------------------------------------------------------------
# article_pulse — vital signs of an article (creation, watchers, edit velocity)
# ---------------------------------------------------------------------------
def _pulse_verdict(edits30: int) -> str:
    """Plain-language activity verdict from the last-30-days edit count."""
    if edits30 >= 30:
        return "buzzing — edited roughly daily or more"
    if edits30 >= 8:
        return "active — edited about weekly"
    if edits30 >= 1:
        return "quiet — occasional edits"
    return "dormant — untouched for 30+ days"


def _days_ago_label(ts: str) -> str:
    """Turn a MediaWiki timestamp into 'today' / '3 days ago' / '~2 years ago'."""
    try:
        dt = datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ").replace(
            tzinfo=timezone.utc
        )
        days = (datetime.now(timezone.utc) - dt).days
    except Exception:
        return ts
    if days <= 0:
        return "today"
    if days == 1:
        return "yesterday"
    if days < 30:
        return f"{days} days ago"
    if days < 365:
        months = days // 30
        return f"~{months} month{'s' if months != 1 else ''} ago"
    years = days // 365
    return f"~{years} year{'s' if years != 1 else ''} ago"


def article_pulse(article: str = "", lang: str = "en") -> str:
    """Vital signs of a Wikipedia article — how alive is this page right now.

    One-screen health check: when the article was created and by whom
    (earliest surviving revision), page length, watcher count, the most
    recent edit (when, who, edit summary), and edit velocity over the last
    30 days (edit count plus number of distinct editors), capped with a
    plain-language activity verdict (buzzing / active / quiet / dormant).
    Follows redirects. The liveliness companion to the other trust signals:
    `article_quality` (the grade earned), `contributors` (who edits it),
    `revisions` (the raw edit log), and `pageviews` (the traffic).
    Read-only via the action API (prop=info + prop=revisions) — GET only,
    no new dependencies.
    """
    article = str(article or "").strip()
    if not article:
        return "An article title is required."
    api = _wiki(lang)
    base = api.replace("/w/api.php", "")
    now = datetime.now(timezone.utc)
    window_start = (now - timedelta(days=30)).strftime("%Y-%m-%dT%H:%M:%SZ")
    window_now = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    try:
        # Call 1: page info (length, watchers, url) + earliest surviving
        # revision (creation date and creator).
        r1 = _get(api, params={
            "action": "query", "prop": "info|revisions",
            "inprop": "url|watchers", "rvprop": "ids|timestamp|user",
            "rvlimit": "1", "rvdir": "newer",
            "titles": article, "redirects": "1", "format": "json",
            "origin": "*",
        })
        r1.raise_for_status()
        d1 = r1.json()
        # Call 2: revisions inside the last 30 days (up to 500).
        r2 = _get(api, params={
            "action": "query", "prop": "revisions",
            "rvprop": "ids|timestamp|user|comment", "rvlimit": "500",
            "rvdir": "older", "rvstart": window_now, "rvend": window_start,
            "titles": article, "redirects": "1", "format": "json",
            "origin": "*",
        })
        r2.raise_for_status()
        d2 = r2.json()
    except Exception:
        return f"Could not fetch '{article}' from Wikipedia."
    for data in (d1, d2):
        if "error" in data:
            return (f"Could not check '{article}': "
                    f"{data['error'].get('info', 'API error')}")
    q1, q2 = d1.get("query", {}), d2.get("query", {})
    redirs = q1.get("redirects", [])
    page1 = next(iter(q1.get("pages", {}).values()), None)
    page2 = next(iter(q2.get("pages", {}).values()), None)
    if page1 is None or page2 is None:
        return f"Could not check '{article}': unexpected API response."
    title = page1.get("title", article)
    link = f"[{title}]({base}/wiki/{_slug(title)})"
    redirect_note = ""
    if redirs:
        chain = " → ".join(r["from"] for r in redirs) + " → " + redirs[-1]["to"]
        redirect_note = f" (via redirect {chain})"
    if "missing" in page1:
        return (f"{link} doesn't exist as an article — no pulse to take."
                f"{redirect_note}")
    length = page1.get("length")
    length_str = f"{length:,} bytes" if isinstance(length, int) else "unknown"
    watchers = page1.get("watchers")
    watchers_str = (f"{watchers:,}" if isinstance(watchers, int)
                    else "not reported by this edition")
    first = (page1.get("revisions") or [None])[0]
    if first:
        created = first.get("timestamp", "")[:10]
        creator = first.get("user", "unknown")
        created_str = (f"{created} ({_days_ago_label(first['timestamp'])}) "
                       f"by {creator}")
    else:
        created_str = "unknown"
    recent = page2.get("revisions") or []
    capped = len(recent) == 500
    edits30 = len(recent)
    edits30_str = f"{edits30}+" if capped else str(edits30)
    editors = sorted({r.get("user", "?") for r in recent})
    if recent:
        latest = recent[0]
        lts = latest.get("timestamp", "")
        last_str = (f"{lts[:10]} ({_days_ago_label(lts)}) by "
                    f"{latest.get('user', 'unknown')}")
        comment = (latest.get("comment") or "").strip()
        if comment:
            comment = comment if len(comment) <= 120 else comment[:117] + "..."
            last_str += f' — "{comment}"'
    else:
        last_str = "no edits in the last 30 days"
    verdict = _pulse_verdict(edits30)
    out = (f"{link} — pulse: **{verdict}**{redirect_note}\n\n"
           f"- **Created:** {created_str} _(earliest surviving revision; "
           "page moves or deletions can reset this)_\n"
           f"- **Length:** {length_str}\n"
           f"- **Watchers:** {watchers_str}\n"
           f"- **Last edited:** {last_str}\n"
           f"- **Edits (last 30 days):** {edits30_str} "
           f"by {len(editors)} editor{'s' if len(editors) != 1 else ''}")
    if editors:
        shown = ", ".join(f"`{e}`" for e in editors[:5])
        more = f" (+{len(editors) - 5} more)" if len(editors) > 5 else ""
        out += f"\n- **Recent editors:** {shown}{more}"
    out += ("\n\n_The liveliness companion to `article_quality` (the grade "
            "earned), `contributors` (who edits it), `revisions` (the raw "
            "edit log), and `pageviews` (the traffic)._")
    return out


# ---------------------------------------------------------------------------
# Tool registry — schemas declared in one place for clarity
# ---------------------------------------------------------------------------
TOOLS = [
    {
        "name": "search",
        "description": (
            "Search Wikipedia for articles matching a query — the entry point when you don't know "
            "the exact article title. Returns a ranked, numbered list of matching articles, each with "
            "a short text snippet and its Wikipedia URL (use `limit` for up to 20 results). Once you've "
            "identified the right title, pass it to `summary` for the gist, `article_extract` for the "
            "full text, or `links` to explore outward. Reports 'No results found' for empty queries "
            "instead of erroring."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"},
                "limit": {
                    "type": "integer",
                    "description": "Max results (default 5, max 20)",
                    "default": 5,
                },
                "lang": {
                    "type": "string",
                    "description": "Wikipedia language code (default 'en')",
                    "default": "en",
                    "enum": list(SUPPORTED_LANGS),
                },
            },
            "required": ["query"],
        },
    },
    {
        "name": "summary",
        "description": (
            "Get a concise summary of a Wikipedia article by exact title, plus its lead thumbnail image "
            "when one exists. The fastest way to get the gist of a known topic — e.g. 'Tyrannosaurus' or "
            "'Albert_Einstein'. If you don't know the exact title, use `search` first to find it. For the "
            "full article text use `article_extract`; for just the section outline use `article_sections`."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Article title (e.g. 'Tyrannosaurus' or 'Albert_Einstein')",
                },
                "lang": {
                    "type": "string",
                    "description": "Wikipedia language code (default 'en')",
                    "default": "en",
                    "enum": list(SUPPORTED_LANGS),
                },
            },
            "required": ["title"],
        },
    },
    {
        "name": "random",
        "description": (
            "Fetch a summary of a random Wikipedia article — serendipitous discovery across the entire "
            "encyclopedia. Returns the same title + summary + thumbnail shape as `summary`, but for a "
            "surprise topic. Ideal for exploration, icebreakers, trivia, and content inspiration when "
            "there's no specific subject in mind; supports other languages via `lang`."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "lang": {
                    "type": "string",
                    "description": "Wikipedia language code (default 'en')",
                    "default": "en",
                    "enum": list(SUPPORTED_LANGS),
                },
            },
        },
    },
    {
        "name": "simple_summary",
        "description": (
            "Get the Simple English Wikipedia version of a topic by title — a plain-language "
            "explanation written in short sentences with common words, in the same title + summary + "
            "thumbnail shape as `summary`. Use when you want \"explain it simply\" (kids, ESL readers, "
            "quick intuition) or the full article is too dense. Reports clearly when no Simple English "
            "article exists for the topic, pointing you at `summary` for the full version."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Article title (e.g. 'Photosynthesis' or 'Quantum_mechanics')",
                },
            },
            "required": ["title"],
        },
    },
    {
        "name": "did_you_know",
        "description": "Get a random 'Did You Know' style fact from Wikipedia — great for hooks and general trivia",
        "inputSchema": {
            "type": "object",
            "properties": {
                "lang": {
                    "type": "string",
                    "description": "Wikipedia language code (default 'en')",
                    "default": "en",
                    "enum": list(SUPPORTED_LANGS),
                },
            },
        },
    },
    {
        "name": "dino_fact",
        "description": (
            "Get a 'Did You Know' style fact about dinosaurs or prehistoric life. "
            "Pass a specific species ('Tyrannosaurus', 'Spinosaurus') for a targeted fact, "
            "or call with no arguments for a random dino. Falls back to a random dino "
            "if the requested species isn't found on Wikipedia."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "species": {
                    "type": "string",
                    "description": "Specific dinosaur name (e.g. 'Tyrannosaurus'). Empty for random.",
                    "default": "",
                },
                "lang": {
                    "type": "string",
                    "description": "Wikipedia language code (default 'en')",
                    "default": "en",
                    "enum": list(SUPPORTED_LANGS),
                },
            },
        },
    },
    {
        "name": "article_extract",
        "description": (
            "Get a Wikipedia article's full plain-text extract by title — "
            "much longer than `summary` (typically several paragraphs). "
            "Returns plain text (no HTML). Complements `summary`: use it "
            "when the summary is too brief and you want a fuller reading."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Article title (e.g. 'Tyrannosaurus' or 'Albert_Einstein')",
                },
                "lang": {
                    "type": "string",
                    "description": "Wikipedia language code (default 'en')",
                    "default": "en",
                    "enum": list(SUPPORTED_LANGS),
                },
            },
            "required": ["title"],
        },
    },
    {
        "name": "article_sections",
        "description": (
            "Get the table of contents (section headings) for a Wikipedia "
            "article — section number, heading text, and nesting level. "
            "Useful for navigating long articles before committing to the "
            "full body via `article_extract`. Major articles can have "
            "50KB+ of body text; `article_sections` gives the TOC in a "
            "compact numbered list so callers can pick what to read next. "
            "Pairs with `summary` (lead), `article_sections` (structure), "
            "`article_extract` (full body)."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Article title (e.g. 'Tyrannosaurus' or 'Albert_Einstein')",
                },
                "lang": {
                    "type": "string",
                    "description": "Wikipedia language code (default 'en')",
                    "default": "en",
                    "enum": list(SUPPORTED_LANGS),
                },
            },
            "required": ["title"],
        },
    },
    {
        "name": "section_text",
        "description": (
            "Read ONE section of a Wikipedia article as plain text — the "
            "targeted-reading companion to `article_sections`. Pass a "
            "section number exactly as shown by `article_sections` "
            "(e.g. 2 or '2.1'; 0 reads the lead/intro), or a heading name "
            "(case-insensitive, e.g. 'Life and career'); misspelled names "
            "get close-match suggestions. Renders the section via the "
            "read-only parse API "
            "and returns clean text with paragraph structure — no need to "
            "pull the whole 50KB+ article via `article_extract` when you "
            "only want one part of it. Follows redirects; the link at the "
            "bottom deep-links to the section on the article page."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Article title (e.g. 'Albert Einstein' or 'Paris')",
                },
                "section": {
                    "type": ["integer", "string"],
                    "description": (
                        "Section to read: number as shown by "
                        "`article_sections` (e.g. 2 or '2.1'; 0 = "
                        "lead/intro), or heading text "
                        "(e.g. 'Life and career')"
                    ),
                },
                "lang": {
                    "type": "string",
                    "description": "Wikipedia language code (default 'en')",
                    "default": "en",
                    "enum": list(SUPPORTED_LANGS),
                },
            },
            "required": ["title", "section"],
        },
    },
    {
        "name": "featured_article",
        "description": (
            "Get today's Wikipedia Featured Article — the single article Wikipedia's editors showcase as "
            "the best of the encyclopedia that day. Returns the full long-form extract plus thumbnail: "
            "reliably high-quality, surprising, in-depth content. A strong daily source of hooks and deep "
            "dives; for the curated daily image instead use `picture_of_the_day`, and for today's "
            "historical events use `on_this_day`."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "lang": {
                    "type": "string",
                    "description": "Wikipedia language code (default 'en')",
                    "default": "en",
                    "enum": list(SUPPORTED_LANGS),
                },
            },
        },
    },
    {
        "name": "picture_of_the_day",
        "description": (
            "Get Wikimedia Commons' Picture of the Day — the curated daily "
            "image from Wikipedia's featured feed. Returns preview + "
            "full-size image URLs, photographer, license, and description. "
            "Accepts an optional YYYYMMDD date (default today UTC) to "
            "browse past pictures — the visual counterpart to "
            "featured_article for daily content hooks."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "lang": {
                    "type": "string",
                    "description": "Wikipedia language code (default 'en')",
                    "default": "en",
                    "enum": list(SUPPORTED_LANGS),
                },
                "date": {
                    "type": "string",
                    "description": "Date in YYYYMMDD format (default: today UTC)",
                    "default": "",
                },
            },
        },
    },
    {
        "name": "media_of_the_day",
        "description": (
            "Get Wikimedia Commons' Media of the Day — the curated daily "
            "video/audio clip from Commons' Media of the Day selection. "
            "Returns media kind, duration, a preview thumbnail (video) or "
            "listen link (audio), artist, license, and description. "
            "Accepts an optional YYYYMMDD date (default today UTC) to "
            "browse past picks — the motion-and-sound counterpart to "
            "picture_of_the_day for daily content hooks."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "description": "Date in YYYYMMDD format (default: today UTC)",
                    "default": "",
                },
            },
        },
    },
    {
        "name": "on_this_day",
        "description": (
            "Get historical events that happened on today's date (UTC) "
            "from Wikipedia's 'On This Day' feed. Returns a random sample "
            "of events with year + description + Wikipedia link — great "
            "daily content hook alongside featured_article."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "lang": {
                    "type": "string",
                    "description": "Wikipedia language code (default 'en')",
                    "default": "en",
                    "enum": list(SUPPORTED_LANGS),
                },
                "count": {
                    "type": "integer",
                    "description": "Number of events to return (default 5, max 10)",
                    "default": 5,
                },
            },
        },
    },
    {
        "name": "deaths_on_this_day",
        "description": (
            "Get notable deaths that happened on today's date (UTC) from "
            "Wikipedia's 'On This Day' feed — the deaths-only companion "
            "to `on_this_day` (which returns events). Useful for "
            "'in memoriam' content hooks, obituary-style social posts, "
            "and newsletter intros. Pairs with `on_this_day` (events) "
            "and `featured_article` (today's long-form pick) for a full "
            "daily 'today in Wikipedia' digest."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "lang": {
                    "type": "string",
                    "description": "Wikipedia language code (default 'en')",
                    "default": "en",
                    "enum": list(SUPPORTED_LANGS),
                },
                "count": {
                    "type": "integer",
                    "description": "Number of deaths to return (default 5, max 10)",
                    "default": 5,
                },
            },
        },
    },
    {
        "name": "births_on_this_day",
        "description": (
            "Get notable births that happened on today's date (UTC) from "
            "Wikipedia's 'On This Day' feed — the births companion to "
            "`on_this_day` (events) and `deaths_on_this_day` (deaths). "
            "Useful for 'born on this day' content hooks, birthday "
            "round-ups, and newsletter intros. Pairs with `on_this_day` "
            "(events) and `featured_article` (today's long-form pick) for "
            "a full daily 'today in Wikipedia' digest."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "lang": {
                    "type": "string",
                    "description": "Wikipedia language code (default 'en')",
                    "default": "en",
                    "enum": list(SUPPORTED_LANGS),
                },
                "count": {
                    "type": "integer",
                    "description": "Number of births to return (default 5, max 10)",
                    "default": 5,
                },
            },
        },
    },
    {
        "name": "categories",
        "description": (
            "List Wikipedia categories an article belongs to. Useful for "
            "taxonomy-based discovery — finding related topics that don't "
            "appear in text search. Hidden/maintenance categories are filtered out."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Article title (e.g. 'Tyrannosaurus' or 'Albert_Einstein')",
                },
                "limit": {
                    "type": "integer",
                    "description": "Max categories to return (default 20, max 50)",
                    "default": 20,
                },
                "lang": {
                    "type": "string",
                    "description": "Wikipedia language code (default 'en')",
                    "default": "en",
                    "enum": list(SUPPORTED_LANGS),
                },
            },
            "required": ["title"],
        },
    },
    {
        "name": "links",
        "description": (
            "List outgoing Wikipedia links from an article (the article "
            "network in raw form). Useful for graph-style discovery — "
            "given 'Tyrannosaurus', see which genera, paleontologists, "
            "formations, and anatomical terms it references. Filters to "
            "main namespace so talk/user/etc. don't pollute the result."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Article title (e.g. 'Tyrannosaurus' or 'Albert_Einstein')",
                },
                "limit": {
                    "type": "integer",
                    "description": "Max links to return (default 20, max 50)",
                    "default": 20,
                },
                "lang": {
                    "type": "string",
                    "description": "Wikipedia language code (default 'en')",
                    "default": "en",
                    "enum": list(SUPPORTED_LANGS),
                },
            },
            "required": ["title"],
        },
    },
    {
        "name": "backlinks",
        "description": (
            "List incoming Wikipedia links to an article — i.e. 'what "
            "links here' / backlinks / referrer pages. Inverse of "
            "`links`: given 'Velociraptor', see which other articles "
            "reference it (cultural mentions, scientific citations, "
            "comparative anatomy pages, etc.). Useful for graph-style "
            "discovery in the reverse direction — mapping an article's "
            "position in the encyclopedia network. Filters to main "
            "namespace so talk/user/etc. don't pollute the result."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Article title (e.g. 'Tyrannosaurus' or 'Albert_Einstein')",
                },
                "limit": {
                    "type": "integer",
                    "description": "Max backlinks to return (default 20, max 50)",
                    "default": 20,
                },
                "lang": {
                    "type": "string",
                    "description": "Wikipedia language code (default 'en')",
                    "default": "en",
                    "enum": list(SUPPORTED_LANGS),
                },
            },
            "required": ["title"],
        },
    },
    {
        "name": "external_links",
        "description": (
            "List external (off-wiki) links from a Wikipedia article — "
            "citations, references, primary sources, and other off-wiki "
            "resources the article points to. Outbound complement to "
            "`links` (internal outgoing) and `backlinks` (internal "
            "incoming): the trio (`links` + `backlinks` + `external_links`) "
            "maps the full reference network around an article. Useful "
            "for source verification, citation audits, primary-source "
            "discovery, and fact-checking research."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Article title (e.g. 'Tyrannosaurus' or 'Albert_Einstein')",
                },
                "limit": {
                    "type": "integer",
                    "description": "Max external links to return (default 20, max 50)",
                    "default": 20,
                },
                "lang": {
                    "type": "string",
                    "description": "Wikipedia language code (default 'en')",
                    "default": "en",
                    "enum": list(SUPPORTED_LANGS),
                },
            },
            "required": ["title"],
        },
    },
    {
        "name": "nearby",
        "description": (
            "List Wikipedia articles geographically near a location — "
            "location-based discovery. Anchor by article title (e.g. "
            "'Eiffel Tower' — uses that article's coordinates, no "
            "geocoding service needed) or by explicit lat/lon. Returns "
            "nearby articles with distances in meters/km. Useful for "
            "travel research and 'what's notable around here' questions."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Anchor article title (e.g. 'Eiffel Tower'). Use instead of lat/lon.",
                },
                "lat": {
                    "type": "number",
                    "description": "Latitude in decimal degrees (-90 to 90). Requires lon.",
                },
                "lon": {
                    "type": "number",
                    "description": "Longitude in decimal degrees (-180 to 180). Requires lat.",
                },
                "radius": {
                    "type": "integer",
                    "description": "Search radius in meters (default 1000, max 10000)",
                    "default": 1000,
                },
                "limit": {
                    "type": "integer",
                    "description": "Max articles to return (default 20, max 50)",
                    "default": 20,
                },
                "lang": {
                    "type": "string",
                    "description": "Wikipedia language code (default 'en')",
                    "default": "en",
                    "enum": list(SUPPORTED_LANGS),
                },
            },
        },
    },
    {
        "name": "translations",
        "description": (
            "List all language versions of a Wikipedia article (langlinks). "
            "Returns the other-language editions the article exists in — "
            "e.g. for 'Tyrannosaurus' (en), returns de/fr/es/ja/zh titles. "
            "Complements the one-way `lang` parameter used by other tools: "
            "every tool can query a single language, but only `translations` "
            "reveals the article's full language coverage so callers can "
            "pick a target language to fetch next. Useful for translation "
            "research (full coverage vs. stub languages), cross-language "
            "content sourcing, and language-coverage analysis. `limit` "
            "clamps the number of entries (default 30, max 100) — popular "
            "articles can have 100+ language versions."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Article title (e.g. 'Tyrannosaurus' or 'Albert_Einstein')",
                },
                "limit": {
                    "type": "integer",
                    "description": "Max language entries to return (default 30, max 100)",
                    "default": 30,
                },
                "lang": {
                    "type": "string",
                    "description": "Wikipedia language code to query from (default 'en')",
                    "default": "en",
                    "enum": list(SUPPORTED_LANGS),
                },
            },
            "required": ["title"],
        },
    },
    {
        "name": "revisions",
        "description": (
            "Show an article's recent edit history ('View history'): "
            "revision id, timestamp, editor, edit summary, and byte-size "
            "delta vs the previous revision. Each revision links to its "
            "diff (Special:Diff/<revid>) so you can inspect exactly what "
            "changed. Useful for tracking how an article evolves, auditing "
            "edits on a topic, or spotting edit activity around current "
            "events. Complements `pageviews` (popularity) with provenance "
            "(who changed what, when)."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Article title (e.g. 'Tyrannosaurus' or 'Albert_Einstein')",
                },
                "limit": {
                    "type": "integer",
                    "description": "Max revisions to return (default 10, max 50)",
                    "default": 10,
                },
                "lang": {
                    "type": "string",
                    "description": "Wikipedia language code (default 'en')",
                    "default": "en",
                    "enum": list(SUPPORTED_LANGS),
                },
            },
            "required": ["title"],
        },
    },
    {
        "name": "pageviews",
        "description": (
            "Get daily view counts for a Wikipedia article over a date range "
            "(popularity research, trending topics, historical interest). "
            "Uses Wikimedia's pageviews REST API. Default window is the "
            "last 7 days ending yesterday UTC. Returns total + daily average "
            "+ markdown table of daily views."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Article title (e.g. 'Tyrannosaurus' or 'Albert_Einstein')",
                },
                "start": {
                    "type": "string",
                    "description": "Start date in YYYYMMDD (default: 7 days before end)",
                },
                "end": {
                    "type": "string",
                    "description": "End date in YYYYMMDD (default: yesterday UTC)",
                },
                "lang": {
                    "type": "string",
                    "description": "Wikipedia language code (default 'en')",
                    "default": "en",
                    "enum": list(SUPPORTED_LANGS),
                },
            },
            "required": ["title"],
        },
    },
    {
        "name": "news",
        "description": (
            "Get current events from Wikipedia's Main Page 'In the news' "
            "section — the editorially-curated list of recent notable "
            "events. Pairs with featured_article (today's long-form pick) "
            "and on_this_day (historical) — news covers the present tense. "
            "Bold-linked article titles become Markdown so the main "
            "subject of each event stands out."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "lang": {
                    "type": "string",
                    "description": "Wikipedia language code (default 'en')",
                    "default": "en",
                    "enum": list(SUPPORTED_LANGS),
                },
                "limit": {
                    "type": "integer",
                    "description": "Max events to return (default 5, max 10)",
                    "default": 5,
                },
            },
        },
    },
    {
        "name": "image",
        "description": (
            "Get just the lead image for a Wikipedia article — "
            "returns both the 300px thumbnail URL and the full-resolution "
            "original URL from Wikipedia's REST summary endpoint. "
            "Useful when you want the article's image for embedding "
            "elsewhere (cards, Telegram posts, slide decks, README "
            "hero images) without the surrounding summary text. "
            "`summary` embeds the thumbnail inline; `image` exposes "
            "both URLs separately so downstream tools can fetch / "
            "display at any size. Returns a clean message if the "
            "article has no image."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Article title (e.g. 'Tyrannosaurus' or 'Albert_Einstein')",
                },
                "lang": {
                    "type": "string",
                    "description": "Wikipedia language code (default 'en')",
                    "default": "en",
                    "enum": list(SUPPORTED_LANGS),
                },
            },
            "required": ["title"],
        },
    },
    {
        "name": "top_reads",
        "description": (
            "Get the most-read articles on Wikipedia for a given date. "
            "Uses Wikimedia's top-pageviews endpoint (all-access, daily). "
            "Default date is yesterday UTC (today's data is typically "
            "not yet finalized). Filters out non-content namespaces "
            "(Main_Page, Special:Search, Portal:Current_events, "
            "Wikipedia:*, etc.) so the result is real articles only. "
            "Pairs with `pageviews` (per-article over a range) for "
            "trending-vs-popular comparisons — top_reads answers "
            "'what is everyone reading right now' while pageviews "
            "answers 'how is this specific article trending'."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "description": "Date in YYYYMMDD (default: yesterday UTC)",
                },
                "limit": {
                    "type": "integer",
                    "description": "Max articles to return (default 10, max 50)",
                    "default": 10,
                },
                "lang": {
                    "type": "string",
                    "description": "Wikipedia language code (default 'en')",
                    "default": "en",
                    "enum": list(SUPPORTED_LANGS),
                },
            },
        },
    },
    {
        "name": "media_list",
        "description": (
            "List all media (images, videos, audio) used in a Wikipedia "
            "article — not just the lead thumbnail. Returns a structured "
            "markdown list: file title, type (image/video/audio), caption, "
            "and thumbnail URL. Lead media is marked so callers can skip "
            "it when they already have it via `image`. Uses Wikipedia's "
            "REST `/page/media-list` endpoint (structured JSON, no HTML "
            "parsing). Pairs with `image` (lead only) — use `image` for "
            "the headline thumbnail, `media_list` for the full inventory "
            "(gallery generation, fact-checking, slide decks, audits). "
            "`limit` clamps the number of items (default 25, max 100)."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Article title (e.g. 'Tyrannosaurus' or 'Albert_Einstein')",
                },
                "limit": {
                    "type": "integer",
                    "description": "Max media items to return (default 25, max 100)",
                    "default": 25,
                },
                "lang": {
                    "type": "string",
                    "description": "Wikipedia language code (default 'en')",
                    "default": "en",
                    "enum": list(SUPPORTED_LANGS),
                },
            },
            "required": ["title"],
        },
    },
    {
        "name": "media_search",
        "description": (
            "Search Wikimedia Commons for freely-licensed media by "
            "keyword — the topic-based counterpart to `image` (lead image "
            "of a known article) and `media_list` (media already used in "
            "an article). Give it a topic ('aurora borealis', 'vintage "
            "trains') and get back real Commons files with thumbnail and "
            "full-size URLs, dimensions, license, and artist — ready to "
            "embed in cards, posts, slide decks, or README hero images. "
            "`filetype` filters to 'image' (default: photos + diagrams / "
            "SVGs), 'video', 'audio', or 'all'. Commons is "
            "language-independent, so this tool takes no `lang` "
            "parameter. Everything returned is freely licensed; check the "
            "license on the file page before reuse."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Media search keywords (e.g. 'aurora borealis' or 'steam locomotive')",
                },
                "limit": {
                    "type": "integer",
                    "description": "Max results to return (default 10, max 50)",
                    "default": 10,
                },
                "filetype": {
                    "type": "string",
                    "description": "Media type filter: 'image' (photos + diagrams/SVGs), 'video', 'audio', or 'all'",
                    "default": "image",
                    "enum": ["image", "video", "audio", "all"],
                },
            },
            "required": ["query"],
        },
    },
    {
        "name": "quote",
        "description": (
            "Get a random notable quote from a curated list of famous "
            "authors (Churchill, Einstein, Twain, Gandhi, Mandela, Wilde, "
            "Angelou, Jobs, Lennon, Socrates, etc.). Returns a short, "
            "time-tested quotation with author attribution. Pairs with "
            "did_you_know (random encyclopedia fact) and dino_fact (random "
            "dino fact) for variety in 'today's trivia' outputs — great "
            "for daily content hooks, social posts, newsletter intros. "
            "Currently English-only (curated list); the `lang` parameter "
            "is accepted for API consistency but non-English values still "
            "return English quotes."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "lang": {
                    "type": "string",
                    "description": "Wikipedia language code (default 'en'). Currently English-only; non-English values fall back to English.",
                    "default": "en",
                    "enum": list(SUPPORTED_LANGS),
                },
            },
        },
    },
    {
        "name": "recent_changes",
        "description": (
            "Show the most recent changes to Wikipedia articles — a live "
            "window into what editors are doing right now. Uses the "
            "MediaWiki recentchanges feed over the article namespace. "
            "`kind` filters the stream: 'edit' (text changes), 'new' "
            "(newly published articles — a discovery feed of brand-new "
            "pages), 'categorize' (category membership changes), 'log' "
            "(page moves, deletions, protections). Complements `revisions` "
            "(history of one article) with the reverse angle: the freshest "
            "edits everywhere. Each entry shows the change kind, article "
            "link, byte-size delta, editor, timestamp, edit comment, and a "
            "diff link — great for spotting breaking-news edits, new pages "
            "on emerging topics, and bot-maintenance sweeps. Read-only."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "kind": {
                    "type": "string",
                    "description": "Filter the change stream: 'all' (default), 'edit', 'new', 'categorize', or 'log'",
                    "default": "all",
                    "enum": ["all", "edit", "new", "categorize", "log"],
                },
                "limit": {
                    "type": "integer",
                    "description": "Max changes to return (default 10, max 50)",
                    "default": 10,
                },
                "lang": {
                    "type": "string",
                    "description": "Wikipedia language code (default 'en')",
                    "default": "en",
                    "enum": list(SUPPORTED_LANGS),
                },
            },
        },
    },
    {
        "name": "category_members",
        "description": (
            "List Wikipedia articles filed under a category — taxonomy-based discovery. The reverse direction of `categories` (which lists an article's categories): given 'Machine learning researchers', enumerate who's actually in it. Each entry includes a 1-2 sentence extract plus a thumbnail URL when one exists, so results are browsable at a glance. Filters to main-namespace articles so subcategories and files don't pollute the result. The 'Category:' prefix is optional. Pairs with `categories` (find the taxonomy) and `search` (find the entry point)."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "category": {
                    "type": "string",
                    "description": "Category name, with or without the 'Category:' prefix (e.g. 'Flightless birds' or 'Category:Flightless birds')",
                },
                "limit": {
                    "type": "integer",
                    "description": "Max articles to return (default 20, max 50)",
                    "default": 20,
                },
                "lang": {
                    "type": "string",
                    "description": "Wikipedia language code (default 'en')",
                    "default": "en",
                    "enum": list(SUPPORTED_LANGS),
                },
            },
            "required": ["category"],
        },
    },
    {
        "name": "infobox",
        "description": (
            "Extract the structured fact box (infobox) from a Wikipedia article as a field/value "
            "table — dates, people, places, statistics, founders, CEOs, populations, capitals. The "
            "fastest path to a concrete fact ('who founded X?', 'what's the population of Y?') without "
            "wading through prose. Renders wikitext into clean plain text (citations stripped, links "
            "flattened, fields capped at 50). Use this for facts; use `summary` for the prose gist and "
            "`article_extract` for full text. Reports clearly when an article has no infobox."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Article title (e.g. 'Albert Einstein' or 'Paris')",
                },
                "lang": {
                    "type": "string",
                    "description": "Wikipedia language code (default 'en')",
                    "default": "en",
                    "enum": list(SUPPORTED_LANGS),
                },
            },
            "required": ["title"],
        },
    },
    {
        "name": "article_quality",
        "description": (
            "Get Wikipedia's quality assessments for an article — the WikiProject grades "
            "(FA, GA, B, C, Start, Stub) and importance ratings assigned by editors. The "
            "encyclopedia's own trust signal: use it before relying on an article (a GA/FA "
            "passed formal review; a Stub is a skeleton). Reports an overall class plus the "
            "per-project breakdown with a quality-ladder legend. Assessment is enabled per "
            "language edition (en works; some editions like de report no data). Read-only "
            "via the pageassessments action API — GET only, no new dependencies."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Article title (e.g. 'Albert Einstein' or 'Paris')",
                },
                "lang": {
                    "type": "string",
                    "description": "Wikipedia language code (default 'en')",
                    "default": "en",
                    "enum": list(SUPPORTED_LANGS),
                },
            },
            "required": ["title"],
        },
    },
    {
        "name": "related_articles",
        "description": (
            "Find Wikipedia articles semantically similar to a given article — "
            "'what should I read next'. Uses Wikipedia's own search engine "
            "(MoreLikeThis scoring over article text and link structure), "
            "unlike `links` (raw outgoing links) or `categories` (shared "
            "topic buckets): given 'Velociraptor', expect dromaeosaurids, "
            "feathered dinosaurs, and 'Deinonychus'. Each result shows the "
            "article's short description and thumbnail; the source article "
            "itself is excluded. Read-only via the action API search "
            "generator — GET only, no new dependencies."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Article title (e.g. 'Velociraptor' or 'Albert Einstein')",
                },
                "limit": {
                    "type": "integer",
                    "description": "Max related articles to return (default 5, max 20)",
                    "default": 5,
                },
                "lang": {
                    "type": "string",
                    "description": "Wikipedia language code (default 'en')",
                    "default": "en",
                    "enum": list(SUPPORTED_LANGS),
                },
            },
            "required": ["title"],
        },
    },
    {
        "name": "contributors",
        "description": (
            "Who writes and maintains a Wikipedia article — the most active "
            "recent editors. Tallies the article's recent edit history (up to "
            "500 revisions) into a ranked contributor table: top named editors "
            "by edit count with their share of sampled edits and user-page "
            "links, plus the anonymous (IP) edit share. A provenance "
            "companion to `article_quality` (the grade earned) and `revisions` "
            "(the raw edit log): a page tended by veteran caretakers reads "
            "differently from one mostly touched by drive-by IP edits, and "
            "the top names are the people to credit or check for conflicts "
            "of interest. Follows redirects. Read-only action API revisions "
            "query — GET only, no new dependencies."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Article title (e.g. 'Albert Einstein' or 'Paris')",
                },
                "limit": {
                    "type": "integer",
                    "description": "Max top contributors to return (default 10, max 20)",
                    "default": 10,
                },
                "lang": {
                    "type": "string",
                    "description": "Wikipedia language code (default 'en')",
                    "default": "en",
                    "enum": list(SUPPORTED_LANGS),
                },
            },
            "required": ["title"],
        },
    },
    {
        "name": "references",
        "description": (
            "The sources an article cites — its bibliography. Returns the "
            "article's numbered reference list: each citation's text plus "
            "the off-wiki URLs it points to (DOI, publisher, archive, "
            "primary-source links). The verification companion to "
            "`external_links` (which dumps every off-wiki link on the page): "
            "`references` returns only the sources the article actually "
            "cites. Useful for source verification, citation audits, "
            "bibliography building, and primary-source discovery. Follows "
            "redirects. Read-only parse API — GET only, no new dependencies."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Article title (e.g. 'Albert Einstein' or 'Paris')",
                },
                "limit": {
                    "type": "integer",
                    "description": "Max citations to return (default 20, max 50)",
                    "default": 20,
                },
                "lang": {
                    "type": "string",
                    "description": "Wikipedia language code (default 'en')",
                    "default": "en",
                    "enum": list(SUPPORTED_LANGS),
                },
            },
            "required": ["title"],
        },
    },
    {
        "name": "revision_diff",
        "description": (
            "Compare two revisions of an article and show exactly what changed — a plain-text "
            "unified diff of the article's wikitext between revision rev_from and rev_to "
            "(get revision IDs from `revisions`). Each side is labelled with its timestamp, "
            "editor, and edit summary. The edit-auditing companion to `revisions`: use it to "
            "see what a specific edit added or removed, review edits before trusting a new "
            "paragraph, or spot stealth rewrites. `limit` clamps diff lines (default 100, max 500)."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Article title (e.g. 'Tyrannosaurus')",
                },
                "rev_from": {
                    "type": "integer",
                    "description": "Older revision ID (from `revisions`)",
                },
                "rev_to": {
                    "type": "integer",
                    "description": "Newer revision ID (from `revisions`)",
                },
                "limit": {
                    "type": "integer",
                    "description": "Max diff lines to show (default 100, max 500)",
                    "default": 100,
                },
                "lang": {
                    "type": "string",
                    "description": "Wikipedia language code (default 'en')",
                    "default": "en",
                    "enum": list(SUPPORTED_LANGS),
                },
            },
            "required": ["title", "rev_from", "rev_to"],
        },
    },
    {
        "name": "disambiguation",
        "description": (
            "Resolve a Wikipedia disambiguation page into its candidate "
            "articles. Detects whether a title (e.g. 'Mercury', 'Apple', "
            "'Python') is a disambiguation page and, if so, returns the "
            "structured option list — article title plus one-line "
            "description — grouped by the page's own sections. Resolves "
            "the classic dead-end where `search`/`summary` land on an "
            "ambiguous title: call this, pick the right candidate, then "
            "fetch it with `summary` or `article_extract`. Reports "
            "clearly when the title is a regular article or doesn't exist."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Article title (e.g. 'Mercury' or 'Apple')",
                },
                "limit": {
                    "type": "integer",
                    "description": "Max options to return (default 30, max 100)",
                    "default": 30,
                },
                "lang": {
                    "type": "string",
                    "description": "Wikipedia language code (default 'en')",
                    "default": "en",
                    "enum": list(SUPPORTED_LANGS),
                },
            },
            "required": ["title"],
        },
    },
    {
        "name": "user_contribs",
        "description": (
            "What a Wikipedia editor has been doing — their recent "
            "contributions across the encyclopedia. Shows the latest edits "
            "by a named account (or an IP address, e.g. user='192.0.2.1'): "
            "edited pages, timestamps, byte-size deltas, edit comments, "
            "and flags for new pages, minor edits, and edits still current. "
            "The header reports registration date and total edit count. The "
            "reverse angle of `contributors` (who edits this article): "
            "profile a top contributor, audit an anonymous IP's activity, or "
            "spot single-purpose accounts (edits confined to one topic hint "
            "at a conflict of interest). `namespace` scopes the search "
            "(default 0 = articles). Read-only — GET only, no new "
            "dependencies."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "user": {
                    "type": "string",
                    "description": "Wikipedia username or IP address (e.g. 'Jimbo Wales')",
                },
                "limit": {
                    "type": "integer",
                    "description": "Max contributions to return (default 10, max 50)",
                    "default": 10,
                },
                "namespace": {
                    "type": "integer",
                    "description": "Namespace to search (default 0 = articles; 3 = user talk)",
                    "default": 0,
                },
                "lang": {
                    "type": "string",
                    "description": "Wikipedia language code (default 'en')",
                    "default": "en",
                    "enum": list(SUPPORTED_LANGS),
                },
            },
            "required": ["user"],
        },
    },
    {
        "name": "citation_needed",
        "description": (
            "Find statements Wikipedia has flagged as needing a source. "
            "Two angles: pass `article` to extract every sentence in that "
            "article carrying a {{citation needed}} tag (the exact claims "
            "editors flagged, with tag dates), or pass `topic` (or "
            "neither) to search Wikipedia for articles with unsourced "
            "claims on that topic, each with the flagged claim's text. "
            "Use it to find sourcing work as an editor or to spot the "
            "shakiest claims in a topic you're researching. The "
            "verification companion to `references`: this finds what's "
            "missing a source. Tag-name matching is English-centric; "
            "`lang` accepted for API consistency. Read-only — GET only, "
            "no new dependencies."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "topic": {
                    "type": "string",
                    "description": "Keyword to scope the search (e.g. 'climate'); omit for a Wikipedia-wide sample",
                },
                "article": {
                    "type": "string",
                    "description": "Exact article title to scan for tagged claims (takes precedence over topic)",
                },
                "limit": {
                    "type": "integer",
                    "description": "Max claims/articles to return (default 10, max 25)",
                    "default": 10,
                },
                "lang": {
                    "type": "string",
                    "description": "Wikipedia language code (default 'en')",
                    "default": "en",
                    "enum": list(SUPPORTED_LANGS),
                },
            },
            "required": [],
        },
    },
    {
        "name": "talk",
        "description": (
            "Show the most recently active discussion threads on an article's "
            "talk page — what Wikipedia editors are currently debating, "
            "questioning, or proposing about the topic. Each thread lists its "
            "heading, last-activity timestamp, signed-comment count, and an "
            "excerpt of the latest comment. Automated maintenance notices "
            "(redirect/deletion discussions) are filtered out. The "
            "behind-the-scenes companion to `contributors` and "
            "`article_quality`: check it to find controversies, open "
            "questions, and editorial disputes before relying on an article. "
            "Read-only — GET only, no new dependencies."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Article title whose talk page to read (e.g. 'Climate change')",
                },
                "limit": {
                    "type": "integer",
                    "description": "Max threads to return (default 5, max 15)",
                    "default": 5,
                },
                "lang": {
                    "type": "string",
                    "description": "Wikipedia language code (default 'en')",
                    "default": "en",
                    "enum": list(SUPPORTED_LANGS),
                },
            },
            "required": [],
        },
    },
    {
        "name": "article_flags",
        "description": (
            "Show the maintenance banners editors placed on an article — "
            "Wikipedia's own warning labels ({{POV}}, {{Original research}}, "
            "{{Unreferenced}}, {{Cleanup}}, {{Disputed}}, ...). Each flag "
            "lists its banner name, tag date, location (article top or "
            "section), and a plain-language meaning. The trust-signal "
            "companion to `article_quality` (the grade), `citation_needed` "
            "(unsourced claims), and `talk` (editor discussion): check it to "
            "see exactly what editors think is wrong with an article before "
            "relying on it. Read-only — GET only, no new dependencies."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "article": {
                    "type": "string",
                    "description": "Article title to check for editorial flags (e.g. 'Climate change')",
                },
                "limit": {
                    "type": "integer",
                    "description": "Max flags to return (default 10, max 25)",
                    "default": 10,
                },
                "lang": {
                    "type": "string",
                    "description": "Wikipedia language code (default 'en')",
                    "default": "en",
                    "enum": list(SUPPORTED_LANGS),
                },
            },
            "required": [],
        },
    },
    {
        "name": "article_protection",
        "description": (
            "Is this Wikipedia article locked, who can still touch it, and "
            "for how long — the page's protection status. Reports which "
            "actions are restricted (editing, moving/renaming, creating a "
            "missing title), at what level (semi-protection, "
            "extended-confirmed, administrators-only), and when each "
            "restriction expires; cascade protections name their source "
            "page. Missing titles are reported too (salted titles carry a "
            "\"create\" protection). Follows redirects. The lockdown "
            "companion to the other trust signals: `article_quality` (the "
            "grade), `article_flags` (editorial warnings), `citation_needed` "
            "(unsourced claims), and `talk` (editor discussion). Read-only — "
            "GET only, no new dependencies."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "article": {
                    "type": "string",
                    "description": "Article title to check for protection (e.g. 'Donald Trump')",
                },
                "lang": {
                    "type": "string",
                    "description": "Wikipedia language code (default 'en')",
                    "default": "en",
                    "enum": list(SUPPORTED_LANGS),
                },
            },
            "required": [],
        },
    },
    {
        "name": "article_pulse",
        "description": (
            "Vital signs of a Wikipedia article — how alive is this page right "
            "now. One-screen health check: creation date and creator (earliest "
            "surviving revision), page length, watcher count, the most recent "
            "edit (when, who, edit summary), and edit velocity over the last "
            "30 days (edit count plus distinct editors), capped with a "
            "plain-language activity verdict (buzzing / active / quiet / "
            "dormant). Follows redirects. The liveliness companion to "
            "`article_quality` (the grade earned), `contributors` (who edits "
            "it), `revisions` (the raw edit log), and `pageviews` (the "
            "traffic). Read-only via the action API — GET only, no new "
            "dependencies."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "article": {
                    "type": "string",
                    "description": "Article title to take the pulse of (e.g. 'Python (programming language)')",
                },
                "lang": {
                    "type": "string",
                    "description": "Wikipedia language code (default 'en')",
                    "default": "en",
                    "enum": list(SUPPORTED_LANGS),
                },
            },
            "required": [],
        },
    },
    {
        "name": "citation_sources",
        "description": (
            "Which publishers an article's evidence comes from — its sources "
            "by domain. Aggregates the article's reference list into a "
            "publisher map: every off-wiki link cited in the numbered "
            "references is grouped by registrable domain (so all *.bbc.co.uk "
            "citations land under bbc.co.uk) and ranked by citation count, "
            "with each domain's share of linked references. Also reports the "
            "share of citations with archived (Wayback Machine / archive.org) "
            "copies and the share pointing at DOI-linked scholarly works. "
            "The diversity lens for the \"can I rely on this article?\" audit: "
            "shows at a glance whether the bibliography is balanced (dozens "
            "of independent publishers) or lopsided (half the evidence from "
            "one outlet). Follows redirects. Pairs with `references` (the "
            "full bibliography), `article_quality` (the grade), "
            "`article_flags` (editorial warnings), and `citation_needed` "
            "(unsourced claims). Read-only via the action API — GET only, no "
            "new dependencies."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Article title to analyze the sources of (e.g. 'Climate change')",
                },
                "limit": {
                    "type": "integer",
                    "description": "Max source domains to show (default 15, max 30)",
                    "default": 15,
                },
                "lang": {
                    "type": "string",
                    "description": "Wikipedia language code (default 'en')",
                    "default": "en",
                    "enum": list(SUPPORTED_LANGS),
                },
            },
            "required": [],
        },
    },
    {
        "name": "article_path",
        "description": (
            "Find the shortest click-path between two articles — the "
            "six-degrees game. Given two article titles, searches "
            "Wikipedia's link graph for the shortest chain of blue links "
            "connecting them (e.g. Banana → Africa → Anatolia → Trojan War). "
            "Bidirectional and bounded: 1 hop checks a direct link, 2 hops "
            "intersects the start's outgoing links with pages linking to "
            "the target, 3 hops expands a bounded sample of the start's "
            "links. Follows redirects. The discovery companion to `links` "
            "and `backlinks`. Read-only action API — GET only, no new "
            "dependencies."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "start": {
                    "type": "string",
                    "description": "Starting article title (e.g. 'Banana')",
                },
                "target": {
                    "type": "string",
                    "description": "Target article title (e.g. 'Trojan War')",
                },
                "max_hops": {
                    "type": "integer",
                    "description": "Max path length to search (default 2, max 3)",
                    "default": 2,
                },
                "lang": {
                    "type": "string",
                    "description": "Wikipedia language code (default 'en')",
                    "default": "en",
                    "enum": list(SUPPORTED_LANGS),
                },
            },
            "required": ["start", "target"],
        },
    },
    {
        "name": "article_at_date",
        "description": (
            "Show what an article said on a given date — the time machine. "
            "Given an article title and a YYYY-MM-DD date, finds the latest "
            "surviving revision at or before that day and returns its lead "
            "text: how the article read then, with the revision ID, "
            "timestamp, editor, edit summary, and a permanent link to the "
            "exact revision. Follows redirects; reports clearly when the "
            "article had no revision before the date. The history companion "
            "to `summary` (the article now), `revisions` (the raw edit "
            "log), and `revision_diff` (what changed between revisions). "
            "Read-only via the action API — GET only, no new dependencies."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Article title (e.g. 'ChatGPT')",
                },
                "date": {
                    "type": "string",
                    "description": "Date to look back to, YYYY-MM-DD (e.g. '2023-01-01')",
                },
                "lang": {
                    "type": "string",
                    "description": "Wikipedia language code (default 'en')",
                    "default": "en",
                    "enum": list(SUPPORTED_LANGS),
                },
            },
            "required": ["title", "date"],
        },
    },
]


def _call_tool(name: str, args: dict) -> str:
    if name == "search":
        return search_wikipedia(**args)
    if name == "summary":
        return get_summary(**args)
    if name == "random":
        return get_random(**args)
    if name == "simple_summary":
        return get_simple_summary(**args)
    if name == "did_you_know":
        return did_you_know(**args)
    if name == "dino_fact":
        return dino_fact(**args)
    if name == "featured_article":
        return featured_article(**args)
    if name == "picture_of_the_day":
        return picture_of_the_day(**args)
    if name == "media_of_the_day":
        return media_of_the_day(**args)
    if name == "article_extract":
        return article_extract(**args)
    if name == "article_sections":
        return article_sections(**args)
    if name == "section_text":
        return section_text(**args)
    if name == "on_this_day":
        return on_this_day(**args)
    if name == "deaths_on_this_day":
        return deaths_on_this_day(**args)
    if name == "births_on_this_day":
        return births_on_this_day(**args)
    if name == "categories":
        return categories(**args)
    if name == "links":
        return links(**args)
    if name == "backlinks":
        return backlinks(**args)
    if name == "external_links":
        return external_links(**args)
    if name == "nearby":
        return nearby(**args)
    if name == "translations":
        return translations(**args)
    if name == "revisions":
        return revisions(**args)
    if name == "pageviews":
        return pageviews(**args)
    if name == "news":
        return news(**args)
    if name == "top_reads":
        return top_reads(**args)
    if name == "image":
        return image(**args)
    if name == "media_list":
        return media_list(**args)
    if name == "media_search":
        return media_search(**args)
    if name == "quote":
        return quote(**args)
    if name == "recent_changes":
        return recent_changes(**args)
    if name == "category_members":
        return category_members(**args)
    if name == "infobox":
        return infobox(**args)
    if name == "article_quality":
        return article_quality(**args)
    if name == "related_articles":
        return related_articles(**args)
    if name == "contributors":
        return contributors(**args)
    if name == "references":
        return references(**args)
    if name == "revision_diff":
        return revision_diff(**args)
    if name == "disambiguation":
        return disambiguation(**args)
    if name == "user_contribs":
        return user_contribs(**args)
    if name == "citation_needed":
        return citation_needed(**args)
    if name == "talk":
        return talk(**args)
    if name == "article_flags":
        return article_flags(**args)
    if name == "article_protection":
        return article_protection(**args)
    if name == "article_pulse":
        return article_pulse(**args)
    if name == "citation_sources":
        return citation_sources(**args)
    if name == "article_path":
        return article_path(**args)
    if name == "article_at_date":
        return article_at_date(**args)
    return f"Unknown tool: {name}"


# ---------------------------------------------------------------------------
# JSON-RPC stdio loop
# ---------------------------------------------------------------------------
def _reply(msg_id, result):
    print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": result}))
    sys.stdout.flush()


def _reply_error(msg_id, code: int, message: str):
    print(
        json.dumps(
            {"jsonrpc": "2.0", "id": msg_id, "error": {"code": code, "message": message}}
        )
    )
    sys.stdout.flush()


def _handle_request(request: dict) -> None:
    method = request.get("method", "")
    msg_id = request.get("id")

    if method == "initialize":
        _reply(
            msg_id,
            {
                "protocolVersion": API_VERSION,
                "capabilities": {"tools": {}},
                "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION},
            },
        )
        return

    if method == "notifications/initialized":
        # Client signals init complete; nothing to do.
        return

    if method == "tools/list":
        _reply(msg_id, {"tools": TOOLS})
        return

    if method == "tools/call":
        params = request.get("params", {})
        name = params.get("name")
        args = params.get("arguments", {}) or {}
        if not name:
            _reply_error(msg_id, -32602, "Missing tool name")
            return
        try:
            result = _call_tool(name, args)
            _reply(msg_id, {"content": [{"type": "text", "text": str(result)}]})
        except Exception as e:
            _reply_error(msg_id, -32603, f"{type(e).__name__}: {e}")
        return

    # Notifications (no id) — ignore unknown
    if msg_id is None:
        return
    _reply_error(msg_id, -32601, f"Method not found: {method}")


def main() -> int:
    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break
            line = line.strip()
            if not line:
                continue
            _handle_request(json.loads(line))
        except json.JSONDecodeError as e:
            print(f"# JSON decode error: {e}", file=sys.stderr)
            sys.stderr.flush()
        except Exception as e:
            print(f"# Loop error: {type(e).__name__}: {e}", file=sys.stderr)
            sys.stderr.flush()
    return 0


if __name__ == "__main__":
    sys.exit(main())


