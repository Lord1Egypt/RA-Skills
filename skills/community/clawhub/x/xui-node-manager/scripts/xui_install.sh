#!/bin/bash
# ============================================================
# 3x-ui 面板自动安装脚本
# 用法: ./xui_install.sh <ip> <ssh_port> <username> <password>
# ============================================================

set -euo pipefail

if [ $# -ne 4 ]; then
    echo "用法: $0 <ip> <ssh_port> <username> <password>"
    exit 1
fi

SSH_IP="$1"
SSH_PORT="$2"
SSH_USER="$3"
SSH_PASS="$4"

SPOOL=$(mktemp)
EXPECT_SCRIPT=$(mktemp)
trap 'rm -f "$SPOOL" "$EXPECT_SCRIPT"' EXIT

export SSHPASS="$SSH_PASS"

# 生成 expect 脚本
cat > "$EXPECT_SCRIPT" << 'EXPEOF'
set timeout 600
set ip [lindex $argv 0]
set port [lindex $argv 1]
set user [lindex $argv 2]
set pass [lindex $argv 3]

spawn sshpass -e ssh -o StrictHostKeyChecking=no -p $port $user@$ip

expect {
    "password:" { send "\r"; exp_continue }
    "Are you sure" { send "y\r"; exp_continue }
    "continue connecting" { send "yes\r"; exp_continue }
    "~#" { send "bash <(curl -Ls https://raw.githubusercontent.com/mhsanaei/3x-ui/master/install.sh)\r" }
    "$ " { send "bash <(curl -Ls https://raw.githubusercontent.com/mhsanaei/3x-ui/master/install.sh)\r" }
    timeout { puts "ERROR: SSH connection timeout"; exit 1 }
}

expect {
    -re {Enter (y/n|Y/n)} { send "\r"; exp_continue }
    -re {选择|Select} { send "\r"; exp_continue }
    -re {自定义|Custom} { send "\r"; exp_continue }
    -re {请输入|请输入端口|Port} { send "\r"; exp_continue }
    -re {WebBasePath|web base path|web_path} { send "\r"; exp_continue }
    -re {Username|用户名} { send "\r"; exp_continue }
    -re {Password|密码} { send "\r"; exp_continue }
    -re {确定|确认|Continue|Yes|yes/no} { send "\r"; exp_continue }
    -re {是否|\[y/N\]|\[Y/n\]} { send "\r"; exp_continue }
    -re {Press any key} { send "\r"; exp_continue }
    -re {Panel Installation Complete} { }
    timeout { puts "ERROR: Install script timed out"; exit 1 }
}

sleep 3
send "exit\r"
expect eof
EXPEOF

echo "🛜  正在连接 $SSH_USER@$SSH_IP:$SSH_PORT ..."
echo "📦 安装 3x-ui，过程较长，自动按默认选项确认 ..."
echo ""

# 运行 expect 脚本
expect "$EXPECT_SCRIPT" "$SSH_IP" "$SSH_PORT" "$SSH_USER" "$SSH_PASS" 2>&1 | tee "$SPOOL"

echo ""
echo "═══════════════════════════════════════════"
echo " 提取面板信息中..."
echo "═══════════════════════════════════════════"

# 去除 ANSI 转义码，再提取信息
CLEAN=$(perl -pe 's/\e\[[0-9;]*[a-zA-Z]//g' "$SPOOL" 2>/dev/null || cat "$SPOOL")
USERNAME=$(echo "$CLEAN" | grep -oP 'Username:\s*\K.*' | head -1 | tr -d '[:space:]')
PASSWORD=$(echo "$CLEAN" | grep -oP 'Password:\s*\K.*' | head -1 | tr -d '[:space:]')
PORT=$(echo "$CLEAN" | grep -oP 'Port:\s*\K.*' | head -1 | tr -d '[:space:]')
WEBPATH=$(echo "$CLEAN" | grep -oP 'WebBasePath:\s*\K.*' | head -1 | tr -d '[:space:]')
ACCESS_URL=$(echo "$CLEAN" | grep -oP 'Access URL:\s*\K.*' | head -1 | tr -d '[:space:]')
API_TOKEN=$(echo "$CLEAN" | grep -oP 'API Token:\s*\K.*' | head -1 | tr -d '[:space:]')

# 检测 SSL 是否失败 -> 改用 http
SSL_FAILED=$(echo "$CLEAN" | grep -i -c 'certificate setup failed\|Failed to issue' || true)
if [ "$SSL_FAILED" -gt 0 ]; then
    ACCESS_URL=$(echo "$ACCESS_URL" | sed 's|^https://|http://|')
    echo "  ⚠️  SSL 证书申请失败，面板使用 HTTP"
fi

# 去除 URL 尾部斜杠（避免拼接 login 时产生 //login）
ACCESS_URL=$(echo "$ACCESS_URL" | sed 's|/$||')

if [ -z "$ACCESS_URL" ]; then
    echo ""
    echo "  ❌ 未能提取到面板信息。请检查完整输出。"
    echo "     可能在面板安装过程中有错误。"
    echo ""
    echo "完整输出:"
    cat "$SPOOL"
    exit 1
fi

echo ""
echo "  ✅ 面板安装成功！"
echo "  ─────────────────────────────"
echo "  📍 URL:    $ACCESS_URL"
echo "  👤 用户:   $USERNAME"
echo "  🔑 密码:   $PASSWORD"
echo "  🚪 端口:   $PORT"
echo "  📁 路径:   $WEBPATH"
[ -n "$API_TOKEN" ] && echo "  🎫 Token:  $API_TOKEN"
echo ""

# 输出 JSON 方便解析
echo "--- JSON ---"
echo "{\"access_url\":\"$ACCESS_URL\",\"username\":\"$USERNAME\",\"password\":\"$PASSWORD\",\"port\":\"$PORT\",\"webpath\":\"$WEBPATH\",\"api_token\":\"$API_TOKEN\"}"
echo "--- END ---"
