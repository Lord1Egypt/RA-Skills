#!/usr/bin/env bash
# Create ROS stack (retry-safe). See reference/deploy/11_create_stack.md
# Usage: ./create_stack.sh <region> <template-url> <stack-name> <params-file>
# Env: APP_NAME APP_DESC [PROJECT_ROOT] [TIMEOUT_MIN]
# stdout: StackId  Exit: 0=success
set -uo pipefail

usage() {
  echo "Usage: $0 <region> <template-url> <stack-name> <params-file>" >&2
  exit 64
}
[ $# -eq 4 ] || usage
REGION="$1"; TPL_URL="$2"; NAME="$3"; PARAMS_FILE="$4"
: "${APP_NAME:?missing APP_NAME}"
: "${APP_DESC:?missing APP_DESC}"
case "$APP_NAME" in
  [a-z]*) [[ "$APP_NAME" =~ ^[a-z][a-z0-9-]{0,30}$ ]] || { echo "Invalid APP_NAME: $APP_NAME (must match ^[a-z][a-z0-9-]{0,30}\$)" >&2; exit 64; } ;;
  *) echo "Invalid APP_NAME: $APP_NAME (must start with a lowercase letter; only lowercase letters/digits/hyphen, length 1-31)" >&2; exit 64 ;;
esac
[ -f "$PARAMS_FILE" ] || { echo "params-file not found: $PARAMS_FILE" >&2; exit 1; }
PROJECT_ROOT="${PROJECT_ROOT:-.}"
# ROS-side timeout: without RDS, ECS+EIP is usually ready in 2-5 minutes, so 15
# minutes is already generous; pass 40 when RDS is included. Keep the relation
# "client --max-wait > ROS TimeoutInMinutes" (see wait_and_probe.py), otherwise
# ROS has already failed the stack while the client keeps waiting.
TIMEOUT="${TIMEOUT_MIN:-15}"

# Build --Parameters.N.ParameterKey/Value from JSON file.
# NUL-separated instead of tab/newline: values may legitimately contain newlines
# or tabs (APP_DESC, UserDataScript), and line-based reading would split one
# value into several bogus parameters. The file path is passed via argv so a
# quote in the path can't break the embedded Python.
PARAMS=()
while IFS= read -r -d '' key && IFS= read -r -d '' val; do
  n=$(( ${#PARAMS[@]} / 4 + 1 ))
  PARAMS+=("--Parameters.${n}.ParameterKey" "$key" "--Parameters.${n}.ParameterValue" "$val")
done < <(python3 - "$PARAMS_FILE" <<'PY'
import json, sys
with open(sys.argv[1], encoding="utf-8") as f:
    params = json.load(f)
out = sys.stdout
for p in params:
    out.write(str(p["key"]) + "\0" + str(p["value"]) + "\0")
PY
)
[ ${#PARAMS[@]} -gt 0 ] || { echo "no parameters parsed from params-file: $PARAMS_FILE" >&2; exit 1; }

# ─── Retry safety: check if same-name stack already exists ───────────────
EXISTING_SID=""
echo "[create] Checking for existing stack: $NAME" >&2
EXISTING=$(aliyun ros ListStacks \
  --RegionId "$REGION" \
  --StackName.1 "$NAME" \
  --Status.1 CREATE_IN_PROGRESS \
  --Status.2 CREATE_COMPLETE \
  --Status.3 CREATE_FAILED \
  --Status.4 ROLLBACK_COMPLETE \
  --Status.5 ROLLBACK_FAILED \
  --PageSize 1 2>&1) || true

EXISTING_SID=$(echo "$EXISTING" | python3 -c "
import json, sys
try:
    d = json.load(sys.stdin)
    stacks = d.get('Stacks', [])
    if stacks:
        s = stacks[0]
        if s.get('Status') in ('CREATE_IN_PROGRESS', 'CREATE_COMPLETE'):
            print(s.get('StackId', ''))
except Exception:
    pass
" 2>/dev/null)

if [ -n "$EXISTING_SID" ]; then
  echo "[create] Found existing stack ${EXISTING_SID} (${NAME}), reusing" >&2
  STACK_ID="$EXISTING_SID"
else
  # Free the name held by a failed or rolled-back stack
  FAILED_SID=$(echo "$EXISTING" | python3 -c "
import json, sys
FAILED = {'CREATE_FAILED', 'ROLLBACK_COMPLETE', 'ROLLBACK_FAILED'}
try:
    d = json.load(sys.stdin)
    stacks = d.get('Stacks', [])
    if stacks and stacks[0].get('Status') in FAILED:
        print(stacks[0].get('StackId', ''))
except Exception:
    pass
" 2>/dev/null)
  if [ -n "$FAILED_SID" ]; then
    echo "[create] Deleting failed/rolled-back stack $FAILED_SID to free the name" >&2
    aliyun ros DeleteStack --RegionId "$REGION" --StackId "$FAILED_SID" >/dev/null 2>&1 || true
    sleep 5
  fi

  # Create new stack
  OUT=$(aliyun ros CreateStack \
    --RegionId "$REGION" \
    --StackName "$NAME" \
    --TemplateURL "$TPL_URL" \
    --DisableRollback false \
    --TimeoutInMinutes "$TIMEOUT" \
    --Tags.1.Key from               --Tags.1.Value qwencloud \
    --Tags.2.Key qwencloud-appName  --Tags.2.Value "$APP_NAME" \
    --Tags.3.Key qwencloud-appDesc  --Tags.3.Value "$APP_DESC" \
    "${PARAMS[@]}" 2>&1)
  CODE=$?
  if [ $CODE -ne 0 ]; then
    echo "[create] CreateStack CLI error (code=${CODE}), checking server..." >&2
    sleep 3
    FALLBACK=$(aliyun ros ListStacks \
      --RegionId "$REGION" --StackName.1 "$NAME" \
      --Status.1 CREATE_IN_PROGRESS --Status.2 CREATE_COMPLETE \
      --PageSize 1 2>&1) || true
    STACK_ID=$(echo "$FALLBACK" | python3 -c "
import json, sys
try:
    d = json.load(sys.stdin)
    stacks = d.get('Stacks', [])
    if stacks: print(stacks[0].get('StackId', ''))
except Exception: pass
" 2>/dev/null)
    if [ -n "$STACK_ID" ]; then
      echo "[create] CLI error but stack exists on server: $STACK_ID" >&2
    else
      echo "$OUT" >&2; exit $CODE
    fi
  else
    STACK_ID=$(echo "$OUT" | python3 -c "import json,sys
try: print(json.load(sys.stdin)['StackId'])
except: pass")
    [ -z "$STACK_ID" ] && { echo "Cannot parse StackId" >&2; echo "$OUT" >&2; exit 1; }
  fi
fi

# Provisional state file: even if interrupted, delete_stack.sh can clean up
python3 - "$PROJECT_ROOT" "$STACK_ID" "$NAME" "$REGION" <<'PY' || true
import datetime, json, os, sys
root, sid, name, region = sys.argv[1:5]
state = {
    "version": 1, "stack_id": sid, "stack_name": name, "region_id": region,
    "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z"),
    "tags": [{"Key": "from", "Value": "qwencloud"}, {"Key": "qwencloud-appName", "Value": os.environ.get("APP_NAME", "")}],
    "provisional": True,
}
with open(os.path.join(root, ".qwencloud-deploy"), "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)
PY

echo "$STACK_ID"
