#!/usr/bin/env python3
"""
勇哥餐饮创业选址评估计算器
根据勇哥自测表自动计算选址评分并给出建议
"""

import json
import sys

def evaluate_location(data):
    """
    评估选址得分
    data: dict 包含各项评估指标
    """
    result = {
        "basic_check": {"score": 0, "max": 100, "passed": False},
        "traffic": {"score": 0, "max": 55, "items": []},
        "facade": {"score": 0, "max": 40, "items": []},
        "competition": {"score": 0, "max": 33, "items": []},
        "cost": {"score": 0, "max": 51, "items": []},
        "risk": {"score": 0, "max": 45, "items": []},
        "total_score": 0,
        "max_total": 324,
        "rating": "",
        "suggestion": ""
    }
    
    # 1. 基础必过项检查
    basic_items = [
        "property_clear", "license", "ventilation", "utilities",
        "fire_safety", "landlord", "demolition_risk"
    ]
    basic_passed = all(data.get(item, False) for item in basic_items)
    result["basic_check"]["passed"] = basic_passed
    result["basic_check"]["score"] = 100 if basic_passed else 0
    
    if not basic_passed:
        result["suggestion"] = "基础必过项未通过，建议直接放弃该选址。"
        return result
    
    # 2. 人流客群评分
    traffic_score = 0
    if data.get("peak_hours_flow", False):
        traffic_score += 10
    
    customer_match = data.get("customer_match", "none")
    if customer_match == "match":
        traffic_score += 10
    elif customer_match == "average":
        traffic_score += 5
    
    daily_flow = data.get("daily_flow", 0)
    if daily_flow >= 5000:
        traffic_score += 15
    elif daily_flow >= 4000:
        traffic_score += 12
    elif daily_flow >= 2000:
        traffic_score += 10
    elif daily_flow >= 800:
        traffic_score += 8
    
    if data.get("real_flow", False):
        traffic_score += 10
    if data.get("occupancy_60", False):
        traffic_score += 5
    if data.get("fixed_customers", False):
        traffic_score += 10
    
    result["traffic"]["score"] = min(traffic_score, 55)
    
    # 3. 门头动线评分
    facade_score = 0
    if data.get("wide_sign", False):
        facade_score += 10
    if data.get("flow_direction", False):
        facade_score += 10
    if data.get("no_steps", False):
        facade_score += 5
    if data.get("parking", False):
        facade_score += 5
    if data.get("golden_corner", False):
        facade_score += 10
    
    result["facade"]["score"] = min(facade_score, 40)
    
    # 4. 竞争业态评分
    comp_score = 0
    if data.get("food_district", False):
        comp_score += 10
    if data.get("competitors_le3", False):
        comp_score += 5
    if data.get("no_price_war", False):
        comp_score += 10
    if data.get("no_cold_business", False):
        comp_score += 5
    if data.get("matching_hours", False):
        comp_score += 3
    
    result["competition"]["score"] = min(comp_score, 33)
    
    # 5. 成本回本评分
    cost_score = 0
    if data.get("rent_15_percent", False):
        cost_score += 15
    if data.get("reasonable_transfer", False):
        cost_score += 5
    if data.get("transparent_fees", False):
        cost_score += 3
    if data.get("deposit_le2", False):
        cost_score += 3
    if data.get("contract_3y", False):
        cost_score += 10
    if data.get("profitable", False):
        cost_score += 15
    
    result["cost"]["score"] = min(cost_score, 51)
    
    # 6. 风险避雷评分
    risk_score = 0
    if data.get("no_complaint", False):
        risk_score += 5
    if data.get("no_dead_end", False):
        risk_score += 10
    if data.get("not_single_peak", False):
        risk_score += 10
    if data.get("no_construction", False):
        risk_score += 10
    if data.get("clean_environment", False):
        risk_score += 5
    if data.get("no_bad_neighbors", False):
        risk_score += 5
    
    result["risk"]["score"] = min(risk_score, 45)
    
    # 计算总分
    total = (
        result["basic_check"]["score"] +
        result["traffic"]["score"] +
        result["facade"]["score"] +
        result["competition"]["score"] +
        result["cost"]["score"] +
        result["risk"]["score"]
    )
    result["total_score"] = total
    
    # 评级和建议
    if total >= 280:
        result["rating"] = "A级"
        result["suggestion"] = "优质旺铺，果断租！条件合适尽快签约。"
    elif total >= 230:
        result["rating"] = "B级"
        result["suggestion"] = "可谈条件租，建议争取租金优惠或更长合同期。"
    elif total >= 180:
        result["rating"] = "C级"
        result["suggestion"] = "谨慎考虑，风险较高。建议继续寻找更优选址。"
    else:
        result["rating"] = "D级"
        result["suggestion"] = "直接放弃，别赌。该选址存在明显短板。"
    
    return result


def evaluate_startup(data):
    """
    评估创业可行性
    """
    result = {
        "fund": {"score": 0, "items": []},
        "location": {"score": 0, "items": []},
        "product": {"score": 0, "items": []},
        "payback": {"score": 0, "items": []},
        "operation": {"score": 0, "items": []},
        "risk": {"score": 0, "items": []},
        "final_decision": {"yes_count": 0, "total": 3},
        "can_start": False,
        "suggestion": ""
    }
    
    # 最终决策3题
    yes_count = 0
    if data.get("payback_le12", False):
        yes_count += 1
    if data.get("rent_le20", False):
        yes_count += 1
    if data.get("can_manage_3m", False):
        yes_count += 1
    
    result["final_decision"]["yes_count"] = yes_count
    
    if yes_count == 3:
        result["can_start"] = True
        result["suggestion"] = "可以开，成功率高！"
    elif yes_count == 2:
        result["can_start"] = True
        result["suggestion"] = "谨慎开，必须优化后再行动。"
    else:
        result["can_start"] = False
        result["suggestion"] = "别开，90%亏。建议重新评估或寻找其他项目。"
    
    return result


def print_report(location_result, startup_result=None):
    """打印评估报告"""
    print("=" * 50)
    print("勇哥餐饮选址评估报告")
    print("=" * 50)
    
    # 基础检查
    print("\n【基础必过项】")
    if location_result["basic_check"]["passed"]:
        print("✓ 全部通过")
    else:
        print("✗ 未通过，建议放弃该选址")
        print(f"\n最终建议：{location_result['suggestion']}")
        return
    
    # 各项得分
    print("\n【分项得分】")
    print(f"人流客群：{location_result['traffic']['score']}/55")
    print(f"门头动线：{location_result['facade']['score']}/40")
    print(f"竞争业态：{location_result['competition']['score']}/33")
    print(f"成本回本：{location_result['cost']['score']}/51")
    print(f"风险避雷：{location_result['risk']['score']}/45")
    
    # 总分和评级
    print("\n【综合评估】")
    print(f"总得分：{location_result['total_score']}/{location_result['max_total']}")
    print(f"评级：{location_result['rating']}")
    print(f"\n建议：{location_result['suggestion']}")
    
    # 创业评估
    if startup_result:
        print("\n" + "=" * 50)
        print("创业可行性评估")
        print("=" * 50)
        print(f"\n最终决策题（3题）：{startup_result['final_decision']['yes_count']}/3 通过")
        print(f"能否开店：{'可以' if startup_result['can_start'] else '不建议'}")
        print(f"建议：{startup_result['suggestion']}")
    
    print("\n" + "=" * 50)


if __name__ == "__main__":
    # 示例用法
    if len(sys.argv) > 1:
        # 从JSON文件读取数据
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        location_data = data.get("location", {})
        startup_data = data.get("startup", {})
        
        location_result = evaluate_location(location_data)
        startup_result = evaluate_startup(startup_data) if startup_data else None
        
        print_report(location_result, startup_result)
        
        # 输出JSON结果
        output = {
            "location": location_result,
            "startup": startup_result
        }
        print("\n【JSON输出】")
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print("用法: python evaluate.py <json_file>")
        print("\n示例JSON格式：")
        print(json.dumps({
            "location": {
                "property_clear": True,
                "license": True,
                "daily_flow": 2500,
                "customer_match": "match",
                "rent_15_percent": True
            },
            "startup": {
                "payback_le12": True,
                "rent_le20": True,
                "can_manage_3m": True
            }
        }, ensure_ascii=False, indent=2))
