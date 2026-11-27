#!/usr/bin/env python3
"""
跨境魔方公司详情
获取公司的详细信息（工商信息）。
"""
import argparse
import sys
from common import make_request, print_json_output, cover_fee_info
from query_guard import require_user_confirmation
from render_results import render_data_results


def get_company_details(pids:list) -> dict:
    """
    根据公司ID获取公司详情。

    Args:
        pids: 公司IDs

    Returns:
        包含公司详情的API响应
    """
    response = make_request('/agent/search/company/info/batch', {'pids': pids})
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
    parser.add_argument(
        '--user_confirmed',
        action='store_true',
        help='确认用户已在独立消息中批准本次收费查询'
    )

    args = parser.parse_args()

    try:
        require_user_confirmation(args.user_confirmed)
    except ValueError as e:
        print(f"错误：{e}", file=sys.stderr)
        sys.exit(1)

    # 获取公司详情（单个或批量）
    pids = args.pids
    if len(pids) > 20:
        print(f"错误：每次最多处理20条数据", file=sys.stderr)
        sys.exit(1)
    
    response = get_company_details(pids)

    # 从响应中提取数据
    if response.get('code') == 0:
        data = response.get('data', {})
        try:
            delivery = render_data_results(data, 'company_details')
        except Exception as e:
            delivery = {
                'deliveryRequired': True,
                'deliveryError': str(e),
                'instruction': '报告生成失败，仍必须把响应data中的全部公司详情展示给用户。'
            }
        print_json_output({"data": data, "fee": cover_fee_info(response.get('fee', {})), "delivery": delivery})
        if delivery.get('deliveryError'):
            sys.exit(1)
    else:
        print(f"错误：{response.get('msg', '未知错误')}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
