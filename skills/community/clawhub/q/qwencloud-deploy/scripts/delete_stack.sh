#!/usr/bin/env bash
# Full stack destruction: DeleteStack + clean OSS + remove state. See reference/cleanup/delete_stack.md
# Usage: ./delete_stack.sh [--project-root .] [--yes]
set -uo pipefail


ROOT="."
ASSUME_YES=0
while [ $# -gt 0 ]; do
  case "$1" in
    --project-root) ROOT="$2"; shift 2 ;;
    --yes) ASSUME_YES=1; shift ;;
    *) echo "Unknown argument $1" >&2; exit 64 ;;
  esac
done

STATE="$ROOT/.qwencloud-deploy"
[ -f "$STATE" ] || { echo "Cannot find $STATE" >&2; exit 1; }

# Parse the state file in one pass, output shell-safe variable assignments.
# If required fields are missing or file is corrupted, print the specific reason and exit non-zero,
# preventing empty variables that could cause deleting wrong resources or "undefined variable" errors
# that force manual deletion.
EVAL=$(python3 - "$STATE" <<'PY'
import json, shlex, sys
path = sys.argv[1]
try:
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
except Exception as e:
    sys.stderr.write(f"State file {path} parse failed: {e}\n")
    sys.exit(3)

def need(k):
    v = d.get(k)
    if not v:
        sys.stderr.write(f"State file missing required field '{k}', cannot locate deployment resources.\n")
        sys.exit(3)
    return v

_https = d.get("https") or {}
vals = {
    "REGION":    need("region_id"),
    "SID":       need("stack_id"),
    "NAME":      d.get("stack_name") or "",
    "BUCKET":    d.get("artifact_bucket") or "",
    "DB_ENGINE": d.get("db_engine") or "",
    "CREATED":   d.get("created_at") or "",
    "PUBLIC_IP": (d.get("outputs") or {}).get("public_ip") or "",
    "DOMAIN":   d.get("domain") or _https.get("domain") or "",
}

for k, v in vals.items():
    print(f"{k}={shlex.quote(str(v))}")
PY
) || { echo "[delete] Failed to read deployment state, aborted (no resources deleted)." >&2; exit 3; }
eval "$EVAL"

echo "[delete] Releasing resources created by this deployment: stack $NAME ($SID) @ $REGION"
[ -n "$PUBLIC_IP" ] && echo "[delete]   Public IP ${PUBLIC_IP}, created at ${CREATED:-?}"
[ -n "$BUCKET" ]    && echo "[delete]   Includes temporary OSS bucket $BUCKET"
[ -n "$DB_ENGINE" ] && echo "[delete]   Includes RDS (${DB_ENGINE}), deletion takes ~10-30 minutes"
[ -n "$DOMAIN" ]    && echo "[delete]   DNS A record for $DOMAIN will be removed"
echo "[delete] Only deletes this stack's resources, does not affect other account resources; full stack destruction is irreversible."

if [ "$ASSUME_YES" -ne 1 ]; then
  read -r -p "Continue? Type 'DELETE' to confirm: " ANS
  [ "$ANS" = "DELETE" ] || { echo "Cancelled" >&2; exit 1; }
fi

# The OSS staging bucket is a separate resource from the stack: even when stack
# deletion fails or times out we should still try to clean it, otherwise the user
# is left thinking things are half-deleted without knowing to come back.
cleanup_bucket() {
  [ -n "$BUCKET" ] || return 0
  # Only clean buckets created by this tool: name has the qwencloud-deploy-tmp- prefix,
  # or carries the from=qwencloud tag.
  case "$BUCKET" in
    qwencloud-deploy-tmp-*) : ;;
    *)
      if ! aliyun oss bucket-tagging --method get "oss://$BUCKET/" 2>/dev/null | tr -d '\n' | grep -q 'from.*qwencloud'; then
        echo "[delete] Skipping OSS bucket $BUCKET: not created by this tool (no qwencloud-deploy-tmp- prefix and no from=qwencloud tag); leaving it intact." >&2
        return 0
      fi
      ;;
  esac
  echo "[delete] Cleaning OSS bucket $BUCKET"
  if ! aliyun oss rm "oss://$BUCKET" -r -f >/dev/null 2>&1 \
     || ! aliyun oss rm "oss://$BUCKET" -b -f >/dev/null 2>&1; then
    echo "[delete] Warning: OSS bucket $BUCKET was not fully cleaned. The bucket has a 7-day auto-expiration lifecycle and won't incur ongoing charges;" >&2
    echo "         to delete immediately, clean up manually in OSS console." >&2
    return 1
  fi
  return 0
}

# Single exit path for "stack not fully deleted": clean the bucket first, then
# spell out what is left and what to do next, and keep the state file so this
# script can simply be re-run.
abort_unfinished() {
  local reason="$1"
  echo "[delete] $reason" >&2
  cleanup_bucket || true
  echo "[delete] Stack $NAME ($SID) @ $REGION is not confirmed deleted; local state file $STATE was kept." >&2
  [ -n "$DOMAIN" ] && echo "[delete] DNS A record for $DOMAIN was left in place (removed once the stack is gone)." >&2
  echo "[delete] Next: re-run ./delete_stack.sh --project-root \"$ROOT\" later," >&2
  echo "         or inspect the stack in the ROS console: https://ros.console.aliyun.com/" >&2
  exit 2
}

# 1) DeleteStack
OUT=$(aliyun ros DeleteStack --RegionId "$REGION" --StackId "$SID" 2>&1)
CODE=$?
if [ $CODE -ne 0 ]; then
  if echo "$OUT" | grep -qiE 'StackNotFound|404'; then
    echo "[delete] Stack already does not exist"
  else
    abort_unfinished "DeleteStack failed: $OUT"
  fi
fi

# 2) Poll until 404 (extend to 45 minutes when RDS is included)
DELETE_TIMEOUT_MIN=20
[ -n "$DB_ENGINE" ] && DELETE_TIMEOUT_MIN=45
DEADLINE=$(( $(date +%s) + DELETE_TIMEOUT_MIN * 60 ))
while :; do
  if [ "$(date +%s)" -gt $DEADLINE ]; then
    abort_unfinished "Timed out waiting for deletion (${DELETE_TIMEOUT_MIN}m). Deletion may still be running in the background."
  fi
  OUT=$(aliyun ros GetStack --RegionId "$REGION" --StackId "$SID" 2>&1)
  if echo "$OUT" | grep -qiE 'StackNotFound|404'; then
    echo "[delete] Stack DELETE_COMPLETE"
    break
  fi
  STATUS=$(echo "$OUT" | python3 -c "import json,sys;print(json.load(sys.stdin).get('Status',''))" 2>/dev/null || echo "?")
  echo "[delete] $(date -u +%H:%M:%S) Status=$STATUS"
  if [ "$STATUS" = "DELETE_COMPLETE" ]; then
    echo "[delete] Stack DELETE_COMPLETE"
    break
  fi
  if [ "$STATUS" = "DELETE_FAILED" ]; then
    echo "$OUT" >&2
    abort_unfinished "DeleteStack failed (DELETE_FAILED); please clean up leftover resources in the console."
  fi
  sleep 10
done

# 3) Clean up OSS temporary bucket
cleanup_bucket || true

# 4) Clean up DNS record (if domain was configured)
if [ -n "$DOMAIN" ]; then
  echo "[delete] Cleaning DNS A record for $DOMAIN"
  # Split domain into RR and base domain
  PARTS=(${DOMAIN//./ })
  NUM_PARTS=${#PARTS[@]}
  if [ "$NUM_PARTS" -le 2 ]; then
    RR="@"
    DNS_DOMAIN="$DOMAIN"
  else
    RR="${PARTS[0]}"
    DNS_DOMAIN="${DOMAIN#*.}"
  fi

  # Find and delete the A record
  RECORD_ID=$(aliyun alidns DescribeDomainRecords \
    --DomainName "$DNS_DOMAIN" --RRKeyWord "$RR" --TypeKeyWord A 2>/dev/null \
    | python3 -c "
import json, sys
try:
    d = json.load(sys.stdin)
    for r in d.get('DomainRecords', {}).get('Record', []):
        if r.get('RR') == '$RR' and r.get('Type') == 'A':
            print(r['RecordId'])
            break
except:
    pass
" 2>/dev/null)

  if [ -n "$RECORD_ID" ]; then
    if aliyun alidns DeleteDomainRecord --RecordId "$RECORD_ID" >/dev/null 2>&1; then
      echo "[delete] DNS A record removed: $DOMAIN"
    else
      echo "[delete] Warning: failed to remove DNS A record for $DOMAIN. Please delete manually in Alidns console." >&2
    fi
  else
    echo "[delete] No DNS A record found for $DOMAIN (may have been removed already)"
  fi
fi

# 5) Clean up local state files
rm -f "$STATE" "$ROOT/.qwencloud-deploy.local"
echo "[delete] Done. Local .qwencloud-deploy(.local) deleted."
