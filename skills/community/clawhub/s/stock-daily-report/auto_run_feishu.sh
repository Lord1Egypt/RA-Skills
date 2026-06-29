#!/bin/bash
# A 股每日投资报告 Pro - 自动运行并推送到飞书
# 执行时间：每个交易日 9:25（集合竞价后，开盘前）

# ============ 环境配置 ============
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="/tmp/stock-report-pro.log"
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
DATE_STR=$(date +%Y%m%d)

# 加载配置文件
CONFIG_FILE="$SCRIPT_DIR/config.json"
if [ -f "$CONFIG_FILE" ]; then
    OUTPUT_DIR=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE')).get('output_dir', '/tmp'))" 2>/dev/null)
    REPORT_PREFIX=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE')).get('report_prefix', 'stock-report'))" 2>/dev/null)
else
    OUTPUT_DIR="/tmp"
    REPORT_PREFIX="stock-report"
fi

# 输出文件路径
IMAGE_FILE="${OUTPUT_DIR}/${REPORT_PREFIX}-${DATE_STR}.png"
HTML_FILE="${OUTPUT_DIR}/${REPORT_PREFIX}-${DATE_STR}.html"

# ============ 日志记录 ============
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> $LOG_FILE
    echo "$1"
}

log "========================================"
log "执行时间：$TIMESTAMP"
log "脚本目录：$SCRIPT_DIR"
log "输出目录：$OUTPUT_DIR"
log "========================================"

# ============ 生成报告 ============
log "📊 正在生成报告..."

cd "$SCRIPT_DIR"
export PATH="$HOME/.local/share/pnpm:$PATH"
export PYTHONIOENCODING="utf-8"

python3 generate_report.py --format both --output "${OUTPUT_DIR}/${REPORT_PREFIX}-${DATE_STR}" >> $LOG_FILE 2>&1

if [ $? -eq 0 ]; then
    log "✅ 报告生成成功"
    
    # 检查生成的文件
    if [ -f "$IMAGE_FILE" ]; then
        log "📷 图片文件：$IMAGE_FILE ($(du -h "$IMAGE_FILE" | cut -f1))"
    else
        log "⚠️ 图片文件未生成：$IMAGE_FILE"
        # 尝试查找实际生成的文件
        ACTUAL_IMAGE=$(ls -t ${OUTPUT_DIR}/${REPORT_PREFIX}-*.png 2>/dev/null | head -1)
        if [ -n "$ACTUAL_IMAGE" ]; then
            log "✅ 找到实际文件：$ACTUAL_IMAGE"
            IMAGE_FILE="$ACTUAL_IMAGE"
        fi
    fi
    
    if [ -f "$HTML_FILE" ]; then
        log "🌐 HTML 文件：$HTML_FILE ($(du -h "$HTML_FILE" | cut -f1))"
    fi
else
    log "❌ 报告生成失败"
    exit 1
fi

# ============ 推送到飞书 ============
if [ -f "$IMAGE_FILE" ]; then
    log "📤 推送到飞书..."
    
    # 从配置文件读取 target
    TARGET_USER=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE')).get('feishu', {}).get('target_user', ''))" 2>/dev/null)
    
    if [ -n "$TARGET_USER" ]; then
        # 使用 openclaw message send 推送（必须指定 channel 和 account）
        RESULT=$(openclaw message send --channel feishu --account team --target "$TARGET_USER" --media "$IMAGE_FILE" -m "📈 A 股每日投资报告 - $(date +%Y年%m月%d日)" 2>&1)
        if echo "$RESULT" | grep -q "Sent via Feishu\|Message ID"; then
            log "✅ 飞书推送成功"
        else
            log "❌ 飞书推送失败：$RESULT"
        fi
    else
        log "⚠️ 未配置 target_user，跳过推送"
    fi
else
    log "⚠️ 图片文件不存在，跳过推送：$IMAGE_FILE"
fi

log "========================================"
log ""
