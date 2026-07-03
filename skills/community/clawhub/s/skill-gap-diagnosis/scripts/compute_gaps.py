#!/usr/bin/env python3
"""
業務缺口計算腳本

輸入：各 Tool 返回的原始數據聚合 + 代理人畫像 + 業務規則
輸出：排序後的 gapIndicators 列表

用法：
    python compute_gaps.py --performance data.json --campaign data.json ...
或直接導入：
    from compute_gaps import compute_gaps
    result = compute_gaps(...)
"""

import os
import json
import math
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)

API_BASE_URL = os.getenv("API_BASE_URL", "https://api.onepartner.example.com")


def _parse_date(date_str: Optional[str]) -> Optional[datetime]:
    """解析日期字符串"""
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return None


def _compute_days_remaining(deadline_str: Optional[str]) -> Optional[int]:
    """計算剩餘天數"""
    deadline = _parse_date(deadline_str)
    if not deadline:
        return None
    remaining = (deadline - datetime.now()).days
    return max(0, remaining)


def _compute_urgency_tag(days_remaining: Optional[int]) -> str:
    """計算緊急度標籤"""
    if days_remaining is None:
        return "常規"
    if days_remaining <= 7:
        return "緊急"
    elif days_remaining <= 30:
        return "重要"
    return "常規"


def _compute_ease_tag(
    gap_amount: float,
    avg_daily_capacity: float,
    days_remaining: Optional[int]
) -> Optional[str]:
    """計算容易度標籤"""
    if days_remaining is None or avg_daily_capacity <= 0:
        return None
    if gap_amount < avg_daily_capacity * days_remaining:
        return "容易"
    return None


def _extract_performance_gaps(perf_data: Optional[Dict]) -> List[Dict]:
    """從業績數據中提取缺口信息"""
    gaps = []
    if not perf_data:
        return gaps

    personal_premium = perf_data.get("personalPremium")
    personal_policy_num = perf_data.get("personalPolicyNum")

    if personal_premium is not None and personal_policy_num and float(personal_policy_num) > 0:
        avg_premium = float(personal_premium) / float(personal_policy_num)
        perf_data["_avgPremiumPerCase"] = avg_premium

    return gaps


def _extract_campaign_gaps(campaign_data: Optional[Dict]) -> List[Dict]:
    """從競賽數據中提取缺口信息"""
    gaps = []
    if not campaign_data or "competitionList" not in campaign_data:
        return gaps

    for comp in campaign_data["competitionList"]:
        gap_indicators = comp.get("gapIndicators", [])
        for indicator in gap_indicators:
            target_val = indicator.get("targetVal")
            actual_val = indicator.get("actualVal")
            gap_val = indicator.get("gapVal")
            deadline = indicator.get("deadline")

            if gap_val is None or (target_val is not None and actual_val is not None
                                   and float(gap_val) <= 0):
                continue

            unit = indicator.get("unit", "AMOUNT")
            gap_name = f"{comp.get('competitionName', '')}{indicator.get('indicatorName', '')}"

            if unit == "RANK":
                continue

            days_remaining = _compute_days_remaining(deadline)
            urgency_tag = _compute_urgency_tag(days_remaining)

            gap_item = {
                "gapName": gap_name,
                "gapType": "CAMPAIGN",
                "deadlineDate": deadline,
                "daysRemaining": days_remaining,
                "targetAmount": float(target_val) if target_val is not None else None,
                "actualAmount": float(actual_val) if actual_val is not None else None,
                "gapAmount": float(gap_val) if gap_val is not None else 0,
                "gapUnit": "HKD" if unit == "AMOUNT" else unit,
                "convertedGapAmount": float(gap_val) if gap_val is not None else 0,
                "urgencyTag": urgency_tag,
                "easeTag": None,
                "requiredCases": None,
                "currentRank": None,
                "targetRank": None,
                "detailUrl": None
            }
            gaps.append(gap_item)

    return gaps


def _extract_honor_gaps(honor_data: Optional[Dict]) -> List[Dict]:
    """從榮譽數據中提取缺口信息"""
    gaps = []
    if not honor_data or "honorList" not in honor_data:
        return gaps

    for honor in honor_data["honorList"]:
        if honor.get("isQualified"):
            continue

        gap_amt = honor.get("gapAmt")
        if gap_amt is None or float(gap_amt) <= 0:
            continue

        deadline = honor.get("deadlineDate")
        days_remaining = _compute_days_remaining(deadline)
        urgency_tag = _compute_urgency_tag(days_remaining)

        items = honor.get("items", [])
        target_fyc = None
        actual_fyc = None
        for item in items:
            if item.get("itemRole") == "TARGET_FYC":
                target_fyc = item.get("itemValue")
            elif item.get("itemRole") == "ACTUAL_FYC":
                actual_fyc = item.get("itemValue")

        gap_item = {
            "gapName": honor.get("honorName", ""),
            "gapType": "HONOR",
            "deadlineDate": deadline,
            "daysRemaining": days_remaining,
            "targetAmount": float(target_fyc) if target_fyc is not None else None,
            "actualAmount": float(actual_fyc) if actual_fyc is not None else None,
            "gapAmount": float(gap_amt),
            "gapUnit": "HKD",
            "convertedGapAmount": float(gap_amt),
            "urgencyTag": urgency_tag,
            "easeTag": None,
            "requiredCases": None,
            "currentRank": None,
            "targetRank": None,
            "detailUrl": None
        }
        gaps.append(gap_item)

    return gaps


def _compute_avg_premium_per_case(perf_data: Optional[Dict]) -> Optional[float]:
    """計算件均保費"""
    if not perf_data:
        return None
    personal_premium = perf_data.get("personalPremium")
    personal_policy_num = perf_data.get("personalPolicyNum")
    if personal_premium is not None and personal_policy_num is not None:
        policy_num = float(personal_policy_num)
        if policy_num >= 0.5:
            return float(personal_premium) / policy_num
    return None


def _compute_avg_daily_capacity(perf_data: Optional[Dict]) -> float:
    """計算代理人日均產能"""
    if not perf_data:
        return 0.0
    personal_premium = perf_data.get("personalPremium")
    if personal_premium is not None and float(personal_premium) > 0:
        return float(personal_premium) / 180.0

    company_ytd_premium = perf_data.get("companyYtdPremium")
    active_agent_count = perf_data.get("activeAgentCount")
    if (company_ytd_premium is not None and active_agent_count
            and int(active_agent_count) > 0):
        return float(company_ytd_premium) / int(active_agent_count) / 180.0

    return 0.0


def _build_diagnosis(
    perf_data: Optional[Dict],
    renewal_data: Optional[Dict],
    customer_growth_data: Optional[Dict],
    skill_data: Optional[Dict]
) -> Dict:
    """構建診斷對象"""
    diagnosis = {
        "pendingPremium": None,
        "avgPremiumPerCase": None,
        "companyAvgPremiumPerCase": None,
        "conversionRate": None,
        "companyAvgConversionRate": None,
        "caseConversionRate": None,
        "companyAvgCaseConversionRate": None,
        "newClientCount": None,
        "churnRate": None,
        "companyAvgChurnRate": None,
        "skillGap": []
    }

    if perf_data:
        diagnosis["pendingPremium"] = perf_data.get("pendingAmt")
        diagnosis["avgPremiumPerCase"] = _compute_avg_premium_per_case(perf_data)
        diagnosis["companyAvgPremiumPerCase"] = None
        diagnosis["conversionRate"] = perf_data.get("conversionRate")
        diagnosis["companyAvgConversionRate"] = perf_data.get("companyAvgConversionRate")
        diagnosis["caseConversionRate"] = perf_data.get("policyConversionRate")
        diagnosis["companyAvgCaseConversionRate"] = perf_data.get("companyAvgPolicyConversionRate")

    if renewal_data:
        diagnosis["personalRenewalRate"] = renewal_data.get("personalRenewalRate")

    if customer_growth_data:
        diagnosis["newClientCount"] = customer_growth_data.get("newCustNum")
        diagnosis["churnRate"] = customer_growth_data.get("churnRate")
        diagnosis["companyAvgChurnRate"] = customer_growth_data.get("avgChurnRate")

    if skill_data:
        skill_gaps = []
        ai_drill = skill_data.get("aiDrill")
        if ai_drill:
            usage_num = ai_drill.get("usageNum")
            if usage_num is not None and int(usage_num) == 0:
                skill_gaps.append("AI陪練未使用")
            completion_rate = ai_drill.get("completionRate")
            if completion_rate is not None and float(completion_rate) < 50:
                skill_gaps.append("AI陪練完成率低")

        university = skill_data.get("university")
        if university:
            mandatory_completed = university.get("mandatoryCompleted")
            mandatory_total = university.get("mandatoryTotal")
            if (mandatory_completed is not None and mandatory_total is not None
                    and int(mandatory_completed) < int(mandatory_total)):
                skill_gaps.append("必修課未完成")

        diagnosis["skillGap"] = skill_gaps

    return diagnosis


def _sort_gaps(gaps: List[Dict]) -> List[Dict]:
    """按優先級排序缺口列表"""
    urgency_order = {"緊急": 0, "重要": 1, "常規": 2}

    def sort_key(gap):
        urgency = urgency_order.get(gap.get("urgencyTag", "常規"), 2)
        gap_amount = gap.get("gapAmount", 0) or 0
        return (urgency, -gap_amount)

    return sorted(gaps, key=sort_key)


def compute_gaps(
    performance_data: Optional[Dict] = None,
    campaign_data: Optional[Dict] = None,
    honor_data: Optional[Dict] = None,
    renewal_data: Optional[Dict] = None,
    customer_growth_data: Optional[Dict] = None,
    skill_data: Optional[Dict] = None,
    assessment_data: Optional[Dict] = None,
    new_allowance_data: Optional[Dict] = None,
    agent_profile: Optional[Dict] = None,
    business_rules: Optional[Dict] = None
) -> Dict:
    """
    計算業務缺口主函數

    Args:
        performance_data: Data_Performance 返回數據
        campaign_data: Data_Campaign 返回數據
        honor_data: Data_Honor 返回數據
        renewal_data: Data_Renewal 返回數據
        customer_growth_data: Data_CustomerGrowth 返回數據
        skill_data: Data_Skill 返回數據
        assessment_data: Data_Assessment 返回數據
        new_allowance_data: Data_NewAllowance 返回數據
        agent_profile: 代理人畫像
        business_rules: 業務規則

    Returns:
        包含 gapIndicators、diagnosis、knowledgeRetrievalHints 的字典
    """
    now = datetime.now()
    today_str = now.strftime("%Y-%m-%d")

    all_gaps = []

    all_gaps.extend(_extract_performance_gaps(performance_data))
    all_gaps.extend(_extract_campaign_gaps(campaign_data))
    all_gaps.extend(_extract_honor_gaps(honor_data))

    avg_daily_capacity = _compute_avg_daily_capacity(performance_data)
    avg_premium_per_case = _compute_avg_premium_per_case(performance_data)

    for gap in all_gaps:
        gap_amount = gap.get("gapAmount", 0) or 0
        days_remaining = gap.get("daysRemaining")

        if avg_daily_capacity > 0 and days_remaining is not None:
            gap["easeTag"] = _compute_ease_tag(gap_amount, avg_daily_capacity, days_remaining)

        if avg_premium_per_case and avg_premium_per_case > 0 and gap_amount > 0:
            gap["requiredCases"] = math.ceil(gap_amount / avg_premium_per_case)

    sorted_gaps = _sort_gaps(all_gaps)

    diagnosis = _build_diagnosis(
        performance_data, renewal_data, customer_growth_data, skill_data
    )

    knowledge_hints = []
    if campaign_data and "competitionList" in campaign_data:
        for comp in campaign_data["competitionList"]:
            hint = comp.get("knowledgeQueryHint")
            if hint:
                knowledge_hints.append(hint)

    if honor_data and "honorList" in honor_data:
        for honor in honor_data["honorList"]:
            if not honor.get("isQualified"):
                knowledge_hints.append(f"{honor.get('honorName', '')}達標攻略")

    return {
        "startDate": performance_data.get("startDate", today_str) if performance_data else today_str,
        "endDate": performance_data.get("endDate", today_str) if performance_data else today_str,
        "dataAsOfDate": today_str,
        "gapIndicators": sorted_gaps,
        "diagnosis": diagnosis,
        "knowledgeRetrievalHints": knowledge_hints
    }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="業務缺口計算")
    parser.add_argument("--performance", type=str, help="業績數據 JSON 文件路徑")
    parser.add_argument("--campaign", type=str, help="競賽數據 JSON 文件路徑")
    parser.add_argument("--honor", type=str, help="榮譽數據 JSON 文件路徑")
    parser.add_argument("--renewal", type=str, help="續保率數據 JSON 文件路徑")
    parser.add_argument("--customer-growth", type=str, help="客戶增長數據 JSON 文件路徑")
    parser.add_argument("--skill", type=str, help="技能數據 JSON 文件路徑")
    parser.add_argument("--output", type=str, help="輸出 JSON 文件路徑")

    args = parser.parse_args()

    def load_json(path):
        if not path:
            return None
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    result = compute_gaps(
        performance_data=load_json(args.performance),
        campaign_data=load_json(args.campaign),
        honor_data=load_json(args.honor),
        renewal_data=load_json(args.renewal),
        customer_growth_data=load_json(args.customer_growth),
        skill_data=load_json(args.skill)
    )

    output_json = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output_json)
        logger.info(f"結果已寫入 {args.output}")
    else:
        print(output_json)
