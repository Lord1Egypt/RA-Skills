#!/usr/bin/env bash
set -euo pipefail

SCRIPT_PATH="$(python3 -c 'import os,sys; print(os.path.realpath(sys.argv[1]))' "${BASH_SOURCE[0]}")"
SCRIPT_DIR="$(cd "$(dirname "$SCRIPT_PATH")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

resolve_skill_root() {
  local candidates=(
    "$(cd "$SCRIPT_DIR/.." && pwd)"
    "$REPO_ROOT"
    "$HOME/.openclaw/skills/wtt"
    "$HOME/.openclaw/skills/wtt-skill"
    "$HOME/.openclaw/workspace/skills/wtt-skill"
  )
  local c
  for c in "${candidates[@]}"; do
    if [[ -f "$c/start_wtt_autopoll.py" ]]; then
      echo "$c"
      return 0
    fi
  done
  return 1
}

SKILL_ROOT="$(resolve_skill_root || true)"
if [[ -z "$SKILL_ROOT" ]]; then
  echo "❌ start_wtt_autopoll.py not found. Checked:"
  echo "   - $(cd "$SCRIPT_DIR/.." && pwd)"
  echo "   - $REPO_ROOT"
  echo "   - $HOME/.openclaw/skills/wtt"
  echo "   - $HOME/.openclaw/skills/wtt-skill"
  echo "   - $HOME/.openclaw/workspace/skills/wtt-skill"
  exit 1
fi

START_SCRIPT="$SKILL_ROOT/start_wtt_autopoll.py"
WORKDIR="$SKILL_ROOT"
WRAPPER_SCRIPT="$SKILL_ROOT/run_autopoll.sh"

ensure_skill_venv() {
  local base_py
  base_py="$(command -v python3 || true)"
  if [[ -z "$base_py" ]]; then
    return 1
  fi

  if "$base_py" -m venv "$SKILL_ROOT/.venv" >/dev/null 2>&1; then
    return 0
  fi

  if [[ "$(uname -s)" == "Linux" ]] && [[ "${EUID:-$(id -u)}" == "0" ]] && command -v apt-get >/dev/null 2>&1; then
    echo "ℹ️  python venv unavailable, installing python3-venv prerequisites..."
    apt-get update -y >/dev/null 2>&1 || true
    apt-get install -y python3-venv python3.12-venv >/dev/null 2>&1 || true
    "$base_py" -m venv "$SKILL_ROOT/.venv" >/dev/null 2>&1 || return 1
    return 0
  fi

  return 1
}

# Resolve runtime python: explicit override > skill-local venv (with pip) > create/repair skill-local venv > fallback python3
PY_BIN="${PY_BIN:-}"
if [[ -z "$PY_BIN" ]]; then
  if [[ -x "$SKILL_ROOT/.venv/bin/python" ]]; then
    if "$SKILL_ROOT/.venv/bin/python" -m pip --version >/dev/null 2>&1; then
      PY_BIN="$SKILL_ROOT/.venv/bin/python"
    else
      echo "⚠️  Found broken .venv (pip missing), recreating..."
      rm -rf "$SKILL_ROOT/.venv"
      if ensure_skill_venv && [[ -x "$SKILL_ROOT/.venv/bin/python" ]]; then
        PY_BIN="$SKILL_ROOT/.venv/bin/python"
      fi
    fi
  fi

  if [[ -z "$PY_BIN" ]]; then
    if ensure_skill_venv && [[ -x "$SKILL_ROOT/.venv/bin/python" ]]; then
      PY_BIN="$SKILL_ROOT/.venv/bin/python"
    else
      PY_BIN="$(command -v python3 || true)"
    fi
  fi
fi

if [[ -z "$PY_BIN" || ! -x "$PY_BIN" ]]; then
  echo "❌ python executable not found (set PY_BIN=... to override)"
  exit 1
fi

OPENCLAW_BIN="${OPENCLAW_BIN:-$(command -v openclaw || true)}"
SERVICE_PATH="${PATH:-/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin}"
ENV_FILE="$SKILL_ROOT/.env"
if [[ -z "$OPENCLAW_BIN" ]]; then
  OPENCLAW_BIN="openclaw"
fi

ensure_python_deps() {
  if [[ "${WTT_SKIP_PIP_INSTALL:-0}" == "1" ]]; then
    echo "ℹ️  Skip python dependency install (WTT_SKIP_PIP_INSTALL=1)"
    return 0
  fi

  if ! "$PY_BIN" -m pip --version >/dev/null 2>&1; then
    "$PY_BIN" -m ensurepip --upgrade >/dev/null 2>&1 || true
  fi

  if ! "$PY_BIN" -m pip --version >/dev/null 2>&1; then
    local fallback_py="$HOME/.openclaw/workspace/skills/.venv311/bin/python"
    if [[ -x "$fallback_py" ]] && "$fallback_py" -m pip --version >/dev/null 2>&1; then
      echo "⚠️  pip unavailable on selected python; fallback to $fallback_py"
      PY_BIN="$fallback_py"
    else
      echo "❌ pip is unavailable for $PY_BIN and no fallback interpreter found"
      return 1
    fi
  fi

  local missing
  missing="$($PY_BIN - <<'PY'
import importlib.util
mods = ["httpx", "websockets", "dotenv", "socksio"]
print(" ".join([m for m in mods if importlib.util.find_spec(m) is None]))
PY
)"

  if [[ -z "${missing// }" ]]; then
    echo "✅ Python runtime deps already present (httpx, websockets, python-dotenv, socksio)"
    return 0
  fi

  local pip_args=("--disable-pip-version-check")
  if [[ "$PY_BIN" != "$SKILL_ROOT/.venv/bin/python" ]] && [[ -z "${VIRTUAL_ENV:-}" ]]; then
    pip_args+=("--user")
  fi

  echo "ℹ️  Installing python deps for wtt-skill: $missing"
  if ! "$PY_BIN" -m pip install "${pip_args[@]}" \
    "httpx>=0.24" \
    "websockets>=11" \
    "python-dotenv>=1" \
    "socksio>=1"; then
    echo "⚠️  Initial pip install failed, retry with --break-system-packages"
    "$PY_BIN" -m pip install --break-system-packages "${pip_args[@]}" \
      "httpx>=0.24" \
      "websockets>=11" \
      "python-dotenv>=1" \
      "socksio>=1"
  fi
  echo "✅ Python deps installed"
}

ensure_wrapper_script() {
  # Always refresh wrapper script to avoid stale logic from older installs.
  cat > "$WRAPPER_SCRIPT" <<'SH'
#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR="${WTT_SKILL_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)}"
cd "$SKILL_DIR"

is_py_ready() {
  local py="$1"
  [[ -x "$py" ]] || return 1
  "$py" - <<'PY' >/dev/null 2>&1
import importlib.util, sys
req = ("httpx", "websockets", "dotenv", "socksio")
missing = [m for m in req if importlib.util.find_spec(m) is None]
sys.exit(0 if not missing else 1)
PY
}

choose_py() {
  local c

  # Even when WTT_PY_BIN is set by systemd, verify deps before using it.
  if [[ -n "${WTT_PY_BIN:-}" ]] && is_py_ready "${WTT_PY_BIN}"; then
    echo "${WTT_PY_BIN}"
    return 0
  fi

  local candidates=(
    "$SKILL_DIR/.venv/bin/python"
    "$SKILL_DIR/.venv311/bin/python"
    "$HOME/.openclaw/workspace/skills/.venv311/bin/python"
    "$(command -v python3 || true)"
  )

  for c in "${candidates[@]}"; do
    if [[ -n "$c" ]] && is_py_ready "$c"; then
      echo "$c"
      return 0
    fi
  done

  # Last resort: keep previous behavior (will fail fast with clear error)
  if [[ -n "${WTT_PY_BIN:-}" ]] && [[ -x "${WTT_PY_BIN}" ]]; then
    echo "${WTT_PY_BIN}"
    return 0
  fi
  command -v python3
}

PY="$(choose_py)"
if [[ -z "$PY" || ! -x "$PY" ]]; then
  echo "❌ No runnable python found for wtt autopoll"
  exit 1
fi

if ! is_py_ready "$PY"; then
  echo "❌ Python missing required deps (httpx/websockets/python-dotenv/socksio): $PY"
  exit 1
fi

exec "$PY" "$SKILL_DIR/start_wtt_autopoll.py"
SH

  chmod +x "$WRAPPER_SCRIPT"
}

init_env_file() {
  local configured_agent_id="${WTT_AGENT_ID:-}"
  local configured_target="${WTT_IM_TARGET:-}"
  local configured_channel="${WTT_IM_CHANNEL:-telegram}"

  mkdir -p "$(dirname "$ENV_FILE")"

  # Prefer copying .env.example so comments/defaults remain visible.
  if [[ ! -f "$ENV_FILE" ]]; then
    if [[ -f "$SKILL_ROOT/.env.example" ]]; then
      cp "$SKILL_ROOT/.env.example" "$ENV_FILE"
    else
      cat > "$ENV_FILE" <<'EOF'
# Auto-generated by install_autopoll.sh
WTT_AGENT_ID=
WTT_IM_TARGET=
WTT_IM_CHANNEL=telegram
EOF
    fi
  fi

  # WTT_AGENT_ID policy:
  # - keep existing non-empty value
  # - if installer env explicitly provides one, write it
  # - if absent, keep empty and let runtime register via API
  if [[ -n "$configured_agent_id" ]]; then
    if grep -q '^WTT_AGENT_ID=' "$ENV_FILE"; then
      sed -i.bak "s|^WTT_AGENT_ID=.*|WTT_AGENT_ID=$configured_agent_id|" "$ENV_FILE" && rm -f "$ENV_FILE.bak"
    else
      printf "\nWTT_AGENT_ID=%s\n" "$configured_agent_id" >> "$ENV_FILE"
    fi
  else
    if ! grep -q '^WTT_AGENT_ID=' "$ENV_FILE"; then
      printf "\nWTT_AGENT_ID=\n" >> "$ENV_FILE"
    fi
  fi

  # WTT_IM_TARGET policy:
  # - do not overwrite existing non-empty value
  # - only fill when current value is empty and env provided target is non-empty
  if grep -q '^WTT_IM_TARGET=' "$ENV_FILE"; then
    local current_target
    current_target="$(grep '^WTT_IM_TARGET=' "$ENV_FILE" | tail -n1 | cut -d'=' -f2- | tr -d '\n\r')"
    if [[ -z "$current_target" && -n "$configured_target" ]]; then
      sed -i.bak "s|^WTT_IM_TARGET=.*|WTT_IM_TARGET=$configured_target|" "$ENV_FILE" && rm -f "$ENV_FILE.bak"
    fi
  else
    printf "WTT_IM_TARGET=%s\n" "$configured_target" >> "$ENV_FILE"
  fi

  # WTT_IM_CHANNEL policy:
  # - do not overwrite existing non-empty value
  # - fill if missing/empty
  if grep -q '^WTT_IM_CHANNEL=' "$ENV_FILE"; then
    local current_channel
    current_channel="$(grep '^WTT_IM_CHANNEL=' "$ENV_FILE" | tail -n1 | cut -d'=' -f2- | tr -d '\n\r')"
    if [[ -z "$current_channel" ]]; then
      sed -i.bak "s|^WTT_IM_CHANNEL=.*|WTT_IM_CHANNEL=$configured_channel|" "$ENV_FILE" && rm -f "$ENV_FILE.bak"
    fi
  else
    printf "WTT_IM_CHANNEL=%s\n" "$configured_channel" >> "$ENV_FILE"
  fi

  local final_agent_id final_target final_channel
  final_agent_id="$(grep '^WTT_AGENT_ID=' "$ENV_FILE" | tail -n1 | cut -d'=' -f2- | tr -d '\n\r' || true)"
  final_target="$(grep '^WTT_IM_TARGET=' "$ENV_FILE" | tail -n1 | cut -d'=' -f2- | tr -d '\n\r' || true)"
  final_channel="$(grep '^WTT_IM_CHANNEL=' "$ENV_FILE" | tail -n1 | cut -d'=' -f2- | tr -d '\n\r' || true)"

  echo "✅ Checked required .env keys: $ENV_FILE"
  echo "ℹ️  Effective env: agent_id=${final_agent_id:-'(empty, will auto-register at runtime)'} channel=${final_channel:-'(empty)'} target=${final_target:-'(empty)'}"
}

ensure_gateway_session_tools() {
  local mode="${WTT_GATEWAY_PATCH_MODE:-auto}"  # auto|check|off
  if [[ "$mode" == "off" ]]; then
    return 0
  fi

  if [[ -z "$OPENCLAW_BIN" ]] || ! command -v "$OPENCLAW_BIN" >/dev/null 2>&1; then
    echo "⚠️  openclaw binary not found; skip gateway.tools.allow check"
    return 0
  fi

  local cfg="${OPENCLAW_CONFIG_PATH:-$HOME/.openclaw/openclaw.json}"
  if [[ ! -f "$cfg" ]]; then
    echo "⚠️  openclaw config not found at $cfg; skip gateway permission check"
    return 0
  fi

  local pyout
  pyout="$(python3 - "$cfg" <<'PY'
import json, sys
p = sys.argv[1]
required = ["sessions_spawn", "sessions_send", "sessions_history", "sessions_list"]
with open(p, 'r', encoding='utf-8') as f:
    data = json.load(f)

gw = data.setdefault('gateway', {})
tools = gw.setdefault('tools', {})
allow = tools.get('allow')
if not isinstance(allow, list):
    allow = [] if allow is None else [str(allow)]

missing = [x for x in required if x not in allow]
changed = False
if missing:
    allow.extend(missing)
    tools['allow'] = allow
    changed = True

if changed:
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write('\n')

print('CHANGED=' + ('1' if changed else '0'))
print('MISSING=' + ','.join(missing))
PY
)"

  local changed missing
  changed="$(echo "$pyout" | sed -n 's/^CHANGED=//p' | tail -n1)"
  missing="$(echo "$pyout" | sed -n 's/^MISSING=//p' | tail -n1)"

  if [[ "$changed" == "1" ]]; then
    echo "✅ Patched gateway.tools.allow in $cfg"
    echo "   Added: ${missing}"
    if [[ "$mode" == "auto" ]]; then
      echo "ℹ️  Restarting gateway to apply permission changes..."
      "$OPENCLAW_BIN" gateway restart || true
    else
      echo "ℹ️  Run: openclaw gateway restart"
    fi
  else
    echo "✅ gateway.tools.allow already includes required session tools"
  fi
}

echo "ℹ️  REPO_ROOT:       $REPO_ROOT"
echo "ℹ️  SKILL_ROOT:      $SKILL_ROOT"
echo "ℹ️  WORKDIR:         $WORKDIR"
echo "ℹ️  START_SCRIPT:    $START_SCRIPT"
echo "ℹ️  WRAPPER_SCRIPT:  $WRAPPER_SCRIPT"
echo "ℹ️  PY_BIN(selected): $PY_BIN"

autostart_mac() {
  local plist="$HOME/Library/LaunchAgents/com.openclaw.wtt.autopoll.plist"
  local label="com.openclaw.wtt.autopoll"
  local uid
  uid="$(id -u)"
  local domains=("gui/$uid" "user/$uid")
  mkdir -p "$HOME/Library/LaunchAgents"

  cat > "$plist" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
  <dict>
    <key>Label</key>
    <string>$label</string>

    <key>ProgramArguments</key>
    <array>
      <string>$WRAPPER_SCRIPT</string>
    </array>

    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>

    <key>EnvironmentVariables</key>
    <dict>
      <key>PATH</key>
      <string>$SERVICE_PATH</string>
      <key>OPENCLAW_BIN</key>
      <string>$OPENCLAW_BIN</string>
      <key>WTT_SKILL_DIR</key>
      <string>$SKILL_ROOT</string>
    </dict>

    <key>StandardOutPath</key>
    <string>/tmp/wtt_autopoll.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/wtt_autopoll_error.log</string>
  </dict>
</plist>
PLIST

  local d
  for d in "${domains[@]}"; do
    launchctl bootout "$d/$label" >/dev/null 2>&1 || true
  done

  for d in "${domains[@]}"; do
    if launchctl bootstrap "$d" "$plist" >/dev/null 2>&1; then
      launchctl kickstart -k "$d/$label" >/dev/null 2>&1 || true
      # Give process a moment to start before checking state
      sleep 2
      if launchctl print "$d/$label" 2>/dev/null | grep -q "state = running"; then
        echo "✅ macOS launchd service installed (domain: $d)"
        launchctl list | grep "$label" || true
        return 0
      fi
      # Bootstrap succeeded even if state check failed — don't try another domain
      echo "✅ macOS launchd service bootstrapped (domain: $d)"
      launchctl list | grep "$label" || true
      return 0
    fi
  done

  # If already loaded, try to force start.
  if launchctl list | grep -q "$label"; then
    for d in "${domains[@]}"; do
      launchctl kickstart -k "$d/$label" >/dev/null 2>&1 || true
      if launchctl print "$d/$label" 2>/dev/null | grep -q "state = running"; then
        echo "✅ macOS launchd service already loaded and running"
        launchctl list | grep "$label" || true
        return 0
      fi
    done
  fi

  if pgrep -f "$SKILL_ROOT/start_wtt_autopoll.py" >/dev/null 2>&1; then
    echo "✅ autopoll process already running (non-launchd fallback)"
    return 0
  fi

  echo "⚠️  launchd not available in current context, trying direct background fallback..."
  nohup "$WRAPPER_SCRIPT" >/tmp/wtt_autopoll.log 2>/tmp/wtt_autopoll_error.log &
  # Wait a bit longer for Python cold start in constrained environments.
  local i
  for i in 1 2 3 4 5; do
    sleep 1
    if pgrep -f "$SKILL_ROOT/start_wtt_autopoll.py" >/dev/null 2>&1; then
      echo "✅ autopoll started via direct background fallback"
      return 0
    fi
  done

  if [[ "${WTT_ALLOW_DEFERRED_LAUNCHD:-0}" == "1" ]]; then
    echo "⚠️  launchd start deferred; plist written but service not running yet"
    echo "   Plist: $plist"
    echo "   Try: launchctl bootstrap gui/$uid $plist && launchctl kickstart -k gui/$uid/$label"
    return 0
  fi

  echo "❌ Failed to start autopoll automatically"
  echo "   Plist: $plist"
  echo "   Tried domains: ${domains[*]}"
  echo "   Direct fallback also failed"
  return 1
}

autostart_linux() {
  local unit_dir="$HOME/.config/systemd/user"
  local unit="$unit_dir/wtt-autopoll.service"
  mkdir -p "$unit_dir"

  cat > "$unit" <<UNIT
[Unit]
Description=OpenClaw WTT Auto Poll
After=network-online.target

[Service]
Type=simple
ExecStart=$WRAPPER_SCRIPT
Restart=always
RestartSec=2
Environment="PATH=$SERVICE_PATH"
Environment="OPENCLAW_BIN=$OPENCLAW_BIN"
Environment="HOME=$HOME"
Environment="WTT_SKILL_DIR=$SKILL_ROOT"
WorkingDirectory=$WORKDIR
StandardOutput=append:/tmp/wtt_autopoll.log
StandardError=append:/tmp/wtt_autopoll_error.log

[Install]
WantedBy=default.target
UNIT

  # Clean stale standalone processes before restarting managed service.
  pkill -f "$SKILL_ROOT/start_wtt_autopoll.py" >/dev/null 2>&1 || true
  rm -f "$SKILL_ROOT/.autopoll.pid" >/dev/null 2>&1 || true

  systemctl --user daemon-reload
  systemctl --user enable --now wtt-autopoll.service
  systemctl --user reset-failed wtt-autopoll.service || true
  systemctl --user restart wtt-autopoll.service

  # Keep only one process: the systemd MainPID.
  local main_pid pids pid count
  sleep 1
  main_pid="$(systemctl --user show wtt-autopoll.service -p MainPID --value 2>/dev/null || echo 0)"
  pids="$(pgrep -f "$SKILL_ROOT/start_wtt_autopoll.py" || true)"
  for pid in $pids; do
    if [[ -n "$main_pid" && "$main_pid" != "0" && "$pid" != "$main_pid" ]]; then
      kill "$pid" >/dev/null 2>&1 || true
    fi
  done

  count="$(pgrep -f "$SKILL_ROOT/start_wtt_autopoll.py" | wc -l | tr -d ' ')"
  if [[ "$count" != "1" ]]; then
    echo "❌ Expected exactly 1 autopoll process, found $count"
    systemctl --user status wtt-autopoll.service --no-pager || true
    return 1
  fi

  echo "✅ Linux systemd user service installed"
  systemctl --user status wtt-autopoll.service --no-pager || true
}

init_env_file
ensure_wrapper_script
ensure_python_deps
ensure_gateway_session_tools

case "$(uname -s)" in
  Darwin)
    autostart_mac
    ;;
  Linux)
    autostart_linux
    ;;
  *)
    echo "❌ Unsupported OS: $(uname -s)"
    exit 1
    ;;
esac

echo "✅ WTT auto_poll autostart configured"