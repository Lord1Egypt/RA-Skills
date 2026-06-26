#!/bin/bash
set -e

echo "===== 安装 PostgreSQL ====="

PG_VERSION="${PG_VERSION:-15}"

# 预定义版本映射（如果用户指定的版本没有对应的仓库，尝试自动调整）
if [ -f /etc/debian_version ]; then
    # Ubuntu/Debian - 使用 PGDG 官方仓库（国内有镜像）
    # Add PostgreSQL GPG key (modern method using signed-by)
    install -d -m 0755 /etc/apt/keyrings
    wget -qO- https://www.postgresql.org/media/keys/ACCC4CF8.asc | gpg --dearmor -o /etc/apt/keyrings/postgresql.gpg

    # 添加仓库（使用阿|里云镜像或官方）
    echo "deb [signed-by=/etc/apt/keyrings/postgresql.gpg] https://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list

    apt-get update
    apt-get install -y postgresql-$PG_VERSION postgresql-contrib-$PG_VERSION postgresql-client-$PG_VERSION

    # 启动服务
    systemctl start postgresql@$PG_VERSION-main
    systemctl enable postgresql@$PG_VERSION-main

    # 设置 postgres 用户密码（可选，如设置了 PG_POSTGRES_PASSWORD）
    if [ -n "$PG_POSTGRES_PASSWORD" ]; then
        sudo -u postgres psql -c "ALTER USER postgres PASSWORD '$PG_POSTGRES_PASSWORD';"
    fi

elif [ -f /etc/redhat-release ]; then
    # CentOS/RHEL - 使用 PGDG 镜像
    cat > /etc/yum.repos.d/pgdg-redhat.repo <<EOF
[pgdg${PG_VERSION}]
name=PostgreSQL ${PG_VERSION} for RHEL \$releasever - \$basearch
baseurl=https://download.postgresql.org/pub/repos/yum/${PG_VERSION}/redhat/rhel-\$releasever-\$basearch
enabled=1
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-PGDG-${PG_VERSION}
EOF

    # 安装
    yum install -y postgresql${PG_VERSION}-server postgresql${PG_VERSION}-contrib postgresql${PG_VERSION}

    # 初始化数据库
    /usr/pgsql-${PG_VERSION}/bin/postgresql-${PG_VERSION}-setup initdb

    systemctl enable postgresql-${PG_VERSION}
    systemctl start postgresql-${PG_VERSION}

    # 设置密码（可选）
    if [ -n "$PG_POSTGRES_PASSWORD" ]; then
        sudo -u postgres psql -c "ALTER USER postgres PASSWORD '$PG_POSTGRES_PASSWORD';"
    fi
else
    echo "不支持的系统，请手动安装 PostgreSQL $PG_VERSION"
    exit 1
fi

# 打印连接信息
echo "PostgreSQL ${PG_VERSION} 安装完成！"
echo "本地连接: psql -U postgres"
echo "远程连接需要配置 pg_hba.conf 并重启服务"
