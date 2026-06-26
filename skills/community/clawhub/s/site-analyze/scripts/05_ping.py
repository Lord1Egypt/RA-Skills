#!/usr/bin/env python3
"""
05_ping.py - ping / TCP 延迟探测
用法: python3 05_ping.py <host> [--count 5] [--tcp-port 80] [--json]
TCP 探测使用 Python socket，不依赖 hping3
"""
import subprocess, sys, json, re, socket, time
from concurrent.futures import ThreadPoolExecutor

def ping_icmp(host, count=5):
    """ICMP ping"""
    try:
        result = subprocess.run(
            ["ping", "-c", str(count), "-W", "3", host],
            capture_output=True, text=True, timeout=30
        )
        output = result.stdout + result.stderr
        # 解析统计
        rtt_match = re.search(r'rtt min/avg/max/mdev = ([\d.]+)/([\d.]+)/([\d.]+)/([\d.]+)', output)
        loss_match = re.search(r'(\d+)% packet loss', output)
        recv_match = re.search(r'(\d+) received', output)

        return {
            "method": "icmp",
            "host": host,
            "count": count,
            "packet_loss_pct": int(loss_match.group(1)) if loss_match else None,
            "received": int(recv_match.group(1)) if recv_match else None,
            "rtt_min_ms": float(rtt_match.group(1)) if rtt_match else None,
            "rtt_avg_ms": float(rtt_match.group(2)) if rtt_match else None,
            "rtt_max_ms": float(rtt_match.group(3)) if rtt_match else None,
            "rtt_mdev_ms": float(rtt_match.group(4)) if rtt_match else None,
            "raw": output.strip()
        }
    except Exception as e:
        return {"method": "icmp", "host": host, "error": str(e)}

def ping_tcp(host, port, count=5):
    """TCP 连接延迟探测（不需要 root）"""
    rtts = []
    errors = []
    for i in range(count):
        try:
            start = time.perf_counter()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            sock.connect((host, port))
            rtt = (time.perf_counter() - start) * 1000
            sock.close()
            rtts.append(round(rtt, 3))
        except Exception as e:
            errors.append(str(e))
        time.sleep(0.2)

    result = {
        "method": "tcp",
        "host": host,
        "port": port,
        "count": count,
        "success": len(rtts),
        "failed": len(errors),
        "packet_loss_pct": round(len(errors) / count * 100),
    }
    if rtts:
        result.update({
            "rtt_min_ms": min(rtts),
            "rtt_avg_ms": round(sum(rtts) / len(rtts), 3),
            "rtt_max_ms": max(rtts),
            "rtts": rtts
        })
    if errors:
        result["errors"] = errors[:3]

    return result

def run(host, count=5, tcp_ports=None, as_json=False):
    """同时做 ICMP ping 和多端口 TCP 探测"""
    results = {}

    with ThreadPoolExecutor(max_workers=5) as pool:
        futures = {"icmp": pool.submit(ping_icmp, host, count)}
        if tcp_ports:
            for port in tcp_ports:
                futures[f"tcp_{port}"] = pool.submit(ping_tcp, host, port, count)

        for key, f in futures.items():
            results[key] = f.result()

    output = {"host": host, "results": results}

    if as_json:
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print(f"\n=== Ping/延迟探测: {host} ===\n")
        for key, r in results.items():
            method = r.get("method", key).upper()
            if r.get("error"):
                print(f"  [{method}] ERROR: {r['error']}")
                continue
            loss = r.get("packet_loss_pct", "?")
            avg = r.get("rtt_avg_ms", "?")
            mn = r.get("rtt_min_ms", "?")
            mx = r.get("rtt_max_ms", "?")
            port_str = f":{r['port']}" if r.get("port") else ""
            print(f"  [{method}{port_str}] loss={loss}%  min={mn}ms  avg={avg}ms  max={mx}ms")
        print()

    return output

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("host")
    parser.add_argument("--count", type=int, default=5)
    parser.add_argument("--tcp-port", type=int, action="append", dest="tcp_ports")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    run(args.host, count=args.count, tcp_ports=args.tcp_ports or [80, 443], as_json=args.json)
