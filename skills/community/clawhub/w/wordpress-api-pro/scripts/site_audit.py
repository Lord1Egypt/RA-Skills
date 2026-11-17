#!/usr/bin/env python3
"""No-auth Tier-1 website audit — public signals only (PageSpeed/SSL/headers/CMS/SEO).

Run cold, before any engagement, as the sales-hook quick scan. Read-only public
fetches; no credentials. Outputs findings JSON (default) or a 1-page --summary.

Usage:
    python3 site_audit.py https://example.com
    python3 site_audit.py https://example.com --summary
Env (optional): PAGESPEED_API_KEY  (higher PageSpeed Insights quota)
"""
import argparse, json, os, re, sys, urllib.request, urllib.parse, urllib.error
from datetime import datetime, timezone

from security import (
    HostResolutionError, SafetyError, connect_public_tls, die_safety, urlopen_probe,
    validate_probe_url,
)

UA = "Mozilla/5.0 (compatible; DigitizerAudit/1.0)"
# Ceiling on a response body. The audit parses the document head - title, meta,
# generator, h1 - so truncating a huge page costs nothing, while reading one
# unbounded lets any server it visits decide how much memory this process uses.
MAX_BODY_BYTES = 5 * 1024 * 1024
SECURITY_HEADERS = [
    "Strict-Transport-Security", "Content-Security-Policy", "X-Frame-Options",
    "X-Content-Type-Options", "Referrer-Policy",
]


# ---- pure parsers (unit-tested, no network) --------------------------------
def parse_cms(html, headers):
    html = html or ""
    headers = {k.lower(): v for k, v in (headers or {}).items()}
    gen = re.search(r'<meta[^>]+name=["\']generator["\'][^>]+content=["\']([^"\']+)["\']', html, re.I)
    generator = gen.group(1) if gen else None
    is_wp = bool(generator and "wordpress" in generator.lower()) or "/wp-content/" in html or "/wp-json" in html
    wp_version = None
    if generator:
        m = re.search(r'WordPress\s+([0-9.]+)', generator, re.I)
        if m:
            wp_version = m.group(1)
    php = None
    xpb = headers.get("x-powered-by", "")
    mp = re.search(r'PHP/([0-9.]+)', xpb)
    if mp:
        php = mp.group(1)
    return {"is_wordpress": is_wp, "wp_version": wp_version, "php_version": php, "generator": generator}


def parse_seo(html):
    html = html or ""
    t = re.search(r'<title[^>]*>(.*?)</title>', html, re.I | re.S)
    d = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\'](.*?)["\']', html, re.I | re.S)
    return {
        "title": t.group(1).strip() if t else None,
        "meta_description": d.group(1).strip() if d else None,
        "h1_count": len(re.findall(r'<h1[\s>]', html, re.I)),
        "has_canonical": bool(re.search(r'<link[^>]+rel=["\']canonical["\']', html, re.I)),
    }


def analyze_headers(headers):
    present_keys = {k.lower() for k in (headers or {})}
    present, missing = [], []
    for h in SECURITY_HEADERS:
        (present if h.lower() in present_keys else missing).append(h)
    return {"present": present, "missing": missing}


def _parse_cert_time(s):
    # OpenSSL notAfter format, e.g. "Mar  2 00:00:00 2026 GMT"
    return datetime.strptime(s, "%b %d %H:%M:%S %Y %Z").replace(tzinfo=timezone.utc)


def ssl_days_left(notafter, now=None):
    end = _parse_cert_time(notafter)
    now = now or datetime.now(timezone.utc)
    return (end - now).days


def grade_pagespeed(score):
    # score is 0..1 (Lighthouse). >=0.9 pass, >=0.7 warn, else fail.
    if score is None:
        return "skipped"
    if score >= 0.9:
        return "pass"
    if score >= 0.7:
        return "warn"
    return "fail"


# ---- fetching (network; not unit-tested) -----------------------------------
def _get(url, method="GET", timeout=15):
    req = urllib.request.Request(url, method=method, headers={"User-Agent": UA})
    try:
        with urlopen_probe(req, timeout=timeout) as r:
            body = r.read(MAX_BODY_BYTES).decode("utf-8", "replace") if method == "GET" else ""
            return r.getcode(), dict(r.headers), r.geturl(), body
    except urllib.error.HTTPError as e:
        # An HTTP 4xx/5xx is a *reachable* server — return its status, headers,
        # url and body so the status/header/SEO checks still run. Only DNS /
        # timeout / connection-refused (URLError, socket errors) mean unreachable,
        # and those propagate to the caller's generic except.
        body = e.read(MAX_BODY_BYTES).decode("utf-8", "replace") if method == "GET" else ""
        return e.code, dict(e.headers), e.geturl(), body


def _ssl_notafter(host, port=443, timeout=10):
    # connect_public_tls validates and dials one address, so the certificate is
    # read from the endpoint that was checked. Validating the name and then
    # letting create_connection resolve it again is the rebinding gap.
    with connect_public_tls(host, port=port, timeout=timeout) as ssock:
        return ssock.getpeercert().get("notAfter")


def _url_exists(url):
    try:
        code, _, _, _ = _get(url, method="GET", timeout=10)
        return 200 <= code < 400
    except Exception:
        return False


def _pagespeed(url, strategy, api_key=None):
    base = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
    q = {"url": url, "strategy": strategy}
    if api_key:
        q["key"] = api_key
    try:
        _, _, _, body = _get(base + "?" + urllib.parse.urlencode(q), timeout=60)
        data = json.loads(body)
        return data["lighthouseResult"]["categories"]["performance"]["score"]
    except Exception:
        return None


def audit(url, api_key=None):
    findings = []

    def add(group, check, value, status, note=""):
        findings.append({"group": group, "check": check, "value": value, "status": status, "note": note})

    try:
        code, headers, final_url, html = _get(url)
    except HostResolutionError as e:
        # A name that does not resolve is an unreachable site, not a refusal.
        add("reach", "reachable", str(e), "fail", "site did not respond")
        return {"url": url, "reachable": False, "findings": findings}
    except SafetyError as e:
        add("reach", "blocked", str(e), "fail", "refused by the address safety rule")
        return {"url": url, "reachable": False, "findings": findings}
    except Exception as e:
        add("reach", "reachable", str(e), "fail", "site did not respond")
        return {"url": url, "reachable": False, "findings": findings}

    add("reach", "status", code, "pass" if code < 400 else "fail")
    add("reach", "https", final_url.startswith("https://"), "pass" if final_url.startswith("https://") else "fail",
        "no HTTPS redirect" if not final_url.startswith("https://") else "")

    host = urllib.parse.urlparse(final_url).hostname
    if final_url.startswith("https://") and host:
        try:
            na = _ssl_notafter(host)
            days = ssl_days_left(na) if na else None
            st = "pass" if (days or 0) > 20 else ("warn" if (days or 0) > 0 else "fail")
            add("security", "ssl_days_left", days, st, f"expires {na}")
        except Exception as e:
            add("security", "ssl", str(e), "fail", "SSL check failed")

    hdr = analyze_headers(headers)
    add("security", "security_headers", f"{len(hdr['present'])}/5",
        "pass" if len(hdr["present"]) >= 4 else ("warn" if hdr["present"] else "fail"),
        "missing: " + ", ".join(hdr["missing"]) if hdr["missing"] else "")

    cms = parse_cms(html, headers)
    add("cms", "wordpress", cms["is_wordpress"], "pass" if cms["is_wordpress"] else "warn",
        f"version {cms['wp_version']}" if cms["wp_version"] else "version hidden")
    if cms["php_version"]:
        php_ok = cms["php_version"].startswith(("8.1", "8.2", "8.3", "8.4"))
        add("security", "php_version", cms["php_version"], "pass" if php_ok else "fail",
            "EOL PHP" if not php_ok else "")

    seo = parse_seo(html)
    add("seo", "title", seo["title"], "pass" if seo["title"] else "fail")
    add("seo", "meta_description", seo["meta_description"], "pass" if seo["meta_description"] else "fail")
    add("seo", "single_h1", seo["h1_count"], "pass" if seo["h1_count"] == 1 else "warn",
        f"{seo['h1_count']} H1s")
    add("seo", "canonical", seo["has_canonical"], "pass" if seo["has_canonical"] else "warn")

    origin = f"{urllib.parse.urlparse(final_url).scheme}://{host}"
    add("seo", "sitemap.xml", _url_exists(origin + "/sitemap.xml"), "pass" if _url_exists(origin + "/sitemap.xml") else "fail")
    add("seo", "robots.txt", _url_exists(origin + "/robots.txt"), "pass" if _url_exists(origin + "/robots.txt") else "warn")

    for strat in ("mobile", "desktop"):
        score = _pagespeed(final_url, strat, api_key)
        add("performance", f"pagespeed_{strat}", round(score * 100) if score is not None else None,
            grade_pagespeed(score), "PSI unavailable" if score is None else "")

    return {"url": final_url, "reachable": True, "findings": findings}


def _summary(result):
    lines = [f"# Quick audit — {result['url']}", ""]
    order = {"fail": 0, "warn": 1, "skipped": 2, "pass": 3}
    icon = {"pass": "🟢", "warn": "🟡", "fail": "🔴", "skipped": "⚪"}
    rendered = []
    for f in sorted(result["findings"], key=lambda x: order.get(x["status"], 9)):
        note = f" — {f['note']}" if f["note"] else ""
        rendered.append(f"{icon.get(f['status'],'')} [{f['group']}] {f['check']}: {f['value']}{note}")
    # An unreachable result still carries a finding, and a refused address is not
    # a connectivity failure: printing a flat "Site unreachable." for both would
    # hide which address was blocked and why.
    return "\n".join(lines + (rendered or ["Site unreachable."]))


def main():
    p = argparse.ArgumentParser(description="No-auth Tier-1 website audit")
    p.add_argument("url", nargs="?", help="Site URL (http(s)://...)")
    p.add_argument("--url", dest="url_opt")
    p.add_argument("--summary", action="store_true", help="Human 1-page summary instead of JSON")
    a = p.parse_args()
    url = a.url or a.url_opt
    if not url:
        print(json.dumps({"error": "URL required"}), file=sys.stderr); sys.exit(1)
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    try:
        validate_probe_url(url)
    except HostResolutionError:
        # Let audit() run and report it as unreachable in its JSON, the way it
        # did before this URL was validated up front.
        pass
    except SafetyError as e:
        die_safety(e)
    result = audit(url, api_key=os.getenv("PAGESPEED_API_KEY"))
    print(_summary(result) if a.summary else json.dumps(result, indent=2))
    # Exit non-zero for a truly unreachable target (DNS/timeout/refused) OR any
    # failing check — otherwise CI/automation would read an unreachable site as
    # a false success.
    if (not result["reachable"]) or any(f["status"] == "fail" for f in result["findings"]):
        sys.exit(2)


if __name__ == "__main__":
    main()
