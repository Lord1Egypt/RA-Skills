"""
发送微信消息脚本
用法：
  python send_message.py "好友备注" "消息内容"
  python send_message.py "好友备注" "消息内容" --tickle
"""
import sys
import os
import argparse

# 添加本地 pywechat3 源码路径
sys.path.insert(0, r'D:\code\pywechat3')

def send_message(friend: str, message: str, tickle: bool = False):
    try:
        from pywechat.WechatAuto import Messages
        Messages.send_message_to_friend(
            friend=friend,
            message=message,
            tickle=tickle,
            close_wechat=True
        )
        print(f"[✓] 消息已发送给: {friend}")
        return True
    except Exception as e:
        print(f"[✗] 发送失败: {e}")
        return False

def batch_send(friends_messages: list):
    """批量发送，friends_messages 格式: [(friend, message), ...]"""
    try:
        from pywechat.WechatAuto import Messages
        from pywechat.WechatTools import Tools

        # 检查微信是否已启动
        try:
            Tools.open_wechat()
        except Exception:
            pass

        for friend, message in friends_messages:
            Messages.send_message_to_friend(
                friend=friend,
                message=message,
                close_wechat=False
            )
            print(f"[✓] 消息已发送给: {friend}")

        # 统一关闭
        try:
            from pywechat.WechatTools import Tools
            Tools.close_wechat()
        except Exception:
            pass
        return True
    except Exception as e:
        print(f"[✗] 批量发送失败: {e}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="发送微信消息")
    parser.add_argument("friend", help="好友或群聊备注")
    parser.add_argument("message", help="待发送的消息")
    parser.add_argument("--tickle", action="store_true", help="发送后拍一拍好友")
    args = parser.parse_args()

    success = send_message(args.friend, args.message, args.tickle)
    sys.exit(0 if success else 1)
