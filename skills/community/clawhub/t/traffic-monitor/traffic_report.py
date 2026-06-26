#!/usr/bin/env python3
"""Traffic usage report for OpenClaw heartbeat."""

import subprocess
import json
import os
from datetime import datetime

# Configuration
INTERFACE = "eth0"
MONTHLY_LIMIT_GB = 2048  # 2TB
WARNING_THRESHOLD = 0.80  # 80%
STATE_FILE = "/root/.openclaw/workspace/memory/traffic-state.json"

def get_proc_dev():
    """Get current interface stats from /proc/net/dev."""
    try:
        with open('/proc/net/dev', 'r') as f:
            for line in f:
                if f'{INTERFACE}:' in line:
                    parts = line.split(':')[1].split()
                    rx_bytes = int(parts[0])
                    tx_bytes = int(parts[8])
                    return rx_bytes, tx_bytes
    except Exception:
        pass
    return None, None

def get_vnstat_json():
    """Get traffic data from vnstat in JSON format."""
    try:
        result = subprocess.run(
            ["vnstat", "-i", INTERFACE, "--json", "m"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode != 0:
            return None
        return json.loads(result.stdout)
    except Exception as e:
        return None

def format_size(gb):
    """Format GB to human readable string."""
    if gb >= 1024:
        return f"{gb/1024:.2f} TB"
    return f"{gb:.1f} GB"

def load_state():
    """Load last reported threshold."""
    try:
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, 'r') as f:
                return json.load(f)
    except Exception:
        pass
    return {"last_reported_threshold": -1, "last_percentage": 0}

def save_state(state):
    """Save current state."""
    try:
        os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
        with open(STATE_FILE, 'w') as f:
            json.dump(state, f)
    except Exception:
        pass

def print_report(rx_gb, tx_gb, total_gb, percentage, month_name=None, year=None):
    """Print formatted traffic report."""
    remaining_gb = MONTHLY_LIMIT_GB - total_gb

    if month_name and year:
        print(f"📊 {year}年{month_name}流量统计")
    else:
        print("📊 流量统计")
    print("━" * 30)
    print(f"📥 入站: {format_size(rx_gb)}")
    print(f"📤 出站: {format_size(tx_gb)}")
    print("━" * 30)
    print(f"📦 总计: {format_size(total_gb)} / {format_size(MONTHLY_LIMIT_GB)} ({percentage:.1f}%)")
    print(f"📋 剩余: {format_size(remaining_gb)}")

    # Warning if over threshold
    if percentage >= WARNING_THRESHOLD * 100:
        print()
        print(f"⚠️  警告: 流量使用已超过 {WARNING_THRESHOLD*100:.0f}%!")

    # Progress bar
    bar_length = 30
    filled = int(bar_length * min(percentage, 100) / 100)
    bar = "█" * filled + "░" * (bar_length - filled)
    print()
    print(f"[{bar}] {percentage:.1f}%")

def main():
    import sys
    heartbeat_mode = "--heartbeat" in sys.argv

    # Try vnstat first
    data = get_vnstat_json()
    rx_gb, tx_gb, total_gb = 0, 0, 0
    percentage = 0
    month_name = None
    year = None
    use_vnstat = False

    if data and "interfaces" in data and data["interfaces"]:
        interface = data["interfaces"][0]
        months = interface.get("traffic", {}).get("months", [])

        if months:
            current = months[-1]
            year = current.get("year", datetime.now().year)
            month = current.get("month", datetime.now().month)

            rx_bytes = current.get("rx", 0)
            tx_bytes = current.get("tx", 0)
            total_bytes = rx_bytes + tx_bytes

            rx_gb = rx_bytes / (1024 ** 3)
            tx_gb = tx_bytes / (1024 ** 3)
            total_gb = rx_gb + tx_gb
            percentage = (total_gb / MONTHLY_LIMIT_GB) * 100

            month_names = ["", "一月", "二月", "三月", "四月", "五月", "六月",
                           "七月", "八月", "九月", "十月", "十一月", "十二月"]
            month_name = month_names[month] if month <= 12 else f"{month}月"
            use_vnstat = True

    # Fallback to /proc/net/dev - but this is cumulative since boot, not monthly!
    # We should NOT use this for monthly tracking, just show it as reference
    if not use_vnstat:
        rx_bytes, tx_bytes = get_proc_dev()
        if rx_bytes and tx_bytes:
            rx_gb = rx_bytes / (1024 ** 3)
            tx_gb = tx_bytes / (1024 ** 3)
            total_gb = rx_gb + tx_gb
            # percentage stays 0 since we don't have monthly data

    if total_gb == 0:
        print("❌ 无法获取流量数据")
        return

    # If we don't have vnstat data, show a message instead of misleading stats
    if not use_vnstat:
        print("⏳ vnstat 正在收集数据，暂无月度统计")
        print(f"   服务器启动以来累计: 📥{rx_gb:.1f}GB 📤{tx_gb:.1f}GB")
        print("   请等待几小时后再查询月度流量")
        return

    # Heartbeat mode: check if we should report
    if heartbeat_mode:
        state = load_state()
        last_threshold = state.get("last_reported_threshold", -1)  # -1 means never reported
        current_threshold = int(percentage // 10)  # 0, 1, 2, ... 10

        # Report if crossed a 10% boundary
        should_report = current_threshold > last_threshold

        # First time: DON'T report (changed from always report)
        # This prevents spam after restarts

        # Also report if over warning threshold
        if percentage >= WARNING_THRESHOLD * 100 and last_threshold < int(WARNING_THRESHOLD * 10):
            should_report = True

        if should_report:
            print_report(rx_gb, tx_gb, total_gb, percentage, month_name, year)
            state["last_reported_threshold"] = current_threshold
            state["last_percentage"] = percentage
            save_state(state)
        else:
            # Silent - no need to report
            pass
    else:
        # Normal mode: always print
        print_report(rx_gb, tx_gb, total_gb, percentage, month_name, year)

if __name__ == "__main__":
    main()
