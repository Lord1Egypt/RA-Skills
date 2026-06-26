#!/usr/bin/env bash
set -euo pipefail

echo "== uptime =="
uptime

echo
echo "== memory =="
free -h

echo
echo "== disk =="
df -h /

echo
echo "== cpu top =="
ps -eo pid,ppid,cmd,%cpu,%mem --sort=-%cpu | head -15

echo
echo "== mem top =="
ps -eo pid,ppid,cmd,%cpu,%mem --sort=-%mem | head -15

echo
echo "== loadavg =="
cat /proc/loadavg
