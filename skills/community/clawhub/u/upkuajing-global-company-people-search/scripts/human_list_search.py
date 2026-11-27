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
from query_guard import (
    enforce_exact_matching,
    normalize_human_search_params,
    require_user_confirmation,
    validate_human_search_params,
)
from render_results import load_jsonl_records, render_task_results
from contact_chain import apply_contact_existence_filters, enrich_task_contacts, resolve_contact_match
from search_quality import (
    assess_and_prioritize_human_results,
    deduplicate_result_batch,
    initialize_list_task_state,
    restore_list_task_state,
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
    request_params = enforce_exact_matching(normalize_human_search_params(params))
    if cursor:
        request_params['cursor'] = cursor
    # 不传 cursor 表示首次请求

    # 发起API请求
    response = make_request('/agent/search/person/list', request_params)
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
        help='期望获取的总记录数（新任务默认：20，范围：20-1000；续跑默认沿用原任务）'
    )
    parser.add_argument(
        '--user_confirmed',
        action='store_true',
        help='确认用户已在独立消息中批准本次完整查询条件和最高费用范围'
    )
    parser.add_argument(
        '--include_contacts',
        action='store_true',
        default=None,
        help='列表查询后自动继续获取具体联系方式，中间不暂停或展示列表'
    )
    parser.add_argument(
        '--contact_types',
        nargs='+',
        choices=['email', 'phone', 'whatsapp'],
        help='需要自动补全的具体联系方式类型；与--include_contacts一起使用'
    )
    parser.add_argument(
        '--contact_match',
        choices=['any', 'all'],
        help='联系方式匹配：any=任一类型即可，all=必须具备全部所选类型'
    )

    args = parser.parse_args()

    try:
        require_user_confirmation(args.user_confirmed)
    except ValueError as e:
        print(f"错误：{e}", file=sys.stderr)
        sys.exit(1)

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

        try:
            params = enforce_exact_matching(normalize_human_search_params(meta['params']))
        except ValueError as e:
            print(f"错误：旧任务使用了不再支持的匹配方式。{e}", file=sys.stderr)
            sys.exit(1)
        current_cursor = meta.get('cursor')
        if not current_cursor:
            print(f"错误：任务 {task_id} 已经没有更多数据，建议调整参数后发起新任务查询", file=sys.stderr)
            sys.exit(1)

        try:
            task_state = restore_list_task_state(meta, args.query_count)
        except ValueError as e:
            print(f"错误：{e}", file=sys.stderr)
            sys.exit(1)

        query_count = task_state['requested']
        include_contacts = task_state['include_contacts']
        requested_contact_types = task_state['requested_contact_types']
        contact_match = task_state['contact_match']

        if args.include_contacts is True and not include_contacts:
            print("错误：续跑不能新增联系方式阶段；请重新确认条件和费用后发起新任务", file=sys.stderr)
            sys.exit(1)
        if args.contact_types and list(dict.fromkeys(args.contact_types)) != requested_contact_types:
            print("错误：续跑必须沿用原任务确认的联系方式类型", file=sys.stderr)
            sys.exit(1)
        if args.contact_match and args.contact_match != contact_match:
            print("错误：续跑必须沿用原任务确认的联系方式匹配方式", file=sys.stderr)
            sys.exit(1)
    else:
        # 创建新任务
        task_id = generate_task_id()
        params = normalize_human_search_params(parse_params(args.params))
        current_cursor = None
        query_count = args.query_count if args.query_count is not None else 20
        include_contacts = bool(args.include_contacts)

        if args.contact_types and not include_contacts:
            print("错误：--contact_types 必须与 --include_contacts 一起使用", file=sys.stderr)
            sys.exit(1)
        if args.contact_match and not include_contacts:
            print("错误：--contact_match 必须与 --include_contacts 一起使用", file=sys.stderr)
            sys.exit(1)

        requested_contact_types = list(dict.fromkeys(
            args.contact_types or ['email', 'phone', 'whatsapp']
        ))
        contact_match = 'all'
        if include_contacts:
            try:
                contact_match = resolve_contact_match(requested_contact_types, args.contact_match)
            except ValueError as e:
                print(f"错误：{e}", file=sys.stderr)
                sys.exit(1)

        task_state = initialize_list_task_state(
            query_count,
            include_contacts,
            requested_contact_types,
            contact_match,
        )

        try:
            params = enforce_exact_matching(params)
            validate_human_search_params(params)
        except ValueError as e:
            print(f"错误：{e}", file=sys.stderr)
            sys.exit(1)

        # 设置默认排序；精准匹配已由请求守卫强制启用。
        if 'sort' not in params:
            params['sort'] = 0  # 0-匹配度排序，1-综合排序

    if query_count < 20 or query_count > 1000:
        print("错误：query_count 必须在 20 到 1000 之间", file=sys.stderr)
        sys.exit(1)

    if include_contacts:
        apply_contact_existence_filters(
            params,
            requested_contact_types,
            contact_match,
        )

    # 游标查询循环。按人物 hid 去重；具体联系方式任务最多预留一批补页。
    existing_records, invalid_lines = load_jsonl_records(get_task_result_file(task_id))
    if invalid_lines:
        print(f"错误：已有任务包含 {invalid_lines} 行无效 JSONL", file=sys.stderr)
        sys.exit(1)
    seen_hids = {
        str(record.get('hid')) for record in existing_records
        if record.get('hid') not in (None, '')
    }
    total_retrieved = len(seen_hids)
    list_call_count = task_state['list_call_count']
    max_list_calls = task_state['max_list_calls']
    error_message = None
    # 列表累计费用，续跑时从任务元数据恢复。单位：分钱。
    list_api_cost = task_state['list_api_cost']
    contact_api_cost = task_state['contact_api_cost']
    account_balance = task_state['account_balance']

    def save_progress(status: str) -> None:
        save_task_meta(task_id, {
            'task_id': task_id,
            'params': params,
            'cursor': current_cursor,
            'total_retrieved': total_retrieved,
            'requested': query_count,
            'include_contacts': include_contacts,
            'requested_contact_types': requested_contact_types if include_contacts else [],
            'contact_match': contact_match if include_contacts else 'all',
            'list_call_count': list_call_count,
            'max_list_calls': max_list_calls,
            'remaining_list_calls': max(0, max_list_calls - list_call_count),
            'list_api_cost': list_api_cost,
            'contact_api_cost': contact_api_cost,
            'account_balance': account_balance,
            'status': status,
        })

    # 显示查询目标
    print(
        f"开始查询：目标获取 {query_count} 条数据，"
        f"累计已用列表调用 {list_call_count}/{max_list_calls} 次..."
    )

    while total_retrieved < query_count and list_call_count < max_list_calls:
        try:
            # 搜索当前批次
            response = search_human_list(params, current_cursor)
            list_call_count += 1

            fee = response.get('fee') or {}
            list_api_cost += fee.get("apiCost", 0) or 0
            if fee.get("accountBalance") is not None:
                account_balance = fee.get("accountBalance")

            # 检查API响应
            if response.get('code') != 0:
                error_message = response.get('msg', '未知错误')
                save_progress('in_progress')
                break

            # 提取数据
            data = response.get('data', {})
            human_list = data.get('list') or []
            current_cursor = data.get('cursor')  # 获取新的游标

            # 保存数据到文件
            if human_list:
                selected_humans = deduplicate_result_batch(
                    human_list,
                    'hid',
                    seen_hids,
                    total_retrieved,
                    query_count,
                )
                append_result_data(task_id, selected_humans)
                total_retrieved += len(selected_humans)

                # 显示进度
                progress = (total_retrieved / query_count) * 100
                print(f"进度：{total_retrieved}/{query_count} ({progress:.1f}%)")

            # 更新任务元数据
            # 是否完成 没有更多数据、没有游标、获取足够数据
            target_reached = total_retrieved >= query_count
            is_completed = target_reached or len(human_list) == 0 or (not current_cursor)
            if target_reached:
                current_cursor = None
            status = 'completed' if is_completed else 'in_progress'
            save_progress(status)

            # 检查是否完成
            if is_completed:
                break

        except SystemExit:
            # SystemExit（如余额不足）直接重新抛出
            raise
        except Exception as e:
            # 其他错误记录并停止
            error_message = str(e)
            try:
                save_progress('in_progress')
            except Exception:
                pass
            break

    if total_retrieved < query_count and list_call_count >= max_list_calls and current_cursor:
        error_message = error_message or (
            f"唯一人物补页已使用确认单中的 {max_list_calls} 次列表调用，"
            f"本次获得 {total_retrieved}/{query_count} 位"
        )

    quality_result = assess_and_prioritize_human_results(task_id, params)
    eligible_contact_ids = quality_result.pop('eligibleIds', [])
    if quality_result.get('applied') and quality_result.get('matchedCount', 0) < query_count:
        error_message = error_message or (
            f"目标职位筛选后获得 {quality_result.get('matchedCount', 0)} 条匹配结果，"
            f"本次列表调用已按确认范围完成"
        )

    # 用户已在同一次确认中要求具体联系方式时，自动连续完成第二阶段。
    # 此处不输出列表预览，也不再次请求确认。
    list_cost = list_api_cost
    contact_cost = contact_api_cost
    contact_result = None
    if include_contacts:
        try:
            contact_result = enrich_task_contacts(
                task_id,
                'human',
                requested_contact_types,
                max_ids=query_count,
                allowed_ids=set(eligible_contact_ids) if quality_result.get('applied') else None,
                contact_match=contact_match,
                required_count=query_count,
            )
            contact_fee = contact_result.get('fee') or {}
            contact_cost += contact_fee.get('apiCost', 0) or 0
            contact_api_cost = contact_cost
            if contact_fee.get('accountBalance') is not None:
                account_balance = contact_fee.get('accountBalance')
            if contact_result.get('status') == 'no_eligible_ids':
                error_message = error_message or '列表结果中没有符合条件且可用于联系方式查询的ID'
            elif contact_result.get('status') in {'partial', 'fail'}:
                error_message = error_message or contact_result.get('errorMessage') or '联系方式补全未完成'
        except Exception as e:
            error_message = error_message or f'联系方式自动补全失败：{e}'

        try:
            save_progress('completed' if not current_cursor else 'in_progress')
        except Exception as e:
            error_message = error_message or f'累计联系方式费用保存失败：{e}'

    total_cost = list_cost + contact_cost

    # 两阶段全部完成后才生成唯一一次用户可见预览、完整JSONL与Excel
    delivery_error = None
    try:
        if contact_result and contact_result.get('delivery'):
            delivery = contact_result['delivery']
        else:
            delivery = render_task_results(task_id, 'human')
    except Exception as e:
        delivery_error = str(e)
        delivery = {
            'deliveryRequired': True,
            'deliveryError': delivery_error,
            'rawFile': get_task_result_file(task_id),
            'instruction': '结果交付文件生成失败；仍必须提供原始JSONL并展示最多前10条，同时明确说明Excel未生成。'
        }

    saved_total = delivery.get('recordCount', total_retrieved)

    # 显示完成提示
    if error_message:
        print(f"查询部分或全部失败：{error_message}；已保存 {saved_total} 条结果", file=sys.stderr)
    elif delivery_error:
        print(f"查询成功，但结果预览生成失败：{delivery_error}", file=sys.stderr)
    else:
        print(f"查询完成：共获取 {total_retrieved} 条数据，总费用 {total_cost}分钱")

    if error_message and saved_total > 0:
        final_status = 'partial'
    elif error_message:
        final_status = 'fail'
    elif delivery_error:
        final_status = 'delivery_failed'
    else:
        final_status = 'success'
    contact_summary = (
        {key: value for key, value in contact_result.items() if key != 'delivery'}
        if contact_result else None
    )

    # 构建最终输出
    output_data = {
        'task_id': task_id,
        'status': final_status,
        'total_hits': total_retrieved,
        'list_call_count': list_call_count,
        'max_list_calls': max_list_calls,
        'remaining_list_calls': max(0, max_list_calls - list_call_count),
        'error_msg': error_message or delivery_error,
        'file_url': get_task_result_file(task_id),
        'fee': {
            "apiCost": f"{total_cost}分钱",
            "listApiCost": f"{list_cost}分钱",
            "contactApiCost": f"{contact_cost}分钱",
            "balance": f"{account_balance}分钱"
        },
        'contactEnrichment': contact_summary,
        'qualityAssessment': quality_result,
        'delivery': delivery
    }

    # 输出结果
    print_json_output(output_data)

    # 如果有错误，返回非0退出码
    if error_message or delivery_error:
        sys.exit(1)


if __name__ == '__main__':
    main()
