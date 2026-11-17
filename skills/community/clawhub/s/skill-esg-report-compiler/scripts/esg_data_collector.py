#!/usr/bin/env python3
"""
ESG Data Collector - ESG数据收集与整理工具
支持环境(E)、社会(S)、治理(G)三个维度的数据收集与格式化
"""

import argparse
import json
import pandas as pd
from pathlib import Path
from datetime import datetime


# ESG指标定义及默认值
ESG_METRICS = {
    "environmental": {
        "E1": {"name": "温室气体排放", "unit": "吨CO2e", "category": "emissions"},
        "E2": {"name": "能源消耗", "unit": "MWh", "category": "energy"},
        "E3": {"name": "水资源使用", "unit": "立方米", "category": "water"},
        "E4": {"name": "废弃物产生", "unit": "吨", "category": "waste"},
        "E5": {"name": "再生能源使用比例", "unit": "%", "category": "energy"},
    },
    "social": {
        "S1": {"name": "员工总数", "unit": "人", "category": "workforce"},
        "S2": {"name": "女性员工比例", "unit": "%", "category": "diversity"},
        "S3": {"name": "员工培训投入", "unit": "万元", "category": "training"},
        "S4": {"name": "安全事故数", "unit": "起", "category": "safety"},
        "S5": {"name": "社区公益投入", "unit": "万元", "category": "community"},
    },
    "governance": {
        "G1": {"name": "董事会独立性", "unit": "%", "category": "board"},
        "G2": {"name": "女性董事比例", "unit": "%", "category": "diversity"},
        "G3": {"name": "反腐败培训覆盖率", "unit": "%", "category": "ethics"},
        "G4": {"name": " ESG目标达成率", "unit": "%", "category": "targets"},
    }
}


def validate_data_row(row, dimension, metric_id):
    """验证单条数据的有效性"""
    errors = []
    
    if pd.isna(row.get('value')):
        errors.append(f"指标 {metric_id} 缺少数值")
    else:
        try:
            value = float(row['value'])
            # 百分比检查
            if metric_id in ['E5', 'S2', 'G1', 'G2', 'G3', 'G4']:
                if value < 0 or value > 100:
                    errors.append(f"指标 {metric_id} 百分比超出范围(0-100)")
        except ValueError:
            errors.append(f"指标 {metric_id} 数值格式错误")
    
    if not row.get('period'):
        errors.append(f"指标 {metric_id} 缺少报告期")
    
    return errors


def collect_esg_data(input_file, output_file=None):
    """
    收集并整理ESG数据
    
    Args:
        input_file: CSV/Excel输入文件路径
        output_file: JSON输出文件路径
    """
    # 读取数据
    df = pd.read_csv(input_file) if input_file.endswith('.csv') else pd.read_excel(input_file)
    
    # 数据整理结果
    result = {
        "collection_time": datetime.now().isoformat(),
        "total_records": len(df),
        "dimensions": {
            "environmental": {},
            "social": {},
            "governance": {}
        },
        "validation_errors": [],
        "summary": {}
    }
    
    # 按维度分组处理
    for _, row in df.iterrows():
        dimension = row.get('dimension', '').lower()
        metric_id = str(row.get('metric_id', '')).strip()
        period = str(row.get('period', datetime.now().year))
        
        if dimension not in result['dimensions']:
            continue
            
        # 验证数据
        errors = validate_data_row(row, dimension, metric_id)
        result['validation_errors'].extend(errors)
        
        # 存储数据
        if metric_id in ESG_METRICS.get(dimension, {}):
            metric_info = ESG_METRICS[dimension][metric_id]
            result['dimensions'][dimension][metric_id] = {
                "name": metric_info['name'],
                "value": row.get('value'),
                "unit": metric_info['unit'],
                "period": period,
                "notes": row.get('notes', '')
            }
    
    # 生成汇总统计
    for dim in ['environmental', 'social', 'governance']:
        result['summary'][dim] = {
            "metric_count": len(result['dimensions'][dim]),
            "metrics": list(result['dimensions'][dim].keys())
        }
    
    # 输出结果
    output_path = output_file or input_file.replace('.csv', '_collected.json').replace('.xlsx', '_collected.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    return result


def generate_template(output_file='esg_data_template.csv'):
    """生成ESG数据采集模板"""
    template_data = []
    
    for dimension, metrics in ESG_METRICS.items():
        for metric_id, info in metrics.items():
            template_data.append({
                'dimension': dimension,
                'metric_id': metric_id,
                'metric_name': info['name'],
                'unit': info['unit'],
                'period': '',
                'value': '',
                'notes': ''
            })
    
    df = pd.DataFrame(template_data)
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    return output_file


def main():
    parser = argparse.ArgumentParser(description='ESG数据收集与整理工具')
    parser.add_argument('--input', '-i', required=True, help='输入数据文件(CSV/Excel)')
    parser.add_argument('--output', '-o', help='输出JSON文件路径')
    parser.add_argument('--generate-template', '-t', action='store_true', help='生成数据模板')
    
    args = parser.parse_args()
    
    if args.generate_template:
        output = generate_template(args.output or 'esg_data_template.csv')
        result = {"status": "success", "template_file": output}
    else:
        result = collect_esg_data(args.input, args.output)
        result["status"] = "success"
        result["output_file"] = result.get("output_file", "")
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
