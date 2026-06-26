#!/usr/bin/env python3
"""
跨境魔方联系方式
获取公司或人物的联系方式（邮箱、电话、社交媒体、网站）。
"""
import argparse
import sys
from common import make_request, print_json_output, cover_fee_info


def get_contact(bus_ids: list, bus_type: int) -> dict:
    """
    获取公司或人物的联系方式。

    Args:
        bus_ids: 业务ID列表（公司ID或人物ID）
        bus_type: 业务类型（1=公司，2=人物）

    Returns:
        包含联系方式的API响应
    """
    params = {
        'bus_ids': bus_ids,
        'bus_type': bus_type
    }
    response = make_request('/search/contact/batch', params)
    return response


def main():
    parser = argparse.ArgumentParser(
        description='从跨境魔方开放平台获取联系方式'
    )
    parser.add_argument(
        '--bus_ids',
        nargs='+',
        required=True,
        help='公司ID或人物ID列表（空格分隔）'
    )
    parser.add_argument(
        '--bus_type',
        type=int,
        required=True,
        choices=[1, 2],
        help='业务类型：1=公司，2=人物'
    )

    args = parser.parse_args()

    # 获取联系方式
    bus_ids = args.bus_ids
    if len(bus_ids) > 20:
        print(f"错误：每次最多处理20条数据", file=sys.stderr)
        sys.exit(1)

    response = get_contact(bus_ids, args.bus_type)

    # 从响应中提取数据
    if response.get('code') == 0:
        data = response.get('data', {})
        print_json_output({"data": data, "fee": cover_fee_info(response.get('fee', {}))})
    else:
        print(f"错误：{response.get('msg', '未知错误')}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
