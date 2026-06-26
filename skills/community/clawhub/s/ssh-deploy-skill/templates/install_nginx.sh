#!/bin/bash
set -e

echo "===== 安装 Nginx ====="

if [ -f /etc/debian_version ]; then
    apt-get update
    apt-get install -y nginx

elif [ -f /etc/redhat-release ]; then
    # CentOS/RHEL: EPEL 仓库可能包含 Nginx
    if ! yum repolist all | grep -q epel; then
        echo "正在安装 EPEL 仓库..."
        yum install -y epel-release
    fi
    yum install -y nginx

else
    echo "未知系统，尝试通用安装..."
    apt-get update && apt-get install -y nginx || yum install -y nginx
fi

# 备份原始配置（如果存在）
if [ -f /etc/nginx/nginx.conf ] && [ ! -f /etc/nginx/nginx.conf.bak ]; then
    cp /etc/nginx/nginx.conf /etc/nginx/nginx.conf.bak
fi

# 启动服务
if systemctl is-active --quiet nginx 2>/dev/null; then
    echo "Nginx 已在运行"
else
    systemctl start nginx 2>/dev/null || service nginx start
    systemctl enable nginx 2>/dev/null || chkconfig nginx on || update-rc.d nginx enable
fi

# 测试配置
nginx -t && echo "Nginx 配置语法正确 ✓" || echo "⚠️  Nginx 配置有错误，请检查"

# 显示版本
nginx -v

echo "Nginx 安装完成！"
