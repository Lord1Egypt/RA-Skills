#!/usr/bin/env bash
set -euo pipefail

LABEL="${1:?Usage: update-checkpoint.sh <label> [ops...]}"
shift
FILE="/tmp/self-heal-council-${LABEL}.json"
[ -f "$FILE" ] || { echo "Missing checkpoint: $FILE" >&2; exit 1; }

while [[ $# -gt 0 ]]; do
  case "$1" in
    --round)
      ROUND="$2"; shift 2
      python3 - "$FILE" "$ROUND" <<'PY'
import json,sys,datetime
p=sys.argv[1]; r=int(sys.argv[2])
obj=json.load(open(p))
obj['round']=r
obj['timestamp']=datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
json.dump(obj, open(p+'.tmp','w'), indent=2)
PY
      mv "$FILE.tmp" "$FILE"
      ;;
    --complete)
      ITEM="$2"; shift 2
      python3 - "$FILE" "$ITEM" <<'PY'
import json,sys,datetime
p=sys.argv[1]; item=sys.argv[2]
obj=json.load(open(p))
if item not in obj['completed']:
    obj['completed'].append(item)
obj['timestamp']=datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
json.dump(obj, open(p+'.tmp','w'), indent=2)
PY
      mv "$FILE.tmp" "$FILE"
      ;;
    --model)
      ITEM="$2"; shift 2
      python3 - "$FILE" "$ITEM" <<'PY'
import json,sys,datetime
p=sys.argv[1]; item=sys.argv[2]
obj=json.load(open(p))
obj.setdefault('models_tried',[]).append(item)
obj['timestamp']=datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
json.dump(obj, open(p+'.tmp','w'), indent=2)
PY
      mv "$FILE.tmp" "$FILE"
      ;;
    --persona)
      ITEM="$2"; shift 2
      python3 - "$FILE" "$ITEM" <<'PY'
import json,sys,datetime
p=sys.argv[1]; item=sys.argv[2]
obj=json.load(open(p))
if item not in obj['personas']:
    obj['personas'].append(item)
obj['timestamp']=datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
json.dump(obj, open(p+'.tmp','w'), indent=2)
PY
      mv "$FILE.tmp" "$FILE"
      ;;
    --error)
      ITEM="$2"; shift 2
      python3 - "$FILE" "$ITEM" <<'PY'
import json,sys,datetime
p=sys.argv[1]; item=sys.argv[2]
obj=json.load(open(p))
obj['last_error']=item
obj['timestamp']=datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
json.dump(obj, open(p+'.tmp','w'), indent=2)
PY
      mv "$FILE.tmp" "$FILE"
      ;;
    *)
      echo "Unknown arg: $1" >&2; exit 1
      ;;
  esac
done

cat "$FILE"
