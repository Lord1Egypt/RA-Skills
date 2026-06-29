#!/usr/bin/env bash
#===============================================================================
# XDesign Eval Runner — 自动验证 Trigger 覆盖 + Eval Cases 完整性
# Usage: bash evals/run-evals.sh [--verbose]
#===============================================================================
set -euo pipefail
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PASS=0; FAIL=0; TOTAL=0

log()   { printf "  %s\n" "$*"; }
pass()  { PASS=$((PASS+1)); TOTAL=$((TOTAL+1)); printf "  ✅ %s\n" "$*"; }
fail()  { FAIL=$((FAIL+1)); TOTAL=$((TOTAL+1)); printf "  ❌ %s\n" "$*"; }
header(){ printf "\n## %s\n" "$*"; }

#===============================================================================
# 1. 文件完整性检查
#===============================================================================
header "[1/4] 文件完整性"

THEME_COUNT=$(ls "$SKILL_DIR/deck-studio/assets/themes/"*.css 2>/dev/null | wc -l | tr -d ' ')
[ "$THEME_COUNT" -eq 36 ] && pass "主题: 36/36" || fail "主题: ${THEME_COUNT}/36"

TEMPLATE_COUNT=$(ls -d "$SKILL_DIR/deck-studio/templates/full-decks/"*/ 2>/dev/null | wc -l | tr -d ' ')
[ "$TEMPLATE_COUNT" -eq 15 ] && pass "full-deck 模板: 15/15" || fail "full-deck 模板: ${TEMPLATE_COUNT}/15"

LAYOUT_COUNT=$(ls "$SKILL_DIR/deck-studio/templates/single-page/"*.html 2>/dev/null | wc -l | tr -d ' ')
[ "$LAYOUT_COUNT" -ge 28 ] && pass "single-page 布局: $LAYOUT_COUNT (≥28)" || fail "single-page 布局: $LAYOUT_COUNT (<28)"

[ -f "$SKILL_DIR/SKILL.md" ]         && pass "SKILL.md 存在"       || fail "SKILL.md 缺失"
[ -f "$SKILL_DIR/evals/evals.json" ] && pass "evals.json 存在"     || fail "evals.json 缺失"
[ -f "$SKILL_DIR/evals/trigger-queries.json" ] && pass "trigger-queries.json 存在" || fail "trigger-queries.json 缺失"
[ -f "$SKILL_DIR/references/workflow-guide.md" ]    && pass "workflow-guide.md 存在"    || fail "workflow-guide.md 缺失"
[ -f "$SKILL_DIR/references/integration-guide.md" ] && pass "integration-guide.md 存在" || fail "integration-guide.md 缺失"
[ -f "$SKILL_DIR/references/schemas.md" ]           && pass "schemas.md 存在"            || fail "schemas.md 缺失"
[ -f "$SKILL_DIR/references/deck-studio-catalog.md" ] && pass "deck-studio-catalog.md 存在" || fail "deck-studio-catalog.md 缺失"

#===============================================================================
# 2. trigger-queries.json 覆盖检查
#===============================================================================
header "[2/4] Trigger Query 覆盖"

QUERY_COUNT=$(python3 -c "import json; d=json.load(open('$SKILL_DIR/evals/trigger-queries.json')); print(len(d))" 2>/dev/null || echo "0")
[ "$QUERY_COUNT" -ge 19 ] && pass "Trigger queries: $QUERY_COUNT 条 (≥19)" || fail "Trigger queries: $QUERY_COUNT (<19)"

TRUE_COUNT=$(python3 -c "import json; d=json.load(open('$SKILL_DIR/evals/trigger-queries.json')); print(sum(1 for q in d if q['should_trigger']))" 2>/dev/null || echo "0")
FALSE_COUNT=$(python3 -c "import json; d=json.load(open('$SKILL_DIR/evals/trigger-queries.json')); print(sum(1 for q in d if not q['should_trigger']))" 2>/dev/null || echo "0")
pass "应触发: $TRUE_COUNT | 不应触发: $FALSE_COUNT"

# 检查 false-positive 和 false-negative
FP_CHECK=$(python3 -c "
import json
d=json.load(open('$SKILL_DIR/evals/trigger-queries.json'))
non_triggers=[q['query'] for q in d if not q['should_trigger']]
# 检查不应触发的 query 是否误触了 XDesign 关键词
risky=[q[:40]+'...' for q in non_triggers if any(k in q.lower() for k in ['slide','ppt','deck','设计','仪表盘','okr','present','html','landing'])]
print(len(risky))
" 2>/dev/null || echo "0")
[ "$FP_CHECK" -eq 0 ] && pass "False-positive risk: 0" || fail "False-positive risk: $FP_CHECK 条可能误触"

#===============================================================================
# 3. Eval Case 覆盖检查
#===============================================================================
header "[3/4] Eval Cases 覆盖"

EVAL_COUNT=$(python3 -c "import json; d=json.load(open('$SKILL_DIR/evals/evals.json')); print(len(d['evals']))" 2>/dev/null || echo "0")
[ "$EVAL_COUNT" -ge 5 ] && pass "Eval cases: $EVAL_COUNT (≥5)" || fail "Eval cases: $EVAL_COUNT (<5)"

# 检查模式覆盖
MODE_COVERAGE=$(python3 -c "
import json
d=json.load(open('$SKILL_DIR/evals/evals.json'))
prompts=[e['prompt'] for e in d['evals']]
modes=[]
if any('pitch deck' in p.lower() or 'slides' in p.lower() for p in prompts): modes.append('Mode1')
if any('dashboard' in p.lower() or 'landing' in p.lower() or 'prototype' in p.lower() for p in prompts): modes.append('Mode2')
if any('animation' in p.lower() or '动效' in p for p in prompts): modes.append('Mode3')
if any('extract' in p.lower() or 'DESIGN.md' in p for p in prompts): modes.append('URL-to-brand')
print('+'.join(modes))
" 2>/dev/null || echo "none")

log "覆盖模式: $MODE_COVERAGE"
# 检查是否覆盖至少 3 种模式
echo "$MODE_COVERAGE" | python3 -c "
import sys
modes = sys.stdin.read().strip()
parts = modes.split('+')
exit(0 if len(parts) >= 3 else 1)
" 2>/dev/null && pass "覆盖 ≥3 种模式 ($MODE_COVERAGE)" || fail "覆盖 <3 种模式 ($MODE_COVERAGE)"

# 检查 skippable thresholds
SKIP_CHECK=$(python3 -c "
import json
d=json.load(open('$SKILL_DIR/evals/evals.json'))
skippable = sum(1 for e in d['evals'] if 'skippable' in str(e.get('expectations','')))
checklist_only = sum(1 for e in d['evals'] if 'checklist' in str(e.get('expectations','')))
print(f'{skippable},{checklist_only}')
" 2>/dev/null || echo "0,0")
log "Skippable: $(echo $SKIP_CHECK | cut -d, -f1) | Checklist-only: $(echo $SKIP_CHECK | cut -d, -f2)"

#===============================================================================
# 4. 文件大小检查（文档健康）
#===============================================================================
header "[4/4] 文档健康"

for f in "SKILL.md" "references/workflow-guide.md" "references/integration-guide.md" \
         "references/schemas.md" "references/deck-studio-catalog.md" \
         "references/design-system-catalog.md" "references/mode-2-prototype.md" \
         "references/technical-specs.md"; do
  fp="$SKILL_DIR/$f"
  if [ -f "$fp" ]; then
    lines=$(wc -l < "$fp" | tr -d ' ')
    if [ "$lines" -le 500 ]; then
      pass "$f: $lines 行 (≤500)"
    else
      fail "$f: $lines 行 (>500, 需拆分)"
    fi
  fi
done

#===============================================================================
# 汇总
#===============================================================================
echo ""
echo "========================================="
echo "  XDesign Eval Summary"
echo "  通过: $PASS | 失败: $FAIL | 总计: $TOTAL"
echo "========================================="

# 如果要求 verbose, 输出评估报告
if [ "${1:-}" = "--verbose" ]; then
  echo ""
  echo "--- 人工评估清单 ---"
  echo "请手动执行以下步骤:"
  echo ""
  echo "1. 在 Trae IDE 中触发 XDesign skill, 验证 trigger-queries.json 中的 true cases 全部触发"
  echo "2. 对 evals.json 中每个 case, 手动验证 expectations 是否满足"
  echo "3. 浏览器打开 deck-studio/templates/theme-showcase.html — 36 主题全部渲染"
  echo "4. 浏览器打开 deck-studio/templates/full-decks-index.html — 15 模板 iframe 可加载"
  echo "5. 确认 SKILL.md 中指向 deck-studio/ 的所有路径可解析"
fi

[ "$FAIL" -eq 0 ] && exit 0 || exit 1
