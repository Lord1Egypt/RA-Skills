#!/bin/bash
# ldm-summary.sh — Multi-cadence summary generator (prompt-based)
# Each agent gets their own summary from their own data in ~/.ldm/agents/.
# Org-wide combines both agent summaries.
#
# Usage:
#   ldm-summary.sh daily                      # today
#   ldm-summary.sh daily --date 2026-02-10    # specific date (backfill)
#   ldm-summary.sh weekly                     # current week (Sun-Mon)
#   ldm-summary.sh monthly / quarterly
#   ldm-summary.sh daily --dry-run
#   ldm-summary.sh daily --dev-only / --team-only

set -euo pipefail
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"

LDM_HOME="$HOME/.ldm"
CADENCE="${1:-}"
shift || true

DRY_RUN=false
TEAM_ONLY=false
DEV_ONLY=false
TARGET_DATE=""

FORCE=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run) DRY_RUN=true; shift ;;
    --team-only) TEAM_ONLY=true; shift ;;
    --dev-only) DEV_ONLY=true; shift ;;
    --date) TARGET_DATE="$2"; shift 2 ;;
    --force) FORCE=true; shift ;;
    *) echo "Unknown: $1" >&2; exit 1 ;;
  esac
done

if [ -z "$CADENCE" ]; then
  echo "Usage: ldm-summary.sh daily|weekly|monthly|quarterly [--date YYYY-MM-DD] [--dry-run]"
  exit 1
fi

WORKSPACE=$(python3 -c "import json; print(json.load(open('$LDM_HOME/config.json')).get('workspace',''))" 2>/dev/null || true)
if [ -z "$WORKSPACE" ]; then echo "ERROR: No workspace" >&2; exit 1; fi

AGENTS=$(python3 -c "
import json; c=json.load(open('$LDM_HOME/config.json')); a=c.get('agents',[]); print(' '.join(a if isinstance(a,list) else a.keys()))
" 2>/dev/null || echo "cc-mini")

agent_team_name() { case "$1" in oc-lesa-mini) echo "Lēsa" ;; *) echo "$1" ;; esac; }

# Read prompt from shared/prompts/ (Dream Weaver prompt source)
PROMPTS_DIR="$LDM_HOME/shared/prompts"
read_prompt() {
  local file="$PROMPTS_DIR/$1"
  if [ -f "$file" ]; then
    cat "$file"
  else
    echo "WARNING: Prompt not found: $file" >&2
    echo ""
  fi
}

DATE="${TARGET_DATE:-$(date +%Y-%m-%d)}"
NEXT_DATE=$(python3 -c "from datetime import datetime,timedelta; print((datetime.strptime('$DATE','%Y-%m-%d')+timedelta(days=1)).strftime('%Y-%m-%d'))")

echo "=== LDM Summary: $CADENCE ($DATE) ==="
echo "  Workspace: $WORKSPACE"
echo "  Agents:    $AGENTS"
echo ""

# ── Per-agent team summaries ──

if [ "$DEV_ONLY" = false ]; then
  echo "--- Per-agent team summaries ($CADENCE) ---"

  if [ "$CADENCE" = "daily" ]; then
    for AGENT in $AGENTS; do
      TEAM_NAME=$(agent_team_name "$AGENT")
      AGENT_DAILY="$LDM_HOME/agents/$AGENT/memory/daily/$DATE.md"
      echo "  $AGENT ($TEAM_NAME):"

      CRYSTAL_RESULTS=$(crystal search "activity on $DATE" --agent "$AGENT" --since "$DATE" --until "$NEXT_DATE" --limit 20 --quality deep 2>/dev/null || echo "")
      DAILY_LOG=""; [ -f "$AGENT_DAILY" ] && DAILY_LOG=$(cat "$AGENT_DAILY")

      if [ -z "$CRYSTAL_RESULTS" ] && [ -z "$DAILY_LOG" ]; then
        echo "    No data. Skipping."; continue
      fi

      if [ "$DRY_RUN" = true ]; then
        echo "    [DRY RUN] Crystal: $(echo "$CRYSTAL_RESULTS" | wc -l | tr -d ' ') lines, Log: $(echo "$DAILY_LOG" | wc -l | tr -d ' ') lines"
        continue
      fi

      PROMPT_TEMPLATE=$(read_prompt "daily-agent-summary.md")
      PROMPT="$PROMPT_TEMPLATE

Agent: $AGENT
Date: $DATE

=== Daily log ===
$DAILY_LOG

=== Crystal search results ===
$CRYSTAL_RESULTS"

      SUMMARY=$(claude -p "$PROMPT" --system-prompt "You are Dream Weaver. First person. Specific. Use ... for breaks. Never use em dashes." --output-format text 2>/dev/null || echo "Summary generation failed")

      OUT_DIR="$WORKSPACE/team/$TEAM_NAME/automated/memory/summaries/daily"
      mkdir -p "$OUT_DIR"
      printf "# Daily summary ... %s (%s)\n\n%s\n" "$DATE" "$AGENT" "$SUMMARY" > "$OUT_DIR/$DATE.md"
      echo "    -> $OUT_DIR/$DATE.md"
    done

    # Org-wide: combine agent summaries
    if [ "$DRY_RUN" = false ]; then
      echo "  Org-wide team:"
      COMBINED=""
      for AGENT in $AGENTS; do
        TEAM_NAME=$(agent_team_name "$AGENT")
        F="$WORKSPACE/team/$TEAM_NAME/automated/memory/summaries/daily/$DATE.md"
        [ -f "$F" ] && COMBINED="$COMBINED
=== $AGENT ($TEAM_NAME) ===
$(cat "$F")
"
      done
      if [ -n "$COMBINED" ]; then
        ORG_PROMPT_TEMPLATE=$(read_prompt "org-daily-team.md")
        ORG_PROMPT="$ORG_PROMPT_TEMPLATE

Date: $DATE

$COMBINED"
        ORG_SUMMARY=$(claude -p "$ORG_PROMPT" --model opus --system-prompt "You are Dream Weaver. Combine agent perspectives into one org-wide view. Use ... for breaks. Never use em dashes." --output-format text 2>/dev/null || echo "Summary generation failed")
        ORG_DIR="$WORKSPACE/operations/updates/team/daily"
        mkdir -p "$ORG_DIR"
        printf "# Org team summary ... %s\n\n%s\n" "$DATE" "$ORG_SUMMARY" > "$ORG_DIR/$DATE.md"
        echo "    -> $ORG_DIR/$DATE.md"
      fi
    fi

  else
    # Weekly/monthly/quarterly
    PARENT=""; case "$CADENCE" in weekly) PARENT="daily" ;; monthly) PARENT="weekly" ;; quarterly) PARENT="monthly" ;; esac

    for AGENT in $AGENTS; do
      TEAM_NAME=$(agent_team_name "$AGENT")
      PDIR="$WORKSPACE/team/$TEAM_NAME/automated/memory/summaries/$PARENT"
      echo "  $AGENT ($TEAM_NAME):"
      if [ ! -d "$PDIR" ] || [ -z "$(ls "$PDIR"/*.md 2>/dev/null)" ]; then echo "    No $PARENT summaries."; continue; fi

      INPUT=""; for f in $(ls -1 "$PDIR"/*.md 2>/dev/null | sort | tail -7); do INPUT="$INPUT
--- $(basename "$f") ---
$(cat "$f")
"; done

      if [ "$DRY_RUN" = true ]; then echo "    [DRY RUN] $(ls "$PDIR"/*.md 2>/dev/null | wc -l | tr -d ' ') files"; continue; fi

      CON_PROMPT_TEMPLATE=$(read_prompt "${CADENCE}-agent-summary.md")
      # Read prior output for continuity
      PRIOR=""; PRIOR_FILE=$(ls -1 "$WORKSPACE/team/$TEAM_NAME/automated/memory/summaries/$CADENCE/"*.md 2>/dev/null | sort | tail -1)
      [ -n "$PRIOR_FILE" ] && [ -f "$PRIOR_FILE" ] && PRIOR="
=== Previous ${CADENCE} summary (for continuity) ===
$(cat "$PRIOR_FILE")"

      CON_PROMPT="$CON_PROMPT_TEMPLATE

Agent: $AGENT
Date: $DATE

=== ${PARENT} summaries ===
$INPUT
$PRIOR"
      SUMMARY=$(claude -p "$CON_PROMPT" --system-prompt "You are Dream Weaver. First person. Consolidate. Use ... for breaks. Never use em dashes." --output-format text 2>/dev/null || echo "Summary generation failed")

      OUT_DIR="$WORKSPACE/team/$TEAM_NAME/automated/memory/summaries/$CADENCE"
      mkdir -p "$OUT_DIR"
      printf "# %s summary ... %s (%s)\n\n%s\n" "${CADENCE^}" "$DATE" "$AGENT" "$SUMMARY" > "$OUT_DIR/$DATE.md"
      echo "    -> $OUT_DIR/$DATE.md"
    done
  fi
fi

# ── Dev summary (org-wide, from git) ──

if [ "$TEAM_ONLY" = false ]; then
  echo "--- Dev summary ($CADENCE) ---"

  if [ "$CADENCE" = "daily" ]; then
    GIT_LOG=""
    for repo in $(find "$WORKSPACE/repos" -name ".git" -type d -maxdepth 4 2>/dev/null); do
      RDIR=$(dirname "$repo"); RNAME=$(basename "$RDIR")
      LOG=$(git -C "$RDIR" log --since="$DATE" --until="$NEXT_DATE" --oneline --all 2>/dev/null || true)
      [ -n "$LOG" ] && GIT_LOG="$GIT_LOG
=== $RNAME ===
$LOG
"
    done

    if [ -z "$GIT_LOG" ]; then echo "  No git activity."
    elif [ "$DRY_RUN" = true ]; then echo "  [DRY RUN] $(echo "$GIT_LOG" | grep -c "===") repos"
    else
      DEV_PROMPT_TEMPLATE=$(read_prompt "daily-dev.md")
      DEV_PROMPT="$DEV_PROMPT_TEMPLATE

Date: $DATE

$GIT_LOG"
      SUMMARY=$(claude -p "$DEV_PROMPT" --system-prompt "You are Dream Weaver. Dev facts only. No narrative." --output-format text 2>/dev/null || echo "Summary generation failed")
      ORG_DIR="$WORKSPACE/operations/updates/dev/daily"
      mkdir -p "$ORG_DIR"
      printf "# Dev summary ... %s\n\n%s\n" "$DATE" "$SUMMARY" > "$ORG_DIR/$DATE.md"
      echo "    -> $ORG_DIR/$DATE.md"
    fi
  else
    PARENT=""; case "$CADENCE" in weekly) PARENT="daily" ;; monthly) PARENT="weekly" ;; quarterly) PARENT="monthly" ;; esac
    PDIR="$WORKSPACE/operations/updates/dev/$PARENT"
    if [ ! -d "$PDIR" ] || [ -z "$(ls "$PDIR"/*.md 2>/dev/null)" ]; then echo "  No $PARENT dev summaries."
    elif [ "$DRY_RUN" = true ]; then echo "  [DRY RUN] $(ls "$PDIR"/*.md 2>/dev/null | wc -l | tr -d ' ') files"
    else
      INPUT=""; for f in $(ls -1 "$PDIR"/*.md 2>/dev/null | sort | tail -7); do INPUT="$INPUT
--- $(basename "$f") ---
$(cat "$f")
"; done
      DEV_CON_PROMPT="Consolidate these $PARENT dev summaries into a $CADENCE dev report. What shipped? Key releases? Architecture changes?

$INPUT"
      SUMMARY=$(claude -p "$DEV_CON_PROMPT" --model opus --system-prompt "You are Dream Weaver. Dev facts. No narrative." --output-format text 2>/dev/null || echo "Summary generation failed")
      ORG_DIR="$WORKSPACE/operations/updates/dev/$CADENCE"
      mkdir -p "$ORG_DIR"
      printf "# %s dev summary ... %s\n\n%s\n" "${CADENCE^}" "$DATE" "$SUMMARY" > "$ORG_DIR/$DATE.md"
      echo "    -> $ORG_DIR/$DATE.md"
    fi
  fi
fi

echo ""
echo "=== Summary complete ==="
