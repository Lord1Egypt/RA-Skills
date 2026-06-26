#!/bin/bash
#
# UOS deb 包检查脚本
# 检查 deb 包是否符合 UOS 打包规范
#

set -e

DEB_FILE="${1:-}"

if [[ -z "$DEB_FILE" ]]; then
    echo "用法: $0 <xxx.deb>"
    exit 1
fi

if [[ ! -f "$DEB_FILE" ]]; then
    echo "错误: 文件不存在: $DEB_FILE"
    exit 1
fi

WORK_DIR="/tmp/uos_inspect_$$"
mkdir -p "$WORK_DIR"

echo "=== UOS deb 包检查: $DEB_FILE ==="
echo ""

dpkg-deb -e "$DEB_FILE" "$WORK_DIR/DEBIAN" 2>/dev/null || true
dpkg-deb -x "$DEB_FILE" "$WORK_DIR/rootfs" 2>/dev/null || true

ERRORS=0
WARNINGS=0

# ── 1. 检查 appid 格式 ───────────────────────────────────
INFO_FILE="$WORK_DIR/rootfs/opt/apps/"*/info 2>/dev/null || INFO_FILE=""
if [[ -f "$INFO_FILE" ]]; then
    APPID=$(grep -oP '"appid"\s*:\s*"\K[^"]+' "$INFO_FILE" | head -1)
    echo "1. appid: $APPID"
    if ! echo "$APPID" | grep -qE '^[a-z][a-z0-9]*(\.[a-z][a-z0-9]*)+$'; then
        echo "   ❌ appid 不符合倒置域名规范"
        ((ERRORS++))
    else
        echo "   ✅ 格式正确"
    fi
    
    # ── 2. 检查 info 版本格式 ─────────────────────────────
    VERSION=$(grep -oP '"version"\s*:\s*"\K[^"]+' "$INFO_FILE" | head -1)
    echo "2. version: $VERSION"
    if ! echo "$VERSION" | grep -qE '^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$'; then
        echo "   ❌ version 格式错误，应为 {MAJOR}.{MINOR}.{PATCH}.{BUILD}（纯数字）"
        ((ERRORS++))
    else
        echo "   ✅ 格式正确"
    fi
    
    # ── 3. 检查 arch ────────────────────────────────────
    ARCH=$(grep -oP '"arch"\s*:\s*\[\K[^\]]+' "$INFO_FILE" | head -1)
    echo "3. arch: [$ARCH]"
    VALID_ARCHS="amd64 arm64 loongarch64 mips64el sw_64"
    for a in $(echo "$ARCH" | tr ',:' ' ' | tr -d '"'); do
        if echo "$VALID_ARCHS" | grep -qw "$a"; then
            echo "   ✅ $a 是支持的架构"
        else
            echo "   ❌ $a 是不支持的架构"
            ((ERRORS++))
        fi
    done
else
    echo "❌ 未找到 info 文件"
    ((ERRORS++))
fi

echo ""

# ── 4. 检查 desktop 文件 ──────────────────────────────────
DESKTOP_FILE="$WORK_DIR/rootfs/usr/share/applications/"*.desktop 2>/dev/null || DESKTOP_FILE=""
if [[ -f "$DESKTOP_FILE" ]]; then
    echo "4. desktop 文件: $(basename $DESKTOP_FILE)"
    
    # 检查编码
    ENCODING=$(file -b --mime-encoding "$DESKTOP_FILE" 2>/dev/null || echo "unknown")
    if [[ "$ENCODING" == "utf-8" ]]; then
        echo "   ✅ UTF-8 编码正确"
    else
        echo "   ❌ 编码是 $ENCODING，必须为 UTF-8"
        ((ERRORS++))
    fi
    
    # 检查必填字段
    for field in Name Exec Icon Type Terminal StartupNotify; do
        if grep -q "^$field=" "$DESKTOP_FILE"; then
            echo "   ✅ $field 已填写"
        else
            echo "   ❌ 缺少必填字段: $field"
            ((ERRORS++))
        fi
    done
else
    echo "4. desktop 文件: 未找到（不会显示在启动器中）"
    ((WARNINGS++))
fi

echo ""

# ── 5. 检查安装路径 ──────────────────────────────────────
OPT_APPS_DIR="$WORK_DIR/rootfs/opt/apps"
if [[ -d "$OPT_APPS_DIR" ]]; then
    echo "5. 安装路径: ✅ 符合 /opt/apps 规范"
    ls "$OPT_APPS_DIR/" | while read d; do
        echo "   - /opt/apps/$d"
    done
else
    echo "5. 安装路径: ❌ 未找到 /opt/apps/"
    ((ERRORS++))
fi

echo ""

# ── 6. 检查钩子脚本 rm -rf 规范 ──────────────────────────
for hook in postinst postrm preinst prerm; do
    HOOK_FILE="$WORK_DIR/DEBIAN/$hook"
    if [[ -f "$HOOK_FILE" ]]; then
        echo "6. 检测到 $hook:"
        
        # 检查危险的 rm -rf 用法
        if grep -n 'rm\s*-rf\s\+[$]' "$HOOK_FILE" | grep -v '".*\$' | grep -v '"\$[^"]*"' > /dev/null; then
            echo "   ⚠ 警告: $hook 中有未加引号的 rm -rf 变量"
            ((WARNINGS++))
        fi
        
        if grep -qE 'rm\s+-rf\s+/\s*\$' "$HOOK_FILE"; then
            echo "   ❌ 致命: $hook 中有递归删除根目录的操作"
            ((ERRORS++))
        fi
        
        if grep -qE 'rm\s+-rf\s+/\*' "$HOOK_FILE"; then
            echo "   ❌ 致命: $hook 中有删除系统目录的操作"
            ((ERRORS++))
        fi
        
        # shellcheck 检查
        if command -v shellcheck &>/dev/null; then
            if ! shellcheck "$HOOK_FILE" > /dev/null 2>&1; then
                echo "   ⚠ shellcheck 发现问题:"
                shellcheck "$HOOK_FILE" | head -3
                ((WARNINGS++))
            else
                echo "   ✅ shellcheck 通过"
            fi
        else
            echo "   ℹ 未安装 shellcheck，跳过语法检查（建议安装: sudo apt install shellcheck）"
        fi
    fi
done

echo ""

# ── 7. 检查文件权限 ───────────────────────────────────────
echo "7. 文件权限检查:"
BIN_FILE="$WORK_DIR/rootfs/opt/apps/"*/files/bin/* 2>/dev/null || true
if [[ -x "$BIN_FILE" ]]; then
    echo "   ✅ 可执行文件权限正确"
else
    echo "   ℹ 未找到可执行文件或未设置执行权限"
fi

echo ""
echo "=== 检查结果 ==="
echo "错误: $ERRORS"
echo "警告: $WARNINGS"

rm -rf "$WORK_DIR"

if [[ $ERRORS -gt 0 ]]; then
    echo ""
    echo "❌ 检查未通过，请修复上述错误"
    exit 1
elif [[ $WARNINGS -gt 0 ]]; then
    echo ""
    echo "⚠ 检查通过但有警告"
    exit 0
else
    echo ""
    echo "✅ 检查通过"
    exit 0
fi
