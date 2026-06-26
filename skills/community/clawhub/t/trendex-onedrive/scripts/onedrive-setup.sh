#!/usr/bin/env bash
# onedrive-setup.sh — Automated Azure AD app registration + OAuth flow for OneDrive (Microsoft Graph)
# Requires: az (Azure CLI), jq, curl

set -euo pipefail

CONFIG_DIR="${ONEDRIVE_MCP_CONFIG_DIR:-$HOME/.onedrive-mcp}"
CONFIG_FILE="$CONFIG_DIR/config.json"
CREDS_FILE="$CONFIG_DIR/credentials.json"

APP_NAME="${ONEDRIVE_APP_NAME:-Clawdbot-OneDrive}"
REDIRECT_URI="${ONEDRIVE_REDIRECT_URI:-http://localhost}"
TENANT="${ONEDRIVE_TENANT:-common}"   # common | consumers | organizations | <tenant-id>
SCOPES="${ONEDRIVE_SCOPES:-https://graph.microsoft.com/Files.ReadWrite.All https://graph.microsoft.com/Sites.ReadWrite.All https://graph.microsoft.com/User.Read offline_access}"

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; NC='\033[0m'

echo -e "${BLUE}=== OneDrive (Microsoft Graph) OAuth Setup ===${NC}"
echo ""

check_prereqs() {
    local missing=()
    command -v az >/dev/null 2>&1 || missing+=("az (Azure CLI)")
    command -v jq >/dev/null 2>&1 || missing+=("jq")
    command -v curl >/dev/null 2>&1 || missing+=("curl")
    if [ ${#missing[@]} -gt 0 ]; then
        echo -e "${RED}Missing prerequisites:${NC} ${missing[*]}"
        echo "  - Azure CLI: curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash"
        echo "  - jq:        sudo apt install jq"
        exit 1
    fi
}

azure_login() {
    echo -e "${YELLOW}Step 1: Azure Login${NC}"
    if az account show >/dev/null 2>&1; then
        local user
        user=$(az account show --query user.name -o tsv)
        echo -e "Currently logged in as: ${GREEN}$user${NC}"
        read -p "Continue with this account? [Y/n] " -n 1 -r REPLY; echo
        if [[ $REPLY =~ ^[Nn]$ ]]; then az logout 2>/dev/null || true; else return 0; fi
    fi
    echo "Using device code login (works headless):"
    az login --use-device-code >/dev/null || { echo -e "${RED}Login failed${NC}"; exit 1; }
    echo -e "${GREEN}✓ Logged in${NC}"
}

create_app() {
    echo ""
    echo -e "${YELLOW}Step 2: Creating App Registration${NC}"
    local existing
    existing=$(az ad app list --display-name "$APP_NAME" --query "[0].appId" -o tsv 2>/dev/null || true)
    if [ -n "$existing" ] && [ "$existing" != "null" ]; then
        echo -e "App '$APP_NAME' exists: ${BLUE}$existing${NC}"
        read -p "Reuse it? [Y/n] " -n 1 -r REPLY; echo
        if [[ ! $REPLY =~ ^[Nn]$ ]]; then
            APP_ID="$existing"
            echo -e "${GREEN}✓ Reusing existing app${NC}"
            return 0
        fi
        APP_NAME="$APP_NAME-$(date +%s)"
        echo "Creating new app: $APP_NAME"
    fi
    APP_ID=$(az ad app create \
        --display-name "$APP_NAME" \
        --sign-in-audience "AzureADandPersonalMicrosoftAccount" \
        --web-redirect-uris "$REDIRECT_URI" \
        --query appId -o tsv)
    echo -e "${GREEN}✓ App created: $APP_ID${NC}"
}

create_secret() {
    echo ""
    echo -e "${YELLOW}Step 3: Creating Client Secret${NC}"
    local result
    result=$(az ad app credential reset --id "$APP_ID" \
        --display-name "onedrive-cli" --years 2 \
        --query "{clientId: appId, clientSecret: password}" -o json)
    CLIENT_ID=$(echo "$result" | jq -r '.clientId')
    CLIENT_SECRET=$(echo "$result" | jq -r '.clientSecret')
    if [ -z "$CLIENT_SECRET" ] || [ "$CLIENT_SECRET" = "null" ]; then
        echo -e "${RED}Failed to create secret${NC}"; exit 1
    fi
    echo -e "${GREEN}✓ Secret created${NC}"
}

add_permissions() {
    echo ""
    echo -e "${YELLOW}Step 4: Adding API Permissions${NC}"
    local GRAPH="00000003-0000-0000-c000-000000000000"
    local files_rw_all sites_rw_all user_read
    files_rw_all=$(az ad sp show --id "$GRAPH" --query "oauth2PermissionScopes[?value=='Files.ReadWrite.All'].id" -o tsv 2>/dev/null || true)
    sites_rw_all=$(az ad sp show --id "$GRAPH" --query "oauth2PermissionScopes[?value=='Sites.ReadWrite.All'].id" -o tsv 2>/dev/null || true)
    user_read=$(az ad sp show --id "$GRAPH" --query "oauth2PermissionScopes[?value=='User.Read'].id" -o tsv 2>/dev/null || true)

    local perms=()
    [ -n "$files_rw_all" ] && perms+=("$files_rw_all=Scope")
    [ -n "$sites_rw_all" ] && perms+=("$sites_rw_all=Scope")
    [ -n "$user_read" ] && perms+=("$user_read=Scope")

    if [ ${#perms[@]} -gt 0 ]; then
        az ad app permission add --id "$APP_ID" --api "$GRAPH" \
            --api-permissions "${perms[@]}" 2>/dev/null || true
    fi
    echo -e "${GREEN}✓ Permissions: Files.ReadWrite.All, Sites.ReadWrite.All, User.Read${NC}"
    echo -e "  (offline_access is requested at sign-in, not declared here)"
}

save_config() {
    echo ""
    echo -e "${YELLOW}Step 5: Saving Configuration${NC}"
    mkdir -p "$CONFIG_DIR" && chmod 700 "$CONFIG_DIR"
    cat > "$CONFIG_FILE" <<EOF
{
  "client_id": "$CLIENT_ID",
  "client_secret": "$CLIENT_SECRET",
  "tenant": "$TENANT",
  "redirect_uri": "$REDIRECT_URI",
  "scopes": "$SCOPES"
}
EOF
    chmod 600 "$CONFIG_FILE"
    echo -e "${GREEN}✓ Config saved to $CONFIG_FILE${NC}"
}

url_encode() {
    python3 -c 'import sys,urllib.parse;print(urllib.parse.quote(sys.argv[1],safe=""))' "$1" 2>/dev/null \
        || jq -nr --arg v "$1" '$v|@uri'
}

authorize() {
    echo ""
    echo -e "${YELLOW}Step 6: User Authorization${NC}"
    local enc_scope enc_redirect
    enc_scope=$(url_encode "$SCOPES")
    enc_redirect=$(url_encode "$REDIRECT_URI")
    local auth_url="https://login.microsoftonline.com/$TENANT/oauth2/v2.0/authorize?client_id=$CLIENT_ID&response_type=code&redirect_uri=$enc_redirect&response_mode=query&scope=$enc_scope"

    echo ""
    echo "Open this URL in a browser (the same Microsoft account whose OneDrive you want to use):"
    echo ""
    echo -e "${BLUE}$auth_url${NC}"
    echo ""
    echo "After consent, the browser will be redirected to $REDIRECT_URI?code=... (page won't load)."
    echo "Copy the FULL redirected URL (or just the code parameter) and paste below."
    echo ""
    read -p "Redirected URL or code: " input

    local code
    if [[ "$input" == *"code="* ]]; then
        code=$(echo "$input" | grep -oP 'code=\K[^&]+' || true)
    else
        code="$input"
    fi

    if [ -z "$code" ]; then
        echo -e "${RED}No authorization code found${NC}"; exit 1
    fi

    echo "Exchanging code for tokens..."
    local response
    response=$(curl -s -X POST "https://login.microsoftonline.com/$TENANT/oauth2/v2.0/token" \
        -H "Content-Type: application/x-www-form-urlencoded" \
        --data-urlencode "client_id=$CLIENT_ID" \
        --data-urlencode "client_secret=$CLIENT_SECRET" \
        --data-urlencode "code=$code" \
        --data-urlencode "redirect_uri=$REDIRECT_URI" \
        --data-urlencode "grant_type=authorization_code" \
        --data-urlencode "scope=$SCOPES")

    if echo "$response" | jq -e '.access_token' >/dev/null 2>&1; then
        # Annotate with expiry timestamp for easy local checking
        local now expires_in
        now=$(date +%s)
        expires_in=$(echo "$response" | jq -r '.expires_in // 3600')
        echo "$response" | jq --argjson now "$now" --argjson exp "$expires_in" \
            '. + {acquired_at: $now, expires_at: ($now + $exp)}' > "$CREDS_FILE"
        chmod 600 "$CREDS_FILE"
        echo -e "${GREEN}✓ Tokens saved to $CREDS_FILE${NC}"
    else
        echo -e "${RED}Token exchange failed:${NC}"
        echo "$response" | jq '.error_description // .'
        exit 1
    fi
}

test_connection() {
    echo ""
    echo -e "${YELLOW}Step 7: Testing Connection${NC}"
    local token
    token=$(jq -r '.access_token' "$CREDS_FILE")
    local drive
    drive=$(curl -s "https://graph.microsoft.com/v1.0/me/drive" -H "Authorization: Bearer $token")
    if echo "$drive" | jq -e '.id' >/dev/null 2>&1; then
        local owner used total
        owner=$(echo "$drive" | jq -r '.owner.user.displayName // .owner.user.email // "?"')
        used=$(echo "$drive" | jq -r '.quota.used // 0')
        total=$(echo "$drive" | jq -r '.quota.total // 0')
        echo -e "${GREEN}✓ Connected!${NC}"
        echo -e "  Owner: ${BLUE}$owner${NC}"
        echo -e "  Storage: $used / $total bytes used"
    else
        echo -e "${RED}Connection test failed:${NC}"
        echo "$drive" | jq '.error.message // .'
        exit 1
    fi
}

main() {
    check_prereqs
    azure_login
    create_app
    create_secret
    add_permissions
    save_config
    authorize
    test_connection
    echo ""
    echo -e "${GREEN}=== Setup complete ===${NC}"
    echo ""
    echo "Try:"
    echo "  ./scripts/onedrive-files.sh list"
    echo "  ./scripts/onedrive-files.sh quota"
    echo "  ./scripts/onedrive-token.sh refresh"
}

main "$@"
