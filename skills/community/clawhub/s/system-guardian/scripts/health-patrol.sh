#!/bin/bash
# 金刚罩 — Health Patrol v1.1
# 系统健康巡检：进程 + 磁盘 + Session + 内存DB + 备份 + Cron健康 + 临时文件 + 插件 + 审计 + 基线 + 自动清理
set -uo pipefail

OPENCLAW_DIR="${HOME}/.openclaw"
SESSIONS_DIR="${OPENCLAW_DIR}/agents/main/sessions"
MEMORY_DIR="${OPENCLAW_DIR}/memory"
BACKUP_DIR="${OPENCLAW_DIR}/backups"
DATA_DIR="${OPENCLAW_DIR}/data"
GUARDIAN_DATA="${OPENCLAW_DIR}/data/system-guardian"
BASELINE_CSV="${GUARDIAN_DATA}/baseline.csv"
AUDIT_LOG="${GUARDIAN_DATA}/config-audit.log"
CONFIG="${OPENCLAW_DIR}/openclaw.json"
CONFIG_HASH_FILE="${GUARDIAN_DATA}/.config-hash"

# Auto-cleanup settings
SESSION_MAX_AGE_DAYS=14
BACKUP_MAX_COUNT=10
TMP_MAX_AGE_DAYS=1

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

ok()      { echo -e "${GREEN}[   OK   ]${NC} $1"; }
warn()    { echo -e "${YELLOW}[ WARNING]${NC} $1"; }
critical(){ echo -e "${RED}[CRITICAL]${NC} $1"; }
info()    { echo -e "${CYAN}[  INFO  ]${NC} $1"; }

WARNINGS=0
CRITICALS=0

# Ensure data dir exists
mkdir -p "$GUARDIAN_DATA"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔱  金刚罩 — Health Patrol v1.1"
echo "   $(date '+%Y-%m-%d %H:%M:%S %Z')"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# ─── 1. Gateway Process ───
info "1/13 Gateway 进程状态"
GW_STATUS=$(openclaw gateway status 2>&1)
GW_MEM_MB=0
if echo "$GW_STATUS" | grep -q "running"; then
    GW_PID=$(echo "$GW_STATUS" | grep -oE "pid [0-9]+" | grep -oE "[0-9]+")
    if [ -n "$GW_PID" ]; then
        GW_MEM_MB=$(ps -o rss= -p "$GW_PID" 2>/dev/null | awk '{printf "%.0f", $1/1024}')
        if [ -n "$GW_MEM_MB" ]; then
            if [ "$GW_MEM_MB" -gt 1536 ]; then
                critical "Gateway 内存占用 ${GW_MEM_MB}MB (>1.5GB)，建议立即重启"
                CRITICALS=$((CRITICALS + 1))
            elif [ "$GW_MEM_MB" -gt 1024 ]; then
                warn "Gateway 内存占用 ${GW_MEM_MB}MB (>1GB)"
                WARNINGS=$((WARNINGS + 1))
            else
                ok "Gateway 运行中 (pid ${GW_PID}, ${GW_MEM_MB}MB)"
            fi
        else
            GW_MEM_MB=0
            ok "Gateway 运行中 (pid ${GW_PID})"
        fi
    fi
else
    critical "Gateway 未运行！"
    CRITICALS=$((CRITICALS + 1))
fi

# ─── 2. Disk Space ───
info "2/13 磁盘空间"
AVAIL_GB=$(df -g "$HOME" 2>/dev/null | tail -1 | awk '{print $4}')
USED_PCT=$(df -g "$HOME" 2>/dev/null | tail -1 | awk '{print $5}' | tr -d '%')
if [ -n "$AVAIL_GB" ]; then
    if [ "$AVAIL_GB" -lt 5 ]; then
        critical "磁盘可用空间仅 ${AVAIL_GB}GB！(使用率 ${USED_PCT}%)"
        CRITICALS=$((CRITICALS + 1))
    elif [ "$AVAIL_GB" -lt 10 ]; then
        warn "磁盘可用空间 ${AVAIL_GB}GB (使用率 ${USED_PCT}%)"
        WARNINGS=$((WARNINGS + 1))
    else
        ok "磁盘空间 ${AVAIL_GB}GB 可用 (使用率 ${USED_PCT}%)"
    fi
fi

# ─── 3. OpenClaw Directory Size ───
info "3/13 OpenClaw 目录空间"
OC_SIZE=$(du -sh "$OPENCLAW_DIR" 2>/dev/null | awk '{print $1}')
ok "OpenClaw 总占用: ${OC_SIZE}"

for subdir in agents/main/sessions memory plugins workspace data backups; do
    D="${OPENCLAW_DIR}/${subdir}"
    if [ -d "$D" ]; then
        SIZE=$(du -sh "$D" 2>/dev/null | awk '{print $1}')
        echo "     └─ ${subdir}: ${SIZE}"
    fi
done

# ─── 4. Session Files ───
info "4/13 Session 文件"
SESSION_COUNT=0
if [ -d "$SESSIONS_DIR" ]; then
    SESSION_COUNT=$(ls -1 "$SESSIONS_DIR"/*.jsonl 2>/dev/null | wc -l | tr -d ' ')
    SESSIONS_SIZE=$(du -sh "$SESSIONS_DIR" 2>/dev/null | awk '{print $1}')

    if [ "$SESSION_COUNT" -gt 50 ]; then
        warn "Session 文件 ${SESSION_COUNT} 个 (${SESSIONS_SIZE})，建议清理旧 session"
        WARNINGS=$((WARNINGS + 1))
    else
        ok "Session 文件 ${SESSION_COUNT} 个 (${SESSIONS_SIZE})"
    fi

    OLD_SESSIONS=$(find "$SESSIONS_DIR" -name "*.jsonl" -mtime +7 2>/dev/null | wc -l | tr -d ' ')
    if [ "$OLD_SESSIONS" -gt 0 ]; then
        info "  └─ 超过 7 天的旧 session: ${OLD_SESSIONS} 个"
    fi
else
    ok "暂无 session 文件"
fi

# ─── 5. Memory Database ───
info "5/13 记忆数据库"
MEM_DB_SIZE="0"
if [ -d "$MEMORY_DIR" ]; then
    MEM_DB_SIZE=$(du -sh "$MEMORY_DIR" 2>/dev/null | awk '{print $1}')
    ok "记忆数据库: ${MEM_DB_SIZE}"
else
    ok "记忆数据库未创建"
fi

# ─── 6. Backup Management ───
info "6/13 备份文件"
BACKUP_COUNT=0
if [ -d "$BACKUP_DIR" ]; then
    BACKUP_COUNT=$(ls -1 "$BACKUP_DIR"/*.bak 2>/dev/null | wc -l | tr -d ' ')
    BACKUP_SIZE=$(du -sh "$BACKUP_DIR" 2>/dev/null | awk '{print $1}')

    if [ "$BACKUP_COUNT" -gt 20 ]; then
        warn "备份文件 ${BACKUP_COUNT} 个 (${BACKUP_SIZE})，建议清理"
        WARNINGS=$((WARNINGS + 1))
    else
        ok "备份文件 ${BACKUP_COUNT} 个 (${BACKUP_SIZE})"
    fi

    LATEST=$(ls -1t "$BACKUP_DIR"/*.bak 2>/dev/null | head -1)
    if [ -n "$LATEST" ]; then
        info "  └─ 最新备份: $(basename "$LATEST")"
    fi
else
    warn "备份目录不存在"
    WARNINGS=$((WARNINGS + 1))
fi

# ─── 7. Cron 任务健康监控 (NEW) ───
info "7/13 Cron 任务健康"
CRON_LIST=$(openclaw cron list 2>&1 | { grep -v "^\[plugins\]" || true; })
CRON_TOTAL=$(echo "$CRON_LIST" | { grep -cE "cron |at " || true; }) || CRON_TOTAL=0
CRON_ERRORS=$(echo "$CRON_LIST" | { grep -c "error" || true; }) || CRON_ERRORS=0
CRON_OK=$(echo "$CRON_LIST" | { grep -c " ok " || true; }) || CRON_OK=0

if [ "$CRON_ERRORS" -gt 0 ]; then
    warn "Cron 任务: ${CRON_TOTAL} 个，其中 ${CRON_ERRORS} 个报错"
    WARNINGS=$((WARNINGS + 1))
    # List the failed ones
    echo "$CRON_LIST" | { grep "error" || true; } | while IFS= read -r line; do
        NAME=$(echo "$line" | awk '{print $2}')
        echo "     └─ ❌ ${NAME}"
    done
else
    ok "Cron 任务: ${CRON_TOTAL} 个，${CRON_OK} 个正常"
fi

# ─── 8. 插件健康检查 (NEW) ───
info "8/13 插件状态"
PLUGIN_DIR="${OPENCLAW_DIR}/plugins"
if [ -d "$PLUGIN_DIR" ]; then
    PLUGIN_COUNT=0
    PLUGIN_ISSUES=0
    for pdir in "$PLUGIN_DIR"/*/; do
        [ -d "$pdir" ] || continue
        PNAME=$(basename "$pdir")
        PLUGIN_COUNT=$((PLUGIN_COUNT + 1))

        # Check basics: does it have an entry point?
        HAS_ENTRY=false
        for f in "index.js" "index.ts" "dist/index.js" "package.json"; do
            if [ -f "${pdir}${f}" ]; then
                HAS_ENTRY=true
                break
            fi
        done

        # Check if it appears in gateway logs as registered
        if echo "$GW_STATUS" | grep -qi "$PNAME"; then
            ok "  插件 ${PNAME}: 已加载"
        elif [ "$HAS_ENTRY" = true ]; then
            ok "  插件 ${PNAME}: 已安装"
        else
            warn "  插件 ${PNAME}: 缺少入口文件"
            PLUGIN_ISSUES=$((PLUGIN_ISSUES + 1))
        fi
    done

    if [ "$PLUGIN_ISSUES" -gt 0 ]; then
        warn "插件: ${PLUGIN_COUNT} 个安装，${PLUGIN_ISSUES} 个有问题"
        WARNINGS=$((WARNINGS + 1))
    else
        ok "插件: ${PLUGIN_COUNT} 个，全部正常"
    fi
else
    ok "无自定义插件"
fi

# ─── 9. 配置变更审计 (NEW) ───
info "9/13 配置变更审计"
if [ -f "$CONFIG" ]; then
    CURRENT_HASH=$(md5 -q "$CONFIG" 2>/dev/null || md5sum "$CONFIG" 2>/dev/null | awk '{print $1}')

    if [ -f "$CONFIG_HASH_FILE" ]; then
        PREV_HASH=$(cat "$CONFIG_HASH_FILE")
        if [ "$CURRENT_HASH" != "$PREV_HASH" ]; then
            warn "openclaw.json 自上次巡检后已变更"
            WARNINGS=$((WARNINGS + 1))
            # Log the change
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] CONFIG CHANGED: hash ${PREV_HASH} → ${CURRENT_HASH}" >> "$AUDIT_LOG"
            # Save a snapshot for diff
            if [ -f "${GUARDIAN_DATA}/.config-snapshot.json" ]; then
                DIFF_LINES=$(diff "${GUARDIAN_DATA}/.config-snapshot.json" "$CONFIG" 2>/dev/null | head -20)
                if [ -n "$DIFF_LINES" ]; then
                    echo "[$(date '+%Y-%m-%d %H:%M:%S')] DIFF:" >> "$AUDIT_LOG"
                    echo "$DIFF_LINES" >> "$AUDIT_LOG"
                fi
            fi
            cp "$CONFIG" "${GUARDIAN_DATA}/.config-snapshot.json"
        else
            ok "openclaw.json 未变更"
        fi
    else
        info "首次记录配置 hash"
        cp "$CONFIG" "${GUARDIAN_DATA}/.config-snapshot.json"
    fi
    echo "$CURRENT_HASH" > "$CONFIG_HASH_FILE"
else
    critical "openclaw.json 不存在！"
    CRITICALS=$((CRITICALS + 1))
fi

# ─── 10. Temp Files ───
info "10/13 临时文件"
TMP_COUNT=$(find /tmp -maxdepth 1 \( -name "token-ledger-*" -o -name "morning-ledger*" -o -name "openclaw-*" -o -name "yt_*" \) 2>/dev/null | wc -l | tr -d ' ')
if [ "$TMP_COUNT" -gt 10 ]; then
    warn "临时文件 ${TMP_COUNT} 个，清理中..."
    find /tmp -maxdepth 1 -name "token-ledger-*" -mtime +${TMP_MAX_AGE_DAYS} -delete 2>/dev/null || true
    find /tmp -maxdepth 1 -name "morning-ledger*" -mtime +${TMP_MAX_AGE_DAYS} -delete 2>/dev/null || true
    find /tmp -maxdepth 1 -name "yt_*" -mtime +${TMP_MAX_AGE_DAYS} -delete 2>/dev/null || true
    ok "已清理过期临时文件"
else
    ok "临时文件 ${TMP_COUNT} 个"
fi

# ─── 11. 自动清理 (NEW) ───
info "11/13 自动清理"
CLEANED=0

# 11a: Old sessions (> SESSION_MAX_AGE_DAYS days)
if [ -d "$SESSIONS_DIR" ]; then
    OLD_COUNT=$(find "$SESSIONS_DIR" -name "*.jsonl" -mtime +${SESSION_MAX_AGE_DAYS} 2>/dev/null | wc -l | tr -d ' ')
    if [ "$OLD_COUNT" -gt 0 ]; then
        find "$SESSIONS_DIR" -name "*.jsonl" -mtime +${SESSION_MAX_AGE_DAYS} -delete 2>/dev/null || true
        ok "清理 ${OLD_COUNT} 个超过 ${SESSION_MAX_AGE_DAYS} 天的旧 session"
        CLEANED=$((CLEANED + OLD_COUNT))
    fi
fi

# 11b: Excess backups (keep latest BACKUP_MAX_COUNT per type)
if [ -d "$BACKUP_DIR" ]; then
    for pattern in "openclaw.json.*.bak" "env.*.bak" "ai.openclaw.gateway.plist.*.bak"; do
        BAK_N=$(ls -1 "$BACKUP_DIR"/$pattern 2>/dev/null | wc -l | tr -d ' ')
        if [ "$BAK_N" -gt "$BACKUP_MAX_COUNT" ]; then
            EXCESS=$((BAK_N - BACKUP_MAX_COUNT))
            ls -1t "$BACKUP_DIR"/$pattern | tail -n "$EXCESS" | xargs rm -f
            ok "清理 $EXCESS 个多余备份 ($pattern)"
            CLEANED=$((CLEANED + EXCESS))
        fi
    done
fi

# 11c: Gateway log rotation (keep last 7 days)
OLD_LOGS=$(find /tmp/openclaw -name "openclaw-*.log" -mtime +7 2>/dev/null | wc -l | tr -d ' ') || OLD_LOGS=0
if [ "$OLD_LOGS" -gt 0 ]; then
    find /tmp/openclaw -name "openclaw-*.log" -mtime +7 -delete 2>/dev/null || true
    ok "清理 ${OLD_LOGS} 个过期 Gateway 日志"
    CLEANED=$((CLEANED + OLD_LOGS))
fi

if [ "$CLEANED" -eq 0 ]; then
    ok "无需清理"
else
    ok "本次共清理 ${CLEANED} 项"
fi

# ─── 12. 性能基线记录 (NEW) ───
info "12/13 性能基线"
# Initialize CSV if needed
if [ ! -f "$BASELINE_CSV" ]; then
    echo "timestamp,gw_mem_mb,disk_avail_gb,disk_used_pct,session_count,backup_count,mem_db_size,cron_errors" > "$BASELINE_CSV"
fi

TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
echo "${TIMESTAMP},${GW_MEM_MB:-0},${AVAIL_GB:-0},${USED_PCT:-0},${SESSION_COUNT:-0},${BACKUP_COUNT:-0},${MEM_DB_SIZE:-0},${CRON_ERRORS:-0}" >> "$BASELINE_CSV"
ok "基线数据已记录 → baseline.csv"

# Show trend if we have enough data
BASELINE_ROWS=$(wc -l < "$BASELINE_CSV" | tr -d ' ')
if [ "$BASELINE_ROWS" -gt 3 ]; then
    # Compare latest memory with 7-day avg
    AVG_MEM=$(tail -n 7 "$BASELINE_CSV" | awk -F',' 'NR>0{sum+=$2;n++}END{if(n>0) printf "%.0f", sum/n; else print 0}')
    if [ -n "$AVG_MEM" ] && [ "$AVG_MEM" -gt 0 ] && [ -n "$GW_MEM_MB" ] && [ "$GW_MEM_MB" -gt 0 ]; then
        DIFF=$((GW_MEM_MB - AVG_MEM))
        if [ "$DIFF" -gt 200 ]; then
            warn "Gateway 内存较近期均值(${AVG_MEM}MB)高出 ${DIFF}MB，可能存在泄漏"
            WARNINGS=$((WARNINGS + 1))
        else
            info "  └─ 近期均值: ${AVG_MEM}MB，当前: ${GW_MEM_MB}MB"
        fi
    fi
fi

# ─── 13. 审计日志大小 ───
info "13/13 审计日志"
if [ -f "$AUDIT_LOG" ]; then
    AUDIT_SIZE=$(du -sh "$AUDIT_LOG" 2>/dev/null | awk '{print $1}')
    AUDIT_LINES=$(wc -l < "$AUDIT_LOG" | tr -d ' ')
    ok "审计日志: ${AUDIT_LINES} 条记录 (${AUDIT_SIZE})"
    # Rotate if too large (>1MB)
    AUDIT_BYTES=$(stat -f%z "$AUDIT_LOG" 2>/dev/null || stat -c%s "$AUDIT_LOG" 2>/dev/null || echo "0")
    if [ "$AUDIT_BYTES" -gt 1048576 ]; then
        mv "$AUDIT_LOG" "${AUDIT_LOG}.$(date +%Y%m%d).old"
        ok "审计日志已轮转（超过 1MB）"
    fi
else
    ok "审计日志: 暂无记录"
fi

# ─── Summary ───
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ "$CRITICALS" -gt 0 ]; then
    critical "巡检完成: $CRITICALS 严重问题, $WARNINGS 警告"
    echo "EXIT_CODE=CRITICAL"
    exit 2
elif [ "$WARNINGS" -gt 0 ]; then
    warn "巡检完成: $WARNINGS 警告"
    echo "EXIT_CODE=WARNING"
    exit 1
else
    ok "巡检完成: 系统健康 ✅"
    echo "EXIT_CODE=OK"
    exit 0
fi
