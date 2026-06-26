#!/bin/bash
# code_review.sh - 代码审查脚本
# Usage: ./code_review.sh [project_path]

PROJECT_PATH="${1:-.}"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M')

echo "========================================"
echo "代码审查"
echo "项目：$PROJECT_PATH"
echo "时间：$TIMESTAMP"
echo "========================================"

# 检查 TODO
echo ""
echo "[1/4] 检查 TODO 注释..."
TODO_COUNT=$(grep -r "TODO\|FIXME\|XXX" --include="*.cpp" --include="*.h" --include="*.py" "$PROJECT_PATH" 2>/dev/null | wc -l)
echo "   发现 $TODO_COUNT 处 TODO/FIXME"

# 检查模拟代码
echo ""
echo "[2/4] 检查模拟代码..."
STUB_COUNT=$(grep -r "stub\|mock\|fake\|dummy" --include="*.cpp" --include="*.h" "$PROJECT_PATH" 2>/dev/null | wc -l)
echo "   发现 $STUB_COUNT 处模拟代码"

# 检查注释覆盖率
echo ""
echo "[3/4] 检查注释..."
HEADER_COUNT=$(find "$PROJECT_PATH" -name "*.h" | wc -l)
COMMENTED_HEADERS=$(grep -l "/\*\*" "$PROJECT_PATH"/**/*.h 2>/dev/null | wc -l)
echo "   头文件：$HEADER_COUNT 个"
echo "   有注释：$COMMENTED_HEADERS 个"

# 生成报告
echo ""
echo "[4/4] 生成报告..."
cat > "$PROJECT_PATH/CODE_REVIEW_$TIMESTAMP.md" << REPORT
# 代码审查报告

**审查时间**: $TIMESTAMP  
**项目**: $PROJECT_PATH

## 统计

| 项目 | 数量 |
|------|------|
| TODO 注释 | $TODO_COUNT |
| 模拟代码 | $STUB_COUNT |
| 头文件 | $HEADER_COUNT |
| 有注释头文件 | $COMMENTED_HEADERS |

## 建议

1. 处理 TODO 注释
2. 替换模拟代码
3. 补充缺失注释

---

*自动生成：code_review.sh*
REPORT

echo "   报告已生成：CODE_REVIEW_$TIMESTAMP.md"
echo ""
echo "========================================"
echo "✅ 代码审查完成"
echo "========================================"
