#!/bin/bash

# 研报搜索 Skill 验证脚本
# 用于验证 skill 目录结构和必要文件是否完整

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

echo "=== 研报搜索 Skill 验证 ==="
echo ""

# 检查必要文件
errors=0

echo "检查必要文件..."

# 检查 SKILL.md
if [ -f "$SKILL_DIR/SKILL.md" ]; then
    echo "✓ SKILL.md 存在"
else
    echo "✗ SKILL.md 缺失"
    errors=$((errors + 1))
fi

# 检查 template.md
if [ -f "$SKILL_DIR/template.md" ]; then
    echo "✓ template.md 存在"
else
    echo "✗ template.md 缺失"
    errors=$((errors + 1))
fi

# 检查 examples 目录
if [ -d "$SKILL_DIR/examples" ]; then
    echo "✓ examples/ 目录存在"
    if [ -f "$SKILL_DIR/examples/sample.md" ]; then
        echo "  ✓ examples/sample.md 存在"
    else
        echo "  ✗ examples/sample.md 缺失"
        errors=$((errors + 1))
    fi
else
    echo "✗ examples/ 目录缺失"
    errors=$((errors + 1))
fi

# 检查 scripts 目录
if [ -d "$SKILL_DIR/scripts" ]; then
    echo "✓ scripts/ 目录存在"
    if [ -f "$SKILL_DIR/scripts/fxbaogao_client.py" ]; then
        echo "  ✓ scripts/fxbaogao_client.py 存在"
    else
        echo "  ✗ scripts/fxbaogao_client.py 缺失"
        errors=$((errors + 1))
    fi
    if [ -f "$SKILL_DIR/scripts/search_reports.py" ]; then
        echo "  ✓ scripts/search_reports.py 存在"
    else
        echo "  ✗ scripts/search_reports.py 缺失"
        errors=$((errors + 1))
    fi
    if [ -f "$SKILL_DIR/scripts/get_report_content.py" ]; then
        echo "  ✓ scripts/get_report_content.py 存在"
    else
        echo "  ✗ scripts/get_report_content.py 缺失"
        errors=$((errors + 1))
    fi
    if [ -f "$SKILL_DIR/scripts/validate.sh" ]; then
        echo "  ✓ scripts/validate.sh 存在"
    else
        echo "  ✗ scripts/validate.sh 缺失"
        errors=$((errors + 1))
    fi
else
    echo "✗ scripts/ 目录缺失"
    errors=$((errors + 1))
fi

echo ""

# 检查 SKILL.md 格式
echo "检查 SKILL.md 格式..."

if grep -q "^name:" "$SKILL_DIR/SKILL.md" 2>/dev/null; then
    echo "✓ 包含 name 字段"
else
    echo "✗ 缺少 name 字段"
    errors=$((errors + 1))
fi

if grep -q "^description:" "$SKILL_DIR/SKILL.md" 2>/dev/null; then
    echo "✓ 包含 description 字段"
else
    echo "✗ 缺少 description 字段"
    errors=$((errors + 1))
fi

echo ""

# 输出结果
if [ $errors -eq 0 ]; then
    echo "=== 验证通过 ==="
    exit 0
else
    echo "=== 验证失败：发现 $errors 个错误 ==="
    exit 1
fi
