"""
获取微信聊天记录脚本
用法：
  python get_messages.py "好友备注" [条数]
"""
import sys
import os
import argparse

sys.path.insert(0, r'D:\code\pywechat3')

def get_messages(friend: str, number: int = 200):
    try:
        from pywechat.WechatTools import Tools

        print(f"正在拉取「{friend}」的最近 {number} 条消息...")
        contents, senders, types = Tools.pull_messages(
            friend=friend,
            number=number,
            parse=True
        )

        print(f"\n{'='*60}")
        print(f"  「{friend}」聊天记录（共 {len(contents)} 条）")
        print(f"{'='*60}\n")

        type_map = {0: "文本", 1: "图片", 2: "语音", 3: "视频", 4: "文件", 49: "链接/其他"}

        for i, (content, sender, msg_type) in enumerate(zip(contents, senders, types), 1):
            type_name = type_map.get(msg_type, f"类型{msg_type}")
            preview = str(content)[:80] + ("..." if len(str(content)) > 80 else "")
            print(f"  [{i}] [{sender}] ({type_name}): {preview}")

        print(f"\n{'='*60}")
        return True
    except Exception as e:
        print(f"[✗] 获取消息失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="获取微信聊天记录")
    parser.add_argument("friend", help="好友或群聊备注")
    parser.add_argument("number", nargs="?", type=int, default=200, help="拉取消息条数（默认200）")
    args = parser.parse_args()

    success = get_messages(args.friend, args.number)
    sys.exit(0 if success else 1)
