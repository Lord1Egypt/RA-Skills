#!/usr/bin/env python3
"""
CP控制计划风险预警分析脚本
功能：基于FMEA方法进行风险评估，识别潜在变异点，生成预警建议
"""

import argparse
import json
import sys
from pathlib import Path

try:
    import pandas as pd
    import numpy as np
except ImportError:
    print("ERROR: Missing required packages. Install: pip install pandas numpy")
    sys.exit(1)


# 严重度评分标准
SEVERITY_TABLE = {
    "无影响": 1,
    "轻微影响": 2,
    "一般影响": 3,
    "较严重": 4,
    "严重": 5,
    "很严重": 6,
    "非常严重": 7,
    "极端严重": 8,
    "最严重": 9,
    "最最严重": 10
}

# 频度评分标准
OCCURRENCE_TABLE = {
    "几乎不可能": 1,
    "极低": 2,
    "很低": 3,
    "低": 4,
    "中等偏低": 5,
    "中等": 6,
    "中等偏高": 7,
    "高": 8,
    "很高": 9,
    "几乎肯定": 10
}

# 探测度评分标准
DETECTION_TABLE = {
    "几乎肯定": 1,
    "很高": 2,
    "高": 3,
    "较高": 4,
    "中等偏高": 5,
    "中等": 6,
    "较低": 7,
    "低": 8,
    "很低": 9,
    "几乎不可能": 10
}


def load_analysis_result(json_path):
    """加载数据分析结果"""
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"ERROR: 读取分析结果失败 - {str(e)}")
        sys.exit(1)


def calculate_rpn(severity, occurrence, detection):
    """计算RPN（风险优先数）"""
    return severity * occurrence * detection


def assess_from_cpk(cpk_value):
    """基于CPK值评估风险参数"""
    if cpk_value >= 1.67:
        return {"severity": 2, "occurrence": 2, "detection": 2, "level": "低风险"}
    elif cpk_value >= 1.33:
        return {"severity": 3, "occurrence": 3, "detection": 3, "level": "中低风险"}
    elif cpk_value >= 1.0:
        return {"severity": 5, "occurrence": 5, "detection": 5, "level": "中等风险"}
    elif cpk_value >= 0.67:
        return {"severity": 7, "occurrence": 7, "detection": 6, "level": "高风险"}
    else:
        return {"severity": 9, "occurrence": 8, "detection": 7, "level": "严重风险"}


def detect_variation_points(characteristics):
    """检测潜在变异点"""
    variation_points = []
    
    for char in characteristics:
        char_name = char.get("characteristic", "Unknown")
        cpk = char.get("cpk", 0)
        mean = char.get("mean", 0)
        std = char.get("std", 0)
        lsl = char.get("lsl")
        usl = char.get("usl")
        
        issues = []
        
        # CPK不足检测
        if cpk < 1.0:
            issues.append({
                "type": "过程能力不足",
                "detail": f"CPK={cpk} < 1.0，过程能力严重不足",
                "priority": "高"
            })
        
        # 偏移检测
        if lsl and usl:
            center = (lsl + usl) / 2
            offset = abs(mean - center) / ((usl - lsl) / 2) * 100
            if offset > 20:
                issues.append({
                    "type": "过程偏移",
                    "detail": f"过程均值偏离中心{(offset):.1f}%，需调整",
                    "priority": "中"
                })
        
        # 变异系数检测
        if mean != 0:
            cv = (std / abs(mean)) * 100
            if cv > 30:
                issues.append({
                    "type": "变异过大",
                    "detail": f"变异系数={cv:.1f}%，波动较大",
                    "priority": "中"
                })
        
        # 边界接近检测
        if lsl and usl:
            tolerance = usl - lsl
            dist_to_lsl = abs(mean - lsl)
            dist_to_usl = abs(usl - mean)
            min_dist = min(dist_to_lsl, dist_to_usl)
            
            if std > 0:
                sigma_to_limit = min_dist / (3 * std)
                if sigma_to_limit < 1.5:
                    issues.append({
                        "type": "边界风险",
                        "detail": f"距离规格限仅{sigma_to_limit:.2f}σ，存在超差风险",
                        "priority": "高"
                    })
        
        if issues:
            variation_points.append({
                "characteristic": char_name,
                "issues": issues
            })
    
    return variation_points


def generate_control_recommendations(characteristics, threshold=100):
    """生成控制措施建议"""
    recommendations = []
    
    for char in characteristics:
        char_name = char.get("characteristic", "Unknown")
        cpk = char.get("cpk", 0)
        level = char.get("capability_level", "未知")
        
        rec = {
            "characteristic": char_name,
            "current_status": level,
            "cpk": cpk,
            "recommendations": []
        }
        
        if cpk < 0.67:
            rec["priority"] = "立即改善"
            rec["recommendations"] = [
                "启动专项改善项目",
                "进行根本原因分析（5Why、鱼骨图）",
                "实施防错装置（Poka-Yoke）",
                "增加检验频次",
                "考虑工艺重新设计"
            ]
        elif cpk < 1.0:
            rec["priority"] = "重点关注"
            rec["recommendations"] = [
                "加强过程监控",
                "分析变差来源",
                "优化工艺参数",
                "实施SPC控制图监控"
            ]
        elif cpk < 1.33:
            rec["priority"] = "一般关注"
            rec["recommendations"] = [
                "保持现有控制",
                "定期审核控制有效性",
                "监控趋势变化"
            ]
        else:
            rec["priority"] = "正常"
            rec["recommendations"] = [
                "维持当前控制水平",
                "定期维护设备",
                "关注人机料法环变化"
            ]
        
        recommendations.append(rec)
    
    return recommendations


def main():
    parser = argparse.ArgumentParser(description="CP控制计划风险预警分析脚本")
    parser.add_argument("--input", required=True, help="输入数据分析结果JSON文件路径")
    parser.add_argument("--method", choices=["fmea", "spc", "both"], default="both", help="分析方法：fmea/spc/both")
    parser.add_argument("--threshold", type=int, default=100, help="RPN阈值，高于此值需重点关注")
    parser.add_argument("--output", required=True, help="输出JSON文件路径")
    
    args = parser.parse_args()
    
    # 加载数据
    data = load_analysis_result(args.input)
    characteristics = data.get("characteristics", [])
    
    if not characteristics:
        print("WARNING: 未找到质量特性数据")
        characteristics = []
    
    # FMEA风险分析
    fmea_results = []
    if args.method in ["fmea", "both"]:
        for char in characteristics:
            char_name = char.get("characteristic", "Unknown")
            
            # 基于CPK评估风险
            cpk = char.get("cpk", 0)
            if cpk > 0:
                assessment = assess_from_cpk(cpk)
                rpn = calculate_rpn(
                    assessment["severity"],
                    assessment["occurrence"],
                    assessment["detection"]
                )
                
                fmea_entry = {
                    "item": char_name,
                    "potential_failure_mode": f"{char_name}超出规格限",
                    "potential_effect": f"产品不合格，造成质量损失",
                    "severity": assessment["severity"],
                    "severity_desc": list(SEVERITY_TABLE.keys())[assessment["severity"]-1],
                    "potential_cause": "过程变异",
                    "occurrence": assessment["occurrence"],
                    "occurrence_desc": list(OCCURRENCE_TABLE.keys())[assessment["occurrence"]-1],
                    "current_controls": "首件检验/过程监控",
                    "detection": assessment["detection"],
                    "detection_desc": list(DETECTION_TABLE.keys())[assessment["detection"]-1],
                    "rpn": rpn,
                    "risk_level": assessment["level"],
                    "action_required": rpn >= args.threshold
                }
                fmea_results.append(fmea_entry)
        
        # 按RPN排序
        fmea_results.sort(key=lambda x: x["rpn"], reverse=True)
    
    # SPC变异点检测
    variation_points = []
    if args.method in ["spc", "both"]:
        variation_points = detect_variation_points(characteristics)
    
    # 生成控制建议
    recommendations = generate_control_recommendations(characteristics, args.threshold)
    
    # 生成预警摘要
    high_risk_count = sum(1 for r in fmea_results if r["rpn"] >= args.threshold)
    critical_count = sum(1 for r in fmea_results if r["risk_level"] in ["高风险", "严重风险"])
    
    result = {
        "status": "success",
        "analysis_method": args.method,
        "rpn_threshold": args.threshold,
        "fmea_analysis": {
            "total_items": len(fmea_results),
            "high_risk_items": high_risk_count,
            "critical_items": critical_count,
            "results": fmea_results[:20]  # 限制输出数量
        },
        "variation_points": {
            "total": len(variation_points),
            "points": variation_points
        },
        "recommendations": recommendations,
        "summary": {
            "overall_risk": "高" if critical_count > 0 else ("中" if high_risk_count > 0 else "低"),
            "priority_actions": [
                r["characteristic"] for r in recommendations 
                if r["priority"] in ["立即改善", "重点关注"]
            ],
            "control_frequency_suggestion": "连续" if critical_count > 0 else ("每小时" if high_risk_count > 0 else "每班次")
        }
    }
    
    # 保存结果
    try:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"SUCCESS: 风险分析结果已保存至 {args.output}")
    except Exception as e:
        print(f"ERROR: 保存结果失败 - {str(e)}")
        sys.exit(1)
    
    # 打印摘要
    print(f"\n=== 风险预警摘要 ===")
    print(f"分析方法: {args.method}")
    print(f"分析项目数: {len(fmea_results)}")
    print(f"高风险项(RPN≥{args.threshold}): {high_risk_count} 个")
    print(f"严重风险项: {critical_count} 个")
    print(f"变异点数量: {len(variation_points)} 个")
    print(f"整体风险等级: {result['summary']['overall_risk']}")
    if result['summary']['priority_actions']:
        print(f"优先处理项: {', '.join(result['summary']['priority_actions'][:5])}")
    print(f"建议控制频次: {result['summary']['control_frequency_suggestion']}")


if __name__ == "__main__":
    main()
