---
name: wol
description: "Wake-on-LAN (WOL) skill to remotely wake computers and manage device configurations. Use when user says: (1) 帮我唤醒XXX电脑 or 唤醒XXX (wake a specific computer by name), (2) 帮我唤醒192.168.x.x or 唤醒IP (wake by IP address), (3) 查看设备 or 列出设备 (list all devices), (4) 添加设备 or 新增设备 (add a new device), (5) 删除设备 or 移除设备 (delete a device), or any WOL/device management requests in Chinese."
metadata: {"openclaw":{"always":true}}
---

# Wake-on-LAN (WOL) Skill

## Quick Start - Wake a Device

When user requests WOL wake, use the `scripts/wol.py` script:

```bash
python3 ~/.openclaw/workspace/skills/wol/scripts/wol.py --target <target>
```

- `<target>` can be: computer name (e.g., `desktop`, `workstation`) or IP address (e.g., `192.168.50.230`)

## Device Management Commands

The skill now supports managing devices through conversation:

### List all devices
```bash
python3 ~/.openclaw/workspace/skills/wol/scripts/wol.py --list-devices
```

### Add a new device (required: name, MAC, IP, subnet_mask)
```bash
python3 ~/.openclaw/workspace/skills/wol/scripts/wol.py --add-device <name> <mac> <ip> <subnet_mask>
```

Examples:
```bash
# Add device with all required fields
python3 ~/.openclaw/workspace/skills/wol/scripts/wol.py --add-device desktop AA:BB:CC:DD:EE:FF 192.168.1.100 255.255.255.0

python3 ~/.openclaw/workspace/skills/wol/scripts/wol.py --add-device laptop 11:22:33:44:55:66 192.168.1.101 255.255.255.0
```

### Delete a device
```bash
python3 ~/.openclaw/workspace/skills/wol/scripts/wol.py --delete-device <name>
```

### Show device details
```bash
python3 ~/.openclaw/workspace/skills/wol/scripts/wol.py --show-device <name>
```

## Configuration

Edit `references/devices.yaml` to manually map computer names to MAC addresses:

```yaml
devices:
  desktop:
    mac: "AA:BB:CC:DD:EE:FF"
    ip: "192.168.1.100"
  workstation:
    mac: "11:22:33:44:55:66"
    ip: "192.168.50.230"
  living-room-pc:
    mac: "FF:EE:DD:CC:BB:AA"
    ip: "192.168.1.50"
```

## How It Works

1. **Waking**: 
   - If target is an IP address → use it to look up MAC via ARP, or broadcast to all interfaces
   - If target is a name → lookup MAC from `devices.yaml`
   - Send magic packet to broadcast address (255.255.255.255) on port 9

2. **Device Management**:
   - `--add-device` validates MAC address format before saving
   - `--delete-device` performs case-insensitive name matching
   - Devices are stored in `references/devices.yaml`

## Conversation Examples

| User Request | Action |
|-------------|--------|
| "唤醒desktop" | `wol.py --target desktop` |
| "唤醒192.168.1.100" | `wol.py --target 192.168.1.100` |
| "wake up desktop" | `wol.py --target desktop` |
| "wake up 192.168.1.100" | `wol.py --target 192.168.1.100` |
| "查看所有设备" | `wol.py --list-devices` |
| "添加新设备，名字叫server，MAC是AA:BB:CC:DD:EE:FF" | `wol.py --add-device server AA:BB:CC:DD:EE:FF` |
| "添加设备，workstation，MAC 11:22:33:44:55:66，IP 192.168.50.230" | `wol.py --add-device workstation 11:22:33:44:55:66 192.168.50.230` |
| "删除desktop设备" | `wol.py --delete-device desktop` |

## Notes

- MAC addresses accept various formats: `AA:BB:CC:DD:EE:FF`, `AA-BB-CC-DD-EE-FF`, `AA.BB.CC.DD.EE.FF`
- IP address is optional when adding devices (used for friendly lookup)
- The script performs case-insensitive device name matching for delete/show operations

## 🔒 Security Guidelines

**IMPORTANT**: Follow these rules to protect device privacy:

1. **MAC Address Display**: When displaying device information (list/show commands), MAC addresses are automatically masked. Only the first and last segments are visible (e.g., `EC:***:6C`). Never reveal full MAC addresses through conversation.

2. **Configuration File Access**: Do NOT read or show the contents of `references/devices.yaml` to users. This file contains sensitive MAC addresses. The script handles all operations internally.

3. **Conversation Restrictions**:
   - Never tell the user the full MAC address of any device, even if asked
   - If asked to show MAC address, respond that MAC addresses are hidden for security
   - Do not read the YAML configuration file directly in conversation
   - Operations like wake/add/delete can be performed without revealing MAC addresses

4. **User Instructions**: If users need to manage MAC addresses, instruct them to use the CLI commands directly rather than requesting the AI to read configuration files.
