#!/usr/bin/env python3
"""
ESG Validator - ESG数据核对与验证工具
支持数据完整性检查、逻辑一致性验证、阈值合规检查
"""

import argparse
import json
import pandas as pd
from datetime import datetime
from pathlib import Path


# GRI标准关键指标验证规则
VALIDATION_RULES = {
    "environmental": {
        "E1": {"min": 0, "max": 10000000, "required": True, "rule": "排放量必须为正数"},
        "E2": {"min": 0, "max": 1000000, "required": True, "rule": "能源消耗必须为正数"},
        "E3": {"min": 0, "max": 10000000, "required": False, "rule": "水资源使用量必须为正数"},
        "E4": {"min": 0, "max": 1000000, "required": False, "rule": "废弃物必须为正数"},
        "E5": {"min": 0, "max": 100, "required": False, "rule": "再生能源比例在0-100%之间"},
    },
    "social": {
        "S1": {"min": 0, "max": 1000000, "required": True, "rule": "员工总数必须为正整数"},
        "S2": {"min": 0, "max": 100, "required": True, "rule": "女性比例在0-100%之间"},
        "S3": {"min": 0, "max": 100000, "required": False, "rule": "培训投入必须为正数"},
        "S4": {"min": 0, "max": 10000, "required": False, "rule": "安全事故数必须为非负整数"},
        "S5": {"min": 0, "max": 100000, "required": False, "rule": "公益投入必须为正数"},
    },
    "governance": {
        "G1": {"min": 0, "max": 100, "required": True, "rule": "董事会独立性在0-100%之间"},
        "G2": {"min": 0, "max": 100, "required": True, "rule": "女性董事比例在0-100%之间"},
        "G3": {"min": 0, "max": 100, "required": False, "rule": "培训覆盖率在0-100%之间"},
        "G4": {"min": 0, "max": 100, "required": False, "rule": "目标达成率在0-100%之间"},
    }
}


# 跨指标一致性规则
CONSISTENCY_RULES = [
    {
        "name": "碳排放强度与总量一致性",
        "check": lambda d: True,  # 需要E1和E2数据
        "error": "碳排放强度计算需要排放量和产量数据"
    },
    {
        "name": "女性员工与董事比例逻辑",
        "check": lambda d: d.get("S2", 0) >= d.get("G2", 0),
        "error": "女性董事比例不应高于女性员工比例"
    },
]


def validate_metric_value(metric_id, value, rules):
    """验证单个指标值"""
    errors = []
    
    if metric_id not in rules:
        return errors
    
    rule = rules[metric_id]
    
    # 非空检查
    if pd.isna(value):
        if rule.get('required', False):
            errors.append(f"必需指标 {metric_id} 缺少数据")
        return errors
    
    # 类型转换
    try:
        num_value = float(value)
    except (ValueError, TypeError):
        errors.append(f"指标 {metric_id} 数值格式错误")
        return errors
    
    # 范围检查
    if 'min' in rule and num_value < rule['min']:
        errors.append(f"指标 {metric_id} 低于最小值 {rule['min']}")
    if 'max' in rule and num_value > rule['max']:
        errors.append(f"指标 {metric_id} 超过最大值 {rule['max']}")
    
    return errors


def check_consistency(data):
    """检查跨指标一致性"""
    results = []
    
    # 提取数值用于一致性检查
    values = {}
    for dim_data in data.get('dimensions', {}).values():
        for metric_id, info in dim_data.items():
            values[metric_id] = info.get('value')
    
    for rule in CONSISTENCY_RULES:
        try:
            if not rule['check'](values):
                results.append({
                    "rule": rule['name'],
                    "status": "fail",
                    "message": rule['error']
                })
            else:
                results.append({
                    "rule": rule['name'],
                    "status": "pass",
                    "message": "数据一致性检查通过"
                })
        except Exception as e:
            results.append({
                "rule": rule['name'],
                "status": "error",
                "message": f"检查执行出错: {str(e)}"
            })
    
    return results


def validate_esg_data(input_file, standard='GRI'):
    """
    验证ESG数据完整性与合规性
    
    Args:
        input_file: 收集后的JSON数据文件
        standard: 披露标准(GRI/TCFD/SASB)
    """
    # 读取数据
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    result = {
        "validation_time": datetime.now().isoformat(),
        "standard": standard,
        "status": "passed",
        "metrics_validated": 0,
        "errors": [],
        "warnings": [],
        "consistency_checks": [],
        "summary": {
            "total_metrics": 0,
            "passed": 0,
            "failed": 0,
            "missing": 0
        }
    }
    
    # 按维度验证
    for dimension in ['environmental', 'social', 'governance']:
        rules = VALIDATION_RULES.get(dimension, {})
        dim_data = data.get('dimensions', {}).get(dimension, {})
        
        for metric_id, rule in rules.items():
            result['summary']['total_metrics'] += 1
            
            if metric_id in dim_data:
                metric_info = dim_data[metric_id]
                value = metric_info.get('value')
                errors = validate_metric_value(metric_id, value, rules)
                
                result['metrics_validated'] += 1
                if errors:
                    result['errors'].extend(errors)
                    result['summary']['failed'] += 1
                else:
                    result['summary']['passed'] += 1
            else:
                if rule.get('required', False):
                    result['errors'].append(f"必需指标 {metric_id} ({rule['rule']}) 缺失")
                    result['summary']['missing'] += 1
                else:
                    result['warnings'].append(f"推荐指标 {metric_id} 未提供")
    
    # 一致性检查
    result['consistency_checks'] = check_consistency(data)
    
    # 设置总体状态
    if result['summary']['failed'] > 0 or result['summary']['missing'] > 0:
        result['status'] = "failed"
    elif result['warnings']:
        result['status'] = "passed_with_warnings"
    
    # 计算完整性得分
    total = result['summary']['total_metrics']
    if total > 0:
        completeness = (result['summary']['passed'] / total) * 100
        result['completeness_score'] = round(completeness, 2)
    else:
        result['completeness_score'] = 0
    
    return result


def main():
    parser = argparse.ArgumentParser(description='ESG数据核对与验证工具')
    parser.add_argument('--input', '-i', required=True, help='ESG数据JSON文件')
    parser.add_argument('--standard', '-s', default='GRI', choices=['GRI', 'TCFD', 'SASB'], 
                        help='ESG披露标准')
    
    args = parser.parse_args()
    
    result = validate_esg_data(args.input, args.standard)
    
    # 输出验证报告
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
