#!/usr/bin/env python3
"""Check the links found on one page: status codes and redirect chains.

Usage: python check_links.py https://example.com/page [--max-links 50] [--delay 0.3]
                             [--include-external] [--allow-private]

Internal = same hostname as the page. External links are only checked with
--include-external, and statuses that usually mean "bot blocked" (401/403/429/999)
are reported as unverifiable, not broken. The check is capped and rate-limited on purpose.
"""
import argparse
import os
import sys
import time
import urllib.parse
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _http import (add_common_args, decode_text, emit, fetch_kwargs, follow, get_header,  # noqa: E402
                   make_issue, normalize_url, now_iso)
from _page import parse_page  # noqa: E402

BOT_BLOCK = (401, 403, 429, 999)


def check_one(url, kw):
    hops, r = follow(url, max_hops=5, method="HEAD", read_body=False, **kw)
    if r["error"] or (r["status"] or 0) >= 400:
        hops, r = follow(url, max_hops=5, method="GET", read_body=False, **kw)
    return hops, r


def classify(kind, hops, r):
    status = r["status"]
    if r["error"]:
        return "unreachable"
    if status is None:
        return "unreachable"
    if status >= 400:
        if kind == "external" and status in BOT_BLOCK:
            return "unverifiable"
        return "broken"
    if 300 <= status < 400:
        return "redirect_unresolved"
    return "redirect" if len(hops) > 1 else "ok"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url")
    ap.add_argument("--max-links", type=int, default=50)
    ap.add_argument("--delay", type=float, default=0.3)
    ap.add_argument("--include-external", action="store_true")
    add_common_args(ap)
    args = ap.parse_args()
    kw = fetch_kwargs(args)
    url = normalize_url(args.url)
    out = {"tool": "check_links", "checked_at": now_iso(), "target": url, "errors": []}

    hops, r = follow(url, **kw)
    if r["error"] or (r["status"] or 0) >= 400:
        out["errors"].append({"url": hops[-1]["url"], "error": r["error"] or "HTTP %s" % r["status"]})
        out["status"] = "not_checked"
        emit(out)
        sys.exit(2)
    final = hops[-1]["url"]
    page_host = (urllib.parse.urlsplit(final).hostname or "").lower()
    p = parse_page(decode_text(r), final)

    found, skipped = {}, Counter()
    for a in p.anchors:
        href = a["href"].strip()
        if not href or href.startswith("#"):
            skipped["fragment_or_empty"] += 1
            continue
        absu = urllib.parse.urldefrag(urllib.parse.urljoin(p.base_url or final, href))[0]
        scheme = urllib.parse.urlsplit(absu).scheme
        if scheme not in ("http", "https"):
            skipped[scheme or "other"] += 1
            continue
        found.setdefault(absu, " ".join("".join(a["text"]).split())[:60])

    internal = [u for u in found if (urllib.parse.urlsplit(u).hostname or "").lower() == page_host]
    external = [u for u in found if u not in set(internal)]
    queue = [(u, "internal") for u in internal]
    if args.include_external:
        queue += [(u, "external") for u in external]
    truncated = len(queue) > args.max_links
    queue = queue[:args.max_links]

    results = []
    for i, (u, kind) in enumerate(queue):
        if i:
            time.sleep(args.delay)
        h, rr = check_one(u, kw)
        results.append({"url": u, "kind": kind, "anchor_text": found[u], "status": rr["status"],
                        "classification": classify(kind, h, rr), "redirect_hops": len(h) - 1,
                        "final_url": h[-1]["url"], "chain": [x["url"] for x in h] if len(h) > 1 else None,
                        "error": rr["error"]})

    by = Counter(x["classification"] for x in results)
    out["summary"] = {"unique_links_found": len(found), "internal_found": len(internal),
                      "external_found": len(external), "checked": len(results),
                      "not_checked_due_to_cap": max(0, (len(internal) + (len(external) if args.include_external else 0)) - len(results)),
                      "external_not_checked_by_choice": 0 if args.include_external else len(external),
                      "skipped_schemes": dict(skipped), "by_classification": dict(by)}
    out["broken"] = [x for x in results if x["classification"] in ("broken", "unreachable")]
    out["redirects"] = [x for x in results if x["classification"] in ("redirect", "redirect_unresolved")]
    out["unverifiable"] = [x for x in results if x["classification"] == "unverifiable"]

    issues = []
    if out["broken"]:
        issues.append(make_issue("links.broken", "content", "medium",
                                 "Links returning an error status or unreachable.", count=len(out["broken"]),
                                 examples=["%s -> %s" % (x["url"], x["status"] or x["error"]) for x in out["broken"]]))
    chains = [x for x in out["redirects"] if x["redirect_hops"] >= 2]
    if chains:
        issues.append(make_issue("links.redirect_chain", "content", "low",
                                 "Links that go through two or more redirects.", count=len(chains),
                                 examples=[" -> ".join(x["chain"]) for x in chains]))
    singles = [x for x in out["redirects"] if x["redirect_hops"] == 1]
    if singles:
        issues.append(make_issue("links.redirecting", "content", "low",
                                 "Internal/external links that redirect once (could point at the final URL).",
                                 count=len(singles), examples=["%s -> %s" % (x["url"], x["final_url"]) for x in singles]))
    out["issues"] = issues
    out["caveats"] = ["Only links present in the static HTML were checked (no JavaScript).",
                      "Internal means the same hostname as the page; other subdomains count as external.",
                      "Capped at --max-links%s." % (" (cap was reached)" if truncated else "")]
    emit(out)


if __name__ == "__main__":
    main()
