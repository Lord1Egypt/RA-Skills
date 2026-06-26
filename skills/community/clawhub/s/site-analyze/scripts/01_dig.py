#!/usr/bin/env python3
"""
01_dig.py - DNS 查询（同时用国内/国外 DNS，失败自动回退 DoH）
用法: python3 01_dig.py <domain> [--json]
输出: 各 DNS 服务器返回的 A/AAAA 记录 + TTL

策略:
  1. 优先用 dig 直查各 DNS（UDP 53）
  2. 若 dig 全部返回空（UDP 被封），自动回退到 DNS over HTTPS (DoH)
     - 国内: alidns DoH (dns.alidns.com)
     - 国外: Google DoH (dns.google) + Cloudflare DoH (cloudflare-dns.com)
"""
import subprocess, sys, json, re, requests
from concurrent.futures import ThreadPoolExecutor, as_completed

DNS_SERVERS = {
    "alidns_1":  "223.5.5.5",
    "alidns_2":  "223.6.6.6",
    "google_1":  "8.8.8.8",
    "google_2":  "8.8.4.4",
}

# DoH 端点配置
DOH_SERVERS = {
    "alidns_doh":    "https://dns.alidns.com/resolve",
    "google_doh":    "https://dns.google/resolve",
    "cloudflare_doh":"https://cloudflare-dns.com/dns-query",
}

DOH_HEADERS = {"accept": "application/dns-json"}

# DNS 记录类型编号 → 名称
RTYPE_MAP = {1: "A", 28: "AAAA", 5: "CNAME", 15: "MX", 16: "TXT", 2: "NS"}


def dig_with_ttl(domain, dns_server, record_type="A"):
    """用 dig 查询，返回带 TTL 的记录列表"""
    try:
        result = subprocess.run(
            ["dig", f"@{dns_server}", domain, record_type,
             "+noall", "+answer", "+time=3", "+tries=1"],
            capture_output=True, text=True, timeout=8
        )
        records = []
        for line in result.stdout.strip().splitlines():
            line = line.strip()
            if not line or line.startswith(';'):
                continue
            parts = line.split()
            if len(parts) >= 5:
                records.append({
                    "name":  parts[0],
                    "ttl":   int(parts[1]) if parts[1].isdigit() else None,
                    "type":  parts[3],
                    "value": parts[4],
                    "via":   "udp",
                })
        return records
    except Exception:
        return []


def doh_query(domain, doh_url, record_type="A"):
    """DNS over HTTPS 查询，返回与 dig_with_ttl 相同格式的记录列表"""
    rtype_num = {"A": 1, "AAAA": 28, "CNAME": 5}.get(record_type, 1)
    try:
        r = requests.get(
            doh_url,
            params={"name": domain, "type": record_type},
            headers=DOH_HEADERS,
            timeout=8,
        )
        data = r.json()
        records = []
        for ans in data.get("Answer", []):
            rtype_name = RTYPE_MAP.get(ans.get("type"), str(ans.get("type")))
            records.append({
                "name":  ans.get("name", domain),
                "ttl":   ans.get("TTL"),
                "type":  rtype_name,
                "value": ans.get("data", "").rstrip("."),
                "via":   "doh",
            })
        return records
    except Exception:
        return []


def _has_real_records(results):
    """检查 dig 结果里有没有真实 A/AAAA 记录"""
    for name, data in results.items():
        for rtype, recs in data.get("records", {}).items():
            for r in recs:
                if r.get("type") in ("A", "AAAA"):
                    return True
    return False


def run(domain, as_json=False):
    results = {}

    # ── Phase 1: dig (UDP) ──────────────────────────────────────────────
    with ThreadPoolExecutor(max_workers=8) as pool:
        futures = {}
        for name, server in DNS_SERVERS.items():
            for rtype in ["A", "AAAA"]:
                futures[pool.submit(dig_with_ttl, domain, server, rtype)] = (name, server, rtype)

        for f in as_completed(futures):
            name, server, rtype = futures[f]
            if results.get(name) is None:
                results[name] = {"server": server, "records": {}, "method": "udp"}
            results[name]["records"][rtype] = f.result()

    # ── Phase 2: DoH 回退（当 UDP 全部返回空时）────────────────────────
    doh_used = False
    if not _has_real_records(results):
        print("[dig] UDP 查询返回空，回退到 DNS over HTTPS...", file=sys.stderr)
        doh_used = True

        with ThreadPoolExecutor(max_workers=6) as pool:
            futures = {}
            for name, url in DOH_SERVERS.items():
                for rtype in ["A", "AAAA"]:
                    futures[pool.submit(doh_query, domain, url, rtype)] = (name, url, rtype)

            for f in as_completed(futures):
                name, url, rtype = futures[f]
                if results.get(name) is None:
                    results[name] = {"server": url, "records": {}, "method": "doh"}
                results[name]["records"][rtype] = f.result()

    # ── 汇总唯一 IP ─────────────────────────────────────────────────────
    all_ips = set()
    all_cnames = []
    for name, data in results.items():
        for rtype, recs in data["records"].items():
            for r in recs:
                if r.get("type") in ("A", "AAAA"):
                    all_ips.add(r["value"])
                elif r.get("type") == "CNAME":
                    all_cnames.append(r["value"])

    output = {
        "domain":      domain,
        "unique_ips":  sorted(all_ips),
        "cnames":      list(dict.fromkeys(all_cnames)),
        "doh_used":    doh_used,
        "by_dns":      results,
    }

    if as_json:
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        method_tag = " [via DoH]" if doh_used else ""
        print(f"\n=== DNS 查询: {domain}{method_tag} ===")
        if output["cnames"]:
            print(f"CNAME 链: {' → '.join(output['cnames'])}")
        print(f"唯一 IP:  {', '.join(sorted(all_ips)) or '(none)'}\n")
        for name, data in sorted(results.items()):
            method = data.get("method", "")
            print(f"[{name}] {data['server']}  ({method})")
            for rtype in ["A", "AAAA", "CNAME"]:
                recs = data["records"].get(rtype, [])
                if recs:
                    for r in recs:
                        print(f"  {r['type']:6s} {r['value']:45s} TTL={r['ttl']}")
            print()

    return output


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("domain")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    run(args.domain, as_json=args.json)
