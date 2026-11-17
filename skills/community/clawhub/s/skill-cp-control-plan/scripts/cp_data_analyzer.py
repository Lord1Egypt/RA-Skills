#!/usr/bin/env python3
"""
CP控制计划数据分析脚本
功能：导入CSV/Excel数据，提取质量特性，计算统计参数，输出分析结果
"""

import argparse
import json
import sys
from pathlib import Path

try:
    import pandas as pd
    import numpy as np
except ImportError:
    print("ERROR: Missing required packages. Install: pip install pandas numpy openpyxl")
    sys.exit(1)


def validate_data(df):
    """数据验证与清洗"""
    issues = []
    cleaned_df = df.copy()
    
    # 检测缺失值
    missing = cleaned_df.isnull().sum()
    if missing.any():
        issues.append(f"检测到 {missing.sum()} 个缺失值，已自动处理（删除含缺失值的行）")
        cleaned_df = cleaned_df.dropna()
    
    # 检测异常值（3σ原则）
    numeric_cols = cleaned_df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        mean = cleaned_df[col].mean()
        std = cleaned_df[col].std()
        lower_bound = mean - 3 * std
        upper_bound = mean + 3 * std
        outliers = cleaned_df[(cleaned_df[col] < lower_bound) | (cleaned_df[col] > upper_bound)]
        if len(outliers) > 0:
            issues.append(f"列 '{col}' 检测到 {len(outliers)} 个异常值（3σ原则）")
            cleaned_df = cleaned_df[(cleaned_df[col] >= lower_bound) & (cleaned_df[col] <= upper_bound)]
    
    return cleaned_df, issues


def calculate_statistics(df, spec_lower=None, spec_upper=None):
    """计算统计参数"""
    results = []
    
    # 识别数值列作为潜在质量特性
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    for col in numeric_cols:
        data = df[col].dropna()
        if len(data) < 2:
            continue
        
        stats = {
            "characteristic": col,
            "count": int(len(data)),
            "mean": round(float(data.mean()), 4),
            "std": round(float(data.std()), 4),
            "min": round(float(data.min()), 4),
            "max": round(float(data.max()), 4),
            "median": round(float(data.median()), 4),
            "range": round(float(data.max() - data.min()), 4)
        }
        
        # 如果提供了规格限，计算过程能力
        if spec_lower is not None and spec_upper is not None:
            stats["spec_lower"] = spec_lower
            stats["spec_upper"] = spec_upper
            stats["usl"] = spec_upper
            stats["lsl"] = spec_lower
            
            cpu = (stats["mean"] - spec_lower) / (3 * stats["std"]) if stats["std"] > 0 else 0
            cpl = (spec_upper - stats["mean"]) / (3 * stats["std"]) if stats["std"] > 0 else 0
            stats["cp"] = round(min(cpu, cpl) * 2, 4) if stats["std"] > 0 else 0
            
            # CPK计算
            if stats["std"] > 0:
                cpk_upper = (spec_upper - stats["mean"]) / (3 * stats["std"])
                cpk_lower = (stats["mean"] - spec_lower) / (3 * stats["std"])
                stats["cpk"] = round(min(cpk_upper, cpk_lower), 4)
                stats["cpu"] = round(cpk_upper, 4)
                stats["cpl"] = round(cpk_lower, 4)
            else:
                stats["cpk"] = 0
                stats["cpu"] = 0
                stats["cpl"] = 0
            
            # 判断过程能力等级
            if stats["cpk"] >= 1.67:
                stats["capability_level"] = "优秀"
            elif stats["cpk"] >= 1.33:
                stats["capability_level"] = "良好"
            elif stats["cpk"] >= 1.0:
                stats["capability_level"] = "勉强"
            else:
                stats["capability_level"] = "不足"
        else:
            stats["capability_level"] = "未提供规格限"
        
        # 控制限计算（X-bar控制图）
        if len(data) >= 20:
            stats["ucl"] = round(stats["mean"] + 3 * stats["std"], 4)
            stats["lcl"] = round(stats["mean"] - 3 * stats["std"], 4)
            stats["control_limits_calculated"] = True
        else:
            stats["control_limits_calculated"] = False
        
        results.append(stats)
    
    return results


def detect_patterns(df):
    """检测SPC趋势模式"""
    patterns = []
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    for col in numeric_cols:
        data = df[col].dropna().values
        if len(data) < 10:
            continue
        
        # 连续点在中心线同一侧检测
        mean = np.mean(data)
        side_count = 0
        max_side_run = 0
        current_side = None
        
        for val in data:
            if val > mean:
                side = 1
            elif val < mean:
                side = -1
            else:
                side = 0
            
            if side == current_side and side != 0:
                side_count += 1
            else:
                side_count = 1
                current_side = side
            
            max_side_run = max(max_side_run, side_count)
        
        if max_side_run >= 8:
            patterns.append({
                "characteristic": col,
                "pattern_type": "连续偏移",
                "description": f"连续{max_side_run}点在中心线同一侧",
                "severity": "高"
            })
        
        # 趋势检测（连续上升或下降）
        trend_count = 0
        max_trend = 0
        for i in range(1, len(data)):
            if (data[i] > data[i-1]) or (data[i] < data[i-1]):
                trend_count += 1
            else:
                trend_count = 0
            max_trend = max(max_trend, trend_count)
        
        if max_trend >= 6:
            patterns.append({
                "characteristic": col,
                "pattern_type": "趋势",
                "description": f"检测到连续{max_trend}点单调变化",
                "severity": "中"
            })
    
    return patterns


def main():
    parser = argparse.ArgumentParser(description="CP控制计划数据分析脚本")
    parser.add_argument("--input", required=True, help="输入数据文件路径（CSV或Excel）")
    parser.add_argument("--format", choices=["csv", "xlsx"], help="数据格式（csv或xlsx），如未指定则根据文件扩展名自动判断")
    parser.add_argument("--output", required=True, help="输出JSON文件路径")
    parser.add_argument("--spec-lower", type=float, help="规格下限（可选）")
    parser.add_argument("--spec-upper", type=float, help="规格上限（可选）")
    
    args = parser.parse_args()
    
    # 自动判断格式
    if args.format is None:
        input_path = Path(args.input)
        if input_path.suffix.lower() == '.csv':
            args.format = 'csv'
        elif input_path.suffix.lower() in ['.xlsx', '.xls']:
            args.format = 'xlsx'
        else:
            print(f"ERROR: 无法判断文件格式，请使用 --format 参数指定")
            sys.exit(1)
    
    # 读取数据
    try:
        if args.format == "csv":
            df = pd.read_csv(args.input)
        else:
            df = pd.read_excel(args.input)
    except Exception as e:
        print(f"ERROR: 读取文件失败 - {str(e)}")
        sys.exit(1)
    
    # 数据验证
    df_cleaned, validation_issues = validate_data(df)
    
    # 计算统计参数
    spec_lower = args.spec_lower
    spec_upper = args.spec_upper
    
    # 如果未指定规格限，尝试从数据中识别（列名包含LSL/USL等）
    if spec_lower is None:
        for col in df_cleaned.columns:
            if 'lsl' in col.lower() or 'lower' in col.lower():
                spec_lower = float(df_cleaned[col].iloc[0])
                break
    
    if spec_upper is None:
        for col in df_cleaned.columns:
            if 'usl' in col.lower() or 'upper' in col.lower():
                spec_upper = float(df_cleaned[col].iloc[0])
                break
    
    statistics = calculate_statistics(df_cleaned, spec_lower, spec_upper)
    
    # 检测趋势模式
    patterns = detect_patterns(df_cleaned)
    
    # 生成结果
    result = {
        "status": "success",
        "input_file": args.input,
        "data_shape": {"rows": len(df_cleaned), "columns": len(df_cleaned.columns)},
        "validation_issues": validation_issues,
        "characteristics": statistics,
        "patterns_detected": patterns,
        "summary": {
            "total_characteristics": len(statistics),
            "capable_count": sum(1 for s in statistics if s.get("capability_level") == "优秀"),
            "marginal_count": sum(1 for s in statistics if s.get("capability_level") == "勉强"),
            "insufficient_count": sum(1 for s in statistics if s.get("capability_level") == "不足"),
            "average_cpk": round(sum(s.get("cpk", 0) for s in statistics) / len(statistics), 4) if statistics else 0
        }
    }
    
    # 输出结果
    try:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"SUCCESS: 分析结果已保存至 {args.output}")
    except Exception as e:
        print(f"ERROR: 保存结果失败 - {str(e)}")
        sys.exit(1)
    
    # 打印摘要
    print(f"\n=== 分析摘要 ===")
    print(f"数据形状: {result['data_shape']['rows']} 行 x {result['data_shape']['columns']} 列")
    print(f"质量特性数: {result['summary']['total_characteristics']}")
    print(f"过程能力优秀: {result['summary']['capable_count']} 个")
    print(f"过程能力勉强: {result['summary']['marginal_count']} 个")
    print(f"过程能力不足: {result['summary']['insufficient_count']} 个")
    if result['summary']['average_cpk']:
        print(f"平均CPK: {result['summary']['average_cpk']}")
    print(f"检测到趋势: {len(patterns)} 个")


if __name__ == "__main__":
    main()
