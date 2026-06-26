#!/bin/bash

echo "============================================================"
echo "  Universal AutoStart - 安装工具 (macOS) v1.1"
echo "============================================================"
echo ""

# 检查 sudo 权限
if [ "$EUID" -ne 0 ]; then 
    echo "[ERROR] 请使用 sudo 运行此脚本："
    echo "sudo ./install_macos.sh"
    exit 1
fi

echo "[OK] 管理员权限已获取"
echo ""

# 查找配置文件
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="$SCRIPT_DIR/qwenpaw_service_config.json"

if [ ! -f "$CONFIG_FILE" ]; then
    CONFIG_FILE="$SCRIPT_DIR/service_config.json"
fi

if [ ! -f "$CONFIG_FILE" ]; then
    echo "[ERROR] 配置文件不存在"
    echo "请确保 service_config.json 或 qwenpaw_service_config.json 在同一目录下"
    exit 1
fi

echo "[步骤] 正在安装服务..."
python3 "$SCRIPT_DIR/universal_service.py" install "$CONFIG_FILE"

if [ $? -eq 0 ]; then
    echo ""
    echo "============================================================"
    echo "  安装完成！"
    echo "============================================================"
    echo ""
    echo "下次开机将自动启动配置的程序"
    echo "如需卸载，请运行：sudo ./uninstall_macos.sh"
    echo ""
else
    echo ""
    echo "[ERROR] 安装失败！"
fi
