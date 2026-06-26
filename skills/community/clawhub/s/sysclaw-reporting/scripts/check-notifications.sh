#!/usr/bin/env bash
# check-notifications.sh — Check and display notifications for an agent
#
# Usage:
#   check-notifications.sh <agent_name> [mark_read]
#
# Arguments:
#   agent_name   — Your agent name (e.g., jobhunter, pmagent)
#   mark_read    — Set to 'yes' to mark displayed notifications as read (default: no)
#
# Connection (set via environment):
#   SYSCLAW_DB_HOST       (default: localhost)
#   SYSCLAW_DB_PORT       (default: 5432)
#   SYSCLAW_DB_NAME       (default: system_comm)
#   SYSCLAW_DB_USER       (default: issue_reporter)
#   SYSCLAW_DB_PASSWORD
#
# Examples:
#   check-notifications.sh jobhunter          # View unread notifications
#   check-notifications.sh jobhunter yes      # View and mark as read

set -euo pipefail

# --- Dependency check ---
command -v python3 >/dev/null 2>&1 || { echo "Error: python3 not found." >&2; exit 1; }

# --- Arguments ---
agent_name="${1:?Usage: check-notifications.sh <agent_name> [mark_read]}"
mark_read="${2:-no}"

# --- Database config ---
DB_HOST="${SYSCLAW_DB_HOST:-localhost}"
DB_PORT="${SYSCLAW_DB_PORT:-5432}"
DB_NAME="${SYSCLAW_DB_NAME:-system_comm}"
DB_USER="${SYSCLAW_DB_USER:-issue_reporter}"
DB_PASSWORD="${SYSCLAW_DB_PASSWORD:-}"

python3 - "$agent_name" "$mark_read" \
  "$DB_HOST" "$DB_PORT" "$DB_NAME" "$DB_USER" "$DB_PASSWORD" <<'PYEOF'
import sys
import time

try:
    import psycopg2
    import psycopg2.extras
except ImportError:
    print("Error: psycopg2 not installed. Run: pip3 install psycopg2-binary", file=sys.stderr)
    sys.exit(1)

agent_name, mark_read = sys.argv[1:3]
db_host, db_port, db_name, db_user, db_password = sys.argv[3:8]

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
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(query, params)
    return conn, cur

try:
    conn = connect_with_retry()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # Fetch unread notifications
    conn, cur = execute_with_retry(
        conn, cur,
        """
        SELECT id, sender, related_request, message, urgency, created_at
        FROM notifications
        WHERE recipient = %s AND read = FALSE
        ORDER BY created_at ASC
        """,
        (agent_name,),
    )
    rows = cur.fetchall()

    if not rows:
        print("No unread notifications.")
        cur.close()
        conn.close()
        sys.exit(0)

    print("# Unread Notifications\n")
    for row in rows:
        flag = "[read]" if mark_read == "yes" else "[ ]"
        print(f"- {flag} #{row['id']} [{row['urgency']}] from {row['sender']} ({row['created_at']})")
        print(f"  {row['message']}")
        if row['related_request']:
            print(f"  Related request: #{row['related_request']}")
        print()

    print(f"Total: {len(rows)} notification(s)")

    # Mark as read if requested
    if mark_read == "yes":
        conn, cur = execute_with_retry(
            conn, cur,
            "UPDATE notifications SET read = TRUE WHERE recipient = %s AND read = FALSE",
            (agent_name,),
        )
        print("All marked as read.")

    cur.close()
    conn.close()
except psycopg2.OperationalError as e:
    print(f"Error: database connection failed after {MAX_RETRIES} attempts: {e}", file=sys.stderr)
    sys.exit(1)
except psycopg2.Error as e:
    print(f"Error: failed to check notifications: {e}", file=sys.stderr)
    sys.exit(1)
PYEOF
