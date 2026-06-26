#!/usr/bin/env python3
"""
跨境魔方公司联系方式
获取公司的联系信息（邮箱、电话、社交媒体、网站）。
"""
import argparse
import sys
from common import make_request, print_json_output, cover_fee_info


def get_contact_info(company_ids) -> dict:
    """
    获取公司的联系信息。

    Args:
        company_ids: 公司ID列表

    Returns:
        包含联系信息的API响应
    """
    params = {
        'companyIds': company_ids
    }
    response = make_request('/customs/company/contact/batch', params)
    return response


def main():
    parser = argparse.ArgumentParser(
        description='从跨境魔方开放平台获取公司联系信息'
    )
    parser.add_argument(
        '--companyIds',
        type=int,
        nargs='+',
        required=True,
        help='公司ID列表（空格分隔）'
    )

    args = parser.parse_args()

    # 获取联系信息
    company_ids = args.companyIds
    if len(company_ids) > 20:
        print(f"错误：每次最多处理20条数据", file=sys.stderr)
        sys.exit(1)

    response = get_contact_info(company_ids)

    # 从响应中提取数据
    if response.get('code') == 0:
        data = response.get('data', {})
        print_json_output({"data": data, "fee": cover_fee_info(response.get('fee', {}))})
    else:
        print(f"错误：{response.get('msg', '未知错误')}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
