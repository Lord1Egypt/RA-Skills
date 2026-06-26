#!/bin/bash

echo "============================================================"
echo "  Universal AutoStart - 卸载工具 (macOS) v1.1"
echo "============================================================"
echo ""

# 检查 sudo 权限
if [ "$EUID" -ne 0 ]; then 
    echo "[ERROR] 请使用 sudo 运行此脚本："
    echo "sudo ./uninstall_macos.sh"
    exit 1
fi

echo "[OK] 管理员权限已获取"
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

python3 "$SCRIPT_DIR/universal_service.py" uninstall

if [ $? -eq 0 ]; then
    echo ""
    echo "============================================================"
    echo "  卸载完成！"
    echo "============================================================"
else
    echo ""
    echo "[ERROR] 卸载失败！"
fi
