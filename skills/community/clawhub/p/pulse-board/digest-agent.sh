#!/usr/bin/env bash
# Pulse Board — digest-agent.sh
# Composes and delivers a twice-daily digest from pending.log.
# LLM summary via openclaw agent; mechanical fallback if unavailable.
# Raw log → last-digest.md. Delivered message → last-delivered.md (via deliver.sh).
# Privacy: raw log is sent to the configured agent as prompt context.
#   If that agent uses a remote LLM, log content leaves this host.
# No sudo. No root.

set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PULSE_HOME="${PULSE_HOME:-$HOME/.pulse-board}"
CONFIG_FILE="$PULSE_HOME/config/pulse.yaml"

[[ -f "$HOME/.openclaw/shared/secrets/openclaw-secrets.env" ]] && \
  { set +u; source "$HOME/.openclaw/shared/secrets/openclaw-secrets.env"; set -u; }

# ── Helpers ───────────────────────────────────────────────────────────────────
g() { printf "\033[0;32m%s\033[0m\n" "$*"; }
y() { printf "\033[0;33m%s\033[0m\n" "$*"; }
r() { printf "\033[0;31m%s\033[0m\n" "$*"; }
b() { printf "\033[0;34m%s\033[0m\n" "$*"; }

cfg()       { grep -E "^[[:space:]]*${1}[[:space:]]*:" "$CONFIG_FILE" 2>/dev/null | head -1 | sed 's/.*:[[:space:]]*//' | sed "s/^[\"']\(.*\)[\"']$/\1/"; }
cfg_under() { awk "/^[[:space:]]*${1}:/{f=1} f && /^[[:space:]]*${2}:/{ sub(/.*:[[:space:]]*/,\"\"); gsub(/[\"' ]/,\"\"); print; exit }" "$CONFIG_FILE" 2>/dev/null; }
expand()    { echo "${1/#\~/$HOME}"; }
count()     { awk "/$1/{c++} END{print c+0}" "$2"; }

# ── Config ────────────────────────────────────────────────────────────────────
PENDING_LOG="$(expand "$(cfg 'pending_log')")"; PENDING_LOG="${PENDING_LOG:-$PULSE_HOME/logs/pending.log}"
DETAIL_DIR="$(expand "$(cfg 'detail_logs')")";  DETAIL_DIR="${DETAIL_DIR:-$PULSE_HOME/logs/detail}"
TIMEZONE="$(cfg 'timezone')";                   TIMEZONE="${TIMEZONE:-UTC}"
SILENT="$(cfg 'silent_if_empty')";              SILENT="${SILENT:-true}"
RETENTION="$(cfg 'retention_hours')";           RETENTION="${RETENTION:-24}"
LLM_AGENT="$(cfg_under 'digest' 'llm_agent')"; LLM_AGENT="${LLM_AGENT:-main}"
LLM_TIMEOUT="$(cfg_under 'digest' 'llm_timeout')"; LLM_TIMEOUT="${LLM_TIMEOUT:-60}"

# ── Lock ──────────────────────────────────────────────────────────────────────
LOCK="$PULSE_HOME/locks/digest.lock"
mkdir -p "$(dirname "$LOCK")"

if [[ -f "$LOCK" ]]; then
  AGE=$(( $(date +%s) - $(date -r "$LOCK" +%s 2>/dev/null || echo 0) ))
  [[ $AGE -lt 3600 ]] && { y "digest-agent: already running (${AGE}s). Exiting."; exit 0; }
  y "digest-agent: removing stale lock (${AGE}s)."; rm -f "$LOCK"
fi
touch "$LOCK"; trap 'rm -f "$LOCK"' EXIT

# ── Guard ─────────────────────────────────────────────────────────────────────
[[ ! -s "$PENDING_LOG" && "$SILENT" == "true" ]] && { y "digest-agent: nothing to report."; exit 0; }

b "digest-agent: $(count '.' "$PENDING_LOG") entries"

# ── Header counts ─────────────────────────────────────────────────────────────
NOW="$(TZ="$TIMEZONE" date +'%Y-%m-%d %H:%M %Z')"
OK=$(count '\[OK'     "$PENDING_LOG")
ERR=$(count '\[ERROR' "$PENDING_LOG")
SKIP=$(count '\[SKIP' "$PENDING_LOG")
WARN=$(count '\[WARN' "$PENDING_LOG")
[[ "$ERR" -gt 0 ]] \
  && STATUS_LINE="⚠️ ${ERR} error(s) · ${OK} ok · ${SKIP} skipped · ${WARN} warnings" \
  || STATUS_LINE="✅ ${OK} ok · ${SKIP} skipped · ${WARN} warnings · 0 errors"

# ── Save raw log ──────────────────────────────────────────────────────────────
LAST_DIGEST="$PULSE_HOME/logs/last-digest.md"
mkdir -p "$(dirname "$LAST_DIGEST")"
{ printf "# Pulse Board Raw Log — %s\n\n" "$NOW"; cat "$PENDING_LOG"; } > "$LAST_DIGEST"

# ── Compose ───────────────────────────────────────────────────────────────────
TEMP="$(mktemp /tmp/pulse-XXXXXX)"; trap 'rm -f "$LOCK" "$TEMP"' EXIT
LLM_SUCCESS=false

if command -v openclaw &>/dev/null; then
  b "digest-agent: requesting summary from '${LLM_AGENT}'..."
  PROMPT="You are writing a brief operational digest for a sysadmin.
Below are cron job outcomes from the last 12 hours. Write:
1. One opening sentence on overall system health (casual, factual)
2. One bullet per skill: what ran, how many times, outcome
3. If errors or warnings exist, expand with relevant log lines

Rules: plain text only — no asterisks, backticks, underscores, or any Markdown.
No title line. No sign-off. No padding. Do not invent information.
Do not include the status counts line.

Raw log:
$(cat "$PENDING_LOG")"

  AGENT_RESPONSE="$(timeout "$LLM_TIMEOUT" openclaw agent \
    --agent "$LLM_AGENT" --message "$PROMPT" --json 2>/dev/null)" \
    && CALL_OK=true || CALL_OK=false

  if $CALL_OK && [[ -n "$AGENT_RESPONSE" ]]; then
    LLM_TEXT="$(echo "$AGENT_RESPONSE" | python3 -c \
      'import json,sys; d=json.load(sys.stdin); print(d["result"]["payloads"][0]["text"])' \
      2>/dev/null)" && PARSE_OK=true || PARSE_OK=false

    if $PARSE_OK && [[ -n "$LLM_TEXT" ]]; then
      printf "📋 *Pulse Board Digest* — %s\n%s\n\n%s" "$NOW" "$STATUS_LINE" "$LLM_TEXT" > "$TEMP"
      LLM_SUCCESS=true
      g "digest-agent: LLM summary composed."
    else
      y "digest-agent: parse failed — falling back."
    fi
  else
    y "digest-agent: agent call failed — falling back."
  fi
else
  y "digest-agent: openclaw not found — falling back."
fi

# ── Mechanical fallback ───────────────────────────────────────────────────────
if ! $LLM_SUCCESS; then
  BODY=""
  while IFS= read -r line; do
    [[ -z "$line" ]] && continue
    echo "$line" | grep -q '\[ERROR' && BODY="${BODY}❌ ${line}\n" && continue
    echo "$line" | grep -q '\[WARN'  && BODY="${BODY}⚠️  ${line}\n" && continue
    echo "$line" | grep -q '\[SKIP'  && BODY="${BODY}⏭️  ${line}\n" && continue
    BODY="${BODY}✓  ${line}\n"
  done < "$PENDING_LOG"
  printf "📋 *Pulse Board Digest* — %s\n%s\n\n%b" "$NOW" "$STATUS_LINE" "$BODY" > "$TEMP"
  y "digest-agent: using mechanical digest."
fi

# ── Deliver ───────────────────────────────────────────────────────────────────
bash "$SKILL_DIR/deliver.sh" "$TEMP" \
  && g "digest-agent: delivered." \
  || r "digest-agent: delivery failed — raw log in last-digest.md."

# ── Cleanup ───────────────────────────────────────────────────────────────────
> "$PENDING_LOG"

if [[ "$RETENTION" -gt 0 && -d "$DETAIL_DIR" ]]; then
  PRUNED=0
  while IFS= read -r -d '' f; do rm -f "$f"; (( PRUNED++ )) || true
  done < <(find "$DETAIL_DIR" -type f -name "*.log" -mmin "+$(( RETENTION * 60 ))" -print0 2>/dev/null)
  [[ $PRUNED -gt 0 ]] && g "digest-agent: pruned ${PRUNED} log(s) older than ${RETENTION}h."
fi

g "digest-agent: done."
