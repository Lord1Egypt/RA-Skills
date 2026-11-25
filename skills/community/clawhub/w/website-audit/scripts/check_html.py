#!/usr/bin/env python3
"""Static HTML audit of one page: SEO, accessibility, content and static performance signals.

Usage:
  python check_html.py https://example.com/page [--allow-private]
  python check_html.py --file page.html --base-url https://example.com/page

Prints JSON with raw measurements and issues. Every issue has evidence. JavaScript is
NOT executed, so anything a script adds after load is invisible here.
"""
import argparse
import datetime
import json
import os
import re
import sys
import urllib.parse
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _http import (add_common_args, decode_text, emit, fetch_kwargs, follow, get_header,  # noqa: E402
                   make_issue, normalize_url, now_iso)
from _page import parse_page  # noqa: E402

LIB_RE = re.compile(r"(jquery|bootstrap|angular|react|vue|lodash|moment)[.@/_-]v?(\d+\.\d+(?:\.\d+)?)", re.I)
PLACEHOLDER_RE = re.compile(r"lorem ipsum|coming soon|under construction|\bTODO\b|\bTBD\b|your text here", re.I)
COPYRIGHT_RE = re.compile(r"(?:©|&copy;|\(c\)|copyright)\s*(?:\(c\)\s*)?(\d{4})(?:\s*[-–]\s*(\d{4}))?", re.I)
ACTIVE_TAGS = {"script", "iframe", "link", "object", "embed"}


def norm(u):
    p = urllib.parse.urlsplit(u)
    path = p.path or "/"
    if path != "/":
        path = path.rstrip("/")
    return (p.scheme, (p.hostname or "").lower(), p.port, path, p.query)


def host_of(u):
    return (urllib.parse.urlsplit(u).hostname or "").lower()


def meta_by_name(p, *names):
    return [(m.get("name", "").lower(), m.get("content", "")) for m in p.metas if m.get("name", "").lower() in names]


def meta_by_prop(p, prop):
    return [m.get("content", "") for m in p.metas if m.get("property", "").lower() == prop]


def has_name(item):
    return bool(item["text_joined"] or item["aria_label"] or item["aria_labelledby"] or item["title"] or item.get("img_alt"))


def analyse(p, page):
    final = page["final_url"]
    https = urllib.parse.urlsplit(final).scheme == "https"
    page_host = host_of(final)
    issues, meas = [], {}
    caveats = ["JavaScript was not executed; content added client-side is not seen."]
    text = p.visible_text()
    words = len(text.split())

    # ---------------- SEO ----------------
    titles = [t for t in p.titles]
    nonempty_titles = [t for t in titles if t]
    descs = [c.strip() for _, c in meta_by_name(p, "description")]
    canon = [l.get("href", "").strip() for l in p.link_tags if "canonical" in l.get("rel", "").lower().split()]
    robots_meta = meta_by_name(p, "robots", "googlebot", "bingbot")
    h1s = [h["text"] for h in p.headings if h["level"] == 1]
    og = {k: meta_by_prop(p, k) for k in ("og:title", "og:description", "og:image")}
    hreflang = [{"hreflang": l.get("hreflang"), "href": l.get("href")} for l in p.link_tags
                if "alternate" in l.get("rel", "").lower().split() and l.get("hreflang")]
    meas["seo"] = {
        "title": nonempty_titles[0] if nonempty_titles else None,
        "title_length": len(nonempty_titles[0]) if nonempty_titles else 0,
        "meta_description": next((d for d in descs if d), None),
        "meta_description_length": len(next((d for d in descs if d), "")),
        "canonical": canon, "robots_meta": [{"name": n, "content": c} for n, c in robots_meta],
        "h1": h1s, "heading_outline": ["h%d %s" % (h["level"], h["text"]) for h in p.headings][:40],
        "hreflang": hreflang, "open_graph": {k: bool(v and any(v)) for k, v in og.items()}}

    if not nonempty_titles:
        issues.append(make_issue("title.missing", "seo", "high", "The page has no non-empty <title>.",
                                 evidence={"titles_found": titles}, wcag="2.4.2"))
    if len(titles) > 1:
        issues.append(make_issue("title.multiple", "seo", "low", "More than one <title> element.", evidence=titles))
    if not any(descs):
        issues.append(make_issue("meta_description.missing", "seo", "medium", "No meta description."))
    elif len([d for d in descs if d]) > 1:
        issues.append(make_issue("meta_description.multiple", "seo", "low", "More than one meta description.", evidence=descs))

    for name, content in robots_meta:
        if "noindex" in re.split(r"[,\s]+", content.lower()):
            issues.append(make_issue("robots.noindex", "seo", "high",
                                     "Meta robots tells search engines not to index this page.",
                                     evidence='<meta name="%s" content="%s">' % (name, content)))
    xrt = get_header(page["headers"], "x-robots-tag")
    if xrt and "noindex" in xrt.lower():
        issues.append(make_issue("robots.noindex_header", "seo", "high",
                                 "X-Robots-Tag header tells search engines not to index this page.", evidence=xrt))

    if not canon:
        issues.append(make_issue("canonical.missing", "seo", "low", "No canonical link."))
    elif len(set(canon)) > 1:
        issues.append(make_issue("canonical.multiple", "seo", "medium", "Several different canonical links.", evidence=canon))
    else:
        resolved = urllib.parse.urljoin(p.base_url or final, canon[0])
        if norm(resolved) != norm(final):
            issues.append(make_issue("canonical.differs", "seo", "low",
                                     "Canonical URL differs from the fetched URL; confirm this is intended.",
                                     evidence={"canonical": resolved, "page_url": final}))
        if https and urllib.parse.urlsplit(resolved).scheme == "http":
            issues.append(make_issue("canonical.http_on_https", "seo", "medium",
                                     "Canonical points to http:// from an https page.", evidence=resolved))

    if not h1s:
        issues.append(make_issue("h1.missing", "seo", "medium", "No <h1> found in the static HTML."))
    elif len(h1s) > 1:
        issues.append(make_issue("h1.multiple", "seo", "low", "More than one <h1>.", evidence=h1s))
    skips, prev = [], None
    for h in p.headings:
        if prev is not None and h["level"] > prev + 1:
            skips.append("h%d to h%d at '%s'" % (prev, h["level"], h["text"]))
        prev = h["level"]
    if skips:
        issues.append(make_issue("heading.skipped_level", "seo", "low", "Heading levels are skipped.",
                                 count=len(skips), examples=skips, wcag="1.3.1"))
    missing_og = [k for k, v in og.items() if not any(v)]
    if missing_og:
        issues.append(make_issue("og.missing", "seo", "low", "Open Graph tags missing.", evidence=missing_og))

    ld_types = []
    for raw in p.jsonld:
        try:
            data = json.loads(raw)
        except ValueError as e:
            issues.append(make_issue("jsonld.invalid", "seo", "medium", "A JSON-LD block is not valid JSON.",
                                     evidence={"error": str(e), "snippet": raw.strip()[:160]}))
            continue
        stack = [data]
        while stack:
            node = stack.pop()
            if isinstance(node, list):
                stack.extend(node)
            elif isinstance(node, dict):
                t = node.get("@type")
                if t:
                    ld_types.extend(t if isinstance(t, list) else [t])
                stack.extend(v for v in node.values() if isinstance(v, (dict, list)))
    meas["seo"]["jsonld_types"] = sorted(set(str(t) for t in ld_types))

    # ---------------- Accessibility ----------------
    for a in p.anchors:
        a["text_joined"] = " ".join("".join(a["text"]).split())
    for b in p.buttons:
        b["text_joined"] = " ".join("".join(b["text"]).split())
    imgs_missing = [i for i in p.images if not i["has_alt"]]
    imgs_empty = [i for i in p.images if i["has_alt"] and not (i["alt"] or "").strip()]
    empty_links = [a for a in p.anchors if not has_name(a)]
    empty_buttons = [b for b in p.buttons if not has_name(b)]
    unlabeled = [c for c in p.controls if not (c["in_label"] or (c["id"] and c["id"] in p.label_for)
                                              or c["aria_label"] or c["aria_labelledby"] or c["title"])]
    viewport = next((c for n, c in meta_by_name(p, "viewport")), None)
    meas["accessibility"] = {
        "lang": p.lang, "images_total": len(p.images), "images_missing_alt": len(imgs_missing),
        "images_empty_alt": len(imgs_empty), "links_total": len(p.anchors),
        "form_controls": len(p.controls), "has_main_landmark": bool(p.tags["main"] or "main" in p.roles),
        "has_nav_landmark": bool(p.tags["nav"] or "navigation" in p.roles), "viewport": viewport}
    if not (p.lang or "").strip():
        issues.append(make_issue("html.lang_missing", "accessibility", "medium", "<html> has no lang attribute.", wcag="3.1.1"))
    if imgs_missing:
        issues.append(make_issue("images.alt_missing", "accessibility", "medium",
                                 "Images without an alt attribute (alt=\"\" is fine for decorative images).",
                                 count=len(imgs_missing), examples=[i["snippet"] for i in imgs_missing], wcag="1.1.1"))
    if empty_links:
        issues.append(make_issue("links.empty_name", "accessibility", "medium",
                                 "Links with no text, aria-label, title or image alt.",
                                 count=len(empty_links), examples=[a["snippet"] for a in empty_links], wcag="2.4.4, 4.1.2"))
    if empty_buttons:
        issues.append(make_issue("buttons.empty_name", "accessibility", "medium",
                                 "Buttons with no accessible name.", count=len(empty_buttons),
                                 examples=[b["snippet"] for b in empty_buttons], wcag="4.1.2"))
    if unlabeled:
        issues.append(make_issue("inputs.no_label", "accessibility", "medium",
                                 "Form controls without a label, aria-label, aria-labelledby or title (placeholder does not count).",
                                 count=len(unlabeled), examples=[c["snippet"] for c in unlabeled], wcag="1.3.1, 3.3.2, 4.1.2"))
    if viewport:
        vp = viewport.lower().replace(" ", "")
        m = re.search(r"maximum-scale=([\d.]+)", vp)
        if "user-scalable=no" in vp or "user-scalable=0" in vp or (m and float(m.group(1)) < 2):
            issues.append(make_issue("viewport.zoom_disabled", "accessibility", "medium",
                                     "Viewport meta restricts pinch zoom.", evidence=viewport, wcag="1.4.4"))
    if p.tabindex_positive:
        issues.append(make_issue("tabindex.positive", "accessibility", "low",
                                 "Elements use tabindex greater than 0.", count=p.tabindex_positive, wcag="2.4.3"))
    if p.aria_hidden_focusable:
        issues.append(make_issue("aria_hidden.focusable", "accessibility", "medium",
                                 "Focusable elements are hidden from assistive tech with aria-hidden=true.",
                                 count=len(p.aria_hidden_focusable), examples=p.aria_hidden_focusable, wcag="4.1.2"))
    if not meas["accessibility"]["has_main_landmark"]:
        issues.append(make_issue("landmarks.main_missing", "accessibility", "low",
                                 "No <main> or role=main in the static HTML.", wcag="1.3.1, 2.4.1"))
    caveats.append("Color contrast, focus visibility, keyboard traps and reflow are NOT checked by this script.")

    # ---------------- Security (static) ----------------
    mixed = []
    if https:
        for r in p.resources:
            if urllib.parse.urlsplit(urllib.parse.urljoin(p.base_url or final, r["url"])).scheme == "http":
                mixed.append(r)
        for f in p.forms:
            if f["action"].lower().startswith("http://"):
                mixed.append({"tag": "form", "url": f["action"]})
    if mixed:
        active = any(r["tag"] in ACTIVE_TAGS or r["tag"] == "form" for r in mixed)
        issues.append(make_issue("mixed_content", "security", "high" if active else "medium",
                                 "HTTP resources referenced from an HTTPS page.", count=len(mixed),
                                 examples=["<%s> %s" % (r["tag"], r["url"]) for r in mixed]))
    if not https and p.has_password:
        issues.append(make_issue("form.password_over_http", "security", "high",
                                 "A password field is on a page served over HTTP.", evidence=final))
    no_sri = []
    for s in p.scripts:
        if s["src"] and host_of(urllib.parse.urljoin(p.base_url or final, s["src"])) not in ("", page_host) and not s["integrity"]:
            no_sri.append("<script> " + s["src"])
    for l in p.link_tags:
        if "stylesheet" in l.get("rel", "").lower().split() and l.get("href") and not l.get("integrity"):
            if host_of(urllib.parse.urljoin(p.base_url or final, l["href"])) not in ("", page_host):
                no_sri.append("<link> " + l["href"])
    if no_sri:
        issues.append(make_issue("sri.missing", "security", "low",
                                 "Cross-origin scripts/stylesheets without Subresource Integrity.",
                                 count=len(no_sri), examples=no_sri))
    libs = []
    for s in p.scripts:
        m = LIB_RE.search(s["src"] or "")
        if m:
            libs.append({"library": m.group(1).lower(), "version_in_filename": m.group(2), "src": s["src"]})
    gen = [c for n, c in meta_by_name(p, "generator")]
    meas["security_static"] = {
        "library_hints": libs, "generator_meta": gen,
        "library_note": "Versions come from file names only. They do not prove the real version or any vulnerability."}

    # ---------------- Performance (static indicators) ----------------
    blocking = [s["src"] for s in p.scripts if s["src"] and s["in_head"] and not s["async"]
                and not s["defer"] and s["type"] != "module"]
    no_dims = [i for i in p.images if not (i["has_width"] and i["has_height"])]
    hosts = Counter(host_of(urllib.parse.urljoin(p.base_url or final, r["url"])) for r in p.resources)
    third = {h: n for h, n in hosts.items() if h and h != page_host}
    enc = get_header(page["headers"], "content-encoding")
    meas["performance_static"] = {
        "html_bytes_decoded": page["decoded_bytes"], "html_bytes_on_wire": page["wire_bytes"],
        "content_encoding": enc, "time_to_headers_ms": page["headers_ms"], "total_ms": page["total_ms"],
        "scripts": len(p.scripts), "scripts_external": sum(1 for s in p.scripts if s["src"]),
        "inline_script_bytes": sum(s["inline_bytes"] for s in p.scripts),
        "stylesheets": sum(1 for l in p.link_tags if "stylesheet" in l.get("rel", "").lower().split()),
        "images": len(p.images), "images_lazy": sum(1 for i in p.images if i["loading"] == "lazy"),
        "third_party_hosts": third,
        "note": "Indicators from one static fetch. These are not Core Web Vitals."}
    if blocking:
        issues.append(make_issue("render_blocking.scripts", "performance", "medium",
                                 "External scripts in <head> without async/defer/module.",
                                 count=len(blocking), examples=blocking))
    if no_dims:
        issues.append(make_issue("images.no_dimensions", "performance", "low",
                                 "Images without width and height attributes (layout shift risk).",
                                 count=len(no_dims), examples=[i["snippet"] for i in no_dims]))
    if "html" in (get_header(page["headers"], "content-type") or "").lower() and not enc and page["decoded_bytes"] > 1500:
        issues.append(make_issue("compression.missing", "performance", "medium",
                                 "HTML response was not compressed although the request offered gzip.",
                                 evidence={"content_encoding": None, "decoded_bytes": page["decoded_bytes"]}))

    # ---------------- Content ----------------
    ph = [m for m in PLACEHOLDER_RE.finditer(text)]
    years = []
    for m in COPYRIGHT_RE.finditer(text):
        years.append(int(m.group(2) or m.group(1)))
    this_year = datetime.date.today().year
    meas["content"] = {"visible_words": words, "internal_links": sum(1 for a in p.anchors if host_of(urllib.parse.urljoin(p.base_url or final, a["href"])) == page_host),
                       "copyright_years_found": years, "script_run_year": this_year}
    if ph:
        issues.append(make_issue("content.placeholder_text", "content", "medium",
                                 "Placeholder-style text found in visible content.", count=len(ph),
                                 examples=[text[max(0, m.start() - 30):m.end() + 30] for m in ph]))
    if years and max(years) < this_year:
        issues.append(make_issue("content.copyright_outdated", "content", "low",
                                 "Latest copyright year on the page is earlier than the year this script ran.",
                                 evidence={"latest_found": max(years), "script_run_year": this_year}))
    if words < 150:
        issues.append(make_issue("content.thin", "content", "low",
                                 "Little visible text in the static HTML; judge against the page's purpose.",
                                 evidence={"visible_words": words}, confidence="likely"))
    if words < 50 and len(p.scripts) >= 3:
        meas["static_html_may_be_incomplete"] = True
        caveats.append("Very little text but several scripts: the page may be rendered client-side, "
                       "so static findings may be incomplete.")
    return meas, issues, caveats


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url", nargs="?")
    ap.add_argument("--file")
    ap.add_argument("--base-url", default="https://example.invalid/")
    add_common_args(ap)
    args = ap.parse_args()
    out = {"tool": "check_html", "checked_at": now_iso(), "errors": []}

    if args.file:
        with open(args.file, "rb") as f:
            body = f.read()
        html = body.decode("utf-8", errors="replace")
        page = {"final_url": args.base_url, "headers": [], "decoded_bytes": len(body),
                "wire_bytes": len(body), "headers_ms": None, "total_ms": None, "status": None,
                "redirects": []}
    else:
        if not args.url:
            ap.error("give a URL or --file")
        url = normalize_url(args.url)
        hops, r = follow(url, **fetch_kwargs(args))
        if r["error"]:
            out["target"] = url
            out["errors"].append({"url": hops[-1]["url"], "error": r["error"]})
            out["status"] = "not_checked"
            emit(out)
            sys.exit(2)
        ctype = (get_header(r["headers"], "content-type") or "").lower()
        out["target"] = url
        if r["status"] >= 400:
            out["errors"].append({"url": hops[-1]["url"], "error": "HTTP %s" % r["status"]})
        if ctype and "html" not in ctype:
            out["errors"].append({"url": hops[-1]["url"], "error": "not HTML (content-type: %s)" % ctype})
            out["status"] = "not_checked"
            emit(out)
            sys.exit(2)
        html = decode_text(r)
        page = {"final_url": hops[-1]["url"], "headers": r["headers"], "decoded_bytes": len(r["body"]),
                "wire_bytes": r["wire_bytes"], "headers_ms": r["headers_ms"], "total_ms": r["total_ms"],
                "status": r["status"], "redirects": hops}
        if r["body_truncated"]:
            out["errors"].append({"url": page["final_url"], "error": "body truncated at size limit; analysis is partial"})

    p = parse_page(html, page["final_url"])
    meas, issues, caveats = analyse(p, page)
    out["page"] = {k: page[k] for k in ("final_url", "status", "redirects")}
    out["measurements"] = meas
    out["issues"] = issues
    out["caveats"] = caveats
    emit(out)


if __name__ == "__main__":
    main()
