#!/bin/bash
# 测试安装脚本

set -e

echo "🧪 测试 Skill Usage Analyzer 安装..."

# 创建临时目录
TEMP_DIR=$(mktemp -d)
echo "📁 临时目录: $TEMP_DIR"

# 复制文件到临时目录
echo "📦 复制文件..."
cp -r . "$TEMP_DIR/"

# 进入临时目录
cd "$TEMP_DIR"

# 测试 1: 检查必要文件
echo ""
echo "✅ 测试 1: 检查必要文件"
for file in "SKILL.md" "README.md" "LICENSE" "CHANGELOG.md" "package.json"; do
    if [ -f "$file" ]; then
        echo "  ✓ $file"
    else
        echo "  ✗ $file 缺失"
        exit 1
    fi
done

# 测试 2: 检查脚本
echo ""
echo "✅ 测试 2: 检查脚本"
for script in scripts/*.py; do
    if [ -f "$script" ]; then
        echo "  ✓ $(basename $script)"
        # 检查是否可执行
        if [ -x "$script" ]; then
            echo "    可执行"
        else
            echo "    警告: 不可执行"
        fi
    fi
done

# 测试 3: 检查 Python 语法
echo ""
echo "✅ 测试 3: 检查 Python 语法"
for script in scripts/*.py; do
    if python3 -m py_compile "$script" 2>/dev/null; then
        echo "  ✓ $(basename $script) 语法正确"
    else
        echo "  ✗ $(basename $script) 语法错误"
        exit 1
    fi
done

# 测试 4: 运行基础功能测试
echo ""
echo "✅ 测试 4: 运行功能测试"
if python3 scripts/analyze_skill.py SKILL.md > /dev/null 2>&1; then
    echo "  ✓ analyze_skill.py 运行正常"
else
    echo "  ✗ analyze_skill.py 运行失败"
    exit 1
fi

# 测试 5: 检查元数据
echo ""
echo "✅ 测试 5: 检查元数据"
if [ -f ".clawhub/meta.json" ]; then
    echo "  ✓ .clawhub/meta.json 存在"
    if python3 -c "import json; json.load(open('.clawhub/meta.json'))" 2>/dev/null; then
        echo "  ✓ JSON 格式正确"
    else
        echo "  ✗ JSON 格式错误"
        exit 1
    fi
else
    echo "  ✗ .clawhub/meta.json 缺失"
    exit 1
fi

# 清理
cd -
rm -rf "$TEMP_DIR"

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "✅ 所有测试通过！"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "📦 可以打包提交了:"
echo "  tar -czvf skill-usage-analyzer-v1.0.0.tar.gz skill-usage-analyzer/"
echo ""
echo "📤 提交到 ClawHub:"
echo "  1. 访问 https://clawhub.com"
echo "  2. 点击 'Publish Skill'"
echo "  3. 上传 skill-usage-analyzer-v1.0.0.tar.gz"
echo ""
