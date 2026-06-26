#!/bin/bash
# qslazy 每日订阅状态汇报模板
# 用法:
#   bash scripts/daily_report.sh [星期几] [env路径]
#
# 参数：
#   星期几：可选。1=周一, 2=周二, ..., 7=周日；不传则自动使用当天。
#   env路径：可选。默认使用 ../.env，也可以传入 <skills-dir>/quark-lazy-cli/.env。
#
# 使用前请把下面 case 里的 剧名1/剧名2/剧名3 替换成你的 QAS 任务名。

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DEFAULT_ENV="$(cd "$SCRIPT_DIR/.." && pwd)/.env"
ENV="${2:-$DEFAULT_ENV}"

if [ -z "$1" ]; then
  DAY=$(date +%w)  # 0=周日, 1=周一...
else
  DAY="$1"
fi

run_status() {
  local task_name="$1"
  echo ""
  echo "================================================"
  echo "🔍 任务: '$task_name'"
  qslazy task status "$task_name" --env "$ENV"
}

echo "===== qslazy 每日订阅状态汇报 ====="
echo "使用配置：$ENV"

case "$DAY" in
  1)
    echo "📅 周一"
    run_status "剧名1"
    ;;
  2)
    echo "📅 周二"
    run_status "剧名2"
    ;;
  3)
    echo "📅 周三"
    run_status "剧名3"
    ;;
  4)
    echo "📅 周四"
    run_status "剧名4"
    ;;
  5)
    echo "📅 周五"
    run_status "剧名5"
    run_status "剧名6"
    ;;
  6)
    echo "📅 周六"
    run_status "剧名7"
    run_status "剧名8"
    ;;
  7|0)
    echo "📅 周日"
    run_status "剧名9"
    run_status "剧名10"
    ;;
  *)
    echo "参数错误：星期几必须是 1-7，或不传参数自动使用当天。"
    exit 1
    ;;
esac

echo ""
echo "===== 汇报完毕 ====="
