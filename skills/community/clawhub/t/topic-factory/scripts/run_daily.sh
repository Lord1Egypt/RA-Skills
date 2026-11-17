#!/bin/bash
# run_daily.sh - 每日选题生成调度脚本（每天 04:00 跑）
#
# 功能：
#   1. cd 到 ${SCRIPT_DIR}（脚本所在目录）
#   2. 运行 node generate_topics.js
#   3. 验证输出文件 ${WORKSPACE_DIR}/claude-hub/topics/YYYYMMDD_topics.md > 5000 字节
#   4. 失败重试 3 次（每次间隔 30 秒）
#   5. 3 次全部失败：调用 send_alert.py 发送飞书告警
#
# 输入：无（完全自包含，路径写死）
# 输出：控制台日志 + 告警到飞书（仅失败时）
#
# 作者：Claude
# 日期：2026-08-14

set -uo pipefail

# ============================================================
# 1. 路径配置（写死在脚本里，不依赖外部环境变量）
# ============================================================

# 本脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# topics/ 输出目录（与 generate_topics.js 保持一致）
WORKSPACE_DIR="${HOME}/.openclaw/workspace"
TOPICS_DIR="${WORKSPACE_DIR}/claude-hub/topics"

# generate_topics.js 路径
GENERATE_SCRIPT="${SCRIPT_DIR}/generate_topics.js"

# send_alert.py 路径（A股报告复用，同一父目录）
SEND_ALERT="${WORKSPACE_DIR}/.analysis/send_alert.py"

# 日志文件（记录每次 generate_topics.js 的 stdout + stderr）
LOG="/tmp/topic_factory.log"

# 最大重试次数
MAX_RETRIES=3

# 输出文件最小字节数（防止生成空文件/过小文件）
MIN_FILE_SIZE=5000

# ============================================================
# 2. 辅助函数
# ============================================================

# 获取今天日期（YYYYMMDD），北京时间
get_today() {
  TZ=Asia/Shanghai date +%Y%m%d
}

# 检查输出文件是否有效（存在且 > MIN_FILE_SIZE 字节）
check_output() {
  local file="${TOPICS_DIR}/${1}_topics.md"
  if [[ ! -f "${file}" ]]; then
    echo "✗ 文件不存在: ${file}"
    return 1
  fi

  # macOS 用 stat -f%z，Linux 用 stat -c%s
  local size
  if [[ "$(uname)" == "Darwin" ]]; then
    size=$(stat -f%z "${file}")
  else
    size=$(stat -c%s "${file}")
  fi

  if [[ ${size} -gt ${MIN_FILE_SIZE} ]]; then
    echo "✓ 文件正常: ${file} (${size} bytes)"
    return 0
  else
    echo "✗ 文件过小: ${file} (${size} bytes < ${MIN_FILE_SIZE})"
    return 1
  fi
}

# ============================================================
# 3. 主流程
# ============================================================

echo "=== run_daily.sh 启动 ==="
echo "时间: $(TZ=Asia/Shanghai date '+%Y-%m-%d %H:%M:%S')"
echo "脚本目录: ${SCRIPT_DIR}"
echo "生成脚本: ${GENERATE_SCRIPT}"
echo "输出目录: ${TOPICS_DIR}"
echo "最大重试: ${MAX_RETRIES} 次"
echo ""

# 前置检查：generate_topics.js 是否存在
if [[ ! -f "${GENERATE_SCRIPT}" ]]; then
  echo "✗ ERROR: generate_topics.js 不存在: ${GENERATE_SCRIPT}"
  exit 1
fi

# 前置检查：send_alert.py 是否存在
if [[ ! -f "${SEND_ALERT}" ]]; then
  echo "✗ ERROR: send_alert.py 不存在: ${SEND_ALERT}"
  exit 1
fi

TODAY=$(get_today)
echo "今天日期: ${TODAY}"

# 循环重试
for i in $(seq 1 ${MAX_RETRIES}); do
  echo ""
  echo "--- 第 $i/${MAX_RETRIES} 次尝试 ---"

  # 切换到脚本目录，确保 generate_topics.js 能找到同目录的模块
  cd "${SCRIPT_DIR}"

  # 运行 generate_topics.js，stdout+stderr 写入日志
  node "${GENERATE_SCRIPT}" > "${LOG}" 2>&1
  EXIT_CODE=$?
  echo "generate_topics.js exit code: ${EXIT_CODE}"

  # 检查输出文件
  if check_output "${TODAY}"; then
    echo ""
    echo "=== ✓ 选题生成成功 ==="
    exit 0
  fi

  # 失败：打印日志摘要
  echo "✗ 第 $i 次失败"
  echo "--- 最近 10 行日志 ---"
  tail -10 "${LOG}" 2>/dev/null || echo "（日志为空）"
  echo "--- 结束 ---"

  # 未达最大重试次数，等待后重试
  if [[ $i -lt ${MAX_RETRIES} ]]; then
    echo "等待 30 秒后重试..."
    sleep 30
  fi
done

# ============================================================
# 4. 3 次全部失败：发送飞书告警
# ============================================================

echo ""
echo "=== ✗ 3 次重试全部失败，发送飞书告警 ==="

# 读取日志最后 20 行作为告警上下文
LOG_CONTEXT=$(tail -20 "${LOG}" 2>/dev/null | tr '\n' ' ' | cut -c1-500)

# 调用 send_alert.py（与 A 股报告共用同一告警脚本）
python3 "${SEND_ALERT}" "选题生成失败 ${MAX_RETRIES} 次 | 日志摘要: ${LOG_CONTEXT}"

echo ""
echo "=== run_daily.sh 结束（失败） ==="
exit 1
