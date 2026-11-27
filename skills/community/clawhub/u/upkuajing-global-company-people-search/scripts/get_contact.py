#!/usr/bin/env python3
"""
跨境魔方联系方式
获取公司或人物的联系方式（邮箱、电话、社交媒体、网站）。
"""
import argparse
import sys
from common import make_request, print_json_output, cover_fee_info
from query_guard import require_user_confirmation
from render_results import merge_contact_results, render_data_results


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
    response = make_request('/agent/search/contact/batch', params)
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
    parser.add_argument(
        '--task_id',
        help='原列表任务ID；提供后会把联系方式合并进该任务的result.jsonl和result.xlsx'
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

    # 获取联系方式
    bus_ids = args.bus_ids
    if len(bus_ids) > 20:
        print(f"错误：每次最多处理20条数据", file=sys.stderr)
        sys.exit(1)

    response = get_contact(bus_ids, args.bus_type)

    # 从响应中提取数据
    if response.get('code') == 0:
        data = response.get('data', {})
        try:
            contact_delivery = render_data_results(data, 'contact')
            if args.task_id:
                delivery = merge_contact_results(args.task_id, bus_ids, data)
                delivery['instruction'] += (
                    ' 本次联系方式已合并到完整文件；对话中的前10条预览必须直接展示已返回的完整邮箱、电话、'
                    'WhatsApp等值。'
                )
            else:
                delivery = contact_delivery
        except Exception as e:
            delivery = {
                'deliveryRequired': True,
                'deliveryError': str(e),
                'instruction': '结果文件更新失败，仍必须把响应data中的全部具体联系方式展示给用户，并明确报告文件更新失败。'
            }
            contact_delivery = render_data_results(data, 'contact')
        print_json_output({
            "data": data,
            "fee": cover_fee_info(response.get('fee', {})),
            "contactDelivery": contact_delivery,
            "delivery": delivery
        })
        if delivery.get('deliveryError'):
            sys.exit(1)
    else:
        print(f"错误：{response.get('msg', '未知错误')}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
