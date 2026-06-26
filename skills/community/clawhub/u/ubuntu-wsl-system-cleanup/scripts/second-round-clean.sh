#!/usr/bin/env bash
set -euo pipefail

TOOLS=(${@:-})
if [ ${#TOOLS[@]} -eq 0 ]; then
  echo "usage: second-round-clean.sh <tool-name> [tool-name...]" >&2
  exit 1
fi

echo "[scan] broken symlinks in ~/.local/bin"
find /root/.local/bin -xtype l -print 2>/dev/null || true

echo
for tool in "${TOOLS[@]}"; do
  echo "[scan] tool=$tool"
  echo "-- cache/config/share matches --"
  find /root/.cache /root/.config /root/.local/share /root/.openclaw/workspace/_trash \
    -maxdepth 4 \( -iname "*${tool}*" \) -print 2>/dev/null || true
  echo
  echo "-- config references --"
  grep -Rni "$tool" /root/.bashrc /root/.zshrc /root/.profile /root/.config /root/.openclaw/workspace 2>/dev/null || true
  echo
  echo "-- local bin matches --"
  ls -l /root/.local/bin 2>/dev/null | grep -i "$tool" || true
  echo
  echo "-- pipx venv matches --"
  find /root/.local/share/pipx/venvs -maxdepth 1 -iname "*${tool}*" -print 2>/dev/null || true
  echo
 done

echo "second-round scan complete"
