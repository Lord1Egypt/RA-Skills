#!/usr/bin/env bash
set -euo pipefail

report_size() {
  du -sh "$@" 2>/dev/null || true
}

echo "[before]"
df -h / || true
report_size /var/cache/apt /var/lib/apt/lists /var/log /tmp /var/tmp /root/.npm /root/.cache
journalctl --disk-usage 2>/dev/null || true

echo
echo "[clean] apt cache"
apt-get clean || true
rm -rf /var/lib/apt/lists/* || true
mkdir -p /var/lib/apt/lists/partial

echo
echo "[clean] journald"
journalctl --vacuum-time=7d 2>/dev/null || true
journalctl --vacuum-size=200M 2>/dev/null || true

echo
echo "[clean] temp directories"
find /tmp -xdev -mindepth 1 -mtime +3 -print -exec rm -rf {} + 2>/dev/null || true
find /var/tmp -xdev -mindepth 1 -mtime +7 -print -exec rm -rf {} + 2>/dev/null || true

echo
echo "[clean] npm cache"
if command -v npm >/dev/null 2>&1; then
  npm cache clean --force || true
fi
rm -rf /root/.npm/_npx 2>/dev/null || true

echo
echo "[clean] common user caches"
rm -rf /root/.cache/pip 2>/dev/null || true
rm -rf /root/.cache/thumbnails 2>/dev/null || true
find /root/.cache -maxdepth 1 -type d -name 'tmp*' -prune -exec rm -rf {} + 2>/dev/null || true

echo
echo "[after]"
df -h / || true
report_size /var/cache/apt /var/lib/apt/lists /var/log /tmp /var/tmp /root/.npm /root/.cache
journalctl --disk-usage 2>/dev/null || true

echo "safe cleanup complete"
