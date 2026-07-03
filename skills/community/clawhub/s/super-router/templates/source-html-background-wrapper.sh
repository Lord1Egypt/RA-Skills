#!/usr/bin/env bash
# Template for Super-Router background jobs that analyze a local source tree and
# produce a durable self-contained HTML guide/report.
# Copy into ~/.openclaw/logs/<task>_<timestamp>/run_<task>_router.sh and replace
# the ALL_CAPS placeholders. Launch with exec(background=true, notify_on_complete=true).

set -uo pipefail
RUN_DIR="RUN_DIR_ABSOLUTE_PATH"
SRC="SOURCE_TREE_ABSOLUTE_PATH"
ROUTER="$HOME/.openclaw/skills/super-router/scripts/router.py"
PY="/opt/homebrew/Caskroom/miniforge/base/bin/python"
if [ ! -x "$PY" ]; then PY="$(command -v python3)"; fi

CTX="$RUN_DIR/context.json"
PROMPT="$RUN_DIR/router_prompt.txt"
LOG="$RUN_DIR/super_router_stream.log"
OUT="$RUN_DIR/FINAL_ARTIFACT.html"
STATUS="$RUN_DIR/status.txt"
: > "$STATUS"

printf '[scope] src=%s\n[scope] out=%s\n[scope] router=%s\n[scope] py=%s\n' \
  "$SRC" "$OUT" "$ROUTER" "$PY" | tee -a "$STATUS"

export SOURCE_SRC="$SRC" CONTEXT_OUT="$CTX" ROUTER_PROMPT="$PROMPT" ROUTER_LOG="$LOG" HTML_OUT="$OUT" RUN_DIR

printf '[step] collect context\n' | tee -a "$STATUS"
python3 "$RUN_DIR/collect_context.py" 2>&1 | tee -a "$STATUS"
COLLECT_EXIT=${PIPESTATUS[0]}
if [ "$COLLECT_EXIT" -ne 0 ]; then
  printf '[failed] collect exit=%s\n' "$COLLECT_EXIT" | tee -a "$STATUS"
  exit "$COLLECT_EXIT"
fi

printf '[step] build router prompt\n' | tee -a "$STATUS"
python3 "$RUN_DIR/make_router_prompt.py" 2>&1 | tee -a "$STATUS"
PROMPT_EXIT=${PIPESTATUS[0]}
if [ "$PROMPT_EXIT" -ne 0 ]; then
  printf '[failed] prompt exit=%s\n' "$PROMPT_EXIT" | tee -a "$STATUS"
  exit "$PROMPT_EXIT"
fi

printf '[step] run super-router stream\n' | tee -a "$STATUS"
set +e
zsh -lic "export ROUTER_TASK=\"\$(/bin/cat '$PROMPT')\"; '$PY' '$ROUTER' --stream" 2>&1 | tee "$LOG"
ROUTER_EXIT=${PIPESTATUS[0]}
set -e
printf '[step] router exit=%s\n' "$ROUTER_EXIT" | tee -a "$STATUS"
export ROUTER_EXIT

printf '[step] generate html\n' | tee -a "$STATUS"
python3 "$RUN_DIR/generate_html.py" 2>&1 | tee -a "$STATUS"
GEN_EXIT=${PIPESTATUS[0]}
if [ "$GEN_EXIT" -ne 0 ]; then
  printf '[failed] html generation exit=%s router_exit=%s\n' "$GEN_EXIT" "$ROUTER_EXIT" | tee -a "$STATUS"
  exit "$GEN_EXIT"
fi

printf '[step] verify html\n' | tee -a "$STATUS"
if [ ! -s "$OUT" ]; then
  printf '[failed] missing html=%s router_exit=%s\n' "$OUT" "$ROUTER_EXIT" | tee -a "$STATUS"
  exit 20
fi
BYTES=$(wc -c < "$OUT" | tr -d ' ')
SECTIONS=$(grep -Eo '<section' "$OUT" | wc -l | tr -d ' ')
WORKFLOWS=$(grep -Eo 'class="workflow"' "$OUT" | wc -l | tr -d ' ')
DETAILS=$(grep -Eo '<details' "$OUT" | wc -l | tr -d ' ')
SVG=$(grep -Eo '<svg' "$OUT" | wc -l | tr -d ' ')
printf '[verify] html=%s bytes=%s sections=%s workflows=%s details=%s svg=%s router_exit=%s\n' \
  "$OUT" "$BYTES" "$SECTIONS" "$WORKFLOWS" "$DETAILS" "$SVG" "$ROUTER_EXIT" | tee -a "$STATUS"

# Tune thresholds per artifact class. Keep them high enough to catch a half-written file.
if [ "$BYTES" -lt MIN_BYTES ] || [ "$SECTIONS" -lt MIN_SECTIONS ] || \
   [ "$WORKFLOWS" -lt MIN_WORKFLOWS ] || [ "$DETAILS" -lt MIN_DETAILS ] || [ "$SVG" -lt 1 ]; then
  printf '[failed] verification thresholds not met\n' | tee -a "$STATUS"
  exit 21
fi

printf '[done] html artifact verified. router_exit=%s\n' "$ROUTER_EXIT" | tee -a "$STATUS"
exit 0
