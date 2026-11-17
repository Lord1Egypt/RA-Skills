"""Extract bibliographic metadata from a web page.

Priority order: citation_* meta tags -> JSON-LD (schema.org ScholarlyArticle)
-> og:* / dc.* -> <title> fallback.
"""
import json
import re
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from common import clean_text, find_doi, parse_author, UA


def _meta(soup, names):
    for n in names:
        tag = soup.find("meta", attrs={"name": n}) or soup.find("meta", attrs={"property": n})
        if tag and tag.get("content"):
            return clean_text(tag["content"])
    return ""


def _extract_jsonld(soup):
    for node in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(node.string or "")
        except (ValueError, TypeError):
            continue
        items = data if isinstance(data, list) else [data]
        for it in items:
            if not isinstance(it, dict):
                continue
            if it.get("@type") in ("ScholarlyArticle", "Article", "WebPage", "Book", "Report"):
                return it
    return None


def extract_web_metadata(url):
    rec = {
        "source_type": "web",
        "original_url": url,
        "original_filename": None,
        "original_apa": None,
        "title": "", "authors": [], "year": "", "month": "", "day": "",
        "journal": "", "publisher": "", "volume": "", "issue": "", "pages": "",
        "doi": None, "url": url,
    }
    resp = requests.get(url, headers=UA, timeout=20)
    resp.raise_for_status()
    html = resp.text
    soup = BeautifulSoup(html, "html.parser")

    title = _meta(soup, ["citation_title", "og:title", "dc.title", "twitter:title"])
    if not title:
        t = soup.find("title")
        title = clean_text(t.get_text()) if t else ""

    authors = []
    for tag in soup.find_all("meta", attrs={"name": "citation_author"}):
        a = parse_author(tag.get("content", ""))
        if a:
            authors.append(a)
    if not authors:
        for tag in soup.find_all("meta", attrs={"name": re.compile(r"^dc\.creator$", re.I)}):
            a = parse_author(tag.get("content", ""))
            if a:
                authors.append(a)

    date_raw = _meta(soup, ["citation_publication_date", "citation_date",
                            "dc.date", "article:published_time", "pubdate"])
    year = month = day = ""
    m = re.search(r'(\d{4})', date_raw or "")
    if m:
        year = m.group(1)
    m2 = re.search(r'(\d{4})[-/](\d{1,2})[-/](\d{1,2})', date_raw or "")
    if m2:
        year, month, day = m2.group(1), m2.group(2), m2.group(3)

    journal = _meta(soup, ["citation_journal_title", "citation_conference_title", "og:site_name"])
    publisher = _meta(soup, ["citation_publisher", "dc.publisher"])
    volume = _meta(soup, ["citation_volume"])
    issue = _meta(soup, ["citation_issue"])
    pages = _meta(soup, ["citation_firstpage"])
    last = _meta(soup, ["citation_lastpage"])
    if pages and last:
        pages = f"{pages}-{last}"

    doi = _meta(soup, ["citation_doi"])
    if not doi:
        doi = find_doi(html)

    jl = _extract_jsonld(soup)
    if jl:
        if not title and isinstance(jl.get("headline"), str):
            title = clean_text(jl["headline"])
        if not authors:
            for a in jl.get("author", []):
                if isinstance(a, dict) and a.get("name"):
                    pa = parse_author(a["name"])
                    if pa:
                        authors.append(pa)
                elif isinstance(a, str):
                    pa = parse_author(a)
                    if pa:
                        authors.append(pa)
        if not journal and isinstance(jl.get("isPartOf"), dict):
            journal = clean_text(jl["isPartOf"].get("name", ""))
        if not year and isinstance(jl.get("datePublished"), str):
            m = re.search(r'(\d{4})', jl["datePublished"])
            if m:
                year = m.group(1)
        if not doi and isinstance(jl.get("sameAs"), str):
            doi = find_doi(jl["sameAs"])

    rec.update(title=clean_text(title), authors=authors, year=year, month=month,
               day=day, journal=clean_text(journal), publisher=clean_text(publisher),
               volume=volume, issue=issue, pages=pages, doi=doi)
    return rec
