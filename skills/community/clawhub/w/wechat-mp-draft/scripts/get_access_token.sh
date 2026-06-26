#!/bin/bash
# 获取微信公众号 Access Token
# 使用方法：./get_access_token.sh

set -e

# 尝试从配置文件加载凭证（优先）
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ -f "$SCRIPT_DIR/config.sh" ]; then
    source "$SCRIPT_DIR/config.sh"
fi

# 如果配置文件不存在，使用默认占位符（需要用户替换）
APPID="${APPID:-wxYOUR_APPID_HERE}"
APPSECRET="${APPSECRET:-YOUR_SECRET_HERE}"

# 检查凭证是否已配置
if [ "$APPID" = "wxYOUR_APPID_HERE" ] || [ "$APPSECRET" = "YOUR_SECRET_HERE" ]; then
    echo "❌ 错误：请先配置微信公众号凭证"
    echo ""
    echo "使用方法："
    echo "1. 复制 config.template.sh 为 config.sh"
    echo "2. 编辑 config.sh 填入你的 AppID 和 AppSecret"
    echo "3. 重新运行本脚本"
    echo ""
    echo "获取凭证：微信公众平台 → 设置与开发 → 基本配置"
    exit 1
fi

# 调用微信 API
RESPONSE=$(curl -s "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=${APPID}&secret=${APPSECRET}")

# 检查是否成功
if echo "$RESPONSE" | grep -q '"access_token"'; then
    TOKEN=$(echo "$RESPONSE" | grep -oP '"access_token":"\K[^"]+')
    EXPIRES=$(echo "$RESPONSE" | grep -oP '"expires_in":\K[0-9]+')
    
    echo "✅ Token 获取成功（有效期 ${EXPIRES} 秒）"
    echo "{\"access_token\":\"$TOKEN\",\"expires_in\":$EXPIRES}"
else
    echo "❌ Token 获取失败"
    echo "$RESPONSE"
    
    # 解析错误码给出提示
    if echo "$RESPONSE" | grep -q '40164'; then
        echo ""
        echo "提示：当前服务器 IP 不在白名单中"
        echo "请登录微信公众平台 → 设置与开发 → 基本配置 → IP 白名单"
        echo "添加当前服务器 IP 地址"
    fi
    
    exit 1
fi
