#!/bin/bash
set -e

echo "===== 安装 Redis ====="

if [ -f /etc/debian_version ]; then
    apt-get update
    apt-get install -y redis-server redis-tools

    # 备份原始配置（如果存在）
    if [ -f /etc/redis/redis.conf ] && [ ! -f /etc/redis/redis.conf.bak ]; then
        cp /etc/redis/redis.conf /etc/redis/redis.conf.bak
    fi

    # 配置允许远程连接（可选，根据需求）
    # sed -i 's/^bind 127.0.0.1/bind 0.0.0.0/' /etc/redis/redis.conf

    systemctl restart redis 2>/dev/null || service redis-server restart
    systemctl enable redis 2>/dev/null || update-rc.d redis-server enable

elif [ -f /etc/redhat-release ]; then
    yum install -y redis
    systemctl start redis
    systemctl enable redis
fi

# 测试连接
if redis-cli ping 2>/dev/null | grep -q PONG; then
    echo "Redis 运行正常 ✓"
else
    echo "Redis 安装完成，但 PING 测试失败，请检查服务状态"
fi

echo "Redis 安装完成！"