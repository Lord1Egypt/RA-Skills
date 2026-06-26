---
name: vps-maintenance
description: |
  VPS 服务器维护与优化配置。用于：(1) 新 VPS 入手后的初始化配置，(2) 服务器安全加固，
  (3) 系统性能优化，(4) 日常维护任务。包含 SSH 加固、防火墙配置、性能调优、时间同步等完整流程。
---

# VPS 维护配置

## 快速开始

### 1. 换源加速

```bash
# 备份原始源
cp /etc/apt/sources.list /etc/apt/sources.list.backup

# 获取系统版本代号
CODENAME=$(lsb_release -cs)

# 国内源（推荐国内用户）
cat > /etc/apt/sources.list <<EOF
deb http://mirrors.aliyun.com/debian/ ${CODENAME} main contrib non-free non-free-firmware
deb http://mirrors.aliyun.com/debian-security ${CODENAME}-security main contrib non-free non-free-firmware
deb http://mirrors.aliyun.com/debian/ ${CODENAME}-updates main contrib non-free non-free-firmware
EOF

# 国外用户用官方源
# deb https://deb.debian.org/debian/ ${CODENAME} main ...

apt update
```

### 2. 账户安全

```bash
# 创建普通用户（禁止直接用 root）
useradd -m -s /bin/bash username
echo "username:StrongPassword123!" | chpasswd
usermod -aG sudo username

# 配置 SSH 密钥
mkdir -p ~/.ssh
chmod 700 ~/.ssh
echo "你的公钥" > ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

### 3. SSH 加固

```bash
# 备份配置
cp /etc/ssh/sshd_config /etc/ssh/sshd_config.backup

# 修改默认端口（防扫描）
sed -i 's/^#*Port .*/Port 54321/' /etc/ssh/sshd_config

# 加固配置
cat >> /etc/ssh/sshd_config <<EOF
PasswordAuthentication no
PermitRootLogin prohibit-password
PubkeyAuthentication yes
LoginGraceTime 30
MaxAuthTries 3
EOF

systemctl restart ssh
```

### 4. 防火墙 (nftables)

```bash
# 安装 nftables（替代 ufw）
apt-get install -y nftables

# 配置规则（只开放 SSH）
cat > /etc/nftables.conf <<EOF
#!/usr/sbin/nft -f
flush ruleset
table inet filter {
  chain input {
    type filter hook input priority 0;
    policy drop;
    iif lo accept;
    ct state established,related accept;
    tcp dport 54321 accept;
  }
  chain forward { type filter hook forward priority 0; policy drop; }
  chain output { type filter hook output priority 0; policy accept; }
}
EOF

systemctl enable --now nftables
```

### 5. 性能优化

```bash
# BBR + 网络参数
cat > /etc/sysctl.d/99-custom.conf <<EOF
net.ipv4.tcp_congestion_control = bbr
net.core.default_qdisc = fq
net.core.rmem_max = 33554432
net.core.wmem_max = 33554432
net.core.somaxconn = 4096
net.ipv4.tcp_max_syn_backlog = 4096
net.ipv4.tcp_fastopen = 3
vm.swappiness = 3
kernel.panic = 1
EOF

sysctl --system

# Swap 配置（内存 < 4GB 时）
fallocate -l 2G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
echo "/swapfile none swap sw 0 0" >> /etc/fstab
```

### 6. 时间同步

```bash
# 时区
timedatectl set-timezone Asia/Shanghai

# NTP（国内用阿里云/清华）
cat > /etc/systemd/timesyncd.conf <<EOF
[Time]
NTP=ntp.aliyun.com ntp.ntsc.ac.cn time1.cloud.tencent.com
FallbackNTP=ntp1.aliyun.com ntp2.aliyun.com
EOF

systemctl enable --now systemd-timesyncd
timedatectl set-ntp yes
```

### 7. 安全加固

```bash
# Fail2Ban 防暴力破解
apt-get install -y fail2ban

cat > /etc/fail2ban/jail.d/sshd.local <<EOF
[sshd]
enabled = true
port = 54321
filter = sshd
maxretry = 5
findtime = 10m
bantime = 30m
EOF

systemctl enable --now fail2ban

# 自动安全更新
apt-get install -y unattended-upgrades
dpkg-reconfigure -plow unattended-upgrades

# 可选：禁用 ICMP ping
echo "net.ipv4.icmp_echo_ignore_all = 1" > /etc/sysctl.d/99-disable-ping.conf
sysctl -w net.ipv4.icmp_echo_ignore_all=1
```

### 8. 系统清理

```bash
# 1. 清理 apt 缓存
apt-get clean
apt-get autoclean
apt-get autoremove -y

# 2. 清理旧内核（Debian/Ubuntu）
dpkg -l 'linux-*' 2>/dev/null | grep '^ii' | grep -v "$(uname -r | sed 's/-.*//')" | awk '{print $2}' | xargs apt-get -y purge 2>/dev/null

# 3. 清理日志（保留最近 7 天）
journalctl --vacuum-time=7d
find /var/log -type f -name "*.log" -mtime +7 -delete 2>/dev/null
find /var/log -type f -name "*.gz" -mtime +30 -delete 2>/dev/null
find /var/log -type f -name "*.old" -delete 2>/dev/null

# 4. 清理临时文件
rm -rf /tmp/* 2>/dev/null
rm -rf /var/tmp/* 2>/dev/null

# 5. 清理用户缓存
rm -rf ~/.cache/* 2>/dev/null
```

---

## 日常维护命令

| 任务 | 命令 |
|------|------|
| 查看负载/内存 | `uptime && free -h` |
| 查看磁盘 | `df -h` |
| 查看登录日志 | `last` / `journalctl -u ssh` |
| 查看被封 IP | `fail2ban-client status sshd` |
| 解封 IP | `fail2ban-client set sshd unbanip <IP>` |
| 查看防火墙规则 | `nft list ruleset` |
| 重启服务 | `systemctl restart ssh` |
| 检查开放端口 | `ss -tulnp` |

### 定期清理脚本

```bash
#!/bin/bash
# vps-cleanup.sh - 定期清理脚本

echo "=== VPS 清理开始 ==="

# apt 清理
apt-get clean
apt-get autoremove -y

# 清理日志
journalctl --vacuum-time=7d
find /var/log -type f -name "*.log" -mtime +7 -delete 2>/dev/null

# 清理临时文件
rm -rf /tmp/* 2>/dev/null
rm -rf /var/tmp/* 2>/dev/null

echo "=== 清理完成 ==="
df -h
```

---

## 安全检查清单

- [ ] SSH 端口已改为非 22
- [ ] 禁用密码登录，使用密钥
- [ ] 禁用 root 直接登录
- [ ] 防火墙默认 DROP，只开必要端口
- [ ] Fail2Ban 已启用
- [ ] BBR 已启用
- [ ] 时区正确（NTP 同步）
- [ ] 自动安全更新已配置
- [ ] Swap 已配置（低内存 VPS）
