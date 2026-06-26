#!/bin/bash
# WhatsApp 428 问题自动修复脚本
# 用法: bash fix-whatsapp-428.sh [代理端口]

set -e

PROXY_PORT=${1:-10808}
SERVICE_FILE="$HOME/.config/systemd/user/openclaw-gateway.service"
OPENCLAW_DIR="/home/admind/.npm-global/lib/node_modules/openclaw"

echo "=== WhatsApp 428 问题修复 ==="

# 1. 获取本地 IP
LOCAL_IP=$(hostname -I | awk '{print $1}')
echo "[1/7] 本地IP: $LOCAL_IP"

# 2. 查找并修改 auth-profiles-*.js (添加 proxy 字段)
echo "[2/7] 修改 auth-profiles 添加 proxy 字段..."
AUTH_PROFILES=$(find "$OPENCLAW_DIR/dist" -name "auth-profiles-*.js" 2>/dev/null | head -1)
if [ -n "$AUTH_PROFILES" ]; then
    echo "      找到: $AUTH_PROFILES"
    cp "$AUTH_PROFILES" "$AUTH_PROFILES.bak"
    
    # 添加 proxy 字段到 WhatsAppSharedSchema
    if ! grep -q "proxy: z.string()" "$AUTH_PROFILES"; then
        sed -i 's/proxy: z\.string()\.optional()/proxy: z.string().url().optional()/' "$AUTH_PROFILES"
        # 如果没有 proxy 字段，则添加
        if ! grep -q "proxy:" "$AUTH_PROFILES"; then
            sed -i '/WhatsAppSharedSchema.*=/{s/$/\n  proxy: z.string().url().optional()/}' "$AUTH_PROFILES"
        fi
    fi
    echo "      完成"
else
    echo "      [警告] 未找到 auth-profiles-*.js"
fi

# 3. 安装 https-proxy-agent
echo "[3/7] 安装 https-proxy-agent..."
cd "$OPENCLAW_DIR"
npm list https-proxy-agent >/dev/null 2>&1 || npm install https-proxy-agent --save

# 4. 修改 session-*.js (添加 HttpsProxyAgent)
echo "[4/7] 修改 session 添加 HttpsProxyAgent..."
SESSION_FILE=$(find "$OPENCLAW_DIR/dist" -name "session-*.js" 2>/dev/null | head -1)
if [ -n "$SESSION_FILE" ]; then
    echo "      找到: $SESSION_FILE"
    cp "$SESSION_FILE" "$SESSION_FILE.bak"
    
    # 添加 import
    if ! grep -q "https-proxy-agent" "$SESSION_FILE"; then
        sed -i "s|import.\+from.*zod.*;|import { z } from \"zod\";\nimport { HttpsProxyAgent } from \"https-proxy-agent\";|" "$SESSION_FILE"
    fi
    
    # 添加 agent 使用 (在 makeWASocket 调用附近)
    if ! grep -q "HttpsProxyAgent" "$SESSION_FILE"; then
        sed -i 's/const agent = undefined;/const agent = opts.proxy ? new HttpsProxyAgent(opts.proxy) : undefined;/' "$SESSION_FILE"
    fi
    echo "      完成"
else
    echo "      [警告] 未找到 session-*.js"
fi

# 5. 修改 channel-web-*.js (传入 proxy 参数)
echo "[5/7] 修改 channel-web 传入 proxy 参数..."
CHANNEL_WEB=$(find "$OPENCLAW_DIR/dist" -name "channel-web-*.js" 2>/dev/null | head -1)
if [ -n "$CHANNEL_WEB" ]; then
    echo "      找到: $CHANNEL_WEB"
    cp "$CHANNEL_WEB" "$CHANNEL_WEB.bak"
    
    # 在 createWaSocket 调用中添加 proxy 参数
    if ! grep -q "proxy:" "$CHANNEL_WEB"; then
        sed -i 's/authDir: options\.authDir/authDir: options.authDir,\n  proxy: options.proxy/' "$CHANNEL_WEB"
    fi
    echo "      完成"
else
    echo "      [警告] 未找到 channel-web-*.js"
fi

# 6. 检查并更新 systemd service
echo "[6/7] 更新 systemd service..."
if [ -f "$SERVICE_FILE" ]; then
    cp "$SERVICE_FILE" "$SERVICE_FILE.bak"
    
    if grep -q "HTTP_PROXY" "$SERVICE_FILE"; then
        echo "      已有代理配置，更新..."
        sed -i "s|HTTP_PROXY=.*|Environment=HTTP_PROXY=http://$LOCAL_IP:$PROXY_PORT|" "$SERVICE_FILE"
        sed -i "s|HTTPS_PROXY=.*|Environment=HTTPS_PROXY=http://$LOCAL_IP:$PROXY_PORT|" "$SERVICE_FILE"
        sed -i "s|ALL_PROXY=.*|Environment=ALL_PROXY=http://$LOCAL_IP:$PROXY_PORT|" "$SERVICE_FILE"
    else
        echo "      添加代理配置..."
        sed -i '/^\[Service\]/a\
Environment=HTTP_PROXY=http://'"$LOCAL_IP:$PROXY_PORT"'\
Environment=HTTPS_PROXY=http://'"$LOCAL_IP:$PROXY_PORT"'\
Environment=ALL_PROXY=http://'"$LOCAL_IP:$PROXY_PORT"'' "$SERVICE_FILE"
    fi
    echo "      完成"
else
    echo "      [警告] 未找到 systemd service 文件"
fi

# 7. 重新加载并重启
echo "[7/7] 重新加载 systemd 并重启 Gateway..."
systemctl --user daemon-reload 2>/dev/null || true
openclaw gateway restart

echo ""
echo "=== 修复完成 ==="
echo "代理地址: http://$LOCAL_IP:$PROXY_PORT"
echo ""
echo "验证连接:"
echo "  openclaw logs --follow | grep -i whatsapp"
