#!/usr/bin/env python3
"""
获取zworker消息通知
从zworker获取最新通知，输出消息详情供后续发送
"""

import json
import sys
import argparse
from zworker_api import get_claw_message, ZworkerAPIError

def main():
    parser = argparse.ArgumentParser(description='获取zworker消息通知')
    parser.add_argument('--claw-type', required=True, help='claw类型，如 openClaw, QClaw 等')
    parser.add_argument('--output-format', choices=['json', 'plain'], default='json',
                       help='输出格式: json(默认) 或 plain')
    
    args = parser.parse_args()
    
    try:
        result = get_claw_message(args.claw_type)
        
        # 验证必要字段
        channel = result.get('channel', '')
        message = result.get('message', '')
        
        if not channel or not message:
            print(f"错误: 无效的通知数据 - channel或message为空: {result}", file=sys.stderr)
            sys.exit(1)
        
        userid = result.get('userid', '')
        
        if args.output_format == 'json':
            # 输出JSON格式，包含完整信息
            output = {
                'channel': channel,
                'userid': userid,
                'message': message,
                'raw': result
            }
            print(json.dumps(output, ensure_ascii=False, indent=2))
        else:
            # 纯文本格式，仅消息内容
            print(f"频道: {channel}")
            if userid:
                print(f"用户ID: {userid}")
            print(f"消息内容: {message}")
        
        sys.exit(0)
        
    except ZworkerAPIError as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"未知错误: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()