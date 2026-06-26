#!/bin/bash
# 代码审查清单工具 - 基于检查清单生成审查报告
# 用法: ./review-checklist.sh /path/to/checklist.md [output.md]

set -e

# 默认参数
CHECKLIST_PATH=$1
OUTPUT_PATH=${2:-"review-report.md"}

# 帮助信息
usage() {
    echo "代码审查清单工具"
    echo "用法: $0 <checklist_path> [output_path]"
    echo ""
    echo "参数:"
    echo "  checklist_path  检查清单文件路径"
    echo "  output_path     输出报告路径（默认: review-report.md）"
    echo ""
    echo "示例:"
    echo "  $0 docs/代码审查检查清单.md"
    echo "  $0 docs/代码审查检查清单.md my-review.md"
}

# 检查参数
if [ -z "$CHECKLIST_PATH" ]; then
    usage
    exit 1
fi

# 验证检查清单文件
if [ ! -f "$CHECKLIST_PATH" ]; then
    echo "错误: 检查清单文件不存在: $CHECKLIST_PATH"
    exit 1
fi

# 生成报告标题
cat > "$OUTPUT_PATH" << 'EOF'
# 代码审查报告

**审查时间:** [填写审查时间]
**审查人:** [填写审查人]
**PR/Commit:** [填写 PR 编号或 Commit Hash]

---

## 审查结果概览

- **检查项总数:** 0
- **通过:** 0
- **未通过:** 0
- **跳过:** 0
- **备注:** [填写备注]

---

## 详细检查清单

EOF

# 解析检查清单并生成可勾选的项目
CHECKLIST_COUNT=0
CURRENT_CATEGORY=""

while IFS= read -r line; do
    # 跳过空行和标题
    if [[ -z "$line" || "$line" =~ ^#+ ]]; then
        if [[ "$line" =~ ^#+ ]]; then
            # 保存分类标题
            CATEGORY=$(echo "$line" | sed 's/^#+\s*//')
            echo "" >> "$OUTPUT_PATH"
            echo "### $CATEGORY" >> "$OUTPUT_PATH"
            echo "" >> "$OUTPUT_PATH"
        fi
        echo "$line" >> "$OUTPUT_PATH"
        continue
    fi

    # 解析检查项
    if [[ "$line" =~ ^-\s*\[(\s|x)\] ]]; then
        CHECKLIST_COUNT=$((CHECKLIST_COUNT + 1))
        ITEM_TEXT=$(echo "$line" | sed 's/^-*\s*\[.\]\s*//')

        # 生成可编辑的检查项
        echo "- [ ] $ITEM_TEXT  \`[通过/未通过/跳过]\`" >> "$OUTPUT_PATH"
    fi
done < "$CHECKLIST_PATH"

# 添加底部信息
cat >> "$OUTPUT_PATH" << 'EOF'

---

## 审查意见

### 通过条件
- [ ] 所有必要检查项都已通过
- [ ] 代码风格符合项目规范
- [ ] 测试覆盖充分
- [ ] 没有引入新的安全风险

### 建议

1. **需要改进的地方:**
   - [ ]

2. **做得好的地方:**
   - [ ]

3. **其他建议:**
   - [ ]

---

## 签名

**审查人:** ____________________  **日期:** ________

*此报告由研发经理助手工具生成*
EOF

echo "✅ 审查报告已生成: $OUTPUT_PATH"
echo "📝 包含 $CHECKLIST_COUNT 个检查项"
echo ""
echo "提示: 使用编辑器打开报告，手动填写审查结果和意见"
