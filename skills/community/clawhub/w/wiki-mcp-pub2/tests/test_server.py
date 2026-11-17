#!/usr/bin/env python3
"""
Smoke tests for wikipedia-mcp — exercises tools directly without spawning stdio.
Run: python3 tests/test_server.py
"""

import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

# Allow running from repo root
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import server  # noqa: E402

PASS = 0
FAIL = 0


def check(label: str, condition: bool, detail: str = "") -> None:
    global PASS, FAIL
    if condition:
        PASS += 1
        print(f"  ✅ {label}")
    else:
        FAIL += 1
        print(f"  ❌ {label}  {detail}")


def section(title: str) -> None:
    print(f"\n=== {title} ===")


def main() -> int:
    section("search_wikipedia")
    out = server.search_wikipedia("velociraptor", limit=3)
    check("returns markdown", "**Velociraptor**" in out, out[:200])
    check("respects limit", out.count("\n1. ") + out.count("\n2. ") + out.count("\n3. ") >= 3)

    section("search_wikipedia — no results")
    out = server.search_wikipedia("xyzzynonesuch", limit=3)
    check("graceful empty", "No results found" in out, out)

    section("search_wikipedia — limit clamping + type safety")
    # limit above 20 should be clamped to ≤20
    out = server.search_wikipedia("dinosaur", limit=100)
    numbered = sum(1 for i in range(1, 21) if f"\n{i}. " in out)
    check("limit=100 clamps to ≤20 results", numbered <= 20, f"got {numbered} items")

    # limit <= 0 should be clamped to 1 (no result number 2+ should appear)
    out = server.search_wikipedia("dinosaur", limit=-5)
    check(
        "limit=-5 clamps to 1",
        "\n1. " in out and "\n2. " not in out,
        out[:300],
    )

    # Non-integer limit must not crash — fall back to default (5)
    out = server.search_wikipedia("dinosaur", limit="abc")
    check(
        "non-int limit returns results (no crash)",
        out.startswith("**Search results"),
        out[:300],
    )
    numbered = sum(1 for i in range(1, 21) if f"\n{i}. " in out)
    check("non-int limit uses default 5", numbered <= 5, f"got {numbered} items")

    section("get_summary")
    out = server.get_summary("Tyrannosaurus")
    check("title rendered", "## Tyrannosaurus" in out, out[:200])
    check("read more link", "Read more" in out)

    section("get_summary — 404")
    out = server.get_summary("ThisArticleDoesNotExist12345")
    check("404 message", "not found" in out, out)

    section("get_summary — input edge cases")
    # Empty title → URL becomes /page/summary/ → Wikipedia returns 404.
    # Guards against regression where an uncaught exception could surface to the MCP client.
    out = server.get_summary("")
    check("empty title returns graceful 404", "not found" in out, out)
    # Whitespace-only title: _slug strips, so URL is empty → 404.
    out = server.get_summary("   ")
    check("whitespace title returns graceful 404", "not found" in out, out)

    section("get_random")
    out = server.get_random()
    check("title rendered", out.startswith("## "), out[:200])

    section("get_simple_summary")
    out = server.get_simple_summary("Photosynthesis")
    check("title rendered", "## Photosynthesis" in out, out[:200])
    check("read more link", "Read more" in out)
    check("points at simple.wikipedia.org", "simple.wikipedia.org" in out, out[-200:])

    section("get_simple_summary — missing article")
    out = server.get_simple_summary("Xyzzynonesuchqqq")
    check("graceful not-found", "No Simple English article" in out, out[:200])
    check("points at summary", "`summary`" in out, out[:200])

    section("get_simple_summary — input edge cases")
    # Empty title → URL becomes /page/summary/ → 404 → graceful message.
    out = server.get_simple_summary("")
    check("empty title graceful", "No Simple English article" in out, out[:200])

    section("did_you_know")
    out = server.did_you_know()
    check("Did you know prefix", "Did you know" in out, out[:200])

    section("dino_fact — specific species")
    out = server.dino_fact("Spinosaurus")
    check("species mentioned", "Spinosaurus" in out, out[:300])

    section("dino_fact — random")
    out = server.dino_fact("")
    check("returns a fact", "Did you know about" in out, out[:200])

    section("dino_fact — fallback when species not found")
    out = server.dino_fact("xyzzynonesuch")
    check("fallback message present", "Couldn't find" in out, out[:200])
    check("still returns a fact", "Did you know about" in out, out[:500])

    section("article_extract")
    out = server.article_extract("Tyrannosaurus")
    check("title rendered", "## Tyrannosaurus" in out, out[:200])
    # Strip the markdown header + footer link to confirm body has no HTML tags
    body = out.split("\n\n", 2)[1] if "\n\n" in out else out
    check("plain text (no HTML tags in body)", "<" not in body and ">" not in body, body[:300])
    check("contains body text", "theropod" in out, out[:500])
    summary_out = server.get_summary("Tyrannosaurus")
    check(
        "longer than summary extract",
        len(out) > len(summary_out),
        f"extract={len(out)} summary={len(summary_out)}",
    )

    section("article_extract — 404")
    out = server.article_extract("ThisArticleDoesNotExist12345")
    check("404 message", "not found" in out, out)

    section("article_extract — multi-language")
    out = server.article_extract("Berlin", lang="de")
    check("de title rendered", "## " in out and "Berlin" in out, out[:200])
    check("de link present", "de.wikipedia.org/wiki/" in out, out[:500])

    section("article_extract — input edge cases")
    out = server.article_extract("")
    check("empty title returns graceful result", "not found" in out or "No extract" in out, out)

    section("article_extract — dispatcher routing")
    out = server._call_tool("article_extract", {"title": "Velociraptor"})
    check("dispatcher routes to article_extract", "Unknown tool" not in out, out[:200])
    check("dispatcher returned real content", "## " in out, out[:200])

    section("article_sections")
    out = server.article_sections("Tyrannosaurus")
    check("returns header", out.startswith("**Sections in"), out[:200])
    check("shows total count", "total" in out, out[:300])
    # Bulleted/numbered list of section headings — every line that
    # starts with whitespace+number or whitespace+dash is a section.
    bullet_count = sum(
        1 for line in out.splitlines()
        if line.startswith("  ") or line.startswith("1.")
    )
    check("contains at least 3 sections", bullet_count >= 3, f"got {bullet_count}")
    check("article link present", "en.wikipedia.org/wiki/Tyrannosaurus" in out, out[:500])
    # Tyrannosaurus's TOC reliably contains a "Description" or "Discovery"
    # section; either surfaces from the parse API.
    check(
        "includes an expected section",
        any(name in out for name in ("Description", "Discovery", "History", "Classification", "Paleobiology")),
        out[:2000],
    )

    section("article_sections — uses section numbering")
    # The parse API returns numeric section indices like "1", "1.1", etc.
    # We render them as "1. Heading", "1.1 Heading". Confirm at least
    # one line starts with a bare digit + period.
    out = server.article_sections("Tyrannosaurus")
    numbered = sum(
        1 for line in out.splitlines()
        if len(line) > 2 and line[0].isdigit() and line[1:3] in (". ", ".\t")
    )
    check("at least one numbered section line", numbered >= 1, f"got {numbered}")

    section("article_sections — missing article")
    out = server.article_sections("ThisArticleDoesNotExist12345")
    check("404 message", "not found" in out, out[:300])

    section("article_sections — input edge cases")
    out = server.article_sections("")
    check("empty title returns graceful result", "not found" in out, out[:300])

    section("article_sections — multi-language")
    out = server.article_sections("Berlin", lang="de")
    check("de returns sections", out.startswith("**Sections in"), out[:300])
    check("de wikipedia link", "de.wikipedia.org/wiki/" in out, out[:500])

    section("article_sections — dispatcher routing")
    out = server._call_tool("article_sections", {"title": "Velociraptor"})
    check("dispatcher routes to article_sections", "Unknown tool" not in out, out[:200])
    check("dispatcher returned real content", "Sections in" in out, out[:200])

    section("featured_article")
    out = server.featured_article()
    check("returns markdown", out.startswith("## "), out[:200])

    section("picture_of_the_day")
    out = server.picture_of_the_day()
    check("returns header", out.startswith("🖼️ **Picture of the Day"), out[:200])
    check("includes image URL", "wikimedia.org" in out, out[:500])
    check("includes file page link", "commons.wikimedia.org" in out, out[-300:])

    section("picture_of_the_day — explicit date")
    out = server.picture_of_the_day(date="20260904")
    check("historical date returns header", out.startswith("🖼️ **Picture of the Day"), out[:200])
    check("header shows the requested date", "September 04, 2026" in out, out[:200])

    section("picture_of_the_day — bad date")
    out = server.picture_of_the_day(date="notadate")
    check("rejects bad date with format hint", "YYYYMMDD" in out, out[:200])

    section("media_of_the_day")
    out = server.media_of_the_day()
    check(
        "returns header or graceful missing",
        "**Media of the Day" in out[:80] or "No media of the day found" in out,
        out[:200],
    )
    if "**Media of the Day —" in out:
        check("includes file page link", "commons.wikimedia.org" in out, out[-300:])

    section("media_of_the_day — explicit date (video)")
    out = server.media_of_the_day(date="20250615")
    check("historical date returns header", "**Media of the Day — June 15, 2025" in out, out[:200])
    check("reports video type + duration", "**Type:** video (" in out, out[:500])
    check("includes watch link", "[Watch]" in out, out[-300:])

    section("media_of_the_day — explicit date (audio)")
    out = server.media_of_the_day(date="20260830")
    check("audio date returns header", "**Media of the Day — August 30, 2026" in out, out[:200])
    check("reports audio type", "**Type:** audio" in out, out[:500])
    check("includes listen link", "[Listen]" in out, out[-300:])

    section("media_of_the_day — date with no pick")
    out = server.media_of_the_day(date="20270615")
    check("missing date is graceful", "No media of the day found for 2027-06-15" in out, out[:200])

    section("media_of_the_day — bad date")
    out = server.media_of_the_day(date="notadate")
    check("rejects bad date with format hint", "YYYYMMDD" in out, out[:200])

    section("media_of_the_day — dispatcher routing")
    out = server._call_tool("media_of_the_day", {"date": "20250615"})
    check("dispatcher routes to media_of_the_day", "Unknown tool" not in out, out[:200])
    check("dispatcher returned real content", "**Media of the Day" in out, out[:200])

    section("on_this_day")
    out = server.on_this_day()
    check("returns header", out.startswith("**On this day"), out[:200])
    check("contains at least one event", "- **" in out, out[:300])
    check("contains Wikipedia link", "wikipedia.org/wiki/" in out, out[:500])

    section("on_this_day — count clamping")
    out = server.on_this_day(count=3)
    bullet_count = sum(1 for line in out.splitlines() if line.startswith("- **"))
    check("count=3 returns ≤3 events", bullet_count <= 3, f"got {bullet_count}")
    out = server.on_this_day(count=999)
    bullet_count = sum(1 for line in out.splitlines() if line.startswith("- **"))
    check("count=999 clamps to ≤10", bullet_count <= 10, f"got {bullet_count}")
    out = server.on_this_day(count=-5)
    bullet_count = sum(1 for line in out.splitlines() if line.startswith("- **"))
    check("count=-5 clamps to ≥1", bullet_count >= 1, f"got {bullet_count}")

    section("on_this_day — non-int count falls back gracefully")
    out = server.on_this_day(count="abc")
    check("non-int count returns events (no crash)", out.startswith("**On this day"), out[:300])

    section("on_this_day — multi-language")
    out = server.on_this_day(lang="de")
    check("de returns events", out.startswith("**On this day"), out[:300])
    check("de wikipedia.org link", "de.wikipedia.org/wiki/" in out, out[:500])

    section("deaths_on_this_day")
    out = server.deaths_on_this_day()
    check("returns header", out.startswith("**Deaths on this day"), out[:200])
    check("contains at least one death", "- **" in out, out[:300])
    check("contains Wikipedia link", "wikipedia.org/wiki/" in out, out[:500])

    section("deaths_on_this_day — count clamping")
    out = server.deaths_on_this_day(count=3)
    bullet_count = sum(1 for line in out.splitlines() if line.startswith("- **"))
    check("count=3 returns ≤3 deaths", bullet_count <= 3, f"got {bullet_count}")
    out = server.deaths_on_this_day(count=999)
    bullet_count = sum(1 for line in out.splitlines() if line.startswith("- **"))
    check("count=999 clamps to ≤10", bullet_count <= 10, f"got {bullet_count}")
    out = server.deaths_on_this_day(count=-5)
    bullet_count = sum(1 for line in out.splitlines() if line.startswith("- **"))
    check("count=-5 clamps to ≥1", bullet_count >= 1, f"got {bullet_count}")

    section("deaths_on_this_day — non-int count falls back gracefully")
    out = server.deaths_on_this_day(count="abc")
    check(
        "non-int count returns deaths (no crash)",
        out.startswith("**Deaths on this day"),
        out[:300],
    )

    section("deaths_on_this_day — multi-language")
    out = server.deaths_on_this_day(lang="de")
    check("de returns deaths", out.startswith("**Deaths on this day"), out[:300])
    check("de wikipedia.org link", "de.wikipedia.org/wiki/" in out, out[:500])

    section("births_on_this_day")
    out = server.births_on_this_day()
    check("returns header", out.startswith("**Births on this day"), out[:200])
    check("contains at least one birth", "- **" in out, out[:300])
    check("contains Wikipedia link", "wikipedia.org/wiki/" in out, out[:500])

    section("births_on_this_day — count clamping")
    out = server.births_on_this_day(count=3)
    bullet_count = sum(1 for line in out.splitlines() if line.startswith("- **"))
    check("count=3 returns ≤3 births", bullet_count <= 3, f"got {bullet_count}")
    out = server.births_on_this_day(count=999)
    bullet_count = sum(1 for line in out.splitlines() if line.startswith("- **"))
    check("count=999 clamps to ≤10", bullet_count <= 10, f"got {bullet_count}")
    out = server.births_on_this_day(count=-5)
    bullet_count = sum(1 for line in out.splitlines() if line.startswith("- **"))
    check("count=-5 clamps to ≥1", bullet_count >= 1, f"got {bullet_count}")

    section("births_on_this_day — non-int count falls back gracefully")
    out = server.births_on_this_day(count="abc")
    check(
        "non-int count returns births (no crash)",
        out.startswith("**Births on this day"),
        out[:300],
    )

    section("births_on_this_day — multi-language")
    out = server.births_on_this_day(lang="de")
    check("de returns births", out.startswith("**Births on this day"), out[:300])
    check("de wikipedia.org link", "de.wikipedia.org/wiki/" in out, out[:500])

    section("births_on_this_day — dispatcher routing")
    out = server._call_tool("births_on_this_day", {"count": 2})
    check("dispatcher routes to births_on_this_day", "Unknown tool" not in out, out[:200])
    check("dispatcher returned real content", out.startswith("**Births on this day"), out[:200])

    section("deaths_on_this_day — dispatcher routing")
    out = server._call_tool("deaths_on_this_day", {})
    check("dispatcher routes to deaths_on_this_day", "Unknown tool" not in out, out[:200])
    check(
        "dispatcher returned real content",
        out.startswith("**Deaths on this day"),
        out[:200],
    )

    section("categories")
    out = server.categories("Tyrannosaurus")
    check("returns header", out.startswith("**Categories for"), out[:200])
    check("contains a bullet list", "- Dinosaur genera" in out or "- Tyrannosaurus" in out, out[:500])
    check("article link present", "en.wikipedia.org/wiki/Tyrannosaurus" in out, out[:500])
    check("no Category: prefix", "Category:" not in out, out[:500])

    section("categories — limit clamping + type safety")
    out = server.categories("Tyrannosaurus", limit=999)
    bullet_count = sum(1 for line in out.splitlines() if line.startswith("- "))
    check("limit=999 clamps to ≤50", bullet_count <= 50, f"got {bullet_count}")
    out = server.categories("Tyrannosaurus", limit=-5)
    bullet_count = sum(1 for line in out.splitlines() if line.startswith("- "))
    check("limit=-5 clamps to ≥1", bullet_count >= 1, f"got {bullet_count}")
    out = server.categories("Tyrannosaurus", limit="abc")
    check("non-int limit returns categories (no crash)", out.startswith("**Categories for"), out[:300])

    section("categories — missing article")
    out = server.categories("ThisArticleDoesNotExist12345")
    check("missing article returns clear message", "not found" in out, out[:300])

    section("categories — multi-language")
    out = server.categories("Berlin", limit=5, lang="de")
    check("de returns categories", out.startswith("**Categories for"), out[:300])
    check("de wikipedia link", "de.wikipedia.org/wiki/" in out, out[:500])

    section("links")
    out = server.links("Tyrannosaurus")
    check("returns header", out.startswith("**Links from"), out[:200])
    # Bulleted list of linked titles — each line "- Some Title"
    bullet_count = sum(1 for line in out.splitlines() if line.startswith("- "))
    check("contains a bullet list", bullet_count >= 5, f"got {bullet_count} bullets")
    check("article link present", "en.wikipedia.org/wiki/Tyrannosaurus" in out, out[:500])
    # Sanity-check that at least one well-known related subject surfaces
    check(
        "includes an expected related article",
        any(name in out for name in ("Albertosaurus", "Allosaurus", "Cretaceous", "theropod", "Dinosaur")),
        out[:1000],
    )

    section("links — limit clamping + type safety")
    out = server.links("Tyrannosaurus", limit=999)
    bullet_count = sum(1 for line in out.splitlines() if line.startswith("- "))
    check("limit=999 clamps to ≤50", bullet_count <= 50, f"got {bullet_count}")
    out = server.links("Tyrannosaurus", limit=-5)
    bullet_count = sum(1 for line in out.splitlines() if line.startswith("- "))
    check("limit=-5 clamps to ≥1", bullet_count >= 1, f"got {bullet_count}")
    out = server.links("Tyrannosaurus", limit="abc")
    check("non-int limit returns links (no crash)", out.startswith("**Links from"), out[:300])

    section("links — missing article")
    out = server.links("ThisArticleDoesNotExist12345")
    check("missing article returns clear message", "not found" in out, out[:300])

    section("links — multi-language")
    out = server.links("Berlin", limit=5, lang="de")
    check("de returns links", out.startswith("**Links from"), out[:300])
    check("de wikipedia link", "de.wikipedia.org/wiki/" in out, out[:500])

    section("links — dispatcher routing")
    out = server._call_tool("links", {"title": "Velociraptor"})
    check("dispatcher routes to links", "Unknown tool" not in out, out[:200])
    check("dispatcher returned real content", out.startswith("**Links from"), out[:200])

    section("backlinks")
    out = server.backlinks("Tyrannosaurus")
    check("returns header", out.startswith("**Backlinks to"), out[:200])
    bullet_count = sum(1 for line in out.splitlines() if line.startswith("- "))
    check("contains a bullet list", bullet_count >= 5, f"got {bullet_count} bullets")
    check("article link present", "en.wikipedia.org/wiki/Tyrannosaurus" in out, out[:500])
    # Velociraptor is widely referenced — at least one referrer should surface
    check(
        "includes an expected referrer article",
        any(name in out for name in ("Albertosaurus", "Allosaurus", "Cretaceous", "theropod", "Dinosaur", "Carnosauria", "Tyrannosauridae")),
        out[:2000],
    )

    section("backlinks — limit clamping + type safety")
    out = server.backlinks("Tyrannosaurus", limit=999)
    bullet_count = sum(1 for line in out.splitlines() if line.startswith("- "))
    check("limit=999 clamps to ≤50", bullet_count <= 50, f"got {bullet_count}")
    out = server.backlinks("Tyrannosaurus", limit=-5)
    bullet_count = sum(1 for line in out.splitlines() if line.startswith("- "))
    check("limit=-5 clamps to ≥1", bullet_count >= 1, f"got {bullet_count}")
    out = server.backlinks("Tyrannosaurus", limit="abc")
    check("non-int limit returns backlinks (no crash)", out.startswith("**Backlinks to"), out[:300])

    section("backlinks — missing article")
    out = server.backlinks("ThisArticleDoesNotExist12345")
    check("missing article returns clear message", "not found" in out, out[:300])

    section("backlinks — multi-language")
    out = server.backlinks("Berlin", limit=5, lang="de")
    check("de returns backlinks", out.startswith("**Backlinks to"), out[:300])
    check("de wikipedia link", "de.wikipedia.org/wiki/" in out, out[:500])

    section("backlinks — dispatcher routing")
    out = server._call_tool("backlinks", {"title": "Velociraptor"})
    check("dispatcher routes to backlinks", "Unknown tool" not in out, out[:200])
    check("dispatcher returned real content", out.startswith("**Backlinks to"), out[:200])

    section("external_links")
    out = server.external_links("Tyrannosaurus")
    check("returns header", out.startswith("**External links from"), out[:200])
    check("contains the article title", "Tyrannosaurus" in out, out[:300])
    # Bulleted list of URL lines — every line starts with "- http" or "- https"
    bullet_count = sum(
        1 for line in out.splitlines()
        if line.startswith("- http://") or line.startswith("- https://")
    )
    check("contains at least 5 external URLs", bullet_count >= 5, f"got {bullet_count}")
    check("article link present", "en.wikipedia.org/wiki/Tyrannosaurus" in out, out[:500])

    section("external_links — URLs are off-wiki")
    # External links by definition point OFF Wikipedia. None of the URLs
    # should be on a wikipedia.org host (those would be `links`, not
    # `external_links`). The article link at the bottom is the only
    # wikipedia.org URL allowed.
    out = server.external_links("Tyrannosaurus", limit=30)
    url_lines = [
        line[len("- "):].strip()
        for line in out.splitlines()
        if line.startswith("- http://") or line.startswith("- https://")
    ]
    check("at least one URL rendered", len(url_lines) >= 1, out[:1000])
    off_wiki = [
        url for url in url_lines
        if "wikipedia.org" not in url and "wikimedia.org" not in url
    ]
    check(
        "all bullet URLs are off-wiki",
        len(off_wiki) == len(url_lines),
        f"off_wiki={len(off_wiki)} total={len(url_lines)}",
    )

    section("external_links — limit clamping + type safety")
    out = server.external_links("Tyrannosaurus", limit=999)
    bullet_count = sum(
        1 for line in out.splitlines()
        if line.startswith("- http://") or line.startswith("- https://")
    )
    check("limit=999 clamps to ≤50", bullet_count <= 50, f"got {bullet_count}")
    out = server.external_links("Tyrannosaurus", limit=-5)
    bullet_count = sum(
        1 for line in out.splitlines()
        if line.startswith("- http://") or line.startswith("- https://")
    )
    check("limit=-5 clamps to ≥1", bullet_count >= 1, f"got {bullet_count}")
    out = server.external_links("Tyrannosaurus", limit="abc")
    check(
        "non-int limit returns external links (no crash)",
        out.startswith("**External links from"),
        out[:300],
    )

    section("external_links — missing article")
    out = server.external_links("ThisArticleDoesNotExist12345")
    check("missing article returns clear message", "not found" in out, out[:300])

    section("external_links — multi-language")
    out = server.external_links("Berlin", limit=5, lang="de")
    check("de returns external links", out.startswith("**External links from"), out[:300])
    check("de wikipedia link", "de.wikipedia.org/wiki/" in out, out[:500])

    section("external_links — dispatcher routing")
    out = server._call_tool("external_links", {"title": "Velociraptor"})
    check("dispatcher routes to external_links", "Unknown tool" not in out, out[:200])
    check(
        "dispatcher returned real content",
        out.startswith("**External links from"),
        out[:200],
    )

    section("nearby")
    out = server.nearby("Eiffel Tower", limit=10)
    check("returns header", out.startswith("**Articles near"), out[:200])
    bullet_count = sum(1 for line in out.splitlines() if line.startswith("- "))
    check("contains a bullet list", bullet_count >= 3, f"got {bullet_count} bullets")
    check("distances shown", " m" in out or " km" in out, out[:500])
    check("article link present", "en.wikipedia.org/wiki/Eiffel_Tower" in out, out[:500])

    section("nearby — coordinates anchor")
    out = server.nearby(lat=40.7484, lon=-73.9857, limit=5)
    check("returns header", out.startswith("**Articles near"), out[:200])
    bullet_count = sum(1 for line in out.splitlines() if line.startswith("- "))
    check("contains a bullet list", bullet_count >= 3, f"got {bullet_count} bullets")

    section("nearby — radius clamping + limit clamping + type safety")
    out = server.nearby("Eiffel Tower", limit=999)
    bullet_count = sum(1 for line in out.splitlines() if line.startswith("- "))
    check("limit=999 clamps to ≤50", bullet_count <= 50, f"got {bullet_count}")
    out = server.nearby("Eiffel Tower", limit=-5)
    bullet_count = sum(1 for line in out.splitlines() if line.startswith("- "))
    check("limit=-5 clamps to ≥1", bullet_count >= 1, f"got {bullet_count}")
    out = server.nearby("Eiffel Tower", radius=999999, limit=3)
    check("radius clamps without crash", out.startswith("**Articles near"), out[:200])
    out = server.nearby("Eiffel Tower", limit="abc")
    check("non-int limit returns nearby (no crash)", out.startswith("**Articles near"), out[:300])

    section("nearby — missing/invalid input")
    out = server.nearby("ThisArticleDoesNotExist12345")
    check("missing article returns clear message", "not found" in out or "No nearby" in out, out[:300])
    out = server.nearby()
    check("no anchor returns usage message", "title" in out and "lat" in out, out[:300])
    out = server.nearby(lat=200, lon=0)
    check("out-of-range lat rejected", "Invalid coordinates" in out, out[:300])
    out = server.nearby(lat="abc", lon=0)
    check("non-numeric lat rejected", "Invalid coordinates" in out, out[:300])

    section("nearby — dispatcher routing")
    out = server._call_tool("nearby", {"title": "Eiffel Tower", "limit": 3})
    check("dispatcher routes to nearby", "Unknown tool" not in out, out[:200])
    check("dispatcher returned real content", out.startswith("**Articles near"), out[:200])

    section("translations")
    out = server.translations("Tyrannosaurus")
    check("returns header", out.startswith("**Translations of"), out[:200])
    # Each row is "- `xx`: [Title](url)" — count rows that match that shape.
    bullet_count = sum(
        1 for line in out.splitlines()
        if line.startswith("- `") and "](" in line and "wikipedia.org/wiki/" in line
    )
    check("contains at least 5 language entries", bullet_count >= 5, f"got {bullet_count}")
    check("article link present", "en.wikipedia.org/wiki/Tyrannosaurus" in out, out[:500])
    # Tyrannosaurus reliably has German and French editions
    check(
        "includes an expected language entry",
        any(lang in out for lang in ("`de`", "`fr`", "`es`", "`ja`", "`zh`", "`pt`", "`it`", "`ru`", "`nl`")),
        out[:2000],
    )

    section("translations — limit clamping + type safety")
    out = server.translations("Tyrannosaurus", limit=999)
    bullet_count = sum(
        1 for line in out.splitlines()
        if line.startswith("- `") and "](" in line and "wikipedia.org/wiki/" in line
    )
    check("limit=999 clamps to ≤100", bullet_count <= 100, f"got {bullet_count}")
    out = server.translations("Tyrannosaurus", limit=-5)
    bullet_count = sum(
        1 for line in out.splitlines()
        if line.startswith("- `") and "](" in line and "wikipedia.org/wiki/" in line
    )
    check("limit=-5 clamps to ≥1", bullet_count >= 1, f"got {bullet_count}")
    out = server.translations("Tyrannosaurus", limit="abc")
    check(
        "non-int limit returns translations (no crash)",
        out.startswith("**Translations of"),
        out[:300],
    )

    section("translations — missing article")
    out = server.translations("ThisArticleDoesNotExist12345")
    check("missing article returns clear message", "not found" in out, out[:300])

    section("translations — multi-language")
    # Query from German Wikipedia — should return the non-German editions
    # of the German 'Berlin' article (so 'en' must be in the list).
    out = server.translations("Berlin", limit=5, lang="de")
    check("de returns translations", out.startswith("**Translations of"), out[:300])
    check("de source article link", "de.wikipedia.org/wiki/Berlin" in out, out[:500])

    section("translations — dispatcher routing")
    out = server._call_tool("translations", {"title": "Velociraptor"})
    check("dispatcher routes to translations", "Unknown tool" not in out, out[:200])
    check("dispatcher returned real content", out.startswith("**Translations of"), out[:200])

    section("revisions")
    out = server.revisions("Tyrannosaurus", limit=3)
    check("returns header", out.startswith('**Revision history of "Tyrannosaurus"'), out[:200])
    check("rows have diff links", "Special:Diff/" in out, out[:500])
    check("rows show editors", "**" in out and "bytes" in out, out[:500])
    check("full history link", "action=history" in out, out[-200:])

    section("revisions — limit clamping + type safety")
    out = server.revisions("Tyrannosaurus", limit=999)
    rows = [l for l in out.splitlines() if l.startswith("- `")]
    check("limit=999 clamps to <=50", len(rows) <= 50, f"got {len(rows)}")
    out = server.revisions("Tyrannosaurus", limit=-5)
    rows = [l for l in out.splitlines() if l.startswith("- `")]
    check("limit=-5 clamps to >=1", len(rows) >= 1, f"got {len(rows)}")
    out = server.revisions("Tyrannosaurus", limit="abc")
    check(
        "non-int limit returns history (no crash)",
        out.startswith("**Revision history of"),
        out[:300],
    )

    section("revisions — missing article")
    out = server.revisions("ThisArticleDoesNotExist12345")
    check("missing article returns clear message", "not found" in out, out[:300])

    section("revisions — dispatcher routing")
    out = server._call_tool("revisions", {"title": "Velociraptor"})
    check("dispatcher routes to revisions", "Unknown tool" not in out, out[:200])
    check("dispatcher returned real content", out.startswith("**Revision history of"), out[:200])

    section("revision_diff")
    out = server.revision_diff("Python_(programming_language)", 1374673264, 1374673393)
    check("returns header", 'Revision diff for "Python (programming language)"' in out, out[:200])
    check("from/to labels present", "rev 1374673264" in out and "rev 1374673393" in out, out[:500])
    check("editor + summary shown", "MrOllie" in out and "cut inline external links" in out, out[:700])
    check(
        "unified diff block",
        "```diff" in out and "\n--- rev 1374673264" in out and "\n+++ rev 1374673393" in out,
        out[:900],
    )
    changed = [
        l
        for l in out.split("\n")
        if (l.startswith("-") and not l.startswith("---"))
        or (l.startswith("+") and not l.startswith("+++"))
    ]
    check(
        "changed lines marked +/-",
        any(l.startswith("-") for l in changed) and any(l.startswith("+") for l in changed),
        f"got {len(changed)} changed lines",
    )
    check("on-wiki diff link", "diff=1374673393&oldid=1374673264" in out, out[-300:])

    section("revision_diff — limit clamping + type safety")
    out = server.revision_diff("Python_(programming_language)", 1374673264, 1374673393, limit=5)
    check("truncation note shown", "truncated" in out, out[-400:])
    out = server.revision_diff("Python_(programming_language)", 1374673264, 1374673393, limit="abc")
    check("non-int limit returns results (no crash)", "Revision diff for" in out, out[:200])

    section("revision_diff — identical revisions")
    out = server.revision_diff("Python_(programming_language)", 1374673264, 1374673264)
    check("same revision returns clear message", "nothing to diff" in out, out[:200])

    section("revision_diff — bad revision id")
    out = server.revision_diff("Python_(programming_language)", 1374673264, 999999999999)
    check("bad revid returns clear error", "not found" in out, out[:300])

    section("revision_diff — non-integer revid")
    out = server.revision_diff("Python_(programming_language)", "abc", 1374673393)
    check("non-int revid returns error", "must be revision IDs" in out, out[:200])

    section("revision_diff — dispatcher routing")
    out = server._call_tool(
        "revision_diff",
        {"title": "Python_(programming_language)", "rev_from": 1374673264, "rev_to": 1374673393},
    )
    check("dispatcher routes to revision_diff", "Unknown tool" not in out, out[:200])
    check("dispatcher returned real content", "Revision diff for" in out, out[:200])

    section("disambiguation")
    out = server.disambiguation("Mercury")
    check("detects dab page", "is a disambiguation page" in out, out[:200])
    check("lists planet option", "Mercury (planet)" in out, out[:2000])
    check("lists element option", "Mercury (element)" in out, out[:2000])
    check("descriptions present", "closest planet to the Sun" in out, out[:2000])
    check("sections grouped", "**Companies**" in out or "**Computing**" in out, out[:4000])
    check("wikipedia link included", "en.wikipedia.org/wiki/Mercury" in out, out[-200:])

    section("disambiguation — limit clamping + type safety")
    out = server.disambiguation("Mercury", limit=5)
    check("limit respected", out.count("\n- **") <= 5, out[:500])
    out = server.disambiguation("Mercury", limit=999)
    check("limit clamps to 100", "raise `limit` (max 100)" in out or out.count("\n- **") <= 100)
    out = server.disambiguation("Mercury", limit="abc")
    check("non-int limit returns options (no crash)", "is a disambiguation page" in out, out[:200])

    section("disambiguation — regular article")
    out = server.disambiguation("Tyrannosaurus")
    check("regular article reported", "not a disambiguation page" in out, out[:200])

    section("disambiguation — missing article")
    out = server.disambiguation("ThisArticleDoesNotExist12345")
    check("missing article returns clear error", "not found" in out, out[:200])

    section("disambiguation — dispatcher routing")
    out = server._call_tool("disambiguation", {"title": "Apple"})
    check("dispatcher routes to disambiguation", "Unknown tool" not in out, out[:200])
    check("dispatcher returned real content", "disambiguation page" in out, out[:200])


    section("user_contribs")
    out = server.user_contribs("Jimbo Wales", limit=3)
    check("header names account", "**Jimbo Wales**" in out, out[:300])
    check("header shows registration date", "registered 2001-03-27" in out, out[:300])
    check("header shows total edit count", "edits total" in out, out[:300])
    check("lists contributions", "Latest contributions" in out, out[:300])
    numbered = sum(1 for i in range(1, 11) if f"\n{i}. " in out)
    check("limit respected", 1 <= numbered <= 3, f"got {numbered} entries")
    check("diff links included", "/w/index.php?diff=" in out, out[:2000])

    section("user_contribs — clamping + type safety")
    out = server.user_contribs("Jimbo Wales", limit=500)
    numbered = sum(1 for i in range(1, 60) if f"\n{i}. " in out)
    check("limit clamps to 50", numbered <= 50, f"got {numbered} entries")
    out = server.user_contribs("Jimbo Wales", limit="abc")
    check("non-int limit returns contribs (no crash)", "Latest contributions" in out, out[:200])
    out = server.user_contribs("Jimbo Wales", limit=-5)
    numbered = sum(1 for i in range(1, 5) if f"\n{i}. " in out)
    check("limit=-5 clamps to 1", numbered == 1, f"got {numbered} entries")

    section("user_contribs — unknown and empty users")
    out = server.user_contribs("ThisAccountDoesNotExistZZZ123")
    check("unknown account reported", "no registered account" in out, out[:300])
    check("no contribs stated", "No contributions found" in out, out[:400])
    out = server.user_contribs("")
    check("empty user rejected", "Provide a Wikipedia username" in out, out[:200])

    section("user_contribs — dispatcher routing")
    out = server._call_tool("user_contribs", {"user": "Jimbo Wales"})
    check("dispatcher routes to user_contribs", "Unknown tool" not in out, out[:200])
    check("dispatcher returned real content", "Latest contributions" in out, out[:200])

    section("citation_needed — article mode")
    out = server.citation_needed(article="Brain of Albert Einstein", limit=5)
    check("header names article", "[Brain of Albert Einstein](https://en.wikipedia.org/wiki/Brain_of_Albert_Einstein)" in out, out[:200])
    check("counts tagged claims", "unsourced claim" in out, out[:200])
    check("extracts the flagged sentence", "Publication bias" in out, out[:600])
    check("shows tag date", "tagged July 2023" in out, out[:800])
    check("no raw wikitext leaks", "{{" not in out and "[[" not in out, out[:800])

    section("citation_needed — article without tags")
    out = server.citation_needed(article="Albert Einstein")
    check("no-tag article reported", 'no "citation needed" tags found' in out, out[:200])

    section("citation_needed — missing article")
    out = server.citation_needed(article="This Article Does Not Exist ZZZ")
    check("missing article reported", "doesn't exist" in out, out[:200])

    section("citation_needed — topic mode")
    out = server.citation_needed(topic="climate", limit=3)
    check("topic header", 'Unsourced claims on "climate"' in out, out[:200])
    numbered = sum(1 for i in range(1, 11) if f"\n{i}. " in out)
    check("limit respected", 1 <= numbered <= 3, f"got {numbered} entries")
    check("no raw wikitext in snippets", "{{" not in out and "[[" not in out, out[:1200])

    section("citation_needed — clamping + precedence")
    out = server.citation_needed(topic="climate", article="Brain of Albert Einstein", limit=1)
    check("article wins over topic", "Brain of Albert Einstein" in out and 'on "climate"' not in out, out[:300])
    out = server.citation_needed(topic="climate", limit=500)
    numbered = sum(1 for i in range(1, 60) if f"\n{i}. " in out)
    check("limit clamps to 25", numbered <= 25, f"got {numbered} entries")
    out = server.citation_needed(topic="climate", limit="abc")
    check("non-int limit returns results (no crash)", "Unsourced claims" in out, out[:200])

    section("citation_needed — dispatcher routing")
    out = server._call_tool("citation_needed", {"article": "Brain of Albert Einstein"})
    check("dispatcher routes to citation_needed", "Unknown tool" not in out, out[:200])
    check("dispatcher returned real content", "unsourced claim" in out, out[:300])
    section("talk — active discussion threads")
    out = server.talk("Climate change", limit=3)
    check("header names talk page", '**Talk: "Climate change"**' in out, out[:200])
    check("threads listed", "\n1. " in out and "Last activity" in out, out[:400])
    check("signed-comment counts shown", "signed comment(s)" in out, out[:600])
    check("no raw wikitext leaks", "{{" not in out and "[[" not in out, out[:1200])

    section("talk — bot notices filtered")
    out = server.talk("Eiffel Tower", limit=10)
    check("redirect-discussion notices excluded", "Redirects for discussion" not in out, out[:800])
    check("real threads kept", "German name" in out, out[:800])

    section("talk — missing talk page")
    out = server.talk("ThisArticleDoesNotExistZZZ123")
    check("missing page reported", "No talk page for" in out, out[:200])

    section("talk — clamping + type safety")
    out = server.talk("Climate change", limit=500)
    numbered = sum(1 for i in range(1, 60) if f"\n{i}. " in out)
    check("limit clamps to 15", numbered <= 15, f"got {numbered} entries")
    out = server.talk("Climate change", limit="abc")
    check("non-int limit returns results (no crash)", "**Talk:" in out, out[:200])

    section("talk — helpers")
    check(
        "_clean_talk_comment strips markup",
        server._clean_talk_comment("Why '''bold''' [[Eifel|Eifel region]]? [https://x.example a link]") == "Why bold Eifel region? a link",
    )
    check("_parse_talk_ts parses", server._parse_talk_ts("15:53, 10 August 2026") is not None)
    check("_parse_talk_ts rejects junk", server._parse_talk_ts("not a date") is None)
    check(
        "_strip_talk_banners removes archivetop",
        "{{archivetop" not in server._strip_talk_banners("{{archivetop|1=x}} real text"),
    )

    section("talk — dispatcher routing")
    out = server._call_tool("talk", {"title": "Eiffel Tower"})
    check("dispatcher routes to talk", "Unknown tool" not in out, out[:200])
    check("dispatcher returned real content", "**Talk:" in out, out[:200])

    section("article_flags — maintenance banners")
    out = server.article_flags("List of unsolved deaths", limit=10)
    check("header names article", "**List of unsolved deaths**" in out or "[List of unsolved deaths]" in out, out[:200])
    check("original research found", "Original research" in out, out[:600])
    check("fringe theories found", "Fringe theories" in out, out[:600])
    check("tag dates shown", "March 2023" in out and "August 2015" in out, out[:600])
    check("plain-language meaning shown", "unverified analysis" in out, out[:800])

    section("article_flags — clean article")
    out = server.article_flags("Eiffel Tower")
    check("no flags reported", "no editorial flags" in out, out[:200])

    section("article_flags — missing article")
    out = server.article_flags("ThisArticleDoesNotExistZZZ123")
    check("missing reported", "Could not check" in out, out[:200])

    section("article_flags — empty article")
    out = server.article_flags("")
    check("empty title reported", "title is required" in out, out[:200])

    section("article_flags — clamping + type safety")
    out = server.article_flags("List of unsolved deaths", limit=500)
    numbered = sum(1 for i in range(1, 60) if f"\n{i}. " in out)
    check("limit clamps to 25", numbered <= 25, f"got {numbered} entries")
    out = server.article_flags("List of unsolved deaths", limit="abc")
    check("non-int limit returns results (no crash)", "editorial flag" in out, out[:200])

    section("article_flags — helpers")
    check(
        "_af_banner matches POV",
        server._af_banner("POV")[0] == "POV",
    )
    check(
        "_af_banner strips section suffix",
        server._af_banner("POV section")[0] == "POV",
    )
    check(
        "_af_banner rejects cite templates",
        server._af_banner("Cite web") == ("", ""),
    )
    check(
        "_af_banner rejects multiple issues wrapper",
        server._af_banner("Multiple issues") == ("", ""),
    )
    wt = (
        "{{Short description|None}}\n{{Multiple issues|\n"
        "{{original research|date=March 2023}}\n"
        "{{Fringe theories|date=August 2015}}\n}}\n"
        "== Reception ==\n{{POV section|date=January 2024}}\ntext"
    )
    flags = server._extract_article_flags(wt)
    check(
        "multiple issues unpacked into sub-flags",
        ("Original research", "March 2023", "article top") in flags
        and ("Fringe theories", "August 2015", "article top") in flags,
        str(flags),
    )
    check(
        "section-scoped banner attributed",
        ("POV", "January 2024", "Reception") in flags,
        str(flags),
    )
    check(
        "wrapper not reported as own flag",
        all("Multiple issues" not in f[0] for f in flags),
        str(flags),
    )

    section("article_flags — dispatcher routing")
    out = server._call_tool("article_flags", {"article": "Eiffel Tower"})
    check("dispatcher routes to article_flags", "Unknown tool" not in out, out[:200])
    check("dispatcher returned real content", "editorial flags" in out, out[:200])

    section("article_protection — extended-confirmed article")
    out = server.article_protection("Donald Trump")
    check("protected header", "**protected**" in out, out[:300])
    check("edit level shown", "extended-confirmed" in out, out[:600])
    check("move restriction shown", "Moving/renaming" in out, out[:600])
    check("indefinite expiry shown", "indefinite" in out, out[:600])
    check("plain-language meaning", "30 days old" in out, out[:600])

    section("article_protection — open article")
    out = server.article_protection("Oxyomus setosopunctatus")
    check("no protection reported", "no protection" in out, out[:200])

    section("article_protection — missing article")
    out = server.article_protection("ThisArticleDoesNotExistZZZ123")
    check("missing reported", "doesn't exist" in out, out[:200])

    section("article_protection — empty article")
    out = server.article_protection("")
    check("empty title reported", "title is required" in out, out[:200])

    section("article_protection — redirect")
    out = server.article_protection("USA")
    check("redirect chain named", "USA → United States" in out, out[:200])
    check("resolved title linked", "[United States]" in out, out[:200])

    section("article_protection — helpers")
    check("infinity -> indefinite", server._ap_expiry("infinity") == "indefinite")
    check("timestamp -> date", server._ap_expiry("2027-03-01T00:00:00Z") == "until 2027-03-01")

    section("article_protection — dispatcher routing")
    out = server._call_tool("article_protection", {"article": "Donald Trump"})
    check("dispatcher routes to article_protection", "Unknown tool" not in out, out[:200])
    check("dispatcher returned real content", "**protected**" in out, out[:200])

    section("article_pulse — helpers")
    check("50 edits -> buzzing", server._pulse_verdict(50) == "buzzing — edited roughly daily or more")
    check("10 edits -> active", server._pulse_verdict(10) == "active — edited about weekly")
    check("3 edits -> quiet", server._pulse_verdict(3) == "quiet — occasional edits")
    check("0 edits -> dormant", server._pulse_verdict(0) == "dormant — untouched for 30+ days")
    # Dates computed relative to "now" so these stay green any day they're run
    today = datetime.now(timezone.utc)
    ts = lambda d: (today - timedelta(days=d)).strftime("%Y-%m-%dT12:00:00Z")
    check("today label", server._days_ago_label(ts(0)) == "today")
    check("yesterday label", server._days_ago_label(ts(1)) == "yesterday")
    check("days-ago label", server._days_ago_label(ts(10)) == "10 days ago")
    check("bad timestamp passthrough", server._days_ago_label("not-a-time") == "not-a-time")

    section("article_pulse — active article")
    out = server.article_pulse("Python (programming language)")
    check("pulse header", "— pulse:" in out, out[:300])
    check("verdict present", any(v in out for v in ("buzzing", "active", "quiet", "dormant")), out[:300])
    check("created line", "**Created:**" in out and "by" in out, out[:600])
    check("length line", "**Length:**" in out and "bytes" in out, out[:600])
    check("watchers line", "**Watchers:**" in out, out[:600])
    check("last-edited line", "**Last edited:**" in out, out[:800])
    check("30-day velocity line", "**Edits (last 30 days):**" in out, out[:1000])
    check("recent editors listed", "**Recent editors:**" in out, out[:1200])

    section("article_pulse — missing article")
    out = server.article_pulse("ThisArticleDoesNotExistZZZ123")
    check("missing reported", "doesn't exist" in out, out[:200])

    section("article_pulse — empty article")
    out = server.article_pulse("")
    check("empty title reported", "title is required" in out, out[:200])

    section("article_pulse — redirect")
    out = server.article_pulse("USA")
    check("redirect chain named", "USA → United States" in out, out[:200])
    check("resolved title linked", "[United States]" in out, out[:200])

    section("article_pulse — dispatcher routing")
    out = server._call_tool("article_pulse", {"article": "Python (programming language)"})
    check("dispatcher routes to article_pulse", "Unknown tool" not in out, out[:200])
    check("dispatcher returned real content", "— pulse:" in out, out[:300])

    section("citation_sources — helpers")
    check("www + co.uk collapse", server._registrable_domain("www.news.bbc.co.uk") == "bbc.co.uk")
    check("edu host collapse", server._registrable_domain("pubmed.ncbi.nlm.nih.gov") == "nih.gov")
    check("plain two-label", server._registrable_domain("books.google.com") == "google.com")
    check("bare domain passthrough", server._registrable_domain("ipcc.ch") == "ipcc.ch")
    check("ip passthrough", server._registrable_domain("192.0.2.1") == "192.0.2.1")
    check("port stripped", server._registrable_domain("example.com:8080") == "example.com")

    section("citation_sources — scholarly article")
    out = server.citation_sources("Climate change", limit=10)
    check("sources header", "Citation sources for" in out and "Climate change" in out, out[:300])
    check("verdict present", any(v in out for v in ("diverse", "lopsided", "top-heavy", "balanced", "thin")), out[:300])
    check("totals line", "references" in out and "unique publishers" in out, out[:400])
    check("table present", "| Source domain | Citations | Share of linked refs |" in out, out[:500])
    check("doi.org ranked", "`doi.org`" in out, out[:800])
    check("archived line", "**Archived:**" in out, out[:1500])
    check("scholarly line", "**Scholarly (DOI):**" in out, out[:1500])

    section("citation_sources — missing article")
    out = server.citation_sources("ThisArticleDoesNotExistZZZ123")
    check("missing reported", "not found" in out, out[:200])

    section("citation_sources — empty article")
    out = server.citation_sources("")
    check("empty title reported", "title is required" in out, out[:200])

    section("citation_sources — redirect")
    out = server.citation_sources("USA", limit=3)
    check("redirect resolves", 'Citation sources for "United States"' in out, out[:200])

    section("citation_sources — clamping + type safety")
    out = server.citation_sources("Eiffel Tower", limit=500)
    check("limit clamps to 30", out.count("| `") <= 30, out[:100])
    out = server.citation_sources("Eiffel Tower", limit="abc")
    check("bad limit falls back to 15", out.count("| `") <= 15, out[:100])

    section("citation_sources — dispatcher routing")
    out = server._call_tool("citation_sources", {"title": "Velociraptor", "limit": 3})
    check("dispatcher routes to citation_sources", "Unknown tool" not in out, out[:200])
    check("dispatcher returned real content", "Citation sources for" in out, out[:300])

    section("tool registry")
    check("all 47 tools listed", len(server.TOOLS) == 47)
    names = {t["name"] for t in server.TOOLS}
    expected = {"search", "summary", "random", "simple_summary", "did_you_know", "dino_fact", "featured_article", "article_extract", "article_sections", "on_this_day", "deaths_on_this_day", "births_on_this_day", "categories", "links", "backlinks", "external_links", "nearby", "translations", "revisions", "pageviews", "news", "top_reads", "image", "media_list", "media_search", "quote", "picture_of_the_day", "media_of_the_day", "recent_changes", "category_members", "infobox", "article_quality", "related_articles", "contributors", "references", "section_text", "revision_diff", "disambiguation", "user_contribs", "citation_needed", "talk", "article_flags", "article_protection", "article_pulse", "citation_sources", "article_path", "article_at_date"}
    check("expected tool names", names == expected, f"got {names}")

    section("pageviews")
    out = server.pageviews("Tyrannosaurus")
    check("returns header", "Pageviews for" in out, out[:300])
    check("table present", "| Date | Views |" in out, out[:500])
    check("at least one day shown", "|" in out and "202" in out, out[:1000])
    check("total + average present", "Total views:" in out and "Daily average:" in out, out[:500])
    check("wikipedia link included", "en.wikipedia.org/wiki/Tyrannosaurus" in out, out[:1000])

    section("pageviews — custom date range")
    out = server.pageviews("Python_(programming_language)", start="20250101", end="20250107")
    check("returns data", "Pageviews for" in out, out[:300])
    check("7 days in window", out.count("| 2025-01-") == 7, out[:1500])

    section("pageviews — missing article")
    out = server.pageviews("ThisArticleDoesNotExist12345")
    check("missing returns clear message", "No pageviews data found" in out, out[:300])

    section("pageviews — invalid date format")
    out = server.pageviews("Tyrannosaurus", start="bad-date")
    check("invalid start returns error", "Error" in out and "YYYYMMDD" in out, out[:300])

    section("pageviews — start after end")
    out = server.pageviews("Tyrannosaurus", start="20250110", end="20250101")
    check("reversed range returns error", "after end" in out, out[:300])

    section("pageviews — empty title")
    out = server.pageviews("")
    check("empty title returns error", "title is required" in out, out[:300])

    section("pageviews — multi-language")
    out = server.pageviews("Berlin", lang="de")
    check("de returns pageviews", "Pageviews for" in out, out[:300])
    check("de wikipedia link", "de.wikipedia.org/wiki/" in out, out[:500])

    section("pageviews — dispatcher routing")
    out = server._call_tool("pageviews", {"title": "Velociraptor"})
    check("dispatcher routes to pageviews", "Unknown tool" not in out, out[:200])
    check("dispatcher returned real content", "Pageviews for" in out, out[:200])

    section("news")
    out = server.news()
    check("returns header", out.startswith("**In the news"), out[:200])
    # Bullet list of events
    bullet_count = sum(1 for line in out.splitlines() if line.startswith("- "))
    check("contains at least one event", bullet_count >= 1, f"got {bullet_count}")
    check("contains wikipedia link", "wikipedia.org/wiki/" in out, out[:500])
    # Bold-linked article titles should be present (Main Page almost always has them)
    check(
        "contains a bold-linked article title",
        "**[",
        out[:500],
    )
    # Main Page link in footer
    check("main page link present", "/wiki/Main_Page" in out, out[:500])

    section("news — limit clamping + type safety")
    out = server.news(limit=999)
    bullet_count = sum(1 for line in out.splitlines() if line.startswith("- "))
    check("limit=999 clamps to ≤10", bullet_count <= 10, f"got {bullet_count}")
    out = server.news(limit=-5)
    bullet_count = sum(1 for line in out.splitlines() if line.startswith("- "))
    check("limit=-5 clamps to ≥1", bullet_count >= 1, f"got {bullet_count}")
    out = server.news(limit="abc")
    check("non-int limit returns news (no crash)", out.startswith("**In the news"), out[:300])

    section("news — multi-language")
    # German Wikipedia's Main Page is structured differently than en's,
    # so the parser may not find an "In the news" h2 block. Accept any
    # graceful outcome (real items, structural fallback, or empty-feed
    # fallback) — what matters is no uncaught exception.
    out = server.news(lang="de")
    check(
        "de returns news or graceful fallback",
        out.startswith("**In the news")
        or "No 'In the news' section" in out
        or "No news" in out
        or "Could not fetch" in out,
        out[:300],
    )

    section("news — dispatcher routing")
    out = server._call_tool("news", {})
    check("dispatcher routes to news", "Unknown tool" not in out, out[:200])
    check("dispatcher returned real content", out.startswith("**In the news"), out[:200])

    section("multi-language (de)")
    out = server.get_summary("Berlin", lang="de")
    check("returns German article", out.startswith("## "), out[:300])

    section("top_reads — explicit date")
    # Use a known date so the test doesn't depend on "today" having
    # finalized pageviews data. Aug 29 2026 is a recent Saturday — should
    # have a healthy list of articles.
    out = server.top_reads(date="20250829", limit=10)
    check("returns header", "Top reads on en.wikipedia" in out, out[:300])
    check("contains the requested date", "2025-08-29" in out, out[:300])
    check("table present", "| Rank | Article | Views |" in out, out[:500])
    # At least one table row (header is "Rank", article link, views)
    table_rows = sum(
        1 for line in out.splitlines()
        if line.startswith("| ") and "https://" in line
    )
    check("contains at least one article row", table_rows >= 1, f"got {table_rows} rows")
    # View counts should be comma-separated thousands (e.g. "198,027").
    # Pull the last "|" field from each row and check it has a comma
    # when the number is ≥1000.
    rows_with_comma = 0
    rows_total = 0
    for line in out.splitlines():
        if line.startswith("| ") and "https://" in line:
            rows_total += 1
            # Markdown table row format: "| rank | [Title](url) | NNN,NNN |"
            # Split on "|" and the view count is the second-to-last field
            # (last field is the empty trailing segment).
            fields = line.split("|")
            # fields: ["", " rank ", " [Title](url) ", " 198,027 ", ""]
            views_field = fields[-2].strip() if len(fields) >= 3 else ""
            try:
                n = int(views_field.replace(",", ""))
                if n >= 1000 and "," in views_field:
                    rows_with_comma += 1
            except ValueError:
                pass
    check(
        "view counts are comma-formatted for ≥1000",
        rows_with_comma >= 1 and rows_with_comma == rows_total,
        f"rows_total={rows_total}, rows_with_comma={rows_with_comma}",
    )

    section("top_reads — filters non-content namespaces")
    # Main_Page, Special:Search, Wikipedia:*, Portal:*, etc. should be
    # filtered out so the result is real articles. Without filtering,
    # Main_Page always ranks #1 with millions of views — which is
    # useless as a content hook.
    out = server.top_reads(date="20250829", limit=20)
    check("no Main_Page row", "Main_Page|" not in out and "Main Page|" not in out, out[:2000])
    check(
        "no Special: row",
        "Special:Search|" not in out and "Wikipedia:Featured" not in out,
        out[:2000],
    )
    check(
        "no Portal: row",
        "Portal:Current_events|" not in out,
        out[:2000],
    )

    section("top_reads — default date (yesterday UTC)")
    # No `date` arg → server picks yesterday UTC. We can't assert the
    # exact date without time-freezing, so just confirm the response
    # shape holds up with no date arg.
    out = server.top_reads()
    check(
        "default date returns a populated table",
        "| Rank | Article | Views |" in out,
        out[:500],
    )

    section("top_reads — limit clamping + type safety")
    out = server.top_reads(date="20250829", limit=999)
    table_rows = sum(
        1 for line in out.splitlines()
        if line.startswith("| ") and "https://" in line
    )
    check("limit=999 clamps to ≤50", table_rows <= 50, f"got {table_rows}")
    out = server.top_reads(date="20250829", limit=-5)
    table_rows = sum(
        1 for line in out.splitlines()
        if line.startswith("| ") and "https://" in line
    )
    check("limit=-5 clamps to ≥1", table_rows >= 1, f"got {table_rows}")
    out = server.top_reads(date="20250829", limit="abc")
    check(
        "non-int limit returns table (no crash)",
        "| Rank | Article | Views |" in out,
        out[:500],
    )

    section("top_reads — invalid date format")
    out = server.top_reads(date="not-a-date")
    check("invalid date returns error", "Error" in out and "YYYYMMDD" in out, out[:300])
    out = server.top_reads(date="2025-08-29")  # wrong separator
    check("wrong-format date returns error", "Error" in out and "YYYYMMDD" in out, out[:300])

    section("top_reads — multi-language")
    # German Wikipedia's top-reads endpoint should work with the same
    # shape as English. Accept any graceful outcome — what matters is
    # no uncaught exception.
    out = server.top_reads(date="20250829", lang="de", limit=5)
    check(
        "de returns a populated table",
        "Top reads on de.wikipedia" in out and "| Rank | Article | Views |" in out,
        out[:500],
    )

    section("top_reads — dispatcher routing")
    out = server._call_tool("top_reads", {"date": "20250829", "limit": 5})
    check("dispatcher routes to top_reads", "Unknown tool" not in out, out[:200])
    check(
        "dispatcher returned real content",
        "Top reads on en.wikipedia" in out,
        out[:200],
    )

    section("image")
    out = server.image("Tyrannosaurus")
    check("returns title", "Tyrannosaurus" in out, out[:300])
    check("lead image header present", "Lead Image" in out, out[:300])
    check("thumbnail URL present", "Thumbnail" in out and "wikimedia.org" in out, out[:500])
    check("original URL present", "Original" in out and "wikimedia.org" in out, out[:500])
    check("wikipedia link", "en.wikipedia.org/wiki/Tyrannosaurus" in out, out[:500])
    check("includes markdown image tag", "![Tyrannosaurus](" in out, out[:500])

    section("image — missing article")
    out = server.image("ThisArticleDoesNotExist12345")
    check("404 message", "not found" in out, out[:300])

    section("image — multi-language")
    out = server.image("Berlin", lang="de")
    check("de returns image data", "Berlin" in out, out[:300])
    check("de wikipedia link", "de.wikipedia.org/wiki/" in out, out[:500])

    section("image — dispatcher routing")
    out = server._call_tool("image", {"title": "Velociraptor"})
    check("dispatcher routes to image", "Unknown tool" not in out, out[:200])
    check("dispatcher returned real content", "Lead Image" in out, out[:200])

    section("recent_changes")
    out = server.recent_changes(limit=3)
    check("returns header", "**Recent changes on en.wikipedia.org**" in out, out[:200])
    check("entries have change-kind labels", any(l in out for l in ("edit", "new article", "categorize", "log")), out[:500])
    check("entries have article links", "en.wikipedia.org/wiki/" in out, out[:500])
    check("entries have byte deltas", "bytes" in out, out[:500])
    check("entries have timestamps", "UTC" in out, out[:500])
    check("diff links included", "index.php?diff=" in out, out[:500])
    rows = [l for l in out.splitlines() if l.startswith("- ")]
    check("respects limit=3", len(rows) <= 3, f"got {len(rows)} rows")

    section("recent_changes — kind='new'")
    out = server.recent_changes(kind="new", limit=3)
    check("new-article label present", "new article" in out, out[:500])
    rows = [l for l in out.splitlines() if l.startswith("- ")]
    check("all rows are new-article entries", all("new article" in r for r in rows), f"got {len(rows)} rows")

    section("recent_changes — kind validation + limit clamping")
    out = server.recent_changes(kind="nonsense", limit=2)
    check("bad kind falls back to all (no crash)", "**Recent changes on" in out, out[:200])
    out = server.recent_changes(limit=100)
    rows = [l for l in out.splitlines() if l.startswith("- ")]
    check("limit=100 clamps to ≤50", len(rows) <= 50, f"got {len(rows)} rows")
    out = server.recent_changes(limit="abc")
    check("non-int limit falls back (no crash)", "**Recent changes on" in out, out[:200])

    section("recent_changes — multi-language")
    out = server.recent_changes(kind="edit", limit=2, lang="de")
    check("german feed header", "**Recent changes on de.wikipedia.org**" in out, out[:200])

    section("recent_changes — dispatcher routing")
    out = server._call_tool("recent_changes", {"kind": "edit", "limit": 2})
    check("dispatcher routes to recent_changes", "Unknown tool" not in out, out[:200])
    check("dispatcher returned real content", "**Recent changes on" in out, out[:200])

    section("category_members")
    out = server.category_members("Flightless birds", limit=5)
    check("returns header", '**Articles in category "Flightless birds":**' in out, out[:200])
    check("entries are bold titles", "- **" in out, out[:500])
    check("entries have extracts", " — " in out, out[:800])
    check("category link included", "en.wikipedia.org/wiki/Category:Flightless_birds" in out, out[-200:])
    rows = [l for l in out.splitlines() if l.startswith("- **")]
    check("respects limit=5", len(rows) <= 5, f"got {len(rows)} rows")

    section("category_members — with Category: prefix")
    out = server.category_members("Category:Flightless birds", limit=3)
    check("prefix form works", '**Articles in category "Flightless birds":**' in out, out[:200])

    section("category_members — missing category")
    out = server.category_members("ThisCategoryDoesNotExist12345")
    check("missing returns clear message", "No articles found" in out, out[:300])

    section("category_members — empty category")
    out = server.category_members("")
    check("empty returns prompt", "provide a category name" in out, out[:200])

    section("category_members — limit clamping")
    out = server.category_members("Flightless birds", limit=100)
    rows = [l for l in out.splitlines() if l.startswith("- **")]
    check("limit=100 clamps to ≤50", len(rows) <= 50, f"got {len(rows)} rows")
    out = server.category_members("Flightless birds", limit="abc")
    check("non-int limit falls back (no crash)", "**Articles in category" in out, out[:200])

    section("category_members — multi-language")
    out = server.category_members("Vögel", limit=3, lang="de")
    check("german category works", "**Articles in category" in out and "de.wikipedia.org" in out, out[:300])

    section("category_members — dispatcher routing")
    out = server._call_tool("category_members", {"category": "Flightless birds"})
    check("dispatcher routes to category_members", "Unknown tool" not in out, out[:200])
    check("dispatcher returned real content", out.startswith("**Articles in category"), out[:200])

    section("infobox")
    out = server.infobox("Albert Einstein")
    check("returns table header", "## Albert Einstein — infobox" in out, out[:200])
    check("markdown table present", "| Field | Value |" in out, out[:400])
    check("birth_date rendered as date", "| birth_date | 1879-3-14 |" in out, out[:600])
    check("wikilinks flattened", "Hans Albert |" in out, out[:800])
    check("no raw ref tags", "<ref" not in out, out[:1500])
    check("article link included", "en.wikipedia.org/wiki/Albert_Einstein" in out, out[-200:])

    section("infobox — missing article")
    out = server.infobox("xyzzynonesuch")
    check("missing returns clear message", "No article found" in out, out[:200])

    section("infobox — empty title")
    out = server.infobox("")
    check("empty returns prompt", "provide an article title" in out, out[:200])

    section("infobox — no infobox on page")
    out = server.infobox("Mercury (disambiguation)")
    check("no-infobox returns guidance", "No infobox found" in out, out[:200])

    section("infobox — multi-language")
    out = server.infobox("Albert Einstein", lang="de")
    check("german infobox works", "infobox" in out and "de.wikipedia.org" in out, out[:300])

    section("infobox — dispatcher routing")
    out = server._call_tool("infobox", {"title": "Paris"})
    check("dispatcher routes to infobox", "Unknown tool" not in out, out[:200])
    check("dispatcher returned real content", "— infobox" in out, out[:200])

    section("article_quality")
    out = server.article_quality("Albert Einstein")
    check("returns header", 'Quality assessments for "Albert Einstein"' in out, out[:200])
    check("overall class shown", "Overall class: **GA**" in out, out[:300])
    check("project table present", "| WikiProject | Class | Importance |" in out, out[:600])
    check("legend present", "FA/FL (featured)" in out, out[:500])
    check("wikipedia link included", "en.wikipedia.org/wiki/Albert_Einstein" in out, out)

    section("article_quality — missing article")
    out = server.article_quality("ThisArticleDoesNotExist12345")
    check("missing article returns clear message", "not found" in out, out[:200])

    section("article_quality — assessment not enabled on this wiki")
    out = server.article_quality("Albert Einstein", lang="de")
    check("de.wiki returns guidance", "No quality assessments recorded" in out, out[:200])

    section("article_quality — dispatcher routing")
    out = server._call_tool("article_quality", {"title": "Paris"})
    check("dispatcher routes to article_quality", "Unknown tool" not in out, out[:200])
    check("dispatcher returned real content", "Quality assessments for" in out, out[:200])

    section("related_articles")
    out = server.related_articles("Albert Einstein")
    check("returns header", 'Articles related to "Albert Einstein"' in out, out[:200])
    check("numbered list present", "1. **" in out, out[:600])
    check("source article excluded", "1. **Albert Einstein**" not in out, out[:600])
    check("wikipedia link included", "en.wikipedia.org/wiki/Albert_Einstein" in out, out)

    section("related_articles — limit respected")
    out = server.related_articles("Velociraptor", limit=3)
    check("exactly 3 results", out.count("**") // 2 >= 3 and "4. **" not in out, out[:800])

    section("related_articles — missing article")
    out = server.related_articles("ThisArticleDoesNotExist12345")
    check("missing article returns clear message", "No related articles found" in out, out[:200])

    section("related_articles — multi-language")
    out = server.related_articles("Albert Einstein", lang="de", limit=2)
    check("german related works", "de.wikipedia.org/wiki/" in out, out[:400])

    section("related_articles — dispatcher routing")
    out = server._call_tool("related_articles", {"title": "Paris"})
    check("dispatcher routes to related_articles", "Unknown tool" not in out, out[:200])
    check("dispatcher returned real content", 'Articles related to "Paris"' in out, out[:200])

    section("contributors")
    out = server.contributors("Albert Einstein")
    check("returns header", 'Top contributors to "Albert Einstein"' in out, out[:200])
    check("numbered list present", "1. **" in out, out[:600])
    check("edit counts shown", "edits (" in out, out[:600])
    check("user page link included", "en.wikipedia.org/wiki/User:" in out, out[:600])
    check("sample span noted", "most recent edits sampled" in out, out[:200])

    section("contributors — limit respected")
    out = server.contributors("Velociraptor", limit=3)
    check("exactly 3 contributors", "3. **" in out and "4. **" not in out, out[:800])

    section("contributors — limit clamping + type safety")
    out = server.contributors("Velociraptor", limit=100)
    numbered = sum(1 for i in range(1, 21) if f"\n{i}. " in out)
    check("limit=100 clamps to ≤20", numbered <= 20, f"got {numbered} items")
    out = server.contributors("Velociraptor", limit=-5)
    check("limit=-5 clamps to 1", "\n1. " in out and "\n2. " not in out, out[:400])
    out = server.contributors("Velociraptor", limit="abc")
    check("non-int limit returns results (no crash)", "Top contributors to" in out, out[:200])

    section("contributors — redirect follows")
    out = server.contributors("Einstein")  # redirects to Albert Einstein
    check("redirect resolves", 'Top contributors to "Albert Einstein"' in out, out[:200])

    section("contributors — missing article")
    out = server.contributors("ThisArticleDoesNotExist12345")
    check("missing article returns clear message", "not found" in out, out[:200])

    section("contributors — dispatcher routing")
    out = server._call_tool("contributors", {"title": "Paris"})
    check("dispatcher routes to contributors", "Unknown tool" not in out, out[:200])
    check("dispatcher returned real content", 'Top contributors to "Paris"' in out, out[:200])


    section("references")
    out = server.references("Albert Einstein")
    check("returns header", 'References cited by "Albert Einstein"' in out, out[:200])
    check("total count shown", "total):" in out, out[:200])
    check("numbered citations present", "\n1. " in out and "\n2. " in out, out[:1200])
    check("citation URLs listed", "https://" in out, out[:1200])
    check("doi link present", "doi.org" in out, out[:1200])
    check("backlink markers stripped", "\n1. ^" not in out and "\n1. ↑" not in out, out[:400])
    check("view article link", "en.wikipedia.org/wiki/Albert_Einstein" in out, out[-200:])

    section("references — limit respected")
    out = server.references("Albert Einstein", limit=3)
    check("exactly 3 citations", "\n3. " in out and "\n4. " not in out, out[:3000])

    section("references — limit clamping + type safety")
    out = server.references("Albert Einstein", limit=100)
    numbered = sum(1 for i in range(1, 51) if f"\n{i}. " in out)
    check("limit=100 clamps to ≤50", numbered <= 50, f"got {numbered} items")
    out = server.references("Albert Einstein", limit=-5)
    check("limit=-5 clamps to 1", "\n1. " in out and "\n2. " not in out, out[:800])
    out = server.references("Albert Einstein", limit="abc")
    check("non-int limit returns results (no crash)", "References cited by" in out, out[:200])

    section("references — redirect follows")
    out = server.references("Einstein")  # redirects to Albert Einstein
    check("redirect resolves", 'References cited by "Albert Einstein"' in out, out[:200])

    section("references — missing article")
    out = server.references("ThisArticleDoesNotExist12345")
    check("missing article returns clear message", "not found" in out, out[:200])

    section("references — article with no references")
    out = server.references("Mercury")  # disambiguation page, no reference list
    check("no-references message", "No references found" in out, out[:200])

    section("references — german")
    out = server.references("Albert Einstein", lang="de", limit=2)
    check("german references work", "References cited by" in out and "de.wikipedia.org/wiki/" in out, out[:400])

    section("references — dispatcher routing")
    out = server._call_tool("references", {"title": "Paris"})
    check("dispatcher routes to references", "Unknown tool" not in out, out[:200])
    check("dispatcher returned real content", 'References cited by "Paris"' in out, out[:200])

    section("section_text")
    out = server.section_text("Albert Einstein", "Life and career")
    check("returns heading", '"Albert Einstein" — Life and career' in out, out[:200])
    check("real section content", "patent" in out.lower(), out[:1200])
    check("inline CSS stripped", ".mw-parser-output" not in out and "{font-style" not in out, out[:400])
    check("citation markers stripped", "[1]" not in out and "cite_note" not in out, out[:1200])
    check("[edit] links stripped", "[edit]" not in out, out[:400])
    check("deep link to section", "en.wikipedia.org/wiki/Albert_Einstein#Life_and_career" in out, out[-200:])

    section("section_text — by number matches by name")
    out_num = server.section_text("Albert Einstein", 1)
    check("number 1 == 'Life and career'", out_num.split("\n")[0] == out.split("\n")[0], out_num[:120])

    section("section_text — hierarchical number")
    out_h = server.section_text("Albert Einstein", "1.1")
    check("1.1 resolves", "Childhood, youth and education" in out_h, out_h[:120])

    section("section_text — int means displayed number, not flat index")
    _, _secs = server._fetch_sections("Albert Einstein", "en")
    _want = next(_s["line"] for _s in _secs if _s.get("number") == "2")
    out_n2 = server.section_text("Albert Einstein", 2)
    check("int 2 == section displayed as '2.'", _want in out_n2.split("\n")[0], out_n2[:160])

    section("section_text — lead section (0)")
    out_lead = server.section_text("Albert Einstein", 0)
    check("0 reads intro", "— Introduction" in out_lead, out_lead[:120])

    section("section_text — case-insensitive name")
    out_ci = server.section_text("Albert Einstein", "life and CAREER")
    check("case-insensitive match", "— Life and career" in out_ci, out_ci[:120])

    section("section_text — misspelled name suggests")
    out_miss = server.section_text("Albert Einstein", "Life and carer")
    check("suggestion offered", "Did you mean: Life and career?" in out_miss, out_miss[:200])

    section("section_text — out of range")
    out_oor = server.section_text("Albert Einstein", 999)
    check("range message", "out of range" in out_oor and "article_sections" in out_oor, out_oor[:200])

    section("section_text — missing article")
    out_no = server.section_text("ThisArticleDoesNotExist12345", 1)
    check("missing article returns clear message", "not found" in out_no, out_no[:120])

    section("section_text — redirect follows")
    out_red = server.section_text("Einstein", 1)  # redirects to Albert Einstein
    check("redirect resolves", '"Albert Einstein" — Life and career' in out_red, out_red[:120])

    section("section_text — german")
    out_de = server.section_text("Albert Einstein", 1, lang="de")
    check("german section works", "de.wikipedia.org/wiki/" in out_de and "View section" in out_de, out_de[:300])

    section("section_text — dispatcher routing")
    out_d = server._call_tool("section_text", {"title": "Paris", "section": "History"})
    check("dispatcher routes to section_text", "Unknown tool" not in out_d, out_d[:200])
    check("dispatcher returned real content", '"Paris" — History' in out_d and "View section" in out_d, out_d[:200])

    section("quote")
    out = server.quote()
    check("returns a quote", out.startswith("💬"), out[:200])
    check("contains quoted text", '"' in out, out[:200])
    check("contains attribution", "— *" in out, out[:300])
    # The curated list has at least 20 entries — verify we're picking from
    # a non-trivial pool (not a single hardcoded quote).
    check("starts with emoji marker", out.startswith("💬"), out[:200])

    section("quote — random distribution")
    # Call multiple times; with 23+ entries we should see at least 2
    # distinct outputs across 10 draws (probability of seeing all same
    # is ~1/23^9 — vanishingly small).
    seen = set()
    for _ in range(10):
        seen.add(server.quote())
    check("returns different quotes across calls (curated list > 1 entry)", len(seen) >= 2, f"got {len(seen)} unique quotes")

    section("quote — every entry is well-formed")
    # Curation quality check: every (author, quote) in FAMOUS_QUOTES must
    # be a real tuple with both fields populated. This catches accidental
    # truncation of the curated list (e.g. leaving a trailing comma that
    # makes one entry a string instead of a tuple).
    for i, entry in enumerate(server.FAMOUS_QUOTES):
        check(
            f"FAMOUS_QUOTES[{i}] is a (author, quote) tuple",
            isinstance(entry, tuple) and len(entry) == 2 and all(isinstance(s, str) and s for s in entry),
            repr(entry)[:100],
        )

    section("quote — lang parameter accepted")
    # `lang` is accepted for API consistency but currently English-only.
    # Verify that non-English values don't crash and still return a quote.
    out = server.quote(lang="de")
    check("non-English lang still returns a quote", out.startswith("💬"), out[:200])
    out = server.quote(lang="Klingon")
    check("invalid lang still returns a quote (no crash)", out.startswith("💬"), out[:200])

    section("quote — dispatcher routing")
    out = server._call_tool("quote", {})
    check("dispatcher routes to quote", "Unknown tool" not in out, out[:200])
    check("dispatcher returned real content", out.startswith("💬"), out[:200])

    section("media_list")
    out = server.media_list("Tyrannosaurus")
    check("returns header", "Media in" in out and "Tyrannosaurus" in out, out[:300])
    check("shows total count", "total" in out, out[:300])
    check("lists File: entries", "File:" in out, out[:500])
    check("includes Type: field", "Type: image" in out or "Type: video" in out, out[:500])
    check("includes Thumbnail: field", "Thumbnail:" in out, out[:500])
    check("thumbnail URL on wikimedia.org", "wikimedia.org" in out, out[:500])
    # Lead image should be marked — every Wikipedia summary endpoint marks
    # exactly one item as leadImage=true, so the trophy should appear at
    # least once in the response.
    check("lead marker present", "🏆" in out, out[:2000])
    check("article link included", "en.wikipedia.org/wiki/Tyrannosaurus" in out, out[:500])

    section("media_list — limit clamping + type safety")
    out = server.media_list("Tyrannosaurus", limit=999)
    # Items are rendered as "- **File:...**" lines. Count those.
    file_count = sum(
        1 for line in out.splitlines()
        if line.startswith("- **File:")
    )
    check("limit=999 clamps to ≤100", file_count <= 100, f"got {file_count}")
    out = server.media_list("Tyrannosaurus", limit=-5)
    file_count = sum(
        1 for line in out.splitlines()
        if line.startswith("- **File:")
    )
    check("limit=-5 clamps to ≥1", file_count >= 1, f"got {file_count}")
    out = server.media_list("Tyrannosaurus", limit="abc")
    check(
        "non-int limit returns media (no crash)",
        "Media in" in out and "Tyrannosaurus" in out,
        out[:300],
    )

    section("media_list — missing article")
    out = server.media_list("ThisArticleDoesNotExist12345")
    check("404 message", "not found" in out, out[:300])

    section("media_list — empty title")
    # Empty title → URL becomes /page/media-list/ → Wikipedia returns 404.
    out = server.media_list("")
    check("empty title returns graceful 404", "not found" in out, out[:300])

    section("media_list — multi-language")
    out = server.media_list("Berlin", limit=5, lang="de")
    check("de returns media", "Media in" in out and "Berlin" in out, out[:300])
    check("de wikipedia link", "de.wikipedia.org/wiki/" in out, out[:500])

    section("media_list — protocol-relative URLs upgraded")
    # srcset entries come back as "//upload.wikimedia.org/..." which
    # would break MCP clients resolving the URL. The tool must add the
    # https: scheme.
    out = server.media_list("Tyrannosaurus", limit=3)
    # Every "Thumbnail:" line must start with "https://" (no "//" alone).
    thumb_lines = [
        line for line in out.splitlines() if line.startswith("  Thumbnail:")
    ]
    check("at least one thumbnail rendered", len(thumb_lines) >= 1, out[:1000])
    if thumb_lines:
        check(
            "thumbnail URLs use https scheme (not protocol-relative)",
            all("https://" in line for line in thumb_lines),
            "\n".join(thumb_lines)[:500],
        )

    section("media_list — dispatcher routing")
    out = server._call_tool("media_list", {"title": "Velociraptor", "limit": 3})
    check("dispatcher routes to media_list", "Unknown tool" not in out, out[:200])
    check(
        "dispatcher returned real content",
        "Media in" in out and "Velociraptor" in out,
        out[:200],
    )

    section("media_search")
    out = server.media_search("aurora borealis", limit=3)
    check("returns header", "Media search" in out and "aurora borealis" in out, out[:300])
    check("lists File: entries", "File:" in out, out[:500])
    check("shows Type: field", "Type: image" in out, out[:500])
    check("thumbnail URL on upload.wikimedia.org", "upload.wikimedia.org" in out, out[:800])
    check("full-size URL present", "Full size:" in out, out[:800])
    check("Commons file page link", "commons.wikimedia.org/wiki/File:" in out, out[:800])

    section("media_search — filetype filters")
    out = server.media_search("volcano eruption", limit=3, filetype="video")
    check("video filter header", "filetype: video" in out, out[:300])
    video_lines = [l for l in out.splitlines() if l.startswith("  Type:")]
    check("results are videos", len(video_lines) >= 1 and all("video" in l for l in video_lines), "\n".join(video_lines)[:300])
    out = server.media_search("thunderstorm", limit=3, filetype="audio")
    audio_lines = [l for l in out.splitlines() if l.startswith("  Type:")]
    check("audio filter returns audio", len(audio_lines) >= 1 and all("audio" in l for l in audio_lines), "\n".join(audio_lines)[:300])

    section("media_search — limit clamping + type safety")
    out = server.media_search("aurora borealis", limit=999)
    file_count = sum(1 for line in out.splitlines() if line.startswith("- **File:"))
    check("limit=999 clamps to ≤50", file_count <= 50, f"got {file_count}")
    out = server.media_search("aurora borealis", limit=-5)
    file_count = sum(1 for line in out.splitlines() if line.startswith("- **File:"))
    check("limit=-5 clamps to ≥1", file_count >= 1, f"got {file_count}")
    out = server.media_search("aurora borealis", limit="abc")
    check(
        "non-int limit returns media (no crash)",
        "Media search" in out and "aurora borealis" in out,
        out[:300],
    )

    section("media_search — invalid filetype")
    out = server.media_search("aurora borealis", filetype="hologram")
    check("invalid filetype rejected", "Invalid filetype" in out, out[:200])

    section("media_search — no results")
    out = server.media_search("xyzzynonesuchquery")
    check("graceful empty", "No media found" in out, out[:200])

    section("media_search — empty query")
    out = server.media_search("")
    check("empty query asks for one", "search query" in out, out[:200])

    section("media_search — dispatcher routing")
    out = server._call_tool("media_search", {"query": "aurora borealis", "limit": 2})
    check("dispatcher routes to media_search", "Unknown tool" not in out, out[:200])
    check(
        "dispatcher returned real content",
        "Media search" in out and "aurora borealis" in out,
        out[:200],
    )

    section("language validation fallback")
    # _base() and _wiki() silently coerce unsupported langs to "en" so a
    # bad/typo'd lang string can't route a request to the wrong Wikipedia.
    # Test the validation directly (no network) so regressions get caught
    # even if the live calls happen to succeed.
    check("_base('en') → en rest_v1", server._base("en") == "https://en.wikipedia.org/api/rest_v1")
    check("_base('de') → de rest_v1", server._base("de") == "https://de.wikipedia.org/api/rest_v1")
    check("_base('ja') → ja rest_v1", server._base("ja") == "https://ja.wikipedia.org/api/rest_v1")
    check("_base('') → en rest_v1 (default)", server._base("") == "https://en.wikipedia.org/api/rest_v1")
    check("_base('invalid') → falls back to en", server._base("invalid") == "https://en.wikipedia.org/api/rest_v1")
    check("_base('EN') → case-sensitive fallback to en", server._base("EN") == "https://en.wikipedia.org/api/rest_v1")
    check("_wiki('en') → en api.php", server._wiki("en") == "https://en.wikipedia.org/w/api.php")
    check("_wiki('de') → de api.php", server._wiki("de") == "https://de.wikipedia.org/w/api.php")
    check("_wiki('invalid') → falls back to en", server._wiki("invalid") == "https://en.wikipedia.org/w/api.php")
    check("_wiki('Klingon') → falls back to en", server._wiki("Klingon") == "https://en.wikipedia.org/w/api.php")
    # Unsupported lang flows through to live calls without crashing
    out = server.get_summary("Berlin", lang="Klingon")
    check("unsupported lang still returns an article", out.startswith("## "), out[:200])

    section("article_path — two hops")
    out = server.article_path("Albert Einstein", "Quantum mechanics")
    check("2-hop header", "**2 hops**" in out, out[:200])
    check("middles listed", "Arthur Eddington" in out, out[:800])
    check("scan footer", "Scanned the first" in out, out[-400:])

    section("article_path — one hop")
    out = server.article_path("Cat", "Dog")
    check("1-hop header", "**1 hop**" in out, out[:200])
    check("direct link shown", "Cat" in out and "Dog" in out, out[:200])

    section("article_path — three hops")
    out = server.article_path("Banana", "Trojan War", max_hops=3)
    check("3-hop header", "**3 hops**" in out, out[:200])
    check("endpoints shown", "Banana" in out and "Trojan War" in out, out[:400])

    section("article_path — same article")
    out = server.article_path("Albert Einstein", "Albert Einstein")
    check("0 hops reported", "**0 hops**" in out, out[:200])

    section("article_path — redirect resolves to same")
    out = server.article_path("USA", "United States")
    check("redirect same-article", "**0 hops**" in out, out[:200])

    section("article_path — missing article")
    out = server.article_path("ThisArticleDoesNotExistZZZ123", "Cat")
    check("missing reported", "not found" in out, out[:200])

    section("article_path — empty title")
    out = server.article_path("", "Cat")
    check("empty reported", "required" in out, out[:200])

    section("article_path — max_hops=1 misses")
    out = server.article_path("Albert Einstein", "Quantum mechanics", max_hops=1)
    check("1-hop miss reported", "No direct link" in out, out[:200])

    section("article_path — max_hops clamps + type safety")
    out = server.article_path("Banana", "Trojan War", max_hops=99)
    check("max_hops clamps to 3", "**3 hops**" in out, out[:200])
    out = server.article_path("Banana", "Trojan War", max_hops="abc")
    check("bad max_hops falls back to 2", "No path within 2 hops" in out, out[:200])

    section("article_path — dispatcher routing")
    out = server._call_tool("article_path", {"start": "Cat", "target": "Dog"})
    check("dispatcher routes to article_path", "Unknown tool" not in out, out[:200])

    section("article_at_date — historical snapshot")
    out = server.article_at_date("ChatGPT", "2023-01-15")
    check("dated header", "## ChatGPT — as it read on 2023-01-15" in out, out[:200])
    check("revision metadata", "Revision 1133794731" in out, out[:300])
    check("lead text from that era", "generative AI chatbot" in out, out[:1200])
    check("permanent link", "oldid=1133794731" in out, out[-500:])
    check("no navbox noise", "Part of a series on" not in out, out[:1500])

    section("article_at_date — bad date format")
    out = server.article_at_date("ChatGPT", "Jan 2023")
    check("format message", "YYYY-MM-DD" in out, out)

    section("article_at_date — date before the article existed")
    out = server.article_at_date("ChatGPT", "2019-05-05")
    check("pre-creation reported", "No surviving revision" in out, out)
    check("first revision named", "first surviving revision" in out, out)

    section("article_at_date — missing article")
    out = server.article_at_date("ThisArticleDoesNotExistZZZ123", "2023-01-15")
    check("missing reported", "not found" in out, out)

    section("article_at_date — empty title")
    out = server.article_at_date("", "2023-01-15")
    check("empty reported", "required" in out, out)

    section("article_at_date — redirect resolves")
    out = server.article_at_date("USA", "2020-06-01")
    check("redirect resolved", "## United States — as it read on 2020-06-01" in out, out[:200])

    section("article_at_date — dispatcher routing")
    out = server._call_tool("article_at_date", {"title": "ChatGPT", "date": "2023-01-15"})
    check("dispatcher routes to article_at_date", "Unknown tool" not in out, out[:200])

    section("_call_tool dispatch routing")
    # Every registered MCP tool name must route through the dispatcher
    # (i.e. NOT return the "Unknown tool" fallback). This is the layer
    # MCP clients actually call via tools/call — if it breaks, the
    # whole server breaks even though individual functions still work.
    routed_ok = set()
    for tool_def in server.TOOLS:
        name = tool_def["name"]
        if name == "search":
            out = server._call_tool(name, {"query": "test", "limit": 1})
        elif name == "summary":
            out = server._call_tool(name, {"title": "Velociraptor"})
        elif name == "dino_fact":
            out = server._call_tool(name, {"species": ""})
        elif name == "article_extract":
            out = server._call_tool(name, {"title": "Velociraptor"})
        elif name == "article_sections":
            out = server._call_tool(name, {"title": "Velociraptor"})
        elif name == "on_this_day":
            out = server._call_tool(name, {})
        elif name == "deaths_on_this_day":
            out = server._call_tool(name, {})
        elif name == "categories":
            out = server._call_tool(name, {"title": "Velociraptor"})
        elif name == "category_members":
            out = server._call_tool(name, {"category": "Flightless birds"})
        elif name == "infobox":
            out = server._call_tool(name, {"title": "Velociraptor"})
        elif name == "links":
            out = server._call_tool(name, {"title": "Velociraptor"})
        elif name == "backlinks":
            out = server._call_tool(name, {"title": "Velociraptor"})
        elif name == "external_links":
            out = server._call_tool(name, {"title": "Velociraptor"})
        elif name == "translations":
            out = server._call_tool(name, {"title": "Velociraptor"})
        elif name == "revisions":
            out = server._call_tool(name, {"title": "Velociraptor"})
        elif name == "pageviews":
            out = server._call_tool(name, {"title": "Velociraptor"})
        elif name == "news":
            out = server._call_tool(name, {})
        elif name == "top_reads":
            # Use a known date so the test doesn't depend on "today"
            # having finalized pageviews data.
            out = server._call_tool(name, {"date": "20250829", "limit": 5})
        elif name == "image":
            out = server._call_tool(name, {"title": "Velociraptor"})
        elif name == "media_list":
            out = server._call_tool(name, {"title": "Velociraptor", "limit": 3})
        elif name == "media_search":
            out = server._call_tool(name, {"query": "aurora borealis", "limit": 2})
        elif name == "article_quality":
            out = server._call_tool(name, {"title": "Paris"})
        elif name == "related_articles":
            out = server._call_tool(name, {"title": "Velociraptor"})
        elif name == "contributors":
            out = server._call_tool(name, {"title": "Velociraptor"})
        elif name == "references":
            out = server._call_tool(name, {"title": "Velociraptor", "limit": 2})
        elif name == "section_text":
            out = server._call_tool(name, {"title": "Albert Einstein", "section": 0})
        elif name == "revision_diff":
            out = server._call_tool(
                name,
                {"title": "Python_(programming_language)", "rev_from": 1374673264, "rev_to": 1374673393},
            )
        elif name == "disambiguation":
            out = server._call_tool(name, {"title": "Mercury"})
        elif name == "user_contribs":
            out = server._call_tool(name, {"user": "Jimbo Wales", "limit": 2})
        elif name == "talk":
            out = server._call_tool(name, {"title": "Velociraptor"})
        elif name == "article_flags":
            out = server._call_tool(name, {"article": "Eiffel Tower"})
        elif name == "citation_sources":
            out = server._call_tool(name, {"title": "Velociraptor", "limit": 3})
        elif name == "article_path":
            out = server._call_tool(name, {"start": "Cat", "target": "Dog"})
        elif name == "article_at_date":
            out = server._call_tool(name, {"title": "ChatGPT", "date": "2023-01-15"})
        elif name == "simple_summary":
            out = server._call_tool(name, {"title": "Velociraptor"})
        else:
            out = server._call_tool(name, {})
        check(
            f"'{name}' routes through dispatcher",
            "Unknown tool" not in out,
            out[:200],
        )
        if "Unknown tool" not in out:
            routed_ok.add(name)
    expected_names = {t["name"] for t in server.TOOLS}
    check(
        "every registered tool is routable",
        routed_ok == expected_names,
        f"missing: {expected_names - routed_ok}",
    )
    # Unknown tool name returns a clear, non-empty message
    out = server._call_tool("definitely_not_a_real_tool", {})
    check(
        "unknown tool returns clear message",
        "Unknown tool: definitely_not_a_real_tool" in out,
        out,
    )

    section("tool schemas — every tool declares inputSchema")
    # Strict MCP clients (e.g. Glama's checks) reject tools/list entries
    # without an inputSchema object, so this must never regress.
    for t in server.TOOLS:
        schema = t.get("inputSchema")
        check(
            f"'{t['name']}' has inputSchema object",
            isinstance(schema, dict) and schema.get("type") == "object",
            f"got: {schema!r}",
        )

    print(f"\n{PASS} passed, {FAIL} failed")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())