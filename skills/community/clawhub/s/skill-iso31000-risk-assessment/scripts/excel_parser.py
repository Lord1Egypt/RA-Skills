#!/usr/bin/env python3
"""
Excel 文档解析工具
用于从 Excel 文件中提取风险数据，支持多 sheet 解析
"""

import argparse
import json
import sys
from pathlib import Path
import pandas as pd


def parse_excel(file_path, sheet_name=None):
    """
    解析 Excel 文件，提取风险数据

    Args:
        file_path: Excel 文件路径
        sheet_name: 指定 sheet 名称，None 表示解析所有 sheet

    Returns:
        dict: 包含解析结果的字典
    """
    try:
        # 读取 Excel 文件
        if sheet_name:
            # 读取指定 sheet
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            sheets_data = {sheet_name: df}
        else:
            # 读取所有 sheet
            sheets_data = pd.read_excel(file_path, sheet_name=None)

        result = {
            "status": "success",
            "file_path": str(file_path),
            "total_sheets": len(sheets_data),
            "sheets": {}
        }

        # 遍历每个 sheet
        for sheet_name, df in sheets_data.items():
            sheet_info = {
                "name": sheet_name,
                "total_rows": len(df),
                "total_columns": len(df.columns),
                "columns": list(df.columns),
                "data": []
            }

            # 转换数据为字典列表
            for idx, row in df.iterrows():
                row_dict = {}
                for col in df.columns:
                    value = row[col]
                    # 处理 NaN 值
                    if pd.isna(value):
                        row_dict[col] = None
                    else:
                        row_dict[col] = str(value)
                sheet_info["data"].append(row_dict)

            result["sheets"][sheet_name] = sheet_info

        return result

    except FileNotFoundError:
        return {
            "status": "error",
            "error": "文件不存在",
            "file_path": str(file_path)
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "file_path": str(file_path)
        }


def identify_risk_data(result):
    """
    识别包含风险相关数据的 sheet

    Args:
        result: parse_excel 返回的结果

    Returns:
        list: 包含风险数据的 sheet 名称列表
    """
    risk_keywords = ["风险", "描述", "概率", "可能性", "严重性", "后果", "影响", "措施"]
    risk_sheets = []

    for sheet_name, sheet_info in result["sheets"].items():
        columns = [col.lower() for col in sheet_info["columns"]]
        # 检查是否包含风险相关关键词
        if any(keyword in " ".join(columns) for keyword in risk_keywords):
            risk_sheets.append(sheet_name)

    return risk_sheets


def main():
    parser = argparse.ArgumentParser(description="解析 Excel 文档，提取风险数据")
    parser.add_argument("--file-path", required=True, help="Excel 文件路径")
    parser.add_argument("--sheet-name", help="指定 sheet 名称（可选）")
    parser.add_argument("--identify-risks", action="store_true", help="识别包含风险数据的 sheet")

    args = parser.parse_args()

    # 解析 Excel
    result = parse_excel(args.file_path, args.sheet_name)

    # 如果需要识别风险数据
    if args.identify_risks and result["status"] == "success":
        risk_sheets = identify_risk_data(result)
        result["risk_sheets"] = risk_sheets
        result["risk_sheet_count"] = len(risk_sheets)

    # 输出 JSON 结果
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
