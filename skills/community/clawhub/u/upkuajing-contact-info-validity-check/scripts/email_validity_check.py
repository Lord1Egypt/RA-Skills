#!/usr/bin/env python3
"""
邮件有效性检测
检测邮箱地址的有效性
"""
import argparse
import json
import sys

from common import make_request, handle_api_error, print_json_output, cover_fee_info


def check_email_validity(emails: list) -> dict:
    """
    检测邮件有效性

    Args:
        emails: 邮箱地址列表

    Returns:
        API 响应数据
    """
    params = {"emails": emails}
    response = make_request('/validation/email', params)
    return response


def main():
    parser = argparse.ArgumentParser(
        description='邮件有效性检测 - 检测邮箱地址的有效性'
    )
    parser.add_argument(
        '--emails',
        type=str,
        help='邮箱地址列表（空格分隔）'
    )
    parser.add_argument(
        '--params',
        type=str,
        help='JSON 参数字符串（可选）'
    )

    args = parser.parse_args()

    # 解析邮箱地址
    emails = []
    if args.emails:
        emails = args.emails.split()
    elif args.params:
        try:
            params = json.loads(args.params)
            emails = params.get('emails', [])
        except json.JSONDecodeError as e:
            print(f"错误：参数中的JSON无效：{str(e)}", file=sys.stderr)
            sys.exit(1)
    else:
        print("错误：请提供 --emails 参数", file=sys.stderr)
        sys.exit(1)

    if not emails:
        print("错误：邮箱地址列表不能为空", file=sys.stderr)
        sys.exit(1)

    # 调用 API
    response = check_email_validity(emails)

    # 检查错误
    if response.get('code') != 0:
        handle_api_error(response)
        return

    # 提取并格式化结果
    data = response.get('data', {})
    fee = response.get('fee', {})

    result = {
        'total': data.get('total', 0),
        'results': data.get('list', []),
        'fee': cover_fee_info(fee)
    }

    print_json_output(result)


if __name__ == '__main__':
    main()
