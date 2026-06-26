---
name: rdk-x5-monitor
description: "只读查询 RDK X5 实时硬件状态：CPU 使用率与频率、BPU 算力占用、内存/磁盘使用、芯片温度、GPU 频率、网络 IP 地址。Use when the user wants to READ or CHECK current CPU usage, BPU utilization, memory, temperature, disk space, or IP address — any real-time status query that does not change system settings. Do NOT use for changing CPU frequency or temperature thresholds (use rdk-x5-system), system backup/upgrade (use rdk-x5-system), network configuration (use rdk-x5-network), or AI inference (use rdk-x5-ai-detect)."
license: MIT-0
metadata:
  openclaw:
    compatibility:
      platform: rdk-x5
---

# RDK X5 Monitor — 系统监控

## 操作步骤

### 1. CPU 状态

```bash
# CPU 使用率（实时）
top -bn1 | head -5

# 各核频率
cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_cur_freq

# 调度策略
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor
```

### 2. BPU 算力监控

```bash
# BPU 使用率（0~100）
cat /sys/devices/system/bpu/bpu0/ratio

# BPU 频率
cat /sys/devices/system/bpu/bpu0/devfreq/*/cur_freq
```

### 3. 温度

```bash
# 芯片温度（除以 1000 = ℃）
cat /sys/class/thermal/thermal_zone0/temp

# BPU 温度
cat /sys/class/hwmon/hwmon0/temp1_input
```
超过 95°C 自动降频，极限 105°C。

### 4. 内存与磁盘

```bash
free -h              # 内存
df -h                # 磁盘
```

### 5. GPU 频率

```bash
cat /sys/class/devfreq/*/cur_freq 2>/dev/null | head -1
```

### 6. 网络 IP

```bash
ip -4 addr show | grep inet | grep -v 127.0.0.1
hostname -I
```

### 7. 一键状态总览

```bash
echo "=== CPU ===" && top -bn1 | head -5 && \
echo "=== BPU ===" && cat /sys/devices/system/bpu/bpu0/ratio 2>/dev/null && \
echo "=== Temp ===" && echo "$(($(cat /sys/class/thermal/thermal_zone0/temp)/1000))°C" && \
echo "=== Mem ===" && free -h | head -2 && \
echo "=== Disk ===" && df -h / | tail -1 && \
echo "=== IP ===" && hostname -I
```

### 8. 持续监控（每 2 秒刷新）

```bash
watch -n 2 'echo "CPU: $(top -bn1 | grep Cpu | head -1)" && \
echo "BPU: $(cat /sys/devices/system/bpu/bpu0/ratio 2>/dev/null)%" && \
echo "Temp: $(($(cat /sys/class/thermal/thermal_zone0/temp)/1000))°C" && \
free -h | head -2'
```

## 排查故障

| 现象 | 原因 | 解决 |
|------|------|------|
| CPU 100% 持续 | 进程占满 | `top` 查看高占用进程；`kill` 或降低负载 |
| 温度 >90°C | 散热不足 | 加装散热片/风扇；降低 BPU 负载 |
| BPU ratio 始终 0 | 无推理任务运行 | 正常现象；启动 AI 推理后会上升 |
| 磁盘满 | 日志或备份过大 | `du -sh /var/log/*`；`sudo apt clean` |
