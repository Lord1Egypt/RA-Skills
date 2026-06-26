#!/usr/bin/env bash
# first-triage.sh — Pull last 50 emails from inbox and output JSON summary
# Usage: ./first-triage.sh [account-name]
# Default account: reads from himalaya default account

set -euo pipefail

ACCOUNT="${1:-}"
MAX_EMAILS=50
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
OUTPUT_FILE="${XDG_DATA_HOME:-$HOME/.local/share}/vexpath/triage-$(date +%Y%m%d-%H%M%S).json"

mkdir -p "$(dirname "$OUTPUT_FILE")"

# ── Check himalaya ────────────────────────────────────────────────────────────
if ! command -v himalaya &>/dev/null; then
  echo '{"error": "himalaya not found. Run scripts/setup-email.sh first."}' >&2
  exit 1
fi

# ── Build account flag ────────────────────────────────────────────────────────
ACCOUNT_FLAG=""
if [[ -n "$ACCOUNT" ]]; then
  ACCOUNT_FLAG="--account $ACCOUNT"
fi

echo "Fetching last $MAX_EMAILS emails..." >&2

# ── Fetch envelope list as JSON ───────────────────────────────────────────────
# himalaya envelope list outputs JSON with --output json
RAW_OUTPUT=$(himalaya $ACCOUNT_FLAG envelope list \
  --folder INBOX \
  --page-size "$MAX_EMAILS" \
  --output json 2>&1) || {
  echo "{\"error\": \"Failed to fetch emails. Check account config.\", \"details\": $(echo "$RAW_OUTPUT" | python3 -c 'import sys,json; print(json.dumps(sys.stdin.read()))')}" >&2
  exit 1
}

# ── Build summary JSON ────────────────────────────────────────────────────────
SUMMARY=$(echo "$RAW_OUTPUT" | python3 - "$TIMESTAMP" "$MAX_EMAILS" <<'PYEOF'
import sys
import json
from datetime import datetime, timezone

timestamp = sys.argv[1]
max_count = int(sys.argv[2])
raw = sys.stdin.read().strip()

try:
    emails = json.loads(raw)
    if not isinstance(emails, list):
        raise ValueError("Expected list")
except (json.JSONDecodeError, ValueError) as e:
    print(json.dumps({
        "error": f"Failed to parse himalaya output: {e}",
        "raw_preview": raw[:500]
    }))
    sys.exit(0)

processed = []
for i, email in enumerate(emails):
    entry = {
        "index": i + 1,
        "id": email.get("id", email.get("uid", "")),
        "subject": email.get("subject", "(no subject)"),
        "from": "",
        "from_name": "",
        "from_email": "",
        "date": email.get("date", ""),
        "flags": email.get("flags", []),
        "is_read": "seen" in [f.lower() for f in email.get("flags", [])],
        "folder": "INBOX",
        "triage_status": "pending"
    }

    # Parse from field
    from_field = email.get("from", email.get("sender", ""))
    if isinstance(from_field, list) and from_field:
        from_field = from_field[0]
    if isinstance(from_field, dict):
        name = from_field.get("name", "")
        addr = from_field.get("addr", from_field.get("email", ""))
        entry["from_name"] = name
        entry["from_email"] = addr
        entry["from"] = f"{name} <{addr}>".strip(" <>") if name else addr
    else:
        entry["from"] = str(from_field)
        entry["from_email"] = str(from_field)

    processed.append(entry)

# Count unread
unread_count = sum(1 for e in processed if not e["is_read"])

output = {
    "meta": {
        "timestamp": timestamp,
        "total_fetched": len(processed),
        "max_requested": max_count,
        "unread_count": unread_count,
        "triage_complete": False,
        "account": "default"
    },
    "emails": processed
}

print(json.dumps(output, indent=2, ensure_ascii=False))
PYEOF
)

# ── Save and Output ───────────────────────────────────────────────────────────
echo "$SUMMARY" > "$OUTPUT_FILE"

echo "" >&2
echo "Triage data saved to: $OUTPUT_FILE" >&2
echo "" >&2

# Print summary stats to stderr
python3 - "$OUTPUT_FILE" <<'PYEOF' >&2
import sys
import json

with open(sys.argv[1]) as f:
    data = json.load(f)

meta = data.get("meta", {})
print(f"=== First Triage Summary ===")
print(f"Timestamp:   {meta.get('timestamp', 'N/A')}")
print(f"Total found: {meta.get('total_fetched', 0)}")
print(f"Unread:      {meta.get('unread_count', 0)}")
print(f"")
print(f"Recent emails:")
for email in data.get("emails", [])[:10]:
    read_marker = "  " if email.get("is_read") else "* "
    print(f"  {read_marker}[{email['index']:2}] {email['subject'][:55]:<55}  {email['from_name'] or email['from_email']}")
if len(data.get("emails", [])) > 10:
    print(f"  ... and {len(data['emails']) - 10} more")
print("")
print(f"Feed this output to the email triage process (references/email-triage.md)")
PYEOF

# Output JSON to stdout for piping
echo "$SUMMARY"
