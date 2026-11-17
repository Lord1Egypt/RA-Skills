"""
LPA审核结果分析与统计脚本
接收审核结果数据，进行多维度分析并输出统计结果
"""

import argparse
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from collections import Counter, defaultdict


def load_data(checklist_path: str, results_path: str) -> tuple:
    """加载清单和结果数据"""
    with open(checklist_path, "r", encoding="utf-8") as f:
        checklist = json.load(f)
    
    with open(results_path, "r", encoding="utf-8") as f:
        results = json.load(f)
    
    return checklist, results


def analyze_findings(checklist: Dict, results: Dict) -> Dict[str, Any]:
    """分析审核发现"""
    
    findings = results.get("findings", [])
    items = {item["item_id"]: item for item in checklist["items"]}
    
    # 初始化统计
    stats = {
        "total": len(findings),
        "pass": 0,
        "fail": 0,
        "na": 0,
        "pending": 0,
    }
    
    # 按分类统计
    category_stats = defaultdict(lambda: {"total": 0, "pass": 0, "fail": 0, "na": 0})
    
    # 问题列表
    issues = []
    
    for finding in findings:
        item_id = finding.get("item_id")
        status = finding.get("status", "").lower()
        
        stats[status] = stats.get(status, 0) + 1
        
        # 获取分类信息
        if item_id in items:
            category = items[item_id]["category"]
            category_name = items[item_id]["category_name"]
            category_stats[category]["total"] += 1
            category_stats[category][status] += 1
            category_stats[category]["name"] = category_name
        
        # 记录不合格项
        if status == "fail":
            issue = {
                "item_id": item_id,
                "name": items[item_id]["name"] if item_id in items else "未知",
                "category": items[item_id]["category"] if item_id in items else "未知",
                "evidence": finding.get("evidence", ""),
                "note": finding.get("note", ""),
            }
            issues.append(issue)
    
    # 计算通过率
    applicable = stats["total"] - stats["na"]
    pass_rate = round(stats["pass"] / applicable * 100, 2) if applicable > 0 else 0
    
    # 按问题严重程度排序
    issues.sort(key=lambda x: x["category"])
    
    return {
        "basic_stats": stats,
        "pass_rate": pass_rate,
        "category_distribution": dict(category_stats),
        "issues": issues,
    }


def generate_trend_data(historical_results: List[Dict]) -> Dict:
    """生成趋势数据（当有多次审核历史时）"""
    
    if not historical_results:
        return {}
    
    trend = {
        "periods": [],
        "pass_rates": [],
        "total_findings": [],
    }
    
    for result in historical_results:
        if "audit_info" in result:
            period = result["audit_info"].get("audit_time", "")[:7]
        else:
            period = f"审核{len(trend['periods']) + 1}"
        
        # 计算通过率
        findings = result.get("findings", [])
        pass_count = sum(1 for f in findings if f.get("status", "").lower() == "pass")
        applicable = sum(1 for f in findings if f.get("status", "").lower() in ["pass", "fail"])
        rate = round(pass_count / applicable * 100, 2) if applicable > 0 else 0
        
        trend["periods"].append(period)
        trend["pass_rates"].append(rate)
        trend["total_findings"].append(len(findings))
    
    return trend


def generate_recommendations(analysis: Dict) -> List[Dict]:
    """根据分析结果生成改进建议"""
    
    recommendations = []
    
    # 基于通过率建议
    if analysis["pass_rate"] < 85:
        recommendations.append({
            "priority": "高",
            "area": "整体水平",
            "suggestion": "通过率偏低，建议开展专项质量提升活动，加强一线作业标准培训"
        })
    elif analysis["pass_rate"] < 95:
        recommendations.append({
            "priority": "中",
            "area": "整体水平",
            "suggestion": "通过率有待提升，建议针对薄弱环节进行改善"
        })
    
    # 基于分类问题建议
    category_issues = {}
    for issue in analysis["issues"]:
        cat = issue["category"]
        category_issues[cat] = category_issues.get(cat, 0) + 1
    
    if category_issues:
        top_category = max(category_issues, key=category_issues.get)
        cat_mapping = {
            "EQP": ("设备设施", "建议检查设备维护计划和点检执行情况"),
            "MAT": ("物料管理", "建议审查物料存储条件和批次管理流程"),
            "MTH": ("作业方法", "建议复核作业标准与实际操作的一致性"),
            "PPE": ("人员资质", "建议加强人员培训与技能认证管理"),
            "ENV": ("环境安全", "建议完善现场5S管理和安全防护措施"),
            "MSR": ("测量系统", "建议开展MSA分析和量具校准核查"),
        }
        if top_category in cat_mapping:
            name, suggestion = cat_mapping[top_category]
            recommendations.append({
                "priority": "高" if category_issues[top_category] >= 3 else "中",
                "area": name,
                "suggestion": f"该分类问题最多({category_issues[top_category]}项)，{suggestion}"
            })
    
    return recommendations


def create_analysis_report(checklist: Dict, results: Dict, analysis: Dict) -> Dict:
    """生成完整分析报告"""
    
    audit_info = results.get("audit_info", {})
    checklist_info = checklist.get("checklist_info", {})
    
    report = {
        "report_info": {
            "report_id": f"AR-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "generated_time": datetime.now().isoformat(),
        },
        "audit_summary": {
            "audit_id": audit_info.get("audit_id", ""),
            "auditor": audit_info.get("auditor", ""),
            "audit_time": audit_info.get("audit_time", ""),
            "level": audit_info.get("level", checklist_info.get("level", "")),
            "department": audit_info.get("department", checklist_info.get("department", "")),
        },
        "statistics": analysis["basic_stats"],
        "pass_rate": analysis["pass_rate"],
        "category_analysis": _format_category_analysis(analysis["category_distribution"]),
        "top_issues": analysis["issues"][:10] if len(analysis["issues"]) > 10 else analysis["issues"],
        "recommendations": generate_recommendations(analysis),
    }
    
    return report


def _format_category_analysis(category_dist: Dict) -> List[Dict]:
    """格式化分类分析"""
    result = []
    for cat, data in category_dist.items():
        applicable = data["total"] - data.get("na", 0)
        pass_rate = round(data["pass"] / applicable * 100, 2) if applicable > 0 else 0
        result.append({
            "category": cat,
            "name": data.get("name", cat),
            "total": data["total"],
            "pass": data["pass"],
            "fail": data["fail"],
            "pass_rate": pass_rate,
        })
    return sorted(result, key=lambda x: x["fail"], reverse=True)


def main():
    parser = argparse.ArgumentParser(description="LPA审核结果分析工具")
    parser.add_argument("--checklist", required=True,
                        help="审核清单文件路径")
    parser.add_argument("--results", required=True,
                        help="审核结果数据文件路径")
    parser.add_argument("--output", required=True,
                        help="分析结果输出路径(JSON格式)")
    
    args = parser.parse_args()
    
    # 加载数据
    checklist, results = load_data(args.checklist, args.results)
    
    # 分析结果
    analysis = analyze_findings(checklist, results)
    
    # 生成报告
    report = create_analysis_report(checklist, results, analysis)
    
    # 输出结果
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    # 输出摘要
    print(json.dumps({
        "status": "success",
        "report_id": report["report_info"]["report_id"],
        "pass_rate": report["pass_rate"],
        "total_items": report["statistics"]["total"],
        "pass_items": report["statistics"]["pass"],
        "fail_items": report["statistics"]["fail"],
        "top_issues_count": len(report["top_issues"]),
        "recommendations_count": len(report["recommendations"]),
        "output_file": args.output,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
