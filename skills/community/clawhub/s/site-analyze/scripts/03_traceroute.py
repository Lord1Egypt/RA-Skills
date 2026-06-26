#!/usr/bin/env python3
"""
03_traceroute.py - traceroute 并对每一跳查询 IP 归属
用法: python3 03_traceroute.py <ip_or_domain> [--max-hops 20] [--json]
     python3 03_traceroute.py --parse-text  (从 stdin 读取已有 traceroute 输出)
"""
import subprocess, sys, json, re
from concurrent.futures import ThreadPoolExecutor, as_completed
import importlib.util, os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def load_ip_info():
    spec = importlib.util.spec_from_file_location("ip_info", os.path.join(SCRIPT_DIR, "02_ip_info.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def run_traceroute(target, max_hops=20):
    """执行 traceroute，返回原始输出"""
    try:
        result = subprocess.run(
            ["traceroute", "-n", "-m", str(max_hops), target],
            capture_output=True, text=True, timeout=120
        )
        return result.stdout
    except subprocess.TimeoutExpired:
        return ""
    except Exception as e:
        return f"ERROR: {e}"

def parse_traceroute(raw_output):
    """解析 traceroute 输出，返回 hops 列表"""
    hops = []
    # 跳过第一行（header）
    lines = raw_output.strip().splitlines()
    for line in lines[1:]:
        # 例: "  5  10.200.16.177  2.493 ms * 2.261 ms"
        m = re.match(r'\s*(\d+)\s+(.*)', line)
        if not m:
            continue
        hop_num = int(m.group(1))
        rest = m.group(2)

        # 提取所有 IP（可能有多个，ECMP 路由）
        ips = list(dict.fromkeys(re.findall(r'(\d+\.\d+\.\d+\.\d+)', rest)))

        # 提取所有延迟
        latencies = re.findall(r'(\d+\.\d+)\s*ms', rest)
        latencies = [float(x) for x in latencies]

        is_timeout = all(p.strip() == '*' for p in rest.split() if p.strip() in ('*',)) and not ips

        hops.append({
            "hop": hop_num,
            "ips": ips,
            "latencies_ms": latencies,
            "avg_ms": round(sum(latencies) / len(latencies), 3) if latencies else None,
            "timeout": len(ips) == 0,
            "raw": line.strip()
        })
    return hops

def enrich_hops(hops):
    """对所有唯一公网 IP 批量查询归属"""
    ip_mod = load_ip_info()
    import ipaddress

    all_ips = []
    for hop in hops:
        for ip in hop.get("ips", []):
            try:
                if not ipaddress.ip_address(ip).is_private:
                    all_ips.append(ip)
            except:
                pass

    unique_ips = list(dict.fromkeys(all_ips))
    if not unique_ips:
        return {}

    return ip_mod.run(unique_ips, as_json=False) if False else \
           ip_mod.run.__wrapped__(unique_ips) if hasattr(ip_mod.run, '__wrapped__') else \
           _batch_query(ip_mod, unique_ips)

def _batch_query(ip_mod, ips):
    return ip_mod.run(ips, as_json=False) or {}

def run(target, max_hops=20, as_json=False, parse_stdin=False):
    if parse_stdin:
        raw = sys.stdin.read()
    else:
        print(f"[traceroute] Running traceroute to {target} (max {max_hops} hops)...", file=sys.stderr)
        raw = run_traceroute(target, max_hops)

    if not raw or raw.startswith("ERROR"):
        print(f"Traceroute failed: {raw}")
        return {}

    hops = parse_traceroute(raw)

    # 批量查询所有跳的 IP 归属
    print(f"[traceroute] Querying IP info for {sum(len(h['ips']) for h in hops)} IPs...", file=sys.stderr)
    ip_mod = load_ip_info()
    all_public_ips = []
    import ipaddress
    for hop in hops:
        for ip in hop.get("ips", []):
            try:
                if not ipaddress.ip_address(ip).is_private:
                    all_public_ips.append(ip)
            except:
                pass
    unique_public = list(dict.fromkeys(all_public_ips))
    ip_info_map = ip_mod.run(unique_public, as_json=False) if unique_public else {}
    # run() prints output; re-run silently for data
    import io, contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        ip_info_map = ip_mod.run(unique_public, as_json=False) if unique_public else {}

    # 富化每一跳
    for hop in hops:
        hop["ip_info"] = []
        for ip in hop.get("ips", []):
            info = ip_info_map.get(ip, {})
            hop["ip_info"].append({
                "ip": ip,
                "private": info.get("private", False),
                "country": info.get("country"),
                "city": info.get("city"),
                "org": info.get("org") or info.get("isp"),
                "as": info.get("as"),
            })

    result = {
        "target": target,
        "hops": hops,
        "raw": raw
    }

    if as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"\n=== Traceroute: {target} ===\n")
        for hop in hops:
            hop_n = hop["hop"]
            if hop["timeout"]:
                print(f"  {hop_n:2d}  * * * (timeout)")
                continue
            latency_str = f"{hop['avg_ms']}ms" if hop['avg_ms'] else "?ms"
            for i, ip in enumerate(hop["ips"]):
                info = hop["ip_info"][i] if i < len(hop["ip_info"]) else {}
                if info.get("private"):
                    loc = "内网"
                    org = ""
                else:
                    loc_parts = [x for x in [info.get("country"), info.get("city")] if x]
                    loc = " · ".join(loc_parts) or "?"
                    org = info.get("org") or info.get("as") or ""
                prefix = f"  {hop_n:2d}" if i == 0 else "    "
                lat_str = latency_str if i == 0 else ""
                print(f"  {hop_n:2d}  {ip:20s}  {lat_str:10s}  {loc}  {org}")
        print()

    return result

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("target", nargs="?")
    parser.add_argument("--max-hops", type=int, default=20)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--parse-text", action="store_true", help="从 stdin 解析已有 traceroute 文本")
    args = parser.parse_args()

    if args.parse_text:
        run(target="(stdin)", max_hops=args.max_hops, as_json=args.json, parse_stdin=True)
    elif args.target:
        run(args.target, max_hops=args.max_hops, as_json=args.json)
    else:
        print("Usage: python3 03_traceroute.py <target> [--max-hops 20] [--json]")
        print("       python3 03_traceroute.py --parse-text < traceroute_output.txt")
        sys.exit(1)
