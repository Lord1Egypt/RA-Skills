#!/bin/bash

# 安全点对点加密通讯技能安装脚本

set -e

echo "🔒 安装安全点对点加密通讯技能..."
echo "================================"

# 检查依赖
echo "📦 检查系统依赖..."
for cmd in bash openssl jq base64; do
    if ! command -v $cmd &> /dev/null; then
        echo "❌ 缺少依赖: $cmd"
        echo "   请安装: sudo apt-get install $cmd  # Debian/Ubuntu"
        echo "   或: brew install $cmd             # macOS"
        exit 1
    fi
done

echo "✅ 所有依赖已安装"

# 创建配置目录
CONFIG_DIR="$HOME/.openclaw/secure-p2p"
KEYRING_DIR="$CONFIG_DIR/keyring"
LOG_DIR="$CONFIG_DIR/logs"

echo "📁 创建配置目录..."
mkdir -p "$KEYRING_DIR" "$LOG_DIR"

# 设置权限
chmod 700 "$KEYRING_DIR"

# 复制脚本文件
echo "📋 安装脚本文件..."
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 使脚本可执行
chmod +x "$SCRIPT_DIR"/*.sh 2>/dev/null || true

# 创建符号链接（可选）
if [ "$1" = "--link" ]; then
    echo "🔗 创建全局符号链接..."
    sudo ln -sf "$SCRIPT_DIR/secure-messenger.sh" /usr/local/bin/secure-messenger 2>/dev/null || true
fi

# 创建默认配置
echo "⚙️ 创建默认配置..."
cat > "$CONFIG_DIR/config.json" << 'EOF'
{
  "version": "1.0.0",
  "key_size": 2048,
  "encryption": {
    "algorithm": "aes-256-gcm",
    "key_derivation_iterations": 100000
  },
  "security": {
    "max_message_size": 10485760,
    "max_file_size": 104857600,
    "key_rotation_days": 180
  },
  "logging": {
    "level": "INFO",
    "max_log_size": 10485760,
    "backup_count": 5
  }
}
EOF

# 创建环境文件
echo "🌍 设置环境变量..."
cat > "$CONFIG_DIR/.env" << 'EOF'
# 安全点对点加密通讯配置
export SECURE_P2P_HOME="$HOME/.openclaw/secure-p2p"
export SECURE_P2P_KEYRING="$SECURE_P2P_HOME/keyring"
export SECURE_P2P_LOGS="$SECURE_P2P_HOME/logs"
export SECURE_P2P_DEBUG=0
EOF

echo ""
echo "✅ 安装完成!"
echo ""
echo "📋 安装摘要:"
echo "  - 配置目录: $CONFIG_DIR"
echo "  - 密钥存储: $KEYRING_DIR"
echo "  - 日志目录: $LOG_DIR"
echo ""
echo "🚀 下一步:"
echo "  1. 初始化身份: ./secure-messenger.sh init"
echo "  2. 查看身份: ./secure-messenger.sh identity"
echo "  3. 添加联系人: ./secure-messenger.sh add-contact"
echo ""
echo "📚 详细文档请查看 SKILL.md"
echo "================================"