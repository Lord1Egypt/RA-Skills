#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="$SCRIPT_DIR/.safeflow-config.json"

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; NC='\033[0m'
info()    { echo -e "${BLUE}[sql-sync]${NC} $*"; }
success() { echo -e "${GREEN}[sql-sync]${NC} $*"; }
warn()    { echo -e "${YELLOW}[sql-sync]${NC} $*"; }
error()   { echo -e "${RED}[sql-sync]${NC} $*" >&2; }

usage() {
    cat <<'EOF'
Usage:
  ./sync_package_id_to_sql.sh [options]

Options:
  --package-id <id>                Package id to sync (default: .safeflow-config.json)
  --driver <sqlite|postgres>       SQL driver (default: sqlite)
  --sqlite-db <path>               SQLite DB file (default: .safeflow-runtime.db)
  --postgres-dsn <dsn>             Postgres DSN (required for postgres driver)
  --table <name>                   Config table name (default: safeflow_runtime_config)
  --key <name>                     Config key (default: package_id)
  -h, --help                       Show help
EOF
}

is_sui_address() {
    [[ "$1" =~ ^0x[0-9a-fA-F]{64}$ ]]
}

is_safe_identifier() {
    [[ "$1" =~ ^[A-Za-z_][A-Za-z0-9_]*$ ]]
}

is_safe_key() {
    [[ "$1" =~ ^[A-Za-z0-9_.-]+$ ]]
}

PACKAGE_ID=""
DRIVER="sqlite"
SQLITE_DB="$SCRIPT_DIR/.safeflow-runtime.db"
POSTGRES_DSN=""
TABLE_NAME="safeflow_runtime_config"
CONFIG_KEY="package_id"

while [[ $# -gt 0 ]]; do
    case "$1" in
        --package-id) PACKAGE_ID="${2:-}"; shift 2 ;;
        --driver) DRIVER="${2:-}"; shift 2 ;;
        --sqlite-db) SQLITE_DB="${2:-}"; shift 2 ;;
        --postgres-dsn) POSTGRES_DSN="${2:-}"; shift 2 ;;
        --table) TABLE_NAME="${2:-}"; shift 2 ;;
        --key) CONFIG_KEY="${2:-}"; shift 2 ;;
        -h|--help) usage; exit 0 ;;
        *) error "Unknown argument: $1"; usage; exit 1 ;;
    esac
done

if [[ -z "$PACKAGE_ID" ]]; then
    if [[ ! -f "$CONFIG_FILE" ]]; then
        error "Missing --package-id and no $CONFIG_FILE found."
        exit 1
    fi
    if ! command -v jq >/dev/null 2>&1; then
        error "jq not found, cannot read package id from config."
        exit 1
    fi
    PACKAGE_ID="$(jq -r '.packageId // empty' "$CONFIG_FILE")"
fi

if ! is_sui_address "$PACKAGE_ID"; then
    error "Invalid package id: $PACKAGE_ID"
    exit 1
fi

if ! is_safe_identifier "$TABLE_NAME"; then
    error "Invalid table name: $TABLE_NAME"
    exit 1
fi

if ! is_safe_key "$CONFIG_KEY"; then
    error "Invalid config key: $CONFIG_KEY"
    exit 1
fi

case "$DRIVER" in
    sqlite)
        if ! command -v sqlite3 >/dev/null 2>&1; then
            error "sqlite3 command not found."
            exit 1
        fi
        mkdir -p "$(dirname "$SQLITE_DB")"
        sqlite3 "$SQLITE_DB" <<EOF
CREATE TABLE IF NOT EXISTS $TABLE_NAME (
  config_key TEXT PRIMARY KEY,
  config_value TEXT NOT NULL,
  updated_at INTEGER NOT NULL
);
INSERT INTO $TABLE_NAME (config_key, config_value, updated_at)
VALUES ('$CONFIG_KEY', '$PACKAGE_ID', strftime('%s','now'))
ON CONFLICT(config_key)
DO UPDATE SET
  config_value = excluded.config_value,
  updated_at = excluded.updated_at;
EOF
        success "Synced package id to SQLite."
        echo "  DB:      $SQLITE_DB"
        echo "  Table:   $TABLE_NAME"
        echo "  Key:     $CONFIG_KEY"
        echo "  Value:   $PACKAGE_ID"
        ;;
    postgres)
        if ! command -v psql >/dev/null 2>&1; then
            error "psql command not found."
            exit 1
        fi
        if [[ -z "$POSTGRES_DSN" ]]; then
            error "--postgres-dsn is required for postgres driver."
            exit 1
        fi
        psql "$POSTGRES_DSN" -v ON_ERROR_STOP=1 <<EOF
CREATE TABLE IF NOT EXISTS $TABLE_NAME (
  config_key TEXT PRIMARY KEY,
  config_value TEXT NOT NULL,
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
INSERT INTO $TABLE_NAME (config_key, config_value, updated_at)
VALUES ('$CONFIG_KEY', '$PACKAGE_ID', NOW())
ON CONFLICT (config_key)
DO UPDATE SET
  config_value = EXCLUDED.config_value,
  updated_at = NOW();
EOF
        success "Synced package id to Postgres."
        echo "  Table: $TABLE_NAME"
        echo "  Key:   $CONFIG_KEY"
        echo "  Value: $PACKAGE_ID"
        ;;
    *)
        error "Unsupported --driver: $DRIVER"
        exit 1
        ;;
esac
