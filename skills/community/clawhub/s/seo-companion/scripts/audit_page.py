#!/usr/bin/env python3
import ipaddress
import json
import re
import socket
import sys
from collections import Counter
from urllib.parse import urljoin, urlparse

try:
    import requests
except ImportError:
    print(
        "Missing dependency: requests. Install it or fall back to web_fetch/browser for manual auditing.",
        file=sys.stderr,
    )
    sys.exit(2)

try:
    from bs4 import BeautifulSoup
except ImportError:
    print(
        "Missing dependency: beautifulsoup4 (bs4). Install it or fall back to web_fetch/browser for manual auditing.",
        file=sys.stderr,
    )
    sys.exit(2)

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
TIMEOUT = 20
BLOCKED_HOSTS = {
    "localhost",
    "metadata.google.internal",
}
BLOCKED_IPS = {
    "127.0.0.1",
    "0.0.0.0",
    "::1",
    "169.254.169.254",
}


def clean_text(value):
    if value is None:
        return None
    return re.sub(r"\s+", " ", value).strip() or None


def get_attr(tag, *names):
    for name in names:
        value = tag.get(name)
        if value:
            return value
    return None


def classify_title(n):
    if n is None:
        return "missing"
    if 50 <= n <= 60:
        return "good"
    if 40 <= n <= 49 or 61 <= n <= 70:
        return "warning"
    return "bad"


def classify_description(n):
    if n is None:
        return "missing"
    if 120 <= n <= 156:
        return "good"
    if 100 <= n <= 119 or 157 <= n <= 165:
        return "warning"
    return "bad"


def classify_word_count(n):
    if n > 1500:
        return "good"
    if 800 <= n <= 1500:
        return "warning"
    return "bad"


def same_host(a, b):
    try:
        return urlparse(a).netloc == urlparse(b).netloc
    except Exception:
        return False


def is_blocked_target(url):
    parsed = urlparse(url)
    host = parsed.hostname
    if not host:
        return True, "URL is missing a valid hostname"

    host_l = host.lower()
    if host_l in BLOCKED_HOSTS:
        return True, f"Blocked host: {host}"

    try:
        ip = ipaddress.ip_address(host_l)
        if (
            ip.is_private
            or ip.is_loopback
            or ip.is_link_local
            or ip.is_reserved
            or ip.is_multicast
            or str(ip) in BLOCKED_IPS
        ):
            return True, f"Blocked IP target: {ip}"
    except ValueError:
        pass

    try:
        infos = socket.getaddrinfo(host, None)
        for info in infos:
            resolved_ip = info[4][0]
            ip = ipaddress.ip_address(resolved_ip)
            if (
                ip.is_private
                or ip.is_loopback
                or ip.is_link_local
                or ip.is_reserved
                or ip.is_multicast
                or str(ip) in BLOCKED_IPS
            ):
                return True, f"Blocked resolved IP target: {resolved_ip}"
    except socket.gaierror:
        return True, f"Host did not resolve: {host}"
    except Exception:
        pass

    return False, None


def fetch(url):
    session = requests.Session()
    session.headers.update({"User-Agent": UA})
    response = session.get(url, timeout=TIMEOUT, allow_redirects=True)
    response.raise_for_status()
    return response, session


def fetch_optional(session, url):
    try:
        r = session.get(url, timeout=TIMEOUT, allow_redirects=True)
        return {
            "url": r.url,
            "status": r.status_code,
            "ok": 200 <= r.status_code < 300,
            "text": r.text[:4000],
        }
    except Exception as e:
        return {"url": url, "ok": False, "error": str(e)}


def extract_meta(soup):
    meta = {}
    for tag in soup.find_all("meta"):
        key = get_attr(tag, "name", "property", "http-equiv")
        if not key:
            continue
        content = clean_text(tag.get("content"))
        if content is not None and key not in meta:
            meta[key.lower()] = content
    return meta


def extract_headings(soup):
    headings = []
    counts = Counter()
    for level in ["h1", "h2", "h3", "h4", "h5", "h6"]:
        for tag in soup.find_all(level):
            text = clean_text(tag.get_text(" ", strip=True))
            headings.append({"tag": level, "text": text})
            counts[level] += 1
    return headings, counts


def extract_links(soup, final_url):
    parsed = []
    for a in soup.find_all("a"):
        href = clean_text(a.get("href"))
        if not href:
            continue
        absolute = urljoin(final_url, href)
        text = clean_text(a.get_text(" ", strip=True))
        rel = " ".join(a.get("rel", [])) if a.get("rel") else ""
        parsed.append({
            "href": absolute,
            "text": text,
            "rel": rel,
            "internal": same_host(absolute, final_url),
        })
    total = len(parsed)
    internal = sum(1 for x in parsed if x["internal"])
    external = total - internal
    nofollow = sum(1 for x in parsed if "nofollow" in (x["rel"] or "").lower())
    empty_anchor = [x for x in parsed if not x["text"]]
    return {
        "total": total,
        "internal": internal,
        "external": external,
        "nofollow": nofollow,
        "empty_anchor_count": len(empty_anchor),
        "sample_empty_anchor_links": empty_anchor[:10],
    }


def extract_images(soup, final_url):
    images = []
    missing_alt = []
    for img in soup.find_all("img"):
        src = clean_text(img.get("src"))
        abs_src = urljoin(final_url, src) if src else None
        alt = clean_text(img.get("alt"))
        item = {"src": abs_src, "alt": alt}
        images.append(item)
        if alt is None:
            missing_alt.append(item)
    return {
        "total": len(images),
        "missing_alt_count": len(missing_alt),
        "missing_alt": missing_alt[:30],
    }


def extract_jsonld(soup):
    types = []
    for script in soup.find_all("script", attrs={"type": "application/ld+json"}):
        raw = script.string or script.get_text()
        if not raw:
            continue
        try:
            data = json.loads(raw)
        except Exception:
            continue
        queue = [data]
        while queue:
            cur = queue.pop(0)
            if isinstance(cur, list):
                queue.extend(cur)
            elif isinstance(cur, dict):
                atype = cur.get("@type")
                if isinstance(atype, list):
                    types.extend([str(x) for x in atype])
                elif atype:
                    types.append(str(atype))
                queue.extend(cur.values())
    deduped = []
    seen = set()
    for t in types:
        if t not in seen:
            seen.add(t)
            deduped.append(t)
    return deduped


def get_body_word_count(soup):
    body = soup.body or soup
    for tag in body(["script", "style", "noscript", "svg"]):
        tag.extract()
    text = clean_text(body.get_text(" ", strip=True)) or ""
    words = [w for w in text.split(" ") if w]
    return len(words)


def build_priority_issues(result):
    issues = []
    if result["status"] >= 400:
        issues.append({"severity": "critical", "issue": f"Page returned HTTP {result['status']}"})
    if result["meta_robots"] and "noindex" in result["meta_robots"].lower():
        issues.append({"severity": "critical", "issue": "Meta robots contains noindex"})
    if result["x_robots"] and any("noindex" in x.lower() for x in result["x_robots"]):
        issues.append({"severity": "critical", "issue": "X-Robots-Tag contains noindex"})
    if not result["canonical"]:
        issues.append({"severity": "high", "issue": "Canonical tag missing"})
    if result["title"]["status"] in {"bad", "missing"}:
        issues.append({"severity": "high", "issue": "Title tag missing or poorly sized"})
    if result["description"]["status"] in {"bad", "missing"}:
        issues.append({"severity": "high", "issue": "Meta description missing or poorly sized"})
    if result["headings"]["counts"].get("h1", 0) != 1:
        issues.append({"severity": "high", "issue": f"H1 count is {result['headings']['counts'].get('h1', 0)} (expected 1)"})
    if result["word_count"]["status"] == "bad":
        issues.append({"severity": "medium", "issue": "Low body word count for a page intended to rank"})
    if result["images"]["missing_alt_count"] > 0:
        issues.append({"severity": "medium", "issue": f"{result['images']['missing_alt_count']} images missing alt text"})
    if not result["robots_txt"].get("ok"):
        issues.append({"severity": "medium", "issue": "robots.txt missing or inaccessible"})
    if not result["sitemap"].get("ok"):
        issues.append({"severity": "medium", "issue": "sitemap endpoint missing or inaccessible"})
    return issues


def main():
    if len(sys.argv) != 2:
        print("Usage: audit_page.py <URL>", file=sys.stderr)
        sys.exit(1)

    url = sys.argv[1]
    blocked, reason = is_blocked_target(url)
    if blocked:
        print(
            f"Refusing to audit target by default: {reason}. Use only public HTTP/HTTPS URLs for routine SEO audits.",
            file=sys.stderr,
        )
        sys.exit(3)

    response, session = fetch(url)
    final_url = response.url
    soup = BeautifulSoup(response.text, "html.parser")
    meta = extract_meta(soup)
    headings, heading_counts = extract_headings(soup)
    links = extract_links(soup, final_url)
    images = extract_images(soup, final_url)
    jsonld_types = extract_jsonld(soup)
    word_count = get_body_word_count(soup)

    title_text = clean_text(soup.title.get_text(" ", strip=True) if soup.title else None)
    description = meta.get("description")
    canonical_tag = soup.find("link", rel=lambda x: x and "canonical" in str(x).lower())
    canonical = clean_text(canonical_tag.get("href")) if canonical_tag else None
    canonical = urljoin(final_url, canonical) if canonical else None
    html_tag = soup.find("html")
    html_lang = clean_text(html_tag.get("lang")) if html_tag else None
    x_robots = response.headers.get("X-Robots-Tag")

    parsed = urlparse(final_url)
    base = f"{parsed.scheme}://{parsed.netloc}"
    robots_txt = fetch_optional(session, base + "/robots.txt")
    sitemap = fetch_optional(session, base + "/sitemap.xml")
    if not sitemap.get("ok"):
        sitemap = fetch_optional(session, base + "/sitemap_index.xml")

    result = {
        "input_url": url,
        "final_url": final_url,
        "status": response.status_code,
        "title": {
            "text": title_text,
            "length": len(title_text) if title_text else None,
            "status": classify_title(len(title_text)) if title_text else "missing",
        },
        "description": {
            "text": description,
            "length": len(description) if description else None,
            "status": classify_description(len(description)) if description else "missing",
        },
        "canonical": canonical,
        "meta_robots": meta.get("robots"),
        "x_robots": [x_robots] if x_robots else [],
        "html_lang": html_lang,
        "headings": {
            "counts": dict(heading_counts),
            "all": headings,
        },
        "links": links,
        "images": images,
        "structured_data_types": jsonld_types,
        "word_count": {
            "value": word_count,
            "status": classify_word_count(word_count),
        },
        "robots_txt": robots_txt,
        "sitemap": sitemap,
    }

    result["priority_issues"] = build_priority_issues(result)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
