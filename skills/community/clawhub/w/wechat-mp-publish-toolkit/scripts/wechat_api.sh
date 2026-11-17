#!/bin/bash
# WeChat Official Account API Helper Functions (Generic Version)
# Usage: source wechat_api.sh
#
# Before using, set environment variables:
#   export WECHAT_APPID="wx_your_appid"
#   export WECHAT_SECRET="your_secret"

require_cmd() {
    command -v "$1" >/dev/null 2>&1 || {
        echo "ERROR: missing command: $1" >&2
        return 1
    }
}

require_env() {
    local name=$1
    local val
    eval "val=\${${name}:-}"
    if [[ -z "$val" ]]; then
        echo "ERROR: missing env var: ${name}" >&2
        return 1
    fi
}

# ============ Official Account API ============

# Get access_token
# Usage: get_wechat_token
# Output: access_token string (or error message to stderr)
get_wechat_token() {
    require_cmd curl || return 1
    require_cmd jq   || return 1
    require_env WECHAT_APPID  || return 1
    require_env WECHAT_SECRET || return 1

    local response
    response=$(curl -s "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=${WECHAT_APPID}&secret=${WECHAT_SECRET}")

    local errcode
    errcode=$(echo "$response" | jq -r '.errcode // 0')

    if [[ "$errcode" == "40164" ]]; then
        local server_ip
        server_ip=$(curl -s https://api.ipify.org)
        echo "ERROR: Server IP ${server_ip} is not whitelisted." >&2
        echo "Add it at: mp.weixin.qq.com -> Development -> Basic Configuration -> IP Whitelist" >&2
        return 1
    fi

    echo "$response" | jq -r '.access_token'
}

# Upload image to WeChat permanent material library (for cover images)
# Usage: upload_wechat_image <token> <image_path>
# Output: JSON with media_id field
upload_wechat_image() {
    require_cmd curl || return 1
    local token=$1
    local image_path=$2

    if [[ ! -f "$image_path" ]]; then
        echo "ERROR: image file not found: $image_path" >&2
        return 1
    fi

    curl -s -X POST \
        "https://api.weixin.qq.com/cgi-bin/material/add_material?access_token=${token}&type=image" \
        -F "media=@${image_path}"
}

# Create draft
# Usage: create_draft <token> <json_file>
# Output: JSON with media_id field (draft ID)
# Note: The JSON file must use ensure_ascii=False to preserve Chinese characters.
#       Generate it with: python3 -c "import json; json.dump(data, f, ensure_ascii=False)"
create_draft() {
    require_cmd curl || return 1
    local token=$1
    local json_file=$2

    if [[ ! -f "$json_file" ]]; then
        echo "ERROR: JSON file not found: $json_file" >&2
        return 1
    fi

    # Use --data-binary to avoid unicode escape issues
    curl -s -X POST \
        "https://api.weixin.qq.com/cgi-bin/draft/add?access_token=${token}" \
        -H "Content-Type: application/json" \
        --data-binary @"${json_file}"
}

# Publish a draft to all subscribers
# Usage: publish_draft <token> <media_id>
# Output: JSON with publish_id field (on success) or errcode
publish_draft() {
    require_cmd curl || return 1
    local token=$1
    local media_id=$2

    curl -s -X POST \
        "https://api.weixin.qq.com/cgi-bin/freepublish/submit?access_token=${token}" \
        -H "Content-Type: application/json" \
        -d "{\"media_id\":\"${media_id}\"}"
}

# List all drafts in the draft box
# Usage: list_drafts <token> [offset] [count]
# Output: JSON with draft items
list_drafts() {
    require_cmd curl || return 1
    local token=$1
    local offset=${2:-0}
    local count=${3:-20}

    curl -s -X POST \
        "https://api.weixin.qq.com/cgi-bin/draft/batchget?access_token=${token}" \
        -H "Content-Type: application/json" \
        -d "{\"offset\":${offset},\"count\":${count},\"no_content\":1}"
}

# Delete a draft
# Usage: delete_draft <token> <media_id>
delete_draft() {
    require_cmd curl || return 1
    local token=$1
    local media_id=$2

    curl -s -X POST \
        "https://api.weixin.qq.com/cgi-bin/draft/delete?access_token=${token}" \
        -H "Content-Type: application/json" \
        -d "{\"media_id\":\"${media_id}\"}"
}

# ============ Echo available functions ============

echo "WeChat MP API helpers loaded. Available functions:"
echo "  get_wechat_token      - Get official account access_token"
echo "  upload_wechat_image   - Upload cover image to material library"
echo "  create_draft          - Create draft from JSON file"
echo "  publish_draft         - Publish draft to all subscribers"
echo "  list_drafts           - List drafts in draft box"
echo "  delete_draft          - Delete a draft by media_id"
