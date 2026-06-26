#!/bin/bash
# Self Evolution Pro - 定期审查脚本
# 审查学习记录，识别可晋级项，更新知识图谱
set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

WORKSPACE="${HOME}/.openclaw/workspace"
LEARNINGS_DIR="${WORKSPACE}/.learnings"
EVOLUTION_DIR="${WORKSPACE}/.evolution"

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_step() { echo -e "${BLUE}[REVIEW]${NC} $1"; }

echo "========================================="
echo "Self Evolution Pro - 学习审查报告"
echo "执行时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "========================================="
echo ""

# 1. 统计概览
log_step "1. 数据统计"
echo ""
TOTALS=$(find "${LEARNINGS_DIR}" -name "*.md" -exec wc -l {} \; 2>/dev/null | tail -1 | awk '{print $1}' || echo "0")
LEARNINGS_COUNT=$(grep -c "^## \[" "${LEARNINGS_DIR}/LEARNINGS.md" 2>/dev/null || echo "0")
ERRORS_COUNT=$(grep -c "^## \[" "${LEARNINGS_DIR}/ERRORS.md" 2>/dev/null || echo "0")
FEATURES_COUNT=$(grep -c "^## \[" "${LEARNINGS_DIR}/FEATURE_REQUESTS.md" 2>/dev/null || echo "0")
PENDING_LEARNINGS=$(grep -c "Status.*pending" "${LEARNINGS_DIR}/LEARNINGS.md" 2>/dev/null || echo "0")
PENDING_ERRORS=$(grep -c "Status.*pending" "${LEARNINGS_DIR}/ERRORS.md" 2>/dev/null || echo "0")

echo "  总记录数: $((LEARNINGS_COUNT + ERRORS_COUNT + FEATURES_COUNT))"
echo "  - 学习记录: ${LEARNINGS_COUNT} (待处理: ${PENDING_LEARNINGS})"
echo "  - 错误记录: ${ERRORS_COUNT} (待处理: ${PENDING_ERRORS})"
echo "  - 功能请求: ${FEATURES_COUNT}"
echo ""

# 2. 高优先级项
log_step "2. 高优先级待处理项"
echo ""
HIGH_LEARNINGS=$(grep -B 3 "Priority.*high" "${LEARNINGS_DIR}/LEARNINGS.md" 2>/dev/null | grep "^## \[" | head -5 || echo "  (无)")
HIGH_ERRORS=$(grep -B 3 "Priority.*high" "${LEARNINGS_DIR}/ERRORS.md" 2>/dev/null | grep "^## \[" | head -5 || echo "  (无)")

if [ -n "$HIGH_LEARNINGS" ] && [ "$HIGH_LEARNINGS" != "  (无)" ]; then
    echo "  学习记录:"
    echo "$HIGH_LEARNINGS" | while read line; do echo "    - $line"; done
fi
if [ -n "$HIGH_ERRORS" ] && [ "$HIGH_ERRORS" != "  (无)" ]; then
    echo "  错误记录:"
    echo "$HIGH_ERRORS" | while read line; do echo "    - $line"; done
fi
[ -z "$HIGH_LEARNINGS" ] && [ -z "$HIGH_ERRORS" ] && echo "  (无高优先级项)"
echo ""

# 3. 复发项检查
log_step "3. 复发模式检测"
echo ""
RECURRING=$(grep -B 1 "Recurrence-Count.*[3-9]" "${LEARNINGS_DIR}/LEARNINGS.md" 2>/dev/null | grep "^## \[" | sort -u || echo "")
if [ -n "$RECURRING" ]; then
    echo "  发现以下高复发项 (≥3次):"
    echo "$RECURRING" | while read line; do echo "    ⚠️  $line"; done
    echo ""
    echo "  💡 建议: 这些项应考虑晋级为技能或项目规范"
else
    echo "  (无高复发项)"
fi
echo ""

# 4. 晋级候选
log_step "4. 晋级候选检查"
echo ""
CANDIDATES=$(grep -B 5 "Status.*pending" "${LEARNINGS_DIR}/LEARNINGS.md" 2>/dev/null | grep "^## \[" | head -5 || echo "")
if [ -n "$CANDIDATES" ]; then
    echo "  待晋级项:"
    echo "$CANDIDATES" | while read line; do echo "    → $line"; done
else
    echo "  (无待晋级项)"
fi
echo ""

# 5. 更新指标
log_step "5. 更新进化指标"
echo ""
mkdir -p "${EVOLUTION_DIR}"
METRICS_FILE="${EVOLUTION_DIR}/metrics.md"

REVIEW_DATE=$(date +%Y-%m-%d)
echo "最后审查: ${REVIEW_DATE}" >> "${METRICS_FILE}" 2>/dev/null || true

echo "  指标已更新到: ${METRICS_FILE}"
echo ""

# 6. 知识图谱检查
log_step "6. 知识图谱状态"
echo ""
if [ -f "${LEARNINGS_DIR}/KNOWLEDGE_GRAPH.md" ]; then
    NODES=$(grep -c "^|" "${LEARNINGS_DIR}/KNOWLEDGE_GRAPH.md" 2>/dev/null || echo "0")
    echo "  知识图谱节点数: ${NODES}"
else
    echo "  知识图谱未初始化，建议运行: 初始化知识图谱"
fi
echo ""

log_info "审查完成！"
echo ""
echo "建议操作:"
echo "  1. 查看高优先级项并处理"
echo "  2. 考虑将复发≥3的项晋级为技能"
echo "  3. 更新知识图谱链接"
echo ""
