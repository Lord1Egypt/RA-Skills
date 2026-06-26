#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

"$BASE_DIR/site-session-registry.sh" write \
  --root "$TMP_DIR/root" \
  --site github.com \
  --session-key default \
  --profile-dir "$TMP_DIR/profiles/github-default" \
  --source-origin "https://github.com" >/dev/null

"$BASE_DIR/site-session-registry.sh" resolve \
  --root "$TMP_DIR/root" \
  --site github.com \
  --session-key default | grep -q '"profile_dir": "'"$TMP_DIR"'/profiles/github-default"'

"$BASE_DIR/site-session-registry.sh" show \
  --root "$TMP_DIR/root" \
  --site github.com | grep -q '"default_session": "default"'

printf '{broken json\n' >"$TMP_DIR/root/index/site-sessions.json"
"$BASE_DIR/site-session-registry.sh" write \
  --root "$TMP_DIR/root" \
  --site google.com \
  --session-key default \
  --profile-dir "$TMP_DIR/profiles/google-default" \
  --source-origin "https://myaccount.google.com/" >/dev/null

"$BASE_DIR/site-session-registry.sh" resolve \
  --root "$TMP_DIR/root" \
  --site google.com \
  --session-key default | grep -q '"source_origin": "https://myaccount.google.com/"'
