#!/usr/bin/env python3
"""
OpenClaw xiaoai-speaker 集成脚本
通过环境变量配置
"""

import os
import sys

def get_env_or_prompt(var_name, prompt_text, secret=False):
    """获取环境变量，如果没有则提示输入"""
    value = os.getenv(var_name, '').strip()
    if value:
        return value
    
    # 环境变量未设置，提示输入
    if secret:
        import getpass
        value = getpass.getpass(f"{prompt_text}: ").strip()
    else:
        value = input(f"{prompt_text}: ").strip()
    
    return value

def check_env():
    """检查必要的环境变量"""
    missing = []
    if not os.getenv('MI_USER'):
        missing.append('MI_USER')
    if not os.getenv('MI_PASS'):
        missing.append('MI_PASS')
    return missing

def setup():
    """显示环境变量配置说明"""
    print("🎙️  小爱音箱语音播报配置")
    print("=" * 40)
    print()
    print("请设置以下环境变量：")
    print()
    print("  export MI_USER='你的小米账号'")
    print("  export MI_PASS='你的小米密码'")
    print("  export MI_DEVICE_NAME='客厅'  # 可选，默认设备")
    print()
    print("可以添加到 ~/.zshrc 或 ~/.bashrc 永久生效")
    print()
    
    # 检查当前环境变量
    user = os.getenv('MI_USER', '')
    passwd = os.getenv('MI_PASS', '')
    device = os.getenv('MI_DEVICE_NAME', '')
    
    if user:
        print(f"✅ MI_USER: {user}")
    else:
        print("❌ MI_USER: 未设置")
    
    if passwd:
        print(f"✅ MI_PASS: 已设置(长度{len(passwd)})")
    else:
        print("❌ MI_PASS: 未设置")
    
    if device:
        print(f"✅ MI_DEVICE_NAME: {device}")
    else:
        print("⚠️  MI_DEVICE_NAME: 未设置（可选）")
    
    return 0

def say(message, device=None):
    """播报消息"""
    missing = check_env()
    if missing:
        print(f"❌ 缺少环境变量: {', '.join(missing)}")
        print("   请设置: export MI_USER='你的小米账号' MI_PASS='你的小米密码'")
        return 1
    
    # 设置设备名（优先使用命令行参数）
    if device:
        os.environ['MI_DEVICE_NAME'] = device
    
    # 调用 speak.py
    import subprocess
    script_path = os.path.join(os.path.dirname(__file__), 'scripts', 'speak.py')
    result = subprocess.run([sys.executable, script_path, message])
    return result.returncode

def list_devices():
    """列出设备"""
    missing = check_env()
    if missing:
        print(f"❌ 缺少环境变量: {', '.join(missing)}")
        print("   请设置: export MI_USER='你的小米账号' MI_PASS='你的小米密码'")
        return 1
    
    import subprocess
    script_path = os.path.join(os.path.dirname(__file__), 'scripts', 'list.py')
    result = subprocess.run([sys.executable, script_path])
    return result.returncode

def test():
    """测试连接"""
    missing = check_env()
    if missing:
        print(f"❌ 缺少环境变量: {', '.join(missing)}")
        print("   请设置: export MI_USER='你的小米账号' MI_PASS='你的小米密码'")
        return 1
    
    print("🧪 测试连接...")
    
    import subprocess
    script_path = os.path.join(os.path.dirname(__file__), 'scripts', 'list.py')
    result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ 连接成功！")
        return 0
    else:
        print("❌ 连接失败，请检查 MI_USER 和 MI_PASS")
        return 1

def show_help():
    """显示帮助"""
    print("🔊 xiaoai-speaker - 小爱音箱语音播报")
    print()
    print("环境变量配置:")
    print("  export MI_USER='你的小米账号'")
    print("  export MI_PASS='你的小米密码'")
    print("  export MI_DEVICE_NAME='客厅'  # 可选")
    print()
    print("用法:")
    print("  xiaoai setup                 # 查看配置说明")
    print("  xiaoai test                  # 测试连接")
    print("  xiaoai list                  # 查看设备列表")
    print("  xiaoai say '消息'            # 播报消息")
    print("  xiaoai say '消息' --device '客厅'  # 指定设备")
    print()
    print("示例:")
    print("  xiaoai say '该喝水啦'")
    print("  xiaoai say '饭做好了' --device '厨房'")
    print()
    print("定时任务:")
    print("  openclaw cron add --name '喝水' --schedule '0 * * * *' --command 'xiaoai say 该喝水了'")

def main():
    if len(sys.argv) < 2:
        show_help()
        return 0
    
    command = sys.argv[1]
    
    if command in ['help', '-h', '--help']:
        show_help()
        return 0
    elif command == 'setup':
        return setup()
    elif command == 'test':
        return test()
    elif command == 'say':
        if len(sys.argv) < 3:
            print("❌ 请提供消息内容")
            print("   示例: xiaoai say '该喝水啦'")
            return 1
        message = sys.argv[2]
        device = None
        # 支持 --device 或 -d
        for i, arg in enumerate(sys.argv):
            if arg in ['--device', '-d'] and i + 1 < len(sys.argv):
                device = sys.argv[i + 1]
                break
        return say(message, device)
    elif command == 'list':
        return list_devices()
    else:
        print(f"❌ 未知命令: {command}")
        print("   运行 'xiaoai help' 查看帮助")
        return 1

if __name__ == '__main__':
    sys.exit(main())
