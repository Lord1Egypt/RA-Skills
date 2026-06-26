#!/usr/bin/env python3
"""uptimecheck — lightweight URL uptime monitor. Zero dependencies."""
import sys, json, time, urllib.request, urllib.error, os, argparse
from datetime import datetime, timezone
from pathlib import Path

DB = Path.home() / ".uptimecheck" / "checks.jsonl"

def check_url(url, timeout=10):
    start = time.monotonic()
    try:
        req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "uptimecheck/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            ms = round((time.monotonic() - start) * 1000)
            return {"url": url, "status": resp.status, "ms": ms, "ok": True, "ts": datetime.now(timezone.utc).isoformat()}
    except urllib.error.HTTPError as e:
        ms = round((time.monotonic() - start) * 1000)
        return {"url": url, "status": e.code, "ms": ms, "ok": e.code < 500, "ts": datetime.now(timezone.utc).isoformat()}
    except Exception as e:
        ms = round((time.monotonic() - start) * 1000)
        return {"url": url, "status": 0, "ms": ms, "ok": False, "error": str(e)[:200], "ts": datetime.now(timezone.utc).isoformat()}

def cmd_check(args):
    urls = args.urls
    if args.file:
        urls += [l.strip() for l in open(args.file) if l.strip() and not l.startswith("#")]
    results = []
    for url in urls:
        r = check_url(url, timeout=args.timeout)
        results.append(r)
        icon = "✅" if r["ok"] else "❌"
        status = r.get("error", r["status"])
        print(f"{icon} {r['ms']:>5}ms  {status:<6}  {url}")
    if args.save:
        DB.parent.mkdir(parents=True, exist_ok=True)
        with open(DB, "a") as f:
            for r in results:
                f.write(json.dumps(r) + "\n")
    down = [r for r in results if not r["ok"]]
    if down:
        print(f"\n⚠️  {len(down)}/{len(results)} endpoints DOWN")
        return 1
    print(f"\n✅ All {len(results)} endpoints UP")
    return 0

def cmd_history(args):
    if not DB.exists():
        print("No history. Run with --save first.")
        return
    lines = DB.read_text().strip().split("\n")
    entries = [json.loads(l) for l in lines[-args.limit:]]
    if args.url:
        entries = [e for e in entries if args.url in e["url"]]
    for e in entries:
        icon = "✅" if e.get("ok") else "❌"
        print(f"{icon} {e['ts'][:19]}  {e.get('ms',0):>5}ms  {e.get('status',0):<6}  {e['url']}")

def main():
    p = argparse.ArgumentParser(prog="uptimecheck", description="Lightweight URL uptime monitor")
    sub = p.add_subparsers(dest="cmd")
    
    c = sub.add_parser("check", help="Check URLs")
    c.add_argument("urls", nargs="*", help="URLs to check")
    c.add_argument("-f", "--file", help="File with URLs (one per line)")
    c.add_argument("-t", "--timeout", type=int, default=10)
    c.add_argument("--save", action="store_true", help="Save results to history")
    
    h = sub.add_parser("history", help="View check history")
    h.add_argument("--url", help="Filter by URL")
    h.add_argument("-n", "--limit", type=int, default=50)
    
    args = p.parse_args()
    if args.cmd == "check":
        sys.exit(cmd_check(args))
    elif args.cmd == "history":
        cmd_history(args)
    else:
        p.print_help()

if __name__ == "__main__":
    main()
