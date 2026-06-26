#!/usr/bin/env bash
set -euo pipefail

# Schedule a one-shot resume cron job that will run after a gateway restart.
# Designed to be created BEFORE restarting the gateway.
#
# Option B behavior:
# - infer delivery route (channel/to) from session key
# - infer model + thinking from the session store for that session key
#
# Usage:
#   schedule-resume-cron.sh --delay 90s --session-key agent:main:discord:channel:123
#
# Optional:
#   --back-delay 75s   (send a short "I'm back" message first)

DELAY="90s"
BACK_DELAY="75s"
SESSION_KEY=""
NAME_RESUME="post-restart-resume"
NAME_BACK="post-restart-back"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --delay) DELAY="$2"; shift 2;;
    --back-delay) BACK_DELAY="$2"; shift 2;;
    --session-key) SESSION_KEY="$2"; shift 2;;
    --name) NAME_RESUME="$2"; shift 2;;
    *) echo "Unknown arg: $1" >&2; exit 2;;
  esac
done

if [[ -z "$SESSION_KEY" ]]; then echo "--session-key is required" >&2; exit 2; fi

# Infer delivery route from sessionKey
DELIVERY_CHANNEL=""
DELIVERY_TO=""
case "$SESSION_KEY" in
  agent:*:discord:channel:*)
    DELIVERY_CHANNEL="discord"
    CH_ID="${SESSION_KEY##*:channel:}"
    DELIVERY_TO="channel:${CH_ID}"
    ;;
  agent:*:discord:direct:*)
    DELIVERY_CHANNEL="discord"
    U_ID="${SESSION_KEY##*:direct:}"
    DELIVERY_TO="user:${U_ID}"
    ;;
  agent:*:telegram:direct:*)
    DELIVERY_CHANNEL="telegram"
    CHAT_ID="${SESSION_KEY##*:direct:}"
    DELIVERY_TO="${CHAT_ID}"
    ;;
  agent:*:telegram:group:*)
    DELIVERY_CHANNEL="telegram"
    CHAT_ID="${SESSION_KEY##*:group:}"
    DELIVERY_TO="${CHAT_ID}"
    ;;
  *)
    echo "Unsupported session key for route inference: $SESSION_KEY" >&2
    exit 2
    ;;
esac

# Infer model + thinking from session store.
# Use a reasonably wide window to avoid missing older-but-still-relevant sessions.
# If this still fails, drop the --active filter.
SESSION_JSON=$(openclaw sessions --active 1440 --json)
MODEL_PROVIDER=$(python3 -c "import json,sys; j=json.loads(sys.argv[1]); key=sys.argv[2]; s=[x for x in j['sessions'] if x.get('key')==key]; print((s[0].get('modelProvider') or '').strip() if s else '')" "$SESSION_JSON" "$SESSION_KEY")
MODEL_NAME=$(python3 -c "import json,sys; j=json.loads(sys.argv[1]); key=sys.argv[2]; s=[x for x in j['sessions'] if x.get('key')==key]; print((s[0].get('model') or '').strip() if s else '')" "$SESSION_JSON" "$SESSION_KEY")
THINKING=$(python3 -c "import json,sys; j=json.loads(sys.argv[1]); key=sys.argv[2]; s=[x for x in j['sessions'] if x.get('key')==key]; print((s[0].get('thinkingLevel') or '').strip() if s else '')" "$SESSION_JSON" "$SESSION_KEY")

if [[ -z "$MODEL_PROVIDER" || -z "$MODEL_NAME" ]]; then
  # Fallback: try without an active filter.
  SESSION_JSON=$(openclaw sessions --json)
  MODEL_PROVIDER=$(python3 -c "import json,sys; j=json.loads(sys.argv[1]); key=sys.argv[2]; s=[x for x in j.get('sessions',[]) if x.get('key')==key]; print((s[0].get('modelProvider') or '').strip() if s else '')" "$SESSION_JSON" "$SESSION_KEY")
  MODEL_NAME=$(python3 -c "import json,sys; j=json.loads(sys.argv[1]); key=sys.argv[2]; s=[x for x in j.get('sessions',[]) if x.get('key')==key]; print((s[0].get('model') or '').strip() if s else '')" "$SESSION_JSON" "$SESSION_KEY")
  THINKING=$(python3 -c "import json,sys; j=json.loads(sys.argv[1]); key=sys.argv[2]; s=[x for x in j.get('sessions',[]) if x.get('key')==key]; print((s[0].get('thinkingLevel') or '').strip() if s else '')" "$SESSION_JSON" "$SESSION_KEY")

  if [[ -z "$MODEL_PROVIDER" || -z "$MODEL_NAME" ]]; then
    echo "Could not infer model for session key: $SESSION_KEY" >&2
    exit 2
  fi
fi
MODEL="$MODEL_PROVIDER/$MODEL_NAME"
if [[ -z "$THINKING" ]]; then THINKING="high"; fi

# Remove any previous stale jobs.
openclaw cron rm "$NAME_BACK" >/dev/null 2>&1 || true
openclaw cron rm "$NAME_RESUME" >/dev/null 2>&1 || true

# 1) "I'm back" message in its own Discord/Telegram message.
openclaw cron add \
  --name "$NAME_BACK" \
  --at "$BACK_DELAY" \
  --agent main \
  --session isolated \
  --session-key "$SESSION_KEY" \
  --model "$MODEL" \
  --thinking "$THINKING" \
  --message "You are back from a gateway restart. Send ONE short, personable message confirming you're back (no extra content). Example: 'Back online — grabbing the thread now.'" \
  --announce \
  --channel "$DELIVERY_CHANNEL" \
  --to "$DELIVERY_TO" \
  --delete-after-run

# 2) Resume the pending task.
openclaw cron add \
  --name "$NAME_RESUME" \
  --at "$DELAY" \
  --agent main \
  --session isolated \
  --session-key "$SESSION_KEY" \
  --model "$MODEL" \
  --thinking "$THINKING" \
  --message "Resume work after gateway restart. Read memory/post-restart-task.md. If it exists and Status is not handled, perform its Next step. Then append a line 'Status: handled' plus an ISO timestamp to the file. Reply with the result only (don't mention thinking/model)." \
  --announce \
  --channel "$DELIVERY_CHANNEL" \
  --to "$DELIVERY_TO" \
  --delete-after-run

echo "Scheduled $NAME_BACK in $BACK_DELAY and $NAME_RESUME in $DELAY to $DELIVERY_CHANNEL/$DELIVERY_TO (sessionKey=$SESSION_KEY, model=$MODEL, thinking=$THINKING)"
