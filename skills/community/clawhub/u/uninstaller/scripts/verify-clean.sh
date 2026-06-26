#!/usr/bin/env bash
# verify-clean.sh — Read-only check for OpenClaw residue. Safe for Agent to run.
# Does NOT delete anything.

set -e

STATE_DIR="${OPENCLAW_STATE_DIR:-$HOME/.openclaw}"
FOUND=0

echo "=== OpenClaw residue check (read-only) ==="
echo ""

# 1. State directory
if [[ -d "$STATE_DIR" ]]; then
  echo "[RESIDUE] State dir: $STATE_DIR"
  FOUND=1
else
  echo "[OK] State dir removed"
fi

# 2. Profile directories
PROFILE_FOUND=0
for d in "$HOME"/.openclaw-*; do
  [[ -d "$d" ]] || continue
  echo "[RESIDUE] Profile dir: $d"
  FOUND=1
  PROFILE_FOUND=1
done
if (( ! PROFILE_FOUND )); then
  echo "[OK] No profile residue"
fi

# 3. macOS launchd
if [[ "$(uname -s)" == "Darwin" ]]; then
  if launchctl print "gui/$UID/ai.openclaw.gateway" &>/dev/null; then
    echo "[RESIDUE] launchd service: ai.openclaw.gateway"
    FOUND=1
  elif [[ -f "$HOME/Library/LaunchAgents/ai.openclaw.gateway.plist" ]]; then
    echo "[RESIDUE] launchd plist: ~/Library/LaunchAgents/ai.openclaw.gateway.plist"
    FOUND=1
  else
    echo "[OK] macOS launchd cleaned"
  fi
fi

# 4. Linux systemd
if [[ "$(uname -s)" == "Linux" ]]; then
  if systemctl --user is-active openclaw-gateway.service &>/dev/null || \
     [[ -f "$HOME/.config/systemd/user/openclaw-gateway.service" ]]; then
    echo "[RESIDUE] systemd service: openclaw-gateway.service"
    FOUND=1
  else
    echo "[OK] systemd cleaned"
  fi
fi

# 5. npm global
if command -v npm &>/dev/null && npm list -g openclaw --depth=0 &>/dev/null; then
  echo "[RESIDUE] npm global: openclaw"
  FOUND=1
else
  echo "[OK] npm global removed"
fi

# 6. Processes (pgrep or ps fallback)
if command -v pgrep &>/dev/null; then
  if pgrep -f "openclaw" &>/dev/null; then
    echo "[RESIDUE] Running openclaw process"
    pgrep -af "openclaw" 2>/dev/null || true
    FOUND=1
  else
    echo "[OK] No openclaw process"
  fi
else
  if ps aux 2>/dev/null | grep -v grep | grep -q openclaw; then
    echo "[RESIDUE] Running openclaw process"
    ps aux 2>/dev/null | grep -v grep | grep openclaw || true
    FOUND=1
  else
    echo "[OK] No openclaw process"
  fi
fi

# 7. macOS app
if [[ "$(uname -s)" == "Darwin" ]] && [[ -d "/Applications/OpenClaw.app" ]]; then
  echo "[RESIDUE] macOS app: /Applications/OpenClaw.app"
  FOUND=1
elif [[ "$(uname -s)" == "Darwin" ]]; then
  echo "[OK] macOS app removed"
fi

echo ""
if (( FOUND )); then
  echo "Result: Residue found. See SKILL.md or run uninstall-oneshot.sh"
  exit 1
else
  echo "Result: Fully cleaned"
  exit 0
fi
