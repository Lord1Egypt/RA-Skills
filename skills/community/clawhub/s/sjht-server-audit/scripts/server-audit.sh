#!/bin/bash
# server-audit.sh — 远程服务器巡检脚本
# 用法: bash server-audit.sh <host> [user]
# 前提: 已配置 SSH 免密登录
#
# 检查项目:
#   系统信息、CPU/内存/磁盘、运行服务、开放端口、
#   Nginx/MariaDB/PHP-FPM 配置、安全配置、可疑进程

set -e

HOST="${1:?❌ 用法: bash server-audit.sh <host> [user]}"
USER="${2:-root}"
TMPFILE=$(mktemp)
trap "rm -f $TMPFILE" EXIT

echo "🔍 正在巡检 ${USER}@${HOST} ..."

ssh -o ConnectTimeout=10 "${USER}@${HOST}" bash -s > "$TMPFILE" << 'AUDIT_SCRIPT'

echo "===SYSINFO_START==="
cat /etc/os-release | grep -E "^(NAME|VERSION)="
uname -r
uptime
echo ""

echo "--- CPU ---"
lscpu | grep "Model name" | head -1
lscpu | grep "^CPU(s):" | head -1
echo ""

echo "--- 内存 ---"
free -h | head -2
echo ""

echo "--- 磁盘 ---"
df -h / | tail -1
echo ""

echo "--- Swap ---"
swapon --show 2>/dev/null || echo "(无 swap)"
echo "===SYSINFO_END==="

echo ""
echo "===SERVICES_START==="
systemctl list-units --type=service --state=running --no-pager --legend=no 2>/dev/null \
  | grep -v "systemd-" | grep -v "getty" | grep -v "user@"
echo "===SERVICES_END==="

echo ""
echo "===PORTS_START==="
ss -tlnp 2>/dev/null
echo "===PORTS_END==="

echo ""
echo "===FIREWALL_START==="
echo "firewalld: $(systemctl is-active firewalld 2>/dev/null || echo 'inactive')"
echo "selinux: $(getenforce 2>/dev/null || echo 'N/A')"
firewall-cmd --list-all 2>/dev/null || echo "(未配置)"
echo "===FIREWALL_END==="

echo ""
echo "===WEB_START==="
echo "--- Nginx ---"
nginx -v 2>&1 || echo "未安装"
echo ""
echo "--- PHP ---"
php -v 2>&1 | head -1 || echo "未安装"
php-fpm83 -v 2>&1 | head -1 2>/dev/null || echo "PHP-FPM 未运行"
echo ""
echo "--- MariaDB/MySQL ---"
mysql --version 2>&1 || echo "未安装"
echo "  监听: $(ss -tlnp 2>/dev/null | grep 3306 || echo '未运行')"
echo ""
echo "--- Node ---"
node --version 2>&1 || echo "未安装"
echo ""
echo "--- Docker ---"
docker --version 2>&1 || echo "未安装"
echo ""
echo "--- Nginx 虚拟主机 ---"
for f in /etc/nginx/conf.d/*.conf /www/server/nginx/conf/vhost/*.conf; do
  [ -f "$f" ] && echo "[$f]" && grep -E "server_name|listen|root" "$f" 2>/dev/null
done
echo ""
echo "--- 网站目录 ---"
ls /www/wwwroot/ 2>/dev/null || echo "/www/wwwroot 不存在"
echo ""
for d in /www/wwwroot/*/; do
  [ -f "$d/wp-config.php" ] && echo "WordPress: $d"
  [ -f "$d/index.html" ] && echo "HTML站点: $d"
done
echo "===WEB_END==="

echo ""
echo "===SECURITY_START==="
echo "--- SSH 配置 ---"
grep -E "^PermitRootLogin|^PasswordAuthentication|^Port|^PubkeyAuthentication|^MaxAuthTries" /etc/ssh/sshd_config 2>/dev/null || echo "(使用默认配置)"
echo ""

echo "--- SSH 密码认证状态 ---"
if grep -q "^PasswordAuthentication no" /etc/ssh/sshd_config 2>/dev/null; then
  echo "✅ 密码认证已禁用"
elif grep -q "^PasswordAuthentication yes" /etc/ssh/sshd_config 2>/dev/null; then
  echo "⚠️ 密码认证已启用"
else
  echo "⚠️ PasswordAuthentication 未显式配置（默认 yes）"
fi
echo ""

echo "--- Root 登录 ---"
grep "^PermitRootLogin" /etc/ssh/sshd_config 2>/dev/null || echo "⚠️ PermitRootLogin 未配置（默认 yes）"
echo ""

echo "--- 最近失败登录 (5条) ---"
lastb 2>/dev/null | head -5 || echo "(无记录)"
echo ""

echo "--- 定时任务 ---"
crontab -l 2>/dev/null || echo "(无用户 crontab)"
echo ""
for f in /etc/cron.d/*; do
  [ -f "$f" ] && echo "[$f]" && cat "$f"
done
echo "===SECURITY_END==="

echo ""
echo "===PROCESSES_START==="
ps aux --sort=-%mem | head -12
echo "===PROCESSES_END==="

AUDIT_SCRIPT

echo ""
echo "✅ 巡检数据已收集"
echo ""
echo "=== 巡检报告 ==="
echo ""

# 简要分析
grep -oP 'Local Address:Port.*?\s+\K[0-9.]+' "$TMPFILE" | sort -u | while read port; do
  echo "  监听: $port"
done

# 安全快速判定
echo ""
echo "--- 快速安全判定 ---"
if grep -q "3306.*0.0.0.0" "$TMPFILE"; then
  echo "🔴 MariaDB 3306 端口全网暴露"
fi
if grep -q "8888.*0.0.0.0" "$TMPFILE"; then
  echo "🔴 管理面板端口全网暴露"
fi
if ! grep -q "PasswordAuthentication no" "$TMPFILE"; then
  echo "⚠️ SSH 密码认证未禁用"
fi
if grep -q "firewalld.*inactive" "$TMPFILE"; then
  echo "⚠️ 防火墙未启用"
fi
if grep -q "selinux.*Disabled" "$TMPFILE"; then
  echo "⚠️ SELinux 已禁用"
fi
grep -q "PermitRootLogin.*yes" "$TMPFILE" && echo "⚠️ SSH 允许 Root 登录"
echo ""

echo "原始数据保存在: $TMPFILE"
