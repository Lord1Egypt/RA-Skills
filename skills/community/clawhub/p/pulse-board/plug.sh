#!/usr/bin/env bash
# Pulse Board — plug.sh
# Discovers cron jobs from system crontab and OpenClaw registry,
# presents a menu, and wires selected jobs into Pulse Board.
# No sudo. No root.
#
# Crontab writes: uses python3 subprocess to avoid shell escaping issues.
# Secrets env: if a secrets_env path is set in pulse.yaml, plug.sh wraps
# each wired cron command with "source <secrets_env> && <cmd>" so that the
# skill's runtime environment matches what you configured in install.sh.
# The secrets file is never read, parsed, or transmitted — only sourced
# in the cron shell context, exactly as if you had run it manually.

set -uo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PULSE_HOME="${PULSE_HOME:-$HOME/.pulse-board}"
CONFIG_FILE="$PULSE_HOME/config/pulse.yaml"

# ── UI helpers ────────────────────────────────────────────────────────────────
green()  { printf "\033[0;32m%s\033[0m\n" "$*"; }
yellow() { printf "\033[0;33m%s\033[0m\n" "$*"; }
blue()   { printf "\033[0;34m%s\033[0m\n" "$*"; }
dim()    { printf "\033[2m%s\033[0m"      "$*"; }
red()    { printf "\033[0;31m%s\033[0m\n" "$*"; }

cfg() {
  grep -E "^[[:space:]]*${1}[[:space:]]*:" "$CONFIG_FILE" 2>/dev/null \
    | head -1 | sed 's/.*:[[:space:]]*//' | sed "s/^[\"']\(.*\)[\"']$/\1/"
}

expand() { echo "${1/#\~/$HOME}"; }

# ── Read secrets env path from config ────────────────────────────────────────
SECRETS_ENV="$(expand "$(cfg 'secrets_env')")"
SECRETS_ENV="${SECRETS_ENV:-}"

# wrap_cmd — prepends "source <secrets_env> &&" to the skill command so the
# cron job runs with the same environment variables as your configured stack.
# The secrets file is only sourced in the cron shell — it is never read,
# parsed, logged, or sent anywhere by plug.sh itself.
wrap_cmd() {
  local cmd="$1"
  if [[ -n "$SECRETS_ENV" && -f "$SECRETS_ENV" ]]; then
    echo "bash -c 'source $SECRETS_ENV && $cmd'"
  else
    echo "$cmd"
  fi
}

# ── Guard ─────────────────────────────────────────────────────────────────────
if [[ ! -f "$CONFIG_FILE" ]]; then
  red "  Pulse Board is not installed. Run install.sh first."
  exit 1
fi

# ── Wire a single job (via python3 to avoid shell crontab escaping issues) ────
wire_job() {
  local skill="$1" cron="$2" cmd="$3" label="$4" ok_msg="$5" err_msg="$6" detail_log="$7"
  local skill_safe
  skill_safe="$(echo "$skill" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9-]/-/g')"

  mkdir -p "$(dirname "$detail_log")"
  mkdir -p "$PULSE_HOME/registry"

  cat > "$PULSE_HOME/registry/${skill_safe}.conf" <<EOF
skill=$skill_safe
label=$label
detail_log=$detail_log
registered_at=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
enabled=true
EOF

  local wrapped_cmd
  wrapped_cmd="$(wrap_cmd "$cmd")"
  local cron_line="${cron} ${wrapped_cmd} >> ${detail_log} 2>&1 && bash ${SKILL_DIR}/log-append.sh --skill ${skill_safe} --status OK --message \"${ok_msg}\" || bash ${SKILL_DIR}/log-append.sh --skill ${skill_safe} --status ERROR --message \"${err_msg}\" # pulse-board:${skill_safe}"

  # Use python3 to write crontab — avoids shell escaping mangling the tag colon
  python3 - <<PYEOF
import subprocess, sys

result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
existing_lines = result.stdout.splitlines()

tag = 'pulse-board:${skill_safe}'
filtered = [l for l in existing_lines if tag not in l]
new_crontab = '\n'.join(filtered).rstrip('\n') + '\n' + r"""${cron_line}""" + '\n'

subprocess.run(['crontab', '-'], input=new_crontab, text=True)
PYEOF

  # Verify the entry landed correctly
  local result
  result="$(python3 - <<PYEOF2
import subprocess
result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
tag = 'pulse-board:${skill_safe}'
lines = [l for l in result.stdout.splitlines() if tag in l]
print('found' if lines else 'missing')
PYEOF2
  )"

  if [[ "$result" == "found" ]]; then
    green "    ✓ Wired: $label"
  else
    red "    ✗ Failed to wire: $label"
  fi
}

# ── Manual mode ───────────────────────────────────────────────────────────────
if [[ $# -gt 0 ]]; then
  SKILL="" CRON="" CMD="" LABEL="" OK_MSG="" ERR_MSG="" DETAIL_LOG=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --skill)  SKILL="$2";      shift 2 ;;
      --cron)   CRON="$2";       shift 2 ;;
      --cmd)    CMD="$2";        shift 2 ;;
      --label)  LABEL="$2";      shift 2 ;;
      --ok)     OK_MSG="$2";     shift 2 ;;
      --error)  ERR_MSG="$2";    shift 2 ;;
      --log)    DETAIL_LOG="$2"; shift 2 ;;
      *) red "Unknown argument: $1"; exit 1 ;;
    esac
  done
  [[ -z "$SKILL" || -z "$CRON" || -z "$CMD" ]] && {
    red "  Manual mode requires --skill, --cron, and --cmd."; exit 1
  }
  SKILL_SAFE="$(echo "$SKILL" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9-]/-/g')"
  wire_job "$SKILL_SAFE" "$CRON" "$CMD" \
    "${LABEL:-$SKILL_SAFE}" \
    "${OK_MSG:-Run complete}" \
    "${ERR_MSG:-Failed — check detail log}" \
    "${DETAIL_LOG:-$PULSE_HOME/logs/detail/$SKILL_SAFE/run.log}"
  exit 0
fi

# ── Discovery ─────────────────────────────────────────────────────────────────
clear
echo ""
blue "  📋 Pulse Board — plug.sh"
echo ""
blue "  Discovering cron jobs..."
echo ""

OPENCLAW_CRON_DIR="$(expand "$(cfg 'openclaw_cron_dir')")"
OPENCLAW_CRON_DIR="${OPENCLAW_CRON_DIR:-$HOME/.openclaw/cron}"

# Collect already-plugged skill IDs
declare -a ALREADY_PLUGGED=()
while IFS= read -r line; do
  [[ "$line" =~ pulse-board:([a-z0-9-]+) ]] && ALREADY_PLUGGED+=("${BASH_REMATCH[1]}")
done < <(crontab -l 2>/dev/null | grep "pulse-board:" || true)

is_plugged() {
  local id="$1"
  for p in "${ALREADY_PLUGGED[@]:-}"; do [[ "$p" == "$id" ]] && return 0; done
  return 1
}

declare -a JOB_SKILL=() JOB_CRON=() JOB_CMD=() JOB_LABEL=() JOB_SOURCE=()

# ── Parse system crontab ──────────────────────────────────────────────────────
while IFS= read -r line; do
  [[ -z "$line" || "$line" =~ ^# ]] && continue
  echo "$line" | grep -q "pulse-board" && continue

  if [[ "$line" =~ ^([^\ ]+[\ \	]+[^\ ]+[\ \	]+[^\ ]+[\ \	]+[^\ ]+[\ \	]+[^\ ]+)[\ \	]+(.*) ]]; then
    cron_expr="${BASH_REMATCH[1]}"
    cmd_part="${BASH_REMATCH[2]}"

    skill_guess="$(echo "$cmd_part" | grep -oP 'skills/\K[^/]+' | head -1 || true)"
    [[ -z "$skill_guess" ]] && skill_guess="$(basename "$(echo "$cmd_part" | awk '{print $2}')" .sh 2>/dev/null || echo "unknown")"
    skill_id="$(echo "$skill_guess" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9-]/-/g')"

    is_plugged "$skill_id" && continue

    JOB_SKILL+=("$skill_id")
    JOB_CRON+=("$cron_expr")
    JOB_CMD+=("$cmd_part")
    JOB_LABEL+=("$skill_guess")
    JOB_SOURCE+=("system")
  fi
done < <(crontab -l 2>/dev/null || true)

# ── Parse OpenClaw jobs.json ──────────────────────────────────────────────────
JOBS_FILE="$OPENCLAW_CRON_DIR/jobs.json"

if [[ -f "$JOBS_FILE" ]] && command -v python3 &>/dev/null; then
  PARSED="$(python3 << PYEOF
import json, sys

try:
    with open("$JOBS_FILE") as f:
        data = json.load(f)
except Exception as e:
    sys.exit(0)

for job in data.get("jobs", []):
    kind = job.get("payload", {}).get("kind", "")
    if kind == "agentTurn":
        continue
    job_id = job.get("id", "")
    name   = job.get("name", job_id)
    sched  = job.get("schedule", {})
    expr   = sched.get("expr", "") if sched.get("kind") == "cron" else ""
    if expr:
        print(f"{job_id}|{name}|{expr}")
PYEOF
  )" || true

  while IFS='|' read -r job_id job_name cron_expr; do
    [[ -z "$job_id" ]] && continue
    skill_id="$(echo "$job_id" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9-]/-/g')"
    is_plugged "$skill_id" && continue

    already=false
    for ec in "${JOB_CRON[@]:-}"; do [[ "$ec" == "$cron_expr" ]] && already=true && break; done
    $already && continue

    JOB_SKILL+=("$skill_id")
    JOB_CRON+=("$cron_expr")
    JOB_CMD+=("")
    JOB_LABEL+=("$job_name")
    JOB_SOURCE+=("openclaw")
  done <<< "$PARSED"
fi

# ── Nothing found ─────────────────────────────────────────────────────────────
TOTAL=${#JOB_SKILL[@]}

if [[ $TOTAL -eq 0 ]]; then
  yellow "  No unplugged cron jobs found."
  echo ""
  printf "  $(dim 'Manual mode:') plug.sh --skill <n> --cron <expr> --cmd <command>\n"
  echo ""
  exit 0
fi

# ── Display menu ──────────────────────────────────────────────────────────────
printf "  \033[1m%-4s %-24s %-22s %s\033[0m\n" "#" "Skill" "Schedule" "Source"
printf "  %-4s %-24s %-22s %s\n"               "────" "────────────────────────" "──────────────────────" "──────"

for idx in "${!JOB_SKILL[@]}"; do
  printf "  \033[1m[%s]\033[0m %-24s %-22s \033[2m%s\033[0m\n" \
    "$((idx + 1))" "${JOB_LABEL[$idx]}" "${JOB_CRON[$idx]}" "${JOB_SOURCE[$idx]}"
done

echo ""
printf "  \033[1m→\033[0m Select jobs (e.g. \033[1m1 3\033[0m, or \033[1mall\033[0m, or \033[1mnone\033[0m): "
read -r SELECTION </dev/tty

[[ -z "$SELECTION" || "$SELECTION" == "none" ]] && { echo ""; dim "  Nothing selected."; echo ""; exit 0; }

declare -a SELECTED=()
if [[ "$SELECTION" == "all" ]]; then
  for idx in "${!JOB_SKILL[@]}"; do SELECTED+=("$idx"); done
else
  for num in $SELECTION; do
    idx=$(( num - 1 ))
    [[ $idx -ge 0 && $idx -lt $TOTAL ]] && SELECTED+=("$idx")
  done
fi

[[ ${#SELECTED[@]} -eq 0 ]] && { yellow "  No valid selections."; echo ""; exit 0; }

# ── Confirm details ───────────────────────────────────────────────────────────
echo ""
blue "  Confirm details:"
echo ""

declare -a FINAL_SKILL=() FINAL_CRON=() FINAL_CMD=() FINAL_LABEL=()

for idx in "${SELECTED[@]}"; do
  label="${JOB_LABEL[$idx]}"
  cron="${JOB_CRON[$idx]}"
  cmd="${JOB_CMD[$idx]}"
  skill="${JOB_SKILL[$idx]}"

  echo ""
  printf "  \033[1m▸ %s\033[0m\n" "$label"
  printf "  \033[2m  Schedule: %s\033[0m\n" "$cron"
  [[ -n "$cmd" ]] && printf "  \033[2m  Command:  %s\033[0m\n" "$cmd"
  echo ""

  printf "  \033[1m→\033[0m Label [%s]: " "$label"
  read -r new_label </dev/tty
  new_label="${new_label:-$label}"

  if [[ -z "$cmd" ]]; then
    printf "  \033[1m→\033[0m Command (required): "
    read -r cmd </dev/tty
  fi

  FINAL_SKILL+=("$skill")
  FINAL_CRON+=("$cron")
  FINAL_CMD+=("$cmd")
  FINAL_LABEL+=("$new_label")
done

# ── Wire ──────────────────────────────────────────────────────────────────────
echo ""
blue "  Wiring..."
echo ""

for i in "${!FINAL_SKILL[@]}"; do
  skill_safe="$(echo "${FINAL_SKILL[$i]}" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9-]/-/g')"
  wire_job \
    "$skill_safe" \
    "${FINAL_CRON[$i]}" \
    "${FINAL_CMD[$i]}" \
    "${FINAL_LABEL[$i]}" \
    "Run complete" \
    "Failed — check detail log" \
    "$PULSE_HOME/logs/detail/$skill_safe/run.log"
done

echo ""
green "  Done. Jobs will appear in the next digest."
echo ""
