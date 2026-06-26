#!/usr/bin/env python3
"""
VPS Guardian — Autonomous VPS monitoring and auto-remediation.
Kills runaway procs, frees disk, restarts dead services, hardens security.

Usage:
  vps-guardian --scan          # One-shot scan + remediate
  vps-guardian --daemon        # Continuous monitoring
  vps-guardian --dry-run       # Report only, no action
"""

import argparse
import configparser
import glob
import json
import os
import signal
import subprocess
import sys
import time
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

# --- Configuration ---
CONF_PATH = "/etc/vps-guardian.conf"
LOG_PATH = "/var/log/vps-guardian.log"

# Defaults
DEFAULTS = {
    "cpu_kill_percent": 90,
    "cpu_kill_duration": 300,
    "disk_warn_percent": 80,
    "disk_act_percent": 90,
    "memory_act_percent": 90,
    "zombie_kill": True,
    "rotate_logs_days": 7,
    "tmp_max_age_days": 3,
    "journal_max_size_mb": 500,
    "apt_cache_clean": True,
    "max_ssh_failures": 10,
    "auto_block": False,
}

PROTECTED_PIDS = {1}  # Never kill init
PROTECTED_COMM = {"systemd", "kthreadd", "guardian.py"}
MAX_KILLS_PER_CYCLE = 5

# --- State ---
remediated = False
kill_count = 0


def log(msg, level="INFO"):
    ts = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    line = f"[{ts}] {level} {msg}"
    print(line)
    try:
        with open(LOG_PATH, "a") as f:
            f.write(line + "\n")
    except OSError:
        pass


def load_config():
    cfg = dict(DEFAULTS)
    if os.path.exists(CONF_PATH):
        cp = configparser.ConfigParser()
        cp.read(CONF_PATH)
        if "thresholds" in cp:
            for k, v in cp["thresholds"].items():
                if k in cfg:
                    if isinstance(cfg[k], bool):
                        cfg[k] = v.lower() in ("true", "yes", "1")
                    else:
                        cfg[k] = type(cfg[k])(v)
    return cfg


def get_process_list():
    """Read /proc for process info."""
    procs = []
    for pid_dir in glob.glob("/proc/[0-9]*"):
        try:
            pid = int(pid_dir.split("/")[-1])
            with open(f"/proc/{pid}/stat") as f:
                stat = f.read().split()
            with open(f"/proc/{pid}/cmdline") as f:
                cmdline = f.read().replace("\x00", " ").strip()
            comm = stat[1].strip("()")
            state = stat[2]
            utime = int(stat[13])
            stime = int(stat[14])
            rss = int(stat[23]) * 4096  # pages to bytes

            # CPU% from /proc/stat delta would need two reads; approximate
            total_ticks = utime + stime
            uptime_secs = float(open("/proc/uptime").read().split()[0])
            hz = os.sysconf("SC_CLK_TCK")
            cpu_pct = (total_ticks / hz / uptime_secs * 100) if uptime_secs > 0 else 0

            procs.append({
                "pid": pid,
                "comm": comm,
                "cmdline": cmdline or comm,
                "state": state,
                "cpu_pct": round(cpu_pct, 1),
                "rss": rss,
                "utime": utime,
                "stime": stime,
            })
        except (PermissionError, FileNotFoundError, ValueError, IndexError):
            continue
    return procs


# --- Remediation Actions ---

def kill_runaway_processes(procs, cfg, dry_run=False):
    """Kill processes using too much CPU or zombies."""
    global remediated, kill_count
    killed = []

    for p in procs:
        if kill_count >= MAX_KILLS_PER_CYCLE:
            break
        if p["pid"] in PROTECTED_PIDS or p["comm"] in PROTECTED_COMM:
            continue
        if "guardian" in p["cmdline"].lower():
            continue

        # Zombie check
        if p["state"] == "Z" and cfg["zombie_kill"]:
            msg = f"ZOMBIE pid={p['pid']} comm={p['comm']} → reaping parent"
            log(msg)
            if not dry_run:
                # Zombies can't be killed directly; signal parent
                try:
                    with open(f"/proc/{p['pid']}/stat") as f:
                        ppid = int(f.read().split()[3])
                    os.kill(ppid, signal.SIGCHLD)
                except (ProcessLookupError, PermissionError, FileNotFoundError):
                    pass
            remediated = True
            continue

        # High CPU check (note: this is lifetime avg, not current — simplified)
        if p["cpu_pct"] > cfg["cpu_kill_percent"]:
            msg = f"RUNAWAY pid={p['pid']} cmd=\"{p['cmdline'][:60]}\" cpu={p['cpu_pct']}% → SIGTERM"
            log(msg)
            if not dry_run:
                try:
                    os.kill(p["pid"], signal.SIGTERM)
                    time.sleep(2)
                    # Check if still alive
                    os.kill(p["pid"], 0)
                    log(f"RUNAWAY pid={p['pid']} still alive → SIGKILL")
                    os.kill(p["pid"], signal.SIGKILL)
                except (ProcessLookupError, PermissionError):
                    pass
            killed.append(p)
            kill_count += 1
            remediated = True

    return killed


def recover_disk_space(cfg, dry_run=False):
    """Free disk space when above threshold."""
    global remediated
    stat = os.statvfs("/")
    total = stat.f_blocks * stat.f_frsize
    avail = stat.f_bavail * stat.f_frsize
    used_pct = round((1 - avail / total) * 100, 1)

    if used_pct < cfg["disk_act_percent"]:
        if used_pct >= cfg["disk_warn_percent"]:
            log(f"DISK / {used_pct}% (warning, below action threshold)")
        return

    log(f"DISK / {used_pct}% → reclaiming space")
    freed = 0

    # Rotate old logs
    for log_file in glob.glob("/var/log/*.1") + glob.glob("/var/log/*.[0-9]"):
        try:
            mtime = os.path.getmtime(log_file)
            age_days = (time.time() - mtime) / 86400
            if age_days > cfg["rotate_logs_days"]:
                size = os.path.getsize(log_file)
                if not dry_run:
                    subprocess.run(["gzip", "-f", log_file], timeout=30, capture_output=True)
                freed += size
        except (OSError, subprocess.TimeoutExpired):
            pass

    # Clean /tmp
    tmp_age = time.time() - (cfg["tmp_max_age_days"] * 86400)
    for f in glob.glob("/tmp/*"):
        try:
            if os.path.isfile(f) and os.path.getmtime(f) < tmp_age:
                size = os.path.getsize(f)
                if not dry_run:
                    os.remove(f)
                freed += size
        except (OSError, PermissionError):
            pass

    # Truncate journal if too large
    if cfg["journal_max_size_mb"]:
        try:
            result = subprocess.run(
                ["journalctl", "--disk-usage"],
                capture_output=True, text=True, timeout=10
            )
            # Parse "Archived and active journals take up X.XM"
            for part in result.stdout.split():
                if part.endswith("M") or part.endswith("G"):
                    size_str = part.rstrip("MG")
                    try:
                        size_mb = float(size_str)
                        if "G" in part:
                            size_mb *= 1024
                        if size_mb > cfg["journal_max_size_mb"]:
                            if not dry_run:
                                subprocess.run(
                                    ["journalctl", "--vacuum-size=f{cfg['journal_max_size_mb']}M"],
                                    timeout=30, capture_output=True
                                )
                            freed += int((size_mb - cfg["journal_max_size_mb"]) * 1024 * 1024)
                    except ValueError:
                        pass
                    break
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass

    # Clean apt cache
    if cfg["apt_cache_clean"]:
        try:
            if not dry_run:
                result = subprocess.run(
                    ["apt-get", "clean"], timeout=30, capture_output=True
                )
                if result.returncode == 0:
                    freed += 50 * 1024 * 1024  # rough estimate
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass

    # Check new usage
    stat2 = os.statvfs("/")
    avail2 = stat2.f_bavail * stat2.f_frsize
    new_pct = round((1 - avail2 / (stat2.f_blocks * stat2.f_frsize)) * 100, 1)

    log(f"DISK / {used_pct}% → freed {freed // (1024*1024)}MB → {new_pct}%")
    remediated = True


def restart_dead_services(cfg, dry_run=False):
    """Restart services that are down."""
    global remediated
    critical_services = ["ssh", "cron", "rsyslog", "systemd-resolved"]
    # Read from config if available
    cp = configparser.ConfigParser()
    if os.path.exists(CONF_PATH):
        cp.read(CONF_PATH)
        if "services" in cp and "critical" in cp["services"]:
            critical_services = [s.strip() for s in cp["services"]["critical"].split(",")]

    for svc in critical_services:
        try:
            result = subprocess.run(
                ["systemctl", "is-active", svc],
                capture_output=True, text=True, timeout=5
            )
            status = result.stdout.strip()
            if status != "active":
                log(f"SERVICE {svc}: {status} → restarting")
                if not dry_run:
                    for attempt in range(3):
                        subprocess.run(
                            ["systemctl", "restart", svc],
                            capture_output=True, timeout=30
                        )
                        time.sleep(5 * (2 ** attempt))  # exponential backoff
                        check = subprocess.run(
                            ["systemctl", "is-active", svc],
                            capture_output=True, text=True, timeout=5
                        )
                        if check.stdout.strip() == "active":
                            log(f"SERVICE {svc}: restarted → active (attempt {attempt + 1})")
                            remediated = True
                            break
                    else:
                        log(f"SERVICE {svc}: FAILED to restart after 3 attempts", level="CRITICAL")
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass


def check_memory(cfg, dry_run=False):
    """Recover memory when pressure is high."""
    global remediated
    try:
        with open("/proc/meminfo") as f:
            mem = {}
            for line in f:
                parts = line.split()
                if len(parts) >= 2:
                    mem[parts[0].rstrip(":")] = int(parts[1]) * 1024
    except IOError:
        return

    total = mem.get("MemTotal", 1)
    available = mem.get("MemAvailable", 0)
    used_pct = round((1 - available / total) * 100, 1) if total else 0

    if used_pct < cfg["memory_act_percent"]:
        return

    log(f"MEMORY {used_pct}% → dropping caches")
    if not dry_run:
        try:
            with open("/proc/sys/vm/drop_caches", "w") as f:
                f.write("3\n")
            remediated = True
        except (PermissionError, IOError):
            pass


def check_security(cfg, dry_run=False):
    """Basic security checks — approval required for blocking."""
    # Check SSH brute force attempts
    if not os.path.exists("/var/log/auth.log"):
        return

    try:
        failures = defaultdict(int)
        with open("/var/log/auth.log") as f:
            for line in f:
                if "Failed password" in line:
                    # Extract IP
                    import re
                    match = re.search(r"from (\d+\.\d+\.\d+\.\d+)", line)
                    if match:
                        failures[match.group(1)] += 1

        for ip, count in failures.items():
            if count >= cfg["max_ssh_failures"]:
                msg = f"SECURITY {count} SSH failures from {ip}"
                if cfg["auto_block"] and not dry_run:
                    log(f"{msg} → blocking via iptables")
                    subprocess.run(
                        ["iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"],
                        capture_output=True, timeout=10
                    )
                    remediated = True
                else:
                    log(f"{msg} → BLOCK RECOMMENDED (auto_block=false)")
    except (IOError, subprocess.TimeoutExpired):
        pass


# --- Main ---

def scan(cfg, dry_run=False):
    """Run all checks and remediations."""
    global remediated
    remediated = False

    log(f"Scan starting (dry_run={dry_run})")

    procs = get_process_list()
    kill_runaway_processes(procs, cfg, dry_run)
    recover_disk_space(cfg, dry_run)
    restart_dead_services(cfg, dry_run)
    check_memory(cfg, dry_run)
    check_security(cfg, dry_run)

    if remediated:
        log("Scan complete — issues remediated")
        return 1
    else:
        log("Scan complete — all healthy")
        return 0


def daemon_loop(cfg, dry_run=False, interval=300):
    """Continuous monitoring loop."""
    while True:
        result = scan(cfg, dry_run)
        time.sleep(interval)


def main():
    parser = argparse.ArgumentParser(description="VPS Guardian — self-healing server agent")
    parser.add_argument("--scan", action="store_true", help="One-shot scan + remediate")
    parser.add_argument("--daemon", action="store_true", help="Continuous monitoring")
    parser.add_argument("--dry-run", action="store_true", help="Report only, no action")
    parser.add_argument("--interval", type=int, default=300, help="Seconds between scans (daemon mode)")
    args = parser.parse_args()

    if not args.scan and not args.daemon:
        args.scan = True

    cfg = load_config()

    if args.daemon:
        daemon_loop(cfg, args.dry_run, args.interval)
    else:
        sys.exit(scan(cfg, args.dry_run))


if __name__ == "__main__":
    main()
