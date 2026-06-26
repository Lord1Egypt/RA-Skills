#!/usr/bin/env python3
"""
MeoW 配置助手 - 对话式配置 MeoW 推送
用法: python3 scripts/meow_config.py [命令]
无参数时进入交互模式
"""

import sys
import os
from pathlib import Path

# 添加脚本目录到路径
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))
os.chdir(str(script_dir))

from push_helper import PushHelper
from feature_flag import FeatureFlag


def show_status():
    """显示当前状态 - 标准化格式"""
    helper = PushHelper()
    status = helper.status()
    ff = FeatureFlag()
    
    # HarmonyOS 设备
    has_harmonyos = status.get('harmonyos', False)
    meow_enabled = status.get('meow', False)
    meow_configured = status.get('meow_configured', False)
    nick = ff.get('push.meow_nickname') or '未设置'
    
    lines = [
        "```",
        "【MeoW推送配置】",
        "",
        "当前状态：",
        f"- HarmonyOS设备: {'✅ 有' if has_harmonyos else '❌ 无'}",
        f"- MeoW推送: {'✅ 已启用' if meow_enabled else '⏸️ 未启用'}",
        f"- 昵称: {nick}",
        "",
        "推送渠道：",
        f"- 负一屏: ✅ 启用",
        f"- MeoW: {'✅ 启用' if meow_enabled else '⏸️ 未启用'}",
        "",
        "操作命令：",
        "```bash",
        "python3 scripts/meow_config.py status   # 查看状态",
        "python3 scripts/meow_config.py enable   # 启用",
        "python3 scripts/meow_config.py disable  # 禁用",
        "```",
        "```",
    ]
    return "\n".join(lines)


def enable_meow(nickname: str = None):
    """启用 MeoW"""
    helper = PushHelper()
    ff = FeatureFlag()
    
    # 检查 HarmonyOS 设备
    if not ff.get('push.harmonyos_device'):
        return "❌ 请先确认拥有 HarmonyOS 设备\n\n使用命令: meow_config.py setup"
    
    # 启用 MeoW
    if nickname:
        helper.enable_meow(nickname)
        return f"✅ MeoW 已启用，昵称: {nickname}"
    else:
        # 尝试获取已有昵称
        current_nick = ff.get('push.meow_nickname') or "夕岸摇"
        helper.enable_meow(current_nick)
        return f"✅ MeoW 已启用，昵称: {current_nick}"


def disable_meow():
    """禁用 MeoW"""
    helper = PushHelper()
    helper.disable_meow()
    return "✅ MeoW 已禁用"


def setup_harmonyos():
    """设置 HarmonyOS 设备"""
    helper = PushHelper()
    helper.set_harmonyos(True)
    return "✅ 已确认拥有 HarmonyOS 设备"


def interactive():
    """交互式配置"""
    print("```")
    print("🔧 MeoW 配置助手")
    print("=" * 40)
    print("1. 查看当前状态")
    print("2. 确认 HarmonyOS 设备")
    print("3. 启用 MeoW 推送")
    print("4. 禁用 MeoW")
    print("5. 退出")
    print("```")
    
    while True:
        choice = input("\n请输入选项 (1-5): ").strip()
        
        if choice == '1':
            print(show_status())
        elif choice == '2':
            print(setup_harmonyos())
        elif choice == '3':
            nick = input("请输入 MeoW 昵称 (直接回车使用默认 '夕岸摇'): ").strip()
            if not nick:
                nick = "夕岸摇"
            print(enable_meow(nick))
        elif choice == '4':
            print(disable_meow())
        elif choice == '5':
            print("👋 再见!")
            break
        else:
            print("❌ 无效选项，请重试")


def main():
    if len(sys.argv) < 2:
        # 无参数：显示状态
        print(show_status())
        return
    
    cmd = sys.argv[1].lower()
    
    if cmd == 'status':
        print(show_status())
    elif cmd == 'setup':
        print(setup_harmonyos())
    elif cmd == 'enable':
        nick = sys.argv[2] if len(sys.argv) > 2 else None
        print(enable_meow(nick))
    elif cmd == 'disable':
        print(disable_meow())
    elif cmd == 'interactive':
        interactive()
    else:
        print("""📱 MeoW 配置助手

```bash
# 查看状态
python3 scripts/meow_config.py status

# 交互式配置
python3 scripts/meow_config.py interactive

# 启用 MeoW
python3 scripts/meow_config.py enable [昵称]

# 禁用 MeoW
python3 scripts/meow_config.py disable

# 确认 HarmonyOS 设备
python3 scripts/meow_config.py setup
```
""")


if __name__ == '__main__':
    main()
