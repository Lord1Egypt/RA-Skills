#!/bin/bash
# cross-agent-config - 配置默认参数

CONFIG_DIR="${HOME}/.config/openclaw"
CONFIG_FILE="${CONFIG_DIR}/cross-agent.conf"

# 确保配置目录存在
mkdir -p "$CONFIG_DIR"

# 显示当前配置
show_config() {
    echo "📋 当前配置:"
    if [ -f "$CONFIG_FILE" ]; then
        cat "$CONFIG_FILE"
    else
        echo "  (无配置)"
    fi
}

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --default-user)
            echo "default_user=$2" >> "$CONFIG_FILE"
            echo "✅ 设置默认用户: $2"
            shift 2
            ;;
        --default-pass)
            echo "default_pass=$2" >> "$CONFIG_FILE"
            echo "✅ 设置默认密码: ***"
            shift 2
            ;;
        --default-ip)
            echo "default_ip=$2" >> "$CONFIG_FILE"
            echo "✅ 设置默认IP: $2"
            shift 2
            ;;
        --show)
            show_config
            exit 0
            ;;
        --clear)
            rm -f "$CONFIG_FILE"
            echo "✅ 配置已清除"
            exit 0
            ;;
        *)
            echo "❌ 未知参数: $1"
            echo "用法: openclaw cross-agent config [选项]"
            echo ""
            echo "选项:"
            echo "  --default-user USER    设置默认用户名"
            echo "  --default-pass PASS    设置默认密码"
            echo "  --default-ip IP        设置默认IP地址"
            echo "  --show                 显示当前配置"
            echo "  --clear                清除所有配置"
            exit 1
            ;;
    esac
done

# 去重配置
if [ -f "$CONFIG_FILE" ]; then
    sort -u "$CONFIG_FILE" > "${CONFIG_FILE}.tmp"
    mv "${CONFIG_FILE}.tmp" "$CONFIG_FILE"
fi

echo ""
show_config