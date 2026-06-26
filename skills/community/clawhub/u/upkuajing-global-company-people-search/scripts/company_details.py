#!/usr/bin/env python3
"""
跨境魔方公司详情
获取公司的详细信息（工商信息）。
"""
import argparse
import sys
from common import make_request, print_json_output, cover_fee_info


def get_company_details(pids:list) -> dict:
    """
    根据公司ID获取公司详情。

    Args:
        pids: 公司IDs

    Returns:
        包含公司详情的API响应
    """
    response = make_request('/search/company/info/batch', {'pids': pids})
    return response


def main():
    parser = argparse.ArgumentParser(
        description='从跨境魔方开放平台获取公司详情'
    )
    parser.add_argument(
        '--pids',
        nargs='+',
        required=True,
        help='公司ID列表（空格分隔）'
    )

    args = parser.parse_args()

    # 获取公司详情（单个或批量）
    pids = args.pids
    if len(pids) > 20:
        print(f"错误：每次最多处理20条数据", file=sys.stderr)
        sys.exit(1)
    
    response = get_company_details(pids)

    # 从响应中提取数据
    if response.get('code') == 0:
        data = response.get('data', {})
        print_json_output({"data": data, "fee": cover_fee_info(response.get('fee', {}))})
    else:
        print(f"错误：{response.get('msg', '未知错误')}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
