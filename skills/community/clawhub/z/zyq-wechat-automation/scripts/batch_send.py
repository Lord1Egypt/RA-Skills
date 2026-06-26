"""
批量发送微信消息脚本
用法：
  python batch_send.py --config "friends.json"
  格式（friends.json）:
  {
    "tasks": [
      {"friend": "好友1", "message": "消息内容1"},
      {"friend": "好友2", "message": "消息内容2"}
    ],
    "delay": 0.4,
    "tickle": false
  }
"""
import sys
import os
import json
import argparse

sys.path.insert(0, r'D:\code\pywechat3')

def batch_send_from_config(config_path: str):
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
    except Exception as e:
        print(f"[✗] 读取配置文件失败: {e}")
        return False

    tasks = config.get("tasks", [])
    delay = config.get("delay", 0.4)
    tickle = config.get("tickle", False)

    if not tasks:
        print("[✗] 任务列表为空")
        return False

    print(f"[*] 开始批量发送，共 {len(tasks)} 个任务")
    print(f"[*] 发送间隔: {delay}s | 拍一拍: {tickle}\n")

    try:
        from pywechat.WechatAuto import Messages
        from pywechat.WechatTools import Tools

        # 尝试打开微信
        try:
            Tools.open_wechat()
        except Exception:
            pass

        for i, task in enumerate(tasks, 1):
            friend = task.get("friend")
            message = task.get("message")
            if not friend or not message:
                print(f"[!] 任务 {i} 格式错误，跳过")
                continue

            print(f"[{i}/{len(tasks)}] → {friend}: {message[:30]}{'...' if len(message) > 30 else ''}")
            try:
                Messages.send_message_to_friend(
                    friend=friend,
                    message=message,
                    tickle=tickle,
                    close_wechat=False
                )
            except Exception as e:
                print(f"  [!] 发送给 {friend} 失败: {e}")

        print(f"\n[✓] 批量发送完成")
        return True

    except Exception as e:
        print(f"[✗] 批量发送失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="批量发送微信消息")
    parser.add_argument("--config", required=True, help="任务配置文件路径（JSON格式）")
    args = parser.parse_args()

    success = batch_send_from_config(args.config)
    sys.exit(0 if success else 1)
