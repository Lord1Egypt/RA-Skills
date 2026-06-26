#!/usr/bin/env bash
set -euo pipefail
# Resolve symlinks to find the real script location
_REAL_SCRIPT="$(readlink -f "$0")"
_SCRIPT_DIR="$(dirname "$_REAL_SCRIPT")"
DB="${TASK_DB:-$PWD/.tasks.db}"
die() { printf '\033[1;31mError:\033[0m %s\n' "$1" >&2; exit 1; }
ok()  { printf '\033[1;32m✓\033[0m %s\n' "$1"; }
warn(){ printf '\033[1;33m⚠\033[0m %s\n' "$1"; }
require_int() {
  local val="$1"
  local name="${2:-argument}"
  [[ "$val" =~ ^[0-9]+$ ]] || die "$name must be a positive integer (got: '$val')"
}
sql() {
  local _tmpf
  _tmpf=$(mktemp)
  printf '%s\n' "$1" > "$_tmpf"
  sqlite3 -batch "$DB" < "$_tmpf"
  local _rc=$?
  rm -f "$_tmpf"
  return $_rc
}
sql_table() {
  local _tmpf
  _tmpf=$(mktemp)
  printf '.mode column\n.headers on\n.width %s\n%s\n' "$1" "$2" > "$_tmpf"
  sqlite3 -batch "$DB" < "$_tmpf"
  local _rc=$?
  rm -f "$_tmpf"
  return $_rc
}
ensure_db() {
  if [ ! -f "$DB" ]; then
    sqlite3 -batch "$DB" <<'SQL'
CREATE TABLE IF NOT EXISTS tasks (
  id           INTEGER PRIMARY KEY AUTOINCREMENT,
  request_text TEXT    NOT NULL,
  project      TEXT,
  status       TEXT    NOT NULL DEFAULT 'pending',
  priority     INTEGER NOT NULL DEFAULT 5,
  parent_id    INTEGER,
  created_at   TEXT    NOT NULL,
  started_at   TEXT,
  completed_at TEXT,
  last_updated TEXT    NOT NULL,
  notes        TEXT,
  due_date     TEXT,
  tags         TEXT
);
CREATE TABLE IF NOT EXISTS dependencies (
  task_id           INTEGER NOT NULL,
  depends_on_task_id INTEGER NOT NULL,
  PRIMARY KEY (task_id, depends_on_task_id)
);
SQL
  fi
  local has_project
  has_project=$(sqlite3 -batch "$DB" "SELECT COUNT(*) FROM pragma_table_info('tasks') WHERE name='project';")
  if [ "$has_project" -eq 0 ]; then
    sqlite3 -batch "$DB" "ALTER TABLE tasks ADD COLUMN project TEXT;"
  fi
  
  local has_verify
  has_verify=$(sqlite3 -batch "$DB" "SELECT COUNT(*) FROM pragma_table_info('tasks') WHERE name='verification_cmd';")
  if [ "$has_verify" -eq 0 ]; then
    sqlite3 -batch "$DB" "ALTER TABLE tasks ADD COLUMN verification_cmd TEXT;"
  fi

  local has_assignee
  has_assignee=$(sqlite3 -batch "$DB" "SELECT COUNT(*) FROM pragma_table_info('tasks') WHERE name='assignee';")
  if [ "$has_assignee" -eq 0 ]; then
    sqlite3 -batch "$DB" "ALTER TABLE tasks ADD COLUMN assignee TEXT;"
  fi

  local has_due_date
  has_due_date=$(sqlite3 -batch "$DB" "SELECT COUNT(*) FROM pragma_table_info('tasks') WHERE name='due_date';")
  if [ "$has_due_date" -eq 0 ]; then
    sqlite3 -batch "$DB" "ALTER TABLE tasks ADD COLUMN due_date TEXT;"
  fi

  local has_tags
  has_tags=$(sqlite3 -batch "$DB" "SELECT COUNT(*) FROM pragma_table_info('tasks') WHERE name='tags';")
  if [ "$has_tags" -eq 0 ]; then
    sqlite3 -batch "$DB" "ALTER TABLE tasks ADD COLUMN tags TEXT;"
  fi
}
usage() {
cat <<'EOF'
task — local task management
USAGE:
  task create "description" [--priority=N] [--parent=ID] [--project=NAME] [--verify="cmd"] [--due="YYYY-MM-DD"] [--tags="a,b"]
  task edit    ID [--desc="new text"] [--priority=N] [--project=NAME] [--verify="cmd"] [--assignee="NAME"|--unassign] [--due="YYYY-MM-DD"] [--tags="a,b"]
  task start   ID
  task block   ID "reason"
  task complete ID
  task list    [--status=STATUS] [--parent=ID] [--project=NAME] [--format=chat] [--tag="foo"]
  task show    ID
  task board
  task claim   [--agent="NAME"]
  task note    ID "context"
  task export  [--status=STATUS] [--project=NAME] [--json]
  task stuck
  task break   ID "subtask 1" "subtask 2" ...
  task delete  ID [--force]
  task depend  ID DEPENDS_ON_ID
  task unblock ID
  task restart ID
STATUSES: pending, in_progress, blocked, done
ENVIRONMENT:
  TASK_DB   Path to SQLite database (default: ./tasks.db)
EOF
exit 0
}
# ── Source Subcommands ───────────────────────────────────────────────────────
for cmd_file in "$_SCRIPT_DIR/cmds/"*.sh; do
  # shellcheck disable=SC1090
  source "$cmd_file"
done

ensure_db
case "$1" in
  create)   shift; cmd_create "$@" ;;
  edit)     shift; cmd_edit "$@" ;;
  start)    shift; cmd_start "$@" ;;
  block)    shift; cmd_block "$@" ;;
  complete) shift; cmd_complete "$@" ;;
  delete)   shift; cmd_delete "$@" ;;
  list)     shift; cmd_list "$@" ;;
  board)    shift; cmd_board "$@" ;;
  show)     shift; cmd_show "$@" ;;
  claim)    shift; cmd_claim "$@" ;;
  note)     shift; cmd_note "$@" ;;
  export)   shift; cmd_export "$@" ;;
  stuck)    shift; cmd_stuck "$@" ;;
  break)    shift; cmd_break "$@" ;;
  depend)   shift; cmd_depend "$@" ;;
  unblock)  shift; cmd_unblock "$@" ;;
  restart)  shift; cmd_restart "$@" ;;
  help|--help|-h) usage ;;
  *)        die "Unknown command: $1. Run 'task help' for usage." ;;
esac
