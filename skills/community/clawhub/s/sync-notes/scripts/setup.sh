#!/usr/bin/env bash
# Interactive configuration wizard for the sync-notes skill.
# Writes config/rclone.conf and config/.env (chmod 600).

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
CONFIG_DIR="$SKILL_DIR/config"
RCLONE_CONFIG_FILE="$CONFIG_DIR/rclone.conf"
ENV_FILE="$CONFIG_DIR/.env"

command -v rclone >/dev/null 2>&1 || { echo "rclone is required" >&2; exit 1; }

prompt() {
  # prompt <var> <question> [default] [silent]
  local var="$1" q="$2" def="${3:-}" silent="${4:-}"
  local ans
  if [[ "$silent" == "silent" ]]; then
    read -r -s -p "$q${def:+ [$def]}: " ans; echo
  else
    read -r -p "$q${def:+ [$def]}: " ans
  fi
  ans="${ans:-$def}"
  printf -v "$var" '%s' "$ans"
}

confirm_overwrite() {
  local path="$1"
  if [[ -f "$path" ]]; then
    local yn
    read -r -p "$path exists. Overwrite? [y/N] " yn
    [[ "$yn" =~ ^[Yy]$ ]] || { echo "aborted."; exit 1; }
  fi
}

echo "=== sync-notes setup ==="
echo "Config will be written to: $CONFIG_DIR"
echo

confirm_overwrite "$RCLONE_CONFIG_FILE"
confirm_overwrite "$ENV_FILE"

echo "--- Cloudflare R2 (S3) ---"
prompt R2_ENDPOINT     "R2 endpoint URL (https://<account>.r2.cloudflarestorage.com)"
prompt R2_ACCESS_KEY   "R2 Access Key ID"
prompt R2_SECRET       "R2 Secret Access Key" "" silent
prompt R2_BUCKET       "R2 bucket name"
prompt R2_PREFIX       "Subpath inside bucket (optional, no leading slash)" ""

echo
echo "--- rclone crypt (must match Remotely Save settings) ---"
prompt CRYPT_PASSWORD  "Crypt password" "" silent
prompt CRYPT_PASSWORD2 "Crypt salt / password2 (leave blank if not set in Remotely Save)" "" silent
prompt CRYPT_FN_ENC    "Filename encryption mode (standard|obfuscate|off)" "standard"
prompt CRYPT_FN_ENCODING "Filename encoding (base32|base64|base32768) [Remotely Save uses base64]" "base64"
prompt CRYPT_DIR_ENC   "Directory name encryption (true|false)" "true"

echo
echo "--- skill behaviour ---"
prompt RCLONE_REMOTE   "Crypt remote name to expose to scripts" "notes"
prompt BACKUP_KEEP     "Local backup snapshots to keep" "1"
prompt EXTRA_FLAGS     "Extra rclone flags" "--transfers=4 --checkers=8"

# obscure passwords (only if non-empty)
OBS_PW="$(rclone obscure "$CRYPT_PASSWORD")"
OBS_PW2=""
[[ -n "$CRYPT_PASSWORD2" ]] && OBS_PW2="$(rclone obscure "$CRYPT_PASSWORD2")"

# build remote target string
REMOTE_TARGET="r2-raw:${R2_BUCKET}"
[[ -n "$R2_PREFIX" ]] && REMOTE_TARGET="${REMOTE_TARGET}/${R2_PREFIX}"

mkdir -p "$CONFIG_DIR"
umask 077

cat > "$RCLONE_CONFIG_FILE" <<EOF
[r2-raw]
type = s3
provider = Cloudflare
access_key_id = ${R2_ACCESS_KEY}
secret_access_key = ${R2_SECRET}
endpoint = ${R2_ENDPOINT}
acl = private

[${RCLONE_REMOTE}]
type = crypt
remote = ${REMOTE_TARGET}
filename_encryption = ${CRYPT_FN_ENC}
filename_encoding = ${CRYPT_FN_ENCODING}
directory_name_encryption = ${CRYPT_DIR_ENC}
password = ${OBS_PW}
EOF
[[ -n "$OBS_PW2" ]] && echo "password2 = ${OBS_PW2}" >> "$RCLONE_CONFIG_FILE"
chmod 600 "$RCLONE_CONFIG_FILE"

cat > "$ENV_FILE" <<EOF
RCLONE_REMOTE=${RCLONE_REMOTE}
BACKUP_KEEP=${BACKUP_KEEP}
RCLONE_EXTRA_FLAGS="${EXTRA_FLAGS}"
EOF
chmod 600 "$ENV_FILE"

echo
echo "✅ wrote $RCLONE_CONFIG_FILE"
echo "✅ wrote $ENV_FILE"
echo
echo "Next:"
echo "  1. export CLOUD_NOTES_PATH=/path/to/your/local/vault"
echo "  2. $SCRIPT_DIR/sync.sh status   # sanity-check"
echo "  3. $SCRIPT_DIR/sync.sh init     # establish bisync baseline"
