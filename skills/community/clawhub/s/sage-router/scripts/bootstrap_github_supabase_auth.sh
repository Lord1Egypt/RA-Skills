#!/usr/bin/env bash
set -euo pipefail

load_local_env_file() {
  local path="$1"
  [[ -f "$path" ]] || return 0

  local key value current
  while IFS='=' read -r -d '' key value; do
    case "$key" in
      SUPABASE_ACCESS_TOKEN|SAGEROUTER_GITHUB_CLIENT_ID|SAGEROUTER_GITHUB_CLIENT_SECRET|GITHUB_CLIENT_ID|GITHUB_CLIENT_SECRET)
        ;;
      *)
        continue
        ;;
    esac
    current="${!key:-}"
    if [[ -z "$current" && -n "$value" ]]; then
      printf -v "$key" '%s' "$value"
      export "$key"
    fi
  done < <(set +u; set -a; source "$path" >/dev/null 2>&1; env -0)
}

DEFAULT_GITHUB_CREDENTIALS_OUTPUT="/home/digit/.openclaw/sage-router-github-auth.env"
load_local_env_file "${SAGEROUTER_SECRET_ENV_FILE:-/home/digit/.openclaw/.env}"
load_local_env_file "${SAGEROUTER_GITHUB_APP_ENV_OUTPUT:-${DEFAULT_GITHUB_CREDENTIALS_OUTPUT}}"

PROJECT_REF="${SUPABASE_PROJECT_REF:-awtangrlqqsdpksarhwo}"
AUTH_SITE_URL="${SAGEROUTER_AUTH_SITE_URL:-https://app.sagerouter.dev}"
APP_NAME="${SAGEROUTER_GITHUB_APP_NAME:-Sage Router Auth}"
APP_OWNER="${SAGEROUTER_GITHUB_APP_OWNER:-}"
LOCAL_CAPTURE="${SAGEROUTER_GITHUB_APP_LOCAL_CAPTURE:-1}"
LOCAL_CAPTURE_PORT="${SAGEROUTER_GITHUB_APP_LOCAL_CAPTURE_PORT:-0}"
LOCAL_CAPTURE_BIND="${SAGEROUTER_GITHUB_APP_LOCAL_CAPTURE_BIND:-127.0.0.1}"
LOCAL_CAPTURE_HOST="${SAGEROUTER_GITHUB_APP_LOCAL_CAPTURE_HOST:-127.0.0.1}"
MANIFEST_INPUT="${1:-${SAGEROUTER_GITHUB_APP_MANIFEST_URL:-${SAGEROUTER_GITHUB_APP_MANIFEST_CODE:-${GITHUB_APP_MANIFEST_CODE:-}}}}"
MANIFEST_CODE=""
GITHUB_CLIENT_ID="${SAGEROUTER_GITHUB_CLIENT_ID:-${GITHUB_CLIENT_ID:-}}"
GITHUB_CLIENT_SECRET="${SAGEROUTER_GITHUB_CLIENT_SECRET:-${GITHUB_CLIENT_SECRET:-}}"
GITHUB_CREDENTIALS_OUTPUT="${SAGEROUTER_GITHUB_APP_ENV_OUTPUT:-${DEFAULT_GITHUB_CREDENTIALS_OUTPUT}}"
SUPABASE_ACCESS_TOKEN="${SUPABASE_ACCESS_TOKEN:?Set SUPABASE_ACCESS_TOKEN to a Supabase Management API token.}"
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WINDOWS_FORM_PATH=""
WINDOWS_FORM_URI=""

callback_url="https://${PROJECT_REF}.supabase.co/auth/v1/callback"

die() {
  printf '%s\n' "$*" >&2
  exit 1
}

parse_manifest_code() {
  MANIFEST_INPUT="$MANIFEST_INPUT" python3 - <<'PY'
import os
import sys
import urllib.parse

value = os.environ.get("MANIFEST_INPUT", "").strip()
if not value:
    sys.exit(0)

parsed = urllib.parse.urlparse(value)
if parsed.scheme and parsed.netloc:
    code = urllib.parse.parse_qs(parsed.query).get("code", [""])[0].strip()
    if not code:
        print("Manifest callback URL did not include a code parameter.", file=sys.stderr)
        sys.exit(2)
    print(code)
    sys.exit(0)

print(value)
PY
}

configure_supabase() {
  SAGEROUTER_AUTH_SITE_URL="$AUTH_SITE_URL" \
  SUPABASE_PROJECT_REF="$PROJECT_REF" \
  SUPABASE_ACCESS_TOKEN="$SUPABASE_ACCESS_TOKEN" \
  SAGEROUTER_GITHUB_CLIENT_ID="$GITHUB_CLIENT_ID" \
  SAGEROUTER_GITHUB_CLIENT_SECRET="$GITHUB_CLIENT_SECRET" \
    bash "${script_dir}/configure_supabase_github_auth.sh"
}

save_github_credentials() {
  [[ -n "$GITHUB_CREDENTIALS_OUTPUT" ]] || return 0
  umask 077
  mkdir -p "$(dirname "$GITHUB_CREDENTIALS_OUTPUT")"
  {
    printf 'SAGEROUTER_GITHUB_CLIENT_ID=%q\n' "$GITHUB_CLIENT_ID"
    printf 'SAGEROUTER_GITHUB_CLIENT_SECRET=%q\n' "$GITHUB_CLIENT_SECRET"
  } > "$GITHUB_CREDENTIALS_OUTPUT"
  printf 'Saved GitHub OAuth credentials to %s.\n' "$GITHUB_CREDENTIALS_OUTPUT" >&2
}

convert_manifest() {
  response="$(
    curl -fsS -X POST "https://api.github.com/app-manifests/${MANIFEST_CODE}/conversions" \
      -H "Accept: application/vnd.github+json" \
      -H "X-GitHub-Api-Version: 2026-03-10"
  )"
  GITHUB_CLIENT_ID="$(printf '%s' "$response" | jq -r '.client_id // empty')"
  GITHUB_CLIENT_SECRET="$(printf '%s' "$response" | jq -r '.client_secret // empty')"
  [[ -n "$GITHUB_CLIENT_ID" && -n "$GITHUB_CLIENT_SECRET" ]] || die "GitHub manifest conversion did not return a client id and secret."
  save_github_credentials
  configure_supabase
  printf 'Configured Supabase GitHub auth for app id %s.\n' "$(printf '%s' "$response" | jq -r '.id // "unknown"')"
}

prepare_windows_form() {
  [[ -z "$WINDOWS_FORM_URI" ]] || return 0
  command -v powershell.exe >/dev/null 2>&1 || return 0
  command -v wslpath >/dev/null 2>&1 || return 0

  win_temp="$(
    powershell.exe -NoProfile -Command '[Console]::Out.Write($env:TEMP)' 2>/dev/null | tr -d '\r'
  )"
  [[ -n "$win_temp" ]] || return 0
  win_temp_wsl="$(wslpath -u "$win_temp" 2>/dev/null || true)"
  [[ -n "$win_temp_wsl" ]] || return 0
  mkdir -p "$win_temp_wsl" >/dev/null 2>&1 || return 0
  cp "$form" "$win_temp_wsl/sage-router-github-auth-app.html" >/dev/null 2>&1 || return 0
  WINDOWS_FORM_PATH="$(
    powershell.exe -NoProfile -Command '$p = Join-Path $env:TEMP "sage-router-github-auth-app.html"; [Console]::Out.Write($p)' 2>/dev/null | tr -d '\r'
  )"
  WINDOWS_FORM_URI="$(
    powershell.exe -NoProfile -Command '$p = Join-Path $env:TEMP "sage-router-github-auth-app.html"; [Console]::Out.Write(([Uri]$p).AbsoluteUri)' 2>/dev/null | tr -d '\r'
  )"
}

form_location_text() {
  if [[ -n "$WINDOWS_FORM_PATH" ]]; then
    cat <<EOF
   Windows path: ${WINDOWS_FORM_PATH}
   WSL path:     ${form}
EOF
  else
    printf '   %s\n' "$form"
  fi
}

open_form() {
  prepare_windows_form
  if command -v powershell.exe >/dev/null 2>&1; then
    if [[ -n "$WINDOWS_FORM_URI" ]]; then
      powershell.exe -NoProfile -Command "Start-Process '$WINDOWS_FORM_URI'" >/dev/null 2>&1 && return
    elif command -v wslpath >/dev/null 2>&1; then
      windows_form="$(wslpath -w "$form")"
      powershell.exe -NoProfile -Command "Start-Process '$windows_form'" >/dev/null 2>&1 && return
    fi
    powershell.exe -NoProfile -Command "Start-Process '$form'" >/dev/null 2>&1 || true
  elif command -v xdg-open >/dev/null 2>&1; then
    xdg-open "$form" >/dev/null 2>&1 || true
  fi
}

if [[ -n "$GITHUB_CLIENT_ID" && -n "$GITHUB_CLIENT_SECRET" ]]; then
  configure_supabase
  exit 0
fi

if [[ -n "$MANIFEST_INPUT" ]]; then
  MANIFEST_CODE="$(parse_manifest_code)" || die "Could not parse GitHub manifest code from input."
fi

if [[ -n "$MANIFEST_CODE" ]]; then
  convert_manifest
  exit 0
fi

state="$(python3 - <<'PY'
import secrets
print(secrets.token_urlsafe(24))
PY
)"
hosted_manifest_path="/github-app-manifest"
redirect_url="${AUTH_SITE_URL%/}${hosted_manifest_path}"
if [[ "$LOCAL_CAPTURE" != "0" && "$LOCAL_CAPTURE" != "false" && "$LOCAL_CAPTURE" != "no" ]]; then
  if [[ "$LOCAL_CAPTURE_PORT" == "0" || "$LOCAL_CAPTURE_PORT" == "auto" ]]; then
    LOCAL_CAPTURE_PORT="$(
      python3 - <<'PY'
import socket

with socket.socket() as sock:
    sock.bind(("127.0.0.1", 0))
    print(sock.getsockname()[1])
PY
    )"
  fi
  redirect_url="http://${LOCAL_CAPTURE_HOST}:${LOCAL_CAPTURE_PORT}/github-app-manifest.html"
fi

manifest="$(
  jq -n \
    --arg name "$APP_NAME" \
    --arg url "$AUTH_SITE_URL" \
    --arg redirect_url "$redirect_url" \
    --arg callback_url "$callback_url" \
    '{
      name: $name,
      url: $url,
      redirect_url: $redirect_url,
      callback_urls: [$callback_url],
      description: "Sage Router hosted account authentication",
      public: true,
      request_oauth_on_install: false,
      default_permissions: {},
      default_events: []
    }'
)"

target="https://github.com/settings/apps/new?state=${state}"
if [[ -n "$APP_OWNER" ]]; then
  target="https://github.com/organizations/${APP_OWNER}/settings/apps/new?state=${state}"
fi

form="${TMPDIR:-/tmp}/sage-router-github-auth-app.html"
python3 - "$target" "$manifest" > "$form" <<'PY'
import html
import sys

target, manifest = sys.argv[1], sys.argv[2]
print(f"""<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><title>Create Sage Router GitHub Auth App</title></head>
<body>
  <form id="github-app-form" action="{html.escape(target, quote=True)}" method="post">
    <input type="hidden" name="manifest" value="{html.escape(manifest, quote=True)}">
    <button type="submit">Create Sage Router GitHub Auth App</button>
  </form>
  <script>document.getElementById('github-app-form').submit();</script>
</body>
</html>""")
PY

prepare_windows_form

if [[ "$LOCAL_CAPTURE" != "0" && "$LOCAL_CAPTURE" != "false" && "$LOCAL_CAPTURE" != "no" ]]; then
  code_file="$(mktemp)"
  capture_log="$(mktemp)"
  python3 - "$LOCAL_CAPTURE_BIND" "$LOCAL_CAPTURE_PORT" "$code_file" "$form" >/dev/null 2>"$capture_log" <<'PY' &
import http.server
import pathlib
import sys
import time
import urllib.parse

bind = sys.argv[1]
port = int(sys.argv[2])
code_file = pathlib.Path(sys.argv[3])
form_file = pathlib.Path(sys.argv[4])
deadline = time.time() + 600

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path in ("/", "/github-app-manifest-form.html"):
            body = form_file.read_text()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body.encode())))
            self.end_headers()
            self.wfile.write(body.encode())
            return
        code = urllib.parse.parse_qs(parsed.query).get("code", [""])[0]
        if code:
            code_file.write_text(code)
            body = """<!doctype html><html><head><meta charset="utf-8"><title>Sage Router GitHub Auth</title></head><body><h1>GitHub auth captured</h1><p>You can close this tab. Supabase configuration is continuing in the terminal.</p></body></html>"""
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body.encode())))
            self.end_headers()
            self.wfile.write(body.encode())
            self.server.done = True
            return
        body = "<!doctype html><html><body><h1>Missing manifest code</h1></body></html>"
        self.send_response(400)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body.encode())))
        self.end_headers()
        self.wfile.write(body.encode())

    def log_message(self, *_args):
        return

class ReusableHTTPServer(http.server.HTTPServer):
    allow_reuse_address = True

with ReusableHTTPServer((bind, port), Handler) as server:
    server.timeout = 1
    server.done = False
    while not server.done and time.time() < deadline:
        server.handle_request()
    if not server.done:
        sys.exit(124)
PY
  capture_pid="$!"
  cleanup_capture() {
    kill "$capture_pid" >/dev/null 2>&1 || true
    rm -f "$code_file" "$capture_log"
  }
  trap cleanup_capture EXIT
  sleep 0.5
  if ! kill -0 "$capture_pid" >/dev/null 2>&1; then
    wait "$capture_pid" || true
    if [[ -s "$capture_log" ]]; then
      sed -n '1,12p' "$capture_log" >&2
    fi
    die "Local GitHub manifest capture server failed to start."
  fi

  cat <<EOF
GitHub requires an owner-approved browser step before it returns app credentials.

1. Opening this local form in a browser signed into the GitHub owner account:
$(form_location_text)
   Tailnet/local URL: ${redirect_url%/github-app-manifest.html}/
2. Approve the app named "${APP_NAME}".
3. The browser will return to ${redirect_url}; this script will capture the temporary code, configure Supabase, and exit.

The callback configured for Supabase will be:
  ${callback_url}
EOF

  open_form
  printf 'Waiting up to 10 minutes for the GitHub manifest approval redirect...\n'
  wait "$capture_pid" || die "Timed out waiting for the GitHub manifest approval redirect. Retry with SAGEROUTER_GITHUB_APP_LOCAL_CAPTURE=0 bash scripts/bootstrap_github_supabase_auth.sh, approve the app, then run the command printed by ${AUTH_SITE_URL%/}${hosted_manifest_path}?code=..."
  MANIFEST_CODE="$(cat "$code_file")"
  trap - EXIT
  rm -f "$code_file" "$capture_log"
  convert_manifest
  exit 0
fi

cat <<EOF
GitHub requires an owner-approved browser step before it returns app credentials.

1. Open this local form in a browser signed into the GitHub owner account:
$(form_location_text)
2. Approve the app named "${APP_NAME}".
3. GitHub redirects to ${AUTH_SITE_URL%/}${hosted_manifest_path}?code=...
4. Rerun this script with:
   bash scripts/bootstrap_github_supabase_auth.sh '${AUTH_SITE_URL%/}${hosted_manifest_path}?code=...'

The callback configured for Supabase will be:
  ${callback_url}
EOF

open_form
