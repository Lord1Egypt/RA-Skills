#!/usr/bin/env python3
"""
列出所有小爱音箱设备
用于查看设备ID和设备名

配置方式：
  export MI_USER="你的小米账号"
  export MI_PASS="你的小米密码"
"""

import sys
import asyncio
import os

sys.path.insert(0, '/tmp/MiService')

MI_USER = os.getenv('MI_USER', '')
MI_PASS = os.getenv('MI_PASS', '')

async def list_devices():
    """列出所有小爱音箱设备"""
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
                print("⚠️ 没有找到任何设备")
                return False
            
            print(f"\n🎵 找到 {len(devices)} 个设备：\n")
            print(f"{'设备ID':<20} {'设备名称':<30} {'类型':<15}")
            print("-" * 70)
            
            for device in devices:
                device_id = device.get('deviceID', 'N/A')
                name = device.get('name', '未知')
                device_type = device.get('type', '未知')
                
                # 标记可能是音箱的设备
                marker = "🔊" if '小爱' in name or '音箱' in name else "  "
                print(f"{marker} {device_id:<18} {name:<28} {device_type:<13}")
            
            print("\n💡 使用方式：")
            print("   1. 通过环境变量指定设备名：")
            print("      export MI_DEVICE_NAME=\"你的音箱名称\"")
            print("   2. 或通过环境变量指定设备ID：")
            print("      export MI_DEVICE_ID=\"你的设备ID\"")
            print("   3. 不指定则默认使用第一个包含'小爱'或'音箱'的设备")
            
            return True
            
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False

if __name__ == '__main__':
    if not MI_USER or not MI_PASS:
        print("❌ 请先设置环境变量：")
        print("   export MI_USER=\"你的小米账号\"")
        print("   export MI_PASS=\"你的小米密码\"")
        sys.exit(1)
    
    result = asyncio.run(list_devices())
    sys.exit(0 if result else 1)
