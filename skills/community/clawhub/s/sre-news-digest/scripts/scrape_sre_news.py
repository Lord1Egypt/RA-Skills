#!/usr/bin/env python3
"""
Scrape https://sre.news for recent news articles.
Outputs a JSON array of {title, url, source} to stdout.

Usage:
    python scrape_sre_news.py [days]

Arguments:
    days  Number of days to look back (default: 1). The script filters
          articles by date markers found on the page when available.
"""

import json
import re
import sys
from datetime import datetime, timedelta, timezone
from urllib.parse import urlparse
from urllib.request import urlopen, Request
from html.parser import HTMLParser


# Map common domains to human-readable source names
SOURCE_MAP = {
    "kubernetes.io": "Kubernetes Blog",
    "etcd.io": "etcd Blog",
    "www.datadoghq.com": "Datadog Blog",
    "victoriametrics.com": "VictoriaMetrics Blog",
    "dev.to": "DEV Community",
    "thenewstack.io": "The New Stack",
    "www.infoq.com": "InfoQ",
    "devops.com": "DevOps.com",
    "techcommunity.microsoft.com": "Microsoft Tech Community",
    "aws.amazon.com": "AWS Blog",
    "cloud.google.com": "Google Cloud Blog",
    "www.cncf.io": "CNCF Blog",
    "grafana.com": "Grafana Blog",
    "www.hashicorp.com": "HashiCorp Blog",
    "blog.cloudflare.com": "Cloudflare Blog",
    "www.redhat.com": "Red Hat Blog",
    "cybersecuritynews.com": "Cyber Security News",
    "www.akamai.com": "Akamai Blog",
    "auth0.com": "Auth0 Blog",
    "www.mongodb.com": "MongoDB Blog",
    "forem.com": "Forem",
    "freek.dev": "Freek.dev",
    "www.51sec.org": "51Sec Blog",
    "observability-360.beehiiv.com": "Observability 360",
}


def source_from_url(url):
    """Derive a human-readable source/publication name from a URL."""
    hostname = urlparse(url).hostname or ""
    if hostname in SOURCE_MAP:
        return SOURCE_MAP[hostname]
    # Strip www. prefix and use domain as fallback
    name = hostname.lstrip("www.").split(".")[0] if hostname else "Unknown"
    return name.capitalize()


def title_from_url(url):
    """Extract a human-readable title from a URL path slug."""
    path = urlparse(url).path.rstrip("/")
    slug = path.split("/")[-1] if path else ""
    # Remove common hash/id suffixes (e.g., -21pi, -4d40)
    slug = re.sub(r'-[a-z0-9]{2,5}$', '', slug)
    title = slug.replace("-", " ").replace("_", " ").strip()
    return title.title() if title else url


class SRENewsParser(HTMLParser):
    """Parse sre.news homepage for news article links and date sections."""

    def __init__(self):
        super().__init__()
        self.articles = []
        self._in_link = False
        self._current_url = None
        self._text_buf = []
        self._current_date = None

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)

        if tag == "a" and "href" in attrs_dict:
            href = attrs_dict["href"]
            if href.startswith("http") and "sre.news" not in href:
                self._in_link = True
                self._current_url = href
                self._text_buf = []

    def handle_data(self, data):
        text = data.strip()
        if not text:
            return

        if self._in_link:
            self._text_buf.append(text)

        # Try to detect date markers in the page (e.g., "March 21, 2026" or "2026-03-21")
        date_match = re.match(
            r'^(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)?,?\s*'
            r'((?:January|February|March|April|May|June|July|August|September|October|November|December)'
            r'\s+\d{1,2},?\s+\d{4})$',
            text
        )
        if date_match:
            try:
                self._current_date = datetime.strptime(
                    date_match.group(1).replace(",", ""), "%B %d %Y"
                ).strftime("%Y-%m-%d")
            except ValueError:
                pass

        iso_match = re.match(r'^(\d{4}-\d{2}-\d{2})$', text)
        if iso_match:
            self._current_date = iso_match.group(1)

    def handle_endtag(self, tag):
        if self._in_link and tag == "a":
            self._in_link = False
            raw_title = " ".join(self._text_buf).strip()
            if self._current_url:
                # Determine title
                if raw_title and raw_title != ">_" and len(raw_title) > 3:
                    title = raw_title
                else:
                    title = title_from_url(self._current_url)

                article = {
                    "title": title,
                    "url": self._current_url,
                    "source": source_from_url(self._current_url),
                }
                if self._current_date:
                    article["date"] = self._current_date

                self.articles.append(article)
            self._current_url = None
            self._text_buf = []


def fetch_page(url):
    """Fetch a web page and return its HTML content."""
    req = Request(url, headers={
        "User-Agent": "Mozilla/5.0 (compatible; SRENewsDigest/1.0)"
    })
    with urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", errors="replace")


def scrape_sre_news(days=1):
    """Scrape sre.news and return articles from the last N days."""
    html = fetch_page("https://sre.news")

    parser = SRENewsParser()
    parser.feed(html)

    # Deduplicate by URL
    seen = set()
    unique = []
    for a in parser.articles:
        if a["url"] not in seen:
            seen.add(a["url"])
            unique.append(a)

    # Filter by date if date info is available
    if days and any("date" in a for a in unique):
        cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%d")
        filtered = [a for a in unique if a.get("date", "9999-99-99") >= cutoff]
        if filtered:
            return filtered

    # If no date info available or filtering yields nothing, return all
    return unique


if __name__ == "__main__":
    days = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    articles = scrape_sre_news(days)
    print(json.dumps(articles, indent=2, ensure_ascii=False))
    print(f"\n# Total: {len(articles)} articles found", file=sys.stderr)
