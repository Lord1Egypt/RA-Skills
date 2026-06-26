#!/usr/bin/env bash
# request-resource.sh — Submit a request to SysClaw via system_comm.agent_requests
#
# Usage:
#   request-resource.sh <source> <type> <action> <target> <justification> [urgency] [payload] [source_host]
#
# Types:      access | software | resource | config | service | deployment | info
# Actions:    install | remove | create | modify | restart | grant | check | deploy
# Urgency:    low | normal | urgent (default: normal)
# Payload:    JSON string for request-specific details (optional)
#
# Connection (set via environment — REQUEST_DB_* overrides SYSCLAW_DB_*):
#   SYSCLAW_DB_HOST / REQUEST_DB_HOST       (default: localhost)
#   SYSCLAW_DB_PORT / REQUEST_DB_PORT       (default: 5432)
#   SYSCLAW_DB_NAME / REQUEST_DB_NAME       (default: system_comm)
#   SYSCLAW_DB_USER / REQUEST_DB_USER       (default: issue_reporter)
#   SYSCLAW_DB_PASSWORD / REQUEST_DB_PASSWORD
#
# Examples:
#   request-resource.sh jobhunter software install nginx '{"version":"latest"}' normal
#   request-resource.sh pmagent access grant /var/data/pm '{"level":"read"}'

set -euo pipefail

# --- Dependency check ---
command -v python3 >/dev/null 2>&1 || { echo "Error: python3 not found." >&2; exit 1; }

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# --- Arguments ---
source="${1:?Usage: request-resource.sh <source> <type> <action> <target> <justification> [urgency] [payload] [source_host]}"
request_type="${2:?Type required: access | software | resource | config | service | deployment | info}"
action="${3:?Action required: install | remove | create | modify | restart | grant | check | deploy}"
target="${4:?Target required — what this request applies to}"
justification="${5:?Justification required — explain why you need this}"
urgency="${6:-normal}"
payload="${7:-}"
source_host="${8:-$(hostname -f 2>/dev/null || hostname 2>/dev/null || echo "no-host")}"

# Validate type
case "$request_type" in
  access|software|resource|config|service|deployment|info) ;;
  *) echo "Error: type must be access, software, resource, config, service, deployment, or info" >&2; exit 1 ;;
esac

# Validate urgency
case "$urgency" in
  low|normal|urgent) ;;
  *) echo "Error: urgency must be low, normal, or urgent" >&2; exit 1 ;;
esac

# Validate JSON payload if provided
if [[ -n "$payload" ]]; then
  if ! echo "$payload" | python3 -c "import sys,json; json.load(sys.stdin)" 2>/dev/null; then
    echo "Error: payload is not valid JSON" >&2
    exit 1
  fi
fi

# --- Database config (REQUEST_DB_* > SYSCLAW_DB_* > defaults) ---
DB_HOST="${REQUEST_DB_HOST:-${SYSCLAW_DB_HOST:-localhost}}"
DB_PORT="${REQUEST_DB_PORT:-${SYSCLAW_DB_PORT:-5432}}"
DB_NAME="${REQUEST_DB_NAME:-${SYSCLAW_DB_NAME:-system_comm}}"
DB_USER="${REQUEST_DB_USER:-${SYSCLAW_DB_USER:-issue_reporter}}"
DB_PASSWORD="${REQUEST_DB_PASSWORD:-${SYSCLAW_DB_PASSWORD:-}}"

python3 - "$source" "$request_type" "$action" "$target" "$justification" "$urgency" "$payload" "$source_host" \
  "$DB_HOST" "$DB_PORT" "$DB_NAME" "$DB_USER" "$DB_PASSWORD" <<'PYEOF'
import sys
import json
import time

try:
    import psycopg2
    import psycopg2.extras
except ImportError:
    print("Error: psycopg2 not installed. Run: pip3 install psycopg2-binary", file=sys.stderr)
    sys.exit(1)

source, request_type, action, target, justification = sys.argv[1:6]
urgency, payload, source_host = sys.argv[6:9]
db_host, db_port, db_name, db_user, db_password = sys.argv[9:14]

# Parse JSON payload
payload_json = None
if payload:
    try:
        payload_json = json.dumps(json.loads(payload))
    except json.JSONDecodeError as e:
        print(f"Error: invalid JSON payload: {e}", file=sys.stderr)
        sys.exit(1)

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

    # Insert request
    conn, cur = execute_with_retry(
        conn, cur,
        """
        INSERT INTO agent_requests
            (requesting_agent, request_type, action, target, justification, urgency, payload, source_host)
        VALUES (%s, %s, %s, %s, %s, %s, %s::jsonb, %s)
        RETURNING id
        """,
        (source, request_type, action, target, justification, urgency, payload_json, source_host),
    )
    request_id = cur.fetchone()[0]
    print(f"Request #{request_id} submitted successfully")

    # Notify SysClaw
    notify_msg = f"New {request_type} request: {action} {target}"
    conn, cur = execute_with_retry(
        conn, cur,
        """
        INSERT INTO notifications (recipient, sender, related_request, message, urgency)
        VALUES (%s, %s, %s, %s, %s)
        """,
        ("sysclaw", source, request_id, notify_msg, urgency),
    )
    print("SysClaw notified.")

    cur.close()
    conn.close()
except psycopg2.OperationalError as e:
    print(f"Error: database connection failed after {MAX_RETRIES} attempts: {e}", file=sys.stderr)
    sys.exit(1)
except psycopg2.Error as e:
    print(f"Error: failed to submit request: {e}", file=sys.stderr)
    if "request_id" not in dir():
        print("  (request was not created)", file=sys.stderr)
    else:
        print(f"  (request #{request_id} was created but notification may have failed)", file=sys.stderr)
    sys.exit(1)
PYEOF
