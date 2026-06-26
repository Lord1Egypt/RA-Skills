#!/bin/bash
set -e

echo "===== 安装 MySQL ====="

# 默认版本
MYSQL_VERSION="${MYSQL_VERSION:-8.0}"

if [ -f /etc/debian_version ]; then
    # Ubuntu/Debian - 使用阿|里云镜像
    echo "deb [signed-by=/etc/apt/keyrings/mysql.gpg] http://mirrors.aliyun.com/mysql/apt/debian/ $(lsb_release -cs) mysql-${MYSQL_VERSION}" > /etc/apt/sources.list.d/mysql.list
    echo "deb-src [signed-by=/etc/apt/keyrings/mysql.gpg] http://mirrors.aliyun.com/mysql/apt/debian/ $(lsb_release -cs) mysql-${MYSQL_VERSION}" >> /etc/apt/sources.list.d/mysql.list

    # 下载并添加 GPG 密钥 (modern signed-by method)
    install -d -m 0755 /etc/apt/keyrings
    wget -qO- https://mirrors.aliyun.com/mysql/apt/debian/RPM-GPG-KEY-mysql-${MYSQL_VERSION} | gpg --dearmor -o /etc/apt/keyrings/mysql.gpg

    apt-get update
    apt-get install -y mysql-server mysql-client

    # 安全初始化（如果设置了 MYSQL_ROOT_PASSWORD）
    if [ -n "$MYSQL_ROOT_PASSWORD" ]; then
        service mysql start
        mysql -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '$MYSQL_ROOT_PASSWORD';"
        mysql -e "DELETE FROM mysql.user WHERE User='';"
        mysql -e "DELETE FROM mysql.user WHERE User='root' AND Host NOT IN ('localhost', '127.0.0.1', '::1');"
        mysql -e "DROP DATABASE IF EXISTS test;"
        mysql -e "FLUSH PRIVILEGES;"
        echo "已设置 root 密码"
    fi

    systemctl enable mysql || update-rc.d mysql enable

elif [ -f /etc/redhat-release ]; then
    # CentOS/RHEL - 使用阿|里云镜像
    cat > /etc/yum.repos.d/mysql-community.repo <<EOF
[mysql${MYSQL_VERSION}-community]
name=MySQL ${MYSQL_VERSION} Community Server
baseurl=https://mirrors.aliyun.com/mysql/yum/mysql-${MYSQL_VERSION}-community/el/7/\$basearch/
enabled=1
gpgcheck=1
gpgkey=https://mirrors.aliyun.com/mysql/RPM-GPG-KEY-mysql-${MYSQL_VERSION}
EOF

    yum install -y mysql-community-server
    systemctl start mysqld
    systemctl enable mysqld

    # 获取初始密码
    if [ -z "$MYSQL_ROOT_PASSWORD" ]; then
        INITIAL_PASSWORD=$(grep 'temporary password' /var/log/mysqld.log | awk '{print $NF}')
        if [ -n "$INITIAL_PASSWORD" ]; then
            echo "初始密码: $INITIAL_PASSWORD（请及时修改）"
        fi
    fi
fi

# 测试连接
if command -v mysql &> /dev/null; then
    echo "MySQL 客户端版本：$(mysql --version)"
fi

echo "MySQL ${MYSQL_VERSION} 安装完成！"
