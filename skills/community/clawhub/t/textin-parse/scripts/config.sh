#!/bin/bash

# Textin API 配置
# 保存用户的 API 凭证

CONFIG_FILE="$HOME/.openclaw/textin-config.json"

save_credentials() {
    local app_id="$1"
    local secret_code="$2"
    
    mkdir -p "$(dirname "$CONFIG_FILE")"
    echo "{\"app_id\": \"$app_id\", \"secret_code\": \"$secret_code\"}" > "$CONFIG_FILE"
    echo "✅ 凭证已保存"
}

get_credentials() {
    if [ -f "$CONFIG_FILE" ]; then
        cat "$CONFIG_FILE"
    else
        echo "{}"
    fi
}

case "$1" in
    save)
        save_credentials "$2" "$3"
        ;;
    get)
        get_credentials
        ;;
    *)
        echo "Usage: $0 {save|get} [app_id] [secret_code]"
        ;;
esac