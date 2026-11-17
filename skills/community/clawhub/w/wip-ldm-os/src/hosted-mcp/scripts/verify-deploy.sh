#!/usr/bin/env bash
# verify-deploy.sh: Verify a hosted-mcp deploy manifest against the live
# VPS. Reads a manifest produced by deploy.sh, fetches the current
# sha256 of each declared destination on the remote, and compares.
#
# Per F-009 of the VPS hosted-mcp audit. Use after deploy.sh, after
# any apparent change to the live tree, or as part of the pre-dogfood
# smoke test.
#
# Usage:
#   bash verify-deploy.sh wip.computer:/var/www/.../<timestamp>.json
#   bash verify-deploy.sh /path/to/local/manifest.json --remote wip.computer
#   bash verify-deploy.sh latest                # use latest manifest on VPS
#
# Exits non-zero on any mismatch. Output lists each file as OK or DIFF.

set -euo pipefail

REMOTE="wip.computer"
MANIFEST_DIR="/var/www/wip.computer/deploy-manifests/hosted-mcp"
ARG=""

while [ $# -gt 0 ]; do
  case "$1" in
    --remote) REMOTE=$2; shift 2 ;;
    -h|--help) sed -n '2,18p' "$0"; exit 0 ;;
    *) ARG=$1; shift ;;
  esac
done

if [ -z "$ARG" ]; then
  echo "usage: bash verify-deploy.sh <manifest-path-or-latest>" >&2
  exit 2
fi

# Resolve manifest path.
if [ "$ARG" = "latest" ]; then
  MANIFEST_PATH=$(ssh "${REMOTE}" "ls -t ${MANIFEST_DIR}/*.json 2>/dev/null | head -1")
  if [ -z "$MANIFEST_PATH" ]; then
    echo "FATAL: no manifests found in ${REMOTE}:${MANIFEST_DIR}" >&2
    exit 1
  fi
  echo "Latest manifest: ${MANIFEST_PATH}"
  MANIFEST_JSON=$(ssh "${REMOTE}" "cat ${MANIFEST_PATH}")
elif [[ "$ARG" == *":"* ]]; then
  # remote:path form
  MANIFEST_REMOTE=${ARG%%:*}
  MANIFEST_PATH=${ARG#*:}
  MANIFEST_JSON=$(ssh "${MANIFEST_REMOTE}" "cat ${MANIFEST_PATH}")
elif [ -f "$ARG" ]; then
  MANIFEST_PATH=$ARG
  MANIFEST_JSON=$(cat "$ARG")
else
  echo "FATAL: manifest not found: ${ARG}" >&2
  exit 1
fi

# Parse files[] entries via python3.
if ! command -v python3 >/dev/null 2>&1; then
  echo "FATAL: python3 required" >&2
  exit 1
fi

ENTRIES=$(printf '%s' "$MANIFEST_JSON" | python3 -c '
import json,sys
m=json.load(sys.stdin)
for f in m.get("files",[]):
    print(f.get("source","")+"\t"+f.get("destination","")+"\t"+f.get("sha256",""))
')

if [ -z "$ENTRIES" ]; then
  echo "FATAL: no files entries in manifest" >&2
  exit 1
fi

echo "Manifest: ${MANIFEST_PATH}"
echo "Verifying ${REMOTE}:"
echo

OK=0
FAIL=0
while IFS=$'\t' read -r src dst expected; do
  [ -z "$dst" ] && continue
  # ssh -n redirects stdin from /dev/null so ssh does not consume the
  # loop's heredoc and short-circuit after the first iteration.
  remote_sha=$(ssh -n "${REMOTE}" "sudo sha256sum ${dst} 2>/dev/null" | awk '{print $1}' || echo "")
  if [ -z "$remote_sha" ]; then
    printf "  MISSING  %s\n" "$dst"
    FAIL=$((FAIL+1))
  elif [ "$remote_sha" = "$expected" ]; then
    printf "  OK       %s\n" "$dst"
    OK=$((OK+1))
  else
    printf "  DIFF     %s\n           expected %s\n           live     %s\n" "$dst" "$expected" "$remote_sha"
    FAIL=$((FAIL+1))
  fi
done <<< "$ENTRIES"

echo
echo "Summary: ${OK} ok, ${FAIL} mismatched"
[ "$FAIL" -eq 0 ] && exit 0
exit 1
