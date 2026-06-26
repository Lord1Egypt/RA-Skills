#!/usr/bin/env python3
"""sys-doctor: Comprehensive system diagnostics and health check.

Usage:
    python3 sys_doctor.py                  # quick health check
    python3 sys_doctor.py --report         # generate HTML report
    python3 sys_doctor.py --check disk     # check specific category
    python3 sys_doctor.py --json           # output JSON

Categories: disk, memory, cpu, network, services, all
"""

import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path


def get_size(bytes_):
    for unit in ("B", "K", "M", "G", "T"):
        if bytes_ < 1024:
            return f"{bytes_:.1f}{unit}"
        bytes_ /= 1024
    return f"{bytes_:.1f}P"


def get_system_info():
    return {
        "hostname": platform.node(),
        "os": f"{platform.system()} {platform.release()}",
        "kernel": platform.version(),
        "arch": platform.machine(),
        "uptime_seconds": _get_uptime(),
        "python": sys.version.split()[0],
        "users": _get_logged_users(),
    }


def _get_uptime():
    if platform.system() == "Linux":
        try:
            with open("/proc/uptime") as f:
                return float(f.read().split()[0])
        except (FileNotFoundError, IndexError):
            return -1
    return -1


def _get_logged_users():
    try:
        result = subprocess.run(["who", "-q"], capture_output=True, text=True, timeout=5)
        lines = result.stdout.strip().split("\n")
        if lines and "users=" in lines[-1]:
            count = lines[-1].split("=")[1]
            users = lines[:-1]
            return {"count": count, "users": users}
    except Exception:
        return {}
    return {}


def check_disk():
    results = []
    try:
        result = subprocess.run(
            ["df", "-h", "--type=ext4", "--type=xfs", "--type=btrfs", "--type=ext3"],
            capture_output=True, text=True, timeout=10
        )
        lines = result.stdout.strip().split("\n")[1:]
        for line in lines:
            if not line.strip():
                continue
            parts = line.split()
            if len(parts) >= 6:
                mount = parts[5]
                total = parts[1]
                used = parts[2]
                avail = parts[3]
                pct = parts[4].rstrip("%")
                status = "critical" if float(pct) >= 90 else ("warning" if float(pct) >= 80 else "ok")
                results.append({
                    "mount": mount, "total": total, "used": used,
                    "available": avail, "used_pct": pct, "status": status
                })
    except Exception:
        # fallback: check root only
        try:
            usage = shutil.disk_usage("/")
            pct = usage.used / usage.total * 100
            status = "critical" if pct >= 90 else ("warning" if pct >= 80 else "ok")
            results.append({
                "mount": "/", "total": get_size(usage.total), "used": get_size(usage.used),
                "available": get_size(usage.free), "used_pct": f"{pct:.0f}", "status": status
            })
        except Exception:
            pass
    return results


def check_memory():
    results = {}
    if platform.system() == "Linux":
        try:
            result = subprocess.run(["free", "-h"], capture_output=True, text=True, timeout=5)
            lines = result.stdout.strip().split("\n")
            for line in lines[1:]:
                parts = line.split()
                if not parts or parts[0].startswith("Swap"):
                    key = "swap"
                    if len(parts) >= 3:
                        results[key] = {
                            "total": parts[1], "used": parts[2],
                            "free": parts[3] if len(parts) > 3 else "?"
                        }
                elif parts[0] == "Mem:":
                    key = "memory"
                    if len(parts) >= 3:
                        results[key] = {
                            "total": parts[1], "used": parts[2],
                            "free": parts[3] if len(parts) > 3 else "?"
                        }
            # calculate memory pressure
            if "memory" in results:
                mem = results["memory"]
                if mem["total"].endswith("i"):
                    pass  # human-readable format
        except Exception:
            pass
    else:
        try:
            import psutil
            mem = psutil.virtual_memory()
            results["memory"] = {
                "total": get_size(mem.total),
                "used": get_size(mem.used),
                "free": get_size(mem.available),
                "used_pct": f"{mem.percent:.0f}",
            }
            swap = psutil.swap_memory()
            results["swap"] = {
                "total": get_size(swap.total),
                "used": get_size(swap.used),
                "free": get_size(swap.free),
                "used_pct": f"{swap.percent:.0f}",
            }
        except ImportError:
            results["error"] = "psutil not available, install with: pip install psutil"
    return results


def check_cpu():
    results = {}
    if platform.system() == "Linux":
        try:
            with open("/proc/loadavg") as f:
                parts = f.read().strip().split()
                results["load_1min"] = parts[0] if len(parts) > 0 else "?"
                results["load_5min"] = parts[1] if len(parts) > 1 else "?"
                results["load_15min"] = parts[2] if len(parts) > 2 else "?"
        except FileNotFoundError:
            pass
    try:
        # Get CPU count
        cpu_count = os.cpu_count() or 1
        results["cores"] = cpu_count
        results["logical_cores"] = _get_cpu_count_logical()
    except Exception:
        pass
    # Temperature (Linux with lm-sensors)
    try:
        result = subprocess.run(["sensors", "-j"], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            results["sensors_available"] = True
        else:
            results["sensors_available"] = False
    except FileNotFoundError:
        results["sensors_available"] = False
    return results


def _get_cpu_count_logical():
    if platform.system() == "Linux":
        try:
            with open("/proc/cpuinfo") as f:
                return sum(1 for line in f if line.startswith("processor"))
        except FileNotFoundError:
            pass
    return os.cpu_count() or 1


def check_network():
    results = {}
    # Get default gateway
    try:
        if platform.system() == "Linux":
            result = subprocess.run(["ip", "route", "show", "default"], capture_output=True, text=True, timeout=5)
            if result.stdout.strip():
                results["default_gateway"] = result.stdout.strip()
    except FileNotFoundError:
        try:
            result = subprocess.run(["route", "-n"], capture_output=True, text=True, timeout=5)
            lines = result.stdout.strip().split("\n")
            for line in lines[2:]:
                parts = line.split()
                if parts and parts[0] == "0.0.0.0":
                    results["default_gateway"] = parts[1] if len(parts) > 1 else ""
                    break
        except Exception:
            pass

    # Interface info via ip
    try:
        result = subprocess.run(["ip", "-br", "addr"], capture_output=True, text=True, timeout=5)
        interfaces = []
        for line in result.stdout.strip().split("\n"):
            parts = line.split()
            if parts and parts[0] != "lo":
                interfaces.append({
                    "name": parts[0],
                    "state": parts[1],
                    "ip": parts[2] if len(parts) > 2 else ""
                })
        results["interfaces"] = interfaces
    except FileNotFoundError:
        pass

    # DNS resolution test
    try:
        start = time.time()
        result = subprocess.run(
            ["getent", "hosts", "google.com"],
            capture_output=True, text=True, timeout=5
        )
        elapsed = time.time() - start
        if result.returncode == 0:
            results["dns_resolution_ms"] = f"{elapsed*1000:.0f}"
    except Exception:
        pass

    return results


def check_services():
    results = []
    # Check systemd services
    if platform.system() == "Linux":
        try:
            result = subprocess.run(
                ["systemctl", "list-units", "--type=service", "--state=running", "--no-pager"],
                capture_output=True, text=True, timeout=10
            )
            lines = result.stdout.strip().split("\n")
            started = False
            for line in lines:
                if not line.strip() or line.startswith(" "):
                    if started and line.strip():
                        break
                    continue
                if line.startswith("UNIT") or "LOAD" in line:
                    started = True
                    continue
                parts = line.split()
                if len(parts) >= 4 and parts[1] == "loaded" and parts[2] == "active":
                    results.append(parts[0])
            results = sorted(set(results))
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass
    return results


def check_all():
    return {
        "system": get_system_info(),
        "disk": check_disk(),
        "memory": check_memory(),
        "cpu": check_cpu(),
        "network": check_network(),
        "services": check_services(),
    }


def generate_html_report(data):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    hostname = data.get("system", {}).get("hostname", "unknown")
    os_info = data.get("system", {}).get("os", "unknown")

    # Compute overall status
    status = "ok"
    for disk in data.get("disk", []):
        if disk.get("status") == "critical":
            status = "critical"
        elif disk.get("status") == "warning" and status != "critical":
            status = "warning"

    status_color = {"ok": "green", "warning": "orange", "critical": "red"}.get(status, "gray")

    disks_html = ""
    for disk in data.get("disk", []):
        c = {"ok": "green", "warning": "orange", "critical": "red"}.get(disk.get("status", "ok"), "gray")
        disks_html += f"<tr><td>{disk['mount']}</td><td>{disk['total']}</td><td>{disk['used']}</td><td>{disk['available']}</td><td style='color:{c}'>{disk['used_pct']}%</td></tr>\n"

    mem = data.get("memory", {})
    mem_html = ""
    if "memory" in mem:
        m = mem["memory"]
        mem_html += f"<tr><td>RAM</td><td>{m.get('total', '?')}</td><td>{m.get('used', '?')}</td><td>{m.get('free', '?')}</td><td>{m.get('used_pct', '?')}%</td></tr>\n"
    if "swap" in mem:
        s = mem["swap"]
        mem_html += f"<tr><td>Swap</td><td>{s.get('total', '?')}</td><td>{s.get('used', '?')}</td><td>{s.get('free', '?')}</td><td>{s.get('used_pct', '?')}%</td></tr>\n"

    cpu = data.get("cpu", {})
    cpu_html = f"""
    <tr><td>Load (1min / 5min / 15min)</td><td>{cpu.get('load_1min', '?')} / {cpu.get('load_5min', '?')} / {cpu.get('load_15min', '?')}</td></tr>
    <tr><td>Cores (logical)</td><td>{cpu.get('cores', '?')} ({cpu.get('logical_cores', '?')})</td></tr>
    <tr><td>Sensors</td><td>{'Available' if cpu.get('sensors_available') else 'Not available'}</td></tr>
    """

    net = data.get("network", {})
    interfaces_html = ""
    for iface in net.get("interfaces", []):
        interfaces_html += f"<tr><td>{iface['name']}</td><td>{iface['state']}</td><td>{iface.get('ip', '')}</td></tr>\n"

    services = data.get("services", [])
    services_html = ""
    for s in services[:20]:
        services_html += f"<li>{s}</li>\n"
    if len(services) > 20:
        services_html += f"<li>... and {len(services) - 20} more</li>\n"

    uptime_s = data.get("system", {}).get("uptime_seconds", 0)
    uptime_str = f"{int(uptime_s // 86400)}d {int((uptime_s % 86400) // 3600)}h {int((uptime_s % 3600) // 60)}m" if uptime_s > 0 else "N/A"

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>System Health Report - {hostname}</title>
<style>
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 900px; margin: 20px auto; padding: 0 20px; background: #f5f5f5; color: #333; }}
h1 {{ color: #333; border-bottom: 2px solid #ddd; padding-bottom: 8px; }}
h2 {{ color: #555; margin-top: 24px; }}
table {{ width: 100%; border-collapse: collapse; margin: 12px 0; background: white; border-radius: 6px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
th, td {{ padding: 8px 12px; text-align: left; border-bottom: 1px solid #eee; }}
th {{ background: #f0f0f0; font-weight: 600; }}
.status-badge {{ display: inline-block; padding: 4px 12px; border-radius: 12px; color: white; font-weight: 600; font-size: 14px; background-color: {status_color}; }}
ul.services {{ columns: 3; list-style: none; padding: 0; }}
ul.services li {{ padding: 3px 8px; font-family: monospace; font-size: 13px; }}
.footer {{ margin-top: 30px; color: #888; font-size: 12px; text-align: center; }}
</style>
</head>
<body>
<h1>System Health Report <span class="status-badge">{status.upper()}</span></h1>
<p><strong>Host:</strong> {hostname} | <strong>OS:</strong> {os_info} | <strong>Uptime:</strong> {uptime_str}</p>

<h2>Disk Usage</h2>
<table><tr><th>Mount</th><th>Total</th><th>Used</th><th>Available</th><th>Usage</th></tr>
{disks_html}</table>

<h2>Memory</h2>
<table><tr><th>Type</th><th>Total</th><th>Used</th><th>Free</th><th>Usage</th></tr>
{mem_html}</table>

<h2>CPU</h2>
<table><tr><th>Metric</th><th>Value</th></tr>
{cpu_html}</table>

<h2>Network Interfaces</h2>
<table><tr><th>Interface</th><th>State</th><th>IP</th></tr>
{interfaces_html}</table>
<p><strong>DNS Resolution:</strong> {net.get('dns_resolution_ms', 'N/A')}ms</p>
<p><strong>Default Gateway:</strong> {net.get('default_gateway', 'N/A')}</p>

<h2>Running Services ({len(services)})</h2>
<ul class="services">{services_html}</ul>

<p class="footer">Generated: {timestamp} | sys-doctor v1.0.0</p>
</body>
</html>"""
    return html


def print_text_report(data):
    def section(title):
        print(f"\n{'='*60}")
        print(f"  {title}")
        print(f"{'='*60}")

    hostname = data.get("system", {}).get("hostname", "unknown")
    print(f"\n  ◆ System Health Report: {hostname}")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}")

    section("DISK")
    for disk in data.get("disk", []):
        icon = {"critical": "🔴", "warning": "🟡", "ok": "🟢"}.get(disk.get("status", "ok"), "⚪")
        print(f"  {icon} {disk['mount']:12s}  {disk['used_pct']:>4s}%  ({disk['used']}/{disk['total']}, avail: {disk['available']})")

    section("MEMORY")
    mem = data.get("memory", {})
    if "memory" in mem:
        m = mem["memory"]
        print(f"  RAM:    {m.get('used', '?')} / {m.get('total', '?')}  ({m.get('used_pct', '?')}%)")
    if "swap" in mem:
        s = mem["swap"]
        print(f"  Swap:   {s.get('used', '?')} / {s.get('total', '?')}  ({s.get('used_pct', '?')}%)")

    section("CPU")
    cpu = data.get("cpu", {})
    print(f"  Load:     {cpu.get('load_1min', '?')} / {cpu.get('load_5min', '?')} / {cpu.get('load_15min', '?')}")
    print(f"  Cores:    {cpu.get('cores', '?')} ({cpu.get('logical_cores', '?')} logical)")

    section("NETWORK")
    for iface in data.get("network", {}).get("interfaces", []):
        state_icon = "🟢" if iface.get("state") == "UP" else "🔴"
        print(f"  {state_icon} {iface['name']:10s}  {iface.get('state', '?'):4s}  {iface.get('ip', '')}")

    section("SERVICES")
    for s in data.get("services", [])[:15]:
        print(f"  • {s}")

    print()


def main():
    parser = argparse.ArgumentParser(description="System Health Diagnostics")
    parser.add_argument("--check", choices=["disk", "memory", "cpu", "network", "services", "all"], default="all")
    parser.add_argument("--report", action="store_true", help="Generate HTML report")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("--output", "-o", help="Output file path (for --report)")
    args = parser.parse_args()

    check_map = {
        "disk": {"disk": check_disk()},
        "memory": {"memory": check_memory()},
        "cpu": {"cpu": check_cpu()},
        "network": {"network": check_network()},
        "services": {"services": check_services()},
        "all": check_all(),
    }

    data = check_map.get(args.check, check_map["all"])
    if args.check == "all":
        data = check_all()

    if args.json:
        print(json.dumps(data, indent=2))
        return

    if args.report:
        html = generate_html_report(data)
        output_path = args.output or f"sys-doctor-report-{datetime.now().strftime('%Y%m%d-%H%M%S')}.html"
        with open(output_path, "w") as f:
            f.write(html)
        print(f"Report saved: {output_path}")
        return

    print_text_report(data)

    # Return exit code based on health
    for disk in data.get("disk", []):
        if disk.get("status") == "critical":
            sys.exit(2)
    sys.exit(0)


if __name__ == "__main__":
    main()
