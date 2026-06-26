#!/usr/bin/env python3
"""
小爱音箱控制脚本
通过小米云服务让小爱音箱播报消息

配置方式：
  export MI_USER="你的小米账号"
  export MI_PASS="你的小米密码"
  
可选配置（指定设备）：
  export MI_DEVICE_NAME="客厅的小爱音箱"  # 通过名称匹配
  或
  export MI_DEVICE_ID="xxxxxxxx"           # 通过ID精确匹配

查看可用设备：
  python3 scripts/list.py
"""

import sys
import asyncio
import os

sys.path.insert(0, '/tmp/MiService')

MI_USER = os.getenv('MI_USER', '')
MI_PASS = os.getenv('MI_PASS', '')
MI_DEVICE_NAME = os.getenv('MI_DEVICE_NAME', '')
MI_DEVICE_ID = os.getenv('MI_DEVICE_ID', '')

async def speak(message="你好"):
    """让小爱音箱播报消息"""
    try:
        from miservice import MiAccount, MiNAService
        import aiohttp
        
        async with aiohttp.ClientSession() as session:
            account = MiAccount(session, MI_USER, MI_PASS)
            
            if not await account.login('micoapi'):
                print("❌ 登录失败，请检查 MI_USER 和 MI_PASS 环境变量")
                return False
            
            service = MiNAService(account)
            devices = await service.device_list()
            
            if not devices:
                print("❌ 没有找到任何设备，请检查小米账号下的设备")
                return False
            
            # 查找目标设备
            target_device = None
            
            # 1. 优先通过设备ID精确匹配
            if MI_DEVICE_ID:
                for device in devices:
                    if device.get('deviceID') == MI_DEVICE_ID:
                        target_device = device
                        print(f"✅ 通过 ID 匹配到设备: {device.get('name')}")
                        break
                if not target_device:
                    print(f"⚠️ 未找到指定 ID 的设备: {MI_DEVICE_ID}")
                    print("   可用设备列表：")
                    for d in devices:
                        print(f"     - {d.get('deviceID')}: {d.get('name')}")
                    return False
            
            # 2. 通过设备名匹配
            elif MI_DEVICE_NAME:
                for device in devices:
                    if MI_DEVICE_NAME in device.get('name', ''):
                        target_device = device
                        print(f"✅ 通过名称匹配到设备: {device.get('name')}")
                        break
                if not target_device:
                    print(f"⚠️ 未找到名称包含 '{MI_DEVICE_NAME}' 的设备")
                    print("   可用设备列表：")
                    for d in devices:
                        print(f"     - {d.get('name')}")
                    return False
            
            # 3. 默认规则：找第一个包含"小爱"或"音箱"的设备
            else:
                for device in devices:
                    name = device.get('name', '')
                    if '小爱' in name or '音箱' in name:
                        target_device = device
                        print(f"✅ 使用默认匹配设备: {name}")
                        break
                
                if not target_device:
                    # 如果找不到，使用第一个设备
                    target_device = devices[0]
                    print(f"⚠️ 未找到小爱音箱，使用第一个可用设备: {target_device.get('name')}")
            
            # 执行播报
            device_id = target_device.get('deviceID')
            result = await service.text_to_speech(device_id, message)
            return result
                
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False

def main():
    """命令行入口"""
    if not MI_USER or not MI_PASS:
        print("❌ 请先设置环境变量：")
        print("   export MI_USER=\"你的小米账号\"")
        print("   export MI_PASS=\"你的小米密码\"")
        return 1
    
    message = sys.argv[1] if len(sys.argv) > 1 else "你好，我是 Nova"
    
    print(f"📢 播报: {message}")
    result = asyncio.run(speak(message))
    
    if result:
        print("✅ 播报成功")
        return 0
    else:
        print("❌ 播报失败")
        return 1

if __name__ == '__main__':
    sys.exit(main())
