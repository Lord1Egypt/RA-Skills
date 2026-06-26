#!/usr/bin/env python3
"""LUI 定时任务创建前重复/冲突检测脚本。

输入 JSON:
{
  "proposed_task": {...},
  "existing_tasks": [...],
  "user_context": {...}
}
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Sequence, Set, Tuple

try:
    from _tracker import emit as track_event
except Exception:  # pragma: no cover - tracking must never block conflict checks.
    def track_event(event: str, payload: Dict[str, Any] | None = None) -> None:
        return


CANONICAL_ALIASES: Dict[str, Sequence[str]] = {
    "auto_listing": ("auto_listing", "automatic_listing", "自动铺货", "铺货", "上架商品", "商品上架", "每日铺货"),
    "auto_follow_order": ("auto_follow_order", "follow_order", "自动跟单", "跟单", "催发货", "物流跟进", "退款风险"),
    "inventory_sync": ("inventory_sync", "stock_sync", "库存同步", "同步库存", "库存管理"),
    "price_adjust": ("price_adjust", "price_change", "改价", "调价", "降价", "低利润商品降价"),
    "auto_delist": ("auto_delist", "delist", "自动下架", "批量下架", "商品下架", "无动销商品下架"),
    "supplier_switch": ("supplier_switch", "智能换供", "换供"),
    "product_selection": ("product_selection", "选品", "找品", "商机"),
    "inspection": ("inspection", "巡检", "风险巡检", "店铺巡检"),
    "customer_service": ("customer_service", "智能客服", "客服巡检"),
    "daily_report": ("daily_report", "经营日报", "日报", "任务汇总报告"),
}

TASK_TRAITS: Dict[str, Dict[str, Any]] = {
    "auto_listing": {"operation": "write", "resource": "product", "field": "listing", "risk": "medium", "steps": ["product_selection", "auto_listing"]},
    "auto_follow_order": {"operation": "write", "resource": "order", "field": "order_status", "risk": "medium", "steps": ["auto_follow_order"]},
    "inventory_sync": {"operation": "write", "resource": "product", "field": "inventory", "risk": "medium", "steps": ["inventory_sync"]},
    "price_adjust": {"operation": "write", "resource": "product", "field": "price", "risk": "high", "steps": ["price_adjust"]},
    "auto_delist": {"operation": "write", "resource": "product", "field": "listing_state", "risk": "high", "steps": ["auto_delist"]},
    "supplier_switch": {"operation": "write", "resource": "product", "field": "supplier", "risk": "medium", "steps": ["supplier_switch"]},
    "product_selection": {"operation": "read", "resource": "product", "field": None, "risk": "low", "steps": ["product_selection"]},
    "inspection": {"operation": "read", "resource": "mixed", "field": None, "risk": "low", "steps": ["inspection"]},
    "customer_service": {"operation": "write", "resource": "message", "field": "message", "risk": "medium", "steps": ["customer_service"]},
    "daily_report": {"operation": "read", "resource": "report", "field": None, "risk": "low", "steps": ["daily_report"]},
}

HIGH_RISK_TYPES = {"price_adjust", "auto_delist"}
API_HEAVY_TYPES = {"auto_listing", "inventory_sync", "price_adjust", "auto_delist", "supplier_switch"}
STRATEGY_KEYS = {
    "profit_margin_min",
    "profit_margin",
    "margin_threshold",
    "max_items",
    "discount_percent",
    "price_discount_percent",
    "min_profit_protection",
    "frequency_limit",
    "product_scope",
    "order_scope",
    "fields",
    "filters",
}


@dataclass
class NormalizedTask:
    raw: Dict[str, Any]
    task_id: str
    source: str
    name: str
    canonical_type: str
    shop_ids: Set[str]
    platforms: Set[str]
    all_shops: bool
    schedule_key: str
    interval_minutes: Optional[int]
    time_points: Tuple[str, ...]
    strategy_key: str
    strategy: Dict[str, Any]
    operation: str
    resource: str
    field: Optional[str]
    risk: str
    steps: Set[str]
    status: str


def as_list(value: Any) -> List[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, tuple):
        return list(value)
    if isinstance(value, set):
        return list(value)
    return [value]


def stringify(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return str(value)


def text_blob(task: Dict[str, Any]) -> str:
    parts = []
    for key in ("canonical_task_type", "task_type", "type", "name", "task_name", "title", "description", "content", "prompt", "intent"):
        if key in task:
            parts.append(stringify(task.get(key)))
    return " ".join(parts).lower()


def canonicalize_type(task: Dict[str, Any]) -> str:
    direct = stringify(task.get("canonical_task_type") or task.get("canonical_type") or task.get("task_type") or task.get("type")).lower()
    for canonical, aliases in CANONICAL_ALIASES.items():
        if direct == canonical:
            return canonical
        if any(direct == alias.lower() for alias in aliases):
            return canonical

    blob = text_blob(task)
    for canonical, aliases in CANONICAL_ALIASES.items():
        for alias in aliases:
            if alias.lower() in blob:
                return canonical
    return direct or "unknown"


def shops_by_id(user_context: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    result: Dict[str, Dict[str, Any]] = {}
    for shop in as_list(user_context.get("shops") or user_context.get("bound_shops")):
        if isinstance(shop, dict):
            shop_id = stringify(shop.get("shop_id") or shop.get("id") or shop.get("shopCode") or shop.get("shop_code"))
            if shop_id:
                result[shop_id] = shop
    return result


def normalize_shop_ids(task: Dict[str, Any], user_context: Dict[str, Any]) -> Tuple[Set[str], bool]:
    all_shops = bool(task.get("all_shops") or task.get("shop_scope") == "all" or task.get("scope") == "all_shops")
    known_shops = shops_by_id(user_context)
    if all_shops and known_shops:
        return set(known_shops), True

    shop_ids: Set[str] = set()
    for key in ("shop_id", "shop_code", "shopCode"):
        if task.get(key):
            shop_ids.add(stringify(task.get(key)))
    for item in as_list(task.get("shop_ids") or task.get("shop_codes") or task.get("shopCodes")):
        if item:
            shop_ids.add(stringify(item))
    for shop in as_list(task.get("shops")):
        if isinstance(shop, dict):
            shop_id = shop.get("shop_id") or shop.get("id") or shop.get("shopCode") or shop.get("shop_code")
            if shop_id:
                shop_ids.add(stringify(shop_id))
        elif shop:
            shop_ids.add(stringify(shop))
    return shop_ids, all_shops


def normalize_platforms(task: Dict[str, Any], shop_ids: Set[str], user_context: Dict[str, Any]) -> Set[str]:
    platforms: Set[str] = set()
    for key in ("platform", "platform_id", "platform_code"):
        if task.get(key):
            platforms.add(stringify(task.get(key)).lower())
    for item in as_list(task.get("platforms") or task.get("platform_ids")):
        if item:
            platforms.add(stringify(item).lower())

    known_shops = shops_by_id(user_context)
    for shop_id in shop_ids:
        shop = known_shops.get(shop_id)
        if shop:
            platform = shop.get("platform") or shop.get("platform_id") or shop.get("platform_code")
            if platform:
                platforms.add(stringify(platform).lower())
    return platforms


def parse_time_point(value: Any) -> List[str]:
    text = stringify(value)
    if not text:
        return []
    results: List[str] = []
    for match in re.finditer(r"(\d{1,2})[:：](\d{1,2})", text):
        hour = int(match.group(1))
        minute = int(match.group(2))
        if 0 <= hour <= 23 and 0 <= minute <= 59:
            results.append(f"{hour:02d}:{minute:02d}")
    for match in re.finditer(r"(上午|早上|下午|晚上|中午)?\s*(\d{1,2})\s*点(?:\s*(\d{1,2})\s*分)?", text):
        prefix = match.group(1) or ""
        hour = int(match.group(2))
        minute = int(match.group(3) or 0)
        if prefix in ("下午", "晚上") and hour < 12:
            hour += 12
        if prefix == "中午" and hour < 11:
            hour += 12
        if 0 <= hour <= 23 and 0 <= minute <= 59:
            results.append(f"{hour:02d}:{minute:02d}")
    return sorted(set(results))


def interval_from_frequency(value: Any, blob: str) -> Optional[int]:
    if value is None:
        value = ""
    text = stringify(value).lower()
    combined = f"{text} {blob}".lower()

    direct_match = re.search(r"(?:every|每)\s*(\d+)\s*(?:min|minute|minutes|分钟)", combined)
    if direct_match:
        return int(direct_match.group(1))
    hour_match = re.search(r"(?:every|每)\s*(\d+)\s*(?:hour|hours|小时)", combined)
    if hour_match:
        return int(hour_match.group(1)) * 60
    if any(token in combined for token in ("hourly", "每小时", "每个小时")):
        return 60
    if any(token in combined for token in ("daily", "每天", "每日")):
        return 1440
    if any(token in combined for token in ("weekly", "每周")):
        return 10080
    if any(token in combined for token in ("monthly", "每月")):
        return 43200
    return None


def normalize_schedule(task: Dict[str, Any]) -> Tuple[str, Optional[int], Tuple[str, ...]]:
    schedule = task.get("schedule") if isinstance(task.get("schedule"), dict) else {}
    interval = task.get("interval_minutes") or schedule.get("interval_minutes")
    if interval is not None:
        try:
            interval_minutes = int(interval)
        except (TypeError, ValueError):
            interval_minutes = None
    else:
        blob = text_blob(task)
        interval_minutes = interval_from_frequency(
            task.get("frequency") or schedule.get("frequency") or task.get("freq") or schedule.get("freq"),
            blob,
        )

    time_values: List[Any] = []
    for key in ("execution_time", "time", "times", "at", "start_time"):
        if key in task:
            time_values.extend(as_list(task.get(key)))
        if key in schedule:
            time_values.extend(as_list(schedule.get(key)))
    time_values.append(text_blob(task))

    time_points: List[str] = []
    for value in time_values:
        time_points.extend(parse_time_point(value))
    time_tuple = tuple(sorted(set(time_points)))

    cron = stringify(task.get("cron") or schedule.get("cron"))
    if cron:
        key = f"cron:{cron}"
    else:
        key = f"interval:{interval_minutes or 'unknown'}|times:{','.join(time_tuple) or 'unknown'}"
    return key, interval_minutes, time_tuple


def normalize_strategy(task: Dict[str, Any]) -> Tuple[Dict[str, Any], str]:
    strategy: Dict[str, Any] = {}
    for key in ("strategy", "params", "parameters", "filters"):
        value = task.get(key)
        if isinstance(value, dict):
            strategy.update(value)
    for key in STRATEGY_KEYS:
        if key in task:
            strategy[key] = task[key]
    clean = {k: strategy[k] for k in sorted(strategy) if strategy[k] not in (None, "", [])}
    key = json.dumps(clean, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return clean, key


def normalize_task(task: Dict[str, Any], user_context: Dict[str, Any]) -> NormalizedTask:
    canonical = canonicalize_type(task)
    shop_ids, all_shops = normalize_shop_ids(task, user_context)
    platforms = normalize_platforms(task, shop_ids, user_context)
    schedule_key, interval_minutes, time_points = normalize_schedule(task)
    strategy, strategy_key = normalize_strategy(task)
    traits = TASK_TRAITS.get(canonical, {"operation": "unknown", "resource": "unknown", "field": None, "risk": "unknown", "steps": [canonical]})
    source = stringify(task.get("source") or task.get("created_by") or "unknown").lower()
    name = stringify(task.get("name") or task.get("task_name") or task.get("title") or canonical)
    steps = set(as_list(task.get("workflow_steps") or traits.get("steps") or [canonical]))

    return NormalizedTask(
        raw=task,
        task_id=stringify(task.get("task_id") or task.get("id") or ""),
        source=source,
        name=name,
        canonical_type=canonical,
        shop_ids=shop_ids,
        platforms=platforms,
        all_shops=all_shops,
        schedule_key=schedule_key,
        interval_minutes=interval_minutes,
        time_points=time_points,
        strategy_key=strategy_key,
        strategy=strategy,
        operation=stringify(traits.get("operation")),
        resource=stringify(traits.get("resource")),
        field=traits.get("field"),
        risk=stringify(traits.get("risk")),
        steps=steps,
        status=stringify(task.get("status") or "active").lower(),
    )


def overlap(a: Set[str], b: Set[str]) -> bool:
    return bool(a and b and (a & b))


def same_scope(a: NormalizedTask, b: NormalizedTask) -> bool:
    return a.shop_ids == b.shop_ids and a.platforms == b.platforms


def same_goal(a: NormalizedTask, b: NormalizedTask) -> bool:
    return a.canonical_type == b.canonical_type


def strategy_impact_sentence(proposed: NormalizedTask, existing: NormalizedTask) -> str:
    if proposed.canonical_type == "auto_listing":
        return "策略变化可能扩大或缩小铺货范围。"
    if proposed.canonical_type == "price_adjust":
        return "策略变化可能影响商品价格和利润保护。"
    if proposed.canonical_type == "inventory_sync":
        return "策略变化可能影响同步范围和平台接口调用量。"
    return "策略变化会改变任务命中的对象或执行方式。"


def summary(task: NormalizedTask) -> str:
    shops = ",".join(sorted(task.shop_ids)) if task.shop_ids else "未指定店铺"
    platforms = ",".join(sorted(task.platforms)) if task.platforms else "未指定平台"
    times = ",".join(task.time_points) if task.time_points else "未指定时间"
    interval = f"每{task.interval_minutes}分钟" if task.interval_minutes and task.interval_minutes < 1440 else task.schedule_key
    return f"{task.name}｜{task.canonical_type}｜店铺:{shops}｜平台:{platforms}｜{interval}｜时间:{times}"


def finding(code: str, severity: str, decision: str, message: str, **extra: Any) -> Dict[str, Any]:
    result = {"code": code, "severity": severity, "decision": decision, "message": message}
    result.update(extra)
    return result


def active_existing_tasks(tasks: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    excluded = {"deleted", "terminated", "finished", "completed", "history", "archived"}
    active = []
    for task in tasks:
        status = stringify(task.get("status") or "active").lower()
        if status not in excluded:
            active.append(task)
    return active


def platform_capability_supported(platform: str, canonical_type: str, user_context: Dict[str, Any]) -> Optional[bool]:
    capabilities = user_context.get("platform_capabilities") or user_context.get("capabilities") or {}
    if not isinstance(capabilities, dict) or platform not in capabilities:
        return None
    allowed = capabilities.get(platform)
    if isinstance(allowed, dict):
        if canonical_type in allowed:
            return bool(allowed[canonical_type])
        aliases = set(CANONICAL_ALIASES.get(canonical_type, ()))
        return any(bool(allowed.get(alias)) for alias in aliases)
    allowed_values = {stringify(x).lower() for x in as_list(allowed)}
    aliases = {alias.lower() for alias in CANONICAL_ALIASES.get(canonical_type, ())}
    return canonical_type.lower() in allowed_values or bool(aliases & allowed_values)


def requires_sv_permission(task: NormalizedTask) -> bool:
    raw = task.raw
    explicit = (
        raw.get("requires_sv_paid")
        or raw.get("requires_sv_advanced_permission")
        or raw.get("requires_paid_shop")
        or raw.get("requires_advanced_permission")
    )
    if explicit is not None:
        return bool(explicit)

    entitlement_text = stringify(raw.get("entitlement_required") or raw.get("membership_required")).lower()
    if any(token in entitlement_text for token in ("isv", "sv", "高级", "advanced", "paid_shop", "paid")):
        return True
    return False


def shop_has_sv_permission(shop: Dict[str, Any]) -> Tuple[Optional[bool], str]:
    status = stringify(shop.get("create_permission_status") or shop.get("sv_permission_status")).lower()
    if status == "ok":
        return True, status
    if status in {
        "sv_not_paid",
        "shop_not_found_or_param_error",
        "paid_status_api_error",
        "paid_status_unknown_error",
        "paid_status_missing",
    }:
        return False, status

    for key in ("has_sv_advanced_permission", "sv_is_paid", "is_paid", "isPaid", "paid"):
        if key in shop:
            value = shop.get(key)
            if isinstance(value, bool):
                return value, "ok" if value else "sv_not_paid"
            value_text = stringify(value).lower()
            if value_text in {"true", "1", "yes", "paid"}:
                return True, "ok"
            if value_text in {"false", "0", "no", "free", "unpaid"}:
                return False, "sv_not_paid"
    return None, "paid_status_missing"


def detect_boundaries(proposed: NormalizedTask, user_context: Dict[str, Any]) -> List[Dict[str, Any]]:
    findings: List[Dict[str, Any]] = []
    known_shops = shops_by_id(user_context)

    if not proposed.shop_ids and not known_shops:
        findings.append(finding(
            "no_bound_shop",
            "blocker",
            "block",
            "用户当前没有可用店铺，不能创建定时任务。需要先绑定或开店。",
            prompt_required=True,
        ))
        return findings

    if not proposed.shop_ids and len(known_shops) == 1:
        shop_id = next(iter(known_shops))
        proposed.shop_ids.add(shop_id)
        proposed.platforms.update(normalize_platforms(proposed.raw, proposed.shop_ids, user_context))

    if not proposed.shop_ids and len(known_shops) > 1:
        findings.append(finding(
            "shop_scope_missing",
            "confirm",
            "ask_confirmation",
            "用户有多个店铺，但本次任务没有明确店铺范围。需要先让用户选择全部店铺、平台子集或指定店铺。",
            prompt_required=True,
        ))

    unbound_shops: List[str] = []
    invalid_shops: List[str] = []
    valid_shops: List[str] = []
    for shop_id in proposed.shop_ids:
        shop = known_shops.get(shop_id)
        if not shop:
            unbound_shops.append(shop_id)
            continue
        permission_status = stringify(shop.get("create_permission_status") or shop.get("permission_status")).lower()
        if permission_status == "not_bound":
            unbound_shops.append(shop_id)
            continue
        if permission_status == "authorization_invalid":
            invalid_shops.append(shop_id)
            continue
        auth_value = shop.get("authorized", shop.get("is_authorized", shop.get("auth_status", True)))
        invalid = auth_value is False or stringify(auth_value).lower() in {"false", "0", "expired", "invalid", "unauthorized", "失效"}
        if invalid:
            invalid_shops.append(shop_id)
        else:
            valid_shops.append(shop_id)
    if unbound_shops:
        decision = "partial_create" if valid_shops else "block"
        findings.append(finding(
            "shop_not_bound",
            "blocker",
            decision,
            f"以下目标店铺未绑定，不能执行该任务：{', '.join(sorted(unbound_shops))}。",
            prompt_required=True,
            unbound_shops=sorted(unbound_shops),
            valid_shops=sorted(valid_shops),
        ))
    if invalid_shops:
        decision = "partial_create" if valid_shops else "block"
        findings.append(finding(
            "authorization_invalid",
            "blocker",
            decision,
            f"以下店铺授权失效，不能执行该任务：{', '.join(sorted(invalid_shops))}。",
            prompt_required=True,
            invalid_shops=sorted(invalid_shops),
            valid_shops=sorted(valid_shops),
        ))

    unsupported: List[str] = []
    supported: List[str] = []
    for platform in proposed.platforms:
        support = platform_capability_supported(platform, proposed.canonical_type, user_context)
        if support is False:
            unsupported.append(platform)
        elif support is True:
            supported.append(platform)
    if unsupported:
        decision = "partial_create" if supported else "block"
        findings.append(finding(
            "platform_capability_missing",
            "blocker",
            decision,
            f"部分平台暂不支持 {proposed.canonical_type}：{', '.join(sorted(unsupported))}。",
            prompt_required=True,
            unsupported_platforms=sorted(unsupported),
            supported_platforms=sorted(supported),
        ))

    entitlement_required = proposed.raw.get("entitlement_required") or proposed.raw.get("membership_required")
    membership = user_context.get("membership") or user_context.get("entitlements") or {}
    if entitlement_required and not requires_sv_permission(proposed):
        entitlement = stringify(entitlement_required)
        has_entitlement = bool(membership.get(entitlement)) if isinstance(membership, dict) else False
        if not has_entitlement:
            findings.append(finding(
                "entitlement_missing",
                "blocker",
                "block",
                f"该任务需要 {entitlement} 权益，当前账号不满足，不能进入执行队列。",
                prompt_required=True,
            ))

    if requires_sv_permission(proposed):
        missing_sv: List[str] = []
        valid_sv: List[str] = []
        unknown_sv: List[str] = []
        for shop_id in proposed.shop_ids:
            shop = known_shops.get(shop_id, {})
            has_permission, status = shop_has_sv_permission(shop)
            if has_permission is True:
                valid_sv.append(shop_id)
            elif status == "paid_status_missing":
                unknown_sv.append(shop_id)
            else:
                missing_sv.append(shop_id)
        if missing_sv or unknown_sv:
            invalid = missing_sv + unknown_sv
            decision = "partial_create" if valid_sv else "block"
            findings.append(finding(
                "sv_advanced_permission_missing",
                "blocker",
                decision,
                "部分店铺缺少 ISV 高级版权限或暂时无法完成 ISV 权限校验，不能直接创建高级版任务。",
                prompt_required=True,
                invalid_shops=sorted(invalid),
                valid_shops=sorted(valid_sv),
                missing_sv_shops=sorted(missing_sv),
                unknown_sv_status_shops=sorted(unknown_sv),
            ))

    notify = proposed.raw.get("notify") or proposed.raw.get("notification") or {}
    if isinstance(notify, dict) and notify.get("wechat"):
        wechat_bound = bool(user_context.get("wechat_bound") or user_context.get("enterprise_wechat_bound"))
        if not wechat_bound:
            findings.append(finding(
                "wechat_not_bound",
                "warning",
                "warn_then_proceed",
                "用户要求微信通知，但当前未绑定企业微信好友；任务可创建，结果需要回退到任务中心或 App Push。",
                prompt_required=False,
            ))

    return findings


def detect_duplicates_and_conflicts(proposed: NormalizedTask, existing_tasks: List[NormalizedTask]) -> List[Dict[str, Any]]:
    findings: List[Dict[str, Any]] = []

    for existing in existing_tasks:
        if not same_goal(proposed, existing):
            continue
        scope_same_or_overlap = same_scope(proposed, existing) or overlap(proposed.shop_ids, existing.shop_ids)
        if not scope_same_or_overlap:
            continue

        if proposed.schedule_key == existing.schedule_key and proposed.strategy_key == existing.strategy_key:
            findings.append(finding(
                "complete_duplicate",
                "silent",
                "reuse_or_update",
                "发现完全重复任务，复用或更新原任务，不新增。",
                prompt_required=False,
                existing_task_id=existing.task_id,
            ))
            return findings

        if proposed.canonical_type in HIGH_RISK_TYPES or existing.canonical_type in HIGH_RISK_TYPES:
            findings.append(finding(
                "high_risk_duplicate",
                "confirm",
                "ask_confirmation",
                "该任务与已有高风险写任务可能命中同一商品或订单，不能静默合并。",
                prompt_required=True,
                existing_task_id=existing.task_id,
                existing_summary=summary(existing),
                proposed_summary=summary(proposed),
            ))
            return findings

        if proposed.strategy_key != existing.strategy_key:
            findings.append(finding(
                "strategy_partial_duplicate",
                "confirm",
                "ask_confirmation",
                strategy_impact_sentence(proposed, existing),
                prompt_required=True,
                existing_task_id=existing.task_id,
                existing_summary=summary(existing),
                proposed_summary=summary(proposed),
            ))
            return findings

        findings.append(finding(
            "semantic_duplicate",
            "silent",
            "reuse_or_update",
            "发现 LUI 配置与已有任务语义重复，复用原任务。",
            prompt_required=False,
            existing_task_id=existing.task_id,
        ))
        return findings

    for existing in existing_tasks:
        if proposed.shop_ids and existing.shop_ids and not overlap(proposed.shop_ids, existing.shop_ids):
            continue
        if proposed.steps > existing.steps or existing.steps > proposed.steps:
            findings.append(finding(
                "process_duplicate",
                "silent",
                "silent_merge",
                "发现流程前置动作重复，可静默合并已覆盖的前置步骤。",
                prompt_required=False,
                existing_task_id=existing.task_id,
            ))
            return findings

    for existing in existing_tasks:
        same_window = bool(set(proposed.time_points) & set(existing.time_points)) if proposed.time_points and existing.time_points else proposed.schedule_key == existing.schedule_key

        if proposed.platforms and existing.platforms and overlap(proposed.platforms, existing.platforms) and same_window:
            if proposed.canonical_type in API_HEAVY_TYPES or existing.canonical_type in API_HEAVY_TYPES:
                findings.append(finding(
                    "same_platform_rate_limit",
                    "info",
                    "proceed",
                    "同平台 API 密集型任务可能触发平台级排队，任务中心可展示排队中。",
                    prompt_required=False,
                    existing_task_id=existing.task_id,
                ))

        if proposed.shop_ids and existing.shop_ids and overlap(proposed.shop_ids, existing.shop_ids) and same_window:
            if proposed.operation == "write" and existing.operation == "write" and proposed.resource == existing.resource == "product":
                code = "product_field_overlap" if proposed.field == existing.field else "same_shop_batch_write"
                message = "同商品字段写入需要串行并基于最新状态重判。" if code == "product_field_overlap" else "同店铺批量写任务可能进入店铺级排队。"
                findings.append(finding(
                    code,
                    "info",
                    "proceed",
                    message,
                    prompt_required=False,
                    existing_task_id=existing.task_id,
                ))
            if proposed.operation == "write" and existing.operation == "write" and proposed.resource == existing.resource == "order":
                findings.append(finding(
                    "same_order_handling",
                    "info",
                    "proceed",
                    "同订单处理需要订单级串行，避免重复催发或重复备注。",
                    prompt_required=False,
                    existing_task_id=existing.task_id,
                ))

    if proposed.interval_minutes is not None and proposed.interval_minutes <= 10:
        findings.append(finding(
            "high_frequency_accumulation",
            "warning",
            "warn_then_proceed",
            "当前频次较高，可能导致上一轮未完成时下一轮已排队；建议降频到每30分钟或更低频。",
            prompt_required=True,
            recommended_frequency="每30分钟",
        ))

    return findings


def choose_decision(findings: List[Dict[str, Any]]) -> str:
    priority = {
        "block": 0,
        "partial_create": 1,
        "ask_confirmation": 2,
        "reuse_or_update": 3,
        "silent_merge": 4,
        "warn_then_proceed": 5,
        "proceed": 6,
    }
    if not findings:
        return "proceed"
    return min((f["decision"] for f in findings), key=lambda d: priority.get(d, 99))


def prompt_from_finding(proposed: NormalizedTask, finding_item: Dict[str, Any]) -> str:
    code = finding_item["code"]
    if code == "strategy_partial_duplicate":
        return (
            "检测到相似定时任务。\n\n"
            f"已有任务：{finding_item.get('existing_summary')}\n"
            f"本次任务：{finding_item.get('proposed_summary')}\n\n"
            f"两个任务目标相同，但策略参数不同。{finding_item['message']}\n\n"
            "你可以回复：\n"
            "1. 修改原任务\n"
            "2. 仍然新建一个任务\n"
            "3. 取消本次创建\n\n"
            "默认建议：修改原任务。"
        )
    if code == "high_risk_duplicate":
        return (
            "该任务存在高风险重复，暂时不会直接创建。\n\n"
            f"已有任务：{finding_item.get('existing_summary')}\n"
            f"本次任务：{finding_item.get('proposed_summary')}\n\n"
            "风险：同一商品或订单可能被重复写入，导致价格、上下架状态、发货或订单处理结果被重复影响。\n\n"
            "你可以回复：\n"
            "1. 合并为一个任务，并设置保护规则\n"
            "2. 保留两个任务，但开启同一对象每日只允许执行一次的保护\n"
            "3. 取消本次创建\n\n"
            "默认建议：合并任务。"
        )
    if code == "high_frequency_accumulation":
        return (
            "当前频次可能导致任务堆积。\n\n"
            f"{summary(proposed)}\n\n"
            "风险：上一轮任务可能尚未完成，下一轮已开始排队，导致延迟、失败率上升或平台限流。\n\n"
            "你可以回复：\n"
            f"1. 按推荐频次创建：{finding_item.get('recommended_frequency', '每30分钟')}\n"
            "2. 仍按当前频次创建，接受排队风险\n"
            "3. 取消本次创建"
        )
    if code == "shop_scope_missing":
        return (
            "请先选择定时任务的店铺范围。\n\n"
            "你当前有多个店铺，本次任务没有明确要在哪些店铺执行。\n\n"
            "你可以回复：\n"
            "1. 全部店铺都开启\n"
            "2. 只开启某个平台的店铺\n"
            "3. 指定店铺编号\n"
            "4. 取消本次创建"
        )
    if code == "no_bound_shop":
        return (
            "当前没有可用店铺，因此不能创建定时任务。\n\n"
            "你可以回复：\n"
            "1. 去绑定店铺\n"
            "2. 先了解支持哪些定时任务\n"
            "3. 取消本次创建"
        )
    if code == "sv_advanced_permission_missing":
        invalid = "、".join(finding_item.get("invalid_shops", [])) or "部分店铺"
        valid = "、".join(finding_item.get("valid_shops", []))
        valid_line = f"\n可继续的店铺：{valid}\n" if valid else ""
        valid_option = "2. 只为已有 ISV 权限的店铺创建\n" if valid else ""
        downgrade_index = "3" if valid else "2"
        cancel_index = "4" if valid else "3"
        return (
            "这个高级版定时任务暂时不能直接创建。\n\n"
            f"原因：{invalid} 未开通 ISV 高级版，或系统暂时无法完成 ISV 权限校验。"
            f"{valid_line}\n"
            "你可以回复：\n"
            "1. 去开通 ISV 高级版后继续创建\n"
            f"{valid_option}"
            f"{downgrade_index}. 改成普通/低频任务\n"
            f"{cancel_index}. 取消本次创建"
        )
    return finding_item["message"]


def evaluate(payload: Dict[str, Any]) -> Dict[str, Any]:
    user_context = payload.get("user_context") or {}
    proposed_raw = payload.get("proposed_task") or {}
    existing_raw = active_existing_tasks(payload.get("existing_tasks") or [])

    proposed = normalize_task(proposed_raw, user_context)
    existing = [normalize_task(task, user_context) for task in existing_raw]

    findings = detect_boundaries(proposed, user_context)
    hard_boundary = any(f["decision"] in {"block", "partial_create"} for f in findings)
    if not hard_boundary:
        findings.extend(detect_duplicates_and_conflicts(proposed, existing))

    decision = choose_decision(findings)
    prompt_required = any(bool(f.get("prompt_required")) for f in findings if f["decision"] in {"block", "partial_create", "ask_confirmation", "warn_then_proceed"})
    primary = next((f for f in findings if f["decision"] == decision), findings[0] if findings else None)

    result = {
        "decision": decision,
        "prompt_required": prompt_required,
        "normalized_proposed_task": {
            "task_id": proposed.task_id,
            "source": proposed.source,
            "name": proposed.name,
            "canonical_type": proposed.canonical_type,
            "shop_ids": sorted(proposed.shop_ids),
            "platforms": sorted(proposed.platforms),
            "schedule_key": proposed.schedule_key,
            "interval_minutes": proposed.interval_minutes,
            "time_points": list(proposed.time_points),
            "strategy": proposed.strategy,
            "operation": proposed.operation,
            "resource": proposed.resource,
            "field": proposed.field,
            "risk": proposed.risk,
            "steps": sorted(proposed.steps),
        },
        "findings": findings,
        "user_prompt": prompt_from_finding(proposed, primary) if primary and prompt_required else "",
    }
    return result


def render_markdown(result: Dict[str, Any]) -> str:
    task = result["normalized_proposed_task"]
    lines = [
        f"决策：`{result['decision']}`",
        f"是否需要用户确认：{'是' if result['prompt_required'] else '否'}",
        "",
        "标准化任务：",
        f"- 类型：`{task['canonical_type']}`",
        f"- 店铺：{', '.join(task['shop_ids']) or '未指定'}",
        f"- 平台：{', '.join(task['platforms']) or '未指定'}",
        f"- 频次：{task['schedule_key']}",
        "",
        "检测结果：",
    ]
    if result["findings"]:
        for item in result["findings"]:
            lines.append(f"- `{item['code']}` / `{item['decision']}`：{item['message']}")
    else:
        lines.append("- 未发现重复、冲突或阻断边界。")
    if result.get("user_prompt"):
        lines.extend(["", "建议对用户展示：", "", result["user_prompt"]])
    return "\n".join(lines)


def read_payload(path: str) -> Dict[str, Any]:
    if path == "-":
        return json.load(sys.stdin)
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def main() -> int:
    parser = argparse.ArgumentParser(description="检测 LUI 定时任务的重复、冲突和边界条件。")
    parser.add_argument("input", help="输入 JSON 文件路径；传 '-' 表示从标准输入读取。")
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    parser.add_argument("--json", action="store_true", help="等价于 --format json，便于 Agent/CI 组合调用。")
    parser.add_argument("--markdown", action="store_true", help="等价于 --format markdown，输出中文可读报告。")
    args = parser.parse_args()

    output_format = args.format
    if args.json:
        output_format = "json"
    if args.markdown:
        output_format = "markdown"

    try:
        payload = read_payload(args.input)
        result = evaluate(payload)
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        track_event("invalid_input", {"error_type": type(exc).__name__})
        print(json.dumps({
            "error": "invalid_input",
            "message": str(exc),
        }, ensure_ascii=False, indent=2), file=sys.stderr)
        return 2

    track_event("evaluated", {
        "decision": result.get("decision"),
        "prompt_required": bool(result.get("prompt_required")),
        "finding_count": len(result.get("findings") or []),
    })

    if output_format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
