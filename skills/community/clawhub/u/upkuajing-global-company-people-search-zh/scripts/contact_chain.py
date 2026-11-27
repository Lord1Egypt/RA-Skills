"""在一次已确认的列表任务中自动补全具体联系方式。"""

import json
import os
from typing import Any, Callable, Dict, List, Optional, Set

from common import get_task_dir, get_task_result_file, make_request
from render_results import (
    extract_contact_values,
    load_jsonl_records,
    merge_contact_results,
    render_task_results,
)


CONTACT_TYPE_TO_FILTER = {
    'email': 'existEmail',
    'phone': 'existPhone',
    'whatsapp': 'existWhatsApp',
}

CONTACT_TYPE_TO_COUNT = {
    'email': 'email_num',
    'phone': 'phone_num',
    'whatsapp': 'ws_num',
}

CONTACT_TYPE_TO_LABEL = {
    'email': '邮箱',
    'phone': '电话',
    'whatsapp': 'WhatsApp',
}


def normalize_contact_types(contact_types: Optional[List[str]]) -> List[str]:
    values = contact_types or ['email', 'phone', 'whatsapp']
    return list(dict.fromkeys(str(value).lower() for value in values))


def resolve_contact_match(contact_types: List[str], contact_match: Optional[str]) -> str:
    """多个联系方式类型必须显式选择“任一”或“全部”逻辑。"""
    requested = normalize_contact_types(contact_types)
    if contact_match in {'any', 'all'}:
        return contact_match
    if len(requested) > 1:
        raise ValueError('选择多个联系方式类型时，必须明确 contact_match=any 或 contact_match=all')
    return 'all'


def apply_contact_existence_filters(
    params: Dict[str, Any],
    contact_types: List[str],
    contact_match: str = 'all',
) -> None:
    """根据“任一”或“全部”语义设置列表联系方式库存筛选。"""
    requested = normalize_contact_types(contact_types)
    if contact_match == 'any':
        # API 的多个存在性字段是 AND。任一类型即可时只使用用户顺序中的
        # 第一种联系方式作为库存锚点，确保入选记录可进入具体值查询。
        for contact_type in CONTACT_TYPE_TO_FILTER:
            params.pop(CONTACT_TYPE_TO_FILTER[contact_type], None)
        if requested:
            params[CONTACT_TYPE_TO_FILTER[requested[0]]] = 1
        return
    for contact_type in requested:
        params[CONTACT_TYPE_TO_FILTER[contact_type]] = 1


def _positive(value: Any) -> bool:
    if isinstance(value, (int, float)):
        return value > 0
    if isinstance(value, str):
        try:
            return float(value.strip()) > 0
        except ValueError:
            return bool(value.strip())
    return False


def _has_requested_contact_values(
    record: Dict[str, Any],
    requested: List[str],
    contact_match: str,
) -> bool:
    existing_labels = set(extract_contact_values(record))
    required_labels = {CONTACT_TYPE_TO_LABEL[item] for item in requested}
    return (
        bool(existing_labels & required_labels)
        if contact_match == 'any'
        else required_labels <= existing_labels
    )


def select_completed_contact_ids(
    records: List[Dict[str, Any]],
    entity_type: str,
    contact_types: List[str],
    max_ids: Optional[int] = None,
    allowed_ids: Optional[Set[str]] = None,
    contact_match: str = 'all',
) -> List[str]:
    """选择已经具备所需具体联系方式的唯一业务 ID。"""
    if max_ids is not None and max_ids <= 0:
        return []
    id_field = 'pid' if entity_type == 'company' else 'hid'
    requested = normalize_contact_types(contact_types)
    selected: List[str] = []
    seen_ids: Set[str] = set()
    for record in records:
        record_id = record.get(id_field)
        if record_id in (None, ''):
            continue
        normalized_id = str(record_id)
        if allowed_ids is not None and normalized_id not in allowed_ids:
            continue
        if normalized_id in seen_ids:
            continue
        seen_ids.add(normalized_id)
        if not _has_requested_contact_values(record, requested, contact_match):
            continue
        selected.append(normalized_id)
        if max_ids is not None and len(selected) >= max_ids:
            break
    return selected


def select_contact_ids(
    records: List[Dict[str, Any]],
    entity_type: str,
    contact_types: List[str],
    max_ids: Optional[int] = None,
    allowed_ids: Optional[Set[str]] = None,
    contact_match: str = 'all',
) -> List[str]:
    """从列表结果中选择应自动进入联系方式接口的 ID。"""
    if max_ids is not None and max_ids <= 0:
        return []
    id_field = 'pid' if entity_type == 'company' else 'hid'
    requested = normalize_contact_types(contact_types)
    selected: List[str] = []
    seen_ids: Set[str] = set()
    for record in records:
        record_id = record.get(id_field)
        if record_id in (None, ''):
            continue
        normalized_id = str(record_id)
        if allowed_ids is not None and normalized_id not in allowed_ids:
            continue
        if normalized_id in seen_ids:
            continue

        if _has_requested_contact_values(record, requested, contact_match):
            continue

        inventory_values = [record.get(CONTACT_TYPE_TO_COUNT[item]) for item in requested]
        inventory_is_reported = any(value not in (None, '') for value in inventory_values)
        if inventory_is_reported:
            inventory_matches = (
                any(_positive(value) for value in inventory_values)
                if contact_match == 'any'
                else all(_positive(value) for value in inventory_values)
            )
            if not inventory_matches:
                continue

        selected.append(normalized_id)
        seen_ids.add(normalized_id)
        if max_ids is not None and len(selected) >= max_ids:
            break
    return selected


def determine_contact_status(
    contact_ids: List[str],
    successful_ids: int,
    error_message: Optional[str],
    required_count: Optional[int] = None,
) -> str:
    """根据实际合并数量判定联系方式阶段状态。"""
    if not contact_ids:
        return 'no_eligible_ids'
    if error_message and successful_ids:
        return 'partial'
    if error_message:
        return 'fail'
    if successful_ids == 0:
        return 'fail'
    target_count = required_count if required_count is not None else len(contact_ids)
    if successful_ids < target_count:
        return 'partial'
    return 'success'


def append_contact_response_audit(task_id: str, batch: List[str], response: Dict[str, Any]) -> str:
    """保存每批联系方式原始响应，支持费用与合并结果核对。"""
    audit_file = os.path.join(get_task_dir(task_id), 'contact_response_batches.jsonl')
    os.makedirs(os.path.dirname(audit_file), exist_ok=True)
    payload = {
        'requested_ids': batch,
        'code': response.get('code'),
        'msg': response.get('msg'),
        'data': response.get('data'),
        'fee': response.get('fee'),
    }
    with open(audit_file, 'a', encoding='utf-8') as file:
        file.write(json.dumps(payload, ensure_ascii=False) + '\n')
    return os.path.abspath(audit_file)


def enrich_task_contacts(
    task_id: str,
    entity_type: str,
    contact_types: List[str],
    max_ids: Optional[int] = None,
    allowed_ids: Optional[Set[str]] = None,
    contact_match: str = 'all',
    required_count: Optional[int] = None,
    request_func: Callable[[str, Dict[str, Any]], Dict[str, Any]] = make_request,
) -> Dict[str, Any]:
    """连续调用联系方式接口并合并结果；过程中不产生用户预览。"""
    records, invalid_lines = load_jsonl_records(get_task_result_file(task_id))
    if invalid_lines:
        raise ValueError(f'列表结果包含 {invalid_lines} 行无效 JSONL，不能安全补全联系方式。')

    requested_types = normalize_contact_types(contact_types)
    already_completed_ids = select_completed_contact_ids(
        records,
        entity_type,
        requested_types,
        max_ids=max_ids,
        allowed_ids=allowed_ids,
        contact_match=contact_match,
    )
    remaining_max_ids = None if max_ids is None else max(0, max_ids - len(already_completed_ids))
    contact_ids = select_contact_ids(
        records,
        entity_type,
        requested_types,
        max_ids=remaining_max_ids,
        allowed_ids=allowed_ids,
        contact_match=contact_match,
    )
    bus_type = 1 if entity_type == 'company' else 2
    total_cost = 0
    account_balance = None
    successful_ids = len(already_completed_ids)
    call_count = 0
    error_message = None
    delivery = render_task_results(task_id, entity_type)
    response_audit_file = None
    aggregate_missing_ids: List[str] = []
    batch_reports: List[Dict[str, Any]] = []

    for offset in range(0, len(contact_ids), 20):
        batch = contact_ids[offset:offset + 20]
        response = request_func('/agent/search/contact/batch', {
            'bus_ids': batch,
            'bus_type': bus_type,
        })
        call_count += 1
        response_audit_file = append_contact_response_audit(task_id, batch, response)

        fee = response.get('fee') or {}
        total_cost += fee.get('apiCost', 0) or 0
        if fee.get('accountBalance') is not None:
            account_balance = fee.get('accountBalance')

        if response.get('code') != 0:
            error_message = response.get('msg', '联系方式接口返回未知错误')
            break

        delivery = merge_contact_results(
            task_id,
            batch,
            response.get('data', {}),
            entity_type=entity_type,
            requested_contact_types=requested_types,
            contact_match=contact_match,
        )
        merge_report = delivery.get('contactMerge', {})
        merged_count = merge_report.get('mergedIdCount', 0)
        successful_ids += merged_count
        aggregate_missing_ids.extend(str(item) for item in merge_report.get('missingIds', []))
        batch_reports.append({
            'requestedIdCount': len(batch),
            'mergedIdCount': merged_count,
            'missingIdCount': len(merge_report.get('missingIds', [])),
        })

    status = determine_contact_status(
        already_completed_ids + contact_ids,
        successful_ids,
        error_message,
        required_count=required_count,
    )
    if status == 'fail' and not error_message and contact_ids:
        error_message = '联系方式接口已完成处理，本次未返回可交付的具体联系方式'
    elif status == 'partial' and not error_message:
        target_count = required_count if required_count is not None else len(contact_ids)
        error_message = f'联系方式已补全 {successful_ids}/{target_count} 条'

    delivery = render_task_results(task_id, entity_type)
    delivery['contactMerge'] = {
        'requestedIdCount': len(already_completed_ids) + len(contact_ids),
        'alreadyCompletedIdCount': len(already_completed_ids),
        'queriedIdCount': len(contact_ids),
        'mergedIdCount': successful_ids,
        'missingIdCount': len(aggregate_missing_ids),
        'missingIds': aggregate_missing_ids,
        'batchReports': batch_reports,
        'responseAuditFile': response_audit_file,
    }

    return {
        'status': status,
        'requestedContactTypes': requested_types,
        'contactMatch': contact_match,
        'eligibleIdCount': len(already_completed_ids) + len(contact_ids),
        'alreadyCompletedIdCount': len(already_completed_ids),
        'queriedIdCount': len(contact_ids),
        'contactCallCount': call_count,
        'successfulIdCount': successful_ids,
        'errorMessage': error_message,
        'responseAuditFile': response_audit_file,
        'fee': {
            'apiCost': total_cost,
            'accountBalance': account_balance,
        },
        'delivery': delivery,
    }
