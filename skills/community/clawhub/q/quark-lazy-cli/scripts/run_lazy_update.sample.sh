#!/bin/bash

# ============================================================
# QasLazyCli 自动化更新脚本
# 用法: ./run_lazy_update.sh [mode] [task_name]
# 示例: ./run_lazy_update.sh new 百炼成神
# ============================================================

# 1. 命令行参数解析
if [ "$#" -lt 2 ]; then
    echo "❌ 错误: 参数缺失。"
    echo "用法: $0 [new|all] [任务名称]"
    exit 1
fi

MODE=$1
TASK_NAME=$2

# 2. 核心路径定义
BIN_PATH="/home/chenli/.local/bin/qas_lazy_cli"
ENV_FILE="/home/chenli/.openclaw/workspace-recruiter/skills/qas-lazy-cli/.env"
BASE_DIR="/home/chenli/.openclaw/workspace-recruiter/skills/qas-lazy-cli"
CRON_LOG="/home/chenli/qas_cron.log"

# 3. 加载 .env 环境变量
# 使用 set -a 让 source 的变量自动 export 给子进程
if [ -f "$ENV_FILE" ]; then
    set -a
    source "$ENV_FILE"
    set +a
else
    echo "⚠️ 警告: 未找到 .env 文件 ($ENV_FILE)" >> "$CRON_LOG"
fi

# 4. 目录自动准备
# 如果你的 .env 里定义了这些变量，下方代码将确保物理目录存在
mkdir -p "${LAZY_CLI_LOG_DIR:-$BASE_DIR/logs}"
mkdir -p "${LAZY_CLI_REPORT_DIR:-$BASE_DIR/report}"

# 5. 特殊任务逻辑 (覆盖 .env 中的默认值)
# 这里体现了“方案 B”的灵活性：针对特定任务修改环境变量
EXTRA_ARGS=""
if [[ "$TASK_NAME" == "百炼成神" ]]; then
    export LAZY_CLI_ADVISOR="llm"
    EXTRA_ARGS="--add-prompt '目前资源发布有2套剧集编号格式，A编号格式百炼成神第三季从01开始，剧集名特性是2为数字，如更新至22集；B编号格式第一季到现在累计1xx集如EP1XX。用户需求：选择A编号格式URL和A编号格式中的最新剧集编号'"
else
    # 其他任务默认使用 code 顾问，除非 .env 里已经指定了
    export LAZY_CLI_ADVISOR=${LAZY_CLI_ADVISOR:-code}
fi

# 6. 执行与记录
echo "------------------------------------------------------------" >> "$CRON_LOG"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 执行任务: $TASK_NAME ($MODE)" >> "$CRON_LOG"

# 运行工具，注意这里显式传入了 --env 确保双重保险
$BIN_PATH update "$MODE" "$TASK_NAME" --env "$ENV_FILE" $EXTRA_ARGS >> "$CRON_LOG" 2>&1

# 记录执行状态
if [ $? -eq 0 ]; then
    echo "[SUCCESS] $TASK_NAME 更新成功" >> "$CRON_LOG"
else
    echo "[ERROR] $TASK_NAME 更新出现异常，请查看上方日志" >> "$CRON_LOG"
fi