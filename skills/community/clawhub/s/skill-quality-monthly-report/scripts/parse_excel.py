#!/usr/bin/env python3
"""
Excel 数据解析脚本

功能：解析 Excel 文件（支持多个 sheet），转换为标准 JSON 格式
依赖：pandas, openpyxl
"""

import pandas as pd
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, Any, List


def parse_excel_file(file_path: str) -> Dict[str, Any]:
    """
    解析 Excel 文件（支持多个 sheet）
    
    返回格式：
    {
        "file_name": "文件名.xlsx",
        "sheets": {
            "sheet1": {
                "name": "Sheet1",
                "data": [...],  # 数据行
                "columns": [...],  # 列名
                "row_count": 10,
                "column_count": 5
            },
            "sheet2": {...}
        }
    }
    """
    excel_path = Path(file_path)
    
    if not excel_path.exists():
        raise FileNotFoundError(f"文件不存在：{file_path}")
    
    print(f"正在解析 Excel 文件：{file_path}")
    
    # 读取所有 sheet
    excel_file = pd.ExcelFile(file_path)
    
    result = {
        "file_name": excel_path.name,
        "sheets": {}
    }
    
    for sheet_name in excel_file.sheet_names:
        print(f"  正在解析 Sheet: {sheet_name}")
        
        # 读取 sheet 数据
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        # 转换为字典列表
        data = df.to_dict('records')
        
        # 处理 NaN 值
        data = [{k: (v if pd.notna(v) else None) for k, v in row.items()} for row in data]
        
        result["sheets"][sheet_name] = {
            "name": sheet_name,
            "data": data,
            "columns": list(df.columns),
            "row_count": len(df),
            "column_count": len(df.columns)
        }
        
        print(f"    - 行数：{len(df)}，列数：{len(df.columns)}")
    
    return result


def parse_multiple_excel_files(file_paths: str) -> List[Dict[str, Any]]:
    """
    解析多个 Excel 文件（逗号分隔）
    
    返回：多个文件的解析结果列表
    """
    files = file_paths.split(",")
    results = []
    
    for file_path in files:
        file_path = file_path.strip()
        if file_path:
            try:
                result = parse_excel_file(file_path)
                results.append(result)
            except Exception as e:
                print(f"警告：解析文件 {file_path} 失败：{e}", file=sys.stderr)
    
    return results


def identify_sheet_type(sheet_data: Dict[str, Any]) -> str:
    """
    识别 sheet 类型
    
    返回：test_cases（测试用例）、defects（缺陷）、work_summary（工作总结）、unknown（未知）
    """
    columns = [col.lower() for col in sheet_data["columns"]]
    
    # 测试用例识别
    if any(keyword in columns for keyword in ['测试用例', 'test_case', '用例数', 'passed', '通过']):
        return "test_cases"
    
    # 缺陷识别
    if any(keyword in columns for keyword in ['缺陷', 'defect', 'bug', '严重级别', 'severity']):
        return "defects"
    
    # 工作总结识别
    if any(keyword in columns for keyword in ['任务', 'task', '工作', 'work', '状态', 'status']):
        return "work_summary"
    
    return "unknown"


def analyze_excel_structure(excel_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    分析 Excel 文件结构，识别各 sheet 的用途
    
    返回：
    {
        "file_name": "文件名.xlsx",
        "structure": {
            "test_cases": {...},
            "defects": {...},
            "work_summary": {...}
        },
        "unknown_sheets": [...]
    }
    """
    result = {
        "file_name": excel_data["file_name"],
        "structure": {},
        "unknown_sheets": []
    }
    
    for sheet_name, sheet_data in excel_data["sheets"].items():
        sheet_type = identify_sheet_type(sheet_data)
        
        if sheet_type != "unknown":
            result["structure"][sheet_type] = {
                "sheet_name": sheet_name,
                "data": sheet_data["data"],
                "row_count": sheet_data["row_count"]
            }
        else:
            result["unknown_sheets"].append({
                "sheet_name": sheet_name,
                "row_count": sheet_data["row_count"]
            })
    
    return result


def convert_to_standard_format(excel_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    将 Excel 数据转换为标准 JSON 格式（用于生成月报）
    
    返回符合 references/data_format.md 规范的格式
    """
    analysis = analyze_excel_structure(excel_data)
    
    standard_format = {
        "month": "待填写",
        "test_cases": {
            "total": 0,
            "passed": 0,
            "failed": 0,
            "skipped": 0
        },
        "defects": {
            "total": 0,
            "by_severity": {
                "critical": 0,
                "high": 0,
                "medium": 0,
                "low": 0
            }
        },
        "work_summary": [],
        "temporary_works": [],
        "pdca_items": [],
        "risks": [],
        "next_month_plan": []
    }
    
    # 解析测试用例数据
    if "test_cases" in analysis["structure"]:
        test_cases_data = analysis["structure"]["test_cases"]["data"]
        if test_cases_data:
            first_row = test_cases_data[0]
            standard_format["test_cases"]["total"] = first_row.get("测试用例数", 0) or first_row.get("total", 0)
            standard_format["test_cases"]["passed"] = first_row.get("通过数", 0) or first_row.get("passed", 0)
            standard_format["test_cases"]["failed"] = first_row.get("失败数", 0) or first_row.get("failed", 0)
            standard_format["test_cases"]["skipped"] = first_row.get("跳过数", 0) or first_row.get("skipped", 0)
    
    # 解析缺陷数据
    if "defects" in analysis["structure"]:
        defects_data = analysis["structure"]["defects"]["data"]
        if defects_data:
            for row in defects_data:
                severity = str(row.get("严重级别", "") or row.get("severity", "")).lower()
                if "critical" in severity or "严重" in severity:
                    standard_format["defects"]["by_severity"]["critical"] += 1
                elif "high" in severity or "高" in severity or "高危" in severity:
                    standard_format["defects"]["by_severity"]["high"] += 1
                elif "medium" in severity or "中" in severity or "中危" in severity:
                    standard_format["defects"]["by_severity"]["medium"] += 1
                elif "low" in severity or "低" in severity or "低危" in severity:
                    standard_format["defects"]["by_severity"]["low"] += 1
            
            standard_format["defects"]["total"] = len(defects_data)
    
    # 解析工作总结数据
    if "work_summary" in analysis["structure"]:
        work_data = analysis["structure"]["work_summary"]["data"]
        if work_data:
            for row in work_data:
                task = {
                    "task": row.get("任务", "") or row.get("task", ""),
                    "status": row.get("状态", "") or row.get("status", ""),
                    "description": row.get("描述", "") or row.get("description", "")
                }
                standard_format["work_summary"].append(task)
    
    return standard_format


def main():
    parser = argparse.ArgumentParser(description='Excel 数据解析工具')
    parser.add_argument('input', nargs='?', help='输入 Excel 文件路径（支持多个文件，逗号分隔）')
    parser.add_argument('--output', help='输出 JSON 文件路径')
    parser.add_argument('--analyze-only', action='store_true', help='仅分析文件结构，不转换为标准格式')
    parser.add_argument('--convert', action='store_true', help='转换为标准 JSON 格式')
    
    args = parser.parse_args()
    
    if not args.input:
        parser.print_help()
        sys.exit(1)
    
    # 解析 Excel 文件
    if "," in args.input:
        excel_results = parse_multiple_excel_files(args.input)
    else:
        excel_results = [parse_excel_file(args.input)]
    
    # 处理结果
    if args.analyze_only:
        # 仅分析结构
        for excel_result in excel_results:
            analysis = analyze_excel_structure(excel_result)
            print(f"\n文件：{analysis['file_name']}")
            print(f"识别到的 Sheet 类型：{list(analysis['structure'].keys())}")
            if analysis['unknown_sheets']:
                print(f"未识别的 Sheet：{[s['sheet_name'] for s in analysis['unknown_sheets']]}")
    
    elif args.convert:
        # 转换为标准格式
        for excel_result in excel_results:
            standard_format = convert_to_standard_format(excel_result)
            
            output_file = args.output
            if not output_file:
                output_file = Path(excel_result["file_name"]).with_suffix('.json')
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(standard_format, f, ensure_ascii=False, indent=2)
            
            print(f"\n✓ 已转换为标准格式：{output_file}")
    
    else:
        # 输出原始解析结果
        output_file = args.output
        if not output_file:
            output_file = Path(excel_results[0]["file_name"]).with_suffix('.json')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(excel_results[0], f, ensure_ascii=False, indent=2)
        
        print(f"\n✓ 解析完成：{output_file}")


if __name__ == "__main__":
    main()
