#!/bin/bash
#===========================================================
# 环境变量配置脚本
#===========================================================

TOOLCHAIN="${TOOLCHAIN:-/workspace/toolchain}"
ENV_FILE="/workspace/.toolchain_env"

ENV_BLOCK=$(cat << 'ENDENV'
# === OpenClaw Toolchain Environment ===
export TOOLCHAIN=/workspace/toolchain
export PATH=/workspace/toolchain/go/bin:/workspace/toolchain/erlang/bin:/workspace/toolchain/elixir/bin:/workspace/toolchain/ruby/bin:/workspace/toolchain/lua/bin:/workspace/toolchain/apache-maven-3.9.6/bin:/workspace/toolchain/bin:$PATH
export JAVA_HOME=/workspace/toolchain/jdk-21.0.10+7
export RUSTUP_HOME=/workspace/toolchain/rust
export CARGO_HOME=/workspace/toolchain/rust/.cargo
export LD_LIBRARY_PATH=/workspace/toolchain/erlang/lib:$LD_LIBRARY_PATH
# =====================================
ENDENV
)

printf '%s\n' "$ENV_BLOCK" > "$ENV_FILE"
echo "[OK] 环境变量已写入 $ENV_FILE"

# 尝试追加到 bashrc（如果可写）
BASHRC="${HOME}/.bashrc"
if [ -w "$BASHRC" ] 2>/dev/null; then
  if ! grep -q "OpenClaw Toolchain Environment" "$BASHRC" 2>/dev/null; then
    printf '%s\n' "$ENV_BLOCK" >> "$BASHRC"
    echo "[OK] 环境变量已追加到 ~/.bashrc"
  fi
fi

echo ""
echo "已配置工具链:"
echo "  TOOLCHAIN=$TOOLCHAIN"
echo "  JAVA_HOME=$TOOLCHAIN/jdk-21.0.10+7"
echo "  PATH 包含: go/bin erlang/bin elixir/bin ruby/bin lua/bin maven/bin"
echo ""
echo "加载环境变量:"
echo "  source $ENV_FILE"
