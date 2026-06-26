#!/bin/bash
set -e

echo "===== 安装 Python 和 pip ====="

PYTHON_VERSION="${PYTHON_VERSION:-3.10}"

if [ -f /etc/debian_version ]; then
    apt-get update
    apt-get install -y python${PYTHON_VERSION} python${PYTHON_VERSION}-dev python${PYTHON_VERSION}-venv python3-pip build-essential curl

    # 设置 python3 默认版本（如果已存在多个版本）
    if command -v update-alternatives &> /dev/null; then
        update-alternatives --install /usr/bin/python3 python3 /usr/bin/python${PYTHON_VERSION} 1
    fi

elif [ -f /etc/redhat-release ]; then
    yum install -y python${PYTHON_VERSION} python${PYTHON_VERSION}-devel python${PYTHON_VERSION}-pip gcc
else
    echo "未知系统，尝试通用安装..."
    apt-get update && apt-get install -y python3 python3-dev python3-venv python3-pip || \
    yum install -y python3 python3-devel python3-pip
fi

# 配置 pip 国内镜像（国内服务器才配置，可通过环境变量控制）
if [ -n "$CONFIGURE_PIP_MIRROR" ] || [ "$(curl -s https://www.google.com)" = "" ]; then
    pip3 config set global.index-url https://mirrors.aliyun.com/pypi/simple
    echo "已设置 pip 镜像为阿|里云国内源"
fi

python3 --version
pip3 --version

echo "Python 安装完成！"