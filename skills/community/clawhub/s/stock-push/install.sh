#!/bin/bash
# =========================================================
# stock-push 一键安装脚本（单机版）
# 用法: bash <(curl -sL <url-to-this-script>) 
#   或直接: bash install_stock_push.sh
# =========================================================
set -e

SKILL_DIR="/root/.openclaw/workspace/skills/stock-push"
CRON_FILE="/etc/cron.d/stock-monitor"
LOGROTATE_FILE="/etc/logrotate.d/stock-monitor"

echo "📦 开始安装 A股股票定时推送..."

# 1. 安装 openclaw skill（支持 clawhub 的设备直接用）
if command -v clawhub &>/dev/null; then
    echo "  🔧 检测到 clawhub，尝试安装..."
    if clawhub install stock-push --force 2>/dev/null; then
        echo "  ✅ clawhub 安装成功"
    else
        echo "  ⚠️ clawhub 安装失败，改用手动解压"
    fi
fi

# 2. 如果 skill 目录不存在，从 .skill 文件安装
if [ ! -d "$SKILL_DIR" ]; then
    echo "  📂 skill 目录不存在，正在创建..."
    mkdir -p "$(dirname $SKILL_DIR)"
    
    # 找 .skill 文件
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    SKILL_FILE=""
    for f in "$SCRIPT_DIR/stock-push.skill" /tmp/stock-push.skill /root/.openclaw/workspace/stock-push.skill; do
        if [ -f "$f" ]; then SKILL_FILE="$f"; break; fi
    done
    
    if [ -z "$SKILL_FILE" ]; then
        echo "  ❌ 未找到 stock-push.skill 文件"
        echo "  请将 stock-push.skill 放到以下位置之一："
        echo "    - $SCRIPT_DIR/"
        echo "    - /tmp/"
        echo "    - /root/.openclaw/workspace/"
        exit 1
    fi
    
    echo "  📦 解压 $SKILL_FILE..."
    cd /tmp && unzip -o "$SKILL_FILE" -d stock-push-extract
    cp -r /tmp/stock-push-extract/stock-push "$SKILL_DIR"
fi

# 3. 写 cron
echo "  ⏰ 配置 cron..."
cat > "$CRON_FILE" << 'CRONEOF'
SHELL=/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

# 股票推送 cron（系统级，不依赖 Gateway）

# 盘前推荐：9:20（周一~五）
20 9 * * 1-5 root python3 /root/.openclaw/workspace/skills/stock-push/scripts/stock_pre.py >> /tmp/stock_pre.log 2>&1

# 收盘复盘：15:05（周一~五）
5 15 * * 1-5 root python3 /root/.openclaw/workspace/skills/stock-push/scripts/stock_after.py >> /tmp/stock_after.log 2>&1

# 次日关注：20:00（周一~四）
0 20 * * 1-4 root python3 /root/.openclaw/workspace/skills/stock-push/scripts/stock_next.py >> /tmp/stock_next.log 2>&1
CRONEOF
chmod 644 "$CRON_FILE"
echo "  ✅ cron 已写入 $CRON_FILE"

# 4. 写 logrotate
echo "  🔄 配置 logrotate..."
cat > "$LOGROTATE_FILE" << 'LOGEOF'
/tmp/stock_pre.log /tmp/stock_after.log /tmp/stock_next.log {
    daily
    rotate 7
    compress
    delaycompress
    notifempty
    missingok
    create 0644 root root
}
LOGEOF
echo "  ✅ logrotate 已写入 $LOGROTATE_FILE"

# 5. 重启 cron
if command -v systemctl &>/dev/null; then
    systemctl restart cron 2>/dev/null && echo "  ✅ cron 服务已重启" || echo "  ⚠️ 无法重启 cron，请手动 restart"
fi

# 6. 验证语法
echo "  🔍 验证脚本语法..."
for script in stock_pre.py stock_after.py stock_next.py; do
    path="$SKILL_DIR/scripts/$script"
    if [ -f "$path" ]; then
        python3 -m py_compile "$path" 2>/dev/null && echo "  ✅ $script OK" || echo "  ❌ $script 语法错误"
    fi
done

echo ""
echo "=================================================="
echo "✅ 安装完成！"
echo ""
echo "⚠️  安装后需修改配置："
echo "  $SKILL_DIR/scripts/stock_pre.py"
echo "  $SKILL_DIR/scripts/stock_after.py"
echo "  $SKILL_DIR/scripts/stock_next.py"
echo ""
echo "  修改内容："
echo "  1. USER_ID → 你的微信用户 ID"
echo "  2. HOLDINGS / WATCH_LIST → 你的持仓"
echo ""
echo "测试发送："
echo '  openclaw message send --channel openclaw-weixin --target <USER_ID> --message "测试"'
echo ""
echo "查看日志："
echo "  tail -f /tmp/stock_pre.log"
echo "=================================================="
