#!/usr/bin/env python3
"""
抽样结果分析器
生成统计分析报告，评估抽样质量
"""

import argparse
import json
import os
from collections import Counter
from datetime import datetime

try:
    import pandas as pd
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False


def load_json(path):
    """加载JSON文件"""
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def is_numeric(value):
    """判断是否为数值"""
    if value is None:
        return False
    if isinstance(value, (int, float)):
        return True
    if isinstance(value, str):
        try:
            float(value)
            return True
        except:
            return False
    return False


def analyze_categorical_field(values):
    """分析分类字段"""
    valid_values = [v for v in values if v is not None]
    distribution = Counter(valid_values)
    
    return {
        "type": "categorical",
        "distribution": dict(distribution),
        "unique_count": len(distribution),
        "missing_count": len(values) - len(valid_values),
        "missing_rate": round((len(values) - len(valid_values)) / len(values) * 100, 2) if values else 0
    }


def analyze_numeric_field(values):
    """分析数值字段"""
    valid_values = []
    for v in values:
        if v is not None:
            try:
                valid_values.append(float(v))
            except:
                pass
    
    if not valid_values:
        return {
            "type": "numeric",
            "count": 0,
            "missing_count": len(values)
        }
    
    result = {
        "type": "numeric",
        "count": len(valid_values),
        "mean": round(sum(valid_values) / len(valid_values), 4),
        "min": min(valid_values),
        "max": max(valid_values),
        "missing_count": len(values) - len(valid_values),
        "missing_rate": round((len(values) - len(valid_values)) / len(values) * 100, 2)
    }
    
    if HAS_NUMPY:
        result["std"] = round(float(np.std(valid_values)), 4)
        result["median"] = round(float(np.median(valid_values)), 4)
    else:
        sorted_vals = sorted(valid_values)
        mid = len(sorted_vals) // 2
        result["median"] = sorted_vals[mid] if len(sorted_vals) % 2 else \
                          (sorted_vals[mid-1] + sorted_vals[mid]) / 2
    
    return result


def analyze_field(field_name, values):
    """分析单个字段"""
    if is_numeric(values[0] if values else None):
        return analyze_numeric_field(values)
    else:
        return analyze_categorical_field(values)


def generate_report_id():
    """生成报告ID"""
    return f"RPT{datetime.now().strftime('%Y%m%d%H%M%S')}"


def assess_quality(field_analysis, sample_count, original_count):
    """评估抽样质量"""
    # 检查缺失率
    high_missing_fields = []
    for field, analysis in field_analysis.items():
        if analysis.get('missing_rate', 0) > 5:
            high_missing_fields.append(field)
    
    coverage_rate = round(sample_count / original_count * 100, 2) if original_count > 0 else 0
    avg_missing_rate = sum(a.get('missing_rate', 0) for a in field_analysis.values()) / len(field_analysis)
    
    # 判断代表性
    if coverage_rate >= 50 and avg_missing_rate < 5:
        representativeness = "良好"
        conclusion = f"样本对总体具有良好的代表性，抽样质量满足检验要求"
    elif coverage_rate >= 20 and avg_missing_rate < 10:
        representativeness = "一般"
        conclusion = f"样本对总体代表性一般，建议关注抽样结果的应用场景"
    else:
        representativeness = "需改进"
        conclusion = f"样本量或数据质量存在不足，建议重新抽样或补充数据"
    
    return {
        "coverage_rate": coverage_rate,
        "avg_missing_rate": round(avg_missing_rate, 2),
        "high_missing_fields": high_missing_fields,
        "representativeness": representativeness,
        "conclusion": conclusion
    }


def generate_recommendations(field_analysis, quality_assessment):
    """生成建议"""
    recommendations = []
    
    if quality_assessment['representativeness'] == '良好':
        recommendations.append("本次抽样符合统计要求，可继续进行质量检验")
    else:
        recommendations.append("建议重新评估抽样方案或增加样本量")
    
    # 针对缺失率的建议
    for field in quality_assessment.get('high_missing_fields', []):
        recommendations.append(f"字段'{field}'缺失率较高，建议补充数据或标记处理")
    
    # 分类字段分布建议
    for field, analysis in field_analysis.items():
        if analysis['type'] == 'categorical' and analysis.get('unique_count', 0) > 20:
            recommendations.append(f"字段'{field}'类别过多({analysis['unique_count']}类)，建议适当归并")
    
    if not recommendations:
        recommendations.append("数据质量良好，可按计划进行后续检验工作")
    
    return recommendations


def main():
    parser = argparse.ArgumentParser(description='抽样结果分析器')
    parser.add_argument('--samples', required=True, help='抽样结果JSON文件路径')
    parser.add_argument('--original', help='原始数据文件路径(用于对比分析)')
    parser.add_argument('--output', required=True, help='报告输出路径')
    
    args = parser.parse_args()
    
    # 加载抽样结果
    if not os.path.exists(args.samples):
        print(json.dumps({"error": f"文件不存在: {args.samples}"}))
        return
    
    sampling_result = load_json(args.samples)
    
    # 分析样本数据
    samples = sampling_result.get('samples', [])
    if not samples:
        print(json.dumps({"error": "样本数据为空"}))
        return
    
    # 获取字段列表
    fields = set()
    for sample in samples:
        fields.update(sample.keys())
    fields = sorted(fields - {'index', 'original_index', '_stratum', '_interval', '_cluster'})
    
    # 分析每个字段
    field_analysis = {}
    for field in fields:
        values = [s.get(field) for s in samples]
        field_analysis[field] = analyze_field(field, values)
    
    # 加载原始数据进行对比
    original_count = sampling_result['data_summary']['total_records']
    
    if args.original and os.path.exists(args.original):
        try:
            if args.original.endswith('.csv'):
                df = pd.read_csv(args.original, encoding='utf-8')
            elif args.original.endswith('.xlsx'):
                df = pd.read_excel(args.original)
            else:
                df = None
            
            if df is not None:
                # 可以添加更详细的对比分析
                pass
        except:
            pass
    
    # 评估质量
    sample_count = len(samples)
    quality_assessment = assess_quality(field_analysis, sample_count, original_count)
    
    # 生成建议
    recommendations = generate_recommendations(field_analysis, quality_assessment)
    
    # 构建报告
    report = {
        "report_id": generate_report_id(),
        "generated_at": datetime.now().isoformat(),
        "sample_source": args.samples,
        "original_source": args.original or "N/A",
        "statistics": {
            "sample_count": sample_count,
            "original_count": original_count,
            "achievement_rate": round(sample_count / original_count * 100, 2) if original_count > 0 else 0
        },
        "field_analysis": field_analysis,
        "quality_assessment": quality_assessment,
        "recommendations": recommendations
    }
    
    # 保存报告
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(json.dumps({"success": True, "report": args.output}, ensure_ascii=False))


if __name__ == "__main__":
    main()
