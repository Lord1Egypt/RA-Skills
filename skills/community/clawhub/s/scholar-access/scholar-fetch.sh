#!/usr/bin/env bash
#
# scholar-fetch.sh — Fetch a URL through the Scholar reverse-proxy when the
# target site (github.com / huggingface.co / ...) is unreachable directly.
#
# It resolves the URL's hostname via the Scholar DoH endpoint and, if that
# hostname maps to a 205.164.50.x proxy IP, rewrites the connection with
# `curl --resolve` and trusts the bundled Scholar Root CA.
#
# Usage:
#   scholar-fetch.sh <url> [extra curl args...]
#   scholar-fetch.sh https://github.com/torvalds/linux/archive/refs/heads/master.tar.gz -o linux.tar.gz
#
# Env:
#   SCHOLAR_CA   path to the Scholar Root CA PEM (default: bundled scholar-root-ca.pem)
#   SCHOLAR_PORT TLS port to use (default 443)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CA="${SCHOLAR_CA:-$SCRIPT_DIR/scholar-root-ca.pem}"
PORT="${SCHOLAR_PORT:-443}"

if [ "$#" -lt 1 ]; then
  sed -n '2,20p' "$0" | sed 's/^# \{0,1\}//'
  exit 1
fi

URL="$1"
shift

# Extract hostname from the URL (works for http/https).
HOST="$(printf '%s' "$URL" | sed -E 's#^[a-zA-Z][a-zA-Z0-9+.-]*://##; s#[/:].*$##')"

if [ -z "$HOST" ]; then
  echo "ERROR: cannot parse hostname from URL: $URL" >&2
  exit 2
fi

# Resolve via the Scholar DoH endpoint.
RESOLVER="$(command -v python3 || command -v python)"
IP="$("$RESOLVER" "$SCRIPT_DIR/scholar-resolve.py" "$HOST" 2>/dev/null | head -n1 || true)"

if [ -n "$IP" ] && [[ "$IP" == 205.164.50.* ]]; then
  echo "[scholar] $HOST -> proxy $IP" >&2
  exec curl --resolve "${HOST}:${PORT}:${IP}" --cacert "$CA" "$@" "$URL"
else
  echo "[scholar] $HOST not proxied (direct fetch)" >&2
  exec curl "$@" "$URL"
fi
