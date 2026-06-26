#!/usr/bin/env bash
# create-sandbox.sh — provision a UKC sandbox instance
# Usage: create-sandbox.sh <sandbox-name>
# Outputs: FQDN of the created instance to stdout
# Env: UKC_TOKEN, UKC_METRO, UKC_USER, UKC_SANDBOX_IMAGE (all required)
set -euo pipefail

SANDBOX_NAME="${1:?sandbox name required}"
TMP_DIR="/tmp/${SANDBOX_NAME}"

# --- 1. Check sandbox doesn't already exist ---
EXISTING=$(curl \
  --silent \
  -H "Authorization: Bearer ${UKC_TOKEN}" \
  "${UKC_METRO}/instances" | jq -r ".data.instances[] | select(.name==\"${SANDBOX_NAME}\") | .name")

if [ -n "${EXISTING}" ]; then
  echo "Sandbox '${SANDBOX_NAME}' already exists." >&2
  exit 1
fi

# --- 2. Create tmp dir and SSH keypair ---
mkdir -p "${TMP_DIR}"
ssh-keygen -t ed25519 -N "" -f "${TMP_DIR}/id_ed25519" -C "${SANDBOX_NAME}" -q
chmod 600 "${TMP_DIR}/id_ed25519"
PUBKEY="$(cat "${TMP_DIR}/id_ed25519.pub")"

# --- 3. Create UKC instance ---
PAYLOAD=$(jq -n \
  --arg image "${UKC_SANDBOX_IMAGE}" \
  --arg name "${SANDBOX_NAME}" \
  --arg pubkey "${PUBKEY}" \
  '{
    image: $image,
    name: $name,
    memory_mb: 4096,
    env: { PUBKEY: $pubkey },
    service_group: {
      services: [
        { port: 2222, destination_port: 2222, handlers: ["tls"] },
        { port: 443, destination_port: 8080, handlers: ["tls", "http"] }
      ]
    },
    scale_to_zero: { policy: "on", stateful: true, cooldown_time_ms: 5000 },
    autostart: true
  }')

RESPONSE=$(curl \
  --silent \
  -X POST \
  -H "Authorization: Bearer ${UKC_TOKEN}" \
  -H "Content-Type: application/json" \
  "${UKC_METRO}/instances" \
  -d "${PAYLOAD}")

# --- 4. Extract FQDN, surface any API errors ---
STATUS=$(echo "${RESPONSE}" | jq -r '.status')
if [ "${STATUS}" != "success" ]; then
  ERROR=$(echo "${RESPONSE}" | jq -r '.data.instances[0].message // .message // "unknown error"')
  echo "Failed to create sandbox '${SANDBOX_NAME}': ${ERROR}" >&2
  exit 1
fi

FQDN=$(echo "${RESPONSE}" | jq -r '.data.instances[0].service_group.domains[0].fqdn')

echo "${FQDN}" > "${TMP_DIR}/fqdn"
echo "${FQDN}"
