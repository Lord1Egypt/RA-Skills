# Server Monitor — 服务器监控技能

## 描述

监控服务器核心资源（CPU、内存、磁盘、网络、负载），支持阈值告警和定时检查。基于 Linux 原生命令，无需额外安装。

## 触发场景

- 用户要求"查看服务器状态"、"监控服务器"、"系统怎么样"
- 定时检查服务器资源使用情况
- 资源超阈值时主动告警

## 监控指标与命令

### CPU 使用率
```bash
top -bn1 | grep "Cpu(s)" | awk '{print 100 - $8}'
```
或使用：
```bash
vmstat 1 2 | tail -1 | awk '{print 100 - $15}'
```

### 内存使用
```bash
free -m | awk '/Mem:/ {printf "已用 %sMB / 总计 %sMB (%.1f%%)\n", $3, $2, $3*100/$2}'
```

### 磁盘使用
```bash
df -h | grep -E '^/dev/' | awk '{printf "%s: 已用 %s/%s (%s)\n", $6, $3, $2, $5}'
```

### 系统负载
```bash
uptime | awk -F'load average:' '{print $2}' | xargs
```
返回值：1分钟、5分钟、15分钟平均负载

### 网络流量
```bash
cat /proc/net/dev | grep -E 'eth0|ens|enp' | awk '{printf "接收: %.1fMB | 发送: %.1fMB\n", $2/1024/1024, $10/1024/1024}'
```

### 磁盘 IO
```bash
iostat -x 1 1 2>/dev/null || echo "未安装sysstat"
```

## 一键全状态检查
```bash
echo "=== 服务器状态 ==="
echo ""
echo "📅 时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "🖥️  主机: $(hostname)"
echo "⏱️   运行: $(uptime -p 2>/dev/null || uptime | awk -F'up ' '{print $2}' | awk -F',' '{print $1}')"
echo ""
echo "💻 CPU: $(top -bn1 | grep 'Cpu(s)' | awk '{printf "%.1f%%", 100-$8}')"
echo "🧠 内存: $(free -m | awk '/Mem:/{printf "%dMB/%dMB (%.1f%%)", $3, $2, $3*100/$2}')"
echo "💾 磁盘: $(df -h / | awk 'NR==2{printf "%s/%s (%s)", $3, $2, $5}')"
echo "📊 负载: $(uptime | awk -F'load average:' '{print $2}' | xargs)"
echo "🌐 网络: $(cat /proc/net/dev | grep -E 'eth0|ens' | awk '{printf "↓%.1fMB ↑%.1fMB", $2/1024/1024, $10/1024/1024}')"
echo ""
echo "=== 占用前五进程 ==="
ps aux --sort=-%mem | head -6 | awk 'NR>1{printf "%-20s %5s %5s\n", $11, $4"%", $4"MB"}'
```

## 告警阈值配置

默认告警阈值：
- CPU > 80% ⚠️
- 内存 > 85% ⚠️
- 磁盘 > 90% 🔴
- 负载 > CPU核心数 × 2 ⚠️

发现超阈值时：
1. 记录告警信息
2. 如用户配置了通知渠道，发送告警消息
3. 建议处理方案

## 定时监控

通过 cron 实现定时检查：
```bash
# 每15分钟检查一次，超阈值通知
*/15 * * * * /path/to/check.sh
```

或通过 heartbeat 检查：
将检查指令加入 `HEARTBEAT.md`。

## 进程异常检测

查找高资源占用进程：
```bash
# CPU占用前10
ps aux --sort=-%cpu | head -11 | tail -10

# 内存占用前10
ps aux --sort=-%mem | head -11 | tail -10

# 僵尸进程
ps aux | awk '$8 ~ /Z/ {print}'
```

## 使用示例

**用户**: "看看服务器状态"

执行一键全状态检查命令，格式化返回结果。

**用户**: "CPU占用高吗"

执行CPU检查命令，分析结果。

**用户**: "磁盘还剩多少"

执行磁盘检查命令，返回各分区剩余空间。

## 注意事项

- 所有命令均为只读，不影响系统运行
- 需要基础 Linux 命令可用（top, free, df等）
- 网络接口名可能因系统而异（eth0/ens/enp等），需根据实际调整
- 高负载时可建议用户执行 `htop` 进一步分析需安装
- 可配合 `universal-notify` 技能实现告警通知
