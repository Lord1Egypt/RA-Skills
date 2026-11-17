#!/usr/bin/env bash

set -euo pipefail

require_wechat_credentials() {
    local missing=()

    [[ -n "${WECHAT_APP_ID:-}" ]] || missing+=("WECHAT_APP_ID")
    [[ -n "${WECHAT_APP_SECRET:-}" ]] || missing+=("WECHAT_APP_SECRET")
    [[ -n "${WECHAT_ACCOUNT_LABEL:-}" ]] || missing+=("WECHAT_ACCOUNT_LABEL")

    if (( ${#missing[@]} > 0 )); then
        printf 'Missing required secret-store/environment values: %s\n' "${missing[*]}" >&2
        printf 'Do not paste credentials into chat or save them in this skill folder.\n' >&2
        return 1
    fi
}

get_access_token() {
    require_wechat_credentials

    local response
    response=$(
        {
            printf 'url = "https://api.weixin.qq.com/cgi-bin/token"\n'
            printf 'silent\n'
            printf 'show-error\n'
            printf 'get\n'
            printf 'data-urlencode = "grant_type=client_credential"\n'
            printf 'data-urlencode = "appid=%s"\n' "$WECHAT_APP_ID"
            printf 'data-urlencode = "secret=%s"\n' "$WECHAT_APP_SECRET"
        } | curl --config -
    )

    local token
    token=$(jq -r '.access_token // empty' <<<"$response")
    if [[ -z "$token" ]]; then
        printf 'Failed to obtain WeChat access token: %s\n' \
            "$(jq -c '{errcode,errmsg}' <<<"$response")" >&2
        return 1
    fi

    printf '%s' "$token"
}

upload_image() {
    local access_token=$1
    local image_path=$2

    local encoded_token
    encoded_token=$(jq -rn --arg value "$access_token" '$value | @uri')

    {
        printf 'url = "https://api.weixin.qq.com/cgi-bin/material/add_material?access_token=%s&type=image"\n' "$encoded_token"
        printf 'silent\n'
        printf 'show-error\n'
    } | curl --config - -F "media=@${image_path}"
}

add_draft() {
    local access_token=$1
    local json_file=$2

    local encoded_token
    encoded_token=$(jq -rn --arg value "$access_token" '$value | @uri')

    {
        printf 'url = "https://api.weixin.qq.com/cgi-bin/draft/add?access_token=%s"\n' "$encoded_token"
        printf 'silent\n'
        printf 'show-error\n'
    } | curl --config - \
        -X POST \
        -H "Content-Type: application/json" \
        --data-binary "@${json_file}"
}
