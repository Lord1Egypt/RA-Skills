#!/usr/bin/env bash
set -euo pipefail

export CLAWD_DIR="${CLAWD_DIR:-$HOME/clawd}"
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STATE_TEMPLATE="$SKILL_DIR/state-template.json"
STATE_DIR="$SKILL_DIR/state"
STATE_FILE="$STATE_DIR/state.json"
CONFIG_DEFAULT="$SKILL_DIR/config/skill-miner.config.json"
CONFIG_LOCAL="$SKILL_DIR/config/skill-miner.config.local.json"

mkdir -p "$STATE_DIR" "$SKILL_DIR/state/logs" "$SKILL_DIR/state/review" "$SKILL_DIR/state/write-log"

if [ ! -f "$STATE_FILE" ]; then
  cp "$STATE_TEMPLATE" "$STATE_FILE"
  echo "Created $STATE_FILE"
else
  echo "Kept existing $STATE_FILE"
fi

if [ ! -f "$CONFIG_LOCAL" ]; then
  cp "$CONFIG_DEFAULT" "$CONFIG_LOCAL"
  echo "Created $CONFIG_LOCAL"
else
  echo "Kept existing $CONFIG_LOCAL"
fi

NIGHTLY_CMD="export CLAWD_DIR=\"$CLAWD_DIR\" && bash \"$SKILL_DIR/scripts/run-nightly-scan.sh\""
WRITE_CMD="export CLAWD_DIR=\"$CLAWD_DIR\" && bash \"$SKILL_DIR/scripts/run-morning-write.sh\""
MANUAL_CMD="export CLAWD_DIR=\"$CLAWD_DIR\" && \"$SKILL_DIR/scripts/skillminer\""

if [ "$EUID" -eq 0 ]; then
  if [ -e /usr/local/bin/skillminer ] || [ -L /usr/local/bin/skillminer ]; then
    SYMLINK_NOTE="Skipped /usr/local/bin/skillminer because it already exists. Review it manually before cleanup or replacement."
  else
    ln -s "$SKILL_DIR/scripts/skillminer" /usr/local/bin/skillminer
    SYMLINK_NOTE="Installed /usr/local/bin/skillminer -> $SKILL_DIR/scripts/skillminer"
  fi
else
  SYMLINK_NOTE="Not root, skipped /usr/local/bin/skillminer symlink install."
fi

cat <<EOF

skillminer setup complete.

Run one manual scan before adding any scheduler jobs:
  $NIGHTLY_CMD

Manual wrappers:
  Nightly: $NIGHTLY_CMD
  Morning: $WRITE_CMD
  Shortcut: $MANUAL_CMD <scan|write|full|status|help>

Symlink setup:
  $SYMLINK_NOTE

Recommended scheduler pattern (OpenClaw cron):
  - payload.kind: agentTurn
  - payload.message: inline contents of prompts/cron-dispatch-nightly.md
    (or prompts/cron-dispatch-morning.md for the morning-write job)
  - delivery.mode: announce
  - delivery target: your channel/topic

The dispatch prompt executes $SKILL_DIR/scripts/run-nightly-scan.sh (or run-morning-write.sh)
via the bash tool. The wrapper owns flock, state backup, atomic .tmp promotion, and
JSON validation. Do NOT inline nightly-scan.md or skill-writer.md directly, those prompts
write to .tmp files and require the wrapper for atomic promotion.

Notifications are handled by cron announce delivery.
Review output is always written locally under:
  $SKILL_DIR/state/review/
  $SKILL_DIR/state/write-log/
EOF
