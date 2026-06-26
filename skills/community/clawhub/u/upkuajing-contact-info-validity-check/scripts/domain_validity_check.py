#!/usr/bin/env python3
"""
域名有效性检测
检测域名的有效性及安全性
"""
import argparse
import json
import sys

from common import make_request, handle_api_error, print_json_output, cover_fee_info


def check_domain_validity(domains: list) -> dict:
    """
    检测域名有效性

    Args:
        domains: 域名列表

    Returns:
        API 响应数据
    """
    params = {"domains": domains}
    response = make_request('/validation/domain', params)
    return response


def main():
    parser = argparse.ArgumentParser(
        description='域名有效性检测 - 检测域名的有效性及安全性'
    )
    parser.add_argument(
        '--domains',
        type=str,
        help='域名列表（空格分隔）'
    )
    parser.add_argument(
        '--params',
        type=str,
        help='JSON 参数字符串（可选）'
    )

    args = parser.parse_args()

    # 解析域名
    domains = []
    if args.domains:
        domains = args.domains.split()
    elif args.params:
        try:
            params = json.loads(args.params)
            domains = params.get('domains', [])
        except json.JSONDecodeError as e:
            print(f"错误：参数中的JSON无效：{str(e)}", file=sys.stderr)
            sys.exit(1)
    else:
        print("错误：请提供 --domains 参数", file=sys.stderr)
        sys.exit(1)

    if not domains:
        print("错误：域名列表不能为空", file=sys.stderr)
        sys.exit(1)

    # 调用 API
    response = check_domain_validity(domains)

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
