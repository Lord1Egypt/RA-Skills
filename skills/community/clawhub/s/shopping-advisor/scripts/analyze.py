#!/usr/bin/env python3
from common import read_stdin_json


def _candidate_by_id(candidates, candidate_id):
    for candidate in candidates:
        if candidate.get("id") == candidate_id:
            return candidate
    return None


def _candidate_label(candidates, candidate_id):
    candidate = _candidate_by_id(candidates, candidate_id)
    if not candidate:
        return candidate_id or "未知候选"
    title = candidate.get("title") or candidate_id
    return f"{candidate_id} ({title})"


def main() -> None:
    payload = read_stdin_json()
    context = payload.get("shopping_context") or {}
    report = payload.get("decision_report") or {}
    query = context.get("query") or {}
    candidates = context.get("candidates") or []
    summary = report.get("summary") or {}
    pitfalls = report.get("pitfalls") or []
    directions = report.get("alternative_directions") or []
    rankings = report.get("rankings") or {}
    missing_info = report.get("missing_info") or []

    print("## Purchase Goal")
    print(f"- Category: {query.get('category') or '未提供'}")
    print(f"- Scenario: {query.get('scenario') or '未提供'}")
    print(f"- Priorities: {', '.join(query.get('priorities') or []) or '未提供'}")
    print()

    print("## Candidate Summary")
    if not candidates:
        print("- No candidates yet")
    else:
        relation_labels = {
            "same_item": "可直接比价",
            "similar_item": "近似款，仅参考",
            "not_directly_comparable": "不可直接比价",
        }
        for candidate in candidates:
            price = ((candidate.get("price") or {}).get("final_price"))
            source = candidate.get("source") or "unknown"
            relation = ((candidate.get("comparison") or {}).get("relation")) or "same_item"
            line = f"- {candidate.get('id')}: {candidate.get('title')}"
            if price is not None:
                line += f" (¥{price})"
            line += f" [{source}] [{relation_labels.get(relation, relation)}]"
            print(line)
    print()

    print("## Decision Comparison")
    if rankings:
        lowest = rankings.get("lowest_price")
        after_sales = rankings.get("best_after_sales")
        best_value = rankings.get("best_value")
        if lowest:
            print(f"- Lowest price: {_candidate_label(candidates, lowest)}")
        if after_sales:
            print(f"- After-sales tilt: {_candidate_label(candidates, after_sales)}")
        if best_value:
            print(f"- Best value: {_candidate_label(candidates, best_value)}")
    else:
        print("- 信息不足，暂时无法形成稳定比较。")
    print()

    print("## Why the Price Gap Exists")
    lowest = rankings.get("lowest_price")
    best_value = rankings.get("best_value")
    non_comparable = [candidate for candidate in candidates if ((candidate.get("comparison") or {}).get("relation")) == "not_directly_comparable"]
    if non_comparable:
        print("- 本次价格比较只应参考可直接比较的候选；有些候选存在规格或套餐差异。")
    if lowest and best_value and lowest != best_value:
        print(f"- 账面最低价是 {_candidate_label(candidates, lowest)}，但更综合的默认选择更偏向 {_candidate_label(candidates, best_value)}。")
        print("- 这通常意味着价差不大，但省心程度或稳妥度更值得考虑。")
    elif lowest:
        print(f"- 当前看 {_candidate_label(candidates, lowest)} 同时占到价格优势，暂时更像默认优先项。")
    else:
        print("- 目前还缺少足够价格信息，无法稳定解释差价。")
    print()

    print("## Pitfalls to Watch")
    if pitfalls:
        for item in pitfalls:
            print(f"- {item}")
    else:
        print("- 暂无")
    print()

    print("## Better Alternative Directions")
    if directions:
        for item in directions:
            print(f"- {item}")
    else:
        print("- 暂无")
    print()

    if missing_info:
        print("## Missing Info")
        for item in missing_info:
            print(f"- {item}")
        print()

    print("## Final Conclusion")
    print(f"- {summary.get('decision') or '先补信息，再决定是否下单。'}")

    similar_candidates = [candidate for candidate in candidates if ((candidate.get("comparison") or {}).get("relation")) == "similar_item"]
    non_comparable_candidates = [candidate for candidate in candidates if ((candidate.get("comparison") or {}).get("relation")) == "not_directly_comparable"]

    if similar_candidates:
        print("- 注意：本次结论里包含近似款参考，适合帮助你缩小范围，但不适合直接把最低价当成最终答案。")
    if non_comparable_candidates:
        print("- 注意：有些候选存在明显规格或套餐差异，应先确认是否同款同配置，再决定要不要按价格比较。")


if __name__ == "__main__":
    main()
