#!/usr/bin/env bash
# wechat-local-reader 安装脚本（macOS / Linux）
# 在 WorkBuddy Bash 或系统终端中执行： bash tool/setup.sh
set -e
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

echo "[1/3] 创建隔离虚拟环境 .venv ..."
python3 -m venv .venv

echo "[2/3] 安装依赖并注册 wechat-cli 命令 ..."
.venv/bin/python -m pip install --upgrade pip -q
.venv/bin/python -m pip install -e . -q

echo "[3/3] 生成启动器 wechat-cli ..."
cat > wechat-cli <<'EOF'
#!/bin/sh
exec "$(cd "$(dirname "$0")" && pwd)/.venv/bin/wechat-cli" "$@"
EOF
chmod +x wechat-cli

echo
echo "安装完成。把 $ROOT 加入 PATH 后，即可直接运行："
echo "    wechat-cli --help"
echo "或在该目录内使用： ./wechat-cli --help"
