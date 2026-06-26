#!/bin/bash
# 测试脚本 v1.0

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "🧪 运行测试..."
echo ""

# 1. 检查必需文件
echo "1️⃣ 检查必需文件..."
REQUIRED_FILES=(
    "SKILL.md"
    "README.md"
    "install.json"
    "_meta.json"
    "clawhub.json"
    "scripts/postinstall.js"
    "scripts/check_environment.py"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "${PROJECT_DIR}/${file}" ]; then
        echo "   ✅ ${file}"
    else
        echo "   ❌ ${file} 不存在"
        exit 1
    fi
done

echo ""

# 2. 检查 Python 环境
echo "2️⃣ 检查 Python 环境..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    echo "   ✅ Python ${PYTHON_VERSION}"
else
    echo "   ❌ Python 3 未安装"
    exit 1
fi

echo ""

# 3. 检查依赖
echo "3️⃣ 检查 Python 依赖..."
python3 -c "import requests; print('   ✅ requests ' + requests.__version__)" || {
    echo "   ❌ requests 未安装"
    exit 1
}

echo ""

# 4. 运行环境检测
echo "4️⃣ 运行环境检测..."
python3 "${PROJECT_DIR}/scripts/check_environment.py"
TEST_RESULT=$?

if [ $TEST_RESULT -eq 0 ]; then
    echo ""
    echo "════════════════════════════════════════════════════════"
    echo "  ✅ 所有测试通过"
    echo "════════════════════════════════════════════════════════"
else
    echo ""
    echo "⚠️ 部分测试未通过"
    exit 1
fi