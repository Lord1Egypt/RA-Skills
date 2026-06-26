#!/usr/bin/env bash
# onedrive-share.sh — Sharing, permissions, and share-URL resolution for OneDrive
#
# Usage: onedrive-share.sh <command> [args]

set -euo pipefail

CONFIG_DIR="${ONEDRIVE_MCP_CONFIG_DIR:-$HOME/.onedrive-mcp}"
CREDS_FILE="$CONFIG_DIR/credentials.json"
GRAPH="${ONEDRIVE_GRAPH_BASE:-https://graph.microsoft.com/v1.0}"
DRIVE_PREFIX="${ONEDRIVE_DRIVE_PREFIX:-/me/drive}"

get_token() {
    if [ -n "${ONEDRIVE_ACCESS_TOKEN:-}" ]; then echo "$ONEDRIVE_ACCESS_TOKEN"; return; fi
    [ -f "$CREDS_FILE" ] || { echo "Error: no token. Run onedrive-setup.sh or set ONEDRIVE_ACCESS_TOKEN" >&2; exit 1; }
    jq -r '.access_token // empty' "$CREDS_FILE"
}

url_encode_path() {
    python3 -c '
import sys, urllib.parse
p = sys.argv[1].strip("/")
print("/".join(urllib.parse.quote(seg, safe="") for seg in p.split("/")))
' "$1" 2>/dev/null || echo "$1"
}

item_url() {
    local target="$1" suffix="${2:-}"
    if [[ "$target" =~ ^[A-Za-z0-9!_-]{8,}$ ]] && [[ "$target" != */* ]]; then
        echo "$GRAPH$DRIVE_PREFIX/items/$target$suffix"
    else
        local enc; enc=$(url_encode_path "$target")
        if [ -z "$suffix" ]; then
            echo "$GRAPH$DRIVE_PREFIX/root:/$enc"
        else
            echo "$GRAPH$DRIVE_PREFIX/root:/$enc:$suffix"
        fi
    fi
}

# ===== link <target> <type> <scope> [--password X --expiry YYYY-MM-DD] =====
cmd_link() {
    local target="${1:?usage: link <path-or-id> <type> <scope> [--password X] [--expiry YYYY-MM-DD]}"
    local type="${2:?type: view|edit|embed}"
    local scope="${3:?scope: anonymous|organization|users}"
    shift 3
    local password="" expiry=""
    while [ $# -gt 0 ]; do
        case "$1" in
            --password) password="$2"; shift 2 ;;
            --expiry)   expiry="$2"; shift 2 ;;
            *) echo "Unknown option: $1" >&2; exit 1 ;;
        esac
    done

    local body
    body=$(jq -n --arg t "$type" --arg s "$scope" '{type:$t, scope:$s}')
    if [ -n "$password" ]; then
        body=$(echo "$body" | jq --arg p "$password" '. + {password:$p}')
    fi
    if [ -n "$expiry" ]; then
        # API expects ISO 8601 datetime; add midnight UTC if user gave a date
        local iso="$expiry"
        [[ "$iso" != *"T"* ]] && iso="${iso}T00:00:00Z"
        body=$(echo "$body" | jq --arg e "$iso" '. + {expirationDateTime:$e}')
    fi

    local token; token=$(get_token)
    local url; url=$(item_url "$target" "/createLink")
    curl -fsS -X POST "$url" \
        -H "Authorization: Bearer $token" \
        -H "Content-Type: application/json" \
        -d "$body" \
      | jq '{id, type: .link.type, scope: .link.scope, webUrl: .link.webUrl, expirationDateTime, hasPassword}'
}

# ===== invite <target> <emails-comma-sep> <role> [message] [--no-notify] =====
cmd_invite() {
    local target="${1:?usage: invite <path-or-id> <emails> <role> [message] [--no-notify]}"
    local emails="${2:?emails: comma-separated list}"
    local role="${3:?role: read | write}"
    local message="${4:-}"
    local send="true"
    [ "${5:-}" = "--no-notify" ] && send="false"

    local recipients
    recipients=$(echo "$emails" | jq -Rc 'split(",") | map({email:(.|gsub("^\\s+|\\s+$";""))})')

    local body
    body=$(jq -n \
        --argjson r "$recipients" \
        --arg role "$role" \
        --arg msg "$message" \
        --argjson send "$send" \
        '{recipients:$r, roles:[$role], sendInvitation:$send, requireSignIn:true, message:$msg}')

    local token; token=$(get_token)
    local url; url=$(item_url "$target" "/invite")
    curl -fsS -X POST "$url" \
        -H "Authorization: Bearer $token" \
        -H "Content-Type: application/json" \
        -d "$body" \
      | jq '.value[] | {id, roles, grantedTo: (.grantedToV2.user.email // .grantedToV2.user.displayName)}'
}

# ===== permissions <target> =====
cmd_permissions() {
    local target="${1:?usage: permissions <path-or-id>}"
    local token; token=$(get_token)
    local url; url=$(item_url "$target" "/permissions")
    curl -fsS "$url" -H "Authorization: Bearer $token" \
      | jq '.value[] | {
            id,
            roles,
            type: (.link.type // (if .invitation then "invitation" else "user" end)),
            scope: .link.scope,
            grantedTo: (.grantedToV2.user.email // .grantedToV2.user.displayName // .invitation.email // null),
            link: .link.webUrl,
            expirationDateTime
        }'
}

# ===== revoke <target> <perm-id> =====
cmd_revoke() {
    local target="${1:?usage: revoke <path-or-id> <perm-id>}"
    local perm="${2:?usage: revoke <path-or-id> <perm-id>}"
    local token; token=$(get_token)
    local url; url=$(item_url "$target" "/permissions/$perm")
    local code
    code=$(curl -s -o /dev/null -w "%{http_code}" -X DELETE "$url" \
        -H "Authorization: Bearer $token")
    if [ "$code" = "204" ]; then
        echo "{\"status\":\"revoked\",\"perm\":\"$perm\"}"
    else
        echo "{\"status\":\"failed\",\"http_code\":$code}" >&2
        exit 1
    fi
}

# ===== update-role <target> <perm-id> <new-role> =====
cmd_update_role() {
    local target="${1:?usage: update-role <path-or-id> <perm-id> <new-role>}"
    local perm="${2:?usage}" role="${3:?usage}"
    local token; token=$(get_token)
    local url; url=$(item_url "$target" "/permissions/$perm")
    curl -fsS -X PATCH "$url" \
        -H "Authorization: Bearer $token" \
        -H "Content-Type: application/json" \
        -d "$(jq -n --arg r "$role" '{roles:[$r]}')" \
      | jq '{id, roles}'
}

# ===== open <share-url> — resolve a sharing URL to a DriveItem =====
cmd_open() {
    local share_url="${1:?usage: open <share-url>}"
    # Encode: u!<base64url(URL)>  (strip padding)
    local share_id
    share_id="u!$(echo -n "$share_url" | base64 -w0 2>/dev/null | tr '+/' '-_' | tr -d '=')"
    local token; token=$(get_token)
    curl -fsS "$GRAPH/shares/$share_id/driveItem" \
        -H "Authorization: Bearer $token" \
      | jq
}

# ===== owner <target> — show creator / owner =====
cmd_owner() {
    local target="${1:?usage: owner <path-or-id>}"
    local token; token=$(get_token)
    local url; url=$(item_url "$target")
    curl -fsS "$url?\$select=createdBy,lastModifiedBy,name,id" \
        -H "Authorization: Bearer $token" \
      | jq '{
            name,
            id,
            createdBy: (.createdBy.user.displayName // .createdBy.user.email),
            lastModifiedBy: (.lastModifiedBy.user.displayName // .lastModifiedBy.user.email)
        }'
}

cmd_help() {
    cat <<EOF
Usage: onedrive-share.sh <command> [args]

LINKS
  link <path-or-id> <type> <scope> [--password X] [--expiry YYYY-MM-DD]
       type:  view | edit | embed
       scope: anonymous | organization | users

INVITE
  invite <path-or-id> <emails> <role> [message] [--no-notify]
       emails: comma-separated (alice@x.com,bob@y.com)
       role:   read | write

PERMISSIONS
  permissions <path-or-id>             List all permissions on an item
  revoke <path-or-id> <perm-id>        Delete a permission
  update-role <path-or-id> <perm-id> <new-role>

RESOLVE
  open <share-url>                     Look up a 1drv.ms / SharePoint share URL → DriveItem

INFO
  owner <path-or-id>                   Show creator / last modifier

Env overrides:
  ONEDRIVE_ACCESS_TOKEN, ONEDRIVE_DRIVE_PREFIX, ONEDRIVE_GRAPH_BASE
EOF
}

case "${1:-help}" in
    link)         shift; cmd_link "$@" ;;
    invite)       shift; cmd_invite "$@" ;;
    permissions)  shift; cmd_permissions "$@" ;;
    revoke)       shift; cmd_revoke "$@" ;;
    update-role)  shift; cmd_update_role "$@" ;;
    open)         shift; cmd_open "$@" ;;
    owner)        shift; cmd_owner "$@" ;;
    help|--help|-h|"") cmd_help ;;
    *) echo "Unknown command: $1"; cmd_help; exit 1 ;;
esac
