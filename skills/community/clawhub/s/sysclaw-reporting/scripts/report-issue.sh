#!/usr/bin/env bash
# report-issue.sh — Report an issue to SysClaw via system_comm.issues
#
# Usage:
#   report-issue.sh <source> <severity> <title> [category] [details] [source_host]
#
# Severity: info | warning | critical
# Category: disk | service | error | resource | network | config | other
#
# Connection (set via environment — ISSUE_DB_* overrides SYSCLAW_DB_*):
#   SYSCLAW_DB_HOST / ISSUE_DB_HOST       (default: localhost)
#   SYSCLAW_DB_PORT / ISSUE_DB_PORT       (default: 5432)
#   SYSCLAW_DB_NAME / ISSUE_DB_NAME       (default: system_comm)
#   SYSCLAW_DB_USER / ISSUE_DB_USER       (default: issue_reporter)
#   SYSCLAW_DB_PASSWORD / ISSUE_DB_PASSWORD
#
# Examples:
#   report-issue.sh jobhunter warning "Disk usage above 80%" disk "df shows 82% on /data" srv-prod-01
#   report-issue.sh propertymanager critical "API returning 500" service "" srv-prod-02

set -euo pipefail

# --- Dependency check ---
command -v python3 >/dev/null 2>&1 || { echo "Error: python3 not found." >&2; exit 1; }

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# --- Arguments ---
source="${1:?Usage: report-issue.sh <source> <severity> <title> [category] [details] [source_host]}"
severity="${2:?Severity required: info | warning | critical}"
title="${3:?Title required}"
category="${4:-other}"
details="${5:-}"
source_host="${6:-$(hostname -f 2>/dev/null || hostname 2>/dev/null || echo "no-host")}"

# Validate severity
case "$severity" in
  info|warning|critical) ;;
  *) echo "Error: severity must be info, warning, or critical" >&2; exit 1 ;;
esac

# --- Database config (ISSUE_DB_* > SYSCLAW_DB_* > defaults) ---
DB_HOST="${ISSUE_DB_HOST:-${SYSCLAW_DB_HOST:-localhost}}"
DB_PORT="${ISSUE_DB_PORT:-${SYSCLAW_DB_PORT:-5432}}"
DB_NAME="${ISSUE_DB_NAME:-${SYSCLAW_DB_NAME:-system_comm}}"
DB_USER="${ISSUE_DB_USER:-${SYSCLAW_DB_USER:-issue_reporter}}"
DB_PASSWORD="${ISSUE_DB_PASSWORD:-${SYSCLAW_DB_PASSWORD:-}}"

python3 - "$source" "$severity" "$title" "$category" "$details" "$source_host" \
  "$DB_HOST" "$DB_PORT" "$DB_NAME" "$DB_USER" "$DB_PASSWORD" <<'PYEOF'
import sys
import time

try:
    import psycopg2
    import psycopg2.extras
except ImportError:
    print("Error: psycopg2 not installed. Run: pip3 install psycopg2-binary", file=sys.stderr)
    sys.exit(1)

source, severity, title, category, details, source_host = sys.argv[1:7]
db_host, db_port, db_name, db_user, db_password = sys.argv[7:12]

MAX_RETRIES = 3
RETRY_DELAYS = [1, 2, 4]  # seconds between attempts (exponential backoff)

def connect_with_retry():
    """Attempt to connect with exponential backoff on failure."""
    last_err = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            conn = psycopg2.connect(
                host=db_host,
                port=db_port,
                dbname=db_name,
                user=db_user,
                password=db_password if db_password else None,
                connect_timeout=10,
            )
            conn.autocommit = True
            return conn
        except psycopg2.OperationalError as e:
            last_err = e
            if attempt < MAX_RETRIES:
                delay = RETRY_DELAYS[attempt - 1]
                print(f"Connection attempt {attempt}/{MAX_RETRIES} failed, retrying in {delay}s...", file=sys.stderr)
                time.sleep(delay)
    raise last_err

def execute_with_retry(conn, cur, query, params):
    """Execute a query, reconnecting once if the connection dropped."""
    try:
        cur.execute(query, params)
    except (psycopg2.OperationalError, psycopg2.InterfaceError):
        # Connection lost mid-session — reconnect and retry once
        print("Connection lost, reconnecting...", file=sys.stderr)
        try:
            conn.close()
        except Exception:
            pass
        conn = connect_with_retry()
        cur = conn.cursor()
        cur.execute(query, params)
    return conn, cur

try:
    conn = connect_with_retry()
    cur = conn.cursor()

    conn, cur = execute_with_retry(
        conn, cur,
        """
        INSERT INTO issues (source, severity, category, title, details, source_host, status)
        VALUES (%s, %s, %s, %s, %s, %s, 'open')
        RETURNING id
        """,
        (source, severity, category, title, details, source_host),
    )
    row = cur.fetchone()
    print(f"Issue #{row[0]} reported successfully")

    cur.close()
    conn.close()
except psycopg2.OperationalError as e:
    print(f"Error: database connection failed after {MAX_RETRIES} attempts: {e}", file=sys.stderr)
    sys.exit(1)
except psycopg2.Error as e:
    print(f"Error: failed to report issue: {e}", file=sys.stderr)
    sys.exit(1)
PYEOF
