#!/usr/bin/env bash
set -euo pipefail

STAMP="${1:-}"

if [[ -z "$STAMP" ]]; then
  echo "Usage: sudo bash $0 <timestamp>"
  echo "Example: sudo bash $0 20260316_164132"
  exit 1
fi

if [[ "${EUID}" -ne 0 ]]; then
  echo "Please run as root: sudo bash $0 $STAMP"
  exit 1
fi

for file in user.rules before.rules after.rules user6.rules before6.rules after6.rules; do
  src="/etc/ufw/${file}.${STAMP}"
  dst="/etc/ufw/${file}"
  if [[ ! -f "$src" ]]; then
    echo "Missing backup file: $src" >&2
    exit 1
  fi
  cp "$src" "$dst"
done

ufw reload
ufw status verbose
