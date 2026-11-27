#!/usr/bin/env python3
"""
跨境魔方人物详情
获取人物的详细信息。
"""
import argparse
import sys
from common import make_request, print_json_output, cover_fee_info
from query_guard import require_user_confirmation
from render_results import render_data_results


def get_human_details(hids) -> dict:
    """
    根据人物ID获取人物详情。

    Args:
        hids: 人物ID（字符串或字符串列表）

    Returns:
        包含人物详情的API响应
    """
    params = {'hids': hids}
    response = make_request('/agent/search/person/info/batch', params)
    return response


def main():
    parser = argparse.ArgumentParser(
        description='从跨境魔方开放平台获取人物详情'
    )
    parser.add_argument(
        '--hids',
        nargs='+',
        required=True,
        help='人物ID列表（空格分隔）'
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

    # 获取人物详情
    hids = args.hids
    if len(hids) > 20:
        print(f"错误：每次最多处理20条数据", file=sys.stderr)
        sys.exit(1)

    response = get_human_details(hids)

    # 从响应中提取数据
    if response.get('code') == 0:
        data = response.get('data', {})
        try:
            delivery = render_data_results(data, 'human_details')
        except Exception as e:
            delivery = {
                'deliveryRequired': True,
                'deliveryError': str(e),
                'instruction': '报告生成失败，仍必须把响应data中的全部人物详情展示给用户。'
            }
        print_json_output({"data": data, "fee": cover_fee_info(response.get('fee', {})), "delivery": delivery})
        if delivery.get('deliveryError'):
            sys.exit(1)
    else:
        print(f"错误：{response.get('msg', '未知错误')}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
