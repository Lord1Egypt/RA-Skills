#!/usr/bin/env python3
"""
WoL 技能安装脚本
自动配置 Hook 服务和 systemd 服务
"""

import os
import sys
import subprocess
import json
import secrets
from pathlib import Path

def check_dependencies():
    """检查依赖"""
    print("📦 检查依赖...")
    
    # 检查 Python
    try:
        result = subprocess.run(['python3', '--version'], capture_output=True, text=True)
        print(f"✅ Python: {result.stdout.strip()}")
    except Exception as e:
        print(f"❌ Python3 未安装：{e}")
        return False
    
    # 检查 wakeonlan 库
    try:
        import wakeonlan
        print("✅ wakeonlan 库已安装")
    except ImportError:
        print("⚠️  正在安装 wakeonlan 库...")
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', 'wakeonlan'], check=True)
            print("✅ wakeonlan 库安装成功")
        except Exception as e:
            print(f"❌ 安装 wakeonlan 失败：{e}")
            return False
    
    return True

def generate_token():
    """生成安全 token"""
    return secrets.token_hex(16)

def configure_openclaw_hook(token):
    """配置 OpenClaw Hook"""
    print("\n🔧 配置 OpenClaw Hook...")
    
    home = Path.home()
    config_path = home / '.openclaw' / 'config.json'
    
    # 读取现有配置
    config = {}
    if config_path.exists():
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
        except Exception as e:
            print(f"⚠️  读取配置文件失败：{e}")
    
    # 更新 Hook 配置
    if 'hooks' not in config:
        config['hooks'] = {}
    
    config['hooks']['enabled'] = True
    config['hooks']['token'] = token
    config['hooks']['internal'] = {
        'enabled': True,
        'endpoint': 'http://127.0.0.1:8765/hook'
    }
    
    # 保存配置
    try:
        config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"✅ OpenClaw 配置已更新：{config_path}")
    except Exception as e:
        print(f"❌ 保存配置文件失败：{e}")
        return False
    
    return True

def create_systemd_service():
    """创建 systemd 服务"""
    print("\n🔧 创建 systemd 服务...")
    
    home = Path.home()
    skill_dir = Path(__file__).parent.parent
    service_file = skill_dir / 'openclaw-hook.service'
    user_service_dir = home / '.config' / 'systemd' / 'user'
    
    # 读取服务文件
    if not service_file.exists():
        print(f"⚠️  服务文件不存在：{service_file}")
        return False
    
    try:
        with open(service_file, 'r') as f:
            service_content = f.read()
    except Exception as e:
        print(f"❌ 读取服务文件失败：{e}")
        return False
    
    # 替换路径占位符
    service_content = service_content.replace('{{HOME}}', str(home))
    service_content = service_content.replace('{{SKILL_DIR}}', str(skill_dir))
    
    # 创建用户 systemd 目录
    user_service_dir.mkdir(parents=True, exist_ok=True)
    
    # 写入服务文件
    user_service_file = user_service_dir / 'openclaw-hook.service'
    try:
        with open(user_service_file, 'w') as f:
            f.write(service_content)
        print(f"✅ systemd 服务文件已创建：{user_service_file}")
    except Exception as e:
        print(f"❌ 创建服务文件失败：{e}")
        return False
    
    # 启用并启动服务
    print("\n🚀 启用 systemd 服务...")
    try:
        subprocess.run(['systemctl', '--user', 'daemon-reload'], check=True)
        subprocess.run(['systemctl', '--user', 'enable', 'openclaw-hook.service'], check=True)
        subprocess.run(['systemctl', '--user', 'start', 'openclaw-hook.service'], check=True)
        print("✅ systemd 服务已启用并启动")
    except Exception as e:
        print(f"⚠️  systemd 服务配置失败（可手动启动）: {e}")
        print(f"   手动启动命令：systemctl --user start openclaw-hook.service")
    
    return True

def create_device_directory():
    """创建设备配置目录"""
    print("\n📁 创建设备配置目录...")
    
    home = Path.home()
    device_dir = home / '.openclaw' / 'wol'
    
    try:
        device_dir.mkdir(parents=True, exist_ok=True)
        print(f"✅ 设备目录已创建：{device_dir}")
    except Exception as e:
        print(f"❌ 创建设备目录失败：{e}")
        return False
    
    return True

def main():
    print("="*60)
    print("🌊 WoL Wakeup 技能安装程序")
    print("="*60)
    
    # 检查依赖
    if not check_dependencies():
        print("\n❌ 依赖检查失败，请手动安装后重试")
        return 1
    
    # 获取技能目录
    script_dir = Path(__file__).parent
    skill_dir = script_dir.parent
    
    print(f"\n📂 技能位置：{skill_dir}")
    
    # 生成安全 token
    token = generate_token()
    print(f"\n🔑 生成安全 Token: {token[:8]}...")
    
    # 配置 OpenClaw Hook
    if not configure_openclaw_hook(token):
        print("\n⚠️  Hook 配置失败，请手动配置")
    
    # 创建 systemd 服务
    if not create_systemd_service():
        print("\n⚠️  systemd 服务创建失败，可手动启动 Hook")
    
    # 创建设备目录
    if not create_device_directory():
        print("\n⚠️  设备目录创建失败")
    
    # 显示使用说明
    print("\n" + "="*60)
    print("✅ 安装完成！使用方法：")
    print("="*60)
    print("""
1. 添加设备：
   发送消息：添加网络唤醒|00:11:22:33:44:55|我的电脑

2. 查看设备列表：
   发送消息：帮我开机 或 列表

3. 唤醒设备：
   发送消息：开机 - 我的电脑 或 开机 -1

4. 删除设备：
   发送消息：删除 - 我的电脑

配置文件位置：~/.openclaw/wol/devices.json
Hook 服务状态：systemctl --user status openclaw-hook.service
    """)
    
    # 保存 token 到文件
    token_file = skill_dir / '.hook_token'
    try:
        with open(token_file, 'w') as f:
            f.write(token)
        print(f"\n💾 Token 已保存到：{token_file}")
    except Exception as e:
        print(f"\n⚠️  Token 保存失败：{e}")
    
    # 测试安装
    print("\n🧪 运行测试...")
    test_script = script_dir / 'test_wol.py'
    if test_script.exists():
        subprocess.run(['python3', str(test_script)], cwd=str(script_dir))
    
    print("\n✅ 技能已就绪！")
    return 0

if __name__ == '__main__':
    sys.exit(main())
