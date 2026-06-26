#!/usr/bin/env python3
"""
SEO Audit Pro - Main audit script
Usage: python3 seo_audit.py <url> [--keyword "target keyword"] [--output report.json]
"""

import sys
import json
import time
import argparse
import re
from urllib.parse import urlparse, urljoin
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
import ssl

def make_request(url, timeout=10):
    """Make HTTP request with browser-like headers."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; SEOAuditPro/1.0; +https://clawhub.ai)',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    }
    # Use system default SSL context (validates certificates properly)
    ctx = ssl.create_default_context()
    req = Request(url, headers=headers)
    try:
        start = time.time()
        response = urlopen(req, timeout=timeout, context=ctx)
        elapsed = round((time.time() - start) * 1000)
        content = response.read()
        return {
            'status': response.status,
            'headers': dict(response.headers),
            'body': content.decode('utf-8', errors='replace'),
            'ttfb_ms': elapsed,
            'final_url': response.url,
        }
    except HTTPError as e:
        return {'status': e.code, 'headers': dict(e.headers), 'body': '', 'ttfb_ms': 0, 'final_url': url, 'error': str(e)}
    except URLError as e:
        return {'status': 0, 'headers': {}, 'body': '', 'ttfb_ms': 0, 'final_url': url, 'error': str(e)}
    except Exception as e:
        return {'status': 0, 'headers': {}, 'body': '', 'ttfb_ms': 0, 'final_url': url, 'error': str(e)}

def extract_meta(html):
    """Extract meta tags and key on-page signals from HTML."""
    result = {}

    # Title
    m = re.search(r'<title[^>]*>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
    result['title'] = m.group(1).strip() if m else None
    result['title_length'] = len(result['title']) if result['title'] else 0

    # Meta description
    m = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', html, re.IGNORECASE)
    if not m:
        m = re.search(r'<meta\s+content=["\'](.*?)["\']\s+name=["\']description["\']', html, re.IGNORECASE)
    result['meta_description'] = m.group(1).strip() if m else None
    result['meta_description_length'] = len(result['meta_description']) if result['meta_description'] else 0

    # H1 tags
    h1s = re.findall(r'<h1[^>]*>(.*?)</h1>', html, re.IGNORECASE | re.DOTALL)
    result['h1_count'] = len(h1s)
    result['h1_tags'] = [re.sub(r'<[^>]+>', '', h).strip() for h in h1s[:3]]

    # H2 tags
    h2s = re.findall(r'<h2[^>]*>(.*?)</h2>', html, re.IGNORECASE | re.DOTALL)
    result['h2_count'] = len(h2s)
    result['h2_tags'] = [re.sub(r'<[^>]+>', '', h).strip() for h in h2s[:5]]

    # Images without alt
    all_imgs = re.findall(r'<img[^>]*>', html, re.IGNORECASE)
    imgs_no_alt = [img for img in all_imgs if 'alt=' not in img.lower() or re.search(r'alt=["\']["\']', img, re.IGNORECASE)]
    result['total_images'] = len(all_imgs)
    result['images_missing_alt'] = len(imgs_no_alt)

    # Canonical
    m = re.search(r'<link[^>]*rel=["\']canonical["\']\s+href=["\'](.*?)["\']', html, re.IGNORECASE)
    if not m:
        m = re.search(r'<link[^>]*href=["\'](.*?)["\']\s+rel=["\']canonical["\']', html, re.IGNORECASE)
    result['canonical'] = m.group(1).strip() if m else None

    # Viewport
    result['has_viewport'] = bool(re.search(r'<meta[^>]*name=["\']viewport["\']', html, re.IGNORECASE))

    # Open Graph
    og_title = re.search(r'<meta[^>]*property=["\']og:title["\']\s+content=["\'](.*?)["\']', html, re.IGNORECASE)
    result['og_title'] = og_title.group(1).strip() if og_title else None

    # Schema.org
    result['has_schema_org'] = 'schema.org' in html or 'application/ld+json' in html

    # Robots meta
    robots_meta = re.search(r'<meta[^>]*name=["\']robots["\']\s+content=["\'](.*?)["\']', html, re.IGNORECASE)
    result['robots_meta'] = robots_meta.group(1).strip() if robots_meta else None

    # Word count estimate (strip all tags)
    text = re.sub(r'<[^>]+>', ' ', html)
    text = re.sub(r'\s+', ' ', text).strip()
    result['word_count'] = len(text.split())

    # Internal / external links
    links = re.findall(r'<a[^>]*href=["\'](.*?)["\']', html, re.IGNORECASE)
    result['total_links'] = len(links)

    return result

def check_robots(base_url):
    """Fetch robots.txt."""
    parsed = urlparse(base_url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    r = make_request(robots_url, timeout=8)
    return {
        'url': robots_url,
        'status': r['status'],
        'exists': r['status'] == 200,
        'has_sitemap': 'sitemap' in r['body'].lower() if r['body'] else False,
        'disallow_all': 'disallow: /' in r['body'].lower() if r['body'] else False,
    }

def check_sitemap(base_url, robots_body=''):
    """Try to find sitemap.xml."""
    parsed = urlparse(base_url)
    sitemap_url = f"{parsed.scheme}://{parsed.netloc}/sitemap.xml"

    # Also check if robots.txt mentions a sitemap
    if robots_body:
        m = re.search(r'sitemap:\s*(https?://\S+)', robots_body, re.IGNORECASE)
        if m:
            sitemap_url = m.group(1).strip()

    r = make_request(sitemap_url, timeout=8)
    return {
        'url': sitemap_url,
        'status': r['status'],
        'exists': r['status'] == 200,
        'size_bytes': len(r['body'].encode()) if r['body'] else 0,
    }

def check_https(url, response):
    """HTTPS / redirect checks."""
    parsed = urlparse(url)
    final_parsed = urlparse(response.get('final_url', url))
    return {
        'uses_https': final_parsed.scheme == 'https',
        'redirected': url != response.get('final_url', url),
        'redirect_chain': [url, response.get('final_url', url)] if url != response.get('final_url', url) else [url],
    }

def check_headers(headers):
    """Analyze security and performance headers."""
    h = {k.lower(): v for k, v in headers.items()}
    return {
        'x_frame_options': h.get('x-frame-options'),
        'x_content_type_options': h.get('x-content-type-options'),
        'strict_transport_security': h.get('strict-transport-security'),
        'content_security_policy': bool(h.get('content-security-policy')),
        'cache_control': h.get('cache-control'),
        'server': h.get('server'),
        'content_encoding': h.get('content-encoding'),  # gzip/br
    }

def keyword_analysis(html, keyword):
    """Basic keyword presence analysis."""
    if not keyword:
        return None
    text = re.sub(r'<[^>]+>', ' ', html).lower()
    kw = keyword.lower()
    count = text.count(kw)
    word_count = len(text.split())
    density = round((count / word_count * 100), 2) if word_count else 0

    # Check in title, h1, meta desc
    title_m = re.search(r'<title[^>]*>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
    h1_m = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.IGNORECASE | re.DOTALL)
    meta_m = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', html, re.IGNORECASE)

    return {
        'keyword': keyword,
        'occurrences': count,
        'density_percent': density,
        'in_title': kw in (title_m.group(1).lower() if title_m else ''),
        'in_h1': kw in (h1_m.group(1).lower() if h1_m else ''),
        'in_meta_description': kw in (meta_m.group(1).lower() if meta_m else ''),
        'in_url': kw.replace(' ', '-') in html[:500].lower() or kw.replace(' ', '_') in html[:500].lower(),
    }

def score_audit(data):
    """Calculate score out of 100."""
    score = 100
    deductions = []

    meta = data.get('on_page', {})
    tech = data.get('technical', {})
    headers = data.get('headers', {})

    # Technical (40 pts)
    if not tech.get('uses_https'):
        score -= 15; deductions.append('No HTTPS (-15)')
    if data['response']['ttfb_ms'] > 2000:
        score -= 10; deductions.append('Slow TTFB >2s (-10)')
    elif data['response']['ttfb_ms'] > 800:
        score -= 5; deductions.append('TTFB between 800ms-2s (-5)')
    if not tech.get('robots', {}).get('exists'):
        score -= 5; deductions.append('No robots.txt (-5)')
    if not tech.get('sitemap', {}).get('exists'):
        score -= 5; deductions.append('No sitemap.xml (-5)')
    if not meta.get('has_viewport'):
        score -= 5; deductions.append('No viewport meta (-5)')

    # On-Page (40 pts)
    if not meta.get('title'):
        score -= 10; deductions.append('Missing title tag (-10)')
    elif meta.get('title_length', 0) > 70 or meta.get('title_length', 0) < 30:
        score -= 5; deductions.append(f"Title length {meta.get('title_length')} chars (ideal 30-70) (-5)")
    if not meta.get('meta_description'):
        score -= 8; deductions.append('Missing meta description (-8)')
    elif meta.get('meta_description_length', 0) > 160 or meta.get('meta_description_length', 0) < 70:
        score -= 4; deductions.append(f"Meta description length {meta.get('meta_description_length')} chars (ideal 70-160) (-4)")
    if meta.get('h1_count', 0) == 0:
        score -= 8; deductions.append('No H1 tag (-8)')
    elif meta.get('h1_count', 0) > 1:
        score -= 4; deductions.append(f"Multiple H1 tags ({meta.get('h1_count')}) (-4)")
    if not meta.get('canonical'):
        score -= 4; deductions.append('No canonical tag (-4)')

    # Content (20 pts)
    if meta.get('images_missing_alt', 0) > 0:
        deduction = min(5, meta.get('images_missing_alt', 0))
        score -= deduction; deductions.append(f"{meta.get('images_missing_alt')} images missing alt text (-{deduction})")
    if not meta.get('has_schema_org'):
        score -= 3; deductions.append('No Schema.org structured data (-3)')
    if meta.get('word_count', 0) < 300:
        score -= 5; deductions.append(f"Low word count ({meta.get('word_count')}) (-5)")

    score = max(0, score)
    grade = 'A' if score >= 90 else 'B' if score >= 75 else 'C' if score >= 60 else 'D' if score >= 45 else 'F'

    return {'score': score, 'grade': grade, 'deductions': deductions}

def run_audit(url, keyword=None):
    """Main audit runner."""
    # Normalize URL
    if not url.startswith('http'):
        url = 'https://' + url

    print(f"[SEO Audit Pro] Auditing: {url}", file=sys.stderr)

    # Fetch main page
    print("[1/4] Fetching main page...", file=sys.stderr)
    response = make_request(url)

    if response['status'] == 0:
        return {'error': f"Failed to fetch {url}: {response.get('error', 'Unknown error')}", 'url': url}

    html = response['body']

    # On-page analysis
    print("[2/4] Analyzing on-page signals...", file=sys.stderr)
    on_page = extract_meta(html)

    # Technical checks
    print("[3/4] Running technical checks...", file=sys.stderr)
    robots = check_robots(url)
    sitemap = check_sitemap(url)
    https_info = check_https(url, response)
    headers_info = check_headers(response['headers'])

    # Keyword analysis
    print("[4/4] Keyword analysis...", file=sys.stderr)
    kw_analysis = keyword_analysis(html, keyword) if keyword else None

    data = {
        'url': url,
        'audited_at': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        'response': {
            'status': response['status'],
            'final_url': response['final_url'],
            'ttfb_ms': response['ttfb_ms'],
        },
        'technical': {
            'uses_https': https_info['uses_https'],
            'redirected': https_info['redirected'],
            'redirect_chain': https_info['redirect_chain'],
            'robots': robots,
            'sitemap': sitemap,
        },
        'headers': headers_info,
        'on_page': on_page,
        'keyword_analysis': kw_analysis,
    }

    data['score'] = score_audit(data)
    return data

def main():
    parser = argparse.ArgumentParser(description='SEO Audit Pro - Full website SEO audit')
    parser.add_argument('url', help='URL to audit (e.g., https://example.com)')
    parser.add_argument('--keyword', '-k', help='Target keyword for keyword analysis', default=None)
    parser.add_argument('--output', '-o', help='Output JSON file (default: stdout)', default=None)
    args = parser.parse_args()

    result = run_audit(args.url, args.keyword)

    output = json.dumps(result, indent=2, ensure_ascii=False)

    if args.output:
        with open(args.output, 'w') as f:
            f.write(output)
        print(f"[SEO Audit Pro] Report saved to {args.output}", file=sys.stderr)
    else:
        print(output)

if __name__ == '__main__':
    main()
