#!/usr/bin/env bash
# Relationship OS — Debug tool
# Usage:
#   bash debug.sh              # Full state snapshot
#   bash debug.sh log          # View recent logs
#   bash debug.sh log 50       # View last 50 lines of logs
#   bash debug.sh log follow   # Follow logs in real time
#   bash debug.sh state        # State only
#   bash debug.sh secrets      # Exclusive memories only
#   bash debug.sh stance       # Stances only
#   bash debug.sh timeline     # Event timeline
#   bash debug.sh threads      # Open threads
#   bash debug.sh health       # Health check

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# scripts/ -> relationship-os/ -> skills/ -> workplace/
WORKSPACE="${RELATIONSHIP_OS_WORKSPACE:-$(cd "$SCRIPT_DIR/../../.." 2>/dev/null && pwd)}"

# If .relationship is not in the current workspace, try looking one level up
if [ ! -d "$WORKSPACE/.relationship" ] && [ -d "$WORKSPACE/workplace/.relationship" ]; then
  WORKSPACE="$WORKSPACE/workplace"
fi

REL_DIR="$WORKSPACE/.relationship"
LOG_FILE="$REL_DIR/debug.log"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

if [ ! -d "$REL_DIR" ]; then
  echo -e "${RED}Error: .relationship/ directory does not exist${NC}"
  echo "Path: $REL_DIR"
  echo "Please run init.sh first"
  exit 1
fi

print_header() {
  echo -e "\n${CYAN}━━━ $1 ━━━${NC}"
}

show_state() {
  print_header "Relationship State (state.json)"
  if command -v jq &>/dev/null; then
    jq -r '
      "  Stage: \(.stage)",
      "  Started: \(.stageStarted)",
      "  Interactions: \(.interactionCount)",
      "  Emotion baseline: valence=\(.emotionBaseline.valence) arousal=\(.emotionBaseline.arousal)",
      "  Last active: \(.userPatterns.lastSeen)",
      "  Avg messages/day: \(.userPatterns.avgMessagesPerDay)",
      "  Active hours: \(.userPatterns.activeHours | join(", "))",
      "  Stage history: \(.stageHistory | join(" → "))",
      "  Milestone count: \(.milestones | length)"
    ' "$REL_DIR/state.json" 2>/dev/null || cat "$REL_DIR/state.json"

    echo -e "\n  ${YELLOW}Milestones:${NC}"
    jq -r '.milestones[] | "    [\(.date)] \(.type): \(.note)"' "$REL_DIR/state.json" 2>/dev/null
  else
    cat "$REL_DIR/state.json"
  fi
}

show_secrets() {
  print_header "Exclusive Memories (secrets.json)"
  if command -v jq &>/dev/null; then
    echo -e "  ${YELLOW}Nicknames:${NC}"
    jq -r '
      "    User calls Agent: \(.nicknames.user_calls_agent | join(", "))",
      "    Agent calls User: \(.nicknames.agent_calls_user | join(", "))"
    ' "$REL_DIR/secrets.json" 2>/dev/null

    local jokes=$(jq '.inside_jokes | length' "$REL_DIR/secrets.json" 2>/dev/null)
    echo -e "  ${YELLOW}Inside Jokes (${jokes}):${NC}"
    jq -r '.inside_jokes[] | "    [\(.created)] \(.reference) — \(.context)"' "$REL_DIR/secrets.json" 2>/dev/null

    local goals=$(jq '.shared_goals | length' "$REL_DIR/secrets.json" 2>/dev/null)
    echo -e "  ${YELLOW}Shared Goals (${goals}):${NC}"
    jq -r '.shared_goals[] | "    [\(.status)] \(.goal)"' "$REL_DIR/secrets.json" 2>/dev/null

    local agreements=$(jq '.agreements | length' "$REL_DIR/secrets.json" 2>/dev/null)
    echo -e "  ${YELLOW}Agreements (${agreements}):${NC}"
    jq -r '.agreements[] | "    [\(.created)] \(.rule)"' "$REL_DIR/secrets.json" 2>/dev/null
  else
    cat "$REL_DIR/secrets.json"
  fi
}

show_stance() {
  print_header "Agent Stances (stance.json)"
  if command -v jq &>/dev/null; then
    echo -e "  ${YELLOW}Value Stances:${NC}"
    jq -r '.values[] | "    [\(.formed)] \(.topic): \(.position) (strength: \(.strength))"' "$REL_DIR/stance.json" 2>/dev/null

    echo -e "  ${YELLOW}Preferences:${NC}"
    jq -r '.preferences[] | "    Likes: \(.like)\n    Dislikes: \(.dislike)"' "$REL_DIR/stance.json" 2>/dev/null
  else
    cat "$REL_DIR/stance.json"
  fi
}

show_timeline() {
  print_header "Event Timeline (timeline/)"
  local count=$(ls "$REL_DIR/timeline/"*.md 2>/dev/null | wc -l | tr -d ' ')
  echo -e "  Total events: ${count}"
  echo ""
  for f in $(ls "$REL_DIR/timeline/"*.md 2>/dev/null | sort -r); do
    local fname=$(basename "$f" .md)
    local date=${fname:0:10}
    local slug=${fname:11}
    local importance=$(grep -oP 'importance.*?(\d+)/10' "$f" 2>/dev/null | grep -oP '\d+(?=/10)' || echo "?")
    local status=$(grep -oP 'status.*?(resolved|unresolved)' "$f" 2>/dev/null | grep -oP '(resolved|unresolved)' || echo "?")
    local color=$GREEN
    [ "$status" = "unresolved" ] && color=$YELLOW
    echo -e "  ${color}[${date}]${NC} ${slug} (importance:${importance}/10, ${status})"
  done
}

show_threads() {
  print_header "Open Threads (threads/)"
  local files=$(ls "$REL_DIR/threads/"*.json 2>/dev/null || true)
  if [ -z "$files" ]; then
    echo -e "  ${GREEN}No pending threads${NC}"
    return
  fi
  for f in $files; do
    if command -v jq &>/dev/null; then
      local status=$(jq -r '.status' "$f")
      local color=$GREEN
      [ "$status" = "pending" ] && color=$YELLOW
      jq -r '"  '$color'[\(.status)]'$NC' \(.id): \(.context) (follow-up: \(.followUpAt), priority: \(.priority))"' "$f" 2>/dev/null
    else
      cat "$f"
    fi
  done
}

show_log() {
  local lines="${1:-30}"
  print_header "Debug Log (last ${lines} lines)"
  if [ ! -f "$LOG_FILE" ]; then
    echo -e "  ${YELLOW}Log file does not exist — waiting for first bootstrap${NC}"
    return
  fi
  tail -n "$lines" "$LOG_FILE"
}

follow_log() {
  print_header "Live Log Tail (Ctrl+C to exit)"
  if [ ! -f "$LOG_FILE" ]; then
    echo -e "  ${YELLOW}Log file does not exist — waiting for first bootstrap${NC}"
    echo "Creating empty log file and waiting..."
    touch "$LOG_FILE"
  fi
  tail -f "$LOG_FILE"
}

health_check() {
  print_header "Health Check"
  local issues=0

  # state.json
  if [ -f "$REL_DIR/state.json" ]; then
    echo -e "  ${GREEN}✓${NC} state.json exists"
    if command -v jq &>/dev/null && ! jq empty "$REL_DIR/state.json" 2>/dev/null; then
      echo -e "  ${RED}✗${NC} state.json has invalid JSON format"
      issues=$((issues + 1))
    fi
  else
    echo -e "  ${RED}✗${NC} state.json does not exist"
    issues=$((issues + 1))
  fi

  # secrets.json
  if [ -f "$REL_DIR/secrets.json" ]; then
    echo -e "  ${GREEN}✓${NC} secrets.json exists"
    if command -v jq &>/dev/null && ! jq empty "$REL_DIR/secrets.json" 2>/dev/null; then
      echo -e "  ${RED}✗${NC} secrets.json has invalid JSON format"
      issues=$((issues + 1))
    fi
  else
    echo -e "  ${RED}✗${NC} secrets.json does not exist"
    issues=$((issues + 1))
  fi

  # stance.json
  if [ -f "$REL_DIR/stance.json" ]; then
    echo -e "  ${GREEN}✓${NC} stance.json exists"
  else
    echo -e "  ${RED}✗${NC} stance.json does not exist"
    issues=$((issues + 1))
  fi

  # timeline/
  if [ -d "$REL_DIR/timeline" ]; then
    local event_count=$(ls "$REL_DIR/timeline/"*.md 2>/dev/null | wc -l | tr -d ' ')
    echo -e "  ${GREEN}✓${NC} timeline/ exists (${event_count} events)"
  else
    echo -e "  ${RED}✗${NC} timeline/ does not exist"
    issues=$((issues + 1))
  fi

  # threads/
  if [ -d "$REL_DIR/threads" ]; then
    local thread_count=$(ls "$REL_DIR/threads/"*.json 2>/dev/null | wc -l | tr -d ' ')
    echo -e "  ${GREEN}✓${NC} threads/ exists (${thread_count} threads)"
  else
    echo -e "  ${RED}✗${NC} threads/ does not exist"
    issues=$((issues + 1))
  fi

  # debug.log
  if [ -f "$LOG_FILE" ]; then
    local log_size=$(wc -c < "$LOG_FILE" | tr -d ' ')
    local log_lines=$(wc -l < "$LOG_FILE" | tr -d ' ')
    echo -e "  ${GREEN}✓${NC} debug.log exists (${log_lines} lines, ${log_size} bytes)"

    # Check for recent ERRORs
    local recent_errors=$(tail -100 "$LOG_FILE" | grep -c '\[ERROR\]' || true)
    if [ "$recent_errors" -gt 0 ]; then
      echo -e "  ${YELLOW}!${NC} ${recent_errors} ERROR(s) in the last 100 lines"
    fi
  else
    echo -e "  ${YELLOW}~${NC} debug.log does not exist (waiting for first bootstrap)"
  fi

  # HEARTBEAT.md
  local heartbeat="$WORKSPACE/HEARTBEAT.md"
  if [ -f "$heartbeat" ]; then
    local has_content=$(grep -v '^#' "$heartbeat" | grep -v '^$' | wc -l | tr -d ' ')
    if [ "$has_content" -gt 0 ]; then
      echo -e "  ${GREEN}✓${NC} HEARTBEAT.md is enabled"
    else
      echo -e "  ${YELLOW}~${NC} HEARTBEAT.md is empty (heartbeat not enabled)"
    fi
  fi

  echo ""
  if [ "$issues" -eq 0 ]; then
    echo -e "  ${GREEN}All checks passed${NC}"
  else
    echo -e "  ${RED}${issues} issue(s) need fixing${NC}"
  fi
}

# ====== Main Entry ======
case "${1:-all}" in
  log)
    if [ "${2:-}" = "follow" ]; then
      follow_log
    else
      show_log "${2:-30}"
    fi
    ;;
  state)    show_state ;;
  secrets)  show_secrets ;;
  stance)   show_stance ;;
  timeline) show_timeline ;;
  threads)  show_threads ;;
  health)   health_check ;;
  all)
    echo -e "${BLUE}╔══════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║   Relationship OS State Snapshot     ║${NC}"
    echo -e "${BLUE}║   $(date '+%Y-%m-%d %H:%M:%S')               ║${NC}"
    echo -e "${BLUE}╚══════════════════════════════════════╝${NC}"
    show_state
    show_secrets
    show_stance
    show_timeline
    show_threads
    health_check
    show_log 15
    ;;
  *)
    echo "Usage: bash debug.sh [all|log|state|secrets|stance|timeline|threads|health]"
    echo "  all       Full state snapshot (default)"
    echo "  log [N]   View last N lines of log (default 30)"
    echo "  log follow Follow logs in real time"
    echo "  state     Relationship state"
    echo "  secrets   Exclusive memories"
    echo "  stance    Agent stances"
    echo "  timeline  Event timeline"
    echo "  threads   Open threads"
    echo "  health    Health check"
    ;;
esac
