#!/usr/bin/env bash
set -euo pipefail

ROOT="/home/zqh2333/.openclaw/workspace"
cd "$ROOT"

node skills/shared-memory-os/scripts/init-shared-memory-os.js
bash skills/shared-memory-os/scripts/ensure-shared-memory-crons.sh
node skills/shared-memory-os/scripts/run-shared-memory-maintenance.js
