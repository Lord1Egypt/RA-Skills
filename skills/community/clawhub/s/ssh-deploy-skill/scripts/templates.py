#!/usr/bin/env python3
"""
安装脚本模板和国内镜像源配置
提供常用软件的自动化安装脚本
"""

import os
import sys
from typing import Dict, List

# ============ 国内镜像源配置 ============

MIRROR_CONFIGS = {
    "apt": """# 阿里云镜像源（Ubuntu/Debian）
deb http://mirrors.aliyun.com/ubuntu/ focal main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal main restricted universe multiverse

deb http://mirrors.aliyun.com/ubuntu/ focal-updates main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal-updates main restricted universe multiverse

deb http://mirrors.aliyun.com/ubuntu/ focal-backports main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal-backports main restricted universe multiverse

deb http://mirrors.aliyun.com/ubuntu/ focal-security main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal-security main restricted universe multiverse

# 如果使用的是其他 Ubuntu 版本，请将 focal 替换为对应的版本名（如 bionic, xenial 等）
""",

    "yum": """# 阿里云镜像源（CentOS/RHEL 7/8）
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
""",

    "docker_ce": """# Docker CE 国内镜像加速
# 阿里云镜像加速器（需要先注册获取专属加速地址）
# 参考：https://cr.console.aliyun.com/cn-hangzhou/instances/mirrors

# 方式1：修改 Docker .service 文件中的镜像加速器地址
# 编辑 /etc/docker/daemon.json
{
  "registry-mirrors": [
    "https://<your-id>.mirror.aliyuncs.com",
    "https://docker.mirrors.ustc.edu.cn",
    "https://hub-mirror.c.163.com"
  ]
}

# 方式2：使用阿里云ACR企业版（免费额度）
# 登录：docker login --username=<阿里云用户名> registry.cn-hangzhou.aliyuncs.com
""",

    "npm": """# NPM 国内镜像配置
# 使用淘宝镜像
npm config set registry https://registry.npmmirror.com

# 验证配置
npm config get registry
""",

    "pip": """# PIP 国内镜像配置
# 阿里云镜像源
pip config set global.index-url https://mirrors.aliyun.com/pypi/simple

# 或使用清华镜像
# pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 验证配置
pip config list
""",

    "yarn": """# Yarn 国内镜像配置
yarn config set registry https://registry.npmmirror.com

# 验证配置
yarn config get registry
""",

    "go": """# Go 模块代理（国内）
# 方式1：使用 GOPROXY
export GOPROXY=https://goproxy.cn,direct

# 方式2：写入 ~/.bashrc 或 ~/.profile
echo 'export GOPROXY=https://goproxy.cn,direct' >> ~/.bashrc
source ~/.bashrc
""",

    "maven": """# Maven 镜像配置
# 编辑 ~/.m2/settings.xml 或项目 pom.xml
<mirrors>
  <mirror>
    <id>aliyunmaven</id>
    <mirrorOf>*</mirrorOf>
    <name>阿里云公共仓库</name>
    <url>https://maven.aliyun.com/repository/public</url>
  </mirror>
</mirrors>
""",

    "python_apt": """# Ubuntu/Debian 安装 Python 依赖时使用国内源
# 编辑 /etc/apt/sources.list 替换为 mirrors.aliyun.com
"""
}

# ============ 软件安装模板 ============

TEMPLATES = {
    "install_git.sh": """#!/bin/bash
set -e  # 遇到错误退出

echo "===== 安装 Git ====="

# 检测系统类型
if [ -f /etc/debian_version ]; then
    # Debian/Ubuntu
    echo "检测到 Debian/Ubuntu 系统"
    apt-get update
    apt-get install -y git git-core

elif [ -f /etc/redhat-release ]; then
    # CentOS/RHEL
    echo "检测到 CentOS/RHEL 系统"
    yum install -y git

elif [ -f /etc/alpine-release ]; then
    # Alpine
    echo "检测到 Alpine 系统"
    apk add --no-cache git

else
    echo "未知系统，尝试通用安装..."
    apt-get update && apt-get install -y git || yum install -y git
fi

# 配置 Git（如果需要）
if [ -n "$GIT_USER_NAME" ] && [ -n "$GIT_USER_EMAIL" ]; then
    git config --global user.name "$GIT_USER_NAME"
    git config --global user.email "$GIT_USER_EMAIL"
    echo "已配置 Git 用户信息"
fi

echo "Git 安装完成！版本：$(git --version)"
""",

    "install_docker.sh": """#!/bin/bash
set -e

echo "===== 安装 Docker ====="

# 卸载旧版本
if command -v docker &> /dev/null; then
    echo "检测到已安装 Docker，先卸载..."
    apt-get remove -y docker docker-engine docker.io containerd runc 2>/dev/null || true
    yum remove -y docker docker-client docker-client-latest docker-common docker-latest docker-latest-logrotate docker-logrotate docker-engine 2>/dev/null || true
fi

# 安装依赖
if [ -f /etc/debian_version ]; then
    apt-get update
    apt-get install -y \
        apt-transport-https \
        ca-certificates \
        curl \
        gnupg \
        lsb-release

    # 添加 Docker 官方 GPG 密钥
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

    # 添加 Docker 仓库（使用阿里云镜像）
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://mirrors.aliyun.com/docker-ce/linux/ubuntu \
    $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

    apt-get update
    apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

elif [ -f /etc/redhat-release ]; then
    yum install -y yum-utils device-mapper-persistent-data lvm2

    # 添加 Docker 仓库（使用阿里云镜像）
    yum-config-manager --add-repo https://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo

    yum install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
fi

# 启动 Docker
systemctl start docker
systemctl enable docker

# 配置 Docker 镜像加速（阿里云或国内镜像）
DOCKER_DAEMON_JSON="/etc/docker/daemon.json"
if [ ! -f "$DOCKER_DAEMON_JSON" ]; then
    cat > $DOCKER_DAEMON_JSON <<EOF
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "100m",
    "max-file": "3"
  },
  "registry-mirrors": [
    "https://docker.mirrors.ustc.edu.cn",
    "https://hub-mirror.c.163.com",
    "https://mirror.baidubce.com"
  ],
  "storage-driver": "overlay2"
}
EOF
    systemctl restart docker
    echo "已配置 Docker 镜像加速器"
else
    echo "daemon.json 已存在，请手动添加 registry-mirrors"
fi

# 验证安装
docker --version
docker compose version

echo "Docker 安装完成！"
""",

    "install_mysql.sh": """#!/bin/bash
set -e

echo "===== 安装 MySQL ====="

# 默认版本
MYSQL_VERSION="${MYSQL_VERSION:-8.0}"

if [ -f /etc/debian_version ]; then
    # Ubuntu/Debian - 使用阿里云镜像
    echo "deb http://mirrors.aliyun.com/mysql/apt/debian/ $(lsb_release -cs) mysql-${MYSQL_VERSION}" > /etc/apt/sources.list.d/mysql.list
    echo "deb-src http://mirrors.aliyun.com/mysql/apt/debian/ $(lsb_release -cs) mysql-${MYSQL_VERSION}" >> /etc/apt/sources.list.d/mysql.list

    # 下载并添加 GPG 密钥
    wget -qO- https://mirrors.aliyun.com/mysql/apt/debian/RPM-GPG-KEY-mysql-${MYSQL_VERSION} | apt-key add -

    apt-get update
    apt-get install -y mysql-server mysql-client

    # 安全初始化
    if [ -f "/usr/bin/mysql_secure_installation" ]; then
        # 自动执行安全设置（根据环境变量）
        if [ -n "$MYSQL_ROOT_PASSWORD" ]; then
            service mysql start
            mysql -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '$MYSQL_ROOT_PASSWORD';"
            mysql -e "DELETE FROM mysql.user WHERE User='';"
            mysql -e "DELETE FROM mysql.user WHERE User='root' AND Host NOT IN ('localhost', '127.0.0.1', '::1');"
            mysql -e "DROP DATABASE IF EXISTS test;"
            mysql -e "FLUSH PRIVILEGES;"
        fi
    fi

elif [ -f /etc/redhat-release ]; then
    # CentOS/RHEL - 使用阿里云镜像
    cat > /etc/yum.repos.d/mysql-community.repo <<EOF
[mysql80-community]
name=MySQL 8.0 Community Server
baseurl=https://mirrors.aliyun.com/mysql/yum/mysql-8.0-community/el/7/$basearch/
enabled=1
gpgcheck=1
gpgkey=https://mirrors.aliyun.com/mysql/RPM-GPG-KEY-mysql-8.0
EOF

    yum install -y mysql-community-server
    systemctl start mysqld
    systemctl enable mysqld

    # 获取初始密码
    INITIAL_PASSWORD=$(grep 'temporary password' /var/log/mysqld.log | awk '{print $NF}')
    if [ -n "$INITIAL_PASSWORD" ]; then
        echo "初始密码: $INITIAL_PASSWORD"
    fi
fi

echo "MySQL 安装完成！"
""",

    "install_postgresql.sh": """#!/bin/bash
set -e

echo "===== 安装 PostgreSQL ====="

PG_VERSION="${PG_VERSION:-15}"

if [ -f /etc/debian_version ]; then
    # Ubuntu/Debian - 使用官方仓库（或 pgdg 镜像）
    echo "deb https://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list

    # 添加 GPG 密钥
    wget -qO- https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -

    apt-get update
    apt-get install -y postgresql-$PG_VERSION postgresql-contrib-$PG_VERSION

    # 启动
    systemctl start postgresql@$PG_VERSION-main
    systemctl enable postgresql@$PG_VERSION-main

elif [ -f /etc/redhat-release ]; then
    # CentOS/RHEL - 使用 PGDG 镜像
    cat > /etc/yum.repos.d/pgdg-redhat.repo <<EOF
[pgdg$PG_VERSION]
name=PostgreSQL $PG_VERSION for RHEL $releasever - $basearch
baseurl=https://download.postgresql.org/pub/repos/yum/$PG_VERSION/redhat/rhel-$releasever-$basearch
enabled=1
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-PGDG-$PG_VERSION
EOF

    yum install -y postgresql$PG_VERSION-server postgresql$PG_VERSION-contrib
    /usr/pgsql-$PG_VERSION/bin/postgresql-$PG_VERSION-setup initdb
    systemctl enable postgresql-$PG_VERSION
    systemctl start postgresql-$PGERSION
fi

echo "PostgreSQL $PG_VERSION 安装完成！"
""",

    "install_nginx.sh": """#!/bin/bash
set -e

echo "===== 安装 Nginx ====="

if [ -f /etc/debian_version ]; then
    apt-get update
    apt-get install -y nginx

elif [ -f /etc/redhat-release ]; then
    yum install -y nginx
fi

# 启动
systemctl start nginx 2>/dev/null || service nginx start
systemctl enable nginx 2>/dev/null || chkconfig nginx on

# 配置国内镜像（可选）
if [ -f /etc/nginx/conf.d/default.conf ]; then
    # 备份原始配置
    cp /etc/nginx/conf.d/default.conf /etc/nginx/conf.d/default.conf.bak
fi

echo "Nginx 安装完成！版本：$(nginx -v 2>&1)"
""",

    "install_nodejs.sh": """#!/bin/bash
set -e

echo "===== 安装 Node.js ====="

NODE_VERSION="${NODE_VERSION:-20}"

# 使用 NodeSource 官方仓库（国内使用镜像可能会慢）
if [ -f /etc/debian_version ]; then
    curl -fsSL https://deb.nodesource.com/setup_${NODE_VERSION}.x | bash -
    apt-get install -y nodejs build-essential

elif [ -f /etc/redhat-release ]; then
    curl -fsSL https://rpm.nodesource.com/setup_${NODE_VERSION}.x | bash -
    yum install -y nodejs gcc-c++ make
fi

# 配置 npm 国内镜像
npm config set registry https://registry.npmmirror.com
echo "已设置 npm 镜像为国内源"

node --version
npm --version

echo "Node.js 安装完成！"
""",

    "install_redis.sh": """#!/bin/bash
set -e

echo "===== 安装 Redis ====="

if [ -f /etc/debian_version ]; then
    apt-get update
    apt-get install -y redis-server redis-tools

    # 配置（可选修改绑定地址）
    if [ ! -f /etc/redis/redis.conf.bak ]; then
        cp /etc/redis/redis.conf /etc/redis/redis.conf.bak
    fi

    systemctl restart redis
    systemctl enable redis

elif [ -f /etc/redhat-release ]; then
    yum install -y redis
    systemctl start redis
    systemctl enable redis
fi

redis-cli ping

echo "Redis 安装完成！"
""",

    "install_python.sh": """#!/bin/bash
set -e

echo "===== 安装 Python 和 pip ====="

PYTHON_VERSION="${PYTHON_VERSION:-3.10}"

if [ -f /etc/debian_version ]; then
    apt-get update
    apt-get install -y python${PYTHON_VERSION} python${PYTHON_VERSION}-dev python${PYTHON_VERSION}-venv python3-pip build-essential

    # 设置 python3 默认版本
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python${PYTHON_VERSION} 1

elif [ -f /etc/redhat-release ]; then
    yum install -y python${PYTHON_VERSION} python${PYTHON_VERSION}-devel python${PYTHON_VERSION}-pip
fi

# 配置 pip 国内镜像
pip3 config set global.index-url https://mirrors.aliyun.com/pypi/simple

python3 --version
pip3 --version

echo "Python 安装完成！"
"""
}


def get_template(name: str) -> str:
    """获取模板内容"""
    return TEMPLATES.get(name, "")

def list_available_templates() -> List[str]:
    """列出所有可用模板"""
    return list(TEMPLATES.keys())

def get_mirror_config(pkg: str) -> str:
    """获取镜像源配置"""
    return MIRROR_CONFIGS.get(pkg, "")


def main():
    """命令行接口"""
    import argparse

    parser = argparse.ArgumentParser(description="安装脚本模板管理")
    parser.add_argument("--list", action="store_true", help="列出所有可用模板")
    parser.add_argument("--template", help="模板名称")
    parser.add_argument("--mirror", help="镜像源配置名称")
    parser.add_argument("--output", help="输出文件路径")

    args = parser.parse_args()

    if args.list:
        print("可用模板:")
        for t in sorted(TEMPLATES.keys()):
            print(f"  - {t}")
        print("\n可用镜像源配置:")
        for m in sorted(MIRROR_CONFIGS.keys()):
            print(f"  - {m}")

    elif args.template:
        content = get_template(args.template)
        if not content:
            print(f"❌ 模板不存在: {args.template}")
            sys.exit(1)

        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ 已保存模板到: {args.output}")
        else:
            print(content)

    elif args.mirror:
        content = get_mirror_config(args.mirror)
        if not content:
            print(f"❌ 镜像源配置不存在: {args.mirror}")
            sys.exit(1)

        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ 已保存镜像源配置到: {args.output}")
        else:
            print(content)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
