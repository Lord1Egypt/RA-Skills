#!/usr/bin/env python3
"""
微信消息发送脚本
通过OpenClaw Gateway发送微信消息

用法:
    python3 send_message.py --to "联系人" --text "消息"
    python3 send_message.py --to "联系人" --image "/path/to/img.jpg"
    python3 send_message.py --to "联系人" --file "/path/to/file.pdf"
"""

import argparse
import json
import sys
import time
from pathlib import Path

# OpenClaw Gateway 默认地址
GATEWAY_HOST = "127.0.0.1"
GATEWAY_PORT = 18789
API_ENDPOINT = f"http://{GATEWAY_HOST}:{GATEWAY_PORT}/api/wechat/send"

# 频率限制配置
RATE_LIMIT = {
    "max_per_minute": 20,
    "cooldown_seconds": 3  # 每条消息间隔
}

# 上次发送时间记录
_last_send_time = 0


def check_rate_limit():
    """检查频率限制"""
    global _last_send_time
    current_time = time.time()
    
    if _last_send_time > 0:
        elapsed = current_time - _last_send_time
        if elapsed < RATE_LIMIT["cooldown_seconds"]:
            wait_time = RATE_LIMIT["cooldown_seconds"] - elapsed
            print(f"[等待] 频率限制，等待 {wait_time:.1f} 秒...")
            time.sleep(wait_time)
    
    _last_send_time = time.time()


def send_message(recipient: str, content: str, msg_type: str = "text", is_group: bool = False):
    """
    发送微信消息
    
    Args:
        recipient: 联系人备注名或群名
        content: 消息内容（文字内容或文件路径）
        msg_type: 消息类型 (text/image/file)
        is_group: 是否为群聊
    
    Returns:
        dict: 发送结果
    """
    import urllib.request
    import urllib.error
    
    # 检查频率限制
    check_rate_limit()
    
    # 构建请求数据
    payload = {
        "channel": "openclaw-weixin",
        "recipient": {
            "type": "group" if is_group else "user",
            "name": recipient
        },
        "message": {
            "type": msg_type,
            "content": content
        },
        "timestamp": int(time.time() * 1000)
    }
    
    # 如果是文件类型，读取并编码
    if msg_type in ["image", "file"]:
        file_path = Path(content)
        if not file_path.exists():
            return {
                "success": False,
                "error": f"文件不存在: {content}",
                "error_code": "E005"
            }
        
        # 读取文件并进行base64编码
        import base64
        with open(file_path, "rb") as f:
            file_data = base64.b64encode(f.read()).decode("utf-8")
        
        payload["message"]["content"] = file_data
        payload["message"]["filename"] = file_path.name
    
    # 发送HTTP请求
    headers = {
        "Content-Type": "application/json",
        "X-Requested-With": "wechat-sender-skill"
    }
    
    data = json.dumps(payload).encode("utf-8")
    
    try:
        req = urllib.request.Request(
            API_ENDPOINT,
            data=data,
            headers=headers,
            method="POST"
        )
        
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))
            return result
            
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        try:
            error_json = json.loads(error_body)
            return {
                "success": False,
                "error": error_json.get("message", str(e)),
                "error_code": error_json.get("code", f"HTTP_{e.code}")
            }
        except:
            return {
                "success": False,
                "error": f"HTTP错误: {e.code} - {error_body}",
                "error_code": f"HTTP_{e.code}"
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_code": "E999"
        }


def main():
    parser = argparse.ArgumentParser(
        description="通过微信发送消息",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s --to "张三" --text "你好"
  %(prog)s --to "李四" --image /path/to/photo.jpg
  %(prog)s --to "工作群" --file /path/to/doc.pdf --group
        """
    )
    
    parser.add_argument(
        "--to", "-t",
        required=True,
        help="收件人备注名（必须与微信中一致）"
    )
    
    parser.add_argument(
        "--text",
        help="文字消息内容"
    )
    
    parser.add_argument(
        "--image",
        help="图片文件路径"
    )
    
    parser.add_argument(
        "--file",
        help="文件路径"
    )
    
    parser.add_argument(
        "--group", "-g",
        action="store_true",
        help="发送到群聊"
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="模拟发送，不实际执行"
    )
    
    args = parser.parse_args()
    
    # 验证参数
    msg_types = []
    if args.text:
        msg_types.append(("text", args.text))
    if args.image:
        msg_types.append(("image", args.image))
    if args.file:
        msg_types.append(("file", args.file))
    
    if len(msg_types) == 0:
        print("错误: 请指定 --text、--image 或 --file 之一")
        sys.exit(1)
    
    if len(msg_types) > 1:
        print("错误: 一次只能发送一种类型的消息")
        sys.exit(1)
    
    msg_type, content = msg_types[0]
    
    # 模拟模式
    if args.dry_run:
        print(f"[模拟发送] 类型: {msg_type}, 收件人: {args.to}")
        print(f"[模拟发送] 内容: {content[:50]}...")
        print("[模拟发送] 成功！")
        return
    
    # 发送消息
    print(f"正在发送 {msg_type} 消息给 {args.to}...")
    result = send_message(args.to, content, msg_type, args.group)
    
    if result.get("success"):
        print(f"✅ 发送成功！")
        print(f"   消息ID: {result.get('messageId', 'N/A')}")
        print(f"   时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        print(f"❌ 发送失败！")
        print(f"   错误码: {result.get('error_code', 'UNKNOWN')}")
        print(f"   错误信息: {result.get('error', '未知错误')}")
        sys.exit(1)


if __name__ == "__main__":
    main()
