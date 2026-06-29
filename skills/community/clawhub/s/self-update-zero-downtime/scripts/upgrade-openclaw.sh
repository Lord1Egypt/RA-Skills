#!/usr/bin/env bash
# ============================================================================
# OpenClaw 零停机升级脚本
#
# 适用场景: npm install -g 全局安装的 OpenClaw
# 不适用的场景: git checkout / 手动构建安装（请改用 openclaw update）
#
# 升级方式: npm install -g openclaw@latest
#
# 流程:
#   1. 探测运行目录（从 systemd ExecStart 反推实际代码目录）
#   2. 校验是否为 npm global install
#   3. 旁路备份
#   4. npm install -g 更新 npm global 下的 openclaw
#   5. 更新 systemd 版本号
#   6. 重启 + 健康检查
#   7. 失败回滚 / 成功清理
#
# 所有输出写入日志。
# ============================================================================

# ─── 日志 ───────────────────────────────────────────────────────────────
LOG_FILE="$HOME/.openclaw/workspace/logs/upgrade-$(date +%Y%m%d-%H%M%S).log"
mkdir -p "$(dirname "$LOG_FILE")"
exec >> "$LOG_FILE" 2>&1

set -euo pipefail

# ─── 工具 ───────────────────────────────────────────────────────────────
log()    { echo "[$(date +%H:%M:%S)] $*"; }
ok()     { echo "[$(date +%H:%M:%S)] ✅ $*"; }
warn()   { echo "[$(date +%H:%M:%S)] ⚠️  $*"; }
fail()   { echo "[$(date +%H:%M:%S)] ❌ $*"; }
step()   { echo ""; echo "===== $* ====="; }

# ────────────────────────────────────────────────────────────────────────
step "阶段 0: 环境探测"
# ────────────────────────────────────────────────────────────────────────

for cmd in node npm systemctl curl; do
    if ! command -v "$cmd" &>/dev/null; then
        fail "缺少命令: $cmd"
        exit 1
    fi
done
NODE_BIN=$(command -v node)
NPM_BIN=$(command -v npm)
log "node: $NODE_BIN ($($NODE_BIN -v))"
log "npm:  $NPM_BIN ($($NPM_BIN -v))"

# ─── 0a: 确定实际运行的代码目录 ──────────────────────────────────────
# 策略: 优先从 systemd ExecStart 反推，再 fallback 到 npm root -g
SERVICE=""
UNITFILE=""
RUN_DIR=""          # 进程实际运行的代码目录
NPM_GLOBAL_DIR=""   # npm global 下的 openclaw 目录
CURRENT_VERSION_VAR="unknown"

# 从 systemd 找
FOUND_SVC=$(systemctl --user list-units --type=service --all --no-legend 2>/dev/null \
    | awk '{print $1}' | grep -i openclaw | head -1 || true)

if [ -n "$FOUND_SVC" ]; then
    SERVICE="${FOUND_SVC%.service}"
    EXEC_START=$(systemctl --user show "$SERVICE" -p ExecStart 2>/dev/null \
        | grep -oP 'path=/[^;]+' | head -1 | cut -d= -f2 || true)
    if [ -n "$EXEC_START" ]; then
        SCRIPT_PATH=$(echo "$EXEC_START" | awk '{print $2}' 2>/dev/null || echo "")
        if [ -n "$SCRIPT_PATH" ] && [ -f "$SCRIPT_PATH" ]; then
            RUN_DIR=$(cd "$(dirname "$SCRIPT_PATH")/.." && pwd 2>/dev/null || echo "")
        fi
    fi
    UNITFILE=$(systemctl --user cat "$SERVICE" 2>/dev/null | head -1 | sed 's/^# //' || true)
    if [ -z "$UNITFILE" ] || [ ! -f "$UNITFILE" ]; then
        UNITFILE="$HOME/.config/systemd/user/${SERVICE}.service"
    fi
    if [ -f "$UNITFILE" ]; then
        CURRENT_VERSION_VAR=$(grep -oP 'OPENCLAW_SERVICE_VERSION=\K[^"]+' "$UNITFILE" 2>/dev/null || echo "unknown")
    fi
    log "systemd 服务: $SERVICE"
    log "systemd ExecStart 反推出: $RUN_DIR"
else
    warn "未发现 openclaw systemd 服务"
fi

# npm global 目录
NPM_ROOT=$($NPM_BIN root -g 2>/dev/null || echo "")
if [ -n "$NPM_ROOT" ] && [ -d "$NPM_ROOT/openclaw" ]; then
    NPM_GLOBAL_DIR="$NPM_ROOT/openclaw"
    log "npm global openclaw: $NPM_GLOBAL_DIR"
fi

# 如果 RUN_DIR 没找到，fallback 到 npm global
if [ -z "$RUN_DIR" ] || [ ! -d "$RUN_DIR" ]; then
    if [ -n "$NPM_GLOBAL_DIR" ]; then
        RUN_DIR="$NPM_GLOBAL_DIR"
        log "fallback: 使用 npm global 目录"
    fi
fi

if [ -z "$RUN_DIR" ] || [ ! -d "$RUN_DIR" ]; then
    fail "无法确定 OpenClaw 安装目录"
    fail "从 systemd ExecStart 和 npm root -g 都未找到"
    exit 1
fi
log "实际运行目录: $RUN_DIR"

# 检查 package.json 是否存在
if [ ! -f "$RUN_DIR/package.json" ]; then
    fail "运行目录下没有 package.json，可能是个空架子"
    fail "目录: $RUN_DIR"
    exit 1
fi

# ─── 0b: 判断安装类型 ──────────────────────────────────────────────
# 只支持 npm global install，不支持 git checkout
INSTALLED_VERSION=$($NODE_BIN -e "console.log(require('$RUN_DIR/package.json').version)" 2>/dev/null || echo "unknown")
PROBE_FILE="$RUN_DIR/.git"  # git checkout 会有 .git 目录或文件

IS_GIT_INSTALL=false
if [ -e "$PROBE_FILE" ]; then
    IS_GIT_INSTALL=true
fi

IS_NPM_GLOBAL_INSTALL=false
if [ -n "$NPM_GLOBAL_DIR" ] && [ "$(cd "$RUN_DIR" && pwd)" = "$(cd "$NPM_GLOBAL_DIR" && pwd)" ]; then
    IS_NPM_GLOBAL_INSTALL=true
fi

log "安装类型检测: npm_global=$IS_NPM_GLOBAL_INSTALL git=$IS_GIT_INSTALL"

# ─── 0c: npm prefix 可写性检查 ─────────────────────────────────────
NPM_PREFIX=$($NPM_BIN config get prefix 2>/dev/null || echo "")
log "npm prefix: $NPM_PREFIX"
NEED_SUDO=false
if [ -n "$NPM_PREFIX" ] && [ ! -w "$NPM_PREFIX" ]; then
    NEED_SUDO=true
fi

# ────────────────────────────────────────────────────────────────────────
step "阶段 1: 校验兼容性"
# ────────────────────────────────────────────────────────────────────────

# 1a. git checkout 不支持
if [ "$IS_GIT_INSTALL" = true ]; then
    fail "检测到 git checkout 安装方式（代码目录下有 .git）"
    fail "本脚本仅支持 npm install -g 全局安装的升级。"
    fail "git 安装请用: openclaw update"
    log "检测详情:"
    log "  运行目录: $RUN_DIR"
    log "  含 .git 标识 → git checkout"
    exit 1
fi

# 1b. npm global install 但代码目录不在 npm global 下（不一致状态）
if [ "$IS_NPM_GLOBAL_INSTALL" = false ] && [ -n "$NPM_GLOBAL_DIR" ]; then
    warn "运行目录 ($RUN_DIR) 与 npm global 目录 ($NPM_GLOBAL_DIR) 不同"
    warn "这意味着实际进程跑的代码和 npm 包不是同一套"
    fail "脚本无法安全处理这种不一致状态，中止"
    log "解决建议:"
    log "  确认哪个目录是实际代码: systemctl --user show $SERVICE -p ExecStart"
    log "  统一后重试"
    exit 1
fi

# 1c. npm global install 但 prefix 不可写
if [ "$NEED_SUDO" = true ]; then
    fail "npm prefix ($NPM_PREFIX) 不可写，npm install -g 需要 root 权限"
    fail "请先执行: npm config set prefix \"\$HOME/.npm-global\""
    log "设置后确保 \$HOME/.npm-global/bin 在 PATH 中"
    log "当前 PATH: $PATH"
    exit 1
fi

ok "兼容性检查通过"
log "  类型: npm global install"
log "  目录: $RUN_DIR (可写: $(test -w "$RUN_DIR" && echo '是' || echo '否'))"
log "  prefix: $NPM_PREFIX (可写: $(test -w "$NPM_PREFIX" && echo '是' || echo '否'))"

# ────────────────────────────────────────────────────────────────────────
step "阶段 2: 前置检查"
# ────────────────────────────────────────────────────────────────────────

AVAIL=$(df -B1 "$HOME" | awk 'NR==2 {print $4}')
if [ "$AVAIL" -lt 2147483648 ]; then
    fail "磁盘空间不足: $(numfmt --to=iec $AVAIL) 可用，需要至少 2G"
    exit 1
fi
ok "磁盘: $(numfmt --to=iec $AVAIL)"

if [ -n "$SERVICE" ]; then
    if [ "$(systemctl --user is-active "$SERVICE" 2>/dev/null)" != "active" ]; then
        fail "服务 $SERVICE 未运行"
        exit 1
    fi
    log "服务状态: active"
fi
ok "当前版本: v$INSTALLED_VERSION (代码: $RUN_DIR)"

# ─── 查 release notes ──────────────────────────────────────────────
step "查 release notes"

TARGET_VERSION=$($NPM_BIN view openclaw version 2>/dev/null || echo "unknown")
if [ "$TARGET_VERSION" = "unknown" ]; then
    TARGET_VERSION=$($NPM_BIN view openclaw version --registry https://registry.npmjs.org 2>/dev/null || echo "unknown")
fi
log "目标版本: v$TARGET_VERSION"

if [ "$TARGET_VERSION" = "unknown" ]; then
    log "无法获取目标版本号，继续升级"
elif [ "$TARGET_VERSION" = "$INSTALLED_VERSION" ]; then
    log "当前已是最新版 (v$INSTALLED_VERSION)"
    ok "无需升级，退出"
    exit 0
else
    RN=$(curl -sL --connect-timeout 10 \
        "https://api.github.com/repos/openclaw/openclaw/releases/tags/v${TARGET_VERSION}" 2>/dev/null \
        | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    body = d.get('body', '')
    name = d.get('name', '')
    html = d.get('html_url', '')
    lines = body.strip().split('\n')
    safe = [l for l in lines[:50] if l.strip()]
    print(f'--- {name} ---')
    for l in safe: print(l)
    if len(lines) > 50: print('...')
    print(f'--- Full: {html} ---')
except: print('ParseError')
" 2>/dev/null || echo "API 请求失败")

    log "=== Release Notes ==="
    echo "$RN" | while IFS= read -r l; do log "$l"; done
    log "=== End ==="

    BREAKING_HINT=$(echo "$RN" | grep -ci "breaking\|BREAKING\|重新.*密码\|密码.*变更\|credential\|re-auth\|reauthenticate\|password.*change\|migration" || true)
    if [ "$BREAKING_HINT" -gt 0 ]; then
        log "⚠️  含疑似 breaking change 关键词，升级后留意"
    fi
fi

# ────────────────────────────────────────────────────────────────────────
step "阶段 3: 旁路备份"
# ────────────────────────────────────────────────────────────────────────

BAKDIR="${RUN_DIR}-fallback"
rm -rf "$BAKDIR"
log "备份 $RUN_DIR → $BAKDIR ..."
cp -r "$RUN_DIR" "$BAKDIR"
ok "备份完成 ($(du -sh "$BAKDIR" | awk '{print $1}'))"

# ────────────────────────────────────────────────────────────────────────
step "阶段 4: npm install -g openclaw@latest"
# ────────────────────────────────────────────────────────────────────────

log "安装..."
if ! $NPM_BIN install -g openclaw 2>&1; then
    fail "npm install 失败"
    log "尝试官方 registry..."
    if ! $NPM_BIN install -g openclaw --registry https://registry.npmjs.org 2>&1; then
        fail "官方 registry 也失败"
        log "回滚..."
        rm -rf "$RUN_DIR"
        cp -r "$BAKDIR" "$RUN_DIR"
        ok "已恢复"
        rm -rf "$BAKDIR"
        exit 1
    fi
fi

# 验证：因为 npm install -g 更新的是 NPM_GLOBAL_DIR（可能和 RUN_DIR 相同）
ACTUAL_DIR="$NPM_GLOBAL_DIR"
if [ -z "$ACTUAL_DIR" ] || [ ! -d "$ACTUAL_DIR" ]; then
    ACTUAL_DIR="$RUN_DIR"
fi

NEW_VERSION=$($NODE_BIN -e "console.log(require('$ACTUAL_DIR/package.json').version)" 2>/dev/null || echo "unknown")
if [ "$NEW_VERSION" = "$INSTALLED_VERSION" ] || [ "$NEW_VERSION" = "unknown" ]; then
    fail "版本未更新 ($INSTALLED_VERSION → $NEW_VERSION)"
    log "回滚..."
    rm -rf "$RUN_DIR"
    cp -r "$BAKDIR" "$RUN_DIR"
    ok "已恢复"
    rm -rf "$BAKDIR"
    exit 1
fi

ENTRY_COUNT=$(find "$ACTUAL_DIR/dist" -maxdepth 1 -name "*.js" -type f 2>/dev/null | wc -l)
if [ "$ENTRY_COUNT" -eq 0 ] && [ ! -f "$ACTUAL_DIR/openclaw.mjs" ]; then
    fail "入口文件缺失（dist/*.js 和 openclaw.mjs 均不存在）"
    log "回滚..."
    rm -rf "$RUN_DIR"
    cp -r "$BAKDIR" "$RUN_DIR"
    ok "已恢复"
    rm -rf "$BAKDIR"
    exit 1
fi

# 如果 RUN_DIR ≠ NPM_GLOBAL_DIR，npm install -g 更新的是 NPM_GLOBAL_DIR
# 需要把新代码同步到 RUN_DIR
if [ "$(cd "$RUN_DIR" && pwd)" != "$(cd "$ACTUAL_DIR" && pwd)" ]; then
    log "npm 更新了 $ACTUAL_DIR，但进程跑的是 $RUN_DIR，需同步..."
    rm -rf "$RUN_DIR"/*
    cp -r "$ACTUAL_DIR"/* "$RUN_DIR/"
    ok "已同步到 $RUN_DIR"
fi

ok "安装完成: v$INSTALLED_VERSION → v$NEW_VERSION"

# ────────────────────────────────────────────────────────────────────────
step "阶段 5: 更新 systemd 版本号"

if [ -n "$UNITFILE" ] && [ -f "$UNITFILE" ]; then
    if grep -q "OPENCLAW_SERVICE_VERSION=" "$UNITFILE"; then
        sed -i "s/OPENCLAW_SERVICE_VERSION=[^\"]*/OPENCLAW_SERVICE_VERSION=$NEW_VERSION/" "$UNITFILE"
        systemctl --user daemon-reload
        ok "systemd 版本号已更新: v$NEW_VERSION"
    else
        warn "unit 文件中未找到 OPENCLAW_SERVICE_VERSION，跳过"
    fi
else
    warn "没有 unit 文件，跳过 systemd 更新"
fi

# ────────────────────────────────────────────────────────────────────────
step "阶段 6: 重启 + 健康检查"

if [ -z "$SERVICE" ]; then
    warn "没有 systemd 服务，仅替换了代码，请手动重启"
    rm -rf "$BAKDIR"
    ok "完成"
    exit 0
fi

log "重启 $SERVICE ..."
systemctl --user restart "$SERVICE"

WAITED=0
while [ $WAITED -lt 60 ]; do
    sleep 2
    WAITED=$((WAITED + 2))
    systemctl --user is-active "$SERVICE" &>/dev/null && break
done

FINAL_STATUS=$(systemctl --user is-active "$SERVICE" 2>/dev/null || echo "inactive")
SERVICE_VERSION=$(systemctl --user show "$SERVICE" -p Environment 2>/dev/null \
    | grep -oP 'OPENCLAW_SERVICE_VERSION=\K[^"]+' || echo "unknown")

if [ "$FINAL_STATUS" = "active" ]; then
    ok "升级成功: v$INSTALLED_VERSION → v$SERVICE_VERSION（闪断 ${WAITED}s）"
    log "清理备份..."
    rm -rf "$BAKDIR"
    ok "完成"
else
    warn "新版本启动异常 (status=$FINAL_STATUS, waited ${WAITED}s)"
    journalctl --user -u "$SERVICE" -n 20 --no-pager || true

    log "从备份恢复..."
    rm -rf "$RUN_DIR"
    cp -r "$BAKDIR" "$RUN_DIR"

    if [ -n "$UNITFILE" ] && [ -f "$UNITFILE" ]; then
        sed -i "s/OPENCLAW_SERVICE_VERSION=[^\"]*/OPENCLAW_SERVICE_VERSION=$CURRENT_VERSION_VAR/" "$UNITFILE"
        systemctl --user daemon-reload
    fi

    log "重启旧版本..."
    systemctl --user restart "$SERVICE"
    sleep 10

    ROLLBACK_STATUS=$(systemctl --user is-active "$SERVICE" 2>/dev/null || echo "inactive")
    if [ "$ROLLBACK_STATUS" = "active" ]; then
        ok "已回滚到 v$CURRENT_VERSION_VAR，服务恢复正常"
    else
        fail "回滚后服务仍无法启动！请手动检查: systemctl --user status $SERVICE"
    fi

    rm -rf "$BAKDIR"
    log "升级中止，已回滚"
    exit 1
fi

ok "日志: $LOG_FILE"
