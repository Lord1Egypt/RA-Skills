#!/usr/bin/env python3
"""
跨境魔方短信发送工具
提供短信发送功能，创建发送任务并同步返回结果。
"""
import argparse
import sys
import json
from common import make_request, get_api_key, print_json_output


def send_sms(
    content: str = None,
    phones: list = None,
    channel_type: int = 0,
    api_key: str = None
) -> dict:
    """
    发送短信

    Args:
        content: 短信内容
        phones: 手机号列表
        channel_type: 发送类型（0-单向发送 1-双向）
        api_key: API密钥（可选，默认从环境变量获取）

    Returns:
        API 响应数据
    """
    # 如果没有提供 api_key，从环境变量获取
    if api_key is None:
        api_key = get_api_key()

    # 构建请求参数
    params = {}

    if content:
        params['content'] = content
    if phones:
        params['phones'] = phones
    params['channelType'] = channel_type

    # 验证必填参数
    if not content:
        return {"success": False, "error": "缺少必填参数：content（短信内容）"}
    if not phones:
        return {"success": False, "error": "缺少必填参数：phones（手机号列表）"}

    # 发起请求
    response = make_request('/sms/send', params, api_key=api_key)

    # 处理响应
    if response.get('code') == 0:
        return {
            "success": True,
            "data": response.get('data', {})
        }
    else:
        return {
            "success": False,
            "error_code": response.get('code'),
            "error_msg": response.get('msg', '未知错误')
        }


def main():
    parser = argparse.ArgumentParser(
        description='跨境魔方短信发送工具'
    )
    parser.add_argument(
        '--content',
        type=str,
        required=True,
        help='短信内容'
    )
    parser.add_argument(
        '--phones',
        type=str,
        required=True,
        help='手机号列表（JSON数组格式，如 \'["13800138000","13800138001"]\'）'
    )
    parser.add_argument(
        '--channel_type',
        type=int,
        default=0,
        choices=[0, 1],
        help='发送类型（0-单向发送 1-双向，支持接收回复消息）'
    )
    parser.add_argument(
        '--api_key',
        type=str,
        help='API密钥（可选，默认从环境变量获取）'
    )

    args = parser.parse_args()

    # 解析 phones 参数
    try:
        phones = json.loads(args.phones)
        if not isinstance(phones, list):
            print("错误：phones 参数必须是 JSON 数组", file=sys.stderr)
            sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"错误：phones 参数 JSON 格式无效：{str(e)}", file=sys.stderr)
        sys.exit(1)

    # 发送短信
    result = send_sms(
        content=args.content,
        phones=phones,
        channel_type=args.channel_type,
        api_key=args.api_key
    )

    # 输出结果
    if result.get('success'):
        print_json_output(result.get('data', {}))
    else:
        print(f"发送失败：{result.get('error_msg', result.get('error'))}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()