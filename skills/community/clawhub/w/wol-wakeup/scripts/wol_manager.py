#!/usr/bin/env python3
"""
WoL (Wake-on-LAN) 设备管理器
支持添加、删除、列表、唤醒设备
"""

import json
import os
import sys
from pathlib import Path

try:
    from wakeonlan import send_magic_packet
except ImportError:
    print("错误：请先安装 wakeonlan 库：pip3 install wakeonlan")
    sys.exit(1)

# 配置文件路径
CONFIG_DIR = Path.home() / ".openclaw" / "wol"
CONFIG_FILE = CONFIG_DIR / "devices.json"

def ensure_config_dir():
    """确保配置目录存在"""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

def load_devices():
    """加载设备列表"""
    if not CONFIG_FILE.exists():
        return []
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def save_devices(devices):
    """保存设备列表"""
    ensure_config_dir()
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(devices, f, ensure_ascii=False, indent=2)

def add_device(name, mac, note=""):
    """添加设备"""
    devices = load_devices()
    
    # 检查是否已存在
    for dev in devices:
        if dev['name'] == name:
            return False, f"设备 '{name}' 已存在"
    
    # 验证 MAC 地址格式
    mac_clean = mac.replace(':', '').replace('-', '').upper()
    if len(mac_clean) != 12 or not all(c in '0123456789ABCDEF' for c in mac_clean):
        return False, "MAC 地址格式不正确（应为 12 位十六进制）"
    
    # 标准化 MAC 地址格式（XX:XX:XX:XX:XX:XX）
    mac_formatted = ':'.join(mac_clean[i:i+2] for i in range(0, 12, 2))
    
    devices.append({
        'name': name,
        'mac': mac_formatted,
        'note': note,
        'id': len(devices) + 1
    })
    
    save_devices(devices)
    return True, f"已添加设备：{name} ({mac_formatted})"

def remove_device(name):
    """删除设备"""
    devices = load_devices()
    original_len = len(devices)
    
    devices = [d for d in devices if d['name'] != name]
    
    if len(devices) == original_len:
        return False, f"未找到设备：{name}"
    
    # 重新编号
    for i, dev in enumerate(devices, 1):
        dev['id'] = i
    
    save_devices(devices)
    return True, f"已删除设备：{name}"

def list_devices():
    """列出所有设备"""
    devices = load_devices()
    
    if not devices:
        return "暂无已保存的设备\n\n使用格式：添加网络唤醒|MAC 地址 | 备注\n例如：添加网络唤醒|00:11:22:33:44:55|我的电脑"
    
    result = ["📋 已保存的 WoL 设备：\n"]
    for dev in devices:
        result.append(f"{dev['id']}. {dev['name']}")
        result.append(f"   MAC: {dev['mac']}")
        if dev.get('note'):
            result.append(f"   备注：{dev['note']}")
        result.append("")
    
    return '\n'.join(result)

def wake_device(identifier):
    """唤醒设备（支持名称或编号）"""
    devices = load_devices()
    
    if not devices:
        return False, "暂无已保存的设备"
    
    # 尝试按编号查找
    try:
        dev_id = int(identifier)
        device = next((d for d in devices if d['id'] == dev_id), None)
    except ValueError:
        device = None
    
    # 尝试按名称查找
    if not device:
        device = next((d for d in devices if d['name'].lower() == identifier.lower()), None)
    
    if not device:
        return False, f"未找到设备：{identifier}\n使用 '列表' 查看可用设备"
    
    # 发送 WoL 包
    try:
        send_magic_packet(device['mac'])
        return True, f"✅ 已发送唤醒信号到：{device['name']} ({device['mac']})\n请等待设备启动（通常 30-60 秒）"
    except Exception as e:
        return False, f"发送唤醒信号失败：{str(e)}"

def main():
    """命令行接口"""
    if len(sys.argv) < 2:
        print("用法:")
        print("  wol_manager.py add <名称> <MAC> [备注]")
        print("  wol_manager.py remove <名称>")
        print("  wol_manager.py list")
        print("  wol_manager.py wake <名称或编号>")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == 'add' and len(sys.argv) >= 4:
        name = sys.argv[2]
        mac = sys.argv[3]
        note = sys.argv[4] if len(sys.argv) > 4 else ""
        success, msg = add_device(name, mac, note)
        print(msg)
        sys.exit(0 if success else 1)
    
    elif command == 'remove' and len(sys.argv) >= 3:
        name = sys.argv[2]
        success, msg = remove_device(name)
        print(msg)
        sys.exit(0 if success else 1)
    
    elif command == 'list':
        print(list_devices())
    
    elif command == 'wake' and len(sys.argv) >= 3:
        identifier = sys.argv[2]
        success, msg = wake_device(identifier)
        print(msg)
        sys.exit(0 if success else 1)
    
    else:
        print("未知命令或参数不足")
        sys.exit(1)

if __name__ == '__main__':
    main()
