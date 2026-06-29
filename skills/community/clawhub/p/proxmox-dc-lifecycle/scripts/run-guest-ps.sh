#!/usr/bin/env bash
# run-guest-ps.sh — run PowerShell inside a Proxmox Windows guest via QGA.
# Encodes the script as base64 (keeps it off the command line) and decodes it in-guest.
# Optionally passes secret lines over stdin (never on the command line).
#
# Usage:
#   run-guest-ps.sh <vmid> <timeout_seconds> '<powershell>'            # no secrets
#   printf '%s\n%s\n' "$USER" "$PW" | run-guest-ps.sh <vmid> <t> '<ps>' --stdin
#
# In the PowerShell, read stdin secrets with: $u=[Console]::In.ReadLine()
set -euo pipefail

vmid="${1:?vmid required}"
timeout="${2:?timeout seconds required}"
ps="${3:?powershell string required}"
use_stdin="${4:-}"

b64="$(printf '%s' "$ps" | base64 -w0)"
decoder="\$d=[System.Text.Encoding]::UTF8.GetString([Convert]::FromBase64String('$b64')); Invoke-Expression \$d"

if [[ "$use_stdin" == "--stdin" ]]; then
  sudo qm guest exec "$vmid" --timeout "$timeout" --pass-stdin 1 -- \
    powershell.exe -NoProfile -NonInteractive -Command "$decoder" 2>&1
else
  sudo qm guest exec "$vmid" --timeout "$timeout" -- \
    powershell.exe -NoProfile -NonInteractive -Command "$decoder" 2>&1
fi
