#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

mkdir -p "$TMP_DIR/home/.agent-browser/profiles/x.com/Default"
touch "$TMP_DIR/home/.agent-browser/profiles/x.com/Default/Cookies"

"$BASE_DIR/site-session-registry.sh" write \
  --root "$TMP_DIR/home/.agent-browser" \
  --site "github.com" \
  --session-key default \
  --profile-dir "$TMP_DIR/home/.agent-browser/profiles/sites/github/default" \
  --source-origin "https://github.com" >/dev/null

registry_status="$(
  HOME="$TMP_DIR/home" \
  "$BASE_DIR/browser-runtime.sh" status \
    --origin "https://github.com" \
    --session-key default
)"
printf '%s\n' "$registry_status" | grep -q "profile_dir: $TMP_DIR/home/.agent-browser/profiles/sites/github/default"

"$BASE_DIR/session-manifest.sh" write \
  --root "$TMP_DIR/manifests" \
  --origin "https://x.com" \
  --session-key default \
  --state ready \
  --browser-pid 123 \
  --profile-dir "$TMP_DIR/home/.agent-browser/profiles/x.com" >/dev/null

status_output="$(
  HOME="$TMP_DIR/home" \
  "$BASE_DIR/browser-runtime.sh" status \
    --manifest-root "$TMP_DIR/manifests" \
    --origin "https://x.com" \
    --session-key default
)"
printf '%s\n' "$status_output" | grep -q "profile_dir: $TMP_DIR/home/.agent-browser/profiles/x.com"

legacy_status="$(
  HOME="$TMP_DIR/home" \
  "$BASE_DIR/browser-runtime.sh" status \
    --origin "https://x.com" \
    --session-key default
)"
printf '%s\n' "$legacy_status" | grep -q "profile_dir: $TMP_DIR/home/.agent-browser/profiles/x.com"

mkdir -p "$TMP_DIR/home/.agent-browser/profiles/https___x_com/default/Default"
touch "$TMP_DIR/home/.agent-browser/profiles/https___x_com/default/Default/Login Data"
touch "$TMP_DIR/home/.agent-browser/profiles/https___x_com/default/Local State"
populated_status="$(
  HOME="$TMP_DIR/home" \
  "$BASE_DIR/browser-runtime.sh" status \
    --origin "https://x.com" \
    --session-key default
)"
printf '%s\n' "$populated_status" | grep -q "profile_dir: $TMP_DIR/home/.agent-browser/profiles/https___x_com/default"

runtime_key="$(
  HOME="$TMP_DIR/home" \
  "$BASE_DIR/browser-runtime.sh" status \
    --origin "HTTPS://X.COM" \
    --session-key default | sed -n 's#.*run_dir: .*/run/\([^/]*\)/.*#\1#p'
)"
manifest_key="$(
  "$BASE_DIR/session-manifest.sh" path \
    --root "$TMP_DIR/manifests" \
    --origin "HTTPS://X.COM" | sed -n 's#.*/sessions/\([^/]*\)$#\1#p'
)"
[ "$runtime_key" = "$manifest_key" ]

mkdir -p "$TMP_DIR/home/.agent-browser/index"
printf '{invalid json\n' >"$TMP_DIR/home/.agent-browser/index/identity-profiles.json"
write_output="$(
  HOME="$TMP_DIR/home" \
  "$BASE_DIR/profile-resolution.sh" write-identity \
    --root "$TMP_DIR/home/.agent-browser" \
    --provider "github.com" \
    --profile-dir "$TMP_DIR/home/.agent-browser/profiles/x.com" \
    --source-origin "https://x.com" \
    --source-session-key default
)"
[ -z "$write_output" ]
grep -q '"github.com"' "$TMP_DIR/home/.agent-browser/index/identity-profiles.json"
