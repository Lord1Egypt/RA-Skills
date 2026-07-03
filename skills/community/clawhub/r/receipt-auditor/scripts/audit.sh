#!/usr/bin/env bash
# =============================================================================
#  Receipt & Expense Auditor — CLI Entrypoint
#  Three modes: report, aa-split, audit
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

# ── Defaults ────────────────────────────────────────────────────────────────
MODE="report"
ITEMS=""
ITEMS_FILE=""
CURRENCY="CNY"
LANGUAGE="zh"

# ── Usage ───────────────────────────────────────────────────────────────────
usage() {
    cat << 'USAGE'
receipt-auditor — Extract, categorize, and audit receipts and bills.

Usage:
  receipt-auditor --mode report [--items "line1\nline2"] [--currency CNY] [--lang zh]
  receipt-auditor --mode aa-split [--aa-config path/to/config.json]
  receipt-auditor --mode audit  [--items "line1\nline2"]

Modes:
  report      Categorize expenses and generate a reimbursement report
  aa-split    Calculate per-person splits for group dining/travel
  audit       Detect duplicate or suspicious charges in a bill

Options:
  --mode      <str>    Mode: report | aa-split | audit (default: report)
  --items     <str>    Raw bill text (one item per line)
  --file      <path>   Read items from a file instead of --items
  --currency  <str>    Currency code (default: CNY)
  --lang      <str>    Output language: zh | en (default: zh)
  --aa-config <path>   JSON config file for AA split details
  --help               Show this help

First-Success Path (30 seconds):
  receipt-auditor --mode report --items "6/1 北京-上海高铁 553元"

Examples:
  receipt-auditor --mode report --file my-trip.txt
  receipt-auditor --mode aa-split --aa-config config.json
  receipt-auditor --mode audit --items "6/1 超市 128.50&#10;6/1 超市 128.50"
USAGE
}

# ── Parse Args ──────────────────────────────────────────────────────────────
AA_CONFIG=""
while [[ $# -gt 0 ]]; do
    case "$1" in
        --mode)  MODE="$2";   shift 2 ;;
        --items) ITEMS="$2";  shift 2 ;;
        --file)  ITEMS_FILE="$2"; shift 2 ;;
        --currency) CURRENCY="$2"; shift 2 ;;
        --lang)  LANGUAGE="$2"; shift 2 ;;
        --aa-config) AA_CONFIG="$2"; shift 2 ;;
        --help|-h) usage; exit 0 ;;
        *) echo "❌ Unknown option: $1"; usage; exit 1 ;;
    esac
done

# ── Validate Mode ───────────────────────────────────────────────────────────
case "$MODE" in
    report|aa-split|audit) ;;
    *) echo "❌ Unknown mode: $MODE. Must be: report, aa-split, audit"; exit 1 ;;
esac

# ── Print context for AI ────────────────────────────────────────────────────
echo "🧾  Receipt & Expense Auditor"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Mode:     $MODE"
echo "  Currency: $CURRENCY"
echo ""

BUILD_PROMPT() {
    case "$MODE" in
        report)
            echo "请作为账单报销小助手，根据以下消费记录生成报销单。"
            echo ""
            echo "要求："
            echo "1. 按日期逐条列出（日期、类别、金额、备注）"
            echo "2. 按类别汇总（交通、住宿、餐饮、办公、其他）"
            echo "3. 检测以下异常：同一商家同一日相同金额、金额明显偏高、缺失摘要信息"
            echo "4. 输出合计金额"
            echo "5. 使用标准表格"
            echo ""
            echo "币种：${CURRENCY}"
            echo ""
            echo "消费记录："
            if [[ -n "$ITEMS" ]]; then
                echo "$ITEMS"
            fi
            if [[ -n "$ITEMS_FILE" && -f "$ITEMS_FILE" ]]; then
                echo "# (来自文件: $ITEMS_FILE)"
                cat "$ITEMS_FILE"
            fi
            ;;

        aa-split)
            echo "请作为账单AA分摊计算器，根据以下信息计算每人应付金额。"
            echo ""
            echo "要求："
            echo "1. 提取公共部分金额（所有共享项目）"
            echo "2. 公共部分按人数均分"
            echo "3. 每人应付 = 个人点单 + 公共分摊"
            echo "4. 验证合计 = 总金额"
            echo "5. 输出表格（人员、个人点单、公共分摊、应付）"
            echo ""

            if [[ -n "$AA_CONFIG" && -f "$AA_CONFIG" ]]; then
                echo "AA 配置 (from JSON):"
                cat "$AA_CONFIG"
            else
                echo "请在输入中提供：总金额、人数、各人点单明细、公共项目"
            fi
            ;;

        audit)
            echo "请作为账单异常检查助手，根据以下消费记录进行检查。"
            echo ""
            echo "要求："
            echo "1. 逐条列出（日期、商家、金额、状态）"
            echo "2. 标出重复消费（同一日期、同一商家、相同金额）"
            echo "3. 标出金额异常（超出消费习惯均值2倍以上）"
            echo "4. 输出异常提醒列表"
            echo "5. 计算月总支出"
            echo ""
            echo "消费记录："
            if [[ -n "$ITEMS" ]]; then
                echo "$ITEMS"
            fi
            if [[ -n "$ITEMS_FILE" && -f "$ITEMS_FILE" ]]; then
                echo "# (来自文件: $ITEMS_FILE)"
                cat "$ITEMS_FILE"
            fi
            ;;
    esac
}

BUILD_PROMPT

# Save prompt for reference
PROMPT_FILE="${SKILL_DIR}/references/last-prompt.txt"
mkdir -p "$(dirname "$PROMPT_FILE")"
BUILD_PROMPT > "$PROMPT_FILE"
echo ""
echo "📎  AI prompt saved to: $PROMPT_FILE"
echo ""
echo "ℹ️   Paste the prompt above into your AI assistant to get the full audit report."
echo "   Or use this skill directly — the assistant will process it for you."
echo ""
echo "📘  First-Success Path:"
echo "   receipt-auditor --mode report --items \"6/1 北京-上海高铁 553元\""
echo ""
echo "✨  Happy auditing!"
