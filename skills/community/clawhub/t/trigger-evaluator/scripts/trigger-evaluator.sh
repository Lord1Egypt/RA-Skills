#!/bin/sh
set -eu

WORKSPACE="/home/cmart/.openclaw/workspace"
ENGINE="$WORKSPACE/scripts/stale_missions_engine.sh"
DB_CONTAINER="supabase-db"
DB_USER="postgres"
DB_NAME="postgres"

usage() {
  echo "Usage:"
  echo "  trigger-evaluator.sh evaluate stale_missions_alert"
  echo "  trigger-evaluator.sh inspect stale_missions_alert"
  exit 1
}

cmd="${1:-}"
trigger_name="${2:-}"

[ -n "$cmd" ] || usage
[ -n "$trigger_name" ] || usage

case "$cmd" in
  evaluate)
    [ "$trigger_name" = "stale_missions_alert" ] || {
      echo "Error: unsupported trigger: $trigger_name" >&2
      exit 1
    }
    [ -x "$ENGINE" ] || {
      echo "Error: engine not executable: $ENGINE" >&2
      exit 1
    }
    exec "$ENGINE"
    ;;
  inspect)
    [ "$trigger_name" = "stale_missions_alert" ] || {
      echo "Error: unsupported trigger: $trigger_name" >&2
      exit 1
    }
    docker exec -i "$DB_CONTAINER" psql -U "$DB_USER" -d "$DB_NAME" -At -F $'\t' -c "
SELECT
  id,
  name,
  trigger_event,
  conditions::text,
  action_config::text,
  target_agent,
  cooldown_minutes,
  enabled,
  fire_count,
  COALESCE(last_fired_at::text, ''),
  created_at::text
FROM public.openclaw_trigger_rules
WHERE name = 'stale_missions_alert'
LIMIT 1;
"
    ;;
  *)
    usage
    ;;
esac
