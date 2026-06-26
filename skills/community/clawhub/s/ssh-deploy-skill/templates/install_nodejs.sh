#!/bin/bash
set -e

echo "===== 安装 Node.js ====="

NODE_VERSION="${NODE_VERSION:-20}"

# 使用 NodeSource 官方仓库（国内自动切换到镜像）
if [ -f /etc/debian_version ]; then
    # Ubuntu/Debian
    curl -fsSL https://deb.nodesource.com/setup_${NODE_VERSION}.x | bash -
    apt-get install -y nodejs build-essential

    # 配置 npm 国内镜像
    npm config set registry https://registry.npmmirror.com
    echo "已设置 npm 镜像为国内源"

elif [ -f /etc/redhat-release ]; then
    # CentOS/RHEL
    curl -fsSL https://rpm.nodesource.com/setup_${NODE_VERSION}.x | bash -
    yum install -y nodejs gcc-c++ make

    # 配置 npm 国内镜像
    npm config set registry https://registry.npmmirror.com
    echo "已设置 npm 镜像为国内源"

else
    echo "未知系统，尝试使用 nvm 方式安装（需要 curl）"
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
    export NVM_DIR="$HOME/.nvm"
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
    nvm install ${NODE_VERSION}
    nvm use ${NODE_VERSION}

    npm config set registry https://registry.npmmirror.com
fi

# 验证安装
node --version
npm --version

# 可选：安装 yarn（如果未安装）
if ! command -v yarn &> /dev/null; then
    echo "是否安装 Yarn？[y/N]"
    read -t 5 -n 1 -r || echo "n"
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        npm install -g yarn
        yarn config set registry https://registry.npmmirror.com
        yarn --version
    fi
fi

echo "Node.js ${NODE_VERSION} 安装完成！"
