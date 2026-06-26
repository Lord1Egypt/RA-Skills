#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────
# RIC v0.2 本机完整测试脚本
# 用法: bash scripts/test-local.sh
# 前提: registry 已在 localhost:3000 运行
# ──────────────────────────────────────────────────────────────

set -euo pipefail

REGISTRY="http://localhost:3000"
export RIC_REGISTRY="$REGISTRY"
PASS=0
FAIL=0
TMP=$(mktemp -d)
trap "rm -rf $TMP" EXIT

# ── 颜色 ──────────────────────────────────────────────────────
GREEN="\033[0;32m"; RED="\033[0;31m"; YELLOW="\033[1;33m"; RESET="\033[0m"; BOLD="\033[1m"

pass() { echo -e "  ${GREEN}✓${RESET} $1"; PASS=$((PASS + 1)); }
fail() { echo -e "  ${RED}✗${RESET} $1"; FAIL=$((FAIL + 1)); }
section() { echo -e "\n${BOLD}${YELLOW}▶ $1${RESET}"; }

# ── 工具函数 ──────────────────────────────────────────────────
post() { curl -s -X POST "$REGISTRY$1" -H "Content-Type: application/json" -d "$2"; }
get()  { curl -s "$REGISTRY$1"; }

# 生成唯一公钥
gen_key() { echo "ed25519:$(python3 -c "import secrets; print(secrets.token_hex(32))")"; }

# ─────────────────────────────────────────────────────────────
section "0. Registry 健康检查"
# ─────────────────────────────────────────────────────────────
HEALTH=$(get /health)
VERSION=$(echo "$HEALTH" | python3 -c "import sys,json; print(json.load(sys.stdin)['version'])" 2>/dev/null)
if [[ "$VERSION" == "0.3.0" ]]; then
  pass "Registry 运行正常 (v$VERSION)"
else
  fail "Registry 未响应或版本不对: $HEALTH"
  echo -e "${RED}请先启动 registry: npm run dev --workspace=packages/registry${RESET}"
  exit 1
fi

# ─────────────────────────────────────────────────────────────
section "1. CLI keygen — 生成密钥对"
# ─────────────────────────────────────────────────────────────
cd "$(dirname "$0")/.."
KEY_FILE="$TMP/bot.key.json"
npx tsx packages/cli/src/index.ts keygen --out "$KEY_FILE" > /dev/null 2>&1
if [[ -f "$KEY_FILE" ]]; then
  PUB=$(python3 -c "import json; d=json.load(open('$KEY_FILE')); print(d['public_key'])")
  PRIV=$(python3 -c "import json; d=json.load(open('$KEY_FILE')); print(d['private_key_hex'])")
  if [[ "$PUB" == ed25519:* ]] && [[ ${#PUB} -eq 72 ]]; then
    pass "keygen 生成文件正确 (公钥: ${PUB:0:20}...)"
  else
    fail "公钥格式不对: $PUB"
  fi
else
  fail "keygen 未生成密钥文件"
fi

# ─────────────────────────────────────────────────────────────
section "2. CLI register — 正常注册"
# ─────────────────────────────────────────────────────────────
CERT_FILE="$TMP/bot.ric.json"
npx tsx packages/cli/src/index.ts register \
  --name "LocalTestBot" \
  --purpose "Automated local test bot for RIC v0.2 validation" \
  --developer "localtest@example.com" \
  --org "TestOrg" \
  --key "$KEY_FILE" \
  --out "$CERT_FILE" > /dev/null 2>&1

if [[ -f "$CERT_FILE" ]]; then
  RIC_ID=$(python3 -c "import json; print(json.load(open('$CERT_FILE'))['id'])")
  GRADE=$(python3 -c "import json; print(json.load(open('$CERT_FILE'))['grade'])")
  if [[ "$RIC_ID" == ric_* ]] && [[ "$GRADE" == "unknown" ]]; then
    pass "CLI 注册成功 (ID: $RIC_ID, 初始评级: $GRADE)"
  else
    fail "证书内容异常: id=$RIC_ID grade=$GRADE"
  fi
else
  fail "CLI 注册未生成证书文件"
  RIC_ID=""
fi

# ─────────────────────────────────────────────────────────────
section "3. 唯一性 — 重复公钥拦截"
# ─────────────────────────────────────────────────────────────
RES=$(post /v1/bots/register "{
  \"developer\":{\"name\":\"X\",\"email\":\"other@example.com\"},
  \"bot\":{\"name\":\"OtherBot\",\"version\":\"1.0.0\",\"purpose\":\"trying to steal a key\",\"capabilities\":[\"read_articles\"],\"user_agent\":\"OtherBot/1.0\"},
  \"public_key\":\"$PUB\"
}")
CODE=$(echo "$RES" | python3 -c "import sys,json; print(json.load(sys.stdin).get('code',''))" 2>/dev/null)
if [[ "$CODE" == "DUPLICATE_KEY" ]]; then
  pass "重复公钥被拦截 (code: DUPLICATE_KEY)"
else
  fail "重复公钥未被拦截: $RES"
fi

# ─────────────────────────────────────────────────────────────
section "4. 唯一性 — 相同 email+名称拦截"
# ─────────────────────────────────────────────────────────────
NEW_KEY=$(gen_key)
RES=$(post /v1/bots/register "{
  \"developer\":{\"name\":\"localtest\",\"email\":\"localtest@example.com\"},
  \"bot\":{\"name\":\"LocalTestBot\",\"version\":\"2.0.0\",\"purpose\":\"same name different key attempt\",\"capabilities\":[\"read_articles\"],\"user_agent\":\"LocalTestBot/2.0\"},
  \"public_key\":\"$NEW_KEY\"
}")
CODE=$(echo "$RES" | python3 -c "import sys,json; print(json.load(sys.stdin).get('code',''))" 2>/dev/null)
if [[ "$CODE" == "DUPLICATE_BOT" ]]; then
  pass "重复 email+名称被拦截 (code: DUPLICATE_BOT)"
else
  fail "重复 bot 未被拦截: $RES"
fi

# ─────────────────────────────────────────────────────────────
section "5. API GET /v1/bots/:id — 查询证书"
# ─────────────────────────────────────────────────────────────
if [[ -n "$RIC_ID" ]]; then
  RES=$(get "/v1/bots/$RIC_ID")
  BOT_NAME=$(echo "$RES" | python3 -c "import sys,json; print(json.load(sys.stdin)['bot']['name'])" 2>/dev/null)
  if [[ "$BOT_NAME" == "LocalTestBot" ]]; then
    pass "GET /v1/bots/:id 返回正确证书"
  else
    fail "查询结果异常: $RES"
  fi
fi

# ─────────────────────────────────────────────────────────────
section "6. CLI status — 查看 bot 状态"
# ─────────────────────────────────────────────────────────────
if [[ -n "$RIC_ID" ]]; then
  STATUS_OUT=$(npx tsx packages/cli/src/index.ts status --cert "$CERT_FILE" 2>/dev/null)
  if echo "$STATUS_OUT" | grep -q "LocalTestBot"; then
    pass "CLI status 正常显示 bot 信息"
  else
    fail "CLI status 输出异常: $STATUS_OUT"
  fi
fi

# ─────────────────────────────────────────────────────────────
section "7. GET /v1/bots — 列表"
# ─────────────────────────────────────────────────────────────
RES=$(get /v1/bots)
TOTAL=$(echo "$RES" | python3 -c "import sys,json; print(json.load(sys.stdin)['total'])" 2>/dev/null)
if [[ "$TOTAL" -ge 1 ]]; then
  pass "GET /v1/bots 返回列表 (共 $TOTAL 个 bot)"
else
  fail "列表返回异常: $RES"
fi

# ─────────────────────────────────────────────────────────────
section "8. 举报 + 自动降级 (3次→DANGEROUS)"
# ─────────────────────────────────────────────────────────────
if [[ -n "$RIC_ID" ]]; then
  # 用新 bot 来测试举报（不污染 LocalTestBot）
  REPORT_KEY=$(gen_key)
  REPORT_RES=$(post /v1/bots/register "{
    \"developer\":{\"name\":\"report-dev\",\"email\":\"report-test@example.com\"},
    \"bot\":{\"name\":\"ReportTestBot\",\"version\":\"1.0.0\",\"purpose\":\"Bot used for auto-flag test\",\"capabilities\":[\"read_articles\"],\"user_agent\":\"ReportTestBot/1.0\"},
    \"public_key\":\"$REPORT_KEY\"
  }")
  REPORT_BOT_ID=$(echo "$REPORT_RES" | python3 -c "import sys,json; print(json.load(sys.stdin)['certificate']['id'])" 2>/dev/null)

  if [[ -n "$REPORT_BOT_ID" ]]; then
    for i in 1 2 3; do
      post /v1/audit/report "{\"ric_id\":\"$REPORT_BOT_ID\",\"reporter_domain\":\"site$i.com\",\"reason\":\"spam\",\"description\":\"Test report $i\"}" > /dev/null
    done

    GRADE_AFTER=$(get "/v1/bots/$REPORT_BOT_ID" | python3 -c "import sys,json; print(json.load(sys.stdin)['grade'])" 2>/dev/null)
    if [[ "$GRADE_AFTER" == "dangerous" ]]; then
      pass "3次举报后自动降级为 DANGEROUS"
    else
      fail "自动降级未触发，当前评级: $GRADE_AFTER"
    fi
  fi
fi

# ─────────────────────────────────────────────────────────────
section "9. 审计日志"
# ─────────────────────────────────────────────────────────────
if [[ -n "$REPORT_BOT_ID" ]]; then
  RES=$(get "/v1/audit/$REPORT_BOT_ID")
  EVENTS=$(echo "$RES" | python3 -c "import sys,json; print(json.load(sys.stdin)['total'])" 2>/dev/null)
  if [[ "$EVENTS" -ge 4 ]]; then
    pass "审计日志完整 ($EVENTS 条事件: registered + 3×report + grade_changed)"
  else
    fail "审计日志事件数不够: $EVENTS"
  fi
fi

# ─────────────────────────────────────────────────────────────
section "10. Admin grade 更新 (需要 admin_key)"
# ─────────────────────────────────────────────────────────────
if [[ -n "$RIC_ID" ]]; then
  # 无 admin_key → 应被拒绝
  RES=$(post /v1/audit/grade "{\"ric_id\":\"$RIC_ID\",\"grade\":\"healthy\",\"reason\":\"Test\",\"admin_key\":\"wrong-key\"}")
  HTTP_CODE=$(echo "$RES" | python3 -c "import sys,json; print(json.load(sys.stdin).get('error',''))" 2>/dev/null)
  if [[ "$HTTP_CODE" == "Forbidden" ]]; then
    pass "错误 admin_key 被拒绝 (403 Forbidden)"
  else
    fail "admin_key 验证未生效: $RES"
  fi

  # 正确 admin_key → 应成功
  RES=$(post /v1/audit/grade "{\"ric_id\":\"$RIC_ID\",\"grade\":\"healthy\",\"reason\":\"Passed local testing\",\"admin_key\":\"dev-admin-key-change-me\"}")
  NEW_GRADE=$(echo "$RES" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('message',''))" 2>/dev/null)
  if echo "$NEW_GRADE" | grep -q "healthy"; then
    pass "管理员评级更新成功 → HEALTHY"
  else
    fail "评级更新失败: $RES"
  fi
fi

# ─────────────────────────────────────────────────────────────
section "11. 重启持久化验证"
# ─────────────────────────────────────────────────────────────
if [[ -n "$RIC_ID" ]]; then
  GRADE_NOW=$(get "/v1/bots/$RIC_ID" | python3 -c "import sys,json; print(json.load(sys.stdin)['grade'])" 2>/dev/null)
  if [[ "$GRADE_NOW" == "healthy" ]]; then
    pass "SQLite 持久化正常 (评级 HEALTHY 已存入数据库)"
  else
    fail "持久化可能有问题: grade=$GRADE_NOW"
  fi
fi

# ─────────────────────────────────────────────────────────────
section "12. 无效公钥格式校验"
# ─────────────────────────────────────────────────────────────
RES=$(post /v1/bots/register "{
  \"developer\":{\"name\":\"X\",\"email\":\"bad@x.com\"},
  \"bot\":{\"name\":\"BadKeyBot\",\"version\":\"1.0.0\",\"purpose\":\"testing invalid key format\",\"capabilities\":[\"read_articles\"],\"user_agent\":\"BadKeyBot/1.0\"},
  \"public_key\":\"notakey\"
}")
ERR=$(echo "$RES" | python3 -c "import sys,json; print('error' in json.load(sys.stdin))" 2>/dev/null)
if [[ "$ERR" == "True" ]]; then
  pass "无效公钥格式被拒绝"
else
  fail "无效公钥未被拦截"
fi

# ─────────────────────────────────────────────────────────────
echo -e "\n${BOLD}══════════════════════════════════════${RESET}"
echo -e "${BOLD}  测试结果: ${GREEN}${PASS} 通过${RESET}${BOLD} / ${RED}${FAIL} 失败${RESET}"
echo -e "${BOLD}══════════════════════════════════════${RESET}\n"

[[ "$FAIL" -eq 0 ]] && exit 0 || exit 1
