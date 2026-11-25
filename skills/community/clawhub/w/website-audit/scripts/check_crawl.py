#!/usr/bin/env python3
"""Check robots.txt, sitemap(s) and /.well-known/security.txt for a site.

Usage: python check_crawl.py https://example.com [--sample 10] [--allow-private]

Sitemap URLs are sampled (evenly spaced) and each sampled URL is requested once without
following redirects, so a redirecting sitemap entry shows up as a redirect.
"""
import argparse
import os
import sys
import urllib.parse
import xml.etree.ElementTree as ET
import zlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _http import (add_common_args, decode_text, emit, fetch, fetch_kwargs, get_header,  # noqa: E402
                   make_issue, normalize_url, now_iso)

ASSET_HINTS = (".css", ".js", "/css", "/js", "/wp-content/", "/wp-includes/", "/assets/", "/static/")
SITEMAP_URL_LIMIT = 50000


def parse_robots(text):
    groups, sitemaps, cur, last_agent = [], [], None, False
    for line in text.splitlines():
        line = line.split("#", 1)[0].strip()
        if not line or ":" not in line:
            continue
        k, v = line.split(":", 1)
        k, v = k.strip().lower(), v.strip()
        if k == "user-agent":
            if cur is None or not last_agent:
                cur = {"agents": [], "rules": []}
                groups.append(cur)
            cur["agents"].append(v.lower())
            last_agent = True
            continue
        last_agent = False
        if k in ("allow", "disallow") and cur is not None:
            cur["rules"].append((k, v))
        elif k == "sitemap" and v:
            sitemaps.append(v)
    return groups, sitemaps


def analyse_robots(r, kw_origin):
    issues, meas = [], {"url": r["url"], "status": r["status"], "error": r["error"]}
    sitemaps = []
    if r["error"]:
        meas["note"] = "Could not fetch robots.txt."
        return meas, issues, sitemaps
    if r["status"] == 200:
        text = decode_text(r)
        head = text.lstrip()[:200].lower()
        if head.startswith("<!doctype html") or head.startswith("<html"):
            issues.append(make_issue("robots.looks_like_html", "seo", "medium",
                                     "robots.txt returns an HTML page (soft 404?).", evidence=head[:100]))
            return meas, issues, sitemaps
        groups, sitemaps = parse_robots(text)
        meas["groups"] = [{"agents": g["agents"], "rules": ["%s: %s" % x for x in g["rules"]][:40]} for g in groups]
        meas["sitemap_directives"] = sitemaps
        for g in groups:
            blocks_all = any(k == "disallow" and v == "/" for k, v in g["rules"]) and \
                not any(k == "allow" and v in ("/", "") for k, v in g["rules"])
            if blocks_all and "*" in g["agents"]:
                issues.append(make_issue("robots.blocks_all", "seo", "critical",
                                         "robots.txt disallows the whole site for all crawlers.",
                                         evidence={"agents": g["agents"], "rule": "Disallow: /"}))
            elif blocks_all:
                issues.append(make_issue("robots.blocks_agent", "seo", "high",
                                         "robots.txt disallows the whole site for specific crawlers.",
                                         evidence={"agents": g["agents"], "rule": "Disallow: /"}))
        asset_rules = sorted({"%s: %s" % (k.capitalize(), v) for g in groups if "*" in g["agents"]
                              for k, v in g["rules"] if k == "disallow" and v and v != "/"
                              and any(h in v.lower() for h in ASSET_HINTS)})
        if asset_rules:
            issues.append(make_issue("robots.may_block_assets", "seo", "low",
                                     "Disallow rules match common CSS/JS/asset paths; verify rendering resources are not blocked.",
                                     evidence=asset_rules, confidence="needs_manual_check"))
    elif r["status"] and r["status"] >= 500:
        issues.append(make_issue("robots.server_error", "seo", "medium",
                                 "robots.txt returns a server error, which can pause crawling.", evidence=r["status"]))
    else:
        meas["note"] = "No robots.txt (status %s). That is allowed; crawlers assume everything is crawlable." % r["status"]
    return meas, issues, sitemaps


def read_sitemap(url, kw):
    r = fetch(url, max_bytes=5_000_000, **kw)
    info = {"url": url, "status": r["status"], "error": r["error"]}
    if r["error"] or r["status"] != 200:
        return info, None, []
    body = r["body"]
    if body[:2] == b"\x1f\x8b":
        try:
            body = zlib.decompressobj(16 + zlib.MAX_WBITS).decompress(body, 50_000_000)
        except zlib.error as e:
            info["error"] = "gzip error: %s" % e
            return info, None, []
    head = body[:4096].lower()
    if b"<!doctype" in head or b"<!entity" in body[:20000].lower():
        info["error"] = "refused to parse: DTD/entity declaration present (or HTML page returned)"
        return info, None, []
    try:
        root = ET.fromstring(body)
    except ET.ParseError as e:
        info["error"] = "XML parse error: %s" % e
        return info, None, []
    kind = root.tag.split("}")[-1]
    locs = [e.text.strip() for e in root.iter() if e.tag.split("}")[-1] == "loc" and e.text]
    info["kind"] = kind
    info["entries"] = len(locs)
    return info, kind, locs


def check_status(url, kw):
    r = fetch(url, method="HEAD", read_body=False, **kw)
    if r["error"] or (r["status"] or 0) >= 400:
        r = fetch(url, method="GET", read_body=False, **kw)
    return r


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url")
    ap.add_argument("--sample", type=int, default=10)
    add_common_args(ap)
    args = ap.parse_args()
    kw = fetch_kwargs(args)
    base = normalize_url(args.url)
    sp = urllib.parse.urlsplit(base)
    origin = "%s://%s" % (sp.scheme, sp.netloc)
    out = {"tool": "check_crawl", "checked_at": now_iso(), "target": origin, "errors": []}

    rr = fetch(origin + "/robots.txt", **kw)
    robots_meas, issues, sitemaps = analyse_robots(rr, origin)
    out["robots"] = robots_meas
    if rr["error"]:
        out["errors"].append({"url": rr["url"], "error": rr["error"]})

    default_used = False
    if not sitemaps:
        sitemaps, default_used = [origin + "/sitemap.xml"], True
    out["sitemaps"] = []
    for sm in sitemaps[:3]:
        info, kind, locs = read_sitemap(sm, kw)
        if kind == "sitemapindex":
            info["children"] = locs[:20]
            for child in locs[:2]:
                cinfo, ckind, clocs = read_sitemap(child, kw)
                info.setdefault("child_details", []).append(cinfo)
                if ckind == "urlset":
                    locs_urls = clocs
                    info.setdefault("_urls", []).extend(locs_urls)
            urls = info.pop("_urls", [])
            info["note"] = "Sitemap index: only the first 2 child sitemaps were read."
        else:
            urls = locs if kind == "urlset" else []
        host = (urllib.parse.urlsplit(origin).hostname or "").lower()
        if urls:
            cross = [u for u in urls if (urllib.parse.urlsplit(u).hostname or "").lower() != host]
            httpu = [u for u in urls if urllib.parse.urlsplit(u).scheme == "http"] if sp.scheme == "https" else []
            info["urls_in_sample_source"] = len(urls)
            info["duplicate_urls"] = len(urls) - len(set(urls))
            if cross:
                issues.append(make_issue("sitemap.cross_host", "seo", "medium",
                                         "Sitemap lists URLs on a different host.", count=len(cross), examples=cross))
            if httpu:
                issues.append(make_issue("sitemap.http_urls", "seo", "medium",
                                         "Sitemap lists http:// URLs on an https site.", count=len(httpu), examples=httpu))
            if len(urls) > SITEMAP_URL_LIMIT:
                issues.append(make_issue("sitemap.too_many_urls", "seo", "medium",
                                         "Sitemap exceeds the 50,000 URL limit.", evidence=len(urls)))
            n = max(1, min(args.sample, len(urls)))
            step = len(urls) / n
            sample = [urls[int(i * step)] for i in range(n)]
            checked, bad = [], []
            for u in sample:
                rs = check_status(u, kw)
                row = {"url": u, "status": rs["status"], "error": rs["error"],
                       "location": get_header(rs["headers"], "location")}
                checked.append(row)
                if rs["error"] or rs["status"] != 200:
                    bad.append("%s -> %s" % (u, rs["status"] or rs["error"]))
            info["sample_checked"] = checked
            if bad:
                issues.append(make_issue("sitemap.urls_not_200", "seo", "medium",
                                         "Sampled sitemap URLs that do not return 200 directly.",
                                         count=len(bad), examples=bad,
                                         evidence={"sampled": len(sample), "of_total": len(urls)}))
        elif info["status"] == 200 and not info.get("error"):
            pass
        out["sitemaps"].append(info)
    found_ok = any(s["status"] == 200 and not s.get("error") for s in out["sitemaps"])
    if default_used and not found_ok:
        issues.append(make_issue("sitemap.not_found", "seo", "low",
                                 "No sitemap declared in robots.txt and none found at /sitemap.xml.",
                                 evidence=[{"url": s["url"], "status": s["status"], "error": s.get("error")} for s in out["sitemaps"]],
                                 confidence="likely"))
    elif default_used and found_ok:
        issues.append(make_issue("sitemap.not_in_robots", "seo", "low",
                                 "A sitemap exists at /sitemap.xml but robots.txt does not declare it."))

    st = fetch(origin + "/.well-known/security.txt", **kw)
    sec = {"url": st["url"], "status": st["status"], "error": st["error"]}
    if st["status"] == 200:
        txt = decode_text(st)
        sec["has_contact"] = any(l.lower().startswith("contact:") for l in txt.splitlines())
    out["security_txt"] = sec
    if not st["error"] and st["status"] != 200:
        issues.append(make_issue("security_txt.missing", "security", "low",
                                 "No security.txt at the standard location (optional best practice).",
                                 evidence={"status": st["status"]}))
    out["issues"] = issues
    out["caveats"] = ["robots.txt rules are listed as written; this script does not evaluate per-URL crawlability.",
                      "Only a sample of sitemap URLs is requested."]
    emit(out)


if __name__ == "__main__":
    main()
