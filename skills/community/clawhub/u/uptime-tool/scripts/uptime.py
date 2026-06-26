#!/usr/bin/env python3
with open('/proc/uptime') as f:
    secs = float(f.read().split()[0])
    days = int(secs // 86400)
    hours = int((secs % 86400) // 3600)
    mins = int((secs % 3600) // 60)
print(f"Up: {days}d {hours}h {mins}m")
