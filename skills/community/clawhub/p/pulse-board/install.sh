#!/usr/bin/env bash
# Pulse Board — install.sh
# Interactive installer. Run once. Does everything.
# No sudo. No root. No system path writes outside ~/.pulse-board/
#
# What this script does — in full:
#   1. Creates ~/.pulse-board/{config,logs,registry,locks}
#   2. Writes ~/.pulse-board/config/pulse.yaml (once — never overwrites)
#   3. Adds two digest cron entries to your user crontab
#   4. Optionally appends LLM_API_KEY and OPENCLAW_WORKSPACE to your
#      secrets env file — only if you confirm at the prompt.
#
# Nothing is written silently. Every change is announced before it happens.

set -uo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PULSE_HOME="${PULSE_HOME:-$HOME/.pulse-board}"

# ── UI helpers ────────────────────────────────────────────────────────────────
green()  { printf "\033[0;32m%s\033[0m\n" "$*"; }
yellow() { printf "\033[0;33m%s\033[0m\n" "$*"; }
blue()   { printf "\033[0;34m%s\033[0m\n" "$*"; }
dim()    { printf "\033[2m%s\033[0m\n"    "$*"; }
red()    { printf "\033[0;31m%s\033[0m\n" "$*"; }

ask() {
  local prompt="$1" default="${2:-}"
  if [[ -n "$default" ]]; then
    printf "  \033[1m→\033[0m %s \033[2m[%s]\033[0m: " "$prompt" "$default"
  else
    printf "  \033[1m→\033[0m %s: " "$prompt"
  fi
  read -r REPLY </dev/tty
  [[ -z "$REPLY" ]] && REPLY="$default"
}

ask_choice() {
  local prompt="$1"; shift
  local options=("$@")
  printf "  \033[1m→\033[0m %s\n" "$prompt"
  local i=1
  for opt in "${options[@]}"; do
    printf "    \033[2m%s)\033[0m %s\n" "$i" "$opt"
    i=$(( i + 1 ))
  done
  printf "  Choice: "
  read -r REPLY </dev/tty
  REPLY="${options[$((REPLY - 1))]}"
}

confirm() {
  printf "  \033[1m→\033[0m %s \033[2m[Y/n]\033[0m: " "$1"
  read -r REPLY </dev/tty
  [[ "${REPLY:-y}" =~ ^[Yy]$ ]]
}

# ── Banner ────────────────────────────────────────────────────────────────────
clear
echo ""
blue "  ╔══════════════════════════════════════════╗"
blue "  ║          📋  Pulse Board                 ║"
blue "  ║    Operational heartbeat for your        ║"
blue "  ║         agent skill stack.               ║"
blue "  ╚══════════════════════════════════════════╝"
echo ""
dim "  Every cron job. One digest."
echo ""

# ── Already installed? ────────────────────────────────────────────────────────
if [[ -f "$PULSE_HOME/config/pulse.yaml" ]]; then
  yellow "  Pulse Board is already installed at $PULSE_HOME"
  if ! confirm "Re-run installer? (config will not be overwritten)"; then
    echo ""; dim "  Nothing changed."; echo ""; exit 0
  fi
fi

# ── Step 1: Timezone ──────────────────────────────────────────────────────────
echo ""
blue "  [ 1 / 7 ]  Timezone"
echo ""

DETECTED_TZ=""
[[ -f /etc/timezone ]] && DETECTED_TZ="$(cat /etc/timezone | tr -d '[:space:]')"
[[ -z "$DETECTED_TZ" && -L /etc/localtime ]] && \
  DETECTED_TZ="$(readlink /etc/localtime | sed 's|.*/zoneinfo/||')"
[[ -z "$DETECTED_TZ" ]] && DETECTED_TZ="UTC"

ask "Timezone" "$DETECTED_TZ"
TIMEZONE="$REPLY"

# ── Step 2: Delivery channel ──────────────────────────────────────────────────
echo ""
blue "  [ 2 / 7 ]  Digest delivery"
echo ""

ask_choice "Where should digests be delivered?" "telegram" "discord" "log file only"
CHANNEL="$REPLY"

BOT_TOKEN="" CHAT_ID="" THREAD_ID="" DISCORD_WEBHOOK=""

case "$CHANNEL" in
  telegram)
    echo ""
    ENV_TOKEN="${PULSE_TELEGRAM_BOT_TOKEN:-}"
    if [[ -n "$ENV_TOKEN" ]]; then
      dim "  Bot token found in environment (PULSE_TELEGRAM_BOT_TOKEN)."
      ask "Use a different token? Leave blank to use env" ""
      BOT_TOKEN="${REPLY:-}"
    else
      dim "  Paste your bot token from @BotFather."
      dim "  Or leave blank and set PULSE_TELEGRAM_BOT_TOKEN in your env file."
      ask "Bot token" ""
      BOT_TOKEN="$REPLY"
    fi
    echo ""
    dim "  Your group or channel chat ID — enter numbers only, no minus sign."
    ask "Chat ID (e.g. 100xxxxxxxxxx)" ""
    CHAT_ID="-${REPLY}"
    echo ""
    dim "  Only needed for Telegram forum groups with topics."
    ask "Thread / topic ID (leave blank if unsure)" ""
    THREAD_ID="$REPLY"
    ;;
  discord)
    echo ""
    dim "  Paste your Discord channel webhook URL."
    dim "  Or leave blank and set PULSE_DISCORD_WEBHOOK_URL in your env file."
    ask "Webhook URL" ""
    DISCORD_WEBHOOK="$REPLY"
    ;;
  "log file only")
    CHANNEL="log"
    ;;
esac

# ── Step 3: Digest schedule ───────────────────────────────────────────────────
echo ""
blue "  [ 3 / 7 ]  Digest schedule"
echo ""
dim "  Pulse Board posts a digest twice daily."
echo ""

ask "Morning digest hour (0-23)" "6"
MORNING_H="$REPLY"
ask "Morning digest minute (0-59)" "0"
MORNING_M="$REPLY"

ask "Evening digest hour (0-23)" "18"
EVENING_H="$REPLY"
ask "Evening digest minute (0-59)" "0"
EVENING_M="$REPLY"

# ── Step 4: OpenClaw cron directory ──────────────────────────────────────────
echo ""
blue "  [ 4 / 7 ]  Cron discovery"
echo ""
dim "  Directory where OpenClaw stores its registered cron jobs."
echo ""

ask "OpenClaw cron directory" "$HOME/.openclaw/cron"
OPENCLAW_CRON_DIR="$REPLY"

# ── Step 5: Secrets env file ──────────────────────────────────────────────────
echo ""
blue "  [ 5 / 7 ]  Secrets env file"
echo ""
dim "  Path to your secrets env file. Will be sourced before each skill runs."
dim "  Leave blank to skip."
echo ""

ask "Secrets env file" "$HOME/.openclaw/shared/secrets/openclaw-secrets.env"
SECRETS_ENV="$REPLY"

# ── Step 6: OpenClaw workspace ────────────────────────────────────────────────
echo ""
blue "  [ 6 / 7 ]  OpenClaw workspace"
echo ""
dim "  Absolute path to your OpenClaw agent workspace."
dim "  Used by skills like Total Recall to locate memory and log directories."
echo ""

ask "OpenClaw workspace" "$HOME/.openclaw/workspace"
OPENCLAW_WORKSPACE="$REPLY"

# ── Step 7: Digest agent ──────────────────────────────────────────────────────
echo ""
blue "  [ 7 / 7 ]  Digest agent"
echo ""
dim "  Pulse Board uses an OpenClaw agent to compose human-readable digests."
dim "  The agent receives the raw log and writes a natural language summary."
dim "  Falls back to mechanical format if the agent call fails."
echo ""

# Try to list available agents for the user
if command -v openclaw &>/dev/null; then
  dim "  Available agents:"
  openclaw agents list 2>/dev/null | grep "^-" | sed 's/^/    /' || true
  echo ""
fi

ask "Agent ID for digest composition" "main"
DIGEST_AGENT="$REPLY"

ask "Agent call timeout in seconds" "60"
DIGEST_TIMEOUT="$REPLY"

# ── Create directory structure ────────────────────────────────────────────────
echo ""
blue "  Installing..."
echo ""

mkdir -p \
  "$PULSE_HOME/config" \
  "$PULSE_HOME/registry" \
  "$PULSE_HOME/logs/detail" \
  "$PULSE_HOME/locks"

touch "$PULSE_HOME/logs/pending.log"
green "  ✓ Directories created at $PULSE_HOME"

# ── Write config ──────────────────────────────────────────────────────────────
CONFIG_FILE="$PULSE_HOME/config/pulse.yaml"

if [[ ! -f "$CONFIG_FILE" ]]; then
  TELEGRAM_ENABLED="false"
  DISCORD_ENABLED="false"
  LOG_ENABLED="true"

  [[ "$CHANNEL" == "telegram" ]] && TELEGRAM_ENABLED="true" && LOG_ENABLED="false"
  [[ "$CHANNEL" == "discord"  ]] && DISCORD_ENABLED="true"  && LOG_ENABLED="false"

  cat > "$CONFIG_FILE" <<EOF
# Pulse Board Configuration — generated by install.sh
# Edit freely. Re-running install.sh will not overwrite this file.

pulse_home: $PULSE_HOME
openclaw_cron_dir: $OPENCLAW_CRON_DIR
openclaw_workspace: $OPENCLAW_WORKSPACE
secrets_env: $SECRETS_ENV

paths:
  pending_log: $PULSE_HOME/logs/pending.log
  last_digest: $PULSE_HOME/logs/last-digest.md
  detail_logs: $PULSE_HOME/logs/detail
  registry:    $PULSE_HOME/registry
  locks:       $PULSE_HOME/locks

digest:
  timezone:        $TIMEZONE
  silent_if_empty: true
  retention_hours: 24
  llm_agent:       $DIGEST_AGENT
  llm_timeout:     $DIGEST_TIMEOUT

delivery:
  channel: $CHANNEL

  telegram:
    enabled:    $TELEGRAM_ENABLED
    bot_token:  "${BOT_TOKEN}"
    chat_id:    "${CHAT_ID}"
    thread_id:  "${THREAD_ID}"

  discord:
    enabled:     $DISCORD_ENABLED
    webhook_url: "${DISCORD_WEBHOOK}"

  log:
    enabled: $LOG_ENABLED
    path:    $PULSE_HOME/logs/last-digest.md
EOF
  green "  ✓ Config written to $CONFIG_FILE"
else
  yellow "  · Config exists — not overwritten"
fi

# ── Add digest cron jobs ──────────────────────────────────────────────────────
EXISTING_CRON="$(crontab -l 2>/dev/null || true)"

if echo "$EXISTING_CRON" | grep -q "pulse-board-morning"; then
  yellow "  · Digest cron jobs already present — skipping"
else
  echo ""
  blue "  Crontab change:"
  dim "  Will add two entries to your user crontab:"
  dim "    ${MORNING_M} ${MORNING_H} * * *  digest-agent.sh  # pulse-board-morning"
  dim "    ${EVENING_M} ${EVENING_H} * * *  digest-agent.sh  # pulse-board-evening"
  echo ""
  if confirm "Add these cron entries?"; then
    python3 - <<PYEOF
import subprocess

result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
existing = result.stdout.rstrip('\n')

morning = "${MORNING_M} ${MORNING_H} * * * bash ${SKILL_DIR}/digest-agent.sh >> ${PULSE_HOME}/logs/digest-agent.log 2>&1 # pulse-board-morning"
evening = "${EVENING_M} ${EVENING_H} * * * bash ${SKILL_DIR}/digest-agent.sh >> ${PULSE_HOME}/logs/digest-agent.log 2>&1 # pulse-board-evening"

new_crontab = existing + '\n' + morning + '\n' + evening + '\n'
subprocess.run(['crontab', '-'], input=new_crontab, text=True)
PYEOF
    green "  ✓ Digest cron jobs added (${MORNING_H}:${MORNING_M} and ${EVENING_H}:${EVENING_M})"
  else
    yellow "  · Cron jobs skipped — add manually when ready"
  fi
fi

# ── Patch secrets env file (explicit opt-in) ──────────────────────────────────
if [[ -n "$SECRETS_ENV" && -f "$SECRETS_ENV" ]]; then
  NEEDS_LLM_KEY=false
  NEEDS_WORKSPACE=false

  grep -q "^LLM_API_KEY="        "$SECRETS_ENV" || NEEDS_LLM_KEY=true
  grep -q "^OPENCLAW_WORKSPACE=" "$SECRETS_ENV" || NEEDS_WORKSPACE=true

  if $NEEDS_LLM_KEY || $NEEDS_WORKSPACE; then
    echo ""
    blue "  Secrets env file:"
    dim "  The following keys are missing from $SECRETS_ENV"
    dim "  and are required by skills that use OpenAI-compatible endpoints:"
    echo ""
    $NEEDS_LLM_KEY   && dim "    LLM_API_KEY=ollama           (dummy value for local Ollama — not a real secret)"
    $NEEDS_WORKSPACE && dim "    OPENCLAW_WORKSPACE=$OPENCLAW_WORKSPACE"
    echo ""
    dim "  These will be appended to your secrets env file."
    dim "  You can skip this and add them manually if you prefer."
    echo ""
    if confirm "Append missing keys to $SECRETS_ENV?"; then
      $NEEDS_LLM_KEY   && echo 'LLM_API_KEY=ollama'                     >> "$SECRETS_ENV" && green "  ✓ LLM_API_KEY=ollama appended"
      $NEEDS_WORKSPACE && echo "OPENCLAW_WORKSPACE=$OPENCLAW_WORKSPACE" >> "$SECRETS_ENV" && green "  ✓ OPENCLAW_WORKSPACE appended"
    else
      yellow "  · Secrets env patch skipped — add manually if needed"
    fi
  else
    dim "  · Secrets env already complete — nothing to add"
  fi
elif [[ -n "$SECRETS_ENV" ]]; then
  yellow "  · Secrets env file not found at $SECRETS_ENV — skipping patch"
fi

# ── Done ──────────────────────────────────────────────────────────────────────
echo ""
green "  ✓ Pulse Board installed."
echo ""
blue "  Next — plug in your skills:"
printf "  \033[2mbash %s/plug.sh\033[0m\n" "$SKILL_DIR"
echo ""
