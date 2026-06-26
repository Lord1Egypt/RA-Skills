import argparse
import sys
from client import VetMewClient, VetMewAuthError, VetMewSessionError

def handle_auth_error(e):
    """输出引导式认证错误指引，并提示重新配置"""
    print("\n" + "="*40)
    print("❌ VetMew API 认证失败：密钥缺失或无效")
    print("-" * 40)
    print(f"原因为: {e.message}")
    
    if sys.stdin.isatty():
        choice = input("\n是否需要现在重新配置 API 凭据？ (y/N): ").strip().lower()
        if choice == 'y':
            client = VetMewClient()
            client.onboard_credentials()
            print("\n[🚀] 配置已更新。请重新运行刚才的命令。")
            return
            
    print("\n[ 操作建议 ]")
    print("1. 检查根目录下的 .env 文件是否已创建并填写了正确的内容。")
    print("2. 确保环境变量 VETMEW_AUTH_TOKEN (格式为 KEY:SECRET) 的值正确无误。")
    print("3. 确认密钥值没有多余的空格或双引号。")
    print("\n参考指引: 见 SKILL.md 中的 Setup & Configuration 章节")
    print("="*40)

def handle_session_error(e):
    """输出引导式会话错误指引"""
    print("\n" + "="*40)
    print("❌ VetMew 会话无效或已过期")
    print("-"*40)
    print(f"API 返回: {e.message}")
    print("\n[ 可能原因 ]")
    print("1. 会话 ID 已在服务器端失效（长时间未操作）。")
    print("2. ⚠️ 隔离冲突：您可能误用了‘医疗问诊’的 ID 来进行‘知识问答’。")
    print("\n[ 操作建议 ]")
    print("1. 请尝试在不携带 --conversation_id 参数的情况下重新发起咨询。")
    print("2. 如果是在对话中，请告知 Agent 重置当前的【知识问答】会话槽位。")
    print("="*40)

def main():
    parser = argparse.ArgumentParser(description="VetMew 宠物知识问答 (Free-Chat) Skill")
    parser.add_argument("--msg", required=True, help="咨询内容 (200 字符内)")
    parser.add_argument("--online", action="store_true", help="开启联网搜索")
    parser.add_argument("--conversation_id", help="对话 ID (用于多轮)")

    args = parser.parse_args()

    # 1. 输入校验
    if len(args.msg) > 200:
        print(f"错误: 咨询内容超过 200 个字符 (当前长度: {len(args.msg)})。")
        sys.exit(1)

    # 2. 准备 Payload
    payload = {
        "msg": args.msg,
        "enable_online": args.online
    }
    if args.conversation_id:
        payload["conversation_id"] = args.conversation_id

    # 3. 发起请求
    try:
        client = VetMewClient()
        path = "/open/v1/free-chat"
        response = client.request_sse(path, payload)
        
        current_conversation_id = None
        if response:
            for chunk in client.stream_response(response):
                if 'msg' in chunk:
                    print(chunk['msg'], end='', flush=True)
                if 'conversation_id' in chunk:
                    current_conversation_id = chunk['conversation_id']
            
            print("\n" + "-"*20)
            if current_conversation_id:
                print(f"CONVERSATION_ID: {current_conversation_id}")
    except VetMewAuthError as e:
        handle_auth_error(e)
        sys.exit(1)
    except VetMewSessionError as e:
        handle_session_error(e)
        sys.exit(1)
    except Exception as e:
        print(f"\n错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
