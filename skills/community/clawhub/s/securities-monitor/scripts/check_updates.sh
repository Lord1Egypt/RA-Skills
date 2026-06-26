#!/bin/bash
# 证券监管监控 - 检查更新脚本
# 这是 skill 中的便捷脚本，调用实际的检查脚本

echo "========================================"
echo "检查证券监管页面更新"
echo "========================================"
echo ""

# 检查实际的监控系统是否存在
MONITOR_DIR="/root/monitoring/securities"

if [ ! -d "${MONITOR_DIR}" ]; then
  echo "❌ 错误: 监控系统目录不存在: ${MONITOR_DIR}"
  echo ""
  echo "请先确保监控系统已正确安装。"
  exit 1
fi

# 运行检查脚本
cd "${MONITOR_DIR}/scripts" && bash check_notifications.sh
