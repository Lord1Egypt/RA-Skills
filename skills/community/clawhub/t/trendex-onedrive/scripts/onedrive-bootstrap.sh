#!/usr/bin/env bash
# onedrive-bootstrap.sh — Headless OneDrive (Microsoft Graph) provisioning.
#
# Templated install: the deploy system substitutes the __PLACEHOLDERS__ below
# with real values before running. No browser, no Azure CLI needed.
#
# Drops:
#   ~/.onedrive-mcp/config.json       client_id, client_secret
#   ~/.onedrive-mcp/credentials.json  access_token, refresh_token, expires_in
# Then refreshes the token at Microsoft Entra and probes Microsoft Graph
# (`/me/drive`) to confirm the install.

set -euo pipefail
export DEBIAN_FRONTEND=noninteractive

export HOME="${HOME:-/root}"
export PATH="$(npm config get prefix 2>/dev/null)/bin:/usr/local/bin:/usr/bin:/bin:$PATH"
hash -r

# === Substituted at deploy time =====================================
CLIENT_ID='__CLIENT_ID__'
CLIENT_SECRET='__CLIENT_SECRET__'
ACCESS_TOKEN='__ACCESS_TOKEN__'
REFRESH_TOKEN='__REFRESH_TOKEN__'
TENANT='__TENANT__'                       # e.g. 'common' or a tenant GUID
SCOPE='__ONEDRIVE_SCOPES__'               # space-separated, full URI form
# ====================================================================

# Fallbacks if the deploy system left something unsubstituted
[ "$TENANT" = "__TENANT__" ] && TENANT="common"
[ "$SCOPE"  = "__ONEDRIVE_SCOPES__" ] && SCOPE="https://graph.microsoft.com/Files.ReadWrite.All https://graph.microsoft.com/Sites.ReadWrite.All https://graph.microsoft.com/User.Read offline_access"

echo "===================================================="
echo "[onedrive/setup] starting"
echo "===================================================="

if ! command -v jq >/dev/null 2>&1 || ! command -v curl >/dev/null 2>&1; then
  echo "[onedrive/setup] installing jq + curl (missing)..."
  apt-get update -qq
  apt-get install -y -qq jq curl ca-certificates
else
  echo "[onedrive/setup] jq + curl already present, skipping apt install"
fi

echo "[onedrive/setup] stopping openclaw (if running)..."
killall openclaw 2>/dev/null || true

echo "[onedrive/setup] writing config + credentials to ~/.onedrive-mcp/..."
mkdir -p "$HOME/.onedrive-mcp"
chmod 700 "$HOME/.onedrive-mcp"

cat > "$HOME/.onedrive-mcp/config.json" <<EOF
{
  "client_id": "$CLIENT_ID",
  "client_secret": "$CLIENT_SECRET",
  "tenant": "$TENANT",
  "redirect_uri": "http://localhost",
  "scopes": "$SCOPE"
}
EOF
chmod 600 "$HOME/.onedrive-mcp/config.json"

cat > "$HOME/.onedrive-mcp/credentials.json" <<EOF
{
  "token_type": "Bearer",
  "access_token": "$ACCESS_TOKEN",
  "refresh_token": "$REFRESH_TOKEN",
  "expires_in": 3600
}
EOF
chmod 600 "$HOME/.onedrive-mcp/credentials.json"

CREDS="$HOME/.onedrive-mcp/credentials.json"
RT_KEEP="$(jq -r '.refresh_token // empty' "$CREDS" | tr -d '\r\n\t ')"

if [ -z "$RT_KEEP" ] || [ "$RT_KEEP" = "null" ]; then
  echo "[onedrive/setup] ERROR: missing refresh_token in credentials file." >&2
  exit 1
fi

TOKEN_URL="https://login.microsoftonline.com/${TENANT}/oauth2/v2.0/token"

echo "[onedrive/setup] refreshing access_token at Microsoft Entra (tenant=$TENANT)..."
TOKEN_JSON="$(curl --http1.1 -sS -X POST "$TOKEN_URL" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data-urlencode "client_id=$CLIENT_ID" \
  --data-urlencode "client_secret=$CLIENT_SECRET" \
  --data-urlencode "grant_type=refresh_token" \
  --data-urlencode "refresh_token=$RT_KEEP" \
  --data-urlencode "scope=$SCOPE")"

if ! echo "$TOKEN_JSON" | jq -e '.access_token' >/dev/null 2>&1; then
  echo "[onedrive/setup] ERROR: Microsoft token refresh failed: $(echo "$TOKEN_JSON" | head -c 3000 | tr -d '\r\n')" >&2
  exit 1
fi
echo "[onedrive/setup] token refresh OK"

NOW="$(date +%s)"
# Persist new tokens (Microsoft rotates the refresh_token); annotate with expiry
echo "$TOKEN_JSON" \
  | jq --arg rt "$RT_KEEP" --argjson now "$NOW" \
       '. + {
          refresh_token: (.refresh_token // $rt),
          token_type:    (.token_type // "Bearer"),
          acquired_at:   $now,
          expires_at:    ($now + (.expires_in // 3600))
        }' \
  > "$CREDS"
chmod 600 "$CREDS"

AT="$(jq -r '.access_token' "$CREDS" | tr -d '\r\n\t ')"

if [ -z "$AT" ] || [ "$AT" = "null" ]; then
  echo "[onedrive/setup] ERROR: no access_token after refresh." >&2
  exit 1
fi

echo "[onedrive/setup] probing Microsoft Graph /me/drive..."

HTTP="$(curl --http1.1 -sS \
  -D /tmp/onedrive-probe.headers \
  -o /tmp/onedrive-probe.body \
  -w "%{http_code}" \
  -H "Authorization: Bearer ${AT}" \
  -H "Accept: application/json" \
  'https://graph.microsoft.com/v1.0/me/drive')"

if [ "$HTTP" != "200" ]; then
  echo "[onedrive/setup] ERROR: Graph drive probe failed HTTP $HTTP" >&2
  echo "---- headers ----" >&2
  cat /tmp/onedrive-probe.headers >&2
  echo "---- body ----" >&2
  head -c 3000 /tmp/onedrive-probe.body | tr -d '\r' >&2
  echo >&2
  exit 1
fi

echo "[onedrive/setup] Graph drive response:"
cat /tmp/onedrive-probe.body \
  | jq '{
      owner: (.owner.user.displayName // .owner.user.email // "?"),
      driveType,
      total: .quota.total,
      used:  .quota.used,
      remaining: .quota.remaining
    }'

# Quick listing probe to confirm read scope
echo "[onedrive/setup] probing Microsoft Graph /me/drive/root/children (top=1)..."
HTTP2="$(curl --http1.1 -sS \
  -o /tmp/onedrive-children.body \
  -w "%{http_code}" \
  -H "Authorization: Bearer ${AT}" \
  -H "Accept: application/json" \
  'https://graph.microsoft.com/v1.0/me/drive/root/children?$top=1&$select=id,name,folder,file')"
if [ "$HTTP2" = "200" ]; then
  COUNT="$(jq '.value | length' /tmp/onedrive-children.body 2>/dev/null || echo 0)"
  echo "[onedrive/setup] root listing OK (sample items: $COUNT)"
else
  echo "[onedrive/setup] WARN: root listing returned HTTP $HTTP2 (not fatal)" >&2
fi

chmod 711 /root

echo "[onedrive/setup] updating ~/.bashrc env exports..."
sed -i '/ONEDRIVE_MCP/d' ~/.bashrc 2>/dev/null || true
cat <<'EOF' >> ~/.bashrc
export ONEDRIVE_MCP_CONFIG_DIR="/root/.onedrive-mcp"
EOF

echo "===================================================="
echo "[onedrive/setup] done — OneDrive Graph access OK (HTTP 200)"
echo "===================================================="
