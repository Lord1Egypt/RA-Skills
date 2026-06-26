#!/bin/bash
#
# 财报日历数据获取脚本
# 方案: Chrome Extension + Native Messaging
#
# 用法:
#   ./scripts/get-company-list.sh [日期]
#
# 参数:
#   日期       YYYY-MM-DD 格式，默认今天
#
# 示例:
#   ./scripts/get-company-list.sh                # 获取今天数据
#   ./scripts/get-company-list.sh 2026-03-14     # 获取指定日期
#
# 成功: stdout 输出 JSON 数组，每项固定字段：code、earningType、marketCap（纯数字）
# 失败: stderr 输出错误，退出非 0
#
# 前置条件:
#   - Chrome 已启动，Today Earnings 扩展已加载
#   - Native Host 已安装: ./native-host/install.sh <扩展ID>

set -euo pipefail

DATE=""

for arg in "$@"; do
  if [[ "$arg" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
    DATE="$arg"
  fi
done

DATE="${DATE:-$(date +%Y-%m-%d)}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLI="$SCRIPT_DIR/get-company-list.mjs"

exec node "$CLI" "$DATE"
