#!/usr/bin/env python3
"""
SEO & GEO audit script (no external dependencies required).
Checks meta tags, headings, robots.txt, sitemap, llms.txt, AI crawler access,
schema markup, Open Graph tags, content metrics, and more.

Usage:
    python3 scripts/seo_audit.py "https://example.com"
    python3 scripts/seo_audit.py "https://example.com" --full
    python3 scripts/seo_audit.py "https://example.com" --ua "Custom/Agent 1.0"
"""
import argparse
import json
import re
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
]

_custom_ua = None


def _get_ua(attempt: int) -> str:
    if _custom_ua:
        return _custom_ua
    return USER_AGENTS[attempt % len(USER_AGENTS)]


def _classify_error(status_code, exception=None) -> str:
    """Return a human-readable diagnostic for the fetch failure."""
    if status_code == 403:
        return "403 Forbidden -- likely WAF or bot detection (Cloudflare, etc.)"
    if status_code == 404:
        return "404 Not Found -- URL may be wrong or CDN is blocking"
    if status_code == 429:
        return "429 Too Many Requests -- rate limited"
    if status_code and 500 <= status_code < 600:
        return f"{status_code} Server Error -- server issue or aggressive bot blocking"
    if exception:
        ename = type(exception).__name__
        if "timeout" in ename.lower() or "Timeout" in str(exception):
            return f"Connection timeout -- firewall may be blocking outbound requests ({ename})"
        if "ssl" in ename.lower() or "SSL" in str(exception):
            return f"SSL/TLS error -- certificate issue or MITM proxy ({ename}: {exception})"
        if "ConnectionRefused" in ename or "refused" in str(exception).lower():
            return f"Connection refused -- host unreachable ({ename})"
        return f"{ename}: {exception}"
    if status_code:
        return f"HTTP {status_code}"
    return "Unknown error -- no response received"


def fetch_url(url: str, timeout: int = 30, max_retries: int = 2) -> tuple:
    """Fetch URL with retries and UA rotation.

    Returns (content, headers, load_time, status_code, error_msg).
    On success error_msg is None. On failure content/headers/load_time are None
    and error_msg contains a diagnostic string.
    """
    last_status = None
    last_error_msg = None

    for attempt in range(max_retries + 1):
        if attempt > 0:
            time.sleep(min(2 ** attempt, 8))

        try:
            start = time.time()
            req = urllib.request.Request(url, headers={
                "User-Agent": _get_ua(attempt),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
            })
            ctx = ssl.create_default_context()
            with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
                content = resp.read().decode("utf-8", errors="ignore")
                headers = dict(resp.headers)
                load_time = time.time() - start
                if not content or not content.strip():
                    last_status = resp.status
                    last_error_msg = "Empty response body -- possible bot trap"
                    continue
                return content, headers, load_time, resp.status, None
        except urllib.error.HTTPError as e:
            last_status = e.code
            last_error_msg = _classify_error(e.code)
            if 500 <= e.code < 600 or e.code == 429:
                continue
            return None, None, None, e.code, last_error_msg
        except Exception as e:
            last_status = None
            last_error_msg = _classify_error(None, e)
            continue

    return None, None, None, last_status, last_error_msg


def extract_meta(html: str) -> dict:
    """Extract meta tags, headings, OG tags, and schema from HTML."""
    result = {}

    title_match = re.search(r"<title[^>]*>([^<]+)</title>", html, re.I)
    result["title"] = title_match.group(1).strip() if title_match else None

    desc_match = re.search(
        r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']+)["\']',
        html, re.I
    )
    if not desc_match:
        desc_match = re.search(
            r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+name=["\']description["\']',
            html, re.I
        )
    result["description"] = desc_match.group(1).strip() if desc_match else None

    og_tags = {}
    for og in ["og:title", "og:description", "og:image", "og:url", "og:type"]:
        pattern = rf'<meta[^>]+property=["\']{ re.escape(og) }["\'][^>]+content=["\']([^"\']*)["\']'
        m = re.search(pattern, html, re.I)
        if not m:
            pattern = rf'<meta[^>]+content=["\']([^"\']*)["\'][^>]+property=["\']{ re.escape(og) }["\']'
            m = re.search(pattern, html, re.I)
        og_tags[og] = m.group(1).strip() if m else None
    result["og_tags"] = og_tags

    tc_match = re.search(
        r'<meta[^>]+name=["\']twitter:card["\'][^>]+content=["\']([^"\']+)["\']',
        html, re.I
    )
    result["twitter_card"] = tc_match.group(1).strip() if tc_match else None

    h1_matches = re.findall(r"<h1[^>]*>(.*?)</h1>", html, re.I | re.DOTALL)
    h1_texts = []
    for h in h1_matches:
        clean = re.sub(r"<[^>]+>", " ", h)
        clean = re.sub(r"\s+", " ", clean).strip()
        if clean:
            h1_texts.append(clean[:120])
    result["h1_tags"] = h1_texts

    h2_count = len(re.findall(r"<h2[^>]*>", html, re.I))
    h3_count = len(re.findall(r"<h3[^>]*>", html, re.I))
    result["h2_count"] = h2_count
    result["h3_count"] = h3_count

    heading_levels = []
    for m in re.finditer(r"<(h[1-6])[^>]*>", html, re.I):
        heading_levels.append(int(m.group(1)[1]))
    result["heading_hierarchy"] = heading_levels

    jsonld_blocks = re.findall(
        r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        html, re.I | re.DOTALL
    )
    result["jsonld_count"] = len(jsonld_blocks)
    schema_types = []
    for block in jsonld_blocks:
        try:
            data = json.loads(block)
            if isinstance(data, dict):
                if "@graph" in data:
                    for item in data["@graph"]:
                        if "@type" in item:
                            schema_types.append(item["@type"])
                elif "@type" in data:
                    schema_types.append(data["@type"])
        except (json.JSONDecodeError, KeyError):
            pass
    result["schema_types"] = schema_types

    has_date = bool(re.search(
        r'<meta[^>]+(datePublished|dateModified|article:published_time|article:modified_time)',
        html, re.I
    ))
    if not has_date:
        for block in jsonld_blocks:
            if "datePublished" in block or "dateModified" in block:
                has_date = True
                break
    result["has_date_meta"] = has_date

    canonical_match = re.search(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)["\']', html, re.I)
    result["canonical"] = canonical_match.group(1).strip() if canonical_match else None

    text_only = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.I | re.DOTALL)
    text_only = re.sub(r"<style[^>]*>.*?</style>", "", text_only, flags=re.I | re.DOTALL)
    text_only = re.sub(r"<[^>]+>", " ", text_only)
    text_only = re.sub(r"\s+", " ", text_only).strip()
    result["word_count"] = len(text_only.split())

    img_tags = re.findall(r"<img[^>]*>", html, re.I)
    imgs_without_alt = 0
    for img in img_tags:
        if not re.search(r'alt=["\']', img, re.I):
            imgs_without_alt += 1
    result["total_images"] = len(img_tags)
    result["images_without_alt"] = imgs_without_alt

    internal_links = len(re.findall(r'<a[^>]+href=["\']/', html, re.I))
    external_links = len(re.findall(r'<a[^>]+href=["\']https?://', html, re.I))
    result["internal_links"] = internal_links
    result["external_links"] = external_links

    return result


def check_heading_hierarchy(levels: list) -> list:
    """Check for heading hierarchy issues. Returns list of issues."""
    issues = []
    if not levels:
        issues.append("No headings found on page")
        return issues

    h1_count = levels.count(1)
    if h1_count == 0:
        issues.append("No H1 tag found")
    elif h1_count > 1:
        issues.append(f"Multiple H1 tags found ({h1_count})")

    for i in range(1, len(levels)):
        if levels[i] > levels[i - 1] + 1:
            issues.append(f"Heading skip: H{levels[i-1]} -> H{levels[i]}")
            break

    return issues


def _parse_robots_sections(lines: list) -> dict:
    """Parse robots.txt into {user-agent: [(directive, path), ...]}."""
    sections = {}
    current_agents = []
    for raw_line in lines:
        line = raw_line.split("#", 1)[0].strip()
        if not line:
            continue
        if ":" not in line:
            continue
        directive, _, value = line.partition(":")
        directive = directive.strip().lower()
        value = value.strip()
        if directive == "user-agent":
            current_agents = [value.lower()]
        elif directive in ("allow", "disallow") and current_agents:
            for agent in current_agents:
                sections.setdefault(agent, []).append((directive, value))
    return sections


def _is_fully_blocked(rules: list) -> bool:
    """Return True only if a rule set blocks the entire site (Disallow: /)
    without a broader Allow that overrides it. Path-specific blocks like
    Disallow: /api/ do NOT count as fully blocked."""
    has_root_disallow = any(
        d == "disallow" and p == "/" for d, p in rules
    )
    if not has_root_disallow:
        return False
    has_root_allow = any(
        d == "allow" and p == "/" for d, p in rules
    )
    return not has_root_allow


def check_robots(url: str) -> dict:
    """Check robots.txt for AI bot access."""
    parsed = urllib.parse.urlparse(url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    content, _, _, status, err = fetch_url(robots_url)

    ai_bots = [
        "GPTBot", "ChatGPT-User", "ClaudeBot", "Claude-Web",
        "anthropic-ai", "PerplexityBot", "Google-Extended",
        "Applebot-Extended", "Bingbot"
    ]

    result = {"exists": False, "bots": {}, "raw_snippet": ""}
    if content and status == 200:
        result["exists"] = True
        lines = content.splitlines()
        bot_sections = _parse_robots_sections(lines)

        for bot in ai_bots:
            bot_lower = bot.lower()
            if bot_lower in bot_sections:
                rules = bot_sections[bot_lower]
                if _is_fully_blocked(rules):
                    result["bots"][bot] = "BLOCKED"
                elif any(r[0] == "allow" for r in rules):
                    result["bots"][bot] = "ALLOWED"
                else:
                    result["bots"][bot] = "MENTIONED"
            else:
                result["bots"][bot] = "NOT_CONFIGURED"

        if "*" in bot_sections and _is_fully_blocked(bot_sections["*"]):
            for bot in ai_bots:
                if result["bots"].get(bot) == "NOT_CONFIGURED":
                    result["bots"][bot] = "BLOCKED_BY_WILDCARD"
    return result


def check_sitemap(url: str) -> dict:
    """Check if sitemap.xml exists and basic stats."""
    parsed = urllib.parse.urlparse(url)
    sitemap_url = f"{parsed.scheme}://{parsed.netloc}/sitemap.xml"
    content, _, _, status, err = fetch_url(sitemap_url)

    result = {"exists": False, "url_count": 0}
    if content and status == 200:
        lower = content.lower()
        if "<urlset" in lower or "<sitemapindex" in lower or "<?xml" in lower:
            result["exists"] = True
            result["url_count"] = len(re.findall(r"<loc>", content, re.I))
    return result


def check_llms_txt(url: str) -> dict:
    """Check if llms.txt exists and validate basic structure."""
    parsed = urllib.parse.urlparse(url)
    llms_url = f"{parsed.scheme}://{parsed.netloc}/llms.txt"
    content, headers, _, status, err = fetch_url(llms_url)

    result = {"exists": False, "valid": False, "issues": []}
    if content and status == 200:
        result["exists"] = True
        has_h1 = bool(re.search(r"^# .+", content, re.M))
        has_blockquote = bool(re.search(r"^> .+", content, re.M))
        has_contact = bool(re.search(r"^## Contact", content, re.M | re.I))
        size_ok = len(content.encode("utf-8")) < 50 * 1024

        if has_h1 and has_blockquote and has_contact and size_ok:
            result["valid"] = True
        else:
            if not has_h1:
                result["issues"].append("Missing H1 heading")
            if not has_blockquote:
                result["issues"].append("Missing blockquote summary")
            if not has_contact:
                result["issues"].append("Missing ## Contact section")
            if not size_ok:
                result["issues"].append("File exceeds 50KB")
    return result


def check_https(url: str) -> bool:
    """Check if site uses HTTPS."""
    return url.startswith("https://")


def print_section(title: str):
    print(f"\n## {title}")


def print_status(label: str, value, good_values=None, bad_values=None):
    """Print a status line with pass/fail indicator."""
    status = ""
    if good_values and value in good_values:
        status = " [PASS]"
    elif bad_values and value in bad_values:
        status = " [FAIL]"
    elif good_values and value not in good_values:
        status = " [WARN]"
    print(f"  {label}: {value}{status}")


def main():
    parser = argparse.ArgumentParser(description="SEO & GEO Audit (no API required)")
    parser.add_argument("url", help="URL to audit")
    parser.add_argument("--full", action="store_true", help="Show detailed output")
    parser.add_argument("--ua", type=str, default=None,
                        help="Override User-Agent string for all requests")
    args = parser.parse_args()

    global _custom_ua
    if args.ua:
        _custom_ua = args.ua

    url = args.url
    if not url.startswith("http"):
        url = f"https://{url}"

    print(f"{'=' * 60}")
    print(f"  SEO & GEO AUDIT: {url}")
    print(f"{'=' * 60}")

    content, headers, load_time, status_code, error_msg = fetch_url(url)
    if not content:
        print(f"\n  ERROR: Could not fetch URL")
        if status_code:
            print(f"  Status code: {status_code}")
        if error_msg:
            print(f"  Diagnosis: {error_msg}")
        print()
        print("  Suggestions:")
        print("    - If using Cursor or Claude Code, try WebFetch tool instead")
        print("    - If using another AI agent, try its built-in web browsing")
        print("    - Try: curl -sL -A \"Mozilla/5.0 ...\" \"" + url + "\"")
        print("    - Check if a firewall or VPN is blocking outbound requests")
        print("    - Paste the page HTML directly for offline analysis")
        print("    - Switch to codebase mode if you have the source locally")
        exit_code = 1 if status_code else 2
        sys.exit(exit_code)

    meta = extract_meta(content)
    heading_issues = check_heading_hierarchy(meta["heading_hierarchy"])

    # --- Meta Tags ---
    print_section("Meta Tags")
    title = meta["title"]
    title_len = len(title) if title else 0
    print_status("title", f'"{title[:70]}{"..." if title and len(title) > 70 else ""}"' if title else "MISSING")
    print_status("title_length", f"{title_len} chars", good_values=[] if not title else (
        [f"{title_len} chars"] if 50 <= title_len <= 60 else []
    ))
    if title_len > 0 and (title_len < 50 or title_len > 60):
        print(f"    -> Recommended: 50-60 chars (currently {title_len})")

    desc = meta["description"]
    desc_len = len(desc) if desc else 0
    print_status("description", f'"{desc[:80]}{"..." if desc and len(desc) > 80 else ""}"' if desc else "MISSING")
    print_status("description_length", f"{desc_len} chars")
    if desc_len > 0 and (desc_len < 150 or desc_len > 160):
        print(f"    -> Recommended: 150-160 chars (currently {desc_len})")

    print_status("canonical", meta["canonical"] if meta["canonical"] else "MISSING")

    # --- Headings ---
    print_section("Headings")
    h1_count = len(meta["h1_tags"])
    print_status("h1_count", h1_count)
    if meta["h1_tags"]:
        for i, h1 in enumerate(meta["h1_tags"]):
            print(f"    H1[{i+1}]: {h1}")
    print_status("h2_count", meta["h2_count"])
    print_status("h3_count", meta["h3_count"])
    if heading_issues:
        for issue in heading_issues:
            print(f"    [ISSUE] {issue}")
    else:
        print("    [PASS] Heading hierarchy OK")

    # --- Open Graph ---
    print_section("Open Graph Tags")
    og = meta["og_tags"]
    og_present = sum(1 for v in og.values() if v)
    print_status("og_tags_present", f"{og_present}/5")
    if args.full:
        for key, val in og.items():
            print_status(f"  {key}", val if val else "MISSING")
    print_status("twitter_card", meta["twitter_card"] if meta["twitter_card"] else "MISSING")

    # --- Schema Markup ---
    print_section("Schema Markup")
    print_status("json_ld_blocks", meta["jsonld_count"])
    if meta["schema_types"]:
        print(f"    types: {', '.join(meta['schema_types'])}")
    else:
        print("    [WARN] No JSON-LD schema detected in static HTML")
        print("    Note: JS-injected schema (Yoast, RankMath) won't appear here.")
        print("    Use Google Rich Results Test for accurate detection.")
    print_status("has_date_meta", "yes" if meta["has_date_meta"] else "no")

    # --- Content Metrics ---
    print_section("Content Metrics")
    print_status("word_count", meta["word_count"])
    if meta["word_count"] < 300:
        print("    [WARN] Thin content (< 300 words)")
    print_status("total_images", meta["total_images"])
    print_status("images_without_alt", meta["images_without_alt"])
    if meta["images_without_alt"] > 0:
        print(f"    [WARN] {meta['images_without_alt']} images missing alt text")
    print_status("internal_links", meta["internal_links"])
    print_status("external_links", meta["external_links"])

    # --- Performance ---
    print_section("Performance")
    print_status("load_time", f"{load_time:.2f}s")
    if load_time > 3:
        print("    [FAIL] Page loads in > 3 seconds")
    elif load_time > 2:
        print("    [WARN] Page loads in > 2 seconds")
    else:
        print("    [PASS] Good load time")
    print_status("https", "yes" if check_https(url) else "NO")

    # --- robots.txt ---
    print_section("robots.txt & AI Crawler Access")
    robots = check_robots(url)
    print_status("robots_txt_exists", "yes" if robots["exists"] else "no")
    if robots["exists"]:
        for bot, status in robots["bots"].items():
            icon = {"ALLOWED": "[PASS]", "BLOCKED": "[FAIL]", "BLOCKED_BY_WILDCARD": "[FAIL]",
                    "MENTIONED": "[INFO]", "NOT_CONFIGURED": "[WARN]"}.get(status, "")
            print(f"    {bot}: {status} {icon}")
    else:
        print("    [WARN] No robots.txt found -- AI bots may not know they're allowed")

    # --- Sitemap ---
    print_section("Sitemap")
    sitemap = check_sitemap(url)
    print_status("sitemap_xml", "yes" if sitemap["exists"] else "no")
    if sitemap["exists"]:
        print_status("urls_in_sitemap", sitemap["url_count"])

    # --- llms.txt ---
    print_section("llms.txt (AI Discovery File)")
    llms = check_llms_txt(url)
    print_status("llms_txt_exists", "yes" if llms["exists"] else "no")
    if llms["exists"]:
        print_status("llms_txt_valid", "yes" if llms["valid"] else "no")
        if llms["issues"]:
            for issue in llms["issues"]:
                print(f"    [ISSUE] {issue}")
    else:
        print("    [WARN] No llms.txt found. Sites with llms.txt see ~35% increase in AI visibility.")
        print("    Create one at: /llms.txt (see fix-prompt-templates.md, Template 4)")

    # --- Summary ---
    print(f"\n{'=' * 60}")
    print("  SUMMARY")
    print(f"{'=' * 60}")

    issues_p0 = []
    issues_p1 = []
    issues_p2 = []

    if not meta["title"]:
        issues_p0.append("Missing title tag")
    elif title_len < 30 or title_len > 70:
        issues_p1.append(f"Title length ({title_len} chars) outside 50-60 range")
    if not meta["description"]:
        issues_p0.append("Missing meta description")
    elif desc_len < 120 or desc_len > 170:
        issues_p1.append(f"Description length ({desc_len} chars) outside 150-160 range")
    if h1_count == 0:
        issues_p0.append("No H1 tag")
    elif h1_count > 1:
        issues_p1.append(f"Multiple H1 tags ({h1_count})")
    if heading_issues:
        for hi in heading_issues:
            if "skip" in hi.lower():
                issues_p1.append(hi)
    if not check_https(url):
        issues_p0.append("No HTTPS")
    if meta["images_without_alt"] > 0:
        issues_p1.append(f"{meta['images_without_alt']} images missing alt text")
    if meta["word_count"] < 300:
        issues_p1.append(f"Thin content ({meta['word_count']} words)")
    if og_present < 3:
        issues_p2.append(f"Only {og_present}/5 Open Graph tags present")
    if not meta["twitter_card"]:
        issues_p2.append("Missing Twitter Card tags")
    if meta["jsonld_count"] == 0:
        issues_p1.append("No JSON-LD schema detected (may be JS-injected)")
    if not meta["has_date_meta"]:
        issues_p2.append("No datePublished/dateModified meta")
    if not meta["canonical"]:
        issues_p1.append("Missing canonical tag")

    if robots["exists"]:
        blocked = [b for b, s in robots["bots"].items() if "BLOCKED" in s]
        not_configured = [b for b, s in robots["bots"].items() if s == "NOT_CONFIGURED"]
        if blocked:
            issues_p1.append(f"AI bots blocked: {', '.join(blocked)}")
        if not_configured:
            issues_p2.append(f"AI bots not configured: {', '.join(not_configured)}")
    else:
        issues_p1.append("No robots.txt file")

    if not sitemap["exists"]:
        issues_p1.append("No sitemap.xml found")

    if not llms["exists"]:
        issues_p2.append("No llms.txt file (AI discovery)")
    elif not llms["valid"]:
        issues_p2.append(f"llms.txt has issues: {', '.join(llms['issues'])}")

    if load_time and load_time > 3:
        issues_p1.append(f"Slow load time ({load_time:.1f}s)")
    elif load_time and load_time > 2:
        issues_p2.append(f"Load time could be better ({load_time:.1f}s)")

    print(f"\n  P0 (Critical): {len(issues_p0)} issues")
    for i in issues_p0:
        print(f"    - {i}")
    print(f"  P1 (Important): {len(issues_p1)} issues")
    for i in issues_p1:
        print(f"    - {i}")
    print(f"  P2 (Recommended): {len(issues_p2)} issues")
    for i in issues_p2:
        print(f"    - {i}")

    total = len(issues_p0) + len(issues_p1) + len(issues_p2)
    if total == 0:
        seo_score = 10
    else:
        seo_score = max(0, 10 - (len(issues_p0) * 3) - (len(issues_p1) * 1.5) - (len(issues_p2) * 0.5))
        seo_score = round(min(10, max(0, seo_score)), 1)

    ai_blocked = any("BLOCKED" in s for s in robots.get("bots", {}).values())
    if ai_blocked:
        geo_score = 0
    else:
        geo_deductions = 0
        if not llms["exists"]:
            geo_deductions += 1.5
        if meta["jsonld_count"] == 0:
            geo_deductions += 2
        if not meta["has_date_meta"]:
            geo_deductions += 1
        if not robots["exists"]:
            geo_deductions += 2
        else:
            not_conf = sum(1 for s in robots["bots"].values() if s == "NOT_CONFIGURED")
            geo_deductions += not_conf * 0.3
        geo_score = round(max(0, 10 - geo_deductions), 1)

    print(f"\n  SEO Health Score: {seo_score}/10")
    print(f"  AI Visibility Score: {geo_score}/10")
    if ai_blocked:
        print("    [VETO] AI crawlers are blocked -- AI visibility is 0 regardless of content quality")

    print(f"\n{'=' * 60}")
    print("  AUDIT COMPLETE")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
