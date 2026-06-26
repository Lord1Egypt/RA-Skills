#!/bin/bash
# Ubuntu System Inspector
# 系统巡检脚本

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Output file
REPORT_FILE="/tmp/ubuntu_inspection_$(date +%Y%m%d_%H%M%S).txt"

echo "========================================" | tee -a "$REPORT_FILE"
echo "   Ubuntu 系统巡检报告" | tee -a "$REPORT_FILE"
echo "   时间: $(date '+%Y-%m-%d %H:%M:%S')" | tee -a "$REPORT_FILE"
echo "========================================" | tee -a "$REPORT_FILE"
echo "" | tee -a "$REPORT_FILE"

# 1. 系统基本信息
echo "【1. 系统基本信息】" | tee -a "$REPORT_FILE"
echo "主机名: $(hostname)" | tee -a "$REPORT_FILE"
echo "操作系统: $(lsb_release -d | cut -f2)" | tee -a "$REPORT_FILE"
echo "内核版本: $(uname -r)" | tee -a "$REPORT_FILE"
echo "架构: $(uname -m)" | tee -a "$REPORT_FILE"
echo "运行时间: $(uptime -p 2>/dev/null || uptime | awk -F',' '{print $1}')" | tee -a "$REPORT_FILE"
echo "" | tee -a "$REPORT_FILE"

# 2. CPU 信息
echo "【2. CPU 信息】" | tee -a "$REPORT_FILE"
echo "CPU 型号: $(grep 'model name' /proc/cpuinfo | head -1 | cut -d':' -f2 | xargs)" | tee -a "$REPORT_FILE"
echo "CPU 核心数: $(nproc)" | tee -a "$REPORT_FILE"
echo "CPU 使用率:" | tee -a "$REPORT_FILE"
top -bn1 | grep "Cpu(s)" | awk '{print "  用户: " $2 " 系统: " $4 " 空闲: " $8}' | tee -a "$REPORT_FILE"
echo "CPU 负载: $(cat /proc/loadavg | awk '{print $1, $2, $3}')" | tee -a "$REPORT_FILE"
echo "" | tee -a "$REPORT_FILE"

# 3. 内存信息
echo "【3. 内存信息】" | tee -a "$REPORT_FILE"
free -h | tee -a "$REPORT_FILE"
echo "" | tee -a "$REPORT_FILE"

# 4. 磁盘空间
echo "【4. 磁盘空间】" | tee -a "$REPORT_FILE"
df -h | grep -E '^/dev/' | tee -a "$REPORT_FILE"
echo "" | tee -a "$REPORT_FILE"

# 检查磁盘使用率是否超过 80%
DISK_USAGE=$(df / | awk 'NR==2 {print $5}' | sed 's/%//')
if [ "$DISK_USAGE" -gt 80 ]; then
    echo -e "${RED}警告: 根分区使用率超过 80% (${DISK_USAGE}%)${NC}" | tee -a "$REPORT_FILE"
fi
echo "" | tee -a "$REPORT_FILE"

# 5. 网络连接
echo "【5. 网络信息】" | tee -a "$REPORT_FILE"
echo "IP 地址:" | tee -a "$REPORT_FILE"
ip addr show | grep -E 'inet ' | grep -v '127.0.0.1' | awk '{print "  " $2}' | tee -a "$REPORT_FILE"
echo "默认网关: $(ip route | grep default | awk '{print $3}' | head -1)" | tee -a "$REPORT_FILE"
echo "DNS 服务器:" | tee -a "$REPORT_FILE"
cat /etc/resolv.conf | grep nameserver | awk '{print "  " $2}' | tee -a "$REPORT_FILE"
echo "" | tee -a "$REPORT_FILE"

# 6. 监听端口
echo "【6. 监听端口】" | tee -a "$REPORT_FILE"
ss -tlnp | head -20 | tee -a "$REPORT_FILE"
echo "" | tee -a "$REPORT_FILE"

# 7. 系统服务状态
echo "【7. 关键服务状态】" | tee -a "$REPORT_FILE"
for service in ssh cron systemd-timesyncd systemd-resolved; do
    if systemctl is-active --quiet $service 2>/dev/null; then
        echo "  $service: 运行中 ✓" | tee -a "$REPORT_FILE"
    else
        echo "  $service: 未运行 ✗" | tee -a "$REPORT_FILE"
    fi
done
echo "" | tee -a "$REPORT_FILE"

# 8. 登录记录
echo "【8. 最近登录记录】" | tee -a "$REPORT_FILE"
last -n 5 | tee -a "$REPORT_FILE"
echo "" | tee -a "$REPORT_FILE"

# 9. 当前登录用户
echo "【9. 当前登录用户】" | tee -a "$REPORT_FILE"
who | tee -a "$REPORT_FILE"
echo "" | tee -a "$REPORT_FILE"

# 10. 进程数量
echo "【10. 进程统计】" | tee -a "$REPORT_FILE"
echo "总进程数: $(ps aux | wc -l)" | tee -a "$REPORT_FILE"
echo "僵尸进程数: $(ps aux | awk '$8 ~ /^Z/ {print}' | wc -l)" | tee -a "$REPORT_FILE"
echo "" | tee -a "$REPORT_FILE"

# 11. 内存占用 Top 10
echo "【11. 内存占用 Top 10 进程】" | tee -a "$REPORT_FILE"
ps aux --sort=-%mem | head -11 | tee -a "$REPORT_FILE"
echo "" | tee -a "$REPORT_FILE"

# 12. 系统日志错误
echo "【12. 最近的系统错误 (最近1小时)】" | tee -a "$REPORT_FILE"
journalctl --priority=err --since "1 hour ago" --no-pager 2>/dev/null | head -10 | tee -a "$REPORT_FILE" || echo "  无法读取日志或没有错误" | tee -a "$REPORT_FILE"
echo "" | tee -a "$REPORT_FILE"

# 13. 安全相关
echo "【13. 安全信息】" | tee -a "$REPORT_FILE"
echo "系统用户数量: $(cat /etc/passwd | wc -l)" | tee -a "$REPORT_FILE"
echo "sudo 用户: $(grep -c 'sudo' /etc/group)" | tee -a "$REPORT_FILE"
echo "失败的登录尝试 (最近10次):" | tee -a "$REPORT_FILE"
lastb -n 10 2>/dev/null | tee -a "$REPORT_FILE" || echo "  无记录" | tee -a "$REPORT_FILE"
echo "" | tee -a "$REPORT_FILE"

# 14. 更新状态
echo "【14. 系统更新状态】" | tee -a "$REPORT_FILE"
if command -v apt &> /dev/null; then
    UPDATES=$(apt list --upgradable 2>/dev/null | grep -c upgradable || echo "0")
    echo "可更新包数量: $UPDATES" | tee -a "$REPORT_FILE"
else
    echo "  无法检查更新" | tee -a "$REPORT_FILE"
fi
echo "" | tee -a "$REPORT_FILE"

echo "========================================" | tee -a "$REPORT_FILE"
echo "巡检完成！报告保存至: $REPORT_FILE" | tee -a "$REPORT_FILE"
echo "========================================" | tee -a "$REPORT_FILE"

# 输出报告路径
echo "$REPORT_FILE"
