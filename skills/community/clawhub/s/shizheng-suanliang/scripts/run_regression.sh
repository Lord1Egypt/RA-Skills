#!/bin/zsh
# 一键回归：全部测试套件 + lint + fixture 校验。任何一项 FAIL 即整体 FAIL。
set -u
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$SKILL_DIR" || exit 1
fail=0

echo "== 1/6 单元测试（scripts/tests）"
python3 scripts/tests/test_municipal_qty.py 2>&1 | tail -1 || fail=1

echo "== 2/6 入口闸门测试（tests/test_entry_gate.py）"
python3 tests/test_entry_gate.py 2>&1 | grep -E "^entry_gate:" || fail=1

echo "== 3/6 内置自检（--self-test）"
python3 scripts/municipal_qty.py --self-test 2>&1 | tail -1 || fail=1

echo "== 4/6 契约闸门自检"
python3 scripts/contract_guard.py --self-test 2>&1 | tail -1 || fail=1

echo "== 5/6 交叉平台 lint"
python3 scripts/lint_cross_platform.py | tail -1 || fail=1

echo "== 6/6 fixtures 完整性"
n=$(ls tests/fixtures/*.json 2>/dev/null | wc -l | tr -d ' ')
if [ "$n" -ge 6 ]; then
  echo "PASS: fixtures $n 个"
else
  echo "FAIL: fixtures 仅 $n 个（要求 >=6）"; fail=1
fi

echo ""
if [ "$fail" -eq 0 ]; then
  echo "== 回归总结果：PASS =="
  exit 0
else
  echo "== 回归总结果：FAIL =="
  exit 1
fi
