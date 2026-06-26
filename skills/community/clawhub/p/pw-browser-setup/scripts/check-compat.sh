#!/usr/bin/env bash
# browser-setup: 系统兼容性检查
# 检查 OS、内存、CPU 核心数是否满足运行非头浏览器的要求
set -e

PASS=0
WARN=0
FAIL=0

ok()   { echo "✅ $1"; PASS=$((PASS+1)); }
warn() { echo "⚠️  $1"; WARN=$((WARN+1)); }
fail() { echo "❌ $1"; FAIL=$((FAIL+1)); }

echo "=== 系统兼容性检查 ==="
echo ""

# 1. 操作系统
echo "--- 操作系统 ---"
OS="$(uname -s)"
ARCH="$(uname -m)"
if [[ "$OS" == "Linux" ]]; then
  ok "操作系统: Linux ($ARCH)"
elif [[ "$OS" == "Darwin" ]]; then
  ok "操作系统: macOS ($ARCH) — 支持，但需自行安装 Chrome"
else
  fail "操作系统: $OS — 不支持"
fi

# 2. 内存（最低 2GB，推荐 4GB+）
echo ""
echo "--- 内存 ---"
if [[ "$OS" == "Linux" ]]; then
  MEM_KB=$(grep MemTotal /proc/meminfo | awk '{print $2}')
  MEM_GB=$(echo "scale=1; $MEM_KB / 1048576" | bc)
  MEM_INT=${MEM_GB%.*}
  if (( MEM_INT >= 4 )); then
    ok "内存: ${MEM_GB}GB — 充足"
  elif (( MEM_INT >= 2 )); then
    warn "内存: ${MEM_GB}GB — 勉强够用（推荐 4GB+）"
  else
    fail "内存: ${MEM_GB}GB — 不足，至少需要 2GB"
  fi
else
  # macOS
  MEM_BYTES=$(sysctl -n hw.memsize 2>/dev/null || echo 0)
  MEM_GB=$(echo "scale=1; $MEM_BYTES / 1073741824" | bc)
  MEM_INT=${MEM_GB%.*}
  if (( MEM_INT >= 4 )); then
    ok "内存: ${MEM_GB}GB — 充足"
  elif (( MEM_INT >= 2 )); then
    warn "内存: ${MEM_GB}GB — 勉强够用（推荐 4GB+）"
  else
    fail "内存: ${MEM_GB}GB — 不足"
  fi
fi

# 3. CPU 核心数（最低 2 核，推荐 4+）
echo ""
echo "--- CPU ---"
CORES=$(nproc 2>/dev/null || sysctl -n hw.ncpu 2>/dev/null || echo 0)
if (( CORES >= 4 )); then
  ok "CPU 核心: $CORES — 充足"
elif (( CORES >= 2 )); then
  warn "CPU 核心: $CORES — 勉强够用（推荐 4+）"
else
  fail "CPU 核心: $CORES — 不足，至少需要 2 核"
fi

# 4. 磁盘空间（Chrome + Playwright 约需 1GB）
echo ""
echo "--- 磁盘空间 ---"
AVAIL_MB=$(df -m / | tail -1 | awk '{print $4}')
if (( AVAIL_MB >= 2048 )); then
  ok "可用空间: ${AVAIL_MB}MB — 充足"
elif (( AVAIL_MB >= 1024 )); then
  warn "可用空间: ${AVAIL_MB}MB — 勉强够用"
else
  fail "可用空间: ${AVAIL_MB}MB — 不足，至少需要 1GB"
fi

# 5. Node.js
echo ""
echo "--- Node.js ---"
if command -v node &>/dev/null; then
  NODE_VER=$(node --version)
  NODE_MAJOR=$(echo "$NODE_VER" | sed 's/v//' | cut -d. -f1)
  if (( NODE_MAJOR >= 18 )); then
    ok "Node.js: $NODE_VER — 满足要求"
  elif (( NODE_MAJOR >= 16 )); then
    warn "Node.js: $NODE_VER — 建议升级到 18+"
  else
    fail "Node.js: $NODE_VER — 版本过低，需要 18+"
  fi
else
  fail "Node.js 未安装"
fi

# 6. npm
if command -v npm &>/dev/null; then
  NPM_VER=$(npm --version)
  ok "npm: v$NPM_VER"
else
  fail "npm 未安装"
fi

# 7. Xvfb（非头浏览器需要虚拟显示器）
echo ""
echo "--- 虚拟显示器 (Xvfb) ---"
if [[ "$OS" == "Linux" ]]; then
  if command -v Xvfb &>/dev/null; then
    ok "Xvfb: 已安装"
  else
    warn "Xvfb: 未安装 — 安装程序会自动安装"
  fi
elif [[ "$OS" == "Darwin" ]]; then
  ok "macOS 不需要 Xvfb（原生支持无头 GUI）"
fi

# 总结
echo ""
echo "=== 检查结果 ==="
echo "通过: $PASS | 警告: $WARN | 失败: $FAIL"
echo ""

if (( FAIL > 0 )); then
  echo "❌ 系统不满足最低要求，请先解决问题后再安装"
  exit 1
elif (( WARN > 0 )); then
  echo "⚠️  系统基本满足要求，但有警告项"
  exit 0
else
  echo "✅ 系统完全满足要求，可以安装"
  exit 0
fi
