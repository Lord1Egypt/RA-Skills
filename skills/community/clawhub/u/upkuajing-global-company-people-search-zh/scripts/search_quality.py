"""列表数量控制与人物职位相关性检查。"""

import re
from typing import Any, Dict, List, Sequence, Set, Tuple

from common import get_task_result_file
from render_results import load_jsonl_records, write_jsonl_records


TITLE_QUERY_FIELDS = ('titleNames', 'titleRoles', 'titleSubRoles')

GENERIC_TITLE_TOKENS = {
    'and', 'of', 'the', 'for', 'regional', 'global', 'group', 'division',
    'head', 'chief', 'lead', 'leader', 'manager', 'director', 'officer',
    'executive', 'senior', 'junior', 'vice', 'president', 'vp', 'coordinator',
}

ROLE_FAMILIES = (
    ({'procurement', 'purchasing', 'sourcing', 'buyer', 'buying'}, (
        {'procurement'}, {'purchasing'}, {'sourcing'}, {'buyer'}, {'buying'},
    )),
    ({'supply', 'chain', 'logistics'}, (
        {'supply', 'chain'}, {'logistics'},
    )),
)


def limit_result_batch(records: Sequence[Dict[str, Any]], retrieved: int, requested: int) -> List[Dict[str, Any]]:
    """只保留本轮达到用户请求数量所需的记录。"""
    remaining = max(0, requested - retrieved)
    return list(records[:remaining])


def deduplicate_result_batch(
    records: Sequence[Dict[str, Any]],
    id_field: str,
    seen_ids: Set[str],
    retrieved: int,
    requested: int,
) -> List[Dict[str, Any]]:
    """按业务 ID 去重当前批次，并只保留补足用户数量所需的记录。"""
    selected: List[Dict[str, Any]] = []
    remaining = max(0, requested - retrieved)
    for record in records:
        value = record.get(id_field)
        if value in (None, ''):
            continue
        normalized_id = str(value)
        if normalized_id in seen_ids:
            continue
        seen_ids.add(normalized_id)
        selected.append(record)
        if len(selected) >= remaining:
            break
    return selected


def maximum_list_calls(requested: int, include_contacts: bool) -> int:
    """计算脚本允许的列表调用上限；联系方式任务预留一批唯一 ID 补页。"""
    base_calls = (requested + 19) // 20
    return base_calls + (1 if include_contacts else 0)


def initialize_list_task_state(
    requested: int,
    include_contacts: bool,
    contact_types: Sequence[str],
    contact_match: str,
) -> Dict[str, Any]:
    """创建新任务的已确认调用预算和累计费用状态。"""
    return {
        'requested': requested,
        'include_contacts': bool(include_contacts),
        'requested_contact_types': list(contact_types) if include_contacts else [],
        'contact_match': contact_match if include_contacts else 'all',
        'list_call_count': 0,
        'max_list_calls': maximum_list_calls(requested, include_contacts),
        'list_api_cost': 0,
        'contact_api_cost': 0,
        'account_balance': 0,
    }


def restore_list_task_state(
    meta: Dict[str, Any],
    requested_override: Any = None,
) -> Dict[str, Any]:
    """恢复续跑任务的原确认配置、累计调用次数和列表费用。"""
    required_fields = (
        'requested',
        'include_contacts',
        'requested_contact_types',
        'contact_match',
        'list_call_count',
        'max_list_calls',
        'list_api_cost',
        'contact_api_cost',
    )
    missing = [field for field in required_fields if field not in meta]
    if missing:
        raise ValueError(
            '旧任务缺少安全续跑所需的累计状态：'
            f"{', '.join(missing)}。请重新确认条件和费用后发起新任务。"
        )

    try:
        requested = int(meta['requested'])
        list_call_count = int(meta['list_call_count'])
        max_list_calls = int(meta['max_list_calls'])
        list_api_cost = int(meta['list_api_cost'])
        contact_api_cost = int(meta['contact_api_cost'])
        account_balance = int(meta.get('account_balance', 0) or 0)
    except (TypeError, ValueError) as exc:
        raise ValueError('任务累计状态格式无效，不能安全续跑。') from exc

    if requested_override is not None and int(requested_override) != requested:
        raise ValueError(
            f'续跑必须沿用原确认数量 {requested}；如需改为 {requested_override}，'
            '请重新确认条件和费用后发起新任务。'
        )

    include_contacts = bool(meta['include_contacts'])
    expected_max = maximum_list_calls(requested, include_contacts)
    if max_list_calls != expected_max:
        raise ValueError(
            f'任务保存的调用上限 {max_list_calls} 与原确认配置应有的 {expected_max} 不一致，'
            '不能安全续跑。'
        )
    if list_call_count < 0 or list_call_count > max_list_calls:
        raise ValueError('任务累计调用次数超出有效范围，不能安全续跑。')
    if list_api_cost < 0 or contact_api_cost < 0 or account_balance < 0:
        raise ValueError('任务累计费用或余额格式无效，不能安全续跑。')

    contact_types = meta.get('requested_contact_types') or []
    if not isinstance(contact_types, list):
        raise ValueError('任务保存的联系方式类型格式无效，不能安全续跑。')
    contact_match = meta.get('contact_match') or 'all'
    if contact_match not in {'any', 'all'}:
        raise ValueError('任务保存的联系方式匹配方式无效，不能安全续跑。')

    return {
        'requested': requested,
        'include_contacts': include_contacts,
        'requested_contact_types': list(contact_types),
        'contact_match': contact_match,
        'list_call_count': list_call_count,
        'max_list_calls': max_list_calls,
        'remaining_list_calls': max_list_calls - list_call_count,
        'list_api_cost': list_api_cost,
        'contact_api_cost': contact_api_cost,
        'account_balance': account_balance,
    }


def _tokens(value: Any) -> Set[str]:
    return set(re.findall(r'[a-z0-9]+', str(value).lower()))


def _title_anchor_groups(params: Dict[str, Any]) -> List[Tuple[Set[str], ...]]:
    groups: List[Tuple[Set[str], ...]] = []
    for field in TITLE_QUERY_FIELDS:
        values = params.get(field) or []
        if not isinstance(values, (list, tuple, set)):
            values = [values]
        for value in values:
            tokens = _tokens(value)
            if not tokens:
                continue

            family_added = False
            for family_tokens, alternatives in ROLE_FAMILIES:
                if tokens & family_tokens:
                    groups.append(tuple(set(item) for item in alternatives))
                    family_added = True
                    break
            if family_added:
                continue

            meaningful = tokens - GENERIC_TITLE_TOKENS
            if meaningful:
                groups.append((meaningful,))
    return groups


def record_matches_target_title(record: Dict[str, Any], params: Dict[str, Any]) -> bool:
    """按岗位业务词检查人物记录，避免通用职级词造成宽泛命中。"""
    groups = _title_anchor_groups(params)
    if not groups:
        return True
    title_tokens = _tokens(' '.join(str(item) for item in (record.get('title_names') or [])))
    return any(any(alternative <= title_tokens for alternative in group) for group in groups)


def assess_and_prioritize_human_results(task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """标记目标职位匹配结果并将匹配记录排在完整文件前部。"""
    raw_file = get_task_result_file(task_id)
    records, invalid_lines = load_jsonl_records(raw_file)
    if invalid_lines:
        raise ValueError(f'人物列表包含 {invalid_lines} 行无效 JSONL。')

    groups = _title_anchor_groups(params)
    if not groups:
        return {
            'applied': False,
            'assessedCount': len(records),
            'matchedCount': len(records),
            'unmatchedCount': 0,
            'eligibleIds': [str(item.get('hid')) for item in records if item.get('hid')],
        }

    matched: List[Dict[str, Any]] = []
    unmatched: List[Dict[str, Any]] = []
    for record in records:
        record['target_title_match'] = 1 if record_matches_target_title(record, params) else 0
        (matched if record['target_title_match'] else unmatched).append(record)

    write_jsonl_records(raw_file, matched + unmatched)
    return {
        'applied': True,
        'assessedCount': len(records),
        'matchedCount': len(matched),
        'unmatchedCount': len(unmatched),
        'eligibleIds': [str(item.get('hid')) for item in matched if item.get('hid')],
    }
