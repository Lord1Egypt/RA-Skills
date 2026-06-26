#!/usr/bin/env python3
"""
跨境魔方商户列表搜索
通过地图获客API搜索商户，使用游标查询支持大数据量检索。
"""
import argparse
import sys
from common import (
    make_request, parse_params, print_json_output,
    generate_task_id, load_task_meta, save_task_meta,
    append_result_data, get_task_result_file
)


def search_merchants(params: dict, cursor: str = None) -> dict:
    """
    使用游标搜索商户列表。

    Args:
        params: 搜索参数
        cursor: 游标字符串，首次请求时不传

    Returns:
        包含商户列表的API响应
    """
    request_params = params.copy()
    if cursor:
        request_params['cursor'] = cursor

    # 向 /map/search 端点发起请求
    response = make_request('/map/search', request_params)
    return response


def main():
    parser = argparse.ArgumentParser(
        description='从跨境魔方开放平台搜索商户信息'
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
        help='期望获取的总记录数（默认：20）'
    )

    args = parser.parse_args()

    # 验证互斥参数
    if not args.params and not args.task_id:
        print("错误：--params 和 --task_id 必须指定其中一个", file=sys.stderr)
        sys.exit(1)

    if args.params and args.task_id:
        print("错误：--params 和 --task_id 不能同时指定", file=sys.stderr)
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

        # 参数校验
        # 新版API不再使用search_type，通过geoDistance判断是否为附近搜索
        geo_distance = params.get('geoDistance')
        if geo_distance:
            # 附近搜索模式
            missing = []
            location = geo_distance.get('location', {})
            if 'lat' not in location:
                missing.append('geoDistance.location.lat')
            if 'lon' not in location:
                missing.append('geoDistance.location.lon')
            if 'distance' not in geo_distance:
                missing.append('geoDistance.distance')
            if missing:
                print(f"错误：附近搜索缺少必填参数: {', '.join(missing)}", file=sys.stderr)
                print("请查看 references/merchants-search-api.md 了解正确的参数格式", file=sys.stderr)
                sys.exit(1)
        else:
            # 区域搜索模式：至少需要 keywords 或 countryCodes
            if 'keywords' not in params and 'countryCodes' not in params:
                print("错误：区域搜索至少需要 keywords 或 countryCodes 参数之一", file=sys.stderr)
                print("请查看 references/merchants-search-api.md 了解正确的参数格式", file=sys.stderr)
                sys.exit(1)

    # 游标查询循环
    total_retrieved = 0
    error_message = None

    # 显示查询目标
    print(f"开始查询：目标获取 {args.query_count} 条数据...")

    while total_retrieved < args.query_count:
        try:
            # 搜索当前批次
            response = search_merchants(params, current_cursor)

            # 检查API响应
            if response.get('code') != 0:
                error_message = response.get('msg', '未知错误')
                break

            # 提取数据
            data = response.get('data', {})
            merchants_list = data.get('list') or []
            current_cursor = data.get('cursor')  # 获取新的游标

            # 保存数据到文件
            if merchants_list:
                append_result_data(task_id, merchants_list)
                total_retrieved += len(merchants_list)

                # 显示进度
                progress = (total_retrieved / args.query_count) * 100
                print(f"进度：{total_retrieved}/{args.query_count} ({progress:.1f}%)")

            # 更新任务元数据
            # 是否完成：获取足够数据、没有更多数据、没有游标
            is_completed = (total_retrieved >= args.query_count) or len(merchants_list) == 0 or (not current_cursor)
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
        print(f"查询完成：共获取 {total_retrieved} 条数据")

    # 构建最终输出
    output_data = {
        'task_id': task_id,
        'status': 'fail' if error_message else 'success',
        'total_hits': total_retrieved,
        'error_msg': error_message,
        'file_url': get_task_result_file(task_id)
    }

    # 输出结果
    print_json_output(output_data)

    # 如果有错误，返回非0退出码
    if error_message:
        sys.exit(1)


if __name__ == '__main__':
    main()
