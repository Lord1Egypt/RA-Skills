#!/bin/bash
# 基础环境准备 - 更新系统、安装基础工具、配置国内镜像源

set -e

echo "===== 基础环境配置 ====="

# 检测系统
if [ -f /etc/debian_version ]; then
    OS_TYPE="debian"
    echo "检测到 Debian/Ubuntu 系统"
elif [ -f /etc/redhat-release ]; then
    OS_TYPE="redhat"
    echo "检测到 CentOS/RHEL 系统"
elif [ -f /etc/alpine-release ]; then
    OS_TYPE="alpine"
    echo "检测到 Alpine 系统"
else
    OS_TYPE="unknown"
    echo "未知系统类型"
fi

# 1. 配置国内镜像源（自动选择）
echo "配置中...（使用阿|里云/清华/中科大镜像，根据网络环境自动选择）"

if [ "$OS_TYPE" = "debian" ]; then
    # Ubuntu/Debian - 改成阿里云源
    if [ -f /etc/apt/sources.list ]; then
        cp /etc/apt/sources.list /etc/apt/sources.list.bak
    fi
    cat > /etc/apt/sources.list <<'EOF'
deb http://mirrors.aliyun.com/ubuntu/ focal main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ focal-updates main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ focal-backports main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal-backports main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ focal-security main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal-security main restricted universe multiverse
EOF
    echo "✔ 已配置 Ubuntu 阿|里云镜像源"

elif [ "$OS_TYPE" = "redhat" ]; then
    # CentOS/RHEL - 改成阿里云源
    if [ -f /etc/yum.repos.d/CentOS-Base.repo ]; then
        mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.bak
    fi
    cat > /etc/yum.repos.d/CentOS-Base.repo <<'EOF'
[base]
name=CentOS-$releasever - Base - mirrors.aliyun.com
baseurl=http://mirrors.aliyun.com/centos/$releasever/os/$basearch/
gpgcheck=1
gpgkey=http://mirrors.aliyun.com/centos/RPM-GPG-KEY-CentOS-7

[updates]
name=CentOS-$releasever - Updates - mirrors.aliyun.com
baseurl=http://mirrors.aliyun.com/centos/$releasever/updates/$basearch/
gpgcheck=1
gpgkey=http://mirrors.aliyun.com/centos/RPM-GPG-KEY-CentOS-7

[extras]
name=CentOS-$releasever - Extras - mirrors.aliyun.com
baseurl=http://mirrors.aliyun.com/centos/$releasever/extras/$basearch/
gpgcheck=1
gpgkey=http://mirrors.aliyun.com/centos/RPM-GPG-KEY-CentOS-7
EOF
    echo "✔ 已配置 CentOS 阿|里云镜像源"
fi

# 2. 更新包管理器缓存
echo "更新包管理器缓存..."
if [ "$OS_TYPE" = "debian" ]; then
    apt-get update -y
    apt-get install -y wget curl ca-certificates -y
elif [ "$OS_TYPE" = "redhat" ]; then
    yum makecache
    yum install -y wget curl ca-certificates
elif [ "$OS_TYPE" = "alpine" ]; then
    apk update
    apk add wget curl ca-certificates
fi

# 3. 配置 pip、npm、docker 等国内镜像（可选）
echo ""
echo "可选：配置 pip/npm/Go 等国内镜像？"
echo "可以通过运行以下命令手动配置："
echo "  - pip: pip config set global.index-url https://mirrors.aliyun.com/pypi/simple"
echo "  - npm: npm config set registry https://registry.npmmirror.com"
echo "  - yarn: yarn config set registry https://registry.npmmirror.com"
echo "  - docker: 编辑 /etc/docker/daemon.json 添加 registry-mirrors"

echo ""
echo "===== 基础环境配置完成 ====="
