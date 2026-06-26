#!/usr/bin/env python3
"""Lightweight website monitor: uptime, change detection, content matching."""

import argparse
import difflib
import hashlib
import os
import re
import sys
import time

try:
    import requests
except ImportError:
    print("Error: requests required. Install with: pip3 install requests")
    sys.exit(1)


HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; WebsiteMonitor/1.0)"
}


def fetch_page(url, timeout=15):
    """Fetch a URL and return (status_code, text, response_time_ms)."""
    start = time.time()
    try:
        resp = requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
        elapsed = int((time.time() - start) * 1000)
        # Extract text content (strip HTML roughly)
        text = re.sub(r"<script[^>]*>.*?</script>", "", resp.text, flags=re.DOTALL)
        text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.DOTALL)
        text = re.sub(r"<[^>]+>", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        return resp.status_code, text, elapsed
    except requests.exceptions.Timeout:
        elapsed = int((time.time() - start) * 1000)
        return 0, "", elapsed
    except requests.exceptions.RequestException as e:
        elapsed = int((time.time() - start) * 1000)
        return -1, str(e), elapsed


def url_hash(url):
    return hashlib.md5(url.encode()).hexdigest()[:12]


def cmd_check(args):
    """Check if a site is up."""
    status, text, ms = fetch_page(args.url)
    if status == 200:
        print(f"✅ UP — {args.url} ({ms}ms, {len(text)} chars)")
        return 0
    elif status == 0:
        print(f"❌ TIMEOUT — {args.url} ({ms}ms)")
        return 2
    elif status == -1:
        print(f"❌ ERROR — {args.url}: {text}")
        return 2
    else:
        print(f"⚠️ HTTP {status} — {args.url} ({ms}ms)")
        return 1


def cmd_watch(args):
    """Monitor for changes vs last snapshot."""
    state_dir = args.state_dir or "/tmp/monitor-state"
    os.makedirs(state_dir, exist_ok=True)
    state_file = os.path.join(state_dir, f"{url_hash(args.url)}.txt")

    status, text, ms = fetch_page(args.url)
    if status != 200:
        print(f"❌ DOWN — {args.url} (HTTP {status}, {ms}ms)")
        return 2

    current_hash = hashlib.md5(text.encode()).hexdigest()

    if os.path.exists(state_file):
        with open(state_file) as f:
            old_text = f.read()
        old_hash = hashlib.md5(old_text.encode()).hexdigest()

        if current_hash == old_hash:
            print(f"✅ UNCHANGED — {args.url} ({ms}ms)")
            # Update state file
            with open(state_file, "w") as f:
                f.write(text)
            return 0
        else:
            print(f"🔄 CHANGED — {args.url} ({ms}ms)")
            # Show diff summary
            old_lines = old_text[:2000].splitlines()
            new_lines = text[:2000].splitlines()
            diff = list(difflib.unified_diff(old_lines, new_lines, lineterm="", n=1))
            for line in diff[:20]:
                print(f"  {line}")
            if len(diff) > 20:
                print(f"  ... ({len(diff) - 20} more diff lines)")
            # Update state
            with open(state_file, "w") as f:
                f.write(text)
            return 1
    else:
        print(f"📝 FIRST CHECK — {args.url} ({ms}ms, {len(text)} chars)")
        with open(state_file, "w") as f:
            f.write(text)
        return 0


def cmd_match(args):
    """Check for specific content pattern."""
    status, text, ms = fetch_page(args.url)
    if status != 200:
        print(f"❌ Cannot check — {args.url} (HTTP {status})")
        return 2

    if re.search(args.pattern, text, re.IGNORECASE):
        print(f"✅ FOUND — Pattern '{args.pattern}' found in {args.url}")
        return 0
    else:
        print(f"❌ NOT FOUND — Pattern '{args.pattern}' not in {args.url}")
        return 1


def cmd_batch(args):
    """Batch check from file."""
    with open(args.file) as f:
        urls = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    state_dir = args.state_dir or "/tmp/monitor-state"
    results = {"up": 0, "down": 0, "changed": 0}

    for url in urls:
        status, text, ms = fetch_page(url)
        if status != 200:
            print(f"❌ DOWN — {url} (HTTP {status}, {ms}ms)")
            results["down"] += 1
            continue

        os.makedirs(state_dir, exist_ok=True)
        state_file = os.path.join(state_dir, f"{url_hash(url)}.txt")
        current_hash = hashlib.md5(text.encode()).hexdigest()

        if os.path.exists(state_file):
            with open(state_file) as f:
                old_hash = hashlib.md5(f.read().encode()).hexdigest()
            if current_hash != old_hash:
                print(f"🔄 CHANGED — {url} ({ms}ms)")
                results["changed"] += 1
            else:
                results["up"] += 1
        else:
            print(f"📝 FIRST — {url} ({ms}ms)")
            results["up"] += 1

        with open(state_file, "w") as f:
            f.write(text)

    print(f"\nSummary: {results['up']} up, {results['changed']} changed, {results['down']} down")
    return 1 if results["down"] or results["changed"] else 0


def main():
    parser = argparse.ArgumentParser(description="Website Monitor")
    sub = parser.add_subparsers(dest="command")

    p_check = sub.add_parser("check", help="Check if a site is up")
    p_check.add_argument("url")

    p_watch = sub.add_parser("watch", help="Detect changes vs last snapshot")
    p_watch.add_argument("url")
    p_watch.add_argument("--state-dir", default="/tmp/monitor-state")

    p_match = sub.add_parser("match", help="Check for content pattern")
    p_match.add_argument("url")
    p_match.add_argument("--pattern", required=True)

    p_batch = sub.add_parser("batch", help="Batch check from file")
    p_batch.add_argument("file")
    p_batch.add_argument("--state-dir", default="/tmp/monitor-state")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    fn = {"check": cmd_check, "watch": cmd_watch, "match": cmd_match, "batch": cmd_batch}
    sys.exit(fn[args.command](args))


if __name__ == "__main__":
    main()
