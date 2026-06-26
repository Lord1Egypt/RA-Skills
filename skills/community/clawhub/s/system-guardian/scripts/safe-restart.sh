#!/bin/bash
# 金刚罩 — Safe Restart
# 安全重启 OpenClaw Gateway：校验 → 备份 → 重启 → 健康检查 → 失败回滚
set -euo pipefail

OPENCLAW_DIR="${HOME}/.openclaw"
CONFIG="${OPENCLAW_DIR}/openclaw.json"
BACKUP_DIR="${OPENCLAW_DIR}/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/openclaw.json.${TIMESTAMP}.bak"
MAX_BACKUPS=10
WAIT_SECONDS=15
RETRY_WAIT=10

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

log() { echo -e "${CYAN}[guardian]${NC} $1"; }
ok()  { echo -e "${GREEN}[  OK  ]${NC} $1"; }
warn(){ echo -e "${YELLOW}[ WARN ]${NC} $1"; }
fail(){ echo -e "${RED}[ FAIL ]${NC} $1"; }

# ─── Step 1: Pre-validate ───
log "Step 1/5: 校验配置文件..."
if openclaw config validate 2>&1 | grep -q "valid"; then
    ok "配置校验通过"
else
    fail "配置校验失败！中止重启。"
    openclaw config validate 2>&1
    exit 1
fi

# ─── Step 2: Check env vars ───
log "Step 2/5: 检查环境变量引用..."
ENV_FILE="${OPENCLAW_DIR}/.env"
# Detect if config uses ${VAR} references (env-based) or inline values (default)
VAR_REFS=$(grep -oE '\$\{[A-Z_]+\}' "$CONFIG" 2>/dev/null | sort -u | sed 's/\${\(.*\)}/\1/') || true
if [ -n "$VAR_REFS" ]; then
    # Config uses env var references → need .env file
    if [ -f "$ENV_FILE" ]; then
        MISSING_VARS=()
        for var in $VAR_REFS; do
            if ! grep -q "^${var}=" "$ENV_FILE" 2>/dev/null; then
                MISSING_VARS+=("$var")
            fi
        done
        if [ ${#MISSING_VARS[@]} -gt 0 ]; then
            warn "以下环境变量在 .env 中未定义: ${MISSING_VARS[*]}"
            warn "Gateway 可能无法正确读取这些值"
        else
            ok "所有环境变量引用已确认 (env-based 模式)"
        fi
    else
        warn "配置中使用了 \${VAR} 引用，但 .env 文件不存在！"
        warn "建议：创建 ${ENV_FILE} 或改用 openclaw.json 内联配置"
    fi
else
    # Config uses inline values (default mode) → no .env needed
    ok "配置使用内联模式（无 \${VAR} 引用）"
    if [ -f "$ENV_FILE" ]; then
        ok ".env 文件存在（可选备份）"
    fi
fi

# ─── Step 3: Backup ───
log "Step 3/5: 备份配置文件..."
mkdir -p "$BACKUP_DIR"

# 3a: openclaw.json
cp "$CONFIG" "$BACKUP_FILE"
ok "备份 openclaw.json → $(basename "$BACKUP_FILE")"

# 3b: .env
ENV_BACKUP="${BACKUP_DIR}/env.${TIMESTAMP}.bak"
if [ -f "$ENV_FILE" ]; then
    cp "$ENV_FILE" "$ENV_BACKUP"
    ok "备份 .env → $(basename "$ENV_BACKUP")"
fi

# 3c: LaunchAgent plist
PLIST_SRC="${HOME}/Library/LaunchAgents/ai.openclaw.gateway.plist"
PLIST_BACKUP="${BACKUP_DIR}/ai.openclaw.gateway.plist.${TIMESTAMP}.bak"
if [ -f "$PLIST_SRC" ]; then
    cp "$PLIST_SRC" "$PLIST_BACKUP"
    ok "备份 LaunchAgent plist → $(basename "$PLIST_BACKUP")"
fi

# Clean old backups (keep latest MAX_BACKUPS sets)
for pattern in "openclaw.json.*.bak" "env.*.bak" "ai.openclaw.gateway.plist.*.bak"; do
    BAK_COUNT=$(ls -1 "$BACKUP_DIR"/$pattern 2>/dev/null | wc -l | tr -d ' ')
    if [ "$BAK_COUNT" -gt "$MAX_BACKUPS" ]; then
        EXCESS=$((BAK_COUNT - MAX_BACKUPS))
        ls -1t "$BACKUP_DIR"/$pattern | tail -n "$EXCESS" | xargs rm -f
        log "清理旧备份 ($pattern): 删除 $EXCESS 个"
    fi
done

# ─── Step 4: Restart ───
log "Step 4/5: 重启 Gateway..."
openclaw gateway restart 2>&1
log "等待 ${WAIT_SECONDS} 秒让 Gateway 启动..."
sleep "$WAIT_SECONDS"

# ─── Step 5: Health check ───
log "Step 5/5: 健康检查..."
STATUS=$(openclaw gateway status 2>&1)
if echo "$STATUS" | grep -q "running"; then
    ok "Gateway 运行正常 ✅"
    echo "$STATUS" | grep -E "Runtime|Listening"
    echo ""
    ok "安全重启完成！"
    exit 0
fi

# ─── Rollback ───
fail "Gateway 未正常启动！开始回滚..."
warn "恢复 openclaw.json 备份..."
cp "$BACKUP_FILE" "$CONFIG"
if [ -f "$ENV_BACKUP" ]; then
    warn "恢复 .env 备份..."
    cp "$ENV_BACKUP" "$ENV_FILE"
fi
if [ -f "$PLIST_BACKUP" ]; then
    warn "恢复 LaunchAgent plist 备份..."
    cp "$PLIST_BACKUP" "$PLIST_SRC"
fi
log "所有备份已恢复，尝试再次重启..."
openclaw gateway restart 2>&1
sleep "$RETRY_WAIT"

STATUS=$(openclaw gateway status 2>&1)
if echo "$STATUS" | grep -q "running"; then
    warn "回滚成功，Gateway 已恢复运行"
    warn "请检查之前的配置变更是否有问题"
    exit 2
fi

fail "回滚后 Gateway 仍然无法启动！"
fail "需要人工介入。最近的备份文件在: $BACKUP_DIR"
fail "手动恢复: cp $BACKUP_DIR/<选择一个.bak> $CONFIG"
exit 3
