#!/bin/bash
# native-host/install.sh
# 将 Native Messaging Host manifest 安装到 Chrome/Chromium 识别目录
#
# 用法:
#   bash native-host/install.sh <扩展ID>
#   （推荐用 bash 直接运行，避免因执行位丢失导致"权限不够"报错）
#
# 扩展 ID 获取方式:
#   1. 在 Chrome 地址栏输入 chrome://extensions
#   2. 开启"开发者模式"
#   3. 加载解压缩的扩展（选择 chrome-extension/ 目录）
#   4. 复制扩展卡片上显示的 ID（32 位小写字母）
#
# 支持平台：
#   macOS   - Google Chrome、Chrome Canary、Chromium
#   Linux   - Google Chrome、Chromium（含 Ubuntu 常见路径）
#   Windows - 生成 manifest + install-windows.bat，手动运行 bat 注册注册表
#             （支持在 Git Bash / MINGW / Cygwin 下运行本脚本）
#   WSL     - 生成 manifest + install-windows.bat，并说明路径注意事项

set -euo pipefail

EXTENSION_ID="${1:-}"

if [ -z "$EXTENSION_ID" ]; then
  echo "错误: 需要提供扩展 ID" >&2
  echo "用法: $0 <chrome-extension-id>" >&2
  exit 1
fi

# 验证扩展 ID 格式（32 位小写字母）
if ! [[ "$EXTENSION_ID" =~ ^[a-z]{32}$ ]]; then
  echo "警告: 扩展 ID 格式可能不正确（预期 32 位小写字母）: $EXTENSION_ID" >&2
fi

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HOST_SCRIPT="$REPO_DIR/native-host/host.js"

# 确保 host.js 存在
if [ ! -f "$HOST_SCRIPT" ]; then
  echo "错误: host.js 不存在: $HOST_SCRIPT" >&2
  exit 1
fi

# 检测 node 路径
NODE_PATH="$(which node 2>/dev/null || echo '')"
if [ -z "$NODE_PATH" ]; then
  echo "错误: 未找到 node，请先安装 Node.js" >&2
  exit 1
fi
echo "Node.js 路径: $NODE_PATH"

# ── 检测操作系统 ─────────────────────────────────────────────────────────────
# uname -s 返回: Darwin / Linux / MINGW64_NT-* / CYGWIN_NT-* / MSYS_NT-*
OS_RAW="$(uname -s 2>/dev/null || echo 'unknown')"
case "$OS_RAW" in
  Darwin)               OS="macos" ;;
  Linux)
    # WSL 内核版本信息里含 Microsoft 字样
    if grep -qi microsoft /proc/version 2>/dev/null; then
      OS="wsl"
    else
      OS="linux"
    fi
    ;;
  MINGW*|MSYS*|CYGWIN*) OS="windows" ;;
  *)                    OS="unknown" ;;
esac

echo "平台: $OS_RAW → $OS"

# ── 生成 manifest JSON 内容 ──────────────────────────────────────────────────
make_manifest() {
  local path="$1"
  cat <<MANIFEST
{
  "name": "com.today.earnings.host",
  "description": "Today Earnings Native Messaging Host",
  "path": "${path}",
  "type": "stdio",
  "allowed_origins": [
    "chrome-extension://${EXTENSION_ID}/"
  ]
}
MANIFEST
}

# ── 安装 manifest 到指定目录（Unix 路径）────────────────────────────────────
install_to_dir() {
  local dir="$1"
  local label="$2"
  local wrapper="$3"
  if ! mkdir -p "$dir" 2>/dev/null; then
    echo "错误: 无法创建目录 $dir（权限不足或路径无效）" >&2
    echo "  提示: 确认当前用户对该路径有写入权限，或使用 sudo 执行。" >&2
    exit 1
  fi
  local manifest_path="$dir/com.today.earnings.host.json"
  if ! make_manifest "$wrapper" > "$manifest_path" 2>/dev/null; then
    echo "错误: 无法写入 Manifest 文件 $manifest_path（磁盘已满或权限不足）" >&2
    exit 1
  fi
  echo "  [$label] Manifest → $manifest_path"
}

# ── 生成 Unix 包装脚本（macOS / Linux 共用）─────────────────────────────────
make_unix_wrapper() {
  WRAPPER_PATH="$REPO_DIR/native-host/run-host.sh"
  if ! cat > "$WRAPPER_PATH" <<WRAPPER
#!/bin/bash
exec "${NODE_PATH}" "\$(dirname "\$0")/host.js"
WRAPPER
  then
    echo "错误: 无法写入包装脚本 $WRAPPER_PATH（磁盘已满或权限不足）" >&2
    exit 1
  fi
  chmod +x "$WRAPPER_PATH"
  echo "包装脚本: $WRAPPER_PATH"
}

# ── 生成 Windows 相关文件（manifest + bat 包装 + bat 注册器）────────────────
# $1: manifest 中 path 字段使用的路径（Windows 路径或 Unix 路径）
# $2: 是否为 WSL 模式（"wsl" 或 ""）
make_windows_artifacts() {
  local manifest_path_value="$1"
  local wsl_mode="${2:-}"

  # 1. 生成 run-host.bat（Windows 包装脚本，Chrome 实际调用的入口）
  BAT_WRAPPER="$REPO_DIR/native-host/run-host.bat"
  cat > "$BAT_WRAPPER" <<'BATWRAPPER'
@echo off
REM run-host.bat - Chrome Native Messaging Host 启动入口（Windows）
REM Chrome 调用此脚本时会通过 stdin/stdout 与 host.js 通信
node "%~dp0host.js"
BATWRAPPER
  echo "  Windows 包装脚本: $BAT_WRAPPER"

  # 2. 生成 manifest（指向 run-host.bat 的路径）
  MANIFEST_FILE="$REPO_DIR/native-host/com.today.earnings.host.json"
  make_manifest "$manifest_path_value" > "$MANIFEST_FILE"
  echo "  Manifest 文件: $MANIFEST_FILE"

  # 3. 生成 install-windows.bat（注册表注册脚本）
  INSTALL_BAT="$REPO_DIR/native-host/install-windows.bat"
  cat > "$INSTALL_BAT" <<'BATEOF'
@echo off
REM native-host/install-windows.bat
REM 将 Native Messaging Host 注册到 Windows 注册表
REM
REM 运行方式：
REM   在文件资源管理器中双击，或在 CMD/PowerShell 中执行：
REM   native-host\install-windows.bat
REM
REM 注意：脚本以普通用户权限运行即可（写入 HKCU，不需要管理员）。

SET SCRIPT_DIR=%~dp0
SET MANIFEST_PATH=%SCRIPT_DIR%com.today.earnings.host.json

echo.
echo === Today Earnings Native Host 注册 ===
echo.
echo Manifest 路径: %MANIFEST_PATH%
echo.

echo [1/2] 注册 Google Chrome Native Messaging Host...
REG ADD "HKCU\Software\Google\Chrome\NativeMessagingHosts\com.today.earnings.host" ^
    /ve /t REG_SZ /d "%MANIFEST_PATH%" /f
if %ERRORLEVEL% NEQ 0 (
  echo   警告: Chrome 注册失败（可能未安装 Chrome）
) else (
  echo   Chrome 注册成功
)

echo.
echo [2/2] 注册 Chromium Native Messaging Host...
REG ADD "HKCU\Software\Chromium\NativeMessagingHosts\com.today.earnings.host" ^
    /ve /t REG_SZ /d "%MANIFEST_PATH%" /f
if %ERRORLEVEL% NEQ 0 (
  echo   警告: Chromium 注册失败（可能未安装 Chromium）
) else (
  echo   Chromium 注册成功
)

echo.
echo 注册完成！请重启 Chrome 并在 chrome://extensions 中刷新扩展。
echo.
pause
BATEOF
  echo "  Windows 注册脚本: $INSTALL_BAT"
}

INSTALLED=0

# ════════════════════════════════════════════════════════════════════════════
# macOS
# ════════════════════════════════════════════════════════════════════════════
if [[ "$OS" == "macos" ]]; then
  echo ""
  echo "安装平台: macOS"

  make_unix_wrapper
  echo ""

  # Google Chrome
  install_to_dir \
    "$HOME/Library/Application Support/Google/Chrome/NativeMessagingHosts" \
    "Google Chrome" \
    "$WRAPPER_PATH"
  INSTALLED=$((INSTALLED + 1))

  # Chrome Canary（仅当目录已存在时）
  CANARY_PARENT="$HOME/Library/Application Support/Google/Chrome Canary"
  if [ -d "$CANARY_PARENT" ]; then
    install_to_dir \
      "$CANARY_PARENT/NativeMessagingHosts" \
      "Chrome Canary" \
      "$WRAPPER_PATH"
    INSTALLED=$((INSTALLED + 1))
  fi

  # Chromium（仅当目录已存在时）
  CHROMIUM_PARENT="$HOME/Library/Application Support/Chromium"
  if [ -d "$CHROMIUM_PARENT" ]; then
    install_to_dir \
      "$CHROMIUM_PARENT/NativeMessagingHosts" \
      "Chromium" \
      "$WRAPPER_PATH"
    INSTALLED=$((INSTALLED + 1))
  fi

# ════════════════════════════════════════════════════════════════════════════
# Linux（非 WSL）
# ════════════════════════════════════════════════════════════════════════════
elif [[ "$OS" == "linux" ]]; then
  echo ""
  echo "安装平台: Linux"

  make_unix_wrapper
  echo ""

  # Google Chrome（用户级，始终安装）
  install_to_dir \
    "$HOME/.config/google-chrome/NativeMessagingHosts" \
    "Google Chrome" \
    "$WRAPPER_PATH"
  INSTALLED=$((INSTALLED + 1))

  # Chromium（用户级，检测到 chromium 命令或配置目录时安装）
  if command -v chromium-browser &>/dev/null \
      || command -v chromium &>/dev/null \
      || [ -d "$HOME/.config/chromium" ]; then
    install_to_dir \
      "$HOME/.config/chromium/NativeMessagingHosts" \
      "Chromium" \
      "$WRAPPER_PATH"
    INSTALLED=$((INSTALLED + 1))
  fi

  # Chrome Beta / Dev / Unstable（配置目录存在时安装）
  for VARIANT in google-chrome-beta google-chrome-unstable; do
    if [ -d "$HOME/.config/$VARIANT" ]; then
      install_to_dir \
        "$HOME/.config/$VARIANT/NativeMessagingHosts" \
        "$VARIANT" \
        "$WRAPPER_PATH"
      INSTALLED=$((INSTALLED + 1))
    fi
  done

  echo ""
  echo "提示（Ubuntu）:"
  echo "  - 如果你使用的是 snap 版 Chromium（Ubuntu 22.04+ 默认），"
  echo "    Native Messaging 支持受限，建议改用 deb 版 Google Chrome："
  echo "    wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -"
  echo "    sudo sh -c 'echo deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main > /etc/apt/sources.list.d/google-chrome.list'"
  echo "    sudo apt-get update && sudo apt-get install google-chrome-stable"

# ════════════════════════════════════════════════════════════════════════════
# Windows（Git Bash / MINGW / Cygwin）
# ════════════════════════════════════════════════════════════════════════════
elif [[ "$OS" == "windows" ]]; then
  echo ""
  echo "安装平台: Windows (${OS_RAW})"
  echo ""

  # 在 Git Bash / MINGW 下，用 cygpath 转换为 Windows 路径
  if command -v cygpath &>/dev/null; then
    WIN_REPO_DIR="$(cygpath -w "$REPO_DIR")"
    MANIFEST_PATH_VALUE="${WIN_REPO_DIR}\\native-host\\run-host.bat"
  else
    # 无 cygpath 时，保留 Unix 路径并提示用户核对
    MANIFEST_PATH_VALUE="$REPO_DIR/native-host/run-host.bat"
    echo "  警告: 无法自动转换为 Windows 路径，manifest 中 path 字段可能需要手动修正。"
  fi

  make_windows_artifacts "$MANIFEST_PATH_VALUE"
  INSTALLED=0

  echo ""
  echo "Windows 手动安装步骤："
  echo "  1. 确认 manifest 文件路径正确（com.today.earnings.host.json）"
  echo "     - 文件中的 'path' 字段必须指向 run-host.bat 的 Windows 绝对路径"
  echo "     - 示例: C:\\Users\\你的用户名\\...\\native-host\\run-host.bat"
  echo "  2. 在文件资源管理器中找到 native-host\\install-windows.bat"
  echo "  3. 双击运行（或在 CMD/PowerShell 中执行）"
  echo "  4. 脚本会将 manifest 路径写入 HKCU 注册表（Chrome 和 Chromium）"
  echo "  5. 重启 Chrome 并在 chrome://extensions 中刷新扩展"

# ════════════════════════════════════════════════════════════════════════════
# WSL（Windows Subsystem for Linux）
# ════════════════════════════════════════════════════════════════════════════
elif [[ "$OS" == "wsl" ]]; then
  echo ""
  echo "安装平台: WSL (Windows Subsystem for Linux)"
  echo ""
  echo "⚠️  WSL 注意事项："
  echo "  Chrome 运行在 Windows 侧，无法直接访问 WSL 文件系统（/home/...）下的文件。"
  echo "  建议将仓库克隆到 Windows 文件系统，例如 /mnt/c/Users/<用户名>/repos/today-earnings-skill，"
  echo "  然后在 Windows 侧运行 native-host\\install-windows.bat 完成注册。"
  echo ""

  # 尝试转换为 Windows 路径
  if command -v wslpath &>/dev/null; then
    WIN_REPO_DIR="$(wslpath -w "$REPO_DIR" 2>/dev/null || echo '')"
    if [ -n "$WIN_REPO_DIR" ]; then
      MANIFEST_PATH_VALUE="${WIN_REPO_DIR}\\native-host\\run-host.bat"
      echo "  检测到 Windows 路径: $WIN_REPO_DIR"
    else
      MANIFEST_PATH_VALUE="$REPO_DIR/native-host/run-host.bat"
      echo "  警告: 路径转换失败，manifest 中 path 字段需要手动修正为 Windows 路径。"
    fi
  else
    MANIFEST_PATH_VALUE="$REPO_DIR/native-host/run-host.bat"
    echo "  警告: wslpath 不可用，manifest 中 path 字段需要手动修正为 Windows 路径。"
  fi

  make_windows_artifacts "$MANIFEST_PATH_VALUE" "wsl"
  INSTALLED=0

  echo ""
  echo "WSL 手动安装步骤："
  echo "  1. 将仓库路径确认可从 Windows 访问（例如 \\\\wsl\$\\...）"
  echo "     或将仓库改放到 /mnt/c/... 路径下"
  echo "  2. 核对 com.today.earnings.host.json 中的 'path' 字段"
  echo "     必须是 Windows 可访问的绝对路径，例如："
  echo "     C:\\Users\\<用户名>\\repos\\today-earnings-skill\\native-host\\run-host.bat"
  echo "  3. 在 Windows 侧运行 native-host\\install-windows.bat（双击或在 CMD 中执行）"
  echo "  4. 重启 Chrome 并在 chrome://extensions 中刷新扩展"

# ════════════════════════════════════════════════════════════════════════════
# 未知平台
# ════════════════════════════════════════════════════════════════════════════
else
  echo ""
  echo "⚠️  未能识别操作系统（$OS_RAW），无法自动安装。" >&2
  echo "请参考 references/usage_guide.md 中的手动安装说明。" >&2
  exit 1
fi

echo ""
if [ "$INSTALLED" -gt 0 ]; then
  echo "✅ Native Host 已安装（共 $INSTALLED 个位置）"
  if [ -n "${WRAPPER_PATH:-}" ]; then
    echo "   Host 脚本: $WRAPPER_PATH"
  fi
  echo "   扩展 ID: $EXTENSION_ID"
  echo ""
  echo "下一步: 重启 Chrome 或在 chrome://extensions 中重新加载扩展"
else
  echo "📄 文件已生成，请按上方说明完成手动注册"
  echo ""
  echo "下一步: 完成注册后，重启 Chrome 并在 chrome://extensions 中重新加载扩展"
fi
