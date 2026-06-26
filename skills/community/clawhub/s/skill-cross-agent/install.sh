#!/bin/bash
# install.sh - Cross-Agent Skill 安装脚本

SKILL_NAME="cross-agent"
SKILL_VERSION="1.0.0"
INSTALL_DIR="${HOME}/.openclaw/skills/${SKILL_NAME}"

echo "🔌 Cross-Agent Skill 安装器"
echo "版本: ${SKILL_VERSION}"
echo ""

# 检查依赖
echo "📋 检查依赖..."
MISSING_DEPS=()

for cmd in sshpass ssh scp ping nc; do
    if ! command -v "$cmd" > /dev/null 2>&1; then
        MISSING_DEPS+=("$cmd")
    fi
done

if [ ${#MISSING_DEPS[@]} -gt 0 ]; then
    echo "❌ 缺少以下依赖: ${MISSING_DEPS[*]}"
    echo ""
    echo "安装命令:"
    echo "  sudo apt update && sudo apt install -y sshpass openssh-client netcat-openbsd iputils-ping"
    echo ""
    read -p "是否自动安装? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        sudo apt update && sudo apt install -y sshpass openssh-client netcat-openbsd iputils-ping
    else
        exit 1
    fi
fi

echo "✅ 所有依赖已满足"
echo ""

# 创建安装目录
echo "📂 安装到: ${INSTALL_DIR}"
mkdir -p "${INSTALL_DIR}"

# 复制文件
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cp -r "${SCRIPT_DIR}/scripts" "${INSTALL_DIR}/"
cp "${SCRIPT_DIR}/SKILL.md" "${INSTALL_DIR}/"
cp "${SCRIPT_DIR}/cross-agent.sh" "${INSTALL_DIR}/"

# 创建 openclaw 命令链接（如果 openclaw 支持）
if command -v openclaw > /dev/null 2>&1; then
    # 检查 skills 目录
    OPENCLAW_SKILLS_DIR="${HOME}/.openclaw/skills"
    if [ -d "$OPENCLAW_SKILLS_DIR" ]; then
        echo "✅ 已注册到 OpenClaw skills 目录"
    fi
fi

# 创建快捷命令别名
echo ""
echo "📝 添加到 .bashrc 的快捷命令（可选）:"
echo ""
echo "# Cross-Agent Skill 快捷命令"
echo "alias ca-scan='${INSTALL_DIR}/cross-agent.sh scan'"
echo "alias ca-test='${INSTALL_DIR}/cross-agent.sh test'"
echo "alias ca-send='${INSTALL_DIR}/cross-agent.sh send'"
echo "alias ca-get='${INSTALL_DIR}/cross-agent.sh get'"
echo "alias ca-wizard='${INSTALL_DIR}/cross-agent.sh wizard'"
echo ""

echo "🎉 安装完成!"
echo ""
echo "使用方法:"
echo "  ${INSTALL_DIR}/cross-agent.sh --help"
echo ""
echo "或者添加到PATH后直接使用:"
echo "  cross-agent.sh --help"
echo ""
echo "快速开始:"
echo "  ${INSTALL_DIR}/cross-agent.sh wizard"