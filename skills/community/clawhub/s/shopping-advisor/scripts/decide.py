#!/usr/bin/env python3
from common import read_stdin_json, write_json, write_error


AFTER_SALES_PRIORITY = {
    "jd": 3,
    "tmall": 2,
    "taobao": 1,
    "pdd": 1,
    "manual": 0,
    "other": 0,
}


def _priced_candidates(candidates):
    priced = []
    for candidate in candidates:
        price = ((candidate.get("price") or {}).get("final_price"))
        if isinstance(price, (int, float)):
            priced.append((candidate, price))
    return priced


def _comparison_relation(candidate):
    return ((candidate.get("comparison") or {}).get("relation")) or "same_item"


def _confidence_from_missing(missing_fields, base):
    penalty = min(len(missing_fields) * 0.08, 0.3)
    return max(0.25, round(base - penalty, 2))


def _best_after_sales_candidate(priced):
    ranked = sorted(
        priced,
        key=lambda item: (
            -AFTER_SALES_PRIORITY.get(item[0].get("source") or "other", 0),
            item[1],
        ),
    )
    return ranked[0][0] if ranked else None


def main() -> None:
    try:
        context = read_stdin_json()
        candidates = context.get("candidates") or []
        query = context.get("query") or {}
        budget = (query.get("budget") or {}).get("max")
        priorities = query.get("priorities") or []
        missing_fields = context.get("meta", {}).get("missing_fields", [])

        if not candidates:
            report = {
                "summary": {
                    "worth_buying": None,
                    "confidence": 0.3,
                    "decision": "当前还没有足够候选，先补商品或关键信息，再做购买判断。",
                    "recommended_action": "gather_more_info"
                },
                "pitfalls": ["没有候选时，不要直接下单。"],
                "alternative_directions": ["先明确预算、场景和至少一个候选。"],
                "missing_info": ["candidates"]
            }
            write_json(report)
            return

        if len(candidates) == 1:
            candidate = candidates[0]
            price = ((candidate.get("price") or {}).get("final_price"))
            over_budget = budget is not None and price is not None and price > budget
            report = {
                "summary": {
                    "worth_buying": False if over_budget else None,
                    "confidence": _confidence_from_missing(missing_fields, 0.55),
                    "decision": "这单可以继续看，但还需要对照项或更多关键信息，才能更稳地下结论。",
                    "recommended_action": "gather_more_info" if not over_budget else "change_direction"
                },
                "pitfalls": ["只有单个候选时，容易因为缺少对照而高估性价比。"],
                "alternative_directions": ["补一个更低价候选和一个更稳妥候选再比较。"],
                "missing_info": ["comparison_baseline"]
            }
            write_json(report)
            return

        comparison_pool = [candidate for candidate in candidates if _comparison_relation(candidate) != "not_directly_comparable"]
        priced = _priced_candidates(comparison_pool or candidates)
        if not priced:
            report = {
                "summary": {
                    "worth_buying": None,
                    "confidence": _confidence_from_missing(missing_fields, 0.4),
                    "decision": "当前候选缺少价格信息，暂时不建议直接下单，先补价格再比较。",
                    "recommended_action": "gather_more_info"
                },
                "pitfalls": ["没有价格就无法判断低价和溢价是否成立。"],
                "alternative_directions": ["先补每个候选的实际到手价。"],
                "missing_info": [*missing_fields, "price"]
            }
            write_json(report)
            return

        priced_sorted = sorted(priced, key=lambda item: item[1])
        lowest_candidate, lowest_price = priced_sorted[0]
        second_price = priced_sorted[1][1] if len(priced_sorted) > 1 else None
        within_budget = [item for item in priced_sorted if budget is None or item[1] <= budget]
        after_sales_candidate = _best_after_sales_candidate(within_budget or priced_sorted)

        rankings = {
            "lowest_price": lowest_candidate.get("id"),
        }
        if after_sales_candidate:
            rankings["best_after_sales"] = after_sales_candidate.get("id")

        value_candidate = lowest_candidate
        if after_sales_candidate and after_sales_candidate.get("id") != lowest_candidate.get("id"):
            after_sales_price = next(price for candidate, price in priced_sorted if candidate.get("id") == after_sales_candidate.get("id"))
            if lowest_price > 0 and (after_sales_price - lowest_price) / lowest_price <= 0.1:
                value_candidate = after_sales_candidate
        rankings["best_value"] = value_candidate.get("id")

        non_comparable_count = len([candidate for candidate in candidates if _comparison_relation(candidate) == "not_directly_comparable"])
        similar_count = len([candidate for candidate in candidates if _comparison_relation(candidate) == "similar_item"])
        all_over_budget = budget is not None and not within_budget
        confidence = _confidence_from_missing(missing_fields, 0.72)
        if non_comparable_count:
            confidence = max(0.3, round(confidence - 0.1, 2))
        elif similar_count:
            confidence = max(0.35, round(confidence - 0.05, 2))

        if all_over_budget:
            decision = f"按你的预算，当前候选都偏贵，暂时不建议直接下单。账面最低价是 {lowest_candidate.get('id')}，但也超出预算，更建议先换方向或降规格。"
            action = "change_direction"
            worth_buying = False
        else:
            if non_comparable_count >= max(1, len(candidates) - 1):
                decision = "当前候选里有明显规格或套餐差异，暂时不建议直接按最低价下结论，先确认是不是同款同配置。"
                action = "gather_more_info"
            elif similar_count:
                decision = f"当前候选里包含近似款，价格只能作参考，不能直接把最低价当最终结论。当前更偏向先看 {value_candidate.get('id')}，但最好先确认版本和系列差异。"
                action = "gather_more_info"
            elif value_candidate.get("id") == lowest_candidate.get("id"):
                decision = f"如果你就是追求到手最低价，优先选 {lowest_candidate.get('id')}；目前它也更像默认的性价比选择。"
                action = "compare_more"
            else:
                decision = f"如果你追求到手最低价，优先选 {lowest_candidate.get('id')}；如果你愿意多花一点换更稳妥的体验，优先选 {value_candidate.get('id')}。"
                action = "compare_more"

            if budget is not None and within_budget:
                budget_ids = ", ".join(candidate.get("id") for candidate, _ in within_budget)
                decision += f" 按你的预算，当前真正可选的是 {budget_ids}。"

            if missing_fields:
                decision += " 但因为还缺少部分关键信息，这个结论更适合作为初步购买建议。"
                action = "gather_more_info"
            worth_buying = None

        pitfalls = [
            "低价不一定等于同款同配置。",
            "套餐和版本差异可能会放大表面价差。"
        ]
        if non_comparable_count:
            pitfalls.append("部分候选存在明显规格或套餐冲突，不适合直接按价格硬比较。")
        elif similar_count:
            pitfalls.append("当前候选里包含近似款，低价不一定代表真正更值。")
        if second_price is not None and abs(second_price - lowest_price) / max(lowest_price, 1) <= 0.05:
            pitfalls.append("当前候选价差很小，不要只因为便宜一点就忽略售后和适配性。")
        if missing_fields:
            pitfalls.append("当前还缺少关键信息，结论可能会随着补充信息而变化。")

        directions = [
            "确认是否同款同配置后，再决定是否为更低价切换。"
        ]
        if all_over_budget:
            directions.append("优先看更低价位版本，或重新收窄预算与核心需求。")
        elif "性价比" not in priorities and missing_fields:
            directions.append("补充你的优先级后，结论会更贴近你的真实购买标准。")

        report = {
            "summary": {
                "worth_buying": worth_buying,
                "confidence": confidence,
                "decision": decision,
                "recommended_action": action
            },
            "rankings": rankings,
            "pitfalls": pitfalls,
            "alternative_directions": directions,
            "missing_info": missing_fields
        }
        write_json(report)
    except Exception as exc:
        write_error(str(exc))


if __name__ == "__main__":
    main()
