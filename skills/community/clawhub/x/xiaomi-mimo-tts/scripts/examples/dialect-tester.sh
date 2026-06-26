#!/bin/bash
# 方言测试器 - 测试各种方言检测 (兼容 Bash 3.x)
# 验证智能版本方言检测的准确性
#
# 用法: ./dialect-tester.sh
# 测试所有支持的方言检测

echo "🔍 方言测试器 - 测试智能方言检测"
echo "=================================="
echo ""

# 检查智能脚本是否存在
if [ ! -f "../mimo-tts-smart.sh" ]; then
    echo "错误: 找不到 mimo-tts-smart.sh 脚本"
    echo "请确保在 scripts/examples/ 目录中运行"
    exit 1
fi

# 创建测试目录
TEST_DIR="/tmp/mimo-dialect-test-$(date +%s)"
mkdir -p "$TEST_DIR"
echo "测试目录: $TEST_DIR"
echo ""

# 测试用例（使用并行数组以兼容较旧的 bash）
DIALECTS=("上海话" "四川话" "山东话" "台湾腔" "台湾闽南话" "东北话" "粤语" "河南话" "陕西话")
TEXTS=(
    "侬是被冬天冻痴特了伐？哪能跟个冰雕一样，动不动就玩消失？"
    "要得！巴适得板！瓜娃子才不晓得嘛！莫得事，摆个龙门阵，撇脱得很！"
    "俺那娘嘞，杠赛来你这个山东话！恁这个话讲得！得劲！熊样！"
    "真的假的！好喔～是喔安捏，酱紫真的是好喔！太扯了！"
    "哩厚！多谢喔！拍谢拍谢！金价足水！有够赞！"
    "老铁，咋整啊？没毛病！杠杠的！必须的！嗷嗷的！"
    "唔系嘛？你做乜嘢啊？好正！真系好掂！睇下啦，食饭未啊？"
    "中！可中！得劲得很！俺说个地道河南顺口溜：恁说中不中？美嘞很！"
    "嫽咋咧！美滴很！咥饭了没？谝一谝嘛！嘹太太！么嘛达！"
)

TOTAL_TESTS=${#DIALECTS[@]}
PASSED_TESTS=0
FAILED_TESTS=0

echo "📊 开始测试 $TOTAL_TESTS 种方言..."
echo ""

for i in "$(seq 0 $((TOTAL_TESTS-1)))"; do
    # seq outputs a newline-separated list; iterate properly
    for idx in $(seq 0 $((TOTAL_TESTS-1))); do
        DIALECT=${DIALECTS[$idx]}
        TEXT=${TEXTS[$idx]}
        OUTPUT_FILE="$TEST_DIR/${DIALECT// /_}.ogg"

        echo "测试: $DIALECT"
        echo "  文本: $TEXT"

        RESULT=$(../mimo-tts-smart.sh "$TEXT" "$OUTPUT_FILE" 2>&1)

        if echo "$RESULT" | grep -q "方言:.*$DIALECT"; then
            echo "  ✅ 检测成功: $DIALECT"
            PASSED_TESTS=$((PASSED_TESTS+1))
            STYLE=$(echo "$RESULT" | grep -o "风格:.*" | cut -d':' -f2 | xargs)
            echo "  风格: $STYLE"
        else
            echo "  ❌ 检测失败: 期望 $DIALECT"
            echo "  实际输出:"
            echo "$RESULT" | grep -E "(方言|风格|检测结果)" || echo "$RESULT"
            FAILED_TESTS=$((FAILED_TESTS+1))
        fi

        echo ""
    done
    break
done

# 测试结果统计
echo "📈 测试结果统计:"
echo "=================="
echo "总测试数: $TOTAL_TESTS"
echo "通过数: $PASSED_TESTS"
echo "失败数: $FAILED_TESTS"
if [ $TOTAL_TESTS -gt 0 ]; then
    echo "通过率: $((PASSED_TESTS * 100 / TOTAL_TESTS))%"
else
    echo "通过率: N/A"
fi

echo ""
if [ $FAILED_TESTS -eq 0 ]; then
    echo "🎉 所有方言检测测试通过！"
else
    echo "⚠️  有 $FAILED_TESTS 个测试失败，请检查方言关键词配置"
    echo ""
    echo "失败的测试:"
    for idx in $(seq 0 $((TOTAL_TESTS-1))); do
        DIALECT=${DIALECTS[$idx]}
        TEXT=${TEXTS[$idx]}
        RESULT=$(../mimo-tts-smart.sh "$TEXT" "/dev/null" 2>&1)
        if ! echo "$RESULT" | grep -q "方言:.*$DIALECT"; then
            DETECTED=$(echo "$RESULT" | grep -o "方言:[^,]*" | cut -d':' -f2 | xargs)
            echo "  - $DIALECT → 检测为: $DETECTED"
        fi
    done
fi

echo ""
echo "💾 测试文件保存在: $TEST_DIR"
echo "   使用命令清理: rm -rf $TEST_DIR"