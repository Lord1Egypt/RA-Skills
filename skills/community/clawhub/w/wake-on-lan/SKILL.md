---
name: wake-on-lan
description: Send Wake on LAN (WOL) magic packets to remotely wake up computers and network devices. Use when the user wants to wake, turn on, or power on a remote device over the network. Triggers on phrases like "wake on lan", "WOL", "wake up computer", "turn on remote PC", "power on device remotely", "send magic packet", or when the user mentions MAC addresses in the context of waking devices.
---

# Wake on LAN / 网络唤醒

**English**: Send magic packets to wake up devices on the local network.
**中文**: 发送魔法包唤醒局域网中的设备。

---

## Quick Start / 快速开始

### English

Wake a device by MAC address:
```bash
python3 scripts/wake.py AA:BB:CC:DD:EE:FF
```

Wake by device name and wait for it to come online:
```bash
python3 scripts/wake.py --device my-pc --wait
```

Returns:
- `✓ 开机成功` (Device online successfully)
- `✗ 开机失败，请稍后再试或者检查网络设置是否正常` (Device failed to come online)

### 中文

通过 MAC 地址唤醒设备：
```bash
python3 scripts/wake.py AA:BB:CC:DD:EE:FF
```

通过设备名称唤醒并等待开机结果：
```bash
python3 scripts/wake.py --device my-pc --wait
```

返回结果：
- `✓ 开机成功` - 设备已成功开机
- `✗ 开机失败，请稍后再试或者检查网络设置是否正常` - 设备未能开机

---

## Prerequisites / 前提条件

The target device must have WOL enabled / 目标设备需要启用 WOL：

1. **BIOS/UEFI**: Enable "Wake on LAN" / 开启 "Wake on LAN" 选项
2. **Network card**: Must support WOL / 网卡需要支持 WOL
3. **OS settings**: May need to enable WOL in network adapter properties / 操作系统可能需要启用网卡 WOL 属性
4. **Power**: Device must be in sleep/soft-off state / 设备需处于睡眠或软关机状态

---

## Device Management / 设备管理

### List configured devices / 查看已配置设备

```bash
python3 scripts/wake.py --list
```

### Add a device / 添加设备

```bash
python3 scripts/wake.py --add my-pc AA:BB:CC:DD:EE:FF
python3 scripts/wake.py --add my-pc AA:BB:CC:DD:EE:FF --broadcast-ip 192.168.1.255
```

### Wake by name / 按名称唤醒

```bash
python3 scripts/wake.py --device my-pc
```

### Wake and wait for device / 唤醒并等待开机

```bash
python3 scripts/wake.py --device my-pc --wait
python3 scripts/wake.py --device my-pc --wait --timeout 120
```

Device configurations are stored in `references/devices.json`.

---

## Configuration Example / 配置示例

```json
{
  "my-pc": {
    "mac": "AA:BB:CC:DD:EE:FF",
    "ip": "192.168.1.100",
    "broadcast": "192.168.1.255",
    "port": 9
  }
}
```

| Field | Description | 说明 |
|-------|-------------|------|
| `mac` | Target MAC address | 目标 MAC 地址 |
| `ip` | IP for ping check (optional) | 用于检测开机的 IP（可选） |
| `broadcast` | Broadcast IP address | 广播地址 |
| `port` | UDP port (default: 9) | UDP 端口（默认: 9） |

---

## Broadcast Address / 广播地址

| Address | Use Case |
|---------|----------|
| `255.255.255.255` | Global broadcast (default) / 全局广播（默认） |
| `192.168.1.255` | Subnet-specific / 特定子网 |

---

## Troubleshooting / 故障排除

### Device doesn't wake / 设备无法唤醒

1. Check WOL is enabled in BIOS/UEFI and OS / 检查 BIOS 和系统是否启用 WOL
2. Verify MAC address matches the target device / 验证 MAC 地址是否正确
3. Try subnet broadcast instead of global broadcast / 尝试使用子网广播地址
4. Check firewall - UDP port 7 or 9 may need to be allowed / 检查防火墙是否允许 UDP 端口 7 或 9

### Device on different subnet / 跨子网唤醒

WOL packets don't normally route across subnets. Options:
- Use directed broadcast / 使用定向广播
- Deploy a WOL relay on the target subnet / 在目标子网部署 WOL 中继

---

## Script Reference / 命令参考

```
scripts/wake.py <mac> [broadcast] [port]
scripts/wake.py --device <name> [--wait] [--timeout SECONDS]
scripts/wake.py --list
scripts/wake.py --add <name> <mac> [--broadcast-ip IP]
```

| Argument | Default | Description |
|----------|---------|-------------|
| `--device` | - | Wake by device name / 按设备名称唤醒 |
| `--wait` | - | Wait for device to come online / 等待设备开机 |
| `--timeout` | 60 | Timeout in seconds (recommended: 30-120s) / 超时秒数（推荐 30-120 秒） |
| `--list` | - | List configured devices / 列出已配置设备 |
| `--add` | - | Add device to config / 添加设备 |

---

## How It Works / 工作原理

1. Send WOL magic packet via UDP broadcast / 通过 UDP 广播发送 WOL 魔法包
2. Magic packet = 6 bytes `0xFF` + 16x MAC address / 魔法包 = 6 字节 0xFF + 16 次 MAC 地址
3. If `--wait` is used, ping the device every 2 seconds / 如果使用 `--wait`，每 2 秒 ping 一次设备
4. Return success/failure based on ping result / 根据 ping 结果返回成功或失败
