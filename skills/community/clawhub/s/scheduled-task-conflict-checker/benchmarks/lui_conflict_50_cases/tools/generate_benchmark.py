#!/usr/bin/env python3
"""生成 scheduled-task-conflict-checker 的 50 组隔离 benchmark fixture。"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any, Dict, List


ROOT = Path(__file__).resolve().parents[1]
FIXTURES_DIR = ROOT / "fixtures"


def shop(
    shop_id: str,
    platform: str,
    *,
    authorized: bool = True,
    sv_status: str | None = "ok",
    paid: bool | None = True,
) -> Dict[str, Any]:
    item: Dict[str, Any] = {
        "shop_id": shop_id,
        "shopCode": shop_id,
        "shop_name": f"{shop_id}店铺",
        "platform": platform,
        "channel": platform,
        "authorized": authorized,
        "is_authorized": authorized,
    }
    if sv_status is not None:
        item["create_permission_status"] = sv_status
        item["sv_permission_status"] = sv_status
    if paid is not None:
        item["has_sv_advanced_permission"] = paid
        item["sv_is_paid"] = paid
    return item


def ctx(
    shops: List[Dict[str, Any]],
    *,
    capabilities: Dict[str, Dict[str, bool]] | None = None,
    wechat_bound: bool = True,
) -> Dict[str, Any]:
    return {
        "ali_id": "ali_test_001",
        "shops": shops,
        "platform_capabilities": capabilities or {
            "pinduoduo": {
                "auto_listing": True,
                "auto_follow_order": True,
                "inventory_sync": True,
                "price_adjust": True,
                "auto_delist": True,
                "supplier_switch": True,
                "product_selection": True,
                "inspection": True,
                "daily_report": True,
            },
            "douyin": {
                "auto_listing": True,
                "auto_follow_order": True,
                "inventory_sync": True,
                "price_adjust": False,
                "auto_delist": False,
                "supplier_switch": True,
                "product_selection": True,
                "inspection": True,
                "daily_report": True,
            },
            "xiaohongshu": {
                "auto_listing": True,
                "auto_follow_order": False,
                "inventory_sync": True,
                "price_adjust": False,
                "auto_delist": False,
                "supplier_switch": False,
                "product_selection": True,
                "inspection": True,
                "daily_report": True,
            },
        },
        "wechat_bound": wechat_bound,
    }


def task(
    task_id: str,
    task_type: str,
    shop_id: str | None = "pdd_A",
    *,
    platform: str | None = None,
    name: str | None = None,
    frequency: str = "daily",
    time: str = "09:00",
    interval_minutes: int | None = None,
    strategy: Dict[str, Any] | None = None,
    status: str = "active",
    source: str = "LUI",
    all_shops: bool = False,
    requires_sv: bool = False,
    notify: Dict[str, Any] | None = None,
    workflow_steps: List[str] | None = None,
) -> Dict[str, Any]:
    item: Dict[str, Any] = {
        "task_id": task_id,
        "source": source,
        "canonical_task_type": task_type,
        "name": name or task_type,
        "frequency": frequency,
        "time": time,
        "status": status,
    }
    if shop_id is not None:
        item["shop_id"] = shop_id
    if platform is not None:
        item["platform"] = platform
    if interval_minutes is not None:
        item["interval_minutes"] = interval_minutes
    if strategy:
        item["strategy"] = strategy
    if all_shops:
        item["all_shops"] = True
        item.pop("shop_id", None)
    if requires_sv:
        item["requires_sv_advanced_permission"] = True
    if notify is not None:
        item["notification"] = notify
    if workflow_steps:
        item["workflow_steps"] = workflow_steps
    return item


def case(
    num: int,
    category: str,
    title: str,
    initial_tasks: List[Dict[str, Any]],
    user_context: Dict[str, Any],
    new_lui_request: str,
    proposed_task: Dict[str, Any],
    expected_decision: str,
    expected_reason_code: str,
    expected_prompt_required: bool,
) -> Dict[str, Any]:
    case_id = f"case_{num:03d}"
    return {
        "case_id": case_id,
        "category": category,
        "title": title,
        "initial_tasks": initial_tasks,
        "existing_tasks": initial_tasks,
        "user_context": user_context,
        "new_lui_request": new_lui_request,
        "proposed_task": proposed_task,
        "expected_decision": expected_decision,
        "expected_reason_code": expected_reason_code,
        "expected_prompt_required": expected_prompt_required,
        "cleanup_required": True,
        "cleanup_policy": "runner 必须在本 case 执行前清空 runtime/task_pool.json，写入 initial_tasks；执行后再次删除 runtime/task_pool.json，禁止后续 case 继承任务状态。",
    }


def build_cases() -> List[Dict[str, Any]]:
    pdd_a = shop("pdd_A", "pinduoduo")
    pdd_b = shop("pdd_B", "pinduoduo")
    dy_a = shop("dy_A", "douyin")
    xhs_a = shop("xhs_A", "xiaohongshu")
    expired = shop("pdd_expired", "pinduoduo", authorized=False, sv_status="authorization_invalid", paid=False)
    unpaid = shop("pdd_unpaid", "pinduoduo", sv_status="sv_not_paid", paid=False)
    api_error = shop("pdd_api_error", "pinduoduo", sv_status="paid_status_api_error", paid=False)
    param_error = shop("pdd_param_error", "pinduoduo", sv_status="shop_not_found_or_param_error", paid=False)
    missing_paid = shop("pdd_missing_paid", "pinduoduo", sv_status="paid_status_missing", paid=None)

    cases: List[Dict[str, Any]] = []

    # 店铺绑定/授权边界 8
    cases.append(case(1, "店铺绑定/授权边界", "无绑定店铺时阻断创建", [], ctx([]), "每天9点帮我同步库存", task("new", "inventory_sync", shop_id=None), "block", "no_bound_shop", True))
    cases.append(case(2, "店铺绑定/授权边界", "单店未指定范围时默认该店铺", [], ctx([pdd_a]), "每天9点同步库存", task("new", "inventory_sync", shop_id=None), "proceed", "none", False))
    cases.append(case(3, "店铺绑定/授权边界", "多店未指定范围要求用户选择", [], ctx([pdd_a, pdd_b]), "每天9点同步库存", task("new", "inventory_sync", shop_id=None), "ask_confirmation", "shop_scope_missing", True))
    cases.append(case(4, "店铺绑定/授权边界", "指定未绑定店铺时阻断", [], ctx([pdd_a]), "每天9点同步未绑定店铺库存", task("new", "inventory_sync", shop_id="pdd_unknown"), "block", "shop_not_bound", True))
    cases.append(case(5, "店铺绑定/授权边界", "目标店铺授权失效时阻断", [], ctx([expired]), "每天9点同步失效店铺库存", task("new", "inventory_sync", shop_id="pdd_expired"), "block", "authorization_invalid", True))
    cases.append(case(6, "店铺绑定/授权边界", "部分店铺授权失效时部分创建", [], ctx([pdd_a, expired]), "每天9点同步两个店铺库存", task("new", "inventory_sync", shop_id=None, all_shops=True), "partial_create", "authorization_invalid", True))
    cases.append(case(7, "店铺绑定/授权边界", "全部店铺均有效可创建", [], ctx([pdd_a, pdd_b]), "每天9点给全部店铺做巡检", task("new", "inspection", shop_id=None, all_shops=True), "proceed", "none", False))
    cases.append(case(8, "店铺绑定/授权边界", "已删除历史任务不参与重复判断", [task("old_deleted", "inventory_sync", status="deleted")], ctx([pdd_a]), "每天9点同步库存", task("new", "inventory_sync"), "proceed", "none", False))

    # ISV 高级版权限边界 8
    cases.append(case(9, "ISV高级版权限边界", "高级版任务付费店铺允许", [], ctx([pdd_a]), "每天9点做高级铺货", task("new", "auto_listing", requires_sv=True), "proceed", "none", False))
    cases.append(case(10, "ISV高级版权限边界", "高级版任务未付费店铺阻断", [], ctx([unpaid]), "每天9点做高级铺货", task("new", "auto_listing", shop_id="pdd_unpaid", requires_sv=True), "block", "sv_advanced_permission_missing", True))
    cases.append(case(11, "ISV高级版权限边界", "多店部分付费时部分创建", [], ctx([pdd_a, unpaid]), "每天9点给两个店做高级铺货", task("new", "auto_listing", shop_id=None, all_shops=True, requires_sv=True), "partial_create", "sv_advanced_permission_missing", True))
    cases.append(case(12, "ISV高级版权限边界", "ISV接口参数错误阻断", [], ctx([param_error]), "每天9点做高级铺货", task("new", "auto_listing", shop_id="pdd_param_error", requires_sv=True), "block", "sv_advanced_permission_missing", True))
    cases.append(case(13, "ISV高级版权限边界", "ISV接口500不能误判为免费而是阻断校验", [], ctx([api_error]), "每天9点做高级铺货", task("new", "auto_listing", shop_id="pdd_api_error", requires_sv=True), "block", "sv_advanced_permission_missing", True))
    cases.append(case(14, "ISV高级版权限边界", "ISV状态缺失时阻断", [], ctx([missing_paid]), "每天9点做高级铺货", task("new", "auto_listing", shop_id="pdd_missing_paid", requires_sv=True), "block", "sv_advanced_permission_missing", True))
    cases.append(case(15, "ISV高级版权限边界", "普通任务不要求ISV权限", [], ctx([unpaid]), "每天9点同步库存", task("new", "inventory_sync", shop_id="pdd_unpaid", requires_sv=False), "proceed", "none", False))
    cases.append(case(16, "ISV高级版权限边界", "权益文本识别ISV高级版", [], ctx([unpaid]), "帮我创建需要ISV高级版的自动换供任务", {**task("new", "supplier_switch", shop_id="pdd_unpaid"), "entitlement_required": "ISV高级版"}, "block", "sv_advanced_permission_missing", True))

    # 平台能力不支持 5
    cases.append(case(17, "平台能力不支持", "抖音不支持改价时阻断", [], ctx([dy_a]), "每天9点给抖音店铺自动改价", task("new", "price_adjust", shop_id="dy_A"), "block", "platform_capability_missing", True))
    cases.append(case(18, "平台能力不支持", "小红书不支持自动跟单时阻断", [], ctx([xhs_a]), "每天9点给小红书店铺自动跟单", task("new", "auto_follow_order", shop_id="xhs_A"), "block", "platform_capability_missing", True))
    cases.append(case(19, "平台能力不支持", "部分平台支持时部分创建", [], ctx([pdd_a, xhs_a]), "每天9点给所有店铺自动跟单", task("new", "auto_follow_order", shop_id=None, all_shops=True), "partial_create", "platform_capability_missing", True))
    cases.append(case(20, "平台能力不支持", "支持平台的改价进入正常检测", [], ctx([pdd_a]), "每天9点给拼多多店铺自动改价", task("new", "price_adjust"), "proceed", "none", False))
    cases.append(case(21, "平台能力不支持", "未知平台能力不在创建前阻断", [], ctx([shop("custom_A", "custom")]), "每天9点给自定义平台做巡检", task("new", "inspection", shop_id="custom_A"), "proceed", "none", False))

    # 完全重复/语义重复/流程重复 9
    cases.append(case(22, "重复检测", "库存同步完全重复复用", [task("t1", "inventory_sync")], ctx([pdd_a]), "每天9点再同步一次库存", task("new", "inventory_sync"), "reuse_or_update", "complete_duplicate", False))
    cases.append(case(23, "重复检测", "日报语义重复复用", [task("t1", "daily_report", frequency="daily", time="20:00")], ctx([pdd_a]), "每天晚上8点给我经营报告", task("new", "daily_report", time="20:00"), "reuse_or_update", "complete_duplicate", False))
    cases.append(case(24, "重复检测", "不同时间同目标语义重复复用", [task("t1", "inspection", time="09:00")], ctx([pdd_a]), "每天10点再做店铺巡检", task("new", "inspection", time="10:00"), "reuse_or_update", "semantic_duplicate", False))
    cases.append(case(25, "重复检测", "选品被选品加铺货流程覆盖静默合并", [task("t1", "product_selection")], ctx([pdd_a]), "每天9点选品并自动铺货", task("new", "auto_listing"), "silent_merge", "process_duplicate", False))
    cases.append(case(26, "重复检测", "已有铺货流程覆盖新增选品", [task("t1", "auto_listing")], ctx([pdd_a]), "每天9点只做选品", task("new", "product_selection"), "silent_merge", "process_duplicate", False))
    cases.append(case(27, "重复检测", "不同店铺相同任务不重复但同平台排队信息保留", [task("t1", "inventory_sync", shop_id="pdd_B")], ctx([pdd_a, pdd_b]), "每天9点同步A店库存", task("new", "inventory_sync", shop_id="pdd_A"), "proceed", "same_platform_rate_limit", False))
    cases.append(case(28, "重复检测", "暂停中的相同任务仍参与去重", [task("t1", "inventory_sync", status="paused")], ctx([pdd_a]), "每天9点同步库存", task("new", "inventory_sync"), "reuse_or_update", "complete_duplicate", False))
    cases.append(case(29, "重复检测", "平台不同但店铺范围重叠时按店铺识别重复", [task("t1", "inspection", platform="pinduoduo")], ctx([pdd_a]), "每天9点巡检这个店铺", task("new", "inspection"), "reuse_or_update", "complete_duplicate", False))
    cases.append(case(30, "重复检测", "库存管理别名标准化后识别重复", [task("t1", "inventory_sync")], ctx([pdd_a]), "每天9点做库存管理", {**task("new", "库存管理"), "name": "库存管理"}, "reuse_or_update", "complete_duplicate", False))

    # 策略部分重复 6
    cases.append(case(31, "策略部分重复", "铺货利润率阈值变化要求确认", [task("t1", "auto_listing", strategy={"profit_margin_min": 15})], ctx([pdd_a]), "每天9点铺货利润率10%以上商品", task("new", "auto_listing", strategy={"profit_margin_min": 10}), "ask_confirmation", "strategy_partial_duplicate", True))
    cases.append(case(32, "策略部分重复", "铺货最大数量变化要求确认", [task("t1", "auto_listing", strategy={"max_items": 50})], ctx([pdd_a]), "每天9点铺货最多100个商品", task("new", "auto_listing", strategy={"max_items": 100}), "ask_confirmation", "strategy_partial_duplicate", True))
    cases.append(case(33, "策略部分重复", "库存同步字段变化要求确认", [task("t1", "inventory_sync", strategy={"fields": ["stock"]})], ctx([pdd_a]), "每天9点同步库存和价格字段", task("new", "inventory_sync", strategy={"fields": ["stock", "price"]}), "ask_confirmation", "strategy_partial_duplicate", True))
    cases.append(case(34, "策略部分重复", "巡检过滤条件变化要求确认", [task("t1", "inspection", strategy={"filters": {"risk": "high"}})], ctx([pdd_a]), "每天9点巡检全部风险商品", task("new", "inspection", strategy={"filters": {"risk": "all"}}), "ask_confirmation", "strategy_partial_duplicate", True))
    cases.append(case(35, "策略部分重复", "换供商品范围变化要求确认", [task("t1", "supplier_switch", strategy={"product_scope": "low_stock"})], ctx([pdd_a]), "每天9点给全部商品智能换供", task("new", "supplier_switch", strategy={"product_scope": "all"}), "ask_confirmation", "strategy_partial_duplicate", True))
    cases.append(case(36, "策略部分重复", "跟单订单范围变化要求确认", [task("t1", "auto_follow_order", strategy={"order_scope": "unshipped_48h"})], ctx([pdd_a]), "每天9点跟进24小时未发货订单", task("new", "auto_follow_order", strategy={"order_scope": "unshipped_24h"}), "ask_confirmation", "strategy_partial_duplicate", True))

    # 高风险重复 6
    cases.append(case(37, "高风险重复", "改价任务重叠要求确认", [task("t1", "price_adjust", strategy={"discount_percent": 5})], ctx([pdd_a]), "每天10点再自动降价10%", task("new", "price_adjust", time="10:00", strategy={"discount_percent": 10}), "ask_confirmation", "high_risk_duplicate", True))
    cases.append(case(38, "高风险重复", "下架任务重叠要求确认", [task("t1", "auto_delist", strategy={"filters": {"no_sales_days": 30}})], ctx([pdd_a]), "每天10点下架60天无动销商品", task("new", "auto_delist", time="10:00", strategy={"filters": {"no_sales_days": 60}}), "ask_confirmation", "high_risk_duplicate", True))
    cases.append(case(39, "高风险重复", "同一改价任务不同时间也要求确认", [task("t1", "price_adjust", time="09:00", strategy={"min_profit_protection": 20})], ctx([pdd_a]), "每天晚上8点也做低利润商品改价", task("new", "price_adjust", time="20:00", strategy={"min_profit_protection": 15}), "ask_confirmation", "high_risk_duplicate", True))
    cases.append(case(40, "高风险重复", "同店铺批量下架策略不同要求确认", [task("t1", "auto_delist", strategy={"product_scope": "seasonal"})], ctx([pdd_a]), "每天9点下架低分商品", task("new", "auto_delist", strategy={"product_scope": "low_score"}), "ask_confirmation", "high_risk_duplicate", True))
    cases.append(case(41, "高风险重复", "高风险完全重复仍复用不新建", [task("t1", "price_adjust", strategy={"discount_percent": 5})], ctx([pdd_a]), "每天9点自动降价5%", task("new", "price_adjust", strategy={"discount_percent": 5}), "reuse_or_update", "complete_duplicate", False))
    cases.append(case(42, "高风险重复", "不同店铺高风险任务不冲突但同平台排队信息保留", [task("t1", "price_adjust", shop_id="pdd_B", strategy={"discount_percent": 5})], ctx([pdd_a, pdd_b]), "每天9点给A店改价", task("new", "price_adjust", shop_id="pdd_A", strategy={"discount_percent": 5}), "proceed", "same_platform_rate_limit", False))

    # 高频堆积/时间窗口集中 4
    cases.append(case(43, "高频堆积", "每5分钟库存同步需要风险提示", [], ctx([pdd_a]), "每5分钟同步一次库存", task("new", "inventory_sync", frequency="每5分钟", time="", interval_minutes=5), "warn_then_proceed", "high_frequency_accumulation", True))
    cases.append(case(44, "高频堆积", "每10分钟巡检需要风险提示", [], ctx([pdd_a]), "每10分钟巡检店铺风险", task("new", "inspection", frequency="每10分钟", time="", interval_minutes=10), "warn_then_proceed", "high_frequency_accumulation", True))
    cases.append(case(45, "高频堆积", "同平台同时间API任务只记录排队信息", [task("t1", "auto_listing", shop_id="pdd_B", time="09:00")], ctx([pdd_a, pdd_b]), "每天9点同步A店库存", task("new", "inventory_sync", shop_id="pdd_A", time="09:00"), "proceed", "same_platform_rate_limit", False))
    cases.append(case(46, "高频堆积", "同店铺同时间不同商品写任务记录排队", [task("t1", "auto_listing", time="09:00")], ctx([pdd_a]), "每天9点同步库存", task("new", "inventory_sync", time="09:00"), "proceed", "same_platform_rate_limit", False))

    # 通知边界 2
    cases.append(case(47, "通知边界", "微信未绑定时回退通知但任务可创建", [], ctx([pdd_a], wechat_bound=False), "每天20点经营日报发微信通知", task("new", "daily_report", time="20:00", notify={"wechat": True}), "warn_then_proceed", "wechat_not_bound", False))
    cases.append(case(48, "通知边界", "微信已绑定时正常创建通知任务", [], ctx([pdd_a], wechat_bound=True), "每天20点经营日报发微信通知", task("new", "daily_report", time="20:00", notify={"wechat": True}), "proceed", "none", False))

    # 正常可创建 2
    cases.append(case(49, "正常可创建", "已有不同资源任务时可创建巡检", [task("t1", "daily_report", time="20:00")], ctx([pdd_a]), "每天9点巡检店铺风险", task("new", "inspection", time="09:00"), "proceed", "none", False))
    cases.append(case(50, "正常可创建", "不同店铺不同任务可创建", [task("t1", "inventory_sync", shop_id="pdd_B", time="09:00")], ctx([pdd_a, pdd_b]), "每天11点给A店生成经营日报", task("new", "daily_report", shop_id="pdd_A", time="11:00"), "proceed", "none", False))

    return cases


def write_case_files(cases: List[Dict[str, Any]]) -> None:
    FIXTURES_DIR.mkdir(parents=True, exist_ok=True)
    for item in cases:
        case_dir = FIXTURES_DIR / item["case_id"]
        case_dir.mkdir(parents=True, exist_ok=True)
        payload = {
            "case_id": item["case_id"],
            "category": item["category"],
            "title": item["title"],
            "new_lui_request": item["new_lui_request"],
            "initial_tasks": item["initial_tasks"],
            "existing_tasks": item["existing_tasks"],
            "user_context": item["user_context"],
            "proposed_task": item["proposed_task"],
            "expected_decision": item["expected_decision"],
            "expected_reason_code": item["expected_reason_code"],
            "expected_prompt_required": item["expected_prompt_required"],
            "cleanup_required": item["cleanup_required"],
            "cleanup_policy": item["cleanup_policy"],
        }
        (case_dir / "input.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_index_files(cases: List[Dict[str, Any]]) -> None:
    csv_path = ROOT / "test_cases_50.csv"
    # CSV 给表格软件直接打开时需要 BOM 才能稳定识别中文编码。
    with csv_path.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "case_id",
                "category",
                "title",
                "new_lui_request",
                "initial_task_count",
                "expected_decision",
                "expected_reason_code",
                "expected_prompt_required",
                "fixture_path",
            ],
        )
        writer.writeheader()
        for item in cases:
            writer.writerow({
                "case_id": item["case_id"],
                "category": item["category"],
                "title": item["title"],
                "new_lui_request": item["new_lui_request"],
                "initial_task_count": len(item["initial_tasks"]),
                "expected_decision": item["expected_decision"],
                "expected_reason_code": item["expected_reason_code"],
                "expected_prompt_required": str(item["expected_prompt_required"]).lower(),
                "fixture_path": f"fixtures/{item['case_id']}/input.json",
            })

    lines = [
        "# 定时任务冲突检测 50 组 Benchmark",
        "",
        "每组测试均包含 `initial_tasks`，用于模拟用户已经配置过的定时任务；runner 在每个 case 前写入临时任务池，在每个 case 后删除临时任务池，避免污染下一组。",
        "",
    ]
    for item in cases:
        lines.extend([
            f"## {item['case_id']}｜{item['category']}｜{item['title']}",
            "",
            f"- 已有任务数：{len(item['initial_tasks'])}",
            f"- 新 LUI 请求：{item['new_lui_request']}",
            f"- 预期决策：`{item['expected_decision']}`",
            f"- 预期原因码：`{item['expected_reason_code']}`",
            f"- 是否需要提示/确认：{'是' if item['expected_prompt_required'] else '否'}",
            f"- Fixture：`fixtures/{item['case_id']}/input.json`",
            "",
        ])
    (ROOT / "test_prompts_50.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    cases = build_cases()
    if len(cases) != 50:
        raise RuntimeError(f"expected 50 cases, got {len(cases)}")
    write_case_files(cases)
    write_index_files(cases)
    print(json.dumps({"generated_cases": len(cases), "fixtures_dir": str(FIXTURES_DIR)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
