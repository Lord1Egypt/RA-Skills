#!/usr/bin/env python3
import argparse
import json
import re
import sys
import time
from collections import Counter
from dataclasses import dataclass, asdict
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, quote, unquote, urlparse
from urllib.request import Request, urlopen

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0 Safari/537.36"
TIMEOUT = 15
JINA_BASE = "https://r.jina.ai/"
JINA_TIMEOUT = 30
STOPWORDS = {
    # Common English function words
    "the","a","an","and","or","to","for","of","in","on","with","from","by","is","are","be",
    "this","that","these","those","they","them","their","there","which","when","where","while",
    "can","will","may","might","should","would","could","also","just","about","after","before",
    # Common comparison/SEO words (appear on every best-of page)
    "best","top","vs","how","what","your","you",
    # Year tokens
    "2026","2025","2024","2023",
    # Jina Reader metadata headers (injected at top of every Jina-rendered page)
    "title","url","source","markdown","content",
    # Image/media tokens from Markdown alt text and figure captions
    "png","jpg","jpeg","gif","svg","webp","image","img",
    # Common navigation / UI / boilerplate text that appears on most pages
    "click","here","read","more","view","learn","get","try","start","sign",
    "login","signup","subscribe","newsletter","cookie","cookies","privacy","policy",
    "terms","copyright","rights","reserved","menu","home","back","next",
    # Generic action words that don't signal topic
    "new","updated","published","posted","written","using","used",
}

class SERPParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
    def handle_starttag(self, tag, attrs):
        if tag.lower() != "a":
            return
        attrs = dict(attrs)
        href = attrs.get("href")
        if not href:
            return
        if href.startswith("//"):
            href = "https:" + href
        if "duckduckgo.com/l/?" in href:
            qs = parse_qs(urlparse(href).query)
            uddg = qs.get("uddg")
            if uddg:
                href = unquote(uddg[0])
        if href.startswith("http"):
            self.links.append(href)

class ArticleParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_title = False
        self.title = []
        self.headings = []
        self.current_heading = None
        self.text = []
        self.skip_stack = []
    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        if tag in {"script", "style", "noscript", "svg"}:
            self.skip_stack.append(tag)
            return
        if tag == "title":
            self.in_title = True
        if tag in {"h1","h2","h3"}:
            self.current_heading = [tag, []]
    def handle_endtag(self, tag):
        tag = tag.lower()
        if self.skip_stack and tag == self.skip_stack[-1]:
            self.skip_stack.pop()
            return
        if tag == "title":
            self.in_title = False
        if self.current_heading and tag == self.current_heading[0]:
            self.headings.append((self.current_heading[0], " ".join("".join(self.current_heading[1]).split())))
            self.current_heading = None
    def handle_data(self, data):
        if self.skip_stack:
            return
        data = data.strip()
        if not data:
            return
        self.text.append(data)
        if self.in_title:
            self.title.append(data)
        if self.current_heading:
            self.current_heading[1].append(data)

@dataclass
class CompetitorDoc:
    url: str
    domain: str
    title: str
    h2s: list
    h3s: list
    tokens: list
    word_count: int


def fetch(url: str):
    req = Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urlopen(req, timeout=TIMEOUT) as resp:
            body = resp.read(180000).decode("utf-8", errors="ignore")
            return str(resp.status), resp.geturl(), body
    except HTTPError as e:
        body = e.read(180000).decode("utf-8", errors="ignore") if hasattr(e, "read") else ""
        return str(e.code), url, body
    except URLError:
        return "000", url, ""
    except Exception:
        return "000", url, ""


def jina_fetch(url: str) -> str:
    """Fetch a URL via Jina Reader (r.jina.ai) and return Markdown content.
    Bypasses Cloudflare and other anti-bot measures using a real browser renderer.
    No API key required for basic usage."""
    jina_url = JINA_BASE + url
    req = Request(jina_url, headers={"User-Agent": USER_AGENT, "Accept": "text/markdown"})
    try:
        with urlopen(req, timeout=JINA_TIMEOUT) as resp:
            return resp.read(500000).decode("utf-8", errors="ignore")
    except Exception:
        return ""


def normalize_domain(url: str) -> str:
    host = urlparse(url).netloc.lower()
    return host[4:] if host.startswith("www.") else host


def ddg_search(query: str, limit: int) -> list[str]:
    search_url = f"https://html.duckduckgo.com/html/?q={quote(query)}"
    SKIP_DOMAINS = {"duckduckgo.com", "youtube.com", "facebook.com", "instagram.com", "x.com", "r.jina.ai"}
    urls = []
    seen = set()

    # Primary: direct urllib fetch (fast path, no extra latency)
    status, _, body = fetch(search_url)
    if status.startswith("2") and body:
        parser = SERPParser()
        parser.feed(body)
        for link in parser.links:
            domain = normalize_domain(link)
            if any(x in domain for x in SKIP_DOMAINS):
                continue
            if link not in seen:
                seen.add(link)
                urls.append(link)
            if len(urls) >= limit:
                break

    # Fallback: Jina renders DDG with a real browser, bypassing bot detection.
    # DDG wraps result URLs in redirect links: duckduckgo.com/l/?uddg=<url-encoded-url>
    # so we must extract and decode the uddg param, same logic as SERPParser.
    if not urls:
        md = jina_fetch(search_url)
        for m in re.finditer(r'https?://duckduckgo\.com/l/\?[^\s\)\]\"\'<>]+', md):
            raw = m.group(0).rstrip(".,;)")
            qs = parse_qs(urlparse(raw).query)
            uddg = qs.get("uddg")
            if not uddg:
                continue
            link = unquote(uddg[0])
            domain = normalize_domain(link)
            if any(x in domain for x in SKIP_DOMAINS):
                continue
            if link not in seen:
                seen.add(link)
                urls.append(link)
            if len(urls) >= limit:
                break

    return urls


def tokenize(text: str) -> list[str]:
    return [t for t in re.findall(r"[a-zA-Z][a-zA-Z0-9+-]{2,}", text.lower()) if t not in STOPWORDS]


def parse_doc_from_markdown(url: str, md: str) -> CompetitorDoc | None:
    """Build a CompetitorDoc from Jina-returned Markdown content."""
    if not md or len(md) < 100:
        return None
    lines = md.splitlines()
    title, h2s, h3s, text_parts = "", [], [], []
    for line in lines:
        s = line.strip()
        if not s:
            continue
        if s.startswith("# ") and not title:
            title = s[2:].strip()
        elif s.startswith("## "):
            h2s.append(s[3:].strip())
        elif s.startswith("### "):
            h3s.append(s[4:].strip())
        elif not s.startswith("#"):
            text_parts.append(s)
    full_text = " ".join(text_parts)
    tokens = tokenize(" ".join([title] + h2s + h3s + [full_text[:6000]]))
    return CompetitorDoc(
        url=url,
        domain=normalize_domain(url),
        title=title[:200],
        h2s=h2s,
        h3s=h3s,
        tokens=tokens,
        word_count=len(full_text.split()),
    )


def parse_doc(url: str) -> CompetitorDoc | None:
    # Primary: Jina Reader — renders with a real browser, bypasses Cloudflare/anti-bot
    md = jina_fetch(url)
    doc = parse_doc_from_markdown(url, md)
    if doc:
        return doc

    # Fallback: direct HTML fetch (works for pages without bot protection)
    status, final_url, body = fetch(url)
    if not status.startswith("2") or not body:
        return None
    parser = ArticleParser()
    parser.feed(body)
    headings = [(lvl, txt) for lvl, txt in parser.headings if txt]
    title = " ".join(" ".join(parser.title).split())[:200]
    text = " ".join(parser.text)
    tokens = tokenize(" ".join([title] + [h for _, h in headings] + [text[:6000]]))
    return CompetitorDoc(
        url=final_url,
        domain=normalize_domain(final_url),
        title=title,
        h2s=[txt for lvl, txt in headings if lvl == "h2"],
        h3s=[txt for lvl, txt in headings if lvl == "h3"],
        tokens=tokens,
        word_count=len(text.split()),
    )


def parse_markdown_article(path: str):
    text = Path(path).read_text(encoding="utf-8")
    lines = text.splitlines()
    h1 = ""
    h2s, h3s, faqs = [], [], []
    for line in lines:
        s = line.strip()
        if s.startswith("# ") and not h1:
            h1 = s[2:].strip()
        elif s.startswith("## "):
            h2s.append(s[3:].strip())
        elif s.startswith("### "):
            h3s.append(s[4:].strip())
        if s.endswith("?"):
            faqs.append(s.lstrip("#-0123456789. ").strip())
    tokens = tokenize(text)
    return {
        "h1": h1,
        "h2s": h2s,
        "h3s": h3s,
        "faqs": faqs,
        "tokens": tokens,
        "word_count": len(text.split()),
    }


def top_terms(docs: list[CompetitorDoc], top_n=25):
    counts = Counter()
    for doc in docs:
        counts.update(set(doc.tokens))
    return counts.most_common(top_n)


def overlap_ratio(terms: set[str], article_tokens: set[str]) -> float:
    if not terms:
        return 0.0
    return len(terms & article_tokens) / len(terms)


def main():
    ap = argparse.ArgumentParser(description="SERP / competitor gap analyzer for SEO article drafts")
    ap.add_argument("keyword", help="Primary keyword")
    ap.add_argument("article", help="Markdown article draft path")
    ap.add_argument("--limit", type=int, default=5, help="Top SERP URLs to inspect")
    ap.add_argument("--urls", nargs="*", default=None, help="Competitor URLs to analyze (skips SERP search)")
    ap.add_argument("--no-jina", action="store_true", help="Disable Jina Reader fallback (use only direct HTTP fetch)")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if args.no_jina:
        # Monkey-patch to disable Jina globally for this run
        global jina_fetch
        jina_fetch = lambda url: ""  # noqa: E731

    article = parse_markdown_article(args.article)
    article_tokens = set(article["tokens"])

    urls = args.urls or ddg_search(args.keyword, args.limit)
    docs = []
    for idx, url in enumerate(urls, 1):
        print(f"[{idx}/{len(urls)}] analyzing {url}", file=sys.stderr)
        doc = parse_doc(url)
        if doc:
            docs.append(doc)
        time.sleep(0.3)

    if not docs:
        raise SystemExit("No competitor pages could be fetched.")

    h2_counter = Counter()
    faq_counter = Counter()
    for doc in docs:
        h2_counter.update(set(doc.h2s))
        faq_counter.update([h for h in doc.h2s + doc.h3s if h.endswith("?")])

    common_h2s = [h for h, c in h2_counter.most_common(20) if c >= 2]
    missing_h2s = [h for h in common_h2s if h not in article["h2s"]]

    common_terms = top_terms(docs, 30)
    must_have_terms = [t for t, c in common_terms if c >= 2]
    missing_terms = [t for t in must_have_terms if t not in article_tokens][:15]

    competitor_word_counts = [d.word_count for d in docs]
    avg_word_count = round(sum(competitor_word_counts) / len(competitor_word_counts))
    article_term_overlap = round(overlap_ratio(set(must_have_terms), article_tokens) * 100, 1)

    patterns = {
        "has_comparison_table_signal": any("|" in line for line in Path(args.article).read_text(encoding="utf-8").splitlines()),
        "has_faq_signal": len(article["faqs"]) >= 4,
        "competitor_faq_count": len(faq_counter),
    }

    report = {
        "keyword": args.keyword,
        "article": {
            "path": args.article,
            "h1": article["h1"],
            "word_count": article["word_count"],
            "h2_count": len(article["h2s"]),
            "faq_count": len(article["faqs"]),
        },
        "competitors": [asdict(d) for d in docs],
        "summary": {
            "avg_competitor_word_count": avg_word_count,
            "article_vs_avg_word_count_delta": article["word_count"] - avg_word_count,
            "article_term_overlap_percent": article_term_overlap,
            "missing_common_h2s": missing_h2s[:10],
            "missing_common_terms": missing_terms,
            "common_serp_h2s": common_h2s[:15],
            "top_serp_terms": common_terms[:20],
            "patterns": patterns,
        },
        "recommendations": [],
    }

    recs = report["recommendations"]
    if article["word_count"] < avg_word_count * 0.75:
        recs.append(f"Article is materially thinner than the SERP average ({article['word_count']} vs {avg_word_count} words). Add depth.")
    if missing_h2s:
        recs.append("Missing common SERP sections: " + ", ".join(missing_h2s[:6]))
    if missing_terms:
        recs.append("Missing recurring SERP concepts/entities: " + ", ".join(missing_terms[:10]))
    if not patterns["has_comparison_table_signal"] and any(k in args.keyword.lower() for k in ["best", "vs", "alternative"]):
        recs.append("SERP intent looks comparison-heavy. Add a comparison table near the top.")
    if not patterns["has_faq_signal"] and faq_counter:
        recs.append("SERP pages include question-led subsections. Add 4+ FAQ questions.")
    if article_term_overlap < 45:
        recs.append(f"Entity/topic overlap with SERP is low ({article_term_overlap}%). You likely missed important subtopics.")

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"## SERP Gap Report — {args.keyword}\n")
        print(f"Article: {args.article}")
        print(f"Word count: {article['word_count']} | Avg top pages: {avg_word_count} | Topic overlap: {article_term_overlap}%\n")
        print("### Common SERP Sections")
        for item in report["summary"]["common_serp_h2s"]:
            print(f"- {item}")
        print("\n### Missing Sections")
        if missing_h2s:
            for item in missing_h2s[:10]:
                print(f"- {item}")
        else:
            print("- None")
        print("\n### Missing Recurring Concepts")
        if missing_terms:
            for item in missing_terms:
                print(f"- {item}")
        else:
            print("- None")
        print("\n### Recommendations")
        if recs:
            for item in recs:
                print(f"- {item}")
        else:
            print("- No major content gaps detected.")
        print("\n### Competitors Reviewed")
        for doc in docs:
            print(f"- {doc.title or doc.url} — {doc.url}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
