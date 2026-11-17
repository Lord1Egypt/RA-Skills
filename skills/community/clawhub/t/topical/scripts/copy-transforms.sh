#!/usr/bin/env bash
# Copy Topical hook transform assets into OpenClaw's hooks transforms directory.
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="${OPENCLAW_HOOKS_TRANSFORMS:-${HOME}/.openclaw/hooks/transforms}"

mkdir -p "${DEST}"
cp "${SKILL_DIR}/assets/topical-inbound.mjs" "${DEST}/"

if [[ ! -f "${DEST}/topical.config.json" ]]; then
  cp "${SKILL_DIR}/assets/topical.config.example.json" "${DEST}/topical.config.json"
  echo "Created ${DEST}/topical.config.json from example — edit agentId and delivery channel."
else
  echo "Kept existing ${DEST}/topical.config.json"
fi

echo "Installed topical-inbound.mjs → ${DEST}/"
