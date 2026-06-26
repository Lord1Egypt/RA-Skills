#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: read-policy.sh <command> [args]

Commands:
  list
  get <policy_key>
  help
USAGE
}

run_psql() {
  local sql="$1"
  docker exec -i supabase-db psql -U postgres -d postgres -t -A -c "$sql"
}

cmd_list() {
  run_psql "SELECT key FROM public.openclaw_policies ORDER BY key;"
}

cmd_get() {
  local policy_key="${1:-}"

  if [[ -z "$policy_key" ]]; then
    echo "Error: policy key required" >&2
    exit 1
  fi

  run_psql "SELECT jsonb_pretty(value) FROM public.openclaw_policies WHERE key = '$(printf "%s" "$policy_key" | sed "s/'/''/g")';"
}

main() {
  local cmd="${1:-help}"
  shift || true

  case "$cmd" in
    list) cmd_list ;;
    get) cmd_get "$@" ;;
    help|-h|--help) usage ;;
    *)
      echo "Error: unknown command: $cmd" >&2
      usage
      exit 1
      ;;
  esac
}

main "$@"
