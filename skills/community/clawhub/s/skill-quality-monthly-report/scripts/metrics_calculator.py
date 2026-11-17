#!/usr/bin/env python3
"""
质量指标计算脚本（月报版）

功能：根据输入的质量测试数据，计算关键质量指标，支持多月对比分析
输出：JSON 格式的计算结果
"""

import json
import argparse
import sys
from typing import Dict, Any, List, Optional


def calculate_pass_rate(total_cases: int, passed_cases: int) -> float:
    """计算通过率"""
    if total_cases == 0:
        return 0.0
    return round((passed_cases / total_cases) * 100, 2)


def calculate_defect_density(total_cases: int, defect_count: int) -> float:
    """计算缺陷密度（缺陷数/测试用例数）"""
    if total_cases == 0:
        return 0.0
    return round((defect_count / total_cases) * 100, 2)


def calculate_defect_severity_ratio(defects: Dict[str, int]) -> Dict[str, float]:
    """计算各严重级别缺陷占比"""
    total = sum(defects.values())
    if total == 0:
        return {severity: 0.0 for severity in defects}
    
    return {
        severity: round((count / total) * 100, 2)
        for severity, count in defects.items()
    }


def calculate_monthly_comparison(current_data: Dict[str, Any], previous_data: Dict[str, Any]) -> Dict[str, Any]:
    """计算月度对比（本月 vs 上月）"""
    comparison = {}
    
    # 通过率对比
    current_pass = calculate_pass_rate(current_data["test_cases"]["total"], current_data["test_cases"]["passed"])
    previous_pass = calculate_pass_rate(previous_data["test_cases"]["total"], previous_data["test_cases"]["passed"])
    comparison["pass_rate"] = {
        "current": current_pass,
        "previous": previous_pass,
        "change": round(current_pass - previous_pass, 2),
        "trend": "上升" if current_pass > previous_pass else "下降" if current_pass < previous_pass else "持平"
    }
    
    # 缺陷数对比
    current_defects = current_data["defects"]["total"]
    previous_defects = previous_data["defects"]["total"]
    comparison["defect_count"] = {
        "current": current_defects,
        "previous": previous_defects,
        "change": current_defects - previous_defects,
        "trend": "增加" if current_defects > previous_defects else "减少" if current_defects < previous_defects else "持平"
    }
    
    # 测试用例数对比
    current_cases = current_data["test_cases"]["total"]
    previous_cases = previous_data["test_cases"]["total"]
    comparison["test_cases"] = {
        "current": current_cases,
        "previous": previous_cases,
        "change": current_cases - previous_cases,
        "trend": "增加" if current_cases > previous_cases else "减少" if current_cases < previous_cases else "持平"
    }
    
    return comparison


def calculate_trend_analysis(monthly_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """计算趋势分析（3个月以上）"""
    if len(monthly_data) < 2:
        return {"note": "数据不足，无法进行趋势分析（需要至少2个月数据）"}
    
    trend = {
        "months": len(monthly_data),
        "pass_rate_trend": [],
        "defect_trend": [],
        "cases_trend": []
    }
    
    for month_data in monthly_data:
        month_id = month_data.get("month", "未知")
        pass_rate = calculate_pass_rate(month_data["test_cases"]["total"], month_data["test_cases"]["passed"])
        defect_count = month_data["defects"]["total"]
        case_count = month_data["test_cases"]["total"]
        
        trend["pass_rate_trend"].append({"month": month_id, "value": pass_rate})
        trend["defect_trend"].append({"month": month_id, "value": defect_count})
        trend["cases_trend"].append({"month": month_id, "value": case_count})
    
    # 计算平均变化率
    if len(monthly_data) >= 3:
        first_pass = trend["pass_rate_trend"][0]["value"]
        last_pass = trend["pass_rate_trend"][-1]["value"]
        avg_pass_change = round((last_pass - first_pass) / (len(monthly_data) - 1), 2) if len(monthly_data) > 1 else 0
        
        first_defect = trend["defect_trend"][0]["value"]
        last_defect = trend["defect_trend"][-1]["value"]
        avg_defect_change = round((last_defect - first_defect) / (len(monthly_data) - 1), 2) if len(monthly_data) > 1 else 0
        
        trend["average_change"] = {
            "pass_rate": avg_pass_change,
            "defect_count": avg_defect_change
        }
    
    return trend


def calculate_pdca_metrics(pdca_items: List[Dict[str, Any]]) -> Dict[str, Any]:
    """计算 PDCA 统计指标"""
    if not pdca_items:
        return {"total_items": 0, "completed_items": 0, "completion_rate": 0.0}
    
    total = len(pdca_items)
    completed = sum(1 for item in pdca_items if item.get("status") == "已完成")
    completion_rate = round((completed / total) * 100, 2) if total > 0 else 0.0
    
    # 按阶段统计
    stage_stats = {
        "plan": sum(1 for item in pdca_items if item.get("plan")),
        "do": sum(1 for item in pdca_items if item.get("do")),
        "check": sum(1 for item in pdca_items if item.get("check")),
        "act": sum(1 for item in pdca_items if item.get("act"))
    }
    
    return {
        "total_items": total,
        "completed_items": completed,
        "in_progress_items": total - completed,
        "completion_rate": completion_rate,
        "stage_stats": stage_stats
    }


def load_json_file(file_path: str) -> Dict[str, Any]:
    """加载 JSON 文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"错误：文件 '{file_path}' 不存在", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"错误：JSON 格式无效 - {e}", file=sys.stderr)
        sys.exit(1)


def load_multiple_json_files(file_paths: str) -> List[Dict[str, Any]]:
    """加载多个 JSON 文件（逗号分隔）"""
    files = file_paths.split(",")
    data_list = []
    for file_path in files:
        file_path = file_path.strip()
        if file_path:
            data_list.append(load_json_file(file_path))
    return data_list


def validate_data(data: Dict[str, Any]) -> bool:
    """验证数据格式"""
    required_fields = ["test_cases", "defects", "work_summary", "month"]
    for field in required_fields:
        if field not in data:
            print(f"错误：缺少必需字段 '{field}'", file=sys.stderr)
            return False
    
    test_cases = data["test_cases"]
    if "total" not in test_cases or "passed" not in test_cases:
        print("错误：test_cases 缺少 total 或 passed 字段", file=sys.stderr)
        return False
    
    defects = data["defects"]
    if "total" not in defects:
        print("错误：defects 缺少 total 字段", file=sys.stderr)
        return False
    
    return True


def calculate_metrics(data: Dict[str, Any], previous_data_list: List[Dict[str, Any]] = None) -> Dict[str, Any]:
    """计算所有质量指标"""
    test_cases = data["test_cases"]
    defects = data["defects"]
    month = data.get("month", "未知")
    
    # 基础指标
    metrics = {
        "month": month,
        "pass_rate": calculate_pass_rate(test_cases["total"], test_cases["passed"]),
        "fail_count": test_cases["total"] - test_cases["passed"],
        "defect_density": calculate_defect_density(test_cases["total"], defects["total"]),
        "defect_severity_ratio": {}
    }
    
    # 缺陷严重级别占比
    if "by_severity" in defects and isinstance(defects["by_severity"], dict):
        metrics["defect_severity_ratio"] = calculate_defect_severity_ratio(defects["by_severity"])
    
    # 附加信息
    metrics["summary"] = {
        "total_cases": test_cases["total"],
        "total_defects": defects["total"],
        "work_items": len(data.get("work_summary", [])),
        "temporary_works": len(data.get("temporary_works", []))
    }
    
    # PDCA 统计
    if "pdca_items" in data and isinstance(data["pdca_items"], list):
        metrics["pdca_metrics"] = calculate_pdca_metrics(data["pdca_items"])
    
    # 月度对比分析
    if previous_data_list:
        if len(previous_data_list) == 1:
            # 单月对比
            metrics["comparison"] = calculate_monthly_comparison(data, previous_data_list[0])
        else:
            # 多月趋势分析
            metrics["trend_analysis"] = calculate_trend_analysis(previous_data_list + [data])
    
    return metrics


def main():
    parser = argparse.ArgumentParser(description='质量指标计算工具（月报版）')
    parser.add_argument('--input', required=True, help='本月数据 JSON 文件路径')
    parser.add_argument('--previous-data', help='历史数据文件路径（支持多个文件，逗号分隔）')
    parser.add_argument('--output', help='输出文件路径（默认输出到控制台）')
    
    args = parser.parse_args()
    
    # 加载本月数据
    data = load_json_file(args.input)
    
    # 验证数据
    if not validate_data(data):
        sys.exit(1)
    
    # 加载历史数据（可选）
    previous_data_list = None
    if args.previous_data:
        previous_data_list = load_multiple_json_files(args.previous_data)
        for prev_data in previous_data_list:
            if not validate_data(prev_data):
                print(f"警告：历史数据 {prev_data.get('month', '未知')} 格式无效，跳过该数据", file=sys.stderr)
                previous_data_list.remove(prev_data)
        
        if not previous_data_list:
            print("警告：所有历史数据格式无效，跳过对比分析", file=sys.stderr)
    
    # 计算指标
    metrics = calculate_metrics(data, previous_data_list)
    
    # 输出结果
    result = json.dumps(metrics, ensure_ascii=False, indent=2)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f"指标计算完成，结果已保存到 {args.output}")
    else:
        print(result)


if __name__ == "__main__":
    main()
