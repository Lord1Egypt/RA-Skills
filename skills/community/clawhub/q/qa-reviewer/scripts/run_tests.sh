#!/bin/bash
# run_tests.sh - 运行测试脚本
# Usage: ./run_tests.sh [project_path]

PROJECT_PATH="${1:-.}"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M')

echo "========================================"
echo "运行测试"
echo "项目：$PROJECT_PATH"
echo "时间：$TIMESTAMP"
echo "========================================"

# 检查测试文件
echo ""
echo "[1/3] 检查测试文件..."
TEST_FILES=$(find "$PROJECT_PATH" -name "*_test.cpp" -o -name "test_*.cpp" -o -name "*_test.py" 2>/dev/null | wc -l)
echo "   发现 $TEST_FILES 个测试文件"

if [ "$TEST_FILES" -eq 0 ]; then
    echo "   ⚠️  未找到测试文件"
    echo ""
    echo "建议创建测试文件:"
    echo "  - C++: tests/test_feature.cpp"
    echo "  - Python: tests/test_feature.py"
    exit 0
fi

# 运行测试
echo ""
echo "[2/3] 运行测试..."

# 检查是否有 CMakeLists.txt
if [ -f "$PROJECT_PATH/tests/CMakeLists.txt" ]; then
    echo "   检测到 CMake 测试配置"
    cd "$PROJECT_PATH/tests"
    if [ ! -d "build" ]; then
        mkdir build
    fi
    cd build
    cmake .. > /dev/null 2>&1
    make > /dev/null 2>&1
    if [ -f "srm_tests" ]; then
        ./srm_tests
        TEST_RESULT=$?
    else
        echo "   ⚠️  编译失败"
        TEST_RESULT=1
    fi
    cd ../..
elif [ -f "$PROJECT_PATH/tests/pytest.ini" ]; then
    echo "   检测到 pytest 配置"
    cd "$PROJECT_PATH"
    pytest tests/ -v
    TEST_RESULT=$?
    cd ..
else
    echo "   ⚠️  未找到测试配置"
    TEST_RESULT=1
fi

# 生成报告
echo ""
echo "[3/3] 生成报告..."
cat > "$PROJECT_PATH/TEST_RESULT_$TIMESTAMP.md" << REPORT
# 测试结果

**运行时间**: $TIMESTAMP  
**项目**: $PROJECT_PATH  
**状态**: $([ $TEST_RESULT -eq 0 ] && echo "✅ 通过" || echo "❌ 失败")

## 统计

| 项目 | 数量 |
|------|------|
| 测试文件 | $TEST_FILES |
| 测试结果 | $([ $TEST_RESULT -eq 0 ] && echo "通过" || echo "失败") |

---

*自动生成：run_tests.sh*
REPORT

echo "   报告已生成：TEST_RESULT_$TIMESTAMP.md"
echo ""
echo "========================================"
if [ $TEST_RESULT -eq 0 ]; then
    echo "✅ 测试通过"
else
    echo "❌ 测试失败"
fi
echo "========================================"

exit $TEST_RESULT
