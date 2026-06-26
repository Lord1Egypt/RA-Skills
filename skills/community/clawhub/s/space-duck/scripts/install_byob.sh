#!/usr/bin/env bash
# Space Duck — one-shot BYOB host installer.
#
# Bootstraps a new BYOB (Lane A) host from zero to fully operational:
#   1. Verifies prerequisites (python ≥3.10, node, claude CLI)
#   2. Installs clawhub if missing
#   3. Installs the space-duck skill via clawhub
#   4. Walks the operator through pair.py (interactive)
#   5. Sets up BYOB workspace bridge + tunnel
#   6. Installs supervised listeners (telegram_listener + peck_listener)
#   7. Reports final state and how to verify
#
# DESIGN — security:
#   • This script is meant to be hosted at a stable HTTPS URL and run via:
#       curl -fsSL <URL> | bash
#     Production deployment should pin the script's SHA256 in the curl
#     command and document the source at a known location.
#   • Sensitive inputs (beak_key, Cognito JWT) come ONLY via env vars,
#     never CLI args, to avoid leaking through `ps aux` and shell history.
#   • Every external dependency (clawhub, claude CLI, supervisord) is
#     installed from its publisher's official channel; no third-party
#     mirrors.
#
# DESIGN — idempotency:
#   • Re-running is safe. Each step detects existing state and either
#     skips (already done) or repairs (broken state).
#   • Use --reset to wipe the install and start over.
#
# Usage (interactive — preferred):
#   export SD_OWNER_EMAIL='you@example.com'   # for Cognito sign-in
#   bash <(curl -fsSL https://spaceduckling.com/install/byob.sh)
#
# Usage (scripted — for re-provisioning):
#   export SD_OWNER_EMAIL='you@example.com'
#   export SPACEDUCK_BEAK_KEY='bk_LIVE_...'   # if you already have one
#   export SD_AGENT_NAME='Wayne'              # duck display name
#   bash install_byob.sh --no-prompt
#
# DESIGN — what this script does NOT do:
#   • Provision the cloud machine (you should already have a host)
#   • Configure DNS / domain
#   • Set up monitoring / alerting
#   • Configure a NAMED cloudflared tunnel (uses quick tunnel by default;
#     warns that quick tunnels drift on restart)

set -euo pipefail

# ─────────────────────────── config ───────────────────────────
SD_DIR="${HOME}/.space-duck"
SKILL_DIR="${HOME}/.clawhub/skills/space-duck"
LOG_PREFIX="[install_byob]"

# CLI flag parsing
NO_PROMPT=0
RESET=0
SKIP_BRIDGE=0
SKIP_LISTENERS=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --no-prompt)      NO_PROMPT=1; shift;;
    --reset)          RESET=1; shift;;
    --skip-bridge)    SKIP_BRIDGE=1; shift;;
    --skip-listeners) SKIP_LISTENERS=1; shift;;
    --help|-h)
      sed -n '2,42p' "$0" | sed 's/^# \?//'
      exit 0;;
    *) echo "✗ unknown arg: $1 (try --help)" >&2; exit 2;;
  esac
done

die()  { echo "${LOG_PREFIX} ✗ $*" >&2; exit 1; }
ok()   { echo "${LOG_PREFIX} ✓ $*"; }
info() { echo "${LOG_PREFIX} → $*"; }
warn() { echo "${LOG_PREFIX} ⚠ $*" >&2; }

prompt() {
  # prompt "Question " VAR_NAME
  local q="$1" var="$2"
  if [[ "$NO_PROMPT" == "1" ]]; then
    [[ -n "${!var:-}" ]] || die "non-interactive mode but \$${var} not set: $q"
    return
  fi
  read -rp "$q" "$var"
}

# ─────────────────────────── step 0: reset (if requested) ─────
if [[ "$RESET" == "1" ]]; then
  warn "RESET requested — will remove ~/.space-duck/ and supervised listeners"
  if [[ "$NO_PROMPT" != "1" ]]; then
    read -rp "Confirm reset (type 'yes' to proceed): " confirm
    [[ "$confirm" == "yes" ]] || die "aborted by user"
  fi
  [[ -x "${SKILL_DIR}/scripts/setup_listeners_supervised.sh" ]] && \
    "${SKILL_DIR}/scripts/setup_listeners_supervised.sh" --uninstall || true
  rm -rf "$SD_DIR"
  ok "Reset complete."
  exit 0
fi

# ─────────────────────────── step 1: environment detection ────
info "Detecting environment..."

OS_KERNEL="$(uname -s)"
case "$OS_KERNEL" in
  Linux)
    # Detect container vs full VM
    if [[ -f /.dockerenv ]] || grep -qE '(docker|lxc|containerd)' /proc/1/cgroup 2>/dev/null; then
      ENV_KIND="container"
    elif command -v systemctl >/dev/null && systemctl is-system-running --quiet 2>/dev/null; then
      ENV_KIND="vps_systemd"
    else
      ENV_KIND="linux_other"
    fi
    ;;
  Darwin) ENV_KIND="macos_dev";;
  *) die "unsupported OS: $OS_KERNEL — Linux/macOS only";;
esac
ok "Environment: $ENV_KIND"

# ─────────────────────────── step 2: prereqs ──────────────────
info "Checking prereqs..."

command -v python3 >/dev/null || die "python3 not installed — apt-get install python3 (or equivalent)"
PYMAJOR=$(python3 -c 'import sys; print(sys.version_info[0])')
PYMINOR=$(python3 -c 'import sys; print(sys.version_info[1])')
{ [[ "$PYMAJOR" -gt 3 ]] || [[ "$PYMAJOR" -eq 3 && "$PYMINOR" -ge 10 ]]; } \
  || die "python3 $PYMAJOR.$PYMINOR too old; need ≥ 3.10"
ok "python3 $PYMAJOR.$PYMINOR"

command -v node >/dev/null || die "node not installed — see https://nodejs.org"
NODE_VER=$(node -v | sed 's/^v//')
ok "node $NODE_VER"

# claude CLI is required by peck_responder. Warn if missing.
if command -v claude >/dev/null; then
  CLAUDE_VER=$(claude --version 2>&1 | head -1)
  ok "claude CLI: $CLAUDE_VER"
else
  warn "claude CLI not on PATH — peck_responder will fail to compose replies"
  warn "Install: https://docs.claude.com/en/docs/claude-code"
  if [[ "$NO_PROMPT" != "1" ]]; then
    read -rp "Continue anyway? (yes/no): " cont
    [[ "$cont" == "yes" ]] || die "aborted — install claude CLI first"
  fi
fi

# cloudflared for the BYOB tunnel
if ! command -v cloudflared >/dev/null; then
  warn "cloudflared not installed — required for the BYOB tunnel"
  case "$ENV_KIND" in
    container|linux_other|vps_systemd)
      info "Install: curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -o /usr/local/bin/cloudflared && chmod +x /usr/local/bin/cloudflared"
      ;;
    macos_dev)
      info "Install: brew install cloudflare/cloudflare/cloudflared"
      ;;
  esac
  if [[ "$NO_PROMPT" != "1" ]]; then
    read -rp "Continue without cloudflared? (yes/no): " cont
    [[ "$cont" == "yes" ]] || die "aborted — install cloudflared first"
  fi
  SKIP_BRIDGE=1
fi

# ─────────────────────────── step 3: install clawhub ──────────
if ! command -v clawhub >/dev/null; then
  info "Installing @clawhub/cli via npm..."
  npm install -g @clawhub/cli || die "clawhub install failed — ensure npm has write access (try sudo or nvm)"
fi
CLAWHUB_VER=$(clawhub --version 2>&1 | head -1)
ok "clawhub: $CLAWHUB_VER"

# ─────────────────────────── step 4: install the skill ────────
if [[ ! -d "$SKILL_DIR" ]]; then
  info "Installing space-duck skill via clawhub..."
  clawhub install space-duck || die "clawhub install space-duck failed"
fi
SKILL_VER=$(python3 -c "import json,sys; print(json.load(open('${SKILL_DIR}/_meta.json'))['version'])" 2>/dev/null || echo "unknown")
ok "space-duck skill: v$SKILL_VER at $SKILL_DIR"

# ─────────────────────────── step 5: pair the duck ────────────
if [[ -f "${SD_DIR}/config.json" ]] && python3 -c "import json; d=json.load(open('${SD_DIR}/config.json')); assert d.get('beak_key','').startswith('bk_LIVE_')" 2>/dev/null; then
  EXISTING_SD=$(python3 -c "import json; print(json.load(open('${SD_DIR}/config.json')).get('spaceduck_id',''))")
  EXISTING_NAME=$(python3 -c "import json; print(json.load(open('${SD_DIR}/config.json')).get('agent_name',''))")
  ok "Already paired: $EXISTING_NAME ($EXISTING_SD) — skipping pair step"
else
  info "Pairing this host with a Space Duck identity..."
  if [[ "$NO_PROMPT" == "1" ]]; then
    [[ -n "${SPACEDUCK_BEAK_KEY:-}" && -n "${SD_AGENT_NAME:-}" ]] \
      || die "non-interactive mode needs SPACEDUCK_BEAK_KEY + SD_AGENT_NAME env vars"
    info "Writing config from env vars..."
    mkdir -p "$SD_DIR"
    python3 -c "
import json, os, pathlib
cfg = {
    'beak_key': os.environ['SPACEDUCK_BEAK_KEY'],
    'agent_name': os.environ['SD_AGENT_NAME'],
    'api_base': 'https://beak.spaceduckling.com',
}
p = pathlib.Path(os.path.expanduser('~/.space-duck/config.json'))
p.parent.mkdir(parents=True, exist_ok=True)
p.write_text(json.dumps(cfg, indent=2))
p.chmod(0o600)
print(f'  wrote {p}')
"
    ok "Pairing written from env"
  else
    info "Running pair.py interactively (foreground — DO NOT background)"
    info "It will print a 6-digit code + URL. Visit the URL in your browser and enter the code."
    python3 "${SKILL_DIR}/scripts/pair.py" || die "pair.py failed"
  fi
fi

# ─────────────────────────── step 6: workspace bridge + tunnel ─
if [[ "$SKIP_BRIDGE" != "1" ]]; then
  info "Setting up BYOB workspace bridge + tunnel..."
  warn "Quick tunnels (trycloudflare) drift on restart — DEV ONLY."
  warn "For production: configure a named cloudflared tunnel + persistent URL."

  if [[ "$NO_PROMPT" != "1" ]]; then
    read -rp "Continue with quick tunnel? (yes/no): " cont
    [[ "$cont" == "yes" ]] || { warn "Skipping bridge setup — run setup_byob_bridge.sh manually later"; SKIP_BRIDGE=1; }
  fi

  if [[ "$SKIP_BRIDGE" != "1" ]]; then
    [[ -n "${SD_JWT:-}" ]] || die "export SD_JWT='<your MC sd_token>' (from spaceduckling.com browser localStorage)"
    [[ -n "${SPACEDUCK_BEAK_KEY:-}" ]] || die "export SPACEDUCK_BEAK_KEY='bk_LIVE_...' (or skip with --skip-bridge)"
    SDID=$(python3 -c "import json; print(json.load(open('${SD_DIR}/config.json')).get('spaceduck_id',''))")
    [[ -n "$SDID" ]] || die "could not read spaceduck_id from config — pair first"
    "${SKILL_DIR}/scripts/setup_byob_bridge.sh" --duck-id "$SDID" \
      || warn "Bridge setup encountered errors — check output above"
  fi
fi

# ─────────────────────────── step 7: supervised listeners ──────
if [[ "$SKIP_LISTENERS" != "1" ]]; then
  info "Installing supervised listeners (auto-restart on failure)..."
  "${SKILL_DIR}/scripts/setup_listeners_supervised.sh" \
    || die "listener supervision setup failed"
fi

# ─────────────────────────── step 8: final report ──────────────
echo ""
echo "══════════════════════════════════════════════════════════"
echo "  Space Duck BYOB host install — COMPLETE"
echo "══════════════════════════════════════════════════════════"

if [[ -f "${SD_DIR}/config.json" ]]; then
  python3 -c "
import json
d = json.load(open('${SD_DIR}/config.json'))
print(f'  Duck:          {d.get(\"agent_name\", \"unnamed\")} ({d.get(\"spaceduck_id\", \"unknown\")})')
print(f'  Duckling:      {d.get(\"duckling_id\", \"unknown\")}')
print(f'  Skill version: ${SKILL_VER}')
print(f'  Environment:   ${ENV_KIND}')
"
fi

echo ""
echo "─── Verify ───"
echo "  Listener status: ${SKILL_DIR}/scripts/setup_listeners_supervised.sh --status"
echo "  Recent pecks:    python3 ${SKILL_DIR}/scripts/check_pecks.py"
echo "  Pulse to server: python3 ${SKILL_DIR}/scripts/pulse.py"
echo ""
echo "─── If anything's wrong ───"
echo "  Listener logs:   tail -f ~/.space-duck/logs/*.log"
echo "  Reset everything: $0 --reset"
echo ""
echo "─── For production ───"
echo "  Replace the quick tunnel with a named cloudflared tunnel before going live."
echo "  Add this to your container entrypoint so listeners survive restart:"
echo "    ~/.local/bin/supervisord -c ~/.space-duck/supervisor/supervisord.conf"
echo ""
