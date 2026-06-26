#!/usr/bin/env bash
# delete-sandbox.sh — tear down a UKC sandbox instance and clean up local state
# Usage: delete-sandbox.sh <sandbox-name>
# Env: UKC_TOKEN, UKC_METRO (required)
set -euo pipefail

SANDBOX_NAME="${1:?sandbox name required}"
FQDN="$(cat "/tmp/${SANDBOX_NAME}/fqdn")"

# --- 1. Delete UKC instance ---
PAYLOAD=$(jq -n --arg name "${SANDBOX_NAME}" '[{name: $name}]')

curl --silent --fail -X DELETE \
  -H "Authorization: Bearer ${UKC_TOKEN}" \
  -H "Content-Type: application/json" \
  "${UKC_METRO}/instances" \
  -d "${PAYLOAD}"

# --- 2. Remove tmp dir (keys + state) ---
rm -rf "/tmp/${SANDBOX_NAME}"
