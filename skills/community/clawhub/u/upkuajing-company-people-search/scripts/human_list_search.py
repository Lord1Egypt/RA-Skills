#!/usr/bin/env python3
"""
跨境魔方人物列表搜索
通过职位、公司、学校等信息搜索人物，使用游标查询支持大数据量检索。
"""
import argparse
import sys
from common import (
    make_request, parse_params, print_json_output,
    generate_task_id, load_task_meta, save_task_meta,
    append_result_data, get_task_result_file
)


def search_human_list(params: dict, cursor: str = None) -> dict:
    """
    使用游标搜索人物列表。

    Args:
        params: 搜索参数
        cursor: 游标字符串，首次请求时不传

    Returns:
        包含人物列表的API响应
    """
    # 复制参数，添加游标信息
    request_params = params.copy()
    if cursor:
        request_params['cursor'] = cursor
    # 不传 cursor 表示首次请求

    # 发起API请求
    response = make_request('/search/person/list', request_params)
    return response


def main():
    parser = argparse.ArgumentParser(
        description='从跨境魔方开放平台搜索人物信息'
    )
    parser.add_argument(
        '--params',
        help='搜索参数JSON字符串'
    )
    parser.add_argument(
        '--task_id',
        help='任务ID，用于继续之前的任务或查询任务状态'
    )
    parser.add_argument(
        '--query_count',
        type=int,
        default=20,
        help='期望获取的总记录数（默认：20，范围：20-1000）'
    )

    args = parser.parse_args()

    # 验证互斥参数
    if not args.params and not args.task_id:
        print("错误：--params 和 --task_id 必须指定其中一个", file=sys.stderr)
        sys.exit(1)

    if args.params and args.task_id:
        print("错误：--params 和 --task_id 不能同时指定", file=sys.stderr)
        sys.exit(1)

    # 验证 query_count 范围
    if args.query_count < 20 or args.query_count > 1000:
        print("错误：query_count 必须在 20 到 1000 之间", file=sys.stderr)
        sys.exit(1)

    # 确定 task_id、参数和游标
    if args.task_id:
        # 继续已有任务
        task_id = args.task_id
        meta = load_task_meta(task_id)
        if not meta:
            print(f"错误：任务 {task_id} 不存在", file=sys.stderr)
            sys.exit(1)

        params = meta['params']
        current_cursor = meta.get('cursor')
        if not current_cursor:
            print(f"错误：任务 {task_id} 已经没有更多数据，建议调整参数后发起新任务查询", file=sys.stderr)
            sys.exit(1)
    else:
        # 创建新任务
        task_id = generate_task_id()
        params = parse_params(args.params)
        current_cursor = None

        # 设置默认参数（建议设置排序和匹配方式）
        if 'sort' not in params:
            params['sort'] = 0  # 0-匹配度排序，1-综合排序
        if 'isExact' not in params:
            params['isExact'] = False  # false-模糊匹配，true-精确匹配

    # 游标查询循环
    total_retrieved = 0
    error_message = None
    # 总费用 单位分钱
    total_cost = 0
    # 余额
    account_balance = 0

    # 显示查询目标
    print(f"开始查询：目标获取 {args.query_count} 条数据...")

    while total_retrieved < args.query_count:
        try:
            # 搜索当前批次
            response = search_human_list(params, current_cursor)

            # 检查API响应
            if response.get('code') != 0:
                error_message = response.get('msg', '未知错误')
                break

            # 提取数据
            data = response.get('data', {})
            # 提取费用信息 金额单位 分钱
            fee = response.get('fee', {})
            human_list = data.get('list') or []
            current_cursor = data.get('cursor')  # 获取新的游标

            # 保存数据到文件
            if human_list:
                append_result_data(task_id, human_list)
                total_retrieved += len(human_list)

                # 显示进度
                progress = (total_retrieved / args.query_count) * 100
                print(f"进度：{total_retrieved}/{args.query_count} ({progress:.1f}%)")

            if fee:
                total_cost += fee.get("apiCost", 0)
                account_balance = fee.get("accountBalance", 0)

            # 更新任务元数据
            # 是否完成 没有更多数据、没有游标、获取足够数据
            is_completed = (total_retrieved >= args.query_count) or len(human_list) == 0 or (not current_cursor)
            status = 'completed' if is_completed else 'in_progress'
            meta = {
                'task_id': task_id,
                'params': params,
                'cursor': current_cursor,
                'total_retrieved': total_retrieved,
                'requested': args.query_count,
                'status': status
            }
            save_task_meta(task_id, meta)

            # 检查是否完成
            if is_completed:
                break

        except SystemExit:
            # SystemExit（如余额不足）直接重新抛出
            raise
        except Exception as e:
            # 其他错误记录并停止
            error_message = str(e)
            break

    # 显示完成提示
    if error_message:
        print(f"查询失败：{error_message}", file=sys.stderr)
    else:
        print(f"查询完成：共获取 {total_retrieved} 条数据，总费用 {total_cost}分钱(RMB)")
    # 构建最终输出
    output_data = {
        'task_id': task_id,
        'status': 'fail' if error_message else 'success',
        'total_hits': total_retrieved,
        'error_msg': error_message,
        'file_url': get_task_result_file(task_id),
        'fee': {
            "apiCost": f"{total_cost}分钱(RMB)",
            "balance": f"{account_balance}分钱(RMB)"
        }
    }

    # 输出结果
    print_json_output(output_data)

    # 如果有错误，返回非0退出码
    if error_message:
        sys.exit(1)


if __name__ == '__main__':
    main()
