#!/usr/bin/env python3
"""
Tech News Bulletin - Collect RSS feeds and TLDR.tech AI newsletter, then send via email.
Combines tech-news-digest (RSS) and tldr-html-sanitizer (TLDR.tech HTML) into one digest.
"""

import feedparser
import logging
import sys
import os
import re
import html as html_lib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from datetime import datetime, date, timedelta
from dataclasses import dataclass
from typing import Iterable
from urllib.parse import urlparse
import html
import requests

logging.basicConfig(
    filename='/tmp/openclaw-debug.log',
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

RSS_FEEDS = [
    "https://techcrunch.com/feed/",
    "https://www.wired.com/feed/tag/ai/latest/rss",
    #"https://blog.google/innovation-and-ai/technology/ai/rss/"
]

EMAIL_ADDRESSES = [
    "juniarto_samsudin@a-star.edu.sg",
    "wei_qingsong@a-star.edu.sg",
    "yang_yechao@a-star.edu.sg",
    "lus@a-star.edu.sg",
    "gao_bo@a-star.edu.sg"
]

TLDR_BASE_URL = "https://tldr.tech/ai/"
MAX_ARTICLES = 25
MIN_ARTICLE_WORDS = 50  # minimum word count after clean_html() to be considered real content
_NO_CONTENT = object()   # sentinel: article fetched but has no usable content

# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

def clean_html(text):
    """Remove HTML tags and decode entities."""
    if not text:
        return ""
    from bs4 import BeautifulSoup
    return BeautifulSoup(text, "html.parser").get_text(separator=' ', strip=True)


# ---------------------------------------------------------------------------
# RSS feed helpers (from tech-news-digest)
# ---------------------------------------------------------------------------

def fetch_articles(feed_url, limit=None):
    """Fetch articles from an RSS feed."""
    feed = feedparser.parse(feed_url)
    articles = []

    for entry in feed.entries:
        published = ''
        if hasattr(entry, 'published_parsed') and entry.published_parsed:
            published = datetime(*entry.published_parsed[:6]).strftime('%Y-%m-%dT%H:%M:%S')
        elif entry.get('published'):
            try:
                from email.utils import parsedate_to_datetime
                published = parsedate_to_datetime(entry.published).strftime('%Y-%m-%dT%H:%M:%S')
            except Exception:
                published = entry.get('published', '')

        desc = entry.get('summary', '')
        if not desc and hasattr(entry, 'content') and entry.content:
            desc = entry.content[0].get('value', '')

        articles.append({
            'title': clean_html(entry.get('title', '(no title)')),
            'link': entry.get('link', ''),
            'published': published,
            'description': clean_html(desc),
            'source': feed.feed.get('title', feed_url),
        })

    return articles[:limit] if limit is not None else articles


# ---------------------------------------------------------------------------
# TLDR HTML sanitizer (inlined from tldr-html-sanitizer skill)
# ---------------------------------------------------------------------------

READ_TIME_RE = re.compile(r"\s*\(\d+\s+minute\s+read\)\s*$", re.IGNORECASE)
SPONSOR_RE = re.compile(r"\bsponsor(?:ed)?\b", re.IGNORECASE)
WHITESPACE_RE = re.compile(r"\s+")
TRACKING_QUERY_RE = re.compile(r"^(utm_|mc_|guccounter|fbclid|gclid)", re.IGNORECASE)


@dataclass
class TLDRArticle:
    title: str
    link: str
    summary: str


def _normalize_space(text: str) -> str:
    text = html_lib.unescape(text or "")
    text = text.replace("\xa0", " ")
    text = WHITESPACE_RE.sub(" ", text)
    return text.strip()


def _clean_title(title: str) -> str:
    title = _normalize_space(title)
    title = READ_TIME_RE.sub("", title)
    return title.strip(" -\u2013\u2014")


def _clean_link(link: str) -> str:
    link = html_lib.unescape((link or "").strip())
    if not link:
        return ""
    parsed = urlparse(link)
    if parsed.scheme not in {"http", "https"}:
        return link
    if not parsed.query:
        return link
    filtered_pairs = [
        pair for pair in parsed.query.split("&")
        if not TRACKING_QUERY_RE.match(pair.split("=", 1)[0])
    ]
    parsed = parsed._replace(query="&".join(filtered_pairs))
    return parsed.geturl()


def _is_sponsor(title: str, link: str) -> bool:
    return any(SPONSOR_RE.search(h) for h in [title or "", link or ""])


def _get_text(node) -> str:
    if node is None:
        return ""
    return _normalize_space(node.get_text(" ", strip=True))


def _extract_from_articles(soup) -> list:
    results = []
    seen = set()
    for article in soup.find_all("article"):
        link_tag = article.find("a", href=True)
        title_tag = article.find(["h1", "h2", "h3", "h4"])
        summary_tag = article.find(class_=re.compile(r"newsletter-html|summary|excerpt", re.I))

        title = _clean_title(_get_text(title_tag))
        link = _clean_link(link_tag.get("href", "") if link_tag else "")
        summary = _get_text(summary_tag)

        if not title and link_tag:
            title = _clean_title(_get_text(link_tag))
        if not summary:
            text = _get_text(article)
            if title and text.startswith(title):
                text = _normalize_space(text[len(title):])
            summary = text

        if not title or not link or not summary:
            continue
        if _is_sponsor(title, link):
            continue

        key = (title.lower(), link)
        if key in seen:
            continue
        seen.add(key)
        results.append(TLDRArticle(title=title, link=link, summary=summary))

    return results


def _extract_fallback(soup) -> list:
    results = []
    seen = set()
    for heading in soup.find_all(["h1", "h2", "h3", "h4"]):
        parent = heading.parent
        if parent is None:
            continue
        link_tag = heading.find_parent("a", href=True) or parent.find("a", href=True)
        title = _clean_title(_get_text(heading))
        link = _clean_link(link_tag.get("href", "") if link_tag else "")
        if not title or not link or _is_sponsor(title, link):
            continue

        summary = ""
        cursor = parent.find_next_sibling()
        steps = 0
        while cursor is not None and steps < 3:
            text = _get_text(cursor)
            if text and len(text.split()) >= 8 and not SPONSOR_RE.search(text):
                summary = text
                break
            cursor = cursor.find_next_sibling() if hasattr(cursor, "find_next_sibling") else None
            steps += 1

        if not summary:
            continue

        key = (title.lower(), link)
        if key in seen:
            continue
        seen.add(key)
        results.append(TLDRArticle(title=title, link=link, summary=summary))

    return results


def extract_tldr_articles(html_text: str) -> list:
    """Parse raw TLDR HTML and return TLDRArticle instances."""
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        logging.error("beautifulsoup4 is required: pip install beautifulsoup4")
        return []

    soup = BeautifulSoup(html_text, "html.parser")
    articles = _extract_from_articles(soup)
    if articles:
        return articles
    return _extract_fallback(soup)


def fetch_tldr_articles(target_date: date) -> list:
    """Fetch and sanitize the TLDR AI newsletter for a given date.

    Returns a list of article dicts compatible with the RSS article format.
    """
    url = f"{TLDR_BASE_URL}{target_date.strftime('%Y-%m-%d')}"
    logging.debug(f"Fetching TLDR newsletter: {url}")
    try:
        resp = requests.get(url, timeout=20, headers={"User-Agent": "Mozilla/5.0"})
        resp.raise_for_status()
    except Exception as e:
        logging.warning(f"Failed to fetch TLDR newsletter at {url}: {e}")
        return []

    tldr_articles = extract_tldr_articles(resp.text)
    published_str = target_date.strftime('%Y-%m-%dT00:00:00')

    articles = []
    for tldr in tldr_articles:
        articles.append({
            'title': tldr.title,
            'link': tldr.link,
            'published': published_str,
            'description': tldr.summary,
            'source': 'TLDR AI',
        })

    logging.debug(f"Got {len(articles)} articles from TLDR newsletter ({url})")
    return articles


# ---------------------------------------------------------------------------
# Ollama summarizer (from tech-news-digest)
# ---------------------------------------------------------------------------

def summarize_article(url, model="glm-4.7-flash:latest"):
    """Fetch article content and summarize using Ollama."""
    try:
        resp = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
        resp.raise_for_status()
        text = clean_html(resp.text)
        text = text[:2000]
        if len(text.split()) < MIN_ARTICLE_WORDS:
            logging.warning(f"Skipping article (insufficient content after clean_html): {url}")
            return _NO_CONTENT
    except Exception:
        return None

    try:
        logging.debug(f"Summarizing article with Ollama: {text}...")
        resp = requests.post(
            "http://172.20.86.203:11434/api/generate",
            json={
                "model": model,
                "prompt": (
                    f"Summarize this news article in 5 sentences:\n\n{text}"
                    #f"Summarize this news article in 5 sentences.\n"
                    f"If the content is not summarizable, "
                    f"respond with exactly: Cannot Summarize\n\n"
                ),
                "stream": False,
            },
            timeout=60,
        )
        resp.raise_for_status()
        result = resp.json().get("response", "").strip()
        logging.debug(f"Ollama summary result: {result}")
        if result.lower() == "cannot summarize":
            logging.warning(f"LLM returned 'Cannot Summarize' for: {url}")
            return _NO_CONTENT
        return result or None
    except requests.exceptions.Timeout:
        logging.warning(f"LLM timeout for: {url}")
        return _NO_CONTENT
    except Exception:
        logging.exception(f"Unexpected error while summarizing article: {url}")
        return None


# ---------------------------------------------------------------------------
# Digest builder
# ---------------------------------------------------------------------------

SOURCE_BADGE_COLORS = {
    'TLDR AI': '#0891b2',   # teal
}
DEFAULT_BADGE_COLOR = '#6b7280'  # gray


def build_digest(articles):
    """Build digest content as HTML with source badges."""
    digest = []

    for article in articles:
        # TLDR AI articles already have a curated summary — skip Ollama
        if article.get('source') == 'TLDR AI':
            summary = None
        else:
            try:
                summary = summarize_article(article['link'])
            except Exception:
                summary = None

        if summary is _NO_CONTENT:
            logging.debug(f"Expunging article with no real content: {article.get('link')}")
            continue

        if not summary and article.get('description'):
            desc = article['description']
            # TLDR AI articles: use the full curated summary without truncation
            if article.get('source') == 'TLDR AI':
                summary = desc
            else:
                summary = f"{desc[:150]}..." if len(desc) > 150 else desc

        title_escaped = html.escape(article['title'])
        link_escaped = html.escape(article['link'])
        source = article.get('source', '')
        badge_color = SOURCE_BADGE_COLORS.get(source, DEFAULT_BADGE_COLOR)
        source_escaped = html.escape(source)

        entry = f'<div style="margin-bottom:24px;">'
        entry += f'<h3 style="font-size:18px;font-weight:bold;margin:0 0 4px 0;">'
        entry += f'<a href="{link_escaped}" style="color:#1a0dab;text-decoration:none;">{title_escaped}</a>'
        entry += f'</h3>'
        if source:
            entry += (
                f'<span style="display:inline-block;background:{badge_color};color:#fff;'
                f'font-size:11px;font-weight:600;padding:1px 7px;border-radius:10px;'
                f'margin-bottom:6px;">{source_escaped}</span>'
            )
        if summary:
            summary_escaped = html.escape(summary)
            entry += f'<p style="margin:4px 0 0;color:#444;font-size:14px;">{summary_escaped}</p>'
        entry += f'</div>'

        digest.append(entry)

    body = "\n".join(digest)
    today = date.today().strftime('%B %d, %Y')
    return f"""<!DOCTYPE html>
<html><body style="font-family:Arial,sans-serif;max-width:700px;margin:auto;padding:24px;">
<div style="border-bottom:2px solid #eee;padding-bottom:8px;margin-bottom:16px;">
<h1 style="font-size:24px;margin:0 0 4px 0;">Daily Tech &amp; AI News Bulletin</h1>
<p style="font-size:13px;color:#888;margin:0;">{today} &mdash; Sources: RSS Feeds + TLDR AI Newsletter</p>
<p style="font-size:13px;color:#888;margin:0;">By: openclaw-glm-4.7-ollama@172.20.86.203</p>
</div>
{body}
</body></html>"""


# ---------------------------------------------------------------------------
# Email sender (from tech-news-digest)
# ---------------------------------------------------------------------------

def send_email(smtp_email, smtp_password, to_address, digest_content, subject="Daily Tech & AI News Bulletin"):
    """Send bulletin email using SMTP with provided credentials."""
    msg = MIMEMultipart()
    msg['From'] = formataddr(("AI Health Bulletin", smtp_email))
    msg['To'] = to_address
    msg['Subject'] = subject

    msg.attach(MIMEText(digest_content, 'html'))

    try:
        import smtplib
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(smtp_email, smtp_password)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        logging.error(f"Failed to send to {to_address}: {e}")
        return False


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    logging.debug(f"using Python: {sys.executable}")
    logging.debug(f"Tech News Bulletin starting at {datetime.now()}")

    # --- Fetch RSS articles ---
    rss_articles = []
    for feed_url in RSS_FEEDS:
        logging.debug(f"Fetching RSS feed: {feed_url}")
        limit = 8 if "techcrunch.com" in feed_url else None
        rss_articles.extend(fetch_articles(feed_url, limit=limit))
    logging.debug(f"Fetched {len(rss_articles)} RSS articles (before dedup)")

    # --- Fetch TLDR AI newsletter (previous day) ---
    yesterday = date.today() - timedelta(days=1)
    tldr_articles = fetch_tldr_articles(yesterday)

    # --- Merge, deduplicate, sort, limit ---
    all_articles = rss_articles + tldr_articles
    seen_urls = set()
    unique_articles = []
    for article in all_articles:
        if article['link'] and article['link'] not in seen_urls:
            seen_urls.add(article['link'])
            unique_articles.append(article)

    unique_articles.sort(
        key=lambda x: x['published'] or '1970-01-01T00:00:00',
        reverse=True,
    )
    articles_to_digest = unique_articles[:MAX_ARTICLES]

    logging.debug(
        f"Merged: {len(rss_articles)} RSS + {len(tldr_articles)} TLDR = "
        f"{len(unique_articles)} unique → top {len(articles_to_digest)} selected"
    )

    # --- Build digest ---
    digest_content = build_digest(articles_to_digest)

    logging.debug("=" * 60)
    logging.debug("TECH NEWS BULLETIN")
    logging.debug("=" * 60 + "\n" + digest_content)

    # --- Send emails ---
    smtp_email = os.environ.get('SMTP_EMAIL', '')
    smtp_password = os.environ.get('SMTP_PASSWORD', '')

    if not smtp_email or not smtp_password:
        logging.warning("SMTP_EMAIL or SMTP_PASSWORD not set - skipping email delivery")
    else:
        logging.debug("Sending bulletin to recipients...")
        for email_addr in EMAIL_ADDRESSES:
            success = send_email(smtp_email, smtp_password, email_addr, digest_content)
            if success:
                logging.debug(f"Sent to {email_addr}")

    logging.debug("Tech News Bulletin completed!")


if __name__ == '__main__':
    main()
