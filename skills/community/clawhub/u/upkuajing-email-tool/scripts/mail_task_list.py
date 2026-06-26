#!/usr/bin/env python3
"""
跨境魔方邮件任务列表工具
查看发送邮件任务列表，支持时间范围筛选。
"""
import argparse
import sys
from typing import Optional, List
from common import make_request, get_api_key, print_json_output


def get_task_list(
    start_time: int = None,
    end_time: int = None,
    status: int = None,
    page_no: int = 1,
    page_size: int = 10,
    api_key: str = None
) -> dict:
    """
    获取邮件任务列表

    Args:
        start_time: 开始时间（秒级时间戳）
        end_time: 结束时间（秒级时间戳）
        status: 发送状态（0-待发送 1-发送中 2-发送完成）
        page_no: 页码（默认1）
        page_size: 页大小（默认10）
        api_key: API密钥（可选，默认从环境变量获取）

    Returns:
        API 响应数据
    """
    # 如果没有提供 api_key，从环境变量获取
    if api_key is None:
        api_key = get_api_key()

    # 构建请求参数
    params = {
        'pageNo': page_no,
        'pageSize': page_size
    }

    if start_time is not None:
        params['startTime'] = start_time
    if end_time is not None:
        params['endTime'] = end_time
    if status is not None:
        params['status'] = status

    # 发起请求
    response = make_request('/mail/task/list', params, api_key=api_key)

    # 处理响应
    if response.get('code') == 0:
        return {
            "success": True,
            "data": response.get('data', {})
        }
    else:
        return {
            "success": False,
            "error_code": response.get('code'),
            "error_msg": response.get('msg', '未知错误')
        }


def main():
    parser = argparse.ArgumentParser(
        description='跨境魔方邮件任务列表工具'
    )
    parser.add_argument(
        '--start_time',
        type=int,
        help='开始时间（秒级时间戳，如：1775812273）'
    )
    parser.add_argument(
        '--end_time',
        type=int,
        help='结束时间（秒级时间戳，如：1775812300）'
    )
    parser.add_argument(
        '--status',
        type=int,
        choices=[0, 1, 2],
        help='发送状态（0-待发送 1-发送中 2-发送完成）'
    )
    parser.add_argument(
        '--page_no',
        type=int,
        default=1,
        help='页码（默认1）'
    )
    parser.add_argument(
        '--page_size',
        type=int,
        default=10,
        help='页大小（默认10）'
    )
    parser.add_argument(
        '--api_key',
        type=str,
        help='API密钥（可选，默认从环境变量获取）'
    )

    args = parser.parse_args()

    # 获取任务列表
    result = get_task_list(
        start_time=args.start_time,
        end_time=args.end_time,
        status=args.status,
        page_no=args.page_no,
        page_size=args.page_size,
        api_key=args.api_key
    )

    # 输出结果
    if result.get('success'):
        print_json_output(result.get('data', {}))
    else:
        print(f"获取失败：{result.get('error_msg', result.get('error'))}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()