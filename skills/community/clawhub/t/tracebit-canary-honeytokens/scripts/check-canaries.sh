#!/usr/bin/env bash
# check-canaries.sh — Show Tracebit canary status and warn about expiry
#
# Primary method: tracebit show (CLI)
# Fallback:       parse ~/.config/tracebit/canaries.json (for environments without CLI)
#
# Usage:
#   bash skills/tracebit-canaries/scripts/check-canaries.sh
#   bash skills/tracebit-canaries/scripts/check-canaries.sh --json

set -euo pipefail

JSON_OUTPUT=false
[[ "${1:-}" == "--json" ]] && JSON_OUTPUT=true

# ── Colors ────────────────────────────────────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; NC='\033[0m'
info()  { [[ "$JSON_OUTPUT" == "false" ]] && echo -e "${BLUE}[check-canaries]${NC} $*"; }
ok()    { [[ "$JSON_OUTPUT" == "false" ]] && echo -e "${GREEN}[check-canaries]${NC} $*"; }
warn()  { [[ "$JSON_OUTPUT" == "false" ]] && echo -e "${YELLOW}[check-canaries]${NC} $*" >&2; }
err()   { [[ "$JSON_OUTPUT" == "false" ]] && echo -e "${RED}[check-canaries]${NC} $*" >&2; }

# ── Expiry helper (requires date command) ─────────────────────────────────────
days_until_expiry() {
  local expiry_str="$1"
  if [[ -z "$expiry_str" || "$expiry_str" == "null" ]]; then
    echo "unknown"
    return
  fi

  local expiry_epoch now_epoch days
  if date --version >/dev/null 2>&1; then
    # GNU date (Linux)
    expiry_epoch=$(date -d "$expiry_str" +%s 2>/dev/null) || { echo "unknown"; return; }
  else
    # BSD date (macOS)
    expiry_epoch=$(date -j -f "%Y-%m-%dT%H:%M:%SZ" "$expiry_str" +%s 2>/dev/null) || \
    expiry_epoch=$(date -j -f "%Y-%m-%dT%H:%M:%S" "${expiry_str%Z}" +%s 2>/dev/null) || \
    { echo "unknown"; return; }
  fi

  now_epoch=$(date +%s)
  days=$(( (expiry_epoch - now_epoch) / 86400 ))
  echo "$days"
}

# ── Method 1: tracebit CLI ────────────────────────────────────────────────────
if command -v tracebit >/dev/null 2>&1; then
  info "Running: tracebit show"
  echo ""

  if "$JSON_OUTPUT"; then
    # Attempt JSON output if CLI supports it
    tracebit show --json 2>/dev/null || tracebit show 2>&1
  else
    tracebit show 2>&1 || {
      warn "tracebit show failed — falling back to local cache"
    }
  fi

  # Additional expiry check from local cache if available
  CACHE_FILE="${HOME}/.config/tracebit/canaries.json"
  if [[ -f "$CACHE_FILE" ]]; then
    echo ""
    info "Checking expiry from local cache: $CACHE_FILE"

    for type in aws ssh; do
      EXPIRY=$(python3 -c "
import sys, json
with open('$CACHE_FILE') as f:
    data = json.load(f)
creds = data.get('${type}', data.get('credentials', {}).get('${type}', {}))
print(creds.get('expiration') or creds.get('awsExpiration') or creds.get('sshExpiration') or '')
" 2>/dev/null || true)

      if [[ -n "$EXPIRY" ]]; then
        DAYS=$(days_until_expiry "$EXPIRY")
        if [[ "$DAYS" == "unknown" ]]; then
          warn "  $type: expiry unknown ($EXPIRY)"
        elif [[ "$DAYS" -lt 0 ]]; then
          err "  $type: EXPIRED ($EXPIRY) — run: tracebit deploy $type"
        elif [[ "$DAYS" -lt 3 ]]; then
          warn "  $type: expires in ${DAYS} day(s) — run: tracebit refresh"
        else
          ok "  $type: active, expires in ${DAYS} day(s)"
        fi
      fi
    done
  fi

  echo ""
  info "To open the web dashboard: tracebit portal"
  exit 0
fi

# ── Method 2: Local JSON fallback ─────────────────────────────────────────────
warn "Tracebit CLI not found. Falling back to local cache."

CACHE_FILE="${HOME}/.config/tracebit/canaries.json"

if [[ ! -f "$CACHE_FILE" ]]; then
  err "No local cache at $CACHE_FILE"
  err "Install the CLI: bash skills/tracebit-canaries/scripts/install-tracebit.sh"
  exit 1
fi

info "Reading: $CACHE_FILE"

if ! command -v python3 >/dev/null 2>&1; then
  warn "python3 not available — showing raw JSON"
  cat "$CACHE_FILE"
  exit 0
fi

python3 - "$CACHE_FILE" << 'PYEOF'
import sys, json, datetime

path = sys.argv[1]
with open(path) as f:
    data = json.load(f)

now = datetime.datetime.utcnow()

def check_expiry(expiry_str):
    if not expiry_str:
        return "unknown expiry"
    try:
        exp = datetime.datetime.strptime(expiry_str, "%Y-%m-%dT%H:%M:%SZ")
        delta = exp - now
        days = delta.days
        if days < 0:
            return f"EXPIRED ({expiry_str})"
        elif days < 3:
            return f"EXPIRING SOON — {days} day(s) left ({expiry_str})"
        else:
            return f"active — {days} day(s) left ({expiry_str})"
    except Exception:
        return f"expiry: {expiry_str}"

print("\n=== Tracebit Canary Status (from local cache) ===\n")

type_fields = {
    "aws":   ("awsExpiration", "expiration"),
    "ssh":   ("sshExpiration", "expiration"),
    "http":  ("expiration",),
}

for ctype, fields in type_fields.items():
    section = data.get(ctype) or data.get("credentials", {}).get(ctype)
    if not section:
        continue
    expiry = None
    for field in fields:
        expiry = section.get(field)
        if expiry:
            break
    status = check_expiry(expiry)
    print(f"  {ctype:20s} {status}")

print()
if data.get("name"):
    print(f"  Canary name: {data['name']}")
if data.get("deployed_at"):
    print(f"  Deployed at: {data['deployed_at']}")

print()
print("Note: Install the Tracebit CLI for live status: bash skills/tracebit-canaries/scripts/install-tracebit.sh")
PYEOF
