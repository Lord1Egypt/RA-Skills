#!/usr/bin/env python3
"""
Search harvester — rotate Tor exit nodes, query engines, harvest candidate
URLs, dedupe, score, export markdown. Privacy-preserving candidate discovery
for link building (server IP never contacts the engine directly).

SAFETY (v1.0.1):
  * Consent gate: refuses to run non-interactively without --yes. Pass --yes
    ONLY after the user has explicitly consented to routing queries through
    the Tor network (queries are visible to exit operators).
  * --out never overwrites an existing file without --force.
  * Queries and harvested URLs are written only to the explicit --out path;
    treat the report as sensitive prospecting data.

Usage:
  python3 search-harvester.py "submit your company" "add your company" --niche "directory" --yes
  python3 search-harvester.py --queries-file queries.txt --engine marginalia --max-rotations 4 --yes

Requirements: tor running with SOCKSPort 127.0.0.1:19050 + ControlPort 127.0.0.1:19051
(see SKILL.md setup section). Python stdlib only.
"""
import argparse
import html as html_mod
import json
import os
import re
import socket
import subprocess
import sys
import time
import urllib.parse
from datetime import datetime

SOCKS = ("127.0.0.1", 19050)
CONTROL = ("127.0.0.1", 19051)
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")
ROTATE_SLEEP = 12  # seconds to let new circuit establish
RETRY_SLEEP = 5


def rotate_tor():
    """Signal NEWNYM on the control port to get a fresh exit node."""
    try:
        s = socket.create_connection(CONTROL, timeout=5)
        s.sendall(b"AUTHENTICATE\r\nSIGNAL NEWNYM\r\nQUIT\r\n")
        s.close()
        time.sleep(ROTATE_SLEEP)
        return True
    except Exception as e:
        print(f"[warn] rotate failed: {e}")
        return False


def current_ip():
    out = subprocess.run(
        ["curl", "-s", "-m", "25", "--socks5-hostname", f"{SOCKS[0]}:{SOCKS[1]}",
         "https://api.ipify.org"],
        capture_output=True, text=True)
    return out.stdout.strip()


def fetch(url, timeout=30):
    """Fetch a URL through the Tor SOCKS proxy via curl. Returns (code, body)."""
    out = subprocess.run(
        ["curl", "-s", "-m", str(timeout), "-L", "--socks5-hostname",
         f"{SOCKS[0]}:{SOCKS[1]}", "-A", UA, "-w", "\n%{http_code}", url],
        capture_output=True)
    raw = out.stdout
    # Non-UTF8 bytes (binary, latin-1, gzip garbage) must not crash the run
    body = raw.decode("utf-8", errors="replace")
    parts = body.rsplit("\n", 1)
    code = parts[1].strip() if len(parts) > 1 else "000"
    return code, parts[0] if parts else ""


def harvest_ddg(query):
    """Query html.duckduckgo.com. Returns list of (title, url)."""
    q = urllib.parse.quote(query)
    code, body = fetch(f"https://html.duckduckgo.com/html/?q={q}")
    if code != "200":
        return None
    links = re.findall(r'href="//duckduckgo\.com/l/\?uddg=([^"]+)"', body)
    titles = re.findall(r'class="result__a"[^>]*>\s*([^<]+?)\s*</a>', body)
    results = []
    for l, t in zip(links, titles):
        url = html_mod.unescape(urllib.parse.unquote(l)).split("&rut=")[0]
        results.append((html_mod.unescape(t).strip(), url))
    return results if results else []


def harvest_marginalia(query):
    """Query search.marginalia.nu. Returns list of (title, url)."""
    q = urllib.parse.quote(query)
    code, body = fetch(f"https://search.marginalia.nu/search?query={q}")
    if code != "200":
        return None
    results = []
    seen = set()
    for url, txt in re.findall(r'<a[^>]+href="(https?://[^"]+)"[^>]*>(.*?)</a>', body):
        txt = re.sub(r"<[^>]+>", "", txt).strip()
        if not txt or url in seen:
            continue
        if any(x in url for x in ["marginalia", "github.com/Marginalia", "creativecommons"]):
            continue
        seen.add(url)
        results.append((txt, url))
    return results


ENGINES = {"ddg": harvest_ddg, "marginalia": harvest_marginalia}


def triage(url):
    """Quick liveness check via Tor. Returns 'alive' | 'dead' | 'cf' | 'unknown'."""
    code, body = fetch(url, timeout=20)
    if code in ("000", "526"):
        return "dead"
    if code == "403":
        if "Just a moment" in body or "cloudflare" in body.lower():
            return "cf"  # alive but Cloudflare-walled
        return "alive"
    if code == "200":
        # parked detection
        low = body.lower()
        if any(sig in low for sig in ["forsale.godaddy.com", "click here to buy", "/lander",
                                      "registered at namecheap", "hugedomains"]):
            return "dead"  # parked domain
        if "just a moment" in low or "performing security verification" in low:
            return "cf"
        return "alive"
    return "unknown"


def confirm_plan(queries, engine, yes):
    """Print the privacy warning and require consent before any Tor query."""
    print("⚠️  You are about to send %d search query(ies) through the Tor network." % len(queries))
    print("    Queries and harvested URLs are visible to Tor exit operators.")
    print("    Do NOT route sensitive, personal, or client-identifying queries.")
    print("    Automated queries may violate engine ToS — keep volume low and rate-limited.")
    if yes:
        return
    if sys.stdin.isatty():
        ans = input("Type 'yes' to continue: ").strip().lower()
        if ans != "yes":
            sys.exit("aborted by user (no consent)")
    else:
        sys.exit("Refusing to run non-interactively without --yes. "
                 "Pass --yes ONLY after the user has explicitly consented to Tor routing.")


def main():
    ap = argparse.ArgumentParser(description="Tor-rotating search harvester (privacy-preserving candidate discovery)")
    ap.add_argument("queries", nargs="*", help="search queries")
    ap.add_argument("--queries-file", help="file with one query per line")
    ap.add_argument("--engine", default="ddg", choices=list(ENGINES.keys()))
    ap.add_argument("--max-rotations", type=int, default=4,
                    help="rotations before giving up on a query")
    ap.add_argument("--triage", action="store_true", help="liveness-check harvested URLs")
    ap.add_argument("--out", default=None, help="output markdown file")
    ap.add_argument("--yes", action="store_true",
                    help="confirm consent to Tor routing (use only after the user agrees)")
    ap.add_argument("--force", action="store_true",
                    help="overwrite an existing --out file")
    args = ap.parse_args()

    queries = list(args.queries)
    if args.queries_file:
        with open(args.queries_file) as f:
            queries += [l.strip() for l in f if l.strip()]
    if not queries:
        queries = ['"submit your company" directory', '"add your company" free directory']

    confirm_plan(queries, args.engine, args.yes)

    harvest = ENGINES[args.engine]
    all_results = {}  # url -> {"title":..., "engine":..., "query":...}
    start_ip = current_ip()
    print(f"[*] start exit IP: {start_ip}")

    for qi, query in enumerate(queries):
        print(f"[*] query {qi+1}/{len(queries)}: {query}")
        if qi > 0:
            # DDG blocks a second query from the SAME exit — always rotate between queries
            rotate_tor()
        results = None
        for rot in range(args.max_rotations + 1):
            if rot > 0:
                rotate_tor()
            ip = current_ip()
            results = harvest(query)
            if results is None:
                print(f"    rotation {rot}: exit={ip} -> blocked/error, rotating")
                continue
            if not results:
                print(f"    rotation {rot}: exit={ip} -> 200 but 0 results, rotating")
                continue
            print(f"    rotation {rot}: exit={ip} -> {len(results)} results")
            break
        if not results:
            print(f"    !! gave up after {args.max_rotations} rotations")
            continue
        for title, url in results:
            if url not in all_results:
                all_results[url] = {"title": title, "engine": args.engine, "query": query}
        time.sleep(RETRY_SLEEP)  # pacing between queries

    print(f"\n[=] harvested {len(all_results)} unique URLs")

    # Triage
    if args.triage:
        for i, (url, meta) in enumerate(all_results.items()):
            status = triage(url)
            meta["status"] = status
            print(f"    [{status}] {url}")
            if i % 5 == 4:
                time.sleep(2)

    # Export
    lines = [f"# Search Harvest — {datetime.now().isoformat(timespec='minutes')}",
             f"\nEngine: {args.engine} | Queries: {len(queries)} | Unique URLs: {len(all_results)}\n"]
    ranked = sorted(all_results.items(),
                    key=lambda kv: 0 if kv[1].get("status") == "alive" else
                    (1 if kv[1].get("status") == "cf" else 2))
    for i, (url, meta) in enumerate(ranked, 1):
        status = meta.get("status", "unknown")
        lines.append(f"{i}. **{meta['title'][:70]}** — {url} [{status}] (q: {meta['query'][:40]})")
    report = "\n".join(lines)
    print("\n" + report)
    if args.out:
        if os.path.exists(args.out) and not args.force:
            sys.exit(f"error: {args.out} already exists — pass --force to overwrite it")
        with open(args.out, "w") as f:
            f.write(report)
        print(f"\n[=] saved to {args.out}")
        print("    ⚠️  This file contains your queries and harvested URLs — review before sharing.")


if __name__ == "__main__":
    main()
