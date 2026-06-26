#!/usr/bin/env python3
"""Lightweight URL uptime checker with response time monitoring and alerting."""

import argparse
import json
import ssl
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_TIMEOUT = 10
DEFAULT_INTERVAL = 60
DEFAULT_EXPECTED_STATUS = 200
HISTORY_FILE = "uptime_history.json"


def check_url(url: str, timeout: float = DEFAULT_TIMEOUT, method: str = "GET",
              expected_status: int = DEFAULT_EXPECTED_STATUS, verify_ssl: bool = True,
              headers: dict | None = None, follow_redirects: bool = True) -> dict:
    """Check a URL and return status information."""
    result = {
        "url": url,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": None,
        "response_time_ms": None,
        "error": None,
        "up": False,
        "ssl_valid": None,
        "redirect_url": None,
    }

    req_headers = {"User-Agent": "UptimeChecker/1.0"}
    if headers:
        req_headers.update(headers)

    request = urllib.request.Request(url, method=method, headers=req_headers)

    # SSL context
    ctx = None
    if url.startswith("https://"):
        ctx = ssl.create_default_context()
        if not verify_ssl:
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE

    start = time.monotonic()
    try:
        if not follow_redirects:
            # Build opener without redirect handler
            class NoRedirect(urllib.request.HTTPRedirectHandler):
                def redirect_request(self, req, fp, code, msg, hdrs, newurl):
                    result["redirect_url"] = newurl
                    return None
            opener = urllib.request.build_opener(NoRedirect, urllib.request.HTTPSHandler(context=ctx) if ctx else urllib.request.HTTPHandler())
            response = opener.open(request, timeout=timeout)
        else:
            response = urllib.request.urlopen(request, timeout=timeout, context=ctx)

        elapsed = (time.monotonic() - start) * 1000
        result["status"] = response.status
        result["response_time_ms"] = round(elapsed, 1)
        result["up"] = response.status == expected_status

        if url.startswith("https://") and verify_ssl:
            result["ssl_valid"] = True

        if response.url != url:
            result["redirect_url"] = response.url

    except urllib.error.HTTPError as e:
        elapsed = (time.monotonic() - start) * 1000
        result["status"] = e.code
        result["response_time_ms"] = round(elapsed, 1)
        result["up"] = e.code == expected_status
        result["error"] = str(e.reason)

    except ssl.SSLError as e:
        elapsed = (time.monotonic() - start) * 1000
        result["response_time_ms"] = round(elapsed, 1)
        result["error"] = f"SSL Error: {e}"
        result["ssl_valid"] = False

    except urllib.error.URLError as e:
        elapsed = (time.monotonic() - start) * 1000
        result["response_time_ms"] = round(elapsed, 1)
        result["error"] = str(e.reason)

    except Exception as e:
        elapsed = (time.monotonic() - start) * 1000
        result["response_time_ms"] = round(elapsed, 1)
        result["error"] = str(e)

    return result


def check_multiple(urls: list[str], **kwargs) -> list[dict]:
    """Check multiple URLs sequentially."""
    return [check_url(url, **kwargs) for url in urls]


def format_text(results: list[dict]) -> str:
    """Format check results as human-readable text."""
    lines = []
    max_url_len = max(len(r["url"]) for r in results) if results else 20
    col = min(max_url_len, 50)

    lines.append(f"{'URL':<{col}} {'STATUS':<8} {'TIME':<10} {'RESULT'}")
    lines.append("-" * (col + 35))

    for r in results:
        url_display = r["url"][:col]
        status = str(r["status"]) if r["status"] else "ERR"
        time_ms = f"{r['response_time_ms']}ms" if r["response_time_ms"] is not None else "N/A"
        icon = "UP" if r["up"] else "DOWN"

        line = f"{url_display:<{col}} {status:<8} {time_ms:<10} {icon}"
        if r["error"]:
            line += f"  ({r['error'][:40]})"
        if r["redirect_url"]:
            line += f"  → {r['redirect_url'][:40]}"
        lines.append(line)

    # Summary
    up_count = sum(1 for r in results if r["up"])
    lines.append("")
    lines.append(f"Summary: {up_count}/{len(results)} endpoints UP")
    if results:
        avg_time = sum(r["response_time_ms"] for r in results if r["response_time_ms"]) / max(
            sum(1 for r in results if r["response_time_ms"]), 1
        )
        lines.append(f"Average response time: {avg_time:.0f}ms")

    return "\n".join(lines)


def load_history(path: str) -> list:
    """Load check history from file."""
    p = Path(path)
    if p.exists():
        with open(p) as f:
            return json.load(f)
    return []


def save_history(path: str, history: list):
    """Save check history to file."""
    with open(path, "w") as f:
        json.dump(history, f, indent=2)


def summarize_history(path: str, url: str | None = None) -> str:
    """Summarize check history."""
    history = load_history(path)
    if not history:
        return "No history found."

    if url:
        history = [h for h in history if h["url"] == url]
        if not history:
            return f"No history found for {url}"

    lines = []
    # Group by URL
    urls = {}
    for h in history:
        u = h["url"]
        if u not in urls:
            urls[u] = []
        urls[u].append(h)

    for u, checks in urls.items():
        up_count = sum(1 for c in checks if c["up"])
        total = len(checks)
        uptime_pct = (up_count / total * 100) if total > 0 else 0
        avg_time = sum(c["response_time_ms"] for c in checks if c["response_time_ms"]) / max(
            sum(1 for c in checks if c["response_time_ms"]), 1
        )
        lines.append(f"{u}")
        lines.append(f"  Checks: {total} | Uptime: {uptime_pct:.1f}% | Avg response: {avg_time:.0f}ms")
        # Last 5 checks
        recent = checks[-5:]
        for c in recent:
            status_icon = "UP" if c["up"] else "DOWN"
            lines.append(f"  [{c['timestamp'][:19]}] {status_icon} {c.get('status', 'ERR')} {c.get('response_time_ms', 'N/A')}ms")
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Lightweight URL uptime checker with response time monitoring",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  %(prog)s https://example.com
  %(prog)s https://api.example.com https://example.com --format json
  %(prog)s https://example.com --expected-status 301
  %(prog)s --urls-file urls.txt
  %(prog)s https://example.com --save --history-file checks.json
  %(prog)s --history --history-file checks.json
  %(prog)s https://example.com --no-verify-ssl --timeout 5
""",
    )
    parser.add_argument("urls", nargs="*", help="URLs to check")
    parser.add_argument("--urls-file", help="File with one URL per line")
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT, help=f"Timeout in seconds (default: {DEFAULT_TIMEOUT})")
    parser.add_argument("--expected-status", type=int, default=DEFAULT_EXPECTED_STATUS, help=f"Expected HTTP status (default: {DEFAULT_EXPECTED_STATUS})")
    parser.add_argument("--method", default="GET", choices=["GET", "HEAD", "POST", "OPTIONS"], help="HTTP method (default: GET)")
    parser.add_argument("--no-verify-ssl", action="store_true", help="Skip SSL certificate verification")
    parser.add_argument("--no-follow-redirects", action="store_true", help="Don't follow redirects")
    parser.add_argument("--header", action="append", help="Add custom header (format: Key:Value)")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format (default: text)")
    parser.add_argument("--save", action="store_true", help="Save results to history file")
    parser.add_argument("--history", action="store_true", help="Show history summary")
    parser.add_argument("--history-file", default=HISTORY_FILE, help=f"History file path (default: {HISTORY_FILE})")

    args = parser.parse_args()

    # Show history
    if args.history:
        url_filter = args.urls[0] if args.urls else None
        print(summarize_history(args.history_file, url_filter))
        sys.exit(0)

    # Collect URLs
    urls = list(args.urls)
    if args.urls_file:
        try:
            with open(args.urls_file) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        urls.append(line)
        except FileNotFoundError:
            print(f"Error: File not found: {args.urls_file}", file=sys.stderr)
            sys.exit(1)

    if not urls:
        parser.print_help()
        sys.exit(1)

    # Parse headers
    custom_headers = {}
    if args.header:
        for h in args.header:
            if ":" in h:
                key, value = h.split(":", 1)
                custom_headers[key.strip()] = value.strip()

    # Run checks
    results = check_multiple(
        urls,
        timeout=args.timeout,
        method=args.method,
        expected_status=args.expected_status,
        verify_ssl=not args.no_verify_ssl,
        headers=custom_headers if custom_headers else None,
        follow_redirects=not args.no_follow_redirects,
    )

    # Save to history
    if args.save:
        history = load_history(args.history_file)
        history.extend(results)
        # Keep last 10000 entries
        if len(history) > 10000:
            history = history[-10000:]
        save_history(args.history_file, history)

    # Output
    if args.format == "json":
        print(json.dumps(results, indent=2))
    else:
        print(format_text(results))

    # Exit code: 0 if all up, 1 if any down
    if not all(r["up"] for r in results):
        sys.exit(1)


if __name__ == "__main__":
    main()
