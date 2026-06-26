#!/usr/bin/env python3
"""小爱音箱测试脚本"""

import json
import sys
from pathlib import Path
from xiaoaitts import XiaoAi

CONFIG_PATH = Path(__file__).parent.parent / "data" / "xiaoai_config.json"


def load_config():
    with open(CONFIG_PATH, encoding='utf-8') as f:
        return json.load(f)


def discover_devices():
    config = load_config()
    client = XiaoAi(config["mi_user"], config["mi_pass"])
    
    devices = client.get_device()
    print("=== 可用设备 ===")
    for d in devices:
        print(f"  - {d.get('name')} (ID: {d.get('deviceID')})")
    
    return devices, client


def speak(text):
    config = load_config()
    client = XiaoAi(config["mi_user"], config["mi_pass"])
    
    device_name = config.get("device_name", "小爱音箱")
    devices = client.get_device(device_name)
    
    if not devices:
        print(f"未找到设备: {device_name}")
        sys.exit(1)
    
    device = devices[0]
    device_id = device["deviceID"]
    print(f"使用设备: {device['name']} ({device_id})")
    
    client.use_device(device_id)
    client.say(text)
    print(f"✓ 已发送: {text}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法:")
        print("  python test_xiaoai.py --discover  # 发现设备")
        print("  python test_xiaoai.py \"要说的内容\"  # 说话")
        sys.exit(1)
    
    if sys.argv[1] == "--discover":
        discover_devices()
    else:
        text = " ".join(sys.argv[1:])
        speak(text)
