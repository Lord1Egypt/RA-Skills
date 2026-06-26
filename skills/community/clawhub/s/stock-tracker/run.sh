#!/bin/bash
# stock_tracker 每日运行脚本
# 用法: bash run.sh [group] [days] [source]
# 示例: bash run.sh mygroup 15 eastmoney
#        bash run.sh test 15 cninfo
#
# 设计原则（对齐 bilibili-auto-transcript）：
#   - 所有日志/状态信息走 stderr（agent 不需要解析）
#   - 只有 digest 结果走 stdout（agent 读取转发）
#   - 失败时输出 ERROR: 标签到 stdout（agent 可靠识别）

cd "$(dirname "$0")"

GROUP="${1:-持仓}"
DAYS="${2:-15}"
SOURCE="${3:-eastmoney}"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >&2
}

log "=== 开始运行 ==="
log "分组: $GROUP, 天数: $DAYS, 数据源: $SOURCE"

# 第零步：检查 Cookie 有效性，过期则自动续签
log "检查 Cookie..."
if python3 scripts/refresh_cookie.py 2>/dev/null; then
    log "Cookie 有效"
else
    log "Cookie 无效或自动续签失败，尝试继续运行（API 调用时会验证）..."
fi

# 第一步：抓取 + 过滤 + 入库
log "抓取公告..."
if ! python3 scripts/stock_tracker.py --group "$GROUP" --source "$SOURCE" --days "$DAYS" --fetch-content 2>/dev/null; then
    echo "ERROR:公告抓取失败（group=$GROUP source=$SOURCE days=$DAYS）"
    exit 1
fi

# 第二步：生成单条公告摘要 + 输出 digest
log "生成摘要..."
if ! python3 scripts/daily_summary.py --group "$GROUP" --digest 2>/dev/null; then
    echo "ERROR:摘要生成失败"
    exit 1
fi

log "=== 运行完成 ==="
