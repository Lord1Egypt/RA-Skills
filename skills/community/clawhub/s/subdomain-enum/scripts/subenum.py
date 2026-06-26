#!/usr/bin/env python3
"""
subenum.py — Enumerate subdomains for a domain using multiple techniques.

Uses DNS brute-forcing with a built-in wordlist, plus certificate transparency
logs via crt.sh API. No external tools or API keys required.

Usage:
    python3 subenum.py example.com
    python3 subenum.py example.com --wordlist custom.txt --threads 20
    python3 subenum.py example.com --json --output results.json
"""

import argparse
import concurrent.futures
import json
import socket
import sys
import time

try:
    import requests
except ImportError:
    print("ERROR: 'requests' is required. Install with: pip install requests", file=sys.stderr)
    sys.exit(1)

# Compact but effective default wordlist (top ~120 subdomains)
DEFAULT_WORDLIST = [
    "www", "mail", "ftp", "smtp", "pop", "imap", "webmail", "mx",
    "blog", "shop", "store", "app", "api", "dev", "staging", "test",
    "admin", "portal", "dashboard", "panel", "cms", "cdn", "static",
    "assets", "media", "img", "images", "files", "docs", "doc",
    "help", "support", "status", "monitor", "ns1", "ns2", "ns3",
    "dns", "dns1", "dns2", "vpn", "remote", "gateway", "proxy",
    "auth", "login", "sso", "oauth", "id", "accounts",
    "git", "gitlab", "github", "ci", "jenkins", "build", "deploy",
    "db", "database", "mysql", "postgres", "redis", "mongo", "elastic",
    "search", "es", "kibana", "grafana", "prometheus", "zabbix",
    "m", "mobile", "wap",
    "beta", "alpha", "demo", "sandbox", "preview", "staging2",
    "internal", "intranet", "extranet", "corp", "office",
    "cloud", "aws", "gcp", "azure",
    "chat", "slack", "teams", "jira", "confluence", "wiki",
    "video", "stream", "live", "tv",
    "payment", "pay", "billing", "checkout", "order", "orders",
    "analytics", "tracking", "events", "logs",
    "news", "press", "careers", "jobs", "hr",
    "api-v1", "api-v2", "api2", "v1", "v2",
    "web", "www2", "www3", "old", "new", "legacy",
    "crm", "erp", "inventory",
    "s3", "bucket", "backup", "archive",
    "relay", "edge", "node", "lb", "loadbalancer",
    "qa", "uat", "prod", "production",
]


def resolve_dns(subdomain: str, domain: str) -> dict | None:
    """Try to resolve a subdomain via DNS A/AAAA lookup."""
    fqdn = f"{subdomain}.{domain}"
    try:
        answers = socket.getaddrinfo(fqdn, None, socket.AF_UNSPEC, socket.SOCK_STREAM)
        ips = sorted(set(addr[4][0] for addr in answers))
        if ips:
            return {"subdomain": fqdn, "ips": ips, "source": "dns"}
    except (socket.gaierror, socket.herror, OSError):
        pass
    return None


def query_crtsh(domain: str, timeout: int) -> list:
    """Query crt.sh certificate transparency logs for subdomains."""
    results = []
    try:
        url = f"https://crt.sh/?q=%.{domain}&output=json"
        resp = requests.get(url, timeout=timeout, headers={
            "User-Agent": "SubdomainEnum/1.0 (OpenClaw skill)"
        })
        if resp.status_code == 200:
            data = resp.json()
            seen = set()
            for entry in data:
                name = entry.get("name_value", "")
                # Handle multi-line name values
                for n in name.split("\n"):
                    n = n.strip().lower()
                    if n.endswith(f".{domain}") or n == domain:
                        if n not in seen and "*" not in n:
                            seen.add(n)
                            results.append({"subdomain": n, "ips": [], "source": "crt.sh"})
    except Exception as e:
        print(f"  crt.sh query failed: {e}", file=sys.stderr)
    return results


def dns_bruteforce(domain: str, wordlist: list, threads: int, verbose: bool) -> list:
    """Brute-force subdomains via DNS resolution."""
    results = []
    total = len(wordlist)
    found = 0

    def check(sub):
        return resolve_dns(sub, domain)

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {executor.submit(check, sub): sub for sub in wordlist}
        for i, future in enumerate(concurrent.futures.as_completed(futures)):
            result = future.result()
            if result:
                results.append(result)
                found += 1
                if verbose:
                    print(f"  [{found}] {result['subdomain']} → {', '.join(result['ips'])}", file=sys.stderr)
            if verbose and (i + 1) % 50 == 0:
                print(f"  Progress: {i+1}/{total} checked, {found} found", file=sys.stderr)

    return results


def load_wordlist(path: str) -> list:
    """Load wordlist from file, one word per line."""
    words = []
    with open(path, "r") as f:
        for line in f:
            word = line.strip().lower()
            if word and not word.startswith("#"):
                words.append(word)
    return words


def print_report(domain: str, results: list):
    """Print human-readable results."""
    print(f"\n{'='*60}")
    print(f" Subdomain Enumeration: {domain}")
    print(f"{'='*60}")
    print(f" Found {len(results)} subdomains\n")

    # Group by source
    dns_results = [r for r in results if r["source"] == "dns"]
    ct_results = [r for r in results if r["source"] == "crt.sh"]

    if dns_results:
        print(f" DNS Brute-force ({len(dns_results)} found):")
        for r in sorted(dns_results, key=lambda x: x["subdomain"]):
            ips = ", ".join(r["ips"]) if r["ips"] else "no IP"
            print(f"   {r['subdomain']:40s} {ips}")

    if ct_results:
        print(f"\n Certificate Transparency ({len(ct_results)} found):")
        for r in sorted(ct_results, key=lambda x: x["subdomain"]):
            print(f"   {r['subdomain']}")

    # Unique subdomains summary
    all_subs = sorted(set(r["subdomain"] for r in results))
    print(f"\n All unique subdomains ({len(all_subs)}):")
    for s in all_subs:
        print(f"   {s}")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Enumerate subdomains for a domain using DNS brute-force and certificate transparency.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  %(prog)s example.com
  %(prog)s example.com --threads 20 --verbose
  %(prog)s example.com --wordlist custom.txt
  %(prog)s example.com --json --output results.json
  %(prog)s example.com --no-crtsh    # DNS only, skip certificate transparency
""",
    )
    parser.add_argument("domain", help="Target domain (e.g., example.com)")
    parser.add_argument("--wordlist", "-w", help="Custom wordlist file (one subdomain per line)")
    parser.add_argument("--threads", "-t", type=int, default=10, help="Concurrent DNS threads (default: 10)")
    parser.add_argument("--timeout", type=int, default=15, help="HTTP timeout for crt.sh (default: 15)")
    parser.add_argument("--no-crtsh", action="store_true", help="Skip certificate transparency lookup")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    parser.add_argument("--output", "-o", help="Write results to file")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show progress")

    args = parser.parse_args()

    domain = args.domain.lower().strip(".")
    if "://" in domain:
        domain = domain.split("://")[1].split("/")[0]

    print(f"Enumerating subdomains for {domain}...", file=sys.stderr)

    # Load wordlist
    if args.wordlist:
        words = load_wordlist(args.wordlist)
        print(f"  Loaded {len(words)} words from {args.wordlist}", file=sys.stderr)
    else:
        words = DEFAULT_WORDLIST
        print(f"  Using built-in wordlist ({len(words)} words)", file=sys.stderr)

    all_results = []

    # DNS brute-force
    print("  Running DNS brute-force...", file=sys.stderr)
    dns_results = dns_bruteforce(domain, words, args.threads, args.verbose)
    all_results.extend(dns_results)
    print(f"  DNS: {len(dns_results)} subdomains found", file=sys.stderr)

    # Certificate transparency
    if not args.no_crtsh:
        print("  Querying certificate transparency (crt.sh)...", file=sys.stderr)
        ct_results = query_crtsh(domain, args.timeout)
        # Deduplicate against DNS results
        dns_subs = set(r["subdomain"] for r in dns_results)
        ct_unique = [r for r in ct_results if r["subdomain"] not in dns_subs]
        all_results.extend(ct_unique)
        print(f"  crt.sh: {len(ct_results)} total, {len(ct_unique)} new", file=sys.stderr)

    print(f"  Total unique: {len(set(r['subdomain'] for r in all_results))}", file=sys.stderr)

    # Output
    if args.json:
        output = json.dumps(all_results, indent=2)
        if args.output:
            with open(args.output, "w") as f:
                f.write(output)
            print(f"  Results written to {args.output}", file=sys.stderr)
        else:
            print(output)
    else:
        print_report(domain, all_results)
        if args.output:
            with open(args.output, "w") as f:
                for r in sorted(all_results, key=lambda x: x["subdomain"]):
                    f.write(r["subdomain"] + "\n")
            print(f"Results written to {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
