#!/usr/bin/env bash
# System Watchdog — check.sh (Linux + macOS)
# Focus on actionable anomalies, not generic resource summaries.
# Auto-detects OS. No external dependencies beyond Python 3.
set -euo pipefail
export PATH="/usr/sbin:/sbin:$PATH"

python3 << 'PYEOF'
import json
import os
import platform
import re
import subprocess
import sys
import time
from pathlib import Path

IS_MACOS = platform.system() == "Darwin"
IS_LINUX = platform.system() == "Linux"

if not (IS_MACOS or IS_LINUX):
    print(json.dumps({"error": f"Unsupported OS: {platform.system()}"}))
    sys.exit(1)

STATE_PATH = Path(os.environ.get("SYSTEM_WATCHDOG_STATE",
    os.path.expanduser("~/.openclaw/workspace/state/system-watchdog-state.json")))

# ============================================================
# Thresholds — tuned to reduce false positives
# ============================================================
SWAP_GROWTH_ALERT_MB = 1024          # +1 GB since last run
SWAP_USED_ALERT_MB = 4096            # 4 GB swap notable only with other pressure signals
FREE_MEM_ALERT_GB = 0.5              # Linux: MemAvailable; macOS: truly free pages
COMPRESSED_ALERT_GB = 4.0            # macOS only: compressor pressure
RUNAWAY_MEM_GROWTH_MB = 1024         # +1 GB since last run for a single process
RUNAWAY_MEM_ABS_MB = 6144            # 6 GB resident for non-allowlisted process
SUSTAINED_CPU_PCT = 200.0            # >2 full cores sustained
SUSTAINED_CPU_MIN_ELAPSED = 900      # 15 min
DISK_USED_PCT_ALERT = 90
DISK_FREE_GB_ALERT = 20

# ============================================================
# Ignore list — processes expected to be long-lived / heavy
# ============================================================
IGNORE_NAMES = {
    # Shared
    "tailscaled", "sshd", "cron", "syncthing",
    "openclaw", "openclaw-gatewa", "bun", "node",
    "dockerd", "containerd", "containerd-shim",
    "containermanagerd", "containermanage",
    # Linux
    "systemd", "systemd-journal", "systemd-oomd", "systemd-logind",
    "systemd-resolve", "systemd-timesyn", "systemd-udevd",
    "NetworkManager", "polkitd", "thermald", "upowerd",
    "avahi-daemon", "dbus-daemon",
    "pulseaudio", "pipewire", "gnome-shell", "gdm", "Xorg", "Xwayland",
    "rsyslogd", "snapd", "udisksd", "accounts-daemon", "colord",
    "rtkit-daemon",
    # macOS
    "launchd", "kernel_task", "WindowServer", "loginwindow",
    "opendirectoryd", "mds_stores", "mds", "Finder", "Dock",
    "SystemUIServer", "airportd", "bluetoothd", "coreduetd",
    "fseventsd", "logd", "notifyd", "powerd", "securityd",
    "syslogd", "trustd", "configd", "distnoted", "UserEventAgent",
    "coreaudiod", "swd", "remoted", "symptomsd", "watchdogd",
    "sandboxd", "diskarbitrationd", "timed", "runningboardd",
    "rapportd", "sharingd", "suggestd", "nsurlsessiond",
}
IGNORE_SUBSTRINGS = [
    "docker", "com.docker", "containerd",
    "virtualization", "orbstack", "vmnetd",
    # Linux kernel threads
    "kworker", "migration", "ksoftirq", "kswapd", "rcu_", "irq/", "watchdog",
]


# ============================================================
# Helpers
# ============================================================
def run(cmd):
    return subprocess.check_output(cmd, shell=isinstance(cmd, str)).decode()


def parse_elapsed(s):
    s = s.strip()
    if not s:
        return 0
    days = 0
    if '-' in s:
        d, s = s.split('-', 1)
        days = int(d)
    parts = [int(p) for p in s.split(':')]
    if len(parts) == 3:
        return days * 86400 + parts[0] * 3600 + parts[1] * 60 + parts[2]
    if len(parts) == 2:
        return days * 86400 + parts[0] * 60 + parts[1]
    return days * 86400 + parts[0]


def human_elapsed(secs):
    if secs >= 86400:
        return f"{secs // 86400}d"
    if secs >= 3600:
        return f"{secs // 3600}h"
    if secs >= 60:
        return f"{secs // 60}m"
    return f"{secs}s"


def gb(n):
    return round(n / (1024 ** 3), 2)


def load_previous_state():
    try:
        return json.loads(STATE_PATH.read_text())
    except Exception:
        return {}


def save_state(state):
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, indent=2))


def should_ignore(name, command):
    low_name = (name or "").lower()
    low_cmd = (command or "").lower()
    if name in IGNORE_NAMES or low_name in IGNORE_NAMES:
        return True
    return any(token in low_name or token in low_cmd for token in IGNORE_SUBSTRINGS)


# ============================================================
# System memory — OS-specific collection
# ============================================================
if IS_LINUX:
    meminfo = {}
    with open("/proc/meminfo") as f:
        for line in f:
            parts = line.split()
            if len(parts) >= 2:
                meminfo[parts[0].rstrip(":")] = int(parts[1]) * 1024  # kB → bytes

    ram_total = meminfo.get("MemTotal", 0)
    ram_free = meminfo.get("MemFree", 0)
    ram_available = meminfo.get("MemAvailable", 0)
    ram_buffers = meminfo.get("Buffers", 0)
    ram_cached = meminfo.get("Cached", 0)
    ram_used = ram_total - ram_free - ram_buffers - ram_cached
    ram_pct = round(ram_used * 100 / max(ram_total, 1), 1)

    swap_total_bytes = meminfo.get("SwapTotal", 0)
    swap_used_bytes = swap_total_bytes - meminfo.get("SwapFree", 0)
    swap_used_mb = swap_used_bytes / (1024 * 1024)
    swap_total_mb = swap_total_bytes / (1024 * 1024)

    # "Available" on Linux is the best single number for pressure
    free_pressure_gb = gb(ram_available)

    # Linux doesn't have macOS-style compressed/inactive breakdown
    compressed_bytes = 0
    inactive_bytes = 0
    free_bytes = ram_free

    with open("/proc/loadavg") as f:
        load = f.read().split()[:3]
    cores = int(run(["nproc"]).strip())

else:  # macOS
    ram_total = int(run(["sysctl", "-n", "hw.memsize"]).strip())
    vm = run(["vm_stat"])
    page_size = int(re.search(r'(\d+)', vm.split('\n')[0]).group(1))

    def vm_val(label):
        m = re.search(rf'{re.escape(label)}:\s+(\d+)', vm)
        return int(m.group(1)) if m else 0

    pages_free = vm_val("Pages free")
    pages_active = vm_val("Pages active")
    pages_inactive = vm_val("Pages inactive")
    pages_speculative = vm_val("Pages speculative")
    pages_wired = vm_val("Pages wired down")
    pages_compressed = vm_val("Pages occupied by compressor")

    free_bytes = pages_free * page_size
    inactive_bytes = (pages_inactive + pages_speculative) * page_size
    wired_bytes = pages_wired * page_size
    active_bytes = pages_active * page_size
    compressed_bytes = pages_compressed * page_size
    ram_used = active_bytes + wired_bytes + compressed_bytes
    ram_pct = round(ram_used * 100 / ram_total, 1)

    swap = run(["sysctl", "-n", "vm.swapusage"])
    swap_total_mb = float(re.search(r'total = ([\d.]+)M', swap).group(1)) if 'total' in swap else 0.0
    swap_used_mb = float(re.search(r'used = ([\d.]+)M', swap).group(1)) if 'used' in swap else 0.0

    # On macOS, "truly free" pages is the closest pressure signal
    free_pressure_gb = gb(free_bytes)

    load = run(["sysctl", "-n", "vm.loadavg"]).strip().strip('{}').split()
    cores = int(run(["sysctl", "-n", "hw.ncpu"]).strip())


# ============================================================
# Disk — OS-specific
# ============================================================
if IS_LINUX:
    df_out = run(["df", "-BG", "--output=target,pcent,used,size,avail", "/"])
    parts = df_out.strip().split("\n")[1].split()
    disk_pct = int(parts[1].rstrip("%"))
    disk_used_gb = int(parts[2].rstrip("G"))
    disk_total_gb = int(parts[3].rstrip("G"))
    disk_free_gb = int(parts[4].rstrip("G"))
else:
    df_parts = run(["df", "-g", "/"]).split('\n')[1].split()
    disk_total_gb = int(df_parts[1])
    disk_used_gb = int(df_parts[2])
    disk_free_gb = int(df_parts[3])
    disk_pct = int(df_parts[4].rstrip('%'))


# ============================================================
# Process scan — works on both OSes
# ============================================================
ps_out = run(["ps", "axo", "pid=,ppid=,pcpu=,rss=,etime=,comm=,args="])
processes = []
for line in ps_out.strip().split('\n'):
    parts = line.split(None, 6)
    if len(parts) < 7:
        continue
    pid, ppid, cpu, rss, elapsed, comm, args = parts
    pid = int(pid)
    ppid = int(ppid)
    cpu = float(cpu)
    rss_kb = int(rss)
    elapsed_secs = parse_elapsed(elapsed)
    command = args.strip()
    first_arg = command.split()[0] if command else ""
    name = os.path.basename(comm).strip() or os.path.basename(first_arg).strip() or comm.strip() or "unknown"
    # macOS sometimes truncates comm to 2 chars — fall back to first arg
    if len(name) <= 2 and first_arg:
        name = os.path.basename(first_arg).strip() or name
    processes.append({
        "pid": pid,
        "ppid": ppid,
        "name": name,
        "command": command,
        "cpu_pct": round(cpu, 1),
        "mem_mb": rss_kb // 1024,
        "elapsed_secs": elapsed_secs,
        "elapsed": human_elapsed(elapsed_secs),
    })

top_processes = sorted(processes, key=lambda p: (p["mem_mb"], p["cpu_pct"]), reverse=True)[:10]


# ============================================================
# Compare with previous state
# ============================================================
previous = load_previous_state()
prev_system = previous.get("system", {})
prev_processes = previous.get("processes", {})

issues = []
ignored = [
    "Process age alone is ignored.",
    "Docker / virtualization / container baseline usage is ignored unless behavior looks abnormal.",
    "Absolute disk-used GB is ignored unless near a real limit.",
]


# ============================================================
# Anomaly detection
# ============================================================

# 1. Memory pressure — look for worsening signals, not just high usage
swap_delta_mb = None
if isinstance(prev_system.get("swap_used_mb"), (int, float)):
    swap_delta_mb = round(swap_used_mb - prev_system["swap_used_mb"], 1)

memory_pressure_signals = []
if swap_delta_mb is not None and swap_delta_mb >= SWAP_GROWTH_ALERT_MB:
    memory_pressure_signals.append(f"swap grew {swap_delta_mb / 1024:.1f} GB since last run")
if swap_used_mb >= SWAP_USED_ALERT_MB and free_pressure_gb <= FREE_MEM_ALERT_GB:
    memory_pressure_signals.append(
        f"swap at {swap_used_mb / 1024:.1f} GB with only {free_pressure_gb:.2f} GB {'available' if IS_LINUX else 'truly free'}"
    )
if IS_MACOS and gb(compressed_bytes) >= COMPRESSED_ALERT_GB and free_pressure_gb <= FREE_MEM_ALERT_GB:
    memory_pressure_signals.append(
        f"compressed memory {gb(compressed_bytes):.1f} GB with only {free_pressure_gb:.2f} GB truly free"
    )

if memory_pressure_signals:
    details = {
        "swap_used_gb": round(swap_used_mb / 1024, 2),
        "swap_delta_gb": round((swap_delta_mb or 0) / 1024, 2) if swap_delta_mb is not None else None,
        "free_gb": gb(free_bytes),
    }
    if IS_LINUX:
        details["available_gb"] = gb(ram_available)
    if IS_MACOS:
        details["inactive_gb"] = gb(inactive_bytes)
        details["compressed_gb"] = gb(compressed_bytes)

    issues.append({
        "type": "memory_pressure",
        "severity": "watch" if len(memory_pressure_signals) == 1 else "investigate",
        "description": "Memory pressure looks real, not just high usage.",
        "why": "; ".join(memory_pressure_signals),
        "suggested_action": "Check which process is growing; consider restarting heavy services if pressure persists.",
        "details": details,
    })


# 2. Per-process anomalies
for proc in processes:
    pid = proc["pid"]
    if pid < 100 or should_ignore(proc["name"], proc["command"]):
        continue

    prev = prev_processes.get(str(pid), {})
    mem_delta_mb = proc["mem_mb"] - int(prev.get("mem_mb", proc["mem_mb"]))

    if proc["mem_mb"] >= RUNAWAY_MEM_ABS_MB:
        issues.append({
            "type": "runaway_memory",
            "severity": "investigate",
            "description": f"{proc['name']} (PID {pid}) is using {proc['mem_mb']} MB resident memory.",
            "why": "Large resident memory in a non-allowlisted process.",
            "suggested_action": "Inspect the process/logs; restart it if the usage is unexpected.",
            "details": proc,
        })
    elif prev and mem_delta_mb >= RUNAWAY_MEM_GROWTH_MB:
        issues.append({
            "type": "runaway_memory_growth",
            "severity": "investigate",
            "description": f"{proc['name']} (PID {pid}) grew by {mem_delta_mb} MB since last run.",
            "why": "Sustained memory growth is a stronger leak signal than absolute usage alone.",
            "suggested_action": "Re-check on next run; inspect/restart if growth continues.",
            "details": {**proc, "mem_delta_mb": mem_delta_mb},
        })

    if proc["cpu_pct"] >= SUSTAINED_CPU_PCT and proc["elapsed_secs"] >= SUSTAINED_CPU_MIN_ELAPSED:
        issues.append({
            "type": "sustained_cpu",
            "severity": "watch",
            "description": f"{proc['name']} (PID {pid}) has sustained {proc['cpu_pct']}% CPU for {proc['elapsed']}.",
            "why": "Short spikes are normal; sustained multi-core burn is more likely stuck or runaway.",
            "suggested_action": "Inspect what the process is doing before killing it.",
            "details": proc,
        })


# 3. Disk — only near a practical limit
if disk_pct >= DISK_USED_PCT_ALERT or disk_free_gb <= DISK_FREE_GB_ALERT:
    issues.append({
        "type": "disk_pressure",
        "severity": "investigate",
        "description": f"Root disk is at {disk_pct}% with {disk_free_gb} GB free.",
        "why": "Disk is only reported when it is actually close enough to matter.",
        "suggested_action": "Check logs, caches, Docker images, and tmp growth.",
        "details": {"mount": "/", "used_pct": disk_pct, "used_gb": disk_used_gb, "total_gb": disk_total_gb, "free_gb": disk_free_gb},
    })


# ============================================================
# Verdict
# ============================================================
severity_rank = {"watch": 1, "investigate": 2, "act_now": 3}
max_severity = max((severity_rank.get(issue.get("severity", "watch"), 1) for issue in issues), default=0)
verdict = "ok" if not issues else {1: "watch", 2: "investigate", 3: "act_now"}[max_severity]

# Build summary — shape varies slightly by OS
summary = {
    "ram": f"{gb(ram_used):.1f}/{gb(ram_total):.1f} GB ({ram_pct}%)",
    "swap": f"{swap_used_mb / 1024:.1f}/{swap_total_mb / 1024:.1f} GB",
    "swap_delta": f"{swap_delta_mb / 1024:+.1f} GB" if swap_delta_mb is not None else None,
    "load": f"{load[0]}/{load[1]}/{load[2]}",
    "cores": cores,
    "disk": f"{disk_used_gb}/{disk_total_gb} GB ({disk_pct}%)",
}
if IS_LINUX:
    summary["available"] = f"{gb(ram_available):.2f} GB available"
if IS_MACOS:
    summary["free"] = f"{gb(free_bytes):.2f} GB truly free"
    summary["inactive"] = f"{gb(inactive_bytes):.2f} GB inactive/speculative"
    summary["compressed"] = f"{gb(compressed_bytes):.2f} GB compressed"

result = {
    "suspicious": len(issues) > 0,
    "verdict": verdict,
    "os": platform.system(),
    "summary": summary,
    "issues": issues,
    "top_processes": top_processes,
    "ignored_normals": ignored,
}
print(json.dumps(result, indent=2))


# ============================================================
# Persist state for next-run deltas
# ============================================================
state = {
    "timestamp": int(time.time()),
    "system": {
        "swap_used_mb": swap_used_mb,
        "free_bytes": free_bytes,
        "disk_free_gb": disk_free_gb,
    },
    "processes": {
        str(p["pid"]): {
            "mem_mb": p["mem_mb"],
            "cpu_pct": p["cpu_pct"],
            "name": p["name"],
            "command": p["command"],
        }
        for p in processes
    },
}
if IS_LINUX:
    state["system"]["ram_available"] = ram_available
    state["system"]["ram_free"] = ram_free
if IS_MACOS:
    state["system"]["inactive_bytes"] = inactive_bytes
    state["system"]["compressed_bytes"] = compressed_bytes

save_state(state)
PYEOF
