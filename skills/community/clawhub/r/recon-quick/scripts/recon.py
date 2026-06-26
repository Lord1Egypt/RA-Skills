#!/usr/bin/env python3
"""
Recon Quick — Fast OSINT presets using bbot and nmap.
One-command recon workflows for bug bounty hunting.
"""

import argparse
import os
import subprocess
import sys
import json
from datetime import datetime


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def run_cmd(cmd, output_file=None, timeout=600):
    print(f"  → {' '.join(cmd[:4])}...", file=sys.stderr)
    try:
        if output_file:
            with open(output_file, "w") as f:
                result = subprocess.run(cmd, stdout=f, stderr=subprocess.PIPE, text=True, timeout=timeout)
        else:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print(f"  ⏰ Timeout: {cmd[0]}", file=sys.stderr)
        return False
    except FileNotFoundError:
        print(f"  ❌ Not found: {cmd[0]}", file=sys.stderr)
        return False


def bbot_subdomains(target, outdir, threads=10):
    """Subdomain enumeration via bbot."""
    scan_dir = os.path.join(outdir, "bbot-scan")
    run_cmd([
        "bbot", "-t", target,
        "-f", "subdomain-enum",
        "-o", scan_dir,
        "-y", "--silent"
    ], timeout=600)

    # Extract subdomains from bbot output
    subs_file = os.path.join(outdir, "subdomains.txt")
    subs = set()
    for fname in os.listdir(scan_dir) if os.path.isdir(scan_dir) else []:
        if "subdomain" in fname.lower() or "dns" in fname.lower():
            fpath = os.path.join(scan_dir, fname)
            if os.path.isfile(fpath):
                with open(fpath) as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#"):
                            subs.add(line)

    # Also try to parse bbot output.csv
    csv_file = os.path.join(scan_dir, "output.csv")
    if os.path.exists(csv_file):
        with open(csv_file) as f:
            for line in f:
                parts = line.strip().split(",")
                for p in parts:
                    if "." in p and target in p:
                        subs.add(p.strip())

    with open(subs_file, "w") as f:
        for s in sorted(subs):
            f.write(s + "\n")

    return subs_file


def nmap_ports(target, outdir, top_ports=100):
    """Quick port scan."""
    outfile = os.path.join(outdir, "ports.txt")
    run_cmd([
        "nmap", "-sV", "--top-ports", str(top_ports),
        "-oN", outfile, target
    ], timeout=300)
    return outfile


def nmap_subdomain_ports(subs_file, outdir, top_ports=100):
    """Port scan discovered subdomains."""
    outfile = os.path.join(outdir, "ports-all.txt")
    if not os.path.exists(subs_file):
        return None
    with open(subs_file) as f:
        targets = [line.strip() for line in f if line.strip()]
    if not targets:
        return None
    # Limit to 50 targets to avoid long scans
    targets = targets[:50]
    run_cmd([
        "nmap", "-sV", "--top-ports", str(top_ports),
        "-iL", "-", "-oN", outfile
    ] + targets, timeout=600)
    return outfile


def http_probe(subs_file, outdir):
    """Probe for live HTTP services."""
    hosts_file = os.path.join(outdir, "live-hosts.txt")
    if not os.path.exists(subs_file):
        return None
    run_cmd([
        "bbot", "-t", subs_file if os.path.exists(subs_file) else "",
        "-f", "web-basic",
        "-o", os.path.join(outdir, "web-scan"),
        "-y", "--silent"
    ], timeout=600)
    return hosts_file


def passive_recon(target, outdir):
    """Passive-only recon (DNS, certs, APIs)."""
    subs_file = os.path.join(outdir, "subdomains.txt")
    run_cmd([
        "bbot", "-t", target,
        "-f", "passive",
        "-o", os.path.join(outdir, "passive-scan"),
        "-y", "--silent"
    ], timeout=300)
    return subs_file


def main():
    parser = argparse.ArgumentParser(description="Recon Quick — Fast OSINT Presets")
    parser.add_argument("target", help="Target domain")
    parser.add_argument("--preset", choices=["subdomains", "ports", "web", "full", "passive"],
                        default="subdomains")
    parser.add_argument("--output", "-o", default="./recon-output")
    parser.add_argument("--json", action="store_true", dest="json_out")
    parser.add_argument("--threads", type=int, default=10)
    parser.add_argument("--proxy", help="Proxy URL")
    args = parser.parse_args()

    outdir = os.path.join(args.output, args.target)
    ensure_dir(outdir)

    start = datetime.now()
    print(f"\n🔍 Recon Quick — {args.preset} scan on {args.target}", file=sys.stderr)
    print(f"   Output: {outdir}\n", file=sys.stderr)

    results = {"target": args.target, "preset": args.preset, "start": start.isoformat()}

    if args.preset == "subdomains":
        results["subdomains"] = bbot_subdomains(args.target, outdir, args.threads)

    elif args.preset == "ports":
        results["ports"] = nmap_ports(args.target, outdir)

    elif args.preset == "web":
        subs = bbot_subdomains(args.target, outdir, args.threads)
        results["web"] = http_probe(subs, outdir)

    elif args.preset == "passive":
        results["subdomains"] = passive_recon(args.target, outdir)

    elif args.preset == "full":
        print("[1/4] Subdomain enumeration...", file=sys.stderr)
        subs = bbot_subdomains(args.target, outdir, args.threads)
        results["subdomains"] = subs

        print("[2/4] Port scanning...", file=sys.stderr)
        results["ports"] = nmap_subdomain_ports(subs, outdir)

        print("[3/4] HTTP probing...", file=sys.stderr)
        results["web"] = http_probe(subs, outdir)

        print("[4/4] Complete.", file=sys.stderr)

    elapsed = (datetime.now() - start).total_seconds()
    results["elapsed_seconds"] = elapsed
    results["end"] = datetime.now().isoformat()

    if args.json_out:
        print(json.dumps(results, indent=2))
    else:
        print(f"\n✅ Done in {elapsed:.1f}s", file=sys.stderr)
        print(f"   Output: {outdir}", file=sys.stderr)
        if os.path.exists(os.path.join(outdir, "subdomains.txt")):
            with open(os.path.join(outdir, "subdomains.txt")) as f:
                count = sum(1 for _ in f)
            print(f"   Subdomains found: {count}", file=sys.stderr)


if __name__ == "__main__":
    main()
