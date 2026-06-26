#!/usr/bin/env python3
"""
analyze.py - 站点综合分析主入口
用法: python3 analyze.py <domain_or_ip> [--json] [--no-traceroute] [--no-robots]

执行流程:
  Phase 1 (并发): dig + whois + robots.txt
  Phase 2 (串行): 对 dig 拿到的每个 IP 做 traceroute + ping
  Phase 3: 对 traceroute 每一跳查询 IP 归属
  Phase 4: 汇总输出站点画像
"""
import sys, json, os, time
from concurrent.futures import ThreadPoolExecutor, as_completed
import importlib.util

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def load_mod(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(SCRIPT_DIR, f"{name}.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def check_env():
    env_file = os.path.expanduser("~/.site-analyzer-env.json")
    if not os.path.exists(env_file):
        print("[setup] First run: probing network environment...", file=sys.stderr)
        os.system(f"bash {os.path.join(SCRIPT_DIR, '00_probe_env.sh')}")
    try:
        with open(env_file) as f:
            return json.load(f)
    except:
        return {}

def run(target, as_json=False, no_traceroute=False, no_robots=False, ping_ports=None):
    t0 = time.time()
    env = check_env()

    # 判断输入是 IP 还是域名
    import re, ipaddress
    is_ip = False
    try:
        ipaddress.ip_address(target)
        is_ip = True
    except:
        pass

    domain = target
    if target.startswith("http"):
        from urllib.parse import urlparse
        domain = urlparse(target).hostname

    report = {
        "target": target,
        "domain": domain,
        "is_ip": is_ip,
        "probe_host": {
            "ip": env.get("my_ip"),
            "country": env.get("country"),
            "city": env.get("city"),
            "isp": env.get("isp"),
        },
        "phases": {}
    }

    # ── Phase 1: 并发 dig + whois + robots ──────────────────────────────
    print(f"\n[Phase 1] dig / whois / robots (并发)...", file=sys.stderr)
    dig_mod    = load_mod("01_dig")
    whois_mod  = load_mod("04_whois")
    robots_mod = load_mod("06_robots")
    ip_mod     = load_mod("02_ip_info")

    import io, contextlib

    def silent(fn, *args, **kwargs):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            result = fn(*args, **kwargs)
        return result

    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = {}
        if not is_ip:
            futures["dig"] = pool.submit(silent, dig_mod.run, domain, False)
        futures["whois"] = pool.submit(silent, whois_mod.run, domain, False)
        if not no_robots and not is_ip:
            futures["robots"] = pool.submit(silent, robots_mod.run, domain, False)

        phase1 = {}
        for key, f in futures.items():
            try:
                phase1[key] = f.result()
            except Exception as e:
                phase1[key] = {"error": str(e)}

    report["phases"]["phase1"] = phase1

    # 拿到要探测的 IP 列表
    ips_to_probe = []
    if is_ip:
        ips_to_probe = [target]
        # 直接查归属
        ip_info_map = silent(ip_mod.run, [target], False)
        report["ip_info"] = ip_info_map
    else:
        dig_result = phase1.get("dig", {})
        ips_to_probe = dig_result.get("unique_ips", [])[:4]  # 最多取 4 个 IP
        if ips_to_probe:
            ip_info_map = silent(ip_mod.run, ips_to_probe, False)
            report["ip_info"] = ip_info_map

    print(f"  IPs to probe: {ips_to_probe}", file=sys.stderr)

    # ── Phase 2: traceroute + ping (对每个 IP) ──────────────────────────
    if ips_to_probe and not no_traceroute:
        print(f"\n[Phase 2] traceroute + ping...", file=sys.stderr)
        tr_mod   = load_mod("03_traceroute")
        ping_mod = load_mod("05_ping")

        probe_ip = ips_to_probe[0]  # traceroute 取第一个 IP（避免时间过长）
        ports = ping_ports or [80, 443]

        with ThreadPoolExecutor(max_workers=2) as pool:
            f_tr   = pool.submit(tr_mod.run, probe_ip, 20, False)
            f_ping = pool.submit(silent, ping_mod.run, probe_ip, 5, ports, False)

            try:
                tr_result = f_tr.result()
            except Exception as e:
                tr_result = {"error": str(e)}
            try:
                ping_result = f_ping.result()
            except Exception as e:
                ping_result = {"error": str(e)}

        report["phases"]["phase2"] = {
            "traceroute": tr_result,
            "ping": ping_result
        }

    # ── Phase 4: 汇总输出 ────────────────────────────────────────────────
    elapsed = round(time.time() - t0, 1)
    report["elapsed_sec"] = elapsed

    if as_json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        _print_report(report)

    return report

def _print_report(report):
    target = report["target"]
    probe = report["probe_host"]
    ip_info_map = report.get("ip_info", {})
    p1 = report["phases"].get("phase1", {})
    p2 = report["phases"].get("phase2", {})

    print(f"\n{'='*60}")
    print(f"  站点分析报告: {target}")
    print(f"  探测节点: {probe.get('ip')} ({probe.get('city')}, {probe.get('country')} · {probe.get('isp')})")
    print(f"{'='*60}\n")

    # IP 归属
    if ip_info_map:
        print("【IP 归属】")
        for ip, info in ip_info_map.items():
            if info.get("private"):
                continue
            country = info.get("country", "?")
            city = info.get("city", "?")
            org = info.get("org") or info.get("isp") or "?"
            asn = info.get("as", "")
            print(f"  {ip:20s}  {country} · {city}")
            print(f"  {'':20s}  {org}  {asn}")
        print()

    # DNS 解析
    dig = p1.get("dig", {})
    if dig and not dig.get("error"):
        print("【DNS 解析】")
        unique_ips = dig.get("unique_ips", [])
        print(f"  唯一 IP: {', '.join(unique_ips)}")
        # 检查各 DNS 返回是否一致
        by_dns = dig.get("by_dns", {})
        cn_ips, global_ips = set(), set()
        for name, data in by_dns.items():
            ips = [r["value"] for r in data["records"].get("A", []) if r.get("type") == "A"]
            if "alidns" in name:
                cn_ips.update(ips)
            else:
                global_ips.update(ips)
        if cn_ips != global_ips and cn_ips and global_ips:
            print(f"  ⚠️  国内/国外 DNS 返回不同 IP（可能有 GeoDNS 或 CDN）")
            print(f"     国内(Ali): {', '.join(sorted(cn_ips))}")
            print(f"     国外(Google): {', '.join(sorted(global_ips))}")
        else:
            print(f"  DNS 一致（国内外解析相同）")
        print()

    # WHOIS
    whois = p1.get("whois", {})
    if whois and not whois.get("error"):
        print("【WHOIS】")
        fields = ["registrar", "creation_date", "expiry_date", "registrant_org",
                  "registrant_country", "netname", "orgname", "descr", "inetnum", "country"]
        for f in fields:
            if v := whois.get(f):
                print(f"  {f:22s}: {v}")
        ns = whois.get("name_servers", [])
        if ns:
            print(f"  {'name_servers':22s}: {', '.join(ns[:4])}")
        print()

    # robots.txt
    robots = p1.get("robots", {})
    if robots and not robots.get("error"):
        fetch = robots.get("fetch", {})
        status = fetch.get("status_code", "?")
        print("【robots.txt】")
        print(f"  HTTP {status}: {fetch.get('final_url', '')}")
        if summary := robots.get("summary"):
            print(summary)
        elif note := robots.get("note"):
            print(f"  {note}")
        print()

    # ping
    ping = p2.get("ping", {})
    if ping and not ping.get("error"):
        print("【延迟探测】")
        for key, r in ping.get("results", {}).items():
            if r.get("error"):
                continue
            method = r.get("method", "").upper()
            port = f":{r['port']}" if r.get("port") else ""
            loss = r.get("packet_loss_pct", "?")
            avg = r.get("rtt_avg_ms", "?")
            mn = r.get("rtt_min_ms", "?")
            mx = r.get("rtt_max_ms", "?")
            print(f"  [{method}{port}] loss={loss}%  min={mn}ms  avg={avg}ms  max={mx}ms")
        print()

    # traceroute 摘要
    tr = p2.get("traceroute", {})
    if tr and not tr.get("error"):
        hops = tr.get("hops", [])
        print("【Traceroute 摘要】")
        # 找出口节点（第一个公网 IP）
        import ipaddress as ipa
        egress_hop = None
        for hop in hops:
            for ip in hop.get("ips", []):
                try:
                    if not ipa.ip_address(ip).is_private:
                        egress_hop = hop
                        break
                except:
                    pass
            if egress_hop:
                break

        if egress_hop:
            ei = egress_hop["ip_info"][0] if egress_hop.get("ip_info") else {}
            eg_ip = egress_hop["ips"][0] if egress_hop["ips"] else "?"
            eg_loc = f"{ei.get('country','?')} · {ei.get('city','?')}"
            eg_org = ei.get("org") or ei.get("as") or "?"
            print(f"  公网出口 (Hop {egress_hop['hop']}): {eg_ip}  {eg_loc}  {eg_org}")

        # 最后一跳
        last_hops = [h for h in hops if h.get("ips")]
        if last_hops:
            lh = last_hops[-1]
            li = lh["ip_info"][0] if lh.get("ip_info") else {}
            lh_ip = lh["ips"][0]
            lh_loc = f"{li.get('country','?')} · {li.get('city','?')}"
            lh_org = li.get("org") or li.get("as") or "?"
            lh_ms = f"{lh['avg_ms']}ms" if lh.get("avg_ms") else "?ms"
            print(f"  目标节点 (Hop {lh['hop']}):  {lh_ip}  {lh_loc}  {lh_org}  RTT={lh_ms}")
        print()

    # 结论
    print("【站点画像】")
    _generate_portrait(report, ip_info_map, dig, whois)
    print(f"\n耗时: {report.get('elapsed_sec', '?')}s")

def _generate_portrait(report, ip_info_map, dig, whois):
    """生成站点画像结论"""
    by_dns = dig.get("by_dns", {}) if dig else {}
    cn_ips, global_ips = set(), set()
    for name, data in by_dns.items():
        ips = [r["value"] for r in data["records"].get("A", []) if r.get("type") == "A"]
        if "alidns" in name:
            cn_ips.update(ips)
        else:
            global_ips.update(ips)

    # CDN 判断
    if cn_ips != global_ips and cn_ips and global_ips:
        print(f"  🌐 GeoDNS / CDN：国内外解析到不同 IP，存在流量调度")
    else:
        print(f"  🌐 DNS：无 GeoDNS，全球统一入口")

    # 机房位置
    locations = set()
    for ip, info in ip_info_map.items():
        country = info.get("country")
        city = info.get("city")
        org = info.get("org") or info.get("isp", "")
        if country and city:
            locations.add(f"{country} · {city} ({org})")
    for loc in locations:
        print(f"  📍 机房: {loc}")

    # 注册信息
    reg_country = whois.get("registrant_country") if whois else None
    registrar = whois.get("registrar") if whois else None
    if registrar:
        print(f"  📝 注册商: {registrar}")
    if reg_country:
        print(f"  📝 注册地: {reg_country}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="站点综合分析工具")
    parser.add_argument("target", help="域名或 IP")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--no-traceroute", action="store_true")
    parser.add_argument("--no-robots", action="store_true")
    parser.add_argument("--tcp-port", type=int, action="append", dest="ping_ports")
    args = parser.parse_args()
    run(args.target, as_json=args.json, no_traceroute=args.no_traceroute,
        no_robots=args.no_robots, ping_ports=args.ping_ports)
