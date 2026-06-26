import json
import os
import sys
from client import VetMewClient, VetMewAuthError, VetMewSessionError, VetMewImageError

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
    print("2. ⚠️ 隔离冲突：您可能误用了‘知识问答 (free-chat)’的 ID 来进行‘医疗问诊’。")
    print("\n[ 操作建议 ]")
    print("1. 请尝试在不携带 --conversation_id 参数的情况下重新发起问诊。")
    print("2. 如果是在对话中，请告知 Agent 重置当前的【医疗问诊】会话槽位。")
    print("="*40)

def main():
    import argparse
    from breed_manager import BreedManager

    parser = argparse.ArgumentParser(description="VetMew 宠物问诊 Skill")
    parser.add_argument("--name", required=True, help="宠物昵称")
    parser.add_argument("--breed", required=True, help="品种名称")
    parser.add_argument("--pet_type", required=True, choices=["1", "2"], help="宠物类型 (1:猫, 2:狗)")
    parser.add_argument("--birth", required=True, help="生日 (YYYY-MM-DD)")
    parser.add_argument("--gender", type=int, default=1, help="性别 (1:公, 2:母)")
    parser.add_argument("--fertility", type=int, default=1, help="绝育 (1:未绝育, 2:已绝育)")
    parser.add_argument("--msg", help="问诊内容")
    parser.add_argument("--image", help="图片 Base64 数据")
    parser.add_argument("--image_url", help="图片 URL 链接")
    parser.add_argument("--image_type", type=int, choices=[1, 2, 3, 4, 5, 6], help="图片分析类型 (1-6)")
    parser.add_argument("--conversation_id", help="对话 ID (用于多轮)")
    parser.add_argument("--thinking", action="store_true", help="开启深度思考")

    args = parser.parse_args()

    # 1. 品种与物种一致性校验
    breed_manager = BreedManager()
    breed_id = breed_manager.get_breed_id(args.breed, args.pet_type)
    if not breed_id:
        type_name = "猫" if args.pet_type == "1" else "狗"
        print(f"错误: 无法在【{type_name}】分类下识别品种 '{args.breed}'。")
        print("请确保选择的物种 (pet_type) 与品种名称相匹配。")
        return

    # 2. 发起问诊
    try:
        client = VetMewClient()
        path = "/open/v2/chat"
        payload = {
            "breed": breed_id,
            "birth": args.birth,
            "gender": args.gender,
            "fertility": args.fertility,
            "nick_name": args.name,
            "enable_thinking": args.thinking
        }

        # 优先级校验：msg > image > image_url
        if args.msg:
            payload["msg"] = args.msg
            if args.image or args.image_url:
                print("警告: 检测到文本消息，将忽略图片相关参数。")
        elif args.image:
            payload["image"] = args.image
            if args.image_type:
                payload["image_type"] = args.image_type
            if args.image_url:
                print("提示: 检测到 Base64 图片，将忽略 --image_url。")
        elif args.image_url:
            payload["image_url"] = args.image_url
            if args.image_type:
                payload["image_type"] = args.image_type
        else:
            print("错误: 必须提供问诊内容 (--msg) 或图片 (--image/--image_url)。")
            return

        if args.conversation_id:
            payload["conversation_id"] = args.conversation_id

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
    except VetMewImageError as e:
        print("\n" + "="*40)
        print("❌ VetMew 图片识别失败")
        print("-" * 40)
        print(f"API 返回: {e.message}")
        print("\n[ 操作建议 ]")
        print("1. 请确保图片清晰，背景不要过于杂乱。")
        print("2. 确认图片内容属于支持的分类（呕吐物、皮肤、耳道等）。")
        print("3. 如果使用 URL，请确保该链接在公网可访问。")
        print("=" * 40)
        sys.exit(1)
    except Exception as e:
        print(f"\n错误: {e}")
        return

if __name__ == "__main__":
    main()
