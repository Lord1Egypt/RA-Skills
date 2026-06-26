import argparse
import sys
import os

# 确保能导入同目录的其他模块
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from wechat_controller import WeChatController

def main():
    parser = argparse.ArgumentParser(description="微信发信命令行工具(Skill入口)")
    parser.add_argument("--to", required=True, help="接收者联系人名称")
    parser.add_argument("--content", required=True, help="消息内容(发文本)或图片URL(发图片)")
    parser.add_argument("--action", choices=["sendtext", "sendpic"], default="sendtext", help="类型: sendtext(默认) 或 sendpic")
    
    args = parser.parse_args()
    
    try:
        controller = WeChatController()
        if args.action == "sendpic":
            success = controller.search_and_send_picture(args.to, args.content)
        else:
            success = controller.search_and_send(args.to, args.content)
            
        if success:
            print("发送成功")
            # Stdout 将被智能体作为成功反馈
            sys.exit(0)
        else:
            print("发送失败，未找到窗体或其他错误")
            sys.exit(1)
            
    except Exception as e:
        print(f"执行异常: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
