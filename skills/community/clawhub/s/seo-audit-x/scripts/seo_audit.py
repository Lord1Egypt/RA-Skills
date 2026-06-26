#!/usr/bin/env python3
"""
SEO Audit Script
Usage: python3 seo_audit.py --url <URL> [--competitors url1,url2] [--keywords kw1,kw2]
Fetches a page and outputs a structured JSON audit payload for the agent to interpret.
"""

import argparse
import json
import re
import sys
import urllib.request
import urllib.parse
from html.parser import HTMLParser


class SEOParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ""
        self.meta_description = ""
        self.h1s = []
        self.h2s = []
        self.h3s = []
        self.images_without_alt = 0
        self.images_total = 0
        self.canonical = ""
        self.robots_meta = ""
        self.viewport = ""
        self.schema_present = False
        self.og_title = ""
        self.https = False
        self._in_title = False
        self._current_heading = None
        self._in_script = False
        self._script_type = ""
        self._body_text_parts = []
        self._in_body = False

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        tag = tag.lower()

        if tag == "title":
            self._in_title = True
        elif tag == "meta":
            name = attrs_dict.get("name", "").lower()
            prop = attrs_dict.get("property", "").lower()
            content = attrs_dict.get("content", "")
            if name == "description":
                self.meta_description = content
            elif name == "robots":
                self.robots_meta = content
            elif name == "viewport":
                self.viewport = content
            elif prop == "og:title":
                self.og_title = content
        elif tag == "link":
            rel = attrs_dict.get("rel", "").lower()
            if rel == "canonical":
                self.canonical = attrs_dict.get("href", "")
        elif tag in ("h1", "h2", "h3"):
            self._current_heading = tag
        elif tag == "img":
            self.images_total += 1
            alt = attrs_dict.get("alt", "")
            if not alt.strip():
                self.images_without_alt += 1
        elif tag == "script":
            self._in_script = True
            self._script_type = attrs_dict.get("type", "")
            if "application/ld+json" in self._script_type:
                self.schema_present = True
        elif tag == "body":
            self._in_body = True

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag == "title":
            self._in_title = False
        elif tag in ("h1", "h2", "h3"):
            self._current_heading = None
        elif tag == "script":
            self._in_script = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data.strip()
        elif self._current_heading == "h1":
            self.h1s.append(data.strip())
        elif self._current_heading == "h2":
            self.h2s.append(data.strip())
        elif self._current_heading == "h3":
            self.h3s.append(data.strip())
        elif self._in_body and not self._in_script and data.strip():
            self._body_text_parts.append(data.strip())


def fetch_page(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (compatible; SEOAuditBot/1.0)"
    })
    with urllib.request.urlopen(req, timeout=15) as response:
        return response.read().decode("utf-8", errors="replace"), response.geturl()


def calculate_keyword_density(text, keywords):
    if not text or not keywords:
        return {}
    text_lower = text.lower()
    word_count = len(text_lower.split())
    densities = {}
    for kw in keywords:
        count = text_lower.count(kw.lower())
        densities[kw] = {
            "count": count,
            "density_pct": round((count / word_count * 100), 2) if word_count > 0 else 0
        }
    return densities


def score_audit(audit):
    score = 0

    # Title (0-8)
    title = audit["title"]
    if title:
        score += 2
        if 50 <= len(title) <= 60:
            score += 3
        elif 40 <= len(title) <= 70:
            score += 1
        if audit["keywords"] and any(k.lower() in title.lower() for k in audit["keywords"]):
            score += 3

    # Meta description (0-6)
    desc = audit["meta_description"]
    if desc:
        score += 2
        if 150 <= len(desc) <= 160:
            score += 2
        if audit["keywords"] and any(k.lower() in desc.lower() for k in audit["keywords"]):
            score += 2

    # H1 (0-5)
    h1s = audit["h1s"]
    if len(h1s) == 1:
        score += 3
        if audit["keywords"] and any(k.lower() in h1s[0].lower() for k in audit["keywords"]):
            score += 2
    elif len(h1s) > 1:
        score += 1  # Has H1 but multiple

    # H2s (0-3)
    if len(audit["h2s"]) >= 2:
        score += 3
    elif len(audit["h2s"]) == 1:
        score += 1

    # Images (0-4)
    if audit["images_total"] > 0:
        coverage = (audit["images_total"] - audit["images_without_alt"]) / audit["images_total"]
        score += round(coverage * 4)
    else:
        score += 4  # No images = not penalized

    # Technical (0-10)
    if audit["https"]:
        score += 2
    if audit["viewport"]:
        score += 2
    if audit["canonical"]:
        score += 2
    if audit["schema_present"]:
        score += 2
    if audit["robots_meta"] and "noindex" not in audit["robots_meta"].lower():
        score += 2
    elif not audit["robots_meta"]:
        score += 2  # Absence of noindex is fine

    # Content (0-14)
    word_count = audit["word_count"]
    if word_count >= 1500:
        score += 5
    elif word_count >= 800:
        score += 3
    elif word_count >= 400:
        score += 1

    # Keyword density
    if audit["keyword_densities"]:
        for kw, data in audit["keyword_densities"].items():
            d = data["density_pct"]
            if 0.8 <= d <= 2.5:
                score += 3
                break
            elif 0 < d < 0.8 or 2.5 < d <= 4:
                score += 1
                break

    score += min(6, len(audit["h2s"]) * 2)  # up to 6 points for content structure

    return min(score, 100)


def audit_url(url, keywords=None, competitors=None):
    if not url.startswith("http"):
        url = "https://" + url

    html, final_url = fetch_page(url)

    parser = SEOParser()
    parser.feed(html)
    parser.https = final_url.startswith("https://")

    body_text = " ".join(parser._body_text_parts)
    word_count = len(body_text.split())

    audit = {
        "url": final_url,
        "https": parser.https,
        "title": parser.title,
        "title_length": len(parser.title),
        "meta_description": parser.meta_description,
        "meta_description_length": len(parser.meta_description),
        "h1s": [h for h in parser.h1s if h],
        "h2s": [h for h in parser.h2s if h],
        "h3s": [h for h in parser.h3s if h],
        "canonical": parser.canonical,
        "robots_meta": parser.robots_meta,
        "viewport": parser.viewport,
        "schema_present": parser.schema_present,
        "og_title": parser.og_title,
        "images_total": parser.images_total,
        "images_without_alt": parser.images_without_alt,
        "word_count": word_count,
        "keywords": keywords or [],
        "keyword_densities": calculate_keyword_density(body_text, keywords or []),
    }

    audit["score"] = score_audit(audit)

    issues = []
    if not audit["title"]:
        issues.append("CRITICAL: Missing title tag")
    elif len(audit["title"]) > 60:
        issues.append(f"Title too long ({len(audit['title'])} chars) — truncated in SERPs")
    elif len(audit["title"]) < 40:
        issues.append(f"Title too short ({len(audit['title'])} chars) — leaving ranking real estate unused")

    if not audit["meta_description"]:
        issues.append("Missing meta description — Google will auto-generate (usually worse)")
    elif len(audit["meta_description"]) > 160:
        issues.append(f"Meta description too long ({len(audit['meta_description'])} chars)")

    if len(audit["h1s"]) == 0:
        issues.append("CRITICAL: No H1 tag found")
    elif len(audit["h1s"]) > 1:
        issues.append(f"Multiple H1 tags ({len(audit['h1s'])}) — confuses crawlers")

    if not audit["https"]:
        issues.append("CRITICAL: Not on HTTPS — security and ranking penalty")

    if not audit["viewport"]:
        issues.append("Missing viewport meta tag — mobile SEO penalty")

    if audit["images_without_alt"] > 0:
        issues.append(f"{audit['images_without_alt']} images missing alt text")

    if audit["word_count"] < 300:
        issues.append(f"Very thin content ({audit['word_count']} words) — likely to be filtered")

    audit["issues"] = issues
    return audit


def main():
    parser = argparse.ArgumentParser(description="SEO Audit Tool")
    parser.add_argument("--url", required=True, help="URL to audit")
    parser.add_argument("--keywords", default="", help="Comma-separated target keywords")
    parser.add_argument("--competitors", default="", help="Comma-separated competitor URLs")
    parser.add_argument("--output", default="json", choices=["json", "summary"])
    args = parser.parse_args()

    keywords = [k.strip() for k in args.keywords.split(",") if k.strip()]
    competitor_urls = [c.strip() for c in args.competitors.split(",") if c.strip()]

    print(f"Auditing: {args.url}", file=sys.stderr)
    result = audit_url(args.url, keywords=keywords)

    competitor_results = []
    for comp_url in competitor_urls:
        print(f"Auditing competitor: {comp_url}", file=sys.stderr)
        try:
            comp_result = audit_url(comp_url, keywords=keywords)
            competitor_results.append(comp_result)
        except Exception as e:
            competitor_results.append({"url": comp_url, "error": str(e)})

    output = {
        "primary": result,
        "competitors": competitor_results
    }

    if args.output == "json":
        print(json.dumps(output, indent=2))
    else:
        print(f"\n=== SEO AUDIT: {result['url']} ===")
        print(f"Score: {result['score']}/100")
        print(f"Title: {result['title'][:60]}... ({result['title_length']} chars)")
        print(f"Meta desc: {result['meta_description_length']} chars")
        print(f"H1s: {result['h1s']}")
        print(f"Word count: {result['word_count']}")
        print(f"HTTPS: {result['https']}")
        print(f"\nIssues ({len(result['issues'])}):")
        for issue in result["issues"]:
            print(f"  ⚠ {issue}")


if __name__ == "__main__":
    main()
