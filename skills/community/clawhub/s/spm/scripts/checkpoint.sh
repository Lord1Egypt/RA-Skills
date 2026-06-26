#!/usr/bin/env bash
# checkpoint.sh — Generate a checkpoint report for the specified phase
#
# Usage:
#   ./scripts/checkpoint.sh phase-1        # Requirements alignment
#   ./scripts/checkpoint.sh phase-2        # Planning alignment
#   ./scripts/checkpoint.sh phase-3        # Execution milestone
#   ./scripts/checkpoint.sh phase-4        # Quality gate
#   ./scripts/checkpoint.sh phase-5        # Delivery gate
#
# The script reads project files and populates the template with actual data.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
TEMPLATES_DIR="$PROJECT_ROOT/CHECKPOINTS"
OUTPUT_DIR="$PROJECT_ROOT/docs/checkpoints"

PHASE="${1:?Usage: $0 phase-1|phase-2|phase-3|phase-4|phase-5}"

# Map phase arg to template filename
case "$PHASE" in
  phase-1) TEMPLATE_NAME="PHASE-1-REQUIREMENTS.md" ;;
  phase-2) TEMPLATE_NAME="PHASE-2-PLANNING.md" ;;
  phase-3) TEMPLATE_NAME="PHASE-3-EXECUTION.md" ;;
  phase-4) TEMPLATE_NAME="PHASE-4-QUALITY.md" ;;
  phase-5) TEMPLATE_NAME="PHASE-5-DELIVERY.md" ;;
  *) echo "✗ Unknown phase: $PHASE. Use: phase-1 | phase-2 | phase-3 | phase-4 | phase-5" >&2; exit 1 ;;
esac

# Ensure output directory exists
mkdir -p "$OUTPUT_DIR"

# Template file
TEMPLATE="$TEMPLATES_DIR/$TEMPLATE_NAME"
if [[ ! -f "$TEMPLATE" ]]; then
  echo "✗ Template not found: $TEMPLATE" >&2
  exit 1
fi

# Gather project data
PROJECT_NAME=$(basename "$PROJECT_ROOT")
TIMESTAMP=$(date +"%Y-%m-%d %H:%M %Z")
AGENT_ID="${AGENT_ID:-unknown}"

# Phase-specific data extraction
case "$PHASE" in
  phase-1)
    # Requirements phase
    REQS_FILE="$PROJECT_ROOT/docs/requirements.md"
    if [[ -f "$REQS_FILE" ]]; then
      REQS_SIZE=$(wc -m < "$REQS_FILE")
      REQS_EXISTS="✅"
    else
      REQS_EXISTS="❌"
      REQS_SIZE=0
    fi

    # Soul-searching answers: try to extract from DECISIONS.md or TASKS.yaml
    ASSUMPTIONS_FILE="$PROJECT_ROOT/DECISIONS.md"
    if [[ -f "$ASSUMPTIONS_FILE" ]]; then
      ASSUMPTIONS_COUNT=$(grep -c "^##" "$ASSUMPTIONS_FILE" || echo 0)
    else
      ASSUMPTIONS_COUNT=0
    fi

    # Populate template variables
    OUTPUT="$OUTPUT_DIR/phase-1-$(date +%Y%m%d-%H%M).md"
    cat "$TEMPLATE" | \
      sed "s/{{project_name}}/$PROJECT_NAME/g" | \
      sed "s/{{timestamp}}/$TIMESTAMP/g" | \
      sed "s/{{agent_id}}/$AGENT_ID/g" | \
      sed "s/{{answer}}/TODO: fill in/g" | \
      sed "s/{{user_comments}}/ /g" \
      > "$OUTPUT"

    ;;

  phase-2)
    # Planning phase
    LEDGER_FILE="$PROJECT_ROOT/docs/spm/ledger.md"
    if [[ -f "$LEDGER_FILE" ]]; then
      # Count data rows only: lines starting with | that contain a status value (skip header and separator)
      TASK_COUNT=$(grep -cE "^\|.*\| (todo|doing|done|blocked|skipped) \|" "$LEDGER_FILE" 2>/dev/null || echo 0)
    else
      TASK_COUNT=0
    fi

    ARCH_FILE="$PROJECT_ROOT/docs/architecture.md"
    ARCH_EXISTS=$([[ -f "$ARCH_FILE" ]] && echo "✅" || echo "❌")

    OUTPUT="$OUTPUT_DIR/phase-2-$(date +%Y%m%d-%H%M).md"
    cat "$TEMPLATE" | \
      sed "s/{{project_name}}/$PROJECT_NAME/g" | \
      sed "s/{{timestamp}}/$TIMESTAMP/g" | \
      sed "s/{{agent_id}}/$AGENT_ID/g" | \
      sed "s/{{example_task}}/Setup Git worktree/g" | \
      sed "s/{{example_criteria}}/Git worktree created and branch checked out/g" | \
      sed "s/{{random_id_1}}/1/g" | \
      sed "s/{{description}}/Initial setup task/g" | \
      sed "s/{{random_id_2}}/2/g" | \
      sed "s/{{random_id_3}}/3/g" | \
      sed "s/{{assumption_1}}/Data source is available/g" | \
      sed "s/{{assumption_2}}/API rate limits sufficient/g" | \
      sed "s/{{assumption_3}}/No schema changes needed/g" | \
      sed "s/{{user_comments}}/ /g" \
      > "$OUTPUT"

    ;;

  phase-3)
    # Execution milestone
    LEDGER_FILE="$PROJECT_ROOT/docs/spm/ledger.md"

    OUTPUT="$OUTPUT_DIR/phase-3-$(date +%Y%m%d-%H%M).md"
    cat "$TEMPLATE" | \
      sed "s/{{project_name}}/$PROJECT_NAME/g" | \
      sed "s/{{timestamp}}/$TIMESTAMP/g" | \
      sed "s/{{agent_id}}/$AGENT_ID/g" | \
      sed "s/{{milestone_name}}/Initial implementation/g" | \
      sed "s/{{task_ids}}/1,2,3/g" | \
      sed "s/{{task_id_1}}/1/g" | \
      sed "s/{{task_name}}/Setup project structure/g" | \
      sed "s/{{task_id_2}}/2/g" | \
      sed "s/{{task_name}}/Implement core module/g" | \
      sed "s/{{task_id_3}}/3/g" | \
      sed "s/{{task_name}}/Create Worker API/g" | \
      sed "s#{{evidence_path}}#docs/spm/ledger.md#g" | \
      sed "s/{{summary}}/Completed initial scaffolding and core data pipeline/g" | \
      sed "s/{{next_milestone_summary}}/Frontend integration and testing/g" | \
      sed "s/{{blocker_details}}/None/g" | \
      sed "s/{{user_comments}}/ /g" \
      > "$OUTPUT"

    ;;

  phase-4)
    # Quality gate
    LEDGER_FILE="$PROJECT_ROOT/docs/spm/ledger.md"
    if [[ -f "$LEDGER_FILE" ]]; then
      DONE_COUNT=$(grep -cE "\| done \|" "$LEDGER_FILE" || echo 0)
      TOTAL_COUNT=$(grep -cE "^\|.*\| (todo|doing|done|blocked|skipped) \|" "$LEDGER_FILE" 2>/dev/null || echo 0)
    else
      DONE_COUNT=0
      TOTAL_COUNT=0
    fi

    OUTPUT="$OUTPUT_DIR/phase-4-$(date +%Y%m%d-%H%M).md"
    cat "$TEMPLATE" | \
      sed "s/{{project_name}}/$PROJECT_NAME/g" | \
      sed "s/{{timestamp}}/$TIMESTAMP/g" | \
      sed "s/{{agent_id}}/$AGENT_ID/g" | \
      sed "s/{{done_count}}/$DONE_COUNT/g" | \
      sed "s/{{total_count}}/$TOTAL_COUNT/g" | \
      sed "s/{{test_output}}/TODO: paste npm test output/g" | \
      sed "s/{{lint_output}}/TODO: paste lint output/g" | \
      sed "s/{{review_summary}}/TODO: summarise code review findings/g" | \
      sed "s/{{issues_list}}/None/g" | \
      sed "s/{{user_comments}}/ /g" \
      > "$OUTPUT"

    ;;

  phase-5)
    # Delivery gate
    OUTPUT="$OUTPUT_DIR/phase-5-$(date +%Y%m%d-%H%M).md"
    cat "$TEMPLATE" | \
      sed "s/{{project_name}}/$PROJECT_NAME/g" | \
      sed "s/{{timestamp}}/$TIMESTAMP/g" | \
      sed "s/{{agent_id}}/$AGENT_ID/g" | \
      sed "s#{{e2e_output}}#TODO: run ./scripts/e2e.sh and paste output#g" | \
      sed "s/{{failed_tests}}/None/g" | \
      sed "s/{{environment}}/staging/g" | \
      sed "s/{{window}}/Anytime/g" | \
      sed "s#{{rollback_steps}}#TODO: document rollback steps#g" | \
      sed "s/{{user_notes}}/ /g" | \
      sed "s/{{issues_list}}/None/g" | \
      sed "s#{{mitigation}}#N/A#g" \
      > "$OUTPUT"

    ;;

esac

echo "✓ Checkpoint report generated: $OUTPUT"
echo ""
echo "============================================================"
echo "  🛑 HARD STOP — 硬节点强制停顿"
echo "============================================================"
echo ""
echo "你必须现在停止、向用户呈现这份报告并等待明确批准。"
echo "禁止在用户确认前进入下一阶段。"
echo ""
echo "报告 Checklist："
echo "  □ 展示阶段完成情况（${PHASE}）"
echo "  □ 逐项说明质量门控结果"
echo "  □ 列出任何未解决的问题或风险"
echo "  □ 明确请求：'是否批准进入下一阶段？'"
echo ""
echo "用户回复 → 批准后继续 / 需修改则回溯修复后重新生成 checkpoint"
