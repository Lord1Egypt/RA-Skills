#!/usr/bin/env python3
"""webclaw CLI wrapper for OpenClaw agents.

Smart fetch: tries local HTTP first, falls back to webclaw cloud API
when bot protection or JS rendering is detected. Zero dependencies.

This wrapper exposes 10 of the webclaw API endpoints as CLI commands
(scrape, crawl, crawl-status, map, endpoints, batch, extract,
summarize, diff, brand). The full HTTP API has more endpoints (search,
research, watch, vertical extractors, /v2 Firecrawl-compat) — see
SKILL.md for the complete reference; call those directly over HTTP.

Usage:
  python3 scripts/webclaw.py scrape <url> [--format markdown|text|llm|json] [--main] [--no-cache] [--cloud]
  python3 scripts/webclaw.py crawl <url> [--depth N] [--pages N] [--sitemap]
  python3 scripts/webclaw.py crawl-status <job_id>
  python3 scripts/webclaw.py map <url>
  python3 scripts/webclaw.py endpoints <url> [--third-party] [--max-bundles N]
  python3 scripts/webclaw.py batch <url1> <url2> ... [--format markdown|text|llm]
  python3 scripts/webclaw.py extract <url> --prompt "..." | --schema '{"type":"object",...}'
  python3 scripts/webclaw.py summarize <url> [--sentences N]
  python3 scripts/webclaw.py diff <url> --previous <file.json>
  python3 scripts/webclaw.py brand <url>

Environment:
  WEBCLAW_API_KEY       API key for the cloud API (required for cloud calls).
  WEBCLAW_API_KEY_FILE  Optional path to a file containing the API key.
                        If unset, falls back to <skill>/secrets/webclaw_api_key
                        resolved relative to this script, never the CWD.
"""

import html.parser
import ipaddress
import json
import os
import socket
import sys
import urllib.error
import urllib.parse
import urllib.request

API_BASE = "https://api.webclaw.io/v1"

# Max redirects local_fetch will follow before giving up. Each hop is
# re-validated by the SSRF guard, so this only bounds redirect loops.
_MAX_REDIRECTS = 5

# Standard error shape printed to stderr before a non-zero exit.
def _fail(message):
    print(f"Error: {message}", file=sys.stderr)
    sys.exit(1)

# --- Antibot detection patterns (ported from webclaw-server/src/antibot.rs) ---

_CF_PATTERNS = [
    "_cf_chl_opt", "challenge-platform", "cf-spinner",
    "cf-turnstile", "challenges.cloudflare.com/turnstile",
]
_DATADOME_PATTERNS = [
    "geo.captcha-delivery.com", "captcha-delivery.com/captcha",
]
_AWS_PATTERNS = ["awswaf-captcha", "aws-waf-client-browser"]
_HCAPTCHA_PATTERNS = ["hcaptcha.com"]
_SPA_MARKERS = [
    "react-app", 'id="__next"', 'id="root"', 'id="app"',
    "__next_data__", "nuxt", "ng-app",
]


def is_bot_protected(html_text):
    """Check if HTML looks like a bot protection challenge page."""
    low = html_text.lower()

    # Cloudflare challenge
    if "_cf_chl_opt" in low or "challenge-platform" in low:
        return True
    if ("just a moment" in low or "checking your browser" in low) and "cf-spinner" in low:
        return True
    if ("cf-turnstile" in low or "challenges.cloudflare.com/turnstile" in low) and len(html_text) < 100_000:
        return True

    # DataDome
    if "geo.captcha-delivery.com" in low or "captcha-delivery.com/captcha" in low:
        return True

    # AWS WAF
    if "awswaf-captcha" in low or "aws-waf-client-browser" in low:
        return True

    # hCaptcha on short pages
    if "hcaptcha.com" in low and "h-captcha" in low and len(html_text) < 50_000:
        return True

    return False


def needs_js_rendering(word_count, html_text):
    """Check if page likely needs JS rendering."""
    if "<script" not in html_text:
        return False
    if word_count < 50 and len(html_text) > 5_000:
        return True
    if word_count < 800 and len(html_text) > 50_000:
        low = html_text.lower()
        return any(m in low for m in _SPA_MARKERS)
    return False


# --- Simple HTML text extractor (stdlib only) ---

class _TextExtractor(html.parser.HTMLParser):
    """Extract visible text from HTML, skipping script/style tags."""
    _skip = {"script", "style", "noscript", "svg", "head"}

    def __init__(self):
        super().__init__()
        self._pieces = []
        self._skip_depth = 0

    def handle_starttag(self, tag, attrs):
        if tag in self._skip:
            self._skip_depth += 1

    def handle_endtag(self, tag):
        if tag in self._skip and self._skip_depth > 0:
            self._skip_depth -= 1

    def handle_data(self, data):
        if self._skip_depth == 0:
            text = data.strip()
            if text:
                self._pieces.append(text)

    def get_text(self):
        return "\n".join(self._pieces)


def extract_text(html_text):
    """Extract plain text from HTML."""
    parser = _TextExtractor()
    try:
        parser.feed(html_text)
    except Exception:
        pass
    return parser.get_text()


# --- API client ---

# Skill root = parent of this script's directory (scripts/). The fallback
# key file is resolved against this fixed base so the lookup does not
# depend on the process working directory.
_SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_api_key():
    key = os.environ.get("WEBCLAW_API_KEY", "")
    if key:
        return key

    key_file = os.environ.get("WEBCLAW_API_KEY_FILE", "")
    candidates = []
    if key_file:
        candidates.append(key_file)
    candidates.append(os.path.join(_SKILL_ROOT, "secrets", "webclaw_api_key"))

    for path in candidates:
        if os.path.isfile(path):
            with open(path) as f:
                key = f.read().strip()
            if key:
                break
    return key


def _require_key():
    key = get_api_key()
    if not key:
        _fail("WEBCLAW_API_KEY not set. Get one at https://webclaw.io")
    return key


def _do_request(req):
    """Run an HTTP request and decode JSON, exiting cleanly on any failure.

    Covers HTTPError (4xx/5xx with a body), URLError (DNS / connection
    refused), socket.timeout (slow upstream), and a non-JSON body. The
    raw API error string is surfaced when the server returns one.
    """
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            raw = resp.read()
    except urllib.error.HTTPError as e:
        body_text = e.read().decode("utf-8", errors="replace")
        try:
            err = json.loads(body_text)
            _fail(f"{e.code}: {err.get('error', body_text)}")
        except json.JSONDecodeError:
            _fail(f"{e.code}: {body_text}")
    except urllib.error.URLError as e:
        _fail(f"request failed: {e.reason}")
    except (socket.timeout, TimeoutError):
        _fail("request timed out after 120s")
    except OSError as e:
        _fail(f"request failed: {e}")

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        _fail("API returned a non-JSON response")


def api(endpoint, body):
    key = _require_key()
    data = json.dumps(body).encode()
    req = urllib.request.Request(
        f"{API_BASE}/{endpoint}",
        data=data,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
    )
    return _do_request(req)


def api_get(endpoint):
    key = _require_key()
    req = urllib.request.Request(
        f"{API_BASE}/{endpoint}",
        headers={"Authorization": f"Bearer {key}"},
    )
    return _do_request(req)


# --- Smart fetch: local first, cloud fallback ---

class SSRFError(Exception):
    """Raised when a URL or redirect target points at a non-public host."""


def _ip_is_blocked(ip_str):
    """True if the address is loopback / private / link-local / ULA / CGNAT
    or otherwise not a normal public unicast address."""
    try:
        ip = ipaddress.ip_address(ip_str)
    except ValueError:
        return True  # unparseable → refuse

    if (
        ip.is_private          # RFC1918 / fc00::/7 ULA / etc.
        or ip.is_loopback      # 127.0.0.0/8, ::1
        or ip.is_link_local    # 169.254.0.0/16, fe80::/10
        or ip.is_multicast
        or ip.is_reserved
        or ip.is_unspecified   # 0.0.0.0, ::
    ):
        return True

    # 100.64.0.0/10 CGNAT (also used by Tailscale) is not flagged by
    # ipaddress.is_private, so check it explicitly.
    if ip.version == 4 and ip in ipaddress.ip_network("100.64.0.0/10"):
        return True

    # IPv4-mapped IPv6 (::ffff:a.b.c.d) — re-check the embedded v4.
    if ip.version == 6 and ip.ipv4_mapped is not None:
        return _ip_is_blocked(str(ip.ipv4_mapped))

    return False


def _validate_url(url):
    """Validate a URL for local fetching. Enforces http/https and refuses
    hosts that resolve to any private/loopback/link-local/ULA/CGNAT IP.
    Returns the parsed result or raises SSRFError."""
    parsed = urllib.parse.urlsplit(url)

    if parsed.scheme not in ("http", "https"):
        raise SSRFError(f"refusing non-http(s) scheme: {parsed.scheme or '(none)'}")

    host = parsed.hostname
    if not host:
        raise SSRFError("URL has no host")

    # Resolve every address the host maps to and block if ANY is non-public.
    # (Defends against DNS records that return one public + one private IP.)
    try:
        infos = socket.getaddrinfo(host, parsed.port or (443 if parsed.scheme == "https" else 80), proto=socket.IPPROTO_TCP)
    except socket.gaierror as e:
        raise SSRFError(f"DNS resolution failed for {host}: {e}")

    addrs = {info[4][0] for info in infos}
    if not addrs:
        raise SSRFError(f"no addresses resolved for {host}")

    for addr in addrs:
        if _ip_is_blocked(addr):
            raise SSRFError(f"host {host} resolves to a non-public address ({addr})")

    return parsed


class _GuardedRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Re-validate every redirect target through the SSRF guard, and bound
    the redirect chain. Prevents an open redirect from a public page to an
    internal address."""

    # urllib's defaults are max_repeats=4 / max_redirections=10; tighten
    # the total-hop cap to _MAX_REDIRECTS.
    max_redirections = _MAX_REDIRECTS

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        try:
            _validate_url(newurl)
        except SSRFError as e:
            raise urllib.error.URLError(f"blocked redirect: {e}")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


_GUARDED_OPENER = urllib.request.build_opener(_GuardedRedirectHandler())


def local_fetch(url):
    """Try fetching a URL locally. Returns (html, final_url) or raises.

    SSRF-hardened: only http/https, the host (and every redirect hop) must
    resolve exclusively to public IPs, and the redirect chain is bounded.
    """
    _validate_url(url)

    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    })
    with _GUARDED_OPENER.open(req, timeout=15) as resp:
        # Bound the redirect chain: urllib's default cap is 10; tighten it.
        if len(resp.url) and getattr(resp, "redirect_count", 0) > _MAX_REDIRECTS:
            raise SSRFError(f"too many redirects (> {_MAX_REDIRECTS})")
        html_bytes = resp.read()
        # Try to detect encoding
        content_type = resp.headers.get("Content-Type", "")
        charset = "utf-8"
        if "charset=" in content_type:
            charset = content_type.split("charset=")[-1].split(";")[0].strip()
        try:
            html_text = html_bytes.decode(charset)
        except (UnicodeDecodeError, LookupError):
            html_text = html_bytes.decode("utf-8", errors="replace")
        return html_text, resp.url


def smart_scrape(url, force_cloud=False, **api_kwargs):
    """
    Smart fetch: try local first, fall back to cloud API if blocked.

    Returns the content string (text extracted locally or from API).
    """
    if force_cloud:
        return api("scrape", {"url": url, **api_kwargs})

    # Step 1: Try local fetch
    try:
        html_text, final_url = local_fetch(url)
    except (urllib.error.HTTPError, urllib.error.URLError, OSError) as e:
        # Network error or HTTP error — try cloud
        print(f"Local fetch failed ({e}), trying cloud API...", file=sys.stderr)
        return api("scrape", {"url": url, **api_kwargs})

    # Step 2: Check for bot protection
    if is_bot_protected(html_text):
        print("Bot protection detected, using cloud API...", file=sys.stderr)
        return api("scrape", {"url": url, **api_kwargs})

    # Step 3: Extract text and check for JS rendering
    text = extract_text(html_text)
    word_count = len(text.split())

    if needs_js_rendering(word_count, html_text):
        print("JS-rendered page detected, using cloud API...", file=sys.stderr)
        return api("scrape", {"url": url, **api_kwargs})

    # Step 4: Local extraction succeeded — return as pseudo-API response
    # (No API credits used)
    return {
        "url": final_url,
        "markdown": text,  # Basic text extraction (not as good as webclaw-core, but free)
        "text": text,
        "_source": "local",
    }


# --- Commands ---

def cmd_scrape(args):
    url = args[0]
    fmt = "markdown"
    main_only = False
    no_cache = False
    force_cloud = False
    include = []
    exclude = []

    i = 1
    while i < len(args):
        if args[i] in ("--format", "-f") and i + 1 < len(args):
            fmt = args[i + 1]
            i += 2
        elif args[i] == "--main":
            main_only = True
            i += 1
        elif args[i] == "--no-cache":
            no_cache = True
            i += 1
        elif args[i] == "--cloud":
            force_cloud = True
            i += 1
        elif args[i] == "--include" and i + 1 < len(args):
            include = args[i + 1].split(",")
            i += 2
        elif args[i] == "--exclude" and i + 1 < len(args):
            exclude = args[i + 1].split(",")
            i += 2
        else:
            i += 1

    api_kwargs = {"formats": [fmt]}
    if main_only:
        api_kwargs["only_main_content"] = True
    if no_cache:
        api_kwargs["no_cache"] = True
    if include:
        api_kwargs["include_selectors"] = include
    if exclude:
        api_kwargs["exclude_selectors"] = exclude

    # Use smart fetch for scrape (unless selectors are used, then always cloud)
    if include or exclude or main_only or fmt in ("llm", "json"):
        force_cloud = True

    result = smart_scrape(url, force_cloud=force_cloud, **api_kwargs)

    source = result.get("_source", "cloud")
    if source == "local":
        print(f"[local extraction - 0 credits used]", file=sys.stderr)

    content = result.get(fmt) or result.get("markdown") or result.get("text") or ""
    if content:
        print(content)
    else:
        print(json.dumps(result, indent=2))


def cmd_crawl(args):
    url = args[0]
    depth = 3
    pages = 50
    sitemap = False

    i = 1
    while i < len(args):
        if args[i] == "--depth" and i + 1 < len(args):
            depth = int(args[i + 1])
            i += 2
        elif args[i] == "--pages" and i + 1 < len(args):
            pages = int(args[i + 1])
            i += 2
        elif args[i] == "--sitemap":
            sitemap = True
            i += 1
        else:
            i += 1

    body = {"url": url, "max_depth": depth, "max_pages": pages}
    if sitemap:
        body["use_sitemap"] = True

    result = api("crawl", body)
    job_id = result.get("job_id", "")
    print(f"Crawl started: {job_id}")
    print(f"Check status: python3 scripts/webclaw.py crawl-status {job_id}")


def cmd_crawl_status(args):
    job_id = args[0]
    result = api_get(f"crawl/{job_id}")
    print(json.dumps(result, indent=2))


def cmd_map(args):
    url = args[0]
    result = api("map", {"url": url})
    count = result.get("count", 0)
    print(f"Found {count} URLs:")
    for u in result.get("urls", []):
        print(f"  {u}")


def cmd_endpoints(args):
    url = args[0]
    third_party = False
    max_bundles = None

    i = 1
    while i < len(args):
        if args[i] == "--third-party":
            third_party = True
            i += 1
        elif args[i] == "--max-bundles" and i + 1 < len(args):
            max_bundles = int(args[i + 1])
            i += 2
        else:
            i += 1

    body = {"url": url}
    if third_party:
        body["include_third_party"] = True
    if max_bundles is not None:
        body["max_bundles"] = max_bundles

    result = api("endpoints", body)
    eps = result.get("endpoints", [])
    print(
        f"Found {result.get('endpoint_count', len(eps))} endpoints "
        f"({result.get('bundles_scanned', 0)} bundles scanned):"
    )
    for ep in eps:
        scope = "1st" if ep.get("first_party") else "3rd"
        print(f"  [{ep.get('kind', '?')}] [{scope}] {ep.get('value', '')}  <- {ep.get('source', '?')}")
    hosts = result.get("hosts", [])
    if hosts:
        print(f"Hosts: {', '.join(hosts)}")
    if result.get("truncated"):
        print("(truncated: more bundles existed than --max-bundles allowed)")


def cmd_batch(args):
    urls = []
    fmt = "markdown"
    i = 0
    while i < len(args):
        if args[i] in ("--format", "-f") and i + 1 < len(args):
            fmt = args[i + 1]
            i += 2
        else:
            urls.append(args[i])
            i += 1

    result = api("batch", {"urls": urls, "formats": [fmt]})
    for item in result.get("results", []):
        url = item.get("url", "?")
        if item.get("error"):
            print(f"FAIL {url}: {item['error']}")
        else:
            content = item.get(fmt) or item.get("markdown") or ""
            print(f"--- {url} ({len(content)} chars) ---")
            print(content[:500])
            if len(content) > 500:
                print(f"  ... ({len(content) - 500} more chars)")
            print()


def cmd_extract(args):
    url = args[0]
    prompt = None
    schema = None

    i = 1
    while i < len(args):
        if args[i] == "--prompt" and i + 1 < len(args):
            prompt = args[i + 1]
            i += 2
        elif args[i] == "--schema" and i + 1 < len(args):
            schema = json.loads(args[i + 1])
            i += 2
        else:
            i += 1

    body = {"url": url}
    if schema:
        body["schema"] = schema
    elif prompt:
        body["prompt"] = prompt
    else:
        print("Error: --prompt or --schema required", file=sys.stderr)
        sys.exit(1)

    result = api("extract", body)
    print(json.dumps(result.get("data", result), indent=2))


def cmd_summarize(args):
    url = args[0]
    sentences = None

    i = 1
    while i < len(args):
        if args[i] == "--sentences" and i + 1 < len(args):
            sentences = int(args[i + 1])
            i += 2
        else:
            i += 1

    body = {"url": url}
    if sentences:
        body["max_sentences"] = sentences

    result = api("summarize", body)
    print(result.get("summary", json.dumps(result, indent=2)))


def cmd_diff(args):
    url = args[0]
    prev_file = None

    i = 1
    while i < len(args):
        if args[i] == "--previous" and i + 1 < len(args):
            prev_file = args[i + 1]
            i += 2
        else:
            i += 1

    if not prev_file:
        print("Error: --previous <file.json> required", file=sys.stderr)
        sys.exit(1)

    with open(prev_file) as f:
        previous = json.load(f)

    result = api("diff", {"url": url, "previous": previous})
    print(json.dumps(result, indent=2))


def cmd_brand(args):
    url = args[0]
    result = api("brand", {"url": url})
    print(json.dumps(result.get("brand", result), indent=2))


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]
    args = sys.argv[2:]

    commands = {
        "scrape": cmd_scrape,
        "crawl": cmd_crawl,
        "crawl-status": cmd_crawl_status,
        "map": cmd_map,
        "endpoints": cmd_endpoints,
        "batch": cmd_batch,
        "extract": cmd_extract,
        "summarize": cmd_summarize,
        "diff": cmd_diff,
        "brand": cmd_brand,
    }

    fn = commands.get(cmd)
    if not fn:
        print(f"Unknown command: {cmd}")
        print(f"Available: {', '.join(commands.keys())}")
        sys.exit(1)

    fn(args)


if __name__ == "__main__":
    main()
