# WSL 运维命令参考

## WSL 访问方式

### 方式1：直接执行（首选，需开启安全策略"系统级工具"）
```bash
wsl.exe -e bash -c '命令'
```

### 方式2：以 root 执行（绕过 sudo 密码）
```bash
wsl.exe -e bash -c "echo '123456' | su -c '命令' - root"
```

### 方式3：SSH root 连接（备用）
```bash
sshpass -p "123456" ssh root@<WSL_IP> "命令"
```

## 服务安装脚本模板

将脚本写入 WSL 的 `/tmp/`，然后通过 `su -c` 以 root 执行：

```bash
# 写入脚本
wsl.exe -e bash -c 'cat > /tmp/install_xxx.sh << "EOF"
#!/bin/bash
set -e
exec &> /tmp/install_xxx.log
echo "=== START $(date) ==="
# ... 安装命令 ...
echo "=== END $(date) ==="
EOF
chmod +x /tmp/install_xxx.sh'

# 执行脚本
wsl.exe -e bash -c "echo '123456' | su -c 'bash /tmp/install_xxx.sh' - root"

# 查看日志
wsl.exe -e bash -c 'cat /tmp/install_xxx.log'
```

## MySQL 安装

```bash
# 卸载旧版
DEBIAN_FRONTEND=noninteractive aptitude purge -y mysql-server mysql-client mysql-common mysql-server-core mysql-client-core
rm -rf /var/lib/mysql /etc/mysql /var/log/mysql
aptitude purge -y ~c

# 安装
DEBIAN_FRONTEND=noninteractive aptitude install -y mysql-server

# 启动
systemctl enable mysql
systemctl start mysql

# 设置 root 密码
mysql -u root -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '123456'; FLUSH PRIVILEGES;"

# 验证
mysql -u root -p123456 -e "SELECT VERSION(); SHOW DATABASES;"
```

## Redis 安装

```bash
# 安装
DEBIAN_FRONTEND=noninteractive aptitude install -y redis-server

# 配置（密码 + 外部访问）
cp /etc/redis/redis.conf /etc/redis/redis.conf.bak
sed -i 's/^# requirepass .*/requirepass 123456/' /etc/redis/redis.conf
sed -i 's/^bind 127.0.0.1/bind 0.0.0.0/' /etc/redis/redis.conf

# 启动
systemctl enable redis-server
systemctl restart redis-server

# 验证
redis-cli -a 123456 PING
redis-cli -a 123456 INFO server | grep redis_version
```

## WSL 环境信息

| 项目 | 值 |
|------|-----|
| Ubuntu 版本 | 26.04 LTS (resolute) |
| 镜像源 | 阿里云 `mirrors.aliyun.com` |
| Root 密码 | `123456` |
| 包管理器 | aptitude（首选）/ apt |
| init 系统 | systemd |
| MySQL | 8.4.x，端口 3306/33060 |
| Redis | 8.0.x，端口 6379 |
