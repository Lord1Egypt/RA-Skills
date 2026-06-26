#!/usr/bin/env python3
"""SEO Audit Report - Comprehensive website SEO analysis."""

import argparse
import json
import re
import sys
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin, urlparse
from html.parser import HTMLParser


class SEOParser(HTMLParser):
    """Parse HTML for SEO-relevant elements."""

    def __init__(self):
        super().__init__()
        self.title = ""
        self.meta_description = ""
        self.meta_viewport = ""
        self.canonical = ""
        self.og_tags = {}
        self.twitter_tags = {}
        self.headings = {f"h{i}": [] for i in range(1, 7)}
        self.images = []  # (src, alt)
        self.links = []  # (href, text, is_internal)
        self._current_tag = None
        self._current_data = ""
        self._in_title = False
        self._in_heading = None
        self._heading_text = ""
        self._in_a = False
        self._a_href = ""
        self._a_text = ""
        self._body_text = ""
        self._in_body = False
        self._in_script = False
        self._in_style = False

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        tag_lower = tag.lower()

        if tag_lower == "title":
            self._in_title = True
            self._current_data = ""
        elif tag_lower == "meta":
            name = attrs_dict.get("name", "").lower()
            prop = attrs_dict.get("property", "").lower()
            content = attrs_dict.get("content", "")
            if name == "description":
                self.meta_description = content
            elif name == "viewport":
                self.meta_viewport = content
            elif prop.startswith("og:"):
                self.og_tags[prop] = content
            elif name.startswith("twitter:") or prop.startswith("twitter:"):
                key = name or prop
                self.twitter_tags[key] = content
        elif tag_lower == "link" and attrs_dict.get("rel") == "canonical":
            self.canonical = attrs_dict.get("href", "")
        elif tag_lower in self.headings:
            self._in_heading = tag_lower
            self._heading_text = ""
        elif tag_lower == "img":
            src = attrs_dict.get("src", "")
            alt = attrs_dict.get("alt", "")
            self.images.append((src, alt))
        elif tag_lower == "a":
            self._in_a = True
            self._a_href = attrs_dict.get("href", "")
            self._a_text = ""
        elif tag_lower == "body":
            self._in_body = True
        elif tag_lower == "script":
            self._in_script = True
        elif tag_lower == "style":
            self._in_style = True

    def handle_endtag(self, tag):
        tag_lower = tag.lower()
        if tag_lower == "title":
            self._in_title = False
            self.title = self._current_data.strip()
        elif tag_lower == self._in_heading:
            self.headings[self._in_heading].append(self._heading_text.strip())
            self._in_heading = None
        elif tag_lower == "a" and self._in_a:
            self._in_a = False
            self.links.append((self._a_href, self._a_text.strip()))
        elif tag_lower == "script":
            self._in_script = False
        elif tag_lower == "style":
            self._in_style = False

    def handle_data(self, data):
        if self._in_title:
            self._current_data += data
        if self._in_heading:
            self._heading_text += data
        if self._in_a:
            self._a_text += data
        if self._in_body and not self._in_script and not self._in_style:
            self._body_text += data

    @property
    def word_count(self):
        return len(self._body_text.split())


def fetch_page(url, timeout=15):
    """Fetch URL, return (status, headers, body, response_time)."""
    import time
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; SEOAuditBot/1.0)"
        }
        req = urllib.request.Request(url, headers=headers)
        start = time.time()
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            elapsed = time.time() - start
            return resp.status, dict(resp.headers), body, elapsed
    except urllib.error.HTTPError as e:
        return e.code, {}, "", 0
    except Exception as e:
        print(f"  Error: {url} - {e}", file=sys.stderr)
        return 0, {}, "", 0


def check_robots_txt(base_url):
    """Check robots.txt."""
    url = urljoin(base_url, "/robots.txt")
    status, _, body, _ = fetch_page(url)
    return {
        "exists": status == 200,
        "has_sitemap": "sitemap:" in body.lower() if body else False,
        "blocks_all": "disallow: /" in body.lower() if body else False,
    }


def check_sitemap(base_url):
    """Check sitemap.xml."""
    url = urljoin(base_url, "/sitemap.xml")
    status, _, body, _ = fetch_page(url)
    url_count = body.count("<url>") if body else 0
    return {
        "exists": status == 200,
        "url_count": url_count,
    }


def audit_page(url, base_domain):
    """Audit a single page."""
    status, headers, body, response_time = fetch_page(url)
    if status != 200 or not body:
        return {"url": url, "status": status, "error": True}

    parser = SEOParser()
    try:
        parser.feed(body)
    except Exception:
        pass

    # Classify links
    internal_links = []
    external_links = []
    broken_candidates = []
    for href, text in parser.links:
        if not href or href.startswith("#") or href.startswith("javascript:"):
            continue
        full_url = urljoin(url, href)
        parsed = urlparse(full_url)
        if parsed.netloc == base_domain or not parsed.netloc:
            internal_links.append(full_url)
        else:
            external_links.append(full_url)

    # Images without alt
    images_total = len(parser.images)
    images_no_alt = sum(1 for _, alt in parser.images if not alt.strip())

    return {
        "url": url,
        "status": status,
        "response_time": response_time,
        "content_size": len(body),
        "title": parser.title,
        "title_length": len(parser.title),
        "meta_description": parser.meta_description,
        "meta_desc_length": len(parser.meta_description),
        "has_viewport": bool(parser.meta_viewport),
        "canonical": parser.canonical,
        "og_tags": parser.og_tags,
        "twitter_tags": parser.twitter_tags,
        "headings": {k: v for k, v in parser.headings.items() if v},
        "h1_count": len(parser.headings["h1"]),
        "word_count": parser.word_count,
        "images_total": images_total,
        "images_no_alt": images_no_alt,
        "internal_links": len(internal_links),
        "external_links": len(external_links),
        "is_https": url.startswith("https://"),
    }


def score_technical(pages, robots, sitemap, base_url):
    """Score technical SEO (0-100)."""
    score = 100
    issues = []

    if not base_url.startswith("https://"):
        score -= 20
        issues.append(("CRITICAL", "Site not using HTTPS"))

    if not robots["exists"]:
        score -= 10
        issues.append(("HIGH", "Missing robots.txt"))
    elif robots["blocks_all"]:
        score -= 25
        issues.append(("CRITICAL", "robots.txt blocks all crawlers"))

    if not sitemap["exists"]:
        score -= 10
        issues.append(("HIGH", "Missing sitemap.xml"))

    for page in pages:
        if page.get("error"):
            score -= 5
            issues.append(("HIGH", f"Page returned {page['status']}: {page['url']}"))
        elif page.get("response_time", 0) > 3:
            score -= 3
            issues.append(("MEDIUM", f"Slow response ({page['response_time']:.1f}s): {page['url']}"))

    return max(0, score), issues


def score_onpage(pages):
    """Score on-page SEO (0-100)."""
    score = 100
    issues = []

    for page in pages:
        if page.get("error"):
            continue

        url_short = page["url"]

        # Title
        if not page["title"]:
            score -= 10
            issues.append(("CRITICAL", f"Missing title tag: {url_short}"))
        elif page["title_length"] < 30:
            score -= 3
            issues.append(("MEDIUM", f"Title too short ({page['title_length']} chars): {url_short}"))
        elif page["title_length"] > 60:
            score -= 2
            issues.append(("LOW", f"Title too long ({page['title_length']} chars): {url_short}"))

        # Meta description
        if not page["meta_description"]:
            score -= 8
            issues.append(("HIGH", f"Missing meta description: {url_short}"))
        elif page["meta_desc_length"] < 70:
            score -= 2
            issues.append(("LOW", f"Meta description too short: {url_short}"))
        elif page["meta_desc_length"] > 160:
            score -= 2
            issues.append(("LOW", f"Meta description too long: {url_short}"))

        # H1
        if page["h1_count"] == 0:
            score -= 8
            issues.append(("HIGH", f"Missing H1 tag: {url_short}"))
        elif page["h1_count"] > 1:
            score -= 3
            issues.append(("MEDIUM", f"Multiple H1 tags ({page['h1_count']}): {url_short}"))

        # Viewport
        if not page["has_viewport"]:
            score -= 5
            issues.append(("HIGH", f"Missing viewport meta tag: {url_short}"))

        # Images
        if page["images_no_alt"] > 0:
            score -= min(5, page["images_no_alt"])
            issues.append(("MEDIUM", f"{page['images_no_alt']}/{page['images_total']} images missing alt text: {url_short}"))

        # OG tags
        if not page["og_tags"]:
            score -= 3
            issues.append(("LOW", f"Missing Open Graph tags: {url_short}"))

    return max(0, score), issues


def score_content(pages):
    """Score content quality (0-100)."""
    score = 100
    issues = []

    for page in pages:
        if page.get("error"):
            continue
        url_short = page["url"]

        if page["word_count"] < 300:
            score -= 8
            issues.append(("HIGH", f"Thin content ({page['word_count']} words): {url_short}"))
        elif page["word_count"] < 500:
            score -= 3
            issues.append(("MEDIUM", f"Short content ({page['word_count']} words): {url_short}"))

    # Check for duplicate titles
    titles = [p["title"] for p in pages if not p.get("error") and p["title"]]
    dupes = set(t for t in titles if titles.count(t) > 1)
    for d in dupes:
        score -= 5
        issues.append(("HIGH", f"Duplicate title: '{d}'"))

    return max(0, score), issues


def score_links(pages):
    """Score link health (0-100)."""
    score = 100
    issues = []

    for page in pages:
        if page.get("error"):
            continue
        if page["internal_links"] == 0:
            score -= 5
            issues.append(("MEDIUM", f"No internal links: {page['url']}"))

    return max(0, score), issues


def generate_report(url, pages, robots, sitemap):
    """Generate the full audit report."""
    base = urlparse(url)
    base_url = f"{base.scheme}://{base.netloc}"

    tech_score, tech_issues = score_technical(pages, robots, sitemap, base_url)
    onpage_score, onpage_issues = score_onpage(pages)
    content_score, content_issues = score_content(pages)
    link_score, link_issues = score_links(pages)

    overall = int(tech_score * 0.35 + onpage_score * 0.35 + content_score * 0.15 + link_score * 0.15)

    def rating(s):
        if s >= 90: return "Excellent"
        if s >= 70: return "Good"
        if s >= 50: return "Fair"
        return "Poor"

    report = f"""# SEO Audit Report
**URL:** {url}
**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Pages Analyzed:** {len(pages)}

## Overall Score: {overall}/100 ({rating(overall)})

| Category | Score | Rating |
|----------|-------|--------|
| Technical SEO | {tech_score}/100 | {rating(tech_score)} |
| On-Page SEO | {onpage_score}/100 | {rating(onpage_score)} |
| Content Quality | {content_score}/100 | {rating(content_score)} |
| Link Health | {link_score}/100 | {rating(link_score)} |

## Technical SEO ({tech_score}/100)
- HTTPS: {'Yes' if url.startswith('https') else 'NO'}
- robots.txt: {'Found' if robots['exists'] else 'MISSING'}
- sitemap.xml: {'Found' if sitemap['exists'] else 'MISSING'}{f" ({sitemap['url_count']} URLs)" if sitemap['exists'] else ''}

## Issues Found ({len(tech_issues) + len(onpage_issues) + len(content_issues) + len(link_issues)} total)

### Critical
"""
    all_issues = tech_issues + onpage_issues + content_issues + link_issues
    for severity in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
        filtered = [i for i in all_issues if i[0] == severity]
        if filtered:
            report += f"\n### {severity.title()} ({len(filtered)})\n"
            for _, desc in filtered:
                report += f"- {desc}\n"

    report += f"\n## Recommendations\n"
    if any(i[0] == "CRITICAL" for i in all_issues):
        report += "1. **Fix critical issues first** — these directly harm search visibility\n"
    report += "2. Address high-priority issues within 1-2 weeks\n"
    report += "3. Schedule medium/low issues for monthly maintenance\n"
    report += "4. Re-run this audit after fixes to verify improvements\n"

    return report, overall


def crawl_site(start_url, max_depth=1, max_pages=20):
    """Simple BFS crawler."""
    parsed = urlparse(start_url)
    base_domain = parsed.netloc
    visited = set()
    queue = [(start_url, 0)]
    pages = []

    while queue and len(pages) < max_pages:
        url, depth = queue.pop(0)
        if url in visited:
            continue
        visited.add(url)

        print(f"  Auditing: {url}")
        result = audit_page(url, base_domain)
        pages.append(result)

        if depth < max_depth and not result.get("error"):
            # Add internal links to queue
            status, _, body, _ = fetch_page(url)
            if body:
                for match in re.finditer(r'href=["\']([^"\']+)["\']', body):
                    href = match.group(1)
                    full = urljoin(url, href)
                    p = urlparse(full)
                    if p.netloc == base_domain and full not in visited:
                        clean = f"{p.scheme}://{p.netloc}{p.path}"
                        if clean not in visited:
                            queue.append((clean, depth + 1))

    return pages


def main():
    parser = argparse.ArgumentParser(description="SEO Audit Report Generator")
    parser.add_argument("--url", required=True, help="URL to audit")
    parser.add_argument("--depth", type=int, default=1, help="Crawl depth (default: 1)")
    parser.add_argument("--quick", action="store_true", help="Single page only")
    parser.add_argument("--output", help="Output file path")
    parser.add_argument("--max-pages", type=int, default=20)

    args = parser.parse_args()

    url = args.url
    if not url.startswith("http"):
        url = f"https://{url}"

    print(f"SEO Audit: {url}")
    print(f"Depth: {'single page' if args.quick else args.depth}")

    # Check robots and sitemap
    parsed = urlparse(url)
    base_url = f"{parsed.scheme}://{parsed.netloc}"
    print("Checking robots.txt...")
    robots = check_robots_txt(base_url)
    print("Checking sitemap.xml...")
    sitemap = check_sitemap(base_url)

    # Crawl
    depth = 0 if args.quick else args.depth
    pages = crawl_site(url, max_depth=depth, max_pages=args.max_pages)

    # Generate report
    report, score = generate_report(url, pages, robots, sitemap)

    if args.output:
        Path(args.output).write_text(report)
        print(f"\nReport saved to: {args.output}")
    else:
        print(report)


if __name__ == "__main__":
    main()
