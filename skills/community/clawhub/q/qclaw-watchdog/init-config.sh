#!/bin/bash
# QClaw Watchdog 配置生成工具 / Config Generator Tool

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CONFIG_FILE="$SCRIPT_DIR/config.json"

# 检查配置文件是否存在 / Check if config exists
if [ -f "$CONFIG_FILE" ]; then
    echo "配置文件已存在: $CONFIG_FILE"
    echo "Config file already exists: $CONFIG_FILE"
    echo ""
    echo "如需重新生成配置，请先备份并删除现有配置"
    echo "To regenerate config, please backup and delete existing config first"
    exit 0
fi

# 创建默认配置 / Create default config
cat > "$CONFIG_FILE" << 'EOF'
{
  "feishu": {
    "app_id": "YOUR_APP_ID",
    "app_secret": "YOUR_APP_SECRET",
    "user_id": "YOUR_USER_OPEN_ID"
  },
  "qclaw": {
    "health_url": "http://127.0.0.1:28789/health"
  },
  "watchdog": {
    "check_interval_ms": 180000,
    "restart_delay_ms": 10000,
    "max_retries": 3
  },
  "logs": {
    "main_log": "./watchdog.log",
    "command_log": "./commands.log"
  }
}
EOF

echo "✅ 默认配置文件已创建: $CONFIG_FILE"
echo "✅ Default config created: $CONFIG_FILE"
echo ""
echo "请编辑配置文件，填入你的飞书应用信息"
echo "Please edit the config file and fill in your Feishu app info"
