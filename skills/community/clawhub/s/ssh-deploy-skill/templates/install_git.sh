#!/bin/bash
set -e

echo "===== 安装 Git ====="

# 检测系统类型
if [ -f /etc/debian_version ]; then
    echo "检测到 Debian/Ubuntu 系统"
    apt-get update
    apt-get install -y git git-core

elif [ -f /etc/redhat-release ]; then
    echo "检测到 CentOS/RHEL 系统"
    yum install -y git

elif [ -f /etc/alpine-release ]; then
    echo "检测到 Alpine 系统"
    apk add --no-cache git

else
    echo "未知系统，尝试通用安装..."
    apt-get update && apt-get install -y git || yum install -y git
fi

# 配置 Git（如果环境变量已设置）
if [ -n "$GIT_USER_NAME" ] && [ -n "$GIT_USER_EMAIL" ]; then
    git config --global user.name "$GIT_USER_NAME"
    git config --global user.email "$GIT_USER_EMAIL"
    echo "已配置 Git 用户信息: $GIT_USER_NAME <$GIT_USER_EMAIL>"
fi

echo "Git 安装完成！版本：$(git --version)"