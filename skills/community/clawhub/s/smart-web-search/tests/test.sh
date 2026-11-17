#!/bin/bash
# smart-web-search smoke tests (v2.0.0)
# Tests basic functionality without obsolete features
set +e

SKILL_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$SKILL_ROOT" || exit 1

PASS=0
FAIL=0
RESULTS=()

run_test() {
  local name="$1"
  local cmd="$2"
  local expect="$3"
  echo ""
  echo "=========================================="
  echo "  [测试] $name"
  echo "=========================================="
  local output
  output=$(eval "$cmd" 2>&1)
  if echo "$output" | grep -q "$expect"; then
    echo "[PASS] $name"
    PASS=$((PASS + 1))
    RESULTS+=("[PASS] $name")
  else
    echo "[FAIL] $name (期望: $expect)"
    echo "--- 实际输出（前 30 行）---"
    echo "$output" | head -30
    FAIL=$((FAIL + 1))
    RESULTS+=("[FAIL] $name")
  fi
}

echo ""
echo "##########################################"
echo "  smart-web-search v2.0.0 smoke tests"
echo "##########################################"

# 1. 依赖检查
run_test "依赖检查 - node_modules 存在" \
  "ls node_modules/playwright 2>&1" \
  "package.json"

# 2. check-env.js 存在并可运行
run_test "check-env.js - 脚本存在" \
  "node scripts/check-env.js 2>&1" \
  "dependencies"

# 3. --help 输出
run_test "search.js --help 输出正常" \
  "node scripts/search.js --help 2>&1" \
  "Usage:"

# 4. --region 参数识别
run_test "search.js 接受 --region 参数" \
  "node scripts/search.js 'test' --max=1 --fetch=0 --region=auto 2>&1" \
  "策略"

# 5. 自动检测搜索 - 返回结果
run_test "自动检测搜索 - 返回结果" \
  "node scripts/search.js 'Python' --max=2 --fetch=0 2>&1" \
  "条结果"

# 6. 地理检测日志
run_test "地理检测日志输出" \
  "node scripts/search.js 'test' --max=1 --fetch=0 2>&1" \
  "\[地理\]"

# 7. 正文抓取 - fetch 参数
run_test "正文抓取 - --fetch 参数" \
  "node scripts/search.js 'OpenClaw' --max=1 --fetch=1 2>&1" \
  "fetch"

# 总结
echo ""
echo "##########################################"
echo "  测试结果汇总"
echo "##########################################"
for r in "${RESULTS[@]}"; do
  echo "$r"
done
echo ""
echo "通过: $PASS / $((PASS + FAIL))"
echo ""

if [ $FAIL -eq 0 ]; then
  echo "全部测试通过"
  exit 0
else
  echo "$FAIL 项失败"
  exit 1
fi
