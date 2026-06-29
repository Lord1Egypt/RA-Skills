#!/usr/bin/env bash
set -euo pipefail

BRIDGE_URL="${WEB_COLLECTION_BRIDGE_URL:-http://127.0.0.1:19820}"
CLOUD_BASE_URL="${WEB_COLLECTION_CLOUD_BASE_URL:-https://i-sync.cn}"
CLOUD_DEVICE_ID="${WEB_COLLECTION_CLOUD_DEVICE_ID:-}"
CLOUD_TOKEN="${WEB_COLLECTION_CLOUD_TOKEN:-}"
FORMAT="shell"

usage() {
  cat <<'EOF'
Usage:
  ensure_connector_auth.sh [options]

Options:
  --bridge-url <url>       Local connector bridge URL, default: http://127.0.0.1:19820
  --cloud-base-url <url>   Cloud API base URL, default: https://i-sync.cn
  --device-id <id>         Existing connector device_id
  --token <token>          Existing connector_token / cloud bearer token
  --format <shell|json>    Output format, default: shell
  -h, --help

The script prints shell assignments when credentials are available.
When login is required, it prints WEB_COLLECTION_AUTH_REQUIRED=1 and
WEB_COLLECTION_LOGIN_URL=<url>, then exits with code 2.
EOF
}

die() {
  printf '[web-collection] error: %s\n' "$*" >&2
  exit 1
}

normalize_url() {
  printf '%s' "${1:-}" | sed 's#/*$##'
}

json_string() {
  node -e '
const value = process.argv[1] ?? "";
process.stdout.write(JSON.stringify(value));
' "$1"
}

print_shell_credentials() {
  local device_id="$1"
  local token="$2"
  local source="$3"
  printf 'WEB_COLLECTION_AUTH_REQUIRED=0\n'
  printf 'WEB_COLLECTION_CLOUD_BASE_URL=%s\n' "$(printf '%q' "$CLOUD_BASE_URL")"
  printf 'WEB_COLLECTION_CLOUD_DEVICE_ID=%s\n' "$(printf '%q' "$device_id")"
  printf 'WEB_COLLECTION_CLOUD_TOKEN=%s\n' "$(printf '%q' "$token")"
  printf 'WEB_COLLECTION_AUTH_SOURCE=%s\n' "$(printf '%q' "$source")"
}

print_json_credentials() {
  local device_id="$1"
  local token="$2"
  local source="$3"
  node -e '
const [baseUrl, deviceId, token, source] = process.argv.slice(1);
process.stdout.write(JSON.stringify({
  authRequired: false,
  cloudBaseUrl: baseUrl,
  deviceId,
  tokenPresent: Boolean(token),
  token,
  source
}, null, 2) + "\n");
' "$CLOUD_BASE_URL" "$device_id" "$token" "$source"
}

emit_credentials() {
  local device_id="$1"
  local token="$2"
  local source="$3"
  [[ -n "$device_id" && -n "$token" ]] || return 1
  if [[ "$FORMAT" == "json" ]]; then
    print_json_credentials "$device_id" "$token" "$source"
  else
    print_shell_credentials "$device_id" "$token" "$source"
  fi
}

print_shell_login_required() {
  local login_url="$1"
  local reason="$2"
  printf 'WEB_COLLECTION_AUTH_REQUIRED=1\n'
  printf 'WEB_COLLECTION_LOGIN_URL=%s\n' "$(printf '%q' "$login_url")"
  printf 'WEB_COLLECTION_AUTH_REASON=%s\n' "$(printf '%q' "$reason")"
}

print_json_login_required() {
  local login_url="$1"
  local reason="$2"
  node -e '
const [loginUrl, reason] = process.argv.slice(1);
process.stdout.write(JSON.stringify({
  authRequired: true,
  loginUrl,
  reason
}, null, 2) + "\n");
' "$login_url" "$reason"
}

emit_login_required() {
  local login_url="$1"
  local reason="$2"
  if [[ "$FORMAT" == "json" ]]; then
    print_json_login_required "$login_url" "$reason"
  else
    print_shell_login_required "$login_url" "$reason"
  fi
  exit 2
}

read_connector_admin_token() {
  local token_file="${HOME}/.meixi-connector/bridge-admin-token.txt"
  if [[ -f "$token_file" ]]; then
    tr -d '\r\n' <"$token_file"
  fi
}

bridge_get() {
  local path="$1"
  local token="${2:-}"
  if [[ -n "$token" ]]; then
    curl -fsS --max-time 3 -H "x-connector-admin-token: $token" "${BRIDGE_URL}${path}"
  else
    curl -fsS --max-time 3 "${BRIDGE_URL}${path}"
  fi
}

read_app_state_credentials() {
  node -e '
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");

const appHome = process.env.RPA_APP_HOME
  || (process.platform === "darwin"
    ? path.join(os.homedir(), "Library", "Application Support", "rpa-app-executor")
    : process.platform === "win32"
      ? path.join(process.env.APPDATA || path.join(os.homedir(), "AppData", "Roaming"), "rpa-app-executor")
      : path.join(process.env.XDG_DATA_HOME || path.join(os.homedir(), ".local", "share"), "rpa-app-executor"));

const readJson = (filePath) => {
  try { return JSON.parse(fs.readFileSync(filePath, "utf8")); } catch { return null; }
};
const readText = (filePath) => {
  try { return fs.readFileSync(filePath, "utf8").trim(); } catch { return ""; }
};

const stateDir = path.join(appHome, "cloud", "state");
const auth = readJson(path.join(stateDir, "cloud-auth.json")) || {};
const config = readJson(path.join(stateDir, "cloud-config.json")) || {};
const deviceId = readText(path.join(stateDir, "device-id.txt")) || config.connectorId || "";
const token = typeof auth.token === "string" ? auth.token.trim() : "";
process.stdout.write(JSON.stringify({
  appHome,
  deviceId,
  token,
  wsUrl: typeof config.wsUrl === "string" ? config.wsUrl.trim() : "",
}));
'
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --bridge-url)
      BRIDGE_URL="$(normalize_url "${2:-}")"
      shift 2
      ;;
    --cloud-base-url)
      CLOUD_BASE_URL="$(normalize_url "${2:-}")"
      shift 2
      ;;
    --device-id)
      CLOUD_DEVICE_ID="${2:-}"
      shift 2
      ;;
    --token)
      CLOUD_TOKEN="${2:-}"
      shift 2
      ;;
    --format)
      FORMAT="${2:-shell}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      die "unknown arg: $1"
      ;;
  esac
done

[[ "$FORMAT" == "shell" || "$FORMAT" == "json" ]] || die "invalid --format: $FORMAT"
BRIDGE_URL="$(normalize_url "$BRIDGE_URL")"
CLOUD_BASE_URL="$(normalize_url "$CLOUD_BASE_URL")"

if emit_credentials "$CLOUD_DEVICE_ID" "$CLOUD_TOKEN" "explicit"; then
  exit 0
fi

app_state_json="$(read_app_state_credentials || printf '{}')"
app_device_id="$(node -e 'const data=JSON.parse(process.argv[1]||"{}"); process.stdout.write(data.deviceId || "");' "$app_state_json")"
app_token="$(node -e 'const data=JSON.parse(process.argv[1]||"{}"); process.stdout.write(data.token || "");' "$app_state_json")"
if emit_credentials "${CLOUD_DEVICE_ID:-$app_device_id}" "${CLOUD_TOKEN:-$app_token}" "app-state"; then
  exit 0
fi

admin_token="$(read_connector_admin_token || true)"

status_json=""
if status_json="$(bridge_get "/api/cloud/status" "$admin_token" 2>/dev/null)"; then
  bridge_device_id="$(node -e '
const data = JSON.parse(process.argv[1] || "{}");
const cloud = data.cloud || data.data?.cloud || data;
const config = data.config || data.data?.config || {};
process.stdout.write(cloud.connectorId || cloud.deviceId || config.connectorId || "");
' "$status_json")"
  bridge_token="$(node -e '
const data = JSON.parse(process.argv[1] || "{}");
const config = data.config || data.data?.config || {};
process.stdout.write(typeof config.token === "string" ? config.token : "");
' "$status_json")"
  if emit_credentials "${CLOUD_DEVICE_ID:-$bridge_device_id}" "${CLOUD_TOKEN:-$bridge_token}" "connector-status"; then
    exit 0
  fi
fi

login_json=""
if login_json="$(bridge_get "/api/auth/login-url" "$admin_token" 2>/dev/null)"; then
  login_url="$(node -e 'const data=JSON.parse(process.argv[1]||"{}"); process.stdout.write(data.loginUrl || data.data?.loginUrl || "");' "$login_json")"
  if [[ -n "$login_url" ]]; then
    emit_login_required "$login_url" "connector authorization required"
  fi
fi

die "connector authorization is required, but no login URL could be generated. Start the connector/App runtime, then retry."
