"""
生成执行脚本（处理沙箱限制）
由于 OpenClaw 运行在沙箱中，无法直接操作真实桌面，
本脚本生成 .bat 文件，用户手动双击后在真实环境中执行微信自动化操作。

用法：
  python generate_bat.py send "好友" "消息"
  python generate_bat.py batch "config.json"
  python generate_bat.py contacts
  python generate_bat.py messages "好友" 200
"""
import sys
import os

sys.path.insert(0, r'D:\code\pywechat3')

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPTS_DIR)

def get_desktop():
    return os.path.join(os.path.expanduser("~"), "Desktop")

def generate_send_bat(friend: str, message: str, output_path: str = None):
    """生成发送消息的bat"""
    if output_path is None:
        output_path = os.path.join(get_desktop(), "WeChatAuto_发送消息.bat")

    bat_content = f'''@echo off
chcp 65001 >nul
echo =====================================
echo   微信RPA - 发送消息
echo =====================================
echo.
echo  好友: {friend}
echo  消息: {message[:50]}{'...' if len(message) > 50 else ''}
echo.
echo  正在执行，请勿移动鼠标键盘...
echo.

cd /d "{SKILL_DIR}"
python "{SCRIPTS_DIR}\\send_message.py" "{friend}" "{message}"

echo.
echo 执行完成，按任意键退出...
pause >nul
'''
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(bat_content)
    print(f'[OK] 脚本已生成: {output_path}')
    print('    请双击运行!')
    return output_path
    """生成批量发送的bat"""
    if output_path is None:
        output_path = os.path.join(get_desktop(), "WeChatAuto_批量发送.bat")

    bat_content = f'''@echo off
chcp 65001 >nul
echo =====================================
echo   微信RPA - 批量发送
echo =====================================
echo.
echo  配置文件: {config_path}
echo.
echo  正在执行，请勿移动鼠标键盘...
echo.

cd /d "{SKILL_DIR}"
python "{SCRIPTS_DIR}\\batch_send.py" --config "{config_path}"

echo.
echo 执行完成，按任意键退出...
pause >nul
'''
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(bat_content)
    print(f'[OK] 脚本已生成: {output_path}')
    print('    请双击运行!')
    return output_path
    """生成获取通讯录的bat"""
    if output_path is None:
        output_path = os.path.join(get_desktop(), f"WeChatAuto_通讯录_{contact_type}.bat")

    bat_content = f'''@echo off
chcp 65001 >nul
echo =====================================
echo   微信RPA - 获取通讯录
echo =====================================
echo.

cd /d "{SKILL_DIR}"
python "{SCRIPTS_DIR}\\get_contacts.py" {contact_type}

echo.
echo 执行完成，按任意键退出...
pause >nul
'''
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(bat_content)
    print(f"[✓] 脚本已生成: {output_path}")
    print("    请双击运行!")
    return output_path

def generate_messages_bat(friend: str, number: int = 200, output_path: str = None):
    """生成获取聊天记录的bat"""
    if output_path is None:
        output_path = os.path.join(get_desktop(), f"WeChatAuto_聊天记录_{friend}.bat")

    bat_content = f'''@echo off
chcp 65001 >nul
echo =====================================
echo   微信RPA - 获取聊天记录
echo =====================================
echo.
echo  好友: {friend}
echo  条数: {number}
echo.

cd /d "{SKILL_DIR}"
python "{SCRIPTS_DIR}\\get_messages.py" "{friend}" {number}

echo.
echo 执行完成，按任意键退出...
pause >nul
'''
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(bat_content)
    print(f"[✓] 脚本已生成: {output_path}")
    print("    请双击运行!")
    return output_path

def main():
    if len(sys.argv) < 2:
        print("用法:")
        print("  python generate_bat.py send <好友> <消息>")
        print("  python generate_bat.py batch <config.json>")
        print("  python generate_bat.py contacts [friends|groups|enterprise]")
        print("  python generate_bat.py messages <好友> [条数]")
        sys.exit(1)

    cmd = sys.argv[1].lower()

    if cmd == "send":
        if len(sys.argv) < 4:
            print("[✗] 用法: generate_bat.py send <好友> <消息>")
            sys.exit(1)
        friend = sys.argv[2]
        message = sys.argv[3]
        generate_send_bat(friend, message)

    elif cmd == "batch":
        if len(sys.argv) < 3:
            print("[✗] 用法: generate_bat.py batch <config.json>")
            sys.exit(1)
        config_path = sys.argv[2]
        generate_batch_bat(config_path)

    elif cmd == "contacts":
        contact_type = sys.argv[2] if len(sys.argv) > 2 else "friends"
        generate_contacts_bat(contact_type)

    elif cmd == "messages":
        if len(sys.argv) < 3:
            print("[✗] 用法: generate_bat.py messages <好友> [条数]")
            sys.exit(1)
        friend = sys.argv[2]
        number = int(sys.argv[3]) if len(sys.argv) > 3 else 200
        generate_messages_bat(friend, number)

    else:
        print(f"[✗] 未知命令: {cmd}")
        sys.exit(1)

if __name__ == "__main__":
    main()
