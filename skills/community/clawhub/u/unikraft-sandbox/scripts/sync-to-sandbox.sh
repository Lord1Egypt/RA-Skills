#!/usr/bin/env bash
# sync-to-sandbox.sh — push a local directory to /workspace on the sandbox
# Usage: sync-to-sandbox.sh <sandbox-name> <local-dir>
set -euo pipefail

SANDBOX_NAME="${1:?sandbox name required}"
LOCAL_DIR="${2:?local dir required}"
FQDN="$(cat "/tmp/${SANDBOX_NAME}/fqdn")"
KEY="/tmp/${SANDBOX_NAME}/id_ed25519"

rsync -az --delete \
  -e "ssh -i ${KEY} -o StrictHostKeyChecking=no -o ConnectTimeout=10 -o ProxyCommand='openssl s_client -quiet -connect ${FQDN}:2222 2>/dev/null'" \
  "${LOCAL_DIR%/}/" \
  "root@${FQDN}:/workspace/"
