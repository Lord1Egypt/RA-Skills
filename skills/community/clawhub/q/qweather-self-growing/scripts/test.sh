#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PASS=0
FAIL=0

green() { printf "\033[32m%s\033[0m\n" "$1"; }
red()   { printf "\033[31m%s\033[0m\n" "$1"; }

assert_exit() {
  local desc="$1" expected="$2"
  shift 2
  local actual=0
  "$@" >/dev/null 2>&1 || actual=$?
  if [[ "$actual" == "$expected" ]]; then
    green "  ✅ $desc"
    PASS=$((PASS + 1))
  else
    red "  ❌ $desc (expected exit=$expected, got exit=$actual)"
    FAIL=$((FAIL + 1))
  fi
}

assert_output_contains() {
  local desc="$1" pattern="$2"
  shift 2
  local output
  output=$("$@" 2>&1) || true
  if echo "$output" | grep -q "$pattern"; then
    green "  ✅ $desc"
    PASS=$((PASS + 1))
  else
    red "  ❌ $desc (output missing: $pattern)"
    FAIL=$((FAIL + 1))
  fi
}

assert_json_field() {
  local desc="$1" field="$2"
  shift 2
  local output
  output=$("$@" 2>&1) || true
  if echo "$output" | node -e "
    const d=JSON.parse(require('fs').readFileSync(0,'utf8'));
    process.exit(d.$field !== undefined ? 0 : 1)
  " 2>/dev/null; then
    green "  ✅ $desc"
    PASS=$((PASS + 1))
  else
    red "  ❌ $desc (missing field: $field)"
    FAIL=$((FAIL + 1))
  fi
}

echo "=== qweather 冒烟测试 ==="
echo ""

# --- JWT ---
echo "🔑 JWT 生成"
assert_exit "gen-jwt.mjs 正常输出 token" 0 node "$SCRIPT_DIR/gen-jwt.mjs"
assert_exit "gen-jwt.mjs --host 输出 API Host" 0 node "$SCRIPT_DIR/gen-jwt.mjs" --host

# --- 实时天气 ---
echo ""
echo "🌤  实时天气 (--now)"
assert_exit "杭州 --now 正常返回" 0 bash "$SCRIPT_DIR/qweather.sh" 杭州 --now
assert_output_contains "杭州 --now 包含实时天气" "实时天气" bash "$SCRIPT_DIR/qweather.sh" 杭州 --now
assert_json_field "杭州 --now --json 包含 now 字段" "now" bash "$SCRIPT_DIR/qweather.sh" 杭州 --now --json

# --- 逐日预报 ---
echo ""
echo "📅 逐日预报"
assert_exit "杭州 3天预报正常返回" 0 bash "$SCRIPT_DIR/qweather.sh" 杭州
assert_output_contains "杭州 预报包含城市名" "杭州" bash "$SCRIPT_DIR/qweather.sh" 杭州
assert_json_field "杭州 --json 包含 daily 字段" "daily" bash "$SCRIPT_DIR/qweather.sh" 杭州 --json

# --- 出行格式 ---
echo ""
echo "🧳 出行格式"
assert_output_contains "杭州 --trip 包含出行天气" "出行天气" bash "$SCRIPT_DIR/qweather.sh" 杭州 --trip

# --- LocationID 直传 ---
echo ""
echo "📍 LocationID 直传"
assert_exit "LocationID 101210101 正常返回" 0 bash "$SCRIPT_DIR/qweather.sh" 101210101

# --- 错误处理 ---
echo ""
echo "⚠️  错误处理"
assert_exit "--days 5 应报错" 1 bash "$SCRIPT_DIR/qweather.sh" 杭州 --days 5
assert_exit "--help 正常退出" 0 bash "$SCRIPT_DIR/qweather.sh" --help

# --- 城市解析 ---
echo ""
echo "🏙  城市解析"
if [[ -f "$SCRIPT_DIR/../local/China-City-List-latest.csv" ]]; then
  assert_exit "北京 通过 CSV 解析" 0 bash "$SCRIPT_DIR/qweather.sh" 北京 --now
  # 朝阳应该有歧义
  assert_exit "朝阳 歧义应返回 exit 4" 4 bash "$SCRIPT_DIR/qweather.sh" 朝阳 --now
  assert_output_contains "朝阳 歧义列出候选" "候选" bash "$SCRIPT_DIR/qweather.sh" 朝阳 --now
else
  echo "  ⏭  跳过 CSV 测试（未找到 LocationList，请先运行 init.sh）"
fi

# --- 汇总 ---
echo ""
echo "==========================="
TOTAL=$((PASS + FAIL))
if [[ "$FAIL" -eq 0 ]]; then
  green "全部通过 $PASS/$TOTAL"
else
  red "通过 $PASS/$TOTAL，失败 $FAIL"
  exit 1
fi
