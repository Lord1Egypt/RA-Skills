#!/bin/bash
# 证券监管监控 - 便捷运行脚本
# 这是 skill 中的便捷脚本，调用实际的监控系统

echo "========================================"
echo "证券监管页面批量监控"
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

# 运行批量抓取
echo "▶️  开始运行批量监控..."
echo ""

cd "${MONITOR_DIR}/scripts" && bash crawl_all.sh

echo ""
echo "========================================"
echo "监控执行完成！"
echo "========================================"
echo ""
echo "💡 提示：运行 'check_notifications.sh' 查看是否有更新通知"
