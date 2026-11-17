from __future__ import annotations

import calendar
import json
from copy import deepcopy
from datetime import date, datetime
from typing import Any


SUPPORTED_DATA_SOURCES = {
    "project",
    "purchase_intention",
    "expiring_project",
    "enterprise",
}
SUPPORTED_ACTIONS = {"search", "refine"}
SUPPORTED_OPERATORS = {"AND", "OR", "NOT"}
SUPPORTED_SOURCES = {"user_explicit", "api_default", "agent_derived"}
MATCH_SCOPE_TERMS = (
    (2, ("标题", "项目名", "项目名称", "完整名称")),
    (3, ("项目编号", "项目ID", "项目 ID", "项目id", "项目 id", "编号")),
    (7, ("联系人", "联系电话", "手机号", "电话")),
    (8, ("正文", "全文")),
    (10, ("附件",)),
)
COMMAND_BY_ROUTE = {
    ("project", "search"): "search",
    ("purchase_intention", "search"): "search-purchase",
    ("expiring_project", "search"): "search-expiring",
    ("enterprise", "search"): "enterprise",
    ("project", "refine"): "refine",
    ("purchase_intention", "refine"): "refine",
    ("expiring_project", "refine"): "refine",
}
CONDITION_FIELDS = {
    "keyword": {
        "project": {"keywords"},
        "purchase_intention": {"keywords"},
        "expiring_project": {"keywords"},
    },
    "exclude_words": {
        "project": {"excludeWords"},
        "purchase_intention": {"excludeWords"},
        "expiring_project": {"excludeWords"},
    },
    "area": {
        "project": {"areaIds"},
        "purchase_intention": {"areaIds"},
        "expiring_project": {"areaIds"},
    },
    "publish_time": {
        "project": {"beginTime", "endTime"},
        "purchase_intention": {"beginTime", "endTime"},
    },
    "planned_purchase_date": {
        "purchase_intention": {"startPlanPurchaseDate", "endPlanPurchaseDate"},
    },
    "service_expiry": {
        "expiring_project": {"beginServiceExpireTime", "endServiceExpireTime"},
    },
    "amount_min": {
        "project": {"beginAmount"},
        "purchase_intention": {"startPlanPurchaseAmount"},
        "expiring_project": {"beginContractAmount"},
    },
    "amount_max": {
        "project": {"endAmount"},
        "purchase_intention": {"endPlanPurchaseAmount"},
        "expiring_project": {"endContractAmount"},
    },
    "amount_range": {
        "project": {"beginAmount", "endAmount"},
        "purchase_intention": {"startPlanPurchaseAmount", "endPlanPurchaseAmount"},
        "expiring_project": {"beginContractAmount", "endContractAmount"},
    },
    "planned_amount_min": {"purchase_intention": {"startPlanPurchaseAmount"}},
    "planned_amount_max": {"purchase_intention": {"endPlanPurchaseAmount"}},
    "planned_amount_range": {
        "purchase_intention": {"startPlanPurchaseAmount", "endPlanPurchaseAmount"}
    },
    "contract_amount_min": {"expiring_project": {"beginContractAmount"}},
    "contract_amount_max": {"expiring_project": {"endContractAmount"}},
    "contract_amount_range": {
        "expiring_project": {"beginContractAmount", "endContractAmount"}
    },
    "stage": {"project": {"infoTypes"}},
    "organization_type": {
        "project": {"purchasingUnitTypes"},
        "purchase_intention": {"purchasingUnitTypes"},
        "expiring_project": {"purchasingUnitTypes"},
    },
    "organization_role": {"project": {"keywords", "infoTypes"}},
    "procurement_method": {
        "project": {"procurementMethod"},
        "expiring_project": {"procurementMethod"},
    },
    "match_scope": {
        "project": {"matchScopes"},
        "purchase_intention": {"matchScopes"},
        "expiring_project": {"matchScopes"},
    },
    "project_title": {
        "project": {"keywords", "matchScopes"},
        "purchase_intention": {"keywords", "matchScopes"},
        "expiring_project": {"keywords", "matchScopes"},
    },
    "project_id": {
        "project": {"keywords", "matchScopes"},
        "expiring_project": {"keywords", "matchScopes"},
    },
    "company_name": {"enterprise": {"companyName"}},
    "enterprise_time": {"enterprise": {"beginTime", "endTime"}},
    "phone_type": {"enterprise": {"phoneType"}},
    "contract_period": {"expiring_project": {"contractPeriodType"}},
    "sort": {
        "project": {"sortType"},
        "purchase_intention": {"sortType"},
        "expiring_project": {"sortType"},
        "enterprise": {"sortType"},
    },
    "quantity": {
        "project": {"numPerPage"},
        "purchase_intention": {"numPerPage"},
        "expiring_project": {"numPerPage"},
        "enterprise": {"currentPage", "numPerPage"},
    },
    "preserve_area": {
        "project": set(),
        "purchase_intention": set(),
        "expiring_project": set(),
    },
}
REQUIRED_CONDITION_FIELDS = {
    "keyword": {
        "project": {"keywords"},
        "purchase_intention": {"keywords"},
        "expiring_project": {"keywords"},
    },
    "exclude_words": {
        "project": {"excludeWords"},
        "purchase_intention": {"excludeWords"},
        "expiring_project": {"excludeWords"},
    },
    "area": {
        "project": {"areaIds"},
        "purchase_intention": {"areaIds"},
        "expiring_project": {"areaIds"},
    },
    "planned_purchase_date": {
        "purchase_intention": {"startPlanPurchaseDate", "endPlanPurchaseDate"}
    },
    "service_expiry": {
        "expiring_project": {"beginServiceExpireTime", "endServiceExpireTime"}
    },
    "amount_min": {
        "project": {"beginAmount"},
        "purchase_intention": {"startPlanPurchaseAmount"},
        "expiring_project": {"beginContractAmount"},
    },
    "amount_max": {
        "project": {"endAmount"},
        "purchase_intention": {"endPlanPurchaseAmount"},
        "expiring_project": {"endContractAmount"},
    },
    "amount_range": {
        "project": {"beginAmount", "endAmount"},
        "purchase_intention": {"startPlanPurchaseAmount", "endPlanPurchaseAmount"},
        "expiring_project": {"beginContractAmount", "endContractAmount"},
    },
    "planned_amount_min": {"purchase_intention": {"startPlanPurchaseAmount"}},
    "planned_amount_max": {"purchase_intention": {"endPlanPurchaseAmount"}},
    "planned_amount_range": {
        "purchase_intention": {"startPlanPurchaseAmount", "endPlanPurchaseAmount"}
    },
    "contract_amount_min": {"expiring_project": {"beginContractAmount"}},
    "contract_amount_max": {"expiring_project": {"endContractAmount"}},
    "contract_amount_range": {
        "expiring_project": {"beginContractAmount", "endContractAmount"}
    },
    "stage": {"project": {"infoTypes"}},
    "organization_type": {
        "project": {"purchasingUnitTypes"},
        "purchase_intention": {"purchasingUnitTypes"},
        "expiring_project": {"purchasingUnitTypes"},
    },
    "organization_role": {"project": {"keywords", "infoTypes"}},
    "procurement_method": {
        "project": {"procurementMethod"},
        "expiring_project": {"procurementMethod"},
    },
    "match_scope": {
        "project": {"matchScopes"},
        "purchase_intention": {"matchScopes"},
        "expiring_project": {"matchScopes"},
    },
    "project_title": {
        "project": {"keywords", "matchScopes"},
        "purchase_intention": {"keywords", "matchScopes"},
        "expiring_project": {"keywords", "matchScopes"},
    },
    "project_id": {
        "project": {"keywords", "matchScopes"},
        "expiring_project": {"keywords", "matchScopes"},
    },
    "company_name": {"enterprise": {"companyName"}},
    "enterprise_time": {"enterprise": {"beginTime", "endTime"}},
    "phone_type": {"enterprise": {"phoneType"}},
    "contract_period": {"expiring_project": {"contractPeriodType"}},
    "sort": {
        "project": {"sortType"},
        "purchase_intention": {"sortType"},
        "expiring_project": {"sortType"},
        "enterprise": {"sortType"},
    },
    "quantity": {
        "project": {"numPerPage"},
        "purchase_intention": {"numPerPage"},
        "expiring_project": {"numPerPage"},
        "enterprise": {"numPerPage"},
    },
}
# Project compiler fragments may still contain a legacy normalized keyword
# mapping; only the final emitted query uses the grouped API contract.
for _condition_type in ("keyword", "project_title", "project_id", "organization_role"):
    CONDITION_FIELDS[_condition_type]["project"].update({"keywordGroups", "matchScopes"})
    REQUIRED_CONDITION_FIELDS[_condition_type]["project"] = set()
CONDITION_FIELDS["keyword_group"] = {"project": {"keywordGroups"}}
REQUIRED_CONDITION_FIELDS["keyword_group"] = {"project": {"keywordGroups"}}
CONDITION_FIELDS["procurement_method"]["project"].add("procurementMethods")
REQUIRED_CONDITION_FIELDS["procurement_method"]["project"] = set()
PROJECT_LIST_FILTERS = {
    "procurement_category": "procurementCategories",
    "funds_source": "fundsSources",
}
PROJECT_BINARY_FILTERS = {
    "has_annex": "hasAnnex",
    "has_agency": "hasAgency",
    "registration_status": "registrationStatus",
    "has_bidding_phone": "hasBiddingPhone",
    "has_winning_phone": "hasWinningPhone",
}
for _condition_type, _field in {**PROJECT_LIST_FILTERS, **PROJECT_BINARY_FILTERS}.items():
    CONDITION_FIELDS[_condition_type] = {"project": {_field}}
    REQUIRED_CONDITION_FIELDS[_condition_type] = {"project": {_field}}

PROJECT_DEFAULT_SCOPES = {
    "keyword": [2, 9],
    "project_title": [2],
    "project_id": [8, 10],
}
PROJECT_CLEAR_FIELDS = {
    "area": ("areaIds",),
    "exclude_words": ("excludeWords",),
    "stage": ("infoTypes",),
    "organization_type": ("purchasingUnitTypes",),
    "procurement_method": ("procurementMethods",),
    **{kind: (field,) for kind, field in {**PROJECT_LIST_FILTERS, **PROJECT_BINARY_FILTERS}.items()},
    "amount_min": ("beginAmount",),
    "amount_max": ("endAmount",),
    "amount_range": ("beginAmount", "endAmount"),
    "sort": ("sortType",),
    "quantity": ("numPerPage",),
}

ENTERPRISE_KIND_FIELDS = {
    "partners": {"companyName", "beginTime", "endTime", "sortType"},
    "area-distribution": {"companyName", "beginTime", "endTime", "sortType"},
    "principals": {"companyName", "beginTime", "endTime", "sortType"},
    "winning-area-distribution": {"companyName", "beginTime", "endTime", "sortType"},
    "co-bidder-competitors": {"companyName", "beginTime", "endTime"},
    "potential-competitors": {"companyName", "beginTime", "endTime"},
    "business-info": {"companyName"},
    "contacts": {"companyName", "phoneType", "currentPage", "numPerPage"},
}
STAGE_VALUES = {
    "意见征集": {"1": [1]},
    "征求意见": {"1": [1]},
    "预告": {"1": [2]},
    "招标预告": {"1": [2]},
    "招标": {"0": [3, 4], "1": [2]},
    "招标项目": {"0": [3, 4], "1": [2]},
    "招标机会": {"0": [3, 4], "1": [2]},
    "公告": {"0": []},
    "招标公告": {"0": [3]},
    "重新招标": {"0": [4]},
    "变更": {"2": [5]},
    "答疑": {"2": [6]},
    "废标": {"3": [7]},
    "流标": {"3": [8]},
    "开标": {"3": [9]},
    "候选人": {"3": [10]},
    "中标": {"3": [11, 12]},
    "中标结果": {"3": [11, 12]},
    "成交结果": {"3": [11, 12]},
    "中标公告": {"3": [11, 12]},
    "结果公示": {"3": []},
    "中标通知": {"3": [11]},
    "合同": {"3": [12]},
    "合同公告": {"3": [12]},
}
ORGANIZATION_TYPE_VALUES = {
    "医院": 1,
    "医疗": 1,
    "医疗机构": 1,
    "政府": 2,
    "机关": 2,
    "学校": 3,
    "公安": 4,
    "金融企业": 5,
    "部队": 6,
    "通信运营商": 7,
}


class PlanValidationError(ValueError):
    def __init__(self, message: str, *, details: dict[str, Any] | None = None):
        super().__init__(message)
        self.details = details or {}


def _iso_date(value: Any, label: str) -> date:
    try:
        return date.fromisoformat(str(value))
    except ValueError as exc:
        raise PlanValidationError(f"{label}必须是 YYYY-MM-DD。") from exc


def _shift_months(value: date, months: int) -> date:
    month_index = value.year * 12 + value.month - 1 + months
    year, zero_based_month = divmod(month_index, 12)
    month = zero_based_month + 1
    day = min(value.day, calendar.monthrange(year, month)[1])
    return value.replace(year=year, month=month, day=day)


def _list_value(value: Any, label: str) -> list[Any]:
    if isinstance(value, list) and value:
        return value
    if isinstance(value, (str, int, float)) and str(value).strip():
        return [value]
    raise PlanValidationError(f"{label}必须是非空值或数组。")


def _explicit_match_scopes(user_text: str) -> list[int]:
    text = str(user_text or "")
    return [scope for scope, terms in MATCH_SCOPE_TERMS if any(term in text for term in terms)]


def sanitize_query_match_scopes(
    raw_query: dict[str, Any],
    user_text: str,
) -> dict[str, Any]:
    # Scopes may follow semantic role/title/identifier inference. A literal-word
    # check cannot establish that a supplied scope is unwanted.
    return deepcopy(raw_query)


def _sanitize_plan_match_scopes(
    raw_plan: dict[str, Any],
    user_text: str,
) -> dict[str, Any]:
    return deepcopy(raw_plan)


def _amount_fragment(condition_type: str, value: Any, source: str) -> dict[str, Any]:
    fields = {
        "project": ("beginAmount", "endAmount"),
        "purchase_intention": ("startPlanPurchaseAmount", "endPlanPurchaseAmount"),
        "expiring_project": ("beginContractAmount", "endContractAmount"),
    }[source]
    if condition_type.endswith("_min"):
        return {fields[0]: value}
    if condition_type.endswith("_max"):
        return {fields[1]: value}
    if not isinstance(value, list) or len(value) != 2:
        raise PlanValidationError("金额范围必须包含下限和上限。")
    return {fields[0]: value[0], fields[1]: value[1]}


def _relative_range(value: Any, current_date: Any, *, month_only: bool) -> tuple[str, str]:
    if isinstance(value, list) and len(value) == 2:
        start, end = str(value[0]), str(value[1])
    else:
        if not isinstance(value, dict):
            raise PlanValidationError("时间条件必须是起止值或相对时间对象。")
        if set(value) >= {"start", "end"}:
            start, end = str(value["start"]), str(value["end"])
        else:
            relative = str(value.get("relative") or "")
            count = value.get("count")
            if not isinstance(count, int) or count < 1:
                raise PlanValidationError("相对时间 count 必须是正整数。")
            today = _iso_date(current_date, "current_date")
            if relative == "past_months":
                start, end = _shift_months(today, -count), today
            elif relative == "future_months" and month_only:
                start = _shift_months(today.replace(day=1), 1)
                end = _shift_months(start, count - 1)
            elif relative == "future_months":
                start, end = today, _shift_months(today, count)
            else:
                raise PlanValidationError("相对时间类型不受支持。")
            start, end = (
                (start.strftime("%Y-%m"), end.strftime("%Y-%m"))
                if month_only
                else (start.isoformat(), end.isoformat())
            )
    if month_only:
        try:
            start_value = date.fromisoformat(f"{start}-01")
            end_value = date.fromisoformat(f"{end}-01")
        except ValueError as exc:
            raise PlanValidationError("预计采购时间需要写成 YYYY-MM。") from exc
        if start_value > end_value:
            raise PlanValidationError("预计采购时间范围开始不能晚于结束，请确认后重试，不要自动交换。")
    else:
        start_value = _iso_date(start, "时间范围开始")
        end_value = _iso_date(end, "时间范围结束")
        if start_value > end_value:
            raise PlanValidationError("时间范围开始不能晚于结束，请确认后重试，不要自动交换。")
    return start, end


def _project_publish_fragment(value: Any, current_date: Any) -> dict[str, Any]:
    if isinstance(value, dict) and "relative" in value:
        start, end = _relative_range(value, current_date, month_only=False)
        return {"beginTime": start, "endTime": end}
    if isinstance(value, list) and len(value) == 2:
        value = {"start": value[0], "end": value[1]}
    if not isinstance(value, dict) or not value or set(value) - {"start", "end"}:
        raise PlanValidationError("发布时间需要开始、结束时间或相对时间。")
    fragment = {}
    parsed = {}
    for key, field in (("start", "beginTime"), ("end", "endTime")):
        if key not in value:
            continue
        text = str(value[key])
        try:
            fmt = "%Y-%m-%d" if len(text) == 10 else "%Y-%m-%d %H:%M:%S"
            stamp = datetime.strptime(text, fmt)
            if stamp.strftime(fmt) != text:
                raise ValueError("noncanonical date")
        except ValueError as exc:
            raise PlanValidationError("发布时间必须是 YYYY-MM-DD 或 YYYY-MM-DD HH:mm:ss。") from exc
        fragment[field] = text
        parsed[key] = stamp.replace(hour=23, minute=59, second=59) if key == "end" and len(text) == 10 else stamp
    if len(parsed) == 2 and parsed["start"] > parsed["end"]:
        raise PlanValidationError("时间范围开始不能晚于结束，请确认后重试，不要自动交换。")
    return fragment


def _semantic_fragment(
    condition_type: str,
    value: Any,
    source: str,
    current_date: Any,
) -> dict[str, Any]:
    if value is None and condition_type != "preserve_area":
        return _clear_fragment(condition_type, source)
    if condition_type == "keyword_group":
        if not isinstance(value, dict) or set(value) != {"keywords", "matchScopes"}:
            raise PlanValidationError("关键词组必须包含 keywords 和 matchScopes。")
        return {"keywordGroups": [{
            "keywords": _list_value(value["keywords"], "关键词"),
            "matchScopes": _list_value(value["matchScopes"], "匹配范围"),
        }]}
    if condition_type in {"keyword", "project_title", "project_id"}:
        keywords = _list_value(value, "关键词")
        if source == "project":
            return {"keywordGroups": [{"keywords": keywords, "matchScopes": list(PROJECT_DEFAULT_SCOPES[condition_type])}]}
        scopes = {"keyword": [2, 8], "project_title": [2], "project_id": [3]}[condition_type]
        return {"keywords": keywords, **({"matchScopes": scopes} if condition_type != "keyword" else {})}
    if condition_type == "organization_role":
        if not isinstance(value, dict):
            raise PlanValidationError("机构角色需要 role 和 keywords。")
        role = value.get("role")
        scopes = {
            "purchasing_unit": 4, "采购单位": 4, "招标单位": 4,
            "winning_unit": 5, "中标单位": 5,
            "agency": 6, "代理机构": 6,
        }
        if role not in scopes:
            raise PlanValidationError("机构角色无法映射到已确认匹配范围。")
        return {"keywordGroups": [{"keywords": _list_value(value.get("keywords"), "机构名称"), "matchScopes": [scopes[role]]}]}
    if condition_type == "exclude_words":
        return {"excludeWords": _list_value(value, "排除词")}
    if condition_type == "area":
        return {"areaIds": _list_value(value, "地区 ID")}
    if condition_type == "publish_time":
        if source == "project":
            return _project_publish_fragment(value, current_date)
        start, end = _relative_range(value, current_date, month_only=False)
        return {"beginTime": start, "endTime": end}
    if condition_type == "planned_purchase_date":
        start, end = _relative_range(value, current_date, month_only=True)
        return {"startPlanPurchaseDate": start, "endPlanPurchaseDate": end}
    if condition_type == "service_expiry":
        start, end = _relative_range(value, current_date, month_only=False)
        return {"beginServiceExpireTime": start, "endServiceExpireTime": end}
    if condition_type in {
        "amount_min",
        "amount_max",
        "amount_range",
        "planned_amount_min",
        "planned_amount_max",
        "planned_amount_range",
        "contract_amount_min",
        "contract_amount_max",
        "contract_amount_range",
    }:
        return _amount_fragment(condition_type, value, source)
    if condition_type == "stage":
        if isinstance(value, dict):
            return {"infoTypes": value}
        mapped = STAGE_VALUES.get(str(value))
        if mapped is None:
            raise PlanValidationError("阶段语义无法映射到已确认枚举。")
        return {"infoTypes": mapped}
    if condition_type == "organization_type":
        values = _list_value(value, "采购单位类型")
        mapped = [
            ORGANIZATION_TYPE_VALUES.get(str(item), item)
            for item in values
        ]
        if any(not isinstance(item, int) for item in mapped):
            raise PlanValidationError("采购单位类型无法映射到已确认枚举。")
        return {"purchasingUnitTypes": mapped}
    if condition_type in PROJECT_LIST_FILTERS:
        return {PROJECT_LIST_FILTERS[condition_type]: _list_value(value, "筛选值")}
    if condition_type in PROJECT_BINARY_FILTERS:
        return {PROJECT_BINARY_FILTERS[condition_type]: value}
    if condition_type == "procurement_method":
        if source == "project":
            return {"procurementMethods": _list_value(value, "采购方式")}
        return {"procurementMethod": value}
    if condition_type == "match_scope":
        return {"matchScopes": _list_value(value, "匹配范围")}
    if condition_type == "contract_period":
        return {"contractPeriodType": value}
    if condition_type == "sort":
        return {"sortType": value}
    if condition_type == "quantity":
        return {"numPerPage": value}
    if condition_type == "company_name":
        return {"companyName": value}
    if condition_type == "enterprise_time":
        start, end = _relative_range(value, current_date, month_only=False)
        return {"beginTime": start, "endTime": end}
    if condition_type == "phone_type":
        return {"phoneType": value}
    if condition_type == "preserve_area":
        return {}
    raise PlanValidationError(f"条件 {condition_type} 需要提供 normalized 映射。")


def prepare_complex_plan(raw_plan: dict[str, Any], *, user_text: str = "") -> dict[str, Any]:
    if not isinstance(raw_plan, dict):
        raise PlanValidationError("复杂查询计划必须是对象。")
    plan = deepcopy(raw_plan)
    conditions = _require_list(plan.get("conditions"), "conditions")
    operations = _require_list(plan.get("operations"), "operations")
    # Derive provenance before semantic defaults are added. Caller-supplied
    # internal markers are never evidence of explicit scope intent.
    for condition in conditions:
        raw_mapping = condition.get("normalized")
        project_mapping = raw_mapping.get("project", {}) if isinstance(raw_mapping, dict) else {}
        condition["_project_keyword_scopes_explicit"] = (
            isinstance(project_mapping, dict)
            and bool({"matchScopes", "keywordGroups"} & set(project_mapping))
        )
    for operation in operations:
        operation.pop("_project_refine_context", None)
    operation_by_id = _unique_by_id(operations, "操作")
    unresolved_conditions = list(plan.get("unresolved_conditions") or [])
    unresolved_pairs = {
        (str(item.get("operation_id") or ""), str(condition_id))
        for item in unresolved_conditions
        if item.get("scope") == "branch"
        for condition_id in item.get("condition_ids", [])
    }
    semantic_mode = any(
        "normalized" not in condition or "applies_to" not in condition
        for condition in conditions
    ) or any("condition_ids" not in operation or "query" not in operation for operation in operations)

    if semantic_mode:
        for condition in conditions:
            condition.setdefault("source", "user_explicit")
            operation_ids = condition.get("operation_ids")
            if operation_ids is not None:
                operation_ids = [str(item) for item in _require_list(operation_ids, "condition.operation_ids")]
                if not operation_ids or any(item not in operation_by_id for item in operation_ids):
                    raise PlanValidationError("条件 operation_ids 引用了无效操作。")
                selected_operations = [operation_by_id[item] for item in operation_ids]
                condition["operation_ids"] = operation_ids
            else:
                supported_sources = set(CONDITION_FIELDS.get(str(condition.get("type") or ""), {}))
                selected_operations = [
                    operation
                    for operation in operations
                    if operation.get("data_source") in supported_sources
                ]
                if condition.get("source", "user_explicit") == "user_explicit":
                    for operation in operations:
                        operation_id = str(operation.get("id") or "")
                        if operation.get("data_source") in supported_sources:
                            continue
                        unresolved_key = (operation_id, str(condition.get("id") or ""))
                        if unresolved_key in unresolved_pairs:
                            continue
                        unresolved_conditions.append(
                            {
                                "scope": "branch",
                                "operation_id": operation_id,
                                "condition_ids": [str(condition.get("id") or "")],
                                "logic_group_ids": [],
                                "reason": "当前数据源不支持该用户明确条件，不得删除条件后继续查询",
                            }
                        )
                        unresolved_pairs.add(unresolved_key)
            applies_to = list(dict.fromkeys(str(item.get("data_source")) for item in selected_operations))
            if not applies_to and "operation_ids" not in condition:
                applies_to = sorted(supported_sources)
            if not applies_to:
                applies_to = list(condition.get("applies_to") or [])
            condition["applies_to"] = applies_to
            if condition.get("resolution") == "unresolved_only":
                condition.setdefault("normalized", {})
                continue
            if "normalized" not in condition:
                condition["normalized"] = {
                    source: _semantic_fragment(
                        str(condition.get("type") or ""),
                        condition.get("value"),
                        source,
                        plan.get("current_date"),
                    )
                    for source in applies_to
                }

        for operation in operations:
            operation_id = str(operation.get("id") or "")
            operation["condition_ids"] = [
                str(condition.get("id") or "")
                for condition in conditions
                if operation["data_source"] in condition.get("applies_to", [])
                and (
                    "operation_ids" not in condition
                    or operation_id in condition["operation_ids"]
                )
                and condition.get("resolution") != "unresolved_only"
            ]
            operation.setdefault("query", {})

    if "logic_groups" not in plan:
        plan["logic_groups"] = [
            {
                "id": "root",
                "operator": "AND",
                "condition_ids": [str(item.get("id") or "") for item in conditions],
                "group_ids": [],
            }
        ]
        plan["root_group_id"] = "root"
    plan["unresolved_conditions"] = unresolved_conditions
    plan.setdefault("planned_business_calls", len(operations))
    return plan


def _require_list(value: Any, label: str) -> list[Any]:
    if not isinstance(value, list):
        raise PlanValidationError(f"{label}必须是数组。")
    return value


def _unique_by_id(items: list[dict[str, Any]], label: str) -> dict[str, dict[str, Any]]:
    indexed: dict[str, dict[str, Any]] = {}
    for item in items:
        item_id = str(item.get("id") or "").strip()
        if not item_id:
            raise PlanValidationError(f"{label}缺少 ID。")
        if item_id in indexed:
            raise PlanValidationError(f"{label} ID 重复：{item_id}。")
        indexed[item_id] = item
    return indexed


def _check_logic_cycles(groups: dict[str, dict[str, Any]]) -> None:
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(group_id: str) -> None:
        if group_id in visiting:
            raise PlanValidationError("逻辑组存在循环。")
        if group_id in visited:
            return
        visiting.add(group_id)
        for child in groups[group_id].get("group_ids", []):
            visit(str(child))
        visiting.remove(group_id)
        visited.add(group_id)

    for group_id in groups:
        visit(group_id)


def _is_clear_condition(condition: dict[str, Any]) -> bool:
    return "value" in condition and condition["value"] is None


def _clear_fragment(condition_type: str, source: str) -> dict[str, Any]:
    if source != "project" or condition_type not in PROJECT_CLEAR_FIELDS:
        raise PlanValidationError("null 只能用于明确取消普通标讯的可选筛选；关键词、匹配范围和有界发布时间不能取消。")
    return {field: None for field in PROJECT_CLEAR_FIELDS[condition_type]}


def _validate_condition_mapping(condition: dict[str, Any], unresolved_ids: set[str]) -> None:
    condition_type = str(condition.get("type") or "")
    applies_to = condition["applies_to"]
    normalized = condition.get("normalized") or {}
    if not isinstance(normalized, dict):
        raise PlanValidationError("条件 normalized 必须是对象。")
    resolution = condition.get("resolution")
    if resolution == "unresolved_only":
        if condition["id"] not in unresolved_ids or normalized:
            raise PlanValidationError("unresolved_only 条件必须仅进入未解决条件且不得生成参数。")
        return
    if resolution not in (None, "mapped"):
        raise PlanValidationError("条件 resolution 无效。")
    if set(normalized) - set(applies_to):
        raise PlanValidationError("条件 normalized 包含未声明的数据源。")
    rules = CONDITION_FIELDS.get(condition_type)
    if rules is None:
        raise PlanValidationError(f"条件类型不受支持：{condition_type}。")
    is_clear = _is_clear_condition(condition)
    if is_clear and condition.get("source", "user_explicit") != "user_explicit":
        raise PlanValidationError("取消筛选必须是用户明确要求。")
    for source in applies_to:
        allowed = rules.get(source)
        if allowed is None:
            raise PlanValidationError(f"条件 {condition_type} 不适用于数据源 {source}。")
        fragment = normalized.get(source)
        if is_clear:
            if fragment != _clear_fragment(condition_type, source):
                raise PlanValidationError("取消筛选必须映射为对应接口字段的 null，不得保留、替换或增加限制。")
        elif source == "project" and isinstance(fragment, dict) and any(value is None for value in fragment.values()):
            raise PlanValidationError("取消筛选必须显式使用 value:null，不能藏在 normalized 映射中。")
        if condition_type == "preserve_area":
            if fragment not in (None, {}):
                raise PlanValidationError("preserve_area 不得生成地区 patch。")
            continue
        if condition.get("source", "user_explicit") == "user_explicit" and not isinstance(fragment, dict):
            raise PlanValidationError("用户明确条件缺少数据源映射。")
        if isinstance(fragment, dict) and not set(fragment) <= allowed:
            raise PlanValidationError(
                f"条件 {condition_type} 在数据源 {source} 的字段或方向错误。",
                details={"allowed_fields": sorted(allowed), "actual_fields": sorted(fragment)},
            )
        if source == "project" and isinstance(fragment, dict):
            if condition_type in {"keyword", "keyword_group", "project_title", "project_id", "organization_role"}:
                if not (fragment.get("keywordGroups") or fragment.get("keywords")):
                    raise PlanValidationError("关键词条件的映射不完整。")
            if condition_type == "procurement_method" and not ({"procurementMethod", "procurementMethods"} & set(fragment)):
                raise PlanValidationError("采购方式条件的映射不完整。")
        required = REQUIRED_CONDITION_FIELDS.get(condition_type, {}).get(source, set())
        if isinstance(fragment, dict) and not required <= set(fragment):
            raise PlanValidationError(
                f"条件 {condition_type} 在数据源 {source} 的映射不完整。",
                details={"required_fields": sorted(required), "actual_fields": sorted(fragment)},
            )


def _condition_applies_to_operation(condition: dict[str, Any], operation: dict[str, Any]) -> bool:
    if operation["data_source"] not in condition["applies_to"]:
        return False
    operation_ids = condition.get("operation_ids")
    return operation_ids is None or operation["id"] in operation_ids


def _reachable_from_root(
    root_group_id: str,
    groups: dict[str, dict[str, Any]],
) -> tuple[set[str], set[str]]:
    condition_ids: set[str] = set()
    group_ids: set[str] = set()

    def visit(group_id: str) -> None:
        if group_id in group_ids:
            return
        group_ids.add(group_id)
        group = groups[group_id]
        condition_ids.update(str(item) for item in group.get("condition_ids", []))
        for child_group_id in group.get("group_ids", []):
            visit(str(child_group_id))

    visit(root_group_id)
    return condition_ids, group_ids


def validate_plan_shape(raw_plan: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(raw_plan, dict):
        raise PlanValidationError("复杂查询计划必须是对象。")
    plan = deepcopy(raw_plan)
    conditions = _require_list(plan.get("conditions"), "conditions")
    groups = _require_list(plan.get("logic_groups"), "logic_groups")
    operations = _require_list(plan.get("operations"), "operations")
    unresolved = _require_list(plan.get("unresolved_conditions"), "unresolved_conditions")
    condition_by_id = _unique_by_id(conditions, "条件")
    group_by_id = _unique_by_id(groups, "逻辑组")
    operation_by_id = _unique_by_id(operations, "操作")
    unresolved_ids = {
        str(condition_id)
        for item in unresolved
        for condition_id in item.get("condition_ids", [])
    }

    for condition in conditions:
        if condition.get("source", "user_explicit") not in SUPPORTED_SOURCES:
            raise PlanValidationError("条件来源不受支持。")
        applies_to = _require_list(condition.get("applies_to"), "applies_to")
        if not applies_to or any(source not in SUPPORTED_DATA_SOURCES for source in applies_to):
            raise PlanValidationError("条件的数据源范围无效。")
        _validate_condition_mapping(condition, unresolved_ids)

    for group in groups:
        if group.get("operator") not in SUPPORTED_OPERATORS:
            raise PlanValidationError("逻辑运算符不受支持。")
        for condition_id in group.get("condition_ids", []):
            if str(condition_id) not in condition_by_id:
                raise PlanValidationError(f"逻辑组引用了不存在的条件：{condition_id}。")
        for child_group_id in group.get("group_ids", []):
            if str(child_group_id) not in group_by_id:
                raise PlanValidationError(f"逻辑组引用了不存在的子组：{child_group_id}。")

    root_group_id = str(plan.get("root_group_id") or "").strip()
    if root_group_id not in group_by_id:
        raise PlanValidationError("root_group_id 无效。")
    _check_logic_cycles(group_by_id)
    root_condition_ids, root_group_ids = _reachable_from_root(root_group_id, group_by_id)

    referenced_condition_ids: set[str] = set()
    for condition in conditions:
        if "operation_ids" not in condition:
            continue
        operation_ids = _require_list(condition["operation_ids"], "condition.operation_ids")
        if not operation_ids or any(str(value) not in operation_by_id for value in operation_ids):
            raise PlanValidationError("条件 operation_ids 引用了无效操作。")
        if any(
            operation_by_id[str(value)]["data_source"] not in condition["applies_to"]
            for value in operation_ids
        ):
            raise PlanValidationError("条件 operation_ids 与数据源范围不一致。")

    for operation in operations:
        source = operation.get("data_source")
        action = operation.get("action")
        route = (source, action)
        if (
            source not in SUPPORTED_DATA_SOURCES
            or action not in SUPPORTED_ACTIONS
            or route not in COMMAND_BY_ROUTE
        ):
            raise PlanValidationError("操作的数据源或动作无效。")
        expected_command = COMMAND_BY_ROUTE[route]
        if operation.get("command") not in (None, expected_command):
            raise PlanValidationError("操作命令与数据源或动作不一致。")
        if source == "enterprise":
            enterprise_kind = str(operation.get("enterprise_kind") or "").strip()
            if not enterprise_kind:
                raise PlanValidationError("企业情报操作缺少 enterprise_kind。")
            if enterprise_kind not in ENTERPRISE_KIND_FIELDS:
                raise PlanValidationError("企业情报操作的 enterprise_kind 不受支持。")
            if not set(operation.get("query") or {}) <= ENTERPRISE_KIND_FIELDS[enterprise_kind]:
                raise PlanValidationError("当前企业能力不支持操作中的条件字段。")
        for condition_id in _require_list(operation.get("condition_ids"), "operation.condition_ids"):
            condition_id = str(condition_id)
            condition = condition_by_id.get(condition_id)
            if condition is None:
                raise PlanValidationError(f"操作引用了不存在的条件：{condition_id}。")
            if not _condition_applies_to_operation(condition, operation):
                raise PlanValidationError(f"条件 {condition_id} 不适用于数据源 {source}。")
            if _is_clear_condition(condition) and (source != "project" or action != "refine"):
                raise PlanValidationError("取消可选筛选仅适用于普通标讯 refine，不能用于新搜索。")
            if source == "enterprise":
                fragment = (condition.get("normalized") or {}).get("enterprise") or {}
                if not set(fragment) <= ENTERPRISE_KIND_FIELDS[enterprise_kind]:
                    raise PlanValidationError("当前企业能力不支持条件中的字段。")
            referenced_condition_ids.add(condition_id)

    explicit_ids = {
        condition_id
        for condition_id, condition in condition_by_id.items()
        if condition.get("source", "user_explicit") == "user_explicit"
    }
    outside_root = sorted(explicit_ids - root_condition_ids - unresolved_ids)
    if outside_root:
        raise PlanValidationError(
            "用户明确条件未进入根逻辑组。", details={"condition_ids": outside_root}
        )
    missing = sorted(explicit_ids - referenced_condition_ids - unresolved_ids)
    if missing:
        raise PlanValidationError(
            "用户明确条件未进入操作或未解决条件。", details={"condition_ids": missing}
        )

    planned_calls = plan.get("planned_business_calls")
    if not isinstance(planned_calls, int) or planned_calls < 0:
        raise PlanValidationError("planned_business_calls 必须是非负整数。")
    if planned_calls != len(operation_by_id):
        raise PlanValidationError("计划业务调用次数与操作数量不一致。")

    for item in unresolved:
        scope = item.get("scope")
        if scope not in {"global", "branch"}:
            raise PlanValidationError("未解决条件 scope 无效。")
        if not str(item.get("reason") or "").strip():
            raise PlanValidationError("未解决条件缺少原因。")
        item_condition_ids = {str(value) for value in item.get("condition_ids", [])}
        item_group_ids = {str(value) for value in item.get("logic_group_ids", [])}
        if not item_condition_ids <= set(condition_by_id) or not item_group_ids <= root_group_ids:
            raise PlanValidationError("未解决条件引用不存在的条件或逻辑组。")
        if scope == "branch" and str(item.get("operation_id") or "") not in operation_by_id:
            raise PlanValidationError("未解决条件引用无效操作。")

    global_unresolved = {
        str(condition_id)
        for item in unresolved
        if item.get("scope") == "global"
        for condition_id in item.get("condition_ids", [])
    }
    branch_unresolved = {
        operation_id: {
            str(condition_id)
            for item in unresolved
            if item.get("scope") == "branch" and str(item.get("operation_id")) == operation_id
            for condition_id in item.get("condition_ids", [])
        }
        for operation_id in operation_by_id
    }
    for operation_id, operation in operation_by_id.items():
        required = {
            condition_id
            for condition_id, condition in condition_by_id.items()
            if condition_id in root_condition_ids
            and condition.get("source", "user_explicit") == "user_explicit"
            and _condition_applies_to_operation(condition, operation)
        }
        missing_from_branch = (
            required
            - set(map(str, operation["condition_ids"]))
            - global_unresolved
            - branch_unresolved[operation_id]
        )
        if missing_from_branch:
            raise PlanValidationError(
                "适用分支遗漏用户明确条件。",
                details={
                    "operation_id": operation_id,
                    "condition_ids": sorted(missing_from_branch),
                },
            )

    return plan


def _merge_value(field: str, existing: Any, incoming: Any) -> Any:
    if existing == incoming:
        return existing
    if field in {"keywords", "excludeWords"} and isinstance(existing, list) and isinstance(incoming, list):
        return list(dict.fromkeys([*existing, *incoming]))
    raise PlanValidationError(f"同一字段存在不能自动合并的多个值：{field}。")


def _apply_logic_groups(
    plan: dict[str, Any],
    operation: dict[str, Any],
    query: dict[str, Any],
    field_conflicts: dict[str, list[str]],
) -> list[dict[str, Any]]:
    condition_by_id = {item["id"]: item for item in plan["conditions"]}
    operation_ids = set(operation["condition_ids"])
    unresolved: list[dict[str, Any]] = []
    keyword_groups: list[tuple[dict[str, Any], list[str]]] = []
    group_by_id = {item["id"]: item for item in plan["logic_groups"]}
    _, reachable_group_ids = _reachable_from_root(plan["root_group_id"], group_by_id)
    for field, condition_ids in field_conflicts.items():
        logic_group_ids = [
            group_id
            for group_id in reachable_group_ids
            if set(condition_ids) & set(map(str, group_by_id[group_id].get("condition_ids", [])))
        ]
        unresolved.append(
            {
                "scope": "branch",
                "operation_id": operation["id"],
                "condition_ids": condition_ids,
                "logic_group_ids": logic_group_ids,
                "reason": f"同一字段 {field} 的多个条件无法证明等价，不得自动合并",
            }
        )
    for group in plan["logic_groups"]:
        if group["id"] not in reachable_group_ids:
            continue
        if group["operator"] in {"OR", "NOT"} and group.get("group_ids"):
            descendant_ids, _ = _reachable_from_root(group["id"], group_by_id)
            relevant_ids = sorted(descendant_ids & operation_ids)
            if relevant_ids:
                unresolved.append({
                    "scope": "branch", "operation_id": operation["id"],
                    "condition_ids": relevant_ids, "logic_group_ids": [group["id"]],
                    "reason": "当前数据源无法证明嵌套 OR/NOT 逻辑等价，不得忽略父组",
                })
                continue
        condition_ids = [item for item in group.get("condition_ids", []) if item in operation_ids]
        if not condition_ids:
            continue
        operator = group["operator"]
        condition_types = {condition_by_id[item]["type"] for item in condition_ids}
        if operator in {"AND", "OR"} and condition_types == {"keyword"}:
            keyword_groups.append((group, condition_ids))
            continue
        if operator == "NOT" and condition_types == {"exclude_words"}:
            continue
        if operator == "AND":
            continue
        unresolved.append(
            {
                "scope": "branch",
                "operation_id": operation["id"],
                "condition_ids": condition_ids,
                "logic_group_ids": [group["id"]],
                "reason": "接口无法等价表达该逻辑组",
            }
        )

    if len(keyword_groups) == 1:
        group, _ = keyword_groups[0]
        query["keywordsSearchType"] = 2 if group["operator"] == "AND" else 1
    elif len(keyword_groups) > 1:
        for group, condition_ids in keyword_groups:
            unresolved.append(
                {
                    "scope": "branch",
                    "operation_id": operation["id"],
                    "condition_ids": condition_ids,
                    "logic_group_ids": [group["id"]],
                    "reason": "单一 keywordsSearchType 无法等价表达多个关键词逻辑组",
                }
            )
    return unresolved


def _project_condition_query(
    plan: dict[str, Any],
    operation: dict[str, Any],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Compile the reachable expression to AND-of-OR keyword clauses.

    Filter atoms are legal only as conjuncts. OR distribution is exact, and a
    scoped OR is emitted only when a single API group preserves its meaning.
    """
    conditions = {item["id"]: item for item in plan["conditions"]}
    groups = {item["id"]: item for item in plan["logic_groups"]}
    selected = set(operation["condition_ids"])
    default_scopes = list(PROJECT_DEFAULT_SCOPES["keyword"])
    scope_values = [
        item["normalized"]["project"]["matchScopes"]
        for item in plan["conditions"]
        if item["id"] in selected and item["type"] == "match_scope"
    ]
    if scope_values:
        if any(set(value) != set(scope_values[0]) for value in scope_values[1:]):
            raise PlanValidationError("同一字段 matchScopes 的多个条件无法证明等价，不得自动合并。")
        default_scopes = scope_values[0]

    def condition_clauses(condition_id: str) -> list[list[dict[str, Any]]]:
        condition = conditions[condition_id]
        fragment = deepcopy((condition.get("normalized") or {}).get("project") or {})
        if not fragment and condition["type"] != "preserve_area":
            raise PlanValidationError(f"条件 {condition_id} 缺少标准化映射。")
        keyword_groups = fragment.pop("keywordGroups", [])
        legacy_keywords = fragment.pop("keywords", None)
        legacy_scopes = fragment.pop("matchScopes", None)
        if legacy_keywords is not None:
            if keyword_groups:
                raise PlanValidationError("一个条件不能同时包含新旧关键词格式。")
            scopes = list(legacy_scopes or {
                "project_title": PROJECT_DEFAULT_SCOPES["project_title"],
                "project_id": PROJECT_DEFAULT_SCOPES["project_id"],
            }.get(condition["type"], default_scopes))
            if condition["type"] == "organization_role" and not legacy_scopes:
                value = condition.get("value")
                if not isinstance(value, dict):
                    raise PlanValidationError("机构角色缺少已确认的匹配位置。")
                scopes = _semantic_fragment("organization_role", value, "project", None)["keywordGroups"][0]["matchScopes"]
            keyword_groups = [{"keywords": legacy_keywords, "matchScopes": scopes}]
        elif condition["type"] == "keyword" and scope_values:
            # A standalone scope condition qualifies general keywords. Explicit
            # keyword_group/title/id/role scopes remain independent.
            for keyword_group in keyword_groups:
                keyword_group["matchScopes"] = default_scopes
        if "procurementMethod" in fragment:
            value = fragment.pop("procurementMethod")
            fragment["procurementMethods"] = _list_value(value, "采购方式")
        clauses = [[{"kind": "keyword", **group}] for group in keyword_groups]
        if fragment or condition["type"] == "match_scope":
            clauses.append([{"kind": "filter", "fields": fragment}])
        return clauses

    def simplify(clauses, expansion_limit=None):
        # Boolean idempotence and absorption avoid exponential repeated clauses.
        output, keys = [], []
        for clause in clauses:
            atoms = {json.dumps(atom, sort_keys=True, ensure_ascii=False): atom for atom in clause}
            key = frozenset(atoms)
            if any(existing <= key for existing in keys):
                continue
            keep = [i for i, existing in enumerate(keys) if not key < existing]
            output = [output[i] for i in keep]
            keys = [keys[i] for i in keep]
            output.append(list(atoms.values()))
            keys.append(key)
            if expansion_limit is not None and len(output) > expansion_limit:
                raise PlanValidationError("查询逻辑展开过大，需先简化条件；未执行或丢弃条件。")
        return output

    def visit(group_id: str) -> list[list[dict[str, Any]]]:
        group = groups[group_id]
        if group["operator"] != "AND":
            descendant_ids, _ = _reachable_from_root(group_id, groups)
            if any(_is_clear_condition(conditions[cid]) for cid in descendant_ids & selected):
                raise PlanValidationError("取消筛选只能通过 AND 组合，不能位于 OR 或 NOT 逻辑组中。")
        condition_ids = [str(cid) for cid in group.get("condition_ids", []) if str(cid) in selected]
        children = [condition_clauses(cid) for cid in condition_ids]
        children += [visit(str(child)) for child in group.get("group_ids", [])]
        children = [child for child in children if child]
        operator = group["operator"]
        if operator == "NOT":
            # exclude_words already denotes the negative predicate.
            if group.get("group_ids") or any(conditions[cid]["type"] != "exclude_words" for cid in condition_ids):
                raise PlanValidationError("接口无法等价表达该 NOT 逻辑组。")
            return simplify(clause for child in children for clause in child)
        if operator == "AND":
            return simplify(clause for child in children for clause in child)
        if not children:
            return []
        result = children[0]
        for child in children[1:]:
            result = simplify((left + right for left in result for right in child), max(256, len(result), len(child)))
        return result

    try:
        clauses = visit(plan["root_group_id"])
        query: dict[str, Any] = {}
        keyword_groups = []
        for clause in clauses:
            if any(atom["kind"] != "keyword" for atom in clause):
                if len(clause) != 1:
                    multi_fields = {"procurementMethods", "procurementCategories", "fundsSources", "areaIds", "purchasingUnitTypes"}
                    fields = [atom.get("fields", {}) for atom in clause]
                    if any(atom["kind"] != "filter" for atom in clause) or any(len(item) != 1 for item in fields):
                        raise PlanValidationError("接口无法等价表达包含筛选条件的 OR 逻辑组。")
                    field = next(iter(fields[0]))
                    if field not in multi_fields or any(set(item) != {field} for item in fields):
                        raise PlanValidationError("接口无法等价表达包含筛选条件的 OR 逻辑组。")
                    clause = [{"fields": {field: list(dict.fromkeys(value for item in fields for value in item[field]))}}]
                for field, value in clause[0]["fields"].items():
                    query[field] = _merge_value(field, query[field], value) if field in query else value
                continue
            scopes = clause[0]["matchScopes"]
            if any(set(atom["matchScopes"]) != set(scopes) for atom in clause[1:]):
                if any(set(atom["keywords"]) != set(clause[0]["keywords"]) for atom in clause[1:]):
                    raise PlanValidationError("接口无法等价表达不同匹配位置之间的 OR 逻辑组。")
                scopes = list(dict.fromkeys(scope for atom in clause for scope in atom["matchScopes"]))
            keywords = list(dict.fromkeys(word for atom in clause for word in atom["keywords"]))
            compiled_group = {"keywords": keywords, "matchScopes": scopes}
            if compiled_group not in keyword_groups:
                keyword_groups.append(compiled_group)
        if keyword_groups:
            query["keywordGroups"] = keyword_groups
        if scope_values and not keyword_groups:
            if operation.get("action") != "refine":
                raise PlanValidationError("匹配范围条件缺少适用关键词。")
            # Internal directive, consumed by the state-aware runtime normalizer.
            query["matchScopes"] = default_scopes
        return query, []
    except PlanValidationError as exc:
        return {}, [{
            "scope": "branch", "operation_id": operation["id"],
            "condition_ids": list(operation["condition_ids"]),
            "logic_group_ids": [plan["root_group_id"]], "reason": str(exc),
        }]


def _condition_query(
    plan: dict[str, Any],
    operation: dict[str, Any],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    source = operation["data_source"]
    if source == "project":
        return _project_condition_query(plan, operation)
    operation_ids = set(operation["condition_ids"])
    query: dict[str, Any] = {}
    field_condition_ids: dict[str, list[str]] = {}
    field_conflicts: dict[str, list[str]] = {}
    for condition in plan["conditions"]:
        condition_id = condition["id"]
        if condition_id not in operation_ids:
            continue
        fragment = (condition.get("normalized") or {}).get(source) or {}
        if (
            condition.get("source", "user_explicit") == "user_explicit"
            and condition.get("type") != "preserve_area"
            and not fragment
        ):
            raise PlanValidationError(
                f"用户明确条件 {condition_id} 缺少当前数据源的标准化映射。",
                details={"condition_ids": [condition_id]},
            )
        for field, value in fragment.items():
            field_condition_ids.setdefault(field, []).append(condition_id)
            if field not in query:
                query[field] = value
                continue
            try:
                query[field] = _merge_value(field, query[field], value)
            except PlanValidationError:
                field_conflicts[field] = list(field_condition_ids[field])
    unresolved = _apply_logic_groups(plan, operation, query, field_conflicts)
    return query, unresolved


def _rebuild_operation_query(
    plan: dict[str, Any],
    operation: dict[str, Any],
) -> tuple[dict[str, Any], list[str], list[dict[str, Any]]]:
    candidate = deepcopy(operation.get("query") or {})
    condition_query, unresolved = _condition_query(plan, operation)
    corrected_fields = sorted(
        field
        for field in set(candidate) | set(condition_query)
        if candidate.get(field) != condition_query.get(field)
    )
    return condition_query, corrected_fields, unresolved


def _minimum_fallback_matches(
    plan: dict[str, Any],
    operation: dict[str, Any],
    normalized_candidate: dict[str, Any],
    normalize_operation: Any,
) -> bool:
    expected_raw, unresolved = _condition_query(plan, operation)
    if unresolved:
        return False
    normalized_expected, _ = normalize_operation(
        operation["data_source"],
        operation["action"],
        expected_raw,
        _normalization_operation(plan, operation),
    )
    return normalized_candidate == normalized_expected


def _normalization_operation(plan: dict[str, Any], operation: dict[str, Any]) -> dict[str, Any]:
    """Pass compiler-derived refinement intent only to the normalizer."""
    context_operation = {key: value for key, value in operation.items() if key != "_project_refine_context"}
    if operation["data_source"] != "project" or operation["action"] != "refine":
        return context_operation
    selected = set(operation["condition_ids"])
    conditions = [item for item in plan["conditions"] if item["id"] in selected]
    keyword_types = {"keyword", "keyword_group", "project_title", "project_id", "organization_role"}
    keyword_conditions = [item for item in conditions if item["type"] in keyword_types]
    types = {item["type"] for item in keyword_conditions}
    context = {
        "mode": "replace" if not types or types == {"keyword_group"} else "ambiguous",
        "explicit_scopes": False,
    }
    if "keyword" in types:
        context["mode"] = "generic" if types == {"keyword"} else "ambiguous"
        explicit = [item["_project_keyword_scopes_explicit"] for item in keyword_conditions]
        scope_condition = any(item["type"] == "match_scope" for item in conditions)
        context["explicit_scopes"] = scope_condition or all(explicit)
        if not scope_condition and any(explicit) and not all(explicit):
            context["mode"] = "ambiguous"
    context_operation["_project_refine_context"] = context
    return context_operation


def _approved_operation(
    operation: dict[str, Any],
    query: dict[str, Any],
    warnings: list[str],
) -> dict[str, Any]:
    return {
        **operation,
        "command": COMMAND_BY_ROUTE[(operation["data_source"], operation["action"])],
        "query": query,
        "warnings": warnings,
    }


def preflight_complex_plan(
    raw_plan: dict[str, Any],
    normalize_operation: Any,
    *,
    user_text: str = "",
) -> dict[str, Any]:
    try:
        plan = validate_plan_shape(
            prepare_complex_plan(
                _sanitize_plan_match_scopes(raw_plan, user_text),
                user_text=user_text,
            )
        )
    except PlanValidationError as exc:
        return {
            "ok": False,
            "error_code": "COMPLEX_PLAN_INVALID",
            "agent_instruction": str(exc),
            "approved_operations": [],
            "approved_business_calls": 0,
            "fallback_status": "blocked",
        }

    unresolved = list(plan["unresolved_conditions"])
    if any(item.get("scope") == "global" for item in unresolved):
        return {
            "ok": False,
            "error_code": "COMPLEX_PLAN_UNRESOLVED",
            "unresolved_conditions": unresolved,
            "approved_operations": [],
            "approved_business_calls": 0,
            "fallback_status": "blocked",
        }

    blocked_ids = {
        str(item.get("operation_id"))
        for item in unresolved
        if item.get("scope") == "branch"
    }
    safe_originals: dict[str, dict[str, Any]] = {}
    for operation in plan["operations"]:
        if operation["id"] in blocked_ids:
            continue
        try:
            original_query, original_warnings = normalize_operation(
                operation["data_source"],
                operation["action"],
                deepcopy(operation.get("query") or {}),
                _normalization_operation(plan, operation),
            )
            if _minimum_fallback_matches(plan, operation, original_query, normalize_operation):
                safe_originals[operation["id"]] = _approved_operation(
                    operation,
                    original_query,
                    original_warnings,
                )
        except Exception:
            pass

    corrections: list[dict[str, Any]] = []
    approved_operations: list[dict[str, Any]] = []
    fallback_used = False
    for operation in plan["operations"]:
        if operation["id"] in blocked_ids:
            continue
        try:
            query, fields, logic_unresolved = _rebuild_operation_query(plan, operation)
            unresolved.extend(logic_unresolved)
            if logic_unresolved:
                blocked_ids.add(operation["id"])
                continue
            normalized_query, warnings = normalize_operation(
                operation["data_source"],
                operation["action"],
                query,
                _normalization_operation(plan, operation),
            )
            approved_operations.append(_approved_operation(operation, normalized_query, warnings))
            if fields:
                corrections.append({"operation_id": operation["id"], "fields": fields})
        except Exception as exc:
            fallback = safe_originals.get(operation["id"])
            if fallback is not None:
                approved_operations.append(fallback)
                fallback_used = True
                continue
            unresolved.append(
                {
                    "scope": "branch",
                    "operation_id": operation["id"],
                    "condition_ids": list(operation["condition_ids"]),
                    "logic_group_ids": [],
                    "reason": f"增强异常且原候选未通过最小检查：{exc}",
                }
            )

    return {
        "ok": bool(approved_operations),
        "error_code": None if approved_operations else "COMPLEX_PREFLIGHT_FAILED",
        "stage": "complex_preflight",
        "approved_operations": approved_operations,
        "approved_business_calls": len(approved_operations),
        "unresolved_conditions": unresolved,
        "corrections": corrections,
        "fallback_status": (
            "used" if fallback_used else ("blocked" if not approved_operations else "not_needed")
        ),
    }
