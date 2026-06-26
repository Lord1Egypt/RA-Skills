#!/usr/bin/env python3
"""
跨境魔方人物详情
获取人物的详细信息。
"""
import argparse
import sys
from common import make_request, print_json_output, cover_fee_info


def get_human_details(hids) -> dict:
    """
    根据人物ID获取人物详情。

    Args:
        hids: 人物ID（字符串或字符串列表）

    Returns:
        包含人物详情的API响应
    """
    params = {'hids': hids}
    response = make_request('/search/person/info/batch', params)
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

    args = parser.parse_args()

    # 获取人物详情
    hids = args.hids
    if len(hids) > 20:
        print(f"错误：每次最多处理20条数据", file=sys.stderr)
        sys.exit(1)

    response = get_human_details(hids)

    # 从响应中提取数据
    if response.get('code') == 0:
        data = response.get('data', {})
        print_json_output({"data": data, "fee": cover_fee_info(response.get('fee', {}))})
    else:
        print(f"错误：{response.get('msg', '未知错误')}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
