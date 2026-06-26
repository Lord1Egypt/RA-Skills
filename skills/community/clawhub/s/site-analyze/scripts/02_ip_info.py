#!/usr/bin/env python3
"""
02_ip_info.py - 批量查询 IP 归属（ipinfo.io + ip-api.com 双源）
用法: python3 02_ip_info.py <ip1> [ip2 ip3 ...] [--json]
     echo '1.2.3.4\n5.6.7.8' | python3 02_ip_info.py --stdin [--json]
"""
import sys, json, requests
from concurrent.futures import ThreadPoolExecutor, as_completed

def query_ip_api(ip):
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}", timeout=6)
        d = r.json()
        if d.get("status") == "success":
            return {
                "source": "ip-api",
                "ip": ip,
                "country": d.get("country"),
                "country_code": d.get("countryCode"),
                "region": d.get("regionName"),
                "city": d.get("city"),
                "isp": d.get("isp"),
                "org": d.get("org"),
                "as": d.get("as"),
                "lat": d.get("lat"),
                "lon": d.get("lon"),
            }
    except Exception as e:
        pass
    return {"source": "ip-api", "ip": ip, "error": "failed"}

def query_ipinfo(ip):
    try:
        r = requests.get(f"https://ipinfo.io/{ip}/json", timeout=6)
        d = r.json()
        if "ip" in d:
            loc = d.get("loc", ",").split(",")
            return {
                "source": "ipinfo",
                "ip": ip,
                "country": d.get("country"),
                "region": d.get("region"),
                "city": d.get("city"),
                "org": d.get("org"),
                "hostname": d.get("hostname"),
                "lat": float(loc[0]) if loc[0] else None,
                "lon": float(loc[1]) if len(loc) > 1 and loc[1] else None,
            }
    except Exception as e:
        pass
    return {"source": "ipinfo", "ip": ip, "error": "failed"}

def merge_info(ip_api, ipinfo):
    """合并两个来源，ip-api 优先，ipinfo 补充"""
    merged = {"ip": ip_api.get("ip") or ipinfo.get("ip")}
    for key in ["country", "country_code", "region", "city", "isp", "org", "as", "lat", "lon", "hostname"]:
        val = ip_api.get(key) or ipinfo.get(key)
        if val is not None:
            merged[key] = val
    merged["_sources"] = {"ip_api": ip_api, "ipinfo": ipinfo}
    return merged

def is_private(ip):
    import ipaddress
    try:
        return ipaddress.ip_address(ip).is_private
    except:
        return False

def run(ips, as_json=False):
    results = {}

    # 过滤私有 IP
    public_ips = [ip for ip in ips if not is_private(ip)]
    private_ips = [ip for ip in ips if is_private(ip)]

    for ip in private_ips:
        results[ip] = {"ip": ip, "private": True, "note": "内网/私有地址"}

    with ThreadPoolExecutor(max_workers=min(len(public_ips) * 2, 20)) as pool:
        futures_api = {pool.submit(query_ip_api, ip): ip for ip in public_ips}
        futures_info = {pool.submit(query_ipinfo, ip): ip for ip in public_ips}

        api_results = {}
        info_results = {}

        for f in as_completed(futures_api):
            ip = futures_api[f]
            api_results[ip] = f.result()

        for f in as_completed(futures_info):
            ip = futures_info[f]
            info_results[ip] = f.result()

    for ip in public_ips:
        results[ip] = merge_info(
            api_results.get(ip, {"ip": ip, "error": "no data"}),
            info_results.get(ip, {"ip": ip, "error": "no data"})
        )

    if as_json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for ip, info in results.items():
            if info.get("private"):
                print(f"[{ip}] 私有地址")
                continue
            country = info.get("country", "?")
            city = info.get("city", "?")
            region = info.get("region", "?")
            org = info.get("org") or info.get("isp") or "?"
            asn = info.get("as", "")
            print(f"[{ip}]")
            print(f"  位置: {country} · {region} · {city}")
            print(f"  组织: {org}")
            if asn:
                print(f"  ASN:  {asn}")
            print()

    return results

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("ips", nargs="*")
    parser.add_argument("--stdin", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    ips = list(args.ips)
    if args.stdin:
        ips += [l.strip() for l in sys.stdin if l.strip()]

    if not ips:
        print("Usage: python3 02_ip_info.py <ip1> [ip2 ...] [--json]")
        sys.exit(1)

    run(ips, as_json=args.json)
