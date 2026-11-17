#!/usr/bin/env bash
# ============================================================================
# video-downloader-by-browser 一键环境就绪脚本（新电脑/迁移后先跑这个）
#
# 作用：
#   1. 检测/定位 node、python3
#   2. 安装 playwright-core 并在本 skill 的 scripts/ 下建立可移植的 node_modules
#      （ESM 不读 NODE_PATH，必须让 browser_ctl.mjs 能解析到 playwright-core）
#   3. 检测本机 Chrome（必需，用于有头模式）
#   4. 检测 ffmpeg（合并用）；没有则尝试 pip 安装 imageio-ffmpeg
#   5. 语法自检
#
# 用法：  bash setup.sh
# 幂等：可重复执行，已装的会跳过。
# ============================================================================
set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
echo "==> skill 目录: $SKILL_DIR"

# ---------- 1. 定位 node / npm ----------
find_bin() {  # find_bin <名字> [额外搜索路径...]
  local name="$1"; shift
  local p
  p="$(command -v "$name" 2>/dev/null)" && { echo "$p"; return 0; }
  for d in "$@"; do
    [ -x "$d/$name" ] && { echo "$d/$name"; return 0; }
  done
  return 1
}

NODE="$(find_bin node \
  "$HOME/.workbuddy/binaries/node/versions/22.22.2-2/bin" \
  "$HOME/.workbuddy/binaries/node/versions/22.12.0/bin" \
  /usr/local/bin /opt/homebrew/bin 2>/dev/null)"
if [ -z "${NODE:-}" ]; then
  echo "❌ 未找到 node。请先安装 Node.js 18+（https://nodejs.org 或 WorkBuddy 托管运行时）。"
  exit 1
fi
NPM="$(dirname "$NODE")/npm"
[ -x "$NPM" ] || NPM="$(find_bin npm "$(dirname "$NODE")" 2>/dev/null)"
echo "==> node:  $($NODE -v)  ($NODE)"

PY="$(find_bin python3 \
  "$HOME/.workbuddy/binaries/python/versions/3.13.12/bin" \
  "$HOME/.workbuddy/binaries/python/versions/3.14.3/bin" \
  /usr/local/bin /opt/homebrew/bin 2>/dev/null)"
[ -z "${PY:-}" ] && PY="$(find_bin python 2>/dev/null)"
if [ -n "${PY:-}" ]; then echo "==> python: $($PY -V 2>&1)  ($PY)"; else echo "⚠️ 未找到 python3（下载/合并脚本需要）"; fi

# ---------- 2. playwright-core + 可移植 node_modules ----------
# 优先装到 WorkBuddy 托管 workspace（若存在）；否则装到 skill 本地 scripts/node_modules_real
WORKSPACE="$HOME/.workbuddy/binaries/node/workspace"
PW_CORE=""
if [ -d "$WORKSPACE" ] && [ -d "$WORKSPACE/node_modules/playwright-core" ]; then
  PW_CORE="$WORKSPACE/node_modules/playwright-core"
  echo "==> 复用已装 playwright-core: $PW_CORE"
elif [ -d "$WORKSPACE" ]; then
  echo "==> 在托管 workspace 安装 playwright-core ..."
  ( cd "$WORKSPACE" && "$NPM" install playwright-core --no-audit --no-fund ) \
    && PW_CORE="$WORKSPACE/node_modules/playwright-core"
fi

# 在 scripts/ 下建立 node_modules 软链（ESM 从脚本位置向上找 node_modules）
if [ -n "$PW_CORE" ]; then
  mkdir -p "$SCRIPT_DIR/node_modules"
  ln -sfn "$PW_CORE" "$SCRIPT_DIR/node_modules/playwright-core"
  echo "==> 已建立软链 scripts/node_modules/playwright-core -> $PW_CORE"
else
  # 兜底：直接在 scripts/ 本地安装（自包含，最可移植）
  echo "==> 未找到托管 workspace，在 skill 本地安装 playwright-core ..."
  ( cd "$SCRIPT_DIR" && "$NPM" install --prefix "$SCRIPT_DIR" playwright-core --no-audit --no-fund )
fi

# ---------- 3. 检测本机 Chrome ----------
CHROME_OK=0
for c in \
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  "/usr/bin/google-chrome" "/usr/bin/google-chrome-stable" \
  "/opt/google/chrome/chrome" \
  "$(command -v google-chrome 2>/dev/null)" "$(command -v chrome 2>/dev/null)"; do
  [ -x "$c" ] && { echo "==> Chrome: $c"; CHROME_OK=1; break; }
done
[ "$CHROME_OK" = "0" ] && echo "⚠️ 未找到本机 Google Chrome。有头模式需要它；请安装 Chrome，或改 browser_ctl.mjs 回退 Chromium。"

# ---------- 4. ffmpeg ----------
if command -v ffmpeg >/dev/null 2>&1; then
  echo "==> ffmpeg: $(command -v ffmpeg)"
else
  echo "==> 系统无 ffmpeg，尝试 pip 安装 imageio-ffmpeg（自带 ffmpeg 二进制）..."
  if [ -n "${PY:-}" ]; then
    "$PY" -m pip install -q imageio-ffmpeg 2>/dev/null \
      && echo "==> imageio-ffmpeg 安装完成（merge_verify.py 会自动调用）" \
      || echo "⚠️ imageio-ffmpeg 安装失败，请手动: pip install imageio-ffmpeg 或 brew install ffmpeg"
  else
    echo "⚠️ 无 python3，无法自动装 ffmpeg。请手动安装 ffmpeg。"
  fi
fi

# ---------- 5. 语法自检 ----------
echo "==> 语法自检..."
"$NODE" --check "$SCRIPT_DIR/browser_ctl.mjs" && echo "  browser_ctl.mjs ✓" || echo "  ❌ browser_ctl.mjs 语法错误"
if [ -n "${PY:-}" ]; then
  for f in "$SCRIPT_DIR"/*.py; do
    "$PY" -m py_compile "$f" 2>/dev/null && echo "  $(basename "$f") ✓" || echo "  ❌ $(basename "$f") 语法错误"
  done
  rm -rf "$SCRIPT_DIR/__pycache__"
fi

echo ""
echo "✅ 就绪。共享 profile: $HOME/.workbuddy/browser-profiles/video-downloader"
echo "   首次使用请在弹出的 Chrome 里登录目标站点并切到最高画质（登录态会长期复用）。"
