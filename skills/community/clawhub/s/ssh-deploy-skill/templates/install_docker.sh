#!/bin/bash
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
    cat > $DOCKER_DAEMON_JSON <<'EOF'
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
