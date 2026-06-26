---
name: rdk-x5-system
description: "修改和管理 RDK X5 系统配置：查看系统版本/硬件信息/系统日志、rdk-backup 一键备份与恢复、apt OTA 升级、miniboot 固件更新、CPU/BPU 频率调节与温度阈值设置、config.txt 配置修改、实时内核切换、systemd 开机自启动、存储扩容。Use when the user wants to CHANGE system settings, backup/restore, upgrade firmware, adjust CPU/BPU frequency, configure autostart services, switch RT kernel, expand storage, check system version, or view system logs. For read-only hardware status queries (CPU/BPU/温度/内存/磁盘 实时查看) → use rdk-x5-monitor instead. Do NOT use for network config (use rdk-x5-network), camera (use rdk-x5-camera), AI inference (use rdk-x5-ai-detect), NAS setup, Docker/容器, or custom application development."
license: MIT-0
metadata:
  openclaw:
    requires:
      bins:
        - apt
        - rdk-backup
    compatibility:
      platform: rdk-x5
---

# RDK X5 System — 系统管理

## 操作步骤

### 1. 查看系统信息

```bash
cat /etc/version                    # 系统版本
rdkos_info                          # 详细版本（OS 2.1.0+）
cat /proc/cpuinfo                   # CPU 信息
free -h                             # 内存
df -h                               # 磁盘
```

### 2. 系统备份（生成可烧录镜像）

```bash
sudo rdk-backup
```
生成 `.img` 文件，可烧录到其他 SD 卡。确保有足够存储空间。eMMC 版本备份问题已在 v3.3.1 修复。

### 3. OTA 在线升级

```bash
sudo apt update && sudo apt upgrade -y

# 升级 miniboot 固件到 NAND
sudo rdk-miniboot-update
```

> ⚠️ **严禁降级 miniboot 固件**，可能导致板子无法启动。

### 4. 温度监控

```bash
# 芯片温度（结果除以 1000 = ℃）
cat /sys/class/thermal/thermal_zone0/temp

# BPU 温度
cat /sys/class/hwmon/hwmon0/temp1_input
```
- 最高结温 105°C，超过 95°C 自动降频
- 开发阶段推荐配备散热片 + 风扇

### 5. CPU 频率管理

```bash
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq          # 当前频率
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_available_frequencies  # 可用频率

# 切换为性能模式（最高频率）
echo performance | sudo tee /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor
```

### 6. config.txt 配置

```bash
sudo nano /boot/config.txt
```
支持：dtoverlay 设备树覆盖、40pin U-Boot 初始化、ION 内存大小、CPU 超频。

### 7. 内核切换（普通 / 实时 RT）

```bash
sudo srpi-config
# → Advanced Options → Kernel → RT Kernel / Normal Kernel
```
实时内核适用于对延迟敏感的机器人控制场景。

### 8. 开机自启动（systemd）

```bash
sudo nano /etc/systemd/system/my-app.service
```
```ini
[Unit]
Description=My RDK Application
After=network.target

[Service]
Type=simple
ExecStart=/path/to/your/app
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```
```bash
sudo systemctl daemon-reload
sudo systemctl enable my-app.service
sudo systemctl start my-app.service
sudo systemctl status my-app.service
```

### 9. 存储扩容

```bash
lsblk                                    # 查看分区布局
sudo resize2fs /dev/mmcblk0p2            # 扩展 SD 卡文件系统
```

### 10. 桌面切换

```bash
sudo srpi-config
# → Display Options → CPU 桌面 / GPU 桌面（3D 加速）
```

## 常用命令速查

```bash
rdkos_info                   # 系统版本
sudo rdk-backup              # 备份
sudo rdk-miniboot-update     # 固件更新
sudo srpi-config             # 配置工具
```

## 排查故障

| 现象 | 原因 | 解决 |
|------|------|------|
| 系统无法启动 | miniboot 降级 | 只能重新烧录官方镜像 |
| 温度过高降频 | 无散热或负载过高 | 加装散热片/风扇；检查 BPU 使用率 |
| `rdk-backup` 失败 | 空间不足 | `df -h` 检查；清理 /tmp 或挂载外部存储 |
| `resize2fs` 无效 | 分区未扩展 | 先 `sudo growpart /dev/mmcblk0 2` 再 `resize2fs` |
