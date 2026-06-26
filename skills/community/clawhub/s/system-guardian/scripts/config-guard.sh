#!/bin/bash
# 金刚罩 — Config Guard
# 配置变更防护：语法校验 + 环境变量检查 + 关键字段检查
set -euo pipefail

OPENCLAW_DIR="${HOME}/.openclaw"
CONFIG="${OPENCLAW_DIR}/openclaw.json"
ENV_FILE="${OPENCLAW_DIR}/.env"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

ok()  { echo -e "${GREEN}[  OK  ]${NC} $1"; }
warn(){ echo -e "${YELLOW}[ WARN ]${NC} $1"; }
fail(){ echo -e "${RED}[ FAIL ]${NC} $1"; }
info(){ echo -e "${CYAN}[ INFO ]${NC} $1"; }

ERRORS=0
WARNINGS=0

# ─── 1. JSON syntax ───
info "检查 JSON 语法..."
if python3 -c "import json; json.load(open('$CONFIG'))" 2>/dev/null; then
    ok "JSON 语法正确"
else
    fail "JSON 语法错误！"
    python3 -c "import json; json.load(open('$CONFIG'))" 2>&1 || true
    ERRORS=$((ERRORS + 1))
fi

# ─── 2. OpenClaw validate ───
info "运行 openclaw config validate..."
if openclaw config validate 2>&1 | grep -q "valid"; then
    ok "OpenClaw 配置校验通过"
else
    fail "OpenClaw 配置校验失败"
    openclaw config validate 2>&1
    ERRORS=$((ERRORS + 1))
fi

# ─── 3. Required fields ───
info "检查必需字段..."
for field in gateway channels agents; do
    if python3 -c "import json; d=json.load(open('$CONFIG')); assert '$field' in d" 2>/dev/null; then
        ok "字段 '$field' 存在"
    else
        fail "缺少必需字段: '$field'"
        ERRORS=$((ERRORS + 1))
    fi
done

# ─── 4. Environment variable references ───
info "检查环境变量引用..."
REFS=$(grep -oE '\$\{[A-Z_]+\}' "$CONFIG" 2>/dev/null | sort -u | sed 's/\${\(.*\)}/\1/') || true
if [ -n "$REFS" ]; then
    # env-based mode: config uses ${VAR} references
    info "检测到 env-based 配置模式"
    if [ -f "$ENV_FILE" ]; then
        MISSING=0
        for var in $REFS; do
            if grep -q "^${var}=" "$ENV_FILE" 2>/dev/null; then
                ok "  \${$var} → 已定义"
            else
                warn "  \${$var} → 未在 .env 中定义"
                MISSING=$((MISSING + 1))
            fi
        done
        if [ "$MISSING" -gt 0 ]; then
            WARNINGS=$((WARNINGS + MISSING))
        fi
    else
        fail "配置中引用了 \${VAR} 变量，但 .env 文件不存在！"
        fail "建议：创建 ${ENV_FILE} 并定义所需变量，或改用 openclaw.json 内联写法"
        ERRORS=$((ERRORS + 1))
    fi
else
    # inline mode: no ${VAR} references, keys are directly in openclaw.json
    ok "配置使用内联模式（无 \${VAR} 引用）"
    if [ -f "$ENV_FILE" ]; then
        info ".env 文件存在但未被配置引用（仅作备份用）"
    fi
fi

# ─── 5. Port conflict check ───
info "检查端口冲突..."
PORT=$(python3 -c "import json; d=json.load(open('$CONFIG')); print(d.get('gateway',{}).get('port', 18789))" 2>/dev/null || echo "18789")
CURRENT_PID=$(lsof -ti tcp:"$PORT" 2>/dev/null || true)
GATEWAY_PID=$(pgrep -f "openclaw.*gateway" 2>/dev/null | head -1 || true)
if [ -n "$CURRENT_PID" ]; then
    if [ "$CURRENT_PID" = "$GATEWAY_PID" ]; then
        ok "端口 $PORT 被当前 Gateway (pid $CURRENT_PID) 占用"
    else
        warn "端口 $PORT 被 pid $CURRENT_PID 占用（非 Gateway 进程）"
        WARNINGS=$((WARNINGS + 1))
    fi
else
    ok "端口 $PORT 可用"
fi

# ─── 6. Disk space ───
info "检查磁盘空间..."
AVAIL_GB=$(df -g "$HOME" 2>/dev/null | tail -1 | awk '{print $4}')
if [ -n "$AVAIL_GB" ] && [ "$AVAIL_GB" -lt 5 ]; then
    fail "磁盘可用空间不足 5GB！(当前: ${AVAIL_GB}GB)"
    ERRORS=$((ERRORS + 1))
elif [ -n "$AVAIL_GB" ] && [ "$AVAIL_GB" -lt 10 ]; then
    warn "磁盘可用空间低于 10GB (当前: ${AVAIL_GB}GB)"
    WARNINGS=$((WARNINGS + 1))
else
    ok "磁盘空间充足 (${AVAIL_GB}GB 可用)"
fi

# ─── Summary ───
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ "$ERRORS" -gt 0 ]; then
    fail "检查完成: $ERRORS 错误, $WARNINGS 警告 — 不建议重启"
    exit 1
elif [ "$WARNINGS" -gt 0 ]; then
    warn "检查完成: 0 错误, $WARNINGS 警告 — 建议检查后再重启"
    exit 0
else
    ok "检查完成: 全部通过 ✅ — 可以安全重启"
    exit 0
fi
