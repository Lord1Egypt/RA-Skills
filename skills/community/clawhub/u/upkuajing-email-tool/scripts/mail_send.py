#!/usr/bin/env python3
"""
跨境魔方邮件发送工具
提供邮件发送功能，创建发送任务并同步返回结果。
"""
import argparse
import sys
import json
from common import make_request, get_api_key, print_json_output


def send_email(
    send_name: str = None,
    email_name: str = None,
    subject: str = None,
    content: str = None,
    reply_email: str = None,
    emails: list = None,
    api_key: str = None
) -> dict:
    """
    发送邮件

    Args:
        send_name: 发送名称（默认 service，最长50字符）
        email_name: 邮件名（默认 service，最长50字符）
        subject: 邮件主题（最长250字符）
        content: 邮件内容
        reply_email: 回复邮箱
        emails: 收件人邮箱列表
        api_key: API密钥（可选，默认从环境变量获取）

    Returns:
        API 响应数据
    """
    # 如果没有提供 api_key，从环境变量获取
    if api_key is None:
        api_key = get_api_key()

    # 构建请求参数
    params = {}

    if send_name:
        params['sendName'] = send_name
    if email_name:
        params['emailName'] = email_name
    if subject:
        params['subject'] = subject
    if content:
        params['content'] = content
    if reply_email:
        params['replyEmail'] = reply_email
    if emails:
        params['emails'] = emails

    # 验证必填参数
    if not subject:
        return {"success": False, "error": "缺少必填参数：subject（邮件主题）"}
    if not content:
        return {"success": False, "error": "缺少必填参数：content（邮件内容）"}
    if not emails:
        return {"success": False, "error": "缺少必填参数：emails（收件人邮箱列表）"}

    # 发起请求
    response = make_request('/mail/send', params, api_key=api_key)

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
        description='跨境魔方邮件发送工具'
    )
    parser.add_argument(
        '--send_name',
        type=str,
        help='发送名称（默认 service，最长50字符）'
    )
    parser.add_argument(
        '--email_name',
        type=str,
        help='邮件名（默认 service，最长50字符）'
    )
    parser.add_argument(
        '--subject',
        type=str,
        required=True,
        help='邮件主题（最长250字符）'
    )
    parser.add_argument(
        '--content',
        type=str,
        required=True,
        help='邮件内容'
    )
    parser.add_argument(
        '--reply_email',
        type=str,
        help='回复邮箱'
    )
    parser.add_argument(
        '--emails',
        type=str,
        required=True,
        help='收件人邮箱列表（JSON数组格式，如 \'["email1@test.com","email2@test.com"]\'）'
    )
    parser.add_argument(
        '--api_key',
        type=str,
        help='API密钥（可选，默认从环境变量获取）'
    )

    args = parser.parse_args()

    # 解析 emails 参数
    try:
        emails = json.loads(args.emails)
        if not isinstance(emails, list):
            print("错误：emails 参数必须是 JSON 数组", file=sys.stderr)
            sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"错误：emails 参数 JSON 格式无效：{str(e)}", file=sys.stderr)
        sys.exit(1)

    # 发送邮件
    result = send_email(
        send_name=args.send_name,
        email_name=args.email_name,
        subject=args.subject,
        content=args.content,
        reply_email=args.reply_email,
        emails=emails,
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