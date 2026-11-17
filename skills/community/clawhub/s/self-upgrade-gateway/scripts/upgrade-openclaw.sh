#!/usr/bin/env bash
# ============================================================================
# OpenClaw 零停机升级脚本 v4
#
# 升级方式: npm install -g openclaw@latest
#
# 流程:
#   1. 前置检查（含 Node 版本兼容性自检 + systemd node 路径检测）
#   2. 查 release notes（备忘，不阻塞）
#   3. 旁路备份 openclaw → openclaw-fallback（安全锚点）
#   4. npm install -g openclaw@latest
#   5. 检查新版 Node 要求，自动修正 systemd ExecStart
#   6. 更新 systemd 单元版本号
#   7. 重启 + 健康检查
#   8. 失败回滚 / 成功清理
#
# 所有输出写入日志，控制台不输出。
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

# ─── 常量 ───────────────────────────────────────────────────────────────
BASE="$HOME/.npm-global/lib/node_modules"
CURDIR="$BASE/openclaw"
BAKDIR="$BASE/openclaw-fallback"
UNITFILE="$HOME/.config/systemd/user/openclaw-gateway.service"
SERVICE="openclaw-gateway"
TMPDIR="${TMPDIR:-/tmp}/openclaw-upgrade.$$"

# 清理临时目录
cleanup_tmp() { rm -rf "$TMPDIR"; }
trap cleanup_tmp EXIT

# ─── 工具函数 ──────────────────────────────────────────────────────────

# 解析 semver 范围是否满足实际版本
# 用法: check_node_satisfies ">=22.22.3 <23 || >=24.15.0 <25 || >=25.9.0" "25.9.0"
# 只支持最简单范围，够用即可
check_node_satisfies() {
    local ranges="$1"
    local ver="$2"
    # 将 ver 拆成 major.minor.patch
    local major minor patch
    IFS='.' read -r major minor patch <<< "$ver"
    # || 分隔的每个子范围，有一个满足即可
    IFS='||' read -ra parts <<< "$ranges"
    for part in "${parts[@]}"; do
        part="${part// /}"
        [ -z "$part" ] && continue
        # 解析 >=M.N.P <M2.N2.P2 形式的范围
        if [[ "$part" =~ ^\>=([0-9]+)\.([0-9]+)\.([0-9]+)\<([0-9]+)\. ]]; then
            local lo_m="${BASH_REMATCH[1]}"
            local lo_n="${BASH_REMATCH[2]}"
            local lo_p="${BASH_REMATCH[3]}"
            # 只检查 major 下限
            if [ "$major" -gt "$lo_m" ] || \
               ([ "$major" -eq "$lo_m" ] && [ "$minor" -gt "$lo_n" ]) || \
               ([ "$major" -eq "$lo_m" ] && [ "$minor" -eq "$lo_n" ] && [ "$patch" -ge "$lo_p" ]); then
                return 0
            fi
        elif [[ "$part" =~ ^\>=([0-9]+)\.([0-9]+)\.([0-9]+)$ ]]; then
            local lo_m="${BASH_REMATCH[1]}"
            local lo_n="${BASH_REMATCH[2]}"
            local lo_p="${BASH_REMATCH[3]}"
            if [ "$major" -gt "$lo_m" ] || \
               ([ "$major" -eq "$lo_m" ] && [ "$minor" -gt "$lo_n" ]) || \
               ([ "$major" -eq "$lo_m" ] && [ "$minor" -eq "$lo_n" ] && [ "$patch" -ge "$lo_p" ]); then
                return 0
            fi
        fi
    done
    return 1
}

# 在系统中寻找满足 openclaw engines 要求的 node 可执行文件
find_compatible_node() {
    local required_engine="$1"
    # 检查所有能找到的 node
    local nodes=()
    while IFS= read -r -d '' n; do nodes+=("$n"); done < <(which -a node 2>/dev/null || true)
    # 额外检查常见位置
    for p in /usr/local/bin/node /usr/bin/node /bin/node "$HOME/.nvm/versions/node/"*/bin/node; do
        if [ -x "$p" ] && ! printf '%s\n' "${nodes[@]}" | grep -qxF "$p"; then
            nodes+=("$p")
        fi
    done
    for n in "${nodes[@]}"; do
        local v
        v=$("$n" --version 2>/dev/null | sed 's/^v//')
        [ -n "$v" ] && check_node_satisfies "$required_engine" "$v" && { echo "$n"; return 0; }
    done
    return 1
}

# 解析 package.json 的 engines.node 字段
get_engines_node() {
    local pkg="$1"
    if [ -f "$pkg" ]; then
        node -e "
            try {
                const p = require('$pkg');
                console.log(p.engines && p.engines.node ? p.engines.node : '');
            } catch(e) {
                console.log('');
            }
        " 2>/dev/null
    fi
}

# ────────────────────────────────────────────────────────────────────────
step "阶段 0: 前置检查"
# ────────────────────────────────────────────────────────────────────────

for cmd in node npm systemctl curl; do
    if ! command -v "$cmd" &>/dev/null; then
        fail "缺少命令: $cmd"
        exit 1
    fi
done
ok "基础命令就绪 (node $(node -v), npm $(npm -v))"

AVAIL=$(df -B1 "$HOME" | awk 'NR==2 {print $4}')
if [ "$AVAIL" -lt 2147483648 ]; then
    fail "磁盘空间不足: $(numfmt --to=iec $AVAIL) 可用，需要至少 2G"
    exit 1
fi
ok "磁盘空间: $(numfmt --to=iec $AVAIL)"

if [ "$(systemctl --user is-active "$SERVICE")" != "active" ]; then
    fail "$SERVICE 服务未运行"
    exit 1
fi
ok "$SERVICE 服务运行中"

# 从 systemd unit 中提取当前使用的 node 路径
CURRENT_NODE=$(grep -oP 'ExecStart=\K\S+' "$UNITFILE" 2>/dev/null | head -1 | sed 's|/node$||;s|/node | |;s| .*||')
[ -z "$CURRENT_NODE" ] && CURRENT_NODE=$(grep -oP 'ExecStart=\K[^ ]+' "$UNITFILE" 2>/dev/null | head -1 | sed 's|/home/.*||' || echo "/usr/bin/node")
[ -z "$CURRENT_NODE" ] || [ ! -x "$CURRENT_NODE" ] && CURRENT_NODE="/usr/bin/node"
CURRENT_NODE_VER=$("$CURRENT_NODE" --version 2>/dev/null | sed 's/^v//' || echo "unknown")
ok "systemd 当前 node: $CURRENT_NODE (v$CURRENT_NODE_VER)"

# ─── 获取新旧版本信息 ─────────────────────────────────────────────
INSTALLED_VERSION=$(node -e "console.log(require('$CURDIR/package.json').version)" 2>/dev/null || echo "unknown")
# 从 systemd Description 获取版本号（兼容两种格式）
CURRENT_VERSION_VAR=$(grep -oP 'Description=OpenClaw Gateway \(v\K[^)]+' "$UNITFILE" 2>/dev/null || echo "")
[ -z "$CURRENT_VERSION_VAR" ] && CURRENT_VERSION_VAR=$(grep -oP 'OPENCLAW_SERVICE_VERSION=\K[^"]+' "$UNITFILE" 2>/dev/null || echo "unknown")
ok "当前版本: $CURRENT_VERSION_VAR (npm: $INSTALLED_VERSION)"

# ─── 预检：新版 openclaw 的 Node 要求 ────────────────────────────────
step "阶段 0b: Node 版本兼容性预检"

# 下载新包信息但不安装，读取 engines.node
mkdir -p "$TMPDIR"
log "获取 openclaw@latest 包信息..."
npm pack openclaw@latest --pack-destination "$TMPDIR" 2>/dev/null || {
    fail "无法获取 openclaw@latest 包信息"
    exit 1
}
TARBALL=$(ls "$TMPDIR"/openclaw-*.tgz 2>/dev/null | head -1)
if [ -z "$TARBALL" ]; then
    fail "未找到下载的包"
    exit 1
fi
tar xzf "$TARBALL" -C "$TMPDIR" 2>/dev/null
NEW_PKG="$TMPDIR/package/package.json"
NEW_VERSION=$(node -e "console.log(require('$NEW_PKG').version)" 2>/dev/null || echo "unknown")
REQUIRED_ENGINE=$(get_engines_node "$NEW_PKG")

if [ -z "$NEW_VERSION" ] || [ "$NEW_VERSION" = "unknown" ]; then
    fail "无法解析新版本信息"
    exit 1
fi

log "目标版本: $NEW_VERSION"
log "Node 要求: ${REQUIRED_ENGINE:-无限制}"

# 检查 systemd 当前使用的 node 是否满足要求
SYSD_NODE_OK=false
if [ -n "$REQUIRED_ENGINE" ]; then
    if check_node_satisfies "$REQUIRED_ENGINE" "$CURRENT_NODE_VER"; then
        SYSD_NODE_OK=true
        ok "systemd node ($CURRENT_NODE_VER) 满足 $REQUIRED_ENGINE"
    else
        warn "systemd node ($CURRENT_NODE @ v$CURRENT_NODE_VER) 不满足要求: $REQUIRED_ENGINE"
        BEST_NODE=$(find_compatible_node "$REQUIRED_ENGINE")
        if [ -n "$BEST_NODE" ]; then
            BEST_VER=$("$BEST_NODE" --version 2>/dev/null | sed 's/^v//')
            ok "找到满足要求的 node: $BEST_NODE (v$BEST_VER)"
            log "升级后将自动修正 systemd ExecStart 指向 $BEST_NODE"
        else
            fail "系统中找不到满足 $REQUIRED_ENGINE 的 Node.js 版本！"
            fail "当前 node 版本: $(node -v)"
            fail "请先升级 Node.js 后再尝试升级"
            exit 1
        fi
    fi
else
    SYSD_NODE_OK=true
fi

# ─── 查 release notes（备忘，不阻塞） ──────────────────────────────
step "阶段 0c: 查 release notes"

log "查询 GitHub API 获取 release notes..."
RN_TAG="${NEW_VERSION}"
# 有些版本标签带 v 前缀
RN=$(curl -sL --connect-timeout 10 \
    "https://api.github.com/repos/openclaw/openclaw/releases/tags/v${RN_TAG}" 2>/dev/null \
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
except Exception as e:
    print(f'ParseError: {e}')
" 2>/dev/null || echo "API 请求失败")

log "=== Release Notes ==="
echo "$RN" | while IFS= read -r l; do log "$l"; done
log "=== End Release Notes ==="

BREAKING_HINT=$(echo "$RN" | grep -ci "breaking\|BREAKING\|重新.*密码\|密码.*变更\|credential\|re-auth\|reauthenticate\|password.*change\|migration" || true)
if [ "$BREAKING_HINT" -gt 0 ]; then
    log "⚠️  Release notes 中含疑似 breaking change 关键词，升级后留意"
fi

# ────────────────────────────────────────────────────────────────────────
step "阶段 1: 旁路备份"
# ────────────────────────────────────────────────────────────────────────

rm -rf "$BAKDIR"
log "备份当前代码到 openclaw-fallback..."
cp -r "$CURDIR" "$BAKDIR"
ok "备份完成 ($(du -sh "$BAKDIR" | awk '{print $1}'))"

# ────────────────────────────────────────────────────────────────────────
step "阶段 2: npm install -g openclaw@latest"
# ────────────────────────────────────────────────────────────────────────

log "安装 openclaw@latest..."

# 确保 npm 能找到正确的 node
NPM_INSTALL_OK=false
for retry in 1 2; do
    if npm install -g openclaw@latest 2>&1; then
        NPM_INSTALL_OK=true
        break
    fi
    log "npm install 第 $retry 次失败，尝试官方 registry..."
    if npm install -g openclaw@latest --registry https://registry.npmjs.org 2>&1; then
        NPM_INSTALL_OK=true
        break
    fi
    [ $retry -eq 1 ] && log "重试..."
done

if [ "$NPM_INSTALL_OK" != "true" ]; then
    fail "npm install 失败"
    log "回滚..."
    rm -rf "$CURDIR"
    cp -r "$BAKDIR" "$CURDIR"
    ok "已恢复旧代码"
    rm -rf "$BAKDIR"
    exit 1
fi

NEW_INSTALLED_V=$(node -e "console.log(require('$CURDIR/package.json').version)" 2>/dev/null || echo "unknown")
if [ "$NEW_INSTALLED_V" = "$INSTALLED_VERSION" ] || [ "$NEW_INSTALLED_V" = "unknown" ]; then
    fail "版本未更新 ($INSTALLED_VERSION → $NEW_INSTALLED_V)"
    log "回滚..."
    rm -rf "$CURDIR"
    cp -r "$BAKDIR" "$CURDIR"
    ok "已恢复旧代码"
    rm -rf "$BAKDIR"
    exit 1
fi

if [ ! -f "$CURDIR/dist/index.js" ] && [ ! -f "$CURDIR/openclaw.mjs" ]; then
    fail "入口文件缺失"
    log "回滚..."
    rm -rf "$CURDIR"
    cp -r "$BAKDIR" "$CURDIR"
    ok "已恢复旧代码"
    rm -rf "$BAKDIR"
    exit 1
fi
ok "安装完成: $INSTALLED_VERSION → $NEW_INSTALLED_V"

# ────────────────────────────────────────────────────────────────────────
step "阶段 3: 修正 systemd ExecStart Node 路径"
# ────────────────────────────────────────────────────────────────────────

# 重新检查新安装版本的 Node 要求，确定正确的 node 路径
INSTALLED_ENGINE=$(get_engines_node "$CURDIR/package.json")
TARGET_NODE="$CURRENT_NODE"

if [ -n "$INSTALLED_ENGINE" ]; then
    TARGET_NODE_VER=$("$TARGET_NODE" --version 2>/dev/null | sed 's/^v//' || echo "unknown")
    if ! check_node_satisfies "$INSTALLED_ENGINE" "$TARGET_NODE_VER"; then
        warn "当前 systemd node ($TARGET_NODE @ v$TARGET_NODE_VER) 不满足新版要求"
        BEST_NODE=$(find_compatible_node "$INSTALLED_ENGINE")
        if [ -n "$BEST_NODE" ]; then
            TARGET_NODE="$BEST_NODE"
            ok "将 systemd ExecStart 修正为: $TARGET_NODE"
        else
            fail "新版 openclaw 需要: $INSTALLED_ENGINE"
            fail "系统中找不到满足要求的 Node，回滚..."
            rm -rf "$CURDIR"
            cp -r "$BAKDIR" "$CURDIR"
            ok "已恢复旧代码"
            rm -rf "$BAKDIR"
            exit 1
        fi
    fi
fi

# 更新 ExecStart 中的 node 路径
CURRENT_EXEC_NODE=$(grep -oP 'ExecStart=\K\S+' "$UNITFILE" 2>/dev/null | head -1 | sed 's|/node$||;s|/node | |;s| .*||')
[ -z "$CURRENT_EXEC_NODE" ] && CURRENT_EXEC_NODE=$(grep -oP 'ExecStart=\K[^ ]+' "$UNITFILE" 2>/dev/null | head -1)
if [ "$CURRENT_EXEC_NODE" != "$TARGET_NODE" ]; then
    sed -i "s|ExecStart=${CURRENT_EXEC_NODE}|ExecStart=${TARGET_NODE}|" "$UNITFILE"
    ok "ExecStart 已更新: $CURRENT_EXEC_NODE → $TARGET_NODE"
else
    ok "ExecStart 无需变更: $TARGET_NODE"
fi
systemctl --user daemon-reload

# ────────────────────────────────────────────────────────────────────────
step "阶段 4: 更新 systemd 版本号"
# ────────────────────────────────────────────────────────────────────────

# 兼容两种格式：Description 中的版本号和 OPENCLAW_SERVICE_VERSION
if grep -q "OPENCLAW_SERVICE_VERSION=" "$UNITFILE"; then
    sed -i "s/OPENCLAW_SERVICE_VERSION=[^\"]*/OPENCLAW_SERVICE_VERSION=$NEW_INSTALLED_V/" "$UNITFILE"
    ok "OPENCLAW_SERVICE_VERSION 已更新: $NEW_INSTALLED_V"
fi
if grep -qP 'Description=OpenClaw Gateway \(v' "$UNITFILE"; then
    sed -i "s/Description=OpenClaw Gateway (v[^)]*/Description=OpenClaw Gateway (v$NEW_INSTALLED_V/" "$UNITFILE"
    ok "Description 版本号已更新: $NEW_INSTALLED_V"
fi
systemctl --user daemon-reload

# ────────────────────────────────────────────────────────────────────────
step "阶段 5: 重启 + 健康检查"
# ────────────────────────────────────────────────────────────────────────

log "重启 $SERVICE (闪断)..."
systemctl --user restart "$SERVICE"

WAITED=0
while [ $WAITED -lt 60 ]; do
    sleep 2
    WAITED=$((WAITED + 2))
    STATUS=$(systemctl --user is-active "$SERVICE" 2>/dev/null || echo "inactive")
    if [ "$STATUS" = "active" ]; then
        break
    fi
done

FINAL_STATUS=$(systemctl --user is-active "$SERVICE" 2>/dev/null || echo "inactive")

if [ "$FINAL_STATUS" = "active" ]; then
    ok "升级成功: $INSTALLED_VERSION → $NEW_INSTALLED_V (闪断 ${WAITED}s)"
    log "自动清理 fallback 备份..."
    rm -rf "$BAKDIR"
    ok "已清理"
else
    warn "新版本启动异常 (status=$FINAL_STATUS, waited ${WAITED}s)"
    journalctl --user -u "$SERVICE" -n 20 --no-pager || true

    log "从 openclaw-fallback 恢复旧代码..."
    rm -rf "$CURDIR"
    cp -r "$BAKDIR" "$CURDIR"

    # 恢复 ExecStart 中的 node 路径
    if [ "$CURRENT_EXEC_NODE" != "$CURRENT_NODE" ]; then
        sed -i "s|ExecStart=${TARGET_NODE}|ExecStart=${CURRENT_NODE}|" "$UNITFILE"
    fi
    # 恢复版本号
    if grep -q "OPENCLAW_SERVICE_VERSION=" "$UNITFILE"; then
        sed -i "s/OPENCLAW_SERVICE_VERSION=[^\"]*/OPENCLAW_SERVICE_VERSION=$CURRENT_VERSION_VAR/" "$UNITFILE"
    fi
    if grep -qP 'Description=OpenClaw Gateway \(v' "$UNITFILE"; then
        sed -i "s/Description=OpenClaw Gateway (v[^)]*/Description=OpenClaw Gateway (v$CURRENT_VERSION_VAR/" "$UNITFILE"
    fi
    systemctl --user daemon-reload

    log "重启旧版本..."
    systemctl --user restart "$SERVICE"
    sleep 10

    ROLLBACK_STATUS=$(systemctl --user is-active "$SERVICE" 2>/dev/null || echo "inactive")
    if [ "$ROLLBACK_STATUS" = "active" ]; then
        ok "已回滚到旧版本 ($CURRENT_VERSION_VAR)，服务恢复正常"
    else
        fail "回滚后服务仍无法启动！"
        fail "请手动检查: systemctl --user status $SERVICE"
    fi

    rm -rf "$BAKDIR"
    exit 1
fi

ok "升级流程完成，日志: $LOG_FILE"
