---
name: rdk-x5-network
description: "管理 RDK X5 的 WiFi 连接、有线网络静态IP、蓝牙配对、WiFi 热点创建、SSH 远程访问配置、VNC 远程连接故障排查。Use when the user wants to connect WiFi, create hotspot, pair Bluetooth, configure SSH, troubleshoot VNC connectivity issues, or troubleshoot any network problems. For checking current IP address → use rdk-x5-monitor. For setting up VNC server/desktop → use rdk-x5-media. Do NOT use for GPIO/hardware (use rdk-x5-gpio), camera setup (use rdk-x5-camera), or system backup/upgrade (use rdk-x5-system)."
license: MIT-0
metadata:
  openclaw:
    requires:
      bins:
        - nmcli
    compatibility:
      platform: rdk-x5
---

# RDK X5 Network — 网络与蓝牙配置

## 操作步骤

### 1. 查看网络状态

```bash
ip addr show                   # 所有接口 IP
nmcli device status            # 连接状态总览
nmcli device wifi list         # 扫描可用 WiFi
```

### 2. 连接 WiFi

```bash
# 连接（替换 SSID 和 PASSWORD）
sudo nmcli device wifi connect "SSID" password "PASSWORD"

# 连接隐藏 WiFi
sudo nmcli device wifi connect "SSID" password "PASSWORD" hidden yes

# 查看 / 删除已保存连接
nmcli connection show
sudo nmcli connection delete "连接名"
```

### 3. 创建 WiFi 热点

```bash
sudo nmcli device wifi hotspot ifname wlan0 ssid "RDK-X5-AP" password "12345678"

# 关闭热点
sudo nmcli connection down Hotspot
```

### 4. 配置有线静态 IP

```bash
sudo nmcli connection modify "Wired connection 1" \
  ipv4.method manual \
  ipv4.addresses "192.168.1.100/24" \
  ipv4.gateway "192.168.1.1" \
  ipv4.dns "8.8.8.8,114.114.114.114"
sudo nmcli connection up "Wired connection 1"

# 恢复 DHCP
sudo nmcli connection modify "Wired connection 1" ipv4.method auto
sudo nmcli connection up "Wired connection 1"
```

### 5. 蓝牙配对

```bash
sudo systemctl start bluetooth
bluetoothctl
```
在 `bluetoothctl` 交互中：
1. `scan on` — 扫描设备
2. `pair XX:XX:XX:XX:XX:XX` — 配对
3. `connect XX:XX:XX:XX:XX:XX` — 连接
4. `quit` — 退出

### 6. SSH / VNC 远程访问

```bash
# SSH 开启
sudo systemctl enable ssh && sudo systemctl start ssh

# VNC 开启（通过 srpi-config）
sudo srpi-config
# → Interface Options → VNC → Enable
```

### 7. srpi-config 快速配置

```bash
sudo srpi-config
```
支持：WiFi、SSH/VNC 开关、40pin 总线、MIPI 屏幕选择、音频通道切换。

## 排查故障

| 现象 | 排查命令 | 解决 |
|------|---------|------|
| 无法上网 | `ping -c 4 8.8.8.8` | 检查网关：`ip route show` |
| DNS 解析失败 | `cat /etc/resolv.conf` | 手动设置 DNS：`sudo nmcli conn modify ... ipv4.dns "114.114.114.114"` |
| WiFi 扫描为空 | `nmcli radio wifi` | 若 disabled 则 `nmcli radio wifi on` |
| 网络服务异常 | `sudo systemctl status NetworkManager` | `sudo systemctl restart NetworkManager` |
