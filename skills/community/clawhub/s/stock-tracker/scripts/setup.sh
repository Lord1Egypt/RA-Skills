#!/usr/bin/env bash
#
# stock-tracker 环境自动配置脚本
# 用法: bash scripts/setup.sh
#
# 功能:
#   1. 安装 Python 依赖（含 Playwright）
#   2. 创建必要目录 (logs, state)
#   3. 提示配置 cookie.txt、.env、config.json
#   4. 设置 crontab 定时任务（每天 9:00 和 15:00）
#

set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SCRIPT_DIR="$SKILL_DIR/scripts"
PYTHON="${PYTHON:-python3}"

echo "========================================"
echo " Stock Tracker - 环境配置脚本"
echo "========================================"

# 1. 安装依赖
echo ""
echo "[1/5] 安装 Python 依赖..."
if command -v pip3 &>/dev/null; then
    pip3 install requests pdfplumber
elif command -v pip &>/dev/null; then
    pip install requests pdfplumber
else
    echo "错误: 未找到 pip/pip3，请先安装 Python 包管理器。"
    exit 1
fi

# 可选安装 Playwright（Cookie 自动续签用）
echo ""
echo "[2/5] 安装 Playwright（可选，Cookie 自动续签用）..."
if command -v pip3 &>/dev/null; then
    pip3 install playwright 2>/dev/null && python3 -m playwright install chromium 2>/dev/null && echo "  [OK] Playwright 安装完成" || echo "  [跳过] Playwright 未安装（不影响核心功能）"
elif command -v pip &>/dev/null; then
    pip install playwright 2>/dev/null && python3 -m playwright install chromium 2>/dev/null && echo "  [OK] Playwright 安装完成" || echo "  [跳过] Playwright 未安装（不影响核心功能）"
fi

# 2. 创建目录
echo ""
echo "[3/5] 创建必要目录..."
mkdir -p "$SKILL_DIR/logs"
STATE_DIR="$SKILL_DIR/.stock-tracker-state"
mkdir -p "$STATE_DIR"
echo "  日志目录: $SKILL_DIR/logs"
echo "  状态目录: $STATE_DIR"

# 3. 检查配置
echo ""
echo "[4/5] 检查配置..."

# cookie.txt
if [ ! -f "$SKILL_DIR/cookie.txt" ]; then
    echo "  [提示] cookie.txt 不存在。"
    echo "  请登录东方财富网页版后，按 F12 → Console → copy(document.cookie) 到:"
    echo "    $SKILL_DIR/cookie.txt"
    echo ""
else
    echo "  [OK] cookie.txt 已存在"
fi

# .env（LLM API Key）
if [ ! -f "$SKILL_DIR/.env" ]; then
    echo "  [提示] .env 不存在，正在创建空白模板..."
    echo "# Stock Tracker LLM 配置" > "$SKILL_DIR/.env"
    echo "# 从 https://platform.openai.com/api-keys 获取" >> "$SKILL_DIR/.env"
    echo "LLM_API_KEY=" >> "$SKILL_DIR/.env"
    echo "  已创建: $SKILL_DIR/.env（如需 LLM 筛选功能，请填入 API Key）"
else
    echo "  [OK] .env 已存在"
fi

# config.json
if [ ! -f "$SKILL_DIR/config.json" ]; then
    echo "  [提示] config.json 不存在，创建默认配置..."
    cat > "$SKILL_DIR/config.json" << 'CONFIGEOF'
{
  "notify": {
    "type": "terminal",
    "webhook_url": ""
  },
  "fetch_interval_days": 7,
  "stocks": [],
  "llm": {
    "enabled": true,
    "base_url": "https://api.openai.com/v1",
    "model": "gpt-4o-mini",
    "timeout": 15,
    "retries": 2
  }
}
CONFIGEOF
    echo "  已创建: $SKILL_DIR/config.json"
else
    echo "  [OK] config.json 已存在"
fi

# 4. 设置 crontab
echo ""
echo "[5/5] 设置定时任务（每天 9:00 和 15:00 北京时间）..."
CRON_CMD_1="0 1 * * * cd $SKILL_DIR && $PYTHON $SCRIPT_DIR/stock_tracker.py --source cninfo --group 持仓 --days 15 --fetch-content >> $SKILL_DIR/logs/stock_tracker.log 2>&1"
CRON_CMD_2="0 7 * * * cd $SKILL_DIR && $PYTHON $SCRIPT_DIR/stock_tracker.py --source cninfo --group 持仓 --days 15 --fetch-content >> $SKILL_DIR/logs/stock_tracker.log 2>&1"

EXISTING=$(crontab -l 2>/dev/null || true)

if echo "$EXISTING" | grep -qF "$SCRIPT_DIR/stock_tracker.py"; then
    echo "  [OK] 定时任务已存在，跳过。如需更新请手动编辑 crontab。"
else
    (
        echo "$EXISTING"
        echo "# stock-tracker: 东方财富自选股公告追踪 (北京时间 9:00)"
        echo "$CRON_CMD_1"
        echo "# stock-tracker: 东方财富自选股公告追踪 (北京时间 15:00)"
        echo "$CRON_CMD_2"
    ) | crontab -
    echo "  [OK] 定时任务已添加！"
    echo "  运行时间: 每天北京时间 09:00 和 15:00"
fi

echo ""
echo "========================================"
echo " 配置完成！"
echo "========================================"
echo ""
echo "下一步:"
echo "  1. 将东方财富 Cookie 写入 $SKILL_DIR/cookie.txt"
echo "  2. （可选）在 $SKILL_DIR/.env 中配置 LLM_API_KEY 开启 AI 筛选"
echo "  3. 完整运行测试:"
echo "     cd $SKILL_DIR && $PYTHON $SCRIPT_DIR/stock_tracker.py --source cninfo --group 持仓 --days 15 --fetch-content"
echo "  4. 查看运行日志:"
echo "     tail -f $SKILL_DIR/logs/stock_tracker_*.log"
echo ""
