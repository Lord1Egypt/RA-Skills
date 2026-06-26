#!/usr/bin/env python3
"""
电话有效性检测
检测电话号码的有效性，返回号码状态、类型、是否WhatsApp等信息
"""
import argparse
import json
import sys

from common import make_request, handle_api_error, print_json_output, cover_fee_info


def check_phone_validity(phones: list) -> dict:
    """
    检测电话有效性

    Args:
        phones: 电话号码列表

    Returns:
        API 响应数据
    """
    params = {"phones": phones}
    response = make_request('/validation/phone', params)
    return response


def main():
    parser = argparse.ArgumentParser(
        description='电话有效性检测 - 检测电话号码的有效性'
    )
    parser.add_argument(
        '--phones',
        type=str,
        help='电话号码列表（空格分隔）'
    )
    parser.add_argument(
        '--params',
        type=str,
        help='JSON 参数字符串（可选）'
    )

    args = parser.parse_args()

    # 解析电话号码
    phones = []
    if args.phones:
        phones = args.phones.split()
    elif args.params:
        try:
            params = json.loads(args.params)
            phones = params.get('phones', [])
        except json.JSONDecodeError as e:
            print(f"错误：参数中的JSON无效：{str(e)}", file=sys.stderr)
            sys.exit(1)
    else:
        print("错误：请提供 --phones 参数", file=sys.stderr)
        sys.exit(1)

    if not phones:
        print("错误：电话号码列表不能为空", file=sys.stderr)
        sys.exit(1)

    # 调用 API
    response = check_phone_validity(phones)

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
