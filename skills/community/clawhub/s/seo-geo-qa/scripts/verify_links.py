#!/usr/bin/env python3
import argparse
import json
import re
import subprocess
import sys
import time
from collections import Counter
from dataclasses import dataclass, asdict
from html.parser import HTMLParser
from pathlib import Path
from typing import List, Optional
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qsl, quote, urlencode, urlparse, urlunparse
from urllib.request import Request, urlopen

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0 Safari/537.36"
TIMEOUT = 12
TIER_A_DOMAINS = {
    "apple.com", "google.com", "microsoft.com", "openai.com", "anthropic.com",
    "gmail.com", "outlook.com", "notion.so", "notion.com",
    "slack.com", "mail.google.com",
    "developers.google.com", "support.apple.com", "support.microsoft.com",
    "keep.google.com", "icloud.com", "onenote.com", "onedrive.live.com",
}
TIER_B_DOMAINS = {
    "nytimes.com", "wsj.com", "theverge.com", "techcrunch.com", "wired.com", "forbes.com",
    "pcmag.com", "cnet.com", "zdnet.com", "mckinsey.com", "gartner.com", "hubspot.com",
    "zapier.com", "macworld.com", "wikipedia.org", "9to5mac.com", "reuters.com", "cnbc.com",
    "youtube.com", "semrush.com", "searchengineland.com", "moz.com", "ahrefs.com",
    "searchenginejournal.com", "nerdwallet.com", "bbc.com", "bbc.co.uk",
}

URL_RE = re.compile(r"https?://[^\s)\]>\"']+")
_EXTRA_BRAND_ROOTS: list[str] = []

class TitleParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_title = False
        self.title = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "title":
            self.in_title = True

    def handle_endtag(self, tag):
        if tag.lower() == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title.append(data)

class SearchResultParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self._current_href = None

    def handle_starttag(self, tag, attrs):
        if tag.lower() != "a":
            return
        attrs = dict(attrs)
        href = attrs.get("href")
        if href and href.startswith("http"):
            self.links.append(href)

@dataclass
class LinkResult:
    url: str
    domain: str
    http_status: str
    final_url: str = ""
    title: str = ""
    verdict: str = "valid"
    evidence: str = ""
    source_quality: str = "skip"
    source_tier: str = "TIER-C"
    source_notes: List[str] = None

    def __post_init__(self):
        if self.source_notes is None:
            self.source_notes = []


def normalize_domain(url: str) -> str:
    host = urlparse(url).netloc.lower()
    return host[4:] if host.startswith("www.") else host


def canonicalize_url(url: str) -> str:
    parsed = urlparse(url)
    keep_params = []
    for k, v in parse_qsl(parsed.query, keep_blank_values=True):
        lk = k.lower()
        if lk.startswith("utm_") or lk in {"fbclid", "gclid", "mc_cid", "mc_eid", "ref", "ref_src", "source"}:
            continue
        keep_params.append((k, v))
    cleaned = parsed._replace(query=urlencode(keep_params), fragment="")
    return urlunparse(cleaned).rstrip("?")


def extract_urls(text: str) -> List[str]:
    urls = []
    for url in sorted(set(URL_RE.findall(text))):
        if "<" in url or ">" in url:
            continue
        urls.append(canonicalize_url(url.rstrip('.,;')))
    return sorted(set(urls))


def curl_head(url: str) -> str:
    cmd = [
        "curl", "-sI", "-o", "/dev/null", "-w", "%{http_code}",
        "--max-time", "10", "-L", "-A", USER_AGENT, url,
    ]
    try:
        out = subprocess.check_output(cmd, text=True).strip()
        return out or "000"
    except Exception:
        return "000"


def fetch(url: str) -> tuple[str, str, str]:
    req = Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urlopen(req, timeout=TIMEOUT) as resp:
            body = resp.read(120000).decode("utf-8", errors="ignore")
            return str(resp.status), resp.geturl(), body
    except HTTPError as e:
        body = e.read(120000).decode("utf-8", errors="ignore") if hasattr(e, "read") else ""
        return str(e.code), url, body
    except URLError:
        return "000", url, ""
    except Exception:
        return "000", url, ""


def parse_title(html: str) -> str:
    parser = TitleParser()
    parser.feed(html)
    return " ".join("".join(parser.title).split())[:160]


def body_looks_404(body: str) -> bool:
    text = body.lower()
    strong = [
        "404 not found", "page not found", "this page doesn\'t exist",
        "the page you are looking for cannot be found", "error 404"
    ]
    return any(x in text for x in strong)


def search_index(domain: str, url: str) -> tuple[bool, str]:
    url = canonicalize_url(url)
    query = quote(f'site:{domain} "{url}"')
    search_url = f"https://html.duckduckgo.com/html/?q={query}"
    status, final_url, body = fetch(search_url)
    if status.startswith("2") and body:
        parser = SearchResultParser()
        parser.feed(body)
        for link in parser.links:
            if domain in normalize_domain(link) or url.rstrip("/") in link:
                return True, f"search hit: {link}"
    return False, "no indexed result found"


def same_brand_domain(a: str, b: str) -> bool:
    if a == b:
        return True
    major_roots = [
        "apple.com", "google.com", "microsoft.com", "notion.com", "notion.so",
        "zapier.com", "openai.com", "anthropic.com", "evernote.com",
    ] + _EXTRA_BRAND_ROOTS
    for root in major_roots:
        if (a == root or a.endswith('.' + root)) and (b == root or b.endswith('.' + root)):
            return True
    return False


def classify_source_quality(domain: str, body: str, url: str) -> tuple[str, str, List[str]]:
    notes = []
    path = urlparse(url).path.lower()
    if domain in TIER_A_DOMAINS or any(domain.endswith(d) for d in TIER_A_DOMAINS):
        return "skip", "TIER-A", ["official / first-party / primary source"]
    if domain in TIER_B_DOMAINS or any(domain.endswith(d) for d in TIER_B_DOMAINS):
        if len(body) > 500:
            return "strong", "TIER-B", ["reputable editorial / research / established secondary source"]
        return "usable", "TIER-B", ["trusted editorial domain; weak extraction but domain reputation override applied"]
    if path in {"", "/"} or any(seg in path for seg in ["/pricing", "/product", "/features", "/blog/"]):
        notes.append("looks like a first-party product/content page")

    indexed, evidence = search_index(domain, url)
    if indexed:
        notes.append(evidence)
    else:
        notes.append("no clear search index evidence")

    text = body.lower()
    spam_hits = sum(1 for token in ["casino", "betting", "viagra", "loan", "replica", "guest post"] if token in text)
    if spam_hits >= 2:
        notes.append("spam-like tokens found")
        return "reject", "TIER-D", notes

    if indexed and len(body) > 1500:
        notes.append("page has enough content to inspect")
        return "usable", "TIER-C", notes
    if indexed:
        notes.append("indexed but thin page")
        return "weak", "TIER-D", notes
    if notes and notes[0] == "looks like a first-party product/content page" and len(body) > 1200:
        notes.append("live page with enough on-page content")
        return "usable", "TIER-C", notes
    return "weak", "TIER-D", notes


_SITE_DOMAIN: str = ""


def verify_url(url: str) -> LinkResult:
    domain = normalize_domain(url)
    http_status = curl_head(url)
    result = LinkResult(url=url, domain=domain, http_status=http_status)

    if http_status in {"404", "410"}:
        result.verdict = "dead"
        result.evidence = f"HTTP {http_status}"
        return result

    status2, final_url, body = fetch(url)
    result.final_url = final_url
    result.title = parse_title(body)

    if status2.startswith("2"):
        if body_looks_404(body):
            result.verdict = "dead"
            result.evidence = "body looks like 404"
        else:
            result.verdict = "valid"
            result.evidence = f"HTTP {status2}"
    elif status2 in {"403", "401", "000", "429", "500", "502", "503"}:
        indexed, evidence = search_index(domain, url)
        if indexed:
            result.verdict = "bot-protected"
            result.evidence = evidence
        else:
            result.verdict = "weak"
            result.evidence = f"fetch blocked ({status2}); {evidence}"
    elif status2 in {"404", "410"}:
        result.verdict = "dead"
        result.evidence = f"fetch HTTP {status2}"
    else:
        result.verdict = "weak"
        result.evidence = f"unexpected status {status2}"

    # Internal links: only check liveness, skip source quality classification
    if _SITE_DOMAIN and (_SITE_DOMAIN == domain or domain.endswith('.' + _SITE_DOMAIN)):
        result.source_quality = "skip"
        result.source_tier = "skip"
        result.source_notes = ["internal link — skipped source classification"]
    else:
        quality, tier, notes = classify_source_quality(domain, body, url)
        result.source_quality = quality
        result.source_tier = tier
        result.source_notes = notes

    parsed_final = normalize_domain(final_url) if final_url else domain
    if final_url and final_url.rstrip("/") != url.rstrip("/") and parsed_final != domain:
        if same_brand_domain(domain, parsed_final):
            result.verdict = "valid"
            result.evidence = f"redirected within same brand: {final_url}"
            if result.source_tier == "TIER-D":
                result.source_tier = "TIER-A"
            if result.source_quality == "weak":
                result.source_quality = "skip"
            result.source_notes.append("same-brand redirect treated as valid")
        else:
            result.verdict = "moved"
            result.evidence = f"redirected to different domain: {final_url}"

    return result


def summarize(results: List[LinkResult]) -> dict:
    verdict_counts = Counter(r.verdict for r in results)
    quality_counts = Counter(r.source_quality for r in results)
    tier_counts = Counter(r.source_tier for r in results)
    return {
        "total": len(results),
        "verdict_counts": dict(verdict_counts),
        "source_quality_counts": dict(quality_counts),
        "source_tier_counts": dict(tier_counts),
        "dead": [asdict(r) for r in results if r.verdict == "dead"],
        "moved": [asdict(r) for r in results if r.verdict == "moved"],
        "bot_protected": [asdict(r) for r in results if r.verdict == "bot-protected"],
        "weak_sources": [asdict(r) for r in results if r.source_quality in {"weak", "reject"}],
        "results": [asdict(r) for r in results],
    }


def print_markdown(report: dict):
    vc = report["verdict_counts"]
    print("## Link Verification Report\n")
    print(f"Total links: {report['total']}")
    print(
        f"✅ Valid: {vc.get('valid',0)} | ✅ Bot-protected: {vc.get('bot-protected',0)} | "
        f"❌ Dead: {vc.get('dead',0)} | ⚠️ Moved: {vc.get('moved',0)} | ⚠️ Weak: {vc.get('weak',0)}\n"
    )
    if report["dead"]:
        print("### Dead Links (MUST REPLACE)")
        for i, item in enumerate(report["dead"], 1):
            print(f"{i}. {item['url']} — {item['evidence']}")
        print()
    if report["moved"]:
        print("### Moved Links")
        for i, item in enumerate(report["moved"], 1):
            print(f"{i}. {item['url']} — {item['evidence']}")
        print()
    if report["bot_protected"]:
        print("### Bot-Protected (verified live)")
        for i, item in enumerate(report["bot_protected"], 1):
            print(f"{i}. {item['url']} — {item['evidence']}")
        print()
    tc = report.get("source_tier_counts", {})
    print(f"Source tiers: TIER-A {tc.get('TIER-A',0)} | TIER-B {tc.get('TIER-B',0)} | TIER-C {tc.get('TIER-C',0)} | TIER-D {tc.get('TIER-D',0)} | skip {tc.get('skip',0)}\n")
    if report["weak_sources"]:
        print("### Weak Sources (SHOULD REPLACE)")
        for i, item in enumerate(report["weak_sources"], 1):
            notes = "; ".join(item.get("source_notes") or [])
            print(f"{i}. {item['url']} — {item['source_tier']} / {item['source_quality']} — {notes}")
        print()


def load_config_overrides(config_path: str | None):
    """Merge user config into module-level domain sets."""
    if not config_path:
        return
    try:
        cfg = json.loads(Path(config_path).read_text(encoding="utf-8"))
    except Exception:
        return
    for d in cfg.get("tierADomains", []):
        TIER_A_DOMAINS.add(d.lower())
    for d in cfg.get("tierBDomains", []):
        TIER_B_DOMAINS.add(d.lower())
    for root in cfg.get("brandDomains", []):
        root = root.lower()
        # Inject into same_brand_domain's major_roots at runtime
        _EXTRA_BRAND_ROOTS.append(root)


def main():
    parser = argparse.ArgumentParser(description="Verify article links and spot weak sources.")
    parser.add_argument("input", help="Markdown/text file to scan")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of markdown")
    parser.add_argument("--config", help="Optional JSON config for domain overrides")
    parser.add_argument("--site-domain", help="Site domain — internal links skip source classification")
    args = parser.parse_args()

    load_config_overrides(args.config)

    global _SITE_DOMAIN
    if args.site_domain:
        _SITE_DOMAIN = args.site_domain.lower()
    elif args.config:
        try:
            cfg = json.loads(Path(args.config).read_text(encoding="utf-8"))
            _SITE_DOMAIN = cfg.get("siteDomain", "").lower()
        except Exception:
            pass

    text = Path(args.input).read_text(encoding="utf-8")
    urls = extract_urls(text)
    if not urls:
        print("No URLs found.")
        return 0

    results = []
    for idx, url in enumerate(urls, 1):
        print(f"[{idx}/{len(urls)}] checking {url}", file=sys.stderr)
        results.append(verify_url(url))
        time.sleep(0.2)

    report = summarize(results)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print_markdown(report)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
