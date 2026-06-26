#!/bin/bash
# SSH Deploy Skill - 自动设置脚本（适配 Ubuntu 24.04+）

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_DIR="${HOME}/.ssh-deploy"

echo "===== SSH Deploy Skill 设置 ====="

# 1. 检查 Python
echo "检查 Python3..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未找到，请先安装 Python 3.8+"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | awk '{print $2}')
echo "✓ Python $PYTHON_VERSION"

# 2. 检查/安装 paramiko
echo "检查 Python 依赖 paramiko..."

# 尝试导入 paramiko
if python3 -c "import paramiko" 2>/dev/null; then
    echo "✓ paramiko 已安装"
else
    echo "尝试安装 paramiko..."

    # 方法1：使用系统包（推荐 Ubuntu/Debian）
    if command -v apt-get &> /dev/null; then
        echo "检测到 apt，尝试安装系统包 python3-paramiko..."
        if sudo apt-get install -y python3-paramiko 2>/dev/null; then
            echo "✓ python3-paramiko 已通过 apt 安装"
        else
            echo "⚠️  apt 安装失败，尝试 pip..."

            # 方法2：使用虚拟环境
            if [ ! -d "${HOME}/.venv/ssh-deploy" ]; then
                echo "创建虚拟环境 ~/.venv/ssh-deploy..."
                python3 -m venv "${HOME}/.venv/ssh-deploy"
            fi

            source "${HOME}/.venv/ssh-deploy/bin/activate"
            pip install --upgrade pip
            pip install paramiko
            echo "✓ paramiko 已安装到虚拟环境: ${HOME}/.venv/ssh-deploy"
            echo "注意：后续运行 deploy.py 需要使用虚拟环境的 python:"
            echo "  ${HOME}/.venv/ssh-deploy/bin/python scripts/deploy.py ..."
        fi
    else
        # 非 Debian 系统，直接使用 pip（可能需要 sudo）
        echo "使用 pip 安装 paramiko..."
        if pip3 install --user paramiko 2>&1 | grep -q "Successfully"; then
            echo "✓ paramiko 已安装到用户目录"
        else
            echo "❌ paramiko 安装失败，请手动安装："
            echo "   pip3 install paramiko"
            exit 1
        fi
    fi
fi

# 3. 检查系统命令
echo "检查系统命令..."
for cmd in ssh scp; do
    if command -v $cmd &> /dev/null; then
        echo "  ✓ $cmd"
    else
        echo "  ❌ $cmd 未找到（需要安装 OpenSSH 客户端）"
        echo "     Ubuntu/Debian: apt-get install openssh-client"
        echo "     CentOS/RHEL:   yum install openssh-clients"
    fi
done

# 4. 创建配置目录
echo "创建配置目录: $CONFIG_DIR"
mkdir -p "$CONFIG_DIR"

# 5. 生成示例 inventory.json
if [ ! -f "$CONFIG_DIR/inventory.json" ]; then
    cat > "$CONFIG_DIR/inventory.json" <<'EOF'
{
  "servers": {
    "example": {
      "host": "192.168.1.100",
      "port": 22,
      "user": "root",
      "ssh_key": "~/.ssh/id_rsa",
      "groups": ["example"],
      "tags": ["示例"],
      "description": "示例服务器，请修改为实际配置"
    }
  }
}
EOF
    echo "✓ 已创建示例 inventory.json"
else
    echo "ℹ inventory.json 已存在，跳过"
fi

# 6. 完成
echo ""
echo "===== 设置完成 ====="
echo ""
echo "下一步："
echo "1. 编辑 $CONFIG_DIR/inventory.json，添加你的服务器信息"
echo "2. 使用以下命令测试连接："
echo "   python3 scripts/deploy.py exec example \"uptime\""
echo ""
echo "如果 paramiko 安装到了虚拟环境，请使用："
echo "   ${HOME}/.venv/ssh-deploy/bin/python scripts/deploy.py exec example \"uptime\""
echo ""
echo "更多文档请查看 README.md 和 docs/ 目录"
